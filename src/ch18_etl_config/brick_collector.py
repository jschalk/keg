from dataclasses import dataclass
from pandas import read_excel as pandas_read_excel
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.brick_db_tool import get_all_excel_sheet_names
from src.ch17_idea.idea_config import get_brick_types, get_quick_bricks_column_ref


def get_all_excel_bricksheets(dir: str) -> set[tuple[str, str, str]]:
    return get_all_excel_sheet_names(dir, get_brick_types())


@dataclass
class BrickFileRef:
    file_dir: str = None
    filename: str = None
    sheet_name: str = None
    brick_type: str = None

    def get_csv_filename(self) -> str:
        return "" if self.brick_type is None else f"{self.brick_type}.csv"


def get_all_brick_dataframes(dir: str) -> list[BrickFileRef]:
    bricksheets = get_all_excel_bricksheets(dir)
    candidate_bricks = set()
    for dir, filename, sheet_name in bricksheets:
        for brick_type in get_brick_types():
            if sheet_name.find(brick_type) >= 0:
                candidate_bricks.add((dir, filename, sheet_name, brick_type))

    brick_dfs = []
    for dir, filename, sheet_name, brick_type in candidate_bricks:
        brick_columns = get_quick_bricks_column_ref().get(brick_type)
        file_path = create_path(dir, filename)
        df = pandas_read_excel(file_path, sheet_name=sheet_name)
        if brick_columns.issubset(set(df.columns)):
            brick_dfs.append(BrickFileRef(dir, filename, sheet_name, brick_type))
    return brick_dfs
