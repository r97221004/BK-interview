# Q21: What is the difference between session-based and JWT-based authentication?

> Tests whether you can trade revocation against statelessness, instead of declaring one of them modern and the other legacy.

**Part:** Security & Auth | **Importance:** 10/10 | **Status:** Complete

**New to these terms?** [cookie](../_glossary.md#cookie), [csrf](../_glossary.md#csrf), [samesite](../_glossary.md#samesite), [xss](../_glossary.md#xss), [microservices](../_glossary.md#microservices)

## In One Sentence

Session-based authentication keeps the user's state on the server and gives the client only an ID, while JWT-based authentication puts the state inside a signed token that the client carries and the server merely verifies.

Session 認證把使用者狀態留在伺服器上，只交給客戶端一個 ID；JWT 認證則把狀態放進一個簽章 token，由客戶端隨身帶著，伺服器只負責驗證。

## Answer Shape

Frame it as one trade rather than two products: where the state lives. Describe each flow in three steps, then state the consequence that follows in each direction - sessions revoke easily but need shared storage, tokens scale freely but cannot be taken back. Finish with the hybrid that most production systems actually run, because declaring one of them the modern choice is the answer that gets pushed back on.

把它定位成「一個取捨」而不是「兩個產品」：狀態放在哪裡。用三個步驟描述各自的流程，接著說出兩邊各自帶來的後果 —— session 容易撤銷但需要共用儲存，token 擴充自如但收不回來。最後帶出多數正式系統實際採用的混合做法，因為宣稱其中一個是「現代做法」正是最容易被反問的答案。

## Full Spoken Answer

With session-based authentication, the server creates a session when the user logs in and stores their information - user ID, roles, expiry - in memory, a database, or a shared store such as Redis. It generates a session ID and returns it to the client, normally in a cookie. On every later request the browser sends that cookie back, and the server looks up the session data by ID. The server is tracking sessions, so this design is stateful.

在 session 認證中，使用者登入時伺服器會建立一個 session，把他的資訊 —— 使用者 ID、角色、到期時間 —— 存在記憶體、資料庫，或像 Redis 這樣的共用儲存裡。伺服器產生一個 session ID 並回傳給客戶端，通常放在 cookie 中。之後的每個請求，瀏覽器都會把那個 cookie 送回來，伺服器再用 ID 查出 session 資料。伺服器需要追蹤 session，所以這個設計是有狀態的。

With JWT-based authentication, the server instead creates a token containing the user's claims - identifier, roles, expiry - and signs it with a secret or a private key. The client stores it and sends it with each request, usually in the authorization header. The server verifies the signature and reads the claims straight out of the token, with no lookup at all. Nothing about the user is stored server-side, so this design is stateless. Worth saying plainly: a JWT is signed, not encrypted, so anyone holding it can read its contents. And the signature is only worth what the verification is: the token's own header names the algorithm, so a library that trusts that header lets an attacker set it to none, or swap RS256 for HS256 and sign with the public key everyone already has. Pin the algorithm on the server instead of reading it out of the token.

在 JWT 認證中，伺服器改為建立一個包含使用者 claims 的 token —— 識別碼、角色、到期時間 —— 並用密鑰或私鑰簽章。客戶端把它存起來，並隨每個請求送出，通常放在 authorization 標頭。伺服器驗證簽章後直接從 token 裡讀出 claims，完全不需要查詢。伺服器端不保存任何使用者資料，所以這個設計是無狀態的。有一點要直說：JWT 是「簽章」而不是「加密」，任何拿到它的人都讀得出裡面的內容。而簽章的價值完全取決於驗證做得如何：token 自己的 header 就寫著要用哪個演算法，所以一個信任這個 header 的函式庫，會讓攻擊者把它改成 none，或是把 RS256 換成 HS256、拿人人都有的公鑰去簽。演算法要由伺服器端寫死，而不是從 token 裡讀出來。

The consequences fall out of that difference. Sessions are easy to revoke - delete the record and the next request fails - and they let you keep sensitive data server-side where the client never sees it. The cost is that the session store has to be reachable from every instance, so you need sticky routing or a shared store, and that store becomes a dependency on your critical path. Tokens invert both: they scale effortlessly because any instance can verify one alone, which suits distributed systems and microservices, but you cannot take a token back before it expires, and a token stored in local storage is readable by any script that gets injected into the page. They also travel heavier: a session ID is a few dozen bytes, while a token carrying claims is routinely several hundred, and that rides along on every single request.

後果就從這個差異推導出來。session 容易撤銷 —— 刪掉紀錄，下一個請求就失敗 —— 而且能把敏感資料留在伺服器端，客戶端永遠看不到。代價是 session 儲存必須讓每台實例都能存取，所以你需要黏著式路由或共用儲存，而那個儲存會變成關鍵路徑上的相依元件。token 則正好相反：它擴充毫不費力，因為任何一台實例都能獨立驗證，很適合分散式系統與微服務；但你無法在 token 過期前把它收回，而且存在 local storage 的 token，會被任何注入頁面的腳本讀走。它們的體積也比較重：session ID 只有幾十個位元組，而帶著 claims 的 token 動輒好幾百，而且每一個請求都要跟著送。

In practice most production systems run a hybrid, and saying so is the strongest version of this answer. You issue a short-lived access token, minutes rather than days, so the revocation window stays small, plus a long-lived refresh token that is stored server-side and can be revoked. Keep both in cookies marked HttpOnly, Secure, and SameSite rather than in local storage. That move is a trade rather than a free win: a cookie is out of reach of an injected script, but the browser sends it automatically, which is exactly what CSRF exploits - SameSite is the attribute that shuts that door again. That gives you the stateless verification of tokens on the hot path with the revocation of sessions where it matters. One line to remember the whole trade: sessions are a phone number you can cancel, tokens are a signed letter you can't un-send.

實務上多數正式系統採用混合做法，能講出這一點就是這題最強的答案。你簽發一個短效的 access token —— 以分鐘而非天為單位 —— 讓撤銷的空窗期夠小；再搭配一個存在伺服器端、可以被撤銷的長效 refresh token。兩者都放在標記 HttpOnly、Secure、SameSite 的 cookie 裡，而不是 local storage。這個轉換是取捨而不是白吃的午餐：cookie 讓注入的腳本讀不到，但瀏覽器會自動把它送出去，而這正是 CSRF 所利用的——SameSite 就是把那扇門重新關上的屬性。這樣你在熱路徑上享有 token 的無狀態驗證，同時在真正需要的地方保有 session 的撤銷能力。一句話記住整個取捨：session 像一支可以停話的電話號碼，token 像一封已經簽好、寄出去就收不回來的信。

## Quick Reference

### The trade, row by row

| | Session | JWT |
|---|---|---|
| Where the state lives | On the server, keyed by the session ID | Inside the token, in the client's hands |
| What the client holds | An opaque ID that means nothing on its own | A readable signed document - base64, not encrypted |
| Cost per request | One lookup in the session store | One signature check, no I/O |
| Added to every request | A few dozen bytes | Several hundred bytes of claims |
| Revoking one user | Delete the record; the next request fails | Not possible before expiry without a server-side list |
| Scaling out | The store must be reachable from every instance, and sits on the critical path | Any instance verifies alone; nothing is shared |
| What breaks it | The session store goes down | The signing key leaks, or the algorithm is not pinned |

### Where to keep the token

| Stored in | Readable by an injected script? | Sent automatically cross-site? |
|---|---|---|
| `localStorage` | **Yes** - any XSS on the page reads it | No |
| Cookie without `HttpOnly` | **Yes** | **Yes** - CSRF is available |
| Cookie: `HttpOnly; Secure; SameSite=Lax` | No | No |

Only the last row answers no twice, which is the whole reason it is the recommendation.

### Pinning the algorithm

The attack in the answer is a one-line difference, using PyJWT:

```python
# Vulnerable: the token gets to say how it is verified
header = jwt.get_unverified_header(token)
claims = jwt.decode(token, key, algorithms=[header["alg"]])

# Safe: the server decides, and a token claiming anything else is rejected
claims = jwt.decode(token, key, algorithms=["RS256"])
```

## Interview Version

> With session-based authentication the server creates a session at login and stores the user's information - ID, roles, expiry - in memory, a database, or a shared store such as Redis. It returns a session ID, normally in a cookie; on every later request the browser sends it back and the server looks the session up. The server is tracking sessions, so it is stateful. With JWT-based authentication the server instead creates a token containing the claims and signs it, the client sends it with each request, and the server verifies the signature and reads the claims straight out of the token with no lookup at all - stateless. Worth saying plainly: a JWT is signed, not encrypted, so anyone holding it can read it; and the signature is only worth what the verification is, because the token's own header names the algorithm, so a library that trusts that header lets an attacker set it to none - pin the algorithm on the server instead. The consequences follow. Sessions are easy to revoke, delete the record and the next request fails, and sensitive data stays server-side; the cost is that the store must be reachable from every instance and becomes a dependency on your critical path. Tokens invert both: any instance verifies one alone, which suits distributed systems, but you cannot take a token back before it expires, and one in local storage is readable by any injected script. In practice most production systems run a hybrid, and saying so is the strongest version of this answer: a short-lived access token so the revocation window stays small, plus a long-lived refresh token stored server-side that can be revoked, both in cookies marked HttpOnly, Secure, and SameSite.

面試時可回答：在 session 認證中，伺服器在登入時建立一個 session，把使用者的資訊 —— ID、角色、到期時間 —— 存在記憶體、資料庫，或像 Redis 這樣的共用儲存裡。它回傳一個 session ID，通常放在 cookie 裡；之後每個請求瀏覽器都會把它送回來，伺服器再據此查出那個 session。伺服器在追蹤 session，所以它是有狀態的。在 JWT 認證中，伺服器改為建立一個裝著 claim 的 token 並簽章，客戶端每個請求都帶著它，伺服器驗證簽章、直接從 token 裡讀出 claim，完全不需要查詢 —— 這是無狀態的。有一點要明講：JWT 是「簽章」不是「加密」，所以任何拿到它的人都讀得懂它；而簽章的價值完全取決於驗證的品質，因為 token 自己的標頭寫著使用哪個演算法，所以一個信任那個標頭的函式庫，會讓攻擊者把它設成 none —— 正確做法是在伺服器端把演算法釘死，而不是從 token 裡讀。後果由此推導。session 容易撤銷，刪掉紀錄下一個請求就失敗，而且敏感資料留在伺服器端；代價是那個儲存必須讓每台實例都連得到，並且變成你關鍵路徑上的一個依賴。token 則把兩者反過來：任何實例都能自己驗證一個 token，適合分散式系統；但你沒辦法在 token 過期前把它收回，而放在 local storage 裡的 token，任何被注入的腳本都讀得到。實務上大多數正式系統跑的是混合方案，把這點講出來是這題最強的版本：一個短效的 access token 讓撤銷窗口保持很小，加上一個存在伺服器端、可以撤銷的長效 refresh token，兩者都放在標記了 HttpOnly、Secure、SameSite 的 cookie 裡。

The sentence to remember is: **Sessions are a phone number you can cancel; tokens are a signed letter you cannot un-send.**

最值得記：**session 是一組你可以停用的電話號碼；token 是一封你寄出去就收不回來的簽章信件。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q16: What is a database index, and how do you work out why a query is slow?](../databases/q16-indexes-and-slow-queries.md) | [All 41 questions](../../README.md) | [Q04: Explain statelessness in HTTP and how it impacts backend services.](../api-and-http/q04-http-statelessness.md) |
