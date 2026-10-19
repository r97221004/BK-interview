# Q13: What is data partitioning?

> Tests whether you can pick a partition key for a stated access pattern, and whether you know what partitioning makes harder.

**Part:** Databases | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [schema migration](../_glossary.md#schema-migration)

## In One Sentence

Partitioning is splitting one large table into smaller physical pieces, so a query only has to touch the piece that holds the rows it wants.

分割是把一張大表切成較小的實體片段，讓查詢只需要碰到真正存有目標資料的那一片。

## Answer Shape

Give the definition and the two reasons it exists - scanning less and spreading load - then separate vertical from horizontal splitting and name the three horizontal strategies with one example each. Spend your last block on choosing the partition key and on what partitioning makes worse, because anyone can list the strategies and only someone who has done it will mention the hot partition.

先給定義和它存在的兩個理由 —— 掃描更少、分散負載 —— 接著區分垂直與水平切分，並各舉一例說明三種水平策略。把最後一段留給分割鍵的選擇，以及分割會讓什麼變差，因為策略人人都列得出來，只有真的做過的人才會提到熱點分割。

## Full Spoken Answer

Data partitioning is the process of splitting a large dataset into smaller, more manageable pieces. It buys you two things. Queries touch less data, because the planner can eliminate every partition that cannot contain a matching row. And the pieces can sit on different disks or different servers, so the load spreads instead of concentrating on one hot table.

資料分割是把大型資料集切成較小、較好管理的片段的過程。它換來兩件事：查詢碰到的資料變少，因為查詢規劃器可以排除掉所有不可能含有符合資料的分割；以及這些片段可以放在不同磁碟或不同伺服器上，讓負載分散，而不是集中在一張熱門的表上。

The first split is vertical: move columns into a separate table, so a wide row becomes two narrow ones. Keeping a user's profile fields apart from their credentials is the usual example, and it helps when different columns are read on different paths. The other split is horizontal, which divides rows, and it comes in three flavors. Range partitioning splits on value ranges, such as orders from January to March in one partition and April to June in the next, and it suits time-series data. Hash partitioning applies a hash to the key and takes the remainder, which distributes evenly when keys have no natural ordering. List partitioning splits on discrete values such as region.

第一種切法是垂直的：把欄位搬到另一張表，讓一列寬資料變成兩列窄資料。把使用者的個人資料欄位和登入憑證分開是典型例子，當不同欄位是在不同路徑上被讀取時特別有用。另一種切法是水平的，切的是列，共有三種型態。範圍分割依照值的範圍切，例如一月到三月的訂單放一個分割、四月到六月放下一個，適合時間序列資料。雜湊分割對鍵套用雜湊函式再取餘數，當鍵沒有自然順序時能分布得很平均。清單分割則依離散值切分，例如依區域。

Sharding is horizontal partitioning taken across separate database servers rather than within one, and it is the only way to scale writes beyond a single machine. That is why Cassandra and MongoDB are built around it. The distinction worth stating is that partitioning inside one server is mostly a query-performance and maintenance tool, while sharding is a capacity decision with much larger consequences.

分片是把水平分割做到「跨不同資料庫伺服器」而不是在同一台之內，而它是把寫入擴充到單機以上的唯一方式，這也是 Cassandra 和 MongoDB 圍繞它設計的原因。值得說清楚的區分是：單機內的分割主要是查詢效能與維護的工具，而分片是一個容量決策，後果大得多。

The whole thing lives or dies on the partition key, which has to match how you actually query. Partition orders by date and a report over one month reads one partition; partition them by customer instead and the same report reads all of them. A key with skewed values produces a hot partition that receives most of the traffic and undoes the benefit entirely. And be honest about the costs: queries that span partitions get slower, a unique constraint across all partitions is hard or impossible, cross-shard joins and transactions may not exist at all, and repartitioning later is a migration, not a setting. One-line summary: pick the partition key wrong and you haven't actually partitioned anything - every query still touches every piece.

整件事的成敗全繫於分割鍵，而它必須符合你實際的查詢方式。用日期分割訂單，那麼一個月的報表只讀一個分割；改用客戶分割，同一份報表就要讀遍所有分割。分布偏斜的鍵會產生熱點分割，讓大部分流量都打在同一片上，好處完全被抵銷。同時也要誠實面對代價：跨分割的查詢會變慢、跨所有分割的唯一性限制很難甚至做不到、跨分片的 join 與交易可能根本不存在，而事後要重新分割是一次資料遷移，不是改個設定。濃縮成一句：分割鍵選錯，等於根本沒分割 —— 每個查詢還是得碰過每一片。

## Quick Reference

| Splits | Type | How It Works | Example | Best For |
|---|---|---|---|---|
| **Vertical** | Vertical Partitioning | Split columns into different tables to reduce row size. | `user_profile` vs `user_credentials` | Tables with many columns accessed separately |
| **Horizontal** | Range Partitioning | Split rows on value ranges, still on one server. | Orders from Jan–Mar in `partition_0`, Apr–Jun in `partition_1` | Time-series or range-based queries |
| **Horizontal** | Hash Partitioning | Apply a hash function to decide the partition. | `hash(user_id) % 4 → partition_0..3` | Evenly distributing load when keys are random |
| **Horizontal** | List Partitioning | Split rows on discrete values. | Partition by region: Asia, Europe, America | Categorized datasets |
| **Horizontal, across servers** | Sharding | Horizontal partitioning taken across separate database servers instead of within one. | Users 1–1M on `db1`, users 1M–2M on `db2` | Write volume that has outgrown a single machine |

## Interview Version

> Partitioning is splitting a large dataset into smaller, more manageable pieces, and it buys two things: queries touch less data, because the planner can eliminate every partition that cannot contain a matching row, and the pieces can sit on different disks or servers, so load spreads instead of concentrating on one hot table. The first split is vertical - move columns into a separate table, so a wide row becomes two narrow ones, which helps when different columns are read on different paths. The other is horizontal, which divides rows, in three flavours. Range partitioning splits on value ranges, such as orders by quarter, and suits time-series data. Hash partitioning applies a hash to the key and takes the remainder, distributing evenly when keys have no natural ordering. List partitioning splits on discrete values such as region. Sharding is horizontal partitioning taken across separate database servers rather than within one, and it is the only way to scale writes beyond a single machine - partitioning inside one server is mostly a query-performance and maintenance tool, while sharding is a capacity decision with much larger consequences. The whole thing lives or dies on the partition key, which has to match how you actually query: partition orders by date and a monthly report reads one partition; partition them by customer and the same report reads all of them. A skewed key produces a hot partition that receives most of the traffic and undoes the benefit entirely. And be honest about the costs - cross-partition queries get slower, a unique constraint across all partitions is hard or impossible, cross-shard joins and transactions may not exist, and repartitioning later is a migration, not a setting.

面試時可回答：分區是把一個大型資料集切成較小、較好管理的片段，它買到兩件事：查詢碰到的資料變少，因為查詢規劃器可以排除掉每一個不可能含有符合列的分區；而這些片段可以放在不同磁碟或不同伺服器上，於是負載被分散，而不是集中在一張很熱的表上。第一種切法是垂直的 —— 把欄位搬到另一張表，讓一列很寬的資料變成兩列窄的，這在不同欄位會被不同路徑讀取時很有用。另一種是水平的，切的是「列」，有三種形式。range 分區依值的範圍切，例如訂單按季分開，適合時間序列資料。hash 分區對鍵做雜湊再取餘數，在鍵沒有自然排序時能分布得很平均。list 分區則依離散的值切，例如地區。sharding 是把水平分區跨到不同的資料庫伺服器上，而不是在同一台裡面切，而且它是把寫入擴展到超越單一機器的唯一方法 —— 在單台伺服器內做分區，主要是查詢效能與維護的工具，sharding 則是一個後果大得多的容量決策。整件事的成敗全繫於分區鍵，而它必須符合你「實際上怎麼查」：把訂單按日期分區，一份月報只讀一個分區；改成按客戶分區，同一份報表就要讀遍所有分區。一個分布傾斜的鍵會造出一個接收大部分流量的熱分區，把好處完全抵銷掉。也要誠實面對成本 —— 跨分區的查詢會變慢、跨所有分區的唯一性約束很難甚至做不到、跨 shard 的 join 和交易可能根本不存在，而事後重新分區是一次資料遷移，不是改個設定。

The sentence to remember is: **Pick the partition key wrong and you have not partitioned anything - every query still touches every piece.**

最值得記：**分區鍵挑錯，你就等於什麼都沒分 —— 每個查詢還是碰到每一塊。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q12: What is data normalization?](q12-data-normalization.md) | [All 52 questions](../../README.md) | [Q14: What are the common application scenarios for Redis?](q14-redis-use-cases.md) |
