from os.path import exists as os_path_exists
from sqlite3 import Cursor
from src.ch00_py.csv_toolbox import open_csv_with_types
from src.ch00_py.file_toolbox import create_path
from src.ch18_etl_config.etl_csv import save_to_split_csvs
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_save_to_split_csvs_CreatesFiles_Scenario0(temp3_fs, cursor0: Cursor):
    # ESTABLISH
    x_tablename = "test_table56"
    key_columns = ["user", "hair"]
    x_column_types = {
        "hair": "INTEGER",
        "user": "TEXT",
        "y_int": "INTEGER",
        kw.knot: "TEXT",
    }

    cursor0.execute(
        f"""CREATE TABLE {x_tablename} (hair INTEGER,user TEXT,y_int INTEGER, {kw.knot} TEXT)"""
    )
    cursor0.execute(
        f"""INSERT INTO {x_tablename} (hair, user, y_int, {kw.knot})
VALUES
(1, "-A-", 100, "{exx.dash}"),
(2, "-A-", 200, "{exx.dash}"),
(3, "-B-", 300, "{exx.dash}"),
(4, "-C-", 400, "{exx.dash}"),
(4, "-C-", 500, "{exx.dash}")
;
"""
    )
    x_dir = str(temp3_fs)
    A_dir = create_path(x_dir, "A")
    B_dir = create_path(x_dir, "B")
    C_dir = create_path(x_dir, "C")
    A1_dir = create_path(A_dir, 1)
    A2_dir = create_path(A_dir, 2)
    B3_dir = create_path(B_dir, 3)
    C4_dir = create_path(C_dir, 4)
    A1_path = create_path(A1_dir, f"{x_tablename}.csv")
    A2_path = create_path(A2_dir, f"{x_tablename}.csv")
    B3_path = create_path(B3_dir, f"{x_tablename}.csv")
    C4_path = create_path(C4_dir, f"{x_tablename}.csv")
    assert os_path_exists(A1_path) is False
    assert os_path_exists(A2_path) is False
    assert os_path_exists(B3_path) is False
    assert os_path_exists(C4_path) is False

    # WHEN
    save_to_split_csvs(cursor0, x_tablename, key_columns, x_dir)

    # THEN
    assert os_path_exists(A1_path)
    assert os_path_exists(A2_path)
    assert os_path_exists(B3_path)
    assert os_path_exists(C4_path)
    # expected_A1_csv = "hair,user,y_int\n1,A,100"
    # expected_A2_csv = "hair,user,y_int\n2,A,200"
    # expected_B3_csv = "hair,user,y_int\n3,C,300"
    # expected_C4_csv = "hair,user,y_int\n4,C,400\n4,C,500"
    expected_A1_row = (1, "-A-", 100, exx.dash)
    expected_A2_row = (2, "-A-", 200, exx.dash)
    expected_B3_row = (3, "-B-", 300, exx.dash)
    expected_C4_0_row = (4, "-C-", 400, exx.dash)
    expected_C4_1_row = (4, "-C-", 500, exx.dash)

    A1_csv = open_csv_with_types(A1_path, x_column_types)
    A2_csv = open_csv_with_types(A2_path, x_column_types)
    B3_csv = open_csv_with_types(B3_path, x_column_types)
    C4_csv = open_csv_with_types(C4_path, x_column_types)

    assert A1_csv[0] == ("hair", "user", "y_int", kw.knot)
    assert A2_csv[0] == ("hair", "user", "y_int", kw.knot)
    assert B3_csv[0] == ("hair", "user", "y_int", kw.knot)
    assert C4_csv[0] == ("hair", "user", "y_int", kw.knot)
    assert A1_csv[1] == expected_A1_row
    assert A2_csv[1] == expected_A2_row
    assert B3_csv[1] == expected_B3_row
    assert C4_csv[1] == expected_C4_0_row
    assert C4_csv[2] == expected_C4_1_row


# def test_save_to_split_csvs_CreatesFiles_Scenario1_add_col1_prefix(
#     temp3_fs, cursor0: Cursor
# ):
#     # ESTABLISH
#     x_tablename = "test_table567"
#     key_columns = ["user", "hair"]
#     x_column_types = {"hair": "INTEGER", "user": "TEXT", "y_int": "INTEGER"}

