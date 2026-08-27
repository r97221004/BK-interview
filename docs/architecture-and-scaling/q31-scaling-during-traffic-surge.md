# Q31: How would you scale a backend application during a traffic surge?

> Tests whether you can name the bottleneck before the remedy, and whether you know the database is usually the real limit.

**Part:** Architecture & Scaling | **Importance:** 9/10 | **Status:** Complete

**New to these terms?** [statelessness](../_glossary.md#statelessness), [session](../_glossary.md#session), [cache](../_glossary.md#cache), [rate limiting](../_glossary.md#rate-limiting), [message queue](../_glossary.md#message-queue)

## In One Sentence

You add more identical instances behind a load balancer, keep them interchangeable by holding no state locally, and put a cache in front of whatever the extra instances would otherwise hammer.

做法是在 load balancer 後面加開更多一模一樣的實例、透過不在本機保存狀態讓它們可互換，並在那些新實例原本會打爆的東西前面加一層快取。

## Answer Shape

Name the bottleneck before the remedy, because adding servers to a database-bound system makes it worse and saying so is the strongest sentence in this answer. Then follow the skeleton - measure, reduce, scale out, shed - which is deliberately in cost order: finding the bottleneck is free, caching is cheap, machines cost money, and shedding load costs you users. Spend your time on the middle two and mention the statelessness that scaling out requires. Finish with shedding, because a system that degrades on purpose beats one that falls over.

先指出瓶頸再談對策，因為對一個受限於資料庫的系統加開伺服器只會更糟，而能說出這一點就是這題最強的一句話。接著照骨架走 —— 量測、減量、擴充、卸載 —— 這個順序是刻意按成本排的：找瓶頸不用錢、快取很便宜、開機器要花錢、卸載流量則是拿使用者去換。把時間花在中間兩項，並提到擴充所要求的無狀態。最後收在卸載，因為刻意降級的系統勝過直接倒下的系統。

## Full Spoken Answer

Put a number on it so the whole answer stays concrete: say normal peak is 1,000 requests a second and a surge pushes that to 8,000. The first thing is to find out which part of the system actually can't keep up, because the fix is completely different depending on the answer. If the app servers are just out of CPU, adding more of them fixes it today. If the database is the wall, adding more app servers only means more connections and more queries hitting that same wall - it makes things worse, faster. So before touching anything, I'd check where the 8,000 requests are actually spending their time: app CPU, the database, or some downstream API call.

用一個具體數字讓整個回答保持具體：假設平常尖峰是每秒 1,000 個請求，流量暴增後衝到每秒 8,000。第一件事是搞清楚系統裡到底是哪一塊撐不住，因為答案不同、對策就完全不同。如果只是應用伺服器 CPU 不夠，加開幾台今天就能解決。如果卡住的是資料庫，加開應用伺服器只會讓連線數和查詢數一起往同一道牆撞，只會讓事情更快變糟。所以在動手擴充之前，我會先看這 8,000 個請求的時間到底花在哪 —— 應用程式 CPU、資料庫，還是某個下游 API。

But the smarter move, usually before adding a single machine, is to shrink the 8,000 before it even reaches your servers. A CDN serves images, CSS, and JS straight from the edge, so a big dumb chunk of that traffic never touches your origin at all. A cache in front of the database means the same read doesn't hit the database twice - typically the single change with the best payoff during a surge. On the database itself, read replicas soak up read traffic, and connection pooling stops a hundred app instances from each opening ten connections and burying a database that can only actually serve fifty at once.

但更聰明的一步，通常是在加開任何一台機器之前，先想辦法把這 8,000 縮小，讓它根本不用打到你的伺服器。CDN 直接從邊緣提供圖片、CSS、JS，一大塊笨重的流量根本碰不到你的來源站。資料庫前面加一層快取，代表同一筆讀取不會對資料庫打第二次 —— 這通常是流量暴增期間報酬率最高的單一改動。在資料庫端，唯讀副本可以吸收讀取流量，連線池則能避免一百個應用實例各自開十條連線，把一台其實只能同時服務五十條連線的資料庫活活埋掉。

Say the app is still the bottleneck after all that - now it's horizontal scaling. Run several copies of the backend behind a load balancer, and add more as the remaining traffic keeps climbing; in the cloud, an auto-scaling group does that add-more-instances step automatically based on CPU or request count. The one condition is that the app has to be stateless - no request can depend on data sitting in one specific instance's memory, or the load balancer can't hand that request to any instance and pick correctly. So sessions, caches, in-process job state all move out to Redis, Memcached, or a shared database first; skip that and the instances stop being interchangeable, and the whole approach falls apart.

假設把能減的都減完，瓶頸還是在應用伺服器 —— 這時才輪到水平擴充。在 load balancer 後面跑好幾份一模一樣的後端，隨著剩下的流量持續往上爬再加開；在雲端環境，auto-scaling group 會依 CPU 或請求數自動完成「多開幾台」這件事。唯一的條件是應用程式要無狀態 —— 沒有任何一個請求依賴某一台特定實例記憶體裡的資料，否則 load balancer 沒辦法隨便挑一台就正確處理。所以 session、快取、行程內的工作狀態，都要先搬到 Redis、Memcached 或共用資料庫；不搬的話，實例就不再可互換，整套做法直接垮掉。

Finally, plan for the case where even that isn't enough, because scaling out and adding cache both take time you may not have in the first minute of a spike. Anything that doesn't have to happen synchronously - sending an email, generating a report - goes onto a queue like RabbitMQ or Kafka, so a burst turns into a backlog that drains over the next few minutes instead of eight thousand requests timing out at once. On top of that, apply backpressure on purpose - rate limiting and load shedding: reject some requests outright to keep serving the rest, and turn off non-essential features first - recommendations go dark, checkout stays up. A system that deliberately gets slower survives a surge; one that tries to serve every single request falls over completely.

最後，要為「就算做了以上全部，還是不夠」的情況做打算，因為擴充機器和加快取都需要時間，而流量暴增的第一分鐘你可能根本沒有這個時間。任何不必立刻同步完成的事 —— 寄一封信、產一份報表 —— 都丟進像 RabbitMQ 或 Kafka 這樣的佇列，讓一波突發流量變成接下來幾分鐘慢慢消化掉的積壓，而不是八千個請求同時逾時。除此之外，刻意施加 backpressure —— 也就是速率限制與負載卸除：直接拒絕一部分請求，換取剩下的請求還能被正常服務，並優先關掉非必要功能 —— 推薦系統先關，結帳留著。刻意變慢的系統撐得過流量高峰；想服務每一個請求的系統，只會整個倒下。

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

## Interview Version

> I would put a number on it to stay concrete: normal peak is a thousand requests a second and a surge pushes it to eight thousand. The first thing is to find out which part actually cannot keep up, because the fix differs completely. If the app servers are out of CPU, adding more fixes it today. If the database is the wall, adding more app servers just means more connections and more queries hitting that same wall - it makes things worse, faster. So before touching anything I would check where those eight thousand requests are spending their time: app CPU, the database, or a downstream call. But the smarter move, usually before adding a single machine, is to shrink the eight thousand before it reaches your servers. A CDN serves images, CSS, and JS from the edge, so a large dumb chunk of that traffic never touches your origin. A cache in front of the database means the same read does not hit it twice - typically the single change with the best payoff during a surge. On the database, read replicas soak up reads, and connection pooling stops a hundred instances each opening ten connections and burying a database that can only serve fifty. If the app is still the bottleneck, then it is horizontal scaling behind a load balancer, with auto-scaling adding instances on CPU or request count. The one condition is that the app must be stateless - sessions, caches, and in-process job state move out to Redis or a shared database first, or the instances stop being interchangeable. And plan for it still not being enough: push anything asynchronous onto a queue so a burst becomes a backlog, then rate limit and shed load deliberately - recommendations go dark, checkout stays up.

面試時可回答：我會給它一個數字好讓整段保持具體：正常尖峰是每秒一千個請求，一波突發把它推到八千。第一件事是找出到底哪一部分跟不上，因為解法完全不同。如果是應用伺服器 CPU 不夠，那今天加機器就解決了。如果牆在資料庫，加更多應用伺服器只是帶來更多連線、更多查詢去撞同一面牆 —— 那會讓情況更快變糟。所以在動任何東西之前，我會先看那八千個請求的時間實際花在哪裡：應用的 CPU、資料庫，還是某個下游呼叫。但更聰明的一步，通常在加任何一台機器之前，是「在流量抵達你的伺服器之前就把那八千縮小」。CDN 從邊緣直接供應圖片、CSS 和 JS，於是那一大塊笨重的流量根本碰不到你的來源伺服器。在資料庫前面放快取，代表同一個讀取不會打到它兩次 —— 這通常是突發期間投報率最高的單一改動。在資料庫這邊，唯讀副本吸收讀取流量；而連線池避免一百台實例各開十條連線，把一台實際上只能同時服務五十條的資料庫活埋。如果做完這些應用仍然是瓶頸，那才輪到在 load balancer 後面做水平擴展，並讓自動擴展依 CPU 或請求數自動加實例。唯一的條件是應用必須無狀態 —— session、快取、行程內的工作狀態要先搬到 Redis 或共用資料庫，否則實例就不再可以互換。也要為「這樣還是不夠」預作準備：把任何不必同步完成的事推到佇列上，讓一波突發變成一份會在接下來幾分鐘排空的積壓；然後刻意做速率限制與丟棄負載 —— 推薦功能先關掉，結帳留著。

The sentence to remember is: **A system that deliberately gets slower survives a surge; one that tries to serve every single request falls over completely.**

最值得記：**一個刻意讓自己變慢的系統撐得過突發流量；一個堅持要服務每一個請求的系統會整個倒下。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q23: How do you protect a server from SQL injection attacks?](../security-and-auth/q23-sql-injection.md) | [All 42 questions](../../README.md) | [Q32: Discuss multiprocessing, multithreading, and asynchronous I/O in Python.](q32-python-concurrency-models.md) |
