from ch00_py.dict_toolbox import get_0_if_None
from ch00_py.file_toolbox import delete_dir, set_dir
from ch20_brick.brick_db_tool import create_brick_df_from_file, save_sheet
from ch23_idea_src._ref.ch23_semantic_types import SheetName
from ch23_idea_src.fission_step import run_fission_steps
from ch23_idea_src.idea_config import get_idea_config_dict, is_non_mirror
from dataclasses import dataclass
from openpyxl import load_workbook
from os import listdir as os_listdir
from os.path import join as os_path_join
from pandas import (
    DataFrame,
    read_excel as pandas_read_excel,
    to_numeric as pandas_to_numeric,
)
from pathlib import Path
from re import search as re_search
from typing import List, Tuple


def get_spark_faces_from_df(df: DataFrame) -> set:
    """
    Returns a set of distinct values from the 'spark_face' column.
    NaN values are excluded.
    If the column does not exist, returns an empty set.
    """
    if "spark_face" not in df.columns:
        return set()

    return set(df["spark_face"].dropna().unique().tolist())


def get_spark_faces_from_files(directory) -> set:
    """
    Given a directory, read all Excel files and return a set of all distinct
    spark_face values across all sheets in all files.

    Uses get_spark_faces_from_df for per-sheet extraction.
    """
    all_faces = set()
    directory = Path(directory)

    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in {".xlsx", ".xls"}:
            continue

        # Read all sheets
        sheets = pandas_read_excel(file_path, sheet_name=None)

        for df in sheets.values():
            faces = get_spark_faces_from_df(df)
            all_faces.update(faces)

    return all_faces


def get_max_spark_num_from_files(directory) -> int | None:
    """
    Returns the maximum integer spark_num across all Excel files and sheets.

    - Ignores missing, empty, and non-numeric values
    - Converts floats to ints
    - Returns None if no valid spark_num is found
    """
    directory = Path(directory)
    max_val = None

    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".xlsx", ".xls"}:
            continue

        sheets = pandas_read_excel(file_path, sheet_name=None)
        for df in sheets.values():
            max_val = get_max_spark_num_from_df(df, max_val)
    return max_val


def get_max_spark_num_from_df(df: DataFrame, max_val: int) -> int:
    if "spark_num" not in df.columns:
        return max_val

    # Convert to numeric, coerce errors to NaN
    numeric_series = pandas_to_numeric(df["spark_num"], errors="coerce").dropna()
    if numeric_series.empty:
        return max_val

    # Convert floats to ints
    numeric_series = numeric_series.astype(int)
    current_max = numeric_series.max()
    if max_val is None or current_max > max_val:
        max_val = int(current_max)
    return max_val


def create_spark_face_spark_nums(
    spark_faces: set[str], max_spark_num: int = None
) -> dict[str, int]:
    if max_spark_num is None:
        max_spark_num = 0
    return {
        spark_face: max_spark_num + x_count
        for x_count, spark_face in enumerate(sorted(list(spark_faces)), start=1)
    }


def set_spark_num_column(df: DataFrame, spark_face_spark_nums: dict[str, int]):
    """
    Adds 'spark_num' as the first column based on 'spark_face' values.
    - mutates original DataFrame (does not create new df)
    """
    if "spark_num" in df.columns:
        df.drop(columns=["spark_num"], inplace=True)

    if "spark_face" not in df.columns:
        # raise ValueError("Column 'spark_face' not found in DataFrame")
        return
    spark_num_series = df["spark_face"].map(spark_face_spark_nums)

    # Insert as first column
    df.insert(0, "spark_num", spark_num_series)


@dataclass
class SheetRef:
    src_filename: str
    src_sheet_name: SheetName
    src_ii_bk_type: str = None
    src_idea_type: str = None
    idea_type_exists: bool = None
    dst_brick_type: str = None
    dst_sheet_name: SheetName = None

    def set_src_ii_bk_type(self):
        if ii_match := re_search(r"ii\d{5}", self.src_sheet_name):
            self.src_ii_bk_type = ii_match.group(0)
        elif bk_match := re_search(r"bk\d{5}", self.src_sheet_name):
            self.src_ii_bk_type = bk_match.group(0)
        else:
            self.src_ii_bk_type = None

    def set_idea_type_exists(self, idea_config: dict):
        if self.src_ii_bk_type:
            if self.src_ii_bk_type.startswith("bk"):
                idea_type = f"ii{self.src_ii_bk_type[2:]}"
            else:
                idea_type = self.src_ii_bk_type
            self.idea_type_exists = idea_config.get(idea_type) is not None
            if self.idea_type_exists:
                self.src_idea_type = idea_type
        else:
            self.idea_type_exists = False

    def set_dst_brick_type(self, idea_config: dict):
        config_dict = idea_config.get(self.src_idea_type)
        self.dst_brick_type = config_dict.get("brick_type")

    def set_brick_sheet_name(self):
        if self.idea_type_exists:
            self.dst_sheet_name = self.src_sheet_name.replace(
                self.src_idea_type, self.dst_brick_type
            )
        else:
            self.dst_sheet_name = self.src_sheet_name

    def set_dst_attrs(self, idea_config: dict):
        self.set_src_ii_bk_type()
        self.set_idea_type_exists(idea_config)
        if self.idea_type_exists:
            self.set_dst_brick_type(idea_config)
        self.set_brick_sheet_name()


