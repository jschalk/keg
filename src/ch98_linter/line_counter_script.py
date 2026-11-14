from os import walk as os_walk
from os.path import join as os_path_join


def count_code_and_pytest_lines(directory, extensions=None, ignore_hidden=True):
    """
    Count total lines of code and pytest-related lines in a directory (recursively).

    Args:
        directory (str): Path to directory.
        extensions (set[str]): File extensions to include (default .py).
        ignore_hidden (bool): Whether to skip hidden files and folders.

    Returns:
        dict: {'total': int, 'pytest': int}
    """
    if extensions is None:
        extensions = {".py"}
    total_lines = 0
    pytest_lines = 0

    for root, dirs, files in os_walk(directory):
        if ignore_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

        for file in files:
            if not any(file.endswith(ext) for ext in extensions):
                continue

            filepath = os_path_join(root, file)
            try:
                with open(filepath, encoding="utf-8") as f:
                    lines = [line for line in f if line.strip()]
                    n_lines = len(lines)
                    total_lines += n_lines

                    # Identify pytest code
                    if (
                        file.startswith("test_")
                        or file.endswith("_test.py")
                        or any(
                            "pytest" in line or "import pytest" in line
                            for line in lines
                        )
                    ):
                        pytest_lines += n_lines
            except (UnicodeDecodeError, PermissionError):
                continue

    return {"total": total_lines, "pytest": pytest_lines}


if __name__ == "__main__":
    src_dir = input("src dir: ").strip()
    x_dict = count_code_and_pytest_lines(src_dir)
    for lines_key, lines_value in x_dict.items():
        print(f"{lines_key} lines: {lines_value}")
