# Q10: What is the difference between TCP and UDP?

> Tests whether you can get past 'TCP is reliable, UDP is fast' to what the reliability actually costs - a round trip before any data moves, and one lost packet stalling everything behind it.

**Part:** API & HTTP | **Importance:** 8/10 | **Status:** Complete

**New to these terms?** [redis](../_glossary.md#redis), [backpressure](../_glossary.md#backpressure), [tls](../_glossary.md#tls), [timeout](../_glossary.md#timeout)

## In One Sentence

TCP is a connection that guarantees your bytes arrive, in order, resending whatever goes missing; UDP throws each message at the network once and never checks whether it got there.

TCP 是一條會保證位元組完整、依序抵達的連線，掉了什麼就重送；UDP 則是把每則訊息往網路一丟就結束，從不確認對方到底有沒有收到。

## Answer Shape

Lead with the guarantee rather than the speed: TCP is a reliable, ordered byte stream over a connection, UDP is unreliable, unordered datagrams with no connection at all. Then say what that guarantee costs - a round trip before any data moves, and a lost packet that stalls everything behind it - because the cost is the entire reason UDP still exists. Give one use of each that a backend engineer actually meets, and finish on HTTP/3, since "why would anyone run HTTP over UDP" is where the interviewer is heading.

先講保證，不要先講快慢：TCP 是建立在連線之上、可靠且有序的位元組串流，UDP 則是完全沒有連線、不保證送達也不保證順序的資料包。接著說明這個保證的代價 —— 送出任何資料之前要先花掉一次來回，而且只要掉一個封包，排在後面的東西全部卡住 —— 因為這個代價正是 UDP 至今仍然存在的理由。各舉一個後端工程師真的會遇到的用途，最後收在 HTTP/3，因為「為什麼有人要把 HTTP 架在 UDP 上」通常就是面試官接下來要問的。

## Full Spoken Answer

Both run on top of IP, and IP promises nothing at all: a packet can be dropped, duplicated, or arrive out of order. TCP is what turns that into a reliable, ordered byte stream between the two ends - you open a connection, write bytes in one end, and the same bytes come out the other end in the same order. UDP adds almost nothing to IP: eight bytes of header carrying the source and destination ports, a length, and a checksum. What you send is one self-contained datagram that either arrives whole or does not arrive at all, and nothing tells you which of the two happened.

兩者都跑在 IP 之上，而 IP 本身什麼都不保證：封包可能被丟掉、重複，或以錯亂的順序抵達。TCP 的作用就是把這種狀況變成兩端之間可靠且有序的位元組串流 —— 你建立一條連線，從這頭把位元組寫進去，另一頭就會以同樣的順序取出同樣的位元組。UDP 幾乎沒有在 IP 上加任何東西：只有八個位元組的標頭，帶著來源與目的埠號、一個長度和一個 checksum。你送出的是一個自成一體的資料包，它要嘛完整抵達、要嘛完全沒到，而且沒有任何東西會告訴你是哪一種。

TCP pays for that guarantee in three ways. It opens with a three-way handshake, so one full round trip is spent before a single byte of your data moves, and on HTTPS the TLS handshake sits on top of that. It numbers every byte and waits for an acknowledgement, retransmitting anything unacknowledged, which is what reliability actually means in practice. And it runs flow control and congestion control, slowing itself down when the receiver's buffer is full or the network starts dropping. The cost worth naming in an interview is the second one: the receiving kernel cannot hand your application byte 5001 before byte 5000, so one lost packet stalls everything queued behind it - including data that already arrived and is sitting in the buffer. That is head-of-line blocking, at the transport layer.

TCP 用三件事換到這個保證。它以三次握手開場，所以在你的資料送出第一個位元組之前，就先花掉一次完整的來回；走 HTTPS 的話，TLS 握手還疊在上面。它為每個位元組編號並等待對方確認，沒被確認的就重送，這才是「可靠」在實務上的意思。它還會做流量控制與壅塞控制，在接收端緩衝區滿了、或網路開始掉封包時自動放慢。面試中值得點名的是第二項的代價：接收端的核心必須先把第 5000 個位元組交給你的應用程式，才能交第 5001 個，所以掉一個封包就會讓排在後面的所有東西一起卡住 —— 包括那些其實早就抵達、正躺在緩衝區裡的資料。這就是傳輸層的 head-of-line blocking。

UDP is the right choice when late data is worthless, or when blocking the sender is worse than losing a message. Voice and video are the classic case: a frame that arrives after its slot has passed is useless, so retransmitting it spends bandwidth delivering something the decoder will discard. DNS is the other classic - one small question, one small answer, so a handshake would cost more than simply asking again when the timeout fires. The one most backend engineers actually touch is metrics: a StatsD client fires counters over UDP from inside a request handler, and if the collector is slow or down the packets are silently dropped. Do the same over TCP and a stalled collector applies backpressure straight into your response time, which means the monitoring takes down the thing it was monitoring.

當「太晚到的資料等於沒用」，或是「卡住送出端比掉一則訊息更糟」時，UDP 才是對的選擇。語音和視訊是經典案例：一個影格晚於它該播的時間才到就沒有用了，重送它只是花頻寬送來一份解碼器會直接丟掉的資料。DNS 是另一個經典：一個小問題、一個小答案，握手的成本比逾時後重問一次還高。而多數後端工程師真正會碰到的是監控指標：StatsD 這類客戶端會在 request handler 裡用 UDP 把計數丟出去，收集端變慢或掛掉時，封包就只是被默默丟掉。同一件事若走 TCP，一個卡住的收集端會把 backpressure 直接推進你的回應時間 —— 等於監控系統把它正在監控的服務弄垮。

The follow-up worth being ready for is HTTP/3, which runs over UDP and sounds like a contradiction. HTTP/2 multiplexes many streams over one TCP connection, so a single lost packet stalls every stream sharing it - the blocking moved down a layer rather than going away. QUIC fixes that by rebuilding reliability, ordering, and congestion control in userspace on top of UDP, tracking delivery per stream so a lost packet stalls only the stream it belonged to, and by folding the TLS handshake into the transport handshake so a new connection costs one round trip instead of two. So I would resist the phrase "UDP is faster". UDP is not faster on the wire; it just does less, and if the application needs that work done, someone has to write it - QUIC is what it looks like when they do.

值得先準備好的追問是 HTTP/3：它跑在 UDP 上，聽起來自相矛盾。HTTP/2 在單一條 TCP 連線上多工處理多個串流，於是掉一個封包，共用那條連線的每一個串流都跟著卡住 —— 阻塞只是往下搬了一層，並沒有消失。QUIC 的解法是在 UDP 之上、於使用者空間重新實作可靠性、順序與壅塞控制，並且以「每個串流各自追蹤」的方式送達，讓掉封包只卡住它自己所屬的那個串流；同時把 TLS 握手併進傳輸層握手，讓建立新連線從兩次來回降成一次。所以我會避免說「UDP 比較快」。UDP 在線路上並沒有比較快，它只是做得比較少；如果應用程式需要那些工作，總得有人把它寫出來 —— QUIC 就是有人把它寫出來的樣子。

## Quick Reference

### Side by side

| | TCP | UDP |
|---|---|---|
| Connection | Established by a three-way handshake before any data | None; the first packet is the data |
| Reliability | Lost segments are retransmitted until acknowledged | None; a lost datagram is simply gone |
| Ordering | Bytes are delivered in the order they were sent | Datagrams may arrive out of order, or twice |
| Message boundaries | None - it is a byte stream, so you frame it yourself | Preserved - one send is one datagram |
| Header | 20 bytes and up | 8 bytes |
| Congestion control | Built in; backs off when the network drops | None; you will flood the link if you do not pace yourself |
| Failure mode | Slow | Silently missing |
| Sockets in Python | `socket.SOCK_STREAM` | `socket.SOCK_DGRAM` |

### What a backend actually runs on which

| Protocol | Transport | Why |
|---|---|---|
| HTTP/1.1, HTTP/2 | TCP | A truncated response is worse than a slow one |
| HTTP/3 (QUIC) | UDP | Reliability rebuilt per stream, so one lost packet stalls only its own stream |
| PostgreSQL, MySQL, Redis | TCP | A partially delivered result set is meaningless |
| DNS | UDP, falling back to TCP | One small query and answer; TCP takes over when the response does not fit or for zone transfers |
| WebRTC media, VoIP, game state | UDP | The next frame supersedes the lost one anyway |
| StatsD metrics | UDP | Dropping a counter beats blocking a request handler |

### Two kinds of head-of-line blocking

The term shows up at two different layers, and knowing which one you mean is most of the answer:

| Layer | What is blocked | Removed by |
|---|---|---|
| HTTP/1.1 | The next request on the connection waits for the current response to finish | HTTP/2 multiplexing |
| TCP | Every stream on the connection waits while one lost packet is retransmitted | HTTP/3, by moving to QUIC over UDP |

## Interview Version

> Both sit on top of IP, which promises nothing - packets can be dropped, duplicated, or reordered. TCP is the "tracked delivery" option: it numbers every byte, and if number 3 goes missing, it holds back 4 and 5 - even though they already arrived - until 3 is resent, so the application always sees the bytes in order. UDP is "fire and forget": it just sends each datagram once and never checks whether it landed, so the receiver might get 1, 2, 4, 5 and simply never see 3. That difference is where TCP's real cost shows up: because TCP refuses to hand over byte 5001 before byte 5000, one lost packet stalls everything queued behind it - even data already sitting in the buffer - until the retransmit arrives, which is head-of-line blocking; TCP also spends a full round trip on a handshake before any data moves, plus TLS on top of that on HTTPS. UDP is worth that risk exactly when late data is worthless - in a video call, if frame 101 is dropped but the call has already moved on to playing frame 103, waiting for 101 to be resent doesn't help, because by the time it arrives its moment is gone - and the same logic applies to DNS, one small question and one small answer, and to metrics, where a StatsD client fires counters over UDP from a request handler because a stalled collector on TCP would push backpressure straight into your response time. That's also what HTTP/3 is solving: HTTP/2 multiplexes several streams over one TCP connection, so one lost packet stalls every stream sharing it, and QUIC runs over UDP and rebuilds reliability itself but per stream, so a lost packet only stalls its own stream while the others keep moving. So the one-line version: TCP guarantees delivery and order, but a single lost packet can stall everything behind it; UDP guarantees neither, which is exactly why it's the right choice when you'd rather drop data than wait for it.

面試時可回答：兩者都疊在 IP 之上，而 IP 什麼都不保證 —— 封包可能被丟棄、重複或順序錯亂。TCP 是「有追蹤的物流」：它為每個位元組編號，如果第 3 個不見了，就算 4、5 早就到了，也會先扣住不交出去，等 3 重送回來，確保應用程式看到的順序永遠是對的。UDP 則是「送出去就不管了」：它把每個 datagram 丟一次，從不確認有沒有送達，所以對方可能收到 1、2、4、5，卻永遠等不到 3。這個差異正是 TCP 真正代價所在：因為 TCP 不肯在交出第 5000 個位元組之前先交第 5001 個，掉一個封包就會讓排在後面的一切卡住 —— 就算那些資料早就到了、正躺在緩衝區裡也一樣 —— 直到重傳的那個到齊為止，這就是 head-of-line blocking；TCP 還會先花一次完整來回做三次握手才讓資料開始動，走 HTTPS 的話 TLS 握手還疊在上面。UDP 值得冒這個風險，正是在「太晚到的資料沒有價值」的場景：視訊通話裡，如果第 101 幀掉了，但畫面已經播到第 103 幀，等 101 重傳回來也沒用，因為它到的時候該播放的時機早就過了；DNS 也是同樣邏輯，一問一答都很小；監控指標更是如此，StatsD 客戶端會在 request handler 裡用 UDP 丟計數，因為若改用 TCP，一個卡住的收集端會把 backpressure 直接推進你的回應時間。這也是 HTTP/3 在解決的問題：HTTP/2 把多個 stream 多工在同一條 TCP 連線上，一個封包掉了，共用那條連線的每個 stream 都跟著卡；QUIC 跑在 UDP 之上，自己重建可靠性，但是以 stream 為單位重建，所以掉封包只會卡住它自己所屬的 stream，其他的照常繼續。所以一句話版本：TCP 保證送達與順序，但只要掉一個封包，後面的東西可能全部一起卡住；UDP 什麼都不保證，所以正因為如此，在你寧願丟資料也不要等待的場景裡，它才是對的選擇。

The sentence to remember is: **TCP guarantees your bytes arrive in order and makes you wait for the one that did not; UDP guarantees nothing and never makes you wait.**

最值得記：**TCP 保證位元組依序送達，代價是要為沒到的那一個等下去；UDP 什麼都不保證，所以從不讓你等。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q08: What is the difference between a REST API and a WebSocket?](q08-rest-vs-websocket.md) | [All 47 questions](../../README.md) | [Q12: What is data normalization?](../databases/q12-data-normalization.md) |
