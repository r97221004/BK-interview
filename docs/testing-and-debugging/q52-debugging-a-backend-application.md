# Q52: What tools and techniques do you use for debugging a backend application?

> Tests whether you have a method rather than a tool list, and whether you can debug something you cannot attach a debugger to.

**Part:** Testing & Debugging | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [endpoint](../_glossary.md#endpoint), [orm](../_glossary.md#orm), [index](../_glossary.md#index), [query plan](../_glossary.md#query-plan), [n+1 query](../_glossary.md#n-1-query)

## In One Sentence

Debugging is a method before it is a toolset: reproduce the problem, narrow it to one component, then instrument that component with whatever the environment allows - a debugger locally, logs and metrics in production.

除錯首先是一套方法，其次才是工具：先重現問題、把範圍縮到單一元件，再依環境允許的方式對它加上觀測 —— 本機用除錯器，正式環境用日誌與指標。

## Answer Shape

Lead with the method rather than the tool list, because tools are easy to name and the interviewer wants to know how you think. The skeleton is reproduce, narrow, instrument, prove - and it is the same four steps whether you can attach a debugger or not. Then split by environment, since the honest and interesting half is production, where a debugger is not an option and the answer becomes what you instrumented in advance. Give one specific technique per environment so it stays concrete, and finish by closing the loop with a test that reproduces the bug.

先講方法而不是工具清單，因為工具誰都說得出來，面試官想知道的是你怎麼思考。骨架是重現、縮小、觀測、驗證 —— 不論你能不能接上除錯器，都是同樣這四步。接著依環境切分，因為誠實而且有趣的那一半是正式環境：那裡沒有除錯器可用，答案變成「你事先埋了什麼觀測」。每個環境各給一個具體技術讓它保持具體，最後用一個能重現該 bug 的測試把迴圈收起來。

## Full Spoken Answer

The method comes first. I try to reproduce the problem reliably, because a bug I cannot trigger on demand cannot be verified as fixed. Then I narrow it down: which component, which request, which layer - is this the application, the database, or a downstream dependency? A useful habit is to check what changed recently, since a deploy, a config change, or a data change explains a large share of problems that appear suddenly. Only once the surface is small do I start reading code.

方法先行。我會設法穩定地重現問題，因為一個無法隨時觸發的臭蟲，也無法被驗證是否修好了。接著縮小範圍：哪個元件、哪個請求、哪一層 —— 這是應用程式、資料庫，還是某個下游相依？一個有用的習慣是先查最近改了什麼，因為部署、設定變更或資料變更，能解釋掉很大一部分「突然出現」的問題。只有在範圍夠小之後，我才開始讀程式碼。

Locally I use the debugger built into the editor, setting breakpoints, inspecting variables, and stepping through the path in question - which is almost always faster than adding print statements and rerunning. Postman is useful for replaying an API request with modified inputs to isolate which field triggers the failure, and Swagger or the OpenAPI spec is where I check whether the endpoint is behaving as specified or whether the specification itself is wrong.

在本機我使用編輯器內建的除錯器，設中斷點、檢視變數、逐步走過有問題的路徑 —— 這幾乎總是比加一堆 print 再重跑要快。Postman 適合用來以修改過的輸入重放 API 請求，以隔離出是哪個欄位觸發了失敗；而 Swagger 或 OpenAPI 規格則是我用來確認 endpoint 是否照規格運作、或規格本身是否有誤的地方。

In staging and production a debugger is not an option, so the answer is observability - being able to ask new questions of a running system without shipping code to answer them. Structured logging is the foundation, and the single thing that makes it work is a request or correlation ID attached to every line and propagated across services, so one user's failing request can be followed end to end instead of guessed at from interleaved output. On top of that, metrics and dashboards in Prometheus and Grafana show error rates, latency percentiles, and saturation, which is how you tell a single broken request apart from a system-wide degradation. Distributed tracing is the natural next step once several services are involved.

在測試與正式環境沒有除錯器可用，所以答案是 observability（可觀測性）—— 也就是不必為了回答問題而重新部署，就能對運行中的系統提出新問題的能力。結構化日誌是基礎，而讓它真正發揮作用的關鍵只有一件事：在每一行都附上並跨服務傳遞的 request ID 或 correlation ID，讓某個使用者失敗的請求能被從頭追到尾，而不是從交錯的輸出裡用猜的。在此之上，Prometheus 與 Grafana 中的指標與儀表板顯示錯誤率、延遲百分位和飽和度，這是你用來分辨「單一壞掉的請求」和「全系統劣化」的方式。當牽涉到多個服務時，分散式追蹤是自然的下一步。

For database-related problems the approach is more specific. I look at the actual SQL being issued, which for an ORM often means logging the generated queries, because the N+1 problem is invisible in the application code and obvious in the query log. Then I run EXPLAIN on the slow query to see whether it is using an index or scanning the table, and check the database's own slow-query log to find which statements are actually costing time rather than the ones I assumed were. Once the cause is found, the last step is a test that reproduces it, so the fix is verified and the regression cannot return unnoticed.

面對資料庫相關的問題，做法更具體。我會去看實際送出的 SQL，對 ORM 而言通常意味著把產生的查詢記錄下來，因為 N+1 問題在應用程式碼裡看不見，在查詢日誌裡卻一目了然。接著我對慢查詢跑 EXPLAIN，看它是走索引還是掃全表，並查看資料庫本身的慢查詢日誌，找出真正在耗時的敘述句，而不是我以為在耗時的那些。找到原因之後，最後一步是寫一個能重現它的測試，讓修復被驗證過，也讓這個退步不會在沒人注意時回來。

## Quick Reference

### The skeleton to memorise

**Reproduce → Narrow → Instrument → Prove**

The same four steps in both environments. Only the tools change.

| Step | Locally | In production |
|---|---|---|
| **Reproduce** | Replay the request in Postman with modified inputs to isolate the field that triggers it | Find the failing request by its request ID in the logs |
| **Narrow** | Breakpoints; step through the path in question | Which service, which endpoint, which dependency - and *what changed recently*: a deploy, a config flip, or a data change explains most sudden failures |
| **Instrument** | The debugger; inspect variables in place | Structured logs with a correlation ID propagated across services; Prometheus and Grafana for error rate, latency percentiles, saturation; tracing once several services are involved |
| **Prove** | A failing test that reproduces it, then the fix | Same - the regression must not be able to return unnoticed |

### For a slow query specifically

Log the SQL your ORM actually generates - an N+1 is invisible in the application
code and obvious in the query log. Then `EXPLAIN` the slow one to see whether it
uses an index or scans, and check the database's own slow-query log to find what
is really costing time rather than what you assumed was.

## Interview Version

> The method comes first. I try to reproduce the problem reliably, because a bug I cannot trigger on demand cannot be verified as fixed. Then I narrow it down - which component, which request, which layer: is this the application, the database, or a downstream dependency? A useful habit is to check what changed recently, since a deploy, a config change, or a data change explains a large share of problems that appear suddenly. Only once the surface is small do I start reading code. Locally I use the debugger built into the editor, setting breakpoints and stepping through the path in question, which is almost always faster than adding print statements and rerunning. In staging and production a debugger is not an option, so the answer is observability - being able to ask new questions of a running system without shipping code to answer them. Structured logging is the foundation, and the single thing that makes it work is a request or correlation ID attached to every line and propagated across services, so one user's failing request can be followed end to end instead of guessed at from interleaved output. On top of that, metrics and dashboards show error rates, latency percentiles, and saturation, which is how you tell a single broken request apart from a system-wide degradation. For database problems the approach is more specific: look at the actual SQL being issued, which for an ORM means logging the generated queries, because the N+1 problem is invisible in the application code and obvious in the query log. Then run EXPLAIN to see whether it uses an index or scans, and check the slow-query log to find which statements actually cost time rather than the ones you assumed. Once the cause is found, the last step is a test that reproduces it.

面試時可回答：方法先於工具。我會試著穩定地重現問題，因為一個我無法隨時觸發的 bug，也無法驗證它被修好了。接著我把範圍收窄 —— 哪個元件、哪個請求、哪一層：這是應用程式、資料庫，還是某個下游依賴？一個有用的習慣是去看最近改了什麼，因為部署、設定變更或資料變更，解釋了很大一部分「突然出現」的問題。只有在範圍夠小之後，我才開始讀程式碼。在本機我用編輯器內建的除錯器，設中斷點、單步走過那條路徑，這幾乎總是比加 print 再重跑快。在測試環境和正式環境，除錯器不是選項，所以答案是可觀測性 —— 能夠對一個正在運行的系統提出新問題，而不必為了回答它而部署新程式碼。結構化日誌是基礎，而讓它真正有用的關鍵只有一件事：一個附加在每一行、並且跨服務傳遞的 request ID 或 correlation ID，這樣一個使用者失敗的請求就能被從頭到尾追下去，而不是從交錯的輸出裡用猜的。在這之上，指標和儀表板顯示錯誤率、延遲的百分位數和飽和度，那是你分辨「單一壞掉的請求」和「全系統降級」的方式。對資料庫相關的問題，做法更具體：去看實際發出的 SQL，對 ORM 來說就是把產生的查詢記錄下來，因為 N+1 問題在應用程式碼裡看不見、在查詢日誌裡卻一目了然。接著跑 EXPLAIN 看它用了索引還是在掃描，並檢查慢查詢日誌，找出真正花時間的語句，而不是你以為的那些。找到原因之後，最後一步是寫一個能重現它的測試。

The sentence to remember is: **A bug you cannot trigger on demand cannot be verified as fixed - reproduce first, narrow second, read code last.**

最值得記：**一個你無法隨時觸發的 bug，也無法驗證它修好了 —— 先重現、再收窄範圍，最後才讀程式碼。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q43: How do you deploy a new version without dropping requests?](../devops-and-deployment/q43-zero-downtime-deploys.md) | [All 51 questions](../../README.md) | [Q62: How would you paginate a large collection endpoint?](../api-design/q62-pagination.md) |
