# Repository review（Windows-first）

- Review date: 2026-08-22
- Review baseline: 見本檔「已修」對應 commit；開放項已在 `fix/review-findings` 處理
- Upstream reviewed through: `4fda173f3fef7fb808f3eba991eeb2528ea4b189`
- Primary environment: Windows 11、PowerShell、Python 3.14.7（本機）、CI Windows 3.14 / Ubuntu 3.9–3.14
- Status: 維護骨架可用；產品規則未改；`check_prose.py` 僅有 UTF-8 stdio 的 fork 修正

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 裝「活人感寫作」Skill 的維護線。產品行為跟隨上游 1.1.0。檢查腳本只讀本機稿件、只報警、不改稿、不上傳。

2026-08-22 審查列出的 R-01～R-08，fork 能修的都修了。**沒有**把警告層升成硬失敗，也**沒有**放寬「不只……還……」正則，也**沒有**回貢上游。

交稿仍須讀 `check_prose.py` 的「需要修改」與「需要人工判斷」。exit 0 只代表沒有硬禁令。

## 已修 findings

| ID | 嚴重度 | Finding | 修復 |
|---|---|---|---|
| R-01 | P2 | Windows CP950 主控台印中文崩潰 | `check_prose.py` 重設 stdin／stdout／stderr 為 UTF-8；`test_checker_prints_on_cp950_stdio` 在 `PYTHONIOENCODING=cp950` 且無 `PYTHONUTF8` 時仍須印出「漢字數」 |
| R-02 | P2 | Skill 把變形翻案當禁令，腳本只警告 | 不改產品行為。`docs/DEVELOPMENT.md` 寫明結束碼契約；測試鎖「你以為……其實……」exit 0 +「需要人工判斷」 |
| R-03 | P2 | 「不只……還……」Skill 允許、正則仍警告 | 不放寬正則。測試鎖這條是警告不是失敗 |
| R-04 | P2 | 「不丟人」測試給假安全感 | `test_clean_draft` 改為：exit 0、無「需要修改」、允許「不丟」出現在「需要人工判斷」 |
| R-05 | P2 | 測試過窄 | 補破折號硬失敗、模型路標硬失敗、URL 冒號遮罩、變形翻案警告、CP950 stdio |
| R-06 | P3 | `.gitignore` 不擋稿件 | 加上 `drafts/`、`manuscripts/`、`*.draft.md` |
| R-07 | P3 | CI 沒跑 Python 3.14 | Ubuntu 矩陣加 3.14；Windows job 改 3.14 |
| R-08 | P3 | 連結檢查不涵蓋 Skill 路徑與封面圖 | `check_links.py` 核對 `SKILL.md` 反引號裝包路徑，以及 Markdown／HTML 圖片 |

## 本輪實證

本機修復後應再跑：

```text
pwsh -NoProfile -File tools\dev_check.ps1
```

預期：pytest 含 CP950 案全綠；`check_links.py` 輸出含 `human-writing\SKILL.md 裝包路徑`。

## 刻意不修

- 不把 `SEMANTIC_PIVOT_PATTERNS` 改成硬失敗。那是產品行為，本輪只文件化。
- 不放寬「不只……還……」正則。
- 不翻譯產品 `SKILL.md`／references／檢查器字串。
- 不開回貢 PR。

## 已檢查、不列為 finding

- 產品 Python 無 `os.system`、`shell=True`、`eval(`、`exec(`、`pickle`。
- URL／code fence 的冒號會被遮罩。
- 產品 `SKILL.md` 仍是寫作規格；`AGENTS.md` / `CLAUDE.md` 分開。
- Dependabot 不自動合併。
- 本 fork 無自己的 GitHub Release；產品版本仍是上游 `1.1.0`。

## 尚未宣稱範圍

- **沒有**用真實長稿做端到端寫作＋改稿。
- **沒有**驗證 ChatGPT／千問直接貼 `human-writing-lite.md` 的效果。
- **沒有**獨立評估檢查器對文學性中文的誤傷率。
- `dev_check.ps1` **不含** Bandit、CodeQL。
