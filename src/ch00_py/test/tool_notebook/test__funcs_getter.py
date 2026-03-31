from src.ch00_py.file_toolbox import create_path, save_file
from src.ch00_py.notebook_toolbox import get_top_level_functions
from textwrap import dedent as textwrap_dedent


def test_get_top_level_functions_ReturnsObj_Scenario0_multiple_functions(
    temp3_fs, temp3_dir
):
    # ESTABLISH
    file_str = """
def a():
    pass

def b():
    return 2
"""
    x_file_path = create_path(temp3_dir, "example_tests.py")
    print(file_str)
    save_file(x_file_path, None, file_str)

    # WHEN
    result = get_top_level_functions(x_file_path)

    # THEN
    assert set(result.keys()) == {"a", "b"}
    assert "def a()" in result["a"]
    assert "def b()" in result["b"]


def test_get_top_level_functions_ReturnsObj_Scenario1_ignores_nested_functions(
    temp3_fs, temp3_dir
):
    # ESTABLISH
    file_str = """
def outer():
    def inner():
        return 1
    return inner()
"""
    x_file_path = create_path(temp3_dir, "example_tests.py")
    save_file(x_file_path, None, file_str)

    # WHEN
    result = get_top_level_functions(x_file_path)

    # THEN
    # only top-level functions should appear
    assert list(result.keys()) == ["outer"]
    assert "def inner" in result["outer"]


def test_get_top_level_functions_ReturnsObj_Scenario2_ignores_class_methods(
    temp3_fs, temp3_dir
):
    # ESTABLISH
    file_str = """
class A:
    def method(self):
        return 1

def standalone():
    return 2
"""
    x_file_path = create_path(temp3_dir, "example_tests.py")
    save_file(x_file_path, None, file_str)

    # WHEN
    result = get_top_level_functions(x_file_path)

    # THEN
    assert set(result.keys()) == {"standalone"}
    assert "def standalone()" in result["standalone"]


def test_get_top_level_functions_ReturnsObj_Scenario3_preserves_function_source(
    temp3_fs, temp3_dir
):
    # ESTABLISH
    file_str = '''
def example(x, y):
    """Docstring"""
    z = x + y
    return z
'''
    x_file_path = create_path(temp3_dir, "example_tests.py")
    save_file(x_file_path, None, file_str)

    # WHEN
    result = get_top_level_functions(x_file_path)

    # THEN
    src = result["example"]
    assert '"""Docstring"""' in src
    assert "z = x + y" in src
    print(f"{src[:11]=}")
    assert src[:11] == ("def example")


def test_get_top_level_functions_ReturnsObj_Scenario4_returns_empty_dict_when_no_functions(
    temp3_fs, temp3_dir
):
    # ESTABLISH
    file_str = """
x = 10

class A:
    pass
"""
    x_file_path = create_path(temp3_dir, "example_tests.py")
    save_file(x_file_path, None, file_str)

    # WHEN
    result = get_top_level_functions(x_file_path)

    # THEN
    assert result == {}
