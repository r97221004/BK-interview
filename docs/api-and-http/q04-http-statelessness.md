# Q04: Explain statelessness in HTTP and how it impacts backend services.

> Tests whether you understand that statelessness is a protocol property that pushes state management into your design, not a claim that applications have no state.

**Part:** API & HTTP | **Importance:** 9/10 | **Status:** Complete

**New to these terms?** [tcp](../_glossary.md#tcp), [cookie](../_glossary.md#cookie), [jwt](../_glossary.md#jwt), [horizontal scaling](../_glossary.md#horizontal-scaling), [load balancer](../_glossary.md#load-balancer)

## In One Sentence

HTTP is stateless, meaning the server keeps no memory of a client between requests, so every request has to carry whatever context it needs on its own.

HTTP 是無狀態的，代表伺服器在兩次請求之間不會記得任何一個客戶端，所以每個請求都必須自己帶著它需要的所有脈絡。

## Answer Shape

State the rule first and be precise that it is the protocol that is stateless, not your application. Then show where the state has to go instead - cookies, a session store, or a token - and finish with the payoff, which is that any instance can serve any request. That last point is what connects this question to scaling, and it is where the interviewer usually goes next.

先把規則講清楚，並且精確指出無狀態的是「協定」，不是你的應用程式。接著說明狀態改放到哪裡去了 —— cookie、session store，或 token —— 最後帶出它的好處：任何一台實例都能服務任何一個請求。最後這點正是這題與擴充性的連結，也是面試官接著會追的方向。

## Full Spoken Answer

HTTP is stateless: every request is independent, and the server does not automatically know who the client is or what happened in the previous request. Two requests arriving one second apart from the same browser look, to the protocol, like two unrelated strangers. That is a property of the protocol, not a claim that applications have no state - plainly, it's not that your app has no memory, it's that HTTP refuses to be the one holding it, so someone else has to. Nor is it undone by connection reuse: keeping one TCP connection open for several exchanges is a transport optimisation, and the server still remembers nothing about the user between them.

HTTP 是無狀態的：每個請求彼此獨立，伺服器不會自動知道對方是誰，也不知道上一個請求發生了什麼。同一個瀏覽器相隔一秒送出的兩個請求，在協定眼中就像兩個素不相識的陌生人。這是協定的性質，並不是說應用程式沒有狀態 —— 說白了，不是你的應用沒有記憶，是 HTTP 拒絕當那個記事本，所以狀態得換個地方放。它也不會被連線重用推翻：讓同一條 TCP 連線承載多次往返只是傳輸層的最佳化，伺服器在這幾次之間依然不記得使用者任何事。

So if you need login state, a shopping cart, or user preferences, you have to manage that state explicitly. The usual options are a cookie holding a session ID that points at server-side session data, a signed token such as a JWT that carries the claims inside the request itself, or state kept entirely on the client, which only works if it is signed - anything the client holds unsigned is something the client can rewrite, starting with its own role. In every case the request arrives self-describing, because the protocol will not describe it for you.

因此如果你需要登入狀態、購物車或使用者偏好，就必須自己明確管理狀態。常見做法有三種：用 cookie 存一個指向伺服器端 session 資料的 session ID、用像 JWT 這種簽章 token 把 claims 直接帶在請求裡，或是把狀態完全放在客戶端——但這只有在簽章過的前提下才成立，客戶端手上任何沒簽章的東西都是它可以改寫的，從自己的角色開始改。無論哪一種，請求抵達時都必須自我描述，因為協定不會替你描述。

The payoff is that any instance can serve any request - provided the state really did leave the process. Put sessions in one server's memory and you have taken it back: that user is now pinned to the machine that happened to serve them, and loses their session the moment it restarts. With the state in a shared store or in the request itself, nothing is pinned to the machine that handled the previous call, so you can put ten identical servers behind a load balancer, restart one during a deploy, or add three more during a traffic surge without breaking a single in-flight user. That property is what makes horizontal scaling straightforward, and it is why the constraint is worth accepting.

它的報酬是：任何一台實例都能服務任何一個請求——前提是狀態真的離開了行程。把 session 放進某一台伺服器的記憶體裡，等於把這個報酬收回去了：那位使用者從此被綁在剛好服務到他的那台機器上，而且那台機器一重啟，他的 session 就沒了。當狀態放在共用儲存、或直接放在請求裡時，才真的沒有東西被綁在處理上一次呼叫的那台機器上，所以你可以在 load balancer 後面放十台一模一樣的伺服器、在部署時重啟其中一台，或在流量暴增時再加三台，而不會影響任何一個進行中的使用者。這個性質讓水平擴充變得直接，也正是這個約束值得接受的原因。

The cost is that the context is repaid on every request. Credentials are re-verified, the token or session lookup happens again, and payloads are slightly larger. Cached lookups and short-lived tokens keep that cheap, but it is a real trade: statelessness buys elasticity and pays for it in repeated work per request.

代價是脈絡必須在每個請求上重新償還一次。憑證要重新驗證、token 或 session 查詢要再做一次，payload 也會稍微變大。用快取和短效 token 可以把成本壓低，但這確實是一個取捨：無狀態換來的是彈性，付出的是每個請求都要重做的那些工作。

## Quick Reference

### Where the state goes, and what it costs you

The protocol will not hold it, so every design picks one of these. The column
that matters is the third: it is the one that decides whether the payoff of
statelessness actually arrives.

| State lives in | Survives an instance restart | Needs sticky routing | Client can read it | Client can forge it |
|---|---|---|---|---|
| The server process's memory | No | **Yes** | No | No |
| A shared store (Redis, a database) | Yes | No | No | No |
| A signed token in the request | Yes, nothing to lose | No | Yes - signed, not encrypted | No, while the key holds |
| An unsigned cookie or field | Yes | No | Yes | **Yes** |

Only the middle two rows give you interchangeable instances without handing
the user anything they can read. The last row is the one that looks like the
others and is not: [Q21](../security-and-auth/q21-session-vs-jwt-authentication.md)
on what a signature does, [Q24](../security-and-auth/q24-session-management.md)
on why the first row logs people out at random.

## Interview Version

> HTTP is stateless: every request is independent, and the server does not automatically know who the client is or what happened in the previous request. Two requests arriving a second apart from the same browser look, to the protocol, like two unrelated strangers. That is a property of the protocol, not a claim that applications have no state - it is not that your app has no memory, it is that HTTP refuses to be the one holding it, so someone else has to. Connection reuse does not undo it either: keeping a TCP connection open is a transport optimisation, and the server still remembers nothing between exchanges. So login state, a cart, or preferences have to be managed explicitly - a cookie holding a session ID that points at server-side data, a signed token such as a JWT carrying the claims in the request, or state on the client, which only works if it is signed, because anything the client holds unsigned is something the client can rewrite, starting with its own role. The payoff is that any instance can serve any request, provided the state really did leave the process: put sessions in one server's memory and you have taken it back, pinning that user to that machine. With state in a shared store or in the request, you can put ten servers behind a load balancer, restart one during a deploy, or add three during a surge without breaking an in-flight user. The cost is that the context is repaid on every request - credentials re-verified, the lookup done again - so statelessness buys elasticity and pays for it in repeated work.

面試時可回答：HTTP 是無狀態的：每個請求都獨立，伺服器不會自動知道客戶端是誰、上一個請求發生了什麼。同一個瀏覽器相隔一秒送來的兩個請求，在協定眼中就像兩個毫無關係的陌生人。這是協定的性質，不是在說應用程式沒有狀態 —— 不是你的應用沒有記憶，而是 HTTP 拒絕當那個負責記住的人，所以得由別人來記。連線重用也不會改變這一點：把一條 TCP 連線開著是傳輸層的最佳化，伺服器在兩次交換之間仍然什麼都不記得。所以登入狀態、購物車、偏好設定都必須明確管理 —— 用一個裝著 session ID 的 cookie 指向伺服器端資料、用像 JWT 這樣的簽章 token 把 claim 帶在請求裡，或是把狀態完全放在客戶端（這只有在有簽章時才成立，因為客戶端手上任何沒簽章的東西，客戶端都能改寫，從它自己的角色開始改）。回報是：任何一台實例都能服務任何請求 —— 前提是狀態真的離開了行程。把 session 放進某一台伺服器的記憶體，就等於把它收了回來，那位使用者從此被釘在剛好服務他的那台機器上。狀態放在共用儲存或請求本身，你就能在 load balancer 後面放十台伺服器、在部署時重啟其中一台、或在流量高峰時再加三台，而不會弄壞任何一個進行中的使用者。代價是每個請求都要重付一次情境成本 —— 憑證重新驗證、查詢重做一次 —— 所以 statelessness 買到的是彈性，付出的是重複的工。

The sentence to remember is: **It is not that your app has no memory - it is that HTTP refuses to hold it, so any instance can serve any request.**

最值得記：**不是你的應用沒有記憶，而是 HTTP 拒絕替你記 —— 於是任何一台實例都能服務任何請求。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q21: What is the difference between session-based and JWT-based authentication?](../security-and-auth/q21-session-vs-jwt-authentication.md) | [All 51 questions](../../README.md) | [Q07: What measures would you take to secure a newly developed API?](q07-securing-a-new-api.md) |
