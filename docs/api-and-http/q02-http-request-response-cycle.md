# Q02: Can you describe a typical HTTP request/response cycle?

> Tests whether you can follow a request end to end, including the TCP connection underneath and what persistent connections changed.

**Part:** API & HTTP | **Importance:** 10/10 | **Status:** Complete

**New to these terms?** [status code](../_glossary.md#status-code), [tcp](../_glossary.md#tcp), [head-of-line blocking](../_glossary.md#head-of-line-blocking), [tls](../_glossary.md#tls), [connection pool](../_glossary.md#connection-pool)

## In One Sentence

The client opens a connection to the server, sends a request made of a method, a path, headers, and an optional body, the server does the work and sends back a status code with its own headers and body, and the connection is then reused or closed.

客戶端先與伺服器建立連線，送出一個由方法、路徑、標頭和選擇性 body 組成的請求；伺服器處理完後回傳一個狀態碼，加上自己的標頭與 body；連線接著被重複使用或關閉。

## Answer Shape

Walk the cycle in order and do not skip the transport: connection, request, processing, response, connection reuse. Name the parts of the request and the response as you go, because that is what the interviewer is checking you can list. Finish with persistent connections, since that is the part most candidates omit and it is the one with real performance consequences.

照順序把整個循環走一遍，而且不要跳過傳輸層：建立連線、送出請求、伺服器處理、回傳回應、連線重複使用。過程中把請求和回應的組成一一點名，因為面試官正是在確認你講不講得出來。最後補上持久連線，因為這是多數人會漏掉、卻真的影響效能的一段。

## Full Spoken Answer

The client first resolves the hostname through DNS and opens a TCP connection to the server, conventionally on port 80 for HTTP and 443 for HTTPS. On HTTPS there is then a TLS handshake that negotiates encryption and verifies the server's certificate before any HTTP bytes are exchanged, which is why a first request to a cold host is noticeably slower than the ones after it.

客戶端會先透過 DNS 解析主機名稱，再與伺服器建立 TCP 連線，慣例上 HTTP 用 port 80、HTTPS 用 443。走 HTTPS 時還會有一次 TLS 交握，在任何 HTTP 位元組交換之前先協商加密並驗證伺服器憑證，這也是為什麼對一台「冷」主機發出的第一個請求會明顯比後續的慢。

The client then sends the request: a method such as GET or POST, the URI identifying the resource, the protocol version, a set of headers carrying metadata, and optionally a body when it is sending data. `Host` is the one header HTTP/1.1 makes mandatory, because the URI on the request line is usually just a path and the server has to know which of the sites it hosts you meant; the others carry content type, authorization, and accepted encodings. Headers are where most of the interesting behavior lives, because caching, authentication, and content negotiation are all decided there rather than in the path.

接著客戶端送出請求：一個方法（例如 GET 或 POST）、標示資源的 URI、協定版本、一組帶著中繼資料的標頭，以及在需要送資料時的 body。其中 `Host` 是 HTTP/1.1 唯一強制要求的標頭，因為請求行上的 URI 通常只是一段路徑，伺服器必須知道你要找的是它代管的哪一個網站；其餘則帶著內容型別、授權、可接受的編碼等資訊。真正有趣的行為大多發生在標頭裡，因為快取、認證和內容協商都是在那裡決定的，而不是在路徑上。

The server routes the request to a handler, runs the business logic, usually queries a database or calls other services, and builds a response. The response starts with a status code that tells the client how to interpret everything after it: 2xx succeeded, 3xx go somewhere else, 4xx the request was wrong, 5xx the server failed. Then come the response headers and, usually, a body. Getting the class right matters because clients, proxies, and monitoring all branch on it.

伺服器把請求路由到對應的處理函式，執行商業邏輯，通常會查資料庫或呼叫其他服務，然後組出回應。回應的開頭是狀態碼，它告訴客戶端該如何解讀後面的一切：2xx 成功、3xx 請去別的地方、4xx 請求本身有問題、5xx 伺服器出錯。接著是回應標頭，通常還有一個 body。狀態碼的分類要正確，因為客戶端、proxy 和監控系統都是依它來分支的。

Finally the connection is either closed or kept open. Since HTTP/1.1, persistent connections are the default, so the same TCP connection carries several request and response pairs and the handshake cost is paid once instead of every time. It is still one exchange at a time, though: the next request on that connection cannot start until the current response has finished, which is head-of-line blocking, and it is why browsers open around six connections per host. HTTP/2 is what removes that limit, by multiplexing many concurrent requests over a single connection. This is also the reason service-to-service calls should go through a pooled client rather than opening a fresh connection per call.

最後連線會被關閉或保持開啟。從 HTTP/1.1 開始持久連線是預設值，同一條 TCP 連線可以承載多組請求與回應，交握成本只付一次而不是每次都付。但同一時間仍然只能進行一組交換：目前的回應沒收完，同一條連線上的下一個請求就不能開始，這就是 head-of-line blocking，也是瀏覽器會對同一個 host 開大約六條連線的原因。真正解除這個限制的是 HTTP/2，它在單一連線上多工處理多個並行請求。這同時也是為什麼服務對服務的呼叫應該走連線池的客戶端，而不是每次呼叫都開一條新連線。

## Quick Reference

### What actually goes over the wire

A request is a start line, then headers, then a blank line, then an optional body:

```http
GET /users/123 HTTP/1.1
Host: api.example.com
Accept: application/json
Accept-Encoding: gzip
Authorization: Bearer <token>
```

The response has the same shape, with a status line in place of the start line:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 55
Cache-Control: max-age=60

{"id": 123, "name": "Ada Lovelace", "role": "engineer"}
```

The blank line is structural rather than cosmetic: it is the only thing marking where the headers stop. That is also why `Content-Length` matters - without it, or without `Transfer-Encoding: chunked`, the receiver has no way to know where the body ends and the next message on a reused connection begins.

### What is paid once, and what is paid every call

| Step | Paid when |
|---|---|
| DNS resolution | Once per hostname, then served from the OS or client cache |
| TCP handshake | Once per connection, and reused for as long as it is kept alive |
| TLS handshake | Once per connection, immediately after the TCP handshake |
| Request and response | Every call |
| Connection teardown | Once, when either side or the pool times the connection out |

The middle three rows are the whole argument for connection pooling: open a connection per call and you pay the top three on every single request.

## Interview Version

> The client resolves the hostname through DNS and opens a TCP connection, conventionally port 80 for HTTP and 443 for HTTPS. On HTTPS there is then a TLS handshake that negotiates encryption and verifies the certificate before any HTTP bytes move, which is why the first request to a cold host is noticeably slower than the ones after it. The client then sends the request: a method, the URI, the protocol version, headers, and optionally a body. Host is the one header HTTP/1.1 makes mandatory, because the request line usually carries only a path and the server has to know which of its sites you meant. Headers are where most of the interesting behaviour lives - caching, authentication, and content negotiation are all decided there rather than in the path. The server routes the request to a handler, runs the logic, usually hits a database or other services, and builds a response that starts with a status code telling the client how to read everything after it: 2xx succeeded, 3xx go elsewhere, 4xx the request was wrong, 5xx the server failed. Finally the connection is kept open or closed. Since HTTP/1.1 persistent connections are the default, so the handshake is paid once instead of every time, but it is still one exchange at a time - the next request cannot start until the current response finishes, which is head-of-line blocking, and it is why browsers open around six connections per host and why HTTP/2 multiplexes.

面試時可回答：客戶端先透過 DNS 解析主機名稱並開啟 TCP 連線，慣例上 HTTP 用 port 80、HTTPS 用 443。走 HTTPS 的話，在任何 HTTP 位元組移動之前還會有一次 TLS 握手，用來協商加密並驗證憑證 —— 這正是為什麼對一台冷的主機發出的第一個請求，明顯比後續的慢。接著客戶端送出請求：一個方法、URI、協定版本、一組標頭，以及選擇性的 body。Host 是 HTTP/1.1 唯一強制的標頭，因為請求行通常只帶路徑，伺服器必須知道你指的是它託管的哪一個站台。標頭是大部分有趣行為所在之處 —— 快取、認證、內容協商都在那裡決定，而不是在路徑上。伺服器把請求路由到 handler、執行邏輯、通常會打資料庫或其他服務，然後組出一個回應；回應以狀態碼開頭，告訴客戶端該怎麼解讀它後面的一切：2xx 成功、3xx 去別的地方、4xx 請求有問題、5xx 伺服器出錯。最後連線被保持或關閉。從 HTTP/1.1 起持久連線是預設，握手成本只付一次而不是每次都付；但它仍然一次只能進行一個交換 —— 下一個請求要等目前的回應結束才能開始，這就是 head-of-line blocking，也是為什麼瀏覽器對每個主機開大約六條連線、以及 HTTP/2 要做多工的原因。

The sentence to remember is: **One round trip is resolve, connect, handshake, send, handle, respond - and then keep the connection for the next one.**

最值得記：**一次來回就是：解析、連線、握手、送出、處理、回應 —— 然後把連線留給下一次。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q01: What is a RESTful API, and what are its core principles?](q01-what-is-a-restful-api.md) | [All 43 questions](../../README.md) | [Q11: Can you explain the difference between SQL and NoSQL databases?](../databases/q11-sql-vs-nosql.md) |
