from ast import (
    FunctionDef as ast_FunctionDef,
    Import as ast_Import,
    ImportFrom as ast_ImportFrom,
    NodeVisitor as ast_NodeVisitor,
    get_docstring as ast_get_docstring,
    parse as ast_parse,
    walk as ast_walk,
)
from dataclasses import dataclass
from os import walk as os_walk
from os.path import exists as os_path_exists, join as os_path_join
from pathlib import Path as pathlib_Path
from re import compile as re_compile, search as re_search
from src.ch00_py.dict_toolbox import is_camel_case, uppercase_in_str
from src.ch00_py.file_toolbox import create_path, get_dir_filenames, open_file
from src.ch00_py.keyword_class_builder import get_example_strs_config
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_descs,
    get_func_names_and_class_bases_from_file,
)
from typing import Dict, List, Set, Tuple


def filename_style_is_correct(filename: str) -> bool:
    filename_has_uppercase_char = uppercase_in_str(filename)
    relevant_file_type = filename.endswith(".py") or filename.endswith(".json")
    if relevant_file_type and filename_has_uppercase_char:
        return False
    elif filename.endswith(".py") and filename.endswith("s.py"):
        print(f"{filename} style is wrong. Should not end with 's'.")
        return False
    return True


def get_filenames_with_wrong_style(filenames: set[str]) -> set[str]:
    return {file for file in filenames if not filename_style_is_correct(file)}


def function_name_style_is_correct(function_name: str):
    if not function_name.startswith("test") and "None" not in function_name:
        return uppercase_in_str(function_name) is False
    elif "scenario" in function_name:
        return False
    else:
        func_lower = function_name.lower()
        if func_lower.endswith("exists") and not function_name.endswith("Exists"):
            print(f"{function_name} and Exists")
            return False
        elif "returnsobj" in func_lower and "ReturnsObj" not in function_name:
            print(f"rtr{func_lower=}")
            return False
        elif "returnobj" in func_lower:
            print(f"sdfas{func_lower=}")
            return False
        uppercase_in_str_bool = uppercase_in_str(function_name)
        if not uppercase_in_str_bool:
            print(f"{function_name=}")
            print(f"{uppercase_in_str(function_name)=}")
        return uppercase_in_str_bool


def get_imports_from_file(file_path):
    """
    Parses a Python file and returns a list of lists.
    Each inner list contains:
    - The source chapter from a 'from ... import ...' statement
    - Followed by all imported objects from that chapter

    Example:
    [['pathlib', 'sqrt', 'pi'], ['os.path', 'join']]

    :param file_path: Path to the Python (.py) file
    :return: List of lists: [chapter, imported_obj1, imported_obj2, ...]
    """
    imports = []

    with open(file_path, "r", encoding="utf-8") as file:
        node = ast_parse(file.read(), filename=file_path)

    for n in ast_walk(node):
        if isinstance(n, ast_ImportFrom) and n.module:
            import_entry = [n.module, [alias.name for alias in n.names]]
            imports.append(import_entry)

    return imports


def get_python_files_with_flag(directory, x_str=None) -> dict[str, list]:
    """
    Recursively finds .py files in a directory.
    If x_str is provided, only files with x_str in the filename are included.

    Returns a dictionary: {file_path: 1, ...}

    :param directory: Root directory to search
    :param x_str: Optional substring to filter filenames
    :return: Dictionary of matching file paths and the number 1
    """
    py_files = {}

    for root, _, files in os_walk(directory):
        for file in files:
            if file.endswith(".py") and (x_str is None or x_str in file):
                full_path = os_path_join(root, file)
                py_files[full_path] = get_imports_from_file(full_path)

    return py_files


def get_json_files(directory) -> set[str]:
    json_files = set()

    for root, _, files in os_walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.add(os_path_join(root, file))

    return json_files


def get_semantic_types_filename(chapter_desc_prefix: str) -> str:
    return f"{chapter_desc_prefix}_semantic_types.py"


def get_all_semantic_types_from_ref_files() -> set[str]:
    all_ref_files_semantic_types = set()
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        ref_dir = create_path(chapter_dir, "_ref")
        semantic_types_filename = get_semantic_types_filename(chapter_prefix)
        str_util_path = create_path(ref_dir, semantic_types_filename)
        functions, class_bases = get_func_names_and_class_bases_from_file(str_util_path)
        print(f"{chapter_desc} {class_bases=}")
        all_ref_files_semantic_types.update(class_bases)
    print(all_ref_files_semantic_types)
    return all_ref_files_semantic_types


def add_or_count_function_name_occurance(all_functions: dict, function_name: str):
    if all_functions.get(function_name):
        all_functions[function_name] += 1
    else:
        all_functions[function_name] = 1


