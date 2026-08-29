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

**理由**：上游 Skill、材料門檻與 `check_prose.py` 已經可用，且檢查完全在本機執行，符合維護者用 AI 協作中文寫作、又不要空話灌水的需求。缺的是 Windows 11 上可重現的開發／驗收骨架，以及繁中入口。直接用上游 repo 難以長期記錄 fork 取捨。

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

## 2026-08-29：上游檢查補上 PR 與 issue 兩個面向

**決定**：`check_upstream_updates.py` 補上以 `--state all` 收集上游 PR／issue 的邏輯，
`upstream-check.yml` 補 `GH_TOKEN: ${{ github.token }}`，新增 `tests/test_upstream_updates.py`。
Baseline 既有的水位不動。

**理由**：`docs/UPSTREAM.md` 早就寫著「四個面向都要看」，`upstream_baseline.json` 也記著
`reviewed_pr_through` 與 `reviewed_issue_through`——但**沒有任何程式讀那兩個欄位**，檢查器只比對
commit 水位。那兩個面向不是「查過沒發現」，是根本沒查，而每週的排程報告長得跟查過一樣綠。
這是艦隊層級的問題：24 個 fork 裡 21 個都這樣（`SanHsien/repo-fleet-ops` 的 `docs/INCIDENTS.md`
第十條）。參考實作是 `SanHsien/harness-guard`。

三個性質，缺一不可：

- **`--state all`**：只查 `open` 看不到「開了又關、沒有合併」的 PR，而那正是「上游拒收、但可能對
  本 fork 有價值」的一類——已合併的遲早會經由 commit 抵達，被關掉的永遠不會。
- **`gh` 失敗時回 `None` 不回 `[]`**，報告寫 `Not checked` 並 **fail closed**（exit 2）。
  「沒查到」和「沒有」在綠色報告裡長得一樣，只有一個是真的。
- **`GH_TOKEN`**：`gh` 在 Actions 裡沒有憑證就列舉不到，配上 fail closed 會讓紅燈的意思變成
  「檢查器壞了」而不是「上游有東西」。

**證據**：落地後實跑 `python tools/check_upstream_updates.py`，三個面向都印出水位與待辦數；
本 repo 的 gate 全綠。

**已知代價**：水位以上真的有東西時，每週的 upstream-check 會回 exit 1。那是它該做的事——先前的
綠燈不是「沒有待辦」，是沒有人看。

**觸發條件**：報告列出項目時逐筆讀 diff、把採用／略過理由寫進本檔，然後才推進 baseline 的水位。
