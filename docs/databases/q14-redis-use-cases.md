# Q14: What are the common application scenarios for Redis?

> Tests whether you know why an in-memory store is used for these jobs, and what you lose by putting data there.

**Part:** Databases | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [session](../_glossary.md#session), [rate limiting](../_glossary.md#rate-limiting), [cache-aside](../_glossary.md#cache-aside), [cache stampede](../_glossary.md#cache-stampede), [message queue](../_glossary.md#message-queue)

## In One Sentence

Redis is an in-memory data-structure store, so it is used wherever you need an answer in well under a millisecond and can afford to lose or rebuild that data: caching, sessions, rate limits, queues, and leaderboards.

Redis 是一個記憶體內的資料結構儲存系統，因此凡是需要遠低於一毫秒就拿到答案、而且那份資料可以遺失或重建的地方都會用到它：快取、session、速率限制、佇列與排行榜。

## Answer Shape

Say what Redis actually is first - not just a cache, but a set of data structures held in memory - because that single framing explains every use case that follows. Then give the two everyone expects, caching and sessions, and two that show more range, such as rate limiting and queues. Close with the constraint, since knowing that RAM is the budget and Redis is not your system of record is what distinguishes a real answer.

先說清楚 Redis 究竟是什麼 —— 不只是快取，而是一組放在記憶體裡的資料結構 —— 因為光是這個定位就能解釋接下來所有的使用情境。接著給出大家預期的兩個：快取與 session；再給兩個展現廣度的：速率限制與佇列。最後收在限制上，因為知道「記憶體就是預算」以及「Redis 不是你的權威資料來源」，才是真正答案與背誦的差別。

## Full Spoken Answer

Redis is an open-source, in-memory data store used as a cache, a database, and a message broker. Its speed comes from keeping data in RAM instead of on disk, but the part worth emphasizing is that it stores data structures, not just strings: hashes, lists, sets, sorted sets, and streams, each with atomic operations. Most of its use cases are really just the right structure combined with an expiry time.

Redis 是一個開源的記憶體內資料儲存系統，可以當快取、資料庫和訊息中介使用。它的速度來自把資料放在記憶體而非磁碟，但更值得強調的是：它儲存的是資料結構，不只是字串 —— 雜湊、串列、集合、有序集合和串流，每一種都附帶原子操作。它大多數的使用情境，其實就是「選對結構」再加上「設定過期時間」。

Caching is the most common. You store the result of an expensive query or an external API call under a key with a time to live, and serve subsequent reads from memory. The usual pattern is cache-aside: check Redis, and on a miss read the database and write the value back. The two decisions that actually matter are how entries expire and what happens on a miss, because a cache with no expiry policy eventually serves wrong data and a cache that stampedes on expiry can take the database down.

快取是最常見的用途。你把昂貴查詢或外部 API 呼叫的結果存在某個鍵底下並設定存活時間，之後的讀取就直接由記憶體提供。常見模式是 cache-aside：先查 Redis，未命中時才讀資料庫並把值寫回去。真正重要的兩個決策是「條目怎麼過期」和「未命中時怎麼辦」，因為沒有過期策略的快取最終會提供錯誤資料，而在過期瞬間發生大量穿透的快取則可能把資料庫打垮。

Session storage is the second. Putting session data in Redis instead of in one server's memory is what lets several application instances share login state, so any instance can serve any request and a deploy does not log everyone out. Beyond those two, an atomic increment with an expiry is a complete rate limiter, sorted sets give you a leaderboard ranked on write, lists and streams work as job queues, and the pub/sub and stream features let you fan events out to several consumers.

第二個是 session 儲存。把 session 資料放在 Redis 而不是某一台伺服器的記憶體裡，才能讓多個應用實例共用登入狀態，於是任何一台實例都能服務任何請求，部署時也不會把所有人踢下線。除了這兩者之外，一個原子遞增加上過期時間就是一個完整的速率限制器；有序集合讓排行榜在寫入時就完成排序；串列與串流可以當工作佇列；而 pub/sub 與串流功能則讓你把事件擴散給多個消費者。

The constraint is that memory is the budget. Your working set has to fit in RAM, and when it does not, the eviction policy decides what is thrown away, so choosing it deliberately matters. Persistence is available through snapshots and an append-only log, but both trade durability against performance, and neither makes Redis a safe system of record for data you cannot rebuild. The healthy default is to treat Redis as fast, disposable state in front of a database that holds the truth.

它的限制是「記憶體就是預算」。你的工作集必須放得進 RAM，放不下時就由淘汰策略決定丟掉什麼，所以刻意挑選那個策略很重要。持久化可以透過快照和 append-only 日誌達成，但兩者都是在耐久性與效能之間取捨，而且都不會讓 Redis 變成一個能安全存放「無法重建之資料」的權威來源。健康的預設是把 Redis 當成擺在資料庫前面的快速、可拋棄狀態，真相仍然存放在資料庫裡。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q13: What is data partitioning?](q13-data-partitioning.md) | [All 41 questions](../../README.md) | [Q19: How do you decide what to cache, and how do you invalidate it?](q19-caching-strategy-and-invalidation.md) |
