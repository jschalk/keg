from os.path import exists as os_path_exists, join as os_path_join
from pandas import (
    DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    isna as pandas_isna,
    read_excel as pandas_read_excel,
)
from pathlib import Path
from pytest import fixture as pytest_fixture, raises as pytest_raises
from src.ch00_py.file_toolbox import create_path
from src.ch19_etl_steps.belief2idea import (  # move_b_src_sheets_to_i_src,
    MigrationConflictError,
    add_spark_num_column,
    compare_br_sheets,
    create_spark_face_spark_nums,
    get_excel_sheet_tuples,
    get_max_spark_num_from_files,
    get_spark_faces_from_df,
    get_spark_faces_from_files,
    update_spark_num_in_belief_files,
    update_spark_num_in_excel_file,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_get_spark_faces_from_df_ReturnsObj_Scenario0_Basic():
    # ESTABLISH
    df = DataFrame({kw.spark_face: ["a", "b", "a", "c"]})
    # WHEN
    result = get_spark_faces_from_df(df)
    # THEN
    assert result == {"a", "b", "c"}


def test_get_spark_faces_from_df_ReturnsObj_Scenario1_excludes_nulls():
    # ESTABLISH
    df = DataFrame({kw.spark_face: ["a", None, "b", float("nan")]})
    # WHEN
    result = get_spark_faces_from_df(df)
    # THEN
    assert result == {"a", "b"}


def test_get_spark_faces_from_df_ReturnsObj_Scenario2_MissingColumnReturnsEmptySet():
    # ESTABLISH
    df = DataFrame({"other_col": [1, 2, 3]})
    # WHEN
    result = get_spark_faces_from_df(df)
    # THEN
    assert result == set()


def test_get_spark_faces_from_files_ReturnsObj_Scenario0_Multiple_files(tmp_path):
    # ESTABLISH
    file1 = tmp_path / "file1.xlsx"
    file2 = tmp_path / "file2.xlsx"

    df1 = DataFrame({kw.spark_face: ["a", "b"]})
    df2 = DataFrame({kw.spark_face: ["b", "c"]})

    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)
    # WHEN
    result = get_spark_faces_from_files(tmp_path)
    # THEN
    assert result == {"a", "b", "c"}


def test_get_spark_faces_from_files_ReturnsObj_Scenario1_Multiple_sheets(tmp_path):
    # ESTABLISH
    file1 = tmp_path / "file1.xlsx"

    df1 = DataFrame({kw.spark_face: ["a"]})
    df2 = DataFrame({kw.spark_face: [exx.sue]})

    with pandas_ExcelWriter(file1) as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)
    # WHEN
    result = get_spark_faces_from_files(tmp_path)
    # THEN
    assert result == {"a", exx.sue}


def test_get_spark_faces_from_files_ReturnsObj_Scenario2_IgnoresMissingColumn(tmp_path):
    # ESTABLISH
    file1 = tmp_path / "file1.xlsx"

    df1 = DataFrame({kw.spark_face: ["a"]})
    df2 = DataFrame({"other": [1, 2]})  # no spark_face column

    with pandas_ExcelWriter(file1) as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)
    # WHEN
    result = get_spark_faces_from_files(tmp_path)
    # THEN
    assert result == {"a"}


def test_get_max_spark_num_from_files_ReturnsObj_Scenario0_MultipleFiles(tmp_path):
    # ESTABLISH
    file1 = tmp_path / "file1.xlsx"
    file2 = tmp_path / "file2.xlsx"
    df1 = DataFrame({kw.spark_num: [1, 2, 3]})
    df2 = DataFrame({kw.spark_num: [4, 5]})
    df1.to_excel(file1, index=False)
    df2.to_excel(file2, index=False)
    # WHEN
    result = get_max_spark_num_from_files(tmp_path)
    # THEN
    assert result == 5


def test_get_max_spark_num_from_files_ReturnsObj_Scenario1_IgnoresInvalidAndConvertsFloats(
    tmp_path,
):
    # ESTABLISH
    file1 = tmp_path / "file1.xlsx"
    df = DataFrame({kw.spark_num: ["10", "bad", None, 7.9]})  # 7.9 -> 7
    df.to_excel(file1, index=False)
    # WHEN
    result = get_max_spark_num_from_files(tmp_path)
    # THEN
    assert result == 10


