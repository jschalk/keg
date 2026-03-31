from src.ch01_allot.allot import default_pool_num
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import caseunit_shop, reasonheir_shop, reasonunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_graphic import display_plantree
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    from_list_get_active,
    get_personunit_with7am_clean_table_reason,
    get_personunit_with_4_levels_and_2reasons,
    personunit_v001,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_conpute_Sets_active_WhenFactSaysNo():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_personunit.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_personunit.make_rope(wk_rope, sun_str)

    # for plan in sue_personunit._plan_dict.values():
    #     print(f"{casa_rope=} {plan.get_plan_rope()=}")
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    assert sue_personunit.get_plan_obj(casa_rope).plan_active is None

    # WHEN
    sue_personunit.add_fact(fact_context=wk_rope, fact_state=sun_rope)
    sue_personunit.conpute()

    # THEN
    assert sue_personunit._plan_dict != {}
    assert len(sue_personunit._plan_dict) == 17
    # for plan in sue_personunit._plan_dict.values():
    #     print(f"{casa_rope=} {plan.get_plan_rope()=}")
    assert sue_personunit.get_plan_obj(casa_rope).plan_active is False


def test_PersonUnit_conpute_Sets_active_WhenFactModifies():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_personunit.make_l1_rope(wk_str)
    sun_str = "Wed"
    sun_rope = sue_personunit.make_rope(wk_rope, sun_str)
    casa_rope = sue_personunit.make_l1_rope(exx.casa)

    # WHEN
    sue_personunit.add_fact(fact_context=wk_rope, fact_state=sun_rope)

    # THEN
    sue_personunit.conpute()
    assert sue_personunit._plan_dict
    assert len(sue_personunit._plan_dict) == 17
    assert sue_personunit._plan_dict.get(casa_rope).plan_active is False

    # WHEN
    nation_str = "nation"
    nation_rope = sue_personunit.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_personunit.make_rope(nation_rope, usa_str)
    sue_personunit.add_fact(fact_context=nation_rope, fact_state=usa_rope)

    # THEN
    sue_personunit.conpute()
    assert sue_personunit._plan_dict
    assert len(sue_personunit._plan_dict) == 17
    assert sue_personunit._plan_dict.get(casa_rope).plan_active

    # WHEN
    france_str = "France"
    france_rope = sue_personunit.make_rope(nation_rope, france_str)
    sue_personunit.add_fact(fact_context=nation_rope, fact_state=france_rope)

    # THEN
    sue_personunit.conpute()
    assert sue_personunit._plan_dict
    assert len(sue_personunit._plan_dict) == 17
    assert sue_personunit._plan_dict.get(casa_rope).plan_active is False


