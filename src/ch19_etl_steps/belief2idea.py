from os import listdir as os_listdir
from os.path import join as os_path_join
from pandas import (
    DataFrame,
    ExcelWriter,
    read_excel as pandas_read_excel,
    to_numeric as pandas_to_numeric,
)
from pathlib import Path


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


def add_spark_num_column(df: DataFrame, spark_face_spark_nums: dict[str, int]):
    """
    Adds 'spark_num' as the first column based on 'spark_face' values.
    - mutates original DataFrame (does not )
    """
    if "spark_face" not in df.columns:
        # raise ValueError("Column 'spark_face' not found in DataFrame")
        return
    spark_num_series = df["spark_face"].map(spark_face_spark_nums)

    # Insert as first column
    df.insert(0, "spark_num", spark_num_series)


class MigrationConflictError(Exception):
    """Raised when there is a conflict between source and destination Excel sheets."""

    pass


def compare_br_sheets(src_dir: str, dst_dir: str) -> None:
    """
    Compares all sheets containing 'br' in their name in Excel files from src_dir and dst_dir.
    Raises MigrationConflictError if any conflict is found.
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    # Only Excel files
    src_files = [f for f in src_dir.iterdir() if f.suffix.lower() in {".xlsx", ".xls"}]
    dst_files = {
        f.name: f for f in dst_dir.iterdir() if f.suffix.lower() in {".xlsx", ".xls"}
    }

    for src_file in src_files:
        if src_file.name not in dst_files:
            # Could ignore or raise a warning if the dst file doesn't exist
            continue

        dst_file = dst_files[src_file.name]

        # Read all sheets
        src_sheets = pandas_read_excel(src_file, sheet_name=None)
        dst_sheets = pandas_read_excel(dst_file, sheet_name=None)

        # Filter sheets containing 'br'
        filtered_sheet_names = [name for name in src_sheets if "br" in name.lower()]

        for sheet_name in filtered_sheet_names:
            if sheet_name not in dst_sheets:
                raise MigrationConflictError(
                    f"Sheet '{sheet_name}' exists in source but not in destination file '{dst_file.name}'"
                )

            src_df = src_sheets[sheet_name].fillna("").astype(str)
            dst_df = dst_sheets[sheet_name].fillna("").astype(str)

            if not src_df.equals(dst_df):
                raise MigrationConflictError(
                    f"Conflict in sheet '{sheet_name}' between '{src_file.name}' and '{dst_file.name}'"
                )


def update_spark_num_in_excel_file(filepath: str, max_spark_num):
    # Read all sheets
    sheets = pandas_read_excel(filepath, sheet_name=None)
    spark_num = max_spark_num + 1
    # Modify each sheet
    updated_sheets = {}
    for sheet_name, df in sheets.items():
        df["spark_num"] = spark_num  # Add or overwrite
        updated_sheets[sheet_name] = df

    # Write all sheets back to the same file
    with ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for sheet_name, df in updated_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def update_spark_num_in_belief_files(directory: str, max_spark_num: int) -> None:
    """
    Adds or updates the 'spark_num' column with a given value
    in all Excel files in the directory that contain 'belief' in the filename.

    Args:
        directory (str): Path to the directory containing Excel files.
        value: The value to set in the 'spark_num' column.
    """
    for filename in os_listdir(directory):
        is_excel_file = filename.lower().endswith((".xlsx", ".xls"))
        if is_excel_file and "belief" in filename.lower():
            filepath = os_path_join(directory, filename)
            update_spark_num_in_excel_file(filepath, max_spark_num)
