# Q36: Monolith or microservices - how would you decide?

> Tests whether you can argue for the boring choice. Reciting the benefits of microservices without naming the operational cost is the failure mode.

**Part:** Architecture & Scaling | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [rest](../_glossary.md#rest), [timeout](../_glossary.md#timeout), [health check](../_glossary.md#health-check)

## In One Sentence

A monolith is one deployable unit and a microservice architecture is many, and the decision is about whether you have enough teams and enough operational maturity to be worth paying for the second one.

單體是一個可部署單位，微服務是很多個；這個決策的重點在於：你是否有足夠的團隊數量和維運成熟度，值得為第二種付出代價。

## Answer Shape

Answer the decision, not the definitions - they already know what the words mean. Start by naming what microservices actually buy, which is independent deployment, then immediately name what they cost, which is that every in-process call becomes a network call that can fail. Then give the honest default for most teams, and finish with the signal that tells you it is time to split.

回答的是這個決策，而不是定義 —— 他們已經知道那兩個詞是什麼意思。先講微服務真正買到的是什麼：獨立部署；接著立刻講它的代價：每一次行程內呼叫都變成一次可能失敗的網路呼叫。然後給出多數團隊的誠實預設，最後說明什麼訊號代表該拆了。

## Full Spoken Answer

The thing microservices actually buy is independent deployment. Each service can be released, rolled back, and scaled on its own schedule, and each team can choose its own stack and move without coordinating a release train with everyone else. That is a real benefit, and notice that it is an organisational benefit before it is a technical one - it matters when you have enough teams that coordinating one deploy has become the bottleneck.

微服務真正買到的是獨立部署。每個服務可以照自己的節奏發布、rollback 和擴充，每個團隊可以選自己的技術堆疊，不必和所有人協調同一班發布列車。這是實實在在的好處，而且要注意它首先是組織上的好處、其次才是技術上的 —— 它要到「團隊多到協調一次部署已經成為瓶頸」時才有意義。

The cost is that you have converted function calls into network calls. What was a method invocation that either returned or raised is now a request that can time out, arrive twice, or half-succeed, so every caller needs timeouts, retries, and a story for partial failure. A transaction that used to be one commit across three tables becomes a distributed workflow with compensating actions, because there is no cross-service rollback. Debugging needs distributed tracing to answer a question a stack trace used to answer for free. And you now need service discovery, per-service CI, per-service monitoring, and a way to run the whole thing locally.

代價是你把函式呼叫換成了網路呼叫。原本是一個「不是回傳就是拋例外」的方法呼叫，現在變成一個可能逾時、可能抵達兩次、可能只成功一半的請求，所以每個呼叫端都需要逾時、重試，以及面對部分失敗的處理方式。原本跨三張表一次提交的交易，變成一套帶補償動作的分散式流程，因為跨服務沒有 rollback。除錯需要分散式追蹤，才能回答以前一份堆疊追蹤免費就能回答的問題。而且你現在還需要服務發現、每個服務各自的 CI、各自的監控，以及一套能在本機跑起整個系統的方法。

So the honest default for most teams is a well-structured monolith: one deployable unit with clear internal module boundaries, so that a domain could be extracted later if it needs to be. This is often called a modular monolith, and it keeps the option open without paying for it upfront. The failure mode to avoid is a distributed monolith - services split by technical layer rather than by domain, so that every feature still requires changing and releasing four of them together. That has all the costs of microservices and none of the independence.

所以對多數團隊而言，誠實的預設是一個結構良好的單體：一個可部署單位，內部有清楚的模組邊界，讓某個領域在需要時能被抽出去。這通常被稱為模組化單體，它保留了未來的選項而不必預先付費。要避免的失敗模式是「分散式單體」—— 服務是照技術分層而不是照領域切開，於是每個功能仍然需要同時改動並一起發布其中四個。那等於承擔了微服務的全部成本，卻沒有得到任何獨立性。

The signal that it is time to split is usually organisational or operational rather than aesthetic: teams blocking each other on a shared release, one part of the system needing wildly different scaling or hardware from the rest, or one component whose failure keeps taking everything else down. When that happens the move is to extract one service along a domain boundary and live with it for a while, not to decompose the whole system at once. And it is worth saying that the prerequisite is operational: without automated deploys, health checks, centralised logging, and tracing already in place, splitting the system multiplies your problems rather than dividing them.

該拆的訊號通常來自組織或維運，而不是美學：團隊在共用的發布上互相卡住、系統的某一部分需要與其餘部分截然不同的擴充規模或硬體，或某個元件一壞就把其他所有東西一起拖垮。當這種情況發生時，做法是沿著一條領域邊界抽出一個服務、然後和它相處一陣子，而不是一次把整個系統拆解掉。另外值得說明的是它的前提是維運面的：如果自動化部署、健康檢查、集中式日誌和追蹤都還沒到位，拆分系統只會讓你的問題相乘，而不是相除。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q27: What is CORS?](../security-and-auth/q27-cors.md) | [All 41 questions](../../README.md) | [Q51: What kind of tests would you write for a new API endpoint?](../testing-and-debugging/q51-testing-a-new-api-endpoint.md) |
