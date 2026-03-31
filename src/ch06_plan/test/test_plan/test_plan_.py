from src.ch01_allot.allot import default_grain_num_if_None
from src.ch02_partner.group import awardunit_shop
from src.ch03_workforce.workforce import workforceunit_shop
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import PlanUnit, planunit_shop
from src.ref.keywords import Ch06Keywords as kw, ExampleStrs as exx


def test_PlanUnit_Exists():
    # ESTABLISH
    x_planunit = PlanUnit()

    # WHEN / THEN
    assert x_planunit
    assert x_planunit.kids is None
    assert x_planunit.star is None
    assert x_planunit.plan_label is None
    assert x_planunit.plan_uid is None
    assert x_planunit.reasonunits is None
    assert x_planunit.reasonheirs is None  # calculated field
    assert x_planunit.workforceunit is None
    assert x_planunit.workforceheir is None  # calculated field
    assert x_planunit.factunits is None
    assert x_planunit.factheirs is None  # calculated field
    assert x_planunit.awardunits is None
    assert x_planunit.awardlines is None  # calculated field'
    assert x_planunit.awardheirs is None  # calculated field'
    assert x_planunit.knot is None
    assert x_planunit.begin is None
    assert x_planunit.close is None
    assert x_planunit.addin is None
    assert x_planunit.numor is None
    assert x_planunit.denom is None
    assert x_planunit.morph is None
    assert x_planunit.gogo_want is None
    assert x_planunit.stop_want is None
    assert x_planunit.pledge is None
    assert x_planunit.problem_bool is None
    assert x_planunit.healerunit is None
    # calculated_fields
    assert x_planunit.range_evaluated is None
    assert x_planunit.gogo_calc is None
    assert x_planunit.stop_calc is None
    assert x_planunit.descendant_pledge_count is None
    assert x_planunit.is_expanded is None
    assert x_planunit.all_partner_cred is None
    assert x_planunit.all_partner_debt is None
    assert x_planunit.tree_level is None
    assert x_planunit.plan_active_hx is None
    assert x_planunit.fund_ratio is None
    assert x_planunit.fund_grain is None
    assert x_planunit.fund_onset is None
    assert x_planunit.fund_cease is None
    assert x_planunit.healerunit_ratio is None
    obj_attrs = set(x_planunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.plan_active,
        kw.plan_active_hx,
        kw.all_partner_cred,
        kw.all_partner_debt,
        kw.awardheirs,
        kw.awardlines,
        kw.descendant_pledge_count,
        kw.factheirs,
        kw.fund_cease,
        kw.fund_onset,
        kw.fund_ratio,
        kw.gogo_calc,
        kw.healerunit_ratio,
        kw.is_expanded,
        kw.kids,
        kw.workforceheir,
        kw.tree_level,
        kw.range_evaluated,
        kw.reasonheirs,
        kw.stop_calc,
        kw.plan_task,
        kw.plan_uid,
        kw.addin,
        kw.awardunits,
        kw.begin,
        kw.knot,
        kw.close,
        kw.plan_label,
        kw.denom,
        kw.factunits,
        kw.fund_grain,
        kw.gogo_want,
        kw.healerunit,
        kw.workforceunit,
        kw.star,
        kw.morph,
        kw.numor,
        kw.parent_rope,
        kw.pledge,
        kw.problem_bool,
        kw.reasonunits,
        kw.stop_want,
    }


from pytest import raises as pytest_raises
from src.ch06_plan.plan import planunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_set_plan_label_Scenario0_SetsAttr():
    # ESTABLISH
    el_paso_str = "El Paso"
    el_paso_plan = planunit_shop(el_paso_str)
    assert el_paso_plan.plan_label != exx.casa

    # WHEN
    el_paso_plan.set_plan_label(exx.casa)

    # THEN
    assert el_paso_plan.plan_label == exx.casa


def test_PlanUnit_set_plan_label_Scenario1_RaisesErrorWhen_plan_label_IsNone():
    # ESTABLISH
    casa_plan = planunit_shop(exx.casa)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_plan.set_plan_label(plan_label=None)
    assert str(excinfo.value) == "Cannot set Plan's Label empty or None"


