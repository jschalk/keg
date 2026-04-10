from pandas import DataFrame
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.brick_db_tool import save_sheet
from src.ch18_etl_config.brick_collector import (
    BrickFileRef,
    get_all_brick_dataframes,
    get_all_excel_bricksheets,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_all_excel_bricksheets_ReturnsObj_Scenario0_SheetNames(temp3_fs):
    # ESTABLISH
    env_dir = str(temp3_fs)
    x_dir = create_path(env_dir, "examples_dir")
    ex_filename = "Faybob.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    br00000_str = "br00000"
    br00001_str = "br00001"
    br00002_str = "br00002"
    save_sheet(ex_file_path, br00000_str, df1)
    save_sheet(ex_file_path, br00001_str, df2)
    save_sheet(ex_file_path, br00002_str, df2)

    # WHEN
    x_sheet_names = get_all_excel_bricksheets(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_filename, br00000_str) in x_sheet_names
    assert (x_dir, ex_filename, br00001_str) in x_sheet_names
    assert (x_dir, ex_filename, br00002_str) in x_sheet_names
    assert len(x_sheet_names) == 3


def test_BrickFileRef_Exists():
    # ESTABLISH / WHEN
    x_brickfileref = BrickFileRef()

    # THEN
    assert x_brickfileref.file_dir is None
    assert x_brickfileref.filename is None
    assert x_brickfileref.sheet_name is None
    assert x_brickfileref.brick_type is None


def test_BrickFileRef_get_csv_filename_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    x_brickfileref = BrickFileRef()

    # THEN
    assert x_brickfileref.get_csv_filename() == ""


def test_BrickFileRef_get_csv_filename_ReturnsObj_Scenario1():
    # ESTABLISH
    br00003_str = "br00003"

    # WHEN
    x_brickfileref = BrickFileRef(brick_type=br00003_str)

    # THEN
    assert x_brickfileref.get_csv_filename() == f"{br00003_str}.csv"


def test_get_all_brick_dataframes_ReturnsObj_Scenario0_TranslateSheetNames(
    temp3_fs,
):
    # ESTABLISH
    env_dir = str(temp3_fs)
    x_dir = create_path(env_dir, "examples_dir")
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    brick_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    row1 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    row2 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    br00003_str = "example_br00003"
    br00003_str = "example_br00003"
    save_sheet(ex_file_path, br00003_str, df1)

    # WHEN
    x_ideasheets = get_all_brick_dataframes(env_dir)

    # THEN
    assert x_ideasheets
    br3_brickfileref = BrickFileRef(x_dir, ex_filename, br00003_str, "br00003")
    assert x_ideasheets == [br3_brickfileref]
    # assert (x_dir, ex_filename, br00003_str) in x_ideasheets
    assert len(x_ideasheets) == 1


def test_get_all_brick_dataframes_ReturnsObj_Scenario1(temp3_fs):
    # ESTABLISH
    env_dir = str(temp3_fs)
    x_dir = create_path(env_dir, "examples_dir")
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    brick_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    row1 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    row2 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    incomplete_brick_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
    ]
    incom_row1 = [spark1, exx.sue, minute_360, exx.a23]
    incom_row2 = [spark1, exx.sue, minute_420, exx.a23]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    save_sheet(ex_file_path, br00003_ex1_str, df1)
    save_sheet(ex_file_path, br00003_ex2_str, df2)

    # WHEN
    x_ideasheets = get_all_brick_dataframes(env_dir)

    # THEN
    assert x_ideasheets
    ex1_brickfileref = BrickFileRef(x_dir, ex_filename, br00003_ex1_str, "br00003")
    ex2_brickfileref = BrickFileRef(x_dir, ex_filename, br00003_ex2_str, "br00003")

    assert x_ideasheets == [ex1_brickfileref]
    assert len(x_ideasheets) == 1
