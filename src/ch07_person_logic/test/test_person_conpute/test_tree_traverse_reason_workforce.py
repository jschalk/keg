from src.ch03_workforce.workforce import workforceheir_shop, workforceunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_conpute_Sets_planroot_workforceheirFrom_planroot_workforceunit():
    # ESTABLISH
    sue_workforceunit = workforceunit_shop()
    sue_workforceunit.add_labor(exx.sue)
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.planroot.get_plan_rope()
    yao_person.edit_plan_attr(root_rope, workforceunit=sue_workforceunit)
    assert yao_person.planroot.workforceunit == sue_workforceunit
    assert not yao_person.planroot.workforceheir

    # WHEN
    yao_person.conpute()

    # THEN
    assert yao_person.planroot.workforceheir is not None
    expected_workforceheir = workforceheir_shop()
    expected_workforceheir.set_labors(
        parent_workforceheir=None, workforceunit=sue_workforceunit, groupunits=None
    )
    assert yao_person.planroot.workforceheir == expected_workforceheir


def test_PersonUnit_conpute_Set_child_plan_workforceheir_FromParent_workforceunit():
    # ESTABLISH
    x_workforceunit = workforceunit_shop()
    bob_person = personunit_shop(exx.bob)
    run_str = "run"
    run_rope = bob_person.make_l1_rope(run_str)
    bob_person.add_partnerunit(exx.bob)
    bob_person.set_l1_plan(planunit_shop(run_str))
    bob_person.edit_plan_attr(run_rope, workforceunit=x_workforceunit)
    run_plan = bob_person.get_plan_obj(run_rope)
    assert run_plan.workforceunit == x_workforceunit
    assert not run_plan.workforceheir

    # WHEN
    bob_person.conpute()

    # THEN
    assert run_plan.workforceheir
    assert run_plan.workforceheir.person_name_is_workforce

    expected_workforceheir = workforceheir_shop()
    expected_workforceheir.set_labors(
        parent_workforceheir=None,
        workforceunit=x_workforceunit,
        groupunits=bob_person.groupunits,
    )
    expected_workforceheir.set_person_name_is_workforce(
        bob_person.groupunits, bob_person.person_name
    )
    print(f"{expected_workforceheir.person_name_is_workforce=}")
    assert (
        run_plan.workforceheir.person_name_is_workforce
        == expected_workforceheir.person_name_is_workforce
    )
    assert run_plan.workforceheir == expected_workforceheir


