# Q32: Discuss multiprocessing, multithreading, and asynchronous I/O in Python.

> Tests whether you can pick a concurrency model from the workload, and whether you understand what the GIL does and does not block.

**Part:** Architecture & Scaling | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [websocket](../_glossary.md#websocket), [query plan](../_glossary.md#query-plan), [message queue](../_glossary.md#message-queue)

## In One Sentence

Use threads for I/O-bound work, processes for CPU-bound work, and asyncio when you need very high I/O concurrency in one thread - the GIL is what forces that split.

I/O 密集的工作用 thread、CPU 密集的工作用 process，而當你需要在單一執行緒內處理極高的 I/O 併發時用 asyncio —— 造成這種分法的正是 GIL。

## Answer Shape

Give the three-way rule in one sentence first so the answer lands even if you are cut off, then explain the GIL, because it is the reason the rule exists. Describe each model by its concurrency style - preemptive, cooperative, truly parallel - and finish with the failure mode of each, since naming how they break is what shows you have used them.

先用一句話給出三選一的原則，這樣即使被打斷答案也已經落地；接著解釋 GIL，因為它正是這條原則存在的原因。用併發風格來描述每個模型 —— 搶佔式、協作式、真正平行 —— 最後講各自的失敗模式，因為能講出它們怎麼壞掉，才顯示你真的用過。

## Full Spoken Answer

The short version is that multithreading suits I/O-bound tasks, multiprocessing suits CPU-bound tasks, and asyncio suits very high I/O concurrency. The reason all three exist rather than one is CPython's Global Interpreter Lock: only one thread can execute Python bytecode at a time. The detail that matters is that the GIL is released during I/O, so threads waiting on a network call or a disk read genuinely overlap - the lock blocks parallel computation, not parallel waiting.

簡短版是：多執行緒適合 I/O 密集工作、多行程適合 CPU 密集工作、asyncio 適合極高的 I/O 併發。三者並存而不是只有一種的原因是 CPython 的 Global Interpreter Lock：同一時間只有一個執行緒能執行 Python 位元組碼。真正關鍵的細節是 GIL 在 I/O 期間會被釋放，所以等待網路呼叫或磁碟讀取的執行緒是真的能重疊的 —— 這把鎖擋住的是平行「運算」，不是平行「等待」。

Multithreading runs several OS threads inside one process, and the operating system decides when to switch between them, which makes it preemptive concurrency. Because threads share memory, they are easy to write - the code looks synchronous - but shared state needs locks, semaphores, or queues, and race conditions are the standard bug. Each thread also carries its own stack, roughly a megabyte, and the kernel pays a real cost to context-switch, so this model works well for tens of concurrent operations and badly for thousands.

多執行緒在同一個行程內跑多條作業系統執行緒，由作業系統決定何時切換，因此屬於搶佔式併發。由於執行緒共用記憶體，寫起來很容易 —— 程式碼看起來就像同步的 —— 但共用狀態需要鎖、號誌或佇列，而競態條件是標準的臭蟲。每條執行緒還各自帶著約一 MB 的堆疊，核心切換上下文也有真實成本，所以這個模型在數十個並行操作時表現良好，數千個時就很糟。

Asyncio runs on a single thread with an event loop that schedules coroutines, and tasks yield control explicitly with await, which makes it cooperative concurrency. Switching happens in user space and costs almost nothing, and there is no shared-state locking to get wrong, so one thread can manage tens of thousands of open connections. The price is that the whole ecosystem has to cooperate: you need async-compatible libraries such as aiohttp or asyncpg, and a single blocking call - a synchronous database driver, a CPU-heavy loop - freezes the entire loop and every other task with it.

asyncio 在單一執行緒上以事件迴圈排程協程，任務用 await 明確交出控制權，因此屬於協作式併發。切換發生在使用者空間、成本幾乎為零，也沒有共用狀態的鎖可以搞砸，所以一條執行緒就能管理數萬條開啟的連線。代價是整個生態系都必須配合：你需要支援非同步的函式庫，例如 aiohttp 或 asyncpg；而只要有一個阻塞呼叫 —— 一個同步的資料庫驅動、一段吃 CPU 的迴圈 —— 就會凍住整個事件迴圈，連同其他所有任務。

Multiprocessing runs separate processes, each with its own interpreter, its own memory, and its own GIL, so it delivers true parallelism across CPU cores. That makes it the right choice for computation, image processing, and machine-learning workloads. The costs are that each process has a much larger memory footprint, startup is slow, and anything shared must be serialized across a pipe, so passing large objects can cost more than the work saved. Stated as failure modes: too many threads degrade into context-switching overhead, a forgotten await or a blocking call stalls the event loop, and multiprocessing loses its advantage when the data transfer dominates.

多行程跑的是各自獨立的行程，每個都有自己的直譯器、自己的記憶體和自己的 GIL，因此能在多個 CPU 核心上達成真正的平行。這使它成為運算、影像處理和機器學習工作負載的正確選擇。代價是每個行程的記憶體佔用大得多、啟動慢，而且任何要共享的東西都必須序列化後透過管線傳遞，所以傳大型物件的成本可能超過省下來的工作。用失敗模式來說：執行緒太多會退化成上下文切換的開銷、漏掉一個 await 或有阻塞呼叫會卡住事件迴圈，而當資料傳輸成為主導時多行程就失去了優勢。

## Quick Reference

| **Aspect** | **Multi-threading** | **Asyncio (Asynchronous I/O)** | **Multiprocessing** |
|---|---|---|---|
| **Core Concept** | Uses multiple **OS threads** within one process. Each thread runs part of your code “in parallel.” | Uses a **single thread** with an **event loop** that schedules and runs asynchronous tasks cooperatively. | Multiple **processes**, each with its own Python interpreter and memory space. |
| **Concurrency Type** | **Preemptive concurrency(搶占式多工)** — the OS decides when to switch between threads. | **Cooperative concurrency(協作式多工)** — tasks explicitly yield control using `await`. | **True parallelism** (processes run in parallel on multiple CPU cores). |
| **Parallel Execution** | Limited by the **Global Interpreter Lock (GIL)** — only one thread runs Python code at a time. | Runs on a **single thread**, so no true parallelism, but achieves *concurrency* through async scheduling. | True parallelism across cores - each process holds its own GIL. |
| **True Parallelism (CPU-bound)** | ❌ Not possible due to GIL (unless you use native C extensions). | ❌ Not possible — still single-threaded. | ✅ Yes (each process has its own GIL). |
| **Best for** | **I/O-bound** tasks with moderate concurrency (e.g., 10–100 simultaneous operations). | **High-concurrency I/O-bound** workloads (e.g., 10,000+ simultaneous connections). | **CPU-bound** tasks (e.g., computation, image processing). |
| **Performance** | OS handles thread scheduling — can become inefficient with many threads due to context-switching overhead. | Very lightweight — event loop switches tasks without OS intervention, minimal overhead. | Fully utilizes all CPU cores for heavy computation. |
| **Scalability** | Limited — each thread consumes memory (~1MB stack) and causes CPU overhead for context switching. | Highly scalable — a single thread can manage thousands of concurrent async tasks. | Scales across CPU cores, but each process has separate memory. |
| **Memory Usage** | Higher — each thread has its own stack and metadata. | Lower — all tasks share one event loop and one stack. | High (each process has its own memory space) |
| **Context Switching** | Done by the OS kernel; expensive. | Done in user space; very cheap. | Done by OS — heavier than threads. |
| **Code Complexity** | Easier to write and understand — looks like normal synchronous code. | Requires async/await syntax and async-compatible libraries; can be harder to debug. | Straightforward per process, but anything shared must be passed explicitly. |
| **Blocking Behavior** | A blocking operation in one thread affects only that thread. | A blocking operation blocks the entire event loop — you must use non-blocking APIs. | A blocking call affects only that process. |
| **Error Handling** | Standard try/except per thread; can be tricky with shared data. | Exceptions propagate through async tasks; easier to aggregate with `asyncio.gather()`. | Exceptions are raised in the child and re-raised on the parent when the result is collected. |
| **Synchronization** | Requires locks, semaphores, or queues to manage shared data safely (risk of race conditions). | Usually no shared state — each async task works independently (simpler concurrency model). | No shared memory by default; sharing needs `Queue`, `Pipe`, or `shared_memory`. |
| **Use of GIL** | GIL prevents multiple threads from executing Python bytecode simultaneously. | GIL not a bottleneck since tasks release control explicitly using `await`. | Each process has its own interpreter and its own GIL, so the GIL is not a limit. |
| **Third-party Library Support** | Works with any normal blocking library (e.g., `requests`, `psycopg2`). | Must use **async-compatible** libraries (e.g., `aiohttp`, `asyncpg`, `aiomysql`). |   |
| **Debugging Tools** | Easier — you can use standard debugging and logging tools. | Harder — stack traces are split across coroutines; requires `asyncio`-aware debuggers. |   |
| **Setup Complexity** | Simple — just create threads using `threading.Thread`. | Slightly complex — need to define `async` functions and run them inside an event loop. |   |
| **Example Frameworks** | `threading`, `concurrent.futures.ThreadPoolExecutor` | `asyncio`, `aiohttp`, `FastAPI`, `Quart` | `multiprocessing`, `concurrent.futures.ProcessPoolExecutor`, `joblib` |
| **Ideal Use Cases** | - Handling a few concurrent I/O tasks (e.g., calling multiple APIs)   - Background file operations  - Network servers with moderate load | - High-concurrency servers (e.g., chat, websocket, game servers)  - Web crawlers  - Realtime dashboards  - Async web frameworks (e.g., FastAPI, Sanic) | - Image or data processing- Machine learning workloads- Any CPU-heavy computation |
| **Example of Failure Mode** | Too many threads → high memory use and context switching → degraded performance. | Forgetting `await` or using blocking I/O → event loop freezes → no concurrency. | Serializing large objects between processes costs more than the parallelism saves. |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q31: How would you scale a backend application during a traffic surge?](q31-scaling-during-traffic-surge.md) | [All 41 questions](../../README.md) | [Q05: What are the benefits and drawbacks of RESTful APIs?](../api-and-http/q05-rest-benefits-and-drawbacks.md) |
