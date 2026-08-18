# Q21: What is the difference between session-based and JWT-based authentication?

> Tests whether you can trade revocation against statelessness, instead of declaring one of them modern and the other legacy.

**Part:** Security & Auth | **Importance:** 10/10 | **Status:** Draft

**New to these terms?** [statelessness](../_glossary.md#statelessness), [cookie](../_glossary.md#cookie), [session](../_glossary.md#session), [samesite](../_glossary.md#samesite), [redis](../_glossary.md#redis)

## In One Sentence

Session-based authentication keeps the user's state on the server and gives the client only an ID, while JWT-based authentication puts the state inside a signed token that the client carries and the server merely verifies.

Session 認證把使用者狀態留在伺服器上，只交給客戶端一個 ID；JWT 認證則把狀態放進一個簽章 token，由客戶端隨身帶著，伺服器只負責驗證。

## Answer Shape

Frame it as one trade rather than two products: where the state lives. Describe each flow in three steps, then state the consequence that follows in each direction - sessions revoke easily but need shared storage, tokens scale freely but cannot be taken back. Finish with the hybrid that most production systems actually run, because declaring one of them the modern choice is the answer that gets pushed back on.

把它定位成「一個取捨」而不是「兩個產品」：狀態放在哪裡。用三個步驟描述各自的流程，接著說出兩邊各自帶來的後果 —— session 容易撤銷但需要共用儲存，token 擴充自如但收不回來。最後帶出多數正式系統實際採用的混合做法，因為宣稱其中一個是「現代做法」正是最容易被反問的答案。

## Full Spoken Answer

With session-based authentication, the server creates a session when the user logs in and stores their information - user ID, roles, expiry - in memory, a database, or a shared store such as Redis. It generates a session ID and returns it to the client, normally in a cookie. On every later request the browser sends that cookie back, and the server looks up the session data by ID. The server is tracking sessions, so this design is stateful.

在 session 認證中，使用者登入時伺服器會建立一個 session，把他的資訊 —— 使用者 ID、角色、到期時間 —— 存在記憶體、資料庫，或像 Redis 這樣的共用儲存裡。伺服器產生一個 session ID 並回傳給客戶端，通常放在 cookie 中。之後的每個請求，瀏覽器都會把那個 cookie 送回來，伺服器再用 ID 查出 session 資料。伺服器需要追蹤 session，所以這個設計是有狀態的。

With JWT-based authentication, the server instead creates a token containing the user's claims - identifier, roles, expiry - and signs it with a secret or a private key. The client stores it and sends it with each request, usually in the authorization header. The server verifies the signature and reads the claims straight out of the token, with no lookup at all. Nothing about the user is stored server-side, so this design is stateless. Worth saying plainly: a JWT is signed, not encrypted, so anyone holding it can read its contents.

在 JWT 認證中，伺服器改為建立一個包含使用者 claims 的 token —— 識別碼、角色、到期時間 —— 並用密鑰或私鑰簽章。客戶端把它存起來，並隨每個請求送出，通常放在 authorization 標頭。伺服器驗證簽章後直接從 token 裡讀出 claims，完全不需要查詢。伺服器端不保存任何使用者資料，所以這個設計是無狀態的。有一點要直說：JWT 是「簽章」而不是「加密」，任何拿到它的人都讀得出裡面的內容。

The consequences fall out of that difference. Sessions are easy to revoke - delete the record and the next request fails - and they let you keep sensitive data server-side where the client never sees it. The cost is that the session store has to be reachable from every instance, so you need sticky routing or a shared store, and that store becomes a dependency on your critical path. Tokens invert both: they scale effortlessly because any instance can verify one alone, which suits distributed systems and microservices, but you cannot take a token back before it expires, and a token stored in local storage is readable by any script that gets injected into the page.

後果就從這個差異推導出來。session 容易撤銷 —— 刪掉紀錄，下一個請求就失敗 —— 而且能把敏感資料留在伺服器端，客戶端永遠看不到。代價是 session 儲存必須讓每台實例都能存取，所以你需要黏著式路由或共用儲存，而那個儲存會變成關鍵路徑上的相依元件。token 則正好相反：它擴充毫不費力，因為任何一台實例都能獨立驗證，很適合分散式系統與微服務；但你無法在 token 過期前把它收回，而且存在 local storage 的 token，會被任何注入頁面的腳本讀走。

In practice most production systems run a hybrid, and saying so is the strongest version of this answer. You issue a short-lived access token, minutes rather than days, so the revocation window stays small, plus a long-lived refresh token that is stored server-side and can be revoked. Keep both in cookies marked HttpOnly, Secure, and SameSite rather than in local storage. That gives you the stateless verification of tokens on the hot path with the revocation of sessions where it matters.

實務上多數正式系統採用混合做法，能講出這一點就是這題最強的答案。你簽發一個短效的 access token —— 以分鐘而非天為單位 —— 讓撤銷的空窗期夠小；再搭配一個存在伺服器端、可以被撤銷的長效 refresh token。兩者都放在標記 HttpOnly、Secure、SameSite 的 cookie 裡，而不是 local storage。這樣你在熱路徑上享有 token 的無狀態驗證，同時在真正需要的地方保有 session 的撤銷能力。

## Quick Reference

| Feature | Session-Based | JWT-Based |
|---|---|---|
| Storage | On the server | On the client |
| Scalability | Harder (server must store sessions) | Easier (stateless) |
| Revocation | Easy | Harder (until token expires) |
| Security | Safer (data stays server-side) | Requires careful handling |
| Typical Use | Web apps with centralized servers | APIs, mobile apps, microservices |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q11: Can you explain the difference between SQL and NoSQL databases?](../databases/q11-sql-vs-nosql.md) | [All 29 questions](../../README.md) | [Q02: Can you describe a typical HTTP request/response cycle?](../api-and-http/q02-http-request-response-cycle.md) |
