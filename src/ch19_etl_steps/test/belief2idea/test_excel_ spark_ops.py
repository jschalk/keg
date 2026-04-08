from os.path import exists as os_path_exists, join as os_path_join
from pandas import (
    DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    isna as pandas_isna,
    read_excel as pandas_read_excel,
)
from src.ch00_py.file_toolbox import create_path
from src.ch19_etl_steps.belief2idea import (
    add_spark_num_column,
    create_spark_face_spark_nums,
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
    update_spark_num_in_excel_file(filepath, 42)

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
    update_spark_num_in_belief_files(temp_dir, 42)

    # THEN
    # Reload the file and verify that spark_num column exists and is correct
    result = pandas_read_excel(file_path, sheet_name=None)

    for sheet_df in result.values():
        assert kw.spark_num in sheet_df.columns
        assert all(sheet_df[kw.spark_num] == 42)
