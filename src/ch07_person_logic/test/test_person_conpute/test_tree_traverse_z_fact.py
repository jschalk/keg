from pytest import raises as pytest_raises
from src.ch05_reason.reason_main import factheir_shop, factunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_1case_task_1ceo_minutes_reason_1fact,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_conpute_ChangesPlanUnit_pledge_case_task():
    # ESTABLISH
    yao_person = get_personunit_1case_task_1ceo_minutes_reason_1fact()
    hr_str = "hr"
    hr_rope = yao_person.make_l1_rope(hr_str)

    # WHEN
    yao_person.add_fact(
        fact_context=hr_rope, fact_state=hr_rope, fact_lower=82, fact_upper=85
    )

    # THEN
    mail_rope = yao_person.make_l1_rope("obtain mail")
    plan_dict = yao_person.get_plan_dict()
    mail_plan = plan_dict.get(mail_rope)
    yao_person.add_fact(
        fact_context=hr_rope, fact_state=hr_rope, fact_lower=82, fact_upper=95
    )
    assert mail_plan.pledge is True
    assert mail_plan.plan_task is False

    # WHEN
    yao_person.conpute()

    # THEN
    mail_plan = yao_person.get_plan_obj(mail_rope)
    assert mail_plan.pledge
    assert mail_plan.plan_task


def test_PersonUnit_conpute_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    zia_person.set_l1_plan(planunit_shop(exx.casa))
    clean_rope = zia_person.make_rope(casa_rope, exx.clean)
    clean_begin = -3
    clean_close = 7
    clean_plan = planunit_shop(exx.clean, begin=clean_begin, close=clean_close)
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_plan = planunit_shop(exx.sweep, gogo_want=sweep_gogo_want)
    sweep_plan.stop_want = sweep_stop_want
    zia_person.set_plan_obj(clean_plan, parent_rope=casa_rope)
    zia_person.add_fact(
        fact_context=clean_rope, fact_state=clean_rope, fact_lower=1, fact_upper=5
    )
    assert zia_person.planroot.factheirs == {}

    # WHEN
    zia_person.conpute()

    # THEN
    assert zia_person.planroot.factheirs != {}
    clean_factheir = factheir_shop(clean_rope, clean_rope, 1.0, 5.0)
    assert zia_person.planroot.factheirs == {
        clean_factheir.fact_context: clean_factheir
    }


def test_PersonUnit_conpute_RaisesErrorIfNon_RangeRootHasFactUnit():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    zia_person.set_l1_plan(planunit_shop(exx.casa))
    clean_rope = zia_person.make_rope(casa_rope, exx.clean)
    clean_begin = -3
    clean_close = 7
    clean_plan = planunit_shop(exx.clean, begin=clean_begin, close=clean_close)
    sweep_rope = zia_person.make_rope(clean_rope, exx.sweep)
    sweep_plan = planunit_shop(exx.sweep, addin=2)
    zia_person.set_plan_obj(clean_plan, parent_rope=casa_rope)
    zia_person.set_plan_obj(sweep_plan, parent_rope=clean_rope)
    zia_person.add_fact(sweep_rope, sweep_rope, fact_lower=1, fact_upper=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_person.conpute()

    # THEN
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_rope}'. A ranged fact plan must have _begin, _close"
    )