def test_get_max_spark_num_from_files_ReturnsObj_Scenario2_MultipleSheetsAndMissingColumn(
    tmp_path,
):
    # ESTABLISH
    file1 = tmp_path / "file1.xlsx"
    df1 = DataFrame({kw.spark_num: [1, 20]})
    df2 = DataFrame({"other": [100, 200]})  # no spark_num
    df3 = DataFrame({kw.spark_num: [15]})
    with pandas_ExcelWriter(file1) as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)
        df3.to_excel(writer, sheet_name="Sheet3", index=False)

    # WHEN
    result = get_max_spark_num_from_files(tmp_path)
    # THEN
    assert result == 20


def test_create_spark_face_spark_nums_ReturnsObj_Scenario0_Simple():
    # ESTABLISH
    spark_faces = {exx.sue, exx.bob, exx.yao}
    max_spark_num = 11
    # WHEN
    x_dict = create_spark_face_spark_nums(spark_faces, max_spark_num)
    # THEN
    assert x_dict == {exx.bob: 12, exx.sue: 13, exx.yao: 14}


def test_create_spark_face_spark_nums_ReturnsObj_Scenario1_max_spark_num_IsNone():
    # ESTABLISH
    spark_faces = {exx.sue, exx.bob, exx.yao}
    max_spark_num = None
    # WHEN
    x_dict = create_spark_face_spark_nums(spark_faces, max_spark_num)
    # THEN
    assert x_dict == {exx.bob: 1, exx.sue: 2, exx.yao: 3}


def test_create_spark_face_spark_nums_ReturnsObj_Scenario2_No_max_spark_num():
    # ESTABLISH
    spark_faces = {exx.sue, exx.bob, exx.yao}
    # WHEN
    x_dict = create_spark_face_spark_nums(spark_faces)
    # THEN
    assert x_dict == {exx.bob: 1, exx.sue: 2, exx.yao: 3}


def test_add_spark_num_column_SetsAttr_Scenario0_Add_spark_num_Basic():
    # ESTABLISH
    df = DataFrame({kw.spark_face: ["a", "b", "c"]})
    mapping = {"a": 1, "b": 2, "c": 3}
    # WHEN
    add_spark_num_column(df, mapping)
    # THEN
    assert list(df.columns)[0] == kw.spark_num
    assert df[kw.spark_num].tolist() == [1, 2, 3]


def test_add_spark_num_column_SetsAttr_Scenario1_MissingSparkFaceSets_nan():
    # ESTABLISH
    df = DataFrame({kw.spark_face: ["a", "b", "x"]})
    mapping = {"a": 1, "b": 2}
    # WHEN
    add_spark_num_column(df, mapping)
    # THEN
    assert df[kw.spark_num].tolist()[:2] == [1, 2]
    assert pandas_isna(df[kw.spark_num].iloc[2])


def test_add_spark_num_column_SetsAttr_Scenario0_MutatesOriginalDataframe():
    # ESTABLISH
    df = DataFrame({kw.spark_face: ["a", "b"]})
    mapping = {"a": 1, "b": 2}
    assert kw.spark_num not in df.columns
    # WHEN
    add_spark_num_column(df, mapping)
    # THEN
    assert kw.spark_num in df.columns


@pytest_fixture
def excel_dir(tmp_path):
    """Creates a temporary directory with sample Excel files for testing."""
    from openpyxl import Workbook

    # File 1: two sheets
    wb1 = Workbook()
    wb1.active.title = "Alpha"
    wb1.create_sheet("Beta")
    wb1.save(tmp_path / "report.xlsx")

    # File 2: one sheet
    wb2 = Workbook()
    wb2.active.title = "Summary"
    wb2.save(tmp_path / "data.xlsx")

    # Non-Excel file (should be ignored)
    (tmp_path / "notes.txt").write_text("ignore me")

    return tmp_path


def test_get_excel_sheet_tuples_ReturnsObj_Scenario0_AllSheetTuples(excel_dir):
    """All (filename, sheet) pairs across every Excel file are returned."""
    # ESTABLISH / WHEN
    result = get_excel_sheet_tuples(str(excel_dir))
    # THEN
    assert ("data.xlsx", "Summary") in result
    assert ("report.xlsx", "Alpha") in result
    assert ("report.xlsx", "Beta") in result
    assert len(result) == 3


def test_get_excel_sheet_tuples_ReturnsObj_Scenario1_SortedList(excel_dir):
    """Returned list is sorted lexicographically by (filename, sheet_name)."""
    # ESTABLISH / WHEN
    result = get_excel_sheet_tuples(str(excel_dir))
    # THEN
    assert result == sorted(result)


