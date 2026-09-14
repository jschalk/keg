from ch97_docs_builder.glossary_definition import (
    get_count_keg_terms_by_chapters,
    get_count_strs_by_dirs,
    get_keywords_definitions,
    get_focus_keyword_frequency,
)
from ch99_glossary.ch_keyword import Ch97Keywords as kw


def test_get_count_strs_by_dirs_CountsTerms_Scenario0_SingleFile(tmp_path):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file1.txt").write_text(
        "ContactName BreakTerm ContactName", encoding="utf-8"
    )
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName", "BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 2}, "BreakTerm": {1: 1}}


def test_get_count_strs_by_dirs_CountsAcrossFiles_Scenario1_MultipleFiles(tmp_path):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file1.txt").write_text("ContactName", encoding="utf-8")
    (ch01_dir / "file2.txt").write_text("ContactName BreakTerm", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName", "BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 2}, "BreakTerm": {1: 1}}


def test_get_count_strs_by_dirs_CountsByChapter_Scenario2_MultipleChapters(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch02_dir = tmp_path / "ch02"
    ch01_dir.mkdir()
    ch02_dir.mkdir()
    (ch01_dir / "file.txt").write_text("ContactName ContactName", encoding="utf-8")
    (ch02_dir / "file.txt").write_text("ContactName BreakTerm", encoding="utf-8")
    ch_dirs = {1: ch01_dir, 2: ch02_dir}
    keg_terms = {"ContactName", "BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 2, 2: 1}, "BreakTerm": {1: 0, 2: 1}}


def test_get_count_strs_by_dirs_ReturnsZero_Scenario3_TermMissing(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file.txt").write_text("SomethingElse", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 0}}


def test_get_count_strs_by_dirs_HandlesNestedFiles_Scenario4_Subdirectories(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    nested_dir = ch01_dir / "nested"

    nested_dir.mkdir(parents=True)
    (nested_dir / "file.txt").write_text("BreakTerm BreakTerm", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"BreakTerm": {1: 2}}


def test_get_count_strs_by_dirs_SkipsBinaryFiles_Scenario5_UnicodeDecodeError(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "valid.txt").write_text("ContactName", encoding="utf-8")
    (ch01_dir / "binary.bin").write_bytes(b"\x80\x81\x82\x83")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 1}}


def test_get_count_strs_by_dirs_ReturnsEmpty_Scenario6_EmptyKegTerms(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file.txt").write_text("ContactName", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = set()

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {}


def test_get_count_keg_terms_by_chapters_CountsTerms_Scenario0_SrcDir():
    # GIVEN / WHEN
    keg_terms_by_chapters = get_count_keg_terms_by_chapters()

    # THEN
    keg_terms = set(get_keywords_definitions().keys())
    assert set(keg_terms_by_chapters.keys()) == keg_terms
    focus_keyword_count_set = {"huh"}
    focus_keyword_frequency = get_focus_keyword_frequency(focus_keyword_count_set)

    for x_keg_term, term_curr_allowed_tup in focus_keyword_frequency.items():
        actual_ch_use = term_curr_allowed_tup[0]
        allowed_ch_use = term_curr_allowed_tup[1]
        print(
            f"{x_keg_term:<20} {str(sorted(set(actual_ch_use.keys()))):<40} {allowed_ch_use[:20]=}"
        )

    # src_keywords_src_path = create_src_keywords_src_path(kw.src)
    # save_json(src_keywords_src_path, None, keywords_src_config)
    # assert 1 == 2
    # TODO keyword valid ch setting
    # ### consider following ###
    # finding all terms used twice and change keyword src.
    # replacing all range with individual listed
    # removing 'Only referenced in ch if not single entry
    # creating pytest tripper that saves changes when activated, otherwise allows failed tests
