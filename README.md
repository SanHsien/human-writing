<p align="center">
  <img src="./assets/readme-cover.svg" alt="活人感寫作" width="100%">
</p>

<p align="center">
  <a href="README.md"><strong>繁體中文</strong></a> ·
  <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="https://github.com/SanHsien/human-writing/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/SanHsien/human-writing/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/KKKKhazix/human-writing/releases/tag/v1.1.0"><img alt="Version 1.1.0" src="https://img.shields.io/badge/version-1.1.0-C4473A?style=flat-square"></a>
  <a href="./LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-313131?style=flat-square"></a>
  <a href="https://github.com/KKKKhazix/human-writing/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/KKKKhazix/human-writing?style=flat-square&color=6B6258"></a>
</p>

<p align="center">
  <a href="#快速安裝">快速安裝</a> ·
  <a href="#它做什麼">寫作流程</a> ·
  <a href="#倉庫結構">倉庫結構</a> ·
  <a href="#開發">開發</a> ·
  <a href="https://github.com/SanHsien/human-writing/issues">提交問題</a>
</p>

> **這是 [`KKKKhazix/human-writing`](https://github.com/KKKKhazix/human-writing) 的 Windows-first 維護型 fork**，沿用 MIT License 與完整 Git 歷史。產品 Skill 跟隨上游；本維護線補上繁中入口、Windows 開發／驗收 gate，以及逐筆審查的上游追蹤。差異見 [`FORK.md`](FORK.md)，同步策略見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

> AI 寫中文有個通病：讀完覺得挺流暢，但說不出是誰寫的。活人感寫作想治的就是這件事。

讓模型寫出來的文章讀起來像一個具體的人在說話——知道一些事，有判斷，偶爾岔開一句，還能接回來。適用於知乎回答、公眾號文章、部落格、論壇帖、人物故事、科普、評測、小說、口播等大多數中文寫作場景。

## 它做什麼

寫作之前先解決一個前置問題：你手上有沒有東西可寫。

現實題材，材料不夠就去查，查不到就追問或者縮短篇幅，絕不拿車轱轆話湊字數。虛構題材可以自由創造人物和情節，但每個場景仍然要有目標、有動作、有變化。

材料過關之後管三件事：

| 材料 | 推進 | 中文 |
| :--- | :--- | :--- |
| 現實寫作核准事實、數字、引語和親歷。虛構寫作檢查人物、行動與因果。 | 每段都要帶來新東西——新事實、新動作、新例子或新後果。寫過的不重複。 | 白話打底，在意詞序和停頓，清掉報告腔、模型腔和翻案句。 |

初稿寫完還有一道關。Skill 會逐段檢查有沒有在原地轉圈，砍掉重複解釋，調整長短句節奏，攔住冒號濫用、破折號、「不是……而是……」之類的翻案腔和常見 AI 黑話。檢查腳本只管已經寫明的硬規則，不替你決定風格。

## 快速安裝

把下面這句話發給你的 Agent。

```text
幫我安裝這個 skill：https://github.com/SanHsien/human-writing
```

Agent 會讀取倉庫、找到 `human-writing`，完成安裝。裝好之後顯示名為「活人感寫作」。

若要安裝上游原版，把網址換成 [`KKKKhazix/human-writing`](https://github.com/KKKKhazix/human-writing)。

<details>
<summary><strong>Agent 不支援直接安裝時</strong></summary>

從上游 [Releases](https://github.com/KKKKhazix/human-writing/releases/latest) 下載，或者把倉庫裡的 [`human-writing`](./human-writing) 資料夾完整複製到本機 Skills 目錄。資料夾名保留 `human-writing`。

```text
~/.agents/skills/human-writing/
```

</details>

裝好之後這樣用：

```text
使用 $human-writing，把我的材料寫成一篇有活人感和中文韻律的作品。
```

## 1.1.0 改了什麼

1.0 用字串禁令攔 AI 味——禁「不是……而是……」、禁冒號、禁一批黑話。有效，但模型會換一套字面繼續做同樣的事。「你以為……其實……」「回頭才發現」和「不是A而是B」是同一個姿勢，讀者認的是姿勢，不是字。

1.1 把防線從字面挪到動作：禁的是「先給讀者立一個他沒有的誤解，再推翻它」這件事本身，不管穿什麼外衣。檢測腳本也跟著升級，補了變形翻案句、AI 排比、抒情借喻的警告層，加了句長變異係數和連詞密度的統計檢查，同時把「不丟人」「打法」這類正常中文從誤傷名單裡撈出來。另外出了一個兩千字的蒸餾版，ChatGPT、千問這類聊天視窗直接貼上就能用。

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
```

| 位置 | 做什麼的 |
| :--- | :--- |
| [`SKILL.md`](./human-writing/SKILL.md) | 入口。材料門檻、現實與虛構分流、寫作流程、交付禁令，全在這一份裡 |
| [`forum-prose.md`](./human-writing/references/forum-prose.md) | 知乎、公眾號、論壇長帖的寫法，節奏和措辭的具體做法都在這裡 |
| [`reality.md`](./human-writing/references/reality.md) | 真人、歷史、新聞、數據和個人經歷的事實邊界 |
| [`fiction.md`](./human-writing/references/fiction.md) | 小說、故事、虛構散文和對白的創作規則 |
| [`formats.md`](./human-writing/references/formats.md) | 短內容、口播、演講、教程、評測等特殊形式 |
| [`revision.md`](./human-writing/references/revision.md) | 初稿寫完之後怎麼改——逐遍檢查清單 |
| [`check_prose.py`](./human-writing/scripts/check_prose.py) | 檢查成稿有沒有踩到硬禁令 |
| [`human-writing-lite.md`](./human-writing/dist/human-writing-lite.md) | 蒸餾版，兩千字以內，聊天視窗直接貼上用 |

</details>

產品語言跟隨上游，仍是簡體中文。本 fork 另外加上維護骨架：[`AGENTS.md`](AGENTS.md)、[`FORK.md`](FORK.md)、[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 開發

Windows 11 + PowerShell 是主要開發與完整驗收環境。

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

細節見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。上游同步見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

## 回饋

MIT 協議開源。倉庫只有原創規則和工具，沒有第三方文章、訓練語料或模型權重。

碰到規則衝突、誤報或者某個模型上表現不對，歡迎在本 fork [提 Issue](https://github.com/SanHsien/human-writing/issues)，或回報給[上游](https://github.com/KKKKhazix/human-writing/issues)。附上你的提示詞、模型輸出片段和你覺得應該是什麼樣，排查起來快很多。

<p align="center">
  <sub>活人感寫作 · Human Writing · 1.1.0 · SanHsien maintenance fork</sub>
</p>
