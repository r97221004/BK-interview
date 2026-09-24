# Q35: When would you move work onto a message queue?

> Tests whether you can name work that does not belong in a request cycle, and whether you know a queue introduces retries, ordering, and duplicate delivery.

**Part:** Architecture & Scaling | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [idempotent](../_glossary.md#idempotent), [index](../_glossary.md#index), [redis](../_glossary.md#redis), [at-least-once delivery](../_glossary.md#at-least-once-delivery), [timeout](../_glossary.md#timeout)

## In One Sentence

You move work onto a queue when the caller does not need the result to answer the request - so the request returns immediately and a separate worker does the slow part.

當呼叫端不需要那個結果就能回應這個請求時，就把工作移到佇列上 —— 請求立刻回傳，慢的那部分交給獨立的 worker 處理。

## Answer Shape

Give the selection rule first, then two or three examples that obviously qualify, because the rule alone sounds abstract. Then name the second reason - absorbing bursts - since that is the scaling half of the answer. Finish with what a queue costs you, because a candidate who only lists benefits has not operated one.

先給出判斷準則，再舉兩三個明顯符合的例子，因為光講準則會顯得抽象。接著點出第二個理由 —— 吸收突發流量 —— 那是這題屬於擴充性的那一半。最後講佇列的代價，因為只列得出好處的候選人並沒有實際維運過它。

## Full Spoken Answer

The test is whether the caller needs the result in order to get an answer. Sending a welcome email, generating a thumbnail, rebuilding a search index, exporting a report, calling a slow third-party API - in all of these the user only needs to know the request was accepted. So the endpoint validates the input, writes a job to the queue, and returns 202 immediately, while a worker process picks the job up and does the work out of band. Plainly: if the answer to "does the user need to see this finish?" is no, it doesn't belong in the request.

判斷標準是：呼叫端是否需要這個結果才能得到答案。寄送歡迎信、產生縮圖、重建搜尋索引、匯出報表、呼叫緩慢的第三方 API —— 這些情況下使用者只需要知道請求被接受了。所以 endpoint 驗證輸入、把一個工作寫進佇列，然後立刻回傳 202，而由一個 worker 行程把工作取走、在請求之外完成它。說白了：如果「使用者需要親眼看到這件事做完嗎」的答案是不需要，它就不該待在請求裡。

The second reason is absorbing bursts. A queue turns a spike into a backlog: if traffic triples for ten minutes, the queue grows and drains afterwards instead of every request timing out at once. That decouples the rate at which work arrives from the rate at which you can do it, and it lets you scale the workers independently of the web tier, which matters because the two usually need different amounts of CPU and memory. It also decouples services - the producer does not need the consumer to be up at the moment it publishes. The third reason follows from that: the queue is a place a failure can be retried. If the payment provider is down for thirty seconds, an in-request call returns a 500 to the user, while a queued job simply retries and succeeds on the second attempt - the failure stays inside the worker instead of reaching the person who made the request.

第二個理由是吸收突發。佇列把尖峰變成積壓：如果流量在十分鐘內變成三倍，佇列會變長、之後再慢慢消化，而不是所有請求同時逾時。這讓「工作抵達的速率」和「你能處理的速率」解耦，也讓你能獨立於 web 層去擴充 worker —— 這很重要，因為兩者需要的 CPU 與記憶體通常不同。它同時也讓服務之間解耦：生產者發布訊息時，不需要消費者正好活著。第三個理由由此而來：佇列提供了一個「可以重試失敗」的位置。如果金流商掛了三十秒，在請求裡直接呼叫就是回一個 500 給使用者；而排進佇列的工作只是重試一次、第二次就成功了 —— 失敗被關在 worker 裡，沒有走到發出請求的那個人面前。

The usual tools split along that line. RabbitMQ is a message broker built for task queues, with routing and per-message acknowledgement, and Celery is the standard Python layer on top of it or on Redis. Kafka is a distributed log rather than a queue: consumers track their own offset and the messages stay put, which suits event streams and replay far better than one-off jobs. Redis lists or streams are a reasonable lightweight option when you already run Redis and do not need strong delivery guarantees.

常見的工具也沿著這條線分開。RabbitMQ 是為任務佇列打造的訊息中介，具備路由與逐則確認，而 Celery 是架在它或 Redis 之上的標準 Python 層。Kafka 則是分散式日誌而不是佇列：消費者自己追蹤位移、訊息會留在原地，這比起一次性工作更適合事件串流與重播。當你本來就在跑 Redis、又不需要強交付保證時，Redis 的 list 或 stream 是合理的輕量選項。

The cost is that asynchronous work is harder to get right, and naming those costs is the point of the question. Delivery is at-least-once in practice, so a job can run twice and every handler needs to be idempotent. Ordering is not guaranteed once you run more than one worker. Failures no longer surface to the user, so you need retries with backoff, a dead-letter queue for jobs that keep failing, and monitoring on queue depth and job age - a backlog that never drains is invisible until someone complains. And the user experience changes: the request returns before the work is done, so the client needs a way to find out how it went.

代價是非同步工作更難做對，而把這些代價點名正是這題的重點。實務上的交付保證是至少一次，所以一個工作可能被執行兩次，每個處理函式都必須具備冪等性。一旦你跑超過一個 worker，順序就不再有保證。失敗不再直接呈現給使用者，所以你需要帶退避的重試、給持續失敗工作的死信佇列，以及對佇列深度與工作年齡的監控 —— 一個永遠消化不完的積壓在有人抱怨之前是看不見的。而且使用者體驗也改變了：請求在工作完成之前就回傳，所以客戶端需要一個管道知道後來怎麼了。

## Interview Version

> The test is whether the caller needs the result in order to get an answer. Sending a welcome email, generating a thumbnail, rebuilding a search index, calling a slow third-party API - in all of these the user only needs to know the request was accepted. So the endpoint validates the input, writes a job to the queue, and returns 202 immediately, while a worker picks the job up and does the work out of band. The second reason is absorbing bursts: a queue turns a spike into a backlog, so if traffic triples for ten minutes the queue grows and drains afterwards instead of every request timing out at once. That decouples the rate work arrives from the rate you can do it, and lets you scale workers independently of the web tier, which matters because the two usually need different CPU and memory. It also decouples services - the producer does not need the consumer to be up at the moment it publishes. The third reason follows from that: the queue is a place a failure can be retried, so a payment provider that is down for thirty seconds turns a 500 in the user's face into a job that retries and succeeds on the second attempt. The tools split along that line: RabbitMQ is a message broker built for task queues with routing and per-message acknowledgement, Kafka is a distributed log where consumers track their own offset and messages stay put, which suits event streams and replay far better than one-off jobs, and Redis lists or streams are a reasonable lightweight option when you already run Redis. The cost is that asynchronous work is harder to get right, and naming those costs is the point of the question. Delivery is at-least-once in practice, so a job can run twice and every handler must be idempotent. Ordering is not guaranteed once you run more than one worker. Failures no longer surface to the user, so you need retries with backoff, a dead-letter queue, and monitoring on queue depth and job age - a backlog that never drains is invisible until someone complains.

面試時可回答：判準是：呼叫端是否需要那個結果才能得到答案。寄送歡迎信、產生縮圖、重建搜尋索引、呼叫一個很慢的第三方 API —— 這些情況裡，使用者只需要知道「請求被接受了」。所以 endpoint 驗證輸入、把一份工作寫進佇列，立刻回傳 202，而由一個 worker 把工作取走、在請求之外完成它。第二個理由是吸收突發：佇列把尖峰變成積壓，所以流量若在十分鐘內變成三倍，佇列會長大、之後再排空，而不是所有請求同時逾時。這把「工作抵達的速率」和「你能處理的速率」解耦，也讓你能獨立於 web 層去擴充 worker —— 這很重要，因為兩者需要的 CPU 和記憶體通常不同。它也讓服務之間解耦：生產者發布的當下，並不需要消費者是活著的。第三個理由由此而來：佇列是一個能重試失敗的位置，所以金流商掛掉三十秒，不再是使用者眼前的 500，而是一份重試一次、第二次就成功的工作。工具也沿著這條線分開：RabbitMQ 是為任務佇列而生的訊息中介，帶有路由與逐則訊息的確認；Kafka 是分散式日誌，消費者自己追蹤 offset、訊息留在原地，這比一次性工作更適合事件串流與重播；而當你本來就跑著 Redis、又不需要強交付保證時，Redis 的 list 或 stream 是合理的輕量選項。代價是非同步工作更難做對，而把這些代價講出來正是這題的重點。實務上交付是至少一次，所以一份工作可能跑兩次，每個處理器都必須是冪等的。一旦你跑超過一個 worker，順序就不再有保證。失敗不再浮現到使用者面前，所以你需要帶退避的重試、一個死信佇列，以及對佇列深度與工作年齡的監控 —— 一份永遠排不空的積壓，在有人抱怨之前是看不見的。

The sentence to remember is: **If the answer to "does the user need to see this finish?" is no, it does not belong in the request - and a queue buys three things at once: the request returns immediately, a spike becomes a backlog instead of a wave of timeouts, and a failure becomes a retry in the worker instead of an error in the user's face.**

最值得記：**如果「使用者需要看著這件事做完嗎」的答案是否，那它就不該待在請求裡 —— 而佇列一次買到三件事：請求立刻回傳（非同步處理）、尖峰變成積壓而不是一整排逾時（吸收突發）、失敗變成 worker 裡的重試而不是使用者眼前的錯誤（重試與故障隔離）。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q28: What is the difference between HS256 and RS256 for signing a JWT?](../security-and-auth/q28-jwt-hs256-vs-rs256.md) | [All 51 questions](../../README.md) | [Q37: How do you stop one slow dependency from taking down your service?](q37-timeouts-retries-and-failure.md) |
