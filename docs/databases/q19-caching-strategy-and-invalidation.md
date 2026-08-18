# Q19: How do you decide what to cache, and how do you invalidate it?

> Tests whether you treat caching as a design with failure modes rather than as a switch, and whether you can say what happens on a miss.

**Part:** Databases | **Importance:** 8/10 | **Status:** Draft

## In One Sentence

You cache data that is read far more often than it changes and expensive to produce, and you decide up front how a stale entry gets removed - by expiry, by explicit invalidation on write, or both.

你該快取的是「讀得遠比改得多、而且產生成本高」的資料；並且要事先決定過期的條目怎麼被移除 —— 靠存活時間、靠寫入時主動失效，或兩者並用。

## Answer Shape

Lead with the selection rule, because caching the wrong thing is the more common mistake and it sounds like an optimization while it is happening. Then give the two patterns by name and say what each does on a write. Spend real time on invalidation and on the failure modes, because anyone can describe a cache hit and only someone who has run one will mention the stampede.

先講「選什麼來快取」的規則，因為快取錯東西是更常見的錯誤，而且它發生時聽起來像是在做優化。接著把兩種模式點名，並說明各自在寫入時的行為。把時間真正花在失效與失敗模式上，因為快取命中誰都描述得出來，只有真的維運過的人才會提到快取雪崩。

## Full Spoken Answer

The first decision is what deserves a cache at all. Three properties have to hold together: the data is read much more often than it is written, producing it is expensive - a multi-table join, an external API call, a computed aggregate - and the caller can tolerate the data being slightly out of date. If any one of those is missing, caching either buys nothing or introduces a correctness bug. A user's account balance fails the third test; a product catalogue passes all three.

第一個決策是「什麼東西值得被快取」。三個條件必須同時成立：這份資料讀的次數遠多於寫、產生它的成本很高（多表 join、外部 API 呼叫、計算出來的彙總），而且呼叫端能容忍資料稍微過期。只要少了任何一項，快取要嘛毫無收益，要嘛引入正確性的錯誤。使用者的帳戶餘額過不了第三關，商品目錄則三關全過。

Cache-aside is the default pattern and the one to describe first. The application checks the cache, and on a miss it reads the database, writes the value back with a time to live, and returns it. The cache never talks to the database itself, so it is simple and it degrades safely: if the cache is down, every request is a miss and the system is slow rather than broken. Write-through instead writes to the cache and the database together on every write, which keeps the two consistent at the cost of making writes slower and caching data nobody may ever read.

cache-aside 是預設模式，也是該先描述的那一個。應用程式先查快取，未命中時去讀資料庫、把值連同存活時間寫回快取，再回傳。快取本身從不與資料庫對話，所以它很單純而且降級安全：快取掛掉時，每個請求都是未命中，系統會變慢但不會壞。write-through 則是在每次寫入時同時寫進快取和資料庫，讓兩者保持一致，代價是寫入變慢，而且會快取到可能永遠沒人讀的資料。

Invalidation is the part that decides whether the design is sound. A time to live is the simplest and most robust answer: every entry expires on its own, so a bug in your invalidation logic costs you staleness for a bounded window rather than forever. Explicit invalidation on write is more precise - delete the key when the underlying row changes - and it is where the hard bugs live, because one piece of data often sits inside several cached shapes and forgetting one of them leaves a permanently wrong entry. The pragmatic combination is to invalidate explicitly on the writes you control and still set a TTL underneath as a backstop.

失效是決定這個設計健不健全的一環。存活時間是最簡單也最穩健的答案：每個條目都會自己過期，所以你失效邏輯裡的 bug 只會讓你在一個有界的時間窗內拿到舊資料，而不是永遠。寫入時主動失效更精確 —— 底層資料列改變時就刪掉那個鍵 —— 而困難的 bug 都住在這裡，因為同一份資料常常存在於好幾個不同形狀的快取條目裡，漏掉其中一個就留下一筆永遠錯誤的資料。務實的組合是：對你掌控得到的寫入做主動失效，同時在底下仍然設一個 TTL 當保險。

Then name the failure modes, because they are what separates experience from theory. A stampede happens when a popular key expires and every concurrent request misses at once and hits the database together; the fixes are a short lock so one request repopulates while the others wait, or staggering expiry with a random jitter so a batch of keys does not expire simultaneously. Memory is finite, so the eviction policy decides what is discarded when it fills, and choosing it deliberately matters. And a cache should never be the only copy of anything: if losing it means losing data rather than losing speed, it is not a cache, it is a database with no durability.

接著把失敗模式點名，因為那正是經驗與理論的分野。快取雪崩發生在一個熱門的鍵過期時，所有並行請求同時未命中、一起打到資料庫；修法是用一個短暫的鎖讓一個請求去重建、其他請求等待，或是在過期時間上加隨機抖動，讓一批鍵不會同時到期。記憶體是有限的，所以淘汰策略決定了滿了之後丟掉什麼，刻意挑選它很重要。而且快取永遠不該是任何東西的唯一副本：如果弄丟它代表弄丟資料而不是弄丟速度，那它就不是快取，而是一個沒有持久性的資料庫。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q14: What are the common application scenarios for Redis?](q14-redis-use-cases.md) | [All 41 questions](../../README.md) | [Q20: How do you change a database schema without downtime?](q20-schema-migrations.md) |
