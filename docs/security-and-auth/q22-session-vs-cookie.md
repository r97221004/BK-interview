# Q22: What is the difference between a session and a cookie?

> Tests whether you can separate the transport mechanism from the state it points at - a common confusion in interviews.

**Part:** Security & Auth | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [statelessness](../_glossary.md#statelessness), [session](../_glossary.md#session), [jwt](../_glossary.md#jwt)

## In One Sentence

A cookie is a small piece of data the browser stores and sends back automatically, while a session is state the server keeps about a logged-in user - the cookie usually just carries the ID that points at it.

cookie 是瀏覽器儲存並自動送回的一小段資料，session 則是伺服器針對已登入使用者保存的狀態 —— cookie 通常只是帶著指向它的那個 ID。

## Answer Shape

Start with why either exists at all: HTTP is stateless, so the server has no memory of the client. Then give the one-line contrast - client-side storage versus server-side state - and immediately show how they connect in a real login, because the connection is what makes the distinction click. Finish by noting a cookie is a general transport, not a session mechanism.

先說明兩者為何存在：HTTP 是無狀態的，伺服器對客戶端沒有記憶。接著給出一句話的對照 —— 客戶端儲存 vs 伺服器端狀態 —— 然後立刻用一次真實登入示範它們如何連結，因為那個連結才是讓區別「打通」的關鍵。最後補上：cookie 是通用的載體，不是 session 機制。

## Full Spoken Answer

The starting point is that HTTP is stateless, so the server does not automatically remember a user between requests. Both cookies and sessions exist to work around that, but they solve different halves of it.

起點是 HTTP 無狀態，所以伺服器不會自動在兩次請求之間記得一個使用者。cookie 和 session 都是為了繞過這一點而存在，但它們解決的是這個問題的不同一半。

A cookie is a small piece of data stored on the client side. The server sets it with a response header, the browser saves it, and from then on the browser attaches it automatically to every request to that site. A session is state stored on the server side, keyed by a session ID. In a typical session-based login the cookie holds nothing but that ID, and the server uses it to look up the real data - who the user is, whether they are authenticated, what they are allowed to do. So the cookie is the pointer and the session is what it points at.

cookie 是存在客戶端的一小段資料。伺服器用回應標頭設定它，瀏覽器把它存起來，此後瀏覽器會自動把它附加在對該網站的每個請求上。session 則是存在伺服器端的狀態，以 session ID 作為鍵。在典型的 session 登入中，cookie 裡除了那個 ID 之外什麼都沒有，伺服器用它去查出真正的資料 —— 使用者是誰、是否通過認證、可以做什麼。所以 cookie 是指標，session 是它指向的東西。

That split is what makes the security properties differ. Session data never leaves the server, so the client cannot read or tamper with it, and marking the cookie HttpOnly keeps scripts from reading the ID either. It is also worth saying that a cookie is a general-purpose transport, not a session mechanism: the same channel carries language preferences, consent flags, analytics identifiers, and sometimes a JWT. A cookie holding a signed token instead of a session ID is exactly the stateless design that removes the server-side session entirely.

這個切分正是兩者安全性質不同的原因。session 資料從不離開伺服器，客戶端既讀不到也改不了；而把 cookie 標記為 HttpOnly，也能讓腳本讀不到那個 ID。另外值得一提的是：cookie 是通用的載體，不是 session 機制 —— 同一個管道也會攜帶語言偏好、同意設定、分析用識別碼，有時還有 JWT。若 cookie 裡放的是簽章 token 而不是 session ID，那正好就是把伺服器端 session 完全移除的無狀態設計。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q12: What is data normalization?](../databases/q12-data-normalization.md) | [All 29 questions](../../README.md) | [Q23: How do you protect a server from SQL injection attacks?](q23-sql-injection.md) |
