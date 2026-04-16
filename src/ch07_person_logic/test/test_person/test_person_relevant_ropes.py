from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import reasonunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_mop_with_reason_personunit_example1,
    get_personunit_with_4_levels,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_get_relevant_ropes_EmptyRopeTermReturnsEmpty():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()

    # WHEN
    relevant_ropes = sue_person._get_relevant_ropes({})

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 0
    assert relevant_ropes == set()


def test_PersonUnit_get_relevant_ropes_RootRopeTermReturnsOnlyItself():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    root_rope = sue_person.planroot.get_plan_rope()

    # WHEN
    root_dict = {root_rope: -1}
    relevant_ropes = sue_person._get_relevant_ropes(root_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 1
    assert relevant_ropes == {root_rope}


def test_PersonUnit_get_relevant_ropes_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    root_rope = sue_person.planroot.get_plan_rope()

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_person.make_rope(wk_rope, sun_str)
    sun_dict = {sun_rope}
    relevant_ropes = sue_person._get_relevant_ropes(sun_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert relevant_ropes == {root_rope, sun_rope, wk_rope}


def test_PersonUnit_get_relevant_ropes_ReturnsSimpleReasonUnitreason_context():
    # ESTABLISH
    sue_person = personunit_shop(person_name="Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_person.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str)
    sue_person.set_plan_obj(floor_plan, parent_rope=casa_rope)

    unim_str = "unimportant"
    unim_rope = sue_person.make_l1_rope(unim_str)
    unim_plan = planunit_shop(unim_str)
    sue_person.set_plan_obj(unim_plan, parent_rope=sue_person.planroot.get_plan_rope())

    situation_str = "cleaniness situation"
    situation_rope = sue_person.make_rope(casa_rope, situation_str)
    situation_plan = planunit_shop(situation_str)
    sue_person.set_plan_obj(situation_plan, parent_rope=casa_rope)
    floor_reason = reasonunit_shop(reason_context=situation_rope)
    floor_reason.set_case(case=situation_rope)
    sue_person.edit_plan_attr(floor_rope, reason=floor_reason)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = sue_person._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 4
    root_rope = sue_person.planroot.get_plan_rope()
    assert relevant_ropes == {root_rope, casa_rope, situation_rope, floor_rope}
    assert unim_rope not in relevant_ropes


def test_PersonUnit_get_relevant_ropes_ReturnsReasonUnitreason_contextAndDescendents():
    # ESTABLISH
    x_person = get_mop_with_reason_personunit_example1()
    root_rope = x_person.planroot.get_plan_rope()
    casa_rope = x_person.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = x_person.make_rope(casa_rope, floor_str)

    unim_str = "unimportant"
    unim_rope = x_person.make_l1_rope(unim_str)

    situation_str = "cleaniness situation"
    situation_rope = x_person.make_rope(casa_rope, situation_str)

    clean_rope = x_person.make_rope(situation_rope, exx.clean)

    very_much_str = "very_much"
    very_much_rope = x_person.make_rope(clean_rope, very_much_str)

    moderately_str = "moderately"
    moderately_rope = x_person.make_rope(clean_rope, moderately_str)

    dirty_str = "dirty"
    dirty_rope = x_person.make_rope(situation_rope, dirty_str)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = x_person._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 8
    assert clean_rope in relevant_ropes
    assert dirty_rope in relevant_ropes
    assert moderately_rope in relevant_ropes
    assert very_much_rope in relevant_ropes
    assert relevant_ropes == {
        root_rope,
        casa_rope,
        situation_rope,
        floor_rope,
        clean_rope,
        dirty_rope,
        very_much_rope,
        moderately_rope,
    }
    assert unim_rope not in relevant_ropes


def test_PersonUnit_get_relevant_ropes_ReturnSimple():
    # ESTABLISH
    yao_person = personunit_shop(person_name=exx.yao)
    root_rope = yao_person.planroot.get_plan_rope()
    min_range_x_str = "a_minute_range"
    min_range_x_rope = yao_person.make_l1_rope(min_range_x_str)
    min_range_plan = planunit_shop(min_range_x_str, begin=0, close=2880)
    yao_person.set_l1_plan(min_range_plan)

    jour_length_str = "jour_1ce"
    jour_length_rope = yao_person.make_l1_rope(jour_length_str)
    jour_length_plan = planunit_shop(jour_length_str, begin=0, close=1440)
    yao_person.set_l1_plan(jour_length_plan)

    hr_length_str = "hr_length"
    hr_length_rope = yao_person.make_l1_rope(hr_length_str)
    hr_length_plan = planunit_shop(hr_length_str)
    yao_person.set_l1_plan(hr_length_plan)

    min_jours_str = "jours in minute_range"
    min_jours_rope = yao_person.make_rope(min_range_x_rope, min_jours_str)
    min_jours_plan = planunit_shop(min_jours_str)
    yao_person.set_plan_obj(min_jours_plan, parent_rope=min_range_x_rope)

    # WHEN
    print(f"{yao_person._plan_dict.keys()}")
    ropes_dict = {min_jours_rope}
    relevant_ropes = yao_person._get_relevant_ropes(ropes_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert min_range_x_rope in relevant_ropes
    assert jour_length_rope not in relevant_ropes
    assert hr_length_rope not in relevant_ropes
    assert min_jours_rope in relevant_ropes
    assert root_rope in relevant_ropes
    # min_jours_plan = yao_person.get_plan_obj(min_jours_rope)


def test_PersonUnit_get_inheritor_plan_list_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    tech_rope = yao_personunit.make_l1_rope("tech")
    wk_rope = yao_personunit.make_rope(tech_rope, exx.wk)
    yao_personunit.set_plan_obj(planunit_shop(exx.wk, begin=0, close=10800), tech_rope)
    mon_str = "Mon"
    mon_rope = yao_personunit.make_rope(wk_rope, mon_str)
    yao_personunit.set_plan_obj(planunit_shop(mon_str), wk_rope)
    yao_personunit.conpute()

    # WHEN
    x_inheritor_plan_list = yao_personunit.get_inheritor_plan_list(wk_rope, mon_rope)

    # # THEN
    assert len(x_inheritor_plan_list) == 2
    wk_plan = yao_personunit.get_plan_obj(wk_rope)
    mon_plan = yao_personunit.get_plan_obj(mon_rope)
    assert x_inheritor_plan_list == [wk_plan, mon_plan]
