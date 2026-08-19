# Q19: How do you decide what to cache, and how do you invalidate it?

> Tests whether you treat caching as a design with failure modes rather than as a switch, and whether you can say what happens on a miss.

**Part:** Databases | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [redis](../_glossary.md#redis)

## In One Sentence

You cache data that is read far more often than it changes and expensive to produce, and you decide up front how a stale entry gets removed - by expiry, by explicit invalidation on write, or both.

你該快取的是「讀得遠比改得多、而且產生成本高」的資料；並且要事先決定過期的條目怎麼被移除 —— 靠存活時間、靠寫入時主動失效，或兩者並用。

## Answer Shape

Lead with the selection rule, because caching the wrong thing is the more common mistake and it sounds like an optimization while it is happening. Then give the two patterns by name and say what each does on a write. Spend real time on invalidation and on the failure modes, because anyone can describe a cache hit and only someone who has run one will mention the stampede.

先講「選什麼來快取」的規則，因為快取錯東西是更常見的錯誤，而且它發生時聽起來像是在做優化。接著把兩種模式點名，並說明各自在寫入時的行為。把時間真正花在失效與失敗模式上，因為快取命中誰都描述得出來，只有真的維運過的人才會提到快取雪崩。

## Full Spoken Answer

Anchor it on one page: a product page assembled from a five-table join - price, stock, reviews, images, recommendations - hit a thousand times a second, changed maybe once an hour. The first decision is whether that deserves a cache at all, and three properties have to hold together: read far more than written, expensive to produce, and tolerable if slightly stale. The product page passes all three. A user's account balance fails the third one outright - nobody wants to see their balance from thirty seconds ago - so it stays out of the cache no matter how often it's read.

用一個具體頁面貫穿整題：一個商品頁，要 join 五張表才能拼出來 —— 價格、庫存、評論、圖片、推薦 —— 每秒被讀一千次，大概一小時才變一次。第一個決策是這東西值不值得被快取，三個條件必須同時成立：讀遠多於寫、產生成本高、稍微過期也能接受。商品頁三關全過。使用者的帳戶餘額直接在第三關被刷掉 —— 沒人想看到三十秒前的餘額 —— 所以不管讀得多頻繁，它都不進快取。

Cache-aside is the default pattern and the one to describe first. For that product page: the app checks Redis for `product:42`, and on a miss it runs the five-table join, writes the result back with a one-hour TTL, and returns it. The cache never talks to the database itself, so it is simple and it degrades safely: if Redis is down, every request is a miss and the site gets slow, not broken. Write-through instead writes to the cache and the database together on every write, which keeps the two consistent at the cost of making writes slower and caching pages nobody may ever load.

cache-aside 是預設模式，也是該先描述的那一個。套進商品頁的例子：應用程式查 Redis 裡的 `product:42`，未命中時才真的去跑那個五表 join、把結果連同一小時的 TTL 寫回快取，再回傳。快取本身從不與資料庫對話，所以它很單純而且降級安全：Redis 掛掉時，每個請求都是未命中，網站會變慢，但不會壞。write-through 則是在每次寫入時同時寫進快取和資料庫，讓兩者保持一致，代價是寫入變慢，而且會快取到可能永遠沒人載入的頁面。

Invalidation is the part that decides whether the design is sound. A TTL alone is the simplest and most robust answer: the product page just expires every hour on its own, so a bug in your invalidation logic costs you an hour of staleness, not forever. Explicit invalidation on write is more precise - the moment the price changes, delete `product:42` - and it is where the hard bugs live, because the same product data often sits inside several cached shapes too: `product:42`, `category:5:products`, `search:results:shoes`. Forget to invalidate one of those and it shows the old price forever, TTL or not. The pragmatic combination is to invalidate explicitly on the writes you control and still keep a TTL underneath as a backstop for the ones you missed.

失效是決定這個設計健不健全的一環。單靠 TTL 是最簡單也最穩健的答案：商品頁每小時自己過期，所以你失效邏輯裡的 bug 頂多讓你錯一小時，不是永遠。寫入時主動失效更精確 —— 價格一改就立刻刪掉 `product:42` —— 而困難的 bug 都住在這裡，因為同一份商品資料常常也躺在好幾個不同形狀的快取裡：`product:42`、`category:5:products`、`search:results:shoes`。漏掉其中一個沒失效，它就會永遠顯示舊價格，TTL 也救不了它。務實的組合是：對你掌控得到的寫入做主動失效，同時在底下留一個 TTL，接住你漏掉的那些。

Then name the failure modes, because they are what separates experience from theory. Say this product goes viral and `product:42` gets hit ten thousand times a second right as its TTL expires - that's a stampede: every one of those requests misses at once and all ten thousand hit the database together, which can take it down. The fixes are a short lock so one request repopulates while the others wait for it, or staggering expiry with random jitter so a batch of keys never expires in the same instant. Memory is finite too, so once Redis fills up, the eviction policy decides what gets thrown out, and choosing it deliberately matters. And a cache should never be the only copy of anything: if losing Redis means losing the product's price rather than just losing speed, it was never a cache, it was a database with no durability. The rule to keep in your head: a cache is allowed to be wrong for a little while, never allowed to be the only copy of the truth.

接著把失敗模式點名，因為那正是經驗與理論的分野。假設這個商品爆紅，`product:42` 在 TTL 剛好過期的那一刻被打了每秒一萬次 —— 這就是快取雪崩：那一萬個請求同時未命中，一起打到資料庫，足以把它打垮。修法是用一個短暫的鎖讓一個請求去重建、其他請求等待，或是在過期時間上加隨機抖動，讓一批鍵不會在同一瞬間一起過期。記憶體也是有限的，所以 Redis 滿了之後，淘汰策略決定丟掉什麼，刻意挑選它很重要。而且快取永遠不該是任何東西的唯一副本：如果弄丟 Redis 代表弄丟了商品的價格，而不只是弄丟速度，那它從來就不是快取，而是一個沒有持久性的資料庫。記住這句話：快取可以允許自己錯一陣子，但絕對不能是真相唯一的副本。

## Quick Reference

**Cache the product page, not the account balance: read >> write, expensive to produce, okay if briefly stale.**

| | Cache-aside | Write-through |
|---|---|---|
| On a read | Check cache, miss → read DB → write cache → return | Check cache, always current |
| On a write | Write DB, then delete the key so the next read repopulates it | Write DB and cache together |
| If the cache is down | Every read is a miss - slow, not broken | Every write is slower |
| Wastes cache space on | Nothing - only what's actually read gets cached | Data nobody may ever read |

| Failure mode | What happens | Fix |
|---|---|---|
| **Stampede** | A hot key expires; every concurrent request misses and hits the DB at once | Short lock so one request repopulates, or jittered expiry so keys don't expire together |
| **Eviction** | Memory fills; something gets discarded | Choose the eviction policy deliberately, don't leave it to chance |
| **Cache as system of record** | Losing the cache means losing data, not just speed | It isn't a cache anymore - keep the database as the source of truth |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q14: What are the common application scenarios for Redis?](q14-redis-use-cases.md) | [All 40 questions](../../README.md) | [Q20: How do you change a database schema without downtime?](q20-schema-migrations.md) |
