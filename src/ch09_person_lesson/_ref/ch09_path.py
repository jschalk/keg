from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson._ref.ch09_semantic_types import PersonName
from src.ch09_person_lesson.lasso import LassoUnit

MOMENT_FILENAME = "moment.json"


def create_moment_dir_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    return create_path(moments_dir, moment_lasso.make_path())


def create_moment_json_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\moment.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_lasso.make_path())
    return create_path(moment_path, "moment.json")


def create_moment_persons_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_lasso.make_path())
    return create_path(moment_dir, "persons")


def create_person_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    return create_path(persons_dir, person_name)


def create_atoms_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\atoms"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    person_dir = create_path(persons_dir, person_name)
    return create_path(person_dir, "atoms")


def create_lessons_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\lessons"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    person_dir = create_path(persons_dir, person_name)
    return create_path(person_dir, "lessons")


def create_gut_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\gut\\person_name.json"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    person_dir = create_path(persons_dir, person_name)
    gut_dir = create_path(person_dir, "gut")
    return create_path(gut_dir, f"{person_name}.json")


def create_job_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\job\\person_name.json"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    person_dir = create_path(persons_dir, person_name)
    job_dir = create_path(person_dir, "job")
    return create_path(job_dir, f"{person_name}.json")
