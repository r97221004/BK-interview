# Q18: What is the N+1 query problem, and how do you fix it?

> Tests whether you can spot the most common performance bug in ORM-backed code, and whether you would have noticed it before production did.

**Part:** Databases | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [orm](../_glossary.md#orm)

## In One Sentence

The N+1 problem is running one query to fetch a list and then one more query for each item in it, so displaying a hundred rows quietly costs a hundred and one round trips to the database.

N+1 問題是先用一個查詢取回一份清單，接著為清單中的每一筆各再查一次；於是顯示一百列，悄悄付出了一百零一次資料庫往返。

## Answer Shape

Give the shape of the bug and then immediately say why it is invisible, because that is the real point: the application code looks completely innocent. Use a concrete loop as the example. Then give the fix in the language you actually use, and finish with how you would catch it before production does.

先給出這個 bug 的形狀，然後立刻說明它為什麼看不見，因為那才是重點：應用程式碼看起來完全人畜無害。用一個具體的迴圈當例子。接著用你實際使用的語言給出修法，最後說明你會怎麼在正式環境發現它之前就抓到它。

## Full Spoken Answer

The name describes the shape. One query fetches N parent rows, then the code touches a related object on each of them, and each touch issues its own query - so the total is N+1. Fetching fifty blog posts and then printing each author's name runs one query for the posts and fifty more for the authors. Each query is individually fast, which is exactly why it hides: nothing in the slow-query log looks wrong, and the page is simply slow.

這個名字描述的就是它的形狀。一個查詢取回 N 筆父層資料列，接著程式碼在每一筆上碰了一個關聯物件，而每一次碰觸都各自發出一個查詢 —— 所以總數是 N+1。取五十篇文章、再印出每篇作者的名字，會跑一個查詢拿文章、再跑五十個拿作者。每一個查詢單獨看都很快，這正是它藏得住的原因：慢查詢日誌裡沒有任何一筆看起來有問題，只是頁面就是慢。

The reason it is so common is that ORMs make it invisible by design. Lazy loading means an attribute lookup that reads exactly like plain attribute access is actually a database round trip, so the loop that causes it contains no visible query at all. It also scales with the data rather than with the code, so it passes review, passes tests against a seed database of ten rows, and only becomes an incident when a real customer has ten thousand.

它之所以這麼常見，是因為 ORM 在設計上就讓它隱形。惰性載入代表一次看起來就像普通屬性存取的取值，實際上是一次資料庫往返，所以造成問題的那個迴圈裡根本看不到任何查詢。而且它的規模隨資料而不是隨程式碼成長，因此它能通過程式碼審查、能通過只有十筆種子資料的測試，直到某個真實客戶有一萬筆時才變成事故。

The fix is to tell the ORM what you are going to need, so it fetches it in one or two queries instead of N. In Django that is select_related for a forward foreign key, which becomes a JOIN, and prefetch_related for reverse or many-to-many relations, which issues a second query and stitches the results together in Python. SQLAlchemy has the same split as joinedload and selectinload. To catch it rather than wait for it, log the generated SQL in development, assert on query counts in tests for endpoints that return collections, and watch queries-per-request as a metric in production - a number that climbs with the size of the response is this bug.

修法是預先告訴 ORM 你接下來會需要什麼，讓它用一到兩個查詢取回，而不是 N 個。在 Django 中，正向外鍵用 select_related，它會變成 JOIN；反向或多對多關聯用 prefetch_related，它會發出第二個查詢再在 Python 端把結果縫合起來。SQLAlchemy 有相同的區分，對應 joinedload 和 selectinload。若要主動抓到而不是被動等它爆發：在開發環境把產生的 SQL 記錄下來、對會回傳集合的 endpoint 在測試中斷言查詢次數，並在正式環境把「每個請求的查詢數」當成指標監看 —— 一個會隨回應大小上升的數字，就是這個 bug。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q17: Explain database transactions and isolation levels.](q17-transactions-and-isolation-levels.md) | [All 37 questions](../../README.md) | [Q23: How do you protect a server from SQL injection attacks?](../security-and-auth/q23-sql-injection.md) |
