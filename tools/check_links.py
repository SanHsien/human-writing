#!/usr/bin/env python3
"""檢查維護文件之間的相對連結，以及產品 Skill 點名的裝包路徑。

本 fork 的公開入口互相連來連去：README、FORK、NOTICE、AGENTS 與 docs。
文件被重新定位或改名時，這些連結會靜靜斷掉。只驗相對連結；外部網址交給人看。

另外核對 `human-writing/SKILL.md` 以反引號寫出的 `references/`、`scripts/` 等路徑，
以及 README 的 `<img src>`，避免裝包缺檔。

    python tools/check_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "human-writing" / "SKILL.md"
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_PATTERN = re.compile(r"""(?is)<img[^>]+src=["']([^"']+)["']""")
SKILL_PATH_PATTERN = re.compile(
    r"`((?:references|scripts|dist|agents)/[A-Za-z0-9._/-]+\.(?:md|py|ya?ml))(?:\s[^`]*)?`"
)
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")


SKIP_NAMES = {
    "upstream-review-report.md",
    "dependency-freshness-report.md",
}


def iter_documents() -> list[Path]:
    documents = []
    documents.extend(ROOT.glob("*.md"))
    documents.extend((ROOT / "docs").glob("*.md"))
    github = ROOT / ".github"
    if github.is_dir():
        documents.extend(github.rglob("*.md"))
    return sorted(
        path
        for path in documents
        if path.is_file() and path.name not in SKIP_NAMES
    )


def _missing_relative(path: Path, target: str) -> str | None:
    target = target.strip().strip("<>")
    if not target or target.startswith(SKIP_PREFIXES):
        return None
    file_part = unquote(target.split("#", 1)[0])
    if not file_part:
        return None
    resolved = (path.parent / file_part).resolve()
    if resolved.exists():
        return None
    try:
        shown = resolved.relative_to(ROOT)
    except ValueError:
        shown = resolved
    return f"{target} → 找不到 {shown}"


def check_document(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    for pattern in (LINK_PATTERN, IMAGE_PATTERN, HTML_SRC_PATTERN):
        for match in pattern.finditer(text):
            missing = _missing_relative(path, match.group(1))
            if missing:
                problems.append(missing)
    return problems


def check_skill_paths(skill_path: Path = SKILL) -> list[str]:
    if not skill_path.is_file():
        return [f"找不到 {skill_path}"]
    text = skill_path.read_text(encoding="utf-8")
    problems: list[str] = []
    seen: set[str] = set()
    for match in SKILL_PATH_PATTERN.finditer(text):
        relative = match.group(1)
        if relative in seen:
            continue
        seen.add(relative)
        resolved = skill_path.parent / relative
        if not resolved.exists():
            try:
                shown = resolved.resolve().relative_to(ROOT)
            except ValueError:
                shown = resolved
            problems.append(f"`{relative}` → 找不到 {shown}")
    if not seen:
        problems.append("SKILL.md 沒有點到 references/ 或 scripts/ 路徑")
    return problems


def main() -> int:
    documents = iter_documents()
    if not documents:
        print("找不到任何維護用 Markdown 檔")
        return 1

    failures = 0
    for path in documents:
        problems = check_document(path)
        rel = path.relative_to(ROOT)
        if problems:
            failures += 1
            for problem in problems:
                print(f"FAIL {rel}: {problem}")
        else:
            print(f"OK   {rel}")

    skill_problems = check_skill_paths()
    skill_rel = SKILL.relative_to(ROOT)
    if skill_problems:
        failures += 1
        for problem in skill_problems:
            print(f"FAIL {skill_rel}: {problem}")
    else:
        print(f"OK   {skill_rel} 裝包路徑")

    print(f"\n共 {len(documents)} 份維護文件 + SKILL 裝包路徑，{failures} 份有缺檔。")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