def check_if_function_name_repeats(
    file_functions: list,
    all_functions: dict,
    non_excluded_functions: set,
    excluded_functions: dict,
    file_path: str,
    duplicate_func_names: set,
):
    for function_name in file_functions:
        add_or_count_function_name_occurance(all_functions, function_name)
        if function_name in non_excluded_functions:
            print(f"Duplicate function {function_name} in {file_path}")
            duplicate_func_names.add(function_name)
        if function_name not in excluded_functions:
            non_excluded_functions.add(function_name)


@dataclass
class ChaptersObjMetrics:
    all_functions: dict
    duplicate_func_names: set
    unnecessarily_excluded_funcs: dict
    semantic_types: set
    all_classes: dict


def get_chapters_obj_metrics(excluded_functions) -> ChaptersObjMetrics:
    """Reads every python file to track all functions and classes."""
    duplicate_func_names = set()
    non_excluded_functions = set()
    all_functions = {}
    all_classes = {}
    semantic_type_candidates = {}
    for chapter_dir in get_chapter_descs().values():
        filenames_set = get_dir_filenames(chapter_dir, include_extensions={"py"})
        for filenames in filenames_set:
            file_dir = create_path(chapter_dir, filenames[0])
            file_path = create_path(file_dir, filenames[1])
            file_functions, class_bases = get_func_names_and_class_bases_from_file(
                file_path
            )
            for x_class, x_bases in class_bases.items():
                evaluate_and_add_classes(
                    x_bases,
                    file_path,
                    all_classes,
                    x_class,
                    semantic_type_candidates,
                )
            check_if_function_name_repeats(
                file_functions,
                all_functions,
                non_excluded_functions,
                excluded_functions,
                file_path,
                duplicate_func_names,
            )

    print(f"{duplicate_func_names=}")
    # print(f"{duplicate_func_names=}")
    # print(f"{len(non_excluded_functions)=}")
    # print(f"{len(all_functions)=}")
    unnecessarily_excluded_funcs = get_unnecessarily_excluded_funcs(
        all_functions, excluded_functions
    )
    semantic_types = get_semantic_types(semantic_type_candidates)
    return ChaptersObjMetrics(
        all_functions=all_functions,
        duplicate_func_names=duplicate_func_names,
        unnecessarily_excluded_funcs=unnecessarily_excluded_funcs,
        semantic_types=semantic_types,
        all_classes=all_classes,
    )


def check_custom_exception_classes_style(all_classes: dict[str, str]):
    x_count = 0
    for x_class, class_str in all_classes.items():
        if "exception" in class_str.lower():
            x_count += 1
            # print(f"{x_count}. {class_str[26:]}")
            file_path = class_str[26:]
            if not os_path_exists(file_path):
                raise AssertionError("File does not exist")
            file_str = open_file(file_path)
            exception_assert_fail_str = f"Exception #{x_count}: {x_class} {class_str}"
            if file_str.count(x_class) < 2:
                return False, exception_assert_fail_str
            if "Exception" in x_class:
                return False, f"{x_class} should not have Exception in it."
            if not x_class.endswith("Error"):
                return False, f"{x_class} does not end in 'Error'."
            if not is_camel_case(x_class):
                return False, f"{x_class} is not CamelCase."
    return (True, "All Exception classes satisfy style requirements")


def evaluate_and_add_classes(
    x_bases, filename, all_classes: dict, x_class, semantic_type_candidates: dict
):
    if len(x_bases) > 1:
        all_classes[x_class] = (
            f"A class with more than one inheritance. {filename} {x_bases}"
        )
    elif len(x_bases) == 0:
        no_bases_str = f"A class with no inheritance. {filename}"
        all_classes[x_class] = no_bases_str
    elif x_bases == ["Exception"]:
        exception_base_str = f"An Exception inheritance. {filename}"
        all_classes[x_class] = exception_base_str
    elif len(x_bases) == 1:
        one_base_str = f"A single inheritance {filename} {x_bases}"
        all_classes[x_class] = one_base_str
        semantic_type_candidates[x_class] = x_bases


def get_unnecessarily_excluded_funcs(
    all_functions: dict, excluded_functions: set[str]
) -> dict[str, str]:
    unnecessarily_excluded_funcs = {
        function_name: f"{func_count=}. '{function_name}' does not need to be in excluded_functions set"
        for function_name, func_count in all_functions.items()
        if func_count == 1 and function_name in excluded_functions
    }
    for excluded_function in excluded_functions:
        if excluded_function not in all_functions:
            does_not_exist_str = f"'{excluded_function}' is not used in codebase"
            unnecessarily_excluded_funcs[excluded_function] = does_not_exist_str
    # for func_name in sorted(list(all_functions.keys()), reverse=False):
    #     func_count = all_functions.get(func_name)
    # if func_count > 1:
    #     print(f"{func_name} {func_count=}")
    print(f"{len(excluded_functions)=}")
    return unnecessarily_excluded_funcs


