from importlib import import_module as importlib_import_module
from inspect import getsource as inspect_getsource
from src.ch00_py.file_toolbox import create_path, get_dir_file_strs, open_file
from src.ch00_py.keyword_class_builder import (
    get_chapter_keyword_classes,
    get_cumlative_ch_keywords_dict,
    get_keywords_by_chapter,
    get_keywords_src_config,
)
from src.ch98_docs_builder.doc_builder import get_chapter_desc_prefix, get_chapter_descs
from src.linter.style import (
    check_custom_exception_classes_style,
    function_name_style_is_correct,
    get_all_semantic_types_from_ref_files,
    get_chapters_obj_metrics,
    get_json_files,
    get_python_files_with_flag,
    get_semantic_types_filename,
)
from src.ref.keywords import Ch98Keywords as kw


def get_semantic_types_dict() -> dict[str, str]:
    semantic_types_keywords = {}
    for x_keyword, x_dict in get_keywords_src_config().items():
        if semantic_type := x_dict.get("semantic_type"):
            semantic_types_keywords[x_keyword] = semantic_type

    return semantic_types_keywords


def test_get_semantic_types_dict_ReturnsObj():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    semantic_types_dict = get_semantic_types_dict()

    # THEN
    src_semantic_types_keywords = {}
    keywords_src_config = get_keywords_src_config()
    for x_keyword, x_dict in keywords_src_config.items():
        if semantic_type := x_dict.get("semantic_type"):
            src_semantic_types_keywords[x_keyword] = semantic_type
    assert src_semantic_types_keywords == semantic_types_dict
    # "semantic_type": "str"


def test_Chapters_CheckStringMetricsFromEveryFile():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    excluded_functions = {
        "__str__",
        "get_inx_value",  # used in Nabu/Translate
        "_is_inx_knot_inclusion_correct",  # used in Nabu/Translate
        "_is_otx_knot_inclusion_correct",  # used in Nabu/Translate
        "unknown_str_in_otx2inx",  # RopeMap method overrides MapCore method
        "del_otx2inx",  # used in Nabu/Translate
        "find_replace_rope",  # used by ReasonUnit, CaseUnit, FactUnit classes
        "get_obj_key",
        "is_valid",
        "otx_exists",  # used in Nabu/Translate
        "otx2inx_exists",  # used in Nabu/Translate
        "reveal_inx",  # used in Nabu/Translate
        "set_all_otx2inx",  # RopeMap method overrides MapCore method
        "set_knot",
        "set_otx2inx",  # used in Nabu/Translate
        "to_dict",  # used to return class custom dictionary, usually for json file storage
    }

    # WHEN
    chapters_func_class_metrics = get_chapters_obj_metrics(excluded_functions)
    duplicate_func_names = chapters_func_class_metrics.duplicate_func_names
    unnecessarily_excluded_funcs = (
        chapters_func_class_metrics.unnecessarily_excluded_funcs
    )
    all_classes = chapters_func_class_metrics.all_classes
    exception_check_result = check_custom_exception_classes_style(all_classes)
    assert exception_check_result[0], exception_check_result[1]

    semantic_types = chapters_func_class_metrics.semantic_types
    all_functions = chapters_func_class_metrics.all_functions

    # THEN
    flagged_func_name_count = {}
    for function_name in sorted(all_functions.keys()):
        func_name_count = all_functions.get(function_name)
        if func_name_count > 1:
            print(f"{function_name} {func_name_count=}")
            flagged_func_name_count[function_name] = func_name_count
        func_name_style_str = f"Function '{function_name}' naming style error."
        assert function_name_style_is_correct(function_name), func_name_style_str
    # print(f"{len(flagged_func_name_count)=}")
    assertion_fail_str = f"Duplicated functions found: {duplicate_func_names}"
    # print(f"{duplicate_func_names=}")
    assert not duplicate_func_names, assertion_fail_str
    # print(f"{sorted(unnecessarily_excluded_funcs.keys())=}")
    assert not unnecessarily_excluded_funcs, sorted(unnecessarily_excluded_funcs.keys())
    assert semantic_types == get_semantic_types_dict()
    # print(f"{len(all_functions)=}")
    for semantic_type in sorted(list(semantic_types)):
        expected_semantic_type_exists_test_str = f"test_{semantic_type}_Exists"
        # print(expected_semantic_type_exists_test_str)
        assert expected_semantic_type_exists_test_str in all_functions


