# Q42: What are the benefits of Docker multi-stage builds?

> Tests whether you can explain why deleting build tools in a later layer does not shrink the image.

**Part:** DevOps & Deployment | **Importance:** 5/10 | **Status:** Draft

**New to these terms?** [cache](../_glossary.md#cache), [containerization](../_glossary.md#containerization), [query plan](../_glossary.md#query-plan)

## In One Sentence

A multi-stage build uses one stage with the full toolchain to compile the application and a second, minimal stage that copies only the finished artifact, so compilers and source code never reach the shipped image.

多階段建置用一個帶有完整工具鏈的階段來編譯應用程式，再用第二個精簡階段只複製最終產物，讓編譯器和原始碼永遠不會進到出貨的映像檔裡。

## Answer Shape

Lead with the mechanism, because the benefits are all consequences of it. Then explain why it is necessary at all - deleting build tools in a later layer does not shrink the image - since that is the piece most candidates miss and it is the real insight. Give size, security, and clarity as the results, and finish with the caching behavior that shows up in CI.

先講機制，因為所有好處都是它的後果。接著解釋它為什麼有存在的必要 —— 在後續層刪掉編譯工具並不會讓映像檔變小 —— 因為這正是多數人會漏掉的一塊，也是真正的洞察。把體積、安全與可讀性列為結果，最後補上在 CI 中會顯現的快取行為。

## Full Spoken Answer

A multi-stage build is a Dockerfile with more than one FROM instruction. The first stage starts from a full image containing compilers, package managers, and development headers, and builds the application. The final stage starts from a minimal base and copies only the artifacts it needs - the compiled binary, the installed dependencies, the built assets - out of the earlier stage. Everything else in that first stage is simply left behind.

多階段建置是一個含有多個 FROM 指令的 Dockerfile。第一階段以一個包含編譯器、套件管理器和開發標頭檔的完整映像檔為起點，把應用程式建置出來。最後一階段則從一個精簡的基底出發，只從先前的階段複製它需要的產物 —— 編譯好的執行檔、安裝好的相依套件、建好的靜態資源。那第一階段裡的其他東西就直接被丟在後面。

The reason this technique is necessary at all is how image layers work, and it is the point worth making explicitly. Layers are additive: a later instruction that deletes a file only records a whiteout entry hiding it, while the bytes remain in the earlier layer forever. So installing a compiler and then removing it in a later RUN leaves the image exactly as large as before, and the compiler is still recoverable from the image history. A multi-stage build sidesteps this entirely, because the discarded stage never becomes part of the final image in the first place.

這個技巧之所以有必要，關鍵在於映像檔的層是怎麼運作的，而這一點值得明講。層是累加的：後面的指令刪除一個檔案，只會記錄一個 whiteout 條目把它藏起來，位元組仍然永遠留在前面的層裡。所以「先安裝編譯器、之後再用一個 RUN 移除它」，映像檔的大小和原本一模一樣，而且編譯器仍然能從映像檔歷史中還原出來。多階段建置完全繞開了這個問題，因為被丟棄的那個階段從一開始就沒有成為最終映像檔的一部分。

The first result is size. A final image built this way contains the runtime and the artifact and nothing else, which routinely turns a build image of several hundred megabytes into a runtime image of tens. That is faster to push, faster to pull, and faster to start on every node during a deploy. The second is security: with no compilers, no package manager, and no source code in the shipped image, the attack surface shrinks and there is simply less software for a vulnerability scanner to find. An attacker who gets code execution in a container without a shell or a package manager has far fewer options.

第一個結果是體積。以這種方式建出的最終映像檔只包含執行環境和產物，沒有其他東西，這通常能把數百 MB 的建置映像檔變成數十 MB 的執行映像檔。它推送更快、拉取更快，在部署時於每個節點上啟動也更快。第二個是安全性：出貨的映像檔裡沒有編譯器、沒有套件管理器、沒有原始碼，攻擊面因此縮小，漏洞掃描器能找到的軟體也單純變少了。一個在沒有 shell、沒有套件管理器的容器中取得程式碼執行能力的攻擊者，可用的選項少得多。

The third is clarity, since each stage has one obvious purpose - build, test, runtime - which makes the Dockerfile easier to read and to change. And in CI the caching behavior pays off: Docker caches each stage, so when only the application source has changed, the dependency-installation stage is reused and only the later stages rebuild. Ordering the instructions so that dependency files are copied and installed before the source is copied is what makes that cache actually hit.

第三個是清晰度，因為每個階段都有一個明確的目的 —— 建置、測試、執行 —— 讓 Dockerfile 更好讀也更好改。而在 CI 中，快取行為會帶來回報：Docker 會快取每個階段，所以當只有應用程式原始碼改變時，安裝相依套件的那個階段會被重用，只有後面的階段需要重建。把指令排成「先複製並安裝相依清單，再複製原始碼」，正是讓那個快取真的命中的關鍵。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q35: When would you move work onto a message queue?](../architecture-and-scaling/q35-message-queues-and-async-work.md) | [All 41 questions](../../README.md) | *(last question)* |
