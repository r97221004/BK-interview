# Q26: What is Cross-Site Request Forgery (CSRF)?

> Tests whether you can explain why the browser sends the cookie at all, and how CSRF differs from XSS.

**Part:** Security & Auth | **Importance:** 7/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [cookie](../_glossary.md#cookie), [session](../_glossary.md#session), [xss](../_glossary.md#xss), [query plan](../_glossary.md#query-plan)

## In One Sentence

CSRF is when an attacker's page causes your browser to send a real, fully authenticated request to another site, because the browser attaches that site's cookies automatically no matter who triggered the request.

CSRF 是攻擊者的頁面讓你的瀏覽器對另一個網站送出一個真實且已通過認證的請求，因為不論是誰觸發的，瀏覽器都會自動附上那個網站的 cookie。

## Answer Shape

Explain the browser behavior that makes the attack possible before describing the attack itself, because the automatic cookie is the whole mechanism. Walk one concrete scenario end to end. Then contrast it with XSS in a single line, since the two are almost always asked together and confused. Finish with the defenses and say which one is the modern default.

在描述攻擊本身之前，先解釋讓攻擊得以成立的瀏覽器行為，因為「自動附上的 cookie」就是整個機制。完整走過一個具體情境。接著用一句話與 XSS 對照，因為這兩題幾乎總是一起問、也總是被混淆。最後講防禦手段，並說明哪一個是現代的預設。

## Full Spoken Answer

The mechanism starts with a browser behavior, not with a bug in your code. When any page causes a request to go to a domain, the browser attaches the cookies it holds for that domain automatically - it does not care which site initiated the request. That is convenient for you when the user navigates around your own site, and it is exactly what the attacker uses.

這個機制的起點是一個瀏覽器行為，而不是你程式碼裡的錯誤。當任何頁面觸發一個往某網域的請求時，瀏覽器都會自動附上它為該網域保存的 cookie —— 它不在乎是哪個網站發起的。使用者在你自己網站上瀏覽時這很方便，而這也正是攻擊者利用的地方。

So the attack goes like this. The victim is logged into a site, say their bank, and their session cookie is sitting in the browser. The attacker builds a page containing a hidden form or an image tag whose target is a state-changing endpoint on that bank. The victim visits the attacker's page, which submits the form automatically. The browser sends the request to the bank with the victim's session cookie attached, the bank sees a valid authenticated request, and it performs the transfer. Notice that the attacker never reads the response and never steals the cookie - they only need the action to happen.

所以攻擊是這樣進行的。受害者已登入某個網站，比方說他的銀行，session cookie 就放在瀏覽器裡。攻擊者做一個頁面，裡面有一個隱藏表單或 image 標籤，目標是那家銀行上會改變狀態的 endpoint。受害者造訪攻擊者的頁面，表單自動送出。瀏覽器把請求連同受害者的 session cookie 一起送到銀行，銀行看到的是一個有效且已認證的請求，於是執行了轉帳。請注意：攻擊者從頭到尾沒有讀到回應，也沒有偷到 cookie —— 他只需要那個動作發生。

The one-line contrast with XSS is worth memorizing because they are asked back to back. CSRF abuses the user's ambient authority: the attacker cannot read your responses, only cause requests. XSS abuses your application's output handling: the attacker gets code running inside your origin and can read everything. CSRF is about the browser's credentials; XSS is about your escaping. And note that XSS defeats every CSRF defense, because a script running on your own page can simply read the token.

和 XSS 的一句話對照值得背下來，因為它們常被連著問。CSRF 濫用的是使用者的「環境權限」：攻擊者讀不到你的回應，只能促使請求發生。XSS 濫用的是你的應用程式輸出處理：攻擊者取得在你來源內執行的程式碼，什麼都讀得到。CSRF 談的是瀏覽器的憑證，XSS 談的是你的跳脫。另外要注意：XSS 會擊破所有 CSRF 防禦，因為在你自己頁面上執行的腳本可以直接把 token 讀出來。

The classic defense is a CSRF token: the server puts an unpredictable value into the form or the page, the client returns it with the request, and the server checks it matches what it issued. The attacker cannot read it across origins, so they cannot forge a valid request. The double-submit cookie variant sends the same token in both a cookie and a request parameter and compares them, which avoids server-side storage. The modern default, though, is the SameSite cookie attribute, which tells the browser not to attach the cookie to cross-site requests at all - Lax, now the default in major browsers, already blocks the cross-site POST that this attack depends on. Checking the Origin or Referer header is a reasonable extra layer, and none of it helps if the endpoint performs a state change in response to a GET.

經典的防禦是 CSRF token：伺服器在表單或頁面中放入一個不可預測的值，客戶端隨請求送回，伺服器檢查它是否與自己簽發的一致。攻擊者無法跨來源讀取它，因此偽造不出有效請求。雙重提交 cookie 的變體則把同一個 token 同時放在 cookie 和請求參數中並比對兩者，藉此免去伺服器端儲存。不過現代的預設是 SameSite cookie 屬性，它告訴瀏覽器根本不要把 cookie 附加到跨站請求上 —— 目前主流瀏覽器預設的 Lax，就已經擋住了這個攻擊所依賴的跨站 POST。檢查 Origin 或 Referer 標頭是合理的額外一層，而如果某個 endpoint 會因為一個 GET 就改變狀態，以上全部都救不了它。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q24: Describe how session management works in web applications.](q24-session-management.md) | [All 41 questions](../../README.md) | [Q33: Explain the underlying data structures of lists, sets, tuples, and dictionaries in Python.](../architecture-and-scaling/q33-python-builtin-data-structures.md) |
