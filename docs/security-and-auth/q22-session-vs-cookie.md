# Q22: What is the difference between a session and a cookie?

> Tests whether you can separate the transport mechanism from the state it points at - a common confusion in interviews.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [jwt](../_glossary.md#jwt), [csrf](../_glossary.md#csrf), [samesite](../_glossary.md#samesite), [xss](../_glossary.md#xss), [tls](../_glossary.md#tls)

## In One Sentence

A cookie is a small piece of data the browser stores and sends back automatically, while a session is state the server keeps about a logged-in user - the cookie usually just carries the ID that points at it.

cookie 是瀏覽器儲存並自動送回的一小段資料，session 則是伺服器針對已登入使用者保存的狀態 —— cookie 通常只是帶著指向它的那個 ID。

## Answer Shape

Start with why either exists at all: HTTP is stateless, so the server has no memory of the client. Then give the one-line contrast - client-side storage versus server-side state - and immediately walk one real login round trip, because the connection is what makes the distinction click. Finish by noting a cookie is a general transport, not a session mechanism.

先說明兩者為何存在：HTTP 是無狀態的，伺服器對客戶端沒有記憶。接著給出一句話的對照 —— 客戶端儲存 vs 伺服器端狀態 —— 然後立刻走一遍真實登入的來回，因為那個連結才是讓區別「打通」的關鍵。最後補上：cookie 是通用的載體，不是 session 機制。

## Full Spoken Answer

The starting point is that HTTP is stateless, so the server does not automatically remember a user between requests. Both cookies and sessions exist to work around that, but they solve different halves of it: the cookie is how something gets carried back and forth, and the session is what is being remembered. The cloakroom is the analogy I would reach for. You hand your coat over and get a numbered tag back - the tag is tiny, it means nothing to anyone without the matching rack, and you carry it in your pocket. That is the cookie. The coat itself stays behind the counter where only the staff can reach it, and that is the session. Hand over the tag and they fetch the coat; lose the tag and the coat is still there, you just cannot prove which one is yours.

起點是 HTTP 無狀態，所以伺服器不會自動在兩次請求之間記得一個使用者。cookie 和 session 都是為了繞過這一點而存在，但它們解決的是這個問題的不同一半：cookie 負責「怎麼把東西帶來帶去」，session 負責「被記住的東西是什麼」。我會用寄物處來比喻。你把外套交出去，拿回一張號碼牌 —— 號碼牌很小，對沒有那排掛鉤的人來說毫無意義，而它就放在你口袋裡，那就是 cookie。外套本身留在櫃檯後面，只有工作人員拿得到，那就是 session。把號碼牌遞過去，他們就把外套拿出來；號碼牌弄丟了，外套還在，你只是無法證明哪一件是你的。

Mechanically: a cookie is a small piece of data stored on the client side. The server sets it with a `Set-Cookie` response header, the browser saves it, and from then on the browser attaches it automatically to every request to that site - you never write code to send it. A session is state stored on the server side, keyed by a session ID, in memory or in a shared store such as Redis. In a typical session-based login the cookie holds nothing but that ID, and the server uses it to look up the real data - who the user is, whether they are authenticated, what they are allowed to do. So the cookie is the pointer and the session is what it points at.

從機制上看：cookie 是存在客戶端的一小段資料。伺服器用 `Set-Cookie` 回應標頭設定它，瀏覽器把它存起來，此後瀏覽器會自動把它附加在對該網站的每個請求上 —— 你完全不用寫程式碼去送它。session 則是存在伺服器端的狀態，以 session ID 作為鍵，放在記憶體或像 Redis 這樣的共用儲存裡。在典型的 session 登入中，cookie 裡除了那個 ID 之外什麼都沒有，伺服器用它去查出真正的資料 —— 使用者是誰、是否通過認證、可以做什麼。所以 cookie 是指標，session 是它指向的東西。

One login makes the whole relationship visible. The user posts their credentials; the server checks them, creates a session record holding the user ID and expiry, and answers with `Set-Cookie: sid=8f3a...; HttpOnly; Secure; SameSite=Lax`. The browser stores that one line. On the next request to the site it sends `Cookie: sid=8f3a...` without being asked, the server looks up `8f3a...` in the session store, finds the record, and knows who is calling. On logout the server deletes the record - and that is the point where the distinction stops being academic: deleting the session kills the login even though the cookie may still be sitting in the browser, while clearing the cookie only makes the browser forget the tag.

一次登入就能把整個關係攤開來看。使用者送出帳密；伺服器驗證後建立一筆存著使用者 ID 與到期時間的 session 紀錄，並回覆 `Set-Cookie: sid=8f3a...; HttpOnly; Secure; SameSite=Lax`。瀏覽器把這一行存起來。下一個對該網站的請求，它會不用人叫就送出 `Cookie: sid=8f3a...`，伺服器拿 `8f3a...` 去 session 儲存裡查，找到紀錄，就知道是誰在呼叫。登出時伺服器刪掉那筆紀錄 —— 而這正是這個區別不再只是紙上談兵的地方：刪掉 session 就終結了登入，即使 cookie 還躺在瀏覽器裡；反之清掉 cookie 只是讓瀏覽器忘了那張號碼牌而已。

That split is also what makes the security properties differ. Session data never leaves the server, so the client cannot read or tamper with it - a user can open devtools and see `sid=8f3a...`, but changing it to another value just points at a session that does not exist. Marking the cookie `HttpOnly` keeps injected scripts from reading the ID, `Secure` keeps it off plaintext connections, and `SameSite` stops the browser attaching it to cross-site requests, which is the CSRF door. What none of that fixes is the tag itself being stolen: whoever holds a valid session ID is that user until it expires or is revoked, which is why the ID has to be long and randomly generated and reissued on login. And it is worth ending on the fact that a cookie is a general-purpose transport, not a session mechanism - the same channel carries language preferences, consent flags, analytics identifiers, and sometimes a JWT, and a cookie holding a signed token instead of a session ID is exactly the stateless design that removes the server-side session entirely, because the tag now has the coat printed on it. The whole answer in one line: the cookie is the numbered tag in your pocket, the session is the coat behind the counter - one is the transport, the other is the state, and the ID is the only thing joining them.

這個切分也正是兩者安全性質不同的原因。session 資料從不離開伺服器，客戶端既讀不到也改不了 —— 使用者可以打開開發者工具看到 `sid=8f3a...`，但把它改成別的值，也只是指向一個不存在的 session。把 cookie 標記為 `HttpOnly` 能讓注入的腳本讀不到那個 ID，`Secure` 讓它不會走上明文連線，`SameSite` 則讓瀏覽器不把它附加到跨站請求上，也就是關上 CSRF 那扇門。但這些都補不了「號碼牌被偷走」這件事：誰拿著一個有效的 session ID，在它過期或被撤銷之前誰就是那個使用者 —— 這正是為什麼 ID 必須夠長、要用亂數產生，而且登入時要重新簽發。最後值得收在這一點：cookie 是通用的載體，不是 session 機制 —— 同一個管道也會攜帶語言偏好、同意設定、分析用識別碼，有時還有 JWT；若 cookie 裡放的是簽章 token 而不是 session ID，那正好就是把伺服器端 session 完全移除的無狀態設計，因為號碼牌上直接印著外套本身。整題濃縮成一句：cookie 是你口袋裡的號碼牌，session 是櫃檯後面的外套 —— 一個是載體，一個是狀態，而那個 ID 是唯一把它們接起來的東西。

## Quick Reference

### The two, side by side

| | Cookie | Session |
|---|---|---|
| Where it lives | In the browser, on the user's machine | On the server - memory, a database, or Redis |
| What it holds | A small string, roughly 4 KB max | Whatever the app needs: user ID, roles, expiry, cart |
| Who can read it | The user, and any script unless `HttpOnly` | Only the server |
| Who can change it | The user - so it is never trusted on its own | Only the server |
| How it moves | The browser attaches it automatically to every matching request | It never moves; only its ID travels |
| Lifetime | Until `Expires`/`Max-Age`, or until the browser closes | Until it expires server-side or the record is deleted |
| Ends when | The browser drops it | The server deletes it - this is what logout does |

The one-line link: the session is the state, the cookie is how its ID gets carried.

### One login round trip

| Step | Who | What happens on the wire |
|---|---|---|
| 1. Log in | Client → Server | `POST /login` with credentials |
| 2. Create session | Server | Stores `8f3a... → {user_id: 42, exp: ...}` in the session store |
| 3. Hand back the tag | Server → Client | `Set-Cookie: sid=8f3a...; HttpOnly; Secure; SameSite=Lax` |
| 4. Next request | Client → Server | `Cookie: sid=8f3a...` - sent automatically, no code needed |
| 5. Look up | Server | Reads `8f3a...` from the store, knows it is user 42 |
| 6. Log out | Server | Deletes the record; the cookie may linger but now points at nothing |

### The attributes that matter, and what each one stops

| Attribute | What it does | What it prevents |
|---|---|---|
| `HttpOnly` | JavaScript cannot read the cookie | An XSS payload stealing the session ID |
| `Secure` | Sent only over HTTPS | The ID being read off a plaintext connection |
| `SameSite=Lax` / `Strict` | Not attached to cross-site requests | CSRF - another site riding your logged-in cookie |
| `Max-Age` / `Expires` | Bounds how long the browser keeps it | A tag that stays valid forever on a shared machine |

### Not every cookie is a session

| Cookie contents | Is there a session behind it? |
|---|---|
| `sid=8f3a...` | Yes - an opaque ID pointing at server-side state |
| `lang=zh-TW` | No - a preference, the whole value is the data |
| `consent=analytics` | No |
| `token=eyJhbGci...` (JWT) | No - the state is inside the token; see [Q21](q21-session-vs-jwt-authentication.md) |

## Interview Version

> The starting point is that HTTP is stateless, so the server does not automatically remember a user between requests. Both cookies and sessions exist to work around that, but they solve different halves: the cookie is how something gets carried back and forth, and the session is what is being remembered. The cloakroom is the analogy I would reach for. You hand your coat over and get a numbered tag - the tag is tiny, it means nothing to anyone without the matching rack, and you carry it in your pocket. That is the cookie. The coat stays behind the counter where only the staff can reach it, and that is the session. Mechanically, a cookie is a small piece of data stored client-side: the server sets it with a Set-Cookie header, the browser saves it and attaches it automatically to every request to that site - you never write code to send it. A session is state stored server-side, keyed by a session ID, in memory or in a shared store such as Redis. In a typical login the cookie holds nothing but that ID, and the server uses it to look up the real data. One login makes the relationship visible: the user posts credentials, the server creates a session record and answers with Set-Cookie: sid=8f3a; the browser stores that one line and sends it back unasked; the server looks up 8f3a and knows who is calling. On logout the server deletes the record - and that is where the distinction stops being academic, because deleting the session kills the login even though the cookie may still sit in the browser, while clearing the cookie only makes the browser forget the tag.

面試時可回答：起點是 HTTP 無狀態，所以伺服器不會自動在兩次請求之間記得一個使用者。cookie 和 session 都是為了繞過這一點而存在，但它們解決的是不同的一半：cookie 負責「怎麼把東西帶來帶去」，session 負責「被記住的東西是什麼」。我會用寄物處來比喻。你把外套交出去，拿回一張號碼牌 —— 號碼牌很小，對沒有那排掛鉤的人來說毫無意義，而它就放在你口袋裡，那就是 cookie。外套留在櫃檯後面，只有工作人員拿得到，那就是 session。從機制上看，cookie 是存在客戶端的一小段資料：伺服器用 Set-Cookie 標頭設定它，瀏覽器把它存起來，並自動附加在對該網站的每個請求上 —— 你完全不用寫程式碼去送它。session 則是存在伺服器端的狀態，以 session ID 為鍵，放在記憶體或像 Redis 這樣的共用儲存裡。在典型的登入中，cookie 裡除了那個 ID 之外什麼都沒有，伺服器用它去查出真正的資料。一次登入就能把整個關係攤開來看：使用者送出帳密，伺服器建立一筆 session 紀錄並回覆 Set-Cookie: sid=8f3a；瀏覽器把這一行存起來，下次不用人叫就送回去；伺服器拿 8f3a 去查，就知道是誰在呼叫。登出時伺服器刪掉那筆紀錄 —— 而這正是這個區別不再只是紙上談兵的地方：刪掉 session 就終結了登入，即使 cookie 還躺在瀏覽器裡；反之清掉 cookie，只是讓瀏覽器忘了那張號碼牌而已。

The sentence to remember is: **The cookie is the numbered tag in your pocket, the session is the coat behind the counter - one is the transport, the other is the state.**

最值得記：**cookie 是你口袋裡的號碼牌，session 是櫃檯後面的外套 —— 一個是載體，另一個是狀態。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q20: How do you change a database schema without downtime?](../databases/q20-schema-migrations.md) | [All 40 questions](../../README.md) | [Q25: What is Cross-Site Scripting (XSS)?](q25-xss.md) |
