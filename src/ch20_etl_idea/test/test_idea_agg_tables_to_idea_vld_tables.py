from ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from ch17_idea.idea_db_tool import create_idea_sorted_table
from ch20_etl_idea.etl_idea_main import (
    etl_ideax_agg_tables_to_ideax_vld_tables,
    get_create_sparks_ideax_vld_sqlstr,
)
from ref.keywords import Ch20Keywords as kw, ExampleStrs as exx
from sqlite3 import Cursor

# TODO create insert from vld tests for etl_ideax_vld_tables_to_ideax_vld_tables
# TODO create insert from vld does not accumlate over time test for etl_ideax_vld_tables_to_ideax_vld_tables


def test_etl_ideax_agg_tables_to_ideax_vld_tables_PopulatesVldTable_Scenario0_valid_spark_nums(
    cursor0: Cursor,
):  # sourcery skip: extract-duplicate-method
    # ESTABLISH
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    # INSERT INTO ideax_agg table
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    agg_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
        kw.knot,
        kw.error_message,
    ]
    create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
    insert_into_agg_clause = f"""INSERT INTO {agg_ii00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
, {kw.knot}
, {kw.error_message}
)"""
    values_agg_clause = f"""
VALUES
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', ';', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', NULL)
;
"""
    cursor0.execute(f"{insert_into_agg_clause} {values_agg_clause}")
    # INSERT INTO
    cursor0.execute(get_create_sparks_ideax_vld_sqlstr())
    select_sparks_ideax_vld_sqlstr = f"""
INSERT INTO sparks_ideax_vld ({kw.spark_num}, {kw.spark_face}) 
VALUES ('{spark1}', '{exx.sue}')
;
"""
    cursor0.execute(select_sparks_ideax_vld_sqlstr)
    vld_ii00103_tablename = f"ii00103_{kw.ideax_vld}"
    assert get_row_count(cursor0, agg_ii00103_tablename) == 2
    assert not db_table_exists(cursor0, vld_ii00103_tablename)

    # WHEN
    etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)

    # THEN
    assert db_table_exists(cursor0, vld_ii00103_tablename)
    assert get_row_count(cursor0, vld_ii00103_tablename) == 2

    ii00103_table_cols = get_table_columns(cursor0, vld_ii00103_tablename)
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str not in set(ii00103_table_cols[0])
    assert filename_str not in set(ii00103_table_cols[1])
    assert sheet_name_str not in set(ii00103_table_cols[2])
    select_vld_sqlstr = f"""
SELECT *
FROM {vld_ii00103_tablename}
ORDER BY {kw.spark_num}, {kw.cumulative_minute};"""
    cursor0.execute(select_vld_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 2
    e1 = spark1
    m_360 = minute_360
    m_420 = minute_420
    row0 = (e1, exx.sue, exx.a23, m_360, hour6am, ";", None)
    row1 = (e1, exx.sue, exx.a23, m_420, hour7am, ";", None)
    print(f"{rows[0]=}")
    print(f"   {row0=}")
    assert rows[0] == row0
    assert rows[1] == row1


def test_etl_ideax_agg_tables_to_ideax_vld_tables_PopulatesVldTable_Scenario1_NoDuplicates(
    cursor0: Cursor,
):  # sourcery skip: extract-duplicate-method
    # ESTABLISH
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    # INSERT INTO ideax_agg table
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    agg_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
        kw.knot,
        kw.error_message,
    ]
    create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
    insert_into_agg_clause = f"""INSERT INTO {agg_ii00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
, {kw.knot}
, {kw.error_message}
)"""
    values_agg_clause = f"""
VALUES
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', ';', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', NULL)
;
"""
    cursor0.execute(f"{insert_into_agg_clause} {values_agg_clause}")
    # INSERT INTO
    cursor0.execute(get_create_sparks_ideax_vld_sqlstr())
    select_sparks_ideax_vld_sqlstr = f"""
INSERT INTO sparks_ideax_vld ({kw.spark_num}, {kw.spark_face}) 
VALUES ('{spark1}', '{exx.sue}')
;
"""
    cursor0.execute(select_sparks_ideax_vld_sqlstr)
    vld_ii00103_tablename = f"ii00103_{kw.ideax_vld}"
    etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)
    assert get_row_count(cursor0, vld_ii00103_tablename) == 2
    minute_480 = 480
    hour8am = "8am"
    insert_into_agg_clause = f"""INSERT INTO {agg_ii00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
, {kw.knot}
, {kw.error_message}
)"""
    values_agg_clause = f"""
VALUES
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', ';', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_480}', '{hour8am}', ';', NULL)
;
"""
    cursor0.execute(f"{insert_into_agg_clause} {values_agg_clause}")
    assert get_row_count(cursor0, vld_ii00103_tablename) == 2

    # WHEN
    etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, vld_ii00103_tablename) == 3


