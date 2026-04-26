from linter.chapter_move_tools import (
    rename_files_and_dirs_4times,
    string_exists_in_filepaths,
)
from os import getcwd as os_getcwd
from os.path import isdir as os_path_isdir

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.rename_paths -x


def main():
    src_dir = os_getcwd()
    find_str = input("Find string: ").strip()
    replace_str = input("Replace string: ").strip()
    print(f"Goal is to move {find_str} to {replace_str}")

    if os_path_isdir(src_dir) is False:
        print("Error: directory does not exist.")
        return

    # if string_exists_in_filepaths(src_dir, replace_str):
    #     print(f"❌ The new string '{replace_str}' already exists in file paths.")
    #     return

    rename_files_and_dirs_4times(src_dir, find_str, replace_str)
    print("✅ Replacement complete.")


if __name__ == "__main__":
    main()