#     cursor0.execute(
#         f"""CREATE TABLE {x_tablename} (hair INTEGER,user TEXT,y_int INTEGER)"""
#     )
#     cursor0.execute(
#         f"""INSERT INTO {x_tablename} (hair, user, y_int)
# VALUES
# (1, "A", 100),
# (2, "A", 200),
# (3, "B", 300),
# (4, "C", 400),
# (4, "C", 500)
# ;
# """
#     )
#     x_dir = str(temp3_fs)
#     hairs_str = "hairs"
#     A_dir = create_path(x_dir, "A")
#     B_dir = create_path(x_dir, "B")
#     C_dir = create_path(x_dir, "C")
#     A_hairs_dir = create_path(A_dir, hairs_str)
#     B_hairs_dir = create_path(B_dir, hairs_str)
#     C_hairs_dir = create_path(C_dir, hairs_str)
#     A1_dir = create_path(A_hairs_dir, 1)
#     A2_dir = create_path(A_hairs_dir, 2)
#     B3_dir = create_path(B_hairs_dir, 3)
#     C4_dir = create_path(C_hairs_dir, 4)
#     A1_path = create_path(A1_dir, f"{x_tablename}.csv")
#     A2_path = create_path(A2_dir, f"{x_tablename}.csv")
#     B3_path = create_path(B3_dir, f"{x_tablename}.csv")
#     C4_path = create_path(C4_dir, f"{x_tablename}.csv")
#     assert os_path_exists(A1_path) is False
#     assert os_path_exists(A2_path) is False
#     assert os_path_exists(B3_path) is False
#     assert os_path_exists(C4_path) is False

#     # WHEN
#     save_to_split_csvs(cursor0, x_tablename, key_columns, x_dir, hairs_str)

#     # THEN
#     assert os_path_exists(A1_path)
#     assert os_path_exists(A2_path)
#     assert os_path_exists(B3_path)
#     assert os_path_exists(C4_path)
#     # expected_A1_csv = "hair,user,y_int\n1,A,100"
#     # expected_A2_csv = "hair,user,y_int\n2,A,200"
#     # expected_B3_csv = "hair,user,y_int\n3,C,300"
#     # expected_C4_csv = "hair,user,y_int\n4,C,400\n4,C,500"
#     expected_A1_row = (1, "A", 100)
#     expected_A2_row = (2, "A", 200)
#     expected_B3_row = (3, "B", 300)
#     expected_C4_0_row = (4, "C", 400)
#     expected_C4_1_row = (4, "C", 500)

#     A1_csv = open_csv_with_types(A1_path, x_column_types)
#     A2_csv = open_csv_with_types(A2_path, x_column_types)
#     B3_csv = open_csv_with_types(B3_path, x_column_types)
#     C4_csv = open_csv_with_types(C4_path, x_column_types)

#     assert A1_csv[0] == ("hair", "user", "y_int")
#     assert A2_csv[0] == ("hair", "user", "y_int")
#     assert B3_csv[0] == ("hair", "user", "y_int")
#     assert C4_csv[0] == ("hair", "user", "y_int")
#     assert A1_csv[1] == expected_A1_row
#     assert A2_csv[1] == expected_A2_row
#     assert B3_csv[1] == expected_B3_row
#     assert C4_csv[1] == expected_C4_0_row
#     assert C4_csv[2] == expected_C4_1_row


# def test_save_to_split_csvs_CreatesFiles_Scenario2_add_col2_prefix(
#     temp3_fs, cursor0: Cursor
# ):
#     # ESTABLISH
#     x_tablename = "test_table568"
#     key_columns = ["user", "hair", "y_int"]
#     cursor0.execute(
#         f"""CREATE TABLE {x_tablename} (hair INTEGER,user TEXT,y_int INTEGER, "run" TEXT)"""
#     )
#     cursor0.execute(
#         f"""INSERT INTO {x_tablename} (hair, user, y_int, run) VALUES (1, "A", 200, "yes") ;"""
#     )
#     x_dir = str(temp3_fs)
#     hairs_str = "hairs"
#     y_ints_str = "y_ints"
#     A_dir = create_path(x_dir, "A")
#     A_hairs_dir = create_path(A_dir, hairs_str)
#     A1_dir = create_path(A_hairs_dir, 1)
#     A1y_ints_dir = create_path(A1_dir, y_ints_str)
#     A200_dir = create_path(A1y_ints_dir, 200)
#     A1_path = create_path(A200_dir, f"{x_tablename}.csv")
#     print(f"{A1_path=}")
#     assert os_path_exists(A1_path) is False

#     # WHEN
#     save_to_split_csvs(
#         conn_or_cursor=cursor0,
#         tablename=x_tablename,
#         key_columns=key_columns,
#         dst_dir=x_dir,
#         col1_prefix=hairs_str,
#         col2_prefix=y_ints_str,
#     )

#     # THEN
#     assert os_path_exists(A1_path)
#     expected_A1_row = (1, "A", 200, "yes")
#     x_column_types = {
#         "hair": "INTEGER",
#         "user": "TEXT",
#         "y_int": "INTEGER",
#         "run": "TEXT",
#     }
#     A1_csv = open_csv_with_types(A1_path, x_column_types)
#     assert A1_csv[0] == ("hair", "user", "y_int", "run")
#     assert A1_csv[1] == expected_A1_row


