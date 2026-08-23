# 維護決策

## 2026-08-23：上游盤點的結論要附逐項證據，不能只寫分類

**決定**：`docs/UPSTREAM.md` 裡任何「不引用／不追」都必須寫出可查證的事實——diff 的檔案與行數、
本 fork 對應檔案的實際內容、或「該 PR 沒有 diff」這類直接可驗的狀態。禁止只寫「產品方向」
「等上游合併」這類分類詞。

**理由**：分類詞讀起來像理由，但它不能被檢驗，也不能被推翻。下一個人（或下一個 session）看到
「產品方向」時，既無法確認結論當時成不成立，也無法判斷現在是否還成立，於是只能整個重做一次
評估——這正是寫這份文件要避免的事。今天重驗上一輪的三筆結論，結論都沒變，但其中一筆的支撐
敘述（「沒有任何分支帶著獨佔 commit」）是錯的，正因為當時沒有逐條列出證據才沒被發現。

**限制**：
- 結論可以是「不引用」，但必須寫清楚**觸發條件**：什麼情況下要回來重看。
- 上游 issue 若指向本 fork 也有的規則或行為，要實際打開本 fork 的檔案確認，不能從 issue 標題推斷。

## 2026-08-22：建立 Windows-first 維護型 fork

**決定**：fork `KKKKhazix/human-writing`，保留 MIT 授權與完整歷史，預設分支維持 `main` 以降低與上游同步摩擦。本線聚焦繁中公開入口、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：上游 Skill、材料門檻與 `check_prose.py` 已經可用，且檢查完全在本機執行，符合主人用 AI 協作中文寫作、又不要空話灌水的需求。缺的是 Windows 11 上可重現的開發／驗收骨架，以及繁中入口。直接用上游 repo 難以長期記錄 fork 取捨。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- `human-writing/SKILL.md` 保持產品規格，不用維護索引覆寫。
- 不把產品規則翻譯成繁體；產品語言跟隨上游。
- 上游更新必須逐筆審查。

## 2026-08-22：維護線直接推 main

**決定**：fork 維護不再開功能分支。改完在本機跑 gate，通過後直接推 `origin/main`。遠端只留 `main`；`upstream/main` 只追蹤。

**理由**：這是單人維護 fork，分支與 PR 沒有第二審查者，只增加同步成本。

**限制**：
- Dependabot 與外部 fork 仍可能開 PR，讀 diff 後再合併，不自動合併。
- 不推 `upstream`，不 force-push `main`。
- 不刪 `upstream` remote。

## 2026-08-22：不啟用 Dependabot 自動合併

**決定**：Dependabot 只開 PR；CI 與人工讀 diff 通過後才合併。

**理由**：開發依賴只有 pytest / ruff，體積小，但自動合併仍會跳過「讀 diff」這一步。

## 2026-08-22：check_prose.py 重設 UTF-8 stdio

**決定**：在 `human-writing/scripts/check_prose.py` 開頭把 stdin／stdout／stderr `reconfigure(encoding="utf-8")`。不改硬禁令、警告層或正則。不同步回上游，除非之後另開回貢。

**理由**：Windows 預設 CP950 主控台印「漢字數」會 `UnicodeEncodeError`。本機 gate 的 `PYTHONUTF8=1` 遮不住一般使用者直接跑腳本。這是執行環境修正，不是寫作規則變更。

**限制**：上游若重寫 `check_prose.py`，merge 時要保留這段 stdio 重設，並重跑 `test_checker_prints_on_cp950_stdio`。

## 2026-08-22：不把警告層升成硬失敗

**決定**：變形翻案句、「不只……還……」、語境詞「不丟」維持警告（exit 0）。契約寫在 `docs/DEVELOPMENT.md` 與測試裡。

**理由**：升成硬失敗會改產品行為，等於另做一套檢查器。本輪只修 fork 能修的文件、測試與 Windows 崩潰。

