from ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from ch17_brick.brick_db_tool import create_brick_sorted_table
from ch20_etl_brick.etl_brick_main import (
    etl_brixk_agg_tables_to_sparks_brixk_agg_table,
    etl_sparks_brixk_agg_db_to_spark_dict,
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table,
    get_create_sparks_brixk_agg_sqlstr,
    get_create_sparks_brixk_vld_sqlstr,
)
from ref.keywords import Ch20Keywords as kw, ExampleStrs as exx
from sqlite3 import Cursor


def test_get_create_sparks_brixk_agg_sqlstr_ReturnsObj():
    # ESTABLISH / WHEN
    create_sparks_brixk_agg_sqlstr = get_create_sparks_brixk_agg_sqlstr()
    # THEN
    expected_create_sparks_brixk_agg_sqlstr = "CREATE TABLE IF NOT EXISTS sparks_brixk_agg (brick_type TEXT, spark_num INTEGER, spark_face TEXT, error_message TEXT)"
    assert create_sparks_brixk_agg_sqlstr == expected_create_sparks_brixk_agg_sqlstr


def test_get_create_sparks_brixk_vld_sqlstr_ReturnsObj():
    # ESTABLISH / WHEN
    create_sparks_brixk_vld_sqlstr = get_create_sparks_brixk_vld_sqlstr()
    # THEN
    expected_create_sparks_brixk_vld_sqlstr = "CREATE TABLE IF NOT EXISTS sparks_brixk_vld (spark_num INTEGER, spark_face TEXT)"
    assert create_sparks_brixk_vld_sqlstr == expected_create_sparks_brixk_vld_sqlstr


def test_etl_brixk_agg_tables_to_sparks_brixk_agg_table_PopulatesTables_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_bk00103_tablename = f"bk00103_{kw.brixk_agg}"
    agg_bk00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_brick_sorted_table(cursor0, agg_bk00103_tablename, agg_bk00103_columns)
    insert_into_clause = f"""INSERT INTO {agg_bk00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
)"""
    values_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_360}', '{hour6am}')
, ('{spark1}', '{exx.sue}', '{exx.a23}', '{minute_420}', '{hour7am}')
, ('{spark3}', '{exx.yao}', '{exx.a23}', '{minute_420}', '{hour7am}')
, ('{spark9}', '{exx.yao}', '{exx.a23}', '{minute_420}', '{hour7am}')
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    brick_sparks_tablename = kw.sparks_brixk_agg
    assert get_row_count(cursor0, agg_bk00103_tablename) == 4
    assert not db_table_exists(cursor0, brick_sparks_tablename)

    # WHEN
    etl_brixk_agg_tables_to_sparks_brixk_agg_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, brick_sparks_tablename)
    brick_sparks_table_cols = set(get_table_columns(cursor0, brick_sparks_tablename))
    assert len(brick_sparks_table_cols) == 4
    assert kw.brick_type in brick_sparks_table_cols
    assert kw.spark_face in brick_sparks_table_cols
    assert kw.spark_num in brick_sparks_table_cols
    assert kw.error_message in brick_sparks_table_cols
    assert get_row_count(cursor0, brick_sparks_tablename) == 3
    select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.spark_face};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 3
    sue_r = ("bk00103", spark1, exx.sue, None)
    yao3_r = ("bk00103", spark3, exx.yao, None)
    yao9_r = ("bk00103", spark9, exx.yao, None)
    print(f"{rows[0]=}")
    assert rows[0] == sue_r
    assert rows[1] == yao3_r
    assert rows[2] == yao9_r