def test_PersonUnit_conpute_Sets_plan_dict():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_personunit.make_l1_rope(wk_str)
    wed_rope = sue_personunit.make_rope(wk_rope, exx.wed)
    nation_str = "nation"
    nation_rope = sue_personunit.make_l1_rope(nation_str)
    france_str = "France"
    france_rope = sue_personunit.make_rope(nation_rope, france_str)
    sue_personunit.add_fact(fact_context=wk_rope, fact_state=wed_rope)
    sue_personunit.add_fact(fact_context=nation_rope, fact_state=france_rope)

    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_plan = sue_personunit.get_plan_obj(casa_rope)
    print(f"{sue_personunit.person_name=} {len(casa_plan.reasonunits)=}")
    # print(f"{casa_plan.reasonunits=}")
    print(f"{sue_personunit.person_name=} {len(sue_personunit.planroot.factunits)=}")
    # print(f"{sue_personunit.planroot.factunits=}")

    sue_personunit.conpute()
    assert sue_personunit._plan_dict
    assert len(sue_personunit._plan_dict) == 17

    usa_str = "USA"
    usa_rope = sue_personunit.make_rope(nation_rope, usa_str)
    oregon_str = "Oregon"
    oregon_rope = sue_personunit.make_rope(usa_rope, oregon_str)

    wed = caseunit_shop(reason_state=wed_rope)
    wed.case_active = True
    wed.case_task = False
    usa = caseunit_shop(reason_state=usa_rope)
    usa.case_active = True
    usa.case_task = False

    wed_lu = reasonunit_shop(wk_rope, cases={wed.reason_state: wed})
    sta_lu = reasonunit_shop(nation_rope, cases={usa.reason_state: usa})
    wed_lh = reasonheir_shop(
        reason_context=wk_rope,
        cases={wed.reason_state: wed},
        reason_active=True,
        reason_task=False,
        parent_heir_active=True,
    )
    sta_lh = reasonheir_shop(
        reason_context=nation_rope,
        cases={usa.reason_state: usa},
        reason_active=True,
        reason_task=False,
        parent_heir_active=True,
    )

    x1_reasonunits = {
        wed_lu.reason_context: wed_lu,
        sta_lu.reason_context: sta_lu,
    }
    x1_reasonheirs = {
        wed_lh.reason_context: wed_lh,
        sta_lh.reason_context: sta_lh,
    }

    # WHEN
    sue_personunit.add_fact(fact_context=nation_rope, fact_state=oregon_rope)
    sue_personunit.conpute()

    # THEN
    casa_plan = sue_personunit._plan_dict.get(casa_rope)
    print(f"\nlook at {casa_plan.get_plan_rope()=}")
    assert casa_plan.parent_rope == sue_personunit.planroot.get_plan_rope()
    assert casa_plan.kids == {}
    assert casa_plan.star == 30
    assert casa_plan.plan_label == exx.casa
    assert casa_plan.tree_level == 1
    assert casa_plan.plan_active
    assert casa_plan.pledge
    # print(f"{casa_plan.reasonheirs=}")
    nation_reasonheir = casa_plan.reasonheirs[nation_rope]
    print(f"  {nation_reasonheir=}")
    print(f"  {nation_reasonheir.reason_active=}\n")
    # assert casa_plan.reasonheirs == x1_reasonheirs

    assert len(casa_plan.reasonheirs) == len(x1_reasonheirs)
    wk_reasonheir = casa_plan.reasonheirs.get(wk_rope)
    # usa_case = wk_reasonheir.cases.get(usa_rope)
    print(f"    {casa_plan.plan_label=}")
    # print(f"    {usa_case.reason_context=}")
    # print(f"    {usa_case.case_task=}")
    # print(f"    {usa_case.case_task=}")
    assert wk_reasonheir.reason_task is False
    # print(f"      cases: {w=}")
    # w_state = usa_case.cases[wed_rope].reason_state
    # print(f"      {w_state=}")
    # assert usa_case.case_task == w_state.case_task
    # assert usa_case.case_active == w_state.reason_active
    # assert wk_reasonheir.cases == wk_reasonheir.cases

    # assert casa_plan.reasonunits == x1_reasonunits

    # print("iterate through every plan...")
    # for x_plan in plan_dict:
    #     if str(type(x_plan)).find(".plan.PlanUnit'>") > 0:
    #         assert x_plan.plan_active is not None

    #     # print("")
    #     # print(f"{x_plan.plan_label=}")
    #     # print(f"{len(x_plan.reasonunits)=}")
    #     print(
    #         f"  {x_plan.plan_label} iterate through every reasonheir... {len(x_plan.reasonheirs)=} {x_plan.plan_label=}"
    #     )
    #     # print(f"{x_plan.reasonheirs=}")
    #     for reason in x_plan.reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.reason_context=}")
    #         assert reason.reason_active is not None
    #         for case_x in reason.cases.values():
    #             assert case_x.reason_active is not None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.cases, type_str="src.s2_personunit.reason.CaseUnit"
    #         )


# def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
#     bool_x = True
#     for x_value in x_dict.values():
#         if type_str not in str(type(x_value)):
#             bool_x = False
#         print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
#     return bool_x


def test_PersonUnit_conpute_CalculatesRangeAttributes():
    # ESTABLISH
    sue_personunit = get_personunit_with7am_clean_table_reason()
    sue_personunit.conpute()
    house_str = "houseadministration"
    house_rope = sue_personunit.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_personunit.make_rope(house_rope, clean_str)
    assert sue_personunit._plan_dict.get(clean_rope).plan_active is False

    # set facts as midevening to 8am
    ziet_str = "ziettech"
    ziet_rope = sue_personunit.make_l1_rope(ziet_str)
    x24hr_str = "24hr"
    x24hr_rope = sue_personunit.make_rope(ziet_rope, x24hr_str)
    x24hr_reason_context = x24hr_rope
    x24hr_fact_state = x24hr_rope
    x24hr_reason_lower = 0.0
    x24hr_reason_upper = 8.0

    # WHEN
    sue_personunit.add_fact(
        x24hr_reason_context,
        fact_state=x24hr_fact_state,
        fact_lower=x24hr_reason_lower,
        fact_upper=x24hr_reason_upper,
    )

    # THEN
    sue_personunit.conpute()
    assert sue_personunit._plan_dict.get(clean_rope).plan_active

    # WHEN
    # set facts as 8am to 10am
    x24hr_reason_lower = 8.0
    x24hr_reason_upper = 10.0
    print(sue_personunit.planroot.factunits[x24hr_rope])
    sue_personunit.add_fact(
        x24hr_reason_context,
        fact_state=x24hr_fact_state,
        fact_lower=x24hr_reason_lower,
        fact_upper=x24hr_reason_upper,
    )
    print(sue_personunit.planroot.factunits[x24hr_rope])
    print(sue_personunit.planroot.kids[house_str].kids[clean_str].reasonunits)
    # sue_personunit.planroot.kids["houseadministration"].kids[clean_str].plan_active = None

    # THEN
    sue_personunit.conpute()
    assert sue_personunit._plan_dict.get(clean_rope).plan_active is False