def test_get_excel_sheet_tuples_ReturnsObj_Scenario2_EmptyListForNoExcelFiles(tmp_path):
    """Returns an empty list when the directory contains no Excel files."""
    # ESTABLISH
    (tmp_path / "readme.md").write_text("nothing here")
    # WHEN
    result = get_excel_sheet_tuples(str(tmp_path))
    # THEN
    assert result == []


def test_compare_br_sheets_Scenario0_DoesNotRaiseException(tmp_path: Path):
    # ESTABLISH
    # Setup source and destination directories
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    # Create Excel files
    src_file = src_dir / "file.xlsx"
    dst_file = dst_dir / "file.xlsx"

    df_br = DataFrame({"A": [1, 2], "B": [3, 4]})
    df_other = DataFrame({"X": [9, 8]})

    with pandas_ExcelWriter(src_file) as writer:
        df_br.to_excel(writer, sheet_name="br_sheet", index=False)
        df_other.to_excel(writer, sheet_name="other_sheet", index=False)

    with pandas_ExcelWriter(dst_file) as writer:
        df_br.to_excel(writer, sheet_name="br_sheet", index=False)
        df_other.to_excel(writer, sheet_name="other_sheet", index=False)

    # WHEN / THEN
    # Should not raise exception
    compare_br_sheets(src_dir, dst_dir)


def test_compare_br_sheets_Scenario1_DoesRaiseException(tmp_path: Path):
    # ESTABLISH
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    src_file = src_dir / "file.xlsx"
    dst_file = dst_dir / "file.xlsx"

    df_br_src = DataFrame({"A": [1, 2]})
    df_br_dst = DataFrame({"A": [1, 99]})  # conflict

    with pandas_ExcelWriter(src_file) as writer:
        df_br_src.to_excel(writer, sheet_name="br_sheet", index=False)

    with pandas_ExcelWriter(dst_file) as writer:
        df_br_dst.to_excel(writer, sheet_name="br_sheet", index=False)

    # WHEN / THEN
    with pytest_raises(MigrationConflictError, match="Conflict in sheet"):
        compare_br_sheets(src_dir, dst_dir)


def test_compare_br_sheets_Scenario2_MissingSheetRaiseException(tmp_path: Path):
    # ESTABLISH
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    src_file = src_dir / "file.xlsx"
    dst_file = dst_dir / "file.xlsx"

    df_br = DataFrame({"A": [1, 2]})

    with pandas_ExcelWriter(src_file) as writer:
        df_br.to_excel(writer, sheet_name="br_missing_in_dst", index=False)

    with pandas_ExcelWriter(dst_file) as writer:
        df_br.to_excel(writer, sheet_name="other_sheet", index=False)

    # WHEN / THEN
    with pytest_raises(
        MigrationConflictError, match="exists in source but not in destination"
    ):
        compare_br_sheets(src_dir, dst_dir)


# def test_move_br_sheets_no_conflict(tmp_path: Path):
#     # ESTABLISH
#     src_dir = tmp_path / "src"
#     dst_dir = tmp_path / "dst"
#     src_dir.mkdir()
#     dst_dir.mkdir()

#     src_file = src_dir / "file.xlsx"
#     dst_file = dst_dir / "file.xlsx"

#     df_br = DataFrame({"A": [1, 2]})
#     df_other = DataFrame({"X": [9]})

#     # Source has br sheet
#     with pandas_ExcelWriter(src_file) as writer:
#         df_br.to_excel(writer, sheet_name="br_sheet", index=False)
#         df_other.to_excel(writer, sheet_name="other", index=False)

#     # Destination starts empty
#     with pandas_ExcelWriter(dst_file) as writer:
#         df_other.to_excel(writer, sheet_name="other", index=False)
#     # WHEN
#     move_b_src_sheets_to_i_src(src_dir, dst_dir)
#     # THEN
#     # Verify br_sheet now exists in destination
#     result_sheets = pandas_read_excel(dst_file, sheet_name=None)
#     assert "br_sheet" in result_sheets
#     assert result_sheets["br_sheet"].equals(df_br)


# def test_move_br_sheets_conflict_raises(tmp_path: Path):
#     # ESTABLISH
#     src_dir = tmp_path / "src"
#     dst_dir = tmp_path / "dst"
#     src_dir.mkdir()
#     dst_dir.mkdir()

#     src_file = src_dir / "file.xlsx"
#     dst_file = dst_dir / "file.xlsx"

#     df_src = DataFrame({"A": [1, 2]})
#     df_dst_conflict = DataFrame({"A": [1, 99]})  # different

