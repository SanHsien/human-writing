# 維護決策

## 2026-08-22：建立 Windows-first 維護型 fork

**決定**：fork `KKKKhazix/human-writing`，保留 MIT 授權與完整歷史，預設分支維持 `main` 以降低與上游同步摩擦。本線聚焦繁中公開入口、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：上游 Skill、材料門檻與 `check_prose.py` 已經可用，且檢查完全在本機執行，符合主人用 AI 協作中文寫作、又不要空話灌水的需求。缺的是 Windows 11 上可重現的開發／驗收骨架，以及繁中入口。直接用上游 repo 難以長期記錄 fork 取捨。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- `human-writing/SKILL.md` 保持產品規格，不用維護索引覆寫。
- 不把產品規則翻譯成繁體；產品語言跟隨上游。
- 上游更新必須逐筆審查。

## 2026-08-22：不啟用 Dependabot 自動合併

**決定**：Dependabot 只開 PR；CI 與人工讀 diff 通過後才合併。

**理由**：開發依賴只有 pytest / ruff，體積小，但自動合併仍會跳過「讀 diff」這一步。
