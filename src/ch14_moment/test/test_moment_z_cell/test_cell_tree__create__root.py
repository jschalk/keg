from ch00_py.file_toolbox import count_dirs_files, open_json, save_json
from ch09_person_lesson._ref.ch09_path import (
    create_moment_json_path,
    create_moment_persons_dir_path,
)
from ch09_person_lesson.lasso import lassounit_shop
from ch11_bud._ref.ch11_path import create_cell_json_path
from ch11_bud.bud_main import DEFAULT_CELLDEPTH
from ch14_moment.moment_main import _get_ote1_max_past_spark_num, momentunit_shop
from os.path import exists as os_path_exists
from ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_get_ote1_max_past_spark_num_ReturnsObj_Scenaro0(
    temp3_fs,
):
    # ESTABLISH
    tp37 = 37
    ote1_dict = {}

    # WHEN / THEN
    assert not _get_ote1_max_past_spark_num(exx.bob, ote1_dict, tp37)


def test_MomentUnit_create_buds_root_cells_Scenaro0_BudEmpty(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    amy23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    print(f"{a23_json_path=}")
    a23_persons_path = create_moment_persons_dir_path(moment_mstr_dir, a23_lasso)
    assert count_dirs_files(a23_persons_path) == 0

    # WHEN
    amy23_moment.create_buds_root_cells({})

    # THEN
    assert count_dirs_files(a23_persons_path) == 0


def test_MomentUnit_create_buds_root_cells_Scenaro1_BudExists(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    timenum37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(exx.bob, timenum37, bud1_quota)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create spark time mapping person_time_agg for time 37
    spark3 = 3
    spark7 = 7
    timenum66 = 66
    a23_ote1_dict = {exx.bob: {str(timenum37): spark3, str(timenum66): spark7}}

    # timenum37 cell path
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_lasso, exx.bob, timenum37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(kw.celldepth) == DEFAULT_CELLDEPTH
    assert cell_dict.get(kw.bud_person_name) == exx.bob
    assert cell_dict.get(kw.quota) == bud1_quota
    assert cell_dict.get(kw.spark_num) == spark3


def test_MomentUnit_create_buds_root_cells_Scenaro2_BudExistsButNoPersonExistsInSparksPast(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    timenum37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(exx.bob, timenum37, bud1_quota)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create spark time mapping person_time_agg for time 37
    spark3 = 3
    spark7 = 7
    timenum40 = 40
    timenum66 = 66
    a23_ote1_dict = {exx.bob: {str(timenum40): spark3, str(timenum66): spark7}}
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_lasso, exx.bob, timenum37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(kw.ancestors) == []
    assert not cell_dict.get(kw.spark_num)
    assert cell_dict.get(kw.celldepth) == DEFAULT_CELLDEPTH
    assert cell_dict.get(kw.bud_person_name) == exx.bob
    assert cell_dict.get(kw.quota) == bud1_quota


def test_MomentUnit_create_buds_root_cells_Scenaro3_BudExistsNotPerfectMatch_bud_time_spark_num(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    a23_mana_grain = 2

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(exx.a23, mstr_dir, mana_grain=a23_mana_grain)
    print(f"{amy23_moment.mana_grain=}")
    timenum37 = 37
    bud1_quota = 450
    bud1_celldepth = 3
    amy23_moment.add_budunit(exx.bob, timenum37, bud1_quota, celldepth=bud1_celldepth)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create spark time mapping person_time_agg for time 37
    spark3 = 3
    spark7 = 7
    timenum30 = 30
    timenum66 = 66
    a23_ote1_dict = {exx.bob: {str(timenum30): spark3, str(timenum66): spark7}}

    # destination of cell json
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_lasso, exx.bob, timenum37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    assert cell_dict.get(kw.ancestors) == []
    assert cell_dict.get(kw.spark_num) == spark3
    assert cell_dict.get(kw.celldepth) == bud1_celldepth
    assert cell_dict.get(kw.bud_person_name) == exx.bob
    assert cell_dict.get(kw.mana_grain) == a23_mana_grain
    assert cell_dict.get(kw.quota) == bud1_quota