def test_PersonUnit_get_agenda_dict_ReturnsObj_WithSinglePledge():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()

    # WHEN
    pledge_plans = sue_personunit.get_agenda_dict()

    # THEN
    assert pledge_plans is not None
    assert len(pledge_plans) > 0
    assert len(pledge_plans) == 1


def test_PersonUnit_conpute_SetsData_personunit_v001():
    # ESTABLISH
    yao_personunit = personunit_v001()
    print(f"{yao_personunit.get_reason_contexts()=}")
    jour_min_str = "jour_minute"
    jour_min_rope = yao_personunit.make_l1_rope(jour_min_str)
    yao_personunit.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=1439,
    )

    mood_str = "Moods"
    mood_rope = yao_personunit.make_l1_rope(mood_str)
    yao_personunit.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    print(f"{yao_personunit.get_reason_contexts()=}")

    yr_mon_str = "yr_month"
    yr_mon_rope = yao_personunit.make_l1_rope(yr_mon_str)
    yao_personunit.add_fact(fact_context=yr_mon_rope, fact_state=yr_mon_rope)
    websites_str = "Websites"
    web_rope = yao_personunit.make_l1_rope(websites_str)
    yao_personunit.add_fact(fact_context=web_rope, fact_state=web_rope)
    assert yao_personunit is not None
    # print(f"{yao_personunit.person_name=}")
    # print(f"{len(yao_personunit.planroot.kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_rope = yao_personunit.make_l1_rope(ulty_str)

    # if yao_personunit.planroot.kids["Ultimate Frisbee"].plan_label == "Ultimate Frisbee":
    assert yao_personunit.planroot.kids[ulty_str].reasonunits is not None
    assert yao_personunit.person_name is not None

    # for fact in yao_personunit.planroot.factunits.values():
    #     print(f"{fact=}")

    # WHEN
    yao_personunit.conpute()

    # THEN
    # print(f"{str(type(plan))=}")
    # print(f"{len(plan_dict)=}")
    laundry_str = "laundry mon"
    casa_rope = yao_personunit.make_l1_rope("casa")
    cleaning_rope = yao_personunit.make_rope(casa_rope, "cleaning")
    laundry_rope = yao_personunit.make_rope(cleaning_rope, laundry_str)

    # for plan in plan_dict:
    #     assert (
    #         str(type(plan)).find(".plan.PlanUnit'>") > 0
    #         or str(type(plan)).find(".plan.PlanUnit'>") > 0
    #     )
    #     # print(f"{plan.plan_label=}")
    #     if plan.plan_label == laundry_str:
    #         for reason in plan.reasonunits.values():
    #             print(f"{plan.plan_label=} {reason.reason_context=}")  # {reason.cases=}")
    # assert plan.plan_active is False
    assert yao_personunit._plan_dict.get(laundry_rope).plan_active is False

    # WHEN
    wk_str = "sem_jours"
    wk_rope = yao_personunit.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = yao_personunit.make_rope(wk_rope, mon_str)
    yao_personunit.add_fact(fact_context=wk_rope, fact_state=mon_rope)
    yao_personunit.conpute()

    # THEN
    assert yao_personunit._plan_dict.get(laundry_rope).plan_active is False


