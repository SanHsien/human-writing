# 貢獻指南

## 開始前

1. 先讀 [`AGENTS.md`](AGENTS.md)、[`FORK.md`](FORK.md) 與 [`README.md`](README.md)。
2. 確認問題在最新 `main` 仍可重現，並查過既有 Issues。
3. 產品規則的實質變更，優先考慮回報或回貢 [`KKKKhazix/human-writing`](https://github.com/KKKKhazix/human-writing)。
4. 不要附上私人稿件、客戶文案或任何憑證。

## 本機開發

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

## Pull Request

- 一個 PR 聚焦一個問題。
- Bug 修正先附失敗測試；新行為需涵蓋成功、邊界與錯誤路徑。
- 修改使用方式時同步更新 `README.md` 與 `README.en.md`。
- 說明是否來自 upstream、是否改動產品 `SKILL.md`／`check_prose.py`，以及實際跑過哪些指令。
- 提交訊息建議使用 `fix:`、`feat:`、`docs:`、`test:`、`chore:`。
