from pytest import raises as pytest_raises
from src.ch02_contact.group import awardunit_shop
from src.ch03_workforce.workforce import workforceunit_shop
from src.ch04_rope.rope import create_rope, default_knot_if_None, is_sub_rope, to_rope
from src.ch05_reason.reason_main import caseunit_shop, factunit_shop, reasonunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_plan_ScenarioXX_RaisesErrorWhen_parent_rope_IsInvalid():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    invalid_rootlabel_bowl_rope = create_rope("bowling")
    casa_plan = planunit_shop(exx.casa)
    assert invalid_rootlabel_bowl_rope != zia_person.planroot.get_plan_rope()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_person.set_plan_obj(casa_plan, parent_rope=invalid_rootlabel_bowl_rope)
    exception_str = f"set_plan failed because parent_rope '{invalid_rootlabel_bowl_rope}' has an invalid root rope. Should be {zia_person.planroot.get_plan_rope()}."
    assert str(excinfo.value) == exception_str


def test_PersonUnit_set_plan_ScenarioXX_RaisesErrorWhen_parent_rope_PlanDoesNotExist():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    bowl_rope = zia_person.make_l1_rope("bowling")

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_person.set_plan_obj(
            planunit_shop(exx.casa),
            parent_rope=bowl_rope,
            create_missing_ancestors=False,
        )
    exception_str = f"set_plan failed because '{bowl_rope}' plan does not exist."
    assert str(excinfo.value) == exception_str


