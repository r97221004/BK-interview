# Q16: What is a database index, and how do you work out why a query is slow?

> The highest-value database question there is. Tests whether you can reason from the access path rather than guess, and whether you know an index is not free.

**Part:** Databases | **Importance:** 10/10 | **Status:** Complete

## In One Sentence

An index is a separate sorted structure that lets the database jump straight to the rows a query wants instead of reading the whole table, and a query is slow when it cannot use one.

索引是一個獨立的排序結構，讓資料庫能直接跳到查詢要的資料列，而不必讀完整張表；當查詢用不到索引時，它就會慢。

## Answer Shape

Define the index by what it replaces - a full table scan - and say what it costs, because an index that is free is an index you have not thought about. Then answer the second half as a method: read the query plan, do not guess. Finish with the reasons an index exists but goes unused, since that is where real slow queries actually live.

用它取代了什麼來定義索引 —— 全表掃描 —— 並說出它的代價，因為「免費的索引」代表你沒想清楚。接著把後半段當成一套方法來回答：看查詢計畫，不要用猜的。最後講「索引存在卻沒被用到」的原因，因為真實世界的慢查詢大多住在那裡。

## Full Spoken Answer

An index is a secondary structure, almost always a B-tree, holding the indexed columns in sorted order along with a pointer to the row. Other types exist for what sorted order cannot serve, such as GIN for searching inside JSON documents or full text, but a B-tree is what you get unless you ask for something else. Without one the database performs a sequential scan: it reads every row and discards the ones that do not match, so the cost grows linearly with the table. With one it descends the tree, which is logarithmic, so a lookup in a ten-million-row table takes a handful of page reads instead of reading all ten million rows.

索引是一個附屬結構，幾乎都是 B-tree，它把被索引的欄位依序排好，並附上指向資料列的指標。另外還有一些型別是為「排序解決不了的事」而存在的，例如用來搜尋 JSON 文件內部或全文檢索的 GIN；但除非你特別指定，拿到的就是 B-tree。沒有索引時資料庫會做循序掃描：讀過每一列、丟掉不符合的，成本隨資料表線性成長。有索引時它會沿著樹往下走，成本是對數的，所以在一千萬列的表裡查一筆，只需要少數幾次分頁讀取，而不是把一千萬列全部讀過一遍。

Indexes are not free, and saying so is half the answer. Every index is extra disk, and every insert and delete, plus every update that touches an indexed column, has to maintain that index, so write throughput falls as index count rises. That is why the useful question is never whether to add an index but which queries justify which indexes. For composite indexes the column order matters: an index on customer and then date serves a filter on customer alone, and a filter on customer plus date, but not a filter on date alone - the leftmost prefix rule. The same structure gives you the other half of the trick: if the index also carries the columns being selected, the database can answer from the index alone and never touch the table, which is an index-only or covering scan.

索引不是免費的，把這點講出來就答對了一半。每個索引都佔額外磁碟，而每次新增與刪除、以及每次動到被索引欄位的更新，都必須維護那個索引，所以索引越多寫入吞吐越低。這也是為什麼真正該問的從來不是「要不要加索引」，而是「哪些查詢值得哪些索引」。複合索引的欄位順序很重要：一個先客戶、後日期的索引，能服務「只篩客戶」和「客戶加日期」，但不能服務「只篩日期」—— 這就是最左前綴原則。同一個結構也給了你另外半個訣竅：如果索引本身還帶著要被選出來的欄位，資料庫就能只讀索引作答、完全不必回表，這就是 index-only scan，也叫覆蓋索引。

For the slow query itself, the method is to look rather than guess. Run EXPLAIN, or EXPLAIN ANALYZE to get real timings, and read the access path: a sequential scan on a large table is the usual culprit, and you are also looking at the estimated versus actual row counts, because a large gap means the planner's statistics are stale and it chose badly. The database's own slow-query log tells you which statements are actually costing time, which is regularly not the ones you suspected.

面對慢查詢本身，方法是「去看」而不是「用猜的」。跑 EXPLAIN，或用 EXPLAIN ANALYZE 取得實際耗時，然後讀它的存取路徑：大表上的循序掃描通常就是元凶；同時也要看預估列數與實際列數的差距，差太多代表規劃器的統計資訊過期，因而選錯了計畫。資料庫自己的慢查詢日誌會告訴你哪些敘述句真正在耗時，而那經常不是你原本懷疑的那些。

The most useful thing to know is why an index exists and still goes unused. Wrapping the column in a function, such as filtering on the lowercased email, defeats the index unless you built a matching expression index. A leading wildcard in a LIKE pattern cannot use a B-tree. A type mismatch between the column and the parameter forces a cast and therefore a scan. And when a query returns a large fraction of the table, the planner correctly decides a scan is cheaper than millions of index lookups plus row fetches - in that case the fix is to return less data, not to add another index.

最有用的一件事，是知道「索引明明存在卻沒被用到」的原因。把欄位包在函式裡（例如對轉成小寫的 email 做篩選）會讓索引失效，除非你另外建了對應的運算式索引。LIKE 樣式開頭是萬用字元時，B-tree 用不上。欄位與參數型別不符會強制轉型，因而變成掃描。而當查詢會回傳整張表的一大部分時，規劃器正確地判斷「掃描比幾百萬次索引查找加上取列更便宜」—— 這種情況該修的是「少回傳一點資料」，而不是再加一個索引。

## Quick Reference

### Reading a plan

The same query before and after an index, from `EXPLAIN ANALYZE`:

