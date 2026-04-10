from openpyxl import Workbook as openpyxl_Workbook, load_workbook
from os import listdir as os_listdir
from os.path import join as os_path_join
from pandas import (
    DataFrame,
    ExcelWriter,
    read_excel as pandas_read_excel,
    to_numeric as pandas_to_numeric,
)
from pathlib import Path
from src.ch17_idea.idea_config import get_brick_types
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


def get_excel_sheet_tuples(directory: str) -> List[Tuple[str, str]]:
    """
    Given a directory, returns a sorted list of (filename, sheet_name) tuples
    for all Excel files found in that directory.

    Args:
        directory: Path to the directory to search for Excel files.

    Returns:
        Sorted list of (filename, sheet_name) tuples.
    """
    result = []
    excel_extensions = (".xlsx", ".xlsm", ".xltx", ".xltm")

    for filename in os_listdir(directory):
        if filename.lower().endswith(excel_extensions):
            filepath = os_path_join(directory, filename)
            wb = load_workbook(filepath, read_only=True)
            for sheet_name in wb.sheetnames:
                result.append((filename, sheet_name))
            wb.close()

    return sorted(result)


def get_sheets_with_brick_types(directory: str) -> List[Tuple[str, str]]:
    """
    Returns all (filename, sheet_name) tuples where the sheet_name contains
    any of the provided br_strings.

    Args:
        directory:  Path to the directory to search for Excel files.
        br_strings: Set of strings to match against sheet names.

    Returns:
        Sorted list of (filename, sheet_name) tuples where sheet_name
        contains at least one br_string.
    """
    brick_types = get_brick_types()
    all_tuples = get_excel_sheet_tuples(directory)
    return [
        (filename, sheet_name)
        for filename, sheet_name in all_tuples
        if any(br in sheet_name.lower() for br in brick_types)
    ]


def get_validated_bele_src_brick_type_sheets(
    bele_src_dir: str,
    idea_src_dir: str,
) -> List[Tuple[str, str]]:
    """
    Returns all BR sheets found in bele_src_dir.
    Raises a ValueError if any of those BR sheets also exist in idea_src_dir.

    Args:
        bele_src_dir: Path to the BELE source directory.
        idea_src_dir: Path to the IDEA source directory.

    Returns:
        Sorted list of (filename, sheet_name) tuples from bele_src_dir
        whose sheet_name contains a BR string.

    Raises:
        ValueError: If any BR sheet found in bele_src_dir also exists
                    in idea_src_dir (matched on sheet_name alone).
    """
    bele_br_sheets = get_sheets_with_brick_types(bele_src_dir)
    idea_br_sheets = get_sheets_with_brick_types(idea_src_dir)

    bele_sheet_names = {sheet_name for _, sheet_name in bele_br_sheets}
    idea_sheet_names = {sheet_name for _, sheet_name in idea_br_sheets}

    overlapping = bele_sheet_names & idea_sheet_names
    if overlapping:
        raise ValueError(
            f"BR sheets found in both bele_src_dir and idea_src_dir: "
            f"{sorted(overlapping)}"
        )

    return bele_br_sheets


def beliefs_sheets_to_idea_sheets(
    bele_src_dir: str,
    idea_src_dir: str,
) -> List[Tuple[str, str]]:
    """
    Copies all BR sheets from bele_src_dir into idea_src_dir.
    Each BR sheet is written into its own new Excel file, named after the sheet,
    preserving values and structure for downstream pandas operations.

    Args:
        bele_src_dir: Path to the BELE source directory.
        idea_src_dir: Path to the IDEA source directory.

    Returns:
        Sorted list of (new_filename, sheet_name) tuples for every sheet copied.

    Raises:
        ValueError: (propagated from get_bele_br_sheets_validated) if any BR
                    sheet name exists in both directories before the copy.
    """
    # TODO get max_spark_num from idea_src_dir
    # TODO get face_sparks from bele_src_dir
    # TODO create spark_num, face_spark tuples
    # TODO when being copied over, add spark_num to dataframe
    bele_br_sheets = get_validated_bele_src_brick_type_sheets(
        bele_src_dir, idea_src_dir
    )

    # Group sheet names by their source file for efficient workbook loading
    file_to_sheets: dict[str, List[str]] = {}
    for filename, sheet_name in bele_br_sheets:
        file_to_sheets.setdefault(filename, []).append(sheet_name)

    copied: List[Tuple[str, str]] = []

    for filename, sheet_names in file_to_sheets.items():
        src_path = os_path_join(bele_src_dir, filename)
        src_wb = load_workbook(src_path, data_only=True)  # resolve formulas to values

        for sheet_name in sheet_names:
            src_ws = src_wb[sheet_name]

            dest_wb = openpyxl_Workbook()
            dest_ws = dest_wb.active
            dest_ws.title = sheet_name

            # Copy column dimensions so pandas read_excel gets clean column widths
            for col_idx, col_dim in src_ws.column_dimensions.items():
                dest_ws.column_dimensions[col_idx].width = col_dim.width

            # Copy all cell values row by row (no styling — pandas doesn't need it)
            for row in src_ws.iter_rows():
                for cell in row:
                    dest_ws.cell(
                        row=cell.row,
                        column=cell.column,
                        value=cell.value,
                    )

            new_filename = f"{sheet_name}.xlsx"
            dest_path = os_path_join(idea_src_dir, new_filename)
            dest_wb.save(dest_path)
            copied.append((new_filename, sheet_name))

        src_wb.close()

    return sorted(copied)


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