def test_save_to_split_csvs_CreatesFiles_Scenario3_Different_Knots(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    x_tablename = "test_table568"
    key_columns = ["hair", "user"]
    create_sql = f"""CREATE TABLE {x_tablename} (hair INTEGER,user TEXT,y_int INTEGER, run TEXT, {kw.knot} TEXT);"""
    cursor0.execute(create_sql)
    x_blue = f";{exx.blue};"
    x_red = f"/{exx.red}/"
    insert1_sql = f"""INSERT INTO {x_tablename} (hair, user, y_int, run, {kw.knot}) VALUES ("{x_blue}", "A", 200, "yes", ";");"""
    insert2_sql = f"""INSERT INTO {x_tablename} (hair, user, y_int, run, {kw.knot}) VALUES ("{x_blue}", "A", 333, "yes", ";");"""
    insert3_sql = f"""INSERT INTO {x_tablename} (hair, user, y_int, run, {kw.knot}) VALUES ("{x_red}", "B", 200, "yes", "/");"""
    cursor0.execute(insert1_sql)
    cursor0.execute(insert2_sql)
    cursor0.execute(insert3_sql)
    x_dir = str(temp3_fs)
    hairs_str = "hairs"
    y_ints_str = "y_ints"
    blue_dir = create_path(x_dir, exx.blue)
    hairs_dir = create_path(blue_dir, hairs_str)
    blue_A_dir = create_path(hairs_dir, "A")
    blue_y_ints_dir = create_path(blue_A_dir, y_ints_str)
    blue_A_csv_path = create_path(blue_y_ints_dir, f"{x_tablename}.csv")
    print(f"{blue_A_csv_path=}")
    assert os_path_exists(blue_A_csv_path) is False

    # WHEN
    save_to_split_csvs(
        conn_or_cursor=cursor0,
        tablename=x_tablename,
        key_columns=key_columns,
        dst_dir=x_dir,
        col1_prefix=hairs_str,
        col2_prefix=y_ints_str,
    )

    # THEN
    assert os_path_exists(blue_A_csv_path)
    x_column_types = {
        "hair": "TEXT",
        "user": "TEXT",
        "y_int": "INTEGER",
        "run": "TEXT",
        kw.knot: "TEXT",
    }
    x_csv = open_csv_with_types(blue_A_csv_path, x_column_types)
    print(f"{x_csv[0]=}")
    print(f"{x_csv[1]=}")
    assert x_csv[0] == ("hair", "user", "y_int", "run", kw.knot)
    expected_csv1_row = (x_blue, "A", 200, "yes", ";")
    assert x_csv[1] == expected_csv1_row
    expected_csv2_row = (x_blue, "A", 333, "yes", ";")
    assert x_csv[2] == expected_csv2_row


# def test_save_to_split_csvs_CreatesFiles_Scenario4_knot_is_NULL(
#     temp3_fs, cursor0: Cursor
# ):
#     # ESTABLISH
#     x_tablename = "test_table568"
#     key_columns = ["hair", "user"]
#     create_sql = f"""CREATE TABLE {x_tablename} (hair INTEGER,user TEXT,y_int INTEGER, run TEXT, {kw.knot} TEXT);"""
#     cursor0.execute(create_sql)
#     x_blue = f";{exx.blue};"
#     x_red = f"/{exx.red}/"
#     insert1_sql = f"""INSERT INTO {x_tablename} (hair, user, y_int, run, {kw.knot}) VALUES ("{x_blue}", "A", 200, "yes", NULL);"""
#     insert2_sql = f"""INSERT INTO {x_tablename} (hair, user, y_int, run, {kw.knot}) VALUES ("{x_blue}", "A", 333, "yes", NULL);"""
#     insert3_sql = f"""INSERT INTO {x_tablename} (hair, user, y_int, run, {kw.knot}) VALUES ("{x_red}", "B", 200, "yes", NULL);"""
#     cursor0.execute(insert1_sql)
#     cursor0.execute(insert2_sql)
#     cursor0.execute(insert3_sql)
#     x_dir = str(temp3_fs)
#     hairs_str = "hairs"
#     y_ints_str = "y_ints"
#     red_dir = create_path(x_dir, exx.red)
#     hairs_dir = create_path(red_dir, hairs_str)
#     red_A_dir = create_path(hairs_dir, "B")
#     red_y_ints_dir = create_path(red_A_dir, y_ints_str)
#     red_A_csv_path = create_path(red_y_ints_dir, f"{x_tablename}.csv")
#     print(f"{red_A_csv_path=}")
#     assert os_path_exists(red_A_csv_path) is False

#     # WHEN
#     save_to_split_csvs(
#         conn_or_cursor=cursor0,
#         tablename=x_tablename,
#         key_columns=key_columns,
#         dst_dir=x_dir,
#         col1_prefix=hairs_str,
#         col2_prefix=y_ints_str,
#     )

#     # THEN
#     assert os_path_exists(red_A_csv_path)
#     expected_A1_row = (x_red, "B", 200, "yes", "")
#     x_column_types = {
#         "hair": "TEXT",
#         "user": "TEXT",
#         "y_int": "INTEGER",
#         "run": "TEXT",
#         kw.knot: "TEXT",
#     }
#     A1_csv = open_csv_with_types(red_A_csv_path, x_column_types)
#     print(f"{A1_csv[0]=}")
#     print(f"{A1_csv[1]=}")
#     assert A1_csv[0] == ("hair", "user", "y_int", "run", kw.knot)
#     assert A1_csv[1] == expected_A1_row
