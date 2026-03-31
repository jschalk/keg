from src.ch00_py.file_toolbox import (
    create_directory_path,
    create_path,
    get_json_filename,
)
from src.ch04_rope.rope import get_all_rope_labels, rebuild_rope
from src.ch09_person_lesson._ref.ch09_path import (
    create_moment_persons_dir_path,
    create_moments_dir_path,
)
from src.ch09_person_lesson.lasso import LassoUnit
from src.ch10_person_listen._ref.ch10_semantic_types import (
    KnotTerm,
    MomentRope,
    PersonName,
    RopeTerm,
)


def create_job_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\job\\person_name.json"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    person_dir = create_path(persons_dir, person_name)
    job_dir = create_path(person_dir, "job")
    return create_path(job_dir, f"{person_name}.json")


def treasury_filename() -> str:
    return "treasury.db"


def create_keeps_dir_path(
    moment_mstr_dir: str, moment_rope: RopeTerm, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps"""
    moment_labels = get_all_rope_labels(moment_rope)
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    moment_dir = create_path(moments_dir, moment_labels[0])
    persons_dir = create_path(moment_dir, "persons")
    person_dir = create_path(persons_dir, person_name)
    return create_path(person_dir, "keeps")


class KeepRopeMissingError(Exception):
    pass


def create_keep_rope_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\planroot\\level1_label"""
    if keep_rope is None:
        raise KeepRopeMissingError(
            f"'{person_name}' cannot save to keep_path because it does not have keep_rope."
        )

    keep_root = "planroot"
    moment_labels = get_all_rope_labels(moment_rope, knot)
    keep_rope = rebuild_rope(keep_rope, moment_labels[0], keep_root)
    x_list = get_all_rope_labels(keep_rope, knot)
    keep_sub_path = create_directory_path(x_list=[*x_list])
    keeps_dir = create_keeps_dir_path(moment_mstr_dir, moment_rope, person_name)
    return create_path(keeps_dir, keep_sub_path)


def create_keep_dutys_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\level1\\dutys"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    return create_path(x_keep_path, "dutys")


def create_keep_duty_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    duty_person: PersonName,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\level1\\dutys\\duty_person.json"""
    x_dutys_path = create_keep_dutys_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    return create_path(x_dutys_path, get_json_filename(duty_person))


def create_keep_visions_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\level1\\visions"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    return create_path(x_keep_path, "visions")


def create_keep_grades_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\level1\\grades"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    return create_path(x_keep_path, "grades")


def create_keep_grade_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    grade_person_name: PersonName,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\level1\\grades\\grade_person_name.json"""
    x_keep_path = create_keep_grades_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    return create_path(x_keep_path, get_json_filename(grade_person_name))


def create_treasury_db_path(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> str:
    "Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\keeps\\level1\\treasury.db"
    keep_path = create_keep_rope_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=person_name,
        moment_rope=moment_rope,
        keep_rope=keep_rope,
        knot=knot,
    )
    return create_path(keep_path, treasury_filename())