def test_PersonUnit_conpute_Set_grandchild_plan_workforceheir_From_plankid_workforceunit_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    swim_rope = sue_person.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_person.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_person.make_rope(morn_rope, four_str)
    x_workforceunit = workforceunit_shop()
    swimmers_str = ";swimmers"
    x_workforceunit.add_labor(labor_title=swimmers_str)

    sue_person.add_partnerunit(exx.yao)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(swimmers_str)

    sue_person.set_l1_plan(planunit_shop(exx.swim))
    sue_person.set_plan_obj(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_person.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_person.edit_plan_attr(swim_rope, workforceunit=x_workforceunit)
    # print(sue_person.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_person.get_plan_obj(four_rope)
    assert four_plan.workforceunit == workforceunit_shop()
    assert four_plan.workforceheir is None

    # WHEN
    sue_person.conpute()

    # THEN
    x_workforceheir = workforceheir_shop()
    x_workforceheir.set_labors(
        parent_workforceheir=None,
        workforceunit=x_workforceunit,
        groupunits=sue_person.groupunits,
    )
    assert four_plan.workforceheir is not None
    assert four_plan.workforceheir == x_workforceheir


def test_PersonUnit_conpute_Set_grandchild_plan_workforceheir_From_plankid_workforceunit_Scenario1_solo_AttrIsPassed():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    swim_rope = sue_person.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_person.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_person.make_rope(morn_rope, four_str)
    swimmers_workforceunit = workforceunit_shop()
    swimmers_str = ";swimmers"
    swimmers_solo_bool = True
    swimmers_workforceunit.add_labor(swimmers_str, solo=swimmers_solo_bool)

    sue_person.add_partnerunit(exx.yao)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(swimmers_str)

    sue_person.set_l1_plan(planunit_shop(exx.swim))
    sue_person.set_plan_obj(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_person.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_person.edit_plan_attr(swim_rope, workforceunit=swimmers_workforceunit)
    # print(sue_person.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_person.get_plan_obj(four_rope)
    assert four_plan.workforceunit == workforceunit_shop()
    assert not four_plan.workforceheir

    # WHEN
    sue_person.conpute()

    # THEN
    expected_workforceheir = workforceheir_shop()
    expected_workforceheir.set_labors(
        parent_workforceheir=None,
        workforceunit=swimmers_workforceunit,
        groupunits=sue_person.groupunits,
    )
    assert four_plan.workforceheir
    assert four_plan.workforceheir == expected_workforceheir
    swimmers_labor = four_plan.workforceheir.labors.get(swimmers_str)
    assert swimmers_labor.solo == swimmers_solo_bool


def test_PersonUnit__get_filtered_awardunits_plan_CleansPlan_Workforceunit():
    # ESTABLISH
    sue1_person = personunit_shop(exx.sue)
    sue1_person.add_partnerunit(exx.xio)
    sue1_person.add_partnerunit(exx.zia)

    casa_rope = sue1_person.make_l1_rope(exx.casa)
    swim_rope = sue1_person.make_l1_rope(exx.swim)
    root_rope = sue1_person.planroot.get_plan_rope()
    sue1_person.set_plan_obj(planunit_shop(exx.casa), parent_rope=root_rope)
    sue1_person.set_plan_obj(planunit_shop(exx.swim), parent_rope=root_rope)
    swim_workforceunit = workforceunit_shop()
    swim_workforceunit.add_labor(labor_title=exx.xio)
    swim_workforceunit.add_labor(labor_title=exx.zia)
    sue1_person.edit_plan_attr(swim_rope, workforceunit=swim_workforceunit)
    sue1_person_swim_plan = sue1_person.get_plan_obj(swim_rope)
    sue1_person_swim_labors = sue1_person_swim_plan.workforceunit.labors
    assert len(sue1_person_swim_labors) == 2

    # WHEN
    sue2_person = personunit_shop(exx.sue)
    sue2_person.add_partnerunit(exx.xio)
    cleaned_plan = sue2_person._get_filtered_awardunits_plan(sue1_person_swim_plan)

    # THEN
    cleaned_swim_labors = cleaned_plan.workforceunit.labors
    assert len(cleaned_swim_labors) == 1
    assert list(cleaned_swim_labors) == [exx.xio]


def test_PersonUnit_set_plan_CleansPlan_awardunits():
    # ESTABLISH
    sue1_person = personunit_shop("Sue")
    sue1_person.add_partnerunit(exx.xio)
    sue1_person.add_partnerunit(exx.zia)

    casa_rope = sue1_person.make_l1_rope(exx.casa)
    swim_rope = sue1_person.make_l1_rope(exx.swim)
    sue1_person.set_plan_obj(
        planunit_shop(exx.casa), parent_rope=sue1_person.planroot.get_plan_rope()
    )
    sue1_person.set_plan_obj(
        planunit_shop(exx.swim), parent_rope=sue1_person.planroot.get_plan_rope()
    )
    swim_workforceunit = workforceunit_shop()
    swim_workforceunit.add_labor(labor_title=exx.xio)
    swim_workforceunit.add_labor(labor_title=exx.zia)
    sue1_person.edit_plan_attr(swim_rope, workforceunit=swim_workforceunit)
    sue1_person_swim_plan = sue1_person.get_plan_obj(swim_rope)
    sue1_person_swim_labors = sue1_person_swim_plan.workforceunit.labors
    assert len(sue1_person_swim_labors) == 2

    # WHEN
    sue2_person = personunit_shop("Sue")
    sue2_person.add_partnerunit(exx.xio)
    sue2_person.set_l1_plan(
        sue1_person_swim_plan, get_rid_of_missing_awardunits_awardee_titles=False
    )

    # THEN
    sue2_person_swim_plan = sue2_person.get_plan_obj(swim_rope)
    sue2_person_swim_labors = sue2_person_swim_plan.workforceunit.labors
    assert len(sue2_person_swim_labors) == 1
    assert list(sue2_person_swim_labors) == [exx.xio]