# def test_etl_ideax_agg_tables_to_ideax_vld_tables_PopulatesVldTable_Scenario1_GroupByOnlyNonConflictingRecords(
#     cursor0: Cursor,
# ):
#     # ESTABLISH
#     spark1 = 1
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     hour8am = "8am"

#     agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
#     agg_ii00103_columns = [
#         kw.spark_num,
#         kw.spark_face,
#         kw.moment_rope,
#         kw.cumulative_minute,
#         kw.hour_label,
#         kw.knot,
#         kw.error_message,
#     ]
#     create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
#     insert_into_clause = f"""INSERT INTO {agg_ii00103_tablename} (
#   {kw.spark_num}
# , {kw.spark_face}
# , {kw.moment_rope}
# , {kw.cumulative_minute}
# , {kw.hour_label}
# , {kw.knot}
# , {kw.error_message}
# )"""
#     values_clause = f"""
# VALUES
#   ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', '/', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', '/', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour8am}', '/', NULL)
# ;
# """
#     insert_sqlstr = f"{insert_into_clause} {values_clause}"
#     cursor0.execute(insert_sqlstr)
#     vld_ii00103_tablename = f"ii00103_{kw.ideax_vld}"
#     assert get_row_count(cursor0, agg_ii00103_tablename) == 3
#     assert not db_table_exists(cursor0, vld_ii00103_tablename)

#     # WHEN
#     etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)

#     # THEN
#     assert db_table_exists(cursor0, vld_ii00103_tablename)
#     assert get_row_count(cursor0, vld_ii00103_tablename) == 1

#     ii00103_table_cols = get_table_columns(cursor0, vld_ii00103_tablename)
#     file_dir_str = "file_dir"
#     filename_str = "filename"
#     sheet_name_str = "sheet_name"
#     assert file_dir_str not in set(ii00103_table_cols[0])
#     assert filename_str not in set(ii00103_table_cols[1])
#     assert sheet_name_str not in set(ii00103_table_cols[2])
#     select_vld_sqlstr = f"""SELECT * FROM {vld_ii00103_tablename};"""
#     cursor0.execute(select_vld_sqlstr)

#     rows = cursor0.fetchall()
#     assert len(rows) == 1
#     e1 = spark1
#     m_360 = minute_360
#     row0 = (e1, exx.sue, exx.a23, m_360, hour6am, "/")
#     print(f"{rows[0]=}")
#     print(f"   {row0=}")
#     assert rows[0] == row0


# def test_etl_ideax_agg_tables_to_ideax_vld_tables_PopulatesVldTable_Scenario2_GroupByExcludesRowsWith_error_message(
#     cursor0: Cursor,
# ):
#     # ESTABLISH
#     spark1 = 1
#     minute_360 = 360
#     minute_420 = 420
#     minute_480 = 480
#     hour6am = "6am"
#     hour7am = "7am"
#     hour8am = "8am"
#     agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
#     agg_ii00103_columns = [
#         kw.spark_num,
#         kw.spark_face,
#         kw.moment_rope,
#         kw.cumulative_minute,
#         kw.hour_label,
#         kw.knot,
#         kw.error_message,
#     ]
#     create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
#     insert_into_clause = f"""INSERT INTO {agg_ii00103_tablename} (
#   {kw.spark_num}
# , {kw.spark_face}
# , {kw.moment_rope}
# , {kw.cumulative_minute}
# , {kw.hour_label}
# , {kw.knot}
# , {kw.error_message}
# )"""
#     values_clause = f"""
# VALUES
#   ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', ';', 'some_error')
# , ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', 'some_error')
# , ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_480}', '{hour8am}', ';', NULL)
# ;
# """
#     insert_sqlstr = f"{insert_into_clause} {values_clause}"
#     cursor0.execute(insert_sqlstr)
#     vld_ii00103_tablename = f"ii00103_{kw.ideax_vld}"
#     assert get_row_count(cursor0, agg_ii00103_tablename) == 4
#     assert not db_table_exists(cursor0, vld_ii00103_tablename)

