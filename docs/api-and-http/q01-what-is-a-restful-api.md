# Q01: What is a RESTful API, and what are its core principles?

> Tests whether you can name REST's constraints and explain what each one buys you, instead of equating REST with 'JSON over HTTP'.

**Part:** API & HTTP | **Importance:** 10/10 | **Status:** Complete

**New to these terms?** [idempotent](../_glossary.md#idempotent), [statelessness](../_glossary.md#statelessness), [status code](../_glossary.md#status-code), [load balancer](../_glossary.md#load-balancer), [cdn](../_glossary.md#cdn)

## In One Sentence

REST is a way of designing an API around resources that are named by URLs and acted on with the standard HTTP methods, so any client that speaks HTTP can use it without special tooling.

REST 是一種 API 設計方式：把系統裡的東西當成「資源」，用 URL 命名，再用標準的 HTTP 方法操作，因此任何會講 HTTP 的客戶端都能直接使用，不需要額外的工具。

## Answer Shape

Define REST as an architectural style defined by constraints, not as a data format. Name the six constraints, then spend your time on the three that actually change how you build the service: client-server separation, statelessness, and the uniform interface. Give one concrete URL as an example, and finish by saying what disqualifies an API from being RESTful, because that is where the interviewer is heading.

先把 REST 定義成一種由「約束」構成的架構風格，而不是一種資料格式。把六個約束列出來，然後把時間花在真正會改變實作方式的三個：client-server 分離、無狀態、統一介面。搭配一個具體的 URL 當例子，最後說明什麼樣的 API 不算 RESTful，因為面試官通常就是要往那裡追問。

## Full Spoken Answer

REST is an architectural style for networked applications, defined by six constraints: client-server separation, statelessness, a uniform interface, a layered system, cacheability, and code on demand, which is the only optional one. It is not a protocol and not a data format, which is why returning JSON over HTTP does not by itself make an API RESTful.

REST 是一種網路應用的架構風格，由六個約束定義：client-server 分離、無狀態、統一介面、分層系統、可快取，以及唯一選擇性的 code on demand。它不是協定，也不是資料格式，所以「用 HTTP 回傳 JSON」本身並不會讓一個 API 變成 RESTful。

Three of those constraints do most of the work. Client-server separation means the two sides only share a contract, so the front end and the back end can be rewritten independently. Statelessness means each request carries everything the server needs, so no request depends on what the same client sent earlier. The uniform interface means resources are nouns identified by URLs, and the verbs come from HTTP itself, with their standard meanings: `GET /users/123` reads that one user and changes nothing, `PUT /users/123` replaces it, `DELETE /users/123` removes it, and all three are idempotent because sending them twice leaves the same state behind. POST and PATCH are the ones that are not, which is why a retried POST can create a second order.

其中三個約束承擔了大部分的作用。client-server 分離代表兩邊只共用一份契約，前端和後端可以各自改寫。無狀態代表每個請求都自帶伺服器需要的所有資訊，不依賴同一個客戶端先前送過什麼。統一介面代表資源是用 URL 標示的名詞，動詞則直接沿用 HTTP 本身，而且要遵守它們的標準語意：`GET /users/123` 只讀取那一位使用者、不改變任何東西，`PUT /users/123` 整份取代，`DELETE /users/123` 刪除，這三個都具冪等性，因為送兩次留下的狀態是一樣的。不冪等的是 POST 和 PATCH，這也是為什麼重送一次 POST 可能會多建立一筆訂單。

The remaining constraints are about what sits between the two ends. A layered system means a proxy, a gateway, or a load balancer can be inserted without either side noticing, and cacheability means responses say whether and for how long they may be reused. Those two are why a REST API gets so much infrastructure for free: any CDN and any HTTP proxy already understands the semantics, because they are the protocol's, not yours.

剩下的約束處理的是「中間那一層」。分層系統代表可以在中間插入 proxy、gateway 或 load balancer，而兩端都不會察覺；可快取代表回應要明確表達自己能不能被重複使用、能用多久。這兩點正是 REST API 能免費取得大量基礎設施的原因：任何 CDN、任何 HTTP proxy 都已經看得懂這些語意，因為那是協定的語意，不是你自己發明的。

In practice most APIs called RESTful break at least one constraint, and the honest answer is to say which. Putting verbs in the path such as a create-user route, keeping login state in server memory, or returning a 200 with an error inside the body all break the uniform interface or statelessness. The one almost everyone skips is HATEOAS, the part of the uniform interface that says a response should carry links to what the client can do next, so the client discovers the API instead of hardcoding its URLs; hardly any JSON API does this, which is what Richardson's maturity model means by stopping at level two. Naming the constraint you knowingly bend, and why, reads far better than claiming full compliance.

實務上大多數自稱 RESTful 的 API 至少違反一個約束，比較誠實的回答是說出違反了哪一個。像是把動詞放進路徑、把登入狀態放在伺服器記憶體裡，或是回傳 200 但把錯誤塞在 body 裡，都違反了統一介面或無狀態。而幾乎每個人都略過的是 HATEOAS：它屬於統一介面的一部分，要求回應要帶上「接下來可以做什麼」的連結，讓客戶端靠探索使用 API，而不是把 URL 寫死；幾乎沒有 JSON API 做到這件事，用 Richardson 成熟度模型來說就是停在 level 2。明確講出自己刻意放寬了哪一條、為什麼，會比宣稱完全符合好得多。

## Quick Reference

The six constraints, and what each one buys you:

| Constraint | What it requires | What you get |
|---|---|---|
| Client-server | The two sides share only the contract | Front end and back end evolve separately |
| Stateless | Every request carries all the context it needs | Any instance can serve any request |
| Uniform interface | Its four parts: resources identified by URLs, acted on through representations, self-descriptive messages, and links to what is next (HATEOAS) | Any HTTP client works without custom tooling |
| Layered system | No side may assume it is talking to the origin | Proxies, gateways, load balancers drop in unnoticed |
| Cacheable | Responses declare whether and how long they may be reused | CDNs and proxies absorb reads for free |
| Code on demand *(optional)* | The server may ship executable code to the client | Rarely used; the one constraint you can ignore |

Method semantics, the part of the uniform interface interviewers actually probe:

| Method | Safe | Idempotent | Typical REST use |
|---|---|---|---|
| `GET` | yes | yes | Read a resource — `GET /users/123` |
| `HEAD` | yes | yes | The headers a `GET` would return, without the body |
| `POST` | no | **no** | Create a subordinate resource — `POST /users` |
| `PUT` | no | yes | Replace a resource wholesale — `PUT /users/123` |
| `PATCH` | no | **no** | Partially update a resource |
| `DELETE` | no | yes | Remove a resource — `DELETE /users/123` |

*Safe* means the request is read-only; *idempotent* means repeating it leaves the same state, which is what makes a retry safe. `PATCH` can be made idempotent by design, but the method does not promise it.

Richardson's maturity model, the usual follow-up:

| Level | What the API does |
|---|---|
| 0 | One URL, one verb — HTTP as a tunnel for RPC |
| 1 | Each resource gets its own URL, but the method carries no meaning — the verb is in the path, or everything is a `POST` |
| 2 | HTTP methods and status codes carry their standard meanings — where most real APIs sit |
| 3 | Responses link to the next available actions (HATEOAS) |

## Interview Version

> REST is an architectural style for networked applications, not a protocol and not a data format - which is why returning JSON over HTTP does not by itself make an API RESTful. It is defined by six constraints, and three of them do most of the work. Client-server separation means the two sides share only a contract, so either can be rewritten independently. Statelessness means every request carries everything the server needs, so no request depends on what the same client sent earlier. The uniform interface means resources are nouns identified by URLs and the verbs come from HTTP itself with their standard meanings: GET /users/123 reads and changes nothing, PUT replaces, DELETE removes, and all three are idempotent, while POST and PATCH are not - which is why a retried POST can create a second order. The other constraints, a layered system and cacheability, are what let you insert a proxy or a CDN without either end noticing, because those components already understand the semantics: they are the protocol's, not yours. In practice most APIs called RESTful break at least one constraint, and the honest answer names which one. The one almost everyone skips is HATEOAS, so I would say where I knowingly bend the rules and why, rather than claim full compliance.

面試時可回答：REST 是一種網路應用的架構風格，不是協定也不是資料格式 —— 這正是為什麼「用 HTTP 回 JSON」本身並不會讓一個 API 變成 RESTful。它由六個 constraint 定義，其中三個做了大部分的工作。client-server 分離代表兩邊只共享一份合約，所以任一邊都能獨立改寫。statelessness 代表每個請求都自帶伺服器需要的一切，沒有任何請求依賴同一個客戶端先前送過什麼。uniform interface 代表 resource 是用 URL 指名的名詞，而動詞來自 HTTP 本身、並帶著它們的標準語意：GET /users/123 是讀取、不改變任何東西，PUT 是取代，DELETE 是移除，這三個都是 idempotent，而 POST 和 PATCH 不是 —— 這也是為什麼重試一次 POST 可能會建立第二筆訂單。其餘的 constraint（layered system 與 cacheability）則讓你能插入 proxy 或 CDN 而兩端都不會察覺，因為那些元件本來就懂這套語意：那是協定的語意，不是你的。實務上大多數被稱為 RESTful 的 API 至少違反一條 constraint，誠實的答案是講出違反的是哪一條。幾乎所有人都跳過的是 HATEOAS，所以我會說明自己在哪裡刻意彎了規則、為什麼，而不是宣稱完全合規。

The sentence to remember is: **REST is a set of constraints, not JSON over HTTP - the nouns live in the URL and the verbs belong to HTTP.**

最值得記：**REST 是一組約束，不是「用 HTTP 回 JSON」—— 名詞放在 URL 裡，動詞交給 HTTP。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| *(first question)* | [All 51 questions](../../README.md) | [Q02: Can you describe a typical HTTP request/response cycle?](q02-http-request-response-cycle.md) |
