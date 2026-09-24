# Q71: How do you make backend code testable?

> Tests whether you can name what actually makes a unit untestable - a dependency built inside it - rather than reaching straight for a mocking library.

**Part:** Code Design | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [redis](../_glossary.md#redis), [unit test](../_glossary.md#unit-test), [message queue](../_glossary.md#message-queue)

## In One Sentence

Keep business logic separate from the database, Redis, and third-party APIs, and pass those in from outside, so a test can swap them for fakes instead of connecting to the real thing.

把 business logic 跟 DB、Redis、外部 API 分開，並且把這些依賴從外面傳進來，測試時就能換成假的，不用真的連線。

## Answer Shape

Say what the question is really asking first: how do you write code so a unit test does not need a real DB, Redis, or third-party API. Then show the version everyone has written - everything stuffed into the API handler - because the problem has to be visible before the fix means anything. Draw the layers, then introduce injection as the one line that makes the layers swappable. Have mock versus fake ready, because that is the follow-up.

先說這題真正在問什麼：你怎麼寫程式，才能讓 unit test 不必真的連 DB、Redis 或外部 API。然後把大家都寫過的那個版本拿出來 —— 什麼都塞在 API handler 裡 —— 因為問題要先看得見，修法才有意義。畫出分層，接著把注入當成「讓這些層可以抽換」的那一行帶進來。最後把 mock 和 fake 的差別準備好，因為那就是追問。

## Full Spoken Answer

The question is really asking one thing: how do you write code so that a unit test does not need a real database, a real Redis, and a real third-party API. Two ideas cover it, and they come in this order. Separation of concerns puts the business logic somewhere by itself. Dependency injection is what then lets you swap what it talks to. The second one only helps if you did the first.

這題真正在問的只有一件事：你怎麼寫程式，才能讓 unit test 不需要真的資料庫、真的 Redis、真的第三方 API。兩個概念就涵蓋了，而且順序是這樣。Separation of concerns 先把 business logic 放到它自己的地方。Dependency injection 接著讓你可以抽換它對話的對象。第二個只有在你做了第一個之後才有用。

Start with the version everyone has written, because it makes the problem visible. A `POST /users` handler that does all of it: read the JSON, validate the input, run the business rules, write the SQL, call an external API, send a welcome email. Now you want to test one rule - a blank name must be rejected. That rule is four lines of pure logic, but to reach it you have to start a database, a mail server, and whatever that external API is. The rule is not hard to test. It is just glued to five things that are.

從大家都寫過的那個版本開始，因為它讓問題看得見。一個 `POST /users` 的 handler 把所有事都做完：讀 JSON、驗證輸入、跑商業規則、寫 SQL、呼叫外部 API、寄歡迎信。現在你想測一條規則 —— 名字空白要被擋下來。這條規則是四行純邏輯，但要碰到它，你得先起一個資料庫、一個 mail server，還有那個外部 API。這條規則本身不難測，它只是被黏在五個難測的東西上。

So split it into layers, and the split is the answer. The controller only reads the request and returns the response. The service holds the business logic and writes no SQL. The repository holds the queries and holds no business rules. Each layer talks only to the one below it. Once that is done, the business logic is a plain class you can hold in your hand - it has no idea an HTTP request exists and no idea which database is underneath.

所以把它切成層，而這個切法就是答案。Controller 只負責讀 request、回 response。Service 放 business logic，不寫 SQL。Repository 放查詢，不放商業規則。每一層只跟它下面那一層說話。做完之後，business logic 就變成一個你可以單獨拿在手上的 class —— 它不知道有 HTTP request 這種東西，也不知道下面是哪個資料庫。

Then injection, which is smaller than the name suggests. The service must not build its own repository inside itself. It takes it as a constructor argument: `def __init__(self, repository)`. Production passes a `PostgresUserRepository`. The test passes a `FakeUserRepository` that keeps rows in a dict. Same service class, different collaborator, and the test runs in milliseconds with nothing leaving the process. Worth saying plainly in an interview: dependency injection is a constructor argument, not a framework. People assume there is a library to install, and in Python there is not.

接著是注入，它比名字聽起來小得多。Service 不可以在自己裡面把 repository new 出來，而是用建構子參數接進來：`def __init__(self, repository)`。正式環境傳一個 `PostgresUserRepository`，測試傳一個把資料放在 dict 裡的 `FakeUserRepository`。同一個 service class、不同的協作者，測試在幾毫秒內跑完，而且沒有任何東西離開這個 process。面試時值得直說：dependency injection 就是一個建構子參數，不是一個框架。大家以為要裝什麼套件，在 Python 不用。

The follow-up to have ready is the difference between a mock and a fake, because interviewers ask it right after this. A fake is a real but simple implementation - a repository backed by a dict instead of PostgreSQL. It works, so you assert on the outcome. A mock records calls, so you assert that something was called, with which arguments, how many times. The rule is short: use a fake when you care about the result, a mock when the call itself is the behaviour, like "we sent exactly one email". I default to fakes, because a fake reads like ordinary code and breaks loudly when the interface changes, while a mock keeps passing against a method that no longer exists.

要準備好的追問是 mock 和 fake 的差別，因為面試官通常緊接著就問。Fake 是一個真的能動、但很簡單的實作 —— 例如一個用 dict 而不是 PostgreSQL 撐起來的 repository。它會動，所以你驗證的是結果。Mock 則是記錄呼叫，所以你驗證的是「有沒有被呼叫、用什麼參數、呼叫幾次」。規則很短：**在意結果就用 fake，呼叫本身就是行為時才用 mock**，例如「我們只寄了一封信」。我預設用 fake，因為 fake 讀起來就像一般程式碼，而且介面一改它會大聲壞掉；mock 則是就算那個方法已經不存在了，測試照樣會過。

## Quick Reference

**The problem, in the version everyone has written:**

```python
# ❌ 全部塞在 handler：要測「名字空白要擋下來」，得先起 DB 和 mail server
@app.post("/users")
def create_user():
    data = request.json
    if not data.get("name"):          # validation
        return {"error": "..."}, 400
    row = db.execute("INSERT INTO users ...")   # SQL
    billing_api.create_customer(row.id)         # external API
    send_welcome_email(data["email"])           # email
    return {"id": row.id}, 201
```

**The layers:**

```
    Controller / API     ← 只讀 request、回 response
          ↓
       Service           ← Business Logic（不寫 SQL）
          ↓
      Repository         ← Database（不放商業規則）
          ↓
       Database
```

```python
class UserService:
    def __init__(self, repository):      # ← 從外面傳進來
        self.repository = repository

    def create_user(self, name):
        if not name:
            raise ValueError("name is required")
        return self.repository.create(name)
```

**Same service, different collaborator:**

```
Production   UserService ──→ PostgresUserRepository ──→ PostgreSQL
Test         UserService ──→ FakeUserRepository      （dict，幾毫秒，不出 process）
```

```python
def test_blank_name_is_rejected():
    service = UserService(FakeUserRepository())
    with pytest.raises(ValueError):
        service.create_user("")
```

**The whole of dependency injection:**

```python
# ❌ 自己在裡面決定依賴，外面換不掉
class UserService:
    def create_user(self):
        db = PostgreSQL(...)

# ✅ 從外面傳進來
class UserService:
    def __init__(self, db):
        self.db = db
```

**Mock or fake - the likely follow-up:**

| | Fake | Mock |
|---|---|---|
| **What it is** | A real but simple implementation - a dict instead of PostgreSQL | A recorder of calls |
| **What you assert** | The outcome: the user came back with that name | The interaction: it was called once, with these arguments |
| **Reach for it when** | You care what the code produced | The call *is* the behaviour - "exactly one email was sent" |
| **When the interface changes** | It breaks loudly - it has to implement the new method | It keeps passing against a method that no longer exists |
| **Default** | ✅ This one | Only when you need to prove a call happened |

**What to inject, and what not to:**

| Inject it | Why |
|---|---|
| Repository / database, Redis, HTTP clients, the queue | Leaves the process - slow, stateful, can fail in ways you must test |
| The clock, the random or UUID generator | Otherwise "expires in 30 minutes" means waiting 30 minutes |
| **Just build it** | **Why** |
| Pure functions, value objects, dataclasses | Same input, same output - there is nothing to swap |
| `dict`, `list`, small private helpers | Injecting them only makes the constructor unreadable |

## Interview Version

> The question is how you write code so a unit test does not need a real database, Redis, or third-party API, and it comes down to separation of concerns first, then dependency injection. The version everyone writes puts validation, business rules, SQL, an external API call, and an email into one handler - so testing the single rule that a blank name is rejected means starting a database and a mail server. I split it into layers: the controller reads the request and returns the response, the service holds business logic and writes no SQL, the repository holds the queries and no business rules. Then the service takes the repository as a constructor argument instead of building it, so production passes a `PostgresUserRepository` and a test passes a `FakeUserRepository` backed by a dict. Dependency injection is a constructor argument, not a framework. I also avoid hidden global state, since a module-level singleton puts back the coupling I just removed. If they follow up on mock versus fake: a fake is a real but simple implementation so you assert on the outcome, a mock records calls so you assert the interaction, and I default to fakes.

面試時可回答：這題問的是你怎麼寫程式，才能讓 unit test 不必真的連 DB、Redis 或第三方 API，關鍵是先做 separation of concerns，再做 dependency injection。大家都寫過的那個版本，把驗證、商業規則、SQL、外部 API 呼叫和寄信全塞在一個 handler 裡 —— 所以光要測「名字空白要擋下來」這一條，就得先起一個資料庫和一個 mail server。我會把它切成層：controller 讀 request、回 response；service 放 business logic，不寫 SQL；repository 放查詢，不放商業規則。然後 service 用建構子參數接 repository，而不是自己 new，所以正式環境傳 `PostgresUserRepository`，測試傳一個用 dict 撐起來的 `FakeUserRepository`。dependency injection 是一個建構子參數，不是一個框架。我也會避免隱藏的全域狀態，因為一個 module 層級的 singleton 會把我剛拆掉的耦合裝回去。如果追問 mock 和 fake 的差別：fake 是真的能動但很簡單的實作，所以你驗證的是結果；mock 記錄呼叫，所以你驗證的是互動 —— 我預設用 fake。

The sentence to remember is: **Separate business logic from external dependencies, inject the dependencies, and swap them for a fake in tests.**

最值得記：**Business logic 跟外部 dependency 分開，dependency 用 injection，測試時換成 mock/fake。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q61: How do you choose HTTP status codes and design error responses?](../api-design/q61-status-codes-and-error-responses.md) | [All 48 questions](../../README.md) | [Q09: How would you handle file uploads in a web application?](../api-and-http/q09-file-uploads.md) |
