from src.ch03_workforce.workforce import workforceheir_shop, workforceunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_conpute_Sets_planroot_workforceheirFrom_planroot_workforceunit():
    # ESTABLISH
    sue_workforceunit = workforceunit_shop()
    sue_workforceunit.add_labor(exx.sue)
    yao_person = personunit_shop(exx.yao)
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
    bob_person.add_contactunit(exx.bob)
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
    bowl_rope = sue_person.make_l1_rope(exx.bowl)
    morn_str = "morning"
    morn_rope = sue_person.make_rope(bowl_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_person.make_rope(morn_rope, four_str)
    x_workforceunit = workforceunit_shop()
    bowlers_str = ";bowlers"
    x_workforceunit.add_labor(labor_title=bowlers_str)

    sue_person.add_contactunit(exx.yao)
    yao_contactunit = sue_person.get_contact(exx.yao)
    yao_contactunit.add_membership(bowlers_str)

    sue_person.set_l1_plan(planunit_shop(exx.bowl))
    sue_person.set_plan_obj(planunit_shop(morn_str), parent_rope=bowl_rope)
    sue_person.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_person.edit_plan_attr(bowl_rope, workforceunit=x_workforceunit)
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
    bowl_rope = sue_person.make_l1_rope(exx.bowl)
    morn_str = "morning"
    morn_rope = sue_person.make_rope(bowl_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_person.make_rope(morn_rope, four_str)
    bowlers_workforceunit = workforceunit_shop()
    bowlers_str = ";bowlers"
    bowlers_solo_bool = True
    bowlers_workforceunit.add_labor(bowlers_str, solo=bowlers_solo_bool)

    sue_person.add_contactunit(exx.yao)
    yao_contactunit = sue_person.get_contact(exx.yao)
    yao_contactunit.add_membership(bowlers_str)

    sue_person.set_l1_plan(planunit_shop(exx.bowl))
    sue_person.set_plan_obj(planunit_shop(morn_str), parent_rope=bowl_rope)
    sue_person.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_person.edit_plan_attr(bowl_rope, workforceunit=bowlers_workforceunit)
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
        workforceunit=bowlers_workforceunit,
        groupunits=sue_person.groupunits,
    )
    assert four_plan.workforceheir
    assert four_plan.workforceheir == expected_workforceheir
    bowlers_labor = four_plan.workforceheir.labors.get(bowlers_str)
    assert bowlers_labor.solo == bowlers_solo_bool


def test_PersonUnit__get_filtered_awardunits_plan_CleansPlan_Workforceunit():
    # ESTABLISH
    sue1_person = personunit_shop(exx.sue)
    sue1_person.add_contactunit(exx.xio)
    sue1_person.add_contactunit(exx.zia)

    casa_rope = sue1_person.make_l1_rope(exx.casa)
    bowl_rope = sue1_person.make_l1_rope(exx.bowl)
    root_rope = sue1_person.planroot.get_plan_rope()
    sue1_person.set_plan_obj(planunit_shop(exx.casa), parent_rope=root_rope)
    sue1_person.set_plan_obj(planunit_shop(exx.bowl), parent_rope=root_rope)
    bowl_workforceunit = workforceunit_shop()
    bowl_workforceunit.add_labor(labor_title=exx.xio)
    bowl_workforceunit.add_labor(labor_title=exx.zia)
    sue1_person.edit_plan_attr(bowl_rope, workforceunit=bowl_workforceunit)
    sue1_person_bowl_plan = sue1_person.get_plan_obj(bowl_rope)
    sue1_person_bowl_labors = sue1_person_bowl_plan.workforceunit.labors
    assert len(sue1_person_bowl_labors) == 2

    # WHEN
    sue2_person = personunit_shop(exx.sue)
    sue2_person.add_contactunit(exx.xio)
    cleaned_plan = sue2_person._get_filtered_awardunits_plan(sue1_person_bowl_plan)

    # THEN
    cleaned_bowl_labors = cleaned_plan.workforceunit.labors
    assert len(cleaned_bowl_labors) == 1
    assert list(cleaned_bowl_labors) == [exx.xio]


def test_PersonUnit_set_plan_CleansPlan_awardunits():
    # ESTABLISH
    sue1_person = personunit_shop("Sue")
    sue1_person.add_contactunit(exx.xio)
    sue1_person.add_contactunit(exx.zia)

    casa_rope = sue1_person.make_l1_rope(exx.casa)
    bowl_rope = sue1_person.make_l1_rope(exx.bowl)
    sue1_person.set_plan_obj(
        planunit_shop(exx.casa), parent_rope=sue1_person.planroot.get_plan_rope()
    )
    sue1_person.set_plan_obj(
        planunit_shop(exx.bowl), parent_rope=sue1_person.planroot.get_plan_rope()
    )
    bowl_workforceunit = workforceunit_shop()
    bowl_workforceunit.add_labor(labor_title=exx.xio)
    bowl_workforceunit.add_labor(labor_title=exx.zia)
    sue1_person.edit_plan_attr(bowl_rope, workforceunit=bowl_workforceunit)
    sue1_person_bowl_plan = sue1_person.get_plan_obj(bowl_rope)
    sue1_person_bowl_labors = sue1_person_bowl_plan.workforceunit.labors
    assert len(sue1_person_bowl_labors) == 2

    # WHEN
    sue2_person = personunit_shop("Sue")
    sue2_person.add_contactunit(exx.xio)
    sue2_person.set_l1_plan(
        sue1_person_bowl_plan, get_rid_of_missing_awardunits_awardee_titles=False
    )

    # THEN
    sue2_person_bowl_plan = sue2_person.get_plan_obj(bowl_rope)
    sue2_person_bowl_labors = sue2_person_bowl_plan.workforceunit.labors
    assert len(sue2_person_bowl_labors) == 1
    assert list(sue2_person_bowl_labors) == [exx.xio]
