# Q11: Can you explain the difference between SQL and NoSQL databases?

> Tests whether you can choose between them for a stated workload, rather than reciting 'SQL is structured, NoSQL is flexible'.

**Part:** Databases | **Importance:** 10/10 | **Status:** Draft

**New to these terms?** [acid](../_glossary.md#acid), [index](../_glossary.md#index), [redis](../_glossary.md#redis), [horizontal scaling](../_glossary.md#horizontal-scaling), [query plan](../_glossary.md#query-plan)

## In One Sentence

A SQL database stores data in tables with a fixed schema and guarantees transactions across them, while NoSQL is an umbrella for stores that relax the schema or the guarantees in exchange for flexibility and easier horizontal scale.

SQL 資料庫把資料存在具有固定結構描述的資料表裡，並保證跨表的交易；NoSQL 則是一個統稱，泛指那些放寬結構描述或交易保證，以換取彈性與更容易水平擴充的儲存系統。

## Answer Shape

Describe each family by what it guarantees rather than by how it looks, because the schema difference is the surface and the guarantees are the substance. Say that NoSQL is four different families, not one thing. Then answer the question the interviewer really wants: how you would choose for a stated workload, and finish by admitting the line has blurred.

用「它保證什麼」而不是「它長什麼樣」來描述兩邊，因為結構描述的差異只是表面，保證才是實質。要說清楚 NoSQL 是四個不同家族，不是單一種東西。接著回答面試官真正想聽的：面對一個具體工作負載你會怎麼選；最後坦白說明兩者的界線已經模糊。

## Full Spoken Answer

SQL databases, also called relational databases, store data in tables with a predefined schema and explicit relationships between them. They follow ACID - atomicity, consistency, isolation, and durability - which is what lets you move money between two accounts and be certain that either both rows changed or neither did. They also give you a declarative query language with joins, so a question you did not anticipate at design time is still answerable without changing how the data is stored.

SQL 資料庫又稱關聯式資料庫，把資料存在具有預先定義結構描述的資料表中，表與表之間有明確的關聯。它們遵守 ACID —— 不可分割性、一致性、隔離性、持久性 —— 這正是讓你能在兩個帳戶之間轉帳，並且確定「兩列都改了」或「兩列都沒改」的原因。它們同時提供帶 join 的宣告式查詢語言，所以即使是設計當下沒預料到的問題，也不必改變資料的儲存方式就能查得出來。

NoSQL is not one thing; it is at least four families with different shapes. Document stores such as MongoDB keep nested records and suit data that is naturally read as one object. Key-value stores such as Redis give you the fastest possible lookup by key and nothing else. Wide-column stores such as Cassandra are built for enormous write volume across many nodes. Graph databases such as Neo4j make relationship traversal the cheap operation. What they share is a flexible or absent schema and a design that assumes scaling out rather than up.

NoSQL 並不是單一種東西，它至少是四個形狀不同的家族。文件資料庫（例如 MongoDB）保存巢狀的紀錄，適合天生就會被當成一個物件讀取的資料。鍵值資料庫（例如 Redis）提供以鍵取值的最快查找，除此之外什麼都不提供。寬欄位資料庫（例如 Cassandra）是為跨多節點的龐大寫入量而設計。圖形資料庫（例如 Neo4j）讓關聯的走訪變成便宜的操作。它們的共通點是結構描述彈性或不存在，而且設計上假設的是向外擴充而非向上擴充。

The choice comes from the workload, not from preference. If the data is relational, the access patterns are varied or not yet known, and correctness across multiple rows matters - orders, payments, inventory - a relational database is the right default. If you have one dominant, well-understood access pattern, a very high write rate, or records that are always read whole, a document or wide-column store fits better. The question to ask out loud is what queries this will serve and what has to be true after a write, and then pick from that.

選擇來自工作負載，而不是偏好。如果資料本身是關聯性的、存取模式多樣或還不確定，而且跨多列的正確性很重要 —— 訂單、金流、庫存 —— 那麼關聯式資料庫是正確的預設。如果你有一個主導性且清楚的存取模式、非常高的寫入速率，或紀錄總是被整筆讀取，那麼文件或寬欄位資料庫更合適。要當場問出口的問題是：這份資料要服務哪些查詢、寫入之後有什麼必須成立；然後據此決定。

It is worth admitting that the line has blurred. PostgreSQL stores and indexes JSON well enough to cover many document use cases, and MongoDB has supported multi-document transactions for years. So the honest framing is that this is a spectrum of trade-offs between schema rigidity, transactional guarantees, and horizontal scale, and that a relational database is the safer default until a specific requirement pushes you off it.

值得坦白承認的是，界線已經模糊了。PostgreSQL 對 JSON 的儲存與索引好到足以涵蓋許多文件型的使用情境，而 MongoDB 支援跨文件交易也已經好幾年。所以比較誠實的說法是：這是一條在結構描述嚴謹度、交易保證與水平擴充之間取捨的光譜，而在有具體需求把你推開之前，關聯式資料庫是比較安全的預設。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q02: Can you describe a typical HTTP request/response cycle?](../api-and-http/q02-http-request-response-cycle.md) | [All 41 questions](../../README.md) | [Q16: What is a database index, and how do you work out why a query is slow?](q16-indexes-and-slow-queries.md) |
