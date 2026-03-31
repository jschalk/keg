from src.ch03_workforce.workforce import workforceunit_shop
from src.ch04_rope.rope import RopeTerm
from src.ch06_plan.plan import PlanUnit, planunit_shop
from src.ch07_person_logic.person_main import get_personunit_from_dict, personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_with7am_clean_table_reason,
    get_personunit_with_4_levels,
    get_personunit_with_4_levels_and_2reasons,
    get_personunit_with_4_levels_and_2reasons_2facts,
    personunit_v001,
    personunit_v001_with_large_agenda,
    personunit_v002,
)
from src.ref.keywords import ExampleStrs as exx


def get_case_tasks_count(agenda_dict: dict[RopeTerm, PlanUnit]) -> int:
    return sum(bool(x_planunit.plan_task) for x_planunit in agenda_dict.values())


def test_PersonUnit_get_agenda_dict_ReturnsObj_WithTwoPlans():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()

    # WHEN
    agenda_dict = sue_person.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert sue_person.make_l1_rope("casa") in agenda_dict.keys()
    assert sue_person.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_PersonUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectPlans():
    # ESTABLISH
    x_person = get_personunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = x_person.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = x_person.make_rope(wk_rope, sun_str)
    x_person.add_fact(fact_context=wk_rope, fact_state=sun_rope)

    # WHEN
    agenda_dict = x_person.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_person.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_PersonUnit_get_agenda_dict_WithLargePerson_fund():
    # ESTABLISH
    x_person = get_personunit_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_person.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_person.make_l1_rope("cat have dinner")).fund_ratio

    print(f"{agenda_dict.keys()=} {x_person.make_l1_rope(exx.casa)=}")
    print(f"{agenda_dict.get(x_person.make_l1_rope(exx.casa)).plan_label=}")
    assert agenda_dict.get(x_person.make_l1_rope(exx.casa)).fund_ratio


def test_PersonUnit_get_agenda_dict_WithNo7amPlanExample():
    # ESTABLISH
    x_person = get_personunit_with7am_clean_table_reason()

    # WHEN
    agenda_dict = x_person.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_str = "clean table"
    print(f"{agenda_dict.keys()=} {x_person.make_l1_rope(clean_str)=}")
    # print(f"{agenda_dict[0].plan_label=}")
    assert len(agenda_dict) == 1

    cat_str = "cat have dinner"
    cat_agenda_plan = agenda_dict.get(x_person.make_l1_rope(cat_str))
    assert cat_agenda_plan.plan_label != clean_str


def test_PersonUnit_get_agenda_dict_With7amPlanExample():
    # ESTABLISH
    # set facts as midevening to 8am
    x_person = get_personunit_with7am_clean_table_reason()
    print(f"{len(x_person.get_agenda_dict())=}")
    assert len(x_person.get_agenda_dict()) == 1
    ziettech_rope = x_person.make_l1_rope("ziettech")
    x24hr_rope = x_person.make_rope(ziettech_rope, "24hr")
    x24hr_reason_lower = 0.0
    x24hr_reason_upper = 8.0
    houseadministration_str = "houseadministration"
    houseadministration_rope = x_person.make_l1_rope(houseadministration_str)
    clean_str = "clean table"
    clean_rope = x_person.make_rope(houseadministration_rope, clean_str)

    # WHEN
    x_person.add_fact(
        x24hr_rope, x24hr_rope, x24hr_reason_lower, x24hr_reason_upper, True
    )

    # THEN
    print(x_person.planroot.factunits[x24hr_rope])
    print(x_person.get_plan_obj(clean_rope).reasonunits)
    print(x_person.get_plan_obj(clean_rope).plan_active)
    agenda_dict = x_person.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_plan = agenda_dict.get(clean_rope)
    assert clean_plan.plan_label == clean_str


