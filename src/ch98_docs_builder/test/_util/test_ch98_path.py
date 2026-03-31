from inspect import getdoc as inspect_getdoc
from pytest import mark as pytest_mark
from src.ch00_py.file_toolbox import create_path, get_json_filename
from src.ch98_docs_builder._ref.ch98_path import (
    create_chapter_ref_path,
    create_src_keg_terminology_path,
)


def test_create_src_keg_terminology_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    src_dir = temp3_dir

    # WHEN
    keywords_class_file_path = create_src_keg_terminology_path(src_dir)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    expected_filename = get_json_filename("keg_terminology")
    expected_file_path = create_path(ref_dir, expected_filename)
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skip_on_linux
def test_create_src_keg_terminology_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ref_dir = create_path(src_dir, "ref")
    doc_str = create_path(ref_dir, get_json_filename("keg_terminology"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_src_keg_terminology_path) == doc_str


def test_create_chapter_ref_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    src_dir = temp3_dir
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


@pytest_mark.skip_on_linux
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
