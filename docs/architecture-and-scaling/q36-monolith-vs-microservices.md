# Q36: Monolith or microservices - how would you decide?

> Tests whether you can argue for the boring choice. Reciting the benefits of microservices without naming the operational cost is the failure mode.

**Part:** Architecture & Scaling | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [idempotent](../_glossary.md#idempotent), [api versioning](../_glossary.md#api-versioning), [idempotency key](../_glossary.md#idempotency-key), [timeout](../_glossary.md#timeout), [health check](../_glossary.md#health-check)

## In One Sentence

Microservices solve organisational and scaling problems and charge you distributed-system complexity for it, so the question is never which is better - it is whether you are yet in a position where that bill is worth paying.

微服務解決的是組織與擴展的問題，代價是分散式系統的複雜度；所以問題從來不是「哪個比較好」，而是「你現在是不是已經到了值得付這筆帳的階段」。

## Answer Shape

Answer the decision, not the definitions - they already know what the words mean. Say up front that you would not pick microservices by default. Name what they actually buy, which is independent deployment and team autonomy, then immediately name the price: every in-process call becomes a network call that can fail. Give the honest default for most teams, and finish with the signals that tell you it is time to split.

回答的是這個決策，而不是定義 —— 他們已經知道那兩個詞是什麼意思。開頭就講明你不會預設選微服務。說出它真正買到的是什麼：獨立部署與團隊自治；接著立刻說出價格：每一次行程內呼叫都變成一次可能失敗的網路呼叫。給出多數團隊的誠實預設，最後說明什麼訊號代表該拆了。

## Full Spoken Answer

I would not choose microservices by default. What I would look at is system complexity, team size, deployment needs, and whether different parts genuinely need to scale independently. Take a new e-commerce system with user, order, payment, and product. If there are three to five engineers, I would build that as one deployable unit: one repo, one pipeline, modules talking through function calls, a transaction across three tables that is still just one commit, and a stack trace that answers "what went wrong" for free.

我不會預設選微服務。我會看的是系統複雜度、團隊規模、部署需求，以及不同部分是不是真的需要獨立擴展。以一個新的電商系統為例，有 user、order、payment、product。如果團隊只有三到五個人，我會把它做成一個可部署單位：一個 repo、一條 pipeline、模組之間用函式呼叫溝通、跨三張表的交易仍然只是一次 commit，而且一份堆疊追蹤就免費回答了「哪裡出錯」。

Splitting that early is where the cost shows up, because you have converted function calls into network calls. The analogy I use is that a function call is turning to the colleague at the next desk and asking a question - you get an answer or you get an exception, and either way you know. A network call is posting a letter. It can get lost, it can arrive twice, and the reply can go missing after the work was already done, so you cannot tell whether it happened. Concretely, `payment = charge(order)` used to either return or raise. As an HTTP call to a payment service it can time out after the card was already charged, and now your retry is a double charge unless you built idempotency keys.

太早拆就是成本現形的地方，因為你把函式呼叫換成了網路呼叫。我會用的比喻是：函式呼叫像轉頭問隔壁桌的同事一句話 —— 你不是得到答案就是得到例外，無論哪種你都知道結果。網路呼叫則像寄一封信。信可能寄丟、可能寄到兩份，也可能對方做完了但回信在路上不見了，於是你根本無從判斷到底做了沒。具體地說，`payment = charge(order)` 原本不是回傳就是拋例外。一旦變成打給 payment 服務的 HTTP 呼叫，它可能在卡片已經扣款之後才逾時，而這時你的重試就是重複扣款 —— 除非你已經做好 idempotency key。

And that is one call. Across a system, splitting adds service discovery, retries and timeouts everywhere, distributed tracing to replace the stack trace, API versioning between services, a message queue, deployment coordination, and distributed transactions with compensating actions because there is no cross-service rollback. That is a lot of machinery to buy for four modules and five engineers.

而那還只是一個呼叫。放大到整個系統，拆分還會帶來服務發現、到處都要的重試與逾時、用來取代堆疊追蹤的分散式追蹤、服務之間的 API 版本管理、訊息佇列、部署協調，以及帶補償動作的分散式交易 —— 因為跨服務沒有 rollback。為了四個模組和五個工程師去買這一整套機具，代價太高了。

Now change the picture. Say the system has grown to user, order, payment, recommendation, notification, and search, with team A on order, team B on payment, and team C on recommendation. Recommendation takes twenty times the traffic of payment. Now microservices start paying for themselves: order runs three replicas, payment five, recommendation fifty, and team C ships recommendation v2 this afternoon without redeploying anything anyone else owns. Notice that both of those wins - independent scaling and independent deployment - are about teams and traffic, not about elegance.

現在換個場景。假設系統長大成 user、order、payment、recommendation、notification、search，A 團隊負責 order、B 團隊負責 payment、C 團隊負責 recommendation。recommendation 的流量是 payment 的二十倍。這時微服務就開始回本了：order 跑三個 replica、payment 五個、recommendation 五十個，而 C 團隊今天下午就能把 recommendation v2 上線，完全不必重新部署任何別人負責的東西。注意這兩個好處 —— 獨立擴展和獨立部署 —— 講的都是團隊和流量，不是優雅。

So the default I would start from is a modular monolith: one deployable unit, but with clear internal boundaries along domains, so a domain can be extracted later when it earns it. Start simple, let the system grow, watch where the real boundaries appear, and extract a service when there is a reason - rather than opening on day one with twenty services and no traffic. The failure mode to avoid is a distributed monolith: services split by technical layer instead of by domain, so every feature still means changing and releasing four of them together. That has all the costs of microservices and none of the independence.

所以我會從模組化單體出發：一個可部署單位，但內部沿著領域有清楚的邊界，讓某個領域在夠格的時候可以被抽出去。從簡單開始，讓系統自己長大，觀察真正的邊界浮現在哪裡，有理由時才抽出一個服務 —— 而不是第一天就開二十個服務、卻一個流量都沒有。要避免的失敗模式是「分散式單體」：服務照技術分層而不是照領域切開，於是每個功能仍然要同時改動並一起發布其中四個。那等於承擔了微服務的全部成本，卻沒有得到任何獨立性。

The signals that it is time are organisational or operational rather than aesthetic: teams blocking each other on a shared release, one part needing wildly different scaling or hardware, or one component whose failure keeps taking everything down. When that happens, extract one service along a domain boundary and live with it for a while instead of decomposing everything at once. One prerequisite is worth stating: without automated deploys, health checks, centralised logging, and tracing already in place, splitting the system multiplies your problems instead of dividing them. The whole answer in one line: microservices buy team autonomy and independent scaling, and they charge distributed-system complexity - so only buy when you can name which team or which traffic spike is paying for it.

該拆的訊號來自組織或維運，而不是美學：團隊在共用的發布上互相卡住、某一部分需要截然不同的擴充規模或硬體，或某個元件一壞就把所有東西一起拖垮。當這種情況出現時，沿著一條領域邊界抽出一個服務、和它相處一陣子，而不是一次把整個系統拆掉。有一個前提值得講明：如果自動化部署、健康檢查、集中式日誌和追蹤都還沒到位，拆分系統只會讓問題相乘，而不是相除。整題濃縮成一句：微服務買到的是團隊自治和獨立擴展，收的是分散式系統複雜度 —— 所以只在你講得出「是哪個團隊、哪一波流量在付這筆錢」的時候才買。

## Quick Reference

### The decision table

| Situation | Lean towards |
|---|---|
| Small team - say under ten engineers | Monolith |
| New product, requirements still moving | Monolith |
| Modules tightly coupled to each other | Monolith |
| Lots of transactions spanning modules | Monolith |
| Several independent teams tripping over one release | Microservices |
| Modules that need to deploy on their own schedule | Microservices |
| Traffic wildly uneven between modules | Microservices |
| Different reliability needs, or a genuinely different stack | Microservices |

Read it as a tally, not a checklist: one row does not decide it, a lopsided column does.

### What the split actually costs

| In a monolith | After splitting |
|---|---|
| `charge(order)` returns or raises | HTTP call that can time out, retry, or double-charge |
| One commit across three tables | Distributed workflow with compensating actions |
| A stack trace | Distributed tracing across services |
| Import the module | Service discovery, API versioning, a message queue |
| One pipeline, one deploy | Per-service CI, monitoring, and deployment coordination |
| Clone the repo and run it | A way to bring the whole system up locally |

### The path to take

```
Start simple
   ↓
Modular monolith - one deploy, clear domain boundaries inside
   ↓
System and team grow; watch where the real boundaries appear
   ↓
Extract one service along a domain boundary, when there is a reason
```

Not: day one → twenty services → no traffic.

## Interview Version

> I would not choose microservices by default. What I would look at is system complexity, team size, deployment needs, and whether different parts genuinely need to scale independently. Take a new e-commerce system with user, order, payment, and product: with three to five engineers I would build that as one deployable unit - one repo, one pipeline, modules talking through function calls, a transaction across three tables that is still one commit, and a stack trace that answers what went wrong for free. Splitting early is where the cost shows up, because you have converted function calls into network calls. A function call is turning to the colleague at the next desk - you get an answer or an exception, and either way you know. A network call is posting a letter: it can get lost, arrive twice, or the reply can go missing after the work was already done, so you cannot tell whether it happened. Concretely, charging a card used to either return or raise; as an HTTP call it can time out after the card was already charged, and now your retry is a double charge unless you built idempotency keys. Across a system, splitting also adds service discovery, retries and timeouts everywhere, distributed tracing to replace the stack trace, a message queue, deployment coordination, and compensating actions because there is no cross-service rollback. Now change the picture: six services, three teams, and recommendation taking twenty times the traffic of payment. Now it pays for itself - order runs three replicas, payment five, recommendation fifty, and one team ships recommendation v2 this afternoon without redeploying anything anyone else owns. So my default is a modular monolith, and I extract a service along a domain boundary when there is a reason.

面試時可回答：我不會預設選微服務。我會看的是系統複雜度、團隊規模、部署需求，以及不同部分是不是真的需要獨立擴展。以一個新的電商系統為例，有 user、order、payment、product：如果團隊只有三到五個人，我會把它做成一個可部署單位 —— 一個 repo、一條 pipeline、模組之間用函式呼叫溝通、跨三張表的交易仍然只是一次 commit，而且一份堆疊追蹤就免費回答了「哪裡出錯」。太早拆就是成本現形的地方，因為你把函式呼叫換成了網路呼叫。函式呼叫像轉頭問隔壁桌的同事 —— 你不是得到答案就是得到例外，無論哪種你都知道結果。網路呼叫則像寄一封信：可能寄丟、可能寄到兩份，也可能對方做完了但回信在路上不見了，於是你根本無從判斷到底做了沒。具體地說，刷一張卡原本不是回傳就是拋例外；一旦變成 HTTP 呼叫，它可能在卡片已經扣款之後才逾時，而這時你的重試就是重複扣款 —— 除非你已經做好 idempotency key。放大到整個系統，拆分還會帶來服務發現、到處都要的重試與逾時、用來取代堆疊追蹤的分散式追蹤、訊息佇列、部署協調，以及帶補償動作的流程，因為跨服務沒有 rollback。現在換個場景：六個服務、三個團隊，而 recommendation 的流量是 payment 的二十倍。這時它就回本了 —— order 跑三個 replica、payment 五個、recommendation 五十個，而某個團隊今天下午就能把 recommendation v2 上線，完全不必重新部署任何別人負責的東西。所以我的預設是模組化單體，並在有理由時沿著領域邊界抽出一個服務。

The sentence to remember is: **Microservices buy team autonomy and independent scaling, and charge distributed-system complexity - so only buy when you can name who is paying for it.**

最值得記：**微服務買到的是團隊自治和獨立擴展，收的是分散式系統複雜度 —— 所以只在你講得出「是誰在付這筆錢」的時候才買。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q33: Explain the underlying data structures of lists, sets, tuples, and dictionaries in Python.](q33-python-builtin-data-structures.md) | [All 42 questions](../../README.md) | [Q41: What is containerization, and how does it benefit backend development?](../devops-and-deployment/q41-what-is-containerization.md) |
