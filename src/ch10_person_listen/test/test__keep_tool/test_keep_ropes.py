from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_graphic import display_plantree
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    lessonfilehandler_shop,
    open_gut_file,
    save_gut_file,
)
from src.ch10_person_listen._ref.ch10_path import create_keep_duty_path
from src.ch10_person_listen.keep_tool import get_keep_ropes, save_all_gut_dutys
from src.ch10_person_listen.test._util.ch10_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_keep_ropes_RaisesErrorWhen_keeps_justified_IsFalse(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue, None)
    save_gut_file(env_dir(), sue_lessonfilehandler.default_gut_person())
    sue_gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    sue_gut_person.add_partnerunit(exx.sue)
    texas_str = "Texas"
    texas_rope = sue_gut_person.make_l1_rope(texas_str)
    dallas_str = "dallas"
    dallas_rope = sue_gut_person.make_rope(texas_rope, dallas_str)
    sue_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_gut_person.set_plan_obj(planunit_shop(dallas_str), texas_rope)
    sue_gut_person.edit_plan_attr(texas_rope, healerunit=healerunit_shop({exx.sue}))
    sue_gut_person.edit_plan_attr(dallas_rope, healerunit=healerunit_shop({exx.sue}))
    sue_gut_person.conpute()
    a23_lasso = lassounit_shop(exx.a23)
    assert sue_gut_person.keeps_justified is False
    save_gut_file(env_dir(), sue_gut_person)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_keep_ropes(env_dir(), moment_lasso=a23_lasso, person_name=exx.sue)
    exception_str = f"Cannot get_keep_ropes from '{exx.sue}' gut person because 'PersonUnit.keeps_justified' is False."
    assert str(excinfo.value) == exception_str


def test_get_keep_ropes_RaisesErrorWhen_keeps_buildable_IsFalse(
    temp_dir_setup,
):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue, None)
    save_gut_file(env_dir(), sue_lessonfilehandler.default_gut_person())
    sue_gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    sue_gut_person.add_partnerunit(exx.sue)
    texas_str = "Tex/as"
    texas_rope = sue_gut_person.make_l1_rope(texas_str)
    sue_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_gut_person.edit_plan_attr(texas_rope, healerunit=healerunit_shop({exx.sue}))
    sue_gut_person.conpute()
    assert sue_gut_person.keeps_justified
    assert sue_gut_person.keeps_buildable is False
    save_gut_file(env_dir(), sue_gut_person)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_keep_ropes(env_dir(), a23_lasso, person_name=exx.sue)
    exception_str = f"Cannot get_keep_ropes from '{exx.sue}' gut person because 'PersonUnit.keeps_buildable' is False."
    assert str(excinfo.value) == exception_str


def test_get_keep_ropes_ReturnsObj(temp_dir_setup, graphics_bool):
    # ESTABLISH
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.sue, None)
    save_gut_file(env_dir(), sue_lessonfilehandler.default_gut_person())
    sue_gut_person = open_gut_file(env_dir(), a23_lasso, exx.sue)
    sue_gut_person.add_partnerunit(exx.sue)
    texas_str = "Texas"
    texas_rope = sue_gut_person.make_l1_rope(texas_str)
    sue_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    elpaso_str = "el paso"
    dallas_rope = sue_gut_person.make_rope(texas_rope, dallas_str)
    elpaso_rope = sue_gut_person.make_rope(texas_rope, elpaso_str)
    dallas_plan = planunit_shop(dallas_str, healerunit=healerunit_shop({exx.sue}))
    elpaso_plan = planunit_shop(elpaso_str, healerunit=healerunit_shop({exx.sue}))
    sue_gut_person.set_plan_obj(dallas_plan, texas_rope)
    sue_gut_person.set_plan_obj(elpaso_plan, texas_rope)
    sue_gut_person.conpute()
    display_plantree(sue_gut_person, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_person)

    # WHEN
    sue_keep_ropes = get_keep_ropes(env_dir(), a23_lasso, person_name=exx.sue)

    # THEN
    assert len(sue_keep_ropes) == 2
    assert dallas_rope in sue_keep_ropes
    assert elpaso_rope in sue_keep_ropes


def test_save_all_gut_dutys_Setsdutys(temp_dir_setup, graphics_bool):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    mstr_dir = env_dir()
    a23_lasso = lassounit_shop(exx.a23)
    sue_lessonfilehandler = lessonfilehandler_shop(mstr_dir, a23_lasso, exx.sue, None)
    save_gut_file(mstr_dir, sue_lessonfilehandler.default_gut_person())
    sue_gut_person = open_gut_file(mstr_dir, a23_lasso, exx.sue)
    sue_gut_person.add_partnerunit(exx.sue)
    sue_gut_person.add_partnerunit(exx.bob)
    texas_str = "Texas"
    texas_rope = sue_gut_person.make_l1_rope(texas_str)
    sue_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_person.make_rope(texas_rope, dallas_str)
    dallas_plan = planunit_shop(dallas_str, healerunit=healerunit_shop({exx.sue}))
    sue_gut_person.set_plan_obj(dallas_plan, texas_rope)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_person.make_rope(texas_rope, elpaso_str)
    elpaso_plan = planunit_shop(elpaso_str, healerunit=healerunit_shop({exx.sue}))
    sue_gut_person.set_plan_obj(elpaso_plan, texas_rope)
    display_plantree(sue_gut_person, mode="Keep", graphics_bool=graphics_bool)
    save_gut_file(env_dir(), sue_gut_person)
    sue_dallas_duty_path = create_keep_duty_path(
        moment_mstr_dir=mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=dallas_rope,
        knot=None,
        duty_person=exx.sue,
    )
    sue_elpaso_duty_path = create_keep_duty_path(
        moment_mstr_dir=mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=elpaso_rope,
        knot=None,
        duty_person=exx.sue,
    )
    sue_keep_ropes = get_keep_ropes(env_dir(), a23_lasso, person_name=exx.sue)
    assert os_path_exists(sue_dallas_duty_path) is False
    assert os_path_exists(sue_elpaso_duty_path) is False

    # WHEN
    save_all_gut_dutys(
        moment_mstr_dir=mstr_dir,
        moment_rope=exx.a23,
        person_name=exx.sue,
        keep_ropes=sue_keep_ropes,
        knot=sue_lessonfilehandler.moment_lasso.knot,
    )

    # THEN
    assert os_path_exists(sue_dallas_duty_path)
    assert os_path_exists(sue_elpaso_duty_path)
