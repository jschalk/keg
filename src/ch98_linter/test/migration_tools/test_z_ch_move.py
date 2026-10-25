from ch98_linter.ch_move1 import replace_string_in_csv, replace_valid_ch
from copy import deepcopy as copy_deepcopy


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
    csv_file_path.write_text(
        "name,age\nSue,19\nBob,20\n",
        encoding="utf-8",
    )

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
    csv_file_path.write_text(
        "19,19,19\n",
        encoding="utf-8",
    )

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

    csv_file_path.write_text(
        original_text,
        encoding="utf-8",
    )

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
    csv_file_path.write_text(
        "value19,test19\n",
        encoding="utf-8",
    )

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
    csv_file_path.write_text(
        "",
        encoding="utf-8",
    )

    # WHEN
    replace_string_in_csv(csv_file_path, "19", "23")

    # THEN
    result = csv_file_path.read_text(encoding="utf-8")
    assert result == ""
