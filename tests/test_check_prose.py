from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "human-writing" / "scripts" / "check_prose.py"

sys.path.insert(0, str(CHECKER.parent))

import check_prose as prose  # noqa: E402


CLEAN_DRAFT = """
他毕业后离开上海，去了成都。那套量化程序已经跑过一段时间，他觉得可以全职试试。收入会不会稳定，当时没人知道。

第二天他把表格重算一次，数字比想象中更难看。他没有改口，只是把风险写进备忘录，然后继续跑。这不丢人。
""".strip()


def run_checker(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_han_count_counts_cjk() -> None:
    assert prose.han_count("他去了成都。") == 5
    assert prose.han_count("hello") == 0


def test_clean_draft_exits_zero(tmp_path: Path) -> None:
    draft = tmp_path / "clean.md"
    draft.write_text(CLEAN_DRAFT, encoding="utf-8")

    result = run_checker(draft)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "需要修改" not in result.stdout
    assert "不丢人" not in result.stdout


def test_hard_stop_fails(tmp_path: Path) -> None:
    draft = tmp_path / "stop.md"
    draft.write_text("说白了这件事没有那么复杂。他把报告交回去。", encoding="utf-8")

    result = run_checker(draft)

    assert result.returncode == 1
    assert "硬停词" in result.stdout
    assert "说白了" in result.stdout


def test_pivot_sentence_fails(tmp_path: Path) -> None:
    draft = tmp_path / "pivot.md"
    draft.write_text("这不是材料不足，而是你没有把事情讲清楚。", encoding="utf-8")

    result = run_checker(draft)

    assert result.returncode == 1
    assert "翻案" in result.stdout


def test_hard_jargon_fails(tmp_path: Path) -> None:
    draft = tmp_path / "jargon.md"
    draft.write_text("下一步要赋能整个内容团队，把流程跑顺。", encoding="utf-8")

    result = run_checker(draft)

    assert result.returncode == 1
    assert "黑话" in result.stdout
    assert "赋能" in result.stdout


def test_prompting_colon_fails_quoted_colon_warns(tmp_path: Path) -> None:
    draft = tmp_path / "colon.md"
    draft.write_text("核心是：把材料写清楚。他说：「今天先停。」", encoding="utf-8")

    result = run_checker(draft)

    assert result.returncode == 1
    assert "冒号" in result.stdout


def test_stdin_dash_reads_draft() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER), "-"],
        input=CLEAN_DRAFT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_file_exits_two() -> None:
    result = run_checker(ROOT / "does-not-exist.md")

    assert result.returncode == 2
    assert result.stderr


def test_mask_non_prose_keeps_newlines() -> None:
    text = "前面\n```python\nprint(1)\n```\n后面"
    masked = prose.mask_non_prose(text)
    assert masked.count("\n") == text.count("\n")
    assert "print" not in masked
