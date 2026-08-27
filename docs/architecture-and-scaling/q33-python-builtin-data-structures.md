# Q33: Explain the underlying data structures of lists, sets, tuples, and dictionaries in Python.

> Tests whether you can derive the performance characteristics from the implementation instead of memorizing a complexity table.

**Part:** Architecture & Scaling | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [index](../_glossary.md#index)

## In One Sentence

A list is a dynamic array and a tuple is a fixed one, while sets and dicts are hash tables - and every performance claim about them follows directly from that.

list 是動態陣列、tuple 是固定陣列，而 set 和 dict 是雜湊表 —— 關於它們的每一個效能說法，都直接由此推導而來。

## Answer Shape

Pair each type with its underlying structure immediately, because the structure is the answer and the behavior is the consequence. Go through them in order, giving the mechanism and then the complexity it implies rather than reciting a table. Save hashing and collisions for last, since that is the standard follow-up and answering it before being asked shows the model is real.

把每個型別立刻和它底層的結構配對，因為結構才是答案，行為只是後果。依序走過四個型別，先給機制、再給它推導出的複雜度，而不是背一張表。把雜湊與碰撞留到最後，因為那是標準的追問，在被問之前就回答出來能顯示這個模型是真的理解過的。

## Full Spoken Answer

A list is ordered, mutable, and allows duplicates, and underneath it is a dynamic array: a contiguous block of memory holding references to the elements. Indexing is therefore O(1) because the address is computed directly. Appending is amortized O(1) - when the block fills, Python allocates a larger one and copies everything over, and it deliberately over-allocates so that resize is rare. Inserting or deleting in the middle is O(n) because every later reference has to shift.

list 是有序、可變、允許重複的，它底層是一個動態陣列：一塊連續的記憶體，存放指向元素的參考。因此以索引存取是 O(1)，因為位址是直接算出來的。附加是攤銷 O(1) —— 當這塊記憶體滿了，Python 會配置更大的一塊並把所有東西複製過去，而且它會刻意過度配置，讓重新配置很少發生。在中間插入或刪除是 O(n)，因為之後的每一個參考都必須位移。

A tuple is ordered, immutable, and allows duplicates, and it is essentially a static array: the size is fixed at creation so no resizing logic is needed. That makes it slightly faster to iterate and index and smaller in memory than an equivalent list. The immutability is not just a style choice - it is what allows a tuple to be hashable, and therefore usable as a dictionary key or a set element, which a list can never be.

tuple 是有序、不可變、允許重複的，本質上是一個靜態陣列：大小在建立時就固定，因此不需要任何重新配置的邏輯。這讓它在走訪與索引時稍快一些，記憶體也比同等的 list 更小。不可變並不只是風格上的選擇 —— 它正是讓 tuple 可雜湊、因而能當字典鍵或集合元素的原因，而 list 永遠做不到這一點。

A set is unordered, mutable, and holds only unique items, and a dict maps unique keys to values, is mutable, and since Python 3.7 preserves insertion order as a language guarantee. Both are hash tables. The key is hashed to pick a slot in an internal array, which gives average O(1) insert, delete, and lookup, and the table resizes once it gets too full to keep collisions rare. Worst case is O(n) when collisions pile up. This is why membership testing in a set is dramatically faster than in a list, and why deduplicating with a set is the idiomatic move.

set 是無序、可變、只保存唯一元素的，而 dict 把唯一的鍵對應到值、可變，並且從 Python 3.7 起把「保留插入順序」列為語言保證。兩者都是雜湊表。鍵被雜湊後用來挑選內部陣列中的一個槽位，因此新增、刪除、查找的平均複雜度是 O(1)，而當表太滿時會重新配置以保持碰撞罕見。最差情況在碰撞堆積時是 O(n)。這正是為什麼在 set 中做成員測試遠比在 list 中快，也是為什麼用 set 去重是慣用做法。

The follow-up is usually what hashing actually means. Python applies a hash function to the key to turn it into an integer, and uses that integer to decide which slot to store or look in - that is where the constant-time behavior comes from. Sometimes two different keys produce the same slot, which is a hash collision, and CPython resolves it with open addressing: if the slot is taken, it probes for the next one in a deterministic sequence, and a lookup follows the same sequence to find the right key. This is also why keys must be immutable. If you could mutate a key after inserting it, its hash would change, and it would be sitting in a slot the table would never probe for it again. The whole answer in one line: don't memorize the complexity table - know the three underlying structures (dynamic array for list, static array for tuple, hash table for both set and dict), and every O() falls out on its own.

接下來的追問通常是「雜湊到底是什麼意思」。Python 對鍵套用雜湊函式把它轉成一個整數，再用那個整數決定要存到哪個槽、或去哪個槽找 —— 常數時間的行為就是從這裡來的。有時兩個不同的鍵會算到同一個槽，這叫雜湊碰撞，CPython 用開放定址法處理：如果槽被佔用，就依照一個確定的序列往下探測，而查找時會沿著同樣的序列找到正確的鍵。這也是為什麼鍵必須是不可變的。如果你能在插入之後修改鍵，它的雜湊值就變了，而它會待在一個表再也不會為它探測的槽裡。整題濃縮成一句：不用背複雜度表，記住底層其實只有三種結構（list 是動態陣列、tuple 是靜態陣列、set 和 dict 都是雜湊表），每個 O() 都能自己推出來。

## Quick Reference

| Type | Ordered | Mutable | Duplicates | Underlying Structure | Average Complexity | Typical Use Case |
|---|---|---|---|---|---|---|
| **List** | ✅ | ✅ | ✅ | Dynamic array | Index O(1), Append O(1), Insert/Delete O(n) | Maintain ordered, modifiable collection |
| **Tuple** | ✅ | ❌ | ✅ | Static array | Index O(1) | Immutable collection, hashable for dict/set |
| **Set** | ❌ | ✅ | ❌ | Hash table | Insert/Delete/Lookup O(1) | Unique items, fast membership test |
| **Dict** | ✅ (3.7+) | ✅ | Keys ❌ | Hash table | Insert/Delete/Lookup O(1) | Key-value mappings, fast lookup |

### The four in code

```python
my_list = [1, 2, 3]
my_list.append(4)
my_list[0] = 10

my_tuple = (1, 2, 3)
# my_tuple[0] = 10  -> Error, immutable

my_set = {1, 2, 3}
my_set.add(4)
print(2 in my_set)      # True

my_dict = {'a': 1, 'b': 2}
my_dict['c'] = 3
print(my_dict['a'])     # 1
```

## Interview Version

> A list is ordered, mutable, and allows duplicates, and underneath it is a dynamic array - a contiguous block of memory holding references. Indexing is O(1) because the address is computed directly. Appending is amortised O(1): when the block fills, Python allocates a larger one and copies everything over, deliberately over-allocating so resizes are rare. Inserting or deleting in the middle is O(n) because every later reference shifts. A tuple is essentially a static array: the size is fixed at creation so no resizing logic is needed, making it slightly faster to iterate and smaller in memory. The immutability is not a style choice - it is what allows a tuple to be hashable and therefore usable as a dict key or set element, which a list can never be. A set holds unique items and a dict maps unique keys to values, and both are hash tables: the key is hashed to pick a slot in an internal array, giving average O(1) insert, delete, and lookup, with the table resizing once it gets too full to keep collisions rare. Worst case is O(n) when collisions pile up. That is why membership testing in a set is dramatically faster than in a list. The follow-up is usually what hashing means: Python turns the key into an integer and uses it to decide which slot to store or look in, and when two keys land on the same slot CPython resolves it with open addressing, probing for the next slot in a deterministic sequence. This is also why keys must be immutable - mutate a key after inserting it and its hash changes, leaving it in a slot the table would never probe again.

面試時可回答：list 是有序、可變、允許重複的，底層是一個動態陣列 —— 一塊連續的記憶體，裝著指向元素的參考。索引是 O(1)，因為位址是直接算出來的。附加是攤銷 O(1)：當那塊空間填滿時，Python 會配置一塊更大的並把所有東西複製過去，而且它刻意多配一些，讓重新配置很少發生。在中間插入或刪除是 O(n)，因為後面每一個參考都得位移。tuple 本質上是一個靜態陣列：大小在建立時就固定，所以不需要任何調整大小的邏輯，這讓它走訪起來稍快、記憶體也更小。不可變性不是風格選擇 —— 它正是讓 tuple 可雜湊、因而能當 dict 的鍵或 set 的元素的原因，而 list 永遠做不到這件事。set 保存不重複的項目，dict 把不重複的鍵對應到值，兩者都是雜湊表：鍵被雜湊後用來挑選內部陣列裡的一個槽，於是插入、刪除、查找的平均複雜度都是 O(1)，而當表太滿時會重新調整大小以維持碰撞罕見。最壞情況在碰撞堆積時是 O(n)。這正是為什麼在 set 裡做成員測試遠比在 list 裡快。接下來的追問通常是「雜湊到底是什麼意思」：Python 把鍵轉成一個整數，並用那個整數決定要存進哪個槽或去哪個槽找；當兩個鍵落在同一個槽，CPython 用開放定址法處理，依一個確定的序列往下探測。這也正是為什麼鍵必須不可變 —— 插入後再改動一個鍵，它的雜湊值就變了，於是它會留在一個表永遠不會再去探測的槽裡。

The sentence to remember is: **Do not memorise the complexity table - know the three structures underneath, and every O() falls out on its own.**

最值得記：**不要背複雜度表 —— 記住底下那三種結構，每一個 O() 都會自己推導出來。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q27: What is CORS?](../security-and-auth/q27-cors.md) | [All 40 questions](../../README.md) | [Q36: Monolith or microservices - how would you decide?](q36-monolith-vs-microservices.md) |
