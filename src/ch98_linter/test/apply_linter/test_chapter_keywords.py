from ch00_py.file_toolbox import create_path, open_file, save_json, save_file
from ch01_keyword.keyword_class_builder import (
    get_ch_int,
    get_chapter_keyword_classes,
    get_cumlative_keywords_src_dict,
    get_keywords_by_chapter,
    get_keywords_src_config,
    create_src_keywords_src_path,
)
from ch01_keyword._ref.ch01_path import create_keywords_classes_file_path
from ch01_keyword.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
    create_src_keywords_src_path,
    get_chapter_descs,
    get_cumlative_keywords_src_dict,
)
from ch97_docs_builder.doc_builder import get_chapter_desc_prefix, get_chapter_descs
from ch98_linter.style import (
    check_custom_exception_classes_style,
    find_matching_tests,
    function_name_style_is_correct,
    get_all_semantic_types_from_ref_files,
    get_chapters_obj_metrics,
    get_json_files,
    get_keyword_scope_files,
    get_semantic_types_filename,
    py_file_has_from_imports_only,
)
from ch99_glossary.ch_keyword import Ch98Keywords as kw
from importlib import import_module as importlib_import_module
from inspect import getsource as inspect_getsource
from typing import Literal


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
        "__init__",
        "__str__",
        "set_label",
        "reveal_aux",
        "label_exists",
        "del_iux2aux",
        "iux_exists",
        "get_aux_value",
        "set_iux2aux",
        "set_all_iux2aux",
        "iux2aux_exists",
        "_is_aux_knot_inclusion_correct",
        "_is_iux_knot_inclusion_correct",
        "del_label",
        "get_inx_value",  # used in Nabu/Jargon
        "_is_inx_knot_inclusion_correct",  # used in Nabu/Jargon
        "_is_otx_knot_inclusion_correct",  # used in Nabu/Jargon
        "_check_core_attrs_match",
        "unknown_str_in_otx2inx",  # RopeMap replaces the inherited MapCore implementation
        "del_otx2inx",  # used in Nabu/Jargon
        "find_replace_rope",  # used by ReasonUnit, CaseUnit, FactUnit classes
        "get_obj_key",
        "is_valid",
        "otx_exists",  # used in Nabu/Jargon
        "otx2inx_exists",  # used in Nabu/Jargon
        "reveal_inx",  # used in Nabu/Jargon
        "set_all_otx2inx",  # RopeMap replaces the inherited MapCore implementation
        "set_knot",
        "set_otx2inx",  # used in Nabu/Jargon
        "to_dict",  # used to return class custom dictionary, usually for json file storage
        # "_run",  # exists in etl app and used in pip install tests
        '_state_path',  # exists in etl app and must be recreated in tests
        '_load_state',  # exists in etl app and must be recreated in tests
        '_on_close',  # exists in etl app and must be recreated in tests
        '_save_state',  # exists in etl app and must be recreated in tests
        '_print_punch_text',  # exists in etl app and must be recreated in tests
    }

    # WHEN
    chapters_func_class_metrics = get_chapters_obj_metrics(excluded_functions)
    duplicate_func_names = chapters_func_class_metrics.duplicate_func_names
    unnecessarily_excluded_funcs = (
        chapters_func_class_metrics.unnecessarily_excluded_funcs
    )
    all_classes = chapters_func_class_metrics.all_classes
    exception_check_result = check_custom_exception_classes_style(all_classes)
    print(f"{exception_check_result=}")
    assert exception_check_result[0], exception_check_result[1]

    semantic_types = chapters_func_class_metrics.semantic_types
    all_functions = chapters_func_class_metrics.all_functions

    # THEN
    matching_tests = find_matching_tests(all_functions)
    assert not matching_tests

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


def is_py_file_allowed_any_imports(file_path: str) -> bool:
    files_with_all_imports_allowed = {
        "test_entry_presistence.py",
        "test_print_punch_text.py",
    }
    return any(file in file_path for file in files_with_all_imports_allowed)


