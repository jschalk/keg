from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch17_idea.idea_db_tool import create_idea_sorted_table
from src.ch19_etl_steps.etl_main import (
    etl_brick_agg_tables_to_sparks_brick_agg_table,
    etl_sparks_brick_agg_db_to_spark_dict,
    etl_sparks_brick_agg_table_to_sparks_brick_valid_table,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_brick_agg_tables_to_sparks_brick_agg_table_PopulatesTables_Scenario0(
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
    agg_br00003_tablename = f"br00003_{kw.brick_agg}"
    agg_br00003_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_idea_sorted_table(cursor0, agg_br00003_tablename, agg_br00003_columns)
    insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {kw.spark_num}
, {kw.face_name}
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
    brick_sparks_tablename = kw.sparks_brick_agg
    assert get_row_count(cursor0, agg_br00003_tablename) == 4
    assert not db_table_exists(cursor0, brick_sparks_tablename)

    # WHEN
    etl_brick_agg_tables_to_sparks_brick_agg_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, brick_sparks_tablename)
    brick_sparks_table_cols = set(get_table_columns(cursor0, brick_sparks_tablename))
    assert len(brick_sparks_table_cols) == 4
    assert kw.idea_number in brick_sparks_table_cols
    assert kw.face_name in brick_sparks_table_cols
    assert kw.spark_num in brick_sparks_table_cols
    assert kw.error_message in brick_sparks_table_cols
    assert get_row_count(cursor0, brick_sparks_tablename) == 3
    select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.face_name};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 3
    sue_r = ("br00003", spark1, exx.sue, None)
    yao3_r = ("br00003", spark3, exx.yao, None)
    yao9_r = ("br00003", spark9, exx.yao, None)
    print(f"{rows[0]=}")
    assert rows[0] == sue_r
    assert rows[1] == yao3_r
    assert rows[2] == yao9_r


def test_etl_brick_agg_tables_to_sparks_brick_agg_table_PopulatesTables_Scenario1(
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
    agg_br00003_tablename = f"br00003_{kw.brick_agg}"
    agg_br00003_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_idea_sorted_table(cursor0, agg_br00003_tablename, agg_br00003_columns)
    insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {kw.spark_num}
, {kw.face_name}
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
    brick_sparks_tablename = kw.sparks_brick_agg
    assert get_row_count(cursor0, agg_br00003_tablename) == 5
    assert not db_table_exists(cursor0, brick_sparks_tablename)

    # WHEN
    etl_brick_agg_tables_to_sparks_brick_agg_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, brick_sparks_tablename)
    assert get_row_count(cursor0, brick_sparks_tablename) == 4
    select_agg_sqlstr = f"""
SELECT * 
FROM {brick_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.face_name};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 4
    invalid_str = "invalid because of conflicting spark_num"
    bob_row = ("br00003", spark3, exx.bob, None)
    sue_row = ("br00003", spark1, exx.sue, invalid_str)
    yao1_row = ("br00003", spark1, exx.yao, invalid_str)
    yao9_row = ("br00003", spark9, exx.yao, None)

    assert rows[0] == sue_row
    assert rows[1] == yao1_row
    assert rows[2] == bob_row
    assert rows[3] == yao9_row


def test_etl_sparks_brick_agg_table_to_sparks_brick_valid_table_PopulatesTables_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    agg_sparks_tablename = kw.sparks_brick_agg
    agg_sparks_columns = [
        kw.idea_number,
        kw.spark_num,
        kw.face_name,
        kw.error_message,
    ]
    create_idea_sorted_table(cursor0, agg_sparks_tablename, agg_sparks_columns)
    insert_into_clause = f"""INSERT INTO {agg_sparks_tablename} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.error_message}
)"""
    invalid_str = "invalid because of conflicting spark_num"
    values_clause = f"""
VALUES
  ('br00003', {spark3}, '{exx.bob}', NULL)
, ('br00003', {spark1}, '{exx.sue}', '{invalid_str}')
, ('br00003', {spark1}, '{exx.yao}', '{invalid_str}')
, ('br00003', {spark9}, '{exx.yao}', NULL)  
;
"""
    insert_sqlstr = f"{insert_into_clause} {values_clause}"
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, agg_sparks_tablename) == 4
    valid_sparks_tablename = kw.sparks_brick_valid
    assert not db_table_exists(cursor0, valid_sparks_tablename)

    # WHEN
    etl_sparks_brick_agg_table_to_sparks_brick_valid_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, valid_sparks_tablename)
    assert get_row_count(cursor0, valid_sparks_tablename) == 2
    select_agg_sqlstr = f"""
SELECT * 
FROM {valid_sparks_tablename} 
ORDER BY {kw.spark_num}, {kw.face_name};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 2
    bob_row = (spark3, exx.bob)
    yao9_row = (spark9, exx.yao)

    assert rows[0] == bob_row
    assert rows[1] == yao9_row


def test_etl_sparks_brick_agg_db_to_spark_dict_ReturnsObj_Scenario0(cursor0: Cursor):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    agg_columns = [kw.face_name, kw.spark_num, kw.error_message]
    agg_sparks_tablename = kw.sparks_brick_agg
    create_idea_sorted_table(cursor0, agg_sparks_tablename, agg_columns)
    insert_into_clause = f"""
INSERT INTO {agg_sparks_tablename} ({kw.spark_num}, {kw.face_name}, {kw.error_message})
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
    etl_sparks_brick_agg_table_to_sparks_brick_valid_table(cursor0)
    assert get_row_count(cursor0, agg_sparks_tablename) == 6

    # WHEN
    sparks_dict = etl_sparks_brick_agg_db_to_spark_dict(cursor0)

    # THEN
    assert sparks_dict == {spark3: exx.bob, spark9: exx.yao}
