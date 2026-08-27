# Q20: How do you change a database schema without downtime?

> Tests whether you know a migration runs while the old code is still serving traffic, and whether you have been bitten by a lock on a large table.

**Part:** Databases | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [index](../_glossary.md#index), [message queue](../_glossary.md#message-queue), [timeout](../_glossary.md#timeout)

## In One Sentence

You never change a column in one step - you add the new shape, get the code writing to both, backfill the old rows, switch reads over, and only then remove what is left.

你永遠不會一步改掉一個欄位 —— 而是先加上新的形狀、讓程式碼同時寫入新舊兩邊、把舊資料回填、把讀取切過去，最後才移除剩下的東西。

## Answer Shape

Start from the constraint that makes this hard: during a deploy the old code and the new code are both running against one database, so every migration has to be compatible with both. That single sentence explains the whole pattern. Then walk expand-and-contract with a rename as the example, and finish with the locking problem, because that is what actually causes the outage.

從讓這件事變難的那個限制講起：部署期間舊版和新版程式碼會同時對著同一個資料庫運行，所以每次遷移都必須同時相容於兩者。光是這一句就能解釋整套模式。接著用「改欄位名稱」當例子走一遍 expand-and-contract，最後收在鎖的問題，因為真正造成停機的是它。

## Full Spoken Answer

The constraint that shapes everything is that a deploy is not atomic. While instances are being replaced, the old version and the new version are both serving traffic against the same database, so the schema has to satisfy both at once. Any migration that is only valid for the new code will break every request still being handled by the old code, and any rollback puts you back in the same situation from the other direction.

決定一切的限制是：部署不是原子操作。當實例正在被替換時，舊版與新版會同時對著同一個資料庫提供服務，所以 schema 必須同時滿足兩者。任何只對新版程式碼有效的遷移，都會弄壞仍由舊版處理的每一個請求；而 rollback 則會從反方向讓你陷入同樣的處境。

That is why the pattern is expand and contract, in separate deploys. Renaming a column is the standard example, and it is never one statement. First expand: add the new column, which is additive and safe for the old code because it simply ignores it. Then deploy code that writes to both columns and still reads the old one. Then backfill the existing rows in batches. Then deploy code that reads the new column. Only once nothing references the old column - and you have left it long enough that a rollback would not need it - do you contract by dropping it. Four or five deploys to rename a column feels excessive until the first time you do it in one and take the site down.

這正是為什麼模式叫做 expand and contract，而且要分成好幾次部署。改欄位名稱是標準例子，而它從來不是一個敘述句能完成的。先 expand：新增新欄位，這是累加式的，對舊版程式碼很安全，因為它會直接忽略。接著部署「同時寫入兩個欄位、但仍讀舊欄位」的程式碼。然後分批回填既有資料列。再部署「讀新欄位」的程式碼。只有在確認沒有任何東西還參照舊欄位、而且已經等得夠久到 rollback 也不需要它之後，才 contract 把它移除。為了改一個欄位名稱要跑四到五次部署，聽起來很誇張 —— 直到你第一次一步做完並把網站弄掛為止。

The other half is locking, and it is what turns a migration into an incident. Some operations rewrite the whole table or take an exclusive lock while they run, and on a large table that means every query behind it queues until it finishes. Adding a nullable column without a default is cheap on modern PostgreSQL and MySQL - milliseconds, regardless of table size. Adding one with a default, changing a type, or adding a constraint can rewrite every row, so on a ten-million-row table that "simple" ALTER TABLE can hold an exclusive lock for ten minutes, and every query behind it queues for the same ten minutes. Build indexes concurrently where the engine supports it, set a short lock timeout so a migration fails fast instead of blocking production behind it, and backfill in batches with a pause rather than one enormous UPDATE that holds a transaction open for an hour.

另一半是鎖，而它正是把一次遷移變成一場事故的原因。有些操作會重寫整張表，或在執行期間取得排他鎖，在大表上這代表後面的每一個查詢都得排隊等它做完。在現代的 PostgreSQL 和 MySQL 上，新增一個可為 null 且沒有預設值的欄位很便宜 —— 不管表多大都是毫秒等級。但新增帶預設值的欄位、改變型別，或加上約束條件，可能要重寫每一列，所以在一千萬列的表上，那個「看起來很簡單」的 ALTER TABLE 可能持有排他鎖十分鐘，後面每一個查詢就跟著排隊十分鐘。在引擎支援時用並行方式建立索引、設定一個短的鎖逾時讓遷移快速失敗而不是把正式環境卡在它後面，並且分批回填、中間留間隔，而不是用一個巨大的 UPDATE 把交易開著一小時。

Operationally, migrations live in version control alongside the code, run through a tool that tracks which ones have been applied - Alembic or Django's migration framework - and are reviewed like any other change. Two habits are worth stating: every migration should be tested against a copy of production-sized data, because that same statement that is instant on a ten-row dev table is the one that locks the real table for ten minutes, and destructive steps should be separated from the deploy that stops using the data, so that rolling back the code does not mean the data is already gone. The whole answer in one line: never change a live column in place - add, dual-write, backfill, switch, then remove, each as its own deploy.

在維運上，遷移檔案與程式碼一起進版本控制，透過會追蹤「哪些已經套用」的工具執行 —— Alembic 或 Django 的 migration 框架 —— 並且像其他變更一樣經過審查。有兩個習慣值得說出來：每個遷移都應該對著與正式環境同等資料量的副本測試過，因為同一句在十列的開發用資料表上瞬間完成的敘述句，換到正式環境就是那個鎖表十分鐘的元凶；而破壞性的步驟應該和「停止使用該資料」的那次部署分開，這樣 rollback 程式碼時才不會發現資料已經沒了。整題濃縮成一句：永遠不要直接改動一個正在使用中的欄位 —— 新增、雙寫、回填、切換、最後才移除，每一步各自獨立部署。

## Quick Reference

### Expand and contract, for renaming a column

| Step | Deploy | Old code still works? |
|---|---|---|
| 1. Expand | Add the new column, nullable | Yes - it ignores the new column |
| 2. Dual write | Code writes both columns, reads the old one | Yes |
| 3. Backfill | Copy existing rows in batches | Yes |
| 4. Switch reads | Code reads the new column, still writes both | Yes |
| 5. Stop writing | Code writes and reads only the new column | No - rollback boundary is here |
| 6. Contract | Drop the old column | n/a |

Steps 5 and 6 belong in separate deploys: once the old column is dropped, a
rollback to step 4 has nothing to read.

## Interview Version

> The constraint that shapes everything is that a deploy is not atomic. While instances are being replaced, the old version and the new version are both serving traffic against the same database, so the schema has to satisfy both at once - any migration only valid for the new code breaks every request still handled by the old code, and a rollback puts you in the same situation from the other direction. That is why the pattern is expand and contract, in separate deploys. Renaming a column is the standard example and it is never one statement. First expand: add the new column, which is additive and safe because the old code ignores it. Then deploy code that writes to both and still reads the old one. Then backfill existing rows in batches. Then deploy code that reads the new column. Only once nothing references the old column, and you have waited long enough that a rollback would not need it, do you contract by dropping it. Four or five deploys to rename a column feels excessive until the first time you do it in one and take the site down. The other half is locking, which is what turns a migration into an incident. Adding a nullable column without a default is milliseconds on modern PostgreSQL and MySQL regardless of table size, but adding one with a default, changing a type, or adding a constraint can rewrite every row - so on a ten-million-row table that simple-looking ALTER TABLE holds an exclusive lock for ten minutes, and every query behind it queues for the same ten minutes. Build indexes concurrently, set a short lock timeout so a migration fails fast instead of blocking production, and backfill in batches with a pause rather than one enormous UPDATE.

面試時可回答：形塑一切的限制是：部署不是原子的。在實例被逐一替換的期間，舊版本和新版本會同時對著同一個資料庫服務流量，所以 schema 必須同時滿足兩者 —— 任何只對新程式碼有效的遷移，都會弄壞每一個還由舊程式碼處理的請求；而回滾則會從另一個方向把你放回同樣的處境。這正是為什麼模式是「擴張與收縮」，而且分成不同次部署。改欄位名稱是標準例子，而它從來不是一道語句。先擴張：新增那個新欄位，這是加法的、對舊程式碼是安全的，因為舊程式碼會直接忽略它。接著部署一版「同時寫兩個欄位、但仍然讀舊的」的程式碼。然後分批回填既有的資料列。再部署一版「讀新欄位」的程式碼。只有在沒有任何東西再引用舊欄位、而且你已經等得夠久、久到回滾也不會需要它時，才收縮、把它刪掉。為了改一個欄位名稱要部署四、五次，聽起來很誇張 —— 直到你第一次用一次部署搞定它、然後把網站弄掛。另一半是鎖，那才是把一次遷移變成一起事故的東西。在現代 PostgreSQL 和 MySQL 上，新增一個沒有預設值的可空欄位是毫秒等級，跟表格大小無關；但新增一個帶預設值的欄位、改型別、或加上約束，可能會重寫每一列 —— 於是在一張一千萬列的表上，那個看起來很單純的 ALTER TABLE 會持有獨占鎖十分鐘，而排在它後面的每一個查詢，也就一起排隊十分鐘。用 concurrently 建索引、設定一個短的 lock timeout 讓遷移快速失敗而不是卡住正式環境，並且分批回填、中間留間隔，而不是跑一個巨大的 UPDATE。

The sentence to remember is: **Never change a live column in place - add, dual-write, backfill, switch, then remove, each as its own deploy.**

最值得記：**絕不原地改動一個上線中的欄位 —— 新增、雙寫、回填、切換、再移除，每一步各自一次部署。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q19: How do you decide what to cache, and how do you invalidate it?](q19-caching-strategy-and-invalidation.md) | [All 42 questions](../../README.md) | [Q22: What is the difference between a session and a cookie?](../security-and-auth/q22-session-vs-cookie.md) |
