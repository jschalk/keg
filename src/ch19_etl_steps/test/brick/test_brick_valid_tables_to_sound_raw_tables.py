from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch17_idea.idea_db_tool import create_idea_sorted_table
from src.ch18_etl_config.etl_sqlstr import create_prime_tablename
from src.ch19_etl_steps.etl_main import etl_brick_valid_tables_to_sound_raw_tables
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx

# get examples from tests from etl_brick_agg_dfs_to_translate_title_raw
# get examples from tests from etl_brick_agg_dfs_to_translate_rope_raw
# get examples from tests from etl_brick_agg_dfs_to_translate__raw
# get examples from tests from etl_brick_agg_dfs_to_translate_rope_raw


def test_etl_brick_valid_tables_to_sound_raw_tables_PopulatesValidTable_Scenario0_Only_valid_sparks(
    cursor0: Cursor,
):
    # ESTABLISH
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    br00117_valid_tablename = f"br00117_{kw.brick_valid}"
    br00117_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_rope,
        kw.inx_rope,
        kw.knot,
    ]
    create_idea_sorted_table(cursor0, br00117_valid_tablename, set(br00117_columns))
    insert_into_clause = f"""INSERT INTO {br00117_valid_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.knot}
)"""
    values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.yao}', '{exx.yao}', '{yao_inx}', ';')
, ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', '{exx.bob}', '{bob_inx}', ';')
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")

    br00045_valid_tablename = f"br00045_{kw.brick_valid}"
    br00045_columns = [
        kw.spark_num,
        kw.face_name,
        kw.otx_rope,
        kw.inx_rope,
        kw.otx_knot,
        kw.inx_knot,
        kw.knot,
        kw.unknown_str,
    ]
    create_idea_sorted_table(cursor0, br00045_valid_tablename, br00045_columns)
    insert_into_clause = f"""INSERT INTO {br00045_valid_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.otx_knot}
, {kw.inx_knot}
, {kw.knot}
, {kw.unknown_str}
)"""
    values_clause = f"""
VALUES
  ({spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', ';', '{ukx}')
, ({spark5}, '{exx.sue}', '{exx.bob}', '{bob_inx}', '{rdx}', '{rdx}', ';', '{ukx}')
, ({spark7}, '{exx.yao}', '{exx.yao}', '{yao_inx}', '{rdx}', '{rdx}', ';', '{ukx}')
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, br00117_valid_tablename) == 2
    assert get_row_count(cursor0, br00045_valid_tablename) == 3
    trlrope_s_raw_tablename = create_prime_tablename("TRLROPE", kw.s_raw)
    prncont_put_s_raw_tblname = create_prime_tablename("PRNCONT", kw.s_raw, "put")
    assert not db_table_exists(cursor0, trlrope_s_raw_tablename)
    assert not db_table_exists(cursor0, prncont_put_s_raw_tblname)

    # WHEN
    etl_brick_valid_tables_to_sound_raw_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, trlrope_s_raw_tablename) == 5
    assert get_row_count(cursor0, prncont_put_s_raw_tblname) == 2
    b117 = "br00117"
    b045 = "br00045"
    ex_row0 = (b117, spark1, exx.sue, exx.yao, yao_inx, None, None, None, None)
    ex_row1 = (b117, spark1, exx.sue, exx.bob, bob_inx, None, None, None, None)
    ex_row2 = (b045, spark2, exx.sue, exx.sue, exx.sue, rdx, rdx, ukx, None)
    ex_row3 = (b045, spark5, exx.sue, exx.bob, bob_inx, rdx, rdx, ukx, None)
    ex_row4 = (b045, spark7, exx.yao, exx.yao, yao_inx, rdx, rdx, ukx, None)
    select_agg_sqlstr = f"""SELECT * FROM {trlrope_s_raw_tablename};"""
    cursor0.execute(select_agg_sqlstr)

    rows = cursor0.fetchall()
    assert len(rows) == 5
    # print(f"{ex_rope2=}")
    # print(f"{rows[0]=}")
    assert rows[0] == ex_row2
    assert rows[1] == ex_row3
    assert rows[2] == ex_row4
    assert rows[3] == ex_row0
    assert rows[4] == ex_row1

    select_agg_sqlstr = f"""SELECT * FROM {prncont_put_s_raw_tblname};"""
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    # print(rows)
    print(f"{rows[0]=}")
    assert len(rows) == 2
    ex_row_b0 = (b117, 1, exx.sue, exx.a23, exx.bob, exx.yao, None, None, ";", None)
    ex_row_b1 = (b117, 1, exx.sue, exx.a23, exx.bob, exx.bob, None, None, ";", None)
    assert rows[0] == ex_row_b0
    assert rows == [ex_row_b0, ex_row_b1]
