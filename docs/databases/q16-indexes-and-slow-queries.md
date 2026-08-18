# Q16: What is a database index, and how do you work out why a query is slow?

> The highest-value database question there is. Tests whether you can reason from the access path rather than guess, and whether you know an index is not free.

**Part:** Databases | **Importance:** 10/10 | **Status:** Draft

## In One Sentence

An index is a separate sorted structure that lets the database jump straight to the rows a query wants instead of reading the whole table, and a query is slow when it cannot use one.

索引是一個獨立的排序結構，讓資料庫能直接跳到查詢要的資料列，而不必讀完整張表；當查詢用不到索引時，它就會慢。

## Answer Shape

Define the index by what it replaces - a full table scan - and say what it costs, because an index that is free is an index you have not thought about. Then answer the second half as a method: read the query plan, do not guess. Finish with the reasons an index exists but goes unused, since that is where real slow queries actually live.

用它取代了什麼來定義索引 —— 全表掃描 —— 並說出它的代價，因為「免費的索引」代表你沒想清楚。接著把後半段當成一套方法來回答：看查詢計畫，不要用猜的。最後講「索引存在卻沒被用到」的原因，因為真實世界的慢查詢大多住在那裡。

## Full Spoken Answer

An index is a secondary structure, almost always a B-tree, holding the indexed columns in sorted order along with a pointer to the row. Without one the database performs a sequential scan: it reads every row and discards the ones that do not match, so the cost grows linearly with the table. With one it descends the tree, which is logarithmic, so a lookup in a ten-million-row table takes a handful of page reads instead of ten million.

索引是一個附屬結構，幾乎都是 B-tree，它把被索引的欄位依序排好，並附上指向資料列的指標。沒有索引時資料庫會做循序掃描：讀過每一列、丟掉不符合的，成本隨資料表線性成長。有索引時它會沿著樹往下走，成本是對數的，所以在一千萬列的表裡查一筆，只需要少數幾次分頁讀取，而不是一千萬次。

Indexes are not free, and saying so is half the answer. Every index is extra disk, and every insert, update, or delete has to maintain every index on that table, so write throughput falls as index count rises. That is why the useful question is never whether to add an index but which queries justify which indexes. For composite indexes the column order matters: an index on customer and then date serves a filter on customer alone, and a filter on customer plus date, but not a filter on date alone - the leftmost prefix rule.

索引不是免費的，把這點講出來就答對了一半。每個索引都佔額外磁碟，而每次新增、更新、刪除都必須維護那張表上的每一個索引，所以索引越多寫入吞吐越低。這也是為什麼真正該問的從來不是「要不要加索引」，而是「哪些查詢值得哪些索引」。複合索引的欄位順序很重要：一個先客戶、後日期的索引，能服務「只篩客戶」和「客戶加日期」，但不能服務「只篩日期」—— 這就是最左前綴原則。

For the slow query itself, the method is to look rather than guess. Run EXPLAIN, or EXPLAIN ANALYZE to get real timings, and read the access path: a sequential scan on a large table is the usual culprit, and you are also looking at the estimated versus actual row counts, because a large gap means the planner's statistics are stale and it chose badly. The database's own slow-query log tells you which statements are actually costing time, which is regularly not the ones you suspected.

面對慢查詢本身，方法是「去看」而不是「用猜的」。跑 EXPLAIN，或用 EXPLAIN ANALYZE 取得實際耗時，然後讀它的存取路徑：大表上的循序掃描通常就是元凶；同時也要看預估列數與實際列數的差距，差太多代表規劃器的統計資訊過期，因而選錯了計畫。資料庫自己的慢查詢日誌會告訴你哪些敘述句真正在耗時，而那經常不是你原本懷疑的那些。

The most useful thing to know is why an index exists and still goes unused. Wrapping the column in a function, such as filtering on the lowercased email, defeats the index unless you built a matching expression index. A leading wildcard in a LIKE pattern cannot use a B-tree. A type mismatch between the column and the parameter forces a cast and therefore a scan. And when a query returns a large fraction of the table, the planner correctly decides a scan is cheaper than millions of index lookups plus row fetches - in that case the fix is to return less data, not to add another index.

最有用的一件事，是知道「索引明明存在卻沒被用到」的原因。把欄位包在函式裡（例如對轉成小寫的 email 做篩選）會讓索引失效，除非你另外建了對應的運算式索引。LIKE 樣式開頭是萬用字元時，B-tree 用不上。欄位與參數型別不符會強制轉型，因而變成掃描。而當查詢會回傳整張表的一大部分時，規劃器正確地判斷「掃描比幾百萬次索引查找加上取列更便宜」—— 這種情況該修的是「少回傳一點資料」，而不是再加一個索引。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q11: Can you explain the difference between SQL and NoSQL databases?](q11-sql-vs-nosql.md) | [All 41 questions](../../README.md) | [Q21: What is the difference between session-based and JWT-based authentication?](../security-and-auth/q21-session-vs-jwt-authentication.md) |
