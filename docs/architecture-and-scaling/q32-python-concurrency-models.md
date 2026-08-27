# Q32: Discuss multiprocessing, multithreading, and asynchronous I/O in Python.

> Tests whether you can pick a concurrency model from the workload, and whether you understand what the GIL does and does not block.

**Part:** Architecture & Scaling | **Importance:** 9/10 | **Status:** Complete

**New to these terms?** [message queue](../_glossary.md#message-queue)

## In One Sentence

Use threads for I/O-bound work, processes for CPU-bound work, and asyncio when you need very high I/O concurrency in one thread - the GIL is what forces that split.

I/O 密集的工作用 thread、CPU 密集的工作用 process，而當你需要在單一執行緒內處理極高的 I/O 併發時用 asyncio —— 造成這種分法的正是 GIL。

## Answer Shape

Give the three-way rule in one sentence first so the answer lands even if you are cut off, then explain the GIL, because it is the reason the rule exists. Describe each model by its concurrency style - preemptive, cooperative, truly parallel - and finish with the failure mode of each, since naming how they break is what shows you have used them.

先用一句話給出三選一的原則，這樣即使被打斷答案也已經落地；接著解釋 GIL，因為它正是這條原則存在的原因。用併發風格來描述每個模型 —— 搶佔式、協作式、真正平行 —— 最後講各自的失敗模式，因為能講出它們怎麼壞掉，才顯示你真的用過。

## Full Spoken Answer

Anchor it on one job: fetch 500 URLs, then compress the images you got back. Fetching is I/O-bound - your code spends nearly all its time waiting on the network, not computing. Compressing is CPU-bound - the CPU is genuinely busy the whole time. That split is the whole answer: threads or asyncio for the fetching, processes for the compressing. The reason Python needs three different tools instead of one is CPython's Global Interpreter Lock: only one thread can execute Python bytecode at a time, full stop. But the GIL is released while a thread is waiting on I/O, so threads that are all just waiting on the network genuinely overlap - the lock blocks parallel *computation*, not parallel *waiting*, which is exactly why it doesn't get in the way of the fetching half of this job.

用一個具體任務貫穿三種模型：抓 500 個網址，再把拿回來的圖片壓縮。抓網址是 I/O 密集 —— 你的程式碼幾乎全部時間都在「等網路」，不是在算東西。壓縮圖片是 CPU 密集 —— CPU 整段時間都真的在忙。這個區分就是這題的全部答案：抓網址用 thread 或 asyncio，壓縮圖片用 process。Python 需要三種工具而不是一種，原因是 CPython 的 Global Interpreter Lock：同一時間只有一個執行緒能執行 Python 位元組碼，沒有例外。但 GIL 在等待 I/O 時會被釋放，所以一群都在等網路回應的執行緒是真的能同時等 —— 這把鎖擋住的是平行「運算」，不是平行「等待」，這正是它不會擋到抓網址這半段工作的原因。

For fetching those 500 URLs with threads: each thread is a real OS thread, and the operating system decides when to switch between them - preemptive concurrency, out of your control. Threads share memory, so the code reads like normal synchronous code, but that means shared state now needs locks or queues, and a race condition is the standard bug you'll hit. Each thread also costs about a megabyte of stack plus a real context-switch cost, so a few dozen threads fetching URLs is fine, and a few thousand starts to hurt.

用 thread 抓這 500 個網址：每個 thread 都是真正的作業系統執行緒，由作業系統決定何時切換 —— 這是搶佔式併發，不由你控制。Thread 共用記憶體，所以程式碼看起來就跟一般同步程式碼一樣，但也代表共用狀態現在需要鎖或佇列，而競態條件就是你會遇到的標準臭蟲。每個 thread 還要付出約一 MB 的堆疊和真實的 context-switch 成本，所以幾十個 thread 去抓網址沒問題，幾千個就開始吃力。

If it's 50,000 URLs instead of 500, switch to asyncio: one thread, one event loop, and each fetch explicitly hands control back with `await` - cooperative concurrency, entirely under your control. Switching happens in user space for almost nothing, and there's no shared-memory locking to get wrong, so one thread can hold tens of thousands of open connections. The catch is the whole ecosystem has to play along: you need async-flavored libraries like aiohttp, not requests, and the one mistake that breaks everything is a single blocking call - a synchronous DB driver, a heavy loop - which freezes the entire event loop and every other task waiting on it.

如果不是 500 個而是 50,000 個網址，就換成 asyncio：一條執行緒、一個事件迴圈，每次抓取都用 `await` 明確把控制權交回去 —— 這是協作式併發，完全由你自己控制。切換發生在使用者空間，成本幾乎是零，也沒有共用記憶體的鎖會搞砸，所以一條執行緒就能撐住數萬條開啟的連線。代價是整個生態系都得配合：你需要 aiohttp 這類非同步函式庫，不能用 requests；而唯一會搞砸全局的錯誤，就是一個阻塞呼叫 —— 一個同步的資料庫驅動、一段吃 CPU 的迴圈 —— 會凍住整個事件迴圈，連帶卡住所有正在等它的任務。

Now the compression half: neither threads nor asyncio actually speeds that up, because the GIL means only one thread computes at a time no matter how many you spawn. Multiprocessing sidesteps this by running separate OS processes, each with its own interpreter, its own memory, and its own GIL - real parallelism across CPU cores, which is what compressing images actually needs. The cost is a much heavier process (bigger memory footprint, slower startup), and anything you need to share between processes has to be serialized and piped across, so shipping large objects back and forth can cost more than the parallelism saves.

現在講壓縮那一半：thread 和 asyncio 對它其實都沒用，因為不管你開幾條，GIL 都讓同一時間只有一條在真正運算。多行程繞過這個限制的方式是跑獨立的作業系統行程，每個都有自己的直譯器、自己的記憶體、自己的 GIL —— 在多個 CPU 核心上真正平行，這正是壓縮圖片需要的東西。代價是每個行程重得多（記憶體佔用大、啟動慢），而任何要在行程間共享的東西都得序列化後透過管線傳遞，所以來回搬大型物件的成本可能超過平行運算省下來的時間。

## Quick Reference

**Pick by workload: threads or asyncio for waiting, processes for computing.**

| Aspect | Multithreading | Asyncio | Multiprocessing |
|---|---|---|---|
| **Concurrency type** | Preemptive - OS switches threads | Cooperative - code yields with `await` | True parallelism - separate GIL per process |
| **Best for** | I/O-bound, tens of concurrent ops | I/O-bound, thousands+ of concurrent ops | CPU-bound: computation, image/ML work |
| **Cost** | ~1MB stack + OS context-switch per thread | Near-zero switch cost, but one blocking call freezes everything | Heavy process startup; sharing data means serializing it |
| **Failure mode** | Race conditions on shared memory; degrades past ~1,000s of threads | A forgotten `await` or sync call stalls the whole event loop | Serialization cost eats the parallelism gain on large shared data |

## Interview Version

> I would anchor it on one job: fetch 500 URLs, then compress the images you got back. Fetching is I/O-bound - your code spends nearly all its time waiting on the network. Compressing is CPU-bound - the CPU is genuinely busy the whole time. That split is the whole answer: threads or asyncio for the fetching, processes for the compressing. The reason Python needs three tools instead of one is CPython's Global Interpreter Lock: only one thread executes Python bytecode at a time. But the GIL is released while a thread waits on I/O, so threads that are all just waiting on the network genuinely overlap - the lock blocks parallel computation, not parallel waiting. With threads, each is a real OS thread and the operating system decides when to switch, so the code reads like normal synchronous code but shared state now needs locks, and each thread costs about a megabyte of stack - a few dozen is fine, a few thousand hurts. If it is fifty thousand URLs instead of five hundred, switch to asyncio: one thread, one event loop, each fetch handing control back with await, switching in user space for almost nothing and no shared-memory locking to get wrong. The catch is that the whole ecosystem has to play along, and a single blocking call freezes the entire event loop and every task waiting on it. Now the compression half: neither threads nor asyncio speeds that up, because only one thread computes at a time no matter how many you spawn. Multiprocessing sidesteps it with separate processes, each with its own interpreter and its own GIL - real parallelism across cores. The cost is heavier processes and having to serialise anything shared between them.

面試時可回答：我會把它固定在一件工作上：抓 500 個網址，然後把抓回來的圖片壓縮。抓取是 I/O 密集的 —— 你的程式碼幾乎所有時間都在等網路。壓縮是 CPU 密集的 —— CPU 是真的整段都在忙。這個切分就是整個答案：抓取用 thread 或 asyncio，壓縮用 process。Python 之所以需要三種工具而不是一種，原因是 CPython 的全域直譯器鎖：同一時間只有一個執行緒能執行 Python bytecode。但執行緒在等待 I/O 時會釋放 GIL，所以一群都只是在等網路的執行緒是真的重疊在跑的 —— 這把鎖擋的是平行「計算」，不是平行「等待」。用 thread 時，每一個都是真正的 OS 執行緒，由作業系統決定何時切換，所以程式碼讀起來就像一般同步程式碼，但共用狀態現在需要鎖；而且每個執行緒大約要一 MB 的堆疊 —— 幾十個沒問題，幾千個就開始痛了。如果是五萬個網址而不是五百個，就換 asyncio：一個執行緒、一個事件迴圈，每次抓取都用 await 明確把控制權交回去，切換在使用者空間發生、幾乎不花成本，也沒有共用記憶體的鎖可以搞砸。代價是整個生態系都得配合，而任何一個阻塞呼叫都會凍住整個事件迴圈，以及所有在上面等待的任務。再看壓縮那一半：thread 和 asyncio 都無法讓它變快，因為不論你開多少個，同一時間只有一個在計算。multiprocessing 用獨立的行程繞過這一點，每個行程有自己的直譯器、自己的 GIL —— 那是真正跨核心的平行。代價是行程更重，而且任何要在行程之間共享的東西都必須序列化。

The sentence to remember is: **Threads for waiting, processes for computing, asyncio when you need tens of thousands of waits in one thread.**

最值得記：**要「等」就用 thread，要「算」就用 process，需要在單一執行緒裡等上幾萬件事時才用 asyncio。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q31: How would you scale a backend application during a traffic surge?](q31-scaling-during-traffic-surge.md) | [All 41 questions](../../README.md) | [Q03: What is an API endpoint?](../api-and-http/q03-what-is-an-api-endpoint.md) |
