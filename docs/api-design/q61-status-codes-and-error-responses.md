# Q61: How do you choose HTTP status codes and design error responses?

> Tests whether you design errors for the caller rather than for yourself, and whether you know why returning 200 with an error body breaks clients and proxies.

**Part:** API Design & Reliability | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [resource](../_glossary.md#resource), [cache](../_glossary.md#cache), [rate limiting](../_glossary.md#rate-limiting), [message queue](../_glossary.md#message-queue)

## In One Sentence

The status code tells the client which category of thing happened so it can decide what to do without parsing anything, and the body tells a developer which specific thing happened so they can fix it.

狀態碼告訴客戶端「發生的是哪一類事情」，讓它不必解析任何內容就能決定下一步；而 body 告訴開發者「具體是哪一件事」，讓他能把問題修好。

## Answer Shape

Start with the four classes and what each one tells a client to do, because that is the decision the code exists to drive. Then say why the class matters more than the exact number - the caller branches on the class. Give the error body's job separately, and finish with the two mistakes that come up constantly: 200 with an error inside, and 500 for something the client did wrong.

先講四個分類，以及每一類要客戶端做什麼，因為那正是狀態碼存在的目的。接著說明「分類比確切數字更重要」—— 呼叫端是依分類分支的。再單獨講錯誤 body 的職責，最後收在兩個一再出現的錯誤：回 200 卻把錯誤塞在裡面，以及把客戶端的錯誤回成 500。

## Full Spoken Answer

The classes carry the meaning. 2xx means it worked. 3xx means the resource is somewhere else and the client should follow. 4xx means the request was wrong, so retrying it unchanged will fail again and the caller has to fix something. 5xx means the server failed, so the same request might well succeed on a retry. That last distinction is the one that actually drives client behaviour: a well-built client retries 5xx with backoff and does not retry 4xx.

意義是由分類承載的。2xx 代表成功。3xx 代表資源在別的地方，客戶端應該跟過去。4xx 代表請求本身有問題，原封不動重試還是會失敗，呼叫端必須改點什麼。5xx 代表伺服器出錯，所以同一個請求重試很可能會成功。最後這個區分才是真正驅動客戶端行為的：一個寫得好的客戶端會對 5xx 帶退避重試，對 4xx 則不重試。

Within the classes, a small set covers almost everything. 200 for a successful read or update, 201 with a Location header when you created something, 202 when you accepted work that will finish later, 204 when there is genuinely nothing to return. On the error side: 400 for a malformed request, 401 when the caller is not authenticated, 403 when they are authenticated but not allowed, 404 when the resource does not exist, 409 for a conflict such as a duplicate, 422 when the syntax is fine but the values are not, and 429 when they are being rate limited. Do not agonise over the exact number - get the class right, then pick the most specific code you are confident about.

在各分類之內，一小組代碼幾乎涵蓋所有情況。讀取或更新成功用 200；建立了東西用 201 並附上 Location 標頭；接受了稍後才會完成的工作用 202；真的沒有東西要回傳時用 204。錯誤這邊：請求格式錯誤用 400；呼叫端未通過認證用 401；已認證但無權限用 403；資源不存在用 404；發生衝突（例如重複）用 409；語法正確但值不合法用 422；被速率限制用 429。不要為了確切數字糾結 —— 先把分類選對，再挑一個你有把握的、最具體的代碼。

The body is a separate job with a separate audience. The status code is for the machine; the body is for the human debugging the integration. A useful one is consistently shaped across every endpoint and carries a stable machine-readable error code that clients can branch on without string-matching the message, a human-readable message, and for validation failures, per-field detail so the caller can highlight the right input. It should also carry a request ID that matches your logs, so a report of a failure can be traced without asking the user what time it happened.

body 是另一份工作，面向的是另一批讀者。狀態碼是給機器看的，body 是給正在除錯這個串接的人看的。好的錯誤 body 在每個 endpoint 上形狀一致，並帶有一個穩定的、機器可讀的錯誤代碼讓客戶端可以據此分支（而不是去比對訊息字串）、一則人類看得懂的訊息，以及在驗證失敗時逐欄位的細節，讓呼叫端能標示出正確的輸入欄位。它還應該帶上一個與你日誌相符的 request ID，這樣收到失敗回報時就能直接追查，不必先問使用者是幾點發生的。

Two mistakes are worth naming because they show up constantly. Returning 200 with an error inside the body breaks everything downstream that reads only the status line - proxies cache it, monitoring reports a healthy service, and every client has to parse the body to find out whether it worked. And returning 500 for something the caller did wrong turns a client bug into a page for your on-call, which is why validation failures must be 4xx. One security note: 404 and 403 leak different information, so for a resource the caller is not allowed to know exists, 404 is the safer answer.

有兩個錯誤值得點名，因為它們一再出現。回傳 200 卻把錯誤塞在 body 裡，會弄壞所有只看狀態列的下游 —— proxy 會把它快取起來、監控會回報服務健康，而每個客戶端都得解析 body 才知道到底成功了沒。而把呼叫端的錯誤回成 500，會把客戶端的 bug 變成你的 on-call 告警，這正是為什麼驗證失敗必須是 4xx。一個安全性補充：404 和 403 洩漏的資訊不同，所以對於「呼叫端無權知道其是否存在」的資源，回 404 是比較安全的答案。

## Quick Reference

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
| **422** Unprocessable | Syntax fine, values not | Validation failed on a well-formed request |
| **429** Too Many Requests | Rate limited | Include a `Retry-After` header |
| **500** Internal Server Error | The server broke | Never for something the caller did wrong |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q51: What kind of tests would you write for a new API endpoint?](../testing-and-debugging/q51-testing-a-new-api-endpoint.md) | [All 41 questions](../../README.md) | [Q09: How would you handle file uploads in a web application?](../api-and-http/q09-file-uploads.md) |
