from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_get_plan_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    ziet_rope = yao_personunit.make_l1_rope("ziet")
    tech_rope = yao_personunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_personunit.make_rope(tech_rope, exx.wk)
    wk_plan = planunit_shop(exx.wk, begin=0, close=10800)
    yao_personunit.set_plan_obj(wk_plan, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_personunit.set_plan_obj(mon_plan, wk_rope)
    yao_personunit.set_plan_obj(tue_plan, wk_rope)
    yao_personunit.set_plan_obj(wed_plan, wk_rope)
    yao_personunit.set_plan_obj(thu_plan, wk_rope)
    yao_personunit.set_plan_obj(fri_plan, wk_rope)
    yao_personunit.set_plan_obj(sat_plan, wk_rope)
    yao_personunit.set_plan_obj(sun_plan, wk_rope)
    yao_personunit.conpute()

    # WHEN
    ranged_plans = yao_personunit.get_plan_ranged_kids(plan_rope=wk_rope)

    # # THEN
    assert len(ranged_plans) == 7


def test_PersonUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    ziet_rope = yao_personunit.make_l1_rope("ziet")
    tech_rope = yao_personunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_personunit.make_rope(tech_rope, exx.wk)
    wk_plan = planunit_shop(exx.wk, begin=0, close=10800)
    yao_personunit.set_plan_obj(wk_plan, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_personunit.set_plan_obj(mon_plan, wk_rope)
    yao_personunit.set_plan_obj(tue_plan, wk_rope)
    yao_personunit.set_plan_obj(wed_plan, wk_rope)
    yao_personunit.set_plan_obj(thu_plan, wk_rope)
    yao_personunit.set_plan_obj(fri_plan, wk_rope)
    yao_personunit.set_plan_obj(sat_plan, wk_rope)
    yao_personunit.set_plan_obj(sun_plan, wk_rope)
    yao_personunit.conpute()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_plans = yao_personunit.get_plan_ranged_kids(wk_rope, x_begin, x_close)

    # THEN
    # for plan_x in wk_plan.kids.values():
    #     print(f"{plan_x.plan_label=} {plan_x.gogo_calc=} {plan_x.stop_calc=} ")
    # print("")
    # for plan_x in ranged_plans.values():
    #     print(f"{plan_x.plan_label=} {plan_x.gogo_calc=} {plan_x.stop_calc=} ")
    assert len(ranged_plans) == 3


def test_PersonUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    ziet_rope = yao_personunit.make_l1_rope("ziet")
    tech_rope = yao_personunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_personunit.make_rope(tech_rope, exx.wk)
    wk_plan = planunit_shop(exx.wk, begin=0, close=10800)
    yao_personunit.set_plan_obj(wk_plan, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_personunit.set_plan_obj(mon_plan, wk_rope)
    yao_personunit.set_plan_obj(tue_plan, wk_rope)
    yao_personunit.set_plan_obj(wed_plan, wk_rope)
    yao_personunit.set_plan_obj(thu_plan, wk_rope)
    yao_personunit.set_plan_obj(fri_plan, wk_rope)
    yao_personunit.set_plan_obj(sat_plan, wk_rope)
    yao_personunit.set_plan_obj(sun_plan, wk_rope)
    yao_personunit.conpute()

    # WHEN / THEN
    assert len(yao_personunit.get_plan_ranged_kids(wk_rope, 0, 1440)) == 1
    assert len(yao_personunit.get_plan_ranged_kids(wk_rope, 0, 2000)) == 2
    assert len(yao_personunit.get_plan_ranged_kids(wk_rope, 0, 3000)) == 3


def test_PersonUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    ziet_rope = yao_personunit.make_l1_rope("ziet")
    tech_rope = yao_personunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_personunit.make_rope(tech_rope, exx.wk)
    wk_plan = planunit_shop(exx.wk, begin=0, close=10800)
    yao_personunit.set_plan_obj(wk_plan, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_plan = planunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_plan = planunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_plan = planunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_plan = planunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_plan = planunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_plan = planunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_plan = planunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_personunit.set_plan_obj(mon_plan, wk_rope)
    yao_personunit.set_plan_obj(tue_plan, wk_rope)
    yao_personunit.set_plan_obj(wed_plan, wk_rope)
    yao_personunit.set_plan_obj(thu_plan, wk_rope)
    yao_personunit.set_plan_obj(fri_plan, wk_rope)
    yao_personunit.set_plan_obj(sat_plan, wk_rope)
    yao_personunit.set_plan_obj(sun_plan, wk_rope)
    yao_personunit.conpute()

    # WHEN / THEN
    assert len(yao_personunit.get_plan_ranged_kids(wk_rope, 0)) == 1
    assert len(yao_personunit.get_plan_ranged_kids(wk_rope, 1440)) == 1

    # ESTABLISH
    wks_plan = planunit_shop(exx.wk, gogo_want=0, stop_want=1440 * 5)
    yao_personunit.set_plan_obj(wks_plan, wk_rope)

    # WHEN
    yao_personunit.conpute()

    # THEN
    assert len(yao_personunit.get_plan_ranged_kids(wk_rope, 1440)) == 2