def test_Chapters_Semantic_Types_HasCorrectFormating():
    # ESTABLISH / WHEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        docs_dir = create_path(chapter_dir, "_ref")
        semantic_types_filename = get_semantic_types_filename(chapter_desc_prefix)
        semantics_path = create_path(docs_dir, semantic_types_filename)
        print(f"{chapter_desc=}")
        # THEN
        # semantic_types_file never has import *
        assert open_file(semantics_path).find("import *") == -1


def test_Chapters_Semantic_Types_AreAllIn_chXX_semantic_types_ref_files():
    # ESTABLISH / WHEN
    ref_files_semantic_types = get_all_semantic_types_from_ref_files()

    # THEN
    print(f"{len(ref_files_semantic_types)=}")
    expected_types_dict = get_semantic_types_dict()
    expected_types_set = set(expected_types_dict.keys())
    print(f"{len(expected_types_set)=}")
    print(f"missing {expected_types_set.difference(ref_files_semantic_types)}")

    assert ref_files_semantic_types == expected_types_set


def test_Chapters_KeywordsAppearWhereTheyShould():
    """Test that checks no str function is created before it is needed or after the term is used."""

    # sourcery skip: low-code-quality, no-conditionals-in-tests, no-loop-in-tests
    # ESTABLISH
    # "close" is excluded because it is used to close sqlite database connections
    excluded_strs = {"close"}
    # new method references from keywords config file
    keywords_dict = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_dict)
    all_keywords_set = set(keywords_dict.keys())
    keywords_in_ch_count = {keyword: {} for keyword in keywords_dict.keys()}
    cumlative_ch_keywords_dict = get_cumlative_ch_keywords_dict(keywords_by_chapter)

    # WHEN / THEN
    # all_file_count = 0
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        allowed_chapter_keywords = cumlative_ch_keywords_dict.get(chapter_prefix)
        not_allowed_keywords = all_keywords_set.difference(allowed_chapter_keywords)
        not_allowed_keywords = not_allowed_keywords.difference(excluded_strs)
        # print(f"{chapter_prefix} {len(not_allowed_keywords)=}")

        chapter_files = list(get_python_files_with_flag(chapter_dir).keys())
        chapter_files.extend(list(get_json_files(chapter_dir)))
        chapter_files = sorted(chapter_files)
        # chapter_file_count = 0
        for file_path in chapter_files:
            # print(f"{chapter_prefix} {file_path=}")
            # chapter_file_count += 1
            # all_file_count += 1
            # print(f"{all_file_count} Chapter: {chapter_file_count} {file_path}")
            file_str = open(file_path).read()
            for keyword in not_allowed_keywords:
                notallowed_keyword_failure_str = f"keyword {keyword} is not allowed in chapter {chapter_prefix}. It is in {file_path=}"
                assert keyword not in file_str, notallowed_keyword_failure_str
            # print(f"{file_path=}")
            excessive_imports_str = f"{file_path} has too many Keywords class imports"
            ch_class_name = f"C{chapter_prefix[1:]}Keywords"
            is_doc_builder_file = "doc_builder.py" in file_path
            if file_path.find(f"test_{chapter_prefix}_keywords.py") == -1:
                assert file_str.count("Keywords") <= 1, excessive_imports_str
            elif not is_doc_builder_file:
                assert file_str.count(ch_class_name) in {0, 4}, ""
            enum_x = f"{file_path} Keywords Class Import is wrong, it should be {ch_class_name}"
            if "Keywords" in file_str and not is_doc_builder_file:
                assert ch_class_name in file_str, enum_x
                # print(f"{file_path=} {ch_class_name=}")

            # check if semantic_types import is from current chapter
            _semantic_types_import_count = file_str.count("_semantic_types import")
            if "semantic_types" not in file_path and _semantic_types_import_count > 0:
                chXX_semantic_types_str = f"{chapter_prefix}_semantic_types"
                semantic_types_failure_str = f"{file_path=} {chXX_semantic_types_str=}"
                assert _semantic_types_import_count == 1, semantic_types_failure_str
                assert chXX_semantic_types_str in file_str, semantic_types_failure_str

            # check if examples import is from current chapter
            dir_import_count = file_str.count("_env import ")
            if dir_import_count > 0:
                chXX_dir_import_str = f"{chapter_prefix}_env import "
                dir_failure_str = f"{file_path=} {chXX_dir_import_str=}"
                assert dir_import_count == 1, dir_failure_str
                assert chXX_dir_import_str in file_str, dir_failure_str

            is_ref_keywords_file = f"\\{chapter_prefix}_keywords.py" in file_path
            if is_ref_keywords_file:
                # print(f"{file_path=}")
                assert file_str.count("keywords import") == 0, "No imports"
                assert file_str.count("from enum import Enum") == 1, "import Enum"

            for keyword in allowed_chapter_keywords:
                if keyword in file_str:
                    add_ch_keyword_count(keywords_in_ch_count, keyword, chapter_prefix)

    # Check that keyword is not introduced before it is used.
    for keyword, chapters_dict in keywords_in_ch_count.items():
        # for chapter_prefix in sorted(chapters_dict.keys()):
        #     chapter_count = chapters_dict.get(chapter_prefix)
        # print(f"{keyword=} {chapter_prefix=} ")
        never_used_assertion_fail_str = (
            f"The Keyword '{keyword}' is never used in the chapters"
        )
        if not chapters_dict.keys():
            init_ch = keywords_dict[keyword][kw.init_chapter]
            assert init_ch == "", never_used_assertion_fail_str
        else:
            min_chapter_prefix = min(chapters_dict.keys())
            min_chapter_count = chapters_dict.get(min_chapter_prefix)
            ch_count_fail_str = f"{keyword=} {min_chapter_prefix} {min_chapter_count=}"
            # if min_chapter_count <= 2:
            #     print()
            if keyword not in {"semantic_type"}:
                assert min_chapter_count != 1, ch_count_fail_str