def test_PersonUnit_conpute_OptionWeekJoursReturnsObj_personunit_v001():
    # ESTABLISH
    yao_personunit = personunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_personunit.make_l1_rope(hr_number_str)
    yao_personunit.add_fact(
        fact_context=hr_number_rope,
        fact_state=hr_number_rope,
        fact_lower=0,
        fact_upper=23,
    )
    jour_min_str = "jour_minute"
    jour_min_rope = yao_personunit.make_l1_rope(jour_min_str)
    yao_personunit.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=59,
    )
    mon_wk_str = "month_wk"
    mon_wk_rope = yao_personunit.make_l1_rope(mon_wk_str)
    yao_personunit.add_fact(fact_context=mon_wk_rope, fact_state=mon_wk_rope)
    nation_str = "Nation-States"
    nation_rope = yao_personunit.make_l1_rope(nation_str)
    yao_personunit.add_fact(fact_context=nation_rope, fact_state=nation_rope)
    mood_str = "Moods"
    mood_rope = yao_personunit.make_l1_rope(mood_str)
    yao_personunit.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_personunit.make_l1_rope(aaron_str)
    yao_personunit.add_fact(fact_context=aaron_rope, fact_state=aaron_rope)
    websites_str = "Websites"
    web_rope = yao_personunit.make_l1_rope(websites_str)
    yao_personunit.add_fact(fact_context=web_rope, fact_state=web_rope)
    yr_mon_str = "yr_month"
    yr_mon_rope = yao_personunit.make_l1_rope(yr_mon_str)
    yao_personunit.add_fact(
        fact_context=yr_mon_rope, fact_state=yr_mon_rope, fact_lower=0, fact_upper=1000
    )

    yao_personunit.conpute()
    missing_facts = yao_personunit.get_missing_fact_reason_contexts()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    wk_str = "sem_jours"
    wk_rope = yao_personunit.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = yao_personunit.make_rope(wk_rope, mon_str)
    tue_str = "Tue"
    tue_rope = yao_personunit.make_rope(wk_rope, tue_str)
    mon_case_x = caseunit_shop(reason_state=mon_rope)
    mon_case_x.case_active = False
    mon_case_x.case_task = False
    tue_case_x = caseunit_shop(reason_state=tue_rope)
    tue_case_x.case_active = False
    tue_case_x.case_task = False
    mt_cases = {
        mon_case_x.reason_state: mon_case_x,
        tue_case_x.reason_state: tue_case_x,
    }
    mt_reasonunit = reasonunit_shop(wk_rope, cases=mt_cases)
    mt_reasonheir = reasonheir_shop(wk_rope, cases=mt_cases, reason_active=False)
    x_planroot = yao_personunit.planroot
    x_planroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_personunit.reasonunits[wk_rope].reason_context=}")
    # print(f"{yao_personunit.reasonunits[wk_rope].cases[mon_rope].reason_state=}")
    # print(f"{yao_personunit.reasonunits[wk_rope].cases[tue_rope].reason_state=}")
    wk_reasonunit = x_planroot.reasonunits[wk_rope]
    print(f"{wk_reasonunit.cases=}")
    case_mon = wk_reasonunit.cases.get(mon_rope)
    case_tue = wk_reasonunit.cases.get(tue_rope)
    assert case_mon
    assert case_mon == mt_reasonunit.cases[case_mon.reason_state]
    assert case_tue
    assert case_tue == mt_reasonunit.cases[case_tue.reason_state]
    assert wk_reasonunit == mt_reasonunit

    # WHEN
    plan_dict = yao_personunit.get_plan_dict()

    # THEN
    gen_wk_reasonheir = x_planroot.get_reasonheir(wk_rope)
    gen_mon_case = gen_wk_reasonheir.cases.get(mon_rope)
    assert gen_mon_case.case_active == mt_reasonheir.cases.get(mon_rope).case_active
    assert gen_mon_case == mt_reasonheir.cases.get(mon_rope)
    assert gen_wk_reasonheir.cases == mt_reasonheir.cases
    assert gen_wk_reasonheir == mt_reasonheir

    casa_rope = yao_personunit.make_l1_rope(exx.casa)
    bird_str = "say hi to birds"
    bird_rope = yao_personunit.make_rope(casa_rope, bird_str)
    assert from_list_get_active(bird_rope, plan_dict) is False