def test_personunit_v001_AgendaExists():
    # ESTABLISH
    yao_person = personunit_v001()
    min_str = "jour_minute"
    min_rope = yao_person.make_l1_rope(min_str)
    yao_person.add_fact(
        fact_context=min_rope, fact_state=min_rope, fact_lower=0, fact_upper=1399
    )
    assert yao_person
    # for plan_kid in yao_person.planroot.kids.values():
    #     # print(plan_kid.plan_label)
    #     assert str(type(plan_kid)) != "<class 'str'>"
    #     assert plan_kid.pledge is not None

    # WHEN
    agenda_dict = yao_person.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].pledge is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_PersonUnit_get_agenda_dict_PersonUnitHasCorrectAttributes_personunit_v001():
    # ESTABLISH
    yao_person = personunit_v001()

    jour_min_str = "jour_minute"
    jour_min_rope = yao_person.make_l1_rope(jour_min_str)
    yao_person.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=1399,
    )
    month_wk_str = "month_wk"
    month_wk_rope = yao_person.make_l1_rope(month_wk_str)
    nations_str = "Nation-States"
    nations_rope = yao_person.make_l1_rope(nations_str)
    mood_str = "Moods"
    mood_rope = yao_person.make_l1_rope(mood_str)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_person.make_l1_rope(aaron_str)
    # websites_str = "Websites"
    # websites_rope = yao_person.make_l1_rope(websites_str)
    yr_month_str = "yr_month"
    yr_month_rope = yao_person.make_l1_rope(yr_month_str)
    yao_person.add_fact(fact_context=month_wk_rope, fact_state=month_wk_rope)
    yao_person.add_fact(fact_context=nations_rope, fact_state=nations_rope)
    yao_person.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    yao_person.add_fact(fact_context=aaron_rope, fact_state=aaron_rope)
    # yao_person.add_fact(fact_context=websites_rope, fact_state=websites_rope)
    yao_person.add_fact(fact_context=yr_month_rope, fact_state=yr_month_rope)
    # season_str = "Seasons"
    # season_rope = yao_person.make_l1_rope(season_str)
    # yao_person.add_fact(fact_context=season_rope, fact_state=season_rope)
    ced_wk_str = "ced_wk"
    ced_wk_rope = yao_person.make_l1_rope(ced_wk_str)
    yao_person.add_fact(fact_context=ced_wk_rope, fact_state=ced_wk_rope)
    # water_str = "WaterExistence"
    # water_rope = yao_person.make_l1_rope(water_str)
    # yao_person.add_fact(fact_context=water_rope, fact_state=water_rope)
    # movie_str = "No Movie playing"
    # movie_rope = yao_person.make_l1_rope(movie_str)
    # yao_person.add_fact(fact_context=movie_rope, fact_state=movie_str)

    # WHEN
    plan_pledge_list = yao_person.get_agenda_dict()

    # THEN
    assert len(plan_pledge_list) == 27

    wk1_rope = yao_person.make_rope(month_wk_rope, "1st wk")
    yao_person.add_fact(month_wk_rope, wk1_rope)
    plan_pledge_list = yao_person.get_agenda_dict()
    assert len(plan_pledge_list) == 27

    sem_jour_str = "sem_jours"
    sem_jour_rope = yao_person.make_l1_rope(sem_jour_str)
    mon_str = "Mon"
    mon_rope = yao_person.make_rope(sem_jour_rope, mon_str)

    yao_person.add_fact(fact_context=sem_jour_rope, fact_state=mon_rope)
    plan_pledge_list = yao_person.get_agenda_dict()
    assert len(plan_pledge_list) == 39

    yao_person.add_fact(fact_context=sem_jour_rope, fact_state=sem_jour_rope)
    plan_pledge_list = yao_person.get_agenda_dict()
    assert len(plan_pledge_list) == 53

    # yao_person.add_fact(fact_context=nations_rope, fact_state=nations_rope)
    # plan_pledge_list = yao_person.get_agenda_dict()
    # assert len(plan_pledge_list) == 53

    # for reason_context in yao_person.get_missing_fact_reason_contexts():
    #     print(f"{reason_context=}")

    # for agenda_plan in plan_pledge_list:
    #     print(f"{agenda_plan.plan_uid=} {agenda_plan.parent_rope=}")

    # for agenda_plan in plan_pledge_list:
    #     # print(f"{agenda_plan.parent_rope=}")
    #     pass

    print(len(plan_pledge_list))