#     # WHEN
#     etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)

#     # THEN
#     select_vld_sqlstr = f"""
# SELECT *
# FROM {vld_ii00103_tablename}
# ORDER BY {kw.spark_num}, {kw.cumulative_minute};"""
#     cursor0.execute(select_vld_sqlstr)

#     rows = cursor0.fetchall()
#     assert len(rows) == 2
#     row0 = (spark1, exx.sue, exx.a23, minute_420, hour7am, ";")
#     row1 = (spark1, exx.sue, exx.a23, minute_480, hour8am, ";")
#     print(f"{rows[0]=}")
#     print(f"   {row0=}")
#     assert rows[0] == row0
#     assert rows[1] == row1


# def test_etl_ideax_agg_tables_to_ideax_vld_tables_PopulatesVldTable_Scenario3_TableDeleteBeforeLoad(
#     cursor0: Cursor,
# ):
#     # ESTABLISH
#     spark1 = 1
#     agg_ii00105_tablename = f"ii00105_{kw.ideax_agg}"
#     agg_ii00105_columns = [
#         kw.spark_num,
#         kw.spark_face,
#         kw.moment_rope,
#         kw.weekday_order,
#         kw.weekday_label,
#         kw.knot,
#         kw.error_message,
#     ]
#     create_idea_sorted_table(cursor0, agg_ii00105_tablename, agg_ii00105_columns)
#     insert_into_clause = f"""INSERT INTO {agg_ii00105_tablename} (
#   {kw.spark_num}
# , {kw.spark_face}
# , {kw.moment_rope}
# , {kw.weekday_order}
# , {kw.weekday_label}
# , {kw.knot}
# , {kw.error_message}
# )"""
#     values_clause = f"""
# VALUES
#   ('{spark1}', '{exx.sue}', '{exx.a23}', 0, '{exx.Wednesday}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', 0, '{exx.Wednesday}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', 1, '{exx.Thursday}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', 3, '{exx.Saturday}', ';', NULL)
# ;
# """
#     insert_sqlstr = f"{insert_into_clause} {values_clause}"
#     cursor0.execute(insert_sqlstr)
#     vld_ii00105_tablename = f"ii00105_{kw.ideax_vld}"
#     assert get_row_count(cursor0, agg_ii00105_tablename) == 4
#     assert not db_table_exists(cursor0, vld_ii00105_tablename)
#     etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)
#     assert get_row_count(cursor0, vld_ii00105_tablename) == 3
#     values2_clause = f"""
# VALUES
#   ('{spark1}', '{exx.sue}', '{exx.a23}', 0, '{exx.Wednesday}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', 0, '{exx.Wednesday}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', 1, '{exx.Thursday}', ';', NULL)
# , ('{spark1}', '{exx.sue}', '{exx.a23}', 2, '{exx.Friday}', ';', NULL)
# ;
# """
#     cursor0.execute(f"{insert_into_clause} {values2_clause}")
#     assert get_row_count(cursor0, vld_ii00105_tablename) == 3

#     # WHEN
#     etl_ideax_agg_tables_to_ideax_vld_tables(cursor0)

#     # THEN
#     select_vld_sqlstr = f"""
# SELECT *
# FROM {vld_ii00105_tablename}
# ORDER BY {kw.spark_num}, {kw.weekday_order};"""
#     cursor0.execute(select_vld_sqlstr)

#     rows = cursor0.fetchall()
#     for x_row in rows:
#         print(f"{x_row=}")
#     row0 = (spark1, exx.sue, exx.a23, 0, f'{exx.Wednesday}', ";")
#     row1 = (spark1, exx.sue, exx.a23, 1, f'{exx.Thursday}', ";")
#     row2 = (spark1, exx.sue, exx.a23, 2, f'{exx.Friday}', ";")
#     row3 = (spark1, exx.sue, exx.a23, 3, f'{exx.Saturday}', ";")
#     print(f"{rows[0]=}")
#     print(f"   {row0=}")
#     assert rows[0] == row0
#     assert rows[1] == row1
#     assert rows[2] == row2
#     assert rows[3] == row3
#     assert get_row_count(cursor0, vld_ii00105_tablename) == 4
