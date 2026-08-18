# Q51: What kind of tests would you write for a new API endpoint?

> Tests whether you can say what each layer is responsible for, instead of listing test types.

**Part:** Testing & Debugging | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [endpoint](../_glossary.md#endpoint), [idempotent](../_glossary.md#idempotent), [breaking change](../_glossary.md#breaking-change), [idempotency key](../_glossary.md#idempotency-key)

## In One Sentence

You write unit tests for the logic, integration tests that call the real endpoint over HTTP, and, where it matters, a load test - each layer proving something the others cannot.

你會為邏輯寫單元測試、寫透過 HTTP 呼叫真實 endpoint 的整合測試，並在有必要時做負載測試 —— 每一層各自證明其他層證明不了的事。

## Answer Shape

Name the three layers and, for each, say what it proves and what it deliberately does not cover, because the question is testing whether you understand responsibility rather than whether you can list test types. Then add the cases you would actually write for one endpoint, since the happy path is the easy half and the interviewer is listening for the other one.

把三個層次點名，並針對每一層說出它證明了什麼、又刻意不涵蓋什麼，因為這題考的是你懂不懂職責劃分，而不是你會不會列出測試種類。接著補上你實際會為某個 endpoint 寫的案例，因為順利路徑只是簡單的那一半，面試官在聽的是另一半。

## Full Spoken Answer

Unit tests come first and target the business logic behind the endpoint. I test the relevant functions through their public interfaces and avoid reaching into private methods, and I keep out anything that touches a database, the filesystem, or another service. That makes them fast enough to run on every save and precise about where a failure is - when a unit test fails, the location is the answer. What they cannot tell you is whether any of it is wired up correctly.

單元測試放在最前面，針對的是 endpoint 背後的商業邏輯。我透過公開介面測試相關的函式，避免去戳私有方法，並且排除任何會碰到資料庫、檔案系統或其他服務的東西。這讓它們快到可以每次存檔就跑一遍，而且對失敗位置很精確 —— 單元測試失敗時，位置本身就是答案。它們無法告訴你的是：這一切到底有沒有正確接起來。

Integration tests answer that. They exercise the endpoint through the actual HTTP interface, with real routing, real serialization, real middleware, and a real database, usually one started for the test run. This is the layer that catches the things unit tests mocked away: a wrong route, middleware ordering, a serializer that drops a field, a migration that was never applied. They are slower, so there are fewer of them, and they are the tests I would keep if I could only keep one set.

整合測試回答的正是這個問題。它們透過真實的 HTTP 介面操作這個 endpoint，走真實的路由、真實的序列化、真實的中介層，以及真實的資料庫 —— 通常是為這次測試而啟動的。這一層抓的正是被單元測試 mock 掉的那些東西：路由寫錯、中介層順序不對、序列化器漏掉一個欄位、某個遷移從沒被套用。它們比較慢，所以數量比較少；如果只能留一套測試，我會留這一套。

The cases matter more than the count. For one endpoint I would cover the happy path, then validation failures with a bad payload, authentication missing or expired, authorization where a valid user requests someone else's record, a not-found identifier, and the boundary conditions - empty list, maximum page size, duplicate submission. The last one is worth calling out: for a POST that creates something, testing what a retry does tells you whether the endpoint needs an idempotency key, and that is a design question the test surfaces.

測試案例比數量更重要。對一個 endpoint，我會涵蓋順利路徑，然後是 payload 錯誤導致的驗證失敗、缺少或過期的認證、有效使用者去請求別人資料的授權情境、找不到的識別碼，以及邊界條件 —— 空清單、最大分頁筆數、重複送出。最後一項特別值得提出來：對一個會建立資料的 POST，測試「重試會發生什麼」能告訴你這個 endpoint 需不需要 idempotency key，而那是一個由測試浮現出來的設計問題。

Beyond those two layers, I add others when the endpoint justifies it. A load test tells you how it behaves under sustained traffic and where it breaks, which is worth running before anything customer-facing goes live. A contract test is valuable when other teams consume the endpoint, because it catches a breaking change at build time rather than in their production. And when a bug is found, the first step is a failing test that reproduces it, so the fix is proven and the same regression cannot come back quietly.

在這兩層之外，當 endpoint 值得時我會再加上其他測試。負載測試告訴你它在持續流量下的行為，以及它會在哪裡崩潰，任何面向客戶的東西上線前都值得跑一次。當這個 endpoint 有其他團隊在使用時，契約測試很有價值，因為它能在建置階段就抓到破壞性變更，而不是在對方的正式環境才發現。而當發現一個 bug 時，第一步是寫一個能重現它的失敗測試，這樣修復才是被證明過的，同樣的退步也不會再悄悄回來。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q27: What is CORS?](../security-and-auth/q27-cors.md) | [All 37 questions](../../README.md) | [Q61: How do you choose HTTP status codes and design error responses?](../api-design/q61-status-codes-and-error-responses.md) |
