from ch98_linter.ch_move_single_script import (
    change_ai_summary_md,
    create_ai_summary_path,
    replace_string_in_csv,
    replace_valid_ch,
)
from copy import deepcopy as copy_deepcopy
from pathlib import Path


def test_replace_valid_ch_ReplacesValue_Scenario0_ExactMatch():
    # ESTABLISH
    data = {
        "Example": {"valid_ch": "19"},
        "Other": {"valid_ch": "13:"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["Example"]["valid_ch"] == "23"
    assert result["Other"]["valid_ch"] == "13:"


def test_replace_valid_ch_DoesNotReplace_Scenario1_PartialMatch():
    # ESTABLISH
    data = {
        "Example": {"valid_ch": "19:"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["Example"]["valid_ch"] == "23:"


def test_replace_valid_ch_ReplacesMultiple_Scenario2_MultipleExactMatches():
    # ESTABLISH
    data = {
        "A": {"valid_ch": "19"},
        "B": {"valid_ch": "19"},
        "C": {"valid_ch": "20"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["A"]["valid_ch"] == "23"
    assert result["B"]["valid_ch"] == "23"
    assert result["C"]["valid_ch"] == "20"


def test_replace_valid_ch_DoesNothing_Scenario3_NoMatches():
    # ESTABLISH
    data = {
        "A": {"valid_ch": "11"},
        "B": {"valid_ch": "12"},
    }

    original_data = copy_deepcopy(data)

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result == original_data


def test_replace_valid_ch_SkipsMissingValidCh_Scenario4_KeyMissing():
    # ESTABLISH
    data = {
        "A": {"semantic_type": "str"},
        "B": {"valid_ch": "19"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result["A"] == {"semantic_type": "str"}
    assert result["B"]["valid_ch"] == "23"


def test_replace_valid_ch_ReturnsSameObject_Scenario5_MutatesInput():
    # ESTABLISH
    data = {
        "A": {"valid_ch": "19"},
    }

    # WHEN
    result = replace_valid_ch(data, 19, 23)

    # THEN
    assert result is data


def test_replace_string_in_csv_ReplacesString_Scenario0_SingleMatch(
    tmp_path,
):
    # ESTABLISH
    csv_file_path = tmp_path / "test.csv"
    csv_file_path.write_text("name,age\nSue,19\nBob,20\n", encoding="utf-8")

    # WHEN
    replace_string_in_csv(csv_file_path, "19", "23")

    # THEN
    result = csv_file_path.read_text(encoding="utf-8")

    assert result == "name,age\nSue,23\nBob,20\n"


def test_replace_string_in_csv_ReplacesMultiple_Scenario1_MultipleMatches(
    tmp_path,
):
    # ESTABLISH
    csv_file_path = tmp_path / "test.csv"
    csv_file_path.write_text("19,19,19\n", encoding="utf-8")

    # WHEN
    replace_string_in_csv(csv_file_path, "19", "23")

    # THEN
    result = csv_file_path.read_text(encoding="utf-8")

    assert result == "23,23,23\n"


def test_replace_string_in_csv_DoesNothing_Scenario2_NoMatches(
    tmp_path,
):
    # ESTABLISH
    csv_file_path = tmp_path / "test.csv"
    original_text = "a,b,c\n1,2,3\n"

    csv_file_path.write_text(original_text, encoding="utf-8")

    # WHEN
    replace_string_in_csv(csv_file_path, "19", "23")

    # THEN
    result = csv_file_path.read_text(encoding="utf-8")

    assert result == original_text


def test_replace_string_in_csv_ReplacesPartialText_Scenario3_SubstringMatch(
    tmp_path,
):
    # ESTABLISH
    csv_file_path = tmp_path / "test.csv"
    csv_file_path.write_text("value19,test19\n", encoding="utf-8")

    # WHEN
    replace_string_in_csv(csv_file_path, "19", "23")

    # THEN
    result = csv_file_path.read_text(encoding="utf-8")

    assert result == "value23,test23\n"


def test_replace_string_in_csv_HandlesEmptyFile_Scenario4_EmptyCsv(
    tmp_path,
):
    # ESTABLISH
    csv_file_path = tmp_path / "empty.csv"
    csv_file_path.write_text("", encoding="utf-8")

    # WHEN
    replace_string_in_csv(csv_file_path, "19", "23")

    # THEN
    result = csv_file_path.read_text(encoding="utf-8")
    assert result == ""


def _summary_path(chapter_dir: Path, chxx_prefix: str) -> Path:
    """Example used for change_ai_summary_md tests"""

    return Path(create_ai_summary_path(str(chapter_dir), chxx_prefix))


def _write_summary(chapter_dir: Path, chxx_prefix: str, text: str) -> Path:
    summary_path = _summary_path(chapter_dir, chxx_prefix)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(text)
    return summary_path


def test_change_ai_summary_md_ReturnsNone_Scenario01_ReplacesChapterAndPrefix(tmp_path):
    # ESTABLISH
    src_dir = tmp_path
    chapter_dir = src_dir / "ch01_desc"
    chapter_dir.mkdir()
    summary_path = _write_summary(
        chapter_dir, "ch01", "Chapter 01 covers ch01 modules."
    )

    # WHEN
    result = change_ai_summary_md(str(src_dir), 1, 2)

    # THEN
    assert result is None
    assert summary_path.read_text() == "Chapter 02 covers ch02 modules."


def test_change_ai_summary_md_ReturnsNone_Scenario02_UpdatesAllMatchingDirs(tmp_path):
    # ESTABLISH
    src_dir = tmp_path
    dir_names = ["ch01_alpha", "ch01_beta", "ch01_gamma"]
    summary_paths = []
    for dir_name in dir_names:
        chapter_dir = src_dir / dir_name
        chapter_dir.mkdir()
        summary_paths.append(
            _write_summary(chapter_dir, "ch01", f"Chapter 01 in {dir_name}")
        )

    # WHEN
    change_ai_summary_md(str(src_dir), 1, 5)

    # THEN
    for dir_name, summary_path in zip(dir_names, summary_paths):
        expected_text = f"Chapter 05 in {dir_name.replace('ch01', 'ch05')}"
        assert summary_path.read_text() == expected_text


def test_change_ai_summary_md_ReturnsNone_Scenario03_IgnoresOtherChapterDirs(tmp_path):
    # ESTABLISH
    src_dir = tmp_path
    src_chapter_dir = src_dir / "ch01_desc"
    other_chapter_dir = src_dir / "ch02_desc"
    src_chapter_dir.mkdir()
    other_chapter_dir.mkdir()
    src_summary_path = _write_summary(src_chapter_dir, "ch01", "Chapter 01 ch01")
    other_text = "Chapter 02 ch02 mentions Chapter 01 and ch01"
    other_summary_path = _write_summary(other_chapter_dir, "ch02", other_text)

    # WHEN
    change_ai_summary_md(str(src_dir), 1, 7)

    # THEN
    assert src_summary_path.read_text() == "Chapter 07 ch07"
    assert other_summary_path.read_text() == other_text


def test_change_ai_summary_md_ReturnsNone_Scenario04_NoMatchingDirsChangesNothing(
    tmp_path,
):
    # ESTABLISH
    src_dir = tmp_path
    other_chapter_dir = src_dir / "ch02_desc"
    other_chapter_dir.mkdir()
    other_summary_path = _write_summary(other_chapter_dir, "ch02", "Chapter 02 ch02")

    # WHEN
    result = change_ai_summary_md(str(src_dir), 1, 3)

    # THEN
    assert result is None
    assert other_summary_path.read_text() == "Chapter 02 ch02"
    assert sorted(path.name for path in src_dir.iterdir()) == ["ch02_desc"]


def test_change_ai_summary_md_ReturnsNone_Scenario05_ZeroPadsNumbers(tmp_path):
    # ESTABLISH
    x_data = [
        (1, 9, "Chapter 09 ch09"),
        (9, 10, "Chapter 10 ch10"),
        (10, 11, "Chapter 11 ch11"),
    ]
    for case_idx, (src_int, dst_int, expected_text) in enumerate(x_data):
        src_dir = tmp_path / f"case{case_idx}"
        src_dir.mkdir()
        src_prefix = f"ch{src_int:02}"
        chapter_dir = src_dir / f"{src_prefix}_desc"
        chapter_dir.mkdir()
        summary_path = _write_summary(
            chapter_dir, src_prefix, f"Chapter {src_int:02} {src_prefix}"
        )

        # WHEN
        change_ai_summary_md(str(src_dir), src_int, dst_int)

        # THEN
        assert summary_path.read_text() == expected_text


def test_change_ai_summary_md_ReturnsNone_Scenario06_KeepsFileNameAndOtherText(
    tmp_path,
):
    # ESTABLISH
    src_dir = tmp_path
    chapter_dir = src_dir / "ch01_desc"
    chapter_dir.mkdir()
    summary_path = _write_summary(
        chapter_dir, "ch01", "# Title\nChapter 01 intro\nunrelated line\nch01 end\n"
    )

    # WHEN
    change_ai_summary_md(str(src_dir), 1, 4)

    # THEN
    assert summary_path.exists()
    assert [path.name for path in summary_path.parent.iterdir()] == [summary_path.name]
    expected_text = "# Title\nChapter 04 intro\nunrelated line\nch04 end\n"
    assert summary_path.read_text() == expected_text