def test_etl_brixk_agg_tables_to_sparks_brixk_agg_table_PopulatesTables_Scenario1(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_bk00103_tablename = f"bk00103_{kw.brixk_agg}"
    agg_bk00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_brick_sorted_table(cursor0, agg_bk00103_tablename, agg_bk00103_columns)
    insert_into_clause = f"""INSERT INTO {agg_bk00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
)"""
    values_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', "{exx.a23}", '{hour6am}', '{minute_360}')
, ('{spark1}', '{exx.sue}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark1}', '{exx.yao}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark9}', '{exx.yao}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark3}', '{exx.bob}', "{exx.a23}", '{hour7am}', '{minute_420}')
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    brick_sparks_tablename = kw.sparks_brixk_agg
    assert get_row_count(cursor0, agg_bk00103_tablename) == 5
    assert not db_table_exists(cursor0, brick_sparks_tablename)

    # WHEN
    etl_brixk_agg_tables_to_sparks_brixk_agg_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, brick_sparks_tablename)
    assert get_row_count(cursor0, brick_sparks_tablename) == 4
    select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.spark_face};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 4
    invalid_str = "invalid because of conflicting spark_num"
    bob_row = ("bk00103", spark3, exx.bob, None)
    sue_row = ("bk00103", spark1, exx.sue, invalid_str)
    yao1_row = ("bk00103", spark1, exx.yao, invalid_str)
    yao9_row = ("bk00103", spark9, exx.yao, None)

    assert rows[0] == sue_row
    assert rows[1] == yao1_row
    assert rows[2] == bob_row
    assert rows[3] == yao9_row


def test_etl_brixk_agg_tables_to_sparks_brixk_agg_table_PopulatesTables_Scenario2_DuplicateRowsNotKept(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_bk00103_tablename = f"bk00103_{kw.brixk_agg}"
    agg_bk00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_brick_sorted_table(cursor0, agg_bk00103_tablename, agg_bk00103_columns)
    insert_into_clause = f"""INSERT INTO {agg_bk00103_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
)"""
    values_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', "{exx.a23}", '{hour6am}', '{minute_360}')
, ('{spark1}', '{exx.sue}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark1}', '{exx.yao}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark9}', '{exx.yao}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark3}', '{exx.bob}', "{exx.a23}", '{hour7am}', '{minute_420}')
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    brick_sparks_tablename = kw.sparks_brixk_agg
    assert not db_table_exists(cursor0, brick_sparks_tablename)
    etl_brixk_agg_tables_to_sparks_brixk_agg_table(cursor0)
    assert get_row_count(cursor0, brick_sparks_tablename) == 4
    spark7 = 7
    values2_clause = f"""
VALUES     
  ('{spark1}', '{exx.sue}', "{exx.a23}", '{hour6am}', '{minute_360}')
, ('{spark1}', '{exx.sue}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark1}', '{exx.yao}', "{exx.a23}", '{hour7am}', '{minute_420}')
, ('{spark7}', '{exx.yao}', "{exx.a23}", '{hour7am}', '{minute_420}')
;
"""
    cursor0.execute(f"{insert_into_clause} {values2_clause}")
    assert get_row_count(cursor0, brick_sparks_tablename) == 4
    # WHEN
    etl_brixk_agg_tables_to_sparks_brixk_agg_table(cursor0)
    # THEN
    assert get_row_count(cursor0, brick_sparks_tablename) == 5

    select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.spark_face};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    invalid_str = "invalid because of conflicting spark_num"
    bob_row = ("bk00103", spark3, exx.bob, None)
    sue_row = ("bk00103", spark1, exx.sue, invalid_str)
    yao1_row = ("bk00103", spark1, exx.yao, invalid_str)
    yao7_row = ("bk00103", spark7, exx.yao, None)
    yao9_row = ("bk00103", spark9, exx.yao, None)

    assert rows[0] == sue_row
    assert rows[1] == yao1_row
    assert rows[2] == bob_row
    assert rows[3] == yao7_row
    assert rows[4] == yao9_row


def test_etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table_PopulatesTables_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    agg_sparks_tablename = kw.sparks_brixk_agg
    agg_sparks_columns = [
        kw.brick_type,
        kw.spark_num,
        kw.spark_face,
        kw.error_message,
    ]
    create_brick_sorted_table(cursor0, agg_sparks_tablename, agg_sparks_columns)
    insert_into_clause = f"""INSERT INTO {agg_sparks_tablename} (
  {kw.brick_type}
, {kw.spark_num}
, {kw.spark_face}
, {kw.error_message}
)"""
    invalid_str = "invalid because of conflicting spark_num"
    values_clause = f"""
VALUES
  ('bk00103', {spark3}, '{exx.bob}', NULL)
, ('bk00103', {spark1}, '{exx.sue}', '{invalid_str}')
, ('bk00103', {spark1}, '{exx.yao}', '{invalid_str}')
, ('bk00103', {spark9}, '{exx.yao}', NULL)  
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, agg_sparks_tablename) == 4
    valid_sparks_tablename = kw.sparks_brixk_vld
    assert not db_table_exists(cursor0, valid_sparks_tablename)

    # WHEN
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, valid_sparks_tablename)
    assert get_row_count(cursor0, valid_sparks_tablename) == 2
    select_agg_sqlstr = f"""
