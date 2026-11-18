from ch00_py.file_toolbox import create_path
from os.path import exists as os_path_exists
from pathlib import Path


def get_excel_reader_config_path() -> str:
    "Returns path: ch21_brick/excel_reader.json"
    cwd_path = create_path(create_path("src", "ch21_brick"), "excel_reader.json")
    if os_path_exists(cwd_path):
        return cwd_path
    module_dir = Path(__file__).resolve().parent
    return str(module_dir / "excel_reader.json")
