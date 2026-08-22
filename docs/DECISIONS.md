# 維護決策

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

