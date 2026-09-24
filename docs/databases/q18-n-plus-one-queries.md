# Q18: What is the N+1 query problem, and how do you fix it?

> Tests whether you can spot the most common performance bug in ORM-backed code, and whether you would have noticed it before production did.

**Part:** Databases | **Importance:** 9/10 | **Status:** Complete

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

Plainly, it is so common because the ORM hides the query behind normal-looking code. `post.author.name` inside the loop reads exactly like touching a plain field - nothing in that line looks like a database call, so there is no query for you to spot by eye. And the bug's size tracks the data, not the code: with ten seed rows in a test it's ten extra queries and nobody notices; with ten thousand real rows it's the same one line of code, just suddenly slow. Slogan to keep in your head: every time a loop touches a *relationship* field, not a plain field, that touch is a hidden query - one per row.

直白地說，它會這麼常見，是因為 ORM 把查詢藏在看起來很普通的程式碼後面。迴圈裡的 `post.author.name` 讀起來就跟存取一個普通欄位一樣 —— 這一行完全看不出是在打資料庫，所以沒有任何「查詢」能讓你用肉眼抓到。而且這個 bug 的規模是跟著資料量走，不是跟著程式碼走：測試用十筆種子資料，就只是多十次查詢，沒人會注意；換成真實客戶一萬筆，還是同一行程式碼，只是突然變慢。記住這句口訣：迴圈裡只要碰到的是「關聯欄位」而不是「普通欄位」，那一碰就是一次藏起來的查詢 —— 一筆資料一次。

The fix, in plain terms, is to tell the ORM up front "I'll need the author too," so it grabs everything in one or two queries instead of one-per-row. In Django that's `select_related` for a forward foreign key (turns into a JOIN) and `prefetch_related` for reverse or many-to-many (a second query, stitched together in Python). SQLAlchemy has the same two-way split as `joinedload` and `selectinload`. To catch it before production does: log the generated SQL in development, assert on query counts in tests for any endpoint returning a collection, and watch queries-per-request as a production metric - a number that climbs with response size is this exact bug.

修法說白了就是先告訴 ORM「我等一下也會要作者的資料」，讓它一次或兩次查詢就把東西都撈回來，而不是一筆資料查一次。在 Django 裡，正向外鍵用 `select_related`（會變成 JOIN）；反向或多對多用 `prefetch_related`（多發一次查詢，再由 Python 把結果拼起來）。SQLAlchemy 對應同一種二分法：`joinedload` 和 `selectinload`。想在正式環境爆掉之前就抓到它：開發環境把產生的 SQL 印出來看、對會回傳一整批資料的 endpoint 在測試裡斷言查詢次數、在正式環境把「每個請求的查詢數」當成指標監看 —— 只要這個數字會隨回應筆數一起往上爬，就是這個 bug。

## Interview Version

> The name describes the shape: one query fetches N parent rows, then the code touches a related object on each of them and each touch issues its own query, so the total is N+1. Fetching fifty blog posts and then printing each author's name runs one query for the posts and fifty more for the authors. Each query is individually fast, which is exactly why it hides - nothing in the slow-query log looks wrong, the page is simply slow. It is so common because the ORM hides the query behind normal-looking code: post.author.name inside a loop reads exactly like touching a plain field, so there is no query to spot by eye. And the bug's size tracks the data rather than the code - ten seed rows in a test means ten extra queries and nobody notices; ten thousand real rows is the same one line, just suddenly slow. The rule I keep in my head is that every time a loop touches a relationship field rather than a plain field, that touch is a hidden query, one per row. The fix is to tell the ORM up front that you will need the author too, so it fetches everything in one or two queries instead of one per row - in Django that is select_related for a forward foreign key, which becomes a JOIN, and prefetch_related for reverse or many-to-many, which is a second query stitched together in Python; SQLAlchemy has the same split as joinedload and selectinload. To catch it before production does: log the generated SQL in development, assert on query counts in tests for any endpoint returning a collection, and watch queries-per-request as a production metric, because a number that climbs with response size is this exact bug.

面試時可回答：這個名字描述的就是它的形狀：一個查詢抓回 N 筆父層資料，接著程式碼在每一筆上碰觸一個關聯物件，而每一次碰觸都發出自己的查詢，所以總數是 N+1。抓五十篇文章然後印出每位作者的名字，會跑一個查詢抓文章、再跑五十個查詢抓作者。每一個查詢單獨看都很快，這正是它藏得住的原因 —— 慢查詢日誌裡什麼都不奇怪，頁面就只是慢。它之所以這麼常見，是因為 ORM 把查詢藏在看起來很正常的程式碼後面：迴圈裡的 post.author.name 讀起來就跟碰一個普通欄位一模一樣，你用眼睛根本抓不到那裡有查詢。而且這個 bug 的大小跟著資料走，不是跟著程式碼走 —— 測試裡十筆種子資料就是多十個查詢，沒人會注意；一萬筆真實資料是同樣那一行程式碼，只是突然變慢了。我記住的規則是：迴圈裡每一次碰觸的是「關聯欄位」而不是普通欄位，那一次碰觸就是一個隱藏查詢，每列一個。解法是事先告訴 ORM「我也會需要作者」，讓它用一到兩個查詢把所有東西抓齊，而不是每列一個 —— 在 Django 裡，正向外鍵用 select_related（會變成 JOIN），反向或多對多用 prefetch_related（第二個查詢，在 Python 裡縫起來）；SQLAlchemy 有同樣的兩分法，叫 joinedload 和 selectinload。要在正式環境之前抓到它：在開發環境把產生的 SQL 記錄下來、對任何回傳集合的 endpoint 在測試裡斷言查詢次數，並把「每個請求的查詢數」當成正式環境的指標來看 —— 一個會隨回應大小往上爬的數字，就是這個 bug。

The sentence to remember is: **Every time a loop touches a relationship field instead of a plain field, that touch is a hidden query - one per row.**

最值得記：**迴圈裡每一次碰的是「關聯欄位」而不是普通欄位，那一下就是一個隱藏查詢 —— 每列一個。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q17: Explain database transactions and isolation levels.](q17-transactions-and-isolation-levels.md) | [All 47 questions](../../README.md) | [Q23: How do you protect a server from SQL injection attacks?](../security-and-auth/q23-sql-injection.md) |
