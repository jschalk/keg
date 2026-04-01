from os import listdir as os_listdir, walk as os_walk
from os.path import basename as os_path_basename, exists as os_path_exists
from pathlib import Path as pathlib_Path
from src.ch00_py.chapter_desc_main import get_chapter_desc_str_number
from src.ch00_py.file_toolbox import create_path, get_level1_dirs, open_json
from src.ch98_docs_builder.doc_builder import get_chapter_desc_prefix
from src.linter.style import (
    get_chapter_descs,
    get_python_files_with_flag,
    get_semantic_types_filename,
)


def path_contains_subpath(full_path: str, sub_path: str):
    full = pathlib_Path(full_path).resolve()
    sub = pathlib_Path(sub_path).resolve()
    try:
        full.relative_to(sub)
        return True
    except ValueError:
        return False


def test_Chapters_test_TestsAreInCorrectDirStructure():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        desc_number = int(chapter_desc_str_number)
        level1_dirs = get_level1_dirs(chapter_dir)
        print(f"{desc_number} {level1_dirs=}")
        test_str = "test"
        for level1_dir in level1_dirs:
            if level1_dir.find(test_str) > -1:
                if level1_dir != test_str:
                    print(f"{desc_number=} {level1_dir=}")
                assert level1_dir == test_str


def test_Chapters_NonTestFilesDoNotHavePrintStatments():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    print_str = "print"

    # WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        py_files = [f for f in os_listdir(chapter_dir) if f.endswith(".py")]
        for py_file in py_files:
            py_file_path = create_path(chapter_dir, py_file)
            py_file_str = open(py_file_path, encoding="utf-8").read()
            print_str_in_py_file_bool = print_str in py_file_str
            if print_str_in_py_file_bool:
                print(f"Chapter {chapter_desc} file {py_file_path} has print statement")
            assert not print_str_in_py_file_bool


def test_Chapters_NonTestFilesDoNotHaveStringFunctionsImports():
    """Check all non-test python files do not import str functions"""

    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        for file_path, file_imports in get_python_files_with_flag(chapter_dir).items():
            filename = str(os_path_basename(file_path))
            file_path = str(file_path)
            print(f"{file_path=}")
            if not filename.startswith("test") and "_util" not in file_path:
                for file_import in file_imports:
                    if str(file_import[0]).endswith("_str"):
                        print(f"{chapter_desc} {filename} {file_import[0]=}")
                    assert not str(file_import[0]).endswith("_str")


def test_Chapters_ChapterReferenceDir_ref_ExistsForEveryChapter_Scenario0():
    """
    Test that all string-related functions in each chapter directory are asserted and tested.
    This test performs the following checks for each chapter:
    Raises:
        AssertionError: If any of the above conditions are not met.
    """

    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        docs_dir = create_path(chapter_dir, "_ref")
        chapter_ref_path = create_path(docs_dir, f"{chapter_desc_prefix}_ref.json")
        # chapter_ref_path = create_chapter_ref_path(chapter_dir,)
        semantic_types_filename = get_semantic_types_filename(chapter_desc_prefix)
        semantics_path = create_path(docs_dir, semantic_types_filename)
        assert os_path_exists(docs_dir)
        assert os_path_exists(chapter_ref_path)
        assert os_path_exists(semantics_path)
        chapter_ref_dict = open_json(chapter_ref_path)
        # print(f"{chapter_ref_path} \t Items: {len(chapter_ref_dict)}")
        ref_keys = set(chapter_ref_dict.keys())
        chapter_description_str = "chapter_description"
        chapter_blurb_str = "chapter_blurb"
        chapter_number_str = "chapter_number"
        chapter_content_str = "chapter_content"
        ontology_str = "ontology summary"
        keys_assertion_fail_str = f"ref json for {chapter_desc} missing required key(s)"
        expected_ref_keys = {
            chapter_blurb_str,
            chapter_description_str,
            chapter_number_str,
            chapter_content_str,
            ontology_str,
        }
        assert ref_keys == expected_ref_keys, keys_assertion_fail_str
        assert chapter_ref_dict.get(chapter_description_str) == chapter_desc
        ref_chapter_blurb = chapter_ref_dict.get(chapter_blurb_str)
        MAX_CHAPTER_BLURB_LENGTH = 88  # arbitrarily choosen

        assert len(ref_chapter_blurb) > 0
        assert len(ref_chapter_blurb) <= MAX_CHAPTER_BLURB_LENGTH
        ontology_assertion_fail_str = (
            f"{chapter_desc} {ontology_str} str value is empty"
        )
        ontology_summary = chapter_ref_dict.get(ontology_str)
        print(f"{ontology_summary=}")
        assert ontology_summary, ontology_assertion_fail_str
        ref_chapter_content = chapter_ref_dict.get(chapter_content_str)
        content_assertion_fail_str = f"{chapter_desc} {chapter_content_str} is invalid"
        assert len(ref_chapter_content) > 0, content_assertion_fail_str
        chapter_desc_ch_int = int(get_chapter_desc_str_number(chapter_desc))
        chapter_ref_ch_int = chapter_ref_dict.get(chapter_number_str)
        assertion_fail_str = f"{chapter_desc} expecting key {chapter_number_str} with value {chapter_desc_ch_int}"
        assert chapter_ref_ch_int == chapter_desc_ch_int, assertion_fail_str


def test_Chapters_DoNotHaveEmptyDirectories():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    excluded_dirs = {
        "src/ch21_world/test/test_world_examples/worlds",
        "src/ch19_etl_steps/test/z_notebooks",
    }

    # WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        for dirpath, dirnames, filenames in os_walk(chapter_dir):
            if not is_excluded_subpath(dirpath, excluded_dirs):
                assert_fail_str = f"{chapter_desc} Empty directory found: {dirpath}"
                if dirnames == ["__pycache__"] and filenames == []:
                    print(f"{dirnames} {dirpath}")
                    dirnames = []
                # print(f"{dirnames=}")
                # print(f"{filenames=}")
                assert dirnames or filenames, assert_fail_str


def is_excluded_subpath(dirpath: str, excluded_dirs: set[str]) -> bool:
    return any(
        path_contains_subpath(dirpath, exclude_dir) for exclude_dir in excluded_dirs
    )