def test_PersonUnit_get_agenda_dict_PersonUnitCanCleanOn_reason_context_personunit_v001_with_large_agenda():
    # ESTABLISH
    yao_person = personunit_v001_with_large_agenda()
    wk_str = "sem_jours"
    wk_rope = yao_person.make_l1_rope(wk_str)
    print(f"{type(yao_person)=}")
    # for reason_context in yao_person.get_missing_fact_reason_contexts():
    #     print(f"{reason_context=}")

    # for agenda_plan in yao_person.get_agenda_dict():
    #     print(
    #         f"{agenda_plan.parent_rope=} {agenda_plan.plan_label} {len(agenda_plan.reasonunits)=}"
    #     )
    #     for reason in agenda_plan.reasonunits.values():
    #         if reason.reason_context == sem_jours:
    #             print(f"         {sem_jours}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(yao_person.get_agenda_dict()) == 69

    # WHEN
    pledge_list = yao_person.get_agenda_dict(necessary_reason_context=wk_rope)

    # THEN
    assert len(pledge_list) != 69
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(pledge_list) == 29


def test_PersonUnit_set_agenda_case_task_as_complete_SetsAttr_Range():
    # ESTABLISH
    zia_person = personunit_shop("Zia")

    run_str = "run"
    run_rope = zia_person.make_l1_rope(run_str)
    ziet_rope = zia_person.make_l1_rope("ziet")
    jour_str = "jour"
    jour_rope = zia_person.make_rope(ziet_rope, jour_str)

    zia_person.set_l1_plan(planunit_shop(run_str, pledge=True))
    zia_person.set_plan_obj(planunit_shop(jour_str, begin=0, close=500), ziet_rope)
    zia_person.edit_plan_attr(
        run_rope,
        reason_context=jour_rope,
        reason_case=jour_rope,
        reason_lower=25,
        reason_upper=81,
    )
    zia_person.add_fact(
        fact_context=jour_rope, fact_state=jour_rope, fact_lower=30, fact_upper=87
    )
    zia_person.get_agenda_dict()
    run_reasonunits = zia_person.planroot.kids[run_str].reasonunits[jour_rope]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.cases[jour_rope].case_active=}")
    print(f"{run_reasonunits.cases[jour_rope].case_task=}")
    print(f"{zia_person.get_reason_contexts()=}")
    assert len(zia_person.get_plan_dict()) == 4
    assert len(zia_person.get_agenda_dict()) == 1
    print(f"{zia_person.get_agenda_dict().keys()=}")
    assert zia_person.get_agenda_dict().get(run_rope).plan_task is True

    # WHEN
    zia_person.set_agenda_plan_task_complete(
        plan_task_rope=run_rope, reason_context=jour_rope
    )

    # THEN
    agenda_dict = zia_person.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_PersonUnit_set_agenda_case_task_as_complete_SetsAttr_Division():
    # ESTABLISH
    zia_person = personunit_shop("Zia")

    run_str = "run"
    run_rope = zia_person.make_l1_rope(run_str)
    ziet_str = "ziet"
    ziet_rope = zia_person.make_l1_rope(ziet_str)
    jour_str = "jour"
    jour_rope = zia_person.make_rope(ziet_rope, jour_str)

    zia_person.set_l1_plan(planunit_shop(run_str, pledge=True))
    zia_person.set_plan_obj(planunit_shop(jour_str, begin=0, close=500), ziet_rope)
    zia_person.edit_plan_attr(
        run_rope,
        reason_context=jour_rope,
        reason_case=jour_rope,
        reason_lower=1,
        reason_upper=1,
        reason_divisor=2,
    )

    run_plan = zia_person.get_plan_obj(run_rope)
    # print(f"{run_plan.factheirs=}")
    zia_person.add_fact(
        fact_context=jour_rope, fact_state=jour_rope, fact_lower=1, fact_upper=2
    )
    assert len(zia_person.get_agenda_dict()) == 1
    zia_person.add_fact(
        fact_context=jour_rope, fact_state=jour_rope, fact_lower=2, fact_upper=2
    )
    assert len(zia_person.get_agenda_dict()) == 0
    zia_person.add_fact(
        fact_context=jour_rope, fact_state=jour_rope, fact_lower=400, fact_upper=400
    )
    assert len(zia_person.get_agenda_dict()) == 0
    zia_person.add_fact(
        fact_context=jour_rope, fact_state=jour_rope, fact_lower=401, fact_upper=402
    )
    assert len(zia_person.get_agenda_dict()) == 1
    # print(f"{run_plan.factheirs=}")
    print(f"{run_plan.factunits=}")

    # WHEN
    zia_person.set_agenda_plan_task_complete(
        plan_task_rope=run_rope, reason_context=jour_rope
    )

    # THEN
    print(f"{run_plan.factunits=}")
    # print(f"{run_plan.factheirs=}")
    assert len(zia_person.get_agenda_dict()) == 0


