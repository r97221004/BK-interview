# Q35: When would you move work onto a message queue?

> Tests whether you can name work that does not belong in a request cycle, and whether you know a queue introduces retries, ordering, and duplicate delivery.

**Part:** Architecture & Scaling | **Importance:** 6/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [idempotent](../_glossary.md#idempotent), [index](../_glossary.md#index), [redis](../_glossary.md#redis), [at-least-once delivery](../_glossary.md#at-least-once-delivery)

## In One Sentence

You move work onto a queue when the caller does not need the result to answer the request - so the request returns immediately and a separate worker does the slow part.

當呼叫端不需要那個結果就能回應這個請求時，就把工作移到佇列上 —— 請求立刻回傳，慢的那部分交給獨立的 worker 處理。

## Answer Shape

Give the selection rule first, then two or three examples that obviously qualify, because the rule alone sounds abstract. Then name the second reason - absorbing bursts - since that is the scaling half of the answer. Finish with what a queue costs you, because a candidate who only lists benefits has not operated one.

先給出判斷準則，再舉兩三個明顯符合的例子，因為光講準則會顯得抽象。接著點出第二個理由 —— 吸收突發流量 —— 那是這題屬於擴充性的那一半。最後講佇列的代價，因為只列得出好處的候選人並沒有實際維運過它。

## Full Spoken Answer

The test is whether the caller needs the result in order to get an answer. Sending a welcome email, generating a thumbnail, rebuilding a search index, exporting a report, calling a slow third-party API - in all of these the user only needs to know the request was accepted. So the endpoint validates the input, writes a job to the queue, and returns 202 immediately, while a worker process picks the job up and does the work out of band.

判斷標準是：呼叫端是否需要這個結果才能得到答案。寄送歡迎信、產生縮圖、重建搜尋索引、匯出報表、呼叫緩慢的第三方 API —— 這些情況下使用者只需要知道請求被接受了。所以 endpoint 驗證輸入、把一個工作寫進佇列，然後立刻回傳 202，而由一個 worker 行程把工作取走、在請求之外完成它。

The second reason is absorbing bursts. A queue turns a spike into a backlog: if traffic triples for ten minutes, the queue grows and drains afterwards instead of every request timing out at once. That decouples the rate at which work arrives from the rate at which you can do it, and it lets you scale the workers independently of the web tier, which matters because the two usually need different amounts of CPU and memory. It also decouples services - the producer does not need the consumer to be up at the moment it publishes.

第二個理由是吸收突發。佇列把尖峰變成積壓：如果流量在十分鐘內變成三倍，佇列會變長、之後再慢慢消化，而不是所有請求同時逾時。這讓「工作抵達的速率」和「你能處理的速率」解耦，也讓你能獨立於 web 層去擴充 worker —— 這很重要，因為兩者需要的 CPU 與記憶體通常不同。它同時也讓服務之間解耦：生產者發布訊息時，不需要消費者正好活著。

The usual tools split along that line. RabbitMQ is a message broker built for task queues, with routing and per-message acknowledgement, and Celery is the standard Python layer on top of it or on Redis. Kafka is a distributed log rather than a queue: consumers track their own offset and the messages stay put, which suits event streams and replay far better than one-off jobs. Redis lists or streams are a reasonable lightweight option when you already run Redis and do not need strong delivery guarantees.

常見的工具也沿著這條線分開。RabbitMQ 是為任務佇列打造的訊息中介，具備路由與逐則確認，而 Celery 是架在它或 Redis 之上的標準 Python 層。Kafka 則是分散式日誌而不是佇列：消費者自己追蹤位移、訊息會留在原地，這比起一次性工作更適合事件串流與重播。當你本來就在跑 Redis、又不需要強交付保證時，Redis 的 list 或 stream 是合理的輕量選項。

The cost is that asynchronous work is harder to get right, and naming those costs is the point of the question. Delivery is at-least-once in practice, so a job can run twice and every handler needs to be idempotent. Ordering is not guaranteed once you run more than one worker. Failures no longer surface to the user, so you need retries with backoff, a dead-letter queue for jobs that keep failing, and monitoring on queue depth and job age - a backlog that never drains is invisible until someone complains. And the user experience changes: the request returns before the work is done, so the client needs a way to find out how it went.

代價是非同步工作更難做對，而把這些代價點名正是這題的重點。實務上的交付保證是至少一次，所以一個工作可能被執行兩次，每個處理函式都必須具備冪等性。一旦你跑超過一個 worker，順序就不再有保證。失敗不再直接呈現給使用者，所以你需要帶退避的重試、給持續失敗工作的死信佇列，以及對佇列深度與工作年齡的監控 —— 一個永遠消化不完的積壓在有人抱怨之前是看不見的。而且使用者體驗也改變了：請求在工作完成之前就回傳，所以客戶端需要一個管道知道後來怎麼了。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q34: How do you ensure your backend code is maintainable and easy to understand?](q34-maintainable-backend-code.md) | [All 41 questions](../../README.md) | [Q42: What are the benefits of Docker multi-stage builds?](../devops-and-deployment/q42-docker-multi-stage-builds.md) |
