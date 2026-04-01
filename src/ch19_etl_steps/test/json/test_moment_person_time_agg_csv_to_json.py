from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import open_json, save_file
from src.ch04_rope.rope import create_rope
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch18_etl_config._ref.ch18_path import (
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from src.ch19_etl_steps.etl_main import etl_moment_ote1_agg_csvs_to_jsons
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_moment_ote1_agg_csvs_to_jsons_CreatesFile_Scenaro0(
    temp3_fs,
):
    # ESTABLISH
    spark3 = 3
    spark7 = 7
    amy45_str = "amy45"
    timenum55 = 55
    timenum66 = 66
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    a45_lasso = lassounit_shop(create_rope(amy45_str))
    a23_spark_time_p = create_moment_ote1_csv_path(moment_mstr_dir, a23_lasso)
    a45_spark_time_p = create_moment_ote1_csv_path(moment_mstr_dir, a45_lasso)
    a23_spark_time_csv = f"""{kw.moment_rope},{kw.person_name},{kw.spark_num},{kw.bud_time},{kw.error_message}
{exx.a23},{exx.bob},{spark3},{timenum55},
"""
    a45_spark_time_csv = f"""{kw.moment_rope},{kw.person_name},{kw.spark_num},{kw.bud_time},{kw.error_message}
{amy45_str},{exx.sue},{spark3},{timenum55},
{amy45_str},{exx.sue},{spark7},{timenum66},
"""
    save_file(a23_spark_time_p, None, a23_spark_time_csv)
    save_file(a45_spark_time_p, None, a45_spark_time_csv)
    assert os_path_exists(a23_spark_time_p)
    assert os_path_exists(a45_spark_time_p)
    a23_ote1_json_path = create_moment_ote1_json_path(moment_mstr_dir, a23_lasso)
    a45_ote1_json_path = create_moment_ote1_json_path(moment_mstr_dir, a45_lasso)
    assert os_path_exists(a23_ote1_json_path) is False
    assert os_path_exists(a45_ote1_json_path) is False

    # WHEN
    etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_ote1_json_path)
    assert os_path_exists(a45_ote1_json_path)
    a23_ote1_dict = open_json(a23_ote1_json_path)
    a45_ote1_dict = open_json(a45_ote1_json_path)
    assert a23_ote1_dict == {exx.bob: {str(timenum55): spark3}}
    assert a45_ote1_dict == {exx.sue: {str(timenum55): spark3, str(timenum66): spark7}}
