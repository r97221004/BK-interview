# Q62: How would you paginate a large collection endpoint?

> Tests whether you know offset pagination degrades on large tables and skips rows when the data shifts underneath the reader.

**Part:** API Design & Reliability | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [endpoint](../_glossary.md#endpoint), [index](../_glossary.md#index)

## In One Sentence

Offset pagination asks for page five by telling the database to skip the first eighty rows, which gets slower the deeper you go; cursor pagination asks for the rows after a specific one, which stays fast at any depth.

offset 分頁要第五頁的做法，是叫資料庫跳過前八十列，翻得越深越慢；cursor 分頁則是要「某一筆之後」的資料列，不論翻多深都一樣快。

## Answer Shape

Describe offset first because it is what everyone writes, then break it - the two problems are that deep offsets are slow and that concurrent inserts make rows skip or repeat. Introduce the cursor as the fix for both. Finish with when offset is still the right answer, because the confident answer is not 'always use cursors'.

先描述 offset，因為那是大家都會寫的做法，然後把它拆掉 —— 它有兩個問題：翻深了會慢，而且並行的新增會讓資料列被跳過或重複。接著把 cursor 當成這兩者的解法引入。最後說明什麼時候 offset 仍然是正確答案，因為有把握的回答不是「永遠用 cursor」。

## Full Spoken Answer

Offset pagination is the obvious implementation: the client asks for a page number and a size, and the query uses LIMIT and OFFSET. It is easy to build, it lets the user jump straight to page fifty, and it makes a total count and a page count natural to display. For a small or slowly-changing dataset it is completely fine, and reaching for anything cleverer would be premature.

offset 分頁是最直覺的實作：客戶端指定頁碼和每頁筆數，查詢用 LIMIT 和 OFFSET。它很好寫，讓使用者可以直接跳到第五十頁，也讓總筆數和總頁數很自然就能顯示。對小型或變動緩慢的資料集，它完全沒問題，這時候用更聰明的做法反而是過早優化。

It breaks in two ways as the table grows. The first is performance: OFFSET does not let the database skip work, it makes the database produce and discard those rows, so page one thousand reads twenty thousand rows to return twenty. The cost grows linearly with the page number, which is why deep pages time out while the first page is instant. The second is correctness under concurrency: if a new row is inserted at the top while the user is reading, every subsequent page shifts by one, so they see a row twice - and a deletion makes them miss one entirely. On an infinite-scroll feed that is a visible bug.

隨著資料表變大，它會從兩個方向壞掉。第一是效能：OFFSET 並不能讓資料庫跳過工作，而是讓資料庫把那些列產生出來再丟掉，所以第一千頁要讀兩萬列才能回傳二十列。成本隨頁碼線性成長，這就是為什麼第一頁瞬間回應、深頁卻會逾時。第二是並行下的正確性：如果使用者正在閱讀時最上面插入了一筆新資料，之後的每一頁都會位移一格，於是同一列被看到兩次 —— 而刪除則會讓他整個漏掉一列。在無限捲動的動態牆上，這是肉眼可見的錯誤。

Cursor pagination fixes both. Instead of a position, the client sends a pointer to the last row it saw, and the query becomes a filter on that value with a LIMIT - give me the twenty rows after this one. That uses the index directly and reads only what it returns, so page one thousand costs the same as page one, and inserts elsewhere in the table cannot shift the window. The cursor must be built on a stable, unique, indexed ordering, which usually means a timestamp plus the primary key as a tiebreaker, and it is normally opaque-encoded so clients do not depend on its internals. The trade is that you lose jumping to an arbitrary page and a cheap total count. So the honest rule is: cursor pagination for feeds, infinite scroll, and any API over a large or busy table; offset pagination for admin tables and small datasets where the user genuinely wants page numbers.

cursor 分頁把兩個問題都修好了。客戶端送的不是位置，而是一個指向「它看到的最後一列」的指標，查詢就變成對那個值的篩選加上 LIMIT —— 給我這一筆之後的二十列。這會直接用到索引，而且只讀取它要回傳的部分，所以第一千頁和第一頁成本相同，資料表其他地方的插入也不可能讓視窗位移。cursor 必須建立在穩定、唯一且有索引的排序上，通常意味著用時間戳加上主鍵當作決勝欄位，而且一般會做不透明編碼，避免客戶端依賴它的內部結構。取捨是你失去了跳到任意頁碼的能力，也失去了便宜的總筆數。所以誠實的原則是：動態牆、無限捲動，以及任何架在大型或高流量資料表上的 API 用 cursor 分頁；管理後台的表格和使用者真的想要頁碼的小型資料集用 offset 分頁。

## Quick Reference

| | Offset pagination | Cursor pagination |
|---|---|---|
| **Request** | Page number and size | A pointer to the last row seen |
| **Query** | `LIMIT 20 OFFSET 19980` | `WHERE (created_at, id) < (?, ?) LIMIT 20` |
| **Deep page cost** | Grows linearly - the skipped rows are still produced | Constant - the index is seeked directly |
| **Concurrent inserts** | Rows shift; the reader repeats or skips one | Unaffected - the window is anchored to a row |
| **Jump to page N** | Yes | No, sequential only |
| **Total count** | Cheap to show | Expensive or omitted |
| **Best for** | Admin tables, small or stable datasets | Feeds, infinite scroll, large or busy tables |

## Interview Version

> Offset pagination is the obvious implementation: the client asks for a page number and a size, and the query uses LIMIT and OFFSET. It is easy to build, it lets the user jump straight to page fifty, and it makes a total count natural to display - for a small or slowly-changing dataset it is completely fine, and reaching for anything cleverer would be premature. It breaks in two ways as the table grows. The first is performance: OFFSET does not let the database skip work, it makes the database produce and discard those rows, so page one thousand reads twenty thousand rows to return twenty. The cost grows linearly with the page number, which is why deep pages time out while the first page is instant. The second is correctness under concurrency: if a new row is inserted at the top while the user is reading, every subsequent page shifts by one, so they see a row twice - and a deletion makes them miss one entirely. On an infinite-scroll feed that is a visible bug. Cursor pagination fixes both. Instead of a position, the client sends a pointer to the last row it saw, and the query becomes a filter on that value with a LIMIT - give me the twenty rows after this one. That uses the index directly and reads only what it returns, so page one thousand costs the same as page one, and inserts elsewhere cannot shift the window. The cursor must be built on a stable, unique, indexed ordering, usually a timestamp plus the primary key as a tiebreaker, and is normally opaque-encoded so clients do not depend on its internals. The trade is losing arbitrary page jumps and a cheap total count.

面試時可回答：offset 分頁是最直覺的實作：客戶端要求一個頁碼和一個頁面大小，查詢用 LIMIT 和 OFFSET。它很好做，讓使用者可以直接跳到第五十頁，也讓總筆數自然地可以顯示 —— 對小型或變動緩慢的資料集，它完全沒問題，去找更聰明的做法反而是過早最佳化。隨著表格變大，它會從兩個方向壞掉。第一個是效能：OFFSET 並不讓資料庫「跳過」工作，它是讓資料庫把那些列產生出來再丟掉，所以第一千頁要讀兩萬列才能回傳二十列。成本隨頁碼線性成長，這正是為什麼深頁會逾時、而第一頁卻是瞬間的。第二個是並行下的正確性：如果使用者正在閱讀時有一筆新資料插到最上面，之後的每一頁都會位移一列，於是他會看到某一列兩次 —— 而一次刪除則會讓他完全漏掉一列。在無限捲動的動態牆上，那是一個看得見的 bug。cursor 分頁把兩者都修好。客戶端送的不是「位置」，而是一個指向它看到的最後一列的指標，查詢因而變成「對那個值做篩選再加上 LIMIT」—— 給我這一列之後的二十列。這直接使用索引，而且只讀它要回傳的東西，所以第一千頁和第一頁一樣便宜，而在表格別處的插入也無法讓視窗位移。cursor 必須建立在一個穩定、唯一、有索引的排序上，通常是時間戳加上主鍵當決勝欄位，而且一般會做不透明編碼，讓客戶端不去依賴它的內部結構。代價是失去任意跳頁和便宜的總筆數。

The sentence to remember is: **OFFSET does not skip work - it makes the database build those rows and throw them away, so cursor pagination for feeds, offset for admin tables.**

最值得記：**OFFSET 並不會跳過工作 —— 它是讓資料庫把那些列做出來再丟掉；所以動態牆用 cursor，後台管理表用 offset。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q52: What tools and techniques do you use for debugging a backend application?](../testing-and-debugging/q52-debugging-a-backend-application.md) | [All 51 questions](../../README.md) | [Q63: How do you make an endpoint safe to retry?](q63-idempotency-and-retries.md) |
