# CLAUDE.md

請先完整閱讀並遵守 [`AGENTS.md`](AGENTS.md)。本檔只補充 Claude Code 的最小入口：

- 這是保留上游歷史的 fork；不要移除 `upstream`、原作者或 MIT 授權標示。
- `human-writing/SKILL.md` 是產品寫作規格，不要改寫成本 fork 的維護索引。
- 修改檢查腳本或硬禁令前，先跑對應 pytest；提交前跑
  `pwsh -NoProfile -File tools\dev_check.ps1`。
- 使用者稿件、本機輸出與憑證一律不可提交。
- 使用繁體中文，直接交付可驗證結果，避免冗長背景鋪陳。
