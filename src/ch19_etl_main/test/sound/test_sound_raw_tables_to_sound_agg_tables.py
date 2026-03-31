from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
from src.ch18_etl_config.etl_sqlstr import (
    CREATE_TRLROPE_SOUND_RAW_SQLSTR,
    create_prime_tablename,
    create_sound_and_heard_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
)
from src.ch19_etl_main.etl_main import (
    etl_sound_raw_tables_to_sound_agg_tables,
    insert_sound_raw_selects_into_sound_agg_tables,
    set_sound_raw_tables_error_message,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ExecutedSqlUpdatesTable_Scenario0(
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

    cursor0.execute(CREATE_TRLROPE_SOUND_RAW_SQLSTR)
    trlrope_str = "translate_rope"
    trlrope_s_raw_tablename = create_prime_tablename(trlrope_str, kw.s_raw)
    insert_into_clause = f"""INSERT INTO {trlrope_s_raw_tablename} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.otx_knot}
, {kw.inx_knot}
, {kw.unknown_str}
, {kw.error_message}
)"""
    b117 = "br00117"
    b045 = "br00045"
    b077 = "br00077"
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.yao}', '{yao_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.bob}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b077}', {spark1}, '{exx.sue}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL, NULL)
, ('{b045}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark5}, '{exx.sue}', '{exx.bob}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark7}, '{exx.yao}', '{exx.yao}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    error_count_sqlstr = f"SELECT COUNT(*) FROM {trlrope_s_raw_tablename} WHERE {kw.error_message} IS NOT NULL"
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 0

    # WHEN
    sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
        cursor0, trlrope_str
    )
    cursor0.execute(sqlstr)

    # THEN
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 2


def test_set_sound_raw_tables_error_message_UpdatesTable_Scenario0(cursor0: Cursor):
    # ESTABLISH
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    create_sound_and_heard_tables(cursor0)
    trlrope_s_raw_tablename = create_prime_tablename(kw.translate_rope, kw.s_raw)
    insert_into_clause = f"""INSERT INTO {trlrope_s_raw_tablename} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.otx_knot}
, {kw.inx_knot}
, {kw.unknown_str}
, {kw.error_message}
)"""
    b117 = "br00117"
    b045 = "br00045"
    b077 = "br00077"
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.yao}', '{yao_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.bob}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b077}', {spark1}, '{exx.sue}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL, NULL)
, ('{b045}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark5}, '{exx.sue}', '{exx.bob}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark7}, '{exx.yao}', '{exx.yao}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    error_count_sqlstr = f"SELECT COUNT(*) FROM {trlrope_s_raw_tablename} WHERE {kw.error_message} IS NOT NULL"
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 0

    # WHEN
    set_sound_raw_tables_error_message(cursor0)

    # THEN
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 2
    error_select_sqlstr = f"SELECT idea_number, spark_num FROM {trlrope_s_raw_tablename} WHERE {kw.error_message} IS NOT NULL"
    cursor0.execute(error_select_sqlstr)
    assert cursor0.fetchall() == [("br00117", 1), ("br00077", 1)]


def test_set_sound_raw_tables_error_message_UpdatesTable_Scenario1_person_raw_del(
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

    create_sound_and_heard_tables(cursor0)
    persona_s_raw_del = create_prime_tablename(kw.person_partnerunit, kw.s_raw, "del")
    insert_into_clause = f"""INSERT INTO {persona_s_raw_del} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}_ERASE
)"""
    b117 = "br00117"
    b045 = "br00045"
    b077 = "br00077"
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{bob_inx}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{bob_inx}')
, ('{b077}', {spark1}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}')
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    error_count_sqlstr = f"SELECT COUNT(*) FROM {persona_s_raw_del}"
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 4
    assert kw.error_message not in get_table_columns(cursor0, persona_s_raw_del)

    # WHEN
    set_sound_raw_tables_error_message(cursor0)

    # THEN No Error message is added and updated
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 4
    assert kw.error_message not in get_table_columns(cursor0, persona_s_raw_del)


def test_insert_sound_raw_selects_into_sound_agg_tables_PopulatesValidTable_Scenario0(
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

    create_sound_and_heard_tables(cursor0)
    trlrope_s_raw_tablename = create_prime_tablename("TRLROPE", kw.s_raw)
    insert_into_clause = f"""INSERT INTO {trlrope_s_raw_tablename} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.otx_knot}
, {kw.inx_knot}
, {kw.unknown_str}
, {kw.error_message}
)"""
    b117 = "br00117"
    b020 = "br00020"
    b045 = "br00045"
    inconsistent_data_str = "Inconsistent data"
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.yao}', '{yao_inx}', NULL, NULL, NULL, '{inconsistent_data_str}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.bob}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b117}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark5}, '{exx.sue}', '{exx.bob}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{inconsistent_data_str}')
, ('{b045}', {spark7}, '{exx.yao}', '{exx.yao}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', '{inconsistent_data_str}')
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    prnptnr_put_s_raw_tblname = create_prime_tablename("PRNPTNR", kw.s_raw, "put")
    insert_into_clause = f"""INSERT INTO {prnptnr_put_s_raw_tblname} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
, {kw.error_message}
)"""
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.yao}', NULL, NULL, '{inconsistent_data_str}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b020}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b020}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{exx.yao}', NULL, NULL, NULL)
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    trlrope_s_agg_tablename = create_prime_tablename("trlrope", "s_agg")
    prnptnr_put_s_agg_tblname = create_prime_tablename("PRNPTNR", "s_agg", "put")
    assert get_row_count(cursor0, trlrope_s_raw_tablename) == 7
    assert get_row_count(cursor0, prnptnr_put_s_raw_tblname) == 6
    assert get_row_count(cursor0, trlrope_s_agg_tablename) == 0
    assert get_row_count(cursor0, prnptnr_put_s_agg_tblname) == 0

    # WHEN
    insert_sound_raw_selects_into_sound_agg_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, trlrope_s_agg_tablename) == 2
    assert get_row_count(cursor0, prnptnr_put_s_agg_tblname) == 2

    select_agg_sqlstr = f"""SELECT * FROM {trlrope_s_agg_tablename};"""
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert len(rows) == 2
    assert rows == [
        (spark1, exx.sue, exx.bob, bob_inx, None, None, None, None),
        (spark2, exx.sue, exx.sue, exx.sue, rdx, rdx, ukx, None),
    ]

    select_agg_sqlstr = f"""SELECT * FROM {prnptnr_put_s_agg_tblname};"""
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert len(rows) == 2
    assert rows == [
        (spark1, exx.sue, exx.a23, exx.bob, exx.bob, None, None, None, None),
        (spark1, exx.sue, exx.a23, exx.yao, exx.yao, None, None, None, None),
    ]


