from datetime import datetime
from os.path import exists as os_path_exists
from pandas import DataFrame as pandas_DataFrame
from pytest import fixture as pytest_fixture
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch04_rope.rope import create_rope, create_rope_from_labels as init_rope
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch10_person_listen._ref.ch10_path import create_job_path
from src.ch10_person_listen.keep_tool import open_job_file, save_job_file
from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch14_moment.moment_main import momentunit_shop, save_moment_file
from src.ch17_idea.brick_db_tool import save_sheet
from src.ch20_kpi._ref.ch20_path import create_day_punch_txt_path as day_punch_path
from src.ch21_world.test._util.ch21_examples import br00013_example
from src.ch21_world.world import idea_sheets_to_gcal_day_punchs, worlddir_shop
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


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
    idea_sheets_to_gcal_day_punchs(worlddir, exx.sue, apr7)

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
    br00011_data = [
        (spark0, exx.bob, exx.hn_blu, exx.sue, exx.sue),
        (spark0, exx.bob, exx.hn_blu, exx.sue, exx.yao),
        (spark0, exx.bob, exx.hn_blu, exx.yao, exx.yao),
        (spark0, exx.bob, exx.hn_blu, exx.yao, exx.sue),
    ]
    br00011_cols = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    br00011_df = pandas_DataFrame(br00011_data, columns=br00011_cols)
    # create tasks for sue, yao, others
    br00013_data = [
        (spark0, exx.bob, exx.zia, exx.hn_red, hr_mop, 1, True),
        (spark0, exx.bob, exx.yao, exx.hn_red, hr_tools, 2, True),
        (spark2, exx.bob, exx.sue, exx.hn_blu, hb_mop, 8, True),
        (spark3, exx.bob, exx.sue, exx.hn_blu, hb_sweep, 3, True),
        (spark4, exx.bob, exx.xio, exx.hn_blu, hb_brush, 1, True),
    ]
    br00013_cols = [
        kw.spark_num,
        kw.spark_face,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    br00013_df = pandas_DataFrame(br00013_data, columns=br00013_cols)
    here_wdir = worlddir_shop("HereNow", str(temp3_fs))
    bricks01_path = create_path(here_wdir.i_src_dir, "example.xlsx")
    # unrelated to this test
    # br00013_export_dir = create_path("C:\dev\_temp_working_dir", "br00013_example.xlsx")
    # br00011_export_dir = create_path("C:\dev\_temp_working_dir", "br00011_example.xlsx")
    # br00013_df.to_excel(br00013_export_dir, sheet_name="br00013_ex1", index=False)
    # br00011_df.to_excel(br00011_export_dir, sheet_name="br00011_ex1", index=False)
    save_sheet(bricks01_path, "br00013_ex1", br00013_df)
    save_sheet(bricks01_path, "br00011_ex1", br00011_df)
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
    idea_sheets_to_gcal_day_punchs(here_wdir, exx.sue, apr7)

    # THEN
    assert os_path_exists(hn_red_mmt_json_path)
    assert os_path_exists(hn_blu_mmt_json_path)
    assert os_path_exists(hn_red_zia_job_path)
    assert os_path_exists(hn_blu_yao_job_path)
    assert os_path_exists(hn_blu_sue_job_path)
    blu_sue_person = open_job_file(mmt_dir, hn_blu_lasso, exx.sue)
    print(f"{blu_sue_person.get_plan_dict().keys()=}")
    assert os_path_exists(hn_blu_xio_job_path)
    sue_hn_red_day_punch_path = day_punch_path(mmt_dir, hn_red_lasso, exx.sue)
    sue_hn_blu_day_punch_path = day_punch_path(mmt_dir, hn_blu_lasso, exx.sue)
    assert not os_path_exists(sue_hn_red_day_punch_path)
    assert os_path_exists(sue_hn_blu_day_punch_path)
    sue_hn_blu_punch_str = open_file(sue_hn_blu_day_punch_path)
    print(sue_hn_blu_punch_str)
    assert exx.sweep in sue_hn_blu_punch_str


# # TODO
# def save_today_day_punchs_to_markdown(
#     worlddir: WorldDir, person_name: PersonName, focus_group_title: GroupTitle = None
# ):
#     create_today_day_punchs(worlddir, person_name, focus_group_title)
#     # save today day punchs for person_name as markdown files in worlddir.output_dir