def get_semantic_types(semantic_type_candidates) -> set:
    confirmed_semantic_types = {}
    base_types = (int, float, bool, str, list, tuple, range, dict, set)
    # Check if any base is in base_types by name
    candidates_list = list(semantic_type_candidates.keys())

    while candidates_list != []:
        x_class = candidates_list.pop()
        x_bases = semantic_type_candidates.get(x_class)
        is_subclass = any(base in [t.__name__ for t in base_types] for base in x_bases)
        if is_subclass:
            confirmed_semantic_types[x_class] = x_bases[0]
        else:
            x_base = x_bases[0]
            if new_bases := semantic_type_candidates.get(x_base):
                # if x_base exists in semantic_type_candidates change classes bases reference to parent class
                semantic_type_candidates[x_class] = new_bases
                candidates_list.append(x_class)
    # print(f"{sorted(list(confirmed_semantic_types))=}")
    return confirmed_semantic_types


def check_if_chapter_keywords_by_chapter_is_sorted(
    chapter_keywords_by_chapter: list[str],
):
    filtered_ch_str_func = []
    filtered_ch_str_func.extend(
        str_func for str_func in chapter_keywords_by_chapter if str_func != "__str__"
    )
    if filtered_ch_str_func != sorted(filtered_ch_str_func):
        for chapter_str_func in sorted(filtered_ch_str_func):
            chapter_str_func = chapter_str_func.replace("'", "")
            chapter_str_func = chapter_str_func.replace("_str", "")
    sorted_filtered_ch_str_func = sorted(filtered_ch_str_func)
    if filtered_ch_str_func != sorted_filtered_ch_str_func:
        first_wrong_index = None
        for x in range(len(filtered_ch_str_func)):
            # print(f"{filtered_ch_str_func[x]}")
            if (
                not first_wrong_index
                and filtered_ch_str_func[x] != sorted_filtered_ch_str_func[x]
            ):
                first_wrong_index = f"{filtered_ch_str_func[x]} should be {sorted_filtered_ch_str_func[x]}"

        # print(f"{first_wrong_index=}")
        # print(f"Bad Order     {filtered_ch_str_func}")
        # print(f"Correct order {sorted(filtered_ch_str_func)}")
    assert filtered_ch_str_func == sorted(filtered_ch_str_func)


def check_keywords_by_chapter_are_not_duplicated(
    chapter_keywords_by_chapter: list[str], running_str_functions_set: set[str]
):
    running_str_functions_set = set(running_str_functions_set)
    chapter_keywords_by_chapter = set(chapter_keywords_by_chapter)
    if chapter_keywords_by_chapter & running_str_functions_set:
        print(
            f"Duplicate functions: {chapter_keywords_by_chapter & running_str_functions_set}"
        )
    assert not chapter_keywords_by_chapter & running_str_functions_set


def get_docstring(file_path: str, function_name: str) -> str:
    with open(file_path, "r") as f:
        tree = ast_parse(f.read(), filename=file_path)

    return next(
        (
            ast_get_docstring(node)
            for node in ast_walk(tree)
            if isinstance(node, ast_FunctionDef) and node.name == function_name
        ),
        None,
    )


