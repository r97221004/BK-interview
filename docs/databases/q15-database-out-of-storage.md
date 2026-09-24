# Q15: What strategies do you have when a database runs out of storage?

> Tests whether you can separate the emergency response from the structural fix, and whether you monitor for this before it happens.

**Part:** Databases | **Importance:** 6/10 | **Status:** Complete

**New to these terms?** [session](../_glossary.md#session), [partitioning](../_glossary.md#partitioning), [sharding](../_glossary.md#sharding), [index](../_glossary.md#index)

## In One Sentence

When a database runs out of storage it is an incident first and a design problem second: find out what is actually consuming the disk, reclaim enough space to keep serving, then fix the growth pattern that got you there.

資料庫空間用盡時，它首先是一次事故，其次才是設計問題：先查清楚磁碟到底被什麼佔滿、回收足夠的空間讓服務繼續運作，再去修正把你帶到這一步的成長模式。

## Answer Shape

Separate the emergency from the fix, and lead with the emergency, because a database that is full is usually refusing writes right now. Say what you would measure before you delete anything. Then move through reclaiming, growing, and splitting in that order, and finish with the monitoring that means this never becomes an incident again.

把緊急處理和根本修正分開，而且從緊急處理講起，因為一個滿了的資料庫此刻通常正在拒絕寫入。說明你在刪掉任何東西之前會先量測什麼。接著依序帶過回收、擴大、切分，最後收在讓這件事不再成為事故的監控上。

## Full Spoken Answer

The first move is to find out what is actually full, because the fix differs completely by cause. Table data, index data, transaction or write-ahead logs, temporary sort files, and old backups all live on the same disk and any of them can be the one that filled it. A runaway log or an unrotated audit table is a far more common cause than genuine data growth, and it is also much faster to fix, so measuring first saves you from deleting production data under pressure.

第一步是查清楚到底是什麼把空間佔滿了，因為不同成因的處理方式完全不同。資料表資料、索引資料、交易或預寫日誌、暫存排序檔、舊備份，全都放在同一顆磁碟上，任何一項都可能是元凶。失控的日誌或沒有輪替的稽核表遠比真正的資料成長更常見，而且修起來也快得多，所以先量測能避免你在壓力下刪掉正式環境的資料。

Then reclaim. Archive historical or rarely accessed rows to cheaper storage, delete genuinely obsolete records such as expired sessions, soft-deleted rows past their retention, and old temporary data, and make sure logs are rotated and purged on a schedule rather than by hand. Drop indexes that are unused or redundant, since every index costs disk and slows every write to its table. One thing to say explicitly: on most engines a DELETE marks space reusable but does not return it to the operating system, so a vacuum, a table rebuild, or a partition drop is what actually gives the disk back.

接著回收。把歷史或很少存取的資料列封存到較便宜的儲存、刪除真正過時的紀錄（過期 session、超過保留期的軟刪除資料、舊的暫存資料），並確保日誌是照排程輪替與清除，而不是靠人工。移除沒在用或重複的索引，因為每個索引都佔磁碟，也讓那張表的每次寫入變慢。有一點要明講：在大多數引擎上，DELETE 只是把空間標記為可重用，並不會把它還給作業系統，真正把磁碟還回來的是 vacuum、重建資料表，或直接卸除一個分割。

If the data is legitimate and simply larger than the disk, grow. Adding disk space to the current server is the simplest step, and most managed databases such as RDS or Azure SQL support expanding storage without downtime, some automatically. This buys time rather than solving anything, so it should come with a decision about what changes before the next threshold is reached.

如果資料是正當的，只是單純比磁碟大，那就擴大。替現有伺服器加磁碟是最簡單的一步，而大多數託管資料庫（例如 RDS 或 Azure SQL）都支援不停機擴充儲存，有些還能自動擴充。這只是爭取時間、並沒有真正解決問題，所以應該同時決定「在下一次觸及門檻之前要改變什麼」。

The structural fixes are partitioning and storage efficiency. Partitioning by time turns deleting last year's data into dropping a partition, which is instant and returns the space immediately, where deleting a hundred million rows one by one would be slow and would not even give the disk back. Sharding spreads rows across servers when one machine genuinely cannot hold them, but it belongs at the end of the list rather than in the middle, because it makes joins, transactions, query routing, and rebalancing all harder - you take that complexity on only when the limit is real capacity and not a retention policy you never wrote. Alongside that, choose smaller data types where the range allows it, enable row or page compression if the engine supports it, and set an explicit retention policy per table so the growth has a ceiling by design.

結構性的修正是分割與儲存效率。用時間分割能把「刪除去年資料」變成「卸除一個分割」，瞬間完成而且立刻把空間還回來；相對地，一列一列刪掉一億筆資料既慢，而且根本不會把磁碟還給你。當一台機器真的再也裝不下時，才用分片把資料列分散到多台伺服器，但它應該排在清單的最後、而不是中間，因為分片會讓 join、交易、查詢路由和資料重新平衡全部變難 —— 只有在限制真的是實體容量，而不是「你從來沒寫過的保留政策」時，才值得扛下這份複雜度。除此之外，在範圍允許的情況下選用較小的資料型別、在引擎支援時啟用列或頁壓縮，並為每張表設定明確的保留政策，讓成長從設計上就有天花板。

None of this should be discovered at a hundred percent. Alert at seventy and eighty percent of capacity, track the growth rate rather than only the level so you can see the wall coming, and watch the things that actually turn into incidents: the largest tables, the largest indexes, and the size of the write-ahead log. Indexes bloat the same way tables do, so sometimes what reclaims the space is a rebuild rather than anything you delete. Apply quotas so one table or one tenant cannot consume everything. The order to remember, plainly: find it, free it, buy time, fix it - and set up alarms so you're never doing this at 100% again.

這一切都不該是在百分之百時才發現。在容量的百分之七十和八十就告警、追蹤成長「速率」而不只是水位，好讓你能看見那面牆正在接近，並盯住真正會演變成事故的那幾項：最大的資料表、最大的索引，以及預寫日誌的大小。索引和資料表一樣會膨脹，所以有時候真正把空間拿回來的是重建索引，而不是你刪掉了什麼。再設定配額，讓單一資料表或單一租戶無法把空間吃光。說白了記住這個順序：先找出來、再騰空間、再爭取時間、最後才修根本，並且設好告警，讓自己再也不會在百分之百的時候才發現。

## Interview Version

> It is an incident first and a design problem second. The first move is to find out what is actually full, because the fix differs completely by cause: table data, index data, transaction or write-ahead logs, temporary sort files, and old backups all live on the same disk, and a runaway log or an unrotated audit table is a far more common cause than genuine data growth - and much faster to fix. Measuring first is what stops you deleting production data under pressure. Then reclaim: archive historical rows to cheaper storage, delete genuinely obsolete records such as expired sessions and soft-deleted rows past retention, make sure logs rotate on a schedule, and drop unused or redundant indexes, since every index costs disk and slows every write to its table. One thing to say explicitly is that on most engines a DELETE marks space reusable but does not return it to the operating system, so a vacuum, a table rebuild, or a partition drop is what actually gives the disk back. If the data is legitimate and simply larger than the disk, grow it - most managed databases expand storage without downtime - but that buys time rather than solving anything, so it should come with a decision about what changes before the next threshold. The structural fixes are partitioning and storage efficiency: partitioning by time turns deleting last year's data into dropping a partition, which is instant and returns space immediately, and an explicit retention policy per table gives the growth a ceiling by design. Sharding spreads rows when one machine genuinely cannot hold them, but it comes last, because it makes joins, transactions, routing, and rebalancing all harder. Finally, none of this should be discovered at a hundred percent - alert at seventy and eighty, track the growth rate rather than only the level so you can see the wall coming, and watch the largest tables, the largest indexes, and the write-ahead log, since indexes bloat too and sometimes a rebuild is what reclaims the space.

面試時可回答：這件事首先是一起事故，其次才是設計問題。第一步是找出到底是什麼把空間佔滿了，因為不同成因的解法完全不同：表格資料、索引資料、交易或 write-ahead 日誌、暫存排序檔、舊備份，全都住在同一顆磁碟上，而失控的日誌或沒有輪替的稽核表，遠比真正的資料成長更常見 —— 而且修起來快得多。先量測，正是讓你不會在壓力下刪掉正式資料的原因。接著回收空間：把歷史資料歸檔到更便宜的儲存、刪掉真正過時的紀錄（例如過期的 session、超過保留期的軟刪除列）、確保日誌按排程輪替，並移除沒在用或重複的索引，因為每個索引都佔磁碟，也讓對該表的每一次寫入變慢。有一點要明講：在大多數引擎上，DELETE 只是把空間標記為可重用，並不會把它還給作業系統，所以真正把磁碟還回來的是 vacuum、重建表，或直接 drop 一個分區。如果資料是正當的、只是單純比磁碟大，那就擴容 —— 大多數受管資料庫都能不停機擴充儲存 —— 但那是買時間，不是解決問題，所以它應該伴隨一個決定：在下一個門檻到來之前，要改變什麼。結構性的解法是分區和儲存效率：按時間分區能把「刪除去年的資料」變成「drop 一個分區」，瞬間完成並立刻歸還空間；而每張表明確的保留政策，能讓成長從設計上就有天花板。當一台機器真的再也裝不下時，才用 sharding 把列分散出去，而且它排在最後，因為 sharding 會讓 join、交易、路由和重新平衡全部變難。最後，這一切都不該是在 100% 的時候才發現 —— 在 70% 和 80% 就告警，追蹤成長「速率」而不只是「水位」，並盯住最大的表、最大的索引和 write-ahead 日誌，因為索引一樣會膨脹，有時候真正拿回空間的是重建索引。

The sentence to remember is: **Find it, free it, buy time, fix it - and a DELETE does not give the disk back; a vacuum or a dropped partition does.**

最值得記：**找出來、清出來、買時間、修根因 —— 而 DELETE 不會把磁碟還你，vacuum 或 drop 一個分區才會。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q73: When would you use composition instead of inheritance?](../code-design/q73-composition-vs-inheritance.md) | [All 48 questions](../../README.md) | [Q34: How do you ensure your backend code is maintainable and easy to understand?](../architecture-and-scaling/q34-maintainable-backend-code.md) |
