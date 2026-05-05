from ch00_py.db_toolbox import (
    db_table_exists,
    get_all_tables_with_duplicates,
    get_row_count,
)
from ch00_py.file_toolbox import (
    count_dirs_files,
    create_path,
    get_level1_dirs,
    save_file,
)
from ch00_py.test.tool_db.test_db_tool_ import print_table
from ch04_rope.rope import create_rope_from_labels as init_rope
from ch09_person_lesson._ref.ch09_path import create_gut_path, create_moment_json_path
from ch09_person_lesson.lasso import lassounit_shop
from ch09_person_lesson.lesson_filehandler import open_gut_file
from ch10_person_listen._ref.ch10_path import create_job_path
from ch11_bud._ref.ch11_path import (
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path as expressed_path,
)
from ch14_moment._ref.ch14_path import (
    create_bud_contact_mandate_ledger_path as bud_mandate,
)
from ch17_brick.brick_db_tool import save_sheet
from ch18_etl_config._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
)
from ch18_etl_config.etl_sqlstr import create_prime_tablename as prime_tbl
from ch32_world.test._util.ch32_examples import bk00002_example
from ch32_world.world import (
    brick_sheets_to_lego_mstr,
    brick_sheets_to_lego_with_cursor,
    worlddir_shop,
)
from os.path import exists as os_path_exists
from pandas import DataFrame, DataFrame as pandas_DataFrame
from ref.keywords import Ch32Keywords as kw, ExampleStrs as exx
from sqlite3 import Cursor, connect as sqlite3_connect


