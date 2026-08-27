# Q23: How do you protect a server from SQL injection attacks?

> Tests whether you know that the fix is separating code from data, not filtering bad characters.

**Part:** Security & Auth | **Importance:** 9/10 | **Status:** Complete

**New to these terms?** [cursor pagination](../_glossary.md#cursor-pagination)

## In One Sentence

SQL injection happens when user input becomes part of the SQL command instead of staying data, and the fix is to send the query and the values to the database separately rather than to filter the input.

SQL injection 發生在使用者輸入變成了 SQL 命令的一部分、而不再只是資料；正確的修法是把查詢和值分開送給資料庫，而不是去過濾輸入。

## Answer Shape

Define the vulnerability by mechanism - input changing the structure of the query, not just its values - because that framing makes the correct fix obvious. Lead with parameterized queries and say why they work, mention ORMs as the same thing by default, then explicitly rank manual escaping last and explain why. Finish with the defense-in-depth layers that limit the damage of the injection you missed.

用機制來定義這個漏洞 —— 輸入改變的是查詢的「結構」而不只是「值」—— 因為這個定位會讓正確的修法變得顯而易見。先講參數化查詢並說明它為什麼有效，接著提到 ORM 預設就是同一件事，然後明確把手動跳脫排在最後並解釋原因。最後補上縱深防禦，用來限制你漏掉的那次注入能造成多大傷害。

## Full Spoken Answer

SQL injection happens when an attacker can manipulate a query by injecting input that the database parses as part of the command. The precise point is that the input changes the structure of the statement, not only the values in it, which is how an attacker bypasses a login check or reads a table they should never see. Everything that follows comes from taking that structure out of the attacker's reach.

SQL injection 發生在攻擊者能透過注入輸入來操縱查詢，而資料庫會把那段輸入解析成命令的一部分。精確的重點是：輸入改變的是敘述句的「結構」，而不只是其中的「值」，這正是攻擊者繞過登入檢查、或讀取本不該看到的資料表的方式。後面所有的做法，都是為了把那個結構移出攻擊者能碰到的範圍。

The primary defense is prepared statements, also called parameterized queries. You write the SQL with placeholders and pass the user input separately as values. The database parses and plans the statement before it ever sees the data, so the input is bound as a value and can never become part of the command - no matter what characters it contains. This is not sanitization; it is a structural separation, which is why it works for every data type without you having to reason about escaping at all.

首要防線是 prepared statement，也叫參數化查詢。你把 SQL 寫成帶佔位符的形式，再把使用者輸入當成值另外傳入。資料庫在看到資料之前就已經解析並規劃好敘述句，因此輸入是以「值」的身分被綁定，永遠不可能變成命令的一部分 —— 不管它含有什麼字元。這不是消毒，而是結構上的分離，這也是為什麼它對所有資料型別都有效，而你完全不需要去推敲跳脫規則。

Using an ORM such as SQLAlchemy or the Django ORM gives you the same protection, because it builds parameterized queries under the hood while you work with objects and methods. That removes a whole class of human error. The caveat worth stating is that every ORM has an escape hatch for raw SQL, and string-formatting user input into that escape hatch is injectable exactly like anything else. Manual escaping of quotes and semicolons is the last resort and should be named as such: it is easy to get wrong, it varies by database and character set, and a single missed path reopens the hole.

使用像 SQLAlchemy 或 Django ORM 這樣的 ORM 能得到同樣的保護，因為當你在操作物件與方法時，它在底層建立的就是參數化查詢，這消除了一整類的人為錯誤。值得說明的但書是：每個 ORM 都有一個寫原生 SQL 的逃生口，而把使用者輸入用字串格式化塞進那個逃生口，跟其他任何地方一樣可被注入。手動跳脫引號和分號是最後手段，而且應該明說它是最後手段：容易做錯、隨資料庫與字元集而異，只要漏掉一條路徑，洞就重新打開了。

Then assume one will slip through anyway and limit what it can do. Give the application's database user the least privilege it needs, so an account that cannot drop tables or read other schemas caps the blast radius. Validate input for format, length, and allowed values at the boundary, which is useful defense but never a substitute for parameterization. Use stored procedures only if they are themselves parameterized inside. And test for it deliberately, with tools such as sqlmap or OWASP ZAP in the pipeline, so a regression is caught by the build rather than by an attacker.

接著假設仍然會有一次漏網，並限制它能做的事。給應用程式的資料庫帳號最小必要權限，一個不能 drop 資料表、不能讀其他 schema 的帳號能把爆炸半徑壓住。在邊界驗證輸入的格式、長度與允許值，這是有用的防禦，但永遠不能取代參數化。只有在 stored procedure 內部本身也是參數化的情況下才使用它。並且刻意去測試，在流程中加入 sqlmap 或 OWASP ZAP 這類工具，讓退步是被建置流程抓到，而不是被攻擊者抓到。

## Quick Reference

### The fix, in two forms

A prepared statement - the query and the values travel separately:

```python
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password = %s",
    (username, password),
)
```

An ORM - the same protection, obtained without writing SQL:

```python
user = User.objects.get(username=username, password=password)
```

## Interview Version

> SQL injection happens when an attacker can manipulate a query by injecting input that the database parses as part of the command. The precise point is that the input changes the structure of the statement, not only the values in it, which is how an attacker bypasses a login check or reads a table they should never see. Everything that follows comes from taking that structure out of the attacker's reach. The primary defence is prepared statements, also called parameterised queries: you write the SQL with placeholders and pass the user input separately as values, so the database parses and plans the statement before it ever sees the data. The input is bound as a value and can never become part of the command, no matter what characters it contains. This is not sanitisation, it is a structural separation - which is why it works for every data type without you having to reason about escaping at all. An ORM gives you the same protection because it builds parameterised queries under the hood, removing a whole class of human error; the caveat worth stating is that every ORM has an escape hatch for raw SQL, and string-formatting user input into that escape hatch is injectable exactly like anything else. Manual escaping of quotes and semicolons is the last resort and should be named as such - it varies by database and character set, and a single missed path reopens the hole. Then assume one slips through anyway and limit what it can do: give the application's database user least privilege so it cannot drop tables or read other schemas, validate input at the boundary as defence in depth but never as a substitute, and test for it deliberately in the pipeline so a regression is caught by the build rather than by an attacker.

面試時可回答：SQL injection 發生在攻擊者能夠透過注入輸入來操縱查詢，而資料庫把那段輸入當成指令的一部分來解析。精確的重點是：輸入改變的是「語句的結構」，不只是裡面的值，這正是攻擊者繞過登入檢查、或讀到他不該看見的資料表的方式。後面的一切，都來自「把那個結構移出攻擊者能觸及的範圍」。主要防禦是預備語句，也叫參數化查詢：你用佔位符寫 SQL，再把使用者輸入當成值分開傳入，於是資料庫在看到資料之前就已經解析並規劃好了那道語句。輸入被綁定為一個值，不論它含有什麼字元，都永遠不可能變成指令的一部分。這不是消毒，而是結構上的分離 —— 這正是為什麼它對每一種資料型別都有效，而你完全不必去推敲跳脫規則。使用 ORM 能得到同樣的保護，因為它在底層建構的就是參數化查詢，這移除了一整類人為錯誤；值得講明的但書是：每個 ORM 都有一個通往原始 SQL 的逃生口，而把使用者輸入用字串格式化塞進那個逃生口，一樣可以被注入。手動跳脫引號和分號是最後手段，也應該這樣稱呼它 —— 它隨資料庫和字元集而異，漏掉任何一條路徑就重新打開了那個洞。然後，假設終究會有一個漏過去，並限制它能做的事：給應用程式的資料庫使用者最小權限，讓它無法刪表或讀取其他 schema；在邊界做輸入驗證當作縱深防禦，但絕不當成替代品；並且刻意為它做測試、放進 pipeline，讓回歸由建置抓到，而不是由攻擊者抓到。

The sentence to remember is: **Parameterisation is not sanitisation - it is structural separation: the query is parsed before the data is ever seen.**

最值得記：**參數化不是消毒，而是結構上的分離 —— 查詢在看到資料之前就已經被解析完了。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q18: What is the N+1 query problem, and how do you fix it?](../databases/q18-n-plus-one-queries.md) | [All 41 questions](../../README.md) | [Q31: How would you scale a backend application during a traffic surge?](../architecture-and-scaling/q31-scaling-during-traffic-surge.md) |
