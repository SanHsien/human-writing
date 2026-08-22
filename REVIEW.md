# Repository review（Windows-first）

- Review date: 2026-08-22
- Review baseline: `9e2cd496360e94a3e6edfe3b3ce083253b10b498`
- Upstream reviewed through: `4fda173f3fef7fb808f3eba991eeb2528ea4b189`
- Primary environment: Windows 11、PowerShell、Python 3.14.7（本機）、CI Windows 3.12 / Ubuntu 3.9–3.13
- Status: 維護骨架可用；產品 Skill／檢查腳本未改寫；官方仍是上游 `KKKKhazix/human-writing`

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 裝「活人感寫作」Skill 的維護線。產品行為跟隨上游 1.1.0：材料門檻、翻案腔、排比、借喻、黑話。檢查腳本只讀本機稿件、只報警、不改稿、不上傳。Bandit High／Medium 為 0。本機 gate 與 GitHub Actions 在 `9e2cd49` 全綠。

現階段的主要風險不是「會不會外連」，而是：

1. 產品檢查器在 Windows 預設 CP950 主控台會 `UnicodeEncodeError` 直接崩潰。本 fork 自稱 Windows-first，但 `check_prose.py` 仍是上游原樣。
2. Skill 寫「命中翻案腔就不能交稿」，腳本把變形翻案句只當警告（exit 0）。Agent 若只看 exit code，會把仍該改的稿交出去。
3. 測試是煙霧測試，沒鎖警告層、編碼、排比與「不只……還……」的契約。

不把 fork 當成第二個官方產品 repo。寫作規則、蒸餾版與 `check_prose.py` 的版權與行為仍屬上游。

## 本輪實證

### 本機

```text
pwsh -NoProfile -File tools\dev_check.ps1
→ compileall / ruff E9+F / pytest / validate_skill / check_links 全綠
→ 18 passed
→ SKILL.md：無 Claude Code-breaking issues（0 warning）
→ check_links：16 份維護文件，0 斷連結

python -m bandit -q -r human-writing/scripts tools --severity-level high --confidence-level medium
→ exit 0（High = 0）

python -m bandit -q -r human-writing/scripts tools -ll
→ exit 0（Medium+ = 0）

python tools/check_upstream_updates.py
→ No new upstream commits.
```

抽查 `human-writing/scripts/check_prose.py`（設 `PYTHONUTF8=1`）：

| 樣本 | exit | 觀察 |
|---|---|---|
| 「這不丟人。……」 | 0 | 不是硬停詞；警告「需辨語境詞：不丟」 |
| 「他不只把表格重算一次，還把風險寫進備忘錄。」 | 0 | 警告「疑似翻案腔變形」 |
| 「你以為材料夠了，其實還差得很遠。」 | 0 | 警告「疑似翻案腔變形」 |
| 「他走了——再也沒回來。」 | 1 | 硬失敗：破折號 2 處 |
| 「詳見 https://example.com/a:b 這一頁。」 | 0 | URL 冒號被 `mask_non_prose` 遮掉 |

未設 `PYTHONUTF8`、主控台為 CP950 時，對 UTF-8 稿件跑檢查器：讀檔成功，列印「漢字數」時 `UnicodeEncodeError`，行程以未捕捉例外結束。

### GitHub Actions（`9e2cd49` push）

