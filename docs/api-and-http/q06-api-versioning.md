# Q06: How do you approach API versioning in your projects?

> Tests whether you can change a live API without breaking clients, and whether you know versioning is a cost to be avoided when possible.

**Part:** API & HTTP | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [status code](../_glossary.md#status-code), [microservices](../_glossary.md#microservices)

## In One Sentence

API versioning means serving more than one version of your contract at the same time, so you can change the API without breaking the clients that were built against the old one.

API 版本控制指的是同時提供多個版本的契約，讓你可以修改 API，而不會弄壞那些照著舊版寫成的客戶端。

## Answer Shape

Start with why a version exists at all, and make the point that most changes should not need one - adding an optional field is not a breaking change. Then compare the two mechanisms you would actually use, URL and header, with a clear recommendation for each audience. Finish with the operational half, because promising to keep an old version alive is easy and retiring it is the hard part.

先說明為什麼會需要版本，並強調大多數改動其實不該需要版本 —— 新增一個選擇性欄位並不是破壞性變更。接著比較你實際會採用的兩種機制，URL 與標頭，並針對不同受眾各給一個明確建議。最後補上維運的那一半，因為承諾維持舊版很容易，真正困難的是把它下線。

## Full Spoken Answer

Versioning is about changing an API without breaking existing clients. The first question is always whether a new version is needed at all, because adding an optional field, adding a new endpoint, or accepting a new value are backwards compatible and need nothing. A version is for breaking changes: removing or renaming a field, tightening validation, or changing what a status code means.

版本控制的目的是在不弄壞既有客戶端的前提下修改 API。第一個要問的永遠是「真的需要新版本嗎」，因為新增選擇性欄位、新增 endpoint、或接受一個新的值都是向後相容的，什麼都不需要做。版本是為破壞性變更而存在的：刪除或重新命名欄位、加嚴驗證，或改變某個狀態碼的意義。

The first mechanism puts the version in the URL: `/api/v1/users` today, `/api/v2/users` once you need to break the contract. It is completely visible: you can see the version in a log line, a browser address bar, and a support ticket, and the gateway can route each version to a different backend without reading the body. The cost is route sprawl and duplicated handlers, and it is the right default for public APIs with clients you do not control.

第一種機制把版本放在 URL 裡：現在是 `/api/v1/users`，需要打破契約時就變成 `/api/v2/users`。它完全可見：在日誌、瀏覽器網址列、客服工單上都看得到版本，而且 gateway 不需要讀 body 就能把不同版本路由到不同後端。代價是路由數量膨脹、處理函式重複，它適合作為公開 API 的預設做法，因為那些客戶端不在你掌控之中。

The second puts the version in a custom request header instead, like `api-version: 2`, so the URL stays clean (`/api/users` either way) and one handler can branch internally on the requested version. It is easier to evolve because a client sets the header once in its shared HTTP layer instead of updating every path. The cost is that the version becomes invisible during debugging, and a client that forgets the header silently gets the default. That trade is usually acceptable inside a system where you own both sides. In one line: URL versioning is what you show a stranger; header versioning is what you agree with a teammate.

第二種把版本放在自訂的請求標頭裡，例如 `api-version: 2`，URL 保持乾淨（不管哪個版本都是 `/api/users`），而且同一個處理函式可以在內部依照被要求的版本分支。它比較好演進，因為客戶端只要在共用的 HTTP 層設定一次標頭，而不必逐一更新每條路徑。代價是除錯時看不到版本，而且忘了帶標頭的客戶端會靜默地拿到預設版本。在兩端都由你掌控的系統內部，這個取捨通常是可以接受的。濃縮成一句：URL 版本是你給陌生人看的，標頭版本是你跟隊友之間的默契。

The part that actually decides whether versioning works is operational. Version the contract as a whole rather than each endpoint separately, or clients end up tracking a matrix. Publish a deprecation window with a date, announce it in a response header so client teams see it in their own logs, and track per-version traffic so you can prove the old one is unused before you remove it. Without that last step you never retire anything and every version lives forever.

真正決定版本控制成不成功的是維運面。把整份契約當成一個版本，而不是每個 endpoint 各自編版本，否則客戶端最後要追蹤一個版本矩陣。公布帶有日期的棄用期，並在回應標頭裡宣告，讓客戶端團隊在自己的日誌就能看到；同時追蹤各版本的流量，這樣你才能在移除之前證明舊版已經沒人使用。少了最後這一步，你永遠不會真的下線任何東西，每個版本都會永遠活著。

## Quick Reference

| Feature | URL-based Versioning | Header-based Versioning |
|---|---|---|
| **How version is specified** | In the URL path (e.g., `/api/v1/users`) or query param (`/api/users?v=1`) | In a custom HTTP header (e.g., `api-version: 1`) |
| **Visibility** | Version is visible to developers and easy to debug | Version is hidden in headers, less visible |
| **Routing** | Easy to route requests to different backend versions automatically | Requires logic in the backend to read the header and route requests |
| **Code duplication risk** | Higher — each version often needs a separate handler | Lower — can handle multiple versions in one endpoint with conditional logic |
| **Client-side management** | Slightly harder if many endpoints need updates | Easier — update header once for multiple requests |
| **Best use case** | Public APIs, external clients | Internal APIs, microservices |
| **Pros** | Clear, simple, easy to test/debug | Clean URLs, easier to evolve versions internally |
| **Cons** | Can lead to many routes and code duplication | Less visible, requires backend logic for version handling |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q05: What are the benefits and drawbacks of RESTful APIs?](q05-rest-benefits-and-drawbacks.md) | [All 41 questions](../../README.md) | [Q08: What is the difference between a REST API and a WebSocket?](q08-rest-vs-websocket.md) |
