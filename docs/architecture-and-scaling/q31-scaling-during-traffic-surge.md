# Q31: How would you scale a backend application during a traffic surge?

> Tests whether you can name the bottleneck before the remedy, and whether you know the database is usually the real limit.

**Part:** Architecture & Scaling | **Importance:** 9/10 | **Status:** Complete

**New to these terms?** [statelessness](../_glossary.md#statelessness), [index](../_glossary.md#index), [cache](../_glossary.md#cache), [rate limiting](../_glossary.md#rate-limiting), [connection pool](../_glossary.md#connection-pool)

## In One Sentence

You add more identical instances behind a load balancer, keep them interchangeable by holding no state locally, and put a cache in front of whatever the extra instances would otherwise hammer.

做法是在 load balancer 後面加開更多一模一樣的實例、透過不在本機保存狀態讓它們可互換，並在那些新實例原本會打爆的東西前面加一層快取。

## Answer Shape

Name the bottleneck before the remedy, because adding servers to a database-bound system makes it worse and saying so is the strongest sentence in this answer. Then let the bottleneck pick the fix - measure, match, shed: the app is out of CPU, scale it out; the database is the wall, take load off the database; work that does not need to happen now, put it on a queue. Say the statelessness that scaling out requires, and the connection limit that scaling out quietly runs into. Finish with shedding, because a system that degrades on purpose beats one that falls over.

先指出瓶頸再談對策，因為對一個受限於資料庫的系統加開伺服器只會更糟，而能說出這一點就是這題最強的一句話。接著讓瓶頸決定解法 —— 量測、對症、卸載：應用程式 CPU 不夠，就水平擴充；牆在資料庫，就幫資料庫減壓；不必現在做完的工作，就丟進佇列。要講出水平擴充所要求的無狀態，以及水平擴充會悄悄撞上的連線數上限。最後收在卸載，因為刻意降級的系統勝過直接倒下的系統。

## Full Spoken Answer

Put a number on it so the whole answer stays concrete: say normal peak is 1,000 requests a second and a surge pushes that to 8,000. The first thing is to find out which part of the system actually can't keep up, because the fix is completely different depending on the answer. If the app servers are just out of CPU, adding more of them fixes it today. If the database is the wall, adding more app servers only means more connections and more queries hitting that same wall - it makes things worse, faster. So before touching anything, I'd check where the 8,000 requests are actually spending their time: app CPU, the database, or some downstream API call. The bottleneck picks the fix, not the other way round.

用一個具體數字讓整個回答保持具體：假設平常尖峰是每秒 1,000 個請求，流量暴增後衝到每秒 8,000。第一件事是搞清楚系統裡到底是哪一塊撐不住，因為答案不同、對策就完全不同。如果只是應用伺服器 CPU 不夠，加開幾台今天就能解決。如果卡住的是資料庫，加開應用伺服器只會讓連線數和查詢數一起往同一道牆撞，只會讓事情更快變糟。所以在動手之前，我會先看這 8,000 個請求的時間到底花在哪 —— 應用程式 CPU、資料庫，還是某個下游 API。**是瓶頸決定解法，不是反過來。**

If it's the app, that's horizontal scaling. Run several copies of the backend behind a load balancer, and let an auto-scaling group add instances on CPU or request count, so capacity follows the traffic without anyone logging in at 3am. Put a CDN in front as well, so images, CSS, and JS are served from the edge and the instances spend their CPU only on real requests. The one condition is that the app has to be stateless - no request can depend on data sitting in one specific instance's memory, or the load balancer can't hand that request to any instance and pick correctly. So sessions, caches, in-process job state all move out to Redis, Memcached, or a shared database first; skip that and the instances stop being interchangeable, and the whole approach falls apart.

如果瓶頸在應用程式，那就是水平擴充。在 load balancer 後面跑好幾份一模一樣的後端，讓 auto-scaling group 依 CPU 或請求數自動加開實例，容量就會跟著流量走，不用有人半夜三點爬起來開機器。前面再擋一層 CDN，讓圖片、CSS、JS 直接從邊緣送出，實例的 CPU 只花在真正的請求上。唯一的條件是應用程式要無狀態 —— 沒有任何一個請求依賴某一台特定實例記憶體裡的資料，否則 load balancer 沒辦法隨便挑一台就正確處理。所以 session、快取、行程內的工作狀態，都要先搬到 Redis、Memcached 或共用資料庫；不搬的話，實例就不再可互換，整套做法直接垮掉。

If it's the database, more app instances are the wrong answer, so the job is to take load off the database. A cache in front of it means the same read doesn't hit the database twice - typically the single change with the best payoff during a surge. Then look at the slow queries: one query doing a full table scan is survivable at 1,000 a second and fatal at 8,000, and a missing index is often the whole problem. Read replicas soak up read traffic. And connection pooling stops a hundred app instances from each opening ten connections and burying a database that can only actually serve fifty at once - which is exactly the trap auto-scaling walks you into, because every new instance brings its own connections.

如果瓶頸在資料庫，加開應用實例就是錯的答案，要做的是幫資料庫減壓。資料庫前面加一層快取，代表同一筆讀取不會對資料庫打第二次 —— 這通常是流量暴增期間報酬率最高的單一改動。再來看慢查詢：一個全表掃描的查詢，每秒 1,000 次還撐得住，每秒 8,000 次就會致命，而少一個索引常常就是整個問題所在。唯讀副本可以吸收讀取流量。連線池則能避免一百個應用實例各自開十條連線，把一台其實只能同時服務五十條連線的資料庫活活埋掉 —— **這正是 auto-scaling 會把你帶進去的陷阱，因為每多開一台實例，就多帶一批連線。**

If the work itself doesn't have to happen right now - sending an email, generating a report - it goes onto a queue like RabbitMQ or Kafka, so a burst turns into a backlog that drains over the next few minutes instead of eight thousand requests timing out at once. And plan for the case where none of that is enough, because new instances and new caches both take time you may not have in the first minute of a spike. Apply backpressure on purpose - rate limiting and load shedding: reject some requests outright to keep serving the rest, and turn off non-essential features first - recommendations go dark, checkout stays up. A system that deliberately gets slower survives a surge; one that tries to serve every single request falls over completely.

如果工作本身不必現在做完 —— 寄一封信、產一份報表 —— 就丟進像 RabbitMQ 或 Kafka 這樣的佇列，讓一波突發流量變成接下來幾分鐘慢慢消化掉的積壓，而不是八千個請求同時逾時。最後，要為「以上全做了還是不夠」的情況做打算，因為開新實例和加快取都需要時間，而流量暴增的第一分鐘你可能根本沒有這個時間。刻意施加 backpressure —— 也就是速率限制與負載卸除：直接拒絕一部分請求，換取剩下的請求還能被正常服務，並優先關掉非必要功能 —— 推薦系統先關，結帳留著。刻意變慢的系統撐得過流量高峰；想服務每一個請求的系統，只會整個倒下。

## Quick Reference

### The skeleton to memorise

**Measure → Match → Shed**

Find the bottleneck, apply the fix that belongs to it, and degrade on purpose if that is still not enough. Do not jump to "add servers" before you know what is slow, which is what most answers do.

| Bottleneck | Fix | Why |
|---|---|---|
| **App** out of CPU | Horizontal scaling behind a load balancer, auto-scaling on CPU or request count, CDN for static assets | Only works if the app is stateless - sessions and caches must live in Redis, not in process |
| **Database** | Cache, query optimisation (slow queries, missing indexes), read replicas, connection pooling | More app instances only add connections and queries to the same wall |
| **Async work** piling up | Queue (RabbitMQ, Kafka) | A burst becomes a backlog that drains, not thousands of timeouts |
| **Still not enough** | Rate limit, shed load, turn off non-essential features | Capacity is finite; recommendations off, checkout up |

## Interview Version

> I would put a number on it to stay concrete: normal peak is a thousand requests a second and a surge pushes it to eight thousand. The first thing is to find out which part cannot keep up, because the fix differs completely. So I would check where those eight thousand requests spend their time - app CPU, the database, or a downstream call - and let that pick the fix. If the app is the bottleneck, I scale it horizontally: more instances behind a load balancer, auto-scaling adding them on CPU or request count, and a CDN so static assets never reach them. The one condition is that the app is stateless - sessions, caches, and in-process job state live in Redis or a shared database, or the instances stop being interchangeable. If the database is the bottleneck, adding app instances makes it worse, because each one brings more connections and more queries to the same wall. There I take load off the database instead: a cache so the same read does not hit it twice, fix the slow queries and missing indexes, read replicas for reads, and a connection pool so a hundred instances cannot bury a database that serves fifty connections. If the problem is work that does not need to happen now, like emails or reports, it goes on a queue, so a burst becomes a backlog that drains. And if all of that is still not enough, I rate limit and shed load on purpose - recommendations go dark, checkout stays up.

面試時可回答：我會給它一個數字好讓整段保持具體：正常尖峰是每秒一千個請求，一波突發把它推到八千。第一件事是找出到底哪一部分跟不上，因為解法完全不同。所以我會先看那八千個請求的時間花在哪 —— 應用程式 CPU、資料庫，還是某個下游呼叫 —— 讓瓶頸決定解法。如果瓶頸在應用層，就在 load balancer 後面做水平擴展，用自動擴展依 CPU 或請求數加實例，再用 CDN 讓靜態檔根本不打到它們。唯一的條件是應用必須無狀態 —— session、快取、行程內的工作狀態放在 Redis 或共用資料庫，否則實例就不再可以互換。如果瓶頸在資料庫，加應用實例反而更糟，因為每一台都帶來更多連線、更多查詢去撞同一面牆。這時候改成幫資料庫減壓：加快取讓同一個讀取不會打兩次、修掉慢查詢和缺少的索引、用唯讀副本吸收讀取，再用連線池避免一百台實例活埋一台只能服務五十條連線的資料庫。如果問題是不必現在做完的工作，像寄信或產報表，就丟進佇列，讓一波突發變成慢慢排空的積壓。要是這些全做了還是不夠，就刻意做速率限制與丟棄負載 —— 推薦功能先關掉，結帳留著。

The sentence to remember is: **A system that deliberately gets slower survives a surge; one that tries to serve every single request falls over completely.**

最值得記：**一個刻意讓自己變慢的系統撐得過突發流量；一個堅持要服務每一個請求的系統會整個倒下。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q23: How do you protect a server from SQL injection attacks?](../security-and-auth/q23-sql-injection.md) | [All 51 questions](../../README.md) | [Q32: Discuss multiprocessing, multithreading, and asynchronous I/O in Python.](q32-python-concurrency-models.md) |
