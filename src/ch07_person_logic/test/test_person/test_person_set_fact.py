from ch05_reason.reason_main import factunit_shop
from ch06_plan.plan import planunit_shop
from ch07_person_logic.person_main import personunit_shop
from ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from pytest import raises as pytest_raises
from ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_fact_ModifiesAttr_1():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sem_jour_rope = sue_person.make_l1_rope("sem_jours")
    sun_rope = sue_person.make_rope(sem_jour_rope, "Sun")
    sun_person_fact = factunit_shop(fact_context=sem_jour_rope, fact_state=sun_rope)
    print(sun_person_fact)
    x_planroot = sue_person.planroot
    x_planroot.factunits = {sun_person_fact.fact_context: sun_person_fact}
    assert x_planroot.factunits is not None
    x_planroot.factunits = {}
    assert not x_planroot.factunits

    # ESTABLISH
    sue_person.add_fact(fact_context=sem_jour_rope, fact_state=sun_rope)

    # THEN
    assert x_planroot.factunits == {sun_person_fact.fact_context: sun_person_fact}

    # ESTABLISH
    x_planroot.factunits = {}
    assert not x_planroot.factunits
    usa_wk_rope = sue_person.make_l1_rope("nation")
    usa_wk_fact = factunit_shop(
        usa_wk_rope, usa_wk_rope, fact_lower=608, fact_upper=610
    )
    x_planroot.factunits = {usa_wk_fact.fact_context: usa_wk_fact}

    x_planroot.factunits = {}
    assert not x_planroot.factunits

    # WHEN
    sue_person.add_fact(
        fact_context=usa_wk_rope, fact_state=usa_wk_rope, fact_lower=608, fact_upper=610
    )

    # THEN
    assert x_planroot.factunits is not None
    assert x_planroot.factunits == {usa_wk_fact.fact_context: usa_wk_fact}


def test_PersonUnit_set_fact_ModifiesAttr_2():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sem_jour_rope = sue_person.make_l1_rope("sem_jours")
    sun_rope = sue_person.make_rope(sem_jour_rope, "Sun")

    # WHEN
    sue_person.add_fact(fact_context=sem_jour_rope, fact_state=sun_rope)

    # THEN
    sun_person_fact = factunit_shop(fact_context=sem_jour_rope, fact_state=sun_rope)
    x_planroot = sue_person.planroot
    assert x_planroot.factunits == {sun_person_fact.fact_context: sun_person_fact}


def test_PersonUnit_set_fact_ModifiesAttrWhen_fact_state_IsNone():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sem_jour_rope = sue_person.make_l1_rope("sem_jours")

    # WHEN
    sue_person.add_fact(fact_context=sem_jour_rope, fact_lower=5, fact_upper=7)

    # THEN
    sun_person_fact = factunit_shop(sem_jour_rope, sem_jour_rope, 5, 7)
    x_planroot = sue_person.planroot
    assert x_planroot.factunits == {sun_person_fact.fact_context: sun_person_fact}


def test_PersonUnit_set_fact_ModifiesAttrWhen_reason_lower_IsNone():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sem_jour_rope = sue_person.make_l1_rope("sem_jours")
    sue_person.add_fact(fact_context=sem_jour_rope, fact_lower=5, fact_upper=7)
    x_planroot = sue_person.planroot
    x7_factunit = factunit_shop(sem_jour_rope, sem_jour_rope, 5, 7)
    assert x_planroot.factunits.get(sem_jour_rope) == x7_factunit

    # WHEN
    sue_person.add_fact(fact_context=sem_jour_rope, fact_upper=10)

    # THEN
    x10_factunit = factunit_shop(sem_jour_rope, sem_jour_rope, 5, 10)
    assert x_planroot.factunits.get(sem_jour_rope) == x10_factunit


def test_PersonUnit_set_fact_FailsToCreateWhenreason_contextAndFactAreDifferenctAndFactPlanIsNot_RangeRoot():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    ziet_str = "ziet"
    ziet_plan = planunit_shop(ziet_str, begin=0, close=140)
    bob_person.set_l1_plan(ziet_plan)
    ziet_rope = bob_person.make_l1_rope(ziet_str)
    a1st = "age1st"
    a1st_rope = bob_person.make_rope(ziet_rope, a1st)
    a1st_plan = planunit_shop(a1st, begin=0, close=20)
    bob_person.set_plan_obj(a1st_plan, parent_rope=ziet_rope)
    a1e1st_str = "a1_era1st"
    a1e1st_plan = planunit_shop(a1e1st_str, begin=20, close=30)
    bob_person.set_plan_obj(a1e1st_plan, parent_rope=a1st_rope)
    a1e1_rope = bob_person.make_rope(a1st_rope, a1e1st_str)
    assert bob_person.planroot.factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_person.add_fact(
            fact_context=a1e1_rope, fact_state=a1e1_rope, fact_lower=20, fact_upper=23
        )
    x_str = f"Non rangeroot fact:{a1e1_rope} can only be set by rangeroot fact"
    assert str(excinfo.value) == x_str


