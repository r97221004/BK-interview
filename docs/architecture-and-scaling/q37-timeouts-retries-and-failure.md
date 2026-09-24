# Q37: How do you stop one slow dependency from taking down your service?

> Tests whether you treat a network call as something that fails, and whether you know a naive retry turns a blip into an outage.

**Part:** Architecture & Scaling | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [idempotent](../_glossary.md#idempotent), [cache](../_glossary.md#cache), [connection pool](../_glossary.md#connection-pool)

## In One Sentence

You put a timeout on every outbound call, retry only what is safe to retry and only with backoff, and trip a circuit breaker when a dependency is clearly down so you stop queueing work behind it.

你要為每一個對外呼叫設逾時、只重試那些重試起來安全的操作而且必須帶退避，並在某個相依服務明顯掛掉時打開熔斷器，好讓你不再把工作堆在它後面排隊。

## Answer Shape

Start with the timeout, because it is the cheapest and most commonly missing control, and explain what a missing one actually does - it holds a worker until the pool is empty. Then add retries with the two conditions that make them safe. Then the circuit breaker as the thing that stops retries making it worse. Finish with graceful degradation, because staying partly up is the goal.

從逾時講起，因為它是最便宜、也最常被漏掉的一道防護，並解釋沒有它實際上會怎樣 —— 它會佔住一個 worker 直到整個 pool 被榨乾。接著加上重試，並說明讓重試安全的兩個條件。再來是熔斷器，它的作用是阻止重試把情況變得更糟。最後收在優雅降級，因為目標是「部分還活著」。

## Full Spoken Answer

Start with timeouts, because a missing timeout is the single most common cause of a cascading outage. A call with no deadline does not fail when the dependency is slow - it waits, holding a worker or a connection the whole time. Enough of those and the pool is exhausted, at which point your service is down even though nothing in it is broken. So every outbound call gets an explicit connect and read timeout, chosen from the dependency's real latency rather than left at the library default, which is very often infinite.

從逾時開始，因為漏設逾時是連鎖故障最常見的單一成因。一個沒有期限的呼叫在相依服務變慢時並不會失敗 —— 它會一直等，而且整段時間都佔著一個 worker 或一條連線。這種呼叫夠多時 pool 就被榨乾了，這時候即使你的服務本身沒有任何東西壞掉，它也已經倒了。所以每一個對外呼叫都要有明確的連線逾時和讀取逾時，數值要從相依服務的真實延遲推算，而不是沿用函式庫的預設 —— 那個預設常常是無限。

Retries come next, with two conditions attached. The operation has to be safe to repeat, which means idempotent, or a retry on a payment double-charges. And the retry has to back off exponentially with jitter, because synchronised retries from every client turn a struggling dependency into a dead one - a retry storm is how a brief blip becomes a real outage. Retries also have to be bounded, and bounded across the whole call chain rather than per hop, since three services each retrying three times is twenty-seven requests for one user action.

接著是重試，並附帶兩個條件。這個操作必須可以安全地重複執行，也就是具備冪等性，否則對付款做重試就會重複扣款。而且重試必須帶指數退避與隨機抖動，因為所有客戶端同步發起的重試會把一個正在掙扎的相依服務直接壓死 —— 重試風暴正是短暫抖動變成真實事故的途徑。重試次數也必須有上限，而且要以整條呼叫鏈為單位設限，而不是每一跳各自設限，因為三個服務各重試三次，一個使用者動作就變成二十七個請求。

A circuit breaker is what stops you retrying into a wall. It watches the failure rate for a dependency, and once that crosses a threshold it opens: subsequent calls fail immediately without touching the network, which frees your workers and gives the failing service room to recover. After a cooling period it lets a trial request through, and closes again if that succeeds. The value is that failing fast is better than failing slowly - it converts a timeout that costs you a worker for thirty seconds into an error you can handle in a millisecond.

熔斷器的作用是阻止你一直往牆上重試。它監看某個相依服務的失敗率，一旦超過門檻就「打開」：後續呼叫立刻失敗、完全不碰網路，這會釋放你的 worker，也給那個故障的服務喘息空間復原。冷卻一段時間後它會放一個試探請求過去，如果成功就重新「關閉」。它的價值在於「快速失敗優於緩慢失敗」—— 它把一個會佔住 worker 三十秒的逾時，換成一個你能在一毫秒內處理掉的錯誤。

Then decide what the user sees, because the point of all this is to stay partly up rather than fully down. Not every dependency is critical: if the recommendation service is unavailable, serve the page without recommendations; if a cache is down, go to the database and be slower. Isolating each dependency behind its own connection pool or worker limit - the bulkhead idea - keeps one slow integration from consuming all your capacity. And make the degradation visible: log it, count it, and alert on the circuit breaker opening, because a system that silently drops a feature is a system where nobody notices for a week. The four in order, as a memory hook: timeout stops one call from hanging forever, retry-with-backoff handles a blip, the breaker stops you hammering a wall, and degradation keeps the site up while one room in it is closed.

接著決定使用者看到什麼，因為做這一切的目的是「部分還活著」而不是「整個倒下」。不是每個相依服務都是關鍵的：如果推薦服務不可用，就提供沒有推薦區塊的頁面；如果快取掛了，就去讀資料庫、慢一點。把每個相依服務隔離在自己的連線池或 worker 上限之內 —— 也就是艙壁的概念 —— 可以避免單一個慢速串接吃光你所有的容量。並且讓降級是可見的：把它記錄下來、計數，並在熔斷器打開時告警，因為一個會靜默關掉某個功能的系統，就是那種一整週都沒人發現的系統。四個步驟濃縮成記憶口訣：逾時避免一次呼叫卡到天荒地老、帶退避的重試處理短暫的抖動、熔斷器阻止你一直往牆上撞、降級則讓網站在某個房間關燈時其餘地方還亮著。

## Interview Version

> Start with timeouts, because a missing timeout is the single most common cause of a cascading outage. A call with no deadline does not fail when the dependency is slow - it waits, holding a worker or a connection the whole time. Enough of those and the pool is exhausted, at which point your service is down even though nothing in it is broken. So every outbound call gets an explicit connect and read timeout, chosen from the dependency's real latency rather than left at the library default, which is very often infinite. Retries come next, with two conditions. The operation has to be safe to repeat, meaning idempotent, or a retry on a payment double-charges. And the retry has to back off exponentially with jitter, because synchronised retries from every client turn a struggling dependency into a dead one. Retries also have to be bounded across the whole call chain rather than per hop, since three services each retrying three times is twenty-seven requests for one user action. A circuit breaker is what stops you retrying into a wall: it watches the failure rate, and once that crosses a threshold it opens, so subsequent calls fail immediately without touching the network, which frees your workers and gives the failing service room to recover. Failing fast is better than failing slowly - it converts a timeout that costs a worker thirty seconds into an error you handle in a millisecond. Then decide what the user sees, because the point is to stay partly up rather than fully down: if recommendations are unavailable, serve the page without them; if a cache is down, go to the database and be slower. And make the degradation visible, because a system that silently drops a feature is one where nobody notices for a week.

面試時可回答：從逾時開始，因為「沒有設逾時」是連鎖故障最常見的單一原因。一個沒有期限的呼叫，在依賴變慢時並不會失敗 —— 它會等，而且整段期間都佔著一個 worker 或一條連線。這種情況一多，池子就被榨乾，那一刻你的服務就掛了，儘管它裡面沒有任何東西壞掉。所以每一個對外呼叫都要有明確的連線逾時與讀取逾時，而且要根據那個依賴的真實延遲來訂，不要留在函式庫的預設值 —— 那個預設值往往是無限。接著是重試，附帶兩個條件。這個操作必須可以安全地重複，也就是冪等，否則對付款的一次重試就是重複扣款。而且重試必須採用帶抖動的指數退避，因為所有客戶端同步重試，會把一個苦撐中的依賴直接變成死的。重試也必須有上限，而且是「整條呼叫鏈」的上限而不是每一跳各算 —— 三個服務各重試三次，就是一個使用者動作變成二十七個請求。斷路器則是讓你停止對著一面牆重試的東西：它盯著失敗率，一旦超過門檻就打開，之後的呼叫立刻失敗、完全不碰網路，這釋放了你的 worker，也給那個故障中的服務恢復的空間。快速失敗優於緩慢失敗 —— 它把一個要花掉一個 worker 三十秒的逾時，換成一個你在一毫秒內就能處理的錯誤。然後決定使用者看到什麼，因為這一切的重點是「部分還活著」而不是「整個掛掉」：如果推薦服務不可用，就把頁面在沒有推薦的情況下送出；如果快取掛了，就去打資料庫、慢一點。並且讓降級是看得見的，因為一個會無聲丟掉某個功能的系統，是一個一週後才有人發現的系統。

The sentence to remember is: **Do not wait too long; retry a temporary failure slowly; stop calling what is clearly down; and if you can keep serving with one feature missing, keep serving - timeout, backoff, breaker, degradation.**

最值得記：**不要等太久；暫時失敗可以慢慢重試；確定掛了就先別打；能少一個功能繼續服務就繼續服務 —— 逾時、退避、斷路器、降級。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q35: When would you move work onto a message queue?](q35-message-queues-and-async-work.md) | [All 48 questions](../../README.md) | [Q38: What is a database connection pool, and how do you size it?](q38-connection-pooling.md) |
