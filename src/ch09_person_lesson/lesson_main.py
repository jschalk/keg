from dataclasses import dataclass
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import (
    create_path,
    get_json_filename,
    open_json,
    save_json,
)
from src.ch07_person_logic.person_main import PersonUnit, get_default_rope
from src.ch08_person_atom.atom_main import PersonAtom, get_personatom_from_dict
from src.ch09_person_lesson._ref.ch09_semantic_types import (
    FaceName,
    MomentRope,
    PersonName,
)
from src.ch09_person_lesson.delta import (
    PersonDelta,
    get_persondelta_from_ordered_dict,
    persondelta_shop,
)


class LessonPersonConflictError(Exception):
    pass


def init_lesson_id() -> int:
    return 0


def get_init_lesson_id_if_None(x_lesson_id: int = None) -> int:
    return init_lesson_id() if x_lesson_id is None else x_lesson_id


@dataclass
class LessonUnit:
    spark_face: FaceName = None
    moment_rope: MomentRope = None
    person_name: PersonName = None
    lessons_dir: str = None
    atoms_dir: str = None
    spark_num: int = None
    # calculated fields (not confident)
    lesson_id: int = None
    persondelta: PersonDelta = None
    delta_start: int = None
    """Represents a per moment_rope/spark_num PersonDelta for a person_name"""

    def set_face(self, x_spark_face: FaceName):
        self.spark_face = x_spark_face

    def del_face(self):
        self.spark_face = None

    def set_persondelta(self, x_persondelta: PersonDelta):
        self.persondelta = x_persondelta

    def del_persondelta(self):
        self.persondelta = persondelta_shop()

    def set_delta_start(self, x_delta_start: int):
        self.delta_start = get_init_lesson_id_if_None(x_delta_start)

    def personatom_exists(self, x_personatom: PersonAtom):
        return self.persondelta.c_personatom_exists(x_personatom)

    def get_step_dict(self) -> dict[str, any]:
        return {
            "spark_face": self.spark_face,
            "moment_rope": self.moment_rope,
            "person_name": self.person_name,
            "spark_num": self.spark_num,
            "delta": self.persondelta.get_ordered_personatoms(self.delta_start),
        }

    def get_serializable_step_dict(self) -> dict[str, dict]:
        total_dict = self.get_step_dict()
        total_dict["delta"] = self.persondelta.get_ordered_dict()
        return total_dict

    def get_delta_atom_numbers(self, lessonunit_dict: list[str]) -> int:
        delta_dict = lessonunit_dict.get("delta")
        return list(delta_dict.keys())

    def get_deltametric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "person_name": x_dict.get("person_name"),
            "spark_face": x_dict.get("spark_face"),
            "spark_num": x_dict.get("spark_num"),
            "delta_atom_numbers": self.get_delta_atom_numbers(x_dict),
        }

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: PersonAtom):
        x_filename = self._get_num_filename(atom_number)
        save_json(self.atoms_dir, x_filename, x_atom.to_dict())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(create_path(self.atoms_dir, x_filename))

    def _open_atom_file(self, atom_number: int) -> PersonAtom:
        x_dict = open_json(self.atoms_dir, self._get_num_filename(atom_number))
        return get_personatom_from_dict(x_dict)

    def _save_lesson_file(self):
        x_filename = self._get_num_filename(self.lesson_id)
        save_json(self.lessons_dir, x_filename, self.get_deltametric_dict())

    def lesson_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self.lesson_id)
        return os_path_exists(create_path(self.lessons_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_personatoms = step_dict.get("delta")
        for order_int, personatom in ordered_personatoms.items():
            self._save_atom_file(order_int, personatom)

    def save_files(self):
        self._save_lesson_file()
        self._save_atom_files()

    def _create_persondelta_from_atom_files(
        self, atom_number_list: list
    ) -> PersonDelta:
        x_persondelta = persondelta_shop()
        for atom_number in atom_number_list:
            x_personatom = self._open_atom_file(atom_number)
            x_persondelta.set_personatom(x_personatom)
        self.persondelta = x_persondelta

    def add_p_personatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        self.persondelta.add_personatom(dimen, crud_str, jkeys=jkeys, jvalues=jvalues)

    def get_lesson_edited_person(self, before_person: PersonUnit) -> PersonUnit:
        if (
            self.moment_rope != before_person.planroot.get_plan_rope()
            or self.person_name != before_person.person_name
        ):
            raise LessonPersonConflictError(
                f"lesson person conflict {self.moment_rope} != {before_person.planroot.get_plan_rope()} or {self.person_name} != {before_person.person_name}"
            )
        return self.persondelta.get_atom_edited_person(before_person)

    def is_empty(self) -> bool:
        return self.persondelta.atoms_empty()


def lessonunit_shop(
    person_name: PersonName,
    spark_face: FaceName = None,
    moment_rope: MomentRope = None,
    lesson_id: int = None,
    persondelta: PersonDelta = None,
    delta_start: int = None,
    lessons_dir: str = None,
    atoms_dir: str = None,
    spark_num: int = None,
) -> LessonUnit:
    persondelta = persondelta_shop() if persondelta is None else persondelta
    moment_rope = get_default_rope() if moment_rope is None else moment_rope
    x_lessonunit = LessonUnit(
        spark_face=spark_face,
        person_name=person_name,
        moment_rope=moment_rope,
        lesson_id=get_init_lesson_id_if_None(lesson_id),
        persondelta=persondelta,
        lessons_dir=lessons_dir,
        atoms_dir=atoms_dir,
        spark_num=spark_num,
    )
    x_lessonunit.set_delta_start(delta_start)
    return x_lessonunit


def create_lessonunit_from_files(
    lessons_dir: str,
    lesson_id: str,
    atoms_dir: str,
) -> LessonUnit:
    lesson_filename = get_json_filename(lesson_id)
    lesson_dict = open_json(lessons_dir, lesson_filename)
    x_person_name = lesson_dict.get("person_name")
    x_moment_rope = lesson_dict.get("moment_rope")
    x_spark_face = lesson_dict.get("spark_face")
    delta_atom_numbers_list = lesson_dict.get("delta_atom_numbers")
    x_lessonunit = lessonunit_shop(
        spark_face=x_spark_face,
        person_name=x_person_name,
        moment_rope=x_moment_rope,
        lesson_id=lesson_id,
        atoms_dir=atoms_dir,
    )
    x_lessonunit._create_persondelta_from_atom_files(delta_atom_numbers_list)
    return x_lessonunit


def get_lessonunit_from_dict(lesson_dict: dict) -> LessonUnit:
    if lesson_dict.get("spark_num") is None:
        x_spark_num = None
    else:
        x_spark_num = int(lesson_dict.get("spark_num"))
    x_lessonunit = lessonunit_shop(
        spark_face=lesson_dict.get("spark_face"),
        person_name=lesson_dict.get("person_name"),
        moment_rope=lesson_dict.get("moment_rope"),
        lesson_id=lesson_dict.get("lesson_id"),
        atoms_dir=lesson_dict.get("atoms_dir"),
        spark_num=x_spark_num,
    )
    x_persondelta = get_persondelta_from_ordered_dict(lesson_dict.get("delta"))
    x_lessonunit.set_persondelta(x_persondelta)
    return x_lessonunit