def test_brick_sheets_to_lego_with_cursor_Scenario0_bk001071PopulatesTables(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00171_columns = [
        kw.spark_face,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_name,
        kw.inx_name,
    ]
    bk00171_str = "bk00171"
    bk00171row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    bk00171_df = DataFrame([bk00171row0], columns=bk00171_columns)
    bk00171_ex0_str = f"example0_{bk00171_str}"
    save_sheet(b_src_dir_file_path, bk00171_ex0_str, bk00171_df)
    bk00171_raw = f"{bk00171_str}_brixk_raw"
    bk00171_agg = f"{bk00171_str}_brixk_agg"
    bk00171_valid = f"{bk00171_str}_brixk_vld"
    sparks_brixk_vld_tablename = kw.sparks_brixk_vld
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

    assert not db_table_exists(cursor0, bk00171_raw)
    assert not db_table_exists(cursor0, bk00171_agg)
    assert not db_table_exists(cursor0, kw.sparks_brixk_agg)
    assert not db_table_exists(cursor0, sparks_brixk_vld_tablename)
    assert not db_table_exists(cursor0, bk00171_valid)
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
    assert not db_table_exists(cursor0, kw.moment_tranbook_nets)
    assert not db_table_exists(cursor0, kw.moment_kpi001_contact_nets)
    assert not os_path_exists(last_run_metrics_path)

    # # create personunits
    # self.person_tables_to_lego_spark_person_csvs(cursor)

    # # create all moment_job and mandate reports
    # calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir)

    # WHEN
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
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

    assert get_row_count(cursor0, bk00171_raw) == 1
    assert get_row_count(cursor0, bk00171_agg) == 1
    assert get_row_count(cursor0, kw.sparks_brixk_agg) == 1
    assert get_row_count(cursor0, sparks_brixk_vld_tablename) == 1
    assert get_row_count(cursor0, bk00171_valid) == 1
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
    assert get_row_count(cursor0, kw.moment_tranbook_nets) == 0
    # assert get_row_count(cursor, moment_ote1_agg_tablename) == 0
    assert get_row_count(cursor0, kw.moment_kpi001_contact_nets) == 0
    assert os_path_exists(last_run_metrics_path)


def test_brick_sheets_to_lego_with_cursor_Scenario1_PopulateBudPayRows(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00171_columns = [
        kw.spark_face,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    bk00171_str = "bk00171"
    bk00171row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    bk00171_df = DataFrame([bk00171row0], columns=bk00171_columns)
    bk00171_ex0_str = f"example0_{bk00171_str}"
    save_sheet(b_src_dir_file_path, bk00171_ex0_str, bk00171_df)

    bk00101_columns = [
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
    bk1row0 = [e3, exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    bk00101_1df = DataFrame([bk1row0], columns=bk00101_columns)
    bk00101_ex0_str = "example0_bk00101"
    save_sheet(b_src_dir_file_path, bk00101_ex0_str, bk00101_1df)

    # Names of tables
    bk00171_raw = f"{bk00171_str}_brixk_raw"
    bk00171_agg = f"{bk00171_str}_brixk_agg"
    bk00171_valid = f"{bk00171_str}_brixk_vld"
    sparks_brixk_vld_tablename = kw.sparks_brixk_vld
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

    assert not db_table_exists(cursor0, bk00171_raw)
    assert not db_table_exists(cursor0, bk00171_agg)
    assert not db_table_exists(cursor0, kw.sparks_brixk_agg)
    assert not db_table_exists(cursor0, sparks_brixk_vld_tablename)
    assert not db_table_exists(cursor0, bk00171_valid)
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
    assert not db_table_exists(cursor0, kw.moment_tranbook_nets)
    assert not db_table_exists(cursor0, kw.moment_kpi001_contact_nets)
    # self.moment_agg_tables_to_moment_ote1_agg(cursor)
    moments_dir = create_path(mstr_dir, "moments")
    print(f"{get_level1_dirs(moments_dir)=}")

    # # create personunits
    # self.person_tables_to_lego_spark_person_csvs(cursor)

    # # create all moment_job and mandate reports
    # calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir)

    # WHEN
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert get_row_count(cursor0, bk00171_raw) == 1
    assert get_row_count(cursor0, bk00171_agg) == 1
    print(cursor0.execute(f"SELECT * FROM {kw.sparks_brixk_agg}").fetchall())
    assert get_row_count(cursor0, kw.sparks_brixk_agg) == 2
    assert get_row_count(cursor0, sparks_brixk_vld_tablename) == 1
    assert get_row_count(cursor0, bk00171_valid) == 1
    assert get_row_count(cursor0, trlname_sound_raw) == 1
    assert get_row_count(cursor0, momentunit_sound_raw) == 2
    assert get_row_count(cursor0, prnunit_put_sound_raw) == 2
    assert get_row_count(cursor0, prncont_put_sound_raw) == 1
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
    assert get_row_count(cursor0, kw.moment_tranbook_nets) == 1
    assert get_row_count(cursor0, kw.moment_kpi001_contact_nets) == 1


def test_brick_sheets_to_lego_with_cursor_Scenario2_PopulateMomentTranBook(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    e3 = 3
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00102_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.tran_time,
        kw.amount,
        kw.knot,
    ]
    bk00102_str = "bk00102"
    tp37 = 37
    sue_to_bob_amount = 200
    bk00102row0 = [e3, exx.sue, exx.a23, exx.sue, exx.bob, tp37, sue_to_bob_amount, ";"]
    bk00102_df = DataFrame([bk00102row0], columns=bk00102_columns)
    bk00102_ex0_str = f"example0_{bk00102_str}"
    save_sheet(b_src_dir_file_path, bk00102_ex0_str, bk00102_df)

    assert not db_table_exists(cursor0, kw.moment_tranbook_nets)

    # WHEN
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert get_row_count(cursor0, kw.moment_tranbook_nets) == 1


def test_brick_sheets_to_lego_with_cursor_Scenario3_WhenNoMomentBricks_ote1_IsStillCreated(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00001_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    bk00001_df = DataFrame(bk00001_rows, columns=bk00001_columns)
    save_sheet(b_src_dir_file_path, "bk00001_ex3", bk00001_df)
    moment_mstr = fay_wdir.moment_mstr_dir
    a23_lasso = lassounit_shop(exx.a23)
    a23_ote1_csv_path = create_moment_ote1_csv_path(moment_mstr, a23_lasso)
    assert os_path_exists(a23_ote1_csv_path) is False

    # WHEN
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert os_path_exists(a23_ote1_csv_path)


def test_brick_sheets_to_lego_with_cursor_Scenario4_DeletesPreviousFiles(
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
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False


def test_brick_sheets_to_lego_with_cursor_Scenario5_CreatesFiles(
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
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    bk00101_columns = [
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
    bk1row0 = [spark2, exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    bk00101_1df = DataFrame([bk1row0], columns=bk00101_columns)
    bk00101_ex0_str = "example0_bk00101"
    save_sheet(b_src_dir_file_path, bk00101_ex0_str, bk00101_1df)

    bk3row0 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    bk3row1 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    bk3row2 = [spark2, exx.sue, minute_420, exx.a23, hour7am, ";"]
    bk00103_1df = DataFrame([bk3row0, bk3row1], columns=bk00103_columns)
    bk00103_3df = DataFrame([bk3row1, bk3row0, bk3row2], columns=bk00103_columns)
    bk00103_ex1_str = "example1_bk00103"
    bk00103_ex3_str = "example3_bk00103"
    save_sheet(b_src_dir_file_path, bk00103_ex1_str, bk00103_1df)
    save_sheet(b_src_dir_file_path, bk00103_ex3_str, bk00103_3df)
    bk00001_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    bk00001_df = DataFrame(bk00001_rows, columns=bk00001_columns)
    save_sheet(b_src_dir_file_path, "bk00001_ex3", bk00001_df)
    mstr_dir = fay_wdir.moment_mstr_dir
    wrong_a23_moment_dir = create_path(mstr_dir, exx.a23)
    assert os_path_exists(wrong_a23_moment_dir) is False
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, exx.sue)
    a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, exx.sue)
    sue37_mandate_path = bud_mandate(mstr_dir, a23_lasso, exx.sue, tp37)
    assert os_path_exists(b_src_dir_file_path)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fay_wdir.worlds_dir) == 5

    # WHEN
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )

    # THEN
    assert os_path_exists(wrong_a23_moment_dir) is False
    assert os_path_exists(b_src_dir_file_path)
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_sue_gut_path)
    assert os_path_exists(a23_sue_job_path)
    assert os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fay_wdir.worlds_dir) == 42


def test_brick_sheets_to_lego_with_cursor_Scenario6_NoDuplicates(
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
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00103_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.cumulative_minute,
        kw.moment_rope,
        kw.hour_label,
        kw.knot,
    ]
    bk3row0 = [spark1, exx.sue, minute_360, exx.a23, hour6am, ";"]
    bk3row1 = [spark1, exx.sue, minute_420, exx.a23, hour7am, ";"]
    bk3row2 = [spark2, exx.sue, minute_420, exx.a23, hour7am, ";"]
    bk00103_1df = DataFrame([bk3row0, bk3row1], columns=bk00103_columns)
    bk00103_3df = DataFrame([bk3row1, bk3row0, bk3row2], columns=bk00103_columns)
    bk00103_ex1_str = "example1_bk00103"
    bk00103_ex3_str = "example3_bk00103"
    save_sheet(b_src_dir_file_path, bk00103_ex1_str, bk00103_1df)
    save_sheet(b_src_dir_file_path, bk00103_ex3_str, bk00103_3df)
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )
    assert [] == get_all_tables_with_duplicates(cursor0)
    # WHEN
    brick_sheets_to_lego_with_cursor(
        cursor0, fay_wdir.bricks_src_dir, fay_wdir.moment_mstr_dir
    )
    # THEN
    all_tables_with_duplicates_after_2nd_run = get_all_tables_with_duplicates(cursor0)
    # for tablename in all_tables_with_duplicates_after_2nd_run:
    #     table_count = get_row_count(cursor0, tablename)
    #     print(f"Table with duplicate '{tablename}' {table_count=}")
    #     print_table(cursor0, tablename)
    assert [] == all_tables_with_duplicates_after_2nd_run


def test_brick_sheets_to_lego_with_cursor_Scenario7_NoDuplicates_bk00170(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))

    spark1 = 1
    spark2 = 2
    otx_360 = 360
    otx_420 = 420
    inx_400 = 400
    inx_500 = 500
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00170_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.otx_time,
        kw.inx_time,
    ]
    bk70row0 = [spark1, exx.sue, exx.a23, otx_360, inx_400]
    bk70row1 = [spark1, exx.sue, exx.a23, otx_420, inx_500]
    bk70row2 = [spark2, exx.sue, exx.a23, otx_420, inx_500]
    bk00170_1df = DataFrame([bk70row0, bk70row1], columns=bk00170_columns)
    bk00170_3df = DataFrame([bk70row1, bk70row0, bk70row2], columns=bk00170_columns)
    bk00170_ex1_str = "example1_bk00170"
    bk00170_ex3_str = "example3_bk00170"
    save_sheet(b_src_dir_file_path, bk00170_ex1_str, bk00170_1df)
    save_sheet(b_src_dir_file_path, bk00170_ex3_str, bk00170_3df)

    bk00101_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.bud_time,
        kw.knot,
        kw.quota,
        kw.celldepth,
    ]
    row0 = [1, exx.sue, exx.a23, "Alice", 360, ";", 10, 1]
    row1 = [1, exx.sue, exx.a23, "Alice", 420, ";", 15, 2]
    row2 = [2, exx.sue, exx.a23, "Bob", 420, ";", 20, 1]
    bk00101_df = DataFrame([row0, row1, row2], columns=bk00101_columns)
    save_sheet(b_src_dir_file_path, "example_bk00101", bk00101_df)

    b_src_dir = fay_wdir.bricks_src_dir
    brick_sheets_to_lego_with_cursor(cursor0, b_src_dir, fay_wdir.moment_mstr_dir)
    assert [] == get_all_tables_with_duplicates(cursor0)

    # WHEN
    brick_sheets_to_lego_with_cursor(cursor0, b_src_dir, fay_wdir.moment_mstr_dir)

    # THEN
    all_tables_with_duplicates_after_2nd_run = get_all_tables_with_duplicates(cursor0)
    assert [] == all_tables_with_duplicates_after_2nd_run


