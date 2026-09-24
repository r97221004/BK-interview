# Q03: What is an API endpoint?

> Usually an opener. Tests whether you can define the term precisely and connect it to how a server routes work.

**Part:** API & HTTP | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [resource](../_glossary.md#resource)

## In One Sentence

An API endpoint is one URL the server exposes, together with the HTTP methods it accepts, and it is the entry point through which a client reaches one particular resource or capability.

API endpoint 是伺服器對外開放的一個 URL，加上它接受的 HTTP 方法；它是客戶端用來存取某一個特定資源或功能的入口。

## Answer Shape

Give the definition in one line, then make it concrete by showing what the server does with it: a router maps the method and path to a handler function. Add a real example URL, and close by distinguishing an endpoint from the API as a whole, because that distinction is the actual point of the question.

先用一句話給出定義，接著用伺服器實際做的事把它具體化：router 會把方法加路徑對應到一個處理函式。補上一個真實的 URL 例子，最後區分「一個 endpoint」和「整個 API」，因為這個區分才是這題真正要問的。

## Full Spoken Answer

An endpoint is a specific URL where an API receives requests and returns responses. It represents an entry point to one function or resource on the server, and it is defined by the path together with the methods it accepts, so the same path answering GET and POST is really two operations behind one address.

endpoint 是 API 接收請求並回傳回應的一個特定 URL。它代表伺服器上某一個功能或資源的入口，並且由「路徑」加上「它接受的方法」共同定義，所以同一個路徑同時接受 GET 和 POST，實際上是同一個位址背後的兩個操作。

Inside the server, the framework's router is what makes an endpoint real: it matches the incoming method and path against a table and calls the handler registered for that pair. Path segments can be variable, so `GET /users/{id}` is one endpoint that serves every user - request `/users/42`, and 42 is pulled out and handed to the handler as an argument.

在伺服器內部，讓 endpoint 真正存在的是框架的 router：它把進來的方法與路徑比對一張路由表，再呼叫註冊在那組配對上的處理函式。路徑片段可以是變數，所以 `GET /users/{id}` 是一個服務所有使用者的 endpoint —— 請求 `/users/42`，42 就會被取出來當成參數傳給處理函式。

Plainly: one endpoint is one door, the API is the whole building. The API is the full contract - every endpoint, the shape of every payload, the error format, the auth scheme, and the guarantees around all of it. `GET /users/{id}` is a single door in that building, which is why a well-designed endpoint opens onto one clear capability instead of becoming a single door that branches into ten different rooms depending on a field in the request body.

說白了：一個 endpoint 是一扇門，API 是整棟建築。API 是整份契約 —— 所有 endpoint、每個 payload 的格式、錯誤格式、認證機制，以及圍繞它們的所有保證。`GET /users/{id}` 只是這棟建築裡的一扇門，這也是為什麼設計良好的 endpoint 會通往一個清楚的功能，而不是變成一扇門、裡面卻依 body 裡某個欄位分岔成十個不同房間。

## Interview Version

> An endpoint is a specific URL where an API receives requests and returns responses. It is an entry point to one function or resource on the server, and it is defined by the path together with the methods it accepts - so the same path answering GET and POST is really two operations behind one address. Inside the server, the framework's router is what makes an endpoint real: it matches the incoming method and path against a table and calls the handler registered for that pair. Path segments can be variable, so GET /users/{id} is one endpoint that serves every user - request /users/42 and 42 is pulled out and handed to the handler as an argument. The distinction I would draw is between an endpoint and the API: one endpoint is one door, and the API is the whole building. The API is the full contract - every endpoint, the shape of every payload, the error format, the auth scheme, and the guarantees around all of it. That is also the design test: a well-designed endpoint opens onto one clear capability, rather than becoming a single door that branches into ten different rooms depending on a field in the request body.

面試時可回答：endpoint 是一個具體的 URL，API 在那裡接收請求並回傳回應。它是通往伺服器上某一個功能或 resource 的入口，由「路徑」加上「它接受的方法」共同定義 —— 所以同一個路徑同時回應 GET 和 POST，其實是同一個位址背後的兩個操作。在伺服器內部，是框架的 router 讓 endpoint 成真：它拿進來的方法與路徑去比對一張表，然後呼叫為那一組所註冊的 handler。路徑片段可以是變數，所以 GET /users/{id} 是一個服務所有使用者的 endpoint —— 請求 /users/42，42 就會被取出來當成參數交給 handler。我會做的區分是 endpoint 和 API 的差別：一個 endpoint 是一扇門，而 API 是整棟建築。API 是完整的合約 —— 每一個 endpoint、每一份 payload 的形狀、錯誤格式、認證機制，以及圍繞這一切的保證。這也正是設計上的檢驗標準：一個設計良好的 endpoint 通往一個清楚的能力，而不是變成一扇會依 request body 裡某個欄位分岔到十個不同房間的門。

The sentence to remember is: **One endpoint is one door; the API is the whole building - and a good door opens onto exactly one room.**

最值得記：**一個 endpoint 是一扇門，API 是整棟建築 —— 而一扇好的門，只通往一個房間。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q32: Discuss multiprocessing, multithreading, and asynchronous I/O in Python.](../architecture-and-scaling/q32-python-concurrency-models.md) | [All 48 questions](../../README.md) | [Q05: What are the benefits and drawbacks of RESTful APIs?](q05-rest-benefits-and-drawbacks.md) |
