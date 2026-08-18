# Q17: Explain database transactions and isolation levels.

> Tests whether you know what your default isolation level actually allows, and whether you can recognise a deadlock and say what causes one.

**Part:** Databases | **Importance:** 9/10 | **Status:** Draft

## In One Sentence

A transaction groups several statements so they either all take effect or none do, and the isolation level decides how much of other in-flight transactions your transaction is allowed to see.

交易把多個敘述句綁成一組，讓它們要嘛全部生效、要嘛全部不生效；而隔離級別決定你的交易能看到多少其他進行中交易的內容。

## Answer Shape

Start with ACID but spend the time on the I, because atomicity is intuitive and isolation is where the interview actually goes. Name the four levels and, for each, the specific anomaly it stops - that pairing is the answer, not the list. Then say what your database actually defaults to, and finish with deadlocks, since that is the follow-up.

從 ACID 開始，但把時間花在 I 上，因為不可分割性很直觀，而隔離性才是面試真正會深入的地方。把四個級別點名，並各配上它所阻止的具體異常 —— 這個配對才是答案，光列出級別不是。接著說出你用的資料庫實際預設是哪一級，最後收在死鎖，因為那是接下來的追問。

## Full Spoken Answer

A transaction is a unit of work that satisfies ACID. Atomicity means all of it commits or none of it does, so a transfer cannot debit one account without crediting the other. Consistency means the database moves from one valid state to another, with constraints upheld. Durability means once you get the commit acknowledgement, the change survives a crash. Those three are rarely argued about. Isolation is the interesting one, because it is not a single guarantee but a dial.

交易是一個滿足 ACID 的工作單位。不可分割性代表全部提交或全部不提交，所以轉帳不可能扣了一邊卻沒加另一邊。一致性代表資料庫從一個有效狀態移動到另一個有效狀態，約束條件維持成立。持久性代表一旦你收到提交確認，這個變更就能撐過當機。這三項很少有爭議，有趣的是隔離性，因為它不是單一的保證，而是一個可調的旋鈕。

The four standard levels are best remembered by the anomaly each one removes. Read uncommitted allows dirty reads: you can see another transaction's uncommitted changes, which may then be rolled back. Read committed removes dirty reads but allows non-repeatable reads: the same row read twice in your transaction can differ, because someone committed in between. Repeatable read removes that but classically allows phantom reads: the same range query returns new rows that another transaction inserted. Serializable removes all of them, behaving as if transactions ran one after another.

四個標準級別最好用「各自消除了哪個異常」來記。讀未提交允許髒讀：你會看到其他交易尚未提交的變更，而那些變更之後可能被回滾。讀已提交消除髒讀，但允許不可重複讀：同一列在你的交易中讀兩次可能不一樣，因為中間有人提交了。可重複讀消除不可重複讀，但傳統上允許幻讀：同一個範圍查詢會出現其他交易新插入的資料列。可序列化把以上全部消除，表現得就像交易是一個接一個依序執行的。

Two practical notes are worth having ready. The default differs by engine: PostgreSQL and Oracle default to read committed, MySQL with InnoDB defaults to repeatable read, so the same application code can behave differently on the two. And the levels are defined by the anomalies they must prevent, not by implementation, so real databases can be stricter than the standard requires - InnoDB's repeatable read prevents most phantoms through next-key locking, and PostgreSQL implements serializable optimistically, aborting a transaction at commit rather than blocking it.

有兩點實務筆記值得先準備好。預設值因引擎而異：PostgreSQL 和 Oracle 預設是讀已提交，MySQL 搭配 InnoDB 預設是可重複讀，所以同一份應用程式碼在兩者上的行為可能不同。而且這些級別是用「必須阻止哪些異常」來定義的，不是用實作定義，所以真實的資料庫可以比標準更嚴格 —— InnoDB 的可重複讀透過 next-key locking 阻止了大部分幻讀，而 PostgreSQL 的可序列化是樂觀實作，會在提交時中止交易而不是阻塞它。

The follow-up is usually deadlocks. A deadlock is two transactions each holding a lock the other needs, so neither can proceed; the database detects the cycle and kills one, which surfaces in your application as an error on an otherwise correct statement. The standard cause is two code paths locking the same rows in different orders, and the standard fixes are to always acquire locks in a consistent order, keep transactions short so locks are held briefly, and make the caller retry on the deadlock error rather than treating it as fatal. Higher isolation costs concurrency, so the honest position is to use the weakest level that is still correct for the operation, and raise it deliberately where money or inventory is involved.

接下來的追問通常是死鎖。死鎖是兩個交易各自持有對方需要的鎖，因此誰都無法前進；資料庫偵測到這個循環後會殺掉其中一個，在你的應用程式裡就表現成「一個本身正確的敘述句卻出錯」。標準成因是兩條程式路徑以不同順序鎖定同一批資料列，標準修法是：永遠以一致的順序取得鎖、讓交易保持短小以縮短持鎖時間，並讓呼叫端在收到死鎖錯誤時重試，而不是把它當成致命錯誤。隔離級別越高，併發度成本越大，所以誠實的立場是：用「仍然正確」的最弱級別，並在牽涉金錢或庫存時刻意調高。

## Quick Reference

| Level | Dirty read | Non-repeatable read | Phantom read | Typical default |
|---|---|---|---|---|
| **Read uncommitted** | ✅ possible | ✅ possible | ✅ possible | rarely used |
| **Read committed** | ❌ prevented | ✅ possible | ✅ possible | PostgreSQL, Oracle, SQL Server |
| **Repeatable read** | ❌ prevented | ❌ prevented | ✅ possible in the standard | MySQL / InnoDB |
| **Serializable** | ❌ prevented | ❌ prevented | ❌ prevented | opt in when correctness demands it |

✅ = the anomaly can still occur at this level.

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q07: What measures would you take to secure a newly developed API?](../api-and-http/q07-securing-a-new-api.md) | [All 41 questions](../../README.md) | [Q18: What is the N+1 query problem, and how do you fix it?](q18-n-plus-one-queries.md) |
