from ch06_plan.plan import get_rangeunit_from_lineage_of_plans, planunit_shop
from ch06_plan.range_toolbox import RangeUnit
from ref.keywords import ExampleStrs as exx


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario0_EmptyList():
    # ESTABLISH
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert (
        get_rangeunit_from_lineage_of_plans([], x_rangeunit.gogo, x_rangeunit.stop)
        == x_rangeunit
    )


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario1_EmptyPlanUnit():
    # ESTABLISH
    wk_plan = planunit_shop(exx.wk)
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert (
        get_rangeunit_from_lineage_of_plans(
            [wk_plan], x_rangeunit.gogo, x_rangeunit.stop
        )
        == x_rangeunit
    )


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario2_1PlanUnit_addin():
    # ESTABLISH
    wk_addin = 5
    wk_plan = planunit_shop(exx.wk, addin=wk_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = get_rangeunit_from_lineage_of_plans(
        [wk_plan], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + wk_addin
    new_stop = old_stop + wk_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario3_2PlanUnit_addin():
    # ESTABLISH
    wk_addin = 5
    wk_plan = planunit_shop(exx.wk, addin=wk_addin)
    tue_addin = 7
    tue_plan = planunit_shop("Tue", addin=tue_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = get_rangeunit_from_lineage_of_plans(
        [wk_plan, tue_plan], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + wk_addin + tue_addin
    new_stop = old_stop + wk_addin + tue_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario4_2PlanUnit_numor():
    # ESTABLISH
    wk_numor = 5
    wk_plan = planunit_shop(exx.wk, numor=wk_numor)
    tue_numor = 10
    tue_plan = planunit_shop("Tue", numor=tue_numor)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    plan_list = [wk_plan, tue_plan]

    # WHEN
    new_rangeunit = get_rangeunit_from_lineage_of_plans(
        plan_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo * wk_numor * tue_numor
    new_stop = old_stop * wk_numor * tue_numor
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario5_2PlanUnit_denom():
    # ESTABLISH
    wk_denom = 5
    wk_plan = planunit_shop(exx.wk, denom=wk_denom)
    tue_denom = 2
    tue_plan = planunit_shop("Tue", denom=tue_denom)
    old_gogo = 30
    old_stop = 80
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    plan_list = [wk_plan, tue_plan]

    # WHEN
    new_rangeunit = get_rangeunit_from_lineage_of_plans(
        plan_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_rangeunit.gogo / wk_denom / tue_denom
    new_stop = old_rangeunit.stop / wk_denom / tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 3
    assert new_rangeunit.stop == 8


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario6_2PlanUnit_denom_morph():
    # ESTABLISH
    wk_denom = 50
    wk_plan = planunit_shop(exx.wk, denom=wk_denom, morph=True)
    tue_denom = 20
    tue_plan = planunit_shop("Tue", denom=tue_denom, morph=True)
    old_gogo = 175
    old_stop = 186
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    plan_list = [wk_plan, tue_plan]

    # WHEN
    new_rangeunit = get_rangeunit_from_lineage_of_plans(
        plan_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = (old_rangeunit.gogo % wk_denom) % tue_denom
    new_stop = (old_rangeunit.stop % wk_denom) % tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 5
    assert new_rangeunit.stop == 16


def test_get_rangeunit_from_lineage_of_plans_ReturnsObj_Scenario7_Zero():
    # ESTABLISH
    wk_denom = 50
    wk_plan = planunit_shop(exx.wk, denom=wk_denom, morph=True)
    tue_denom = 20
    tue_plan = planunit_shop("Tue", denom=tue_denom, morph=True)
    ancestor_gogo = 0
    ancestor_stop = 0
    plan_list = [wk_plan, tue_plan]

    # WHEN
    x_rangeunit = get_rangeunit_from_lineage_of_plans(
        plan_list, ancestor_gogo, ancestor_stop
    )

    # THEN
    expected_gogo = (ancestor_gogo % wk_denom) % tue_denom
    expected_stop = (ancestor_stop % wk_denom) % tue_denom
    assert x_rangeunit.gogo == expected_gogo
    assert x_rangeunit.stop == expected_stop
    assert x_rangeunit.gogo == 0
    assert x_rangeunit.stop == 0
