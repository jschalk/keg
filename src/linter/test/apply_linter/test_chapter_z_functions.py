from ch00_py.chapter_desc_main import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
)
from ch00_py.file_toolbox import create_path, get_dir_filenames
from ch00_py.notebook_toolbox import get_top_level_functions
from ch98_docs_builder.doc_builder import get_chapter_descs
from linter.style import (
    check_all_test_functions_are_formatted,
    check_path_funcs_HasDocString_TestsExist,
    check_path_funcs_ReturnsObj_TestsExist,
    find_incorrect_imports,
    get_docstring,
    get_python_files_with_flag,
)
from os.path import exists as os_path_exists


def test_Chapters_AllImportsAreFromLibrariesInLessThanEqual_aXX():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    chapter_descs = get_chapter_descs()
    mod_descs_sorted = sorted(list(chapter_descs.keys()))

    # WHEN / THEN
    all_file_count = 0
    for chapter_desc in mod_descs_sorted:
        chapter_dir = chapter_descs.get(chapter_desc)
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        print(f"{chapter_desc=}")
        desc_number_int = int(chapter_desc_str_number)
        chapter_files = sorted(list(get_python_files_with_flag(chapter_dir).keys()))
        # print(f"{desc_number_str} src.{chapter_desc}")
        for chapter_file_count, file_path in enumerate(chapter_files, start=1):
            all_file_count += 1
            incorrect_imports = find_incorrect_imports(file_path, desc_number_int)
            if len(incorrect_imports) == 1 and file_path.find("_keywords.py") > 0:
                incorrect_imports = []

            assertion_fail_str = f"File #{all_file_count} a{chapter_desc_str_number} file #{chapter_file_count} Imports: {len(incorrect_imports)} {file_path}"
            assert not incorrect_imports, assertion_fail_str


def test_Chapters_path_FunctionStructureAndFormat():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    x_count = 0
    path_functions = {}
    all_test_functions = {}
    chapters_path_funcs = {}
    filtered_chapters_path_funcs = {}
    filterout_path_funcs = {
        "create_path",
        "create_directory_path",
        "rope_is_valid_dir_path",
    }
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        filenames_set = get_dir_filenames(chapter_dir, include_extensions={"py"})
        filtered_path_funcs = set()
        path_func_set = set()
        chapters_path_funcs[chapter_desc] = path_func_set
        filtered_chapters_path_funcs[chapter_desc] = filtered_path_funcs
        for filepath_set in filenames_set:
            file_dir = create_path(chapter_dir, filepath_set[0])
            file_path = create_path(file_dir, filepath_set[1])
            file_functions = get_top_level_functions(file_path)
            for function_name in file_functions.keys():
                x_count += 1
                if str(function_name).endswith("_path"):
                    # print(
                    #     f"Function #{x_count}: Path function {function_name} in {file_path}"
                    # )
                    path_functions[function_name] = file_path
                    path_func_set.add(function_name)
                    if (
                        not str(function_name).endswith("config_path")
                        and function_name not in filterout_path_funcs
                    ):
                        filtered_path_funcs.add(function_name)
                if str(function_name).startswith("test_"):
                    function_str = file_functions.get(function_name)
                    all_test_functions[function_name] = function_str

    print(f"Total path functions found: {len(path_functions)}")
    # THEN
    for function_name, file_path in path_functions.items():
        func_docstring = get_docstring(file_path, function_name)
        # if not func_docstring:
        #     print(f"docstring for {function_name} is None")
        # else:
        #     print(
        #         f"docstring for {function_name}: \t{func_docstring.replace("\n", "")}"
        #     )
        assert func_docstring is not None, function_name

    # print(f"Path functions: {path_functions.keys()=}")
    # for chapter_desc, path_funcs in chapters_path_funcs.items():
    #     print(f"{chapter_desc=} {path_funcs=}")

    for chapter_desc, chapter_dir in get_chapter_descs().items():
        if len(filtered_chapters_path_funcs.get(chapter_desc)) > 0:
            chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
            path_func_filename = f"{chapter_desc_prefix}_path.py"
            _ref_dir = create_path(chapter_dir, "_ref")
            path_func_library = create_path(_ref_dir, path_func_filename)
            path_funcs = filtered_chapters_path_funcs.get(chapter_desc)
            assert os_path_exists(path_func_library)

            test_dir = create_path(chapter_dir, "test")
            util_dir = create_path(test_dir, "_util")
            pytest_path_func_filename = f"test_{path_func_filename}"
            pytest_path_func_path = create_path(util_dir, pytest_path_func_filename)
            assert os_path_exists(pytest_path_func_path)
            test_path_func_names = set(
                get_top_level_functions(pytest_path_func_path).keys()
            )
            # print(f"{chapter_desc} {test_path_func_names=}")
            check_path_funcs_ReturnsObj_TestsExist(path_funcs, test_path_func_names)
            check_path_funcs_HasDocString_TestsExist(path_funcs, test_path_func_names)

    check_all_test_functions_are_formatted(all_test_functions)
