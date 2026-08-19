# Q61: How do you choose HTTP status codes and design error responses?

> Tests whether you design errors for the caller rather than for yourself, and whether you know why returning 200 with an error body breaks clients and proxies.

**Part:** API Design & Reliability | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [resource](../_glossary.md#resource), [cache](../_glossary.md#cache), [rate limiting](../_glossary.md#rate-limiting), [message queue](../_glossary.md#message-queue)

## In One Sentence

The status code tells the client which category of thing happened so it can decide what to do without parsing anything, and the body tells a developer which specific thing happened so they can fix it.

狀態碼告訴客戶端「發生的是哪一類事情」，讓它不必解析任何內容就能決定下一步；而 body 告訴開發者「具體是哪一件事」，讓他能把問題修好。

## Answer Shape

Start by sorting outcomes into kinds - bad request, authentication, authorisation, resource state, server failure - and pick the code from the kind, rather than reaching for 200 every time. Spend your detail on the pairs that actually get asked: 401 versus 403, and 400 versus 422 versus 409. Then give the error body its own job: a stable machine-readable code, never a leaked stack trace. Finish with the two mistakes that come up constantly.

先把結果分類 —— 請求本身有問題、認證、授權、資源狀態、伺服器故障 —— 再從分類挑代碼，而不是每次都伸手拿 200。把細節花在真的會被追問的那幾組：401 對 403，以及 400 對 422 對 409。接著給錯誤 body 一份自己的職責：一個穩定的、機器可讀的代碼，而且絕不外洩堆疊追蹤。最後收在兩個一再出現的錯誤。

## Full Spoken Answer

I would not return 200 for everything and put the outcome in the body. I sort what happened into kinds first - is the request itself malformed, is this an authentication problem, an authorisation problem, a conflict with the current state of the resource, or did my server break - and the kind picks the class. 2xx means it worked. 3xx means it lives elsewhere, follow it. 4xx means the request was wrong, so retrying it unchanged will fail again and the caller has to change something. 5xx means the server failed, so the same request might well succeed on a retry. That last split is the one that actually drives client behaviour: a well-built client retries 5xx with backoff and does not retry 4xx at all.

我不會什麼都回 200、再把結果塞在 body 裡。我會先把發生的事分類 —— 是請求本身格式錯誤、是認證問題、是授權問題、是與資源目前狀態衝突，還是我的伺服器爆了 —— 由分類決定 class。2xx 代表成功。3xx 代表東西在別的地方，跟過去。4xx 代表請求本身有問題，原封不動重試還是會失敗，呼叫端必須改點什麼。5xx 代表伺服器出錯，所以同一個請求重試很可能會成功。最後這個切分才是真正驅動客戶端行為的：一個寫得好的客戶端會對 5xx 帶退避重試，對 4xx 則完全不重試。

Within the classes, a small set covers almost everything. 200 for a successful read or update, 201 with a `Location` header when you created something, 202 when you accepted work that finishes later, 204 when there is genuinely nothing to return. On the error side: 400 malformed, 401 not authenticated, 403 not allowed, 404 no such resource, 409 conflict, 422 values invalid, 429 rate limited, 500 for an unexpected server failure, and 503 when the service is temporarily down or overloaded. Do not agonise over the exact number - get the class right, then pick the most specific code you are confident about.

在各分類之內，一小組代碼幾乎涵蓋所有情況。讀取或更新成功用 200；建立了東西用 201 並附上 `Location` 標頭；接受了稍後才完成的工作用 202；真的沒有東西要回傳用 204。錯誤這邊：格式錯誤 400、未通過認證 401、無權限 403、資源不存在 404、衝突 409、值不合法 422、被速率限制 429、伺服器未預期錯誤 500，服務暫時不可用或過載則是 503。不要為了確切數字糾結 —— 先把分類選對，再挑一個你有把握的、最具體的代碼。

Two groups get asked almost every time. First, 401 versus 403, and the shortest way to hold it is as two questions: 401 is "who are you?" and 403 is "I know who you are, but you cannot do this." No token, or an expired one, is 401. Matt is logged in but is not an admin - that is 403. Second, 400 versus 422 versus 409, using one endpoint to keep it concrete. `POST /users` with `{"email": "abc"}` is not a valid email, so that is 400, or 422 if your API reserves 400 for requests that will not even parse. `POST /users` with `{"email": "matt@example.com"}` is perfectly well formed - and if that address is already registered, that is 409, because nothing about the request is wrong; it conflicts with the state the system is already in. That is the line: 400 and 422 mean I cannot make sense of what you sent, 409 means I understood you perfectly and it clashes with reality.

有兩組幾乎每次都會被問。第一組是 401 對 403，記住它最短的方式是兩個問句：401 是「你是誰？」，403 是「我知道你是誰，但你不能做這件事」。沒有 token、或 token 過期，是 401。Matt 已經登入但不是 admin，那是 403。第二組是 400 對 422 對 409，用同一個 endpoint 把它固定住。`POST /users` 帶 `{"email": "abc"}`，這不是合法的 email，所以是 400 —— 如果你的 API 把 400 保留給「根本解析不了」的請求，那就用 422。`POST /users` 帶 `{"email": "matt@example.com"}`，格式完全正確 —— 而如果這個地址已經註冊過了，那是 409，因為請求本身沒有任何問題，它是跟系統目前已經處在的狀態打架。界線就在這：400 和 422 是「我看不懂你送來的東西」，409 是「我完全看懂了，而它跟現實衝突」。

For the body, the thing I care about most is that clients never have to read English to make a decision. A response of `{"error": "Something went wrong"}` tells the caller nothing they can act on. What I return instead is consistently shaped across every endpoint: a stable machine-readable `code` such as `EMAIL_ALREADY_EXISTS`, a human-readable `message`, `details` naming the offending field for validation failures, and a `request_id`. The `code` is the important one, because a client that writes `if (error.message === "A user with this email already exists.")` breaks the day someone improves the wording or ships a second language. Branching on `error.code` lets the backend rewrite and translate messages freely without touching a single client.

至於 body，我最在意的是：客戶端永遠不必讀英文才能做決定。回一句 `{"error": "Something went wrong"}`，呼叫端根本無從處理。我會回的是每個 endpoint 形狀都一致的內容：一個穩定的、機器可讀的 `code`（例如 `EMAIL_ALREADY_EXISTS`）、一則人類看得懂的 `message`、驗證失敗時指出出問題欄位的 `details`，以及一個 `request_id`。其中 `code` 最重要，因為一個寫成 `if (error.message === "A user with this email already exists.")` 的客戶端，會在有人潤飾文案、或上線第二種語言的那天壞掉。改成依 `error.code` 分支，後端就能自由改寫與翻譯訊息，完全不必動到任何一個客戶端。

The other rule is that internal errors never go out as they came in. If the database blows up, the client must not receive `psycopg2.errors.UniqueViolation at user_repository.py line 184` - that hands a stranger your database engine, your table names, and your file layout. Outward it is a 500 with `{"code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "request_id": "req_abc123"}`; inward the real exception and stack trace go to your logs, tagged with that same `req_abc123`. That is what the request ID is for - it is the thread joining what the user saw to what your logs recorded, so a support report can be traced without asking anyone what time it happened.

另一條規則是：內部錯誤絕不原樣送出去。如果資料庫爆了，客戶端不該收到 `psycopg2.errors.UniqueViolation at user_repository.py line 184` —— 那等於把你的資料庫引擎、資料表名稱和程式結構交給一個陌生人。對外是一個 500，內容是 `{"code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "request_id": "req_abc123"}`；對內則把真正的例外與堆疊追蹤寫進你的日誌，並標上同一組 `req_abc123`。request ID 存在的意義就是這個 —— 它是把「使用者看到的畫面」和「你的日誌記下的東西」接起來的那條線，讓一則客服回報可以直接追查，不必先問任何人是幾點發生的。

Two mistakes are worth naming because they show up constantly. Returning 200 with an error inside the body breaks everything downstream that reads only the status line - proxies cache it, monitoring reports a healthy service, and every client has to parse the body to find out whether it worked. And returning 500 for something the caller did wrong turns a client bug into a page for your on-call, which is why validation failures must be 4xx. One security note: 404 and 403 leak different information, so for a resource the caller is not allowed to know exists, 404 is the safer answer. The whole answer in one line: the status code answers "whose fault is this and should I try again," and the body answers "what exactly, so I can fix it" - and the client should be able to act on both without reading a sentence.

有兩個錯誤值得點名，因為它們一再出現。回傳 200 卻把錯誤塞在 body 裡，會弄壞所有只看狀態列的下游 —— proxy 會把它快取起來、監控會回報服務健康，而每個客戶端都得解析 body 才知道到底成功了沒。而把呼叫端的錯誤回成 500，會把客戶端的 bug 變成你的 on-call 告警，這正是為什麼驗證失敗必須是 4xx。一個安全性補充：404 和 403 洩漏的資訊不同，所以對於「呼叫端無權知道其是否存在」的資源，回 404 是比較安全的答案。整題濃縮成一句：狀態碼回答「這是誰的錯、我該不該重試」，body 回答「具體是什麼、我要怎麼修」—— 而客戶端不必讀懂任何一句英文，就該能依這兩者行動。

## Quick Reference

### The codes worth knowing

| Code | Meaning | Use it when |
|---|---|---|
| **200** OK | Succeeded | A read, or an update that returns the new state |
| **201** Created | Resource created | A create; include a `Location` header |
| **202** Accepted | Queued, not done | You handed the work to a queue |
| **204** No Content | Succeeded, nothing to say | A delete, or an update with no useful body |
| **400** Bad Request | Malformed | The body will not parse, or a parameter is the wrong type |
| **401** Unauthorized | Not authenticated | Missing, expired, or invalid credentials |
| **403** Forbidden | Authenticated, not allowed | Valid caller, insufficient permission |
| **404** Not Found | No such resource | Also the safer answer when existence itself is private |
| **409** Conflict | State conflict | Duplicate creation, or a version mismatch |
| **422** Unprocessable Content | Syntax fine, values not | Validation failed on a well-formed request |
| **429** Too Many Requests | Rate limited | Include a `Retry-After` header |
| **500** Internal Server Error | The server broke | Never for something the caller did wrong |
| **503** Service Unavailable | Temporarily down | Overloaded, deploying, or a dependency is out; send `Retry-After` if you can |

### The ones that get confused

Who you are, versus what you may do:

| Code | The question it answers |
|---|---|
| **401** | Who are you? - no token, expired token, bad token |
| **403** | I know who you are, but you cannot do this - logged in, not an admin |
| **404** | There is nothing here - or you are not allowed to know there is |

One `POST /users`, three outcomes:

| Request body | Result | Why |
|---|---|---|
| `{"email": "matt@example.com"}` - new | **201** Created | It worked |
| `{"email": "abc"}` | **400** / **422** | I cannot make sense of what you sent |
| `{"email": "matt@example.com"}` - taken | **409** Conflict | I understood you perfectly; it clashes with reality |

### Error body: the shape to aim for

```jsonc
// Useless - the client cannot act on this
{ "error": "Something went wrong" }

// Useful - branch on code, show message, highlight details, trace by request_id
{
  "code": "EMAIL_ALREADY_EXISTS",
  "message": "A user with this email already exists.",
  "details": { "field": "email" },
  "request_id": "req_abc123"
}
```

Client code should read `error.code`, never `error.message` - the message is free to change or be translated, the code is a contract.

### Out to the caller, down to the log

```jsonc
// Response - 500, and nothing about how the server is built
{
  "code": "INTERNAL_ERROR",
  "message": "An unexpected error occurred.",
  "request_id": "req_abc123"
}
```

```text
# Server log - the real thing, joined by the same id
request_id=req_abc123
psycopg2.errors.UniqueViolation at user_repository.py line 184
<stack trace>
```

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q51: What kind of tests would you write for a new API endpoint?](../testing-and-debugging/q51-testing-a-new-api-endpoint.md) | [All 41 questions](../../README.md) | [Q09: How would you handle file uploads in a web application?](../api-and-http/q09-file-uploads.md) |
