from os import getcwd as os_getcwd
from os.path import isdir as os_path_isdir
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch98_docs_builder._ref.ch98_path import create_chapter_ref_path
from src.linter.chapter_migration_tools import (
    delete_if_empty_or_pycache_only,
    first_level_dirs_with_prefix,
    rename_files_and_dirs_4times,
    replace_in_tracked_python_files,
    string_exists_in_directory,
    string_exists_in_filepaths,
)

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.ch_move


def main():
    src_dir = create_path(os_getcwd(), "src")
    src_chxx_str = input("Chapter to move (int): ").strip()
    dst_chxx_str = input("Chapter destina (int): ").strip()
    src_chxx_int = int(src_chxx_str)
    dst_chxx_int = int(dst_chxx_str)
    src_chxx_prefix = f"ch{src_chxx_int:02}"
    dst_chxx_prefix = f"ch{dst_chxx_int:02}"
    src_uppercase_chxx = f"Ch{src_chxx_int:02}"
    dst_uppercase_chxx = f"Ch{dst_chxx_int:02}"
    print(f"Goal is to move {src_chxx_prefix} to {dst_chxx_prefix}")

    # Sanity checks
    dst_chxx_dir_prefix = create_path(src_dir, dst_chxx_prefix)
    x_prefix_dir = ""
    for prefix_dir in first_level_dirs_with_prefix(dst_chxx_dir_prefix):
        print(f"Try to delete {prefix_dir}")
        delete_if_empty_or_pycache_only(prefix_dir)

    if not os_path_isdir(src_dir):
        print("Error: directory does not exist.")
        return

    if string_exists_in_filepaths(src_dir, dst_chxx_prefix):
        print(f"❌ The new string '{dst_chxx_prefix}' already exists in file paths.")
        return

    if string_exists_in_directory(src_dir, dst_chxx_prefix):
        print(f"❌ The new string '{dst_chxx_prefix}' already exists in file contents.")
        return

    # change ref json
    change_ref_json(src_dir, src_chxx_prefix, x_prefix_dir, dst_chxx_int)
    replace_in_tracked_python_files(src_chxx_prefix, replace_text=dst_chxx_prefix)
    replace_in_tracked_python_files(src_uppercase_chxx, dst_uppercase_chxx)
    rename_files_and_dirs_4times(src_dir, src_chxx_prefix, dst_chxx_prefix)
    print("✅ Replacement complete.")


def change_ref_json(src_dir, src_chxx_prefix, prefix_dir: str, dst_chxx_int: int):
    src_chxx_dir_prefix = create_path(src_dir, src_chxx_prefix)
    for src_ch_desc_dir in first_level_dirs_with_prefix(src_chxx_dir_prefix):
        ref_dir = create_path(src_ch_desc_dir, "_ref")
        chapter_ref_json_path = create_path(ref_dir, f"{src_chxx_prefix}_ref.json")
        ref_dict = open_json(chapter_ref_json_path)
        ref_dict["chapter_number"] = dst_chxx_int
        save_json(chapter_ref_json_path, None, ref_dict)
        print(f"Updated ref json '{chapter_ref_json_path}'")


if __name__ == "__main__":
    main()