def get_idea_sheet_refs(directory: str) -> List[SheetRef]:
    idea_config = get_idea_config_dict()
    file_sheet_refs = []
    excel_extensions = (".xlsx", ".xlsm", ".xltx", ".xltm")

    for filename in os_listdir(directory):
        if filename.lower().endswith(excel_extensions):
            filepath = os_path_join(directory, filename)
            wb = load_workbook(filepath, read_only=True)
            wb_sheet_refs = [SheetRef(filename, s_name) for s_name in wb.sheetnames]
            for wb_sheet_ref in wb_sheet_refs:
                wb_sheet_ref.set_src_ii_bk_type()
                wb_sheet_ref.set_dst_attrs(idea_config)
                if wb_sheet_ref.idea_type_exists:
                    file_sheet_refs.append(wb_sheet_ref)
            wb.close()

    return sorted(file_sheet_refs, key=lambda x: (x.src_filename, x.src_sheet_name))


def get_spark_face_spark_nums_from_dir(
    i_src_dir: str, b_src_dir: str, db_max_spark_num: int
) -> dict[str, int]:
    idea_spark_faces = get_spark_faces_from_files(i_src_dir)
    brick_max_spark_num = get_0_if_None(get_max_spark_num_from_files(b_src_dir))
    calc_max_spark_num = max(brick_max_spark_num, get_0_if_None(db_max_spark_num))
    return create_spark_face_spark_nums(idea_spark_faces, calc_max_spark_num)


def validate_idea_columns(
    df: DataFrame, config: dict, strict: bool
) -> DataFrame | None:
    """Validates that the DataFrame contains all columns defined in config src_columns.
    Raises ValueError if strict, returns None if not."""
    expected = set(config.get("src_columns", []))
    missing = expected - set(df.columns)
    if missing:
        if strict:
            raise ValueError(
                f"validate_idea_columns found missing source columns: {missing}. "
                f"Expected: {expected}. "
                f"Present: {set(df.columns)}."
            )
        return None
    return df


def ideas_sheets_to_brick_sheets(
    i_src_dir: str, b_src_dir: str, db_max_spark_num: int = None
) -> List[Tuple[str, str]]:
    """
    Copies all brick_type sheets from i_src_dir into b_src_dir.
    Each brick_type sheet is written into its own new Excel file, named after the sheet,
    preserving values and structure for downstream pandas operations.

    Args:
        i_src_dir: Path to the IDEA source directory.
        b_src_dir: Path to the BRICK source directory.

    Returns:
        Sorted list of (new_filename, sheet_name) tuples for every sheet copied.

    Raises:
        ValueError: (propagated from get_idea_bk_sheets_validated) if any BR
                    sheet name exists in both directories before the copy.
    """

    spark_face_spark_nums = get_spark_face_spark_nums_from_dir(
        i_src_dir, b_src_dir, db_max_spark_num
    )
    idea_sheet_refs = get_idea_sheet_refs(i_src_dir)
    idea_config_dict = get_idea_config_dict()
    for idea_sheet_ref in idea_sheet_refs:
        src_path = os_path_join(i_src_dir, idea_sheet_ref.src_filename)
        dst_path = os_path_join(b_src_dir, idea_sheet_ref.src_filename)
        idea_df = create_brick_df_from_file(src_path, idea_sheet_ref.src_sheet_name)
        set_spark_num_column(idea_df, spark_face_spark_nums)
        if is_non_mirror(idea_sheet_ref.src_idea_type):
            idea_type_config = idea_config_dict.get(idea_sheet_ref.src_idea_type)
            x_fission_steps = idea_type_config.get("fission_steps")
            idea_df = run_fission_steps(idea_df, x_fission_steps)
        save_sheet(dst_path, idea_sheet_ref.dst_sheet_name, idea_df, False)

    delete_dir(i_src_dir)
    set_dir(i_src_dir)
    return idea_sheet_refs
