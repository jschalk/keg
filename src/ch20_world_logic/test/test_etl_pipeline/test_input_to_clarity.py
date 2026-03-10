from os.path import exists as os_path_exists
from pandas import DataFrame
from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch00_py.file_toolbox import (
    count_dirs_files,
    create_path,
    get_level1_dirs,
    save_file,
)
from src.ch09_person_lesson._ref.ch09_path import (
    create_gut_path,
    create_job_path,
    create_moment_json_path,
)
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import open_gut_file
from src.ch11_bud._ref.ch11_path import (
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path as expressed_path,
)
from src.ch14_moment._ref.ch14_path import (
    create_bud_partner_mandate_ledger_path as bud_mandate,
)
from src.ch17_idea.idea_db_tool import upsert_sheet
from src.ch18_world_etl._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
)
from src.ch18_world_etl.etl_sqlstr import create_prime_tablename as prime_tbl
from src.ch20_world_logic.test._util.ch20_env import (
    cursor0,
    get_temp_dir as worlds_dir,
    temp_dir_setup,
)
from src.ch20_world_logic.world import worldunit_shop
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario0_br000113PopulatesTables(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        kw.face_name,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
        kw.otx_name,
        kw.inx_name,
    ]
    br00113_str = "br00113"
    br00113row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_valid"
    sparks_brick_valid_tablename = kw.sparks_brick_valid
    trlname_sound_raw = prime_tbl(kw.trlname, "s", "raw")
    trlname_sound_agg = prime_tbl(kw.trlname, "s", "agg")
    trlname_sound_vld = prime_tbl(kw.trlname, "s", "vld")
    trlcore_sound_raw = prime_tbl(kw.trlcore, "s", "raw")
    trlcore_sound_agg = prime_tbl(kw.trlcore, "s", "agg")
    trlcore_sound_vld = prime_tbl(kw.trlcore, "s", "vld")
    momentunit_sound_raw = prime_tbl(kw.momentunit, "s", "raw")
    momentunit_sound_agg = prime_tbl(kw.momentunit, "s", "agg")
    momentunit_sound_vld = prime_tbl(kw.momentunit, "s", "vld")
    prnunit_sound_put_raw = prime_tbl(kw.personunit, "s", "raw", "put")
    prnunit_sound_put_agg = prime_tbl(kw.personunit, "s", "agg", "put")
    prnunit_sound_put_vld = prime_tbl(kw.personunit, "s", "vld", "put")
    prnptnr_sound_put_raw = prime_tbl(kw.prnptnr, "s", "raw", "put")
    prnptnr_sound_put_agg = prime_tbl(kw.prnptnr, "s", "agg", "put")
    prnptnr_sound_put_vld = prime_tbl(kw.prnptnr, "s", "vld", "put")
    momentunit_heard_raw = prime_tbl(kw.momentunit, "h", "raw")
    momentunit_heard_agg = prime_tbl(kw.momentunit, "h", "agg")
    momentunit_heard_vld = prime_tbl(kw.momentunit, "h", "vld")
    prnunit_heard_put_raw = prime_tbl(kw.personunit, "h", "raw", "put")
    prnunit_heard_put_agg = prime_tbl(kw.personunit, "h", "vld", "put")
    prnptnr_heard_put_raw = prime_tbl(kw.prnptnr, "h", "raw", "put")
    prnptnr_heard_put_agg = prime_tbl(kw.prnptnr, "h", "vld", "put")
    mstr_dir = fay_world._moment_mstr_dir
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    a23_e1_all_lesson_path = create_spark_all_lesson_path(
        mstr_dir, a23_lasso, sue_inx, e3
    )
    a23_e1_expressed_lesson_path = expressed_path(mstr_dir, a23_lasso, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, sue_inx)
    prnptnr_job = prime_tbl(kw.prnptnr, "job", None)
    last_run_metrics_path = create_last_run_metrics_path(mstr_dir)

    assert not db_table_exists(cursor0, br00113_raw)
    assert not db_table_exists(cursor0, br00113_agg)
    assert not db_table_exists(cursor0, kw.sparks_brick_agg)
    assert not db_table_exists(cursor0, sparks_brick_valid_tablename)
    assert not db_table_exists(cursor0, br00113_valid)
    assert not db_table_exists(cursor0, trlname_sound_raw)
    assert not db_table_exists(cursor0, trlname_sound_agg)
    assert not db_table_exists(cursor0, momentunit_sound_raw)
    assert not db_table_exists(cursor0, momentunit_sound_agg)
    assert not db_table_exists(cursor0, momentunit_sound_vld)
    assert not db_table_exists(cursor0, prnunit_sound_put_raw)
    assert not db_table_exists(cursor0, prnunit_sound_put_agg)
    assert not db_table_exists(cursor0, prnunit_sound_put_vld)
    assert not db_table_exists(cursor0, trlcore_sound_raw)
    assert not db_table_exists(cursor0, trlcore_sound_agg)
    assert not db_table_exists(cursor0, trlcore_sound_vld)
    assert not db_table_exists(cursor0, trlname_sound_vld)
    assert not db_table_exists(cursor0, momentunit_heard_raw)
    assert not db_table_exists(cursor0, momentunit_heard_agg)
    assert not db_table_exists(cursor0, momentunit_heard_vld)
    assert not db_table_exists(cursor0, prnunit_heard_put_raw)
    assert not db_table_exists(cursor0, prnunit_heard_put_agg)
    assert not db_table_exists(cursor0, prnptnr_heard_put_raw)
    assert not db_table_exists(cursor0, prnptnr_heard_put_agg)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_e1_all_lesson_path)
    assert not os_path_exists(a23_e1_expressed_lesson_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not db_table_exists(cursor0, kw.moment_ote1_agg)
    assert not db_table_exists(cursor0, prnptnr_job)
    assert not db_table_exists(cursor0, kw.moment_partner_nets)
    assert not db_table_exists(cursor0, kw.moment_kpi001_partner_nets)
    assert not os_path_exists(last_run_metrics_path)

    # # create personunits
    # self.person_tables_to_spark_person_csvs(cursor)

    # # create all moment_job and mandate reports
    # self.calc_moment_bud_partner_mandate_net_ledgers()

    # WHEN
    fay_world.sheets_input_to_clarity_with_cursor(cursor0)

    # THEN
    # select_translate_core = f"SELECT * FROM {trlcore_sound_vld}"
    # select_personunit_put = f"SELECT * FROM {prnunit_sound_put_agg}"
    # select_prnptnr_put = f"SELECT * FROM {prnptnr_sound_put_agg}"
    # select_momentunit_put_raw = f"SELECT * FROM {momentunit_sound_raw}"
    # select_momentunit_put_agg = f"SELECT * FROM {momentunit_sound_agg}"
    # print(f"{cursor.execute(select_translate_core).fetchall()=}")
    # print(f"{cursor.execute(select_personunit_put).fetchall()=}")
    # print(f"{cursor.execute(select_prnptnr_put).fetchall()=}")
    # print(f"{cursor.execute(select_momentunit_put_raw).fetchall()=}")
    # print(f"{cursor.execute(select_momentunit_put_agg).fetchall()=}")

    assert get_row_count(cursor0, br00113_raw) == 1
    assert get_row_count(cursor0, br00113_agg) == 1
    assert get_row_count(cursor0, kw.sparks_brick_agg) == 1
    assert get_row_count(cursor0, sparks_brick_valid_tablename) == 1
    assert get_row_count(cursor0, br00113_valid) == 1
    assert get_row_count(cursor0, trlname_sound_raw) == 1
    assert get_row_count(cursor0, momentunit_sound_raw) == 1
    assert get_row_count(cursor0, prnunit_sound_put_raw) == 1
    assert get_row_count(cursor0, prnptnr_sound_put_raw) == 1
    assert get_row_count(cursor0, trlname_sound_agg) == 1
    assert get_row_count(cursor0, momentunit_sound_agg) == 1
    assert get_row_count(cursor0, prnunit_sound_put_agg) == 1
    assert get_row_count(cursor0, prnptnr_sound_put_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_raw) == 1
    assert get_row_count(cursor0, trlcore_sound_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_vld) == 1
    assert get_row_count(cursor0, trlname_sound_vld) == 1
    assert get_row_count(cursor0, momentunit_sound_vld) == 1
    assert get_row_count(cursor0, prnunit_sound_put_vld) == 1
    assert get_row_count(cursor0, prnptnr_sound_put_vld) == 1
    assert get_row_count(cursor0, momentunit_heard_raw) == 1
    assert get_row_count(cursor0, momentunit_heard_agg) == 1
    assert get_row_count(cursor0, prnunit_heard_put_raw) == 1
    assert get_row_count(cursor0, prnptnr_heard_put_raw) == 1
    assert get_row_count(cursor0, momentunit_heard_vld) == 1
    assert get_row_count(cursor0, prnunit_heard_put_agg) == 1
    assert get_row_count(cursor0, prnptnr_heard_put_agg) == 1
    assert os_path_exists(a23_json_path)
    print(f"{a23_e1_all_lesson_path=}")
    assert os_path_exists(a23_e1_all_lesson_path)
    assert os_path_exists(a23_e1_expressed_lesson_path)
    assert os_path_exists(a23_sue_gut_path)
    sue_gut = open_gut_file(mstr_dir, a23_lasso, sue_inx)
    time_rope = sue_gut.make_l1_rope(kw.time)
    creg_rope = sue_gut.make_rope(time_rope, kw.creg)
    assert sue_gut.plan_exists(creg_rope)
    assert os_path_exists(a23_sue_job_path)
    assert get_row_count(cursor0, prnptnr_job) == 1
    assert get_row_count(cursor0, kw.moment_partner_nets) == 0
    # assert get_row_count(cursor, moment_ote1_agg_tablename) == 0
    assert get_row_count(cursor0, kw.moment_kpi001_partner_nets) == 0
    assert os_path_exists(last_run_metrics_path)


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario1_PopulateBudPayRows(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        kw.face_name,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        kw.spark_num,
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
    br1row0 = [e3, exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)

    # Names of tables
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_valid"
    sparks_brick_valid_tablename = kw.sparks_brick_valid
    trlname_sound_raw = prime_tbl(kw.trlname, "s", "raw")
    trlname_sound_agg = prime_tbl(kw.trlname, "s", "agg")
    trlname_sound_vld = prime_tbl(kw.trlname, "s", "vld")
    trlcore_sound_raw = prime_tbl(kw.trlcore, "s", "raw")
    trlcore_sound_agg = prime_tbl(kw.trlcore, "s", "agg")
    trlcore_sound_vld = prime_tbl(kw.trlcore, "s", "vld")
    momentunit_sound_raw = prime_tbl(kw.momentunit, "s", "raw")
    momentunit_sound_agg = prime_tbl(kw.momentunit, "s", "agg")
    prnunit_sound_put_raw = prime_tbl(kw.personunit, "s", "raw", "put")
    prnunit_sound_put_agg = prime_tbl(kw.personunit, "s", "agg", "put")
    prnptnr_sound_put_raw = prime_tbl(kw.prnptnr, "s", "raw", "put")
    prnptnr_sound_put_agg = prime_tbl(kw.prnptnr, "s", "agg", "put")
    momentunit_heard_raw = prime_tbl(kw.momentunit, "h", "raw")
    momentunit_heard_vld = prime_tbl(kw.momentunit, "h", "vld")
    prnunit_heard_put_raw = prime_tbl(kw.personunit, "h", "raw", "put")
    prnunit_heard_put_agg = prime_tbl(kw.personunit, "h", "vld", "put")
    prnptnr_heard_put_raw = prime_tbl(kw.prnptnr, "h", "raw", "put")
    prnptnr_heard_put_agg = prime_tbl(kw.prnptnr, "h", "vld", "put")
    mstr_dir = fay_world._moment_mstr_dir
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    a23_e1_all_lesson_path = create_spark_all_lesson_path(
        mstr_dir, a23_lasso, sue_inx, e3
    )
    a23_e1_expressed_lesson_path = expressed_path(mstr_dir, a23_lasso, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, sue_inx)
    sue37_mandate_path = bud_mandate(mstr_dir, a23_lasso, sue_inx, tp37)

    assert not db_table_exists(cursor0, br00113_raw)
    assert not db_table_exists(cursor0, br00113_agg)
    assert not db_table_exists(cursor0, kw.sparks_brick_agg)
    assert not db_table_exists(cursor0, sparks_brick_valid_tablename)
    assert not db_table_exists(cursor0, br00113_valid)
    assert not db_table_exists(cursor0, trlname_sound_raw)
    assert not db_table_exists(cursor0, trlname_sound_agg)
    assert not db_table_exists(cursor0, momentunit_sound_raw)
    assert not db_table_exists(cursor0, momentunit_sound_agg)
    assert not db_table_exists(cursor0, prnunit_sound_put_raw)
    assert not db_table_exists(cursor0, prnunit_sound_put_agg)
    assert not db_table_exists(cursor0, trlcore_sound_raw)
    assert not db_table_exists(cursor0, trlcore_sound_agg)
    assert not db_table_exists(cursor0, trlcore_sound_vld)
    assert not db_table_exists(cursor0, trlname_sound_vld)
    assert not db_table_exists(cursor0, momentunit_heard_raw)
    assert not db_table_exists(cursor0, momentunit_heard_vld)
    assert not db_table_exists(cursor0, prnunit_heard_put_raw)
    assert not db_table_exists(cursor0, prnunit_heard_put_agg)
    assert not db_table_exists(cursor0, prnptnr_heard_put_raw)
    assert not db_table_exists(cursor0, prnptnr_heard_put_agg)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_e1_all_lesson_path)
    assert not os_path_exists(a23_e1_expressed_lesson_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not db_table_exists(cursor0, kw.moment_ote1_agg)
    assert not os_path_exists(sue37_mandate_path)
    assert not db_table_exists(cursor0, kw.moment_partner_nets)
    assert not db_table_exists(cursor0, kw.moment_kpi001_partner_nets)
    # self.moment_agg_tables_to_moment_ote1_agg(cursor)
    moments_dir = create_path(mstr_dir, "moments")
    print(f"{get_level1_dirs(moments_dir)=}")

    # # create personunits
    # self.person_tables_to_spark_person_csvs(cursor)

    # # create all moment_job and mandate reports
    # self.calc_moment_bud_partner_mandate_net_ledgers()

    # WHEN
    fay_world.sheets_input_to_clarity_with_cursor(cursor0)

    # THEN
    assert get_row_count(cursor0, br00113_raw) == 1
    assert get_row_count(cursor0, br00113_agg) == 1
    print(cursor0.execute(f"SELECT * FROM {kw.sparks_brick_agg}").fetchall())
    assert get_row_count(cursor0, kw.sparks_brick_agg) == 2
    assert get_row_count(cursor0, sparks_brick_valid_tablename) == 2
    assert get_row_count(cursor0, br00113_valid) == 2
    assert get_row_count(cursor0, trlname_sound_raw) == 2
    assert get_row_count(cursor0, momentunit_sound_raw) == 4
    assert get_row_count(cursor0, prnunit_sound_put_raw) == 4
    assert get_row_count(cursor0, prnptnr_sound_put_raw) == 2
    assert get_row_count(cursor0, trlname_sound_agg) == 1
    assert get_row_count(cursor0, momentunit_sound_agg) == 1
    assert get_row_count(cursor0, prnunit_sound_put_agg) == 1
    assert get_row_count(cursor0, prnptnr_sound_put_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_raw) == 1
    assert get_row_count(cursor0, trlcore_sound_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_vld) == 1
    assert get_row_count(cursor0, trlname_sound_vld) == 1
    assert get_row_count(cursor0, momentunit_heard_raw) == 1
    assert get_row_count(cursor0, prnunit_heard_put_raw) == 1
    assert get_row_count(cursor0, prnptnr_heard_put_raw) == 1
    assert get_row_count(cursor0, momentunit_heard_vld) == 1
    assert get_row_count(cursor0, prnunit_heard_put_agg) == 1
    assert get_row_count(cursor0, prnptnr_heard_put_agg) == 1
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_e1_all_lesson_path)
    assert os_path_exists(a23_e1_expressed_lesson_path)
    assert os_path_exists(a23_sue_gut_path)
    assert os_path_exists(a23_sue_job_path)
    assert get_row_count(cursor0, kw.moment_ote1_agg) == 1
    print(f"{sue37_mandate_path=}")
    assert os_path_exists(sue37_mandate_path)
    assert get_row_count(cursor0, kw.moment_partner_nets) == 1
    assert get_row_count(cursor0, kw.moment_kpi001_partner_nets) == 1


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario2_PopulateMomentTranBook(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00002_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
        kw.tran_time,
        kw.amount,
        kw.knot,
    ]
    br00002_str = "br00002"
    tp37 = 37
    sue_to_bob_amount = 200
    br00002row0 = [e3, exx.sue, exx.a23, exx.sue, exx.bob, tp37, sue_to_bob_amount, ";"]
    br00002_df = DataFrame([br00002row0], columns=br00002_columns)
    br00002_ex0_str = f"example0_{br00002_str}"
    upsert_sheet(input_file_path, br00002_ex0_str, br00002_df)

    assert not db_table_exists(cursor0, kw.moment_partner_nets)

    # WHEN
    fay_world.sheets_input_to_clarity_with_cursor(cursor0)

    # THEN
    assert get_row_count(cursor0, kw.moment_partner_nets) == 1


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario3_WhenNoMomentIdeas_ote1_IsStillCreated(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00011_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    moment_mstr = fay_world._moment_mstr_dir
    a23_lasso = lassounit_shop(exx.a23)
    a23_ote1_csv_path = create_moment_ote1_csv_path(moment_mstr, a23_lasso)
    assert os_path_exists(a23_ote1_csv_path) is False

    # WHEN
    fay_world.sheets_input_to_clarity_with_cursor(cursor0)

    # THEN
    assert os_path_exists(a23_ote1_csv_path)


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario4_DeletesPreviousFiles(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    print(f"{fay_world.worlds_dir=}")
    mstr_dir = fay_world._moment_mstr_dir
    moments_dir = create_path(mstr_dir, "moments")
    testing2_filename = "testing2.txt"
    testing3_filename = "testing3.txt"
    save_file(fay_world.worlds_dir, testing2_filename, "")
    save_file(moments_dir, testing3_filename, "")
    testing2_path = create_path(fay_world.worlds_dir, testing2_filename)
    testing3_path = create_path(moments_dir, testing3_filename)
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path)
    print(f"{testing3_path=}")

    # WHEN
    fay_world.sheets_input_to_clarity_with_cursor(cursor0)

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario5_CreatesFiles(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    spark1 = 1
    spark2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00003_columns = [
        kw.spark_num,
        kw.face_name,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    br00001_columns = [
        kw.spark_num,
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
    br1row0 = [spark2, exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)

    br3row0 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    br3row1 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    br3row2 = [spark2, exx.sue, minute_420, exx.a23, hour7am, ";"]
    br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
    br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(input_file_path, br00003_ex1_str, br00003_1df)
    upsert_sheet(input_file_path, br00003_ex3_str, br00003_3df)
    br00011_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    mstr_dir = fay_world._moment_mstr_dir
    wrong_a23_moment_dir = create_path(mstr_dir, exx.a23)
    assert os_path_exists(wrong_a23_moment_dir) is False
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, exx.sue)
    a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, exx.sue)
    sue37_mandate_path = bud_mandate(mstr_dir, a23_lasso, exx.sue, tp37)
    assert os_path_exists(input_file_path)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fay_world.worlds_dir) == 5

    # WHEN
    fay_world.sheets_input_to_clarity_with_cursor(cursor0)

    # THEN
    assert os_path_exists(wrong_a23_moment_dir) is False
    assert os_path_exists(input_file_path)
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_sue_gut_path)
    assert os_path_exists(a23_sue_job_path)
    assert os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fay_world.worlds_dir) == 42


