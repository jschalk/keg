from pandas import DataFrame
from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.idea_db_tool import save_sheet
from src.ch19_etl_steps.etl_main import etl_input_dfs_to_brick_raw_tables
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_input_dfs_to_brick_raw_tables_PopulatesTables_Scenario0(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    input_dir = create_path(str(temp3_fs), "input")
    input_file_path = create_path(input_dir, ex_filename)
    br3_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    row0 = [spark1, exx.sue, minute_360, exx.a23_dash, hour6am, exx.dash]
    row1 = [spark1, exx.sue, minute_420, exx.a23_dash, hour7am, exx.dash]
    row2 = [spark2, exx.sue, minute_420, exx.a23_dash, hour7am, exx.dash]
    row3 = [spark3, exx.sue, "num55", exx.a23_dash, hour7am, exx.dash]
    row4 = ["spark3", exx.sue, "num55", exx.a23_dash, hour7am, exx.dash]

    df1 = DataFrame([row0, row1, row2, row3, row4], columns=br3_columns)
    br00003_ex1_str = "example1_br00003"
    save_sheet(input_file_path, br00003_ex1_str, df1)
    br00003_tablename = f"br00003_{kw.brick_raw}"
    assert not db_table_exists(cursor0, br00003_tablename)

    # WHEN
    etl_input_dfs_to_brick_raw_tables(cursor0, input_dir)

    # THEN
    assert db_table_exists(cursor0, br00003_tablename)
    br00003_table_cols = get_table_columns(cursor0, br00003_tablename)
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str == br00003_table_cols[0]
    assert filename_str == br00003_table_cols[1]
    assert sheet_name_str == br00003_table_cols[2]
    assert kw.error_message == br00003_table_cols[-1]
    assert get_row_count(cursor0, br00003_tablename) == 5
    select_agg_sqlstr = f"""
SELECT * 
FROM {br00003_tablename} 
ORDER BY sheet_name, {kw.spark_num}, {kw.cumulative_minute};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 5
    file = ex_filename
    e1 = spark1
    e2 = spark2
    e3 = spark3
    s_dir = create_path(input_dir, ".")
    m_360 = minute_360
    m_420 = minute_420
    br3_str = br00003_ex1_str
    err4 = f"Conversion errors: {kw.cumulative_minute}: num55"
    err0 = f"Conversion errors: {kw.spark_num}: spark3, {kw.cumulative_minute}: num55"
    row0 = (s_dir, file, br3_str, None, exx.sue, exx.a23_dash, None, hour7am, "-", err0)
    row1 = (s_dir, file, br3_str, e1, exx.sue, exx.a23_dash, m_360, hour6am, "-", None)
    row2 = (s_dir, file, br3_str, e1, exx.sue, exx.a23_dash, m_420, hour7am, "-", None)
    row3 = (s_dir, file, br3_str, e2, exx.sue, exx.a23_dash, m_420, hour7am, "-", None)
    row4 = (s_dir, file, br3_str, e3, exx.sue, exx.a23_dash, None, hour7am, "-", err4)
    print(f"{rows[0]=}")
    print(f"   {row0=}")
    assert rows[0] == row0
    assert rows[1] == row1
    assert rows[2] == row2
    assert rows[3] == row3
    assert rows[4] == row4


def test_etl_input_dfs_to_brick_raw_tables_PopulatesTables_Scenario1(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    input_dir = create_path(str(temp3_fs), "input")
    input_file_path = create_path(input_dir, ex_filename)
    idea_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    row1 = [spark1, exx.sue, minute_360, exx.a23_dash, hour6am, exx.dash]
    row2 = [spark1, exx.sue, minute_420, exx.a23_dash, hour7am, exx.dash]
    row3 = [spark2, exx.sue, minute_420, exx.a23_dash, hour7am, exx.dash]
    incomplete_idea_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.knot,
    ]
    incom_row1 = [spark1, exx.sue, minute_360, exx.a23_dash, exx.dash]
    incom_row2 = [spark1, exx.sue, minute_420, exx.a23_dash, exx.dash]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    df3 = DataFrame([row2, row1, row3], columns=idea_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    save_sheet(input_file_path, br00003_ex1_str, df1)
    save_sheet(input_file_path, br00003_ex2_str, df2)
    save_sheet(input_file_path, br00003_ex3_str, df3)
    br00003_tablename = f"br00003_{kw.brick_raw}"
    assert not db_table_exists(cursor0, br00003_tablename)

    # WHEN
    etl_input_dfs_to_brick_raw_tables(cursor0, input_dir)

    # THEN
    assert db_table_exists(cursor0, br00003_tablename)
    assert get_row_count(cursor0, br00003_tablename) == 5
    br00003_table_cols = get_table_columns(cursor0, br00003_tablename)
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str == br00003_table_cols[0]
    assert filename_str == br00003_table_cols[1]
    assert sheet_name_str == br00003_table_cols[2]
    assert kw.error_message == br00003_table_cols[-1]
    select_agg_sqlstr = f"""
SELECT * 
FROM {br00003_tablename} 
ORDER BY sheet_name, {kw.spark_num}, {kw.cumulative_minute};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 5
    file = ex_filename
    e1 = spark1
    e2 = spark2
    s_dir = create_path(input_dir, ".")
    m_360 = minute_360
    m_420 = minute_420
    b1_str = br00003_ex1_str
    b3_str = br00003_ex3_str
    row0 = (s_dir, file, b1_str, e1, exx.sue, exx.a23_dash, m_360, hour6am, "-", None)
    row1 = (s_dir, file, b1_str, e1, exx.sue, exx.a23_dash, m_420, hour7am, "-", None)
    row2 = (s_dir, file, b3_str, e1, exx.sue, exx.a23_dash, m_360, hour6am, "-", None)
    row3 = (s_dir, file, b3_str, e1, exx.sue, exx.a23_dash, m_420, hour7am, "-", None)
    row4 = (s_dir, file, b3_str, e2, exx.sue, exx.a23_dash, m_420, hour7am, "-", None)
    print(f"{rows[0]=}")
    print(f"   {row0=}")
    assert rows[0] == row0
    assert rows[1] == row1
    assert rows[2] == row2
    assert rows[3] == row3
    assert rows[4] == row4


# def test_etl_input_dfs_to_brick_raw_tables_PopulatesTables_Scenario2(
#     temp3_fs,
# ):
#     # ESTABLISH
#     spark1 = 1
#     spark2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "Faybob.xlsx"
#     input_dir = create_path(str(temp3_fs), "input")
#     input_file_path = create_path(input_dir, ex_filename)
#     idea_columns = [
#     kw.spark_num,
#     kw.spark_face,
#     kw.cumulative_minute,
#     kw.moment_rope,
#     kw.hour_label,
#     ]
#     exx.a23_dash = exx.a23_dash
#     df_row0 = [spark1, exx.sue, minute_360, exx.a23_dash, hour6am]
#     df_row1 = [spark1, exx.sue, minute_420, exx.a23_dash, hour7am]
#     df_row2 = [spark2, exx.sue, minute_420, exx.a23_dash, hour7am]

#     df1 = DataFrame([df_row0, df_row1, df_row2], columns=idea_columns)
#     br00003_ex1_str = "example1_br00003"
#     save_sheet(input_file_path, br00003_ex1_str, df1)
#     cursor0 = db_conn.cursor0()
#     br00003_tablename = f"br00003_{kw.brick_raw}"
#     assert not db_table_exists(cursor0, br00003_tablename)

#     # WHEN
#     etl_input_dfs_to_brick_raw_tables(db_conn, input_dir)

#     # THEN
#     assert db_table_exists(cursor0, br00003_tablename)
#     assert get_row_count(cursor0, br00003_tablename) == 5
#     br00003_table_cols = get_table_columns(cursor0, br00003_tablename)
#     file_dir_str = "file_dir"
#     filename_str = "filename"
#     sheet_name_str = "sheet_name"
#     assert file_dir_str == br00003_table_cols[0]
#     assert filename_str == br00003_table_cols[1]
#     assert sheet_name_str == br00003_table_cols[2]
#     assert kw.error_message != br00003_table_cols[-1]
#     select_agg_sqlstr = f"""
# SELECT *
# FROM {br00003_tablename}
# ORDER BY sheet_name, {kw.spark_num}, {kw.cumulative_minute};"""
#     cursor0.execute(select_agg_sqlstr)

#     br3rows = cursor0.fetchall()
#     assert len(br3rows) == 5
#     file = ex_filename
#     e1 = spark1
#     e2 = spark2
#     s_dir = create_path(input_dir, ".")
#     m_360 = minute_360
#     m_420 = minute_420
#     br3_ex1_str = br00003_ex1_str
#     br3row0 = (s_dir, file, br3_ex1_str, e1, exx.sue, exx.a23_dash, m_360, hour6am)
#     br3row1 = (s_dir, file, br3_ex1_str, e1, exx.sue, exx.a23_dash, m_420, hour7am)
#     br3row2 = (s_dir, file, br3_ex1_str, e1, exx.sue, exx.a23_dash, m_360, hour6am)
#     print(f"{rows[0]=}")
#     print(f"   {row0=}")
#     assert rows[0] == row0
#     assert rows[1] == row1
#     assert rows[2] == row2
#     assert rows[3] == row3
#     assert rows[4] == row4
