# from datetime import datetime
# from os.path import exists as os_path_exists
# from src.ch00_py.file_toolbox import open_file
# from src.ch09_person_lesson.lasso import lassounit_shop
# from src.ch10_person_listen.keep_tool import save_job_file
# from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
# from src.ch14_moment.moment_main import momentunit_shop, save_moment_file
# from src.ch20_kpi._ref.ch20_path import create_day_report_txt_path as day_report_path
# from src.ch20_kpi.test._util.ch20_examples import (
#     get_a23_sue_clean_example,
#     get_ep8_sue_clean_example,
#     get_ep8_yao_clean_example,
# )
# from src.ch21_world.test._util.ch21_env import get_temp_dir, temp_dir_setup
# from src.ch21_world.world import sheets_to_gcal_day_reports
# from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


# def test_get_person_gcal_day_reports_ReturnsObj_Scenario0_NoData(
#     temp_dir_setup,
# ):
#     # ESTABLISH
#     mmt_mstr_dir = get_temp_dir()
#     apr7 = datetime(2010, 4, 7)

#     # WHEN
#     sue_day_reports = sheets_to_gcal_day_reports(
#         moment_mstr_dir=mmt_mstr_dir,
#         person_name=exx.sue,
#         day=apr7,
#         focus_group_title=exx.run,
#     )

#     # THEN
#     assert sue_day_reports == {}


# def test_sheets_to_gcal_day_reports_SavesFiles_Scenario0_TwoSueReports(
#     temp_dir_setup,
# ):
#     # ESTABLISH
#     # TODO convert this to dataframe
#     sue_a23_person = get_a23_sue_clean_example()
#     sue_ep8_person = get_ep8_sue_clean_example()
#     yao_ep8_person = get_ep8_yao_clean_example()
#     # TODO save dataframes as sheets
#     epoch_config = get_default_epoch_config_dict()
#     x_epoch_label = epoch_config.get("epoch_label")
#     add_epoch_planunit(sue_a23_person, epoch_config)
#     add_epoch_planunit(sue_ep8_person, epoch_config)
#     add_epoch_planunit(yao_ep8_person, epoch_config)
#     apr7 = datetime(2010, 4, 7)
#     # save momentunit json
#     mmt_mstr_dir = get_temp_dir()
#     a23_lasso = lassounit_shop(exx.a23)
#     ep8_lasso = lassounit_shop(exx.ep8)
#     # assert exists moment_file(a23_moment, a23_lasso)
#     # assert exists moment_file(ep8_moment, ep8_lasso)
#     # assert exists job_file(mmt_mstr_dir, sue_a23_person)
#     # assert exists job_file(mmt_mstr_dir, sue_ep8_person)
#     # assert exists job_file(mmt_mstr_dir, yao_ep8_person)
#     sue_a23_day_report_path = day_report_path(mmt_mstr_dir, a23_lasso, exx.sue)
#     sue_ep8_day_report_path = day_report_path(mmt_mstr_dir, ep8_lasso, exx.sue)
#     assert not os_path_exists(sue_a23_day_report_path)
#     assert not os_path_exists(sue_ep8_day_report_path)

#     # WHEN
#     sheets_to_gcal_day_reports(moment_mstr_dir=mmt_mstr_dir)

#     # THEN
#     assert os_path_exists(sue_a23_day_report_path)
#     assert os_path_exists(sue_ep8_day_report_path)
#     sue_a23_day_report_str = open_file(sue_a23_day_report_path)
#     sue_ep8_day_report_str = open_file(sue_ep8_day_report_path)
#     assert "Schedule Priorities" in sue_ep8_day_report_str
#     assert f"Day Report for {exx.sue}" in sue_a23_day_report_str
#     assert f"Day Report for {exx.sue}" in sue_ep8_day_report_str
