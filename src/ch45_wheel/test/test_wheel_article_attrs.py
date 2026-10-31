from ch38_article.article_toolbox import (
    get_snippets_locations_dict,
    get_articleunit_from_file,
)
from pathlib import Path
from os.path import join as os_path_join, exists as os_path_exists

NARRATIVE_ARTICLES = {
    "schalk_wheel0_theory.md",
    # "schalk_wheel1_implications.md",
    # "schalk_wheel2_campaign.md",
}


def test_NarrativeArticlesExist():
    # ESTABLISH / WHEN
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
    # ESTABLISH
    home_str = "<!--Home"
    need_str = "<!--Need"
    search_str = "<!--Search"
    go_str = "<!--Go"
    find_str = "<!--Find"
    take_str = "<!--Take"
    return_str = "<!--Return"
    change_str = "<!--Change"
    required_snippets = [
        home_str,
        need_str,
        go_str,
        search_str,
        find_str,
        take_str,
        return_str,
        change_str,
    ]
    ordered_snippets = [
        home_str,
        need_str,
        go_str,
        search_str,
        find_str,
        take_str,
        return_str,
        change_str,
    ]

    # WHEN / THEN
    current_ch_dir = Path(__file__).resolve().parent.parent
    for article_filename in NARRATIVE_ARTICLES:
        md_file_path = Path(os_path_join(current_ch_dir, article_filename))
        md_articleunit = get_articleunit_from_file(
            md_file_path, required_snippets, ordered_snippets
        )
        assert not md_articleunit.missing_required, md_file_path
        assert not md_articleunit.out_of_order_req_str, md_file_path

        content_str = md_file_path.read_text(encoding="utf-8")
        str_loc_dict = get_snippets_locations_dict(content_str, required_snippets)
        for required_str in required_snippets:
            str_locs = str_loc_dict.get(required_str)
            len_assertion_failure_str = f"{md_file_path} has too many {required_str!r}"
            assert len(str_locs) == 1, len_assertion_failure_str
