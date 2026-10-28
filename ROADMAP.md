# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `fbb80bafdbeb` 查的快照，開工前先重查 GitHub。

## 現況

本 repo 維護中文寫作 Skill 與純標準庫檢查器，檢查器只報告規則命中，不自動改稿；exit 0 仍需人工判斷文體（`AGENTS.md:7-8,21,25-30`）。2026-10-29 快照 open PR、安全告警均為 0，CI、CodeQL、Dependency freshness、Upstream check 最近結果為 success；issue 因停用而未查到（2026-10-29 `gh` 查詢，`fbb80bafdbeb`）。上游第三方憑證提案已審不採用，沒有待補的 workflow 修復；真實長稿驗收仍缺（`docs/DECISIONS.md:117-125`；`REVIEW.md`〈尚未宣稱範圍〉）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 補一篇真實長稿的寫作與改稿驗收 | 現有 gate 只驗規則契約，不能證明完整寫作流程或文學性中文的誤傷情況 | 維護者提供可用且去識別的材料；同一稿走材料核對、初稿、檢查與人工改稿，記錄硬失敗／人工警告及保留理由；確認原稿未被檢查器改寫、未提交私人材料 | 維護者 | `REVIEW.md`〈尚未宣稱範圍〉；`AGENTS.md:19,21,29` |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 增量審查上游與 description 變更 | 超過 baseline 水位、已審 PR head 改變，或本 fork 實測出現誤觸發／長度限制 | 逐筆讀 diff 並記錄取捨；保留 UTF-8 stdio 修正與警告契約；Windows gate 通過後才更新 baseline | Codex | `tools/upstream_baseline.json:4-8`；`docs/DECISIONS.md:98-102`；`AGENTS.md:30,44-53` |
| 修連結檢查器的孤立反引號處理 | 維護文件出現孤立反引號，且證明後續真連結被吞掉 | 新增跨段孤立反引號與真斷鏈的重現測試；真斷鏈需報錯、合法行內碼不誤報；`pwsh -NoProfile -File tools/dev_check.ps1` 通過 | Codex | 深掃報告（2026-10-26）〈刻意不修〉；`tools/check_links.py` 的行內碼處理 |
| 驗證聊天介面的 lite 版本 | 維護者實際需要在 ChatGPT／千問直接貼上使用 | 選一個介面、一份合法來源做一次有停止條件的驗收，記錄貼入版本、輸出與規則限制；只報該宿主結果 | 維護者 | `REVIEW.md`〈尚未宣稱範圍〉；`human-writing/dist/human-writing-lite.md` |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 把人工警告升為硬失敗、讓腳本自動改稿或建立作者畫像服務 | 這會改變產品契約；決策見 `docs/DECISIONS.md:56-60`，邊界見 `AGENTS.md:21,29` | 有可重現誤判與明確產品變更需求，先定義人工裁量與相容性 |
| 引進第三方憑證 reusable workflow | 本線沒有對下游簽署的需求；已審理由見 `docs/DECISIONS.md:117-125` | 上游正式採用或本線需對外發布來源證明時，先評估 GitHub 原生方案 |
| 先行採用平行翻譯版或 WorkBuddy 封裝、為 fork 文件修改上游 CHANGELOG | 產品語言與發佈線邊界見 `AGENTS.md:17-18,74`、`docs/DECISIONS.md:91-102`、`docs/UPSTREAM.md` | 上游產品契約改變，或維護者提出該宿主的實際需求 |

## 維護方式

每週依 baseline 及已審 PR head 做增量審查；水位表示已審，不表示合併，沒有共同祖先也不需改寫歷史。
每月查看 Dependency freshness、`gh pr list --repo SanHsien/human-writing` 與安全告警；發現 CP950 或規則回歸才跑對應測試及 Windows gate，其他文件只連結本路線圖。