def test_insert_sound_raw_selects_into_sound_agg_tables_PopulatesValidTable_Scenario1_del_table(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    b117 = "br00117"
    b020 = "br00020"
    create_sound_and_heard_tables(cursor0)
    prnptnr_del_s_raw_tblname = create_prime_tablename("PRNPTNR", kw.s_raw, "del")
    insert_into_clause = f"""INSERT INTO {prnptnr_del_s_raw_tblname} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}_ERASE
)"""
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.yao}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}')
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}')
, ('{b020}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}')
, ('{b020}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{exx.yao}')
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    prnptnr_del_s_agg_tblname = create_prime_tablename("PRNPTNR", "s_agg", "del")
    assert get_row_count(cursor0, prnptnr_del_s_raw_tblname) == 6
    assert get_row_count(cursor0, prnptnr_del_s_agg_tblname) == 0

    # WHEN
    insert_sound_raw_selects_into_sound_agg_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, prnptnr_del_s_agg_tblname) == 3

    select_agg_sqlstr = f"""SELECT * FROM {prnptnr_del_s_agg_tblname};"""
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (spark1, exx.sue, exx.a23, exx.bob, exx.bob, None),
        (spark1, exx.sue, exx.a23, exx.bob, exx.yao, None),
        (spark1, exx.sue, exx.a23, exx.yao, exx.yao, None),
    ]


def test_etl_sound_raw_tables_to_sound_agg_tables_PopulatesValidTable_Scenario0(
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

    create_sound_and_heard_tables(cursor0)
    trlrope_s_raw_tablename = create_prime_tablename("TRLROPE", kw.s_raw)
    insert_into_clause = f"""INSERT INTO {trlrope_s_raw_tablename} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.otx_rope}
, {kw.inx_rope}
, {kw.otx_knot}
, {kw.inx_knot}
, {kw.unknown_str}
, {kw.error_message}
)"""
    b117 = "br00117"
    b020 = "br00020"
    b045 = "br00045"
    inconsistent_data_str = "Inconsistent data"
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.yao}', '{yao_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.yao}', '{exx.yao}', NULL, NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.bob}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b117}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark2}, '{exx.sue}', '{exx.sue}', '{exx.sue}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark5}, '{exx.sue}', '{exx.bob}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {spark7}, '{exx.yao}', '{exx.bob}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    prnptnr_put_s_raw_tblname = create_prime_tablename("PRNPTNR", kw.s_raw, "put")
    insert_into_clause = f"""INSERT INTO {prnptnr_put_s_raw_tblname} (
  {kw.idea_number}
, {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
, {kw.error_message}
)"""
    values_clause = f"""
VALUES
  ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.yao}', NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b117}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b020}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.bob}', '{exx.bob}', NULL, NULL, NULL)
, ('{b020}', {spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{exx.yao}', NULL, NULL, NULL)
;
"""
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    trlrope_s_agg_tablename = create_prime_tablename("trlrope", "s_agg")
    prnptnr_put_s_agg_tblname = create_prime_tablename("PRNPTNR", "s_agg", "put")
    assert get_row_count(cursor0, trlrope_s_raw_tablename) == 8
    assert get_row_count(cursor0, prnptnr_put_s_raw_tblname) == 7
    assert get_row_count(cursor0, trlrope_s_agg_tablename) == 0
    assert get_row_count(cursor0, prnptnr_put_s_agg_tblname) == 0

    # WHEN
    etl_sound_raw_tables_to_sound_agg_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, trlrope_s_agg_tablename) == 4
    assert get_row_count(cursor0, prnptnr_put_s_agg_tblname) == 3

    select_agg_sqlstr = f"""SELECT * FROM {trlrope_s_agg_tablename};"""
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    ex_row0 = (spark1, exx.sue, exx.bob, bob_inx, None, None, None, None)
    ex_row1 = (spark2, exx.sue, exx.sue, exx.sue, rdx, rdx, ukx, None)
    ex_row2 = (spark5, exx.sue, exx.bob, bob_inx, rdx, rdx, ukx, None)
    ex_row3 = (spark7, exx.yao, exx.bob, yao_inx, rdx, rdx, ukx, None)
    print(f"{rows[0]=}")
    print(f"{ex_row0=}")
    assert rows[0] == ex_row0
    assert rows == [ex_row0, ex_row1, ex_row2, ex_row3]

    select_agg_sqlstr = f"""SELECT * FROM {prnptnr_put_s_agg_tblname};"""
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (spark1, exx.sue, exx.a23, exx.bob, exx.bob, None, None, None, None),
        (spark1, exx.sue, exx.a23, exx.bob, exx.yao, None, None, None, None),
        (spark1, exx.sue, exx.a23, exx.yao, exx.yao, None, None, None, None),
    ]