def test_WorldUnit_sheets_input_to_clarity_mstr_Scenario0_CreatesDatabaseFile(
    temp_dir_setup,
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        kw.face_name,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.partner_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        kw.spark_num,
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
    br1row0 = [e3, exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)
    fay_db_path = fay_world.get_world_db_path()
    assert not os_path_exists(fay_db_path)

    # WHEN
    fay_world.sheets_input_to_clarity_mstr()

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn:
        br00113_raw = f"{br00113_str}_brick_raw"
        br00113_agg = f"{br00113_str}_brick_agg"
        br00113_valid = f"{br00113_str}_brick_valid"
        sparks_brick_valid_tablename = kw.sparks_brick_valid
        trlname_sound_raw = prime_tbl("trlname", "s", "raw")
        trlname_sound_agg = prime_tbl("trlname", "s", "agg")
        trlname_sound_vld = prime_tbl("trlname", "s", "vld")
        trlcore_sound_raw = prime_tbl("trlcore", "s", "raw")
        trlcore_sound_agg = prime_tbl("trlcore", "s", "agg")
        trlcore_sound_vld = prime_tbl("trlcore", "s", "vld")
        momentunit_sound_raw = prime_tbl("momentunit", "s", "raw")
        momentunit_sound_agg = prime_tbl("momentunit", "s", "agg")
        prnunit_sound_put_raw = prime_tbl("personunit", "s", "raw", "put")
        prnunit_sound_put_agg = prime_tbl("personunit", "s", "agg", "put")
        prnptnr_sound_put_raw = prime_tbl("prnptnr", "s", "raw", "put")
        prnptnr_sound_put_agg = prime_tbl("prnptnr", "s", "agg", "put")
        momentunit_heard_raw = prime_tbl("momentunit", "h", "raw")
        momentunit_heard_vld = prime_tbl("momentunit", "h", "vld")
        prnunit_heard_put_raw = prime_tbl("personunit", "h", "raw", "put")
        prnunit_heard_put_agg = prime_tbl("personunit", "h", "vld", "put")
        prnptnr_heard_put_raw = prime_tbl("prnptnr", "h", "raw", "put")
        prnptnr_heard_put_agg = prime_tbl("prnptnr", "h", "vld", "put")

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
