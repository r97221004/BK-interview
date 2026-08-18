# Q02: Can you describe a typical HTTP request/response cycle?

> Tests whether you can follow a request end to end, including the TCP connection underneath and what persistent connections changed.

**Part:** API & HTTP | **Importance:** 9/10 | **Status:** Draft

**New to these terms?** [resource](../_glossary.md#resource), [cache](../_glossary.md#cache), [tls](../_glossary.md#tls)

## In One Sentence

The client opens a connection to the server, sends a request made of a method, a path, headers, and an optional body, the server does the work and sends back a status code with its own headers and body, and the connection is then reused or closed.

客戶端先與伺服器建立連線，送出一個由方法、路徑、標頭和選擇性 body 組成的請求；伺服器處理完後回傳一個狀態碼，加上自己的標頭與 body；連線接著被重複使用或關閉。

## Answer Shape

Walk the cycle in order and do not skip the transport: connection, request, processing, response, connection reuse. Name the parts of the request and the response as you go, because that is what the interviewer is checking you can list. Finish with persistent connections, since that is the part most candidates omit and it is the one with real performance consequences.

照順序把整個循環走一遍，而且不要跳過傳輸層：建立連線、送出請求、伺服器處理、回傳回應、連線重複使用。過程中把請求和回應的組成一一點名，因為面試官正是在確認你講不講得出來。最後補上持久連線，因為這是多數人會漏掉、卻真的影響效能的一段。

## Full Spoken Answer

The client first resolves the hostname through DNS and opens a TCP connection to the server, conventionally on port 80 for HTTP and 443 for HTTPS. On HTTPS there is then a TLS handshake that negotiates encryption and verifies the server's certificate before any HTTP bytes are exchanged, which is why a first request to a cold host is noticeably slower than the ones after it.

客戶端會先透過 DNS 解析主機名稱，再與伺服器建立 TCP 連線，慣例上 HTTP 用 port 80、HTTPS 用 443。走 HTTPS 時還會有一次 TLS 交握，在任何 HTTP 位元組交換之前先協商加密並驗證伺服器憑證，這也是為什麼對一台「冷」主機發出的第一個請求會明顯比後續的慢。

The client then sends the request: a method such as GET or POST, the URI identifying the resource, the protocol version, a set of headers carrying metadata such as content type, authorization, and accepted encodings, and optionally a body when it is sending data. Headers are where most of the interesting behavior lives, because caching, authentication, and content negotiation are all decided there rather than in the path.

接著客戶端送出請求：一個方法（例如 GET 或 POST）、標示資源的 URI、協定版本、一組帶著中繼資料的標頭（內容型別、授權、可接受的編碼等），以及在需要送資料時的 body。真正有趣的行為大多發生在標頭裡，因為快取、認證和內容協商都是在那裡決定的，而不是在路徑上。

The server routes the request to a handler, runs the business logic, usually queries a database or calls other services, and builds a response. The response starts with a status code that tells the client how to interpret everything after it: 2xx succeeded, 3xx go somewhere else, 4xx the request was wrong, 5xx the server failed. Then come the response headers and, usually, a body. Getting the class right matters because clients, proxies, and monitoring all branch on it.

伺服器把請求路由到對應的處理函式，執行商業邏輯，通常會查資料庫或呼叫其他服務，然後組出回應。回應的開頭是狀態碼，它告訴客戶端該如何解讀後面的一切：2xx 成功、3xx 請去別的地方、4xx 請求本身有問題、5xx 伺服器出錯。接著是回應標頭，通常還有一個 body。狀態碼的分類要正確，因為客戶端、proxy 和監控系統都是依它來分支的。

Finally the connection is either closed or kept open. Since HTTP/1.1 persistent connections are the default, so the same TCP connection carries several request and response pairs and the handshake cost is paid once instead of every time. HTTP/2 goes further and multiplexes many concurrent requests over one connection. This is the reason service-to-service calls should go through a pooled client rather than opening a fresh connection per call.

最後連線會被關閉或保持開啟。從 HTTP/1.1 開始持久連線是預設值，同一條 TCP 連線可以承載多組請求與回應，交握成本只付一次而不是每次都付。HTTP/2 更進一步，在單一連線上多工處理多個並行請求。這也是為什麼服務對服務的呼叫應該走連線池的客戶端，而不是每次呼叫都開一條新連線。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q21: What is the difference between session-based and JWT-based authentication?](../security-and-auth/q21-session-vs-jwt-authentication.md) | [All 29 questions](../../README.md) | [Q04: Explain statelessness in HTTP and how it impacts backend services.](q04-http-statelessness.md) |
