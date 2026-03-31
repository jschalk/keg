from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch18_etl_config.etl_sqlstr import create_prime_tablename
from src.ch19_etl_main.etl_main import (
    create_sound_and_heard_tables,
    etl_heard_raw_tables_to_moment_ote1_agg,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_heard_raw_tables_to_moment_ote1_agg_SetsTableAttr(cursor0: Cursor):
    # ESTABLISH
    spark3 = 3
    spark7 = 7
    amy45_rope = f"{exx.dash}amy45{exx.dash}"
    timenum55 = 55
    timenum66 = 66
    timenum77 = 77
    create_sound_and_heard_tables(cursor0)
    momentbud_h_raw_table = create_prime_tablename(kw.moment_budunit, kw.h_raw)
    insert_raw_sqlstr = f"""
INSERT INTO {momentbud_h_raw_table} ({kw.spark_num}, {kw.moment_rope}_inx, {kw.person_name}_inx, {kw.bud_time}, {kw.knot})
VALUES
  ({spark3}, '{exx.a23_dash}', '{exx.bob}', {timenum55}, '{exx.dash}')
, ({spark3}, '{exx.a23_dash}', '{exx.bob}', {timenum55}, '{exx.dash}')
, ({spark3}, '{amy45_rope}', '{exx.sue}', {timenum55}, '{exx.dash}')
, ({spark7}, '{amy45_rope}', '{exx.sue}', {timenum66}, '{exx.dash}')
;
"""
    cursor0.execute(insert_raw_sqlstr)
    assert get_row_count(cursor0, momentbud_h_raw_table) == 4
    assert db_table_exists(cursor0, kw.moment_ote1_agg) is False

    # WHEN
    etl_heard_raw_tables_to_moment_ote1_agg(cursor0)

    # THEN
    assert db_table_exists(cursor0, kw.moment_ote1_agg)
    assert get_row_count(cursor0, kw.moment_ote1_agg) == 3
    cursor0.execute(f"SELECT * FROM {kw.moment_ote1_agg};")
    momentunit_agg_rows = cursor0.fetchall()
    ex_row0 = (exx.a23_dash, exx.bob, spark3, timenum55, exx.dash, None)
    ex_row1 = (amy45_rope, exx.sue, spark3, timenum55, exx.dash, None)
    ex_row2 = (amy45_rope, exx.sue, spark7, timenum66, exx.dash, None)
    print(f"{momentunit_agg_rows[0]=}")
    print(f"{momentunit_agg_rows[1]=}")
    print(f"{momentunit_agg_rows[2]=}")
    assert momentunit_agg_rows[0] == ex_row0
    assert momentunit_agg_rows == [ex_row0, ex_row1, ex_row2]
