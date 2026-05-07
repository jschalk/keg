from ch00_py.keyword_class_builder import (
    get_keywords_src_config,
    save_keywords_by_chapter_md,
)
from ch98_docs_builder.doc_builder import (
    get_rebuilt_keywords_src_config,
    resave_chapter_and_keyword_json_files,
    save_brick_formats_md,
    save_brick_mds,
    save_chapter_blurbs_md,
    save_ropeterm_description_md,
)
from random import random as random_random
from ref.keywords import Ch98Keywords as kw
from ref.sorter import get_keg_elements_sort_order


def test_recreate_keyword_src_config_Scenario0_Includes_sort_ordinal():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    keywords_src_config = get_keywords_src_config()
    expected_clean_keywords_src_config = {}
    for keyword, kw_config in keywords_src_config.items():
        new_kw_config = {
            kw.exam_tier: kw_config.get(kw.exam_tier),
            kw.init_ch: kw_config.get(kw.init_ch),
        }
        if kw_config.get(kw.semantic_type):
            new_kw_config[kw.semantic_type] = kw_config.get(kw.semantic_type)
        expected_clean_keywords_src_config[keyword] = new_kw_config

    for sort_index, sorting_keyword in enumerate(get_keg_elements_sort_order()):
        expected_clean_keywords_src_config[sorting_keyword]["sort_ordinal"] = sort_index

    # WHEN / THEN
    # assert get_keywords_src_config() == clean_keywords_src_config
    assert get_rebuilt_keywords_src_config() == expected_clean_keywords_src_config

    # missing_elements = {
    #     keyword
    #     for keyword in get_keg_elements_sort_order()
    #     if keyword not in keywords_set
    # }
    # ch_num = 17
    # x_count = 0
    # for missing_element in sorted(missing_elements):
    #     x_count += 1
    #     print(
    #         f""""{missing_element}": {{"exam_tier": 0, "init_ch": "ch{ch_num}"}},"""
    #     )
    # print(f"{x_count} elements")
    # assert set(get_keg_elements_sort_order()).issubset(keywords_set)


def test_SpecialTestThatBuildsDocs(rebuild_jsons):
    """
    Intended to be the last test before the style checker (linter) tests.
    Should only create documentation and/or sort json files
    """
    print(f"{rebuild_jsons=}")
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    destination_dir = "docs"
    # This is a special test in that instead of asserting anything it just writes
    # documentation to production when Pytest is run
    save_brick_mds(destination_dir)
    save_brick_formats_md(destination_dir)
    save_chapter_blurbs_md(destination_dir)
    save_ropeterm_description_md(destination_dir)
    save_keywords_by_chapter_md(destination_dir)  # docs\keywords_by_chapter.md
    # 4% of stances resave all json files so that they are ordered alphabetically
    if random_random() < 0.04 or rebuild_jsons:
        resave_chapter_and_keyword_json_files()
