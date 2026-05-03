from ch00_py.file_toolbox import create_path
from ch17_brick.brick_db_tool import save_sheet
from ch18_etl_config.brick_collector import (
    BrickFileRef,
    get_all_brickfilerefs,
    get_all_excel_bricksheets,
    get_etl_db_sheets_tier2_order,
    reorder_etl_db_sheets,
)
from pandas import (
    DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    read_excel as pandas_read_excel,
)
from pathlib import Path
from ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_all_excel_bricksheets_ReturnsObj_Scenario0_SheetNames(temp3_fs):
    # ESTABLISH
    env_dir = str(temp3_fs)
    x_dir = create_path(env_dir, "examples_dir")
    ex_filename = "Faybob.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    bk00100_str = "bk00100"
    bk00101_str = "bk00101"
    bk00102_str = "bk00102"
    save_sheet(ex_file_path, bk00100_str, df1)
    save_sheet(ex_file_path, bk00101_str, df2)
    save_sheet(ex_file_path, bk00102_str, df2)

    # WHEN
    x_sheet_names = get_all_excel_bricksheets(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_filename, bk00100_str) in x_sheet_names
    assert (x_dir, ex_filename, bk00101_str) in x_sheet_names
    assert (x_dir, ex_filename, bk00102_str) in x_sheet_names
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
    bk00103_str = "bk00103"

    # WHEN
    x_brickfileref = BrickFileRef(brick_type=bk00103_str)

    # THEN
    assert x_brickfileref.get_csv_filename() == f"{bk00103_str}.csv"


def test_get_all_brickfilerefs_ReturnsObj_Scenario0_TranslateSheetNames(
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
    bk00103_str = "example_bk00103"
    bk00103_str = "example_bk00103"
    save_sheet(ex_file_path, bk00103_str, df1)

    # WHEN
    x_bricksheets = get_all_brickfilerefs(env_dir)

    # THEN
    assert x_bricksheets
    bk3_brickfileref = BrickFileRef(x_dir, ex_filename, bk00103_str, "bk00103")
    assert x_bricksheets == [bk3_brickfileref]
    # assert (x_dir, ex_filename, bk00103_str) in x_bricksheets
    assert len(x_bricksheets) == 1


def test_get_all_brickfilerefs_ReturnsObj_Scenario1_OneSheets(temp3_fs):
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
    bk00103_ex1_str = "example1_bk00103"
    bk00103_ex2_str = "example2_bk00103"
    save_sheet(ex_file_path, bk00103_ex1_str, df1)
    save_sheet(ex_file_path, bk00103_ex2_str, df2)

    # WHEN
    x_bricksheets = get_all_brickfilerefs(env_dir)

    # THEN
    assert x_bricksheets
    ex1_brickfileref = BrickFileRef(x_dir, ex_filename, bk00103_ex1_str, "bk00103")
    ex2_brickfileref = BrickFileRef(x_dir, ex_filename, bk00103_ex2_str, "bk00103")

    assert x_bricksheets == [ex1_brickfileref]
    assert len(x_bricksheets) == 1


def test_get_all_brickfilerefs_ReturnsObj_Scenario2_TwoSheets(temp3_fs):
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
    ex1_brick_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    ex1_row1 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    ex1_row2 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    ex2_brick_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    ex2_row1 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    ex2_row2 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]

    df1 = DataFrame([ex1_row1, ex1_row2], columns=ex1_brick_columns)
    df2 = DataFrame([ex2_row1, ex2_row2], columns=ex2_brick_columns)
    bk00103_ex1_str = "example1_bk00103"
    bk00103_ex2_str = "example2_bk00103"
    save_sheet(ex_file_path, bk00103_ex1_str, df1)
    save_sheet(ex_file_path, bk00103_ex2_str, df2)

    # WHEN
    x_bricksheets = get_all_brickfilerefs(env_dir)

    # THEN
    assert x_bricksheets
    ex1_brickfileref = BrickFileRef(x_dir, ex_filename, bk00103_ex1_str, "bk00103")
    ex2_brickfileref = BrickFileRef(x_dir, ex_filename, bk00103_ex2_str, "bk00103")

    assert x_bricksheets == [ex1_brickfileref, ex2_brickfileref]
    assert len(x_bricksheets) == 2


def test_get_etl_db_sheets_tier2_order_ReturnsObj():
    # ESTABLISH
    tier2_postfixs = get_etl_db_sheets_tier2_order()
    # WHEN / THEN
    assert tier2_postfixs
    assert tier2_postfixs == [
        "b_src",
        "k_src",
        "brixk_raw",
        "brixk_agg",
        "brixk_vld",
        "s_raw",
        "s_agg",
        "s_vld",
        "h_raw",
        "h_agg",
        "h_vld",
        "lynx",
        "b_dst",
    ]


def create_excel(filepath: Path, sheet_names: list[str]):
    with pandas_ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for name in sheet_names:
            DataFrame({"col": [name]}).to_excel(writer, sheet_name=name, index=False)


def get_sheet_order(filepath: Path) -> list[str]:
    return list(pandas_read_excel(filepath, sheet_name=None).keys())


def test_reorder_etl_db_sheets_SortsSheets_Scenario0_NoPrefixOrPostfix(tmp_path):
    # ESTABLISH
    filepath = tmp_path / "test.xlsx"

    create_excel(filepath, ["misc", "BBB_data", "AAA_info"])
    # WHEN
    reorder_etl_db_sheets(filepath)
    # THEN
    result = get_sheet_order(filepath)
    assert result == ["AAA_info", "BBB_data", "misc"]


def test_reorder_etl_db_sheets_SortsSheets_Scenario1_PostfixPriority(tmp_path):
    # ESTABLISH
    filepath = tmp_path / "test.xlsx"

    create_excel(filepath, ["misc", "report_done_brixk_raw", "zzz_final_brixk_vld"])
    # WHEN
    reorder_etl_db_sheets(filepath)
    # THEN
    result = get_sheet_order(filepath)
    assert result == ["report_done_brixk_raw", "zzz_final_brixk_vld", "misc"]


def test_reorder_etl_db_sheets_SortsSheets_Scenario2_FallbackIgnoresOriginalOrder(
    tmp_path,
):
    # ESTABLISH
    filepath = tmp_path / "test.xlsx"
    original = ["sheet3_s_vld", "sheet7_brixk_vld", "sheet2"]
    create_excel(filepath, original)
    # WHEN
    reorder_etl_db_sheets(filepath)
    # THEN
    result = get_sheet_order(filepath)
    expected_sheet_order = ["sheet7_brixk_vld", "sheet3_s_vld", "sheet2"]
    assert result == expected_sheet_order


def test_reorder_etl_db_sheets_SortsSheets_Scenario3_brixk_raw_brixk_agg_AreSorted(
    tmp_path,
):
    # ESTABLISH
    filepath = tmp_path / "test.xlsx"
    original = ["sheet3_s_vld", "bksheet2brixk_agg", "bksheet3brixk_raw"]
    create_excel(filepath, original)
    # WHEN
    reorder_etl_db_sheets(filepath)
    # THEN
    result = get_sheet_order(filepath)
    expected_sheet_order = ["bksheet3brixk_raw", "bksheet2brixk_agg", "sheet3_s_vld"]
    assert result == expected_sheet_order
