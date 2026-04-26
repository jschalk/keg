from ch00_py.file_toolbox import create_path, open_json, save_json
from ch98_docs_builder._ref.ch98_path import create_chapter_ref_path
from linter.chapter_migration_tools import (
    delete_if_empty_or_pycache_only,
    first_level_dirs_with_prefix,
    rename_files_and_dirs_4times,
    replace_in_tracked_python_files,
    string_exists_in_directory,
    string_exists_in_filepaths,
)
from os import (
    getcwd as os_getcwd,
    listdir as os_listdir,
    rename as os_rename,
    walk as os_walk,
)
from os.path import (
    basename as os_path_basename,
    dirname as os_path_dirname,
    exists as os_path_exists,
    isdir as os_path_isdir,
    join as os_path_join,
)
from shutil import rmtree as shutil_rmtree
from subprocess import (
    CalledProcessError as subprocess_CalledProcessError,
    run as subprocess_run,
)

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.ch_move


def first_level_dirs_with_prefix(path_prefix: str):
    """
    Returns all first-level directories that start with `path_prefix`.
    Only includes directories that are direct children of the parent of path_prefix.
    """
    parent_dir = os_path_dirname(path_prefix)
    prefix_name = os_path_basename(path_prefix)

    if not os_path_isdir(parent_dir):
        return []

    result = []
    for entry in os_listdir(parent_dir):
        full_path = os_path_join(parent_dir, entry)
        if entry.startswith(prefix_name) and os_path_isdir(full_path):
            result.append(full_path)

    return result


def delete_if_empty_or_pycache_only(x_dir: str) -> bool:
    """
    Recursively deletes `x_dir` and subdirectories if they are empty
    or only contain __pycache__ directories with .pyc files.
    Returns True if x_dir was deleted, False otherwise.
    """
    if not os_path_isdir(x_dir):
        return False

    # Process subdirectories first (post-order)
    for entry in os_listdir(x_dir):
        full_path = os_path_join(x_dir, entry)
        if os_path_isdir(full_path):
            delete_if_empty_or_pycache_only(full_path)

    # After processing subdirectories, check current dir
    entries = os_listdir(x_dir)
    remaining = []
    for entry in entries:
        full_path = os_path_join(x_dir, entry)
        if entry == "__pycache__" and os_path_isdir(full_path):
            sub_entries = os_listdir(full_path)
            if all(f.endswith(".pyc") for f in sub_entries):
                continue  # safe to ignore
        remaining.append(entry)

    if not remaining:
        print(f"delete empty dir {x_dir}")
        shutil_rmtree(x_dir)
        return True

    return False


def string_exists_in_filepaths(root_dir: str, search_text: str) -> bool:
    """
    Return False if `search_text` does NOT appear in any file path
    (including subdirectories and filenames) under `root_dir`.
    """
    for dirpath, _, filenames in os_walk(root_dir):
        if "__pycache__" not in dirpath:
            for filename in filenames:
                filepath = os_path_join(dirpath, filename)
                if search_text in filepath:
                    print(f"'{search_text}' exists in {filepath=}")
                    return True
    return False


def rename_files_and_dirs_4times(directory: str, old_string: str, new_string: str):
    rename_files_and_dirs(directory, old_string, new_string)
    rename_files_and_dirs(directory, old_string, new_string)
    rename_files_and_dirs(directory, old_string, new_string)
    rename_files_and_dirs(directory, old_string, new_string)


def rename_files_and_dirs(
    directory: str, old_string: str, new_string: str
) -> list[str]:
    # new_string = new_string.lower()
    # old_string = old_string.lower()

    for root, dirs, files in os_walk(directory):
        rename_directories(dirs, root, old_string, new_string)

        if "." not in root:
            # List of file extensions to consider
            file_extensions = ["txt", ".py", ".json", ".ui"]
            for filename in files:
                if any(filename.endswith(ext) for ext in file_extensions):
                    old_file_path = os_path_join(root, filename)
                    new_filename = filename.replace(old_string, new_string)
                    new_file_path = os_path_join(root, new_filename)
                    if old_file_path != new_file_path:
                        os_rename(old_file_path, new_file_path)
                        print(f"{old_string=} {new_string=} {new_file_path=}")


def rename_directories(dirs: list[str], root, old_string: str, new_string: str):
    for d in dirs:
        old_dir_path = os_path_join(root, d)
        new_dir_name = d.replace(old_string, new_string)
        new_dir_path = os_path_join(root, new_dir_name)
        if ".git" not in old_dir_path and old_dir_path != new_dir_path:
            os_rename(old_dir_path, new_dir_path)
            print(f"{old_string=} {new_string=} {new_dir_path=}")


def string_exists_in_directory(root_dir: str, search_text: str) -> bool:
    """
    Return True if `search_text` appears in any file under `root_dir`.
    Searches recursively through all subdirectories.
    """
    for dirpath, _, filenames in os_walk(root_dir):
        for filename in filenames:
            filepath = os_path_join(dirpath, filename)
            if "__pycache__" not in filepath:
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            if search_text in line:
                                print(f"'{search_text}' exists in {filepath=}")
                                return True
                except Exception as e:
                    # Skip unreadable files (permissions, binary, etc.)
                    continue
    return False


def replace_in_tracked_python_files(find_text, replace_text):
    """
    Perform find-and-replace only on tracked .py files in the current git repo.
    """
    try:
        # Get list of tracked .py files
        result = subprocess_run(
            ["git", "ls-files", "*.py", "*.json"],
            capture_output=True,
            text=True,
            check=True,
        )
        tracked_files = result.stdout.strip().split("\n")
    except subprocess_CalledProcessError as e:
        print("Error: not a git repository or unable to list files.")
        return

    for filepath in tracked_files:
        if not filepath or not os_path_exists(filepath):
            continue

        try:
            with open(filepath, "r", encoding="utf-8-sig") as f:
                content = f.read()
            if find_text in content:
                new_content = content.replace(find_text, replace_text)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Find: '{find_text}' Replace: '{replace_text}' {filepath=}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")


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
