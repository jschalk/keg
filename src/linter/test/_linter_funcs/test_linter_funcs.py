from linter.style import (
    filename_style_is_correct,
    function_name_style_is_correct,
    get_filenames_with_wrong_style,
    py_file_has_from_imports_only,
)


def test_filename_style_is_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert filename_style_is_correct("get_label.py")
    assert not filename_style_is_correct("get_labelN.py")
    assert not filename_style_is_correct("get_labels.py")
    assert filename_style_is_correct("get_labels.md")
    assert filename_style_is_correct("get_labelN.md")
    assert not filename_style_is_correct("fidels_MOM_IS_WHAT.py")


def test_filenames_style_arg_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_filenames_with_wrong_style({"get_label.py"}) == set()
    assert len(get_filenames_with_wrong_style({"get_labelN.py"})) == 1
    assert len(get_filenames_with_wrong_style({"get_labels.py"})) == 1
    assert get_filenames_with_wrong_style({"get_label.py", "style.json"}) == set()
    assert len(get_filenames_with_wrong_style({"get_label.py", "styles.py"})) == 1


def test_function_name_style_is_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert function_name_style_is_correct("get_label")
    assert not function_name_style_is_correct("get_label_No")
    assert function_name_style_is_correct("get_label_None")
    assert not function_name_style_is_correct("Get_label")
    assert not function_name_style_is_correct("test_get_label")
    assert function_name_style_is_correct("test_get_label_ReturnsObj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj_scenari")
    assert not function_name_style_is_correct("test_get_label_ReturnObj_scenario")
    assert not function_name_style_is_correct("test_GetLabel_exists")
    assert function_name_style_is_correct("test_GetLabel_Exists")
    assert not function_name_style_is_correct("test_get_label_Returnsobj")
    assert not function_name_style_is_correct("test_get_label_returnsobj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj")
    assert not function_name_style_is_correct("test_get_label_ReturnObj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj_correctly")


def test_py_file_has_from_imports_only_ReturnsObj_Scenario0_Allows_from_import():
    code = "from os import path"
    assert py_file_has_from_imports_only(code, None) == True


def test_py_file_has_from_imports_only_ReturnsObj_Scenario1_rejects_plain_import():
    code = "import os"
    assert py_file_has_from_imports_only(code, None) == False


def test_py_file_has_from_imports_only_ReturnsObj_Scenario2_rejects_mixed_imports():
    code = """
from sys import argv
import os
"""
    assert py_file_has_from_imports_only(code, None) == False


def test_py_file_has_from_imports_only_ReturnsObj_Scenario3_rejects_wildcard_import():
    code = "from math import *"
    assert py_file_has_from_imports_only(code, None) == False


def test_py_file_has_from_imports_only_ReturnsObj_Scenario4_allows_multiple_from_imports():
    code = """
from os import path
from sys import argv
"""
    assert py_file_has_from_imports_only(code, None) == True


def test_py_file_has_from_imports_only_ReturnsObj_Scenario5_handles_syntax_error():
    code = "from os import"
    assert py_file_has_from_imports_only(code, None) == False
