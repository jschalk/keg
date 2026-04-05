from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_json
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.lesson_main import (
    create_lessonunit_from_files,
    lessonunit_shop,
)
from src.ch09_person_lesson.test._util.ch09_examples import (
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_LessonUnit_save_atom_file_SavesCorrectFile(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_atoms_dir = create_path(sue_person_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_lessonunit = lessonunit_shop(exx.sue, atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_planunit_sports()
    sue_lessonunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_dict = open_json(sue_atoms_dir, two_filename)
    assert two_file_dict == sports_atom.to_dict()


def test_LessonUnit_atom_file_exists_ReturnsObj(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_atoms_dir = create_path(sue_person_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_lessonunit = lessonunit_shop(exx.sue, atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert sue_lessonunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_planunit_sports()
    sue_lessonunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert sue_lessonunit.atom_file_exists(two_int)


def test_LessonUnit_open_atom_file_ReturnsObj(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_atoms_dir = create_path(sue_person_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_lessonunit = lessonunit_shop(exx.sue, atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_planunit_sports()
    sue_lessonunit._save_atom_file(two_int, sports_atom)
    assert sue_lessonunit.atom_file_exists(two_int)

    # WHEN
    file_atom = sue_lessonunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_LessonUnit_save_lesson_file_SavesCorrectFile(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_lesson_id = 2
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_lessons_dir = create_path(sue_person_dir, "lessons")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_lesson2_path = create_path(sue_lessons_dir, two_filename)
    sue_lesson6_path = create_path(sue_lessons_dir, six_filename)
    print(f"{sue_lesson2_path=}")
    print(f"{sue_lesson6_path=}")
    sue_lessonunit = lessonunit_shop(
        exx.sue, None, None, sue_lesson_id, lessons_dir=sue_lessons_dir
    )
    assert os_path_exists(sue_lesson2_path) is False
    assert os_path_exists(sue_lesson6_path) is False

    # WHEN
    sue_lessonunit._save_lesson_file()

    # THEN
    assert os_path_exists(sue_lesson2_path)
    assert os_path_exists(sue_lesson6_path) is False
    lesson_file_dict = open_json(sue_lessons_dir, two_filename)
    print(f"{lesson_file_dict=}")
    assert lesson_file_dict.get("delta_atom_numbers") == []
    assert lesson_file_dict.get(kw.person_name) == exx.sue
    assert lesson_file_dict.get(kw.spark_face) is None
    print(f"{lesson_file_dict.keys()=}")


def test_LessonUnit_lesson_file_exists_ReturnsObj(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_lessons_dir = create_path(sue_person_dir, "lessons")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_lesson2_path = create_path(sue_lessons_dir, two_filename)
    sue_lesson6_path = create_path(sue_lessons_dir, six_filename)
    print(f"{sue_lesson2_path=}")
    print(f"{sue_lesson6_path=}")
    sue_lessonunit = lessonunit_shop(exx.sue, lessons_dir=sue_lessons_dir)
    assert os_path_exists(sue_lesson2_path) is False
    assert sue_lessonunit.lesson_file_exists() is False

    # WHEN
    sue_lessonunit._save_lesson_file()

    # THEN
    assert sue_lessonunit.lesson_file_exists()


def test_LessonUnit_save_files_SavesFiles(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_atoms_dir = create_path(sue_person_dir, "atoms")
    sue_lessons_dir = create_path(sue_person_dir, "lessons")

    sue_delta_start = 4
    sue_lessonunit = lessonunit_shop(
        exx.sue, atoms_dir=sue_atoms_dir, lessons_dir=sue_lessons_dir
    )
    sue_lessonunit.set_delta_start(sue_delta_start)
    sue_lessonunit.set_face(exx.zia)
    sue_lessonunit.set_face(exx.yao)
    int4 = 4
    int5 = 5
    sports_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    sue_lessonunit.persondelta.set_personatom(sports_atom)
    sue_lessonunit.persondelta.set_personatom(knee_atom)
    assert sue_lessonunit.lesson_file_exists() is False
    assert sue_lessonunit.atom_file_exists(int4) is False
    assert sue_lessonunit.atom_file_exists(int5) is False

    # WHEN
    sue_lessonunit.save_files()

    # THEN
    assert sue_lessonunit.lesson_file_exists()
    assert sue_lessonunit.atom_file_exists(int4)
    assert sue_lessonunit.atom_file_exists(int5)


def test_LessonUnit_create_persondelta_from_atom_files_SetsAttr(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_atoms_dir = create_path(sue_person_dir, "atoms")

    sue_lessonunit = lessonunit_shop(exx.sue, atoms_dir=sue_atoms_dir)
    int4 = 4
    int5 = 5
    int9 = 9
    spor_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    ball_atom = get_atom_example_planunit_ball()
    sue_lessonunit._save_atom_file(int4, spor_atom)
    sue_lessonunit._save_atom_file(int5, knee_atom)
    sue_lessonunit._save_atom_file(int9, ball_atom)
    assert sue_lessonunit.persondelta == persondelta_shop()

    # WHEN
    atoms_list = [int4, int5, int9]
    sue_lessonunit._create_persondelta_from_atom_files(atoms_list)

    # THEN
    static_persondelta = persondelta_shop()
    static_persondelta.set_personatom(spor_atom)
    static_persondelta.set_personatom(knee_atom)
    static_persondelta.set_personatom(ball_atom)
    assert sue_lessonunit.persondelta != persondelta_shop()
    assert sue_lessonunit.persondelta == static_persondelta


def test_create_lessonunit_from_files_ReturnsObj(temp3_fs):
    # ESTABLISH
    x_moment_dir = create_path(str(temp3_fs), exx.a23)
    x_persons_dir = create_path(x_moment_dir, "persons")
    sue_person_dir = create_path(x_persons_dir, exx.sue)
    sue_atoms_dir = create_path(sue_person_dir, "atoms")
    sue_lessons_dir = create_path(sue_person_dir, "lessons")

    sue_delta_start = 4
    src_sue_lessonunit = lessonunit_shop(
        exx.sue, atoms_dir=sue_atoms_dir, lessons_dir=sue_lessons_dir
    )
    src_sue_lessonunit.set_delta_start(sue_delta_start)
    src_sue_lessonunit.set_face(exx.yao)
    sports_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    ball_atom = get_atom_example_planunit_ball()
    src_sue_lessonunit.persondelta.set_personatom(sports_atom)
    src_sue_lessonunit.persondelta.set_personatom(knee_atom)
    src_sue_lessonunit.persondelta.set_personatom(ball_atom)
    src_sue_lessonunit.save_files()

    # WHEN
    new_sue_lessonunit = create_lessonunit_from_files(
        lessons_dir=sue_lessons_dir,
        lesson_id=src_sue_lessonunit.lesson_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_lessonunit.person_name == new_sue_lessonunit.person_name
    assert src_sue_lessonunit.spark_face == new_sue_lessonunit.spark_face
    assert src_sue_lessonunit.persondelta == new_sue_lessonunit.persondelta