def test_PersonUnit_conpute_FactHeirsInherited():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    swim_rope = zia_person.make_l1_rope(exx.swim)
    zia_person.set_l1_plan(planunit_shop(exx.swim))
    fast_str = "fast"
    slow_str = "slow"
    fast_rope = zia_person.make_rope(swim_rope, fast_str)
    slow_rope = zia_person.make_rope(swim_rope, slow_str)
    zia_person.set_plan_obj(planunit_shop(fast_str), parent_rope=swim_rope)
    zia_person.set_plan_obj(planunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_person.make_l1_rope(earth_str)
    zia_person.set_l1_plan(planunit_shop(earth_str))

    swim_plan = zia_person.get_plan_obj(swim_rope)
    fast_plan = zia_person.get_plan_obj(fast_rope)
    slow_plan = zia_person.get_plan_obj(slow_rope)
    zia_person.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    assert swim_plan.factheirs == {}
    assert fast_plan.factheirs == {}
    assert slow_plan.factheirs == {}

    # WHEN
    zia_person.conpute()

    # THEN
    assert swim_plan.factheirs != {}
    assert fast_plan.factheirs != {}
    assert slow_plan.factheirs != {}
    factheir_set_range = factheir_shop(earth_rope, earth_rope, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.fact_context: factheir_set_range}
    assert swim_plan.factheirs == factheirs_set_range
    assert fast_plan.factheirs == factheirs_set_range
    assert slow_plan.factheirs == factheirs_set_range
    print(f"{swim_plan.factheirs=}")
    assert len(swim_plan.factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_plan.factheirs.get(earth_rope)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_rope, earth_rope, None, None)
    facts_none_range = {fact_none_range.fact_context: fact_none_range}
    assert swim_plan.factheirs == facts_none_range
    assert fast_plan.factheirs == factheirs_set_range
    assert slow_plan.factheirs == factheirs_set_range

    fact_x1 = swim_plan.factheirs.get(earth_rope)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_PersonUnit_conpute_FactUnitMoldsFactHeir():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    swim_rope = zia_person.make_l1_rope(exx.swim)
    zia_person.set_l1_plan(planunit_shop(exx.swim))
    swim_plan = zia_person.get_plan_obj(swim_rope)

    fast_str = "fast"
    slow_str = "slow"
    zia_person.set_plan_obj(planunit_shop(fast_str), parent_rope=swim_rope)
    zia_person.set_plan_obj(planunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_person.make_l1_rope(earth_str)
    zia_person.set_l1_plan(planunit_shop(earth_str))

    assert swim_plan.factheirs == {}

    # WHEN
    zia_person.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    zia_person.conpute()

    # THEN
    first_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    first_earthdict = {first_earthheir.fact_context: first_earthheir}
    assert swim_plan.factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(fact_context=earth_rope, fact_state=earth_rope, reason_lower=3.0, reason_upper=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_person.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=3.0, fact_upper=5.0
    )
    zia_person.conpute()

    # THEN
    after_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=3.0, fact_upper=5.0
    )
    after_earthdict = {after_earthheir.fact_context: after_earthheir}
    assert swim_plan.factheirs == after_earthdict


def test_PersonUnit_conpute_FactHeirDeletesFactUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    swim_rope = sue_person.make_l1_rope(exx.swim)
    sue_person.set_l1_plan(planunit_shop(exx.swim))
    fast_str = "fast"
    slow_str = "slow"
    sue_person.set_plan_obj(planunit_shop(fast_str), parent_rope=swim_rope)
    sue_person.set_plan_obj(planunit_shop(slow_str), parent_rope=swim_rope)
    earth_str = "earth"
    earth_rope = sue_person.make_l1_rope(earth_str)
    sue_person.set_l1_plan(planunit_shop(earth_str))
    swim_plan = sue_person.get_plan_obj(swim_rope)
    first_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=200.0, fact_upper=500.0
    )
    first_earthdict = {first_earthheir.fact_context: first_earthheir}
    sue_person.add_fact(earth_rope, earth_rope, fact_lower=200.0, fact_upper=500.0)
    assert swim_plan.factheirs == {}

    # WHEN
    sue_person.conpute()

    # THEN
    assert swim_plan.factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_rope, earth_rope, fact_lower=3.0, fact_upper=4.0)
    swim_plan.set_factunit(factunit=earth_curb)
    sue_person.conpute()

    # THEN
    assert swim_plan.factheirs == first_earthdict
    assert swim_plan.factunits == {}


def test_PersonUnit_conpute_Setscase_taskAsComplete():
    # ESTABLISH
    yao_person = get_personunit_1case_task_1ceo_minutes_reason_1fact()
    mail_str = "obtain mail"
    assert yao_person is not None
    assert len(yao_person.planroot.kids[mail_str].reasonunits) == 1
    plan_dict = yao_person.get_plan_dict()
    mail_plan = plan_dict.get(yao_person.make_l1_rope(mail_str))
    hr_str = "hr"
    hr_rope = yao_person.make_l1_rope(hr_str)
    yao_person.add_fact(hr_rope, hr_rope, fact_lower=82, fact_upper=85)
    assert mail_plan.pledge
    assert mail_plan.plan_task

    # WHEN
    yao_person.conpute()

    # THEN
    assert mail_plan.pledge
    assert not mail_plan.plan_task
