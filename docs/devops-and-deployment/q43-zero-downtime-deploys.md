# Q43: How do you deploy a new version without dropping requests?

> Tests whether you have shipped to production. The revealing part is what you do when the new version is bad, not how you get it out.

**Part:** DevOps & Deployment | **Importance:** 7/10 | **Status:** Draft

**New to these terms?** [resource](../_glossary.md#resource), [cache](../_glossary.md#cache), [load balancer](../_glossary.md#load-balancer), [message queue](../_glossary.md#message-queue), [schema migration](../_glossary.md#schema-migration)

## In One Sentence

You start the new version alongside the old one, wait for it to pass a health check before sending it traffic, shift traffic over gradually, and keep the old version around long enough to switch back.

你會讓新版本和舊版本並存啟動、等它通過健康檢查之後才把流量導過去、逐步移轉流量，並且把舊版本保留夠久，久到你隨時可以切回去。

## Answer Shape

Describe the mechanism before the strategies, because without health checks and connection draining all three strategies drop requests. The skeleton is ready, shift, watch, roll back. Give rolling, blue-green, and canary as three answers to the middle step, with what each one costs, and say that canary is the only one that limits how many users meet a bad release. Then spend your last sentence on rollback, because that is what the question is really testing: getting a good version out is easy, getting a bad one back out under pressure is not.

先描述機制再講策略，因為少了健康檢查與連線排空，三種策略都會掉請求。骨架是就緒、切換、觀察、回滾。把 rolling、blue-green、canary 當成中間那一步的三種答案，各自附上代價，並說明 canary 是唯一能限制「多少使用者碰到壞版本」的做法。最後把一句話留給 rollback，因為這才是這題真正在考的：把好版本推出去很容易，在壓力下把壞版本收回來才難。

## Full Spoken Answer

Underneath every strategy are two mechanisms, and without them the strategy does not matter. The first is the health check: the load balancer only sends traffic to an instance that reports ready, so a new version that has not finished starting or cannot reach its database never receives a request. It is worth separating liveness, meaning the process is alive, from readiness, meaning it can serve - a process that is up but whose database connection is not yet established should fail readiness, not be killed. The second is connection draining: when an instance is being removed, it is taken out of the pool first and given time to finish the requests it is already handling, so in-flight work is not cut off mid-response.

所有策略底下都有兩個機制，少了它們策略本身就沒有意義。第一個是健康檢查：load balancer 只把流量送到回報「就緒」的實例，所以還沒啟動完成、或連不上資料庫的新版本永遠不會收到請求。值得區分 liveness（行程還活著）和 readiness（它能提供服務）—— 一個已經啟動但資料庫連線尚未建立的行程應該讓 readiness 失敗，而不是被殺掉。第二個是連線排空：當某個實例要被移除時，先把它從流量池中拿掉，再給它時間處理完手上已經在進行的請求，這樣進行中的工作才不會在回應到一半時被切斷。

A rolling deploy replaces instances a few at a time, so capacity stays roughly constant and only one extra instance's worth of resource is needed. The consequence is that both versions run simultaneously for the duration, which is exactly why the database schema has to be compatible with both. Blue-green instead stands up a complete second environment, tests it, and switches all traffic at once; the cutover and the rollback are both instant, which is its main appeal, and the cost is running double the infrastructure during the switch.

rolling 部署一次替換少量實例，因此總容量大致維持不變，只需要多出一台實例左右的資源。它的後果是兩個版本在整個過程中同時運行，這正是為什麼資料庫 schema 必須同時相容於兩者。blue-green 則是另外架起一整套完整環境、測試它，然後一次把所有流量切過去；切換和 rollback 都是瞬間完成，這是它的主要賣點，代價則是切換期間要跑雙倍的基礎設施。

A canary sends a small slice of real traffic - one percent, then five, then twenty - to the new version while watching its error rate and latency against the old one, and promotes or aborts based on what it sees. It is the only one of the three that limits how many users are exposed to a bad release, which is why it is the right choice for anything risky, and it needs real per-version metrics to be worth doing. A feature flag is the finer-grained version of the same idea: ship the code dark, then turn the behaviour on for a subset of users independently of the deploy, which also decouples releasing from deploying.

canary 把一小部分真實流量 —— 百分之一、然後百分之五、然後百分之二十 —— 導向新版本，同時盯著它的錯誤率與延遲並與舊版比較，再根據結果決定推進或中止。它是三者中唯一能限制「有多少使用者暴露在壞版本下」的做法，這也是為什麼任何有風險的變更都該選它；而它必須有真正的分版本指標才值得做。feature flag 是同一個概念更細緻的版本：把程式碼先關著發布出去，之後再獨立於部署之外，針對一部分使用者打開那個行為，這同時也讓「發布」和「部署」解耦。

The part worth spending your last sentence on is rollback, because that is what the question is really testing. Keep the previous image and be able to redeploy it with one command, and know your rollback time the way you know your deploy time. The thing that makes rollback hard is almost never the code - it is state: a migration that already dropped a column, a queue full of messages only the new version understands, or a cache populated in a new format. That is why destructive schema changes are separated from the deploy that stops using the data, and why a deploy should be observed rather than declared finished - watch error rate, latency, and saturation for a while afterwards, because the failure often shows up minutes later under real load rather than at the moment of the switch.

值得把最後一句花在 rollback 上，因為這才是這題真正在考的東西。保留前一個映像檔，並且能用一個指令把它重新部署回去，而且要像知道部署時間一樣清楚知道自己的 rollback 時間。讓 rollback 變困難的幾乎從來不是程式碼，而是狀態：一個已經把欄位刪掉的遷移、一個裝滿只有新版看得懂的訊息的佇列，或一個以新格式填好的快取。這正是為什麼破壞性的 schema 變更要和「停止使用該資料」的那次部署分開，也是為什麼部署應該被「觀察」而不是被「宣告完成」—— 之後要持續盯著錯誤率、延遲和飽和度一段時間，因為故障往往是在幾分鐘後真實負載下才浮現，而不是在切換的那一刻。

## Quick Reference

### The skeleton to memorise

**Ready → Shift → Watch → Roll back**

| Step | What has to be true |
|---|---|
| **Ready** | The load balancer only sends traffic to an instance that passes its readiness check, and an instance being removed is drained first so in-flight requests finish. Liveness means the process is alive; readiness means it can actually serve |
| **Shift** | Pick a strategy below. Whichever you pick, both versions run at once, so the schema must be compatible with both - see [Q20](../databases/q20-schema-migrations.md) |
| **Watch** | Error rate, latency, and saturation for a while afterwards. Failures usually appear minutes later under real load, not at the moment of the switch |
| **Roll back** | The previous image, one command away, with a rollback time you actually know |

### The three ways to shift

| Strategy | How traffic moves | Extra capacity | Blast radius of a bad release | Rollback |
|---|---|---|---|---|
| **Rolling** | A few instances at a time | ~1 instance | Grows as the rollout proceeds | Roll forward or roll back through the same process |
| **Blue-green** | All at once, at the switch | 2x during cutover | Everyone, immediately | Instant - switch back to blue |
| **Canary** | 1% → 5% → 20% → 100%, watched | 1 instance upward | Limited to the slice, by design | Abort and drop the canary |
| **Feature flag** | Deploy dark, enable per user | none | Whoever the flag is on for | Turn the flag off - no deploy |

Rollback is almost never hard because of the code - it is hard because of state:
a migration that already dropped a column, a queue full of messages only the new
version understands, a cache in a new format. That is why destructive schema
changes ship separately from the deploy that stops using the data.

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q37: How do you stop one slow dependency from taking down your service?](../architecture-and-scaling/q37-timeouts-retries-and-failure.md) | [All 41 questions](../../README.md) | [Q52: What tools and techniques do you use for debugging a backend application?](../testing-and-debugging/q52-debugging-a-backend-application.md) |