def test_PersonUnit_del_fact_ModifiesAttr():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sem_jour_rope = sue_person.make_l1_rope("sem_jours")
    sun_rope = sue_person.make_rope(sem_jour_rope, "Sun")
    sue_person.add_fact(fact_context=sem_jour_rope, fact_state=sun_rope)
    sun_person_fact = factunit_shop(fact_context=sem_jour_rope, fact_state=sun_rope)
    x_planroot = sue_person.planroot
    assert x_planroot.factunits == {sun_person_fact.fact_context: sun_person_fact}

    # WHEN
    sue_person.del_fact(fact_context=sem_jour_rope)

    # THEN
    assert x_planroot.factunits == {}


def test_PersonUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    situations_str = "situations"
    situations_rope = sue_person.make_l1_rope(situations_str)
    climate_str = "climate"
    climate_rope = sue_person.make_rope(situations_rope, climate_str)
    sue_person.add_fact(situations_rope, climate_rope, create_missing_plans=True)

    # WHEN
    generated_situations_reason_context = sue_person.get_fact(situations_rope)

    # THEN
    static_situations_reason_context = sue_person.planroot.factunits.get(
        situations_rope
    )
    assert generated_situations_reason_context == static_situations_reason_context


def test_PersonUnit_get_rangeroot_factunits_ReturnsObj_Scenario0():
    # ESTABLISH a single ranged fact
    sue_person = personunit_shop("Sue")
    ziet_str = "ziet"
    ziet_plan = planunit_shop(ziet_str, begin=0, close=140)
    sue_person.set_l1_plan(ziet_plan)

    clean_plan = planunit_shop(exx.clean, pledge=True)
    sue_person.set_l1_plan(clean_plan)
    c_rope = sue_person.make_l1_rope(exx.clean)
    ziet_rope = sue_person.make_l1_rope(ziet_str)
    # sue_person.edit_plan_attr(c_rope, reason_context=ziet_rope, reason_case=ziet_rope, reason_lower=5, reason_upper=10)

    sue_person.add_fact(
        fact_context=ziet_rope, fact_state=ziet_rope, fact_lower=5, fact_upper=10
    )
    print(f"Establish a single ranged fact {sue_person.planroot.factunits=}")
    assert len(sue_person.planroot.factunits) == 1

    # WHEN / THEN
    assert len(sue_person._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_str = "place_x"
    place_plan = planunit_shop(place_str, begin=600, close=800)
    sue_person.set_l1_plan(place_plan)
    place_rope = sue_person.make_l1_rope(place_str)
    sue_person.add_fact(
        fact_context=place_rope, fact_state=place_rope, fact_lower=5, fact_upper=10
    )
    print(f"When one ranged fact added {sue_person.planroot.factunits=}")
    assert len(sue_person.planroot.factunits) == 2

    # THEN
    assert len(sue_person._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_person.set_l1_plan(planunit_shop(mood))
    m_rope = sue_person.make_l1_rope(mood)
    sue_person.add_fact(fact_context=m_rope, fact_state=m_rope)
    print(f"When one non-ranged_fact added {sue_person.planroot.factunits=}")
    assert len(sue_person.planroot.factunits) == 3

    # THEN
    assert len(sue_person._get_rangeroot_factunits()) == 2


def test_PersonUnit_get_rangeroot_factunits_ReturnsObj_Scenario1():
    # ESTABLISH a two ranged facts where one is "rangeroot" get_root_ranged_facts returns one "rangeroot" fact
    sue_person = personunit_shop("Sue")
    ziet_str = "ziet"
    sue_person.set_l1_plan(planunit_shop(ziet_str, begin=0, close=140))
    ziet_rope = sue_person.make_l1_rope(ziet_str)
    mood_x = "mood_x"
    sue_person.set_l1_plan(planunit_shop(mood_x))
    m_x_rope = sue_person.make_l1_rope(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_person.set_plan_obj(planunit_shop(happy), parent_rope=m_x_rope)
    sue_person.set_plan_obj(planunit_shop(sad), parent_rope=m_x_rope)
    sue_person.add_fact(
        fact_context=ziet_rope, fact_state=ziet_rope, fact_lower=5, fact_upper=10
    )
    sue_person.add_fact(
        fact_context=m_x_rope, fact_state=sue_person.make_rope(m_x_rope, happy)
    )
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_person.planroot.factunits=}"
    )
    assert len(sue_person.planroot.factunits) == 2

    # WHEN / THEN
    assert len(sue_person._get_rangeroot_factunits()) == 1
    assert sue_person._get_rangeroot_factunits()[0].fact_context == ziet_rope


def test_PersonUnit_set_fact_create_missing_plans_Createsreason_contextAndFact():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    situations_str = "situations"
    situations_rope = sue_person.make_l1_rope(situations_str)
    climate_str = "climate"
    climate_rope = sue_person.make_rope(situations_rope, climate_str)
    assert sue_person.planroot.get_kid(situations_str) is None

    # WHEN
    sue_person.add_fact(situations_rope, climate_rope, create_missing_plans=True)

    # THEN
    assert sue_person.planroot.get_kid(situations_str) is not None
    assert sue_person.get_plan_obj(situations_rope) is not None
    assert sue_person.get_plan_obj(climate_rope) is not None
