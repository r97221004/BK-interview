# Q09: How would you handle file uploads in a web application?

> Tests whether you treat uploads as untrusted input and whether you know the scaling problem hidden in the naive implementation.

**Part:** API & HTTP | **Importance:** 7/10 | **Status:** Draft

**New to these terms?** [tls](../_glossary.md#tls), [message queue](../_glossary.md#message-queue)

## In One Sentence

Handling uploads well means treating the file as untrusted input, storing it under a name you generated, recording what it was in the database, and keeping the bytes out of your application server.

把上傳處理好，指的是把檔案當成不可信任的輸入、用你自己產生的名稱儲存、把它的資訊記在資料庫，並且讓實際的位元組不要經過你的應用伺服器。

## Answer Shape

Answer as a sequence of decisions rather than a list of tips: where the bytes go, how you validate them, what you name the file, and what you record about it. Say explicitly that validation is server-side and based on content rather than the extension. Finish with direct-to-storage uploads, because that is the answer that shows you have run this at scale rather than only built it once.

用一連串決策來回答，而不是一串小技巧：位元組要送到哪裡、你怎麼驗證它們、檔案要取什麼名字、以及你要記錄什麼。明確說出驗證是在伺服器端、而且是根據內容而非副檔名。最後帶到直傳儲存服務，因為這個答案顯示你真的在規模下跑過，而不只是做過一次。

## Full Spoken Answer

First, the connection must be HTTPS so the file and any credentials are protected in transit. Then decide where the bytes actually land. The straightforward implementation streams a multipart form upload through the application server to disk or to object storage, and it is fine at low volume. Its problem is that large uploads occupy a request worker for the whole transfer, so a handful of slow clients can starve the pool.

首先，連線必須是 HTTPS，讓檔案和任何憑證在傳輸中受到保護。接著決定位元組實際上要落在哪裡。最直接的做法是把 multipart 表單上傳串流經過應用伺服器寫到磁碟或物件儲存，在流量不大時完全沒問題。它的問題在於大檔案上傳會在整個傳輸期間佔住一個請求 worker，所以少數幾個慢速客戶端就可能把 worker pool 榨乾。

Validate on the server, always, and never trust what the client says the file is. Enforce a maximum size at the proxy as well as in the handler so an oversized body is rejected before it is buffered. Check the actual content type by inspecting the file's magic bytes rather than believing the extension or the declared content type, and accept from an allowlist rather than rejecting a blocklist. Store uploads outside any directory the web server will execute or serve directly. The OWASP File Upload Cheat Sheet is the reference worth citing here.

一定要在伺服器端驗證，而且永遠不要相信客戶端宣稱這個檔案是什麼。在 proxy 和處理函式兩邊都設定大小上限，讓過大的 body 在被緩衝之前就被拒絕。用檢查檔案 magic bytes 的方式判斷真正的內容型別，而不是相信副檔名或宣告的 content type，並且採用白名單放行而不是黑名單阻擋。上傳的檔案要存放在網頁伺服器不會直接執行或提供的目錄之外。這裡值得引用的參考是 OWASP File Upload Cheat Sheet。

Never store the file under the name the user supplied. Generate your own identifier, such as a UUID, and use that as the stored object key. This removes path-traversal tricks and collisions between two users uploading the same filename in one step. Keep the original filename, size, content type, owner, and upload timestamp as a row in the database alongside that key, so you can show users a sensible name on download and clean up orphaned objects later.

永遠不要用使用者提供的名稱來存檔。自己產生一個識別碼，例如 UUID，用它當作儲存的物件鍵值。這一步同時消除了路徑穿越的手法，以及兩個使用者上傳同名檔案時的碰撞。把原始檔名、大小、內容型別、擁有者和上傳時間記成資料庫裡的一列，和那個鍵值放在一起，這樣下載時可以顯示合理的名稱，之後也能清理掉沒有主人的物件。

At scale, take the bytes out of the application path entirely. The backend issues a short-lived presigned URL and the client uploads straight to object storage such as S3, then calls back with the key so the server records the metadata. The application never buffers the file, so upload size stops being a scaling problem. Layer on the rest as the product needs it: virus scanning before the file is marked usable, per-user quotas, and a queue for anything expensive such as thumbnailing or transcoding.

在規模上來之後，就把位元組完全移出應用程式的路徑。後端簽發一個短效的 presigned URL，客戶端直接上傳到像 S3 這樣的物件儲存，接著再回呼把鍵值交回來讓伺服器記錄中繼資料。應用程式從頭到尾都不需要緩衝檔案，上傳大小也就不再是擴充上的問題。其餘的再依產品需要疊加：在標記為可用之前先做病毒掃描、對每個使用者設配額，以及把縮圖或轉檔這類昂貴工作丟進佇列。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q61: How do you choose HTTP status codes and design error responses?](../api-design/q61-status-codes-and-error-responses.md) | [All 41 questions](../../README.md) | [Q24: Describe how session management works in web applications.](../security-and-auth/q24-session-management.md) |
