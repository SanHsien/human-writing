# Project Review 2026-08-22

## 結論

`SanHsien/human-writing` 已從上游 `KKKKhazix/human-writing` fork，並補上與其他維護型 fork 相同的開發環境與治理檔。產品 `human-writing/SKILL.md`、references 與 `check_prose.py` 未改寫。

本機 Windows 11 gate 通過：**18 passed**。Upstream baseline 對齊 fork 起點，沒有未審查的上游 commit。

這是維護骨架落地，**不是**寫作規則改寫。發行仍以上游 tag `v1.1.0` 為準，直到有 fork-only 修正需要獨立版本。

## 本輪實證

- Fork：`https://github.com/SanHsien/human-writing`，`origin/main` 追上游 `4fda173f3fef7fb808f3eba991eeb2528ea4b189`。
- `pwsh -NoProfile -File tools\dev_check.ps1`：**WINDOWS DEV CHECK GREEN**
  - compileall 通過
  - ruff E9+F：All checks passed
  - pytest：18 passed
  - `tools/validate_skill.py human-writing/SKILL.md`：無 Claude Code-breaking issues（0 warning）
  - `tools/check_links.py`：16 份維護文件，0 斷連結
- `python tools/check_upstream_updates.py`：No new upstream commits.

## 本輪落地

| 項目 | 狀態 |
| --- | --- |
| 繁中 `README.md` + 英文 `README.en.md` | 完成 |
| `AGENTS.md` / `CLAUDE.md` / `FORK.md` / `NOTICE.md` | 完成 |
| `docs/DECISIONS.md` / `UPSTREAM.md` / `DEVELOPMENT.md` | 完成 |
| Windows gate `tools/dev_check.ps1` + CI Windows job | 完成 |
| `upstream-check` + CodeQL + Dependabot | 完成 |
| 產品 `human-writing/SKILL.md` | 保留上游原文 |

## 尚未通過 / 後續

- 本 fork 尚無自己的 GitHub Release；安裝 Skill 仍複製 `human-writing/` 目錄，或叫 Agent 安裝本 fork URL。
- 產品規則、references 與檢查腳本維持上游簡體中文，不在本輪翻譯。
