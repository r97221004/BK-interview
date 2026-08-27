# Q25: What is Cross-Site Scripting (XSS)?

> Tests whether you know that the fix is context-correct output encoding, and whether you can name the three XSS variants.

**Part:** Security & Auth | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [cookie](../_glossary.md#cookie), [session](../_glossary.md#session), [jwt](../_glossary.md#jwt)

## In One Sentence

XSS is a web vulnerability where untrusted input ends up interpreted as executable JavaScript in another user's browser - input that should have stayed data gets treated as code.

XSS 是一種 Web 漏洞：不可信的輸入最後在別的使用者瀏覽器裡被解讀成可執行的 JavaScript —— 本來應該是 data 的東西，被當成 code 執行了。

## Answer Shape

Lead with the one idea that explains everything else: the site let data become code. Show it with a comment box, because one line of HTML makes it obvious. Name the three variants, since that is the standard follow-up. Then give the fix in order - output encoding first, safe DOM APIs, a sanitizer if you truly need HTML, and CSP as the extra layer.

先講那個能解釋其他一切的核心概念：網站讓 data 變成了 code。用留言框把它演出來，因為一行 HTML 就講完了。接著點名三種類型，因為那是標準追問。然後依序給修法 —— 輸出編碼第一、安全的 DOM API、真的需要 HTML 時才用 sanitizer，最後 CSP 當額外一層。

## Full Spoken Answer

XSS happens when an application takes user input and puts it into a page without escaping it, so the browser parses it as markup instead of displaying it as text. Say a site has a comment box. I type `Hello Matt` and the server renders `<div>Hello Matt</div>`, which is fine. An attacker types `<script>alert('XSS')</script>`, the server renders it the same way, and now the browser sees a real `<script>` tag and runs it. Nothing was broken into - the site simply let a string that was meant to be data become code.

XSS 發生在應用程式取用使用者輸入後，沒有做跳脫就放進頁面，於是瀏覽器把它解析成標記，而不是當成文字顯示。假設網站有個留言框。我輸入 `Hello Matt`，伺服器渲染成 `<div>Hello Matt</div>`，沒問題。攻擊者輸入 `<script>alert('XSS')</script>`，伺服器一樣照放，這下瀏覽器看到的是一個真的 `<script>` 標籤，就把它執行了。沒有任何東西被闖入 —— 網站只是讓一段本該是 data 的字串變成了 code。

The `alert()` is just the proof. Because that code runs inside your site's origin, the browser cannot tell it apart from your own scripts: it can read anything on the page, read a token such as a JWT from local storage, send requests as the logged-in user, or rewrite the login form to steal a password. An HttpOnly cookie keeps the script from reading the session ID, but the browser still attaches that cookie to requests the script makes - so HttpOnly stops the key being copied, not the door being used.

`alert()` 只是概念驗證。因為那段程式碼是在你網站的來源內執行，瀏覽器無法把它跟你自己的腳本分辨開來：它可以讀取頁面上的任何東西、讀取 local storage 裡的 token（例如 JWT）、以已登入使用者的身分發送請求，或改寫登入表單來竊取密碼。標記 HttpOnly 的 cookie 能讓腳本讀不到 session ID，但腳本發出的請求，瀏覽器照樣會附上那個 cookie —— 所以 HttpOnly 擋的是鑰匙被複製，不是門被使用。

There are three variants, and the only difference is where the payload waits before it runs. Stored XSS is saved in your database - a comment, a username - and fires for everyone who opens the page, which makes it the most dangerous. Reflected XSS rides in on the URL, typically `/search?q=<script>...</script>`, and is echoed straight back into the response, so the victim has to click a crafted link. DOM-based XSS never reaches the server at all: front-end JavaScript takes something from the URL and does `element.innerHTML = userInput`.

它有三種類型，差別只在 payload 執行前待在哪裡。儲存型存在你的資料庫裡 —— 一則留言、一個使用者名稱 —— 對每個打開頁面的人都會觸發，所以最危險。反射型搭著網址進來，典型是 `/search?q=<script>...</script>`，又被直接回顯進回應，所以受害者必須點一條精心構造的連結。DOM 型則完全不經過伺服器：前端 JavaScript 從網址取值，然後做 `element.innerHTML = userInput`。

The main fix is output encoding at the point of rendering: turn `<` and `>` into `&lt;` and `&gt;` so the browser shows `<script>` as visible text instead of executing it. It has to be context-aware, because escaping for an HTML body, an attribute, a JavaScript literal and a URL are four different rules - which is also why encoding belongs at output, not at input, since when the data arrives you do not yet know where it will end up. In practice, use a framework that escapes by default and audit the escape hatches - `innerHTML`, `dangerouslySetInnerHTML`, Jinja's `|safe`. When you genuinely must accept HTML, run it through a proven sanitizer such as DOMPurify rather than your own regex. Then add a Content Security Policy as an extra layer, and be honest that it is damage limitation for the injection you missed, not the primary defence. One line to remember: XSS is user input that should have been data being executed as code.

主要修法是在「渲染的當下」做輸出編碼：把 `<` 和 `>` 變成 `&lt;` 和 `&gt;`，讓瀏覽器把 `<script>` 當成看得見的文字顯示，而不是執行它。而且必須依情境而定，因為 HTML 內文、屬性、JavaScript 字面值、URL 的跳脫規則各不相同 —— 這也正是編碼屬於輸出端而非輸入端的原因：資料剛進來時，你還不知道它最後會去哪裡。實務上，使用預設就會跳脫的框架，並且盯緊那些逃生口 —— `innerHTML`、`dangerouslySetInnerHTML`、Jinja 的 `|safe`。當你真的必須接受 HTML 時，用經過驗證的 sanitizer（例如 DOMPurify），而不是自己寫的正規表達式。接著加上 Content Security Policy 當額外一層，並且誠實看待它：它是「你漏掉的那次注入」的損害控制，不是主要防線。記住一句：XSS 就是本該當 data 的使用者輸入，被當成 code 執行了。

## Quick Reference

### Data becoming code, in one line of HTML

```html
<!-- What the server sends when it does not escape - the browser runs it -->
<div><script>alert('XSS')</script></div>

<!-- What it sends when it escapes on output - the browser displays <script> as plain text -->
<div>&lt;script&gt;alert('XSS')&lt;/script&gt;</div>
```

### The three variants

| | Stored | Reflected | DOM-based |
|---|---|---|---|
| Where the payload waits | Your database | The URL the victim clicks | Only in the browser |
| Does the server see it? | Yes - stored, then served | Yes - echoed back | No |
| How the victim is hit | Just opens the page | Must click a crafted link | Opens a crafted URL |
| Typical entry point | Comment, username, profile | Search box, error message | `location.hash` → `innerHTML` |
| Blast radius | Everyone who views the page | One victim per click | One victim per click |

Memory hook: stored sits in your database, reflected bounces off your server, DOM-based never gets there.

### Defences, in the order you should say them

| Layer | What it is | What it buys you |
|---|---|---|
| 1. Context-aware output encoding | Escape at render time, per destination | The real fix - the payload becomes visible text |
| 2. Safe DOM APIs | `textContent` instead of `innerHTML` | Removes the most common front-end sink |
| 3. A sanitizer | DOMPurify, allowlist-based | Lets you accept real HTML safely |
| 4. Content Security Policy | Restrict script sources, ban inline and `eval` | Damage limitation for the one you missed |

## Interview Version

> XSS happens when an application takes user input and puts it into a page without escaping it, so the browser parses it as markup instead of displaying it as text. Say a site has a comment box: I type Hello Matt and the server renders a div containing Hello Matt, which is fine. An attacker types a script tag containing alert('XSS'), the server renders it the same way, and now the browser sees a real script tag and runs it. Nothing was broken into - the site simply let a string that was meant to be data become code. The alert is just the proof. Because that code runs inside your site's origin, the browser cannot tell it apart from your own scripts: it can read anything on the page, read a token from local storage, send requests as the logged-in user, or rewrite the login form to steal a password. An HttpOnly cookie keeps the script from reading the session ID, but the browser still attaches that cookie to requests the script makes - so HttpOnly stops the key being copied, not the door being used. There are three variants, and the only difference is where the payload waits before it runs. Stored XSS is saved in your database and fires for everyone who opens the page. Reflected XSS rides in on the URL and is echoed back, so the victim has to click a crafted link. DOM-based XSS never reaches the server at all - front-end JavaScript takes something from the URL and assigns it to innerHTML. The main fix is output encoding at render time, and it must be context-aware, which is also why encoding belongs at output rather than input: when the data arrives you do not yet know where it will end up.

面試時可回答：XSS 發生在應用程式取用使用者輸入後，沒有做跳脫就放進頁面，於是瀏覽器把它解析成標記，而不是當成文字顯示。假設網站有個留言框：我輸入 Hello Matt，伺服器渲染出一個含有 Hello Matt 的 div，沒問題。攻擊者輸入一個裝著 alert('XSS') 的 script 標籤，伺服器一樣照放，這下瀏覽器看到的是一個真的 script 標籤，就把它執行了。沒有任何東西被闖入 —— 網站只是讓一段本該是 data 的字串變成了 code。alert 只是概念驗證。因為那段程式碼是在你網站的來源內執行，瀏覽器無法把它跟你自己的腳本分辨開來：它可以讀取頁面上的任何東西、讀 local storage 裡的 token、以已登入使用者的身分發送請求，或改寫登入表單來竊取密碼。標記 HttpOnly 的 cookie 能讓腳本讀不到 session ID，但腳本發出的請求，瀏覽器照樣會附上那個 cookie —— 所以 HttpOnly 擋的是鑰匙被複製，不是門被使用。它有三種類型，差別只在 payload 執行前待在哪裡。儲存型存在你的資料庫裡，對每個打開頁面的人都會觸發。反射型搭著網址進來又被回顯，所以受害者必須點一條精心構造的連結。DOM 型則完全不經過伺服器 —— 前端 JavaScript 從網址取值，然後指派給 innerHTML。主要修法是在渲染當下做輸出編碼，而且必須依情境而定；這也正是編碼屬於輸出端而非輸入端的原因：資料剛進來時，你還不知道它最後會去哪裡。

The sentence to remember is: **XSS is user input that should have stayed data being executed as code, inside your own origin.**

最值得記：**XSS 就是本該當 data 的使用者輸入，在你自己的來源裡被當成 code 執行了。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q22: What is the difference between a session and a cookie?](q22-session-vs-cookie.md) | [All 41 questions](../../README.md) | [Q27: What is CORS?](q27-cors.md) |
