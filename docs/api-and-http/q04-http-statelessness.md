# Q04: Explain statelessness in HTTP and how it impacts backend services.

> Tests whether you understand that statelessness is a protocol property that pushes state management into your design, not a claim that applications have no state.

**Part:** API & HTTP | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [cookie](../_glossary.md#cookie), [jwt](../_glossary.md#jwt), [cache](../_glossary.md#cache), [horizontal scaling](../_glossary.md#horizontal-scaling), [load balancer](../_glossary.md#load-balancer)

## In One Sentence

HTTP is stateless, meaning the server keeps no memory of a client between requests, so every request has to carry whatever context it needs on its own.

HTTP 是無狀態的，代表伺服器在兩次請求之間不會記得任何一個客戶端，所以每個請求都必須自己帶著它需要的所有脈絡。

## Answer Shape

State the rule first and be precise that it is the protocol that is stateless, not your application. Then show where the state has to go instead - cookies, a session store, or a token - and finish with the payoff, which is that any instance can serve any request. That last point is what connects this question to scaling, and it is where the interviewer usually goes next.

先把規則講清楚，並且精確指出無狀態的是「協定」，不是你的應用程式。接著說明狀態改放到哪裡去了 —— cookie、session store，或 token —— 最後帶出它的好處：任何一台實例都能服務任何一個請求。最後這點正是這題與擴充性的連結，也是面試官接著會追的方向。

## Full Spoken Answer

HTTP is stateless: every request is independent, and the server does not automatically know who the client is or what happened in the previous request. Two requests arriving one second apart from the same browser look, to the protocol, like two unrelated events. That is a property of the protocol, not a claim that applications have no state.

HTTP 是無狀態的：每個請求彼此獨立，伺服器不會自動知道對方是誰，也不知道上一個請求發生了什麼。同一個瀏覽器相隔一秒送出的兩個請求，在協定眼中就是兩個互不相關的事件。這是協定的性質，並不是說應用程式沒有狀態。

So if you need login state, a shopping cart, or user preferences, you have to manage that state explicitly. The usual options are a cookie holding a session ID that points at server-side session data, a signed token such as a JWT that carries the claims inside the request itself, or state kept entirely on the client. In every case the request arrives self-describing, because the protocol will not describe it for you.

因此如果你需要登入狀態、購物車或使用者偏好，就必須自己明確管理狀態。常見做法有三種：用 cookie 存一個指向伺服器端 session 資料的 session ID、用像 JWT 這種簽章 token 把 claims 直接帶在請求裡，或是把狀態完全放在客戶端。無論哪一種，請求抵達時都必須自我描述，因為協定不會替你描述。

The payoff is that any instance can serve any request. Nothing is pinned to the machine that handled the previous call, so you can put ten identical servers behind a load balancer, restart one during a deploy, or add three more during a traffic surge without breaking a single in-flight user. That property is what makes horizontal scaling straightforward, and it is why the constraint is worth accepting.

它的報酬是：任何一台實例都能服務任何一個請求。沒有東西被綁在處理上一次呼叫的那台機器上，所以你可以在 load balancer 後面放十台一模一樣的伺服器、在部署時重啟其中一台，或在流量暴增時再加三台，而不會影響任何一個進行中的使用者。這個性質讓水平擴充變得直接，也正是這個約束值得接受的原因。

The cost is that the context is repaid on every request. Credentials are re-verified, the token or session lookup happens again, and payloads are slightly larger. Cached lookups and short-lived tokens keep that cheap, but it is a real trade: statelessness buys elasticity and pays for it in repeated work per request.

代價是脈絡必須在每個請求上重新償還一次。憑證要重新驗證、token 或 session 查詢要再做一次，payload 也會稍微變大。用快取和短效 token 可以把成本壓低，但這確實是一個取捨：無狀態換來的是彈性，付出的是每個請求都要重做的那些工作。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q02: Can you describe a typical HTTP request/response cycle?](q02-http-request-response-cycle.md) | [All 29 questions](../../README.md) | [Q07: What measures would you take to secure a newly developed API?](q07-securing-a-new-api.md) |
