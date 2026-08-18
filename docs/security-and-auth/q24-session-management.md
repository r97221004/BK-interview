# Q24: Describe how session management works in web applications.

> Tests whether you can walk the full lifecycle and explain what breaks when a second application server appears.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [jwt](../_glossary.md#jwt), [samesite](../_glossary.md#samesite), [horizontal scaling](../_glossary.md#horizontal-scaling), [load balancer](../_glossary.md#load-balancer), [tls](../_glossary.md#tls)

## In One Sentence

Session management is how the server recognizes the same user across many requests: it creates a record when they log in, gives the client an ID that points at it, looks it up on every request, and destroys it when they leave.

session 管理是伺服器在多次請求之間辨認同一個使用者的方式：登入時建立一筆紀錄、把指向它的 ID 交給客戶端、在每個請求時查出它，並在使用者離開時銷毀它。

## Answer Shape

Walk the lifecycle in order - create, store, transmit, use, end - because the question is asking for a process and the order is the answer. Then answer the follow-up before it is asked: what breaks when a second application server appears, and how the storage choice fixes it. Close on why REST APIs usually reach for tokens instead.

照順序把生命週期走一遍 —— 建立、儲存、傳送、使用、結束 —— 因為這題問的是一個流程，順序本身就是答案。接著在對方問之前先回答追問：當第二台應用伺服器出現時什麼會壞掉，以及儲存方式的選擇怎麼修好它。最後收在為什麼 REST API 通常改用 token。

## Full Spoken Answer

Session management is how the server keeps track of a user across multiple requests. When the user logs in, the backend creates a session and generates a unique session ID for it. The session record holds whatever the server needs to recognize them later - the user ID, their roles, when the session was created, and when it expires.

session 管理是伺服器在多次請求之間追蹤同一個使用者的方式。使用者登入時，後端建立一個 session 並為它產生一個唯一的 session ID。這筆 session 紀錄保存伺服器之後辨認他所需要的一切 —— 使用者 ID、角色、建立時間，以及到期時間。

That record is stored somewhere - in the application's memory, in a database, or in a fast shared store such as Redis. The ID is then sent to the client, almost always in a cookie, which the browser saves and attaches automatically to every later request. On each request the server reads the ID, looks up the matching session, and now knows who is calling. Eventually the session ends: it expires after a timeout, or it is deleted when the user logs out, and the server discards the data.

這筆紀錄會被存在某處 —— 應用程式的記憶體、資料庫，或像 Redis 這樣的快速共用儲存。ID 接著被送給客戶端，幾乎都是放在 cookie 裡，瀏覽器把它存起來並自動附加在之後的每個請求上。每次請求時，伺服器讀出 ID、查出對應的 session，就知道來的是誰了。最後 session 會結束：逾時過期，或在使用者登出時被刪除，伺服器隨即丟棄那份資料。

The detail that separates a textbook answer from a working one is where that record lives. Keeping sessions in the application process works until there are two processes: the load balancer sends the next request to the other instance, the lookup fails, and the user is logged out at random. The fixes are sticky sessions, which pin a user to one instance and lose that user's session whenever it restarts, or a shared store such as Redis, which is the normal answer because it keeps every instance interchangeable and survives a deploy. Alongside that, the cookie should be HttpOnly so scripts cannot read the ID, Secure so it only travels over HTTPS, and SameSite to blunt cross-site requests, and the ID should be regenerated on login so a pre-set ID cannot be fixated.

區分「教科書答案」和「能運作的答案」的細節在於那筆紀錄放在哪裡。把 session 放在應用程式行程裡，在只有一個行程時沒問題；一旦有兩個，load balancer 把下一個請求送到另一台實例、查不到、使用者就被隨機登出了。解法是黏著式 session（把使用者釘在某一台實例上，但那台重啟時該使用者的 session 就沒了），或是共用儲存如 Redis —— 後者是正常答案，因為它讓每台實例都可互換，也能撐過一次部署。除此之外，cookie 應該設 HttpOnly 讓腳本讀不到 ID、設 Secure 讓它只走 HTTPS、設 SameSite 來削弱跨站請求；而且 ID 應該在登入時重新產生，讓事先設定好的 ID 無法被固定利用。

In RESTful APIs the usual choice is a token instead, because REST is meant to be stateless. Rather than storing session data on the server, the client sends a signed token with every request and any instance can verify it on its own. That removes the dependency on a central session store and makes horizontal scaling simpler, at the cost of not being able to revoke a token before it expires - which is exactly the trade discussed under the session-versus-JWT question.

在 RESTful API 中通常改用 token，因為 REST 的設計就是無狀態的。客戶端不再依賴伺服器保存 session 資料，而是每個請求都帶著一個簽章 token，任何一台實例都能獨立驗證。這消除了對中央 session 儲存的依賴，也讓水平擴充更單純，代價是無法在 token 過期前撤銷它 —— 這正是 session 與 JWT 那一題所討論的取捨。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q14: What are the common application scenarios for Redis?](../databases/q14-redis-use-cases.md) | [All 29 questions](../../README.md) | [Q26: What is Cross-Site Request Forgery (CSRF)?](q26-csrf.md) |
