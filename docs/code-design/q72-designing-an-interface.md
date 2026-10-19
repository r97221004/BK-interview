# Q72: How do you decide what goes into an interface?

> Tests whether you design an interface from the caller's needs or copy one out of an existing implementation. A wide interface is the tell.

**Part:** Code Design | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [idempotent](../_glossary.md#idempotent), [idempotency key](../_glossary.md#idempotency-key)

## In One Sentence

An interface should be decided by what the caller needs, not by copying the public methods of something you already built.

Interface 該由呼叫方需要什麼來決定，不是把你已經寫好的東西的 public method 抄一遍。

## Answer Shape

Open with the common mistake, because it is what almost everyone does by default: extract the interface from the implementation. Then flip it - ask what the caller needs and let the interface grow from that. Make the difference visible with one example, because said abstractly the two sound the same. Then say how you would actually write it in Python, and finish with when not to add one at all.

從常見的錯誤開場，因為那是幾乎所有人的預設做法：從實作把 interface 抽出來。然後把它翻轉 —— 問呼叫方需要什麼，讓 interface 從那裡長出來。用一個例子讓差別看得見，因為抽象地講這兩件事聽起來一樣。接著說在 Python 實際上會怎麼寫，最後收在「什麼時候根本不該加」。

## Full Spoken Answer

The default move is backwards, and most codebases have it. You write `StripePaymentService` first, it works, and then you extract an interface from it by taking its public methods: `create_charge`, `retrieve_charge`, `create_customer`, `list_refunds`, and a dozen more. The interface now looks exactly like Stripe. So when you try to add PayPal, half those methods have no equivalent and the implementation is full of `raise NotImplementedError`. The interface failed at the one job it existed for, which was letting you swap the implementation.

大家的預設做法是反的，而多數專案都有這個問題。你先寫好 `StripePaymentService`，它能跑，然後你把它的 public method 抄出來變成一個 interface：`create_charge`、`retrieve_charge`、`create_customer`、`list_refunds`，還有十幾個。這個 interface 現在長得跟 Stripe 一模一樣。所以當你要加 PayPal 時，那些方法有一半找不到對應的東西，實作裡塞滿 `raise NotImplementedError`。這個 interface 在它唯一存在的任務上失敗了 —— 它本來是為了讓你換掉實作。

Start from the other end instead. Ask what the business logic actually needs, not what the vendor offers. Usually the answer is surprisingly small: `charge(amount, currency) -> ChargeResult`, and maybe `refund(charge_id)`. That is the whole interface. Everything else - Stripe's idempotency keys, its customer objects, its webhook shapes - is implementation detail and stays inside `StripePaymentService`. The principle underneath is that the interface belongs to the caller, not to the implementer.

改成從另一端開始。問「我的商業邏輯到底需要什麼」，而不是「這家廠商提供什麼」。答案通常小得驚人：`charge(amount, currency) -> ChargeResult`，可能再加一個 `refund(charge_id)`。這樣就是整個 interface 了。其他的 —— Stripe 的 idempotency key、它的 customer 物件、它的 webhook 格式 —— 都是實作細節，留在 `StripePaymentService` 裡面。底下的原則是：**interface 屬於呼叫方，不屬於實作方。**

That gives you a size rule you can apply without thinking hard. A two-method interface is usually healthier than a fifteen-method one, because a long list means you copied an implementation rather than a need. There are two symptoms that tell you an interface is too wide. One is an implementation that has to write `NotImplementedError` for methods it does not support. The other is a caller that only ever uses three of the fifteen methods. Both mean the same thing: split it into smaller interfaces named after what each caller actually does. That is interface segregation, but the symptom is the useful half - the name on its own changes nothing.

這給了你一條不用多想就能套的大小規則。一個兩個方法的 interface，通常比十五個方法的健康，因為方法一長就代表你抄的是實作，不是需求。有兩個症狀會告訴你 interface 太寬了。一個是某個實作被迫為它不支援的方法寫 `NotImplementedError`。另一個是某個呼叫方十五個方法裡只用到三個。兩者代表同一件事：把它拆成比較小的 interface，用「每個呼叫方實際在做什麼」來命名。這就是介面隔離原則，不過有用的是症狀 —— 光記住名字改變不了任何事。

In Python there are three ways to write it and the choice matters. Duck typing means declaring nothing and relying on the object having the right methods - fine for a small script, but nothing tells a reader what shape is expected, and the failure arrives at runtime. An `ABC` makes the implementation inherit from your base class, which works when you own every implementation, but a third-party class can never satisfy it. `typing.Protocol` is structural: any object with the right shape counts, no inheritance required. That is the best default for most cases, and it lines up exactly with the idea above - a `Protocol` can be defined in the caller's own module, so the interface literally lives with the code that needs it.

在 Python 有三種寫法，而選哪一種是有差的。Duck typing 是什麼都不宣告，靠物件剛好有對的方法 —— 小腳本沒問題，但沒有任何東西告訴讀者「這裡期待什麼形狀」，而且錯誤要到執行時才出現。`ABC` 要求實作繼承你的基底類別，當所有實作都是你自己寫的時候可以用，但第三方的 class 永遠不可能符合。`typing.Protocol` 是結構化的：只要形狀對就算數，不必繼承。這是多數情況最好的預設，而且它跟上面那句完全對得上 —— `Protocol` 可以定義在呼叫方自己的模組裡，所以 interface 真的就住在需要它的程式碼旁邊。

The part people miss is knowing when not to add one at all. If there is one implementation and you cannot name a second, use the class directly. An interface added because "we might swap this later" usually buys nothing, and that later rarely arrives - meanwhile every reader has to jump through one extra file to find the five lines that do the work. My rule is to extract the interface when the second implementation actually shows up, or when a test genuinely needs to substitute it. Those two are real reasons. "It is good practice" is not.

大家最常漏掉的一塊，是知道什麼時候根本不該加。如果只有一個實作、而且你講不出第二個會是什麼，那就直接用那個 class。為了「以後可能會換」而先加的 interface 通常什麼也沒買到，而那個「以後」多半不會來 —— 同時每個讀程式的人都得多跳一個檔案，才找得到真正做事的那五行。我的規則是：**第二個實作真的出現時再抽，或是測試真的需要替換它的時候再抽。** 這兩個是真的理由，「這樣寫比較好」不是。

## Quick Reference

**The same interface, extracted the two ways:**

```python
# ❌ 從實作抄出來：長得跟 Stripe 一樣，換 PayPal 就爆
class PaymentService(Protocol):
    def create_charge(self, amount, currency, source, idempotency_key, metadata): ...
    def retrieve_charge(self, charge_id): ...
    def create_customer(self, email, payment_method): ...
    def list_refunds(self, charge_id, limit, starting_after): ...
    # ...還有十個

# ✅ 從呼叫方的需求長出來：商業邏輯只需要這兩件事
class PaymentGateway(Protocol):
    def charge(self, amount: Money) -> ChargeResult: ...
    def refund(self, charge_id: str) -> RefundResult: ...

# Stripe 的 idempotency key、customer 物件、webhook 格式
# 全部留在 StripeGateway 裡面，呼叫方看不到
```

**Choosing how to declare it in Python:**

| | Duck typing | `ABC` | `typing.Protocol` |
|---|---|---|---|
| **Implementation must inherit** | No | Yes | No |
| **Third-party class can satisfy it** | Yes | No | Yes |
| **Where the interface can live** | Nowhere - it is unwritten | With the implementations | With the caller ✅ |
| **Checked by a type checker** | No | Yes | Yes |
| **Reach for it when** | A small script | You own every implementation and want a shared base | Most cases - the sensible default |

**Is this interface the right size?**

| Symptom | What it means | Fix |
|---|---|---|
| An implementation writes `raise NotImplementedError` | The interface describes one vendor, not the need | Cut it back to what callers use |
| A caller uses 3 of 15 methods | One interface is doing several jobs | Split it, named per caller |
| Only one implementation exists and you cannot name a second | It may not need to exist yet | Use the class directly; extract when the second arrives |
| Two methods, both used by every caller | Correctly sized | Leave it |

## Interview Version

> Most codebases extract the interface backwards: write `StripePaymentService` first, then copy its public methods into an interface. It ends up looking exactly like Stripe, so when PayPal arrives half the methods have no equivalent and you are writing `NotImplementedError`. I start from what the business logic needs instead, which is usually just `charge(amount, currency)` and maybe `refund(charge_id)` - Stripe's idempotency keys and customer objects stay inside the implementation. The principle is that the interface belongs to the caller, not the implementer. Two symptoms say one is too wide: an implementation forced to raise `NotImplementedError`, and a caller using three of fifteen methods. In Python I default to `typing.Protocol` rather than an `ABC`, because it needs no inheritance, a third-party class can satisfy it, and it can be defined in the caller's own module. And when there is one implementation and I cannot name a second, I skip the interface and use the class directly - I extract it when the second implementation actually arrives, or when a test needs to substitute it.

面試時可回答：多數專案抽 interface 的方向是反的：先寫 `StripePaymentService`，再把它的 public method 抄成一個 interface。結果它長得跟 Stripe 一模一樣，所以 PayPal 進來時有一半的方法找不到對應，你只能寫 `NotImplementedError`。我改成從「商業邏輯需要什麼」開始，答案通常只有 `charge(amount, currency)`，可能再加一個 `refund(charge_id)` —— Stripe 的 idempotency key 和 customer 物件都留在實作裡面。原則是：interface 屬於呼叫方，不屬於實作方。有兩個症狀代表它太寬了：某個實作被迫 raise `NotImplementedError`，以及某個呼叫方十五個方法只用到三個。在 Python 我預設用 `typing.Protocol` 而不是 `ABC`，因為它不用繼承、第三方 class 也能符合，而且可以定義在呼叫方自己的模組裡。而當只有一個實作、我又講不出第二個會是什麼時，我就不加 interface，直接用那個 class —— 等第二個實作真的出現、或測試真的需要替換它的時候再抽。

The sentence to remember is: **The interface belongs to the caller - grow it from what the business logic needs, not from the methods an implementation happens to have, and two methods usually beat fifteen.**

最值得記：**Interface 屬於呼叫方 —— 從「商業邏輯需要什麼」長出來，不是把某個實作剛好有的方法抄一遍；兩個方法通常勝過十五個。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q63: How do you make an endpoint safe to retry?](../api-design/q63-idempotency-and-retries.md) | [All 52 questions](../../README.md) | [Q73: When would you use composition instead of inheritance?](q73-composition-vs-inheritance.md) |
