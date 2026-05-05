from ch00_py.db_toolbox import get_sorted_cols_only_list
from ch00_py.file_toolbox import create_path, get_json_filename, open_json
from enum import Enum
from os import getcwd as os_getcwd
from ref.sorter import get_keg_elements_sort_order


def idea_config_path() -> str:
    "Returns path: ch19_idea_src/idea_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch19_idea_src")
    return create_path(chapter_dir, "idea_config.json")


def get_idea_config_dict() -> dict:
    return open_json(idea_config_path())