def test_PersonUnit_conpute_SetsPlanUnitsActiveWithEvery6WeeksReason_personunit_v001():
    # ESTABLISH
    yao_personunit = personunit_v001()
    hr_num_str = "hr_number"
    hr_num_rope = yao_personunit.make_l1_rope(hr_num_str)
    min_str = "jour_minute"
    min_rope = yao_personunit.make_l1_rope(min_str)

    # WHEN
    yao_personunit.add_fact(
        fact_context=hr_num_rope, fact_state=hr_num_rope, fact_lower=0, fact_upper=23
    )
    yao_personunit.add_fact(
        fact_context=min_rope, fact_state=min_rope, fact_lower=0, fact_upper=59
    )
    yao_personunit.conpute()

    # THEN
    ced_wk_reason_context = yao_personunit.make_l1_rope("ced_wk")

    reason_divisor = None
    reason_lower = None
    reason_upper = None
    print(f"{len(yao_personunit._plan_dict)=}")

    casa_rope = yao_personunit.make_l1_rope("casa")
    cleaning_rope = yao_personunit.make_rope(casa_rope, "cleaning")
    clean_couch_rope = yao_personunit.make_rope(cleaning_rope, "clean couch blankets")
    clean_couch_plan = yao_personunit.get_plan_obj(clean_couch_rope)
    # print(f"{clean_couch_plan.reasonunits.values()=}")
    ced_wk_reason = clean_couch_plan.reasonunits.get(ced_wk_reason_context)
    ced_wk_case = ced_wk_reason.cases.get(ced_wk_reason_context)
    print(
        f"{clean_couch_plan.plan_label=} {ced_wk_reason.reason_context=} {ced_wk_case.reason_state=}"
    )
    # print(f"{clean_couch_plan.plan_label=} {ced_wk_reason.reason_context=} {case_x=}")
    reason_divisor = ced_wk_case.reason_divisor
    reason_lower = ced_wk_case.reason_lower
    reason_upper = ced_wk_case.reason_upper
    # print(f"{plan.reasonunits=}")
    assert clean_couch_plan.plan_active is False

    # for plan in plan_dict:
    #     # print(f"{plan.parent_rope=}")
    #     if plan.plan_label == "clean couch blankets":
    #         print(f"{plan.get_plan_rope()=}")

    assert reason_divisor == 6
    assert reason_lower == 1
    print(
        f"There exists a plan with a reason_context {ced_wk_reason_context} that also has lemmet div =6 and reason_lower/reason_upper =1"
    )
    # print(f"{len(plan_dict)=}")
    ced_wk_reason_lower = 6001

    # WHEN
    yao_personunit.add_fact(
        ced_wk_reason_context,
        fact_state=ced_wk_reason_context,
        fact_lower=ced_wk_reason_lower,
        fact_upper=ced_wk_reason_lower,
    )
    nation_str = "Nation-States"
    nation_rope = yao_personunit.make_l1_rope(nation_str)
    yao_personunit.add_fact(fact_context=nation_rope, fact_state=nation_rope)
    print(
        f"Nation set and also fact set: {ced_wk_reason_context=} with {ced_wk_reason_lower=} and {ced_wk_reason_lower=}"
    )
    print(f"{yao_personunit.planroot.factunits=}")
    yao_personunit.conpute()

    # THEN
    wk_str = "ced_wk"
    wk_rope = yao_personunit.make_l1_rope(wk_str)
    casa_rope = yao_personunit.make_l1_rope("casa")
    cleaning_rope = yao_personunit.make_rope(casa_rope, "cleaning")
    clean_couch_str = "clean couch blankets"
    clean_couch_rope = yao_personunit.make_rope(cleaning_rope, clean_couch_str)
    clean_couch_plan = yao_personunit.get_plan_obj(rope=clean_couch_rope)
    wk_reason = clean_couch_plan.reasonunits.get(wk_rope)
    wk_case = wk_reason.cases.get(wk_rope)
    print(f"{clean_couch_plan.plan_label=} {wk_reason.reason_context=} {wk_case=}")
    assert wk_case.reason_divisor == 6 and wk_case.reason_lower == 1


def test_PersonUnit_conpute_SetsAttr_PlanUnits_active_personunit_v001():
    # ESTABLISH
    yao_personunit = personunit_v001()

    # WHEN
    yao_personunit.conpute()

    # THEN
    print(f"{len(yao_personunit._plan_dict)=}")
    # first_plan_kid_count = 0
    # first_plan_kid_none_count = 0
    # first_plan_kid_true_count = 0
    # first_plan_kid_false_count = 0
    # for plan in plan_list:
    #     if str(type(plan)).find(".plan.PlanUnit'>") > 0:
    #         first_plan_kid_count += 1
    #         if plan.plan_active is None:
    #             first_plan_kid_none_count += 1
    #         elif plan.plan_active:
    #             first_plan_kid_true_count += 1
    #         elif plan.plan_active is False:
    #             first_plan_kid_false_count += 1

    # print(f"{first_plan_kid_count=}")
    # print(f"{first_plan_kid_none_count=}")
    # print(f"{first_plan_kid_true_count=}")
    # print(f"{first_plan_kid_false_count=}")

    # plan_kid_count = 0
    # for plan in plan_list_without_planroot:
    #     plan_kid_count += 1
    #     print(f"{plan.plan_label=} {plan_kid_count=}")
    #     assert plan.plan_active is not None
    #     assert plan.plan_active in (True, False)
    # assert plan_kid_count == len(plan_list_without_planroot)

    assert len(yao_personunit._plan_dict) == sum(
        plan.plan_active is not None for plan in yao_personunit._plan_dict.values()
    )


