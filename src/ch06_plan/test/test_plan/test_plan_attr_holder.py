from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import (
    PlanAttrHolder,
    PlanUnit,
    planattrholder_shop,
    planunit_shop,
)
from src.ch06_plan.test._util.ch06_examples import RangeAttrHolder, get_range_attrs
from src.ref.keywords import Ch06Keywords as kw


def test_PlanAttrHolder_Exists():
    # ESTABLISH / WHEN
    new_obj = PlanAttrHolder()

    # THEN
    assert new_obj.star is None
    assert new_obj.plan_uid is None
    assert new_obj.reason is None
    assert new_obj.reason_context is None
    assert new_obj.reason_case is None
    assert new_obj.reason_lower is None
    assert new_obj.reason_upper is None
    assert new_obj.reason_divisor is None
    assert new_obj.reason_del_case_reason_context is None
    assert new_obj.reason_del_case_reason_state is None
    assert new_obj.reason_requisite_active is None
    assert new_obj.workforceunit is None
    assert new_obj.healerunit is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.morph is None
    assert new_obj.pledge is None
    assert new_obj.factunit is None
    assert new_obj.awardunit is None
    assert new_obj.awardunit_del is None
    assert new_obj.is_expanded is None
    assert set(new_obj.__dict__.keys()) == {
        kw.star,
        kw.plan_uid,
        "reason",
        "reason_context",
        "reason_case",
        kw.reason_lower,
        kw.reason_upper,
        kw.reason_divisor,
        "reason_del_case_reason_context",
        "reason_del_case_reason_state",
        "reason_requisite_active",
        kw.workforceunit,
        kw.healerunit,
        kw.begin,
        kw.close,
        kw.addin,
        kw.numor,
        kw.denom,
        kw.morph,
        kw.pledge,
        "factunit",
        "awardunit",
        "awardunit_del",
        kw.is_expanded,
        kw.problem_bool,
        kw.stop_want,
        kw.gogo_want,
    }


def test_PlanAttrHolder_CalculatesCaseRanges():
    # ESTABLISH
    plan_attr = PlanAttrHolder(reason_case="some_rope")
    assert plan_attr.reason_lower is None
    assert plan_attr.reason_upper is None
    # assert plan_attr.reason_case_numor is None
    assert plan_attr.reason_divisor is None
    # assert plan_attr.reason_case_morph is None

    # WHEN
    plan_attr.set_case_range_influenced_by_case_plan(
        reason_lower=5.0,
        reason_upper=20.0,
        # case_numor,
        case_denom=4.0,
        # case_morph,
    )

    # THEN
    assert plan_attr.reason_lower == 5.0
    assert plan_attr.reason_upper == 20.0
    # assert plan_attr.reason_case_numor is None
    assert plan_attr.reason_divisor == 4.0
    # assert plan_attr.reason_case_morph is None


def test_planattrholder_shop_ReturnsObj():
    # ESTABLISH
    sue_healerunit = healerunit_shop({"Sue", "Yim"})

    # WHEN
    x_planattrholder = planattrholder_shop(healerunit=sue_healerunit)

    # THEN
    assert x_planattrholder.healerunit == sue_healerunit


def test_RangeAttrHolder_Exists():
    # ESTABLISH / WHEN
    x_rangeattrholder = RangeAttrHolder()
    # THEN
    assert not x_rangeattrholder.begin
    assert not x_rangeattrholder.close
    assert not x_rangeattrholder.addin
    assert not x_rangeattrholder.numor
    assert not x_rangeattrholder.denom
    assert not x_rangeattrholder.morph
    assert not x_rangeattrholder.gogo_want
    assert not x_rangeattrholder.stop_want
    assert not x_rangeattrholder.gogo_calc
    assert not x_rangeattrholder.stop_calc


def test_get_range_attrs_ReturnsObj():
    # ESTABLISH
    mop_plan = planunit_shop("mop")
    mop_plan.begin = "arg_begin"
    mop_plan.close = "arg_close"
    mop_plan.addin = "arg_addin"
    mop_plan.numor = "arg_numor"
    mop_plan.denom = "arg_denom"
    mop_plan.morph = "arg_morph"
    mop_plan.gogo_want = "arg_gogo_want"
    mop_plan.stop_want = "arg_stop_want"
    mop_plan.gogo_calc = "arg_gogo_calc"
    mop_plan.stop_calc = "arg_stop_calc"

    # WHEN
    mop_range_attrs = get_range_attrs(mop_plan)

    # THEN
    assert mop_range_attrs.begin == "arg_begin"
    assert mop_range_attrs.close == "arg_close"
    assert mop_range_attrs.addin == "arg_addin"
    assert mop_range_attrs.numor == "arg_numor"
    assert mop_range_attrs.denom == "arg_denom"
    assert mop_range_attrs.morph == "arg_morph"
    assert mop_range_attrs.gogo_want == "arg_gogo_want"
    assert mop_range_attrs.stop_want == "arg_stop_want"
    assert mop_range_attrs.gogo_calc == "arg_gogo_calc"
    assert mop_range_attrs.stop_calc == "arg_stop_calc"
