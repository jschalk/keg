from ch00_py.file_toolbox import create_path, open_file
from ch04_rope.rope import create_rope_from_labels as init_rope
from ch09_person_lesson._ref.ch09_path import create_moment_json_path
from ch09_person_lesson.lasso import lassounit_shop
from ch10_person_listen._ref.ch10_path import create_job_path
from ch10_person_listen.keep_tool import open_job_file
from ch17_brick.brick_db_tool import save_sheet
from ch25_kpi._ref.ch25_path import (
    create_day_punch_txt_path as day_punch_path,
    create_dst_person_punch_path,
)
from ch26_world.world import (
    create_today_punchs,
    idea_sheets_to_gcal_day_punchs,
    worlddir_shop,
)
from datetime import datetime
from os.path import exists as os_path_exists
from pandas import DataFrame as pandas_DataFrame
from ref.keywords import Ch26Keywords as kw, ExampleStrs as exx


def test_idea_sheets_to_gcal_day_punchs_SavesFiles_Scenario0_TwoSueReports(
    temp3_fs,
):
    # ESTABLISH
    apr7 = datetime(2010, 4, 7)
    mmt_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    ep8_lasso = lassounit_shop(exx.ep8)
    sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
    sue_ep8_day_punch_path = day_punch_path(mmt_mstr_dir, ep8_lasso, exx.sue)
    worlddir = worlddir_shop("HereNow", str(temp3_fs))
    assert not os_path_exists(sue_a23_day_punch_path)
    assert not os_path_exists(sue_ep8_day_punch_path)

    # WHEN
    idea_sheets_to_gcal_day_punchs(worlddir, {exx.sue}, apr7)

    # THEN
    assert not os_path_exists(sue_a23_day_punch_path)
    assert not os_path_exists(sue_ep8_day_punch_path)


