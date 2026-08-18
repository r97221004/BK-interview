# Q08: What is the difference between a REST API and a WebSocket?

> Tests whether you can name the cases that actually need server push, and what a long-lived connection costs the backend.

**Part:** API & HTTP | **Importance:** 8/10 | **Status:** Draft

**New to these terms?** [rest](../_glossary.md#rest), [statelessness](../_glossary.md#statelessness), [persistent connection](../_glossary.md#persistent-connection), [redis](../_glossary.md#redis)

## In One Sentence

A REST API is one request and one response initiated by the client, while a WebSocket is a connection that stays open so either side, including the server, can send a message at any time.

REST API 是由客戶端發起的一來一回，而 WebSocket 是一條保持開啟的連線，兩邊（包含伺服器）在任何時候都可以主動送訊息。

## Answer Shape

Lead with the direction of communication, because that is the whole difference: REST is client-initiated and one-directional, a WebSocket is bidirectional and persistent. Give one example of each from the same product so the contrast is concrete, then close with what the persistent connection costs the backend, which is the part that separates a memorized answer from a used one.

先講通訊方向，因為差別全在這裡：REST 由客戶端發起、單向；WebSocket 是雙向且持續的。用同一個產品裡的兩個例子做對照，讓差異具體，最後說明持久連線對後端的代價 —— 這一段正是「背過答案」和「真的用過」之間的分水嶺。

## Full Spoken Answer

A REST API is stateless and one-directional. The client always starts the exchange: it sends a request, the server answers, and that interaction is finished. The underlying TCP connection may be reused, but the server has no way to speak first, so anything the client wants to know about it must ask for. That fits ordinary operations perfectly - fetching a record, submitting a form, creating an order.

REST API 是無狀態且單向的。永遠由客戶端開啟這次交換：它送出請求、伺服器回答，這次互動就結束了。底層的 TCP 連線可能會被重複使用，但伺服器沒有辦法先開口，所以客戶端想知道的任何事都必須自己去問。這非常適合一般操作 —— 取得一筆資料、送出表單、建立訂單。

A WebSocket is stateful and bidirectional. It begins as an HTTP request carrying an upgrade header, and once the handshake succeeds the same connection is repurposed into a full-duplex channel that stays open. From then on the server can push a message the instant something happens, without being asked. That is what makes it right for chat, live dashboards, collaborative editing, and multiplayer games, where the interesting events originate on the server.

WebSocket 是有狀態且雙向的。它一開始是一個帶著 upgrade 標頭的 HTTP 請求，交握成功後，同一條連線就被轉用成一條保持開啟的全雙工通道。從那時起，伺服器可以在事情一發生的當下就把訊息推出去，不需要被詢問。這使它適合聊天室、即時儀表板、協作編輯和多人遊戲 —— 這些場景裡有意義的事件都源自伺服器端。

In practice you use both, and an e-commerce site is the clearest illustration: REST for user management, the product catalog, and order creation, and a WebSocket for the live order-tracking panel where the status changes without a refresh. The cost is that an open connection is state. A connected client is tied to one instance, so scaling out needs either sticky routing or a shared pub/sub backplane such as Redis to fan messages across instances, and every idle connection still consumes a file descriptor and memory. If you only need modest freshness, server-sent events or plain polling is cheaper and much simpler to operate.

實務上兩者會並用，電商網站就是最清楚的例子：使用者管理、商品目錄和建立訂單走 REST，而不需重新整理就會更新的即時訂單追蹤面板走 WebSocket。代價是「一條開啟的連線就是狀態」。已連線的客戶端被綁在某一台實例上，所以要水平擴充就需要黏著式路由，或是像 Redis 這樣的共用 pub/sub 中介層把訊息擴散到各實例；而且每一條閒置連線仍然佔用一個 file descriptor 和記憶體。如果你只需要普通程度的即時性，server-sent events 或單純的輪詢會更便宜、也好維運得多。

## Quick Reference

| Feature | REST API | WebSocket |
|---|---|---|
| Communication | Client → Server | Client ↔ Server |
| Connection | New connection per request | Persistent connection |
| Protocol | HTTP | WS / WSS (after HTTP handshake) |
| Use Case | CRUD operations, simple data fetching | Real-time updates, live data streams |
| Example | `GET /users/1` → returns user data | Chat message instantly pushed to browser |

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q06: How do you approach API versioning in your projects?](q06-api-versioning.md) | [All 29 questions](../../README.md) | [Q13: What is data partitioning?](../databases/q13-data-partitioning.md) |
