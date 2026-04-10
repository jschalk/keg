from src.ch04_rope.rope import create_rope
from src.ch05_reason.reason_main import FactUnit, factunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import open_gut_file, save_gut_file
from src.ch14_moment.moment_main import MomentUnit, momentunit_shop
from src.ref.keywords import ExampleStrs as exx


def create_example_moment2(x_moment_mstr_dir) -> MomentUnit:
    a45_rope = create_rope("amy45")
    amy_moment = momentunit_shop(a45_rope, x_moment_mstr_dir)
    wei_str = "Wei"
    amy_moment.create_init_job_from_guts(exx.yao)
    amy_moment.create_init_job_from_guts(wei_str)
    amy_moment.create_init_job_from_guts(exx.zia)
    a45_lasso = lassounit_shop(a45_rope)
    yao_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, exx.yao)
    wei_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, wei_str)
    zia_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, exx.zia)

    yao_gut_person.set_credor_respect(101)
    wei_gut_person.set_credor_respect(75)
    zia_gut_person.set_credor_respect(52)
    yao_gut_person.set_debtor_respect(1000)
    wei_gut_person.set_debtor_respect(750)
    zia_gut_person.set_debtor_respect(500)

    yao_gut_person.add_contactunit(exx.yao, 34, 600)
    yao_gut_person.add_contactunit(exx.zia, 57, 300)
    yao_gut_person.add_contactunit(wei_str, 10, 100)
    wei_gut_person.add_contactunit(exx.yao, 37, 100)
    wei_gut_person.add_contactunit(wei_str, 11, 400)
    wei_gut_person.add_contactunit(exx.zia, 27, 250)
    zia_gut_person.add_contactunit(exx.yao, 14, 100)
    zia_gut_person.add_contactunit(exx.zia, 38, 400)
    texas_str = "Texas"
    texas_rope = yao_gut_person.make_l1_rope(texas_str)
    yao_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    wei_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    zia_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = yao_gut_person.make_rope(texas_rope, dallas_str)
    dallas_healerunit = healerunit_shop({exx.yao, exx.zia})
    dallas_plan = planunit_shop(dallas_str, healerunit=dallas_healerunit)
    elpaso_str = "el paso"
    elpaso_rope = yao_gut_person.make_rope(texas_rope, elpaso_str)
    elpaso_healerunit = healerunit_shop({exx.yao})
    elpaso_plan = planunit_shop(elpaso_str, healerunit=elpaso_healerunit)

    yao_gut_person.set_plan_obj(dallas_plan, texas_rope)
    yao_gut_person.set_plan_obj(elpaso_plan, texas_rope)
    wei_gut_person.set_plan_obj(dallas_plan, texas_rope)
    wei_gut_person.set_plan_obj(elpaso_plan, texas_rope)
    zia_gut_person.set_plan_obj(dallas_plan, texas_rope)
    zia_gut_person.set_plan_obj(elpaso_plan, texas_rope)
    save_gut_file(x_moment_mstr_dir, yao_gut_person)
    save_gut_file(x_moment_mstr_dir, wei_gut_person)
    save_gut_file(x_moment_mstr_dir, zia_gut_person)
    amy_moment._set_all_healer_dutys(exx.yao)
    amy_moment._set_all_healer_dutys(wei_str)
    amy_moment._set_all_healer_dutys(exx.zia)

    return amy_moment


def create_example_moment3(x_moment_mstr_dir) -> MomentUnit:
    # ESTABLISH
    a45_rope = create_rope("amy45")
    a45_lasso = lassounit_shop(a45_rope)
    amy_moment = momentunit_shop(a45_rope, x_moment_mstr_dir)
    wei_str = "Wei"
    amy_moment.create_init_job_from_guts(exx.yao)
    amy_moment.create_init_job_from_guts(wei_str)
    amy_moment.create_init_job_from_guts(exx.zia)
    yao_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, exx.yao)
    wei_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, wei_str)
    zia_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, exx.zia)

    casa_rope = yao_gut_person.make_l1_rope(exx.casa)
    yao_gut_person.set_l1_plan(planunit_shop(exx.casa))
    wei_gut_person.set_l1_plan(planunit_shop(exx.casa))
    zia_gut_person.set_l1_plan(planunit_shop(exx.casa))
    clean_rope = yao_gut_person.make_rope(casa_rope, exx.clean)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    yao_gut_person.set_plan_obj(planunit_shop(bath_str, pledge=True), clean_rope)
    yao_gut_person.set_plan_obj(planunit_shop(hall_str, pledge=True), clean_rope)

    wei_gut_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    wei_gut_person.set_plan_obj(planunit_shop(bath_str, pledge=True), clean_rope)

    zia_gut_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    zia_gut_person.set_plan_obj(planunit_shop(bath_str, pledge=True), clean_rope)
    zia_gut_person.set_plan_obj(planunit_shop(hall_str, pledge=True), clean_rope)

    save_gut_file(x_moment_mstr_dir, yao_gut_person)
    save_gut_file(x_moment_mstr_dir, wei_gut_person)
    save_gut_file(x_moment_mstr_dir, zia_gut_person)

    return amy_moment


