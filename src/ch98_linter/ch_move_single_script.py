from ch00_py.file_toolbox import open_json, save_json
from ch01_keyword.keyword_class_builder import (
    create_src_keywords_src_path,
    get_keywords_src_config,
)
from ch97_docs_builder.glossary_ranking import create_keg_exam_questions_path
from ch98_linter.ch_move_tool import (
    delete_if_empty_or_pycache_only,
    first_level_dirs_with_prefix,
    rename_files_and_dirs_4times,
    replace_in_tracked_python_files,
    string_exists_in_directory,
    string_exists_in_filepaths,
)
from os import getcwd as os_getcwd
from os.path import isdir as os_path_isdir, join as os_path_join
from pathlib import Path

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.chapter_move_main


def ch_move_main():
    src_chxx_str = input("Chapter to move (int): ").strip()
    dst_chxx_str = input("Chapter destina (int): ").strip()
    src_chxx_int = int(src_chxx_str)
    dst_chxx_int = int(dst_chxx_str)
    move_chapters_given_ints(src_chxx_int, dst_chxx_int)


def move_chapters_given_ints(src_chxx_int, dst_chxx_int):
    src_chxx_prefix = f"ch{src_chxx_int:02}"
    dst_chxx_prefix = f"ch{dst_chxx_int:02}"
    src_uppercase_chxx = f"Ch{src_chxx_int:02}"
    dst_uppercase_chxx = f"Ch{dst_chxx_int:02}"
    print(f"Goal is to move {src_chxx_prefix} to {dst_chxx_prefix}")

    # Sanity checks
    dst_chxx_dir_prefix = os_path_join("src", dst_chxx_prefix)
    print(f"{dst_chxx_dir_prefix=}")
    x_prefix_dir = ""
    for prefix_dir in first_level_dirs_with_prefix(dst_chxx_dir_prefix):
        print(f"Try to delete {prefix_dir}")
        delete_if_empty_or_pycache_only(prefix_dir)

    if not os_path_isdir("src"):
        print("Error: directory does not exist.")
        return

    if string_exists_in_filepaths("src", dst_chxx_prefix):
        print(f"❌ The new string '{dst_chxx_prefix}' already exists in file paths.")
        return

    if string_exists_in_directory("src", dst_chxx_prefix):
        print(f"❌ The new string '{dst_chxx_prefix}' already exists in file contents.")
        return

    # file contents
    change_ref_json("src", src_chxx_prefix, x_prefix_dir, dst_chxx_int)
    replace_in_tracked_python_files(src_chxx_prefix, replace_text=dst_chxx_prefix)
    replace_in_tracked_python_files(src_uppercase_chxx, dst_uppercase_chxx)
    # change file paths
    rename_files_and_dirs_4times("src", src_chxx_prefix, dst_chxx_prefix)
    update_keywords_source_valid_ch(src_chxx_int, dst_chxx_int)
    update_keg_questions_csv(src_chxx_prefix, dst_chxx_prefix)
    update_keg_questions_csv(src_uppercase_chxx, dst_uppercase_chxx)
    print("✅ Replacement complete.")


def change_ref_json(src_dir, src_chxx_prefix, prefix_dir: str, dst_chxx_int: int):
    src_chxx_dir_prefix = os_path_join(src_dir, src_chxx_prefix)
    for src_ch_desc_dir in first_level_dirs_with_prefix(src_chxx_dir_prefix):
        ref_dir = os_path_join(src_ch_desc_dir, "_ref")
        chapter_ref_json_path = os_path_join(ref_dir, f"{src_chxx_prefix}_ref.json")
        ref_dict = open_json(chapter_ref_json_path)
        ref_dict["chapter_number"] = dst_chxx_int
        save_json(chapter_ref_json_path, None, ref_dict)
        print(f"Updated ref json '{chapter_ref_json_path}'")


def update_keywords_source_valid_ch(src_chxx_int, dst_chxx_int):
    config_dict = get_keywords_src_config()
    config_dict = replace_valid_ch(config_dict, src_chxx_int, dst_chxx_int)
    save_json(create_src_keywords_src_path("src"), None, config_dict)


def replace_valid_ch(config_dict: dict, src_num: int | str, dst_num: int | str) -> dict:
    src_str = str(src_num)
    dst_str = str(dst_num)

    for config in config_dict.values():
        valid_ch = str(config.get("valid_ch"))
        src_with_colon = f"{src_num}:"

        if valid_ch == src_str:
            config["valid_ch"] = dst_str
        elif valid_ch.startswith(src_with_colon):
            dst_with_colon = f"{dst_num}:"
            new_v_ch = valid_ch.replace(src_with_colon, dst_with_colon)
            config["valid_ch"] = new_v_ch

    return config_dict


def update_keg_questions_csv(old_string, new_string):
    keg_path = create_keg_exam_questions_path("src")
    replace_string_in_csv(keg_path, old_string, new_string)


def replace_string_in_csv(
    csv_file_path: str | Path, old_string: str, new_string: str
) -> None:
    csv_file_path = Path(csv_file_path)
    file_text = csv_file_path.read_text(encoding="utf-8")
    updated_text = file_text.replace(old_string, new_string)
    csv_file_path.write_text(updated_text, encoding="utf-8")


if __name__ == "__main__":
    ch_move_main()
