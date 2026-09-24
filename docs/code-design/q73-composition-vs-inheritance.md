# Q73: When would you use composition instead of inheritance?

> Tests whether you can say what inheritance costs, rather than reciting the three pillars of OOP.

**Part:** Code Design | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [dependency injection](../_glossary.md#dependency-injection), [duck typing](../_glossary.md#duck-typing)

## In One Sentence

Inheritance says "I am a kind of that", composition says "I have one of those" - and because inheritance ties you to the parent's internals, composition is the safer default.

繼承是「我就是一種它」，組合是「我有一個它」—— 而因為繼承會把你綁在父類的內部實作上，所以組合是比較安全的預設。

## Answer Shape

Give the quick test first, is-a against has-a, because it sorts most cases in one second. Then go past it to what inheritance actually costs, with one example that visibly breaks, because the cost is the part that separates a real answer from a recited one. State composition as the default and name the two cases where inheritance still wins. Finish with the Python-specific trap, since mixins are where this goes wrong in practice.

先給快速判斷法，is-a 對 has-a，因為它一秒就能分掉大部分情況。然後往下講繼承真正的代價，配一個看得到壞掉的例子，因為代價才是「真的懂」和「背過」的分水嶺。接著把組合定為預設，並說出繼承仍然勝出的兩種情況。最後講 Python 特有的陷阱，因為實務上就是在 mixin 這裡出事。

## Full Spoken Answer

The quick test is to say it out loud. Inheritance is is-a, composition is has-a. "A Dog is an Animal" sounds right, so inheritance is at least plausible. "An OrderService is a Logger" sounds wrong immediately - it just needs a logger, which is has-a, so that should be composition. That sorts most cases in a second. But it is only a filter, not the reason, and the reason is what decides the cases the filter cannot.

快速判斷法是把它唸出來。繼承是 is-a，組合是 has-a。「Dog is an Animal」聽起來對，所以繼承至少說得通。「OrderService is a Logger」一聽就不對 —— 它只是需要一個 logger，那是 has-a，所以該用組合。這一秒就能分掉大部分情況。但它只是一道篩子，不是理由 —— 而篩子分不掉的那些案例，要靠理由才判斷得了。

The real cost is that inheritance couples you to the parent's internals, not just to its public interface. The classic example: you subclass `list` to make a `CountingList` that tracks how many items were added, so you override `append` to increment a counter. Then someone calls `extend`, three items go in, and the counter says zero - because `extend` does not necessarily call your `append` underneath. Now your count is silently wrong, and to understand why you have to go and read the parent's source. This is the fragile base class problem: the parent changes an internal detail in a patch release and your subclass breaks without either side doing anything wrong. Composition does not have this failure mode, because you only ever touch the object through its public methods.

真正的代價是：**繼承把你綁在父類的內部實作上，不只是它的公開介面。** 經典例子：你繼承 `list` 做一個 `CountingList` 來記錄加進來幾筆，於是你覆寫 `append` 讓計數加一。然後有人呼叫 `extend`，進去三筆，計數卻是零 —— 因為 `extend` 底層不一定會呼叫你覆寫的那個 `append`。現在你的計數悄悄錯了，而要搞懂為什麼，你得去讀父類的原始碼。這就是脆弱基底類別問題：父類在某個修補版本改了一個內部細節，你的子類就壞了，而兩邊都沒有做錯任何事。組合沒有這種故障模式，因為你只透過公開方法碰那個物件。

The second cost is the one people rarely mention. Inheritance is decided once, at class definition time, and it cannot be changed afterwards - an object is stuck with the parent it was born with. Composition is decided per instance, at runtime, so the same class can be given a different collaborator in production and in a test. That is exactly why dependency injection works: injecting a fake gateway is composition. Anyone who has tried to test a class that inherits its database access has met this - there is no seam to substitute, because the parent is welded on.

第二個代價很少有人提到。**繼承是在 class 定義時決定一次，之後改不了** —— 一個物件出生時的父類就是它一輩子的父類。組合是每個 instance 在執行時決定的，所以同一個 class 在正式環境和測試裡可以拿到不同的協作者。這正是 dependency injection 能成立的原因：注入一個假的 gateway，本質上就是組合。任何試過去測「一個把資料庫存取繼承下來的 class」的人都遇過這件事 —— 沒有接縫可以替換，因為父類是焊死的。

The old advice to favour composition over inheritance is right, and those two costs are the reason - it is a conclusion, not a slogan. So composition is the default, and inheritance is for two specific cases. The first is a genuine is-a where you actually want polymorphism: several payment gateways sharing one base so callers can treat them interchangeably. The second is when a framework requires it - a Django `Model` or a DRF `APIView` - where you are opting into the framework's contract and that is the whole point. The decision rule that covers the rest: if you are inheriting just to get a few of the parent's methods, what you want is code reuse, not polymorphism, and composition gives you that without the coupling.

「組合優於繼承」這條老建議是對的，而上面那兩個代價就是它的理由 —— 它是一個結論，不是一句口號。所以組合是預設，繼承留給兩種特定情況。第一種是真正的 is-a 而且你確實要多型：好幾個 payment gateway 共用一個基底，讓呼叫方可以無差別地對待它們。第二種是框架要求 —— Django 的 `Model`、DRF 的 `APIView` —— 這時你是刻意接受框架的約定，那本來就是重點。其餘情況用這條規則涵蓋：**如果你繼承只是為了拿到父類的幾個方法，那你要的是程式碼重用，不是多型 —— 用組合就能拿到，而且不必付耦合的代價。**

The Python-specific trap is mixins. Multiple inheritance makes it easy to pile on `LoggingMixin`, `CacheMixin`, `PermissionMixin`, and then nobody can say where a given method actually comes from without walking the MRO. A mixin is only safe when it adds one small orthogonal capability and does not depend on the host class's internals - the moment it starts reading `self.something` that it did not define, it has become a base class in disguise. Python's duck typing also means you need inheritance for polymorphism far less than in Java. Two classes with the same method names are already interchangeable, with no shared ancestor at all, which removes the most common reason people reach for a base class.

Python 特有的陷阱是 mixin。多重繼承讓人很容易一路疊上 `LoggingMixin`、`CacheMixin`、`PermissionMixin`，然後沒有人能不走一遍 MRO 就說出某個方法到底來自哪裡。Mixin 只在「它加的是一個小而正交的能力，而且不依賴宿主 class 的內部」時才安全 —— 一旦它開始讀取自己沒有定義的 `self.something`，它就已經是一個偽裝成 mixin 的基底類別了。另外，Python 的 duck typing 讓「為了多型而繼承」的需求比 Java 少很多。兩個 class 只要方法名字一樣就已經可以互換，完全不需要共同祖先，而這正好消掉了大家伸手去拿基底類別的最常見理由。

## Quick Reference

**The cost, made visible:**

```python
# ❌ 繼承：綁在父類的內部實作上
class CountingList(list):
    def __init__(self): super().__init__(); self.count = 0
    def append(self, item):
        self.count += 1
        super().append(item)

c = CountingList()
c.extend([1, 2, 3])      # extend 底層不一定走你覆寫的 append
print(len(c), c.count)   # 3 0   ← 計數悄悄錯了

# ✅ 組合：只透過公開介面用它
class CountingList:
    def __init__(self): self._items = []; self.count = 0
    def add(self, item):
        self.count += 1
        self._items.append(item)
    # 你只暴露你真的想支援的操作，沒有意外的後門
```

**Two costs inheritance charges you:**

| | Inheritance | Composition |
|---|---|---|
| **Coupled to** | The parent's internals - a patch release can break you | Only the collaborator's public methods |
| **Decided** | Once, at class definition | Per instance, at runtime |
| **Swappable in a test** | No - the parent is welded on | Yes - this is what injection is |
| **Reader has to** | Walk the MRO to find where a method came from | Read one attribute |

**Which one to reach for:**

| Situation | Use | Why |
|---|---|---|
| Several payment gateways treated interchangeably | Inheritance (or a `Protocol`) | A genuine is-a with real polymorphism |
| Django `Model`, DRF `APIView` | Inheritance | The framework's contract - that is the point |
| "I want the parent's three helper methods" | Composition | You want reuse, not polymorphism |
| "I need to swap this in a test" | Composition | Inheritance leaves no seam |
| A mixin that reads `self.x` it did not define | Neither - rework it | It is a base class in disguise |

## Interview Version

> Is-a against has-a sorts most cases in a second, but the reason matters more than the filter. Inheritance couples you to the parent's internals, not just its public interface: subclass `list` and override `append` to count, then `extend` puts three items in and the counter still says zero, because `extend` does not necessarily call your `append` underneath. The parent changes an internal detail in a patch release and your subclass breaks with neither side doing anything wrong. The second cost, rarely mentioned, is that inheritance is decided once at class definition and cannot change afterwards, while composition is decided per instance at runtime - which is exactly why dependency injection works, since injecting a fake is composition. So composition is my default. Inheritance is for a genuine is-a where I actually want polymorphism, and for where a framework requires it, like a Django `Model`. For everything else: if I am inheriting just to get a few of the parent's methods, I want code reuse rather than polymorphism, and composition gives me that without the coupling. The Python-specific trap is mixins - stack three and nobody can say where a method came from without walking the MRO.

面試時可回答：is-a 對 has-a 一秒就能分掉大部分情況，但理由比篩子重要。繼承把你綁在父類的內部實作上，不只是它的公開介面：繼承 `list` 並覆寫 `append` 來計數，然後 `extend` 進去三筆，計數還是零，因為 `extend` 底層不一定會走你覆寫的 `append`。父類在某個修補版本改了一個內部細節，你的子類就壞了，而兩邊都沒做錯任何事。第二個很少有人提的代價是：繼承在 class 定義時決定一次，之後改不了；組合則是每個 instance 在執行時決定 —— 這正是 dependency injection 能成立的原因，因為注入一個假物件本質上就是組合。所以我的預設是組合。繼承留給真正的 is-a 而且我確實要多型的情況，以及框架要求的時候，像 Django 的 `Model`。其餘一律用這條：如果我繼承只是為了拿父類的幾個方法，那我要的是程式碼重用不是多型，而組合能給我，還不用付耦合的代價。Python 特有的陷阱是 mixin —— 疊三個上去，就沒有人能不走一遍 MRO 說出某個方法到底從哪來。

The sentence to remember is: **Inheritance binds you to the parent's internals and is decided once; composition goes through public methods only and can be swapped per instance - so default to composition, and keep inheritance for a real is-a with polymorphism.**

最值得記：**繼承綁的是父類的內部實作，而且只決定一次；組合只走公開方法，還能每個 instance 換掉 —— 所以預設用組合，繼承留給真正的 is-a 加多型。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q72: How do you decide what goes into an interface?](q72-designing-an-interface.md) | [All 51 questions](../../README.md) | [Q83: How do you do code review?](../process-and-collaboration/q83-code-review.md) |
