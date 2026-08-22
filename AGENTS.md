# AGENTS.md

給 Codex、Claude Code、Cursor 與其他自動化代理在本專案工作時的指引。產品與使用方式先讀 [`README.md`](README.md)；開發與驗收細節見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 專案定位

這是 [`KKKKhazix/human-writing`](https://github.com/KKKKhazix/human-writing) 的 MIT fork。
核心價值是讓模型寫出來的中文讀起來像一個具體的人在說話：先檢驗材料夠不夠，再管推進與中文腔調，成稿用腳本攔住翻案腔、排比、借喻與模型黑話。

`origin` 是 `SanHsien/human-writing`，`upstream` 是原作者 repo，預設分支皆為 `main`。
保留上游作者、MIT 授權與產品 `human-writing/SKILL.md`。本 fork 的維護差異記在 [`FORK.md`](FORK.md) 與 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

主要開發與完整驗收環境是 **Windows 11 + PowerShell**；Ubuntu CI 補跨平台相容性。

## 硬性邊界

- **不要覆寫產品 `human-writing/SKILL.md`。** 那是給 Agent 安裝的寫作規格，不是本 fork 的維護索引。參考檔、檢查腳本與蒸餾版同樣以上游為準，除非有已記錄的 fork 修正。維護規則以本檔為準。
- 不要把產品 Skill、`references/`、`dist/` 或 `scripts/check_prose.py` 翻譯成繁體來「統一文件語言」。上游產品語言是簡體中文；本 fork 的繁中／英文只覆蓋公開入口與維護文件。
- 不提交使用者稿件、API key、cookie、帳號資料或私人寫作材料。
- 不推送到 `upstream`。上游同步先跑 `python tools/check_upstream_updates.py`，逐筆審查後再 merge / cherry-pick；不盲目覆蓋 fork 文件與 Windows gate。
- 不新增 hosted backend、不把檢查腳本改成自動改稿、不把本 Skill 擴成個人作者畫像或長期規則庫。

## 技術與資料流

- Python 3.9+；`human-writing/scripts/check_prose.py` 只使用標準庫。
- `human-writing/`：可安裝的 Skill 目錄（`SKILL.md`、references、dist、scripts）。
- `tools/`：fork 維護工具（上游檢查、Skill 規格驗證、相對連結檢查、Windows gate）。
- `tests/`：pytest。CI 另跑 ruff（E9+F）與 `validate_skill.py`。
- 檢查腳本只管已寫明的硬規則；警告項不能替作者決定文體。`check_prose.py` 結束碼 0 只代表沒有硬禁令，交稿仍須讀「需要人工判斷」。
- 已記錄的 fork 修正：`check_prose.py` 把 stdin／stdout／stderr 重設成 UTF-8，避免 Windows CP950 主控台崩潰。不要在同步上游時丟掉這段。

## 開發原則

- 一般修改使用 **branch → PR → CI → merge**，不要直接在 `main` 做正常維護。
- 修 bug 先補可重現失敗測試，再做最小修正。
- 上游公開安裝方式、`SKILL.md` 步驟與 `check_prose.py` 的硬禁令視為相容性契約。
- 不為了套格式而大改上游程式；Ruff 只閘 E9（語法）與 F（pyflakes）。
- 使用繁體中文回覆；使用者文件以繁中為主，公開入口同步維護 `README.en.md`。
- 上游更新簡體 `README.md` 時：把新內容翻進本 fork 的繁中 `README.md`，並同步 `README.en.md`。
- PR 標題建議 Conventional Commit；合併前先讀 `gh pr diff <編號>`。
- `REVIEW.md` 是風險快照，不是每個一般 bug 的流水帳。

## 上游處理

1. `git fetch upstream main`
2. `python tools/check_upstream_updates.py --strict`
3. 逐筆判斷是否與繁中 README、Windows gate 或測試衝突。
4. 可同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
5. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`
6. 採用／略過寫進 `docs/DECISIONS.md`，驗證後才推進 `tools/upstream_baseline.json`

Baseline 代表「已審查」，不代表「全部已合併」。

## 驗證

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

沒有實際跑過檢查腳本與 Windows gate，不要宣稱本機開發環境已可用。

## 文件責任

- `README.md` / `README.en.md`：公開產品與 fork 入口。
- `FORK.md`：與上游的關係、差異、同步方式。
- `NOTICE.md`：授權與 attribution。
- `docs/UPSTREAM.md`：upstream remote 與審查清冊。
- `docs/DEVELOPMENT.md`：本機開發與驗收指令。
- `docs/DECISIONS.md`：長期取捨。
- `CHANGELOG.md`：上游產品變更；不要為了 fork 文件手改它。
- `CONTRIBUTING.md` / `SECURITY.md`：本 fork 的貢獻與安全回報流程。
