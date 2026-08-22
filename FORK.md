# Fork 維護說明

本 repo fork 自 [`KKKKhazix/human-writing`](https://github.com/KKKKhazix/human-writing)，
沿用 MIT License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留原作者持續更新的寫作規則、檢查腳本與蒸餾版提示詞。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口改以繁體中文為主，英文鏡像放 `README.en.md`。
- 建立可重現的 Windows 開發 gate、Windows CI job，以及逐筆審查的上游追蹤。
- 產品 Skill 仍可直接安裝到 `~/.agents/skills/human-writing/`。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；英文鏡像在 `README.en.md` |
| `AGENTS.md` / `CLAUDE.md` | 本 fork 的 AI 維護單一真相源 |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate |
| `human-writing/scripts/check_prose.py` | 唯一產品程式修正：stdio 重設為 UTF-8，避免 Windows CP950 崩潰 |
| `.github/workflows/ci.yml` | Ubuntu 3.9–3.14 + Windows Python 3.14：pytest / ruff / Skill 驗證 / 連結與裝包路徑檢查 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit 檢查 |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |

產品 `human-writing/SKILL.md`、`references/`、`dist/` 以上游為準。`scripts/check_prose.py` 僅允許已記錄的 UTF-8 stdio 修正，其餘行為跟隨上游。

## 分支與 remote

- `origin/main`：SanHsien 維護線。
- `upstream/main`：KKKKhazix 原始專案。
- 功能與修正使用短期分支；驗證通過後再合併到 `main`。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

上游更新簡體 `README.md` 時，把新內容翻進本 fork 的繁中 `README.md`，並同步 `README.en.md`。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/human-writing.git
cd human-writing
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

只想安裝 Skill、不開發時：

```text
把 human-writing/ 資料夾完整複製到 ~/.agents/skills/human-writing/
```
