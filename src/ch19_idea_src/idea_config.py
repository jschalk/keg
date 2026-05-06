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


def get_idea_types() -> set:
    return {
        "ii00001",
        "ii00002",
        "ii00005",
        "ii00007",
        "ii00015",
        "ii00100",
        "ii00101",
        "ii00102",
        "ii00103",
        "ii00104",
        "ii00105",
        "ii00106",
        "ii00112",
        "ii00119",
        "ii00120",
        "ii00121",
        "ii00122",
        "ii00123",
        "ii00124",
        "ii00125",
        "ii00126",
        "ii00127",
        "ii00128",
        "ii00129",
        "ii00136",
        "ii00142",
        "ii00143",
        "ii00144",
        "ii00145",
        "ii00150",
        "ii00151",
        "ii00152",
        "ii00153",
        "ii00154",
        "ii00155",
        "ii00156",
        "ii00157",
        "ii00158",
        "ii00159",
        "ii00170",
        "ii00171",
        "ii00172",
        "ii00173",
        "ii00174",
    }
