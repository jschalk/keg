from pytest import raises as pytest_raises
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_conpute_Sets_keeps_justified_WhenPersonUnit_Empty():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified


def test_PersonUnit_conpute_Sets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified


def test_PersonUnit_conpute_Sets_keeps_justified_WhenSinglePlanUnit_healerunit_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.set_l1_plan(
        planunit_shop("Texas", healerunit=healerunit_shop({exx.yao}))
    )
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified is False


def test_PersonUnit_conpute_Sets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    yao_healerunit = healerunit_shop({exx.yao})
    sue_person.set_l1_plan(
        planunit_shop("Texas", healerunit=yao_healerunit, problem_bool=True)
    )
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified


def test_PersonUnit_conpute_Sets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    yao_healerunit = healerunit_shop({exx.yao})

    texas_str = "Texas"
    texas_rope = sue_person.make_l1_rope(texas_str)
    sue_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_person.set_plan_obj(
        planunit_shop(ep_str, healerunit=yao_healerunit), texas_rope
    )
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified


def test_PersonUnit_conpute_Sets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_person.make_l1_rope(texas_str)
    yao_healerunit = healerunit_shop({exx.yao})
    sue_person.set_l1_plan(planunit_shop(texas_str, healerunit=yao_healerunit))
    sue_person.set_plan_obj(planunit_shop("El Paso", problem_bool=True), texas_rope)
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified is False


def test_PersonUnit_conpute_RaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_person.make_l1_rope(texas_str)
    yao_healerunit = healerunit_shop({exx.yao})
    texas_plan = planunit_shop(texas_str, healerunit=yao_healerunit)
    sue_person.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", problem_bool=True)
    sue_person.set_plan_obj(elpaso_plan, texas_rope)
    assert sue_person.keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_person.conpute(keep_exceptions=True)

    # THEN
    assert (
        str(excinfo.value)
        == f"PlanUnit '{elpaso_plan.get_plan_rope()}' cannot sponsor ancestor keeps."
    )


def test_PersonUnit_conpute_Sets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    yao_healerunit = healerunit_shop({exx.yao})
    texas_str = "Texas"
    texas_rope = sue_person.make_l1_rope(texas_str)
    texas_plan = planunit_shop(texas_str, healerunit=yao_healerunit, problem_bool=True)
    sue_person.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", healerunit=yao_healerunit, problem_bool=True)
    sue_person.set_plan_obj(elpaso_plan, texas_rope)
    assert sue_person.keeps_justified is False

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.keeps_justified is False


def test_PersonUnit_get_plan_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    yao_healerunit = healerunit_shop({exx.yao})
    texas_str = "Texas"
    texas_rope = sue_person.make_l1_rope(texas_str)
    texas_plan = planunit_shop(texas_str, healerunit=yao_healerunit, problem_bool=True)
    sue_person.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", healerunit=yao_healerunit, problem_bool=True)
    sue_person.set_plan_obj(elpaso_plan, texas_rope)
    sue_person.conpute()
    assert sue_person.keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because keeps_justified={sue_person.keeps_justified}."
    )