def test_get_personunit_from_dict_LoadsPledgeFromJSON():
    # ESTABLISH
    yao_person_dict = personunit_v001().to_dict()

    # WHEN
    yao_person = get_personunit_from_dict(person_dict=yao_person_dict)

    # THEN
    assert len(yao_person.get_plan_dict()) == 252
    print(f"{len(yao_person.get_plan_dict())=}")
    casa_rope = yao_person.make_l1_rope(exx.casa)
    body_str = "exercise"
    body_rope = yao_person.make_rope(casa_rope, body_str)
    veg_str = "veggies every morning"
    veg_rope = yao_person.make_rope(body_rope, veg_str)
    veg_plan = yao_person.get_plan_obj(veg_rope)
    assert not veg_plan.plan_active
    assert veg_plan.pledge

    # plan_list = yao_person.get_plan_dict()
    # pledge_true_count = 0
    # for plan in plan_list:
    #     if str(type(plan)).find(".plan.PlanUnit'>") > 0:
    #         assert plan.plan_active in (True, False)
    #     assert plan.pledge in (True, False)
    #     # if plan.plan_active:
    #     #     print(plan.plan_label)
    #     if plan.pledge:
    #         pledge_true_count += 1
    #         # if plan.pledge is False:
    #         #     print(f"pledge is false {plan.plan_label}")
    #         # for reason in plan.reasonunits.values():
    #         #     assert reason.reason_active in (True, False)
    # assert pledge_true_count > 0

    # WHEN
    jour_min_str = "jour_minute"
    jour_min_rope = yao_person.make_l1_rope(jour_min_str)
    yao_person.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=1399,
    )

    # THEN
    assert len(yao_person.get_agenda_dict()) > 0


def test_PersonUnit_set_fact_Isue116Resolved_Setscase_taskAsTrue():
    # ESTABLISH
    yao_person = personunit_v002()
    print(f"{yao_person.get_reason_contexts()=}")

    assert len(yao_person.get_agenda_dict()) == 44
    ziet_rope = yao_person.make_l1_rope("ziet")
    gregziet_rope = yao_person.make_rope(ziet_rope, "gregziet")

    # WHEN
    yao_person.add_fact(
        gregziet_rope, gregziet_rope, fact_lower=1063998720, fact_upper=1064130373
    )
    pledge_plan_list = yao_person.get_agenda_dict()

    # THEN
    assert len(pledge_plan_list) == 66
    db_rope = yao_person.make_l1_rope("D&B")
    evening_str = "late_evening_go_to_sleep"
    evening_rope = yao_person.make_rope(db_rope, evening_str)
    evening_plan = yao_person._plan_dict.get(evening_rope)
    # for plan_x in yao_person.get_agenda_dict():
    #     # if plan_x.case_task != True:
    #     #     print(f"{len(pledge_plan_list)=} {plan_x.case_task=} {plan_x.get_plan_rope()}")
    #     if plan_x.plan_label == evening_plan_label:
    #         evening_plan = plan_x
    #         print(f"{plan_x.get_plan_rope()=}")

    print(f"\nPlan = '{evening_str}' and reason '{gregziet_rope}'")
    factheir_gregziet = evening_plan.factheirs.get(gregziet_rope)
    print(f"\n{factheir_gregziet=}")

    # for reasonheir in agenda_plan.reasonheirs.values():
    #     print(f"{reasonheir.reason_context=} {reasonheir.reason_active=} {reasonheir.reason_task=}")
    reasonheir_gregziet = evening_plan.reasonheirs.get(gregziet_rope)
    reasonheir_str = f"\nreasonheir_gregziet= '{reasonheir_gregziet.reason_context}', reason_active={reasonheir_gregziet.reason_active}, case_task={reasonheir_gregziet.reason_task}"
    print(reasonheir_str)

    caseunit = reasonheir_gregziet.cases.get(gregziet_rope)
    print(f"----\n {caseunit=}")
    print(f" {caseunit._get_case_task_bool(factheir=factheir_gregziet)=}")
    print(f" {caseunit.case_active=} , {caseunit._is_range()=} caseunit fails")
    print(f" {caseunit.case_active=} , {caseunit._is_segregate()=} caseunit passes")

    # print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_case_task_bool()=}")
    assert get_case_tasks_count(pledge_plan_list) == 64


