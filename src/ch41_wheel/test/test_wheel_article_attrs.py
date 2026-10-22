from src.ch38_article_tool.article_toolbox import (
    get_string_locations_dict,
    get_articleunit_from_file,
)
from pathlib import Path
from os.path import join as os_path_join, exists as os_path_exists


def test_Ch41MarkDownFilesHaveRequiredStrings():
    # ESTABLISH
    current_ch_dir = Path(__file__).resolve().parent.parent
    author_str = "**Author:**"
    date_str = "**Date:**"
    # source_str = "**Source:**"
    # copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str]

    # WHEN / THEN
    for md_file_path in sorted(current_ch_dir.glob("*.md")):
        md_articleunit = get_articleunit_from_file(md_file_path, required_strings)
        assert not md_articleunit.missing_required, md_file_path
        assert not md_articleunit.out_of_order_req_str, md_file_path


NARRATIVE_ARTICLES = {
    "schalk_wheel0_theory.md",
    # "schalk_wheel1_implications.md",
    # "schalk_wheel2_campaign.md",
}


def test_NarrativeArticlesExist():
    # GIVEN / WHEN
    narr_arts = NARRATIVE_ARTICLES
    # THEN
    current_ch_dir = Path(__file__).resolve().parent.parent
    art1_filename = "schalk_wheel0_theory.md"
    art2_filename = "schalk_wheel1_implications.md"
    art3_filename = "schalk_wheel2_campaign.md"
    assert art1_filename in narr_arts
    # assert art2_filename in narr_arts
    # assert art3_filename in narr_arts
    for x_filename in narr_arts:
        x_path = os_path_join(current_ch_dir, x_filename)
        assert os_path_exists(x_path)


def test_NarrativeArticlesContainCircleBeats():
    # GIVEN
    home_str = "<!--Home"
    need_str = "<!--Need"
    search_str = "<!--Search"
    go_str = "<!--Go"
    find_str = "<!--Find"
    take_str = "<!--Take"
    return_str = "<!--Return"
    change_str = "<!--Change"
    required_strings = {
        home_str,
        need_str,
        go_str,
        search_str,
        find_str,
        take_str,
        return_str,
        change_str,
    }

    # WHEN / THEN
    current_ch_dir = Path(__file__).resolve().parent.parent
    for article_filename in NARRATIVE_ARTICLES:
        md_file_path = Path(os_path_join(current_ch_dir, article_filename))
        content_str = md_file_path.read_text(encoding="utf-8")
        str_loc_dict = get_string_locations_dict(content_str, required_strings)
        for required_str in required_strings:
            miss_assertion_failure_str = f"{md_file_path} is missing {required_str!r}"
            str_locs = str_loc_dict.get(required_str)
            assert str_locs, miss_assertion_failure_str
            len_assertion_failure_str = f"{md_file_path} has too many {required_str!r}"
            assert len(str_locs) == 1, len_assertion_failure_str
        home_line = str_loc_dict.get(home_str)[0][0]
        need_line = str_loc_dict.get(need_str)[0][0]
        go_line = str_loc_dict.get(go_str)[0][0]
        search_line = str_loc_dict.get(search_str)[0][0]
        find_line = str_loc_dict.get(find_str)[0][0]
        take_line = str_loc_dict.get(take_str)[0][0]
        return_line = str_loc_dict.get(return_str)[0][0]
        change_line = str_loc_dict.get(change_str)[0][0]
        assert home_line <= need_line
        assert need_line <= go_line
        assert go_line <= search_line
        assert search_line <= find_line
        assert find_line <= take_line
        assert take_line <= return_line
        assert return_line <= change_line