#     with pandas_ExcelWriter(src_file) as writer:
#         df_src.to_excel(writer, sheet_name="br_sheet", index=False)

#     with pandas_ExcelWriter(dst_file) as writer:
#         df_dst_conflict.to_excel(writer, sheet_name="br_sheet", index=False)

#     # WHEN / THEN
#     with pytest_raises(MigrationConflictError):
#         move_b_src_sheets_to_i_src(src_dir, dst_dir)


# def test_move_br_sheets_overwrites_or_adds_when_missing(tmp_path: Path):
#     # ESTABLISH
#     src_dir = tmp_path / "src"
#     dst_dir = tmp_path / "dst"
#     src_dir.mkdir()
#     dst_dir.mkdir()
#     src_file = src_dir / "file.xlsx"
#     dst_file = dst_dir / "file.xlsx"
#     df_src = DataFrame({"A": [5, 6]})
#     with pandas_ExcelWriter(src_file) as writer:
#         df_src.to_excel(writer, sheet_name="br_new", index=False)
#     # Destination has no br sheets
#     with pandas_ExcelWriter(dst_file) as writer:
#         DataFrame({"X": [1]}).to_excel(writer, sheet_name="other", index=False)
#     # WHEN
#     move_b_src_sheets_to_i_src(src_dir, dst_dir)
#     # THEN
#     result_sheets = pandas_read_excel(dst_file, sheet_name=None)
#     assert "br_new" in result_sheets
#     assert result_sheets["br_new"].equals(df_src)


#################################################################################


def create_excel_file(filepath, sheets_dict):
    with pandas_ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for name, df in sheets_dict.items():
            df.to_excel(writer, sheet_name=name, index=False)


def test_update_spark_num_in_excel_file_SetsFile_Scenario0_UpdatesAllSheets(temp3_fs):
    # ESTABLISH
    filepath = create_path(str(temp3_fs), "test.xlsx")
    df1 = DataFrame({"a": [1, 2]})
    df2 = DataFrame({"b": [3, 4]})
    create_excel_file(filepath, {"Sheet1": df1, "Sheet2": df2})

    # WHEN
    update_spark_num_in_excel_file(filepath, 41)

    # THEN
    result = pandas_read_excel(filepath, sheet_name=None)
    assert set(result.keys()) == {"Sheet1", "Sheet2"}
    for df in result.values():
        assert kw.spark_num in df.columns
        assert all(df[kw.spark_num] == 42)


def test_update_spark_num_in_excel_file_SetsFile_Scenario1_PreservesOtherColumns(
    temp3_fs,
):
    # ESTABLISH
    filepath = temp3_fs / "test.xlsx"
    df = DataFrame({"a": [1, 2], "b": [3, 4]})
    create_excel_file(filepath, {"Sheet1": df})
    # WHEN
    update_spark_num_in_excel_file(filepath, 99)
    # THEN
    result = pandas_read_excel(filepath, sheet_name=None)
    out_df = result["Sheet1"]

    assert list(out_df.columns) == ["a", "b", kw.spark_num]
    assert out_df["a"].tolist() == [1, 2]
    assert out_df["b"].tolist() == [3, 4]


# def test_update_spark_num_in_excel_file_SetsFile_Scenario2_EmptyWorkbook(temp3_fs):
#     # ESTABLISH
#     filepath = temp3_fs / "test.xlsx"

#     # Create empty workbook
#     with pandas_ExcelWriter(filepath, engine="xlsxwriter"):
#         pass
#     # WHEN
#     update_spark_num_in_excel_file(filepath, 5)
#     # THEN
#     result = pandas_read_excel(filepath, sheet_name=None)
#     assert result == {}


def test_update_spark_num_in_belief_files_SetAttrs(temp3_fs):
    # ESTABLISH
    # Setup: Create test directory and Excel file
    temp_dir = str(temp3_fs)
    file_path = os_path_join(temp_dir, "example_belief.xlsx")

    # Create Excel file with two sheets
    df1 = DataFrame({"name": ["Alice", "Bob"], "score": [80, 90]})
    df2 = DataFrame({"item": ["Pen", "Notebook"], "price": [1.5, 3.0]})
    with pandas_ExcelWriter(file_path) as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)

    # WHEN
    # Apply function
    update_spark_num_in_belief_files(temp_dir, 41)

    # THEN
    # Reload the file and verify that spark_num column exists and is correct
    result = pandas_read_excel(file_path, sheet_name=None)

    for sheet_df in result.values():
        assert kw.spark_num in sheet_df.columns
        assert all(sheet_df[kw.spark_num] == 42)
