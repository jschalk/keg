from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, delete_dir
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    create_gut_path,
    gut_file_exists,
    lessonfilehandler_shop,
    open_gut_file,
    save_gut_file,
)
from src.ch09_person_lesson.lesson_main import init_lesson_id
from src.ch09_person_lesson.test._util.ch09_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ch09_person_lesson.test._util.ch09_examples import sue_2personatoms_lessonunit
from src.ref.keywords import ExampleStrs as exx


def test_LessonFileHandler_default_gut_person_ReturnsObj():
    # ESTABLISH
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(),
        lassounit_shop(exx.a23_slash, knot=exx.slash),
        exx.sue,
        fund_pool=x_fund_pool,
        fund_grain=pnine_float,
        respect_grain=pnine_float,
        mana_grain=pfour_float,
    )

    # WHEN
    sue_default_gut = sue_lessonfilehandler.default_gut_person()

    # THEN
    assert (
        sue_default_gut.planroot.get_plan_rope()
        == sue_lessonfilehandler.moment_lasso.moment_rope
    )
    assert sue_default_gut.person_name == sue_lessonfilehandler.person_name
    assert sue_default_gut.knot == sue_lessonfilehandler.moment_lasso.knot
    assert sue_default_gut.fund_pool == sue_lessonfilehandler.fund_pool
    assert sue_default_gut.fund_grain == sue_lessonfilehandler.fund_grain
    assert sue_default_gut.respect_grain == sue_lessonfilehandler.respect_grain
    assert sue_default_gut.mana_grain == sue_lessonfilehandler.mana_grain
    assert sue_default_gut.last_lesson_id == init_lesson_id()


def test_LessonFileHandler_create_initial_lesson_files_from_default_SavesLessonUnitFiles(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue)
    init_lesson_filename = sue_lessonfilehandler.lesson_filename(init_lesson_id())
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, init_lesson_filename
    )
    assert os_path_exists(init_lesson_file_path) is False
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False

    # WHEN
    sue_lessonfilehandler._create_initial_lesson_files_from_default()

    # THEN
    assert os_path_exists(init_lesson_file_path)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False


def test_LessonFileHandler_create_gut_from_lessons_CreatesgutFileFromLessonFiles(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue)
    init_lesson_filename = sue_lessonfilehandler.lesson_filename(init_lesson_id())
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, init_lesson_filename
    )
    sue_lessonfilehandler._create_initial_lesson_files_from_default()
    assert os_path_exists(init_lesson_file_path)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False

    # WHEN
    sue_lessonfilehandler._create_gut_from_lessons()

    # THEN
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue)
    static_sue_gut = sue_lessonfilehandler._merge_any_lessons(
        sue_lessonfilehandler.default_gut_person()
    )
    gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    assert gut_person.to_dict() == static_sue_gut.to_dict()


def test_LessonFileHandler_create_initial_lesson_and_gut_files_CreatesLessonFilesAndgutFile(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue)
    init_lesson_filename = sue_lessonfilehandler.lesson_filename(init_lesson_id())
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, init_lesson_filename
    )
    assert os_path_exists(init_lesson_file_path) is False
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False

    # WHEN
    sue_lessonfilehandler._create_initial_lesson_and_gut_files()

    # THEN
    assert os_path_exists(init_lesson_file_path)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue)
    static_sue_gut = sue_lessonfilehandler._merge_any_lessons(
        sue_lessonfilehandler.default_gut_person()
    )
    gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    assert gut_person.to_dict() == static_sue_gut.to_dict()


def test_LessonFileHandler_create_initial_lesson_files_from_gut_SavesOnlyLessonFiles(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue)
    sue_gut_person = sue_lessonfilehandler.default_gut_person()
    sue_gut_person.add_partnerunit(exx.bob)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False
    save_gut_file(env_dir(), sue_gut_person)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue)
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, f"{init_lesson_id()}.json"
    )
    assert os_path_exists(init_lesson_file_path) is False

    # WHEN
    sue_lessonfilehandler._create_initial_lesson_files_from_gut()

    # THEN
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_initialize_lesson_gut_files_SavesgutFileAndLessonFile(
    temp_dir_setup,
):
    # ESTABLISH
    seven_int = 25
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(), a23_lasso, exx.sue, respect_grain=seven_int
    )
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, f"{init_lesson_id()}.json"
    )
    delete_dir(sue_lessonfilehandler.lessons_dir)
    assert os_path_exists(init_lesson_file_path) is False

    # WHEN
    sue_lessonfilehandler.initialize_lesson_gut_files()

    # THEN
    gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    assert gut_person.planroot.get_plan_rope() == exx.a23
    assert gut_person.person_name == exx.sue
    assert gut_person.respect_grain == seven_int
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_initialize_lesson_gut_files_SavesOnlygutFile(
    temp_dir_setup,
):
    # ESTABLISH
    seven_int = 25
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(), a23_lasso, exx.sue, respect_grain=seven_int
    )
    sue_lessonfilehandler.initialize_lesson_gut_files()
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue)
    gut_path = create_gut_path(env_dir(), a23_lasso, exx.sue)
    delete_dir(gut_path)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue) is False
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, f"{init_lesson_id()}.json"
    )
    assert os_path_exists(init_lesson_file_path)

    # WHEN
    sue_lessonfilehandler.initialize_lesson_gut_files()

    # THEN
    gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    assert gut_person.planroot.get_plan_rope() == exx.a23
    assert gut_person.person_name == exx.sue
    assert gut_person.respect_grain == seven_int
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_initialize_lesson_gut_files_SavesOnlyLessonFile(
    temp_dir_setup,
):
    # ESTABLISH
    seven_int = 25
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(), a23_lasso, exx.sue, respect_grain=seven_int
    )
    sue_lessonfilehandler.initialize_lesson_gut_files()
    sue_gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    sue_gut_person.add_partnerunit(exx.bob)
    save_gut_file(env_dir(), sue_gut_person)
    assert gut_file_exists(env_dir(), a23_lasso, exx.sue)
    init_lesson_file_path = create_path(
        sue_lessonfilehandler.lessons_dir, f"{init_lesson_id()}.json"
    )
    delete_dir(sue_lessonfilehandler.lessons_dir)
    assert os_path_exists(init_lesson_file_path) is False

    # WHEN
    sue_lessonfilehandler.initialize_lesson_gut_files()

    # THEN
    assert sue_gut_person.planroot.get_plan_rope() == exx.a23
    assert sue_gut_person.person_name == exx.sue
    assert sue_gut_person.respect_grain == seven_int
    assert sue_gut_person.partner_exists(exx.bob)
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_append_lessons_to_gut_file_AddsLessonsTogutFile(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue)
    sue_lessonfilehandler.initialize_lesson_gut_files()
    sue_lessonfilehandler.save_lesson_file(sue_2personatoms_lessonunit())
    gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    # gut_person.add_plan(gut_person.make_l1_rope("sports"))
    sports_str = "sports"
    sports_rope = gut_person.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_person.make_rope(sports_rope, knee_str)
    assert gut_person.plan_exists(sports_rope) is False
    assert gut_person.plan_exists(knee_rope) is False

    # WHEN
    new_person = sue_lessonfilehandler.append_lessons_to_gut_file()

    # THEN
    assert new_person != gut_person
    assert new_person.plan_exists(sports_rope)
    assert new_person.plan_exists(knee_rope)
