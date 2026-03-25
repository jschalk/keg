from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from pytest import mark as pytest_mark
from src.ch00_py.file_toolbox import create_path, get_json_filename
from src.ch98_docs_builder._ref.ch98_path import (
    create_chapter_ref_path,
    create_src_keywords_description_path,
)
from src.ch98_docs_builder.test._util.ch98_env import get_temp_dir


def test_create_src_keywords_description_path_ReturnsObj():
    # ESTABLISH
    src_dir = get_temp_dir()

    # WHEN
    keywords_class_file_path = create_src_keywords_description_path(src_dir)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    expected_filename = get_json_filename("keywords_description")
    expected_file_path = create_path(ref_dir, expected_filename)
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_src_keywords_description_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ref_dir = create_path(src_dir, "ref")
    doc_str = create_path(ref_dir, get_json_filename("keywords_description"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_src_keywords_description_path) == doc_str


def test_create_chapter_ref_path_ReturnsObj():
    # ESTABLISH
    src_dir = get_temp_dir()
    chapter_prefix = "ch04"

    # WHEN
    keywords_class_file_path = create_chapter_ref_path(src_dir, chapter_prefix)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "_ref")
    expected_filename = get_json_filename(f"{chapter_prefix}_ref")
    expected_file_path = create_path(ref_dir, expected_filename)
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_chapter_ref_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ch_dir = create_path(src_dir, "chapter_dir")
    ref_dir = create_path(ch_dir, "_ref")
    doc_str = create_path(ref_dir, get_json_filename("chXX_ref"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_chapter_ref_path) == doc_str
