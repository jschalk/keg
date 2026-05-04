from ch00_py.file_toolbox import create_path, set_dir
from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.lasso import lassounit_shop
from ch10_person_listen.keep_tool import save_job_file
from ch14_moment.moment_main import momentunit_shop, save_moment_file
from ch17_brick.brick_db_tool import get_sheet_names, openpyxl_load_workbook
from ch17_brick.brick_idea_csv import (
    add_momentunit_to_idea_csv_strs,
    add_personunit_to_idea_csv_strs,
    create_init_idea_brick_csv_strs,
)
from ch18_etl_config._ref.ch18_path import create_moment_mstr_path, create_world_db_path
from ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)
from ch24_idea_dst._ref.ch24_path import create_mind0002_path
from ch24_idea_dst.mind_db2df import (
    collect_mind0002_idea_csv_strs,
    create_mind0002_file,
)
from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from ref.keywords import Ch24Keywords as kw, ExampleStrs as exx
from sqlite3 import connect as sqlite3_connect


def test_collect_mind0002_idea_csv_strs_ReturnsObj_Scenario0_NoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    # WHEN
    gen_idea_csv_strs = collect_mind0002_idea_csv_strs(world_dir, exx.sue)
    # THEN
    expected_idea_csv_strs = create_init_idea_brick_csv_strs()
    assert gen_idea_csv_strs == expected_idea_csv_strs


def test_collect_mind0002_idea_csv_strs_ReturnsObj_Scenario1_MomentUnitsDoesNotHaveSue(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    save_moment_file(a23_moment, a23_lasso)
    # create bob job file
    bob_job = personunit_shop(exx.bob, exx.a23)
    bob_job.add_contactunit(exx.yao, 44, 55)
    bob_job.add_contactunit(exx.yao, 44, 55)
    save_job_file(moment_mstr_dir, bob_job)

    # WHEN
    gen_idea_csv_strs = collect_mind0002_idea_csv_strs(world_dir, exx.sue)
    # THEN
    # empty because Sue is not associated with any moment
    expected_idea_csv_strs = create_init_idea_brick_csv_strs()
    assert gen_idea_csv_strs == expected_idea_csv_strs


def test_collect_mind0002_idea_csv_strs_ReturnsObj_Scenario2_SingleMomentUnitHasSueJob(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    save_moment_file(a23_moment, a23_lasso)
    # create sue job file
    sue_job = personunit_shop(exx.sue, exx.a23)
    sue_job.add_contactunit(exx.yao, 44, 55)
    sue_job.add_contactunit(exx.yao, 44, 55)
    save_job_file(moment_mstr_dir, sue_job)

    # WHEN
    gen_idea_csv_strs = collect_mind0002_idea_csv_strs(world_dir, exx.sue)

    # THEN
    expected_idea_csv_strs = create_init_idea_brick_csv_strs()
    add_momentunit_to_idea_csv_strs(a23_moment, expected_idea_csv_strs, ",")
    add_personunit_to_idea_csv_strs(sue_job, expected_idea_csv_strs, ",")
    expected_bk00120_csv_str = expected_idea_csv_strs.get("bk00120")
    gen_bk00120_csv_str = gen_idea_csv_strs.get("bk00120")
    print(f"{expected_bk00120_csv_str=}")
    print(f"     {gen_bk00120_csv_str=}")
    assert gen_bk00120_csv_str == expected_bk00120_csv_str
    assert gen_idea_csv_strs == expected_idea_csv_strs
    print(gen_bk00120_csv_str)


def test_create_mind0002_file_CreatesFile_Scenario0_NoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    output_dir = create_path(world_dir, "output")
    sue_mind0002_path = create_mind0002_path(output_dir, exx.sue)
    assert os_path_exists(sue_mind0002_path) is False

    # WHEN
    create_mind0002_file(world_dir, output_dir, exx.sue)

    # THEN
    assert os_path_exists(sue_mind0002_path)
    sue_mind0002_sheetnames = get_sheet_names(sue_mind0002_path)
    idea_csv_strs = create_init_idea_brick_csv_strs()
    assert len(sue_mind0002_sheetnames) > 0
    assert set(sue_mind0002_sheetnames).issubset(set(idea_csv_strs.keys()))


def test_create_mind0002_file_CreatesFile_Scenario1_Basic(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    save_moment_file(a23_moment, a23_lasso)
    # create sue job file
    sue_job = personunit_shop(exx.sue, exx.a23)
    sue_job.add_contactunit(exx.yao, 44, 55)
    sue_job.add_contactunit(exx.yao, 44, 55)
    save_job_file(moment_mstr_dir, sue_job)
    output_dir = create_path(world_dir, "output")
    sue_mind0002_path = create_mind0002_path(output_dir, exx.sue)
    assert os_path_exists(sue_mind0002_path) is False

    # WHEN
    create_mind0002_file(world_dir, output_dir, exx.sue)

    # THEN
    assert os_path_exists(sue_mind0002_path)
    expected_idea_csv_strs = create_init_idea_brick_csv_strs()
    add_momentunit_to_idea_csv_strs(a23_moment, expected_idea_csv_strs, ",")
    add_personunit_to_idea_csv_strs(sue_job, expected_idea_csv_strs, ",")
    expected_bk00120_csv_str = expected_idea_csv_strs.get("bk00120")
    # print(f"{expected_bk00120_csv_str=}")
    sue_mind0002_sheetnames = get_sheet_names(sue_mind0002_path)
    idea_csv_strs = create_init_idea_brick_csv_strs()
    assert len(sue_mind0002_sheetnames) > 0
    assert set(sue_mind0002_sheetnames).issubset(set(idea_csv_strs.keys()))
    sue_wb = openpyxl_load_workbook(sue_mind0002_path)
    bk00120_worksheet = sue_wb["bk00120"]
    # for row in bk00120_worksheet.iter_rows(values_only=True):
    #     print(row)
