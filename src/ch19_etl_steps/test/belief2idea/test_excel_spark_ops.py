from openpyxl import Workbook as openpyxl_Workbook
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
    add_spark_num_column,
    beliefs_sheets_to_idea_sheets,
    create_spark_face_spark_nums,
    get_excel_sheet_tuples,
    get_max_spark_num_from_files,
    get_sheets_with_brick_types,
    get_spark_faces_from_df,
    get_spark_faces_from_files,
    get_validated_bele_src_brick_type_sheets,
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

    # File 1: two sheets
    wb1 = openpyxl_Workbook()
    wb1.active.title = "Alpha"
    wb1.create_sheet("Beta")
    wb1.save(tmp_path / "report.xlsx")

    # File 2: one sheet
    wb2 = openpyxl_Workbook()
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


def test_get_excel_sheet_tuples_ReturnsObj_Scenario2_EmptyListForNoExcelFiles(
    tmp_path: Path,
):
    """Returns an empty list when the directory contains no Excel files."""
    # ESTABLISH
    (tmp_path / "readme.md").write_text("nothing here")
    # WHEN
    result = get_excel_sheet_tuples(str(tmp_path))
    # THEN
    assert result == []


def test_get_sheets_with_brick_types_ReturnsObj_Scenario0_MatchingTuples(
    tmp_path: Path,
):
    """Only tuples whose sheet_name contains a br_string are returned."""
    # ESTABLISH
    br_excel_dir = tmp_path / "beliefs"
    br_excel_dir.mkdir()
    wb1 = openpyxl_Workbook()
    wb1.active.title = "br00002_Sales"
    wb1.create_sheet("Revenue")
    wb1.create_sheet("Costs_BR00005")
    wb1.save(br_excel_dir / "x300reports.xlsx")

    wb2 = openpyxl_Workbook()
    wb2.active.title = "Summary"
    wb2.create_sheet("BR00042_Overview")
    wb2.save(br_excel_dir / "report.xlsx")

    # WHEN
    result = get_sheets_with_brick_types(br_excel_dir)

    # THEN
    assert ("x300reports.xlsx", "br00002_Sales") in result
    assert ("x300reports.xlsx", "Costs_BR00005") in result
    assert ("report.xlsx", "BR00042_Overview") in result
    assert ("x300reports.xlsx", "Revenue") not in result
    assert ("report.xlsx", "Summary") not in result


# --- Pytest fixtures & tests ---


@pytest_fixture
def idea_dir_no_overlap(tmp_path):

    d = tmp_path / "idea"
    d.mkdir()
    wb = openpyxl_Workbook()
    wb.active.title = "Summary"
    wb.create_sheet("Details")
    wb.save(d / "idea_report.xlsx")
    return d


@pytest_fixture
def idea_dir_with_overlap(tmp_path):

    d = tmp_path / "idea_overlap"
    d.mkdir()
    wb = openpyxl_Workbook()
    wb.active.title = "BR00005_Sales"  # overlaps with bele_dir
    wb.save(d / "idea_report.xlsx")
    return d


def test_get_validated_bele_src_brick_type_sheets_ReturnsBeleBrSheets(
    idea_dir_no_overlap, tmp_path
):
    """Returns only BR sheet tuples from bele_src_dir when there is no overlap."""
    # ESTABLISH
    bele_dir = tmp_path / "bele"
    bele_dir.mkdir()
    wb = openpyxl_Workbook()
    wb.active.title = "BR00005_Sales"
    wb.create_sheet("Revenue")
    wb.create_sheet("BR00042_Costs")
    wb.save(bele_dir / "x300reports.xlsx")

    # WHEN
    result = get_validated_bele_src_brick_type_sheets(
        bele_dir, str(idea_dir_no_overlap)
    )
    # THEN
    assert ("x300reports.xlsx", "BR00005_Sales") in result
    assert ("x300reports.xlsx", "BR00042_Costs") in result
    assert ("x300reports.xlsx", "Revenue") not in result


def test_get_validated_bele_src_brick_type_sheets_RaisesOnOverlap(
    idea_dir_with_overlap, tmp_path
):
    """Raises ValueError when a BR sheet name exists in both directories."""
    # ESTABLISH
    bele_dir = tmp_path / "bele"
    bele_dir.mkdir()
    wb = openpyxl_Workbook()
    wb.active.title = "BR00005_Sales"
    wb.create_sheet("Revenue")
    wb.create_sheet("BR00042_Costs")
    wb.save(bele_dir / "x300reports.xlsx")

    # WHEN / THEN
    with pytest_raises(ValueError, match="BR00005_Sales"):
        get_validated_bele_src_brick_type_sheets(
            str(bele_dir), str(idea_dir_with_overlap)
        )


