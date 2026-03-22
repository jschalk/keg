from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_table_columns
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    create_update_heard_raw_empty_inx_col_sqlstr,
    create_update_heard_raw_existing_inx_col_sqlstr,
)
from src.ch19_etl_main.etl_main import set_all_heard_raw_inx_columns
from src.ch19_etl_main.test._util.ch19_env import cursor0
from src.ref.keywords import Ch19Keywords as kw


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario0_FullTranslateTables(
    cursor0: Cursor,
):
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    create_sound_and_heard_tables(cursor0)
    prnawar_dimen = kw.person_plan_awardunit
    prnawar_h_raw_put_tablename = prime_tbl(prnawar_dimen, "h_raw", "put")
    # print(f"{get_table_columns(cursor0, prnawar_h_raw_put_tablename)=}")
    insert_face_name_only_sqlstr = f"""INSERT INTO {prnawar_h_raw_put_tablename} 
    ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
    VALUES
      ({spark1}, '{sue_otx}', NULL)
    , ({spark2}, '{yao_otx}', NULL)
    , ({spark5}, '{sue_otx}', NULL)
    , ({spark7}, '{bob_otx}', NULL)
    ;
    """
    cursor0.execute(insert_face_name_only_sqlstr)

    trlname_dimen = kw.translate_name
    trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s_vld")
    print(f"{trlname_s_vld_tablename=}")
    insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename} 
    ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
    VALUES
      ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
    , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
    ;
    """
    cursor0.execute(insert_trlname_sqlstr)

    face_name_inx_count_sql = f"SELECT COUNT(*) FROM {prnawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 0

    # WHEN
    update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
        "name", prnawar_h_raw_put_tablename, kw.face_name
    )
    print(update_sqlstr)
    cursor0.execute(update_sqlstr)

    # THEN
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 3
    select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {prnawar_h_raw_put_tablename}"""
    cursor0.execute(select_face_name_only_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (1, sue_otx, sue_inx),
        (2, yao_otx, None),
        (5, sue_otx, sue_inx),
        (7, bob_otx, bob_inx),
    ]


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario1_PartialTranslateTables(
    cursor0: Cursor,
):
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    create_sound_and_heard_tables(cursor0)
    prnawar_dimen = kw.person_plan_awardunit
    prnawar_h_raw_put_tablename = prime_tbl(prnawar_dimen, "h_raw", "put")
    insert_face_name_only_sqlstr = f"""INSERT INTO {prnawar_h_raw_put_tablename}
    ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
    VALUES
      ({spark1}, '{sue_otx}', NULL)
    , ({spark2}, '{yao_otx}', NULL)
    , ({spark5}, '{bob_otx}', NULL)
    ;
    """
    cursor0.execute(insert_face_name_only_sqlstr)
    trlname_dimen = kw.translate_name
    trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s_vld")
    print(f"{trlname_s_vld_tablename=}")
    insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
    ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
    VALUES
      ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
    , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
    ;
    """
    cursor0.execute(insert_trlname_sqlstr)

    face_name_inx_count_sql = f"SELECT COUNT(*) FROM {prnawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 0

    # WHEN
    update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
        "name", prnawar_h_raw_put_tablename, kw.face_name
    )
    print(update_sqlstr)
    cursor0.execute(update_sqlstr)

    # THEN
    select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {prnawar_h_raw_put_tablename}"""
    cursor0.execute(select_face_name_only_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    # spark5 does not link to spark7 translate record's
    assert rows == [
        (spark1, sue_otx, sue_inx),
        (spark2, yao_otx, None),
        (spark5, bob_otx, None),
    ]


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario2_Different_spark_num_TranslateMappings(
    cursor0: Cursor,
):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    spark0 = 0
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark8 = 8
    spark9 = 9

    create_sound_and_heard_tables(cursor0)
    prnawar_dimen = kw.person_plan_awardunit
    prnawar_h_raw_put_tablename = prime_tbl(prnawar_dimen, "h_raw", "put")
    print(f"{get_table_columns(cursor0, prnawar_h_raw_put_tablename)=}")
    insert_face_name_only_sqlstr = f"""INSERT INTO {prnawar_h_raw_put_tablename}
    ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
    VALUES
      ({spark0}, '{bob_otx}', NULL)
    , ({spark1}, '{bob_otx}', NULL)
    , ({spark2}, '{yao_otx}', NULL)
    , ({spark5}, '{bob_otx}', NULL)
    , ({spark7}, '{bob_otx}', NULL)
    , ({spark9}, '{bob_otx}', NULL)
    ;
    """
    cursor0.execute(insert_face_name_only_sqlstr)

    trlname_dimen = kw.translate_name
    trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s_vld")
    print(f"{trlname_s_vld_tablename=}")
    insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
    ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
    VALUES
      ({spark1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
    , ({spark2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
    , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
    , ({spark7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
    , ({spark8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
    ;
    """
    cursor0.execute(insert_trlname_sqlstr)

    face_name_inx_count_sql = f"SELECT COUNT(*) FROM {prnawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 0

    # WHEN
    update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
        "name", prnawar_h_raw_put_tablename, kw.face_name
    )
    print(update_sqlstr)
    cursor0.execute(update_sqlstr)

    # THEN
    select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {prnawar_h_raw_put_tablename}"""
    cursor0.execute(select_face_name_only_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    # spark5 does not link to spark7 translate record's
    assert rows == [
        (0, bob_otx, None),
        (1, bob_otx, bob_inx0),
        (2, yao_otx, yao_inx),
        (5, bob_otx, bob_inx0),
        (7, bob_otx, bob_inx7),
        (9, bob_otx, bob_inx7),
    ]


def test_create_update_heard_raw_empty_inx_col_sqlstr_UpdatesTable_Scenario0_EmptyTranslateTables(
    cursor0: Cursor,
):
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    create_sound_and_heard_tables(cursor0)
    trlname_s_vld_tablename = prime_tbl(kw.translate_name, "s_vld")
    print(f"{trlname_s_vld_tablename=}")
    print(f"{get_table_columns(cursor0, trlname_s_vld_tablename)=}")

    prnawar_dimen = kw.person_plan_awardunit
    prnawar_h_raw_put_tablename = prime_tbl(prnawar_dimen, "h_raw", "put")
    print(f"{get_table_columns(cursor0, prnawar_h_raw_put_tablename)=}")
    insert_face_name_only_sqlstr = f"""INSERT INTO {prnawar_h_raw_put_tablename} ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
VALUES
  ({spark1}, '{sue_otx}', '{sue_inx}')
, ({spark2}, '{yao_otx}', NULL)
, ({spark5}, '{sue_otx}', NULL)
, ({spark7}, '{bob_otx}', '{bob_inx}')
;
"""
    cursor0.execute(insert_face_name_only_sqlstr)
    face_name_inx_count_sql = f"SELECT COUNT(*) FROM {prnawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 2

    # WHEN
    update_sqlstr = create_update_heard_raw_empty_inx_col_sqlstr(
        prnawar_h_raw_put_tablename, kw.face_name
    )
    print(update_sqlstr)
    cursor0.execute(update_sqlstr)

    # THEN
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 4
    select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {prnawar_h_raw_put_tablename}"""
    cursor0.execute(select_face_name_only_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (1, sue_otx, sue_inx),
        (2, yao_otx, yao_otx),
        (5, sue_otx, sue_otx),
        (7, bob_otx, bob_inx),
    ]


def test_set_all_heard_raw_inx_columns_Scenario0_empty_tables(cursor0: Cursor):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    spark0 = 0
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark8 = 8
    spark9 = 9

    create_sound_and_heard_tables(cursor0)
    prnawar_dimen = kw.person_plan_awardunit
    prnawar_h_raw_put_tablename = prime_tbl(prnawar_dimen, "h_raw", "put")
    print(f"{get_table_columns(cursor0, prnawar_h_raw_put_tablename)=}")
    insert_face_name_only_sqlstr = f"""INSERT INTO {prnawar_h_raw_put_tablename}
    ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
    VALUES
      ({spark0}, '{bob_otx}', NULL)
    , ({spark1}, '{bob_otx}', NULL)
    , ({spark2}, '{yao_otx}', NULL)
    , ({spark5}, '{bob_otx}', NULL)
    , ({spark7}, '{bob_otx}', NULL)
    , ({spark9}, '{bob_otx}', NULL)
    ;
    """
    cursor0.execute(insert_face_name_only_sqlstr)

    trlname_dimen = kw.translate_name
    trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s_vld")
    print(f"{trlname_s_vld_tablename=}")
    insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
    ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
    VALUES
      ({spark1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
    , ({spark2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
    , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
    , ({spark7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
    , ({spark8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
    ;
    """
    cursor0.execute(insert_trlname_sqlstr)

    face_name_inx_count_sql = f"SELECT COUNT(*) FROM {prnawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
    assert cursor0.execute(face_name_inx_count_sql).fetchone()[0] == 0

    # WHEN
    set_all_heard_raw_inx_columns(cursor0)

    # THEN
    select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {prnawar_h_raw_put_tablename}"""
    cursor0.execute(select_face_name_only_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    # spark5 does not link to spark7 translate record's
    assert rows == [
        (0, bob_otx, bob_otx),
        (1, bob_otx, bob_inx0),
        (2, yao_otx, yao_inx),
        (5, bob_otx, bob_inx0),
        (7, bob_otx, bob_inx7),
        (9, bob_otx, bob_inx7),
    ]