def test_planunit_shop_ReturnsObj_Scenario0_WithOneParameter():
    # ESTABLISH

    # WHEN
    x_planunit = planunit_shop(exx.casa)

    # THEN
    assert x_planunit
    assert x_planunit.kids == {}
    assert x_planunit.star == 1
    assert x_planunit.plan_label == exx.casa
    assert not x_planunit.plan_uid
    assert not x_planunit.begin
    assert not x_planunit.close
    assert not x_planunit.addin
    assert not x_planunit.numor
    assert not x_planunit.denom
    assert not x_planunit.morph
    assert x_planunit.pledge is False
    assert x_planunit.problem_bool is False
    assert x_planunit.descendant_pledge_count is None
    assert x_planunit.awardlines == {}
    assert x_planunit.awardunits == {}
    assert x_planunit.awardheirs == {}
    assert x_planunit.is_expanded is True
    assert x_planunit.factheirs == {}
    assert x_planunit.factunits == {}
    assert x_planunit.healerunit == healerunit_shop()
    assert x_planunit.gogo_calc is None
    assert x_planunit.stop_calc is None
    assert x_planunit.tree_level is None
    assert x_planunit.plan_active_hx == {}
    assert x_planunit.fund_ratio is None
    assert x_planunit.fund_grain == default_grain_num_if_None()
    assert x_planunit.fund_onset is None
    assert x_planunit.fund_cease is None
    assert x_planunit.reasonunits == {}
    assert x_planunit.reasonheirs == {}
    assert x_planunit.workforceunit == workforceunit_shop()
    assert x_planunit.workforceheir is None
    assert x_planunit.knot == default_knot_if_None()
    assert x_planunit.all_partner_cred is None
    assert x_planunit.all_partner_debt is None
    assert x_planunit.healerunit_ratio == 0


def test_planunit_shop_ReturnsObj_Scenario1_Allows_starToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_planunit = planunit_shop("run", star=zero_int)
    # THEN
    assert x_planunit.star == zero_int


def test_planunit_shop_ReturnsObj_Scenario2_ConvertsNegative_starToZero():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_planunit = planunit_shop("run", star=negative_int)
    # THEN
    zero_int = 0
    assert x_planunit.star == zero_int


def test_planunit_shop_ReturnsObj_Scenario3_Given_healerunit_Parameter():
    # ESTABLISH
    x_healerunit = healerunit_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_grain = 88

    # WHEN
    x_planunit = planunit_shop(
        exx.clean,
        healerunit=x_healerunit,
        problem_bool=x_problem_bool,
        fund_grain=x_fund_grain,
    )

    # THEN
    assert x_planunit.healerunit == x_healerunit
    assert x_planunit.problem_bool == x_problem_bool
    assert x_planunit.fund_grain == x_fund_grain


def test_planunit_shop_ReturnsObj_Scenario4_ReturnsObjWith_awardunits():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardunit = awardunit_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_title = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardunit = awardunit_shop(swim_group_title, swim_give_force, swim_take_force)
    x_awardunits = {
        swim_awardunit.awardee_title: swim_awardunit,
        biker_awardunit.awardee_title: biker_awardunit,
    }

    # WHEN
    sport_str = "sport"
    sport_plan = planunit_shop(plan_label=sport_str, awardunits=x_awardunits)

    # THEN
    assert sport_plan.awardunits == x_awardunits


def test_planunit_shop_ReturnsObj_Scenario5_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_str = "sport"
    sport_plan = planunit_shop(
        sport_str, gogo_want=sport_gogo_want, stop_want=sport_stop_want
    )

    # THEN
    assert sport_plan.gogo_want == sport_gogo_want
    assert sport_plan.stop_want == sport_stop_want


def test_PlanUnit_get_obj_key_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    red_plan = planunit_shop(exx.red)

    # THEN
    assert red_plan.get_obj_key() == exx.red


def test_PlanUnit_set_knot_SetsAttr():
    # ESTABLISH
    casa_plan = planunit_shop(exx.casa)
    casa_plan.set_parent_rope("")

    # WHEN
    casa_plan.set_knot(exx.slash)

    # THEN
    assert casa_plan.knot == exx.slash