def test_PersonUnit_set_plan_ScenarioXX_RaisesErrorWhen_plan_label_IsNotLabel():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    bowl_rope = zia_person.make_l1_rope("bowling")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    run_str = "run"
    run_rope = zia_person.make_rope(casa_rope, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_person.set_plan_obj(planunit_shop(run_rope), parent_rope=bowl_rope)
    exception_str = f"set_plan failed because '{run_rope}' is not a LabelTerm."
    assert str(excinfo.value) == exception_str


def test_PersonUnit_set_plan_ScenarioXX_SetsAttr():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    root_plan_rope = zia_person.planroot.get_plan_rope()
    assert not zia_person.planroot.kids.get(exx.casa)

    # WHEN
    zia_person.set_plan_obj(planunit_shop(exx.casa), parent_rope=root_plan_rope)

    # THEN
    print(f"{zia_person.planroot.kids.keys()=}")
    assert zia_person.planroot.kids.get(exx.casa)


def test_PersonUnit_plan_exists_ReturnsObj():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    assert zia_person.plan_exists(casa_rope) is False

    # WHEN
    zia_person.set_plan_obj(
        planunit_shop(exx.casa), parent_rope=zia_person.planroot.get_plan_rope()
    )

    # THEN
    assert zia_person.plan_exists(casa_rope)


def test_PersonUnit_set_l1_plan_SetsAttr():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    assert not zia_person.planroot.kids.get(casa_rope)

    # WHEN
    zia_person.set_l1_plan(planunit_shop(exx.casa))

    # THEN
    assert not zia_person.planroot.kids.get(casa_rope)


def test_PersonUnit_add_plan_SetsAttr_Scenario0():
    # ESTABLISH
    bob_personunit = personunit_shop(exx.bob, knot=exx.slash)
    casa_rope = bob_personunit.make_l1_rope("casa")
    assert not bob_personunit.plan_exists(casa_rope)

    # WHEN
    bob_personunit.add_plan(casa_rope)

    # THEN
    assert bob_personunit.plan_exists(casa_rope)
    casa_planunit = bob_personunit.get_plan_obj(casa_rope)
    assert casa_planunit.knot == bob_personunit.knot
    assert not casa_planunit.pledge


def test_PersonUnit_add_plan_SetsAttr_Scenario1():
    # ESTABLISH
    bob_personunit = personunit_shop(exx.bob)
    casa_rope = bob_personunit.make_l1_rope("casa")
    casa_star = 13
    casa_pledge = True

    # WHEN
    bob_personunit.add_plan(casa_rope, star=casa_star, pledge=casa_pledge)

    # THEN
    casa_planunit = bob_personunit.get_plan_obj(casa_rope)
    assert casa_planunit.star == casa_star
    assert casa_planunit.pledge


def test_PersonUnit_add_plan_ReturnsObj():
    # ESTABLISH
    bob_personunit = personunit_shop(exx.bob)
    casa_rope = bob_personunit.make_l1_rope("casa")
    casa_star = 13

    # WHEN
    casa_planunit = bob_personunit.add_plan(casa_rope, star=casa_star)

    # THEN
    assert casa_planunit.plan_label == "casa"
    assert casa_planunit.star == casa_star


def test_PersonUnit_set_plan_ScenarioXX_AddsPlanObjWithNonDefault_knot():
    # ESTABLISH
    assert exx.slash != default_knot_if_None()
    bob_person = personunit_shop("Bob", knot=exx.slash)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    wk_rope = bob_person.make_l1_rope(exx.wk)
    wed_rope = bob_person.make_rope(wk_rope, exx.wed)
    bob_person.set_l1_plan(planunit_shop(exx.casa))
    bob_person.set_l1_plan(planunit_shop(exx.wk))
    bob_person.set_plan_obj(planunit_shop(exx.wed), wk_rope)
    print(f"{bob_person.planroot.kids.keys()=}")
    assert len(bob_person.planroot.kids) == 2
    wed_plan = bob_person.get_plan_obj(wed_rope)
    assert wed_plan.knot == exx.slash
    assert wed_plan.knot == bob_person.knot

    # WHEN
    bob_person.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan = bob_person.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits.get(wk_rope) is not None


def test_PersonUnit_set_plan_ScenarioXX_CanCreateMissingPlanUnits():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    ww2_rope = sue_person.make_l1_rope("ww2")
    battles_rope = sue_person.make_rope(ww2_rope, "battles")
    coralsea_rope = sue_person.make_rope(battles_rope, "coralsea")
    saratoga_plan = planunit_shop("USS Saratoga")
    assert sue_person.plan_exists(battles_rope) is False
    assert sue_person.plan_exists(coralsea_rope) is False

    # WHEN
    sue_person.set_plan_obj(saratoga_plan, parent_rope=coralsea_rope)

    # THEN
    assert sue_person.plan_exists(battles_rope)
    assert sue_person.plan_exists(coralsea_rope)


def test_PersonUnit_del_plan_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    root_rope = sue_person.planroot.get_plan_rope()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.del_plan_obj(rope=root_rope)
    assert str(excinfo.value) == "Planroot cannot be deleted"


def test_PersonUnit_del_plan_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_person.make_rope(wk_rope, sun_str)
    assert sue_person.get_plan_obj(wk_rope)
    assert sue_person.get_plan_obj(sun_rope)

    # WHEN
    sue_person.del_plan_obj(rope=wk_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_obj(wk_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{wk_rope}'"
    new_sun_rope = sue_person.make_l1_rope("Sun")
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_obj(new_sun_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{new_sun_rope}'"


def test_PersonUnit_del_plan_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    sun_str = "Sun"
    old_sun_rope = sue_person.make_rope(wk_rope, sun_str)
    assert sue_person.get_plan_obj(old_sun_rope)

    # WHEN
    sue_person.del_plan_obj(rope=wk_rope, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_obj(old_sun_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{old_sun_rope}'"
    new_sun_rope = sue_person.make_l1_rope(sun_str)
    assert sue_person.get_plan_obj(new_sun_rope)
    new_sun_plan = sue_person.get_plan_obj(new_sun_rope)
    assert new_sun_plan.parent_rope == sue_person.planroot.get_plan_rope()


def test_PersonUnit_del_plan_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_person.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_rope = sue_person.make_rope(usa_rope, texas_str)
    usa_oregon_rope = sue_person.make_rope(usa_rope, oregon_str)
    nation_texas_rope = sue_person.make_rope(nation_rope, texas_str)
    nation_oregon_rope = sue_person.make_rope(nation_rope, oregon_str)
    assert sue_person.plan_exists(usa_rope)
    assert sue_person.plan_exists(usa_texas_rope)
    assert sue_person.plan_exists(usa_oregon_rope)
    assert sue_person.plan_exists(nation_texas_rope) is False
    assert sue_person.plan_exists(nation_oregon_rope) is False

    # WHEN
    sue_person.del_plan_obj(rope=usa_rope, del_children=False)

    # THEN
    assert sue_person.plan_exists(nation_texas_rope)
    assert sue_person.plan_exists(nation_oregon_rope)
    assert sue_person.plan_exists(usa_texas_rope) is False
    assert sue_person.plan_exists(usa_oregon_rope) is False
    assert sue_person.plan_exists(usa_rope) is False


def test_PersonUnit_del_plan_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sem_jour_rope = sue_person.make_l1_rope("sem_jours")
    mon_rope = sue_person.make_rope(sem_jour_rope, "Mon")
    assert sue_person.get_plan_obj(mon_rope)

    # WHEN
    sue_person.del_plan_obj(rope=mon_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_obj(mon_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{mon_rope}'"


def test_PersonUnit_del_plan_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_person.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    usa_texas_rope = sue_person.make_rope(usa_rope, texas_str)
    assert sue_person.get_plan_obj(usa_texas_rope)

    # WHEN
    sue_person.del_plan_obj(rope=usa_texas_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_obj(usa_texas_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{usa_texas_rope}'"


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario00_Star():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    print(f"{casa_rope=}")
    old_star = sue_person.planroot.kids[exx.casa].star
    assert old_star == 30

    # WHEN
    sue_person.edit_plan_attr(casa_rope, star=23)

    # THEN
    new_star = sue_person.planroot.kids[exx.casa].star
    assert new_star == 23


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario01_plan_uid():
    # ESTABLISH:
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # plan_uid: int = None,
    sue_person.planroot.kids[exx.casa].plan_uid = 34
    x_plan_uid = sue_person.planroot.kids[exx.casa].plan_uid
    assert x_plan_uid == 34

    # WHEN
    sue_person.edit_plan_attr(casa_rope, plan_uid=23)

    # THEN
    plan_uid_new = sue_person.planroot.kids[exx.casa].plan_uid
    assert plan_uid_new == 23


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario02_begin_close():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # begin: float = None,
    # close: float = None,
    sue_person.planroot.kids[exx.casa].begin = 39
    x_begin = sue_person.planroot.kids[exx.casa].begin
    assert x_begin == 39

    # WHEN
    sue_person.planroot.kids[exx.casa].close = 43

    # THEN
    x_close = sue_person.planroot.kids[exx.casa].close
    assert x_close == 43

    # WHEN
    sue_person.edit_plan_attr(casa_rope, begin=25, close=29)

    # THEN
    assert sue_person.planroot.kids[exx.casa].begin == 25
    assert sue_person.planroot.kids[exx.casa].close == 29


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario03_gogo_want_stop_want():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # gogo_want: float = None,
    # stop_want: float = None,
    sue_person.planroot.kids[exx.casa].gogo_want = 439
    x_gogo_want = sue_person.planroot.kids[exx.casa].gogo_want
    assert x_gogo_want == 439

    # WHEN
    sue_person.planroot.kids[exx.casa].stop_want = 443

    # THEN
    x_stop_want = sue_person.planroot.kids[exx.casa].stop_want
    assert x_stop_want == 443

    # WHEN
    sue_person.edit_plan_attr(casa_rope, gogo_want=425, stop_want=429)

    # THEN
    assert sue_person.planroot.kids[exx.casa].gogo_want == 425
    assert sue_person.planroot.kids[exx.casa].stop_want == 429


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario04_factunits():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # factunit: factunit_shop = None,
    # sue_person.planroot.kids[exx.casa].factunits = None
    assert sue_person.planroot.kids[exx.casa].factunits == {}
    sem_jours_rope = sue_person.make_l1_rope("sem_jours")
    fact_rope = sue_person.make_rope(sem_jours_rope, "Sun")
    x_factunit = factunit_shop(fact_context=fact_rope, fact_state=fact_rope)

    casa_factunits = sue_person.planroot.kids[exx.casa].factunits
    print(f"{casa_factunits=}")

    # WHEN
    sue_person.edit_plan_attr(casa_rope, factunit=x_factunit)
    casa_factunits = sue_person.planroot.kids[exx.casa].factunits
    print(f"{casa_factunits=}")

    # THEN
    assert sue_person.planroot.kids[exx.casa].factunits == {
        x_factunit.fact_context: x_factunit
    }


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario05_awardunit():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # awardunit: dict = None,
    sue_person.planroot.kids[exx.casa].awardunits = {
        "fun": awardunit_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    awardunits = sue_person.planroot.kids[exx.casa].awardunits
    assert awardunits == {
        "fun": awardunit_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    x_awardunit = awardunit_shop(awardee_title="fun", give_force=4, take_force=8)

    # WHEN
    sue_person.edit_plan_attr(casa_rope, awardunit=x_awardunit)

    # THEN
    assert sue_person.planroot.kids[exx.casa].awardunits == {"fun": x_awardunit}


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario06_is_expanded():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # is_expanded: dict = None,
    sue_person.planroot.kids[exx.casa].is_expanded = "what"
    is_expanded = sue_person.planroot.kids[exx.casa].is_expanded
    assert is_expanded == "what"

    # WHEN
    sue_person.edit_plan_attr(casa_rope, is_expanded=True)

    # THEN
    assert sue_person.planroot.kids[exx.casa].is_expanded is True


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario07_pledge():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # pledge: dict = None,
    sue_person.planroot.kids[exx.casa].pledge = "funfun3"
    pledge = sue_person.planroot.kids[exx.casa].pledge
    assert pledge == "funfun3"

    # WHEN
    sue_person.edit_plan_attr(casa_rope, pledge=True)

    # THEN
    assert sue_person.planroot.kids[exx.casa].pledge is True


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario08_healerunit():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # healerunit:
    sue_person.planroot.kids[exx.casa].healerunit = "fun3rol"
    src_healerunit = sue_person.planroot.kids[exx.casa].healerunit
    assert src_healerunit == "fun3rol"

    # WHEN
    x_healerunit = healerunit_shop({exx.sue, exx.yao})
    sue_person.add_contactunit(exx.sue)
    sue_person.add_contactunit(exx.yao)
    sue_person.edit_plan_attr(casa_rope, healerunit=x_healerunit)

    # THEN
    assert sue_person.planroot.kids[exx.casa].healerunit == x_healerunit


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario09_problem_bool():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    # _problem_bool: bool
    sue_person.planroot.kids[exx.casa].problem_bool = "fun3rol"
    src_problem_bool = sue_person.planroot.kids[exx.casa].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True

    # WHEN
    sue_person.edit_plan_attr(casa_rope, problem_bool=x_problem_bool)

    # THEN
    assert sue_person.planroot.kids[exx.casa].problem_bool == x_problem_bool


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario10_workforceunit():
    # ESTABLISH
    xio_person = personunit_shop("Xio")
    run_str = "run"
    run_rope = xio_person.make_l1_rope(run_str)
    xio_person.set_l1_plan(planunit_shop(run_str))
    run_plan = xio_person.get_plan_obj(run_rope)
    sue_workforceunit = workforceunit_shop()
    sue_workforceunit.add_labor(exx.sue)
    assert run_plan.workforceunit == workforceunit_shop()

    # WHEN
    xio_person.edit_plan_attr(run_rope, workforceunit=sue_workforceunit)

    # THEN
    assert run_plan.workforceunit == sue_workforceunit


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario11_reasonunit():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sem_jour_str = "sem_jours"
    sem_jour_rope = sue_person.make_l1_rope(sem_jour_str)
    wed_rope = sue_person.make_rope(sem_jour_rope, exx.wed)

    wed_case = caseunit_shop(reason_state=wed_rope)
    casa_wk_reason = reasonunit_shop(sem_jour_rope, {wed_case.reason_state: wed_case})
    print(f"{type(casa_wk_reason.reason_context)=}")
    print(f"{casa_wk_reason.reason_context=}")

    # WHEN
    sue_person.edit_plan_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_plan = sue_person.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits is not None
    print(casa_plan.reasonunits)
    assert casa_plan.reasonunits[sem_jour_rope] is not None
    assert casa_plan.reasonunits[sem_jour_rope] == casa_wk_reason


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario12_reasonunit_knot():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope("casa")
    wk_rope = sue_person.make_l1_rope("sem_jours")
    wed_rope = sue_person.make_rope(wk_rope, "Wed")

    before_wk_reason = reasonunit_shop(wk_rope, knot=exx.slash)
    before_wk_reason.set_case(wed_rope)
    assert before_wk_reason.knot == exx.slash

    # WHEN
    sue_person.edit_plan_attr(casa_rope, reason=before_wk_reason)

    # THEN
    casa_plan = sue_person.get_plan_obj(casa_rope)
    wk_reasonunit = casa_plan.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != exx.slash
    assert wk_reasonunit.knot == sue_person.knot


def test_PersonUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario13_reason_context_knot():
    # ESTABLISH
    bob_person = personunit_shop("Bob", knot=exx.slash)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    wk_rope = bob_person.make_l1_rope(exx.wk)
    wed_rope = bob_person.make_rope(wk_rope, exx.wed)
    bob_person.set_l1_plan(planunit_shop(exx.casa))
    bob_person.set_l1_plan(planunit_shop(exx.wk))
    bob_person.set_plan_obj(planunit_shop(exx.wed), wk_rope)
    print(f"{bob_person.planroot.kids.keys()=}")
    wed_plan = bob_person.get_plan_obj(wed_rope)
    assert wed_plan.knot == exx.slash
    assert wed_plan.knot == bob_person.knot

    # WHEN
    bob_person.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan = bob_person.get_plan_obj(casa_rope)
    assert casa_plan.knot == exx.slash
    wk_reasonunit = casa_plan.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != ","
    assert wk_reasonunit.knot == bob_person.knot


def test_PersonUnit_edit_plan_attr_RaisesError_SetNestedPlanUnitAttr_Scenario13_reason_context_knot():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    casa_rope = bob_person.make_l1_rope(exx.casa)
    wk_rope = bob_person.make_l1_rope(exx.wk)
    incorrect_wed_rope = bob_person.make_l1_rope(exx.wed)
    assert not is_sub_rope(wk_rope, incorrect_wed_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_person.edit_plan_attr(
            casa_rope, reason_context=wk_rope, reason_case=incorrect_wed_rope
        )
    exception_str = f"""Plan cannot edit reason because reason_case is not sub_rope to reason_context 
reason_context: {wk_rope}
reason_case:    {incorrect_wed_rope}"""
    assert str(excinfo.value) == exception_str


def test_PersonUnit_edit_plan_attr_RaisesError_Scenario15_When_healerunit_healer_names_DoNotExist():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    casa_rope = yao_person.make_l1_rope(exx.casa)
    yao_person.set_l1_plan(planunit_shop(exx.casa))
    jour_str = "jour_range"
    jour_plan = planunit_shop(jour_str, begin=44, close=110)
    yao_person.set_l1_plan(jour_plan)

    casa_plan = yao_person.get_plan_obj(casa_rope)
    assert casa_plan.begin is None
    assert casa_plan.close is None

    # WHEN / THEN
    x_healerunit = healerunit_shop({exx.sue})
    with pytest_raises(Exception) as excinfo:
        yao_person.edit_plan_attr(casa_rope, healerunit=x_healerunit)
    exception_str = f"Plan cannot edit healerunit because group_title '{exx.sue}' does not exist as group in Person"
    assert str(excinfo.value) == exception_str


def test_PersonUnit_set_plan_ScenarioXX_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    bob_person.set_l1_plan(planunit_shop(exx.casa))
    bob_person.set_l1_plan(planunit_shop(exx.bowl))

    # WHEN
    plan_list = list(bob_person.planroot.kids.values())

    # THEN
    assert plan_list[0].plan_label == exx.bowl
    assert plan_list[1].plan_label == exx.casa


def test_PersonUnit_set_plan_ScenarioXX_adoptee_RaisesErrorIfAdopteePlanDoesNotHaveParent():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_person.make_l1_rope(sports_str)
    bob_person.set_l1_plan(planunit_shop(sports_str))
    bob_person.set_plan_obj(planunit_shop(exx.bowl), parent_rope=sports_rope)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_rope = bob_person.make_rope(sports_rope, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_person.set_plan_obj(
            plan_kid=planunit_shop(summer_str),
            parent_rope=sports_rope,
            adoptees=[exx.bowl, hike_str],
        )
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{hike_rope}'"


def test_PersonUnit_set_plan_ScenarioXX_adoptee_AddsAdoptee():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_person.make_l1_rope(sports_str)
    bob_person.set_l1_plan(planunit_shop(sports_str))
    bob_person.set_plan_obj(planunit_shop(exx.bowl), parent_rope=sports_rope)
    hike_str = "hike"
    bob_person.set_plan_obj(planunit_shop(hike_str), parent_rope=sports_rope)

    sports_bowl_rope = bob_person.make_rope(sports_rope, exx.bowl)
    sports_hike_rope = bob_person.make_rope(sports_rope, hike_str)
    assert bob_person.plan_exists(sports_bowl_rope)
    assert bob_person.plan_exists(sports_hike_rope)
    summer_str = "summer"
    summer_rope = bob_person.make_rope(sports_rope, summer_str)
    summer_bowl_rope = bob_person.make_rope(summer_rope, exx.bowl)
    summer_hike_rope = bob_person.make_rope(summer_rope, hike_str)
    assert bob_person.plan_exists(summer_bowl_rope) is False
    assert bob_person.plan_exists(summer_hike_rope) is False

    # WHEN / THEN
    bob_person.set_plan_obj(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[exx.bowl, hike_str],
    )

    # THEN
    summer_plan = bob_person.get_plan_obj(summer_rope)
    print(f"{summer_plan.kids.keys()=}")
    assert bob_person.plan_exists(summer_bowl_rope)
    assert bob_person.plan_exists(summer_hike_rope)
    assert bob_person.plan_exists(sports_bowl_rope) is False
    assert bob_person.plan_exists(sports_hike_rope) is False


def test_PersonUnit_set_plan_ScenarioXX_bundling_SetsNewParentWithstarEqualToSumOfAdoptedPlans():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_person.make_l1_rope(sports_str)
    bob_person.set_l1_plan(planunit_shop(sports_str, star=2))
    bowl_star = 3
    bob_person.set_plan_obj(planunit_shop(exx.bowl, star=bowl_star), sports_rope)
    hike_str = "hike"
    hike_star = 5
    bob_person.set_plan_obj(planunit_shop(hike_str, star=hike_star), sports_rope)
    bball_str = "bball"
    bball_star = 7
    bob_person.set_plan_obj(planunit_shop(bball_str, star=bball_star), sports_rope)

    sports_bowl_rope = bob_person.make_rope(sports_rope, exx.bowl)
    sports_hike_rope = bob_person.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_person.make_rope(sports_rope, bball_str)
    assert bob_person.get_plan_obj(sports_bowl_rope).star == bowl_star
    assert bob_person.get_plan_obj(sports_hike_rope).star == hike_star
    assert bob_person.get_plan_obj(sports_bball_rope).star == bball_star
    summer_str = "summer"
    summer_rope = bob_person.make_rope(sports_rope, summer_str)
    summer_bowl_rope = bob_person.make_rope(summer_rope, exx.bowl)
    summer_hike_rope = bob_person.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_person.make_rope(summer_rope, bball_str)
    assert bob_person.plan_exists(summer_bowl_rope) is False
    assert bob_person.plan_exists(summer_hike_rope) is False
    assert bob_person.plan_exists(summer_bball_rope) is False

    # WHEN / THEN
    bob_person.set_plan_obj(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[exx.bowl, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_person.get_plan_obj(summer_rope).star == bowl_star + hike_star
    assert bob_person.get_plan_obj(summer_bowl_rope).star == bowl_star
    assert bob_person.get_plan_obj(summer_hike_rope).star == hike_star
    assert bob_person.plan_exists(summer_bball_rope) is False
    assert bob_person.plan_exists(sports_bowl_rope) is False
    assert bob_person.plan_exists(sports_hike_rope) is False
    assert bob_person.plan_exists(sports_bball_rope)


def test_PersonUnit_del_plan_obj_DeletingBundledPlanReturnsPlansToOriginalState():
    # ESTABLISH
    bob_person = personunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_person.make_l1_rope(sports_str)
    bob_person.set_l1_plan(planunit_shop(sports_str, star=2))
    bowl_star = 3
    bob_person.set_plan_obj(planunit_shop(exx.bowl, star=bowl_star), sports_rope)
    hike_str = "hike"
    hike_star = 5
    bob_person.set_plan_obj(planunit_shop(hike_str, star=hike_star), sports_rope)
    bball_str = "bball"
    bball_star = 7
    bob_person.set_plan_obj(planunit_shop(bball_str, star=bball_star), sports_rope)

    sports_bowl_rope = bob_person.make_rope(sports_rope, exx.bowl)
    sports_hike_rope = bob_person.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_person.make_rope(sports_rope, bball_str)
    assert bob_person.get_plan_obj(sports_bowl_rope).star == bowl_star
    assert bob_person.get_plan_obj(sports_hike_rope).star == hike_star
    assert bob_person.get_plan_obj(sports_bball_rope).star == bball_star
    summer_str = "summer"
    summer_rope = bob_person.make_rope(sports_rope, summer_str)
    summer_bowl_rope = bob_person.make_rope(summer_rope, exx.bowl)
    summer_hike_rope = bob_person.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_person.make_rope(summer_rope, bball_str)
    assert bob_person.plan_exists(summer_bowl_rope) is False
    assert bob_person.plan_exists(summer_hike_rope) is False
    assert bob_person.plan_exists(summer_bball_rope) is False
    bob_person.set_plan_obj(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[exx.bowl, hike_str],
        bundling=True,
    )
    assert bob_person.get_plan_obj(summer_rope).star == bowl_star + hike_star
    assert bob_person.get_plan_obj(summer_bowl_rope).star == bowl_star
    assert bob_person.get_plan_obj(summer_hike_rope).star == hike_star
    assert bob_person.plan_exists(summer_bball_rope) is False
    assert bob_person.plan_exists(sports_bowl_rope) is False
    assert bob_person.plan_exists(sports_hike_rope) is False
    assert bob_person.plan_exists(sports_bball_rope)
    print(f"{bob_person._plan_dict.keys()=}")

    # WHEN
    bob_person.del_plan_obj(rope=summer_rope, del_children=False)

    # THEN
    sports_bowl_plan = bob_person.get_plan_obj(sports_bowl_rope)
    sports_hike_plan = bob_person.get_plan_obj(sports_hike_rope)
    sports_bball_plan = bob_person.get_plan_obj(sports_bball_rope)
    assert sports_bowl_plan.star == bowl_star
    assert sports_hike_plan.star == hike_star
    assert sports_bball_plan.star == bball_star


def test_PersonUnit_edit_plan_attr_DeletesPlanUnit_awardunits():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao)
    yao_person.add_contactunit(exx.zia)
    yao_person.add_contactunit(exx.xio)

    bowl_rope = yao_person.make_l1_rope(exx.bowl)

    yao_person.set_l1_plan(planunit_shop(exx.bowl))
    awardunit_yao = awardunit_shop(exx.yao, give_force=10)
    awardunit_zia = awardunit_shop(exx.zia, give_force=10)
    awardunit_Xio = awardunit_shop(exx.xio, give_force=10)

    bowl_plan = yao_person.get_plan_obj(bowl_rope)
    yao_person.edit_plan_attr(bowl_rope, awardunit=awardunit_yao)
    yao_person.edit_plan_attr(bowl_rope, awardunit=awardunit_zia)
    yao_person.edit_plan_attr(bowl_rope, awardunit=awardunit_Xio)

    assert len(bowl_plan.awardunits) == 3
    assert len(yao_person.planroot.kids[exx.bowl].awardunits) == 3

    # WHEN
    yao_person.edit_plan_attr(bowl_rope, awardunit_del=exx.yao)

    # THEN
    bowl_plan = yao_person.get_plan_obj(bowl_rope)
    print(f"{bowl_plan.plan_label=}")
    print(f"{bowl_plan.awardunits=}")
    print(f"{bowl_plan.awardheirs=}")

    assert len(yao_person.planroot.kids[exx.bowl].awardunits) == 2


def test_PersonUnit__get_filtered_awardunits_plan_RemovesContact_awardunits():
    # ESTABLISH
    example_person = personunit_shop(exx.bob)
    xia_str = "Xia"
    hike_str = ";hikers"
    example_person.add_contactunit(xia_str)
    example_person.get_contact(xia_str).add_membership(exx.run)

    sports_str = "sports"
    sports_rope = example_person.make_l1_rope(sports_str)
    example_person.set_l1_plan(planunit_shop(sports_str))
    example_person.edit_plan_attr(sports_rope, awardunit=awardunit_shop(exx.run))
    example_person.edit_plan_attr(sports_rope, awardunit=awardunit_shop(hike_str))
    example_person_sports_plan = example_person.get_plan_obj(sports_rope)
    assert len(example_person_sports_plan.awardunits) == 2
    bob_person = personunit_shop(exx.bob)
    bob_person.add_contactunit(xia_str)
    bob_person.get_contact(xia_str).add_membership(exx.run)
    print(f"{example_person_sports_plan.awardunits=}")

    # WHEN
    cleaned_plan = bob_person._get_filtered_awardunits_plan(example_person_sports_plan)

    # THEN
    assert len(cleaned_plan.awardunits) == 1
    assert list(cleaned_plan.awardunits.keys()) == [exx.run]


def test_PersonUnit__get_filtered_awardunits_plan_RemovesGroup_awardunit():
    # ESTABLISH
    example_person = personunit_shop(exx.bob)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_person.add_contactunit(xia_str)
    example_person.add_contactunit(zoa_str)

    bowl_rope = example_person.make_l1_rope(exx.bowl)
    example_person.set_l1_plan(planunit_shop(exx.bowl))
    example_person.edit_plan_attr(bowl_rope, awardunit=awardunit_shop(xia_str))
    example_person.edit_plan_attr(bowl_rope, awardunit=awardunit_shop(zoa_str))
    example_person_bowl_plan = example_person.get_plan_obj(bowl_rope)
    assert len(example_person_bowl_plan.awardunits) == 2
    bob_person = personunit_shop(exx.bob)
    bob_person.add_contactunit(xia_str)

    # WHEN
    cleaned_plan = bob_person._get_filtered_awardunits_plan(example_person_bowl_plan)

    # THEN
    assert len(cleaned_plan.awardunits) == 1
    assert list(cleaned_plan.awardunits.keys()) == [xia_str]


def test_PersonUnit_set_plan_ScenarioXX_SetsPlan_awardunits():
    # ESTABLISH
    example_person = personunit_shop(exx.bob)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_person.add_contactunit(xia_str)
    example_person.add_contactunit(zoa_str)

    casa_rope = example_person.make_l1_rope(exx.casa)
    bowl_rope = example_person.make_l1_rope(exx.bowl)
    example_person.set_l1_plan(planunit_shop(exx.casa))
    example_person.set_l1_plan(planunit_shop(exx.bowl))
    example_person.edit_plan_attr(bowl_rope, awardunit=awardunit_shop(xia_str))
    example_person.edit_plan_attr(bowl_rope, awardunit=awardunit_shop(zoa_str))
    example_person_bowl_plan = example_person.get_plan_obj(bowl_rope)
    assert len(example_person_bowl_plan.awardunits) == 2
    bob_person = personunit_shop(exx.bob)
    bob_person.add_contactunit(xia_str)

    # WHEN
    bob_person.set_l1_plan(example_person_bowl_plan, create_missing_plans=False)

    # THEN
    bob_person_bowl_plan = bob_person.get_plan_obj(bowl_rope)
    assert len(bob_person_bowl_plan.awardunits) == 1
    assert list(bob_person_bowl_plan.awardunits.keys()) == [xia_str]


def test_PersonUnit_get_plan_obj_ReturnsPlan():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    brazil_str = "Brazil"
    brazil_rope = sue_person.make_rope(nation_rope, brazil_str)

    # WHEN
    brazil_plan = sue_person.get_plan_obj(rope=brazil_rope)

    # THEN
    assert brazil_plan is not None
    assert brazil_plan.plan_label == brazil_str

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    wk_plan = sue_person.get_plan_obj(rope=wk_rope)

    # THEN
    assert wk_plan is not None
    assert wk_plan.plan_label == wk_str

    # WHEN
    root_plan = sue_person.get_plan_obj(sue_person.planroot.get_plan_rope())

    # THEN
    assert root_plan is not None
    assert root_plan.get_plan_rope() == sue_person.planroot.get_plan_rope()

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_rope = sue_person.make_l1_rope(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_person.get_plan_obj(rope=wrong_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{wrong_rope}'"


def test_PersonUnit_plan_exists_ReturnsBool():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    cat_rope = sue_person.make_l1_rope("cat have dinner")
    wk_rope = sue_person.make_l1_rope("sem_jours")
    casa_rope = sue_person.make_l1_rope("casa")
    nation_rope = sue_person.make_l1_rope("nation")
    sun_rope = sue_person.make_rope(wk_rope, "Sun")
    mon_rope = sue_person.make_rope(wk_rope, "Mon")
    tue_rope = sue_person.make_rope(wk_rope, "Tue")
    wed_rope = sue_person.make_rope(wk_rope, "Wed")
    thu_rope = sue_person.make_rope(wk_rope, "Thur")
    fri_rope = sue_person.make_rope(wk_rope, "Fri")
    sat_rope = sue_person.make_rope(wk_rope, "Sat")
    france_rope = sue_person.make_rope(nation_rope, "France")
    brazil_rope = sue_person.make_rope(nation_rope, "Brazil")
    usa_rope = sue_person.make_rope(nation_rope, "USA")
    texas_rope = sue_person.make_rope(usa_rope, "Texas")
    oregon_rope = sue_person.make_rope(usa_rope, "Oregon")
    # do not exist in person
    sports_rope = sue_person.make_l1_rope("sports")
    bowl_rope = sue_person.make_rope(sports_rope, "bowling")
    idaho_rope = sue_person.make_rope(usa_rope, "Idaho")
    japan_rope = sue_person.make_rope(nation_rope, "Japan")

    # WHEN / THEN
    assert sue_person.plan_exists("") is False
    assert sue_person.plan_exists(None) is False
    assert sue_person.plan_exists(sue_person.planroot.get_plan_rope())
    assert sue_person.plan_exists(cat_rope)
    assert sue_person.plan_exists(wk_rope)
    assert sue_person.plan_exists(casa_rope)
    assert sue_person.plan_exists(nation_rope)
    assert sue_person.plan_exists(sun_rope)
    assert sue_person.plan_exists(mon_rope)
    assert sue_person.plan_exists(tue_rope)
    assert sue_person.plan_exists(wed_rope)
    assert sue_person.plan_exists(thu_rope)
    assert sue_person.plan_exists(fri_rope)
    assert sue_person.plan_exists(sat_rope)
    assert sue_person.plan_exists(usa_rope)
    assert sue_person.plan_exists(france_rope)
    assert sue_person.plan_exists(brazil_rope)
    assert sue_person.plan_exists(texas_rope)
    assert sue_person.plan_exists(oregon_rope)
    assert sue_person.plan_exists(to_rope("B")) is False
    assert sue_person.plan_exists(sports_rope) is False
    assert sue_person.plan_exists(bowl_rope) is False
    assert sue_person.plan_exists(idaho_rope) is False
    assert sue_person.plan_exists(japan_rope) is False


def test_PersonUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert not bob_personunit.offtrack_fund

    # WHEN
    bob_personunit.set_offtrack_fund() == 0

    # THEN
    assert bob_personunit.offtrack_fund == 0

    # ESTABLISH
    casa_rope = bob_personunit.make_l1_rope(exx.casa)
    wk_rope = bob_personunit.make_l1_rope(exx.wk)
    wed_rope = bob_personunit.make_rope(wk_rope, exx.wed)
    casa_plan = planunit_shop(exx.casa, fund_onset=70, fund_cease=170)
    wk_plan = planunit_shop(exx.wk, fund_onset=70, fund_cease=75)
    wed_plan = planunit_shop(exx.wed, fund_onset=72, fund_cease=75)
    casa_plan.parent_rope = bob_personunit.planroot.get_plan_rope()
    wk_plan.parent_rope = bob_personunit.planroot.get_plan_rope()
    wed_plan.parent_rope = wk_rope
    bob_personunit.set_l1_plan(casa_plan)
    bob_personunit.set_l1_plan(wk_plan)
    bob_personunit.set_plan_obj(wed_plan, wk_rope)
    bob_personunit.offtrack_kids_star_set.add(casa_rope)
    bob_personunit.offtrack_kids_star_set.add(wk_rope)
    assert bob_personunit.offtrack_fund == 0

    # WHEN
    bob_personunit.set_offtrack_fund()

    # THEN
    assert bob_personunit.offtrack_fund == 105

    # WHEN
    bob_personunit.offtrack_kids_star_set.add(wed_rope)
    bob_personunit.set_offtrack_fund()

    # THEN
    assert bob_personunit.offtrack_fund == 108


def test_PersonUnit_allot_offtrack_fund_SetsCharUnit_fund_take_fund_give():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    bob_personunit = personunit_shop(exx.bob)
    bob_personunit.add_contactunit(exx.bob)
    bob_personunit.add_contactunit(exx.yao, contact_cred_lumen=2)
    bob_personunit.add_contactunit(exx.sue, contact_debt_lumen=2)
    bob_personunit.set_offtrack_fund()
    assert bob_personunit.offtrack_fund == 0

    # WHEN
    bob_personunit._allot_offtrack_fund()

    # THEN
    assert bob_personunit.get_contact(exx.bob).fund_give == 0
    assert bob_personunit.get_contact(exx.bob).fund_take == 0
    assert bob_personunit.get_contact(exx.yao).fund_give == 0
    assert bob_personunit.get_contact(exx.yao).fund_take == 0
    assert bob_personunit.get_contact(exx.sue).fund_give == 0
    assert bob_personunit.get_contact(exx.sue).fund_take == 0

    # WHEN
    casa_rope = bob_personunit.make_l1_rope(exx.casa)
    wk_rope = bob_personunit.make_l1_rope(exx.wk)
    wed_rope = bob_personunit.make_rope(wk_rope, exx.wed)
    casa_plan = planunit_shop(exx.casa, fund_onset=70, fund_cease=170)
    wk_plan = planunit_shop(exx.wk, fund_onset=70, fund_cease=75)
    wed_plan = planunit_shop(exx.wed, fund_onset=72, fund_cease=75)
    casa_plan.parent_rope = bob_personunit.planroot.get_plan_rope()
    wk_plan.parent_rope = bob_personunit.planroot.get_plan_rope()
    wed_plan.parent_rope = wk_rope
    bob_personunit.set_l1_plan(casa_plan)
    bob_personunit.set_l1_plan(wk_plan)
    bob_personunit.set_plan_obj(wed_plan, wk_rope)
    bob_personunit.offtrack_kids_star_set.add(casa_rope)
    bob_personunit.offtrack_kids_star_set.add(wk_rope)
    bob_personunit.set_offtrack_fund()
    assert bob_personunit.offtrack_fund == 105

    # WHEN
    bob_personunit._allot_offtrack_fund()

    # THEN
    assert bob_personunit.get_contact(exx.bob).fund_give == 26
    assert bob_personunit.get_contact(exx.bob).fund_take == 26
    assert bob_personunit.get_contact(exx.yao).fund_give == 53
    assert bob_personunit.get_contact(exx.yao).fund_take == 26
    assert bob_personunit.get_contact(exx.sue).fund_give == 26
    assert bob_personunit.get_contact(exx.sue).fund_take == 53

    bob_personunit.offtrack_kids_star_set.add(wed_rope)
    bob_personunit.set_offtrack_fund()

    # THEN
    assert bob_personunit.offtrack_fund == 108
