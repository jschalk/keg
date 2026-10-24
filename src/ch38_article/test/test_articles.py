from ch00_py.file_toolbox import save_file
from ch38_article.article_toolbox import (
    get_snippets_locations_dict,
    ArticleUnit,
    get_articleunit_from_file,
    get_default_article_snippets_order,
)
from pathlib import Path
from os.path import join as os_path_join


def test_get_snippets_locations_dict_ReturnsDict_Scenario01_SingleMatchSingleLine():
    # ESTABLISH
    x_markdown_str = "Hello keg world"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(1, 7)]}


def test_get_snippets_locations_dict_ReturnsDict_Scenario02_MultipleMatchesSameLine():
    # ESTABLISH
    x_markdown_str = "keg keg keg"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(1, 1), (1, 5), (1, 9)]}


def test_get_snippets_locations_dict_ReturnsDict_Scenario03_MatchesAcrossMultipleLines():
    # ESTABLISH
    x_markdown_str = "# Title\nkeg intro\nsecond keg line\n"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(2, 1), (3, 8)]}


def test_get_snippets_locations_dict_ReturnsDict_Scenario04_NoMatchFound():
    # ESTABLISH
    x_markdown_str = "This document does not have required word."
    x_search_list = ["missing"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"missing": []}


def test_get_snippets_locations_dict_ReturnsDict_Scenario05_EmptySearchStringYieldsNoMatches():
    # ESTABLISH
    x_markdown_str = "Any content here"
    x_search_list = [""]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"": []}


def test_get_snippets_locations_dict_ReturnsDict_Scenario06_EmptyMarkdownTextYieldsNoMatches():
    # ESTABLISH
    x_markdown_str = ""
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": []}


def test_get_snippets_locations_dict_ReturnsDict_Scenario07_OverlappingMatchesAreAllCaptured():
    # ESTABLISH
    x_markdown_str = "aaaa"
    x_search_list = ["aa"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"aa": [(1, 1), (1, 2), (1, 3)]}


def test_get_snippets_locations_dict_ReturnsDict_Scenario08_SearchIsCaseSensitive():
    # ESTABLISH
    x_markdown_str = "Keg keg KEG"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(1, 5)]}


def test_get_snippets_locations_dict_ReturnsDict_Scenario09_MultipleSearchStringsEachGetOwnEntry():
    # ESTABLISH
    x_markdown_str = "# keg2 Title\nBody text about keg2 and stuff.\n"
    x_search_list = ["keg2", "stuff", "gold"]

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {
        "keg2": [(1, 3), (2, 17)],
        "stuff": [(2, 26)],
        "gold": [],
    }


def test_get_snippets_locations_dict_ReturnsDict_Scenario10_EmptySearchListYieldsEmptyDict():
    # ESTABLISH
    x_markdown_str = "keg content"
    x_search_list = []

    # WHEN
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {}


def test_get_snippets_locations_dict_ReturnsDict_Scenario11_MarkdownFileReadFromDisk(
    tmp_path,
):
    # ESTABLISH
    x_markdown_file_path = tmp_path / "sample.md"
    x_markdown_file_path.write_text("# keg2\n\nSee the keg2 docs.\n")
    x_search_list = ["keg2"]

    # WHEN
    x_markdown_str = x_markdown_file_path.read_text()
    x_result_dict = get_snippets_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg2": [(1, 3), (3, 9)]}


def test_get_default_article_snippets_order_ReturnsObj():
    # ESTABLISH / WHEN
    ref_article_str_order = get_default_article_snippets_order()
    # THEN
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    expected_ref_article_str_order = [author_str, date_str, source_str, copied_str]
    assert ref_article_str_order == expected_ref_article_str_order


def test_ArticleUnit_Exists():
    # ESTABLISH / WHEN
    x_articleunit = ArticleUnit()
    # THEN
    assert not x_articleunit.md_file_path
    assert not x_articleunit.required_snippets
    assert not x_articleunit.ordered_line_nums
    assert not x_articleunit.missing_required
    assert not x_articleunit.ordered_snippets
    assert not x_articleunit.out_of_order_req_index
    assert not x_articleunit.out_of_order_req_str


