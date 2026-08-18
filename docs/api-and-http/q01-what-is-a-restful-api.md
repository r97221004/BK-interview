# Q01: What is a RESTful API, and what are its core principles?

> Tests whether you can name REST's constraints and explain what each one buys you, instead of equating REST with 'JSON over HTTP'.

**Part:** API & HTTP | **Importance:** 10/10 | **Status:** Draft

**New to these terms?** [statelessness](../_glossary.md#statelessness), [load balancer](../_glossary.md#load-balancer), [cdn](../_glossary.md#cdn)

## In One Sentence

REST is a way of designing an API around resources that are named by URLs and acted on with the standard HTTP methods, so any client that speaks HTTP can use it without special tooling.

REST 是一種 API 設計方式：把系統裡的東西當成「資源」，用 URL 命名，再用標準的 HTTP 方法操作，因此任何會講 HTTP 的客戶端都能直接使用，不需要額外的工具。

## Answer Shape

Define REST as an architectural style defined by constraints, not as a data format. Name the six constraints, then spend your time on the three that actually change how you build the service: client-server separation, statelessness, and the uniform interface. Give one concrete URL as an example, and finish by saying what disqualifies an API from being RESTful, because that is where the interviewer is heading.

先把 REST 定義成一種由「約束」構成的架構風格，而不是一種資料格式。把六個約束列出來，然後把時間花在真正會改變實作方式的三個：client-server 分離、無狀態、統一介面。搭配一個具體的 URL 當例子，最後說明什麼樣的 API 不算 RESTful，因為面試官通常就是要往那裡追問。

## Full Spoken Answer

REST is an architectural style for networked applications, defined by six constraints: client-server separation, statelessness, a uniform interface, a layered system, cacheability, and code on demand, which is the only optional one. It is not a protocol and not a data format, which is why returning JSON over HTTP does not by itself make an API RESTful.

REST 是一種網路應用的架構風格，由六個約束定義：client-server 分離、無狀態、統一介面、分層系統、可快取，以及唯一選擇性的 code on demand。它不是協定，也不是資料格式，所以「用 HTTP 回傳 JSON」本身並不會讓一個 API 變成 RESTful。

Three of those constraints do most of the work. Client-server separation means the two sides only share a contract, so the front end and the back end can be rewritten independently. Statelessness means each request carries everything the server needs, so no request depends on what the same client sent earlier. The uniform interface means resources are nouns identified by URLs, and the verbs come from HTTP itself, with their standard meanings: GET reads and changes nothing, PUT replaces and is idempotent, DELETE is idempotent, POST is the one that is not.

其中三個約束承擔了大部分的作用。client-server 分離代表兩邊只共用一份契約，前端和後端可以各自改寫。無狀態代表每個請求都自帶伺服器需要的所有資訊，不依賴同一個客戶端先前送過什麼。統一介面代表資源是用 URL 標示的名詞，動詞則直接沿用 HTTP 本身，而且要遵守它們的標準語意：GET 只讀取、不改變任何東西，PUT 是取代且具冪等性，DELETE 也具冪等性，POST 則是唯一不冪等的。

The remaining constraints are about what sits between the two ends. A layered system means a proxy, a gateway, or a load balancer can be inserted without either side noticing, and cacheability means responses say whether and for how long they may be reused. Those two are why a REST API gets so much infrastructure for free: any CDN and any HTTP proxy already understands the semantics, because they are the protocol's, not yours.

剩下的約束處理的是「中間那一層」。分層系統代表可以在中間插入 proxy、gateway 或 load balancer，而兩端都不會察覺；可快取代表回應要明確表達自己能不能被重複使用、能用多久。這兩點正是 REST API 能免費取得大量基礎設施的原因：任何 CDN、任何 HTTP proxy 都已經看得懂這些語意，因為那是協定的語意，不是你自己發明的。

In practice most APIs called RESTful break at least one constraint, and the honest answer is to say which. Putting verbs in the path such as a create-user route, keeping login state in server memory, or returning a 200 with an error inside the body all break the uniform interface or statelessness. Naming the constraint you knowingly bend, and why, reads far better than claiming full compliance.

實務上大多數自稱 RESTful 的 API 至少違反一個約束，比較誠實的回答是說出違反了哪一個。像是把動詞放進路徑、把登入狀態放在伺服器記憶體裡，或是回傳 200 但把錯誤塞在 body 裡，都違反了統一介面或無狀態。明確講出自己刻意放寬了哪一條、為什麼，會比宣稱完全符合好得多。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| *(first question)* | [All 29 questions](../../README.md) | [Q11: Can you explain the difference between SQL and NoSQL databases?](../databases/q11-sql-vs-nosql.md) |
