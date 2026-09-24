# Q05: What are the benefits and drawbacks of RESTful APIs?

> Tests whether you can criticize the style you use daily, and name the cases where REST is the wrong tool.

**Part:** API & HTTP | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [rest](../_glossary.md#rest), [status code](../_glossary.md#status-code), [websocket](../_glossary.md#websocket), [horizontal scaling](../_glossary.md#horizontal-scaling), [cdn](../_glossary.md#cdn)

## In One Sentence

REST gives you scalability and a vocabulary that every HTTP tool already understands, at the cost of fetching the wrong amount of data and having to keep old contracts alive as the API changes.

REST 帶來的是擴充性，以及一套所有 HTTP 工具都已經看得懂的共同語彙；代價是取回的資料量常常不剛好，而且 API 演進時必須讓舊契約繼續活著。

## Answer Shape

Split the answer cleanly in two and do not let the benefits run long, because the interviewer is really listening for whether you can criticize what you use daily. Give three benefits with the mechanism behind each, then three drawbacks with a concrete symptom, and finish by naming a case where you would choose something other than REST.

把回答乾淨地切成兩半，而且優點不要講太久，因為面試官真正在聽的是你能不能批評自己每天在用的東西。先講三個優點並附上背後的機制，再講三個缺點並各配一個具體症狀，最後說出一個你會選擇 REST 以外方案的情境。

## Full Spoken Answer

The main benefits come from three constraints. Statelessness means the server stores nothing between requests, so instances are interchangeable and horizontal scaling is straightforward. The uniform interface means standard methods and status codes, so proxies, caches, and monitoring understand your traffic without being told anything about your domain. And client-server separation means the two sides evolve independently as long as the contract holds.

主要的好處來自三個約束。無狀態代表伺服器在請求之間不保存任何東西，因此實例可以互換，水平擴充很直接。統一介面代表使用標準方法和狀態碼，所以 proxy、快取和監控系統不需要知道你的領域知識就能理解你的流量。client-server 分離則代表只要契約不變，兩邊就能各自演進。

Two more benefits follow from being ordinary HTTP. Responses can be marked cacheable, so a CDN or a reverse proxy absorbs repeated reads before they ever reach your application. And any client that can make an HTTP request can consume the API, which means no shared runtime, no generated stubs, and no language coupling between the two sides.

另外兩個好處來自「它就是普通的 HTTP」。回應可以被標記為可快取，因此 CDN 或反向 proxy 會在重複的讀取抵達你的應用程式之前就先吸收掉。而且任何能發出 HTTP 請求的客戶端都能使用這個 API，代表兩端不需要共用執行環境、不需要產生 stub，也沒有語言上的耦合。

The drawbacks are just as concrete. Over-fetching and under-fetching are the common ones: `GET /users/42` always returns the full user object - name, address, billing history, everything - even when the mobile screen only needs to show the name, so it downloaded forty fields to use one. Go the other way and a screen that needs a user plus their last five orders has to make two separate round trips, because REST has no built-in way to say "and also fetch this related thing." There is also no standard error format, only the status code, so every team invents its own error body and clients cannot handle failures generically.

缺點同樣具體。過度取得與取得不足是最常見的：`GET /users/42` 永遠回傳完整的 user 物件 —— 名字、地址、帳單記錄，全部都在 —— 即使手機畫面只需要顯示名字，也是下載了四十個欄位卻只用了一個。反過來，如果一個畫面需要使用者資料加上他最近五筆訂單，就得分兩次來回，因為 REST 沒有內建的方式說「順便也把這個關聯的東西撈回來」。此外沒有標準的錯誤格式，只有狀態碼，於是每個團隊都自己發明錯誤 body，客戶端無法用通用的方式處理失敗。

The rest are costs of evolution and of HTTP's own shape. Changing a contract means running two versions for a deprecation window, which is real maintenance. Operations that are not create, read, update, or delete, such as a multi-step transaction or a bulk job, are awkward to model as resources. And statelessness means every request repeats its authentication and context. When a client needs to choose its own payload shape, GraphQL fits better; when two services need low-latency streaming, gRPC or a WebSocket does.

其餘的缺點來自演進成本和 HTTP 本身的形狀。改變契約意味著在棄用期內同時維護兩個版本，這是真實的維護負擔。不屬於新增、讀取、更新、刪除的操作 —— 例如多步驟交易或批次工作 —— 用資源來建模會很彆扭。而無狀態則代表每個請求都要重複做認證和脈絡建立。當客戶端需要自己決定 payload 形狀時，GraphQL 更適合；當兩個服務之間需要低延遲串流時，gRPC 或 WebSocket 更適合。

## Interview Version

> The benefits come from three constraints. Statelessness means the server stores nothing between requests, so instances are interchangeable and horizontal scaling is straightforward. The uniform interface means standard methods and status codes, so proxies, caches, and monitoring understand your traffic without knowing anything about your domain. Client-server separation means the two sides evolve independently as long as the contract holds. Two more follow from being ordinary HTTP: responses can be marked cacheable, so a CDN absorbs repeated reads before they reach your application, and any client that can make an HTTP request can consume the API - no shared runtime, no generated stubs, no language coupling. The drawbacks are just as concrete. Over-fetching and under-fetching are the common ones: GET /users/42 returns the full user object even when the screen only needs the name, so you downloaded forty fields to use one; go the other way and a screen needing a user plus their last five orders makes two round trips, because REST has no way to say "and also fetch this related thing". There is no standard error format either, only the status code, so every team invents its own error body. Then there are the costs of evolution: changing a contract means running two versions for a deprecation window, operations that are not CRUD are awkward to model as resources, and every request repeats its authentication. When a client needs to choose its own payload shape, GraphQL fits better; when two services need low-latency streaming, gRPC or a WebSocket does.

面試時可回答：好處來自三個 constraint。statelessness 代表伺服器在請求之間什麼都不存，所以實例可以互換、水平擴展很直接。uniform interface 代表標準的方法與狀態碼，所以 proxy、快取和監控完全不需要知道你的領域知識就能理解你的流量。client-server 分離代表只要合約還在，兩邊就能各自演進。另外兩個好處來自「它就是普通的 HTTP」：回應可以被標記為可快取，於是 CDN 在重複讀取抵達你的應用之前就把它們吸收掉；而任何能發出 HTTP 請求的客戶端都能使用這個 API —— 不需要共用執行環境、不需要產生的 stub、兩邊沒有語言上的耦合。缺點同樣具體。over-fetching 和 under-fetching 是最常見的：GET /users/42 會回傳完整的 user 物件，即使畫面只需要顯示名字，於是你下載了四十個欄位只為了用一個；反過來，一個需要使用者外加他最近五筆訂單的畫面得跑兩趟，因為 REST 沒有內建方式可以說「順便把這個關聯的東西也抓來」。錯誤格式也沒有標準，只有狀態碼，所以每個團隊都自己發明一套錯誤 body。接著是演進的成本：改合約意味著要在一段淘汰期內同時跑兩個版本；不屬於 CRUD 的操作很難用 resource 模型表達；而每個請求都要重做一次認證。當客戶端需要自己決定 payload 的形狀時，GraphQL 更合適；當兩個服務之間需要低延遲串流時，gRPC 或 WebSocket 更合適。

The sentence to remember is: **REST buys you every HTTP tool for free, and charges you in round trips and old contracts you have to keep alive.**

最值得記：**REST 讓你免費得到整套 HTTP 工具，收的錢是多跑的來回，和你得繼續養著的舊合約。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q03: What is an API endpoint?](q03-what-is-an-api-endpoint.md) | [All 47 questions](../../README.md) | [Q06: How do you approach API versioning in your projects?](q06-api-versioning.md) |
