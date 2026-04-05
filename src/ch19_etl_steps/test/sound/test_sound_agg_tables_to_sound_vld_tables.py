from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_insert_into_sound_vld_sqlstrs,
)
from src.ch19_etl_steps.etl_main import etl_sound_agg_tables_to_sound_vld_tables
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_PopulatesTable_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    yao = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    create_sound_and_heard_tables(cursor0)
    personacontact_s_agg_put_tablename = prime_tbl(
        kw.person_contactunit, "s_agg", "put"
    )
    print(f"{get_table_columns(cursor0, personacontact_s_agg_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {personacontact_s_agg_put_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
)"""
    values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, personacontact_s_agg_put_tablename) == 4
    prnawar_h_vld_put_tablename = prime_tbl(kw.person_contactunit, kw.s_vld, "put")
    assert get_row_count(cursor0, prnawar_h_vld_put_tablename) == 0

    # WHEN
    sqlstr = get_insert_into_sound_vld_sqlstrs().get(prnawar_h_vld_put_tablename)
    print(sqlstr)
    cursor0.execute(sqlstr)

    # THEN
    assert get_row_count(cursor0, prnawar_h_vld_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
FROM {prnawar_h_vld_put_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (1, exx.sue, exx.a23, exx.yao, yao, 44.0, 22.0),
        (2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
    ]


def test_etl_sound_agg_tables_to_sound_vld_tables_Scenario0_AddRowsToTable(
    cursor0: Cursor,
):
    # ESTABLISH
    yao = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    create_sound_and_heard_tables(cursor0)
    prncont_s_agg_put_tablename = prime_tbl(kw.person_contactunit, "s_agg", "put")
    print(f"{get_table_columns(cursor0, prncont_s_agg_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prncont_s_agg_put_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
)"""
    values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, prncont_s_agg_put_tablename) == 4
    prncont_h_vld_put_tablename = prime_tbl(kw.person_contactunit, kw.s_vld, "put")
    assert get_row_count(cursor0, prncont_h_vld_put_tablename) == 0

    # WHEN
    etl_sound_agg_tables_to_sound_vld_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, prncont_h_vld_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
FROM {prncont_h_vld_put_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (1, exx.sue, exx.a23, exx.yao, yao, 44.0, 22.0),
        (2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
    ]


def test_etl_sound_agg_tables_to_sound_vld_tables_Scenario1_Populates_Columns(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    create_sound_and_heard_tables(cursor0)
    prncont_s_agg_put_tablename = prime_tbl(kw.person_contactunit, "s_agg", "put")
    print(f"{get_table_columns(cursor0, prncont_s_agg_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prncont_s_agg_put_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
)"""
    values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{exx.yao}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, prncont_s_agg_put_tablename) == 4
    prncont_h_vld_put_tablename = prime_tbl(kw.person_contactunit, kw.s_vld, "put")
    assert get_row_count(cursor0, prncont_h_vld_put_tablename) == 0

    # WHEN
    etl_sound_agg_tables_to_sound_vld_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, prncont_h_vld_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
FROM {prncont_h_vld_put_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (1, exx.sue, exx.a23, exx.yao, exx.yao, 44.0, 22.0),
        (2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
    ]


def test_etl_sound_agg_tables_to_sound_vld_tables_Scenario2_DoesNotSelectWhere_error_message_IsNotNull(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    create_sound_and_heard_tables(cursor0)
    prncont_s_agg_put_tablename = prime_tbl(kw.person_contactunit, "s_agg", "put")
    print(f"{get_table_columns(cursor0, prncont_s_agg_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prncont_s_agg_put_tablename} (
  {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
, {kw.error_message}
)"""
    values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{exx.yao}', {x44_credit}, {x22_debt}, NULL)
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt}, 'Data is not correct')
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt}, NULL)
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt}, NULL)
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, prncont_s_agg_put_tablename) == 4
    prncont_h_vld_put_tablename = prime_tbl(kw.person_contactunit, kw.s_vld, "put")
    assert get_row_count(cursor0, prncont_h_vld_put_tablename) == 0

    # WHEN
    etl_sound_agg_tables_to_sound_vld_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, prncont_h_vld_put_tablename) == 3
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.spark_face}
, {kw.moment_rope}
, {kw.person_name}
, {kw.contact_name}
, {kw.contact_cred_lumen}
, {kw.contact_debt_lumen}
FROM {prncont_h_vld_put_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (1, exx.sue, exx.a23, exx.yao, exx.yao, 44.0, 22.0),
        (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
    ]