def test_PersonUnit_agenda_IsSetByWorkforceUnit_1PartnerGroup():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    casa_rope = yao_person.make_l1_rope(exx.casa)
    yao_person.set_l1_plan(planunit_shop(exx.casa, pledge=True))
    assert len(yao_person.get_agenda_dict()) == 1

    yao_person.add_partnerunit(exx.sue)
    workforceunit_sue = workforceunit_shop()
    workforceunit_sue.add_labor(labor_title=exx.sue)
    assert len(yao_person.get_agenda_dict()) == 1

    # WHEN
    yao_person.edit_plan_attr(casa_rope, workforceunit=workforceunit_sue)

    # THEN
    assert len(yao_person.get_agenda_dict()) == 0

    # WHEN
    yao_person.add_partnerunit(exx.yao)
    workforceunit_yao = workforceunit_shop()
    workforceunit_yao.add_labor(labor_title=exx.yao)

    # WHEN
    yao_person.edit_plan_attr(casa_rope, workforceunit=workforceunit_yao)

    # THEN
    assert len(yao_person.get_agenda_dict()) == 1

    # agenda_dict = yao_person.get_agenda_dict()
    # print(f"{agenda_dict[0].plan_label=}")


def test_PersonUnit_get_agenda_dict_IsSetByWorkforceUnit_2PartnerGroup():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_partnerunit(exx.yao)
    casa_rope = yao_person.make_l1_rope(exx.casa)
    yao_person.set_l1_plan(planunit_shop(exx.casa, pledge=True))

    yao_person.add_partnerunit(exx.sue)
    sue_partnerunit = yao_person.get_partner(exx.sue)
    sue_partnerunit.add_membership(exx.run)

    run_workforceunit = workforceunit_shop()
    run_workforceunit.add_labor(labor_title=exx.run)
    assert len(yao_person.get_agenda_dict()) == 1

    # WHEN
    yao_person.edit_plan_attr(casa_rope, workforceunit=run_workforceunit)

    # THEN
    assert len(yao_person.get_agenda_dict()) == 0

    # WHEN
    yao_partnerunit = yao_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)

    # THEN
    assert len(yao_person.get_agenda_dict()) == 1


def test_PersonUnit_get_all_pledges_ReturnsObj():
    # ESTABLISH
    zia_person = personunit_shop(exx.zia)
    casa_rope = zia_person.make_l1_rope(exx.casa)
    clean_rope = zia_person.make_rope(casa_rope, exx.clean)

    sweep_rope = zia_person.make_rope(clean_rope, exx.sweep)
    couch_str = "couch"
    couch_rope = zia_person.make_rope(casa_rope, couch_str)
    zia_person.set_plan_obj(planunit_shop(couch_str), casa_rope)
    zia_person.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    zia_person.set_plan_obj(planunit_shop(exx.sweep, pledge=True), clean_rope)
    sweep_plan = zia_person.get_plan_obj(sweep_rope)
    zia_person.add_partnerunit(exx.yao)
    sweep_plan.workforceunit.add_labor(exx.yao)
    print(f"{sweep_plan}")
    agenda_dict = zia_person.get_agenda_dict()
    assert agenda_dict.get(clean_rope) is not None
    assert agenda_dict.get(sweep_rope) is None
    assert agenda_dict.get(couch_rope) is None

    # WHEN
    all_pledges_dict = zia_person.get_all_pledges()

    # THEN
    assert all_pledges_dict.get(sweep_rope) == zia_person.get_plan_obj(sweep_rope)
    assert all_pledges_dict.get(clean_rope) == zia_person.get_plan_obj(clean_rope)
    assert all_pledges_dict.get(couch_rope) is None