def get_keywords_in_ch_count(keywords_dict: dict) -> dict:
    # new method references from keywords config file
    all_keywords = set(keywords_dict.keys())
    keywords_in_ch_count = {keyword: {} for keyword in keywords_dict}
    filtered_chapter_descs = {
        chapter_desc: x_value
        for chapter_desc, x_value in get_chapter_descs().items()
        if chapter_desc != "ch99_glossary"
    }
    # WHEN / THEN
    # all_file_count = 0
    for chapter_desc, chapter_dir in filtered_chapter_descs.items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_files = sorted(get_keyword_scope_files(chapter_dir))
        chapter_files.extend(list(get_json_files(chapter_dir)))
        chapter_files = sorted(chapter_files)
        for file_path in chapter_files:
            file_str = open_file(file_path)
            for keyword in all_keywords:
                if keyword in file_str:
                    add_ch_keyword_count(keywords_in_ch_count, keyword, chapter_prefix)

    return keywords_in_ch_count


def get_expected_ch_config() -> dict:
    keywords_dict = get_keywords_src_config()
    keywords_in_ch_count = get_keywords_in_ch_count(keywords_dict)
    expected_ch_config = {}
    for keyword, chapters_dict in keywords_in_ch_count.items():
        expected_keyword_ch_set = {
            int(ch_prefix[2:4]) for ch_prefix in sorted(chapters_dict.keys())
        }
        expected_keyword_ch_str = ""
        expected_keyword_ch_str = ", ".join(map(str, sorted(expected_keyword_ch_set)))
        #     chapter_count = chapters_dict.get(chapter_prefix)
        # print(f"{keyword=} {expected_keyword_ch_str=} ")
        expected_ch_config[keyword] = {"valid_ch": expected_keyword_ch_str}
        if current_sort_ordinal := keywords_dict.get(keyword).get(kw.sort_ordinal):
            expected_ch_config[keyword]["sort_ordinal"] = current_sort_ordinal
        if current_semantic_type := keywords_dict.get(keyword).get(kw.semantic_type):
            expected_ch_config[keyword]["semantic_type"] = current_semantic_type
    return expected_ch_config


def test_SpecialBuild_get_keywords_src_config(rebuild_keyword_src):
    # ESTABLISH / WHEN / THEN
    # sourcery skip: extract-method, no-conditionals-in-tests
    if not rebuild_keyword_src:
        return
    old_keywords_dict = get_keywords_src_config()
    expected_ch_config = get_expected_ch_config()
    for keyword_str, keyword_chs in expected_ch_config.items():
        if keyword_str.startswith("hon"):
            print(f"{keyword_str}: '{keyword_chs}'")
    src_keywords_src_path = create_src_keywords_src_path("src")
    prev_and_curr_keyword_file_are_same = old_keywords_dict == expected_ch_config
    print(f"{prev_and_curr_keyword_file_are_same=}")
    if not prev_and_curr_keyword_file_are_same:
        print(
            "Create and save keyword_src_config file, fail test if there are any changes so changes can apply to next test run. "
        )
        save_json(src_keywords_src_path, None, expected_ch_config)
        keywords_classes_file_path = create_keywords_classes_file_path("src")
        enum_classes_str = create_all_enum_keyword_classes_str()
        save_file(keywords_classes_file_path, None, enum_classes_str)
    assertion_failure_str = (
        "Special case: keyword_src_config & ch_keyword.py were changed. Run test again."
    )
    assert prev_and_curr_keyword_file_are_same, assertion_failure_str


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
    cumlative_keywords_src_dict = get_cumlative_keywords_src_dict(keywords_by_chapter)
    filtered_chapter_descs = {
        chapter_desc: x_value
        for chapter_desc, x_value in get_chapter_descs().items()
        if chapter_desc != "ch99_glossary"
    }
    # WHEN / THEN
    # all_file_count = 0
    for chapter_desc, chapter_dir in filtered_chapter_descs.items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_int = get_ch_int(chapter_desc)
        allowed_chapter_keywords = cumlative_keywords_src_dict.get(chapter_int)
        not_allowed_keywords = all_keywords_set.difference(allowed_chapter_keywords)
        not_allowed_keywords = sorted(not_allowed_keywords.difference(excluded_strs))
        # print(f"{chapter_prefix} {len(not_allowed_keywords)=}")

        # TODO confirm add .md and .txt and .json files to chapter files
        chapter_files = sorted(get_keyword_scope_files(chapter_dir))
        chapter_files.extend(list(get_json_files(chapter_dir)))
        chapter_files = sorted(chapter_files)
        # chapter_file_count = 0
        for file_path in chapter_files:
            for x_keyword in not_allowed_keywords:
                if x_keyword not in {kw.semantic_type, kw.src, "crud"}:
                    if x_keyword in file_path:
                        print(f"{file_path=} {x_keyword=}")
                    assert x_keyword not in file_path
            # print(f"{chapter_prefix} {file_path=}")
            # chapter_file_count += 1
            # all_file_count += 1
            # print(f"{all_file_count} Chapter: {chapter_file_count} {file_path}")
            file_str = open_file(file_path)
            check_not_allowed_keywords(
                not_allowed_keywords, file_str, chapter_prefix, file_path
            )
            if file_path.endswith(".py") or file_path.endswith(".json"):
                assert does_not_allowed_from_src_import_exist(file_str, file_path)
                allowed_any_import = is_py_file_allowed_any_imports(file_path)
                has_from_imports_only = py_file_has_from_imports_only(
                    file_str, file_path
                )
                assert has_from_imports_only or allowed_any_import, file_path

                is_ref_keywords_file = f"\\{chapter_prefix}_ch_keyword.py" in file_path
                if is_ref_keywords_file:
                    # print(f"{file_path=}")
                    assert file_str.count("keywords import") == 0, "No imports"
                    assert file_str.count("from enum import Enum") == 1, "import Enum"
    expected_ch_config = get_expected_ch_config()
    assert len(expected_ch_config) == len(keywords_dict)
    assert len(expected_ch_config) == 850
    assertion_failure_str = "keyword_src.json has conflicts with generated keyword_src dict. To make file generated version rerun tests with 'rebuild_keyword_src'."
    assert keywords_dict == expected_ch_config, assertion_failure_str