SELECT * 
FROM {valid_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.spark_face};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 2
    bob_row = (spark3, exx.bob)
    yao9_row = (spark9, exx.yao)

    assert rows[0] == bob_row
    assert rows[1] == yao9_row


def test_etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table_PopulatesTables_Scenario1_DuplicateRows(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    agg_sparks_tablename = kw.sparks_brixk_agg
    agg_sparks_columns = [
        kw.brick_type,
        kw.spark_num,
        kw.spark_face,
        kw.error_message,
    ]
    create_brick_sorted_table(cursor0, agg_sparks_tablename, agg_sparks_columns)
    insert_into_clause = f"""INSERT INTO {agg_sparks_tablename} (
  {kw.brick_type}
, {kw.spark_num}
, {kw.spark_face}
, {kw.error_message}
)"""
    invalid_str = "invalid because of conflicting spark_num"
    values_clause = f"""
VALUES
  ('bk00103', {spark3}, '{exx.bob}', NULL)
, ('bk00103', {spark1}, '{exx.sue}', '{invalid_str}')
, ('bk00103', {spark1}, '{exx.yao}', '{invalid_str}')
, ('bk00103', {spark9}, '{exx.yao}', NULL)  
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, agg_sparks_tablename) == 4
    valid_sparks_tablename = kw.sparks_brixk_vld
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table(cursor0)
    assert get_row_count(cursor0, valid_sparks_tablename) == 2
    spark7 = 7
    values2_clause = f"""
VALUES
  ('bk00103', {spark3}, '{exx.bob}', NULL)
, ('bk00103', {spark7}, '{exx.yao}', NULL)  
;
"""
    cursor0.execute(f"{insert_into_clause} {values2_clause}")
    assert get_row_count(cursor0, valid_sparks_tablename) == 2
    # WHEN
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table(cursor0)
    # THEN
    assert get_row_count(cursor0, valid_sparks_tablename) == 3

    select_agg_sqlstr = f"""
SELECT * 
FROM {valid_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.spark_face};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    bob_row = (spark3, exx.bob)
    yao7_row = (spark7, exx.yao)
    yao9_row = (spark9, exx.yao)

    assert rows[0] == bob_row
    assert rows[1] == yao7_row
    assert rows[2] == yao9_row


def test_etl_sparks_brixk_agg_db_to_spark_dict_ReturnsObj_Scenario0(cursor0: Cursor):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    agg_columns = [kw.spark_face, kw.spark_num, kw.error_message]
    agg_sparks_tablename = kw.sparks_brixk_agg
    create_brick_sorted_table(cursor0, agg_sparks_tablename, agg_columns)
    insert_into_clause = f"""
INSERT INTO {agg_sparks_tablename} ({kw.spark_num}, {kw.spark_face}, {kw.error_message})
VALUES     
  ('{spark3}', '{exx.bob}', NULL)
, ('{spark1}', '{exx.sue}', 'invalid because of conflicting spark_num')
, ('{spark1}', '{exx.yao}', 'invalid because of conflicting spark_num')
, ('{spark9}', '{exx.yao}', NULL)
, ('{spark9}', '{exx.yao}', NULL)
, ('{spark9}', '{exx.yao}', NULL)
;
"""
    cursor0.execute(insert_into_clause)
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table(cursor0)
    assert get_row_count(cursor0, agg_sparks_tablename) == 6

    # WHEN
    sparks_dict = etl_sparks_brixk_agg_db_to_spark_dict(cursor0)

    # THEN
    assert sparks_dict == {spark3: exx.bob, spark9: exx.yao}
