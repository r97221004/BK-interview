# Q17: Explain database transactions and isolation levels.

> Tests whether you know what your default isolation level actually allows, and whether you can recognise a deadlock and say what causes one.

**Part:** Databases | **Importance:** 9/10 | **Status:** Complete

## In One Sentence

A transaction groups several statements so they either all take effect or none do, and the isolation level decides how much of other in-flight transactions your transaction is allowed to see.

交易把多個敘述句綁成一組，讓它們要嘛全部生效、要嘛全部不生效；而隔離級別決定你的交易能看到多少其他進行中交易的內容。

## Answer Shape

Start with ACID but spend the time on the I, because atomicity is intuitive and isolation is where the interview actually goes. Name the four levels and, for each, the specific anomaly it stops - that pairing is the answer, not the list. Then say what your database actually defaults to, and finish with deadlocks, since that is the follow-up.

從 ACID 開始，但把時間花在 I 上，因為不可分割性很直觀，而隔離性才是面試真正會深入的地方。把四個級別點名，並各配上它所阻止的具體異常 —— 這個配對才是答案，光列出級別不是。接著說出你用的資料庫實際預設是哪一級，最後收在死鎖，因為那是接下來的追問。

## Full Spoken Answer

A transaction is a unit of work that satisfies ACID. Atomicity means all of it commits or none of it does, so a transfer cannot debit one account without crediting the other. Consistency means the database moves from one valid state to another, with constraints upheld. Durability means once you get the commit acknowledgement, the change survives a crash. Those three are rarely argued about. Isolation is the interesting one, because it is not a single guarantee but a dial.

交易是一個滿足 ACID 的工作單位。不可分割性代表全部提交或全部不提交，所以轉帳不可能扣了一邊卻沒加另一邊。一致性代表資料庫從一個有效狀態移動到另一個有效狀態，約束條件維持成立。持久性代表一旦你收到提交確認，這個變更就能撐過當機。這三項很少有爭議，有趣的是隔離性，因為它不是單一的保證，而是一個可調的旋鈕。

The four standard levels stick better as one running story than as four definitions. Picture one account, balance 1000, read at the start of your transaction. At read uncommitted, another transaction can set it to 500 without committing yet, and you already see 500 - a dirty read, and it can evaporate if that other transaction rolls back. Read committed refuses to show you the 500 until it is committed, so dirty reads are gone; but read the balance twice inside your own transaction and someone commits an update in between, and your first read says 1000, your second says 500 - a non-repeatable read, the same row changing under you mid-transaction. Repeatable read pins that row so both reads say 1000, but classically can't pin the whole table: query orders where amount > 1000 and get 10 rows, someone commits an 11th matching row, run the identical query again and get 11 - a phantom, the *set* of rows changing rather than one row's value. Serializable removes even that, behaving as if one transaction ran fully before the other started.

四個標準級別用一個連貫的故事記，比背四條定義好記。想像一個帳戶，餘額 1000，在你的交易一開始讀到。在讀未提交下，另一個交易可以把它改成 500 但還沒提交，而你已經看到 500 —— 這是髒讀，如果對方之後回滾，這筆資料就憑空消失過。讀已提交會擋住這個還沒提交的 500，所以髒讀不見了；但如果你在自己的交易裡讀兩次餘額，中間有人提交了更新，你第一次讀到 1000、第二次讀到 500 —— 這是不可重複讀，同一列資料在你的交易途中變了。可重複讀把那一列釘住，讓兩次都讀到 1000，但傳統上釘不住整張表：查詢 orders where amount > 1000 得到 10 列，有人提交了第 11 列符合條件的新資料，同樣的查詢再跑一次變成 11 列 —— 這是幻讀，變的是「一整批列的集合」而不是某一列的值。可序列化把這些全部消除，表現得就像一個交易完全跑完，另一個才開始。

Reduced to a slogan: each level answers "how much of what the other guy is doing right now am I allowed to see" - uncommitted data, a row that changed under me, or a row set that changed under me - and Serializable is the level that says none of it.

濃縮成一句口訣：每個級別回答的都是同一個問題 ——「對方正在做的事，我能看到多少」：還沒提交的資料？在我交易中途變掉的那一列？還是連整批列的集合都變了？可序列化就是全部都不給看。

Two practical notes are worth having ready. The default differs by engine: PostgreSQL and Oracle default to read committed, MySQL with InnoDB defaults to repeatable read, so the same application code can behave differently on the two. And the levels are defined by the anomalies they must prevent, not by implementation, so real databases can be stricter than the standard requires - InnoDB's repeatable read prevents most phantoms through next-key locking, and PostgreSQL implements serializable optimistically, aborting a transaction at commit rather than blocking it. It also helps to say *how* repeatable read gets its stability without blocking every reader: on Postgres and InnoDB it is MVCC, not locking - your transaction reads from a consistent snapshot taken at its start, so rows committed by someone else afterward are simply invisible to it rather than being blocked or locked.

