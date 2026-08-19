# Q09: How would you handle file uploads in a web application?

> Tests whether you treat uploads as untrusted input and whether you know the scaling problem hidden in the naive implementation.

**Part:** API & HTTP | **Importance:** 7/10 | **Status:** Draft

**New to these terms?** [presigned url](../_glossary.md#presigned-url), [tls](../_glossary.md#tls), [cdn](../_glossary.md#cdn), [message queue](../_glossary.md#message-queue)

## In One Sentence

Your backend decides who may upload and what is allowed; object storage carries the bytes - and everything else follows from keeping those two jobs apart.

你的後端負責決定「誰可以上傳、可以上傳什麼」，物件儲存負責搬運位元組 —— 其餘的一切，都是把這兩份工作分開之後自然推導出來的。

## Answer Shape

Split it into the decisions rather than a list of tips: where the bytes land, how you validate them, what you name the file, and how large files get through. Say explicitly that validation is server-side and based on content, not the extension. Finish with direct-to-storage uploads, because that is the answer that shows you have run this at scale rather than built it once.

把它拆成幾個決策，而不是一串小技巧：位元組落在哪裡、你怎麼驗證、檔案取什麼名字，以及大檔怎麼通過。明確說出驗證在伺服器端、而且看內容不看副檔名。最後帶到直傳儲存服務，因為這個答案顯示你真的在規模下跑過，而不只是做過一次。

## Full Spoken Answer

I would split it into file size, validation, security, storage, and the flow for large files. The baseline shape is: the browser posts `multipart/form-data` to the backend over HTTPS, the backend validates it, the file goes into object storage such as S3, and the database stores only metadata - `file_id`, `original_filename`, `storage_key`, `content_type`, `size`, `owner_id`, `created_at`. I would not put the file itself in the database. Row 123 says the user called it `resume.pdf` and that it lives at `uploads/2026/08/<uuid>.pdf`; the actual bytes sit in the bucket under exactly that key. Keeping them apart is what makes CDNs, backups, capacity, and lifecycle rules straightforward later.

我會把它拆成檔案大小、驗證、安全性、儲存方式，以及大檔的流程。基本形狀是：瀏覽器透過 HTTPS 送出 `multipart/form-data` 給後端，後端驗證，檔案進到像 S3 這樣的物件儲存，而資料庫只存中繼資料 —— `file_id`、`original_filename`、`storage_key`、`content_type`、`size`、`owner_id`、`created_at`。我不會把檔案本身放進資料庫。第 123 列記著使用者把它叫做 `resume.pdf`，以及它放在 `uploads/2026/08/<uuid>.pdf`；真正的位元組就躺在 bucket 裡的那個鍵值底下。把兩者分開，正是之後要做 CDN、備份、容量擴展和生命週期規則時會輕鬆的原因。

Validation has to be server-side, always. The front end can check first, but you cannot trust the front end. And the thing you especially cannot trust is the extension: an attacker renames `malware.exe` to `photo.jpg` and nothing about the name has changed what the file is. So the backend checks size, checks the type from an allowlist, and confirms the real content type by reading the file's magic bytes rather than believing the extension or the declared `Content-Type`. Enforce the size cap at the proxy as well as in the handler - say 10 MB - so an oversized body is rejected before you buffer it, otherwise anyone can drain your memory, disk, and bandwidth just by uploading. And store uploads outside any directory the web server would execute or serve directly. OWASP's File Upload Cheat Sheet is the reference worth naming.

驗證一定要在伺服器端。前端可以先檢查，但你不能信任前端。而其中最不能信的就是副檔名：攻擊者把 `malware.exe` 改名成 `photo.jpg`，這個檔案是什麼並沒有因為改名而改變。所以後端要檢查大小、用白名單檢查型別，並且透過讀取檔案的 magic bytes 來確認真正的內容型別，而不是相信副檔名或宣告的 `Content-Type`。大小上限要在 proxy 和處理函式兩邊都設 —— 例如 10 MB —— 讓過大的 body 在被緩衝之前就遭拒；否則任何人只要一直上傳，就能把你的記憶體、磁碟和頻寬吃光。另外，上傳的檔案要放在網頁伺服器不會直接執行或提供的目錄之外。值得點名的參考是 OWASP 的 File Upload Cheat Sheet。

Never store a file under the name the user gave you. If someone uploads a file called `../../etc/passwd` and your code does `save_path = "/uploads/" + filename`, you have handed them path traversal. Generate the storage key yourself - a UUID such as `550e8400-e29b-41d4-a716-446655440000.pdf` - and keep `resume.pdf` purely as metadata to show on download. That one move removes path traversal and the collision between two users uploading `photo.jpg` on the same day.

永遠不要用使用者給的名稱來存檔。如果有人上傳一個叫 `../../etc/passwd` 的檔案，而你的程式碼寫的是 `save_path = "/uploads/" + filename`，你就等於把路徑穿越送給了對方。儲存鍵值要自己產生 —— 一個 UUID，例如 `550e8400-e29b-41d4-a716-446655440000.pdf` —— 而 `resume.pdf` 純粹當成中繼資料保存，下載時顯示用。這一個動作同時消除了路徑穿越，以及兩個使用者在同一天上傳 `photo.jpg` 的碰撞問題。

For a small system, routing the bytes through the backend is fine. It stops being fine the moment someone uploads a 2 GB video, because now your backend receives 2 GB and then sends 2 GB onward - you pay for every byte twice, and its CPU, memory, bandwidth, and connections are tied up for the whole transfer. A handful of slow clients can starve the worker pool. So at any real size the answer is a presigned URL: the browser asks the backend "I want to upload file.pdf", the backend checks permissions and returns a short-lived presigned upload URL, the browser uploads straight to object storage, and then tells the backend it finished so the metadata gets recorded. The way I would put it in an interview is that the backend is the front desk issuing passes - it decides who may upload and what is allowed - and object storage is the loading dock that actually takes the hundreds of megabytes. The person issuing passes should not be carrying the boxes.

對小型系統來說，讓位元組經過後端沒問題。但只要有人上傳一支 2 GB 的影片，它就不再沒問題了，因為你的後端要先「收」2 GB，再「送」2 GB 出去 —— 每一個位元組你都付兩次錢，而它的 CPU、記憶體、頻寬和連線在整段傳輸期間都被佔住。少數幾個慢速客戶端就能把 worker pool 榨乾。所以到了真正的規模，答案是 presigned URL：瀏覽器先問後端「我要上傳 file.pdf」，後端檢查權限後回一個短效的 presigned 上傳網址，瀏覽器直接把檔案傳到物件儲存，傳完再告訴後端一聲，讓中繼資料被記下來。面試時我會這樣說：後端是發通行證的櫃檯 —— 它決定誰可以上傳、可以上傳什麼 —— 而物件儲存是真正承接那幾百 MB 的卸貨區。發通行證的人不該自己扛箱子。

For genuinely large files, add multipart or resumable uploads. A 5 GB file does not go up as 5 GB; it goes up as roughly fifty 100 MB parts. The reason that matters is failure: if part 37 dies on a flaky connection, you retry part 37, not the whole 5 GB. For video, datasets, and backups this is the difference between an upload that completes and one that never does.

面對真正的大檔，再加上 multipart 或可續傳上傳。一個 5 GB 的檔案不是以 5 GB 送上去，而是切成大約五十個 100 MB 的 part。這件事之所以重要，關鍵在失敗：如果第 37 個 part 在不穩的連線上掛了，你重試的是第 37 個 part，而不是整個 5 GB。對影片、資料集和備份來說，這就是「上傳得完」和「永遠傳不完」的差別。

The same thinking applies on the way back down. A private document must not sit at a permanently public `https://bucket.s3.amazonaws.com/user123/passport.pdf`, because that URL is a password that never expires and cannot be revoked. Instead the request goes to the backend, the backend checks that this user may read this file, and it issues a signed URL that expires in five minutes. Around that, layer what the product needs: virus scanning before a file is marked usable, per-user quotas, rate limits, a sensible `Content-Disposition` so a browser downloads rather than renders untrusted content, locked-down bucket permissions, and a queue for expensive work like thumbnailing or transcoding. The whole answer in one line: object storage, presigned URLs, server-side validation, size limits, generated filenames, and authorization on both ends - the backend issues the passes and never carries the boxes.

同樣的思路也適用在下載方向。一份私人文件不該永久公開地放在 `https://bucket.s3.amazonaws.com/user123/passport.pdf`，因為那個網址等於一組永不過期、也無法撤銷的密碼。正確做法是請求先進到後端，後端確認這位使用者有權讀這個檔案，然後簽發一個五分鐘後過期的 signed URL。在這之外，再依產品需要疊加：標記為可用前先做病毒掃描、對每位使用者設配額、速率限制、設定合理的 `Content-Disposition` 讓瀏覽器下載而不是直接渲染不可信內容、把 bucket 權限鎖緊，以及把縮圖或轉檔這類昂貴工作丟進佇列。整題濃縮成一句：物件儲存、presigned URL、伺服器端驗證、大小上限、自己產生的檔名，以及上傳與下載兩端的授權 —— 後端只發通行證，永遠不扛箱子。

## Quick Reference

### Who stores what

| Where | What it holds |
|---|---|
| Database row | `file_id: 123`, `original_filename: resume.pdf`, `content_type`, `size`, `owner_id`, `created_at` - and `storage_key: uploads/2026/08/<uuid>.pdf` |
| Object storage | The actual bytes, under exactly that key |

`storage_key` is the only thing joining the two. Metadata in the database, bytes in the bucket. Putting the file in the database costs you CDN delivery, cheap backups, and lifecycle rules.

### Never trust what the client controls

| The client says | The attack | What you do instead |
|---|---|---|
| `photo.jpg` | `malware.exe` renamed | Read the magic bytes; allowlist the real type |
| `Content-Type: image/png` | Declares PNG, ships anything | Same - the declared type is a hint, not evidence |
| Filename `../../etc/passwd` | Path traversal | Generate a UUID storage key; keep the name as metadata only |
| No size at all | Fills memory, disk, bandwidth | Cap at the proxy *and* the handler, e.g. 10 MB |

### Two upload paths

| | Through the backend | Presigned URL |
|---|---|---|
| Flow | Browser → backend → storage | Browser → backend for a pass, then browser → storage |
| Backend handles | Every byte, twice | A permission check and a signature |
| A 2 GB upload | 2 GB in, 2 GB out, worker held | Backend touches none of it |
| Good for | Small files, simple systems | Anything large, or high volume |

Presigned upload, four steps:

```
1. Browser → Backend      "I want to upload file.pdf"
2. Backend → Browser      short-lived presigned upload URL
3. Browser ──────────────→ Object storage    (the bytes go here, directly)
4. Browser → Backend      "done" → backend records the metadata
```

### Large files: parts, not one stream

```
5 GB in one request        →  one flaky moment loses everything
5 GB as ~50 × 100 MB parts →  part 37 fails, retry part 37
```

### Private downloads

| Wrong | Right |
|---|---|
| `https://bucket.s3.amazonaws.com/user123/passport.pdf`, public forever | Backend checks permission, issues a signed URL that expires in ~5 minutes |

### The words to get into the answer

Object storage · presigned URL · server-side validation · size limit · generated filename · authorization

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q61: How do you choose HTTP status codes and design error responses?](../api-design/q61-status-codes-and-error-responses.md) | [All 41 questions](../../README.md) | [Q24: Describe how session management works in web applications.](../security-and-auth/q24-session-management.md) |