def check_path_funcs_ReturnsObj_TestsExist(
    path_funcs: set, test_path_func_names: set[str]
):
    for path_func in path_funcs:
        pytest_for_func_exists = False
        # print(f"{chapter_desc} {path_func}")
        expected_test_func = f"test_{path_func}_ReturnsObj"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {chapter_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{chapter_desc} {test_func_exists} {path_func}")


def check_path_funcs_HasDocString_TestsExist(
    path_funcs: set, test_path_func_names: set[str]
):
    for path_func in path_funcs:
        pytest_for_func_exists = False
        # print(f"{chapter_desc} {path_func}")
        expected_test_func = f"test_{path_func}_HasDocString"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {chapter_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{chapter_desc} {test_func_exists} {path_func}")


def necessary_comments_exist(function_name: str, test_function_str: str) -> bool:
    establish_exists = "ESTABLISH" in test_function_str
    when_exists = "WHEN" in test_function_str
    then_exists = "THEN" in test_function_str
    establish_when_then_exist = establish_exists and when_exists and then_exists
    if "SQLTEST" in function_name:
        before_str_exists = "BEFORE" in test_function_str
        if not before_str_exists:
            print(f"SQLTEST {function_name} requires BEFORE comment")
        return before_str_exists and establish_when_then_exist
    return establish_when_then_exist


def check_all_test_functions_are_formatted(all_test_functions: dict[str, str]):
    example_strs = get_example_strs_config()
    func_total_count = len(all_test_functions)
    sorted_test_functions_names = sorted(all_test_functions.keys())

    print(f"check all {func_total_count} functions...")
    for function_count, function_name in enumerate(sorted_test_functions_names):
        test_function_str = all_test_functions.get(function_name)
        fail_str = f"Necessary comments like 'ESTABLISH', 'WHEN', 'THEN' are missing in test function '{function_name}'"
        assert necessary_comments_exist(function_name, test_function_str), fail_str
        # check that no test creates it's own cursor in memory
        memory_cursor_fail_str = f"{function_name} init memory cursor"
        if (
            "create_marimo_notebook_from_test_str" not in function_name
            and "test_export_db_to_excel" not in function_name
        ):
            assert ":memory:" not in test_function_str, memory_cursor_fail_str

        # check for each example key in the function str.
        for key_str in sorted(example_strs.keys()):
            value_str = example_strs.get(key_str)
            declare_str = f"""{key_str}_str = "{value_str}"\n"""
            fail2_str = f"#{function_count} of {func_total_count}:'{function_name}' Replace '{declare_str}' with Enum class reference."
            assert declare_str not in test_function_str, fail2_str


_CH_PATTERN = re_compile(r"^src\.ch(\d+)(?:[._]|$)")
_CH_STR_PATTERN = re_compile(r"ch(\d{2})_str(?:[._]|$)")


def _extract_series_number(chapter: str) -> int | None:
    if not chapter:
        return None
    m = _CH_PATTERN.match(chapter)
    return int(m.group(1)) if m else None


def _extract_aXX_str_number(chapter: str) -> int | None:
    if not chapter:
        return None
    m = _CH_STR_PATTERN.search(chapter)
    return int(m.group(1)) if m else None


class _ImportCollector(ast_NodeVisitor):
    def __init__(self, min_number: int):
        self.min_number = min_number
        self.matches: list[str] = []

    def visit_Import(self, node: ast_Import):
        for alias in node.names:
            chapter = alias.name
            # Check src.aXX
            n = _extract_series_number(chapter)
            if n is not None and n > self.min_number:
                s = f"import {chapter}"
                if alias.asname:
                    s += f" as {alias.asname}"
                self.matches.append(s)
            # Check aXX_str
            n2 = _extract_aXX_str_number(chapter)
            if n2 is not None and n2 != self.min_number:
                s = f"import {chapter}"
                if alias.asname:
                    s += f" as {alias.asname}"
                self.matches.append(s)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast_ImportFrom):
        chapter = node.module
        # Check src.aXX
        n = _extract_series_number(chapter) if chapter else None
        if n is not None and n > self.min_number:
            parts = [
                f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
            ]
            self.matches.append(f"from {chapter} import {', '.join(parts)}")
        # Check aXX_str
        n2 = _extract_aXX_str_number(chapter) if chapter else None
        if n2 is not None and n2 != self.min_number:
            parts = [
                f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
            ]
            self.matches.append(f"from {chapter} import {', '.join(parts)}")
        self.generic_visit(node)


def find_incorrect_imports(py_file_path: str, min_number: int) -> list[str]:
    p = pathlib_Path(py_file_path)
    file_text = p.read_text(encoding="utf-8")
    tree = ast_parse(file_text, filename=str(p))
    collector = _ImportCollector(min_number)
    collector.visit(tree)
    return collector.matches


_PATTERN = re_compile(r"^test_(?P<func>.+?)_ReturnsObj(?P<rest>.*)$")

_SCENARIO_PATTERN = re_compile(r"(Scenario\d+)")


def find_matching_tests(test_names: Set[str]) -> List[str]:
    """
    Returns test names that:
    - match: test_<func>_ReturnsObj...
    - contain a ScenarioX anywhere after that
    - have at least one other test with the same (func, ScenarioX)
    """

    groups: Dict[Tuple[str, str], List[str]] = {}

    for name in test_names:
        match = _PATTERN.match(name)
        if not match:
            continue

        func_name = match.group("func")
        rest = match.group("rest")

        scenario_match = _SCENARIO_PATTERN.search(rest)
        if not scenario_match:
            continue

        scenario = scenario_match.group(1)

        key = (func_name, scenario)
        groups.setdefault(key, []).append(name)

    # Flatten only groups with duplicates
    result: List[str] = []
    for names in groups.values():
        if len(names) > 1:
            result.extend(names)

    return result
