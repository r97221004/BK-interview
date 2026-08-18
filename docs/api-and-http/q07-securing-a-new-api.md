# Q07: What measures would you take to secure a newly developed API?

> Tests whether you have a layered checklist rather than one favorite mechanism, and whether you can say what each layer does not cover.

**Part:** API & HTTP | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [cookie](../_glossary.md#cookie), [session](../_glossary.md#session), [jwt](../_glossary.md#jwt), [cors](../_glossary.md#cors), [prepared statement](../_glossary.md#prepared-statement)

## In One Sentence

Securing an API means layering several controls: prove who the caller is, check what they are allowed to touch, encrypt the connection, validate everything they send, and cap how much they can send.

保護一個 API 是把多層防護疊起來：確認呼叫者是誰、檢查他能碰哪些資源、加密連線、驗證他送來的所有東西，並限制他能送多少。

## Answer Shape

Answer as an ordered checklist rather than a favorite technique, because breadth is what is being scored here. Separate authentication from authorization explicitly, since conflating them is the most common miss. Then cover transport, input, and abuse limits, and finish with the operational layer that tells you when a control has already failed.

用一份有順序的檢查清單回答，而不是講你最喜歡的那一招，因為這題評的是廣度。務必明確區分認證與授權，因為把兩者混為一談是最常見的漏洞。接著涵蓋傳輸、輸入與濫用限制，最後補上維運層 —— 那是在某道防線已經被突破時告訴你的東西。

## Full Spoken Answer

Start by separating the two questions that get merged. Authentication answers who the caller is, using a session cookie, an API key, a signed token such as a JWT, or OAuth 2.0 when a third party acts on a user's behalf. Authorization answers what that caller may do, and it has to be checked per object, not just per route. An endpoint that verifies the token but then returns any record whose identifier is in the path is authenticated and still completely broken.

先把兩個常被混在一起的問題分開。認證回答的是「呼叫者是誰」，做法有 session cookie、API key、像 JWT 這樣的簽章 token，或在第三方代表使用者行動時使用 OAuth 2.0。授權回答的是「這個呼叫者可以做什麼」，而且必須逐一物件檢查，不能只檢查路由。一個驗證了 token、卻把路徑上任何 ID 對應的資料都回傳出去的 endpoint，是通過認證但完全失守的。

Then secure the transport. Serve everything over HTTPS, redirect plain HTTP to it, and send HSTS so the browser refuses to downgrade. TLS stops an attacker on the network from reading or modifying traffic, including the token in the authorization header, which is why it is not optional even for an internal service. It says nothing about who the caller is, so it never substitutes for authentication.

接著保護傳輸層。全部走 HTTPS，把純 HTTP 轉導過去，並送出 HSTS 讓瀏覽器拒絕降級。TLS 阻止網路上的攻擊者讀取或竄改流量，包括 authorization 標頭裡的 token，這也是為什麼即使是內部服務也不能省略。但它完全不說明呼叫者是誰，所以永遠不能拿來取代認證。

Next, treat every incoming value as hostile. Validate types, lengths, ranges, and allowed values at the boundary and reject rather than coerce. Use parameterized queries so input can never become part of a SQL command, and encode output for the context it is rendered into. If a browser calls the API from another origin, configure CORS with an explicit allowlist of origins rather than a wildcard, and remember it constrains browsers only.

再來，把每一個進來的值都當成有敵意的。在邊界驗證型別、長度、範圍和允許值，並且選擇拒絕而不是自動轉換。使用參數化查詢，讓輸入永遠不可能變成 SQL 命令的一部分，並依照輸出所在的情境做編碼。如果瀏覽器會從其他來源呼叫這個 API，就用明確的白名單設定 CORS，不要用萬用字元，同時記得它只約束瀏覽器。

Finally, limit and observe. Rate limiting per key or per user contains credential stuffing, scraping, and accidental retry storms, and it is the cheapest control on this list. Keep secrets out of the code and out of the image, rotate them, and log authentication failures, authorization denials, and rate-limit hits with enough structure to alert on. Those logs are how you find out a control failed while you still have time to respond.

最後是限制與觀察。以金鑰或使用者為單位的速率限制可以遏止憑證填充、爬取和意外的重試風暴，而且是這份清單上最便宜的一道防護。把密鑰留在程式碼與映像檔之外、定期輪替，並把認證失敗、授權拒絕和觸發速率限制的事件記錄成有結構的日誌以便告警。這些日誌是你在還來得及反應時，發現某道防護已經失效的方式。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q04: Explain statelessness in HTTP and how it impacts backend services.](q04-http-statelessness.md) | [All 37 questions](../../README.md) | [Q17: Explain database transactions and isolation levels.](../databases/q17-transactions-and-isolation-levels.md) |
