from ast import (
    FunctionDef as ast_FunctionDef,
    Import as ast_Import,
    ImportFrom as ast_ImportFrom,
    NodeVisitor as ast_NodeVisitor,
    get_docstring as ast_get_docstring,
    get_source_segment as ast_get_source_segment,
    parse as ast_parse,
    walk as ast_walk,
)
from pathlib import Path
from src.ch00_py.file_toolbox import open_file, save_file
from textwrap import dedent as textwrap_dedent
from typing import List


def get_imports_from_source(source: str) -> List[str]:
    """
    Return all import statements found in Python source code.

    Parameters
    ----------
    source : str
        Full Python file contents.

    Returns
    -------
    List[str]
        Import statements reconstructed as strings.
    """
    tree = ast_parse(source)
    imports: list[str] = []

    for node in ast_walk(tree):
        # import x, import x as y
        if isinstance(node, ast_Import):
            parts = []
            for alias in node.names:
                if alias.asname:
                    parts.append(f"{alias.name} as {alias.asname}")
                else:
                    parts.append(alias.name)
            imports.append(f"import {', '.join(parts)}")

        # from x import y
        elif isinstance(node, ast_ImportFrom):
            module = "." * node.level + (node.module or "")

            parts = []
            for alias in node.names:
                if alias.asname:
                    parts.append(f"{alias.name} as {alias.asname}")
                else:
                    parts.append(alias.name)

            imports.append(f"from {module} import {', '.join(parts)}")

    return imports


def get_top_level_functions(file_path) -> dict[str, str]:
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast_parse(source_code)
    functions = {}

    for node in tree.body:
        if isinstance(node, ast_FunctionDef):
            # Get the function name
            func_name = node.name

            # Extract the exact source text of the function
            # (ast.get_source_segment is available in Python 3.8+)
            func_source = ast_get_source_segment(source_code, node)

            # Optional: dedent to remove extra indentation
            if func_source:
                func_source = textwrap_dedent(func_source)

            functions[func_name] = func_source

    return functions


def extract_function_name(function_string):
    # Split the string at the first open bracket
    function_name_part = function_string.split(" ")[1]
    function_name_part = function_name_part.split("(")[0]
    # Strip any extra whitespace and return the function name
    return function_name_part.strip()


def get_marimo_cells(function_str: str) -> List[str]:
    # sourcery skip: remove-redundant-slice-index, str-prefix-suffix
    """
    Split a Python function string into cells using comment boundaries.

    Rules:
    - A comment line creates a new cell.
    - Lines continue in the same cell until a new comment
      appears after a non-comment line.
    - Blank lines belong to the current cell.
    """

    lines = function_str.splitlines(keepends=True)

    cells: list[list[str]] = []
    current_cell: list[str] = []

    def is_comment(line: str) -> bool:
        return line.lstrip()[0:1] == "#"

    prev_was_code = False

    for line in lines:
        comment = is_comment(line)

        # Start new cell when:
        # 1) first comment encountered
        # 2) comment follows code
        if comment and (prev_was_code or not current_cell) and current_cell:
            cells.append(current_cell)
            current_cell = []

        current_cell.append(line)

        # Track whether previous meaningful line was code
        if line.strip() != "":
            prev_was_code = not comment

    if current_cell:
        cells.append(current_cell)

    cells = cells[1:]

    for cell in cells:
        cell.insert(0, "@app.cell\ndef _():\n")
        cell.append("    return\n\n\n")

    # join lines back into strings
    return ["".join(cell) for cell in cells]


def create_marimo_notebook_from_test_str(
    test_file_path: Path, test_func_str: str
) -> str:
    marimo_str = f"""import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup(hide_code=True):
    # source file: {test_file_path}
    # source test name: {extract_function_name(test_func_str)}"""
    test_file_str = open_file(test_file_path)
    imports_list = get_imports_from_source(test_file_str)
    for import_line in imports_list:
        marimo_str += f"\n    {import_line}"

    p_str = "p"
    marimo_str = f"""{marimo_str}
    from sqlite3 import connect as sqlite3_connect

    conn = sqlite3_connect(":memory:")
    cursor0 = conn.cursor()
    {p_str}rint("cursor0 created for SQLite db in memory.")


"""
    cell_strs = get_marimo_cells(test_func_str)
    for cell_str in cell_strs:
        marimo_str = f"{marimo_str}{cell_str}"
    trailer_str = """if __name__ == "__main__":
    app.run()
"""
    marimo_str = f"{marimo_str}{trailer_str}"
    return marimo_str


def save_marimo_notebook_from_test_file(
    test_file_path: Path, testname: str, dest_file_path: Path
) -> str:
    file_top_level_functions = get_top_level_functions(test_file_path)
    test_func_str = file_top_level_functions.get(testname)
    notebook_str = create_marimo_notebook_from_test_str(test_file_path, test_func_str)
    save_file(dest_file_path, None, notebook_str)