def create_example_moment4(x_moment_mstr_dir) -> MomentUnit:
    # ESTABLISH
    a45_rope = create_rope("amy45")
    a45_lasso = lassounit_shop(a45_rope)
    amy_moment = momentunit_shop(a45_rope, x_moment_mstr_dir)
    wei_str = "Wei"
    amy_moment.create_init_job_from_guts(exx.yao)
    amy_moment.create_init_job_from_guts(wei_str)
    amy_moment.create_init_job_from_guts(exx.zia)
    yao_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, exx.yao)
    wei_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, wei_str)
    zia_gut_person = open_gut_file(x_moment_mstr_dir, a45_lasso, exx.zia)

    casa_rope = yao_gut_person.make_l1_rope(exx.casa)
    yao_gut_person.set_l1_plan(planunit_shop(exx.casa))
    wei_gut_person.set_l1_plan(planunit_shop(exx.casa))
    zia_gut_person.set_l1_plan(planunit_shop(exx.casa))
    clean_rope = yao_gut_person.make_rope(casa_rope, exx.clean)
    bath_str = "clean bathroom"
    hall_str = "clean hall"

    yao_gut_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    yao_gut_person.set_plan_obj(planunit_shop(bath_str, pledge=True), clean_rope)
    yao_gut_person.set_plan_obj(planunit_shop(hall_str, pledge=True), clean_rope)

    wei_gut_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    wei_gut_person.set_plan_obj(planunit_shop(bath_str, pledge=True), clean_rope)

    zia_gut_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    zia_gut_person.set_plan_obj(planunit_shop(bath_str, pledge=True), clean_rope)
    zia_gut_person.set_plan_obj(planunit_shop(hall_str, pledge=True), clean_rope)

    yao_gut_person.set_credor_respect(101)
    wei_gut_person.set_credor_respect(75)
    zia_gut_person.set_credor_respect(52)
    yao_gut_person.set_debtor_respect(1000)
    wei_gut_person.set_debtor_respect(750)
    zia_gut_person.set_debtor_respect(500)

    yao_gut_person.add_contactunit(exx.yao, 34, 600)
    yao_gut_person.add_contactunit(exx.zia, 57, 300)
    yao_gut_person.add_contactunit(wei_str, 10, 100)
    wei_gut_person.add_contactunit(exx.yao, 37, 100)
    wei_gut_person.add_contactunit(wei_str, 11, 400)
    wei_gut_person.add_contactunit(exx.zia, 27, 250)
    zia_gut_person.add_contactunit(exx.yao, 14, 100)
    zia_gut_person.add_contactunit(exx.zia, 38, 400)

    texas_str = "Texas"
    yao_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    wei_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    zia_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    save_gut_file(x_moment_mstr_dir, yao_gut_person)
    save_gut_file(x_moment_mstr_dir, wei_gut_person)
    save_gut_file(x_moment_mstr_dir, zia_gut_person)

    return amy_moment


def example_casa_floor_clean_factunit() -> FactUnit:
    casa_rope = create_rope(exx.a23, "casa")
    floor_rope = create_rope(casa_rope, "floor situation")
    clean_rope = create_rope(floor_rope, "clean")
    return factunit_shop(floor_rope, clean_rope)


def example_casa_floor_dirty_factunit() -> FactUnit:
    casa_rope = create_rope(exx.a23, "casa")
    floor_rope = create_rope(casa_rope, "floor situation")
    dirty_rope = create_rope(floor_rope, "dirty")
    return factunit_shop(floor_rope, dirty_rope)


def _example_empty_bob_personunit() -> PersonUnit:
    return personunit_shop("Bob", exx.a23)


def get_bob_mop_without_reason_personunit_example() -> PersonUnit:
    bob_person = _example_empty_bob_personunit()
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    clean_rope = bob_person.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(casa_rope, 1)
    bob_person.add_plan(floor_rope, 1)
    bob_person.add_plan(clean_rope, 1)
    bob_person.add_plan(dirty_rope, 1)
    bob_person.add_plan(mop_rope, 1, pledge=True)
    return bob_person


def get_bob_mop_with_reason_personunit_example() -> PersonUnit:
    """person_name: bob, moment_rope: amy23"""
    bob_person = get_bob_mop_without_reason_personunit_example()
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    return bob_person


def get_bob_mop_fact_clean_personunit_example() -> PersonUnit:
    bob_person = get_bob_mop_with_reason_personunit_example()
    bob_person.add_contactunit("Bob")
    casa_rope = bob_person.make_l1_rope("casa")
    floor_rope = bob_person.make_rope(casa_rope, "floor situation")
    clean_rope = bob_person.make_rope(floor_rope, "clean")
    bob_person.add_fact(floor_rope, clean_rope)
    return bob_person


def get_yao_run_with_reason_personunit_example() -> PersonUnit:
    yao_person = personunit_shop("Yao", exx.a23)
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "sking"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowng_str = "snowng"
    sport_rope = yao_person.make_l1_rope(sport_str)
    participate_rope = yao_person.make_rope(sport_rope, participate_str)
    ski_rope = yao_person.make_rope(participate_rope, ski_str)
    run_rope = yao_person.make_rope(participate_rope, run_str)
    weather_rope = yao_person.make_l1_rope(weather_str)
    rain_rope = yao_person.make_rope(weather_rope, raining_str)
    snow_rope = yao_person.make_rope(weather_rope, snowng_str)
    yao_person.add_plan(participate_rope)
    yao_person.add_plan(ski_rope, 5, pledge=True)
    yao_person.add_plan(run_rope, 1, pledge=True)
    yao_person.add_plan(weather_rope)
    yao_person.add_plan(rain_rope)
    yao_person.add_plan(snow_rope)
    yao_person.edit_plan_attr(
        ski_rope, reason_context=weather_rope, reason_case=snow_rope
    )
    yao_person.edit_plan_attr(
        run_rope, reason_context=weather_rope, reason_case=rain_rope
    )
    return yao_person


def get_yao_run_rain_fact_personunit_example() -> PersonUnit:
    yao_person = get_yao_run_with_reason_personunit_example()
    weather_rope = yao_person.make_l1_rope("weather")
    rain_rope = yao_person.make_rope(weather_rope, "raining")
    yao_person.add_fact(weather_rope, rain_rope)
    return yao_person
