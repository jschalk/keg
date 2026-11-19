from ch00_py.file_toolbox import create_path
from ch17_nabu._ref.ch17_semantic_types import TimeNum
from ch17_nabu.nabu_config import create_nabu_config_path, get_nabu_config_filename
from ch99_glossary.ch_keyword import Ch17Keywords as kw


def test_get_nabu_config_filename_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config_filename = get_nabu_config_filename()
    # THEN
    assert nabu_config_filename == "nabu_config.json"


def test_create_nabu_config_path_ReturnsObj_Nabu() -> str:
    # ESTABLISH / WHEN
    chapter_dir = create_path(kw.src, "ch17_nabu")
    # THEN
    assert create_nabu_config_path() == create_path(chapter_dir, "nabu_config.json")


# def test_create_nabu_config_path_ReturnsObj():
#     # ESTABLISH / WHEN
#     nabu_config_path = create_nabu_config_path()

#     # THEN
#     moments_dir = create_path(temp3_dir, "moments")
#     a23_path = create_path(moments_dir, "Amy23")
#     expected_a23_te_path = create_path(a23_path, MOMENT_OTE1_AGG_JSON_FILENAME)
#     assert nabu_config_path == expected_a23_te_path


# @pytest_mark.skip_on_linux
# def test_create_nabu_config_path_HasDocString():
#     # ESTABLISH
#     moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
#     doc_str = create_nabu_config_path("moment_mstr_dir", moment_lasso)
#     doc_str = f"Returns path: {doc_str}"
#     # WHEN / THEN
#     assert inspect_getdoc(create_nabu_config_path) == doc_str