def test_PersonUnit_conpute_EveryTwoMonthReturnsObj_personunit_v001():
    # ESTABLISH
    yao_personunit = personunit_v001()
    minute_str = "jour_minute"
    minute_rope = yao_personunit.make_l1_rope(minute_str)
    yao_personunit.add_fact(
        fact_context=minute_rope, fact_state=minute_rope, fact_lower=0, fact_upper=1399
    )
    month_str = "month_wk"
    month_rope = yao_personunit.make_l1_rope(month_str)
    yao_personunit.add_fact(fact_context=month_rope, fact_state=month_rope)
    nations_str = "Nation-States"
    nations_rope = yao_personunit.make_l1_rope(nations_str)
    yao_personunit.add_fact(fact_context=nations_rope, fact_state=nations_rope)
    mood_str = "Moods"
    mood_rope = yao_personunit.make_l1_rope(mood_str)
    yao_personunit.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_personunit.make_l1_rope(aaron_str)
    yao_personunit.add_fact(fact_context=aaron_rope, fact_state=aaron_rope)
    websites_str = "Websites"
    websites_rope = yao_personunit.make_l1_rope(websites_str)
    yao_personunit.add_fact(fact_context=websites_rope, fact_state=websites_rope)
    sem_jours_str = "sem_jours"
    sem_jours_rope = yao_personunit.make_l1_rope(sem_jours_str)
    yao_personunit.add_fact(fact_context=sem_jours_rope, fact_state=sem_jours_rope)
    plan_dict = yao_personunit.get_plan_dict()
    print(f"{len(plan_dict)=}")

    casa_rope = yao_personunit.make_l1_rope(exx.casa)
    clean_str = "cleaning"
    clean_rope = yao_personunit.make_rope(casa_rope, clean_str)
    mat_plan_label = "deep clean play mat"
    mat_rope = yao_personunit.make_rope(clean_rope, mat_plan_label)
    assert from_list_get_active(mat_rope, plan_dict) is False

    yr_month_reason_context = yao_personunit.make_l1_rope("yr_month")
    print(f"{yr_month_reason_context=}, {yr_month_reason_context=}")

    # WHEN
    yao_personunit.add_fact(
        yr_month_reason_context,
        fact_state=yr_month_reason_context,
        fact_lower=0,
        fact_upper=8,
    )
    ced_wk = yao_personunit.make_l1_rope("ced_wk")
    yao_personunit.add_fact(
        fact_context=ced_wk, fact_state=ced_wk, fact_lower=0, fact_upper=4
    )
    yao_personunit.conpute()

    # THEN
    print(f"{len(plan_dict)=}")
    print(f"{len(yao_personunit.planroot.factunits)=}")
    assert from_list_get_active(mat_rope, yao_personunit._plan_dict)


def test_PersonUnit_conpute_SetsEmpty_sum_healerunit_plans_fund_total():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    assert sue_personunit.sum_healerunit_plans_fund_total == 0
    assert sue_personunit._keep_dict == {}

    # WHEN
    sue_personunit.conpute()

    # THEN
    assert sue_personunit.sum_healerunit_plans_fund_total == 0
    assert sue_personunit._keep_dict == {}


