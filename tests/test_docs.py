from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402
import validate_skill  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "human-writing" / "SKILL.md"


def test_skill_frontmatter_is_installable() -> None:
    errors, _warns = validate_skill.audit(str(SKILL), lens="claude")
    assert errors == []


def test_skill_name_and_version_files() -> None:
    text = SKILL.read_text(encoding="utf-8")
    version = (ROOT / "human-writing" / "VERSION").read_text(encoding="utf-8").strip()

    assert "name: human-writing" in text
    assert version == "1.1.0"
    assert f"活人感写作 {version}" in text


def test_maintainer_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_skill_referenced_pack_paths_exist() -> None:
    problems = check_links.check_skill_paths()
    assert problems == []
    text = SKILL.read_text(encoding="utf-8")
    assert "references/forum-prose.md" in text
    assert "scripts/check_prose.py" in text


def test_readme_cover_image_exists() -> None:
    readme = ROOT / "README.md"
    problems = check_links.check_document(readme)
    assert problems == []
    assert (ROOT / "assets" / "readme-cover.svg").is_file()


def test_gitignore_covers_user_drafts() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "drafts/" in text
    assert "manuscripts/" in text
    assert "*.draft.md" in text


def test_skill_path_checker_flags_missing_reference(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("读取 `references/missing-file.md`。\n", encoding="utf-8")
    problems = check_links.check_skill_paths(skill)
    assert problems
    assert "references/missing-file.md" in problems[0]


def test_ci_covers_python_314() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert '"3.14"' in workflow
    assert "windows / py3.14" in workflow


