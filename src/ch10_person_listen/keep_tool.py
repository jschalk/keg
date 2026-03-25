from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch00_py.dict_toolbox import get_empty_set_if_None
from src.ch00_py.file_toolbox import (
    create_path,
    get_json_filename,
    open_json,
    save_json,
    set_dir,
)
from src.ch07_person_logic.person_main import PersonUnit, get_personunit_from_dict
from src.ch09_person_lesson._ref.ch09_path import create_job_path
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    open_gut_file,
    open_person_file,
    save_person_file,
)
from src.ch10_person_listen._ref.ch10_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_keep_visions_path,
    create_treasury_db_path,
)
from src.ch10_person_listen._ref.ch10_semantic_types import (
    KnotTerm,
    MomentRope,
    PersonName,
    RopeTerm,
)


def job_file_exists(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> bool:
    job_path = create_job_path(moment_mstr_dir, moment_lasso, person_name)
    return os_path_exists(job_path)


def save_job_file(moment_mstr_dir: str, personunit: PersonUnit):
    moment_lasso = lassounit_shop(personunit.planroot.get_plan_rope(), personunit.knot)
    job_path = create_job_path(moment_mstr_dir, moment_lasso, personunit.person_name)
    save_person_file(job_path, None, personunit)


def open_job_file(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> PersonUnit:
    """moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\job\\person_name.json"""
    job_path = create_job_path(moment_mstr_dir, moment_lasso, person_name)
    return open_person_file(job_path)


def create_keep_path_dir_if_missing(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
):
    keep_path = create_keep_rope_path(
        moment_mstr_dir,
        person_name,
        moment_rope,
        keep_rope,
        knot,
    )
    set_dir(keep_path)


def treasury_db_file_exists(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> bool:
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=person_name,
        moment_rope=moment_rope,
        keep_rope=keep_rope,
        knot=knot,
    )
    return os_path_exists(treasury_db_path)


def create_treasury_db_file(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
) -> None:
    create_keep_path_dir_if_missing(
        moment_mstr_dir=moment_mstr_dir,
        person_name=person_name,
        moment_rope=moment_rope,
        keep_rope=keep_rope,
        knot=knot,
    )
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=person_name,
        moment_rope=moment_rope,
        keep_rope=keep_rope,
        knot=knot,
    )
    conn = sqlite3_connect(treasury_db_path)
    conn.close()


def save_duty_person(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    duty_person: PersonUnit,
) -> None:
    duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=person_name,
        moment_rope=moment_rope,
        keep_rope=keep_rope,
        knot=knot,
        duty_person=duty_person.person_name,
    )
    save_json(duty_path, None, duty_person.to_dict())


def get_duty_person(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    duty_person_name: PersonName,
) -> PersonUnit:
    keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=person_name,
        moment_rope=moment_rope,
        keep_rope=keep_rope,
        knot=knot,
        duty_person=duty_person_name,
    )
    if os_path_exists(keep_duty_path) is False:
        return None
    duty_person = get_personunit_from_dict(open_json(keep_duty_path))
    # duty_person.planroot.get_plan_rope() = moment_rope
    return duty_person


def save_all_gut_dutys(
    moment_mstr_dir: str,
    moment_rope: MomentRope,
    person_name: PersonName,
    keep_ropes: set[RopeTerm],
    knot: KnotTerm,
):
    moment_lasso = lassounit_shop(moment_rope)
    gut = open_gut_file(moment_mstr_dir, moment_lasso, person_name)
    for x_keep_rope in keep_ropes:
        save_duty_person(
            moment_mstr_dir=moment_mstr_dir,
            person_name=person_name,
            moment_rope=moment_rope,
            keep_rope=x_keep_rope,
            knot=knot,
            duty_person=gut,
        )


class GetKeepRopesError(Exception):
    pass


def get_keep_ropes(
    moment_mstr_dir, moment_lasso: LassoUnit, person_name
) -> set[RopeTerm]:
    x_gut_person = open_gut_file(moment_mstr_dir, moment_lasso, person_name)
    x_gut_person.conpute()
    if x_gut_person.keeps_justified is False:
        x_str = f"Cannot get_keep_ropes from '{person_name}' gut person because 'PersonUnit.keeps_justified' is False."
        raise GetKeepRopesError(x_str)
    if x_gut_person.keeps_buildable is False:
        x_str = f"Cannot get_keep_ropes from '{person_name}' gut person because 'PersonUnit.keeps_buildable' is False."
        raise GetKeepRopesError(x_str)
    person_healer_dict = x_gut_person._healers_dict.get(person_name)
    if person_healer_dict is None:
        return get_empty_set_if_None()
    keep_ropes = x_gut_person._healers_dict.get(person_name).keys()
    return get_empty_set_if_None(keep_ropes)


def get_perspective_person(
    speaker: PersonUnit, listener_name: PersonName
) -> PersonUnit:
    # get copy of person without any metrics
    perspective_person = get_personunit_from_dict(speaker.to_dict())
    perspective_person.set_person_name(listener_name)
    perspective_person.conpute()
    return perspective_person


def vision_file_exists(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    speaker_id: PersonName,
) -> bool:
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    file_path = create_path(keep_visions_path, get_json_filename(speaker_id))
    return os_path_exists(file_path)


def get_vision_person(
    moment_mstr_dir: str,
    person_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    speaker_id: PersonName,
) -> PersonUnit:
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir, person_name, moment_rope, keep_rope, knot
    )
    if (
        vision_file_exists(
            moment_mstr_dir, person_name, moment_rope, keep_rope, knot, speaker_id
        )
        is False
    ):
        return None
    person_dict = open_json(keep_visions_path, get_json_filename(speaker_id))
    return get_personunit_from_dict(person_dict)


def get_dw_perspective_person(
    moment_mstr_dir: str,
    moment_rope: MomentRope,
    speaker_id: PersonName,
    prespective_id: PersonName,
) -> PersonUnit:
    moment_lasso = lassounit_shop(moment_rope)
    speaker_job = open_job_file(moment_mstr_dir, moment_lasso, speaker_id)
    return get_perspective_person(speaker_job, prespective_id)


def rj_speaker_person(
    moment_mstr_dir: str,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    healer_name: PersonName,
    speaker_id: PersonName,
) -> PersonUnit:
    return get_vision_person(
        moment_mstr_dir=moment_mstr_dir,
        moment_rope=moment_rope,
        person_name=healer_name,
        keep_rope=keep_rope,
        knot=knot,
        speaker_id=speaker_id,
    )


def rj_perspective_person(
    moment_mstr_dir: str,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    healer_name: PersonName,
    speaker_id: PersonName,
    perspective_id: PersonName,
) -> PersonUnit:
    speaker_vision = rj_speaker_person(
        moment_mstr_dir,
        moment_rope,
        keep_rope,
        knot,
        healer_name,
        speaker_id,
    )
    return get_perspective_person(speaker_vision, perspective_id)


def save_vision_person(
    moment_mstr_dir: str,
    healer_name: PersonName,
    moment_rope: MomentRope,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    x_person: PersonUnit,
) -> None:
    x_filename = get_json_filename(x_person.person_name)
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir,
        healer_name,
        moment_rope,
        keep_rope,
        knot,
    )
    save_person_file(keep_visions_path, x_filename, x_person)
