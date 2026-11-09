<p align="center">
  <img src="./assets/readme-cover.svg" alt="活人感寫作" width="100%">
</p>

<p align="center">
  <a href="README.md"><strong>繁體中文</strong></a> ·
  <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="https://github.com/SanHsien/human-writing/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/SanHsien/human-writing/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/KKKKhazix/human-writing/releases/tag/v1.2.0"><img alt="Version 1.2.0" src="https://img.shields.io/badge/version-1.2.0-C4473A?style=flat-square"></a>
  <a href="./LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-313131?style=flat-square"></a>
  <a href="https://github.com/KKKKhazix/human-writing/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/KKKKhazix/human-writing?style=flat-square&color=6B6258"></a>
</p>

<p align="center">
  <a href="#快速安裝">快速安裝</a> ·
  <a href="#它做什麼">寫作流程</a> ·
  <a href="#倉庫結構">倉庫結構</a> ·
  <a href="#開發">開發</a> ·
  <a href="https://github.com/KKKKhazix/human-writing/issues">產品問題</a>
</p>

> **這是 [`KKKKhazix/human-writing`](https://github.com/KKKKhazix/human-writing) 的 Windows-first 維護型 fork**，沿用 MIT License 與完整 Git 歷史。產品 Skill 跟隨上游；本維護線補上繁中入口、Windows 開發／驗收 gate，以及逐筆審查的上游追蹤。差異見 [`FORK.md`](FORK.md)，同步策略見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

> AI 寫的中文讀著挺順，讀完卻說不出是誰寫的。這個 Skill 想治的就是這個毛病。

裝上以後，模型寫知乎回答、公眾號文章、部落格、論壇長帖、人物故事、科普、評測、小說和口播稿，會先看手裡有沒有東西可寫，再像一個具體的人那樣把事講出來。這個人知道一些事，也有拿不準的地方，敢下判斷，偶爾岔開一句，還能把話接回來。

## 它做什麼

動筆之前，它先清點材料。

現實題材的材料不夠，它就去查。查不到就問你，一次最多問三個問題。你不讓問，它就把文章寫短，不拿車軲轆話湊字數，也不替你編一段沒發生過的親歷。虛構題材可以放開編人物和情節，每場戲仍然要有人想要點什麼，做了點什麼，戲演完以後有東西變了。

材料過關以後，寫的時候盯著三件事。

| 材料 | 推進 | 中文 |
| :--- | :--- | :--- |
| 現實稿核准事實、數字、引語和親歷，虛構稿檢查人物、行動和因果 | 每段都要帶來一件新東西，新事實、新動作都算，寫過的意思不換個說法再寫一遍 | 白話打底，在意詞序和停頓，清掉報告腔、模型腔和翻案腔 |

初稿寫完還有一道關。它會逐段看文章有沒有在原地轉圈，砍掉重複的解釋，調一調長短句，再清掉冒號、破折號、`不是……而是……` 這類翻案腔和常見的 AI 黑話。檢查腳本只管寫明了的硬規則，文風好不好它不管。

## 快速安裝

最省事的辦法，是把下面這句話發給你的 Agent。

```text
幫我安裝這個 skill：https://github.com/SanHsien/human-writing
```

Agent 會自己讀倉庫，找到 `human-writing` 資料夾裝好，裝完顯示名叫活人感寫作。Claude Code、Codex 和其他支援 Agent Skills 標準的工具都能這麼裝。若要安裝上游原版，把網址換成 `https://github.com/KKKKhazix/human-writing`。

Claude Code 也可以走外掛市場。

```text
/plugin marketplace add KKKKhazix/human-writing
/plugin install human-writing@human-writing
```

<details>
<summary><strong>手動安裝</strong></summary>

從上游 [Releases](https://github.com/KKKKhazix/human-writing/releases/latest) 下載 `human-writing-版本號.zip`，解壓後把整個 `human-writing` 資料夾放進 Skills 目錄，資料夾名別改。只複製 `SKILL.md` 不夠用，`references/` 和 `scripts/` 也得一起帶上。

```text
Claude Code   ~/.claude/skills/human-writing/
Codex         ~/.agents/skills/human-writing/
```

別的工具放進它自己的 Skills 目錄就行。

</details>

裝好以後照常提需求，寫東西、改稿、去 AI 味都會用上它。想點名用，就在需求裡寫上活人感寫作。

```text
用活人感寫作，把下面這些材料寫成一篇知乎回答。
```

聊天視窗裝不了 Skill，就用[蒸餾版](./human-writing/dist/human-writing-lite.md)。把它整段貼進去，跟在寫作需求後面。

## 1.2.0 改了什麼

這一版基本都在處理大家提的反饋，合進了 Shann5、qshanx 和 TZPlus 的 PR，謝謝他們。

- 寫小說時心理描寫被刪光的問題修了。改稿時刪的只是動作後面那句重複的情緒解釋，動作看不出來的心理照樣要寫。
- 檢查腳本會攔 `在当今……时代` 這種開頭、`让我们……吧` 這種結尾和 `不仅仅是……而是……`。誤判也少了好幾類，`10:30` 裡的冒號、Markdown 表格對齊語法、引號裡的人物對白都不再算違規。
- description 壓到兩百來字，寫明公文、合同、技術文檔、程式碼和翻譯不用它。
- 這份 README 照它自己的規則重寫了一遍。以前的版本被人在 Issue 裡說一股 AI 味，說得沒錯。

完整變更見 [CHANGELOG.md](./CHANGELOG.md)。

## 倉庫結構

<details>
<summary><strong>展開查看完整目錄</strong></summary>

```text
human-writing/
├── SKILL.md
├── VERSION
├── LICENSE
├── agents/
│   └── openai.yaml
├── dist/
│   └── human-writing-lite.md
├── references/
│   ├── forum-prose.md
│   ├── reality.md
│   ├── fiction.md
│   ├── formats.md
│   └── revision.md
└── scripts/
    └── check_prose.py
tests/
.claude-plugin/
└── marketplace.json
```

| 位置 | 做什麼的 |
| :--- | :--- |
| [`SKILL.md`](./human-writing/SKILL.md) | 入口。材料門檻、現實和虛構怎麼分、寫作流程、交稿前的禁令，都在這一份裡 |
| [`forum-prose.md`](./human-writing/references/forum-prose.md) | 知乎、公眾號、論壇長帖怎麼寫，節奏和措辭的具體做法 |
| [`reality.md`](./human-writing/references/reality.md) | 寫真人、歷史、新聞、數據和個人經歷時，事實的邊界在哪 |
| [`fiction.md`](./human-writing/references/fiction.md) | 小說、故事、虛構散文和對白的寫法 |
| [`formats.md`](./human-writing/references/formats.md) | 短內容、口播、演講、教程、評測這些特殊形式 |
| [`revision.md`](./human-writing/references/revision.md) | 初稿寫完以後一遍一遍怎麼改 |
| [`check_prose.py`](./human-writing/scripts/check_prose.py) | 查成稿有沒有踩到硬禁令 |
| [`human-writing-lite.md`](./human-writing/dist/human-writing-lite.md) | 蒸餾版，不到兩千字，給聊天視窗直接貼上 |
| [`tests/`](./tests) | 檢查腳本的測試 |

</details>

產品語言跟隨上游，仍是簡體中文。本 fork 另外加上維護骨架，包含 [`AGENTS.md`](AGENTS.md)、[`FORK.md`](FORK.md) 與 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 開發

Windows 11 + PowerShell 是主要開發與完整驗收環境。

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

改了檢查腳本，在倉庫根目錄跑一遍測試。Windows 跑 `pwsh -NoProfile -File tools\dev_check.ps1`，Linux 跑 `python -m pytest tests -q`。

每個 PR 上 CI 都會跑這些測試，再用 `check_prose.py` 把這份 README 查一遍。

細節見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。上游同步見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

## 回饋

MIT 協議開源。產品規則與工具沿用上游原作者的 MIT 內容；本 fork 未收錄第三方文章、訓練語料或模型權重。

產品規則、誤報或模型行為問題，請回報[上游 Issues](https://github.com/KKKKhazix/human-writing/issues)。若是 Windows 維護、CI 或 fork 文件問題，可直接提交 PR 到本 fork；附上可重現資訊會更容易判斷。

<p align="center">
  <sub>活人感寫作 · Human Writing · 1.2.0 · SanHsien maintenance fork</sub>
</p>