有兩點實務筆記值得先準備好。預設值因引擎而異：PostgreSQL 和 Oracle 預設是讀已提交，MySQL 搭配 InnoDB 預設是可重複讀，所以同一份應用程式碼在兩者上的行為可能不同。而且這些級別是用「必須阻止哪些異常」來定義的，不是用實作定義，所以真實的資料庫可以比標準更嚴格 —— InnoDB 的可重複讀透過 next-key locking 阻止了大部分幻讀，而 PostgreSQL 的可序列化是樂觀實作，會在提交時中止交易而不是阻塞它。值得補一句可重複讀「怎麼」在不鎖住每個讀者的情況下維持穩定：在 Postgres 和 InnoDB 上靠的是 MVCC 而不是鎖 —— 你的交易讀的是交易開始時那一份一致快照，所以之後別人提交的資料列對你來說根本不存在，而不是被擋住或被鎖住。

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

## Interview Version

> A transaction is a unit of work satisfying ACID. Atomicity means all of it commits or none does, consistency means constraints are upheld, durability means the change survives a crash once acknowledged. Those three are rarely argued about; isolation is the interesting one, because it is not a single guarantee but a dial. The four levels stick better as one story than four definitions. Picture one account, balance 1000. At read uncommitted, another transaction sets it to 500 without committing and you already see 500 - a dirty read, which evaporates if they roll back. Read committed refuses to show the 500 until it commits, so dirty reads are gone; but read twice inside your own transaction with a commit in between and you get 1000 then 500 - a non-repeatable read, the same row changing under you. Repeatable read pins that row so both reads say 1000, but classically cannot pin the whole table: query orders over 1000 and get 10 rows, someone commits an 11th, run it again and get 11 - a phantom, the set of rows changing rather than one row's value. Serializable removes even that. Two practical notes: the default differs by engine, PostgreSQL defaults to read committed and MySQL InnoDB to repeatable read, so the same code behaves differently on each; and repeatable read gets its stability through MVCC rather than locking - your transaction reads from a snapshot taken at its start, so later commits are simply invisible. The follow-up is usually deadlocks: two transactions each holding a lock the other needs, so the database detects the cycle and kills one. The fixes are to acquire locks in a consistent order, keep transactions short, and retry on the deadlock error.

面試時可回答：交易是一個滿足 ACID 的工作單位。原子性代表要嘛全部提交、要嘛都不提交；一致性代表約束被維持住；耐久性代表一旦收到提交確認，那個改變就撐得過當機。這三個很少有人爭論；有趣的是隔離性，因為它不是單一保證，而是一個旋鈕。四個等級當成一個故事比當成四個定義好記。想像一個帳戶，餘額 1000。在 read uncommitted，另一個交易把它設成 500 但還沒提交，你就已經看到 500 —— 這是髒讀，而如果對方回滾，它就蒸發了。read committed 拒絕在提交前把 500 給你看，所以髒讀消失了；但在你自己的交易裡讀兩次、中間有人提交了更新，你就會第一次讀到 1000、第二次讀到 500 —— 這是不可重複讀，同一列在你腳下變了。repeatable read 把那一列釘住，所以兩次都讀到 1000，但傳統上釘不住整張表：查金額大於 1000 的訂單得到 10 列，有人提交了第 11 列符合條件的，再查一次變 11 列 —— 這是幻讀，變的是「那一組列」而不是某一列的值。serializable 連這個都消除。兩個實務補充：預設值因引擎而異，PostgreSQL 預設 read committed、MySQL InnoDB 預設 repeatable read，所以同一份程式碼在兩邊行為不同；而 repeatable read 的穩定性來自 MVCC 而不是鎖 —— 你的交易從它開始時拍下的快照讀取，所以之後別人提交的東西對它根本不可見。接下來的追問通常是死結：兩個交易各自持有對方需要的鎖，於是資料庫偵測到這個環並殺掉其中一個。解法是以一致的順序取得鎖、讓交易保持短，以及在收到死結錯誤時重試。

The sentence to remember is: **Each level answers one question - how much of what the other transaction is doing right now am I allowed to see - and Serializable answers none of it.**

最值得記：**每個隔離等級都在回答同一個問題：「另一個交易此刻正在做的事，我可以看到多少」—— 而 Serializable 的答案是：一點都不行。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q07: What measures would you take to secure a newly developed API?](../api-and-http/q07-securing-a-new-api.md) | [All 42 questions](../../README.md) | [Q18: What is the N+1 query problem, and how do you fix it?](q18-n-plus-one-queries.md) |