```text
Seq Scan on orders  (cost=0.00..18334.00 rows=142 width=64)
                    (actual time=0.412..96.233 rows=137 loops=1)
  Filter: (customer_id = 42)
  Rows Removed by Filter: 999863
Execution Time: 96.410 ms
```

```text
Index Scan using orders_customer_id_idx on orders
                    (cost=0.42..268.44 rows=142 width=64)
                    (actual time=0.021..0.058 rows=137 loops=1)
  Index Cond: (customer_id = 42)
Execution Time: 0.079 ms
```

Three things to read, in this order:

| Look at | It says | Act when |
|---|---|---|
| The node type | `Seq Scan` reads everything; `Index Scan` seeks; `Index Only Scan` never touches the table | A `Seq Scan` sits on a large table inside a selective query |
| `rows=` estimated against `rows=` actual | Whether the planner knew what it was choosing between | They differ by orders of magnitude - the statistics are stale, so run `ANALYZE` |
| `Rows Removed by Filter` | How much work was thrown away after being read | It dwarfs the rows returned, as the 999863 above does |

### An index exists and is still unused

| What the query does | Why the index is skipped | Fix |
|---|---|---|
| `WHERE lower(email) = $1` | The column is wrapped in a function, so the stored order no longer applies to it | An expression index on `lower(email)` |
| `WHERE name LIKE '%smith'` | A leading wildcard leaves no prefix for a B-tree to seek to | A trigram or full-text index |
| `WHERE id = '42'` with an integer column | The type mismatch forces a cast on the column side | Correct the parameter type in the application |
| `WHERE date = $1` on an index over `(customer, date)` | `date` is not the leftmost column | Reorder the columns, or add an index led by `date` |
| Returns a large share of the table | Nothing is wrong: a scan really is cheaper than millions of lookups plus row fetches | Return less data - filter harder or paginate; another index will not help |

## Interview Version

> An index is a secondary structure, almost always a B-tree, holding the indexed columns in sorted order along with a pointer to the row. Without one the database performs a sequential scan - it reads every row and discards the ones that do not match - so cost grows linearly with the table. With one it descends the tree, which is logarithmic, so a lookup in a ten-million-row table takes a handful of page reads instead of ten million. Indexes are not free, and saying so is half the answer: every index is extra disk, and every insert, delete, and update touching an indexed column has to maintain it, so write throughput falls as index count rises. The useful question is never whether to add an index but which queries justify which indexes. For composite indexes the column order matters - an index on customer then date serves a filter on customer alone and on customer plus date, but not on date alone, which is the leftmost prefix rule. The same structure gives the other half of the trick: if the index also carries the selected columns, the database answers from the index alone and never touches the table. For the slow query itself the method is to look rather than guess: run EXPLAIN ANALYZE and read the access path, watching for a sequential scan on a large table and for a large gap between estimated and actual row counts, which means the planner's statistics are stale. The most useful thing to know is why an index exists and still goes unused - wrapping the column in a function defeats it, a leading wildcard in LIKE cannot use a B-tree, a type mismatch forces a cast and therefore a scan, and when a query returns a large fraction of the table the planner correctly prefers a scan, in which case the fix is to return less data, not to add another index.

面試時可回答：索引是一個次要結構，幾乎總是 B-tree，它以排序好的順序保存被索引的欄位，並附帶指向該列的指標。沒有索引時，資料庫會做循序掃描 —— 讀過每一列，再把不符合的丟掉 —— 所以成本隨表格大小線性成長。有索引時，它沿著樹往下走，那是對數的，所以在一張一千萬列的表裡查一筆，只需要少數幾次分頁讀取，而不是讀完一千萬列。索引不是免費的，而把這件事說出口就答對了一半：每個索引都是額外的磁碟，而每一次 insert、delete，以及每一次觸及被索引欄位的 update，都必須維護它，所以索引數量上升，寫入吞吐量就下降。有用的問題從來不是「要不要加索引」，而是「哪些查詢值得哪些索引」。對複合索引來說欄位順序很重要 —— 一個先 customer 後 date 的索引，可以服務「只篩 customer」和「篩 customer 加 date」，但無法服務「只篩 date」，這就是最左前綴規則。同一個結構也給了你另一半的訣竅：如果索引本身也帶著被選取的欄位，資料庫就能只靠索引回答、完全不必碰那張表。至於那個慢查詢本身，方法是「去看」而不是「用猜的」：跑 EXPLAIN ANALYZE 並讀出存取路徑，留意大表上的循序掃描，以及預估列數與實際列數之間的巨大落差 —— 那代表查詢規劃器的統計資訊過期了。最有用的知識，是理解「索引明明存在卻沒被用到」的原因：把欄位包在函式裡會讓它失效、LIKE 的前置萬用字元用不了 B-tree、欄位與參數型別不符會強制轉型因而變成掃描；而當一個查詢會回傳表格中很大一部分時，規劃器正確地判斷掃描比較便宜 —— 這時候的解法是「回傳更少資料」，不是再加一個索引。

The sentence to remember is: **The question is never whether to index, but which queries justify which index - and an unused index still slows every write.**

最值得記：**問題從來不是「要不要加索引」，而是「哪些查詢值得哪個索引」—— 而一個沒人用的索引，照樣拖慢每一次寫入。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q11: Can you explain the difference between SQL and NoSQL databases?](q11-sql-vs-nosql.md) | [All 41 questions](../../README.md) | [Q21: What is the difference between session-based and JWT-based authentication?](../security-and-auth/q21-session-vs-jwt-authentication.md) |