def test_get_articleunit_from_file_ReturnsObj_Scenario0_Empty(temp3_dir):
    # ESTABLISH
    temp_file_path = os_path_join(temp3_dir, "temp_file.md")
    temp_file_str = """
empty file
"""
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str, source_str, copied_str]
    save_file(temp_file_path, None, temp_file_str)

    # WHEN
    x_articleunit = get_articleunit_from_file(
        temp_file_path, required_strings, ordered_snippets=required_strings
    )
    # THEN
    assert x_articleunit.md_file_path == temp_file_path
    assert x_articleunit.required_snippets == required_strings
    assert x_articleunit.ordered_line_nums == [None, None, None, None]
    assert x_articleunit.missing_required
    expected_missing_required_lines = (
        ", '**Author:**', '**Date:**', '**Source:**', '**Copied to Keg:**'"
    )
    print(x_articleunit.missing_required)
    assert x_articleunit.missing_required == expected_missing_required_lines
    assert not x_articleunit.out_of_order_req_index
    assert x_articleunit.out_of_order_req_str == ""


def test_get_articleunit_from_file_ReturnsObj_Scenario1_AllRequiredExist(temp3_dir):
    # ESTABLISH
    temp_file_path = os_path_join(temp3_dir, "temp_file.md")
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str, source_str, copied_str]
    ordered_snippets = [author_str, date_str, source_str, copied_str]
    temp_file_str = """
**Author:**
**Date:**
**Source:**

**Copied to Keg:**
"""
    save_file(temp_file_path, None, temp_file_str)

    # WHEN
    x_articleunit = get_articleunit_from_file(
        file_path=temp_file_path,
        required_snippets=required_strings,
        ordered_snippets=ordered_snippets,
    )
    # THEN
    assert x_articleunit.md_file_path == temp_file_path
    assert x_articleunit.required_snippets == required_strings
    assert x_articleunit.ordered_line_nums == [2, 3, 4, 6]
    assert x_articleunit.missing_required == ""
    assert not x_articleunit.out_of_order_req_index
    assert x_articleunit.out_of_order_req_str == ""


def test_get_articleunit_from_file_ReturnsObj_Scenario2_OutOfOrder(temp3_dir):
    # ESTABLISH
    temp_file_path = os_path_join(temp3_dir, "temp_file.md")
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str, source_str]
    ordered_snippets = [author_str, date_str, source_str, copied_str]
    temp_file_str = """
**Author:**
**Source:**
**Date:**

**Copied to Keg:**
"""
    save_file(temp_file_path, None, temp_file_str)

    # WHEN
    x_articleunit = get_articleunit_from_file(
        temp_file_path, required_strings, ordered_snippets
    )
    # THEN
    assert x_articleunit.md_file_path == temp_file_path
    assert x_articleunit.required_snippets == required_strings
    assert x_articleunit.ordered_line_nums == [2, 4, 3, 6]
    assert x_articleunit.missing_required == ""
    assert x_articleunit.out_of_order_req_index == 2
    assert x_articleunit.out_of_order_req_str == "**Source:** is out of order."


def test_CurrentMarkDownFilesHaveRequiredStrings():
    # TODO find out why lack of "Esta..." string isn't causing linter test to fail
    # check_all_test_functions_are_formatted(all_test_functions)
    # ESTABLISH
    current_ch_dir = Path(__file__).resolve().parent.parent
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str, source_str, copied_str]

    # WHEN / THEN
    for md_file_path in sorted(current_ch_dir.glob("*.md")):
        print(f"{md_file_path=}")
        md_articleunit = get_articleunit_from_file(md_file_path, required_strings)
        assert not md_articleunit.missing_required, md_file_path
        assert not md_articleunit.out_of_order_req_str, md_file_path
        # content_str = md_file_path.read_text(encoding="utf-8")
        # str_loc_dict = get_snippets_locations_dict(content_str, required_strings)
        # for required_str in required_strings:
        #     assertion_failure_str = f"{md_file_path} is missing {required_str!r}"
        #     assert str_loc_dict.get(required_str), assertion_failure_str
        # author_line = str_loc_dict.get(author_str)[0][0]
        # date_line = str_loc_dict.get(date_str)[0][0]
        # source_line = str_loc_dict.get(source_str)[0][0]
        # copied_line = str_loc_dict.get(copied_str)[0][0]
        # assert author_line > date_line, md_file_path
        # assert source_line > author_line, md_file_path
        # assert copied_line > source_line, md_file_path
