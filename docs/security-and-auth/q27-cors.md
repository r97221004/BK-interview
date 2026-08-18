# Q27: What is CORS?

> Tests whether you know CORS is a browser rule that relaxes a restriction, not a server-side security control.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [resource](../_glossary.md#resource), [csrf](../_glossary.md#csrf), [samesite](../_glossary.md#samesite), [cache](../_glossary.md#cache), [rate limiting](../_glossary.md#rate-limiting)

## In One Sentence

CORS is a set of response headers by which a server tells the browser which other origins are allowed to read its responses, relaxing the same-origin policy in a controlled way.

CORS 是一組回應標頭，伺服器用它告訴瀏覽器有哪些其他來源可以讀取它的回應，以受控的方式放寬同源政策。

## Answer Shape

Explain the restriction before the mechanism: the browser blocks cross-origin reads by default, and CORS is how a server opts out of that for specific origins. Walk the preflight so it is concrete. Then land the point that decides whether you actually understand it - CORS is enforced by the browser and protects the user, not your server - because that is what the interviewer is checking.

先解釋限制、再解釋機制：瀏覽器預設會擋掉跨來源的讀取，而 CORS 是伺服器針對特定來源解除該限制的方式。把 preflight 走一遍讓它具體。接著落在真正決定你是否理解的那一點 —— CORS 由瀏覽器執行、保護的是使用者而不是你的伺服器 —— 因為那正是面試官在確認的。

## Full Spoken Answer

CORS stands for Cross-Origin Resource Sharing, and it is a browser security mechanism. It exists because browsers enforce the same-origin policy: JavaScript on one origin - the combination of scheme, host, and port - cannot read a response from a different origin. Without that rule, any page you visited could quietly call your bank's API in the background using your cookies and read the result. CORS is the controlled way for a server to say which origins are exempt.

CORS 的全稱是 Cross-Origin Resource Sharing，它是一個瀏覽器的安全機制。它存在是因為瀏覽器會執行同源政策：某個來源（協定、主機、port 三者的組合）上的 JavaScript 不能讀取另一個來源的回應。若沒有這條規則，你造訪的任何頁面都能在背景悄悄用你的 cookie 呼叫你銀行的 API 並讀走結果。CORS 就是伺服器用來聲明「哪些來源可以豁免」的受控方式。

The mechanism is headers. For a request that is not simple - anything using a method beyond GET, HEAD, or POST, or carrying a custom header such as authorization - the browser first sends an automatic OPTIONS request called a preflight, which asks the server whether the real request is permitted. The server answers with headers naming the allowed origin, methods, and headers, and optionally a max-age so the answer can be cached. If the reply is satisfactory the browser sends the real request; if not, it blocks the response and the console shows a CORS error.

它的機制是標頭。對於「非簡單」的請求 —— 使用 GET、HEAD、POST 以外的方法，或帶有像 authorization 這樣的自訂標頭 —— 瀏覽器會先送出一個自動的 OPTIONS 請求，稱為 preflight，用來詢問伺服器是否允許真正的請求。伺服器以標頭回答，指明允許的來源、方法與標頭，並可選擇性地加上 max-age 讓這個答案能被快取。如果回覆令人滿意，瀏覽器就送出真正的請求；如果不滿意，它會擋下回應，主控台則顯示 CORS 錯誤。

A concrete example makes it stick. If a front end at one subdomain calls an API at another, the API must return an allow-origin header naming the front end's exact origin for the browser to hand the response to the page. Two practical notes: the wildcard is convenient in development but should never reach production, and it cannot be combined with credentialed requests at all, so as soon as cookies are involved you must name the origin explicitly and set the allow-credentials header.

一個具體例子能讓它記得住。如果某個子網域上的前端呼叫另一個子網域上的 API，API 必須回傳一個 allow-origin 標頭並指明前端的確切來源，瀏覽器才會把回應交給頁面。兩點實務提醒：萬用字元在開發時很方便，但絕不該進到正式環境，而且它完全不能與帶憑證的請求併用，所以一旦牽涉到 cookie，你就必須明確指名來源並設定 allow-credentials 標頭。

The point that matters most is what CORS is not. It is enforced by the browser, so it protects your users from other websites - it does not protect your server from anything. A script, a mobile app, or a command-line client ignores CORS entirely and can call your API however it likes, and even in a browser the request usually reaches your server before the response is blocked. So server-side controls have to stand on their own: authentication and authorization on every endpoint, CSRF tokens and SameSite cookies for browser sessions, Origin checks as an extra signal, rate limiting, and request signing for machine clients. If browsers stopped enforcing CORS tomorrow, a correctly built API would still be safe.

最重要的一點是「CORS 不是什麼」。它由瀏覽器執行，所以它保護的是你的使用者不被其他網站利用 —— 它完全不保護你的伺服器。腳本、行動 App 或命令列客戶端會完全忽略 CORS，想怎麼呼叫你的 API 就怎麼呼叫；而且即使在瀏覽器裡，請求通常也已經抵達你的伺服器，只是回應被擋下來而已。因此伺服器端的控制必須能夠獨立成立：每個 endpoint 都做認證與授權、瀏覽器 session 用 CSRF token 與 SameSite cookie、把 Origin 檢查當成額外訊號、加上速率限制，並對機器客戶端使用請求簽章。如果瀏覽器明天起不再執行 CORS，一個正確建構的 API 仍然是安全的。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q26: What is Cross-Site Request Forgery (CSRF)?](q26-csrf.md) | [All 29 questions](../../README.md) | [Q33: Explain the underlying data structures of lists, sets, tuples, and dictionaries in Python.](../architecture-and-scaling/q33-python-builtin-data-structures.md) |
