from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from pytest import mark as pytest_mark
from src.ch00_py._ref.ch00_path import (
    create_keywords_classes_file_path,
    create_src_example_strs_path,
    create_src_keywords_main_path,
)
from src.ch00_py.file_toolbox import create_path, get_json_filename
from src.ch00_py.test._util.ch00_env import get_temp_dir


def test_create_src_example_strs_path_ReturnsObj():
    # ESTABLISH
    src_dir = get_temp_dir()

    # WHEN
    keywords_class_file_path = create_src_example_strs_path(src_dir)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    expected_file_path = create_path(ref_dir, get_json_filename("example_strs"))
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_src_example_strs_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ref_dir = create_path(src_dir, "ref")
    doc_str = create_path(ref_dir, get_json_filename("example_strs"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_src_example_strs_path) == doc_str


def test_create_src_keywords_main_path_ReturnsObj():
    # ESTABLISH
    src_dir = get_temp_dir()

    # WHEN
    keywords_class_file_path = create_src_keywords_main_path(src_dir)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    expected_file_path = create_path(ref_dir, get_json_filename("keywords_main"))
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_src_keywords_main_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ref_dir = create_path(src_dir, "ref")
    doc_str = create_path(ref_dir, get_json_filename("keywords_main"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_src_keywords_main_path) == doc_str


def test_create_keywords_classes_file_path_ReturnsObj():
    # ESTABLISH
    src_dir = "src"

    # WHEN
    keywords_class_file_path = create_keywords_classes_file_path(src_dir)

    # THEN
    ref_dir = create_path(src_dir, "ref")
    expected_keywords_file_path = create_path(ref_dir, "keywords.py")
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    assert keywords_class_file_path == expected_keywords_file_path


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keywords_classes_file_path_HasDocString():
    # ESTABLISH
    doc_str = create_keywords_classes_file_path("src")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keywords_classes_file_path) == doc_str
