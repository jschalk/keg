from random import random as random_random
from src.ch00_py.keyword_class_builder import save_keywords_by_chapter_md
from src.ch98_docs_builder.doc_builder import (
    resave_chapter_and_keyword_json_files,
    save_brick_formats_md,
    save_chapter_blurbs_md,
    save_idea_brick_mds,
    save_ropeterm_description_md,
)


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
    save_idea_brick_mds(destination_dir)
    save_brick_formats_md(destination_dir)
    save_chapter_blurbs_md(destination_dir)
    save_ropeterm_description_md(destination_dir)
    save_keywords_by_chapter_md(destination_dir)  # docs\keywords_by_chapter.md
    # 4% of instances resave all json files so that they are ordered alphabetically
    if random_random() < 0.04 or rebuild_jsons:
        resave_chapter_and_keyword_json_files()
