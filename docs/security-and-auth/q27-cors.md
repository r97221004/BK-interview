# Q27: What is CORS?

> Tests whether you know CORS is a browser rule that relaxes a restriction, not a server-side security control.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [cookie](../_glossary.md#cookie), [csrf](../_glossary.md#csrf), [samesite](../_glossary.md#samesite), [tls](../_glossary.md#tls), [rate limiting](../_glossary.md#rate-limiting)

## In One Sentence

CORS is a browser mechanism that controls whether a page from one origin may read a response from another, and the server opts specific origins in with headers such as `Access-Control-Allow-Origin`.

CORS 是瀏覽器的機制，用來控制某個來源的頁面能不能讀取另一個來源的回應；伺服器則用 `Access-Control-Allow-Origin` 這類標頭，把特定來源放進允許名單。

## Answer Shape

Explain the restriction before the mechanism: the browser blocks cross-origin reads by default, and CORS is how a server opts out of that for specific origins. Define origin precisely, since that is a likely follow-up. Then land the point that decides whether you actually understand it - CORS is enforced by the browser and protects the user, not your server - and prove it with `curl`.

先解釋限制、再解釋機制：瀏覽器預設會擋掉跨來源的讀取，而 CORS 是伺服器針對特定來源解除該限制的方式。把 origin 定義清楚，因為那很可能是追問。接著落在真正決定你是否理解的那一點 —— CORS 由瀏覽器執行、保護的是使用者而不是你的伺服器 —— 並用 `curl` 來證明它。

## Full Spoken Answer

CORS stands for Cross-Origin Resource Sharing, and the thing to say first is that it is a browser mechanism, not a server one. Browsers enforce the same-origin policy: JavaScript running on one origin cannot read a response from a different origin. Without that rule, any page you happened to open could quietly call `https://mybank.com/account` in the background with your cookies attached and read the result. So the default is no. CORS is how a server says "these particular origins are fine" - the same-origin policy is the locked door, and CORS is the guest list the server hands to the browser.

CORS 的全稱是 Cross-Origin Resource Sharing，而第一句該說的是：它是瀏覽器的機制，不是伺服器的機制。瀏覽器會執行同源政策：在某個來源上執行的 JavaScript，不能讀取另一個來源的回應。若沒有這條規則，你隨手打開的任何頁面都能在背景帶著你的 cookie 呼叫 `https://mybank.com/account` 並讀走結果。所以預設是「不行」。CORS 就是伺服器說「這幾個來源沒問題」的方式 —— 同源政策是那道上鎖的門，CORS 是伺服器交給瀏覽器的那份訪客名單。

An origin is scheme plus host plus port, all three, and if any one differs it is cross-origin. `https://example.com` and `http://example.com` are different origins because the scheme differs. `https://example.com` and `https://api.example.com` are different because the host differs - a subdomain is a different origin, which surprises people. And `http://localhost:3000` and `http://localhost:8080` are different because the port differs, which is why almost everyone meets CORS for the first time while running a React dev server against a local API.

一個 origin 是 scheme 加 host 加 port，三者缺一不可，只要其中任何一個不同就是跨來源。`https://example.com` 和 `http://example.com` 是不同來源，因為 scheme 不同。`https://example.com` 和 `https://api.example.com` 是不同來源，因為 host 不同 —— 子網域算是不同來源，這點常讓人意外。而 `http://localhost:3000` 和 `http://localhost:8080` 是不同來源，因為 port 不同 —— 這也正是幾乎所有人第一次遇到 CORS，都是在用 React 開發伺服器打本機 API 的時候。

Concretely: a front end at `https://frontend.com` runs `fetch("https://api.backend.com/users")`. The browser sees two different origins, sends the request, and then checks the response for permission. If the API answers with `Access-Control-Allow-Origin: https://frontend.com`, the browser hands the response to the JavaScript. If that header is missing or names a different origin, the browser blocks the page from reading it and the console shows the "blocked by CORS policy" message. For requests that are not simple - anything beyond GET, HEAD, or a basic POST, or carrying a custom header such as `Authorization` - the browser first sends an automatic `OPTIONS` preflight asking whether the real request is allowed, and only sends the real one if the answer is satisfactory.

具體來說：位在 `https://frontend.com` 的前端執行 `fetch("https://api.backend.com/users")`。瀏覽器看到兩個不同的來源，把請求送出去，然後檢查回應裡有沒有許可。如果 API 回覆 `Access-Control-Allow-Origin: https://frontend.com`，瀏覽器就把回應交給 JavaScript。如果那個標頭不存在、或指名的是別的來源，瀏覽器就會擋住頁面去讀它，主控台則出現「blocked by CORS policy」。至於「非簡單」的請求 —— GET、HEAD、基本 POST 以外的，或帶著像 `Authorization` 這種自訂標頭的 —— 瀏覽器會先自動送一個 `OPTIONS` preflight 去問真正的請求是否被允許，答案滿意才送出真正的那一個。

Two practical notes. The wildcard `*` is convenient in development but should never reach production, and it cannot be combined with credentialed requests at all - so the moment cookies are involved you must name the exact origin and add `Access-Control-Allow-Credentials: true`. And notice the sequence above: the browser usually sends the request and your server usually runs it, then the response gets blocked on the way back. What CORS withholds is the reading of the response, not the arrival of the request.

兩點實務提醒。萬用字元 `*` 在開發時很方便，但絕不該進到正式環境，而且它完全不能與帶憑證的請求併用 —— 所以一旦牽涉到 cookie，你就必須指名確切的來源，並加上 `Access-Control-Allow-Credentials: true`。另外注意上面那個順序：瀏覽器通常已經把請求送出去、你的伺服器通常也已經執行了，然後回應才在回程被擋下。CORS 扣住的是「讀取回應」，不是「請求的抵達」。

That leads to the point that matters most, and the fastest way to prove it is `curl`. Call the same API from `curl` or Postman and it just works - no CORS error, ever - because there is no browser in the loop to enforce anything. A mobile app, a script, a scraper: same story. So CORS protects your users from other websites reading their data; it does not protect your server from anyone. Server-side controls have to stand on their own - authentication and authorization on every endpoint, CSRF tokens and `SameSite` cookies for browser sessions, rate limiting. If browsers stopped enforcing CORS tomorrow, a correctly built API would still be safe. One line to remember: CORS is a guest list the server gives the browser, and the bouncer only stands at the browser's door.

這就帶到最重要的那一點，而證明它最快的方法就是 `curl`。用 `curl` 或 Postman 去打同一個 API，它就是會成功 —— 永遠不會有 CORS 錯誤 —— 因為這中間根本沒有瀏覽器來執行任何限制。行動 App、腳本、爬蟲，也都一樣。所以 CORS 保護的是你的使用者不被其他網站讀走資料；它完全不保護你的伺服器。伺服器端的控制必須能夠獨立成立 —— 每個 endpoint 都做認證與授權、瀏覽器 session 用 CSRF token 與 `SameSite` cookie、加上速率限制。如果瀏覽器明天起不再執行 CORS，一個正確建構的 API 仍然是安全的。記住一句：CORS 是伺服器交給瀏覽器的一份訪客名單，而保鏢只站在瀏覽器那道門口。

## Quick Reference

### Same origin, or not? Scheme + host + port, all three must match

| Compared with `https://example.com` | Same origin? | Why |
|---|---|---|
| `https://example.com/about` | Yes | Path is not part of the origin |
| `http://example.com` | No | Scheme differs |
| `https://api.example.com` | No | Host differs - a subdomain counts |
| `https://example.com:8443` | No | Port differs - 443 is implied above |

Same rule off `example.com`: `http://localhost:3000` and `http://localhost:8080`
are different origins too, which is why a React dev server calling a local API is
where most people meet CORS for the first time.

### The headers you should be able to name

| Header | Sent by | What it says |
|---|---|---|
| `Origin` | Browser | Who is asking - set automatically, cannot be forged by page JS |
| `Access-Control-Allow-Origin` | Server | Which origin may read the response - one origin, or `*` |
| `Access-Control-Allow-Methods` | Server | Which methods the real request may use (preflight answer) |
| `Access-Control-Allow-Headers` | Server | Which custom headers are permitted (preflight answer) |
| `Access-Control-Allow-Credentials` | Server | Cookies are allowed - and then `*` is forbidden |
| `Access-Control-Max-Age` | Server | How long the browser may cache the preflight answer |

```http
Access-Control-Allow-Origin: https://frontend.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Content-Type, Authorization
```

### What CORS does and does not stop

| Caller | Blocked by CORS? | Why |
|---|---|---|
| Page JS at another origin, no allow header | Yes | The browser withholds the response from the page |
| Page JS at an allowed origin | No | The server put it on the guest list |
| `curl` / Postman | No | No browser, no enforcement |
| Mobile app, backend service, scraper | No | Same - CORS is a browser rule only |

Note what "blocked" means in row one: for a simple request the browser still sends
it and your server still runs it - only the reading of the response is withheld.

The line to remember: CORS protects your users from other sites, never your server from attackers.

## Interview Version

> CORS stands for Cross-Origin Resource Sharing, and the thing to say first is that it is a browser mechanism, not a server one. Browsers enforce the same-origin policy: JavaScript running on one origin cannot read a response from a different origin. Without that rule, any page you happened to open could quietly call your bank's account endpoint in the background with your cookies attached and read the result. So the default is no, and CORS is how a server says these particular origins are fine - the same-origin policy is the locked door, and CORS is the guest list the server hands to the browser. An origin is scheme plus host plus port, all three, and if any one differs it is cross-origin: a subdomain is a different origin, which surprises people, and localhost:3000 versus :8080 is why almost everyone meets CORS for the first time running a dev server against a local API. Concretely, a front end at frontend.com calls api.backend.com. The browser sends the request, then checks the response for permission: if the API answers with Access-Control-Allow-Origin naming that front end, the browser hands the response to the JavaScript; if it is missing or names a different origin, the browser blocks the page from reading it. For requests that are not simple, the browser first sends an automatic OPTIONS preflight asking whether the real request is allowed. Then the point that matters most, and the fastest way to prove it is curl: call the same API from curl or Postman and it just works, no CORS error ever, because there is no browser in the loop. So CORS protects your users from other websites reading their data; it does not protect your server from anyone.

面試時可回答：CORS 的全稱是 Cross-Origin Resource Sharing，而第一句該說的是：它是瀏覽器的機制，不是伺服器的機制。瀏覽器會執行同源政策：在某個來源上執行的 JavaScript，不能讀取另一個來源的回應。若沒有這條規則，你隨手打開的任何頁面都能在背景帶著你的 cookie 呼叫你銀行的帳戶 endpoint 並讀走結果。所以預設是「不行」，而 CORS 就是伺服器說「這幾個來源沒問題」的方式 —— 同源政策是那道上鎖的門，CORS 是伺服器交給瀏覽器的那份訪客名單。一個 origin 是 scheme 加 host 加 port，三者缺一不可，只要其中任何一個不同就是跨來源：子網域算不同來源，這點常讓人意外；而 localhost:3000 對 :8080，正是幾乎所有人第一次遇到 CORS 的場景 —— 用開發伺服器打本機 API 的時候。具體來說，位在 frontend.com 的前端呼叫 api.backend.com。瀏覽器把請求送出去，然後檢查回應裡有沒有許可：如果 API 回覆的 Access-Control-Allow-Origin 指名了那個前端，瀏覽器就把回應交給 JavaScript；如果那個標頭不存在、或指名的是別的來源，瀏覽器就擋住頁面去讀它。至於非簡單的請求，瀏覽器會先自動送一個 OPTIONS preflight 去問真正的請求是否被允許。接著是最重要的那一點，而證明它最快的方法就是 curl：用 curl 或 Postman 去打同一個 API，它就是會成功，永遠不會有 CORS 錯誤，因為這中間根本沒有瀏覽器。所以 CORS 保護的是你的使用者不被其他網站讀走資料；它完全不保護你的伺服器。

The sentence to remember is: **CORS is a guest list the server hands the browser, and the bouncer only stands at the browser's door - which is why curl never sees a CORS error.**

最值得記：**CORS 是伺服器交給瀏覽器的一份訪客名單，而保鏢只站在瀏覽器那道門口 —— 這正是為什麼 curl 永遠不會遇到 CORS 錯誤。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q25: What is Cross-Site Scripting (XSS)?](q25-xss.md) | [All 42 questions](../../README.md) | [Q33: Explain the underlying data structures of lists, sets, tuples, and dictionaries in Python.](../architecture-and-scaling/q33-python-builtin-data-structures.md) |
