from ch17_idea.idea_db_tool import create_idea_sorted_table
from ch18_etl_config.etl_sqlstr import create_sound_and_heard_tables
from ch23_lynx.lynx import get_max_ideax_agg_spark_num
from ref.keywords import Ch23Keywords as kw, ExampleStrs as exx
from sqlite3 import Cursor


def test_get_max_ideax_agg_spark_num_ReturnsObj_Scenario0_NoTables(cursor0: Cursor):
    # ESTABLISH
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    agg_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)

    # WHEN / THEN
    assert get_max_ideax_agg_spark_num(cursor0) == 1


def test_get_max_ideax_agg_spark_num_ReturnsObj_Scenario1_OneTable(cursor0: Cursor):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    agg_ii00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
    insert_into_clause = f"""INSERT INTO {agg_ii00103_tablename} (
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

    # WHEN
    max_spark_num = get_max_ideax_agg_spark_num(cursor0)

    # THEN
    assert max_spark_num
    assert max_spark_num == spark9


def test_get_max_ideax_agg_spark_num_ReturnsObj_Scenario2_MultipleTable(
    cursor0: Cursor,
):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    create_sound_and_heard_tables(cursor0)
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    agg_ii00103_columns = [kw.spark_num]
    create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
    agg_ii00103_insert_sqlstr = f"""
INSERT INTO {agg_ii00103_tablename} ({kw.spark_num})
VALUES ('{spark1}'), ('{spark1}'), ('{spark9}');"""
    cursor0.execute(agg_ii00103_insert_sqlstr)

    agg_ii00144_tablename = f"ii00144_{kw.ideax_agg}"
    agg_ii00144_columns = [kw.spark_num]
    create_idea_sorted_table(cursor0, agg_ii00144_tablename, agg_ii00144_columns)
    agg_ii00144_insert_sqlstr = f"""
INSERT INTO {agg_ii00144_tablename} ({kw.spark_num})
VALUES ('{spark3}');"""
    cursor0.execute(agg_ii00144_insert_sqlstr)

    # WHEN
    max_spark_num = get_max_ideax_agg_spark_num(cursor0)

    # THEN
    assert max_spark_num
    assert max_spark_num == spark9
