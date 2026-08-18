# Q34: How do you ensure your backend code is maintainable and easy to understand?

> Tests whether you have habits that survive a growing team, rather than a list of style rules.

**Part:** Architecture & Scaling | **Importance:** 6/10 | **Status:** Draft

**New to these terms?** [rest](../_glossary.md#rest), [unit test](../_glossary.md#unit-test), [query plan](../_glossary.md#query-plan)

## In One Sentence

Maintainable code comes from small pieces with one clear responsibility each, conventions applied consistently so nothing is surprising, and tests that let the next person change it without fear.

可維護的程式碼來自三件事：每個小單元只負責一件清楚的事、慣例一致到不會有意外，以及讓下一個人敢動它的測試。

## Answer Shape

Answer with habits rather than style rules, because anyone can name a linter and the question is really about what survives a growing team. Group them: structure first, then the conventions and documentation that make reading fast, then the safety net of tests and consistent error handling. Say who the audience is - the next engineer, who is often you in six months.

用習慣來回答，而不是風格規則，因為誰都說得出一個 linter，這題真正問的是「什麼能在團隊變大之後留下來」。把它們分組：先講結構，再講讓閱讀變快的慣例與文件，最後講測試與一致錯誤處理這張安全網。並且說出讀者是誰 —— 下一位工程師，而那常常是六個月後的你自己。

## Full Spoken Answer

The foundation is structure. I write modular code where each function or class has a single clear responsibility, so that a reader can understand one piece without holding the rest in their head, and so that changing one behavior touches one place. That means keeping the boundaries explicit - business logic separated from the HTTP layer and from the database layer - because when those blur, every change starts rippling and testing anything in isolation becomes impossible.

基礎是結構。我寫模組化的程式碼，讓每個函式或類別只有一個清楚的職責，這樣讀者理解某一段時不必把其餘部分都記在腦子裡，而修改某個行為時也只需要動一個地方。這代表要保持邊界明確 —— 商業邏輯與 HTTP 層、資料庫層分離 —— 因為當這些界線模糊時，每次改動都會開始擴散，任何東西都變得無法獨立測試。

On top of that come the conventions that make reading fast. I follow PEP 8 so formatting is never a discussion, use type hints so a signature says what it takes and returns without me having to read the body, and write docstrings for anything whose purpose is not obvious from the name. Comments I reserve for why rather than what - the code already says what it does, and a comment explaining a non-obvious decision or a workaround is worth far more than one narrating the next line. Enforcing the formatter and linter in CI matters more than the specific rules, because consistency is the actual benefit.

在此之上是讓閱讀變快的慣例。我遵循 PEP 8，讓格式永遠不必拿出來討論；使用型別提示，讓函式簽章不必讀內文就說清楚它收什麼、回傳什麼；並為任何無法從名稱看出用途的東西寫 docstring。註解我留給「為什麼」而不是「做什麼」—— 程式碼已經說明了它做什麼，而一則解釋非顯而易見的決策或繞道做法的註解，價值遠高於一則轉述下一行的註解。在 CI 中強制執行格式化工具與 linter，比具體採用哪套規則更重要，因為一致性才是真正的好處。

The last part is what makes change safe. I write unit tests with pytest so that a refactor is verified rather than hoped for, keep error handling and logging consistent across the system so a failure looks the same wherever it happens, and refactor regularly in small steps instead of letting technical debt accumulate into a rewrite. The way I judge all of it is by asking whether the next engineer to open this file - often me in six months, with no memory of the context - can understand it and change it confidently.

最後一部分是讓改動變安全的東西。我用 pytest 寫單元測試，讓重構是被驗證過的而不是靠祈禱；讓錯誤處理與日誌在整個系統中保持一致，使失敗無論發生在哪裡看起來都一樣；並且以小步驟持續重構，而不是任由技術債累積到必須整個重寫。我判斷這一切的方式是問一個問題：下一個打開這個檔案的工程師 —— 常常是六個月後、對脈絡毫無記憶的我自己 —— 能不能看懂它，並且有把握地修改它。

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q15: What strategies do you have when a database runs out of storage?](../databases/q15-database-out-of-storage.md) | [All 41 questions](../../README.md) | [Q42: What are the benefits of Docker multi-stage builds?](../devops-and-deployment/q42-docker-multi-stage-builds.md) |
