from ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from ch17_idea.idea_db_tool import create_idea_sorted_table
from ch20_etl_idea.etl_idea_main import etl_ideax_raw_tables_to_ideax_agg_tables
from ref.keywords import Ch20Keywords as kw, ExampleStrs as exx
from sqlite3 import Cursor


def test_etl_ideax_raw_tables_to_ideax_agg_tables_PopulatesAggTable_Scenario0_GroupByWorks(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    raw_ii00103_tablename = f"ii00103_{kw.ideax_raw}"
    raw_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
        kw.knot,
        kw.error_message,
    ]
    create_idea_sorted_table(cursor0, raw_ii00103_tablename, raw_ii00103_columns)
    insert_into_clause = f"""INSERT INTO {raw_ii00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
, {kw.knot}
, {kw.error_message}
)"""
    values_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', ';', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', NULL)
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    assert get_row_count(cursor0, raw_ii00103_tablename) == 3
    assert not db_table_exists(cursor0, agg_ii00103_tablename)

    # WHEN
    etl_ideax_raw_tables_to_ideax_agg_tables(cursor0)

    # THEN
    assert db_table_exists(cursor0, agg_ii00103_tablename)
    assert get_row_count(cursor0, agg_ii00103_tablename) == 2

    ii00103_table_cols = get_table_columns(cursor0, agg_ii00103_tablename)
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str not in set(ii00103_table_cols[0])
    assert filename_str not in set(ii00103_table_cols[1])
    assert sheet_name_str not in set(ii00103_table_cols[2])
    select_agg_sqlstr = f"""
SELECT * 
FROM {agg_ii00103_tablename} 
ORDER BY {kw.spark_num}, {kw.cumulative_minute};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 2
    e1 = spark1
    m_360 = minute_360
    m_420 = minute_420
    row0 = (e1, exx.sue, exx.a23, m_360, hour6am, ";")
    row1 = (e1, exx.sue, exx.a23, m_420, hour7am, ";")
    print(f"{rows[0]=}")
    print(f"   {row0=}")
    assert rows[0] == row0
    assert rows[1] == row1


def test_etl_ideax_raw_tables_to_ideax_agg_tables_PopulatesAggTable_Scenario1_GroupByOnlyNonConflictingRecords(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"

    raw_ii00103_tablename = f"ii00103_{kw.ideax_raw}"
    raw_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
        kw.knot,
        kw.error_message,
    ]
    create_idea_sorted_table(cursor0, raw_ii00103_tablename, raw_ii00103_columns)
    insert_into_clause = f"""INSERT INTO {raw_ii00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
, {kw.knot}
, {kw.error_message}
)"""
    values_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', '/', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', '/', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour8am}', '/', NULL)
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    assert get_row_count(cursor0, raw_ii00103_tablename) == 3
    assert not db_table_exists(cursor0, agg_ii00103_tablename)

    # WHEN
    etl_ideax_raw_tables_to_ideax_agg_tables(cursor0)

    # THEN
    assert db_table_exists(cursor0, agg_ii00103_tablename)
    assert get_row_count(cursor0, agg_ii00103_tablename) == 1

    ii00103_table_cols = get_table_columns(cursor0, agg_ii00103_tablename)
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str not in set(ii00103_table_cols[0])
    assert filename_str not in set(ii00103_table_cols[1])
    assert sheet_name_str not in set(ii00103_table_cols[2])
    select_agg_sqlstr = f"""SELECT * FROM {agg_ii00103_tablename};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 1
    e1 = spark1
    m_360 = minute_360
    row0 = (e1, exx.sue, exx.a23, m_360, hour6am, "/")
    print(f"{rows[0]=}")
    print(f"   {row0=}")
    assert rows[0] == row0


def test_etl_ideax_raw_tables_to_ideax_agg_tables_PopulatesAggTable_Scenario2_GroupByExcludesRowsWith_error_message(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    raw_ii00103_tablename = f"ii00103_{kw.ideax_raw}"
    raw_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
        kw.knot,
        kw.error_message,
    ]
    create_idea_sorted_table(cursor0, raw_ii00103_tablename, raw_ii00103_columns)
    insert_into_clause = f"""INSERT INTO {raw_ii00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
, {kw.knot}
, {kw.error_message}
)"""
    values_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}', ';', 'some_error')
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', NULL)
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}', ';', 'some_error')
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_480}', '{hour8am}', ';', NULL)
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    assert get_row_count(cursor0, raw_ii00103_tablename) == 4
    assert not db_table_exists(cursor0, agg_ii00103_tablename)

    # WHEN
    etl_ideax_raw_tables_to_ideax_agg_tables(cursor0)

    # THEN
    select_agg_sqlstr = f"""
SELECT * 
FROM {agg_ii00103_tablename} 
ORDER BY {kw.spark_num}, {kw.cumulative_minute};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 2
    row0 = (spark1, exx.sue, exx.a23, minute_420, hour7am, ";")
    row1 = (spark1, exx.sue, exx.a23, minute_480, hour8am, ";")
    print(f"{rows[0]=}")
    print(f"   {row0=}")
    assert rows[0] == row0
    assert rows[1] == row1
