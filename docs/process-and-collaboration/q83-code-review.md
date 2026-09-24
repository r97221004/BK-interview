# Q83: How do you do code review?

> Tests whether review is a real quality gate or a rubber stamp. The tell is whether you can say what you deliberately do not comment on.

**Part:** Process & Collaboration | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [timeout](../_glossary.md#timeout)

## In One Sentence

Keep the pull request small enough that someone can actually read it, look at correctness and failure paths rather than formatting, and let the linter own everything a machine can decide.

把 pull request 維持在「別人真的讀得完」的大小，看的是正確性和失敗路徑而不是排版，並且把所有機器判斷得了的事情交給 linter。

## Answer Shape

Start with size, because it decides everything else and it is the one thing most teams get wrong. Then say what you look at, in order, since an unordered list of virtues is not a method. Say what you deliberately do not comment on - that is the sentence that separates a real reviewer from someone performing thoroughness. Cover how to disagree without stalling the PR. Finish on what review is actually for, which is not catching bugs.

從大小開始，因為它決定了其他一切，而且那正是多數團隊做錯的地方。接著說你依序看什麼，因為一串沒有順序的美德不是方法。說出你**刻意不評論**什麼 —— 那一句話會把真正的 reviewer 和「表演仔細」的人分開。再講意見不合時怎麼不把 PR 卡住。最後收在 review 真正的目的，而那不是抓 bug。

## Full Spoken Answer

The first thing I would say is that pull request size decides review quality more than anything else. An 800-line PR gets an LGTM, because nobody can hold that much in their head and the honest reviewer and the lazy one produce the same comment. A 200-line PR gets real questions. So most of what makes review work happens before the review: keeping changes small, separating a refactor from a behaviour change so the diff is not half noise, and opening the PR early rather than after two weeks of work. If a change genuinely cannot be small, splitting it into a stack of PRs that each make sense on their own is better than one that nobody can evaluate.

我會先講的是：**pull request 的大小，比任何其他因素都更能決定 review 的品質**。一個 800 行的 PR 只會拿到 LGTM，因為沒有人腦袋裝得下那麼多東西，認真的 reviewer 和敷衍的 reviewer 會給出一模一樣的留言。一個 200 行的 PR 才會得到真正的問題。所以讓 review 有效的事情，大部分發生在 review 之前：改動要小、**把重構和行為改動分開**讓 diff 不會有一半是雜訊、以及早一點開 PR 而不是做完兩週才開。如果一個改動真的沒辦法小，那把它拆成一疊各自都說得通的 PR，也好過一個沒人評估得了的。

When I read one, I go in a fixed order, because looking at everything at once means looking at nothing properly. First correctness: does this actually do what the story says, and does the code match the description in the PR. Second the failure paths, which is where most real bugs live - what happens when this call times out, when the list is empty, when the input is null, when two of these run at the same time. Third readability, meaning whether I can follow it without asking the author. And fourth the tests: not whether tests exist, but whether they cover the new behaviour and would actually fail if someone broke it.

我讀一個 PR 的時候會照固定順序，因為同時看所有東西等於什麼都沒看仔細。**第一是正確性**：這段東西真的有做到 story 說的事嗎，而且程式碼跟 PR 描述相符嗎。**第二是失敗路徑**，真正的 bug 大多住在這裡 —— 這個呼叫逾時了會怎樣、清單是空的會怎樣、輸入是 null 會怎樣、兩個同時跑會怎樣。**第三是可讀性**，也就是我能不能不問作者就讀懂。**第四是測試**：不是「有沒有測試」，而是它有沒有涵蓋新的行為，以及如果有人把它弄壞了，那個測試會不會真的失敗。

The sentence that matters most here is what I deliberately do not comment on. Formatting, import order, naming conventions, line length - none of that belongs to a human. It goes in a formatter and a linter that run in CI, so the PR is already consistent before anyone opens it. Every minute spent arguing about a blank line is a minute not spent on the failure path that will page someone at 3am, and style comments also make review feel like harassment rather than help. If a machine can decide it, a machine should.

這裡最重要的一句，是**我刻意不評論什麼**。排版、import 順序、命名慣例、行寬 —— 這些都不屬於人類。它們該放進在 CI 裡跑的 formatter 和 linter，讓 PR 在任何人打開之前就已經一致了。每一分鐘花在爭論一個空行，就是一分鐘沒有花在那個會讓人半夜三點被 call 起來的失敗路徑上；而且風格留言會讓 review 感覺像找碴，而不是幫忙。**機器判斷得了的事，就該讓機器判斷。**

How the comment is written matters as much as what it says. I separate what must change from what is a suggestion, usually by marking the optional ones explicitly, so the author is not guessing which of eight comments block the merge. I ask rather than instruct - "what happens if this is empty?" gets a better outcome than "handle the empty case", because sometimes the answer is that it cannot be empty and I was the one who was wrong. And I say why, since a comment that only says what to change teaches nothing and has to be made again on the next PR.

**留言怎麼寫，跟留言寫什麼一樣重要。** 我會把「必須改」和「建議」分開，通常是把選擇性的那些明確標記出來，這樣作者就不用猜八則留言裡哪幾則會擋住 merge。我用問句而不是命令句 —— 「這裡如果是空的會怎樣？」得到的結果比「請處理空值的情況」好，因為有時候答案是「它不可能是空的」，錯的是我。而且我會說明**為什麼**，因為一則只說「要改成什麼」的留言什麼也沒教會人，下一個 PR 還得再講一次。

Disagreement needs a rule, otherwise a PR sits for three days. Mine is two round trips: if a thread has gone back and forth twice without converging, it stops being a comment thread and becomes a five-minute conversation, because text is a terrible medium for design disagreement. On who wins - for correctness, security, or something that breaks an existing contract, the reviewer's objection blocks. For anything that is a matter of taste or approach, the author decides, because they have the context and because a reviewer who overrides on preference is just slowing the team down. Either way the PR should not be the thing that is stuck.

意見不合需要一條規則，不然一個 PR 會卡三天。我的規則是**兩個來回**：如果一串討論來回兩次還沒收斂，它就不再是留言串，而是一次五分鐘的當面對話，因為文字是討論設計分歧最糟的媒介。至於誰說了算 —— **正確性、安全性、或是會破壞既有契約的事情，reviewer 的反對可以擋下 merge**。而任何屬於品味或做法偏好的事，**作者決定**，因為他有上下文，也因為一個用偏好去否決別人的 reviewer 只是在拖慢團隊。無論如何，卡住的不該是那個 PR。

The closing point is what review is actually for, because people assume it is catching bugs. It catches some, but tests and types catch far more, and catching bugs by reading is not something humans are reliably good at. The real output is that a second person now understands this part of the system. That is what stops a codebase where only one person can safely touch the payment module, it is how conventions actually spread through a team rather than living in a document nobody reads, and it is why review is worth the time even on a PR where you find nothing wrong.

收尾的重點是 **review 到底是為了什麼**，因為大家都以為是抓 bug。它確實會抓到一些，但測試和型別抓到的多得多，而且「靠讀程式碼抓 bug」本來就不是人類穩定做得好的事。**真正的產出是：現在有第二個人理解了系統的這一塊。** 那才是避免「只有一個人敢動金流模組」的原因，也是慣例真正在團隊裡擴散的方式 —— 而不是躺在一份沒人看的文件裡；這也是為什麼即使一個 PR 你什麼問題都沒挑出來，review 的時間還是值得花。

## Quick Reference

**What I look at, in this order:**

| Order | What | The question I am actually asking |
|---|---|---|
| **1** | Correctness | 它真的有做到 story 說的事嗎？程式碼跟 PR 描述相符嗎？ |
| **2** | Failure paths | 逾時了呢？空的呢？null 呢？兩個同時跑呢？ ← 真正的 bug 住這裡 |
| **3** | Readability | 我不問作者讀得懂嗎？ |
| **4** | Tests | 有沒有涵蓋新行為，而且**弄壞了真的會失敗**？ |
| ~~5~~ | ~~Formatting, imports, naming~~ | 不看 - 交給 formatter 和 linter |

**PR size is the whole game:**

| Size | What the review becomes |
|---|---|
| ~800 lines | LGTM - the careful reviewer and the lazy one produce the same comment |
| ~200 lines | Real questions |
| Refactor + behaviour change mixed | Half the diff is noise, so the real change hides in it |
| Too big to split | A stack of PRs that each stand alone beats one nobody can evaluate |

**How to write the comment:**

| Instead of | Write | Why |
|---|---|---|
| Eight comments, all equal | Mark which are blocking and which are optional | The author is not guessing what stops the merge |
| "Handle the empty case" | "What happens if this is empty?" | Sometimes it cannot be empty and the reviewer was wrong |
| "Use a set here" | "Use a set here - this is O(n²) on a list that grows with orders" | A comment without a why has to be made again next PR |

**Disagreement, so the PR does not sit for three days:**

| Situation | Rule |
|---|---|
| A thread has gone back and forth twice | Stop typing - five-minute conversation |
| Correctness, security, breaking an existing contract | The reviewer's objection blocks |
| Taste, approach, preference | The author decides - they have the context |

**What it is actually for:**

> Not catching bugs - tests and types catch more of those. The output is that **a second person now understands this part of the system**, which is what stops only one person being able to touch the payment module.

## Interview Version

> The thing that decides review quality more than anything else is pull request size. An 800-line PR gets an LGTM, because the careful reviewer and the lazy one produce the same comment; a 200-line PR gets real questions. So most of what makes review work happens before it: small changes, refactors separated from behaviour changes so the diff is not half noise, and a stack of PRs rather than one nobody can evaluate. When I read one I go in a fixed order. Correctness first: does it do what the story says. Then failure paths, where most real bugs live - what happens on a timeout, on an empty list, on null, when two run at once. Then readability, meaning can I follow it without asking the author. Then tests, not whether they exist but whether they cover the new behaviour and would fail if someone broke it. What I deliberately do not comment on is formatting, import order and naming - that belongs to a formatter and linter in CI, because a minute spent on a blank line is a minute not spent on the failure path that pages someone at 3am, and style comments make review feel like harassment. On how to comment: I separate blocking from optional so the author is not guessing, I ask rather than instruct because sometimes the answer is that I was wrong, and I say why, or the same comment has to be made on the next PR. For disagreement I use two round trips - if a thread has not converged twice, it becomes a five-minute conversation. The reviewer blocks on correctness, security or a broken contract; the author decides on taste, because they have the context. And the real point is not catching bugs, since tests catch more of those - it is that a second person now understands this part of the system.

面試時可回答：決定 review 品質最關鍵的，是 pull request 的大小。一個 800 行的 PR 只會拿到 LGTM，因為認真的 reviewer 和敷衍的 reviewer 會留下一模一樣的話；一個 200 行的 PR 才會得到真正的問題。所以讓 review 有效的事，大多發生在 review 之前：改動要小、把重構和行為改動分開讓 diff 不會有一半是雜訊，以及寧可拆成一疊各自成立的 PR，也不要一個沒人評估得了的。我讀的時候照固定順序。先是正確性：它有做到 story 說的事嗎。再來是失敗路徑，真正的 bug 大多住在那裡 —— 逾時會怎樣、清單是空的會怎樣、null 會怎樣、兩個同時跑會怎樣。接著是可讀性，也就是我不問作者讀不讀得懂。最後是測試，不是看有沒有，而是看它有沒有涵蓋新行為、而且弄壞了會不會真的失敗。我刻意不評論的是排版、import 順序和命名 —— 那屬於 CI 裡的 formatter 和 linter，因為花一分鐘在一個空行上，就是少花一分鐘在那個會讓人半夜被 call 起來的失敗路徑上，而且風格留言會讓 review 感覺像找碴。留言的寫法：我會把「必須改」和「建議」分開，讓作者不用猜；我用問句而不是命令句，因為有時候答案是我錯了；而且我會說明為什麼，否則同一則留言下個 PR 還得再寫一次。意見不合我用兩個來回當界線 —— 一串討論來回兩次還沒收斂，就改成五分鐘的當面對話。正確性、安全性、或破壞既有契約，reviewer 可以擋；屬於品味和做法的，作者決定，因為他有上下文。而真正的重點不是抓 bug，那件事測試做得比人好 —— 重點是現在有第二個人理解了系統的這一塊。

The sentence to remember is: **PR size decides review quality, the linter owns anything a machine can decide, and the real output is not a bug caught but a second person who understands that part of the system.**

最值得記：**PR 的大小決定 review 的品質；機器判斷得了的事交給 linter；而 review 真正的產出不是抓到一個 bug，是多了第二個看得懂這塊程式碼的人。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q73: When would you use composition instead of inheritance?](../code-design/q73-composition-vs-inheritance.md) | [All 51 questions](../../README.md) | [Q15: What strategies do you have when a database runs out of storage?](../databases/q15-database-out-of-storage.md) |
