from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson.lasso import LassoUnit
from src.ch18_etl_config._ref.ch18_semantic_types import PersonName


def create_moment_mstr_path(world_dir: str) -> str:
    """Returns path: world_dir\\moment_mstr"""
    return create_path(world_dir, "moment_mstr")


def create_moment_ote1_csv_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\moment_ote1_agg.csv"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_lasso.make_path())
    return create_path(moment_path, "moment_ote1_agg.csv")


def create_moment_ote1_json_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\moment_ote1_agg.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_lasso.make_path())
    return create_path(moment_path, "moment_ote1_agg.json")


def create_stances_dir_path(moment_mstr_dir: str) -> str:
    """Returns path: moment_mstr_dir\\stances"""
    return create_path(moment_mstr_dir, "stances")


def create_stances_person_dir_path(
    moment_mstr_dir: str, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\stances\\person_name"""
    stances_dir = create_path(moment_mstr_dir, "stances")
    return create_path(stances_dir, person_name)


def create_stance0001_path(output_dir: str) -> str:
    """Returns path: output_dir\\stance0001.xlsx"""
    return create_path(output_dir, "stance0001.xlsx")


def create_last_run_metrics_path(world_dir: str) -> str:
    """Returns path: world_dir\\last_run_metrics.json"""
    return create_path(world_dir, "last_run_metrics.json")


def create_world_db_path(world_dir: str) -> str:
    "Returns path: moment_mstr_dir\\world.db"
    return create_path(world_dir, "world.db")
