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

## 2026-08-22：上游 PR、issue、分支盤點

上游當時 **3 個 open PR、4 個 open issue、2 個分支**。沒有需要引用的項目；之後只看更大的編號。

| 項目 | 結論 | 理由 |
| --- | --- | --- |
| PR #1 `test: cover check_prose CLI behavior` | **不引用：本 fork 覆蓋更廣。** | 上游那份是 subprocess 層的四個案例，且斷言綁定簡體中文輸出字串（「未发现…」）。本 fork 的 `tests/test_check_prose.py` 已有 15 個案例，涵蓋 stdin、退出碼、遮罩、URL 冒號等它沒有的路徑，輸出也是繁中。引用會讓測試同時綁兩種語系的字面值。 |
| PR #5（README 提示詞批評）、PR #6（WorkBuddy 專家包，新增 `workbuddy/` 與建置腳本） | 不引用 | 見下方 2026-08-23 段落的逐項證據（此處原本只寫「產品方向」，已補實）。 |
| issue #2、#7、#8（功能與用法討論）、#3（英文版） | 不追 | 見下方 2026-08-23 段落；#8 已實查本 fork 規則確認有對應出口。 |

### 分支

已逐一與上游預設分支比對（不是只數數量）。**這一段當時的敘述有誤，已於 2026-08-23 更正**：
`feat/workbuddy-expert` 其實帶著 1 個獨佔 commit（`ea50a60`，即 PR #6 的 head）。結論（不引用）
未受影響，理由見下方同日段落。

### 水位
- PR：已看到 **#6**；issue：已看到 **#8**。記在 `tools/upstream_baseline.json`。

## 2026-08-23：重驗上一輪的結論，補上逐項證據

上一輪對 PR #5／#6 與四個 issue 只寫了「產品方向」「不追」。那不是理由，是分類——照那個寫法，
下一個人沒有辦法判斷結論還成不成立。今天逐項回頭看，結論不變，但理由換成可查證的東西：

| 項目 | 結論 | 逐項證據 |
| --- | --- | --- |
| PR #5「提示词这ai味太浓了」 | 不引用（**沒有可引用的東西**） | 該 PR 沒有 diff，內容是兩句意見（原文兩行，無檔案變動）。它是一則回饋，不是變更。 |
| PR #6 WorkBuddy 專家包 | 不引用（**新增平行封裝線，非缺陷修正**） | diff 為 `+468 −0`、七個新檔：`scripts/build_workbuddy_expert.py`（298 行打包腳本）、`workbuddy/.codebuddy-plugin/plugin.json`、`workbuddy/agents/human-writing.md`、一張 405 KB 的 `expert.png`。它把同一套規則打包成 CodeBuddy 平台的外掛，沒有修改 `human-writing/` 底下任何規則或 `check_prose.py`——亦即**不含本 fork 會受影響的行為變更**。本 fork 沒有 CodeBuddy 發佈線，引用等於維護一份不會被使用的打包產物。 |
| issue #8「一點心理描寫和神態描寫都沒有」 | 不追（**本 fork 已有對應出口**） | 這是唯一可能命中規則的一則。實查：`SKILL.md:132`、`references/reality.md:67`、`references/revision.md:60` 三處都寫明限制只針對**現實稿**（沒有來源的神態／天氣／對白是假細節），而虛構稿明文可以創造這些內容。上游同一份檔案的同一行也是這樣寫的（`git show upstream/main:human-writing/SKILL.md`），亦即這是使用者的用法問題，不是規則缺口。若日後上游真的改了那三行，會以 commit 進來，屆時照 commit 流程審。 |
| issue #2（產品案例寫作分支）、#3（英文版）、#7（README 是否用了本 skill） | 不追 | #2 與 #3 是功能請求，落地後會是 commit；#7 是提問。三則都沒有指出既有行為的缺陷。 |

### 分支：更正上一輪的說法

上一輪寫「沒有任何分支帶著獨佔 commit」。**那句話是錯的**：`feat/workbuddy-expert` 相對
`upstream/main` 有 1 個獨佔 commit（`ea50a60`）。當時的結論（不引用）沒有受影響——那條分支正是
PR #6 的 head，內容已在上表逐項看過——但敘述本身不準確，在此更正。今天複查：上游共 2 條分支，
只有這一條有獨佔 commit。

### 增量

`4fda173`（上一輪水位）到 `upstream/main` 之間 **0 個新 commit**；open PR 仍為 #1／#5／#6，
open issue 仍為 #2／#3／#7／#8，皆未超過水位。
