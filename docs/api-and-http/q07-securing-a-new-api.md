# Q07: What measures would you take to secure a newly developed API?

> Tests whether you have a layered checklist rather than one favorite mechanism, and whether you can say what each layer does not cover.

**Part:** API & HTTP | **Importance:** 9/10 | **Status:** Complete

**New to these terms?** [endpoint](../_glossary.md#endpoint), [resource](../_glossary.md#resource), [jwt](../_glossary.md#jwt), [prepared statement](../_glossary.md#prepared-statement)

## In One Sentence

I think about API security in five layers - who you are, what you are allowed to touch, whether what you sent is safe, how the API resists abuse, and whether I would notice an attack - and the second layer is the one people skip.

我會把 API 安全拆成五層來想 —— 你是誰、你能碰什麼、你送來的東西安不安全、這個 API 怎麼抵抗濫用、以及出事我看不看得到 —— 而第二層正是最多人漏掉的那一層。

## Answer Shape

Lead with the skeleton, not the keywords: identity, permission, input, protection, monitoring. Then spend most of your time on the first two, because authentication is the layer everyone remembers and authorization is the layer that actually gets breached - give the concrete example there rather than a definition. Move through the remaining three quickly, in one sentence each. Listing nine security terms in a row sounds like reciting a checklist; five layers with one real example sounds like someone who has built it, and it gives the interviewer somewhere obvious to dig.

開場給骨架，不要給關鍵字：身分、權限、輸入、防護、監控。接著把大部分時間花在前兩層，因為認證是人人都記得的那層，授權才是真正會被打穿的那層 —— 在這裡給具體例子，而不是給定義。剩下三層各用一句話快速帶過。一口氣列九個安全名詞聽起來像在背清單；五層搭配一個真實例子，聽起來像真的做過，而且讓面試官有明顯的地方可以往下追問。

## Full Spoken Answer

I do not think of API security as one feature, I think of it in layers. The first is identity - who you are. Every protected endpoint has to verify the caller, typically with a JWT, or with OAuth 2.0 and OpenID Connect when a third party is acting on a user's behalf.

我不會把 API 安全當成某一個功能，而是分層來想。第一層是身分 —— 你是誰。每個受保護的 endpoint 都必須驗證呼叫者，通常用 JWT，或在第三方代表使用者行動時用 OAuth 2.0 搭配 OpenID Connect。

The second layer is permission, and this is the one that matters more. A valid token does not mean you may touch this particular record. Take GET /users/123/orders - your JWT can be perfectly valid and still not entitle you to user 123's orders, so the handler has to check ownership of that specific resource, not just that someone is logged in. Skipping this is broken object level authorization, or IDOR, and it is first in the OWASP API Security Top 10 precisely because the endpoint looks correct in review.

第二層是權限，而且這層更重要。token 有效不代表你可以碰這一筆資料。以 GET /users/123/orders 為例 —— 你的 JWT 可以完全合法，卻仍然沒有資格看 user 123 的訂單，所以處理函式必須檢查這筆特定資源的歸屬，而不是只確認「有人登入了」。漏掉這一層就是 broken object level authorization，也就是 IDOR，它排在 OWASP API Security Top 10 第一名，正是因為這種 endpoint 在程式碼審查時看起來完全正常。

The third layer is input. I validate everything at the boundary and bind it to an explicit schema rather than handing the payload to my model, so a caller cannot set a field I never meant to expose, and I use parameterized queries so input can never become part of a SQL command. The fourth is protection: HTTPS only, secrets like database passwords and API keys injected from the environment or a secret manager instead of being hard-coded, and rate limiting so the API survives abuse or an unexpected spike.

第三層是輸入。我會在邊界驗證所有東西，並把它綁定到一份明確的 schema，而不是把整包 payload 交給 model，這樣呼叫端就無法設定我從沒打算開放的欄位；同時使用參數化查詢，讓輸入永遠不可能變成 SQL 命令的一部分。第四層是防護：只走 HTTPS；資料庫密碼、API key 這類密鑰從環境變數或 secret manager 注入，而不是寫死在程式裡；再加上速率限制，讓 API 撐得住濫用或非預期的流量尖峰。

The last layer is monitoring, because every control above it can fail quietly. I log authentication failures, authorization denials, and rate-limit hits with enough structure to alert on, so repeated failures or an unusual access pattern surface while there is still time to respond. So the shape I keep in my head is: who you are, what you can access, whether the input is safe, how abuse is contained, and whether abnormal behaviour would be noticed.

最後一層是監控，因為上面每一道防護都可能靜默失效。我會把認證失敗、授權拒絕和觸發速率限制的事件記成有結構的日誌以便告警，讓連續失敗或異常存取模式在還來得及反應時就浮現出來。所以我腦子裡記的骨架是：你是誰、你能存取什麼、輸入安不安全、濫用怎麼被擋住，以及異常行為會不會被發現。

## Quick Reference

### The skeleton to memorise

**Identity → Permission → Input → Protection → Monitoring**

| Layer | The question it answers | What you say |
|---|---|---|
| **Identity** | Who are you? | JWT, or OAuth with OpenID Connect for third-party access |
| **Permission** | Are you allowed to touch *this*? | `GET /users/123/orders` - a valid token is not entitlement to user 123's data. Check ownership per object (IDOR / BOLA) |
| **Input** | Is what you sent safe? | Validate at the boundary, bind to an explicit schema (stops mass assignment), parameterized queries |
| **Protection** | How does the API resist abuse? | HTTPS only, secrets from a secret manager, rate limiting |
| **Monitoring** | Would I notice an attack? | Log auth failures, authz denials, rate-limit hits - and alert on them |

Spend your time on the first two. Identity is the layer everyone remembers;
permission is the layer that actually gets breached.

## Interview Version

> I do not think of API security as one feature, I think of it in five layers. The first is identity - who you are. Every protected endpoint verifies the caller, typically with a JWT, or with OAuth 2.0 and OpenID Connect when a third party acts on a user's behalf. The second layer is permission, and it is the one that matters more and the one people skip. A valid token does not mean you may touch this particular record: on GET /users/123/orders your JWT can be perfectly valid and still not entitle you to user 123's orders, so the handler has to check ownership of that specific resource, not just that someone is logged in. Skipping it is broken object level authorization, or IDOR, and it is first in the OWASP API Security Top 10 precisely because the endpoint looks correct in review. The third layer is input: validate everything at the boundary and bind it to an explicit schema rather than handing the payload to your model, so a caller cannot set a field you never meant to expose, and use parameterised queries so input can never become part of a SQL command. The fourth is protection: HTTPS only, secrets injected from the environment or a secret manager instead of hard-coded, and rate limiting so the API survives abuse or a spike. The fifth is monitoring, because every control above it can fail quietly - log authentication failures, authorisation denials, and rate-limit hits with enough structure to alert on, so an unusual access pattern surfaces while there is still time to respond.

面試時可回答：我不會把 API 安全當成單一功能，我把它想成五層。第一層是身分 —— 你是誰。每個受保護的 endpoint 都要驗證呼叫者，通常用 JWT；當有第三方代表使用者行動時，就用 OAuth 2.0 與 OpenID Connect。第二層是權限，這一層更重要，而且正是大家會跳過的那一層。有一個有效的 token，不代表你就可以碰這一筆特定的紀錄：在 GET /users/123/orders 上，你的 JWT 可以完全有效，卻仍然無權取得 user 123 的訂單，所以 handler 必須檢查對那個特定 resource 的所有權，而不只是檢查「有人登入了」。跳過這一步就是 broken object level authorization（也就是 IDOR），它排在 OWASP API Security Top 10 的第一位，正因為這種 endpoint 在 code review 時看起來完全正確。第三層是輸入：在邊界驗證所有東西，並綁定到一個明確的 schema，而不是把 payload 直接交給你的模型，這樣呼叫端就無法設定你從未打算開放的欄位；同時使用參數化查詢，讓輸入永遠不可能變成 SQL 指令的一部分。第四層是防護：只走 HTTPS、機密從環境變數或 secret manager 注入而不是寫死在程式碼裡，以及速率限制，讓 API 撐得過濫用或突發流量。第五層是監控，因為上面每一道控制都可能無聲地失效 —— 把認證失敗、授權拒絕和觸發速率限制的事件記成有結構、可以拿來告警的日誌，讓異常的存取模式在還來得及反應時就浮現出來。

The sentence to remember is: **A valid token says who you are, never what you may touch - checking ownership of that specific record is the layer people skip.**

最值得記：**有效的 token 只說明你是誰，從不說明你可以碰什麼 —— 檢查對那一筆紀錄的所有權，正是大家會跳過的那一層。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q04: Explain statelessness in HTTP and how it impacts backend services.](q04-http-statelessness.md) | [All 47 questions](../../README.md) | [Q17: Explain database transactions and isolation levels.](../databases/q17-transactions-and-isolation-levels.md) |
