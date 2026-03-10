from os.path import exists as os_path_exists
from pandas import DataFrame
from sqlite3 import connect as sqlite3_connect
from src.ch00_py.db_toolbox import get_row_count
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import create_rope
from src.ch17_idea.idea_db_tool import create_idea_sorted_table, upsert_sheet
from src.ch18_world_etl.etl_main import get_max_brick_agg_spark_num
from src.ch18_world_etl.etl_sqlstr import create_prime_tablename
from src.ch20_world_logic.test._util.ch20_env import (
    get_temp_dir as worlds_dir,
    temp_dir_setup,
)
from src.ch20_world_logic.world import WorldUnit, worldunit_shop
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_WorldUnit_stance_sheets_to_clarity_mstr_Scenario0_CreatesDatabaseFile(
    temp_dir_setup,
):  # sourcery skip: extract-method
    # ESTABLISH:
    fay_str = "Fay34"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_inx = "Suzy"
    ex_filename = "stance_Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [exx.sue, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.bud_time,
        kw.knot,
        kw.quota,
        kw.celldepth,
    ]
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)
    fay_db_path = fay_world.get_world_db_path()
    assert not os_path_exists(fay_db_path)

    # WHEN
    fay_world.stance_sheets_to_clarity_mstr()

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn:
        br00113_raw = f"{br00113_str}_brick_raw"
        br00113_agg = f"{br00113_str}_brick_agg"
        br00113_valid = f"{br00113_str}_brick_valid"
        sparks_brick_valid_tablename = kw.sparks_brick_valid
        trlname_sound_raw = create_prime_tablename("trlname", "s", "raw")
        trlname_sound_agg = create_prime_tablename("trlname", "s", "agg")
        trlname_sound_vld = create_prime_tablename("trlname", "s", "vld")
        trlcore_sound_raw = create_prime_tablename("trlcore", "s", "raw")
        trlcore_sound_agg = create_prime_tablename("trlcore", "s", "agg")
        trlcore_sound_vld = create_prime_tablename("trlcore", "s", "vld")
        momentunit_sound_raw = create_prime_tablename("momentunit", "s", "raw")
        momentunit_sound_agg = create_prime_tablename("momentunit", "s", "agg")
        prnunit_sound_put_raw = create_prime_tablename("personunit", "s", "raw", "put")
        prnunit_sound_put_agg = create_prime_tablename("personunit", "s", "agg", "put")
        prnptnr_sound_put_raw = create_prime_tablename("prnptnr", "s", "raw", "put")
        prnptnr_sound_put_agg = create_prime_tablename("prnptnr", "s", "agg", "put")
        momentunit_heard_raw = create_prime_tablename("momentunit", "h", "raw")
        momentunit_heard_vld = create_prime_tablename("momentunit", "h", "vld")
        prnunit_heard_put_raw = create_prime_tablename("personunit", "h", "raw", "put")
        prnunit_heard_put_agg = create_prime_tablename("personunit", "h", "vld", "put")
        prnptnr_heard_put_raw = create_prime_tablename("prnptnr", "h", "raw", "put")
        prnptnr_heard_put_agg = create_prime_tablename("prnptnr", "h", "vld", "put")

        cursor = db_conn.cursor()
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, kw.sparks_brick_agg) == 2
        assert get_row_count(cursor, sparks_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, trlname_sound_raw) == 2
        assert get_row_count(cursor, momentunit_sound_raw) == 4
        assert get_row_count(cursor, prnunit_sound_put_raw) == 4
        assert get_row_count(cursor, prnptnr_sound_put_raw) == 2
        assert get_row_count(cursor, trlname_sound_agg) == 1
        assert get_row_count(cursor, momentunit_sound_agg) == 1
        assert get_row_count(cursor, prnunit_sound_put_agg) == 1
        assert get_row_count(cursor, prnptnr_sound_put_agg) == 1
        assert get_row_count(cursor, trlcore_sound_raw) == 1
        assert get_row_count(cursor, trlcore_sound_agg) == 1
        assert get_row_count(cursor, trlcore_sound_vld) == 1
        assert get_row_count(cursor, trlname_sound_vld) == 1
        assert get_row_count(cursor, momentunit_heard_raw) == 1
        assert get_row_count(cursor, prnunit_heard_put_raw) == 1
        assert get_row_count(cursor, prnptnr_heard_put_raw) == 1
        assert get_row_count(cursor, momentunit_heard_vld) == 1
        assert get_row_count(cursor, prnunit_heard_put_agg) == 1
        assert get_row_count(cursor, prnptnr_heard_put_agg) == 1
        assert get_row_count(cursor, kw.moment_ote1_agg) == 1
    db_conn.close()


def create_brick_agg_record(world: WorldUnit, spark_num: int):
    minute_360 = 360
    hour6am = "6am"
    agg_br00003_tablename = f"br00003_{kw.brick_agg}"
    agg_br00003_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.cumulative_minute,
        kw.hour_label,
    ]
    with sqlite3_connect(world.get_world_db_path()) as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.cumulative_minute}
, {kw.hour_label}
)"""
        values_clause = f"""VALUES ('{spark_num}', '{exx.sue}', '{world.world_name}', '{minute_360}', '{hour6am}');"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
    db_conn.close()


def test_WorldUnit_stance_sheets_to_clarity_mstr_Scenario1_DatabaseFileExists(
    temp_dir_setup,
):  # sourcery skip: extract-method
    # ESTABLISH:
    fay_rope = create_rope("Fay34")
    fay_world = worldunit_shop(fay_rope, worlds_dir())
    spark5 = 5
    create_brick_agg_record(fay_world, spark5)
    # delete_dir(fay_world.worlds_dir)
    sue_inx = "Suzy"
    ex_filename = "stance_Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
        kw.otx_name,
        kw.inx_name,
    ]
    a23_rope = create_rope("amy2345")
    br00113_str = "br00113"
    br00113row0 = [exx.sue, a23_rope, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)
    fay_db_path = fay_world.get_world_db_path()
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn0:
        cursor0 = db_conn0.cursor()
        assert get_max_brick_agg_spark_num(cursor0) == spark5
    db_conn0.close()
    assert os_path_exists(input_file_path)

    # WHEN
    fay_world.stance_sheets_to_clarity_mstr()

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn1:
        cursor1 = db_conn1.cursor()
        assert get_max_brick_agg_spark_num(cursor1) != spark5
        assert get_max_brick_agg_spark_num(cursor1) == spark5 + 1
        select_sqlstr = f"SELECT * FROM {kw.sparks_brick_agg}"
        cursor1.execute(select_sqlstr)
        rows = cursor1.fetchall()
        assert len(rows) == 2
    db_conn1.close()
    assert not os_path_exists(input_file_path)
