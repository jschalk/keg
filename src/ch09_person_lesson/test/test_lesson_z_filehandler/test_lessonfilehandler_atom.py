from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, get_dir_file_strs
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import lessonfilehandler_shop
from src.ch09_person_lesson.test._util.ch09_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ch09_person_lesson.test._util.ch09_examples import (
    get_atom_example_factunit_knee,
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
    get_ch09_example_moment_lasso as moment_lasso,
)
from src.ref.keywords import ExampleStrs as exx


def test_LessonFileHandler_atom_filename_ReturnsObj():
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    one_int = 1

    # WHEN
    one_atom_filename = yao_lessonfilehandler.atom_filename(one_int)

    # THEN
    assert one_atom_filename == f"{one_int}.json"


def test_LessonFileHandler_atom_file_path_ReturnsObj():
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    one_int = 1

    # WHEN
    one_atom_file_path = yao_lessonfilehandler.atom_file_path(one_int)

    # THEN
    one_atom_filename = yao_lessonfilehandler.atom_filename(one_int)
    expected_path = create_path(yao_lessonfilehandler.atoms_dir, one_atom_filename)
    assert one_atom_file_path == expected_path


def test_LessonFileHandler_save_valid_atom_file_SavesFile(temp_dir_setup):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    one_int = 1
    assert os_path_exists(yao_lessonfilehandler.atom_file_path(one_int)) is False

    # WHEN
    knee_atom = get_atom_example_factunit_knee()
    atom_num = yao_lessonfilehandler._save_valid_atom_file(knee_atom, one_int)

    # THEN
    assert os_path_exists(yao_lessonfilehandler.atom_file_path(one_int))
    assert atom_num == one_int


def test_LessonFileHandler_atom_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    four_int = 4
    assert os_path_exists(yao_lessonfilehandler.atom_file_path(four_int)) is False
    assert yao_lessonfilehandler.h_atom_file_exists(four_int) is False

    # WHEN
    yao_lessonfilehandler._save_valid_atom_file(
        get_atom_example_factunit_knee(), four_int
    )

    # THEN
    assert os_path_exists(yao_lessonfilehandler.atom_file_path(four_int))
    assert yao_lessonfilehandler.h_atom_file_exists(four_int)


def test_LessonFileHandler_delete_atom_file_DeletesFile(temp_dir_setup):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    ten_int = 10
    yao_lessonfilehandler._save_valid_atom_file(
        get_atom_example_factunit_knee(), ten_int
    )
    assert yao_lessonfilehandler.h_atom_file_exists(ten_int)

    # WHEN
    yao_lessonfilehandler.delete_atom_file(ten_int)

    # THEN
    assert yao_lessonfilehandler.h_atom_file_exists(ten_int) is False


def test_LessonFileHandler_get_max_atom_file_number_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    ten_int = 10
    yao_lessonfilehandler._save_valid_atom_file(
        get_atom_example_factunit_knee(), ten_int
    )
    assert yao_lessonfilehandler.h_atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_lessonfilehandler.get_max_atom_file_number() == ten_int


def test_LessonFileHandler_get_max_atom_file_number_ReturnsObjWhenDirIsEmpty(
    temp_dir_setup,
):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)

    # WHEN / THEN
    assert yao_lessonfilehandler.get_max_atom_file_number() is None


def test_LessonFileHandler_get_next_atom_file_number_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    # WHEN / THEN
    assert yao_lessonfilehandler._get_next_atom_file_number() == 0

    ten_int = 10
    yao_lessonfilehandler._save_valid_atom_file(
        get_atom_example_factunit_knee(), ten_int
    )
    assert yao_lessonfilehandler.h_atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_lessonfilehandler._get_next_atom_file_number() == 11