def test_PlanUnit_get_obj_key_ReturnsObj_Scenario1():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(exx.a23, round_str)
    ball_str = "ball"

    # WHEN
    ball_plan = planunit_shop(plan_label=ball_str, parent_rope=round_rope)

    # THEN
    assert ball_plan.get_obj_key() == ball_str


def test_PlanUnit_get_rope_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(exx.a23, round_str, knot=exx.slash)
    ball_str = "ball"

    # WHEN
    ball_plan = planunit_shop(ball_str, parent_rope=round_rope, knot=exx.slash)

    # THEN
    ball_rope = create_rope(round_rope, ball_str, knot=exx.slash)
    assert ball_plan.get_plan_rope() == ball_rope


def test_PlanUnit_set_parent_rope_SetsAttr():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(exx.a23, round_str, knot=exx.slash)
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, parent_rope=round_rope, knot=exx.slash)
    assert ball_plan.parent_rope == round_rope

    # WHEN
    sports_rope = create_rope(exx.a23, "sports", knot=exx.slash)
    ball_plan.set_parent_rope(parent_rope=sports_rope)

    # THEN
    assert ball_plan.parent_rope == sports_rope


def test_PlanUnit_clear_descendant_pledge_count_SetsAttr_ToNone():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, descendant_pledge_count=55)
    assert ball_plan.descendant_pledge_count == 55

    # WHEN
    ball_plan.clear_descendant_pledge_count()

    # THEN
    assert ball_plan.descendant_pledge_count is None


def test_PlanUnit_add_to_descendant_pledge_count_SetsAttr_AddsToCount():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, descendant_pledge_count=55)
    ball_plan.clear_descendant_pledge_count()
    assert not ball_plan.descendant_pledge_count

    # WHEN
    ball_plan.add_to_descendant_pledge_count(44)

    # THEN
    assert ball_plan.descendant_pledge_count == 44

    # WHEN
    ball_plan.add_to_descendant_pledge_count(33)

    # THEN
    assert ball_plan.descendant_pledge_count == 77


def test_PlanUnit_has_begin_close_ReturnsObj():
    # ESTABLISH
    swim_plan = planunit_shop(exx.swim)
    assert not swim_plan.has_begin_close()
    # WHEN
    swim_plan.begin = 9
    # THEN
    assert not swim_plan.has_begin_close()
    # WHEN
    swim_plan.close = 10
    # THEN
    assert swim_plan.has_begin_close()
    # WHEN
    swim_plan.begin = None
    # THEN
    assert not swim_plan.has_begin_close()


def test_PlanUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_plan = planunit_shop(num_range_str)
    num_range_plan.range_evaluated = True
    num_range_plan.gogo_calc = 3
    num_range_plan.stop_calc = 4
    assert num_range_plan.range_evaluated
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan.clear_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.range_evaluated
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert not num_range_plan.range_evaluated
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.range_evaluated
    assert num_range_plan.gogo_calc == init_gogo_calc / num_range_denom
    assert num_range_plan.stop_calc == init_stop_calc / num_range_denom
    assert num_range_plan.gogo_calc == 3
    assert num_range_plan.stop_calc == 6


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == 0
    assert num_range_plan.stop_calc == num_range_denom
    assert num_range_plan.gogo_calc == 0
    assert num_range_plan.stop_calc == 7


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == 0
    assert (
        num_range_plan.stop_calc == (init_stop_calc - init_gogo_calc) % num_range_denom
    )
    assert num_range_plan.gogo_calc == 0
    assert num_range_plan.stop_calc == 3


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == init_gogo_calc % num_range_denom
    assert num_range_plan.stop_calc == init_stop_calc % num_range_denom
    assert num_range_plan.gogo_calc == 1
    assert num_range_plan.stop_calc == 4


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == gogo_want
    assert num_range_plan.stop_calc == stop_want
    assert num_range_plan.gogo_calc == 30
    assert num_range_plan.stop_calc == 40


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc
    assert num_range_plan.gogo_calc == 21
    assert num_range_plan.stop_calc == 45


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == stop_want
    assert num_range_plan.gogo_calc == 21
    assert num_range_plan.stop_calc == 40


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == gogo_want
    assert num_range_plan.stop_calc == init_stop_calc
    assert num_range_plan.gogo_calc == 30
    assert num_range_plan.stop_calc == 45


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc
