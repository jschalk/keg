from os.path import exists as os_path_exists
from pandas import DataFrame, DataFrame as pandas_DataFrame
from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch00_py.file_toolbox import (
    count_dirs_files,
    create_path,
    get_level1_dirs,
    save_file,
)
from src.ch04_rope.rope import create_rope_from_labels as init_rope
from src.ch09_person_lesson._ref.ch09_path import (
    create_gut_path,
    create_moment_json_path,
)
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import open_gut_file
from src.ch10_person_listen._ref.ch10_path import create_job_path
from src.ch11_bud._ref.ch11_path import (
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path as expressed_path,
)
from src.ch14_moment._ref.ch14_path import (
    create_bud_contact_mandate_ledger_path as bud_mandate,
)
from src.ch17_idea.brick_db_tool import save_sheet
from src.ch18_etl_config._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
)
from src.ch18_etl_config.etl_sqlstr import create_prime_tablename as prime_tbl
from src.ch21_world.test._util.ch21_examples import br00013_example
from src.ch21_world.world import (
    idea_sheets_to_lynx_mstr,
    idea_sheets_to_lynx_with_cursor,
    worlddir_shop,
)
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


def test_idea_sheets_to_lynx_with_cursor_Scenario0_br000113PopulatesTables(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00113_columns = [
        kw.spark_face,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_name,
        kw.inx_name,
    ]
    br00113_str = "br00113"
    br00113row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    save_sheet(i_src_dir_file_path, br00113_ex0_str, br00113_df)
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_vld"
    sparks_brick_vld_tablename = kw.sparks_brick_vld
    trlname_sound_raw = prime_tbl(kw.trlname, kw.s_raw)
    trlname_sound_agg = prime_tbl(kw.trlname, "s_agg")
    trlname_sound_vld = prime_tbl(kw.trlname, kw.s_vld)
    trlcore_sound_raw = prime_tbl(kw.trlcore, kw.s_raw)
    trlcore_sound_agg = prime_tbl(kw.trlcore, "s_agg")
    trlcore_sound_vld = prime_tbl(kw.trlcore, kw.s_vld)
    momentunit_sound_agg = prime_tbl(kw.momentunit, "s_agg")
    momentunit_sound_raw = prime_tbl(kw.momentunit, kw.s_raw)
    momentunit_sound_vld = prime_tbl(kw.momentunit, kw.s_vld)
    prnunit_put_sound_raw = prime_tbl(kw.personunit, kw.s_raw, "put")
    prnunit_put_sound_agg = prime_tbl(kw.personunit, "s_agg", "put")
    prnunit_put_sound_vld = prime_tbl(kw.personunit, kw.s_vld, "put")
    prncont_put_sound_raw = prime_tbl(kw.prncont, kw.s_raw, "put")
    prncont_put_sound_agg = prime_tbl(kw.prncont, "s_agg", "put")
    prncont_put_sound_vld = prime_tbl(kw.prncont, kw.s_vld, "put")
    momentunit_heard_raw = prime_tbl(kw.momentunit, kw.h_raw)
    momentunit_heard_agg = prime_tbl(kw.momentunit, kw.h_agg)
    momentunit_heard_vld = prime_tbl(kw.momentunit, kw.h_vld)
    prnunit_put_heard_raw = prime_tbl(kw.personunit, kw.h_raw, "put")
    prnunit_put_heard_agg = prime_tbl(kw.personunit, kw.h_vld, "put")
    prncont_put_heard_raw = prime_tbl(kw.prncont, kw.h_raw, "put")
    prncont_put_heard_agg = prime_tbl(kw.prncont, kw.h_vld, "put")
    mstr_dir = fay_wdir.moment_mstr_dir
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    a23_e1_all_lesson_path = create_spark_all_lesson_path(
        mstr_dir, a23_lasso, sue_inx, e3
    )
    a23_e1_expressed_lesson_path = expressed_path(mstr_dir, a23_lasso, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, sue_inx)
    prncont_job = prime_tbl(kw.prncont, "job", None)
    last_run_metrics_path = create_last_run_metrics_path(mstr_dir)

    assert not db_table_exists(cursor0, br00113_raw)
    assert not db_table_exists(cursor0, br00113_agg)
    assert not db_table_exists(cursor0, kw.sparks_brick_agg)
    assert not db_table_exists(cursor0, sparks_brick_vld_tablename)
    assert not db_table_exists(cursor0, br00113_valid)
    assert not db_table_exists(cursor0, trlname_sound_raw)
    assert not db_table_exists(cursor0, trlname_sound_agg)
    assert not db_table_exists(cursor0, momentunit_sound_raw)
    assert not db_table_exists(cursor0, momentunit_sound_agg)
    assert not db_table_exists(cursor0, momentunit_sound_vld)
    assert not db_table_exists(cursor0, prnunit_put_sound_raw)
    assert not db_table_exists(cursor0, prnunit_put_sound_agg)
    assert not db_table_exists(cursor0, prnunit_put_sound_vld)
    assert not db_table_exists(cursor0, trlcore_sound_raw)
    assert not db_table_exists(cursor0, trlcore_sound_agg)
    assert not db_table_exists(cursor0, trlcore_sound_vld)
    assert not db_table_exists(cursor0, trlname_sound_vld)
    assert not db_table_exists(cursor0, momentunit_heard_raw)
    assert not db_table_exists(cursor0, momentunit_heard_agg)
    assert not db_table_exists(cursor0, momentunit_heard_vld)
    assert not db_table_exists(cursor0, prnunit_put_heard_raw)
    assert not db_table_exists(cursor0, prnunit_put_heard_agg)
    assert not db_table_exists(cursor0, prncont_put_heard_raw)
    assert not db_table_exists(cursor0, prncont_put_heard_agg)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_e1_all_lesson_path)
    assert not os_path_exists(a23_e1_expressed_lesson_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not db_table_exists(cursor0, kw.moment_ote1_agg)
    assert not db_table_exists(cursor0, prncont_job)
    assert not db_table_exists(cursor0, kw.moment_contact_nets)
    assert not db_table_exists(cursor0, kw.moment_kpi001_contact_nets)
    assert not os_path_exists(last_run_metrics_path)

    # # create personunits
    # self.person_tables_to_spark_person_csvs(cursor)

    # # create all moment_job and mandate reports
    # calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir)

    # WHEN
    idea_sheets_to_lynx_with_cursor(
        cursor0, fay_wdir.i_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    # select_translate_core = f"SELECT * FROM {trlcore_sound_vld}"
    # select_personunit_put = f"SELECT * FROM {prnunit_put_sound_agg}"
    # select_prncont_put = f"SELECT * FROM {prncont_put_sound_agg}"
    # select_momentunit_put_raw = f"SELECT * FROM {momentunit_sound_raw}"
    # select_momentunit_put_agg = f"SELECT * FROM {momentunit_sound_agg}"
    # print(f"{cursor.execute(select_translate_core).fetchall()=}")
    # print(f"{cursor.execute(select_personunit_put).fetchall()=}")
    # print(f"{cursor.execute(select_prncont_put).fetchall()=}")
    # print(f"{cursor.execute(select_momentunit_put_raw).fetchall()=}")
    # print(f"{cursor.execute(select_momentunit_put_agg).fetchall()=}")

    assert get_row_count(cursor0, br00113_raw) == 1
    assert get_row_count(cursor0, br00113_agg) == 1
    assert get_row_count(cursor0, kw.sparks_brick_agg) == 1
    assert get_row_count(cursor0, sparks_brick_vld_tablename) == 1
    assert get_row_count(cursor0, br00113_valid) == 1
    assert get_row_count(cursor0, trlname_sound_raw) == 1
    assert get_row_count(cursor0, momentunit_sound_raw) == 1
    assert get_row_count(cursor0, prnunit_put_sound_raw) == 1
    assert get_row_count(cursor0, prncont_put_sound_raw) == 1
    assert get_row_count(cursor0, trlname_sound_agg) == 1
    assert get_row_count(cursor0, momentunit_sound_agg) == 1
    assert get_row_count(cursor0, prnunit_put_sound_agg) == 1
    assert get_row_count(cursor0, prncont_put_sound_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_raw) == 1
    assert get_row_count(cursor0, trlcore_sound_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_vld) == 1
    assert get_row_count(cursor0, trlname_sound_vld) == 1
    assert get_row_count(cursor0, momentunit_sound_vld) == 1
    assert get_row_count(cursor0, prnunit_put_sound_vld) == 1
    assert get_row_count(cursor0, prncont_put_sound_vld) == 1
    assert get_row_count(cursor0, momentunit_heard_raw) == 1
    assert get_row_count(cursor0, momentunit_heard_agg) == 1
    assert get_row_count(cursor0, prnunit_put_heard_raw) == 1
    assert get_row_count(cursor0, prncont_put_heard_raw) == 1
    assert get_row_count(cursor0, momentunit_heard_vld) == 1
    assert get_row_count(cursor0, prnunit_put_heard_agg) == 1
    assert get_row_count(cursor0, prncont_put_heard_agg) == 1
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
    assert get_row_count(cursor0, prncont_job) == 1
    assert get_row_count(cursor0, kw.moment_contact_nets) == 0
    # assert get_row_count(cursor, moment_ote1_agg_tablename) == 0
    assert get_row_count(cursor0, kw.moment_kpi001_contact_nets) == 0
    assert os_path_exists(last_run_metrics_path)


def test_idea_sheets_to_lynx_with_cursor_Scenario1_PopulateBudPayRows(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00113_columns = [
        kw.spark_face,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    save_sheet(i_src_dir_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        kw.spark_num,
        kw.spark_face,
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
    save_sheet(i_src_dir_file_path, br00001_ex0_str, br00001_1df)

    # Names of tables
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_vld"
    sparks_brick_vld_tablename = kw.sparks_brick_vld
    trlname_sound_raw = prime_tbl(kw.trlname, kw.s_raw)
    trlname_sound_agg = prime_tbl(kw.trlname, "s_agg")
    trlname_sound_vld = prime_tbl(kw.trlname, kw.s_vld)
    trlcore_sound_raw = prime_tbl(kw.trlcore, kw.s_raw)
    trlcore_sound_agg = prime_tbl(kw.trlcore, "s_agg")
    trlcore_sound_vld = prime_tbl(kw.trlcore, kw.s_vld)
    momentunit_sound_raw = prime_tbl(kw.momentunit, kw.s_raw)
    momentunit_sound_agg = prime_tbl(kw.momentunit, "s_agg")
    prnunit_put_sound_raw = prime_tbl(kw.personunit, kw.s_raw, "put")
    prnunit_put_sound_agg = prime_tbl(kw.personunit, "s_agg", "put")
    prncont_put_sound_raw = prime_tbl(kw.prncont, kw.s_raw, "put")
    prncont_put_sound_agg = prime_tbl(kw.prncont, "s_agg", "put")
    momentunit_heard_raw = prime_tbl(kw.momentunit, kw.h_raw)
    momentunit_heard_vld = prime_tbl(kw.momentunit, kw.h_vld)
    prnunit_put_heard_raw = prime_tbl(kw.personunit, kw.h_raw, "put")
    prnunit_put_heard_agg = prime_tbl(kw.personunit, kw.h_vld, "put")
    prncont_put_heard_raw = prime_tbl(kw.prncont, kw.h_raw, "put")
    prncont_put_heard_agg = prime_tbl(kw.prncont, kw.h_vld, "put")
    mstr_dir = fay_wdir.moment_mstr_dir
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
    assert not db_table_exists(cursor0, sparks_brick_vld_tablename)
    assert not db_table_exists(cursor0, br00113_valid)
    assert not db_table_exists(cursor0, trlname_sound_raw)
    assert not db_table_exists(cursor0, trlname_sound_agg)
    assert not db_table_exists(cursor0, momentunit_sound_raw)
    assert not db_table_exists(cursor0, momentunit_sound_agg)
    assert not db_table_exists(cursor0, prnunit_put_sound_raw)
    assert not db_table_exists(cursor0, prnunit_put_sound_agg)
    assert not db_table_exists(cursor0, trlcore_sound_raw)
    assert not db_table_exists(cursor0, trlcore_sound_agg)
    assert not db_table_exists(cursor0, trlcore_sound_vld)
    assert not db_table_exists(cursor0, trlname_sound_vld)
    assert not db_table_exists(cursor0, momentunit_heard_raw)
    assert not db_table_exists(cursor0, momentunit_heard_vld)
    assert not db_table_exists(cursor0, prnunit_put_heard_raw)
    assert not db_table_exists(cursor0, prnunit_put_heard_agg)
    assert not db_table_exists(cursor0, prncont_put_heard_raw)
    assert not db_table_exists(cursor0, prncont_put_heard_agg)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_e1_all_lesson_path)
    assert not os_path_exists(a23_e1_expressed_lesson_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not db_table_exists(cursor0, kw.moment_ote1_agg)
    assert not os_path_exists(sue37_mandate_path)
    assert not db_table_exists(cursor0, kw.moment_contact_nets)
    assert not db_table_exists(cursor0, kw.moment_kpi001_contact_nets)
    # self.moment_agg_tables_to_moment_ote1_agg(cursor)
    moments_dir = create_path(mstr_dir, "moments")
    print(f"{get_level1_dirs(moments_dir)=}")

    # # create personunits
    # self.person_tables_to_spark_person_csvs(cursor)

    # # create all moment_job and mandate reports
    # calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir)

    # WHEN
    idea_sheets_to_lynx_with_cursor(
        cursor0, fay_wdir.i_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert get_row_count(cursor0, br00113_raw) == 1
    assert get_row_count(cursor0, br00113_agg) == 1
    print(cursor0.execute(f"SELECT * FROM {kw.sparks_brick_agg}").fetchall())
    assert get_row_count(cursor0, kw.sparks_brick_agg) == 2
    assert get_row_count(cursor0, sparks_brick_vld_tablename) == 2
    assert get_row_count(cursor0, br00113_valid) == 2
    assert get_row_count(cursor0, trlname_sound_raw) == 2
    assert get_row_count(cursor0, momentunit_sound_raw) == 4
    assert get_row_count(cursor0, prnunit_put_sound_raw) == 4
    assert get_row_count(cursor0, prncont_put_sound_raw) == 2
    assert get_row_count(cursor0, trlname_sound_agg) == 1
    assert get_row_count(cursor0, momentunit_sound_agg) == 1
    assert get_row_count(cursor0, prnunit_put_sound_agg) == 1
    assert get_row_count(cursor0, prncont_put_sound_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_raw) == 1
    assert get_row_count(cursor0, trlcore_sound_agg) == 1
    assert get_row_count(cursor0, trlcore_sound_vld) == 1
    assert get_row_count(cursor0, trlname_sound_vld) == 1
    assert get_row_count(cursor0, momentunit_heard_raw) == 1
    assert get_row_count(cursor0, prnunit_put_heard_raw) == 1
    assert get_row_count(cursor0, prncont_put_heard_raw) == 1
    assert get_row_count(cursor0, momentunit_heard_vld) == 1
    assert get_row_count(cursor0, prnunit_put_heard_agg) == 1
    assert get_row_count(cursor0, prncont_put_heard_agg) == 1
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_e1_all_lesson_path)
    assert os_path_exists(a23_e1_expressed_lesson_path)
    assert os_path_exists(a23_sue_gut_path)
    assert os_path_exists(a23_sue_job_path)
    assert get_row_count(cursor0, kw.moment_ote1_agg) == 1
    print(f"{sue37_mandate_path=}")
    assert os_path_exists(sue37_mandate_path)
    assert get_row_count(cursor0, kw.moment_contact_nets) == 1
    assert get_row_count(cursor0, kw.moment_kpi001_contact_nets) == 1


def test_idea_sheets_to_lynx_with_cursor_Scenario2_PopulateMomentTranBook(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    e3 = 3
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00002_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
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
    save_sheet(i_src_dir_file_path, br00002_ex0_str, br00002_df)

    assert not db_table_exists(cursor0, kw.moment_contact_nets)

    # WHEN
    idea_sheets_to_lynx_with_cursor(
        cursor0, fay_wdir.i_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert get_row_count(cursor0, kw.moment_contact_nets) == 1


def test_idea_sheets_to_lynx_with_cursor_Scenario3_WhenNoMomentIdeas_ote1_IsStillCreated(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00011_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    save_sheet(i_src_dir_file_path, "br00011_ex3", br00011_df)
    moment_mstr = fay_wdir.moment_mstr_dir
    a23_lasso = lassounit_shop(exx.a23)
    a23_ote1_csv_path = create_moment_ote1_csv_path(moment_mstr, a23_lasso)
    assert os_path_exists(a23_ote1_csv_path) is False

    # WHEN
    idea_sheets_to_lynx_with_cursor(
        cursor0, fay_wdir.i_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert os_path_exists(a23_ote1_csv_path)


def test_idea_sheets_to_lynx_with_cursor_Scenario4_DeletesPreviousFiles(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    print(f"{fay_wdir.worlds_dir=}")
    mstr_dir = fay_wdir.moment_mstr_dir
    moments_dir = create_path(mstr_dir, "moments")
    testing2_filename = "testing2.txt"
    testing3_filename = "testing3.txt"
    save_file(fay_wdir.worlds_dir, testing2_filename, "")
    save_file(moments_dir, testing3_filename, "")
    testing2_path = create_path(fay_wdir.worlds_dir, testing2_filename)
    testing3_path = create_path(moments_dir, testing3_filename)
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path)
    print(f"{testing3_path=}")

    # WHEN
    idea_sheets_to_lynx_with_cursor(
        cursor0, fay_wdir.i_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False


def test_idea_sheets_to_lynx_with_cursor_Scenario5_CreatesFiles(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    spark1 = 1
    spark2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00003_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    br00001_columns = [
        kw.spark_num,
        kw.spark_face,
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
    save_sheet(i_src_dir_file_path, br00001_ex0_str, br00001_1df)

    br3row0 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    br3row1 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    br3row2 = [spark2, exx.sue, minute_420, exx.a23, hour7am, ";"]
    br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
    br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex3_str = "example3_br00003"
    save_sheet(i_src_dir_file_path, br00003_ex1_str, br00003_1df)
    save_sheet(i_src_dir_file_path, br00003_ex3_str, br00003_3df)
    br00011_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    save_sheet(i_src_dir_file_path, "br00011_ex3", br00011_df)
    mstr_dir = fay_wdir.moment_mstr_dir
    wrong_a23_moment_dir = create_path(mstr_dir, exx.a23)
    assert os_path_exists(wrong_a23_moment_dir) is False
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, exx.sue)
    a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, exx.sue)
    sue37_mandate_path = bud_mandate(mstr_dir, a23_lasso, exx.sue, tp37)
    assert os_path_exists(i_src_dir_file_path)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fay_wdir.worlds_dir) == 5

    # WHEN
    idea_sheets_to_lynx_with_cursor(
        cursor0, fay_wdir.i_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert os_path_exists(wrong_a23_moment_dir) is False
    assert os_path_exists(i_src_dir_file_path)
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_sue_gut_path)
    assert os_path_exists(a23_sue_job_path)
    assert os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fay_wdir.worlds_dir) == 42


def test_idea_sheets_to_lynx_mstr_Scenario0_CreatesDatabaseFile(
    temp3_fs,
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00113_columns = [
        kw.spark_face,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    save_sheet(i_src_dir_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        kw.spark_num,
        kw.spark_face,
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
    save_sheet(i_src_dir_file_path, br00001_ex0_str, br00001_1df)
    fay_db_path = fay_wdir.get_world_db_path()
    assert not os_path_exists(fay_db_path)

    # WHEN
    idea_sheets_to_lynx_mstr(
        world_db_path=fay_wdir.get_world_db_path(),
        i_src_dir=fay_wdir.i_src_dir,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
    )

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn:
        br00113_raw = f"{br00113_str}_brick_raw"
        br00113_agg = f"{br00113_str}_brick_agg"
        br00113_valid = f"{br00113_str}_brick_vld"
        sparks_brick_vld_tablename = kw.sparks_brick_vld
        trlname_sound_raw = prime_tbl("trlname", kw.s_raw)
        trlname_sound_agg = prime_tbl("trlname", "s_agg")
        trlname_sound_vld = prime_tbl("TRLNAME", kw.s_vld)
        trlcore_sound_raw = prime_tbl("TRLCORE", kw.s_raw)
        trlcore_sound_agg = prime_tbl("trlcore", "s_agg")
        trlcore_sound_vld = prime_tbl("TRLCORE", kw.s_vld)
        momentunit_sound_raw = prime_tbl("momentunit", kw.s_raw)
        momentunit_sound_agg = prime_tbl("momentunit", "s_agg")
        prnunit_put_sound_raw = prime_tbl("personunit", kw.s_raw, "put")
        prnunit_put_sound_agg = prime_tbl("personunit", "s_agg", "put")
        prncont_put_sound_raw = prime_tbl("prncont", kw.s_raw, "put")
        prncont_put_sound_agg = prime_tbl("prncont", "s_agg", "put")
        momentunit_heard_raw = prime_tbl("momentunit", kw.h_raw)
        momentunit_heard_vld = prime_tbl("momentunit", kw.h_vld)
        prnunit_put_heard_raw = prime_tbl("personunit", kw.h_raw, "put")
        prnunit_put_heard_agg = prime_tbl("personunit", kw.h_vld, "put")
        prncont_put_heard_raw = prime_tbl("prncont", kw.h_raw, "put")
        prncont_put_heard_agg = prime_tbl("prncont", kw.h_vld, "put")

        cursor = db_conn.cursor()
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, kw.sparks_brick_agg) == 2
        assert get_row_count(cursor, sparks_brick_vld_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, trlname_sound_raw) == 2
        assert get_row_count(cursor, momentunit_sound_raw) == 4
        assert get_row_count(cursor, prnunit_put_sound_raw) == 4
        assert get_row_count(cursor, prncont_put_sound_raw) == 2
        assert get_row_count(cursor, trlname_sound_agg) == 1
        assert get_row_count(cursor, momentunit_sound_agg) == 1
        assert get_row_count(cursor, prnunit_put_sound_agg) == 1
        assert get_row_count(cursor, prncont_put_sound_agg) == 1
        assert get_row_count(cursor, trlcore_sound_raw) == 1
        assert get_row_count(cursor, trlcore_sound_agg) == 1
        assert get_row_count(cursor, trlcore_sound_vld) == 1
        assert get_row_count(cursor, trlname_sound_vld) == 1
        assert get_row_count(cursor, momentunit_heard_raw) == 1
        assert get_row_count(cursor, prnunit_put_heard_raw) == 1
        assert get_row_count(cursor, prncont_put_heard_raw) == 1
        assert get_row_count(cursor, momentunit_heard_vld) == 1
        assert get_row_count(cursor, prnunit_put_heard_agg) == 1
        assert get_row_count(cursor, prncont_put_heard_agg) == 1
        assert get_row_count(cursor, kw.moment_ote1_agg) == 1
    db_conn.close()


def test_idea_sheets_to_lynx_mstr_Scenario1_Creates_job_Files(temp3_fs):
    # ESTABLISH
    hr_mop = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.mop])
    hr_tools = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.scrub])

    data = [
        (0, exx.sue, exx.zia, exx.hn_red, hr_mop, 1, True),
        (0, exx.sue, exx.yao, exx.hn_red, hr_tools, 2, True),
    ]
    cols = [
        kw.spark_num,
        kw.spark_face,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    br00013_example = pandas_DataFrame(data, columns=cols)

    here_wdir = worlddir_shop("HereNow", str(temp3_fs))
    br00013_example_path = create_path(here_wdir.i_src_dir, "example.xlsx")
    save_sheet(br00013_example_path, "br00013_ex1", br00013_example)
    # print(br00013_example().to_dict())
    mmt_dir = here_wdir.moment_mstr_dir
    hn_red_lasso = lassounit_shop(exx.hn_red)
    hn_red_mmt_json_path = create_moment_json_path(mmt_dir, hn_red_lasso)
    hn_red_yao_job_path = create_job_path(mmt_dir, hn_red_lasso, exx.yao)
    hn_red_zia_job_path = create_job_path(mmt_dir, hn_red_lasso, exx.zia)
    assert not os_path_exists(hn_red_mmt_json_path)
    assert not os_path_exists(hn_red_yao_job_path)
    assert not os_path_exists(hn_red_zia_job_path)

    # WHEN
    idea_sheets_to_lynx_mstr(
        world_db_path=here_wdir.get_world_db_path(),
        i_src_dir=here_wdir.i_src_dir,
        moment_mstr_dir=here_wdir.moment_mstr_dir,
    )

    # THEN
    # world_test_ex_dir = "src\ch21_world\test\test_world_examples"
    # export_db_to_excel(here_wdir.get_world_db_path(), here_wdir.worlds_dir, "export.xlsx")
    assert os_path_exists(hn_red_mmt_json_path)
    assert os_path_exists(hn_red_zia_job_path)
    assert os_path_exists(hn_red_yao_job_path)