def test_brick_sheets_to_lego_mstr_Scenario0_CreatesDatabaseFile(
    temp3_fs,
):
    # sourcery skip: extract-method, move-assign-in-block
    # ESTABLISH:
    fay_str = "Fay"
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
    # delete_dir(fay_wdir.worlds_dir)
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00171_columns = [
        kw.spark_face,
        kw.spark_num,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.otx_name,
        kw.inx_name,
    ]
    tp37 = 37
    bk00171_str = "bk00171"
    bk00171row0 = [exx.sue, e3, exx.a23, exx.sue, exx.sue, exx.sue, sue_inx]
    bk00171_df = DataFrame([bk00171row0], columns=bk00171_columns)
    bk00171_ex0_str = f"example0_{bk00171_str}"
    save_sheet(b_src_dir_file_path, bk00171_ex0_str, bk00171_df)

    bk00101_columns = [
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
    bk1row0 = [e3, exx.sue, exx.a23, exx.sue, tp37, ";", sue_quota, sue_celldepth]
    bk00101_1df = DataFrame([bk1row0], columns=bk00101_columns)
    bk00101_ex0_str = "example0_bk00101"
    save_sheet(b_src_dir_file_path, bk00101_ex0_str, bk00101_1df)
    fay_db_path = fay_wdir.get_world_db_path()
    assert not os_path_exists(fay_db_path)

    # WHEN
    brick_sheets_to_lego_mstr(fay_wdir)

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn:
        bk00171_raw = f"{bk00171_str}_brixk_raw"
        bk00171_agg = f"{bk00171_str}_brixk_agg"
        bk00171_valid = f"{bk00171_str}_brixk_vld"
        sparks_brixk_vld_tablename = kw.sparks_brixk_vld
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
        assert get_row_count(cursor, bk00171_raw) == 1
        assert get_row_count(cursor, bk00171_agg) == 1
        assert get_row_count(cursor, kw.sparks_brixk_agg) == 2
        assert get_row_count(cursor, sparks_brixk_vld_tablename) == 1
        assert get_row_count(cursor, bk00171_valid) == 1
        assert get_row_count(cursor, trlname_sound_raw) == 1
        assert get_row_count(cursor, momentunit_sound_raw) == 2
        assert get_row_count(cursor, prnunit_put_sound_raw) == 2
        assert get_row_count(cursor, prncont_put_sound_raw) == 1
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


def test_brick_sheets_to_lego_mstr_Scenario1_Creates_job_Files(temp3_fs):
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
    bk00002_example = pandas_DataFrame(data, columns=cols)

    here_wdir = worlddir_shop("HereNow", str(temp3_fs))
    bk00002_example_path = create_path(here_wdir.bricks_src_dir, "example.xlsx")
    save_sheet(bk00002_example_path, "bk00002_ex1", bk00002_example)
    # print(bk00002_example().to_dict())
    mmt_dir = here_wdir.moment_mstr_dir
    hn_red_lasso = lassounit_shop(exx.hn_red)
    hn_red_mmt_json_path = create_moment_json_path(mmt_dir, hn_red_lasso)
    hn_red_yao_job_path = create_job_path(mmt_dir, hn_red_lasso, exx.yao)
    hn_red_zia_job_path = create_job_path(mmt_dir, hn_red_lasso, exx.zia)
    assert not os_path_exists(hn_red_mmt_json_path)
    assert not os_path_exists(hn_red_yao_job_path)
    assert not os_path_exists(hn_red_zia_job_path)

    # WHEN
    brick_sheets_to_lego_mstr(here_wdir)

    # THEN
    # world_test_ex_dir = "src\ch32_world\test\test_world_examples"
    # export_db_to_excel(here_wdir.get_world_db_path(), here_wdir.worlds_dir, "export.xlsx")
    assert os_path_exists(hn_red_mmt_json_path)
    assert os_path_exists(hn_red_zia_job_path)
    assert os_path_exists(hn_red_yao_job_path)