def test_get_validated_bele_src_brick_type_sheets_ReturnsEmptyWhenNoBeleBrSheets(
    idea_dir_no_overlap, tmp_path
):
    """Returns an empty list when bele_src_dir has no BR sheets."""
    # ESTABLISH

    empty_bele = tmp_path / "empty_bele"
    empty_bele.mkdir()
    wb = openpyxl_Workbook()
    wb.active.title = "Summary"
    wb.save(empty_bele / "plain.xlsx")
    # WHEN
    result = get_validated_bele_src_brick_type_sheets(
        str(empty_bele), str(idea_dir_no_overlap)
    )
    # THEN
    assert result == []


def test_beliefs_sheets_to_idea_sheets_Scenario0_ReturnsObj_TwoTuples(tmp_path: Path):
    """Returns one (filename, sheet_name) tuple per BR sheet copied."""
    # ESTABLISH
    empty_idea_dir = tmp_path / "idea"
    empty_idea_dir.mkdir()

    populated_bele_dir = tmp_path / "bele"
    populated_bele_dir.mkdir()
    wb = openpyxl_Workbook()
    ws1 = wb.active
    ws1.title = "BR00020_Sales"
    ws1.append(["product", "units", "revenue"])
    ws1.append(["widget", 10, 500])
    ws1.append(["gadget", 5, 250])

    ws2 = wb.create_sheet("BR00004_Costs")
    ws2.append(["category", "amount"])
    ws2.append(["rent", 1000])
    wb.create_sheet("Summary")  # non-BR, should be ignored
    wb.save(populated_bele_dir / "AllSales.xlsx")

    # WHEN
    result = beliefs_sheets_to_idea_sheets(populated_bele_dir, empty_idea_dir)
    # THEN
    assert ("BR00004_Costs.xlsx", "BR00004_Costs") in result
    assert ("BR00020_Sales.xlsx", "BR00020_Sales") in result
    assert len(result) == 2


def test_beliefs_sheets_to_idea_sheets_Scenario1_ReturnsObj_DataReadableByPandas(
    tmp_path: Path,
):
    """Each copied sheet can be read by pandas and contains the original data."""
    # ESTABLISH
    empty_idea_dir = tmp_path / "idea"
    empty_idea_dir.mkdir()
    populated_bele_dir = tmp_path / "bele"
    populated_bele_dir.mkdir()
    wb = openpyxl_Workbook()
    ws1 = wb.active
    ws1.title = "BR00020_Sales"
    ws1.append(["product", "units", "revenue"])
    ws1.append(["widget", 10, 500])
    ws1.append(["gadget", 5, 250])

    ws2 = wb.create_sheet("BR00004_Costs")
    ws2.append(["category", "amount"])
    ws2.append(["rent", 1000])
    wb.create_sheet("Summary")  # non-BR, should be ignored
    wb.save(populated_bele_dir / "AllSales.xlsx")

    # WHEN
    beliefs_sheets_to_idea_sheets(populated_bele_dir, empty_idea_dir)
    # THEN
    df = pandas_read_excel(
        os_path_join(str(empty_idea_dir), "BR00020_Sales.xlsx"),
        sheet_name="BR00020_Sales",
    )
    assert list(df.columns) == ["product", "units", "revenue"]
    assert len(df) == 2
    assert df["revenue"].sum() == 750


def test_beliefs_sheets_to_idea_sheets_Scenario2_RaisesOnOverlap(tmp_path: Path):
    """Propagates ValueError from get_bele_br_sheets_validated on sheet name overlap."""
    # ESTABLISH
    beliefs_dir = tmp_path / "bele"
    beliefs_dir.mkdir()
    ideas_dir = tmp_path / "idea"
    ideas_dir.mkdir()

    wb_bele = openpyxl_Workbook()
    wb_bele.active.title = "BR00020_Sales"
    wb_bele.save(beliefs_dir / "AllSales.xlsx")

    wb_idea = openpyxl_Workbook()
    wb_idea.active.title = "BR00020_Sales"
    wb_idea.save(ideas_dir / "existing.xlsx")
    # WHEN / THEN
    with pytest_raises(ValueError, match="BR00020_Sales"):
        beliefs_sheets_to_idea_sheets(beliefs_dir, ideas_dir)


def create_excel_file(filepath, sheets_dict):
    with pandas_ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for name, df in sheets_dict.items():
            df.to_excel(writer, sheet_name=name, index=False)


# TODO depercate this function
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


# TODO depercate this function
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
