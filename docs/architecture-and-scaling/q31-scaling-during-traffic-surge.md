# Q31: How would you scale a backend application during a traffic surge?

> Tests whether you can name the bottleneck before the remedy, and whether you know the database is usually the real limit.

**Part:** Architecture & Scaling | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [statelessness](../_glossary.md#statelessness), [redis](../_glossary.md#redis), [rate limiting](../_glossary.md#rate-limiting), [message queue](../_glossary.md#message-queue), [timeout](../_glossary.md#timeout)

## In One Sentence

You add more identical instances behind a load balancer, keep them interchangeable by holding no state locally, and put a cache in front of whatever the extra instances would otherwise hammer.

做法是在 load balancer 後面加開更多一模一樣的實例、透過不在本機保存狀態讓它們可互換，並在那些新實例原本會打爆的東西前面加一層快取。

## Answer Shape

Name the bottleneck before the remedy, because adding servers to a database-bound system makes it worse and saying so is the strongest sentence in this answer. Then follow the skeleton - measure, reduce, scale out, shed - which is deliberately in cost order: finding the bottleneck is free, caching is cheap, machines cost money, and shedding load costs you users. Spend your time on the middle two and mention the statelessness that scaling out requires. Finish with shedding, because a system that degrades on purpose beats one that falls over.

先指出瓶頸再談對策，因為對一個受限於資料庫的系統加開伺服器只會更糟，而能說出這一點就是這題最強的一句話。接著照骨架走 —— 量測、減量、擴充、卸載 —— 這個順序是刻意按成本排的：找瓶頸不用錢、快取很便宜、開機器要花錢、卸載流量則是拿使用者去換。把時間花在中間兩項，並提到擴充所要求的無狀態。最後收在卸載，因為刻意降級的系統勝過直接倒下的系統。

## Full Spoken Answer

The first thing is to know what is actually saturated, because the remedy differs completely. If the application servers are CPU-bound, more instances help immediately. If the database is the constraint, adding application instances increases the connection count and the query rate and makes the outage arrive sooner. So the honest opening is that I would look at where the time is going - application CPU, database, or a downstream dependency - before scaling anything.

第一件事是搞清楚到底是什麼飽和了，因為對策完全不同。如果應用伺服器受限於 CPU，加開實例會立刻有幫助。如果瓶頸在資料庫，加開應用實例只會增加連線數和查詢速率，讓事故來得更快。所以誠實的開場是：在擴充任何東西之前，我會先看時間花在哪裡 —— 應用程式 CPU、資料庫，還是某個下游相依服務。

The standard remedy is horizontal scaling: run several instances of the backend behind a load balancer and add more as traffic rises, which in a cloud environment an auto-scaling group does automatically based on CPU, memory, or request metrics. This only works if the application is stateless, meaning no request depends on data held in one instance's memory. Anything stateful - sessions, caches, in-process job state - has to move to external storage such as Redis, Memcached, or a shared database, or the instances stop being interchangeable and the whole approach collapses.

標準對策是水平擴充：在 load balancer 後面跑多個後端實例，並隨流量上升再加開；在雲端環境中，auto-scaling group 會依 CPU、記憶體或請求量指標自動完成這件事。這只有在應用程式無狀態時才行得通，也就是沒有任何請求依賴某一台實例記憶體裡的資料。任何有狀態的東西 —— session、快取、行程內的工作狀態 —— 都必須搬到外部儲存，例如 Redis、Memcached 或共用資料庫，否則實例就不再可互換，整套做法會直接瓦解。

Then reduce the work that reaches the origin at all. A CDN serves static assets from the edge and removes the largest and dullest slice of traffic before it arrives. A cache layer in front of the database holds frequently read data so repeated queries never run twice, which is usually the single highest-leverage change during a surge. On the database itself, read replicas absorb read traffic, and connection pooling stops a hundred application instances from opening a thousand connections into a server that can serve fifty.

接著減少真正抵達來源站的工作量。CDN 從邊緣提供靜態資源，在流量抵達之前就先移除掉最大也最無趣的那一塊。資料庫前面的快取層保存常被讀取的資料，讓重複查詢不必跑第二次，這通常是流量暴增期間單一槓桿最大的改動。在資料庫端，唯讀副本可以吸收讀取流量，而連線池能避免一百個應用實例對一台只能服務五十條連線的伺服器開出一千條連線。

Finally, decide what to do when demand still exceeds capacity, because scaling is never instant. Move work that does not have to be synchronous onto a queue such as RabbitMQ or Kafka, so a burst becomes a backlog that drains instead of a wall of timeouts. Apply rate limiting and load shedding so the system rejects some requests deliberately and keeps serving the rest, and degrade non-essential features first - recommendations off, checkout up. A system that gets slower in a controlled way survives a surge; one that tries to serve everything falls over completely.

最後，決定在需求仍然超過容量時該怎麼辦，因為擴充從來不是瞬間完成的。把不必同步處理的工作丟到像 RabbitMQ 或 Kafka 這樣的佇列上，讓突發變成會慢慢消化的積壓，而不是一整面逾時的牆。套用速率限制與負載卸除，讓系統刻意拒絕一部分請求以維持服務其餘的請求，並優先降級非必要功能 —— 關掉推薦、保住結帳。以受控方式變慢的系統能撐過流量高峰；試圖服務所有請求的系統則會徹底倒下。

## Quick Reference

### The skeleton to memorise

**Measure → Reduce → Scale out → Shed**

Deliberately in cost order. Do not skip to step three, which is what most answers do.

| Step | What you do | Why it comes here |
|---|---|---|
| **Measure** | Find the actual bottleneck: app CPU, database, or a downstream call | Free. And if the database is the limit, step three makes it worse |
| **Reduce** | CDN for static assets, cache in front of the database, read replicas, connection pooling | Cheapest real win - work that never reaches the origin costs nothing to serve |
| **Scale out** | More instances behind a load balancer, auto-scaling on CPU or request metrics | Costs money, and only works if the app is stateless - sessions and caches must live in Redis, not in process |
| **Shed** | Queue what can be async, rate limit, degrade non-essential features first | Capacity is finite; recommendations off, checkout up |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q23: How do you protect a server from SQL injection attacks?](../security-and-auth/q23-sql-injection.md) | [All 41 questions](../../README.md) | [Q32: Discuss multiprocessing, multithreading, and asynchronous I/O in Python.](q32-python-concurrency-models.md) |
