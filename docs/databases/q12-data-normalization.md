# Q12: What is data normalization?

> Tests whether you can explain the normal forms in terms of the update anomalies they prevent, and whether you know when denormalizing is correct.

**Part:** Databases | **Importance:** 9/10 | **Status:** Draft

## In One Sentence

Normalization is organizing tables so that each fact is stored in exactly one place, which stops the data from contradicting itself when you insert, update, or delete.

正規化就是把資料表整理成「每個事實只存在一個地方」，避免資料在新增、更新或刪除時自我矛盾。

## Answer Shape

Define it by the problem it solves - the update anomalies caused by duplicated data - rather than by reciting the normal forms. Then walk 1NF to 3NF with one example each, and state the difference between a partial and a transitive dependency in one line, because that comparison is the question they are actually building toward. Finish with when you would deliberately denormalize.

用它解決的問題來定義它 —— 重複資料造成的更新異常 —— 而不是背誦正規化形式。接著用一個例子帶過 1NF 到 3NF，並用一句話說清楚部分依賴與傳遞依賴的差別，因為那個比較才是他們真正在鋪陳的問題。最後說明什麼時候你會刻意反正規化。

## Full Spoken Answer

Normalization is the process of organizing a database to reduce redundancy and improve consistency, by splitting large tables into smaller related ones connected with foreign keys. The reason it matters is anomalies. If a customer's address is copied into every one of their orders, then updating the address means updating every row, and any row you miss now contradicts the others. Store each fact once and that entire class of bug disappears.

正規化是把資料庫整理成減少冗餘、提升一致性的過程，做法是把大表拆成較小的關聯表，再用外鍵連起來。它之所以重要是因為「異常」。如果把客戶的地址複製到他每一筆訂單裡，那麼更新地址就意味著要更新每一列，而任何一列漏掉，它就和其他列互相矛盾了。讓每個事實只存一次，這一整類的錯誤就消失了。

First normal form requires every column to hold an atomic value - one piece of information, with no lists and no repeating groups. Storing a student's courses as the single string Math, English breaks it; each course belongs in its own row. Second normal form builds on that and requires every non-key attribute to depend on the whole primary key. With a composite key of student and course, a student's name depends only on the student half, so it belongs in a separate students table.

第一正規化要求每個欄位只存放不可再分的原子值 —— 一項資訊，沒有清單也沒有重複群組。把學生的課程存成「數學, 英文」這樣一個字串就違反了它；每門課應該各自佔一列。第二正規化建立在此之上，要求每個非鍵屬性都必須依賴「整個」主鍵。若複合主鍵是學生加課程，學生的姓名只依賴其中的學生那一半，因此它應該被移到獨立的學生資料表。

Third normal form goes one step further: a non-key attribute must not depend on another non-key attribute. If the city determines the postal code, then storing both in the same table means the postal code depends on the city rather than on the row's key, so it moves to its own table. Boyce-Codd normal form is a stricter version of 3NF requiring every determinant to be a candidate key, and it exists to cover rare cases 3NF misses. The one-line distinction worth having ready: 2NF removes partial dependencies on part of a composite key, while 3NF removes transitive dependencies through another non-key column.

第三正規化再往前一步：非鍵屬性不得依賴另一個非鍵屬性。如果城市決定了郵遞區號，那麼把兩者放在同一張表就代表郵遞區號依賴的是城市而不是這一列的鍵，因此它應該搬到自己的表。Boyce-Codd 正規化是 3NF 的更嚴格版本，要求每個決定因子都必須是候選鍵，用來涵蓋 3NF 漏掉的罕見情況。值得先準備好的一句話區分是：2NF 移除的是對複合鍵「一部分」的部分依賴，3NF 移除的是透過另一個非鍵欄位的傳遞依賴。

In practice 3NF is where most designs stop, and denormalizing back is a legitimate decision rather than a failure. A read-heavy dashboard that joins six tables on every page load may be better served by one precomputed row, and an analytics table is usually deliberately wide and flat. The rule is to normalize first so the model is correct, then denormalize specific paths where you have measured the cost, and to know that you have taken on the job of keeping the copies in step.

實務上大多數設計停在 3NF，而往回反正規化是一個正當的決策，不是失敗。一個每次載入都要 join 六張表的讀取密集儀表板，可能用一列預先算好的資料會更好；分析用的表通常也是刻意做得又寬又平。原則是：先正規化讓模型正確，再針對你已經量測過成本的特定路徑做反正規化，並且清楚知道你從此接下了「讓副本保持同步」這份工作。

## Quick Reference

| **Normal Form** | **Definition** | **Example / Purpose** |
|---|---|---|
| **1NF (First Normal Form)** | Every column holds **atomic values**, meaning each field contains only one piece of information — no lists or repeating groups. | A student’s courses shouldn’t be stored as “Math, English” in one cell. Each course should have its own row. |
| **2NF (Second Normal Form)** | Must satisfy 1NF, and **all non-key attributes** must depend on the **entire primary key**, not just part of it. | If you have a composite key like (StudentID, CourseID), attributes like StudentName should not depend only on StudentID. |
| **3NF (Third Normal Form)** | Must satisfy 2NF, and **non-key attributes** should **not depend on other non-key attributes** (no transitive dependency). | For example, if `City → ZipCode`, remove ZipCode to a separate table. |
| **BCNF (Boyce–Codd Normal Form)** | A stronger version of 3NF — every **determinant** (attribute that determines another) must be a **candidate key**. | Used to handle rare edge cases not covered by 3NF. |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q07: What measures would you take to secure a newly developed API?](../api-and-http/q07-securing-a-new-api.md) | [All 29 questions](../../README.md) | [Q22: What is the difference between a session and a cookie?](../security-and-auth/q22-session-vs-cookie.md) |
