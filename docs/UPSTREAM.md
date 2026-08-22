# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/human-writing.git`
- 原作者：`upstream` → `https://github.com/KKKKhazix/human-writing.git`
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交。
有新提交或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確失敗。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案。
2. 判斷是否與繁中 README、Windows gate 或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 `docs/DECISIONS.md` 記錄採用／略過理由。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA。

Baseline 代表「已審查」，不代表「全部已合併」。

README 衝突的解法：上游新簡體內容翻進 `README.md`，並同步 `README.en.md`。

## 2026-08-22：fork 起點

本 fork 自上游 `main` `4fda173f3fef7fb808f3eba991eeb2528ea4b189`
（`docs: 重写 README，去掉产品说明书腔`）建立。此 SHA 設為第一個 `reviewed_through`。
之後的上游 commit 才需要進入審查清冊。