def does_not_allowed_from_src_import_exist(
    file_str: str, file_path
) -> tuple[Literal[False]] | Literal[True]:
    if "from " in file_str:
        return False, f"file {file_path} should not have 'from '"
    return True, ""


def check_not_allowed_keywords(
    not_allowed_keywords: list, file_str: str, chapter_prefix: str, file_path: str
):
    for keyword in not_allowed_keywords:
        if keyword != "ch99":
            notallowed_keyword_failure_str = f"keyword '{keyword}' is not allowed in chapter {chapter_prefix}. It is in {file_path=}"
            if keyword in {"fact", "factory"}:
                # Special case, doesn't provide perfect check but better than nothing
                if keyword in file_str and "row_factory" not in file_str:
                    assert False, notallowed_keyword_failure_str
            else:
                if keyword in file_str:
                    print(f"{keyword=}")
                    print(f"{file_path=}")
                assert keyword not in file_str, notallowed_keyword_failure_str


def add_ch_keyword_count(keywords_ch_counts: dict, keyword: str, chapter_prefix: str):
    keyword_ch_counts = keywords_ch_counts.get(keyword)
    if keyword_ch_counts.get(chapter_prefix) is None:
        keyword_ch_counts[chapter_prefix] = 0
    keyword_ch_counts[chapter_prefix] += 1


def test_Chapters_KeywordEnumClassesAreCorrectlyTested():
    """"""
    # ESTABLISH
    keywords_dict = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_dict)
    cumlative_keywords_src_dict = get_cumlative_keywords_src_dict(keywords_by_chapter)

    chXX_keyword_classes = get_chapter_keyword_classes(cumlative_keywords_src_dict)
    # WHEN / THEN
    for chapter_prefix, ExpectedEnumClass in chXX_keyword_classes.items():
        chapter_ref_keywords_path = f"src.ch99_glossary.ch_keyword"
        print(f"{chapter_ref_keywords_path=}")

        # dynamically import the module
        mod = importlib_import_module(chapter_ref_keywords_path)
        enum_class_name = f"C{chapter_prefix[1:]}Keywords"
        # try:
        #     getattr(mod, enum_class_name)
        # except Exception:
        #     print(f"class {enum_class_name}(str, Enum):")
        #     for keyword in sorted(list(cumlative_keywords_src_dict.get(chapter_num))):
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
