# Q25: What is Cross-Site Scripting (XSS)?

> Tests whether you know that the fix is context-correct output encoding, and whether you can name the three XSS variants.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [cookie](../_glossary.md#cookie), [jwt](../_glossary.md#jwt)

## In One Sentence

XSS is when attacker-supplied text ends up being executed as script in another user's browser, so it runs with your site's origin and can do anything that user could do.

XSS 是攻擊者提供的文字最後在別的使用者瀏覽器裡被當成腳本執行，於是它以你網站的來源身分運行，能做那位使用者能做的任何事。

## Answer Shape

Define it by what the attacker gains - code running under your origin - rather than by the alert box example, because the impact is what the question is really about. Name the three variants, since that is the follow-up. Then give the fix in the right order: context-correct output encoding first, a framework that does it by default second, and CSP as the layer that limits the damage when the first two fail.

用攻擊者「得到什麼」來定義它 —— 以你的來源身分執行的程式碼 —— 而不是用彈出視窗當例子，因為影響才是這題真正在問的。把三種類型講出來，因為那是接下來的追問。接著依正確順序給出修法：先是依情境正確的輸出編碼，其次是預設就會做這件事的框架，最後是 CSP，作為前兩者失守時限制傷害的那一層。

## Full Spoken Answer

Cross-site scripting happens when an application takes user input and renders it into a page without escaping it for that context, so the browser parses it as markup rather than as text. An attacker submits something containing a script tag, another user opens the page, and the browser executes that script as if the trusted site had written it. The classic alert box is only the proof; what the attacker actually gets is arbitrary code running inside your origin.

跨站腳本攻擊發生在應用程式取用了使用者輸入，並在沒有針對該情境做跳脫的情況下渲染進頁面，於是瀏覽器把它解析成標記而非文字。攻擊者送出含有 script 標籤的內容，另一位使用者打開該頁面，瀏覽器就把那段腳本當成可信任網站寫的來執行。經典的彈出視窗只是概念驗證；攻擊者真正得到的，是在你的來源內部執行任意程式碼的能力。

That is why the impact is severe. Code running under your origin can read the DOM, read any token reachable from JavaScript including a JWT in local storage, send requests as the logged-in user, rewrite the page to phish for a password, or install a keylogger on the login form. An HttpOnly cookie is out of reach of the script, which is a real reason to prefer it, but the script can still make authenticated requests using that cookie, so it does not make XSS harmless.

這正是它影響嚴重的原因。以你的來源身分執行的程式碼可以讀取 DOM、讀取任何 JavaScript 拿得到的 token（包括存在 local storage 的 JWT）、以已登入使用者的身分發送請求、改寫頁面來釣取密碼，或在登入表單上裝設鍵盤側錄。標記 HttpOnly 的 cookie 是腳本拿不到的，這確實是偏好它的理由，但腳本仍然可以「使用」那個 cookie 發出已認證的請求，所以它並不會讓 XSS 變得無害。

There are three variants and the interviewer usually asks for them. Stored XSS is when the payload is saved on the server - in a comment, a profile field - and served to everyone who views it, which makes it the most damaging. Reflected XSS is when the payload comes in on the request, typically in a query parameter, and is echoed straight back into the response, so it needs a crafted link. DOM-based XSS never involves the server at all: client-side JavaScript reads something from the URL or storage and writes it into the page unsafely.

它有三種類型，面試官通常會問。儲存型 XSS 是 payload 被存在伺服器上 —— 在留言、個人資料欄位裡 —— 並提供給所有瀏覽的人，因此傷害最大。反射型 XSS 是 payload 隨請求進來（通常在 query 參數裡），又被直接回顯到回應中，所以需要一條精心構造的連結。DOM 型 XSS 則完全不經過伺服器：客戶端 JavaScript 從 URL 或儲存中讀取某個值，再以不安全的方式寫進頁面。

The fix is output encoding at the point of rendering, and it has to match the context: escaping for an HTML body, an HTML attribute, a JavaScript literal, and a URL are four different rules, which is why one global sanitize-on-input step is not enough. In practice that means using a templating engine or framework that escapes by default - React and Jinja2 both do - and being deliberate about the specific escape hatches that turn it off, such as rendering raw HTML. Validate and sanitize input as well, using a proven library rather than your own regular expression when you genuinely must accept rich text. Then add a Content Security Policy to restrict which script sources may run, avoid eval and inline JavaScript so the policy can actually be strict, and treat it as damage limitation for the injection you missed rather than as the primary defense.

修法是在「渲染的當下」做輸出編碼，而且必須符合情境：HTML 內文、HTML 屬性、JavaScript 字面值、URL 這四種的跳脫規則各不相同，這正是為什麼在輸入端做一次全域消毒並不足夠。實務上這代表使用預設就會跳脫的樣板引擎或框架 —— React 和 Jinja2 都是 —— 並且對那些會關掉跳脫的特定逃生口（例如渲染原始 HTML）保持警覺。同時也要驗證與消毒輸入；當你真的必須接受富文字時，使用經過驗證的函式庫而不是自己寫的正規表達式。接著加上 Content Security Policy 來限制哪些腳本來源可以執行，避免 eval 和行內 JavaScript 好讓政策真的能設嚴，並且把它當成「你漏掉的那次注入」的損害控制，而不是主要防線。

## Quick Reference

### What an injected payload looks like

Submitted into any field that is later rendered without escaping:

```html
<script>alert('hacked')</script>
```

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q22: What is the difference between a session and a cookie?](q22-session-vs-cookie.md) | [All 37 questions](../../README.md) | [Q27: What is CORS?](q27-cors.md) |