def test_idea_sheets_to_gcal_day_punchs_SavesFiles_Scenario1_PopulatedSueReport(
    temp3_fs,
):
    # ESTABLISH
    hr_mop = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.mop])
    hr_tools = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.scrub])
    hb_mop = init_rope(["herenow_blu", "family", exx.casa, exx.clean, exx.mop])
    hb_sweep = init_rope(["herenow_blu", "family", exx.casa, exx.clean, exx.sweep])
    hb_brush = init_rope(["herenow_blu", "family", exx.casa, exx.clean, "brush"])
    spark0, spark2, spark3, spark4 = (0, 2, 3, 4)
    # create connections between sue and yao and themselves
    bk00001_data = [
        (spark0, exx.bob, exx.hn_blu, exx.sue, exx.sue),
        (spark0, exx.bob, exx.hn_blu, exx.sue, exx.yao),
        (spark0, exx.bob, exx.hn_blu, exx.yao, exx.yao),
        (spark0, exx.bob, exx.hn_blu, exx.yao, exx.sue),
    ]
    bk00001_cols = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_df = pandas_DataFrame(bk00001_data, columns=bk00001_cols)
    # create tasks for sue, yao, others
    bk00002_data = [
        (spark0, exx.bob, exx.zia, exx.hn_red, hr_mop, 1, True),
        (spark0, exx.bob, exx.yao, exx.hn_red, hr_tools, 2, True),
        (spark2, exx.bob, exx.sue, exx.hn_blu, hb_mop, 8, True),
        (spark3, exx.bob, exx.sue, exx.hn_blu, hb_sweep, 3, True),
        (spark4, exx.bob, exx.xio, exx.hn_blu, hb_brush, 1, True),
    ]
    bk00002_cols = [
        kw.spark_num,
        kw.spark_face,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    bk00002_df = pandas_DataFrame(bk00002_data, columns=bk00002_cols)
    here_wdir = worlddir_shop("HereNow", str(temp3_fs))
    bricks01_path = create_path(here_wdir.bricks_src_dir, "example.xlsx")
    # unrelated to this test
    # bk00002_export_dir = create_path("C:\dev\_temp_working_dir", "bk00002_example.xlsx")
    # bk00001_export_dir = create_path("C:\dev\_temp_working_dir", "bk00001_example.xlsx")
    # bk00002_df.to_excel(bk00002_export_dir, sheet_name="bk00002_ex1", index=False)
    # bk00001_df.to_excel(bk00001_export_dir, sheet_name="bk00001_ex1", index=False)
    save_sheet(bricks01_path, "bk00002_ex1", bk00002_df)
    save_sheet(bricks01_path, "bk00001_ex1", bk00001_df)
    mmt_dir = here_wdir.moment_mstr_dir
    hn_red_lasso = lassounit_shop(exx.hn_red)
    hn_blu_lasso = lassounit_shop(exx.hn_blu)
    hn_red_mmt_json_path = create_moment_json_path(mmt_dir, hn_red_lasso)
    hn_blu_mmt_json_path = create_moment_json_path(mmt_dir, hn_blu_lasso)
    hn_red_zia_job_path = create_job_path(mmt_dir, hn_red_lasso, exx.zia)
    hn_blu_yao_job_path = create_job_path(mmt_dir, hn_blu_lasso, exx.yao)
    hn_blu_sue_job_path = create_job_path(mmt_dir, hn_blu_lasso, exx.sue)
    hn_blu_xio_job_path = create_job_path(mmt_dir, hn_blu_lasso, exx.xio)
    assert not os_path_exists(hn_red_mmt_json_path)
    assert not os_path_exists(hn_blu_mmt_json_path)
    assert not os_path_exists(hn_red_zia_job_path)
    assert not os_path_exists(hn_blu_yao_job_path)
    assert not os_path_exists(hn_blu_sue_job_path)
    assert not os_path_exists(hn_blu_xio_job_path)
    sue_hn_red_day_punch_path = day_punch_path(mmt_dir, hn_red_lasso, exx.sue)
    sue_hn_blu_day_punch_path = day_punch_path(mmt_dir, hn_blu_lasso, exx.sue)
    assert not os_path_exists(sue_hn_red_day_punch_path)
    assert not os_path_exists(sue_hn_blu_day_punch_path)

    # WHEN
    apr7 = datetime(2010, 5, 7)
    idea_sheets_to_gcal_day_punchs(here_wdir, {exx.sue}, apr7)

    # THEN
    assert os_path_exists(hn_red_mmt_json_path)
    assert os_path_exists(hn_blu_mmt_json_path)
    assert os_path_exists(hn_red_zia_job_path)
    assert os_path_exists(hn_blu_yao_job_path)
    assert os_path_exists(hn_blu_sue_job_path)
    blu_sue_person = open_job_file(mmt_dir, hn_blu_lasso, exx.sue)
    # print(f"{blu_sue_person.get_plan_dict().keys()=}")
    assert os_path_exists(hn_blu_xio_job_path)
    sue_hn_red_day_punch_path = day_punch_path(mmt_dir, hn_red_lasso, exx.sue)
    sue_hn_blu_day_punch_path = day_punch_path(mmt_dir, hn_blu_lasso, exx.sue)
    assert not os_path_exists(sue_hn_red_day_punch_path)
    assert os_path_exists(sue_hn_blu_day_punch_path)
    sue_hn_blu_punch_str = open_file(sue_hn_blu_day_punch_path)
    print(sue_hn_blu_punch_str)
    assert exx.sweep in sue_hn_blu_punch_str


def test_create_today_punchs_SavesFiles_Scenario0_PopulatedSueReport(
    temp3_fs,
):
    # ESTABLISH
    hr_mop = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.mop])
    hr_tools = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.scrub])
    hb_mop = init_rope(["herenow_blu", "family", exx.casa, exx.clean, exx.mop])
    hb_sweep = init_rope(["herenow_blu", "family", exx.casa, exx.clean, exx.sweep])
    hb_brush = init_rope(["herenow_blu", "family", exx.casa, exx.clean, "brush"])
    spark0, spark2, spark3, spark4 = (0, 2, 3, 4)
    # create connections between sue and yao and themselves
    bk00001_cols = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_data = [
        (spark0, exx.bob, exx.hn_blu, exx.sue, exx.sue),
        (spark0, exx.bob, exx.hn_blu, exx.sue, exx.yao),
        (spark0, exx.bob, exx.hn_blu, exx.yao, exx.yao),
        (spark0, exx.bob, exx.hn_blu, exx.yao, exx.sue),
    ]
    bk00001_df = pandas_DataFrame(bk00001_data, columns=bk00001_cols)
    # create tasks for sue, yao, others
    bk00002_cols = [
        kw.spark_num,
        kw.spark_face,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    bk00002_data = [
        (spark0, exx.bob, exx.zia, exx.hn_red, hr_mop, 1, True),
        (spark0, exx.bob, exx.yao, exx.hn_red, hr_tools, 2, True),
        (spark2, exx.bob, exx.sue, exx.hn_blu, hb_mop, 8, True),
        (spark3, exx.bob, exx.sue, exx.hn_blu, hb_sweep, 3, True),
        (spark4, exx.bob, exx.xio, exx.hn_blu, hb_brush, 1, True),
    ]
    bk00002_df = pandas_DataFrame(bk00002_data, columns=bk00002_cols)
    # external_dir = "C:dev/_temp_working_dir"
    here_wdir = worlddir_shop("HereNow", str(temp3_fs))
    bricks01_path = create_path(here_wdir.bricks_src_dir, "example.xlsx")
    # unrelated to this test
    # bk00002_export_dir = create_path("C:\dev\_temp_working_dir", "bk00002_example.xlsx")
    # bk00001_export_dir = create_path("C:\dev\_temp_working_dir", "bk00001_example.xlsx")
    # bk00002_df.to_excel(bk00002_export_dir, sheet_name="bk00002_ex1", index=False)
    # bk00001_df.to_excel(bk00001_export_dir, sheet_name="bk00001_ex1", index=False)
    save_sheet(bricks01_path, "bk00002_ex1", bk00002_df)
    save_sheet(bricks01_path, "bk00001_ex1", bk00001_df)
    mmt_dir = here_wdir.moment_mstr_dir
    hn_red_lasso = lassounit_shop(exx.hn_red)
    hn_blu_lasso = lassounit_shop(exx.hn_blu)
    hn_red_mmt_json_path = create_moment_json_path(mmt_dir, hn_red_lasso)
    hn_blu_mmt_json_path = create_moment_json_path(mmt_dir, hn_blu_lasso)
    hn_red_zia_job_path = create_job_path(mmt_dir, hn_red_lasso, exx.zia)
    hn_blu_yao_job_path = create_job_path(mmt_dir, hn_blu_lasso, exx.yao)
    hn_blu_sue_job_path = create_job_path(mmt_dir, hn_blu_lasso, exx.sue)
    hn_blu_xio_job_path = create_job_path(mmt_dir, hn_blu_lasso, exx.xio)
    assert not os_path_exists(hn_red_mmt_json_path)
    assert not os_path_exists(hn_blu_mmt_json_path)
    assert not os_path_exists(hn_red_zia_job_path)
    assert not os_path_exists(hn_blu_yao_job_path)
    assert not os_path_exists(hn_blu_sue_job_path)
    assert not os_path_exists(hn_blu_xio_job_path)
    sue_hn_red_day_punch_path = day_punch_path(mmt_dir, hn_red_lasso, exx.sue)
    sue_hn_blu_day_punch_path = day_punch_path(mmt_dir, hn_blu_lasso, exx.sue)
    assert not os_path_exists(sue_hn_red_day_punch_path)
    assert not os_path_exists(sue_hn_blu_day_punch_path)

    # WHEN
    gen_dst_persons_punch_paths = create_today_punchs(
        person_names={exx.sue},
        world_name=here_wdir.world_name,
        worlds_dir=here_wdir.worlds_dir,
        output_dir=here_wdir.output_dir,
        bricks_src_dir=here_wdir.bricks_src_dir,
        ideas_src_dir=here_wdir.ideas_src_dir,
    )

    # THEN
    # assert os_path_exists(hn_red_mmt_json_path)
    # assert os_path_exists(hn_blu_mmt_json_path)
    assert os_path_exists(hn_red_zia_job_path)
    assert os_path_exists(hn_blu_yao_job_path)
    assert os_path_exists(hn_blu_sue_job_path)
    blu_sue_person = open_job_file(mmt_dir, hn_blu_lasso, exx.sue)
    # print(f"{blu_sue_person.get_plan_dict().keys()=}")
    assert os_path_exists(hn_blu_xio_job_path)
    sue_hn_red_day_punch_path = day_punch_path(mmt_dir, hn_red_lasso, exx.sue)
    sue_hn_blu_day_punch_path = day_punch_path(mmt_dir, hn_blu_lasso, exx.sue)
    assert not os_path_exists(sue_hn_red_day_punch_path)
    assert os_path_exists(sue_hn_blu_day_punch_path)
    sue_hn_blu_punch_str = open_file(sue_hn_blu_day_punch_path)
    # print(sue_hn_blu_punch_str)
    assert exx.sweep in sue_hn_blu_punch_str
    sue_dst_person_punch_path = create_dst_person_punch_path(
        here_wdir.output_dir, hn_blu_lasso, exx.sue
    )
    print(f"{exx.sue=} {sue_dst_person_punch_path=}")
    expected_dst_persons_punch_paths = {
        exx.sue: {hn_blu_lasso.moment_rope: {sue_dst_person_punch_path}}
    }
    for person_name, gen_dst_file_paths in gen_dst_persons_punch_paths.items():
        print(f"{person_name=} {gen_dst_file_paths=}")
    assert gen_dst_persons_punch_paths.keys() == expected_dst_persons_punch_paths.keys()
    gen_sue_punch_paths = gen_dst_persons_punch_paths.get(exx.sue)
    expected_sue_punch_paths = expected_dst_persons_punch_paths.get(exx.sue)
    assert gen_sue_punch_paths == expected_sue_punch_paths
    assert gen_dst_persons_punch_paths == expected_dst_persons_punch_paths
