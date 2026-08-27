# Q11: Can you explain the difference between SQL and NoSQL databases?

> Tests whether you can choose between them for a stated workload, rather than reciting 'SQL is structured, NoSQL is flexible'.

**Part:** Databases | **Importance:** 10/10 | **Status:** Complete

**New to these terms?** [acid](../_glossary.md#acid), [partitioning](../_glossary.md#partitioning), [index](../_glossary.md#index), [redis](../_glossary.md#redis), [horizontal scaling](../_glossary.md#horizontal-scaling)

## In One Sentence

A SQL database stores data in tables with a fixed schema and guarantees transactions across them, while NoSQL is an umbrella for stores that relax the schema or the guarantees in exchange for flexibility and easier horizontal scale.

SQL 資料庫把資料存在具有固定結構描述的資料表裡，並保證跨表的交易；NoSQL 則是一個統稱，泛指那些放寬結構描述或交易保證，以換取彈性與更容易水平擴充的儲存系統。

## Answer Shape

Describe each family by what it guarantees rather than by how it looks, because the schema difference is the surface and the guarantees are the substance. Say that NoSQL is four different families, not one thing. Then answer the question the interviewer really wants: how you would choose for a stated workload, and finish by admitting the line has blurred.

用「它保證什麼」而不是「它長什麼樣」來描述兩邊，因為結構描述的差異只是表面，保證才是實質。要說清楚 NoSQL 是四個不同家族，不是單一種東西。接著回答面試官真正想聽的：面對一個具體工作負載你會怎麼選；最後坦白說明兩者的界線已經模糊。

## Full Spoken Answer

SQL databases, also called relational databases, store data in tables with a predefined schema and explicit relationships between them. They follow ACID - atomicity, consistency, isolation, and durability - which is what lets you move money between two accounts and be certain that either both rows changed or neither did. They also give you a declarative query language with joins, so a question you did not anticipate at design time is still answerable without changing how the data is stored.

SQL 資料庫又稱關聯式資料庫，把資料存在具有預先定義結構描述的資料表中，表與表之間有明確的關聯。它們遵守 ACID —— 不可分割性、一致性、隔離性、持久性 —— 這正是讓你能在兩個帳戶之間轉帳，並且確定「兩列都改了」或「兩列都沒改」的原因。它們同時提供帶 join 的宣告式查詢語言，所以即使是設計當下沒預料到的問題，也不必改變資料的儲存方式就能查得出來。

NoSQL is not one thing; it is at least four families with different shapes. Document stores such as MongoDB keep nested records and suit data that is naturally read as one object. Key-value stores such as Redis reach every value through its key, which is what makes the lookup as fast as it gets, though the values themselves can still be rich data structures. Wide-column stores such as Cassandra are built for enormous write volume across many nodes. Graph databases such as Neo4j make relationship traversal the cheap operation. What they share is a flexible or absent schema and a design that assumes scaling out rather than up, and the way they buy that scale is by giving up the two things that are expensive to coordinate across machines: joins, and transactions spanning several records.

NoSQL 並不是單一種東西，它至少是四個形狀不同的家族。文件資料庫（例如 MongoDB）保存巢狀的紀錄，適合天生就會被當成一個物件讀取的資料。鍵值資料庫（例如 Redis）一律透過鍵取得資料，這正是它查找能快到極限的原因，不過值本身仍然可以是豐富的資料結構。寬欄位資料庫（例如 Cassandra）是為跨多節點的龐大寫入量而設計。圖形資料庫（例如 Neo4j）讓關聯的走訪變成便宜的操作。它們的共通點是結構描述彈性或不存在，而且設計上假設的是向外擴充而非向上擴充；而它們換到這種擴充性的方式，就是捨棄跨機器協調成本最高的兩件事：join，以及橫跨多筆紀錄的交易。

The choice comes from the workload, not from preference. If the data is relational, the access patterns are varied or not yet known, and correctness across multiple rows matters - orders, payments, inventory - a relational database is the right default. If you have one dominant, well-understood access pattern, a very high write rate, or records that are always read whole, a document or wide-column store fits better. The trade-off to name out loud is consistency. Once copies of the data live on several nodes, a network partition - the machines are all up but cannot reach each other - forces a choice between refusing the request and answering from a replica that may be stale, which is what the CAP theorem describes; eventual consistency is what that feels like in practice, when you write, read back from a different replica, and briefly do not see your own write. So the question to ask is what queries this will serve and what has to be true immediately after a write, and then pick from that. Boiled down: if the data has to add up across tables, use SQL; if it's already shaped like one self-contained blob and you mainly need raw write speed, NoSQL earns its keep.

選擇來自工作負載，而不是偏好。如果資料本身是關聯性的、存取模式多樣或還不確定，而且跨多列的正確性很重要 —— 訂單、金流、庫存 —— 那麼關聯式資料庫是正確的預設。如果你有一個主導性且清楚的存取模式、非常高的寫入速率，或紀錄總是被整筆讀取，那麼文件或寬欄位資料庫更合適。應該當場講出來的取捨是一致性。一旦資料的副本分散在多個節點上，網路分區（機器都活著，但彼此連不上）就會逼你在「拒絕這個請求」和「用一份可能過期的副本回答」之間二選一，這就是 CAP 定理在講的事；而最終一致性就是它在實務上的樣子——你寫入之後從另一個副本讀取，會有一小段時間看不到自己剛剛寫的東西。所以要問的問題是：這份資料要服務哪些查詢、寫入之後有什麼必須「立刻」成立；然後據此決定。濃縮成一句：資料需要跨表對得起來，就用 SQL；資料本來就長成一個自成一體的東西、而你要的是寫入速度，NoSQL 才划算。

It is worth admitting that the line has blurred. PostgreSQL stores and indexes JSON well enough to cover many document use cases, and MongoDB has supported multi-document transactions for years. So the honest framing is that this is a spectrum of trade-offs between schema rigidity, transactional guarantees, and horizontal scale, and that a relational database is the safer default until a specific requirement pushes you off it.

值得坦白承認的是，界線已經模糊了。PostgreSQL 對 JSON 的儲存與索引好到足以涵蓋許多文件型的使用情境，而 MongoDB 支援跨文件交易也已經好幾年。所以比較誠實的說法是：這是一條在結構描述嚴謹度、交易保證與水平擴充之間取捨的光譜，而在有具體需求把你推開之前，關聯式資料庫是比較安全的預設。

## Quick Reference

### The five families, side by side

| Family | Example | What one record is | Best at | Falls down when |
|---|---|---|---|---|
| **Relational** | PostgreSQL, MySQL | A row in a table with a fixed schema, joined to others by key | Varied or unforeseen queries; correctness across several rows | You need linear write scale across many nodes |
| **Document** | MongoDB | One nested, self-contained object | Records that are always read whole; a schema still moving | The same data must be queried several unrelated ways |
| **Key-value** | Redis | A value reached only through its key | Sub-millisecond lookup: sessions, counters, leaderboards | You need to query by anything other than the key |
| **Wide-column** | Cassandra | A row grouped under a partition key, columns varying per row | Enormous write volume spread across many nodes | The access pattern was not designed into the key up front |
| **Graph** | Neo4j | A node, plus the edges connecting it to others | Traversing relationships many hops deep | The work is bulk aggregation rather than traversal |

The rows are ordered the way the answer is spoken, with relational first because it is the default you have to be pushed off, not one option among five.

## Interview Version

> SQL databases store data in tables with a predefined schema and explicit relationships, and they follow ACID - which is what lets you move money between two accounts and be certain that either both rows changed or neither did. They also give you a declarative query language with joins, so a question you did not anticipate at design time is still answerable without changing how the data is stored. NoSQL is not one thing; it is at least four families. Document stores such as MongoDB keep nested records and suit data read as one object. Key-value stores such as Redis reach every value through its key. Wide-column stores such as Cassandra are built for enormous write volume across many nodes. Graph databases make relationship traversal the cheap operation. What they share is a flexible or absent schema and a design that assumes scaling out rather than up - and the way they buy that scale is by giving up the two things that are expensive to coordinate across machines: joins, and transactions spanning several records. So the choice comes from the workload. If the data is relational, the access patterns are varied or not yet known, and correctness across rows matters - orders, payments, inventory - relational is the right default. If there is one dominant access pattern, a very high write rate, or records always read whole, a document or wide-column store fits. The trade-off to name out loud is consistency: once copies live on several nodes, a partition forces a choice between refusing the request and answering from a possibly stale replica. And the line has blurred - PostgreSQL indexes JSON well, MongoDB has had multi-document transactions for years - so the honest framing is a spectrum, with relational as the safer default until a requirement pushes you off it.

面試時可回答：SQL 資料庫把資料存在有預先定義 schema、彼此有明確關聯的表格裡，並且遵循 ACID —— 這正是為什麼你可以在兩個帳戶之間轉錢，並確定「兩列都改了，或兩列都沒改」。它們也給你一套帶 join 的宣告式查詢語言，所以一個你在設計時沒預料到的問題，不必改變資料的儲存方式就還是答得出來。NoSQL 不是單一一種東西，它至少是四個家族。像 MongoDB 這樣的 document store 保存巢狀紀錄，適合會被當成一個物件整份讀取的資料。像 Redis 這樣的 key-value store 透過鍵直接取值。像 Cassandra 這樣的 wide-column store 是為了跨多節點的龐大寫入量而生。graph database 則讓關聯走訪變成便宜的操作。它們的共通點是 schema 有彈性或根本沒有，以及「假設向外擴展而不是向上擴展」的設計 —— 而它們買到這種擴展性的方式，是放棄兩件跨機器協調起來很貴的事：join，以及跨越多筆紀錄的交易。所以選擇來自工作負載。如果資料本身是關聯性的、存取模式多樣或還不確定、而且跨列的正確性很重要 —— 訂單、付款、庫存 —— 關聯式資料庫就是正確的預設。如果有一個主導性的存取模式、非常高的寫入速率，或紀錄總是被整份讀取，document 或 wide-column store 更合適。要講出口的取捨是一致性：一旦資料的副本住在好幾個節點上，網路分區就會逼你在「拒絕這個請求」和「用一個可能過期的副本回答」之間二選一。而且界線已經模糊了 —— PostgreSQL 能好好索引 JSON、MongoDB 支援多文件交易也已經好幾年 —— 所以誠實的說法是：這是一道光譜，而關聯式是比較安全的預設，直到某個具體需求把你推離它。

The sentence to remember is: **If the data has to add up across tables, use SQL; if it is already one self-contained blob and you need write speed, NoSQL earns its keep.**

最值得記：**如果資料必須跨表兜得起來，用 SQL；如果它本來就是一團自成一體的東西、而你要的是寫入速度，NoSQL 才划算。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q02: Can you describe a typical HTTP request/response cycle?](../api-and-http/q02-http-request-response-cycle.md) | [All 40 questions](../../README.md) | [Q16: What is a database index, and how do you work out why a query is slow?](q16-indexes-and-slow-queries.md) |