def test_PersonUnit_conpute_Sets_sum_healerunit_plans_fund_total(graphics_bool):
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    sue_personunit.add_partnerunit("Sue")
    sue_personunit.conpute()
    nation_rope = sue_personunit.make_l1_rope("nation")
    usa_rope = sue_personunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_personunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({"Sue"})
    sue_personunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerunit=sue_healerunit
    )
    oregon_plan = sue_personunit.get_plan_obj(oregon_rope)
    print(f"{oregon_plan.fund_ratio=}")
    assert sue_personunit.sum_healerunit_plans_fund_total == 0
    assert oregon_plan.healerunit_ratio == 0

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert (
        sue_personunit.sum_healerunit_plans_fund_total
        == 0.038461539 * default_pool_num()
    )
    assert oregon_plan.healerunit_ratio == 1

    # WHEN
    wk_rope = sue_personunit.make_l1_rope("sem_jours")
    sue_personunit.edit_plan_attr(wk_rope, problem_bool=True)
    mon_rope = sue_personunit.make_rope(wk_rope, "Mon")
    sue_personunit.edit_plan_attr(mon_rope, healerunit=sue_healerunit)
    mon_plan = sue_personunit.get_plan_obj(mon_rope)
    # print(f"{mon_plan.problem_bool=} {mon_plan.fund_ratio=}")
    sue_personunit.conpute()
    # THEN
    assert (
        sue_personunit.sum_healerunit_plans_fund_total
        != 0.038461539 * default_pool_num()
    )
    assert (
        sue_personunit.sum_healerunit_plans_fund_total
        == 0.06923077 * default_pool_num()
    )
    assert oregon_plan.healerunit_ratio == 0.5555555571604938
    assert mon_plan.healerunit_ratio == 0.4444444428395062

    # WHEN
    tue_rope = sue_personunit.make_rope(wk_rope, "Tue")
    sue_personunit.edit_plan_attr(tue_rope, healerunit=sue_healerunit)
    tue_plan = sue_personunit.get_plan_obj(tue_rope)
    # print(f"{tue_plan.problem_bool=} {tue_plan.fund_ratio=}")
    # sat_rope = sue_personunit.make_rope(wk_rope, "Sat")
    # sat_plan = sue_personunit.get_plan_obj(sat_rope)
    # print(f"{sat_plan.problem_bool=} {sat_plan.fund_ratio=}")
    sue_personunit.conpute()

    # THEN
    assert (
        sue_personunit.sum_healerunit_plans_fund_total
        != 0.06923076923076923 * default_pool_num()
    )
    assert (
        sue_personunit.sum_healerunit_plans_fund_total
        == 0.100000001 * default_pool_num()
    )
    assert oregon_plan.healerunit_ratio == 0.38461538615384616
    assert mon_plan.healerunit_ratio == 0.3076923069230769
    assert tue_plan.healerunit_ratio == 0.3076923069230769

    # WHEN
    sue_personunit.edit_plan_attr(wk_rope, healerunit=sue_healerunit)
    wk_plan = sue_personunit.get_plan_obj(wk_rope)
    print(f"{wk_plan.plan_label=} {wk_plan.problem_bool=} {wk_plan.fund_ratio=}")
    sue_personunit.conpute()
    # THEN
    display_plantree(sue_personunit, "Keep", graphics_bool)
    assert sue_personunit.sum_healerunit_plans_fund_total == 0
    assert oregon_plan.healerunit_ratio == 0
    assert mon_plan.healerunit_ratio == 0
    assert tue_plan.healerunit_ratio == 0


def test_PersonUnit_conpute_Sets_keep_dict_v1(graphics_bool):
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    sue_personunit.add_partnerunit("Sue")
    sue_personunit.conpute()
    nation_rope = sue_personunit.make_l1_rope("nation")
    usa_rope = sue_personunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_personunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({"Sue"})
    sue_personunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerunit=sue_healerunit
    )
    assert len(sue_personunit._keep_dict) == 0
    assert sue_personunit._keep_dict.get(oregon_rope) is None

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert len(sue_personunit._keep_dict) == 1
    assert sue_personunit._keep_dict.get(oregon_rope) is not None

    # WHEN
    wk_rope = sue_personunit.make_l1_rope("sem_jours")
    sue_personunit.edit_plan_attr(wk_rope, problem_bool=True)
    mon_rope = sue_personunit.make_rope(wk_rope, "Mon")
    sue_personunit.edit_plan_attr(mon_rope, healerunit=sue_healerunit)
    # mon_plan = sue_personunit.get_plan_obj(mon_rope)
    # print(f"{mon_plan.problem_bool=} {mon_plan.fund_ratio=}")
    sue_personunit.conpute()
    # THEN
    assert len(sue_personunit._keep_dict) == 2
    assert sue_personunit._keep_dict.get(oregon_rope) is not None
    assert sue_personunit._keep_dict.get(mon_rope) is not None

    # WHEN
    tue_rope = sue_personunit.make_rope(wk_rope, "Tue")
    sue_personunit.edit_plan_attr(tue_rope, healerunit=sue_healerunit)
    # tue_plan = sue_personunit.get_plan_obj(tue_rope)
    # print(f"{tue_plan.problem_bool=} {tue_plan.fund_ratio=}")
    # sat_rope = sue_personunit.make_rope(wk_rope, "Sat")
    # sat_plan = sue_personunit.get_plan_obj(sat_rope)
    # print(f"{sat_plan.problem_bool=} {sat_plan.fund_ratio=}")
    sue_personunit.conpute()

    # THEN
    assert len(sue_personunit._keep_dict) == 3
    assert sue_personunit._keep_dict.get(oregon_rope) is not None
    assert sue_personunit._keep_dict.get(mon_rope) is not None
    assert sue_personunit._keep_dict.get(tue_rope) is not None

    # WHEN
    sue_personunit.edit_plan_attr(wk_rope, healerunit=sue_healerunit)
    wk_plan = sue_personunit.get_plan_obj(wk_rope)
    print(f"{wk_plan.plan_label=} {wk_plan.problem_bool=} {wk_plan.fund_ratio=}")
    sue_personunit.conpute()
    # THEN
    display_plantree(sue_personunit, "Keep", graphics_bool)
    assert len(sue_personunit._keep_dict) == 0
    assert sue_personunit._keep_dict == {}


