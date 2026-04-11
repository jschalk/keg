from pandas import DataFrame
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.idea_db_tool import save_sheet
from src.ch18_etl_config.idea_collector import (
    IdeaFileRef,
    get_all_excel_ideasheets,
    get_all_idea_dataframes,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_all_excel_ideasheets_ReturnsObj_Scenario0_SheetNames(temp3_fs):
    # ESTABLISH
    env_dir = str(temp3_fs)
    x_dir = create_path(env_dir, "examples_dir")
    ex_filename = "Faybob.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    ii00000_str = "ii00000"
    ii00001_str = "ii00001"
    ii00002_str = "ii00002"
    save_sheet(ex_file_path, ii00000_str, df1)
    save_sheet(ex_file_path, ii00001_str, df2)
    save_sheet(ex_file_path, ii00002_str, df2)

    # WHEN
    x_sheet_names = get_all_excel_ideasheets(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_filename, ii00000_str) in x_sheet_names
    assert (x_dir, ex_filename, ii00001_str) in x_sheet_names
    assert (x_dir, ex_filename, ii00002_str) in x_sheet_names
    assert len(x_sheet_names) == 3


def test_IdeaFileRef_Exists():
    # ESTABLISH / WHEN
    x_ideafileref = IdeaFileRef()

    # THEN
    assert x_ideafileref.file_dir is None
    assert x_ideafileref.filename is None
    assert x_ideafileref.sheet_name is None
    assert x_ideafileref.idea_type is None


def test_IdeaFileRef_get_csv_filename_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    x_ideafileref = IdeaFileRef()

    # THEN
    assert x_ideafileref.get_csv_filename() == ""


def test_IdeaFileRef_get_csv_filename_ReturnsObj_Scenario1():
    # ESTABLISH
    ii00003_str = "ii00003"

    # WHEN
    x_ideafileref = IdeaFileRef(idea_type=ii00003_str)

    # THEN
    assert x_ideafileref.get_csv_filename() == f"{ii00003_str}.csv"


def test_get_all_idea_dataframes_ReturnsObj_Scenario0_TranslateSheetNames(
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
    idea_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    row1 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    row2 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    ii00003_str = "example_ii00003"
    ii00003_str = "example_ii00003"
    save_sheet(ex_file_path, ii00003_str, df1)

    # WHEN
    x_ideasheets = get_all_idea_dataframes(env_dir)

    # THEN
    assert x_ideasheets
    ii3_ideafileref = IdeaFileRef(x_dir, ex_filename, ii00003_str, "ii00003")
    assert x_ideasheets == [ii3_ideafileref]
    # assert (x_dir, ex_filename, ii00003_str) in x_ideasheets
    assert len(x_ideasheets) == 1


def test_get_all_idea_dataframes_ReturnsObj_Scenario1(temp3_fs):
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
    idea_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    row1 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    row2 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    incomplete_idea_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
    ]
    incom_row1 = [spark1, exx.sue, minute_360, exx.a23]
    incom_row2 = [spark1, exx.sue, minute_420, exx.a23]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    ii00003_ex1_str = "example1_ii00003"
    ii00003_ex2_str = "example2_ii00003"
    save_sheet(ex_file_path, ii00003_ex1_str, df1)
    save_sheet(ex_file_path, ii00003_ex2_str, df2)

    # WHEN
    x_ideasheets = get_all_idea_dataframes(env_dir)

    # THEN
    assert x_ideasheets
    ex1_ideafileref = IdeaFileRef(x_dir, ex_filename, ii00003_ex1_str, "ii00003")
    ex2_ideafileref = IdeaFileRef(x_dir, ex_filename, ii00003_ex2_str, "ii00003")

    assert x_ideasheets == [ex1_ideafileref]
    assert len(x_ideasheets) == 1
