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




def _linked_doc(tmp_path: Path, monkeypatch, body: str) -> Path:
    (tmp_path / "a.md").write_text("x", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text(body, encoding="utf-8")
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    return doc


def test_link_title_is_not_part_of_the_target(tmp_path: Path, monkeypatch) -> None:
    """`[t](a.md "title")` is valid Markdown; a.md exists, so it must not fail."""
    doc = _linked_doc(tmp_path, monkeypatch, '[t](a.md "title") [u](a.md \'t\')\n')
    assert check_links.check_document(doc) == []


def test_link_query_string_is_not_part_of_the_target(tmp_path: Path, monkeypatch) -> None:
    doc = _linked_doc(tmp_path, monkeypatch, "[t](a.md?plain=1)\n")
    assert check_links.check_document(doc) == []


def test_links_inside_code_are_examples_not_links(tmp_path: Path, monkeypatch) -> None:
    body = ("```md" + chr(10) + "[x](nope.md)" + chr(10) + "```" + chr(10) * 2
            + "`[y](nope2.md)`" + chr(10) * 2
            + "~~~" + chr(10) + "[z](nope3.md)" + chr(10) + "~~~" + chr(10))
    doc = _linked_doc(tmp_path, monkeypatch, body)
    assert check_links.check_document(doc) == []


def test_missing_link_with_title_is_still_reported(tmp_path: Path, monkeypatch) -> None:
    doc = _linked_doc(tmp_path, monkeypatch, '[t](gone.md "title")\n')
    problems = check_links.check_document(doc)
    assert len(problems) == 1 and "gone.md" in problems[0]


def _audit_text(tmp_path: Path, frontmatter: str, body: str = "body\n"):
    path = tmp_path / "SKILL.md"
    path.write_text("---\n" + frontmatter + "---\n" + body, encoding="utf-8")
    return validate_skill.audit(str(path), lens="claude")


def test_comma_separated_allowed_tools_are_recognised(tmp_path: Path) -> None:
    """`allowed-tools: Bash, Read` grants Bash; it is not an unknown tool 'Bash,'."""
    errors, warns = _audit_text(
        tmp_path,
        "name: x\ndescription: d\nallowed-tools: Bash, Read\n",
        "```bash\nls\n```\n",
    )
    assert errors == []
    assert warns == []


def test_scoped_bash_grant_with_space_stays_one_tool(tmp_path: Path) -> None:
    errors, warns = _audit_text(
        tmp_path, "name: x\ndescription: d\nallowed-tools: Bash(python3 *) Read\n"
    )
    assert errors == []
    assert warns == []


def test_folded_description_length_is_checked(tmp_path: Path) -> None:
    errors, _warns = _audit_text(
        tmp_path, "name: x\ndescription: >\n  " + "a" * 1100 + "\n"
    )
    assert any("1024" in item for item in errors)