def add_ch_keyword_count(keywords_ch_counts: dict, keyword: str, chapter_prefix: str):
    keyword_ch_counts = keywords_ch_counts.get(keyword)
    if keyword_ch_counts.get(chapter_prefix) is None:
        keyword_ch_counts[chapter_prefix] = 0
    keyword_ch_counts[chapter_prefix] += 1


def test_Chapters_FirstLevelFilesDoNotImportKeywords():
    """Test that checks no str function is created before it is needed or after the term is used."""
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # all_file_count = 0
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)

        chapter_files = list(get_dir_file_strs(chapter_dir, include_dirs=False).keys())
        chapter_files = sorted(chapter_files)
        print(f"{chapter_files=}")
        # chapter_file_count = 0
        for filename in chapter_files:
            file_path = create_path(chapter_dir, filename)
            file_str = open_file(file_path)
            print(f"{file_path=}")
            # THEN
            assert "Keywords" not in file_str, f"Keywords reference in {file_path}"
            failure_example_str = f"ExampleStrs reference in {file_path}"
            assert "ExampleStrs " not in file_str, failure_example_str


def test_Chapters_KeywordEnumClassesAreCorrectlyTested():
    """"""
    keywords_dict = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_dict)
    cumlative_ch_keywords_dict = get_cumlative_ch_keywords_dict(keywords_by_chapter)

    chXX_keyword_classes = get_chapter_keyword_classes(cumlative_ch_keywords_dict)
    for chapter_prefix, ExpectedEnumClass in chXX_keyword_classes.items():
        chapter_ref_keywords_path = f"src.ref.keywords"
        print(f"{chapter_ref_keywords_path=}")

        # dynamically import the module
        mod = importlib_import_module(chapter_ref_keywords_path)
        enum_class_name = f"C{chapter_prefix[1:]}Keywords"
        # try:
        #     getattr(mod, enum_class_name)
        # except Exception:
        #     print(f"class {enum_class_name}(str, Enum):")
        #     for keyword in sorted(list(cumlative_ch_keywords_dict.get(chapter_num))):
        #         print(f"    {keyword} = '{keyword}'")
        #     print("def __str__(self): return self.value")

        # print(f"{len(mod.__dict__)=}")
        ChKeywordsClass = getattr(mod, enum_class_name)
        assert ChKeywordsClass
        expected_enum_keys = set(ExpectedEnumClass.__dict__.keys())
        current_enum_keys = set(ChKeywordsClass.__dict__.keys())
        non_found_expected_enum_keys = expected_enum_keys.difference(current_enum_keys)
        assertion_failure_str = (
            f"These were expected but not found: {non_found_expected_enum_keys}"
        )
        assert not non_found_expected_enum_keys, assertion_failure_str
        expected_dunder_str_func = """    def __str__(self):
        return self.value
"""
        assert inspect_getsource(ChKeywordsClass.__str__) == expected_dunder_str_func
        # assert ChKeywordsClass == ExpectedEnumClass
