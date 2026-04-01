from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from src.ch09_person_lesson.lasso import LassoUnit
from src.ch20_kpi._ref.ch20_semantic_types import PersonName


def create_day_punch_txt_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\day_punchs\\person_name.txt"""
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    moment_path = create_path(moments_dir, moment_lasso.make_path())
    day_punchs_path = create_path(moment_path, "day_punchs")
    return create_path(day_punchs_path, f"{person_name}.txt")


def create_dst_person_punch_path(
    dst_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: dst_dir\\person_name\\moment_first_label.txt"""
    person_punch_dir = create_path(dst_dir, person_name)
    return create_path(person_punch_dir, f"{moment_lasso.get_first_label()}.txt")