def test_PersonUnit_conpute_Sets_healers_dict():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    sue_personunit.add_partnerunit(exx.sue)
    sue_personunit.add_partnerunit(exx.bob)
    assert sue_personunit._healers_dict == {}

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert sue_personunit._healers_dict == {}

    # ESTABLISH
    nation_rope = sue_personunit.make_l1_rope("nation")
    usa_rope = sue_personunit.make_rope(nation_rope, "USA")
    oregon_keep_rope = sue_personunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({exx.sue})
    sue_personunit.edit_plan_attr(
        oregon_keep_rope, problem_bool=True, healerunit=sue_healerunit
    )

    wk_rope = sue_personunit.make_l1_rope("sem_jours")
    bob_healerunit = healerunit_shop({exx.bob})
    sue_personunit.edit_plan_attr(wk_rope, problem_bool=True, healerunit=bob_healerunit)
    assert sue_personunit._healers_dict == {}

    # WHEN
    sue_personunit.conpute()

    # THEN
    assert len(sue_personunit._healers_dict) == 2
    wk_plan = sue_personunit.get_plan_obj(wk_rope)
    assert sue_personunit._healers_dict.get(exx.bob) == {wk_rope: wk_plan}
    oregon_plan = sue_personunit.get_plan_obj(oregon_keep_rope)
    assert sue_personunit._healers_dict.get(exx.sue) == {oregon_keep_rope: oregon_plan}


def test_PersonUnit_conpute_Sets_keeps_buildable_True():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    sue_personunit.add_partnerunit(exx.sue)
    sue_personunit.add_partnerunit(exx.bob)
    assert sue_personunit.keeps_buildable is False

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert sue_personunit.keeps_buildable

    # ESTABLISH
    nation_rope = sue_personunit.make_l1_rope("nation")
    usa_rope = sue_personunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_personunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({exx.sue})
    sue_personunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerunit=sue_healerunit
    )

    wk_rope = sue_personunit.make_l1_rope("sem_jours")
    bob_healerunit = healerunit_shop({exx.bob})
    sue_personunit.edit_plan_attr(wk_rope, problem_bool=True, healerunit=bob_healerunit)

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert sue_personunit.keeps_buildable


def test_PersonUnit_conpute_Sets_keeps_buildable_False():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()
    sue_personunit.add_partnerunit(exx.sue)
    sue_personunit.add_partnerunit(exx.bob)
    assert sue_personunit.keeps_buildable is False

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert sue_personunit.keeps_buildable

    # ESTABLISH
    nation_rope = sue_personunit.make_l1_rope("nation")
    usa_rope = sue_personunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_personunit.make_rope(usa_rope, "Oregon")
    bend_str = "Be/nd"
    bend_rope = sue_personunit.make_rope(oregon_rope, bend_str)
    sue_personunit.set_plan_obj(planunit_shop(bend_str), oregon_rope)
    sue_healerunit = healerunit_shop({exx.sue})
    sue_personunit.edit_plan_attr(
        bend_rope, problem_bool=True, healerunit=sue_healerunit
    )
    assert sue_personunit.keeps_buildable

    # WHEN
    sue_personunit.conpute()
    # THEN
    assert sue_personunit.keeps_buildable is False
