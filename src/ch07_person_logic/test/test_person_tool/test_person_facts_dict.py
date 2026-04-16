from copy import deepcopy as copy_deepcopy
from src.ch04_rope.rope import create_rope
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.person_tool import (
    clear_factunits_from_person,
    get_person_root_facts_dict,
    set_factunits_to_person,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_get_person_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    # WHEN / THEN
    assert get_person_root_facts_dict(sue_person) == {}
    assert (
        get_person_root_facts_dict(sue_person)
        == sue_person.get_planroot_factunits_dict()
    )


def test_get_person_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_l1_rope("clean")
    dirty_rope = sue_person.make_l1_rope("dirty")
    sue_person.add_fact(casa_rope, dirty_rope, create_missing_plans=True)

    # WHEN
    sue_fact_dict = get_person_root_facts_dict(sue_person)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get(kw.fact_context) == casa_rope
    assert casa_fact_dict.get(kw.fact_state) == dirty_rope
    expected_sue_fact_dict = {
        casa_rope: {kw.fact_context: casa_rope, kw.fact_state: dirty_rope}
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_person_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_l1_rope("clean")
    dirty_rope = sue_person.make_l1_rope("dirty")
    dirty_reason_lower = 10
    dirty_reason_upper = 13
    sue_person.add_fact(
        casa_rope, dirty_rope, dirty_reason_lower, dirty_reason_upper, True
    )

    # WHEN
    sue_fact_dict = get_person_root_facts_dict(sue_person)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get(kw.fact_context) == casa_rope
    assert casa_fact_dict.get(kw.fact_state) == dirty_rope
    assert casa_fact_dict.get("fact_lower") == dirty_reason_lower
    assert casa_fact_dict.get("fact_upper") == dirty_reason_upper
    expected_sue_fact_dict = {
        casa_rope: {
            kw.fact_context: casa_rope,
            kw.fact_state: dirty_rope,
            "fact_lower": dirty_reason_lower,
            "fact_upper": dirty_reason_upper,
        }
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_set_factunits_to_person_ReturnsObj_Scenario0_PersonEmptyNoFacts():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao, exx.a23)
    before_yao_person = copy_deepcopy(yao_person)
    facts_dict = {}
    assert yao_person.to_dict() == before_yao_person.to_dict()

    # WHEN
    set_factunits_to_person(yao_person, facts_dict)

    # THEN
    assert yao_person.to_dict() == before_yao_person.to_dict()


def test_set_factunits_to_person_ReturnsObj_Scenario1_Person1FactsChanged():
    # ESTABLISH
    bob_person = personunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    clean_rope = bob_person.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(floor_rope)
    bob_person.add_plan(clean_rope)
    bob_person.add_plan(dirty_rope)
    bob_person.add_plan(mop_rope, pledge=True)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    dirty_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: dirty_rope}
    }
    before_bob_person = copy_deepcopy(bob_person)
    assert bob_person.get_planroot_factunits_dict() != dirty_facts_dict
    assert bob_person.get_planroot_factunits_dict() == {}
    assert bob_person.to_dict() == before_bob_person.to_dict()

    # WHEN
    set_factunits_to_person(bob_person, dirty_facts_dict)

    # THEN
    assert bob_person.to_dict() != before_bob_person.to_dict()
    assert bob_person.get_planroot_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_person_ReturnsObj_Scenario2_FactUnit_reason_context_DoesNotExistInPerson():
    # ESTABLISH
    bob_person = personunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    clean_rope = bob_person.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(floor_rope)
    # bob_person.add_plan(clean_rope)
    bob_person.add_plan(dirty_rope)
    bob_person.add_plan(mop_rope, pledge=True)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    clean_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: clean_rope}
    }
    before_bob_person = copy_deepcopy(bob_person)
    assert bob_person.get_planroot_factunits_dict() != clean_facts_dict
    assert bob_person.get_planroot_factunits_dict() == {}
    assert bob_person.to_dict() == before_bob_person.to_dict()

    # WHEN
    set_factunits_to_person(bob_person, clean_facts_dict)

    # THEN
    assert bob_person.to_dict() != before_bob_person.to_dict()
    assert bob_person.get_planroot_factunits_dict() == clean_facts_dict
    assert bob_person.get_plan_obj(clean_rope)


def test_set_factunits_to_person_ReturnsObj_Scenario3_FactUnit_reason_context_Withoutreason_contextNotAddedToPerson():
    # ESTABLISH
    bob_person = personunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    clean_rope = bob_person.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(floor_rope)
    # bob_person.add_plan(clean_rope)
    bob_person.add_plan(dirty_rope)
    bob_person.add_plan(mop_rope, pledge=True)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )

    weather_str = "weather"
    raining_str = "raining"
    weather_rope = bob_person.make_l1_rope(weather_str)
    rain_rope = bob_person.make_rope(weather_rope, raining_str)

    two_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: clean_rope},
        weather_rope: {kw.fact_context: weather_rope, kw.fact_state: rain_rope},
    }
    before_bob_person = copy_deepcopy(bob_person)
    assert bob_person.get_planroot_factunits_dict() != two_facts_dict
    assert bob_person.get_planroot_factunits_dict() == {}
    assert bob_person.to_dict() == before_bob_person.to_dict()

    # WHEN
    set_factunits_to_person(bob_person, two_facts_dict)

    # THEN
    assert floor_rope in set(bob_person.get_planroot_factunits_dict().keys())
    assert weather_rope not in set(bob_person.get_planroot_factunits_dict().keys())
    assert bob_person.to_dict() != before_bob_person.to_dict()


def test_clear_factunits_from_person_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_person = personunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    clean_rope = bob_person.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(floor_rope)
    # bob_person.add_plan(clean_rope)
    bob_person.add_plan(dirty_rope)
    bob_person.add_plan(mop_rope, pledge=True)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    bob_person.add_fact(floor_rope, dirty_rope)
    floor_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: dirty_rope}
    }
    assert bob_person.get_planroot_factunits_dict() == floor_facts_dict
    assert bob_person.get_planroot_factunits_dict() != {}

    # WHEN
    clear_factunits_from_person(bob_person)

    # THEN
    assert bob_person.get_planroot_factunits_dict() != floor_facts_dict
    assert bob_person.get_planroot_factunits_dict() == {}