| Workflow | 結果 | 說明 |
|---|---|---|
| [CI](https://github.com/SanHsien/human-writing/actions/runs/32553169289) | success | Ubuntu 3.9–3.13、Windows py3.12 |
| [CodeQL](https://github.com/SanHsien/human-writing/actions/runs/32553169279) | success | Python `security-extended` |
| [Upstream check](https://github.com/SanHsien/human-writing/actions/runs/32553169340) | success | 無未審查上游 commit |

`git ls-files` 46 檔。無 `.env`、金鑰、稿件。`origin` / `upstream` remote 正確。產品樹含 `human-writing/dist/human-writing-lite.md`。

## 開放 findings

| ID | 嚴重度 | Finding | 證據 | 建議 |
|---|---|---|---|---|
| R-01 | P2 | `check_prose.py` 在 Windows CP950 主控台印中文會崩潰。本 fork 的 Windows gate 靠 `PYTHONUTF8=1` 遮住，一般使用者直接 `python human-writing\scripts\check_prose.py 稿.md` 會炸。 | 本機實測：`print(f"汉字数 {total_han}")` → `UnicodeEncodeError: 'cp950' codec can't encode character '\u6c49'`；`tools/validate_skill.py` 已對 stdout `reconfigure(encoding="utf-8")` | 給檢查器加上與 `validate_skill.py` 相同的 UTF-8 重設，並補一條「無 PYTHONUTF8 仍能印出結果」的測試。可回貢上游。 |
| R-02 | P2 | `SKILL.md` 把翻案腔變形列成「成稿絕對不能出現」；腳本把 `SEMANTIC_PIVOT_PATTERNS` 只寫進警告，exit 0。只看 exit code 的 Agent 會交仍該改的稿。 | `human-writing/SKILL.md`「命中一項就不能交稿」+「你以為……其實……」；`check_prose.py` 490–494 行 `warnings.append`；抽查「你以為材料夠了，其實……」exit 0 | 維持現況就在 `docs/DEVELOPMENT.md` 寫明：交稿要看「需要修改」與「需要人工判斷」兩段，不能只看 exit code。若要跟 Skill 對齊，變形翻案句改硬失敗（那是產品變更，先回報上游）。 |
| R-03 | P2 | Skill 寫「不只……還……」是正常遞進，可以用；正則 `不只(?:是)?[^。！？\n]{0,90}(?:还|也)` 對普通遞進也警告。 | 抽查「他不只把表格重算一次，還把風險寫進備忘錄。」exit 0，仍報「疑似翻案腔變形」 | 上游問題。本線不要自行放寬正則，除非有誤報樣本要回貢。測試應鎖這條是警告、不是失敗。 |
| R-04 | P2 | Changelog 說「不丟人」不再觸發硬停詞，屬實；`CONTEXT_JARGON` 的「不丟」仍當子字串打中「不丟人」。`test_clean_draft` 只 assert stdout 不含「不丟人」，警告詞是「不丟」，測試給假安全感。 | 抽查警告「第 1 行出現 不丟」；`tests/test_check_prose.py` 37–45 行 | 測試改成：exit 0、無「需要修改」、允許「不丟」出現在「需要人工判斷」。不要宣稱「不丟人」完全豁免。 |
| R-05 | P2 | 18 個測試只覆蓋硬停詞、翻案硬句、黑話、提示冒號、stdin、缺檔、遮罩換行。沒有：破折號、模型路標、三連排比、名詞化、抒情詞、句長 CV、連詞密度、CP950。 | `tests/test_check_prose.py` | 先補 R-01 編碼與破折號硬失敗；警告層用「exit 0 + 需要人工判斷」鎖契約，不要為了綠燈把警告改成失敗。 |
| R-06 | P3 | `.gitignore` 不擋使用者稿件。有人把 `draft.md` 丟進工作樹，policy 擋不住。 | `.gitignore` 只有 venv、快取、`.env`、產生報告 | 可加 `drafts/`、`manuscripts/`、`*.draft.md`。提交前仍要人工看。 |
| R-07 | P3 | CI 矩陣到 Python 3.13；本機是 3.14.7。3.14 本機 18 passed，但 Ubuntu job 沒跑 3.14。 | `.github/workflows/ci.yml`；`python --version` → 3.14.7 | 下次改 CI 時把 Windows 或 Ubuntu 一格升到 3.14。非阻斷。 |
| R-08 | P3 | `check_links.py` 只掃根目錄／`docs/`／`.github` 的 Markdown 連結，不掃 `human-writing/SKILL.md` 裡的反引號路徑，也不掃 README 的 `<img src>`。 | `tools/check_links.py`；產品檔用 `` `references/forum-prose.md` `` | 現況可接受。若要防裝包缺檔，改驗證 `SKILL.md` 點名的相對路徑存在。 |

## 已檢查、不列為 finding

- 產品 Python 無 `os.system`、`shell=True`、`eval(`、`exec(`、`pickle`。唯一 `subprocess.run` 在維護工具 `tools/check_upstream_updates.py`，argv 列表呼叫 `git`。
- `check_prose.py` 只讀使用者指定檔或 stdin，標準庫，不上網。
- URL／code fence／inline code 的冒號會被遮罩；抽查 `https://example.com/a:b` 通過。
- 破折號 `——` 以兩個 `—` 計，硬失敗，與 Skill 一致。
- 產品 `SKILL.md` 仍是寫作規格；`AGENTS.md` / `CLAUDE.md` 分開且禁止覆寫。產品語言維持簡體。
- 繁中／英文 README 的安裝 URL、CI badge、fork 橫幅一致，都指向 `SanHsien/human-writing`，Release badge 仍指向上游 tag（本 fork 無自己的 Release，正確）。
- `NOTICE.md` 保留上游 MIT 與 `Copyright (c) 2026 Human Writing Skill contributors`。
- Dependabot 不自動合併（`docs/DECISIONS.md`），合理。開發依賴只有 pytest / ruff。
- CodeQL action 已 pin SHA，與 CI checkout / setup-python 一致。
- `human-writing/dist/human-writing-lite.md`、五份 references、`agents/openai.yaml`、`VERSION=1.1.0` 都在 git 裡。

## 尚未宣稱範圍

- **沒有**用真實長稿（知乎／公眾號／小說）做端到端寫作＋改稿；閘門是單元煙霧測試 + Skill frontmatter 驗證。
- **沒有**在未設 `PYTHONUTF8` 的互動 PowerShell 裡，證明檢查器對使用者是可用的。反證是 CP950 崩潰。
- **沒有**驗證 ChatGPT／千問直接貼 `human-writing-lite.md` 的效果。
- **沒有**獨立評估檢查器對文學性中文的誤傷率；R-03／R-04 只是最小樣本。
- `dev_check.ps1` **不含** Bandit、CodeQL。那些只在本機抽查／GitHub。
- **不宣稱** fork 有自己的 GitHub Release 或獨立版號；產品版本仍是上游 `1.1.0`。
- **不宣稱** 已把產品規則翻成繁體。那是刻意不做。

## 建議下一步（未動手）

1. `check_prose.py` 加上 UTF-8 stdout／stderr 重設（R-01），測試在 `PYTHONUTF8` 關掉時仍能印中文。這是唯一值得本 fork 先做、再考慮回貢的 Windows bug。
2. 文件寫明：交稿看「需要修改」與「需要人工判斷」，exit 0 不是「沒問題」（R-02）。
3. 補破折號硬失敗測試，並修正「不丟人」測試的斷言（R-04、R-05）。
4. 使用者稿件目錄加入 `.gitignore`（R-06）。
