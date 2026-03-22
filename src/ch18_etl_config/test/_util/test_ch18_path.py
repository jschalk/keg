from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import create_rope
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch18_etl_config._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_mstr_path,
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
    create_stance0001_path,
    create_stances_dir_path,
    create_stances_person_dir_path,
    create_world_db_path,
)
from src.ch18_etl_config.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

STANCE0001_FILENAME = "stance0001.xlsx"
MOMENT_OTE1_AGG_CSV_FILENAME = "moment_ote1_agg.csv"
MOMENT_OTE1_AGG_JSON_FILENAME = "moment_ote1_agg.json"
LAST_RUN_METRICS_JSON_FILENAME = "last_run_metrics.json"
WORLD_DB_FILENAME = "world.db"


def test_a18_path_constants_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert MOMENT_OTE1_AGG_CSV_FILENAME == "moment_ote1_agg.csv"
    assert MOMENT_OTE1_AGG_JSON_FILENAME == "moment_ote1_agg.json"
    assert LAST_RUN_METRICS_JSON_FILENAME == "last_run_metrics.json"
    assert STANCE0001_FILENAME == "stance0001.xlsx"
    assert WORLD_DB_FILENAME == "world.db"


def test_create_moment_mstr_path_ReturnsObj():
    # ESTABLISH
    x_world_dir = get_temp_dir()

    # WHEN
    gen_last_run_metrics_path = create_moment_mstr_path(x_world_dir)

    # THEN
    expected_path = create_path(x_world_dir, "moment_mstr")
    assert gen_last_run_metrics_path == expected_path


def test_create_moment_mstr_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_mstr_path(world_dir="world_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_mstr_path) == doc_str


def test_create_last_run_metrics_path_ReturnsObj():
    # ESTABLISH
    x_world_dir = get_temp_dir()

    # WHEN
    gen_last_run_metrics_path = create_last_run_metrics_path(x_world_dir)

    # THEN
    expected_path = create_path(x_world_dir, LAST_RUN_METRICS_JSON_FILENAME)
    assert gen_last_run_metrics_path == expected_path


def test_create_stances_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_dir_path(x_moment_mstr_dir)

    # THEN
    expected_stances_dir = create_path(x_moment_mstr_dir, "stances")
    assert gen_bob_stance_dir == expected_stances_dir


def test_create_stances_person_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_person_dir_path(x_moment_mstr_dir, exx.bob)

    # THEN
    stances_dir = create_stances_dir_path(x_moment_mstr_dir)
    expected_bob_stance_dir = create_path(stances_dir, exx.bob)
    assert gen_bob_stance_dir == expected_bob_stance_dir


def test_create_stance0001_path_ReturnsObj():
    # ESTABLISH
    output_dir = get_temp_dir()

    # WHEN
    gen_stance0001_xlsx_path = create_stance0001_path(output_dir)

    # THEN
    expected_stance000001_path = create_path(output_dir, STANCE0001_FILENAME)
    assert gen_stance0001_xlsx_path == expected_stance000001_path


LINUX_OS = platform_system() == "Linux"


def test_create_last_run_metrics_path_HasDocString():
    # ESTABLISH
    doc_str = create_last_run_metrics_path("world_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_last_run_metrics_path) == doc_str


def test_create_stances_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_dir_path(moment_mstr_dir="moment_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_dir_path) == doc_str


def test_create_stances_person_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_person_dir_path(
        moment_mstr_dir="moment_mstr_dir", person_name=kw.person_name
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_person_dir_path) == doc_str


def test_create_stance0001_path_HasDocString():
    # ESTABLISH
    doc_str = create_stance0001_path(output_dir="output_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stance0001_path) == doc_str


def test_create_moment_ote1_csv_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_a23_te_csv_path = create_moment_ote1_csv_path(x_moment_mstr_dir, a23_lasso)

    # THEN
    moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_path = create_path(moments_dir, "Amy23")
    expected_a23_te_path = create_path(a23_path, MOMENT_OTE1_AGG_CSV_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_create_moment_ote1_json_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_a23_te_csv_path = create_moment_ote1_json_path(x_moment_mstr_dir, a23_lasso)

    # THEN
    moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_path = create_path(moments_dir, "Amy23")
    expected_a23_te_path = create_path(a23_path, MOMENT_OTE1_AGG_JSON_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_create_world_db_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_world_db_path = create_world_db_path(x_moment_mstr_dir)

    # THEN
    expected_path = create_path(x_moment_mstr_dir, WORLD_DB_FILENAME)
    assert gen_world_db_path == expected_path


def test_create_moment_ote1_csv_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_moment_ote1_csv_path("moment_mstr_dir", moment_lasso)
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_ote1_csv_path) == doc_str


def test_create_moment_ote1_json_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_moment_ote1_json_path("moment_mstr_dir", moment_lasso)
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_ote1_json_path) == doc_str


def test_create_world_db_path_HasDocString():
    # ESTABLISH
    doc_str = create_world_db_path("moment_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_world_db_path) == doc_str
