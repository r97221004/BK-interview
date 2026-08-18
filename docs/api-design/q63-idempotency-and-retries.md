# Q63: How do you make an endpoint safe to retry?

> Tests whether you have thought about what happens when a client times out and retries a payment - the classic double-charge.

**Part:** API Design & Reliability | **Importance:** 7/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [resource](../_glossary.md#resource), [message queue](../_glossary.md#message-queue)

## In One Sentence

An endpoint is safe to retry when sending the same request twice has the same effect as sending it once, which for anything that creates or charges means the client attaches a key you use to recognise the repeat.

一個 endpoint 之所以能安全重試，是因為同一個請求送兩次和送一次的結果相同；對於任何會建立資料或扣款的操作，這意味著客戶端要附上一把鑰匙，讓你能辨認出這是重複的那一次。

## Answer Shape

Start from why this matters at all: the client cannot tell a lost response from a failed request, so it will retry, and you do not get to prevent that. Then separate the methods that are already idempotent from POST, which is not. Give the idempotency key mechanism concretely, and finish with the honest limit - at-least-once delivery is what you actually get.

從「為什麼這件事重要」開始：客戶端無法分辨「回應弄丟了」和「請求失敗了」，所以它一定會重試，而你阻止不了。接著把本來就冪等的方法和不冪等的 POST 分開。具體給出 idempotency key 的機制，最後收在誠實的極限 —— 你實際上拿到的保證是「至少一次」。

## Full Spoken Answer

The problem starts with an ambiguity the client cannot resolve. If a request times out, the client has no way to know whether the server never received it, received it and failed, or completed it successfully and the response was lost on the way back. From where it stands those look identical, so it retries - and if the request was a payment that actually succeeded, the customer is charged twice. You cannot design that retry away, so the endpoint has to be built to absorb it.

問題起於一個客戶端無法解決的歧義。如果一個請求逾時，客戶端沒有辦法知道究竟是伺服器從未收到、收到了但失敗了，還是已經成功完成而回應在返程弄丟了。從它的角度看這三者一模一樣，所以它會重試 —— 而如果那個請求是一筆真的成功了的付款，客戶就被扣了兩次款。你沒辦法把這個重試設計掉，所以 endpoint 必須被打造成能吸收它。

Some of this comes free from HTTP. GET, PUT, and DELETE are defined as idempotent: reading twice changes nothing, setting a resource to a given state twice leaves it in that state, and deleting an already-deleted resource still leaves it deleted. POST is the one that is not, because it means create another one - which is exactly why the double-charge problem belongs to POST. Where the operation genuinely fits PUT with a client-chosen identifier, using it is the simplest possible answer and needs no extra machinery.

其中一部分是 HTTP 免費給的。GET、PUT、DELETE 依定義就是冪等的：讀兩次不改變任何東西、把資源設定成某個狀態兩次仍然是那個狀態、刪除一個已被刪除的資源它依然是被刪除的。POST 則是不冪等的那一個，因為它的意思是「再建立一個」—— 這正是為什麼重複扣款問題屬於 POST。當某個操作真的適合用 PUT 搭配客戶端自選的識別碼時，直接那樣做就是最簡單的答案，不需要任何額外機制。

For POST, the standard mechanism is an idempotency key. The client generates a unique value, usually a UUID, and sends it in a header; it must be generated once for the logical operation and reused across retries, not regenerated each attempt. The server records the key before doing the work, and on seeing a key it has already completed, it returns the stored original response instead of doing the work again. Two details make it correct rather than approximately correct: the key and the result must be written in the same transaction as the operation itself, otherwise a crash between them reopens the hole; and concurrent retries need a unique constraint or a lock on the key, so the second one waits or is rejected rather than racing through beside the first. Keys expire after a window, typically twenty-four hours.

對於 POST，標準機制是 idempotency key。客戶端產生一個唯一值（通常是 UUID）並放在標頭送出；這個值必須為「一次邏輯操作」產生一次，並在各次重試間重複使用，而不是每次嘗試都重新產生。伺服器在動手之前先記下這把鑰匙，之後若看到一把已經完成過的鑰匙，就回傳先前存下的原始回應，而不是再做一次。有兩個細節決定它是「真的正確」還是「大致正確」：鑰匙與結果必須和操作本身寫在同一個交易裡，否則兩者之間當機就會重新打開那個洞；以及並行的重試需要對鑰匙加上唯一性約束或鎖，讓第二個請求等待或被拒絕，而不是與第一個並排衝過去。鑰匙會在一段時間後過期，通常是二十四小時。

The honest framing is that you are converting at-least-once delivery into effectively-once processing. You cannot get exactly-once delivery over an unreliable network - the client will always be able to send the request twice - so the guarantee has to live in the handler, not in the transport. That is the same reason every queue consumer needs to be idempotent, since queues also deliver at least once. A useful way to close is that this is a property you design in per endpoint, and the ones that need it most are exactly the ones where a duplicate is expensive: payments, order creation, and sending anything to a customer.

誠實的說法是：你是在把「至少一次交付」轉換成「效果上只發生一次的處理」。在不可靠的網路上你拿不到「剛好一次交付」—— 客戶端永遠有能力把請求送兩次 —— 所以這個保證必須住在處理函式裡，而不是傳輸層裡。這也是為什麼每個佇列消費者都需要具備冪等性，因為佇列同樣是至少一次交付。一個好的收尾是：這是你逐一為每個 endpoint 設計進去的性質，而最需要它的，正是那些「重複一次就很貴」的操作：付款、建立訂單，以及任何會發送給客戶的東西。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q62: How would you paginate a large collection endpoint?](q62-pagination.md) | [All 37 questions](../../README.md) | [Q15: What strategies do you have when a database runs out of storage?](../databases/q15-database-out-of-storage.md) |
