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
 硬禁令清零才可交稿；警告項留給人判斷
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

## Canonical gate

`tools\dev_check.ps1` 會依序：

1. `python -m compileall`（`human-writing/scripts`、`tests`、`tools`）
2. `ruff check`（E9 + F）
3. `pytest tests/ -q`
4. `python tools/validate_skill.py human-writing/SKILL.md`
5. `python tools/check_links.py`

PR CI 在 Ubuntu 跑 3.9–3.13，並加一個 Windows job 跑同一套 gate。

## 不要做的事

- 不要手改上游 `CHANGELOG.md` 來記錄 fork 文件。
- 不要把產品 `SKILL.md` 改寫成維護索引。
- 不要提交使用者稿件或檢查報告以外的私人寫作材料。
- 測試用的稿件必須是人造樣本，不能拿真實客戶文案。