def test_LessonFileHandler_save_atom_file_SavesFile(temp_dir_setup):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)
    ten_int = 10
    yao_lessonfilehandler._save_valid_atom_file(
        get_atom_example_factunit_knee(), ten_int
    )
    assert yao_lessonfilehandler.get_max_atom_file_number() == ten_int
    eleven_int = ten_int + 1
    assert yao_lessonfilehandler.h_atom_file_exists(eleven_int) is False

    # WHEN
    atom_num1 = yao_lessonfilehandler.save_atom_file(get_atom_example_factunit_knee())

    # THEN
    assert yao_lessonfilehandler.get_max_atom_file_number() != ten_int
    assert yao_lessonfilehandler.get_max_atom_file_number() == eleven_int
    assert yao_lessonfilehandler.h_atom_file_exists(eleven_int)
    assert atom_num1 == eleven_int
    atom_num2 = yao_lessonfilehandler.save_atom_file(get_atom_example_factunit_knee())
    assert atom_num2 == 12


def test_LessonFileHandler_get_person_from_atom_files_ReturnsFileWithZeroAtoms(
    temp_dir_setup,
):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)

    # WHEN
    yao_person = yao_lessonfilehandler._get_person_from_atom_files()

    # THEN
    assert yao_person.person_name == exx.yao
    assert (
        yao_person.planroot.get_plan_rope()
        == yao_lessonfilehandler.moment_lasso.moment_rope
    )
    assert yao_person.knot == yao_lessonfilehandler.moment_lasso.knot
    assert yao_person.fund_pool == yao_lessonfilehandler.fund_pool
    assert yao_person.fund_grain == yao_lessonfilehandler.fund_grain
    assert yao_person.respect_grain == yao_lessonfilehandler.respect_grain


def test_LessonFileHandler_get_person_from_atom_files_ReturnsFile_SimplePlan(
    temp_dir_setup,
):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)

    # save atom files
    sports_atom = get_atom_example_planunit_sports(
        yao_lessonfilehandler.moment_lasso.moment_rope
    )
    yao_lessonfilehandler.save_atom_file(sports_atom)

    # WHEN
    yao_person = yao_lessonfilehandler._get_person_from_atom_files()

    # THEN
    assert yao_person.person_name == exx.yao
    assert (
        yao_person.planroot.get_plan_rope()
        == yao_lessonfilehandler.moment_lasso.moment_rope
    )
    assert yao_person.knot == yao_lessonfilehandler.moment_lasso.knot
    sports_str = "sports"
    sports_rope = yao_person.make_l1_rope(sports_str)

    assert yao_person.plan_exists(sports_rope)


def test_LessonFileHandler_get_person_from_atom_files_ReturnsFile_WithFactUnit(
    temp_dir_setup,
):
    # ESTABLISH
    yao_lessonfilehandler = lessonfilehandler_shop(env_dir(), moment_lasso(), exx.yao)

    # save atom files
    x_moment_rope = yao_lessonfilehandler.moment_lasso.moment_rope
    yao_lessonfilehandler.save_atom_file(
        get_atom_example_planunit_sports(x_moment_rope)
    )
    yao_lessonfilehandler.save_atom_file(get_atom_example_planunit_ball(x_moment_rope))
    yao_lessonfilehandler.save_atom_file(get_atom_example_planunit_knee(x_moment_rope))
    yao_lessonfilehandler.save_atom_file(get_atom_example_factunit_knee(x_moment_rope))
    print(f"{get_dir_file_strs(yao_lessonfilehandler.atoms_dir).keys()=}")

    # WHEN
    yao_person = yao_lessonfilehandler._get_person_from_atom_files()

    # THEN
    assert yao_person.person_name == exx.yao
    assert (
        yao_person.planroot.get_plan_rope()
        == yao_lessonfilehandler.moment_lasso.moment_rope
    )
    assert yao_person.knot == yao_lessonfilehandler.moment_lasso.knot
    sports_str = "sports"
    sports_rope = yao_person.make_l1_rope(sports_str)

    assert yao_person.plan_exists(sports_rope)
