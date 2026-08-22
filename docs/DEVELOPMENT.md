# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
材料（經歷、事實、數字、原話、虛構事件）
        │
        ▼
 human-writing/SKILL.md   材料門檻 → 現實／虛構分流 → 寫作 → 改稿
        │
        ▼
 成稿（Markdown / 純文字）
        │
        ▼
 human-writing/scripts/check_prose.py
        │
        ▼
 硬禁令清零才可交稿。警告項（「需要人工判斷」）exit 0，不能只看結束碼。
```

`human-writing/` 是要安裝到 Agent Skills 目錄的產品。根目錄其餘檔案是本 fork 的開發與治理骨架，不要一起複製進 `~/.agents/skills/`。

## 本機開發（Windows）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

手動抽查成稿：

```powershell
.venv\Scripts\python human-writing\scripts\check_prose.py 稿件.md
```

檢查器結束碼：

| 結束碼 | 含義 | 能不能交稿 |
|---|---|---|
| 0 | 沒有硬禁令。仍可能印出「需要人工判斷」 | 要讀完整輸出。變形翻案句、語境黑話、「不只……還……」只會警告 |
| 1 | 「需要修改」：硬停詞、硬翻案句、破折號、提示冒號、模型路標、硬黑話 | 不能交 |
| 2 | 讀檔失敗或沒有漢字 | 先修輸入 |

`SKILL.md` 把部分翻案腔變形寫成「絕對不能出現」，腳本目前只警告。本 fork 不自行把警告升成硬失敗。Agent 與維護者交稿時要看「需要修改」與「需要人工判斷」兩段，不能只看 exit 0。

## Canonical gate

`tools\dev_check.ps1` 會依序：

1. `python -m compileall`（`human-writing/scripts`、`tests`、`tools`）
2. `ruff check`（E9 + F）
3. `pytest tests/ -q`
4. `python tools/validate_skill.py human-writing/SKILL.md`
5. `python tools/check_links.py`

CI 在 Ubuntu 跑 3.9–3.14，並加一個 Windows Python 3.14 job 跑同一套 gate。推 `main` 前先跑本機 gate。

## 不要做的事

- 不要手改上游 `CHANGELOG.md` 來記錄 fork 文件。
- 不要把產品 `SKILL.md` 改寫成維護索引。
- 不要提交使用者稿件或檢查報告以外的私人寫作材料。
- 測試用的稿件必須是人造樣本，不能拿真實客戶文案。
