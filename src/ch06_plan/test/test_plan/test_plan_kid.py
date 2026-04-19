from ch04_rope.rope import create_rope
from ch06_plan.plan import planunit_shop
from pytest import raises as pytest_raises
from ref.keywords import Ch06Keywords as kw, ExampleStrs as exx


def test_get_kids_in_range_GetsCorrectPlans():
    # ESTABLISH
    mon_str = "months"
    mon_plan = planunit_shop(mon_str, begin=0, close=366)
    jan_str = "Jan"
    feb_str = "Feb"
    mar_str = "Mar"
    mon_plan.add_kid(planunit_shop(jan_str))
    mon_plan.add_kid(planunit_shop(feb_str))
    mon_plan.add_kid(planunit_shop(mar_str))
    jan_plan = mon_plan.get_kid(jan_str)
    feb_plan = mon_plan.get_kid(feb_str)
    mar_plan = mon_plan.get_kid(mar_str)
    jan_plan.gogo_calc = 0
    jan_plan.stop_calc = 31
    feb_plan.gogo_calc = 31
    feb_plan.stop_calc = 60
    mar_plan.gogo_calc = 60
    mar_plan.stop_calc = 91

    # WHEN / THEN
    assert len(mon_plan.get_kids_in_range(x_gogo=100, x_stop=120)) == 0
    assert len(mon_plan.get_kids_in_range(x_gogo=0, x_stop=31)) == 1
    assert len(mon_plan.get_kids_in_range(x_gogo=5, x_stop=5)) == 1
    assert len(mon_plan.get_kids_in_range(x_gogo=0, x_stop=61)) == 3
    assert len(mon_plan.get_kids_in_range(x_gogo=31, x_stop=31)) == 1
    assert set(mon_plan.get_kids_in_range(x_gogo=31, x_stop=31).keys()) == {feb_str}
    assert list(mon_plan.get_kids_in_range(x_gogo=31, x_stop=31).values()) == [feb_plan]


def test_get_kids_in_range_EmptyParametersReturnsAll_kids():
    # ESTABLISH
    mon_str = "366months"
    mon_plan = planunit_shop(mon_str)
    jan_str = "Jan"
    feb29_str = "Feb29"
    mar_str = "Mar"
    mon_plan.add_kid(planunit_shop(jan_str))
    mon_plan.add_kid(planunit_shop(feb29_str))
    mon_plan.add_kid(planunit_shop(mar_str))

    # WHEN / THEN
    assert len(mon_plan.get_kids_in_range()) == 3


def test_PlanUnit_get_descendants_ReturnsNoRopeTerms():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)

    # WHEN
    nation_descendants = nation_plan.get_descendant_ropes_from_kids()

    # THEN
    assert nation_descendants == {}


def test_PlanUnit_get_descendants_Returns3DescendantsRopeTerms():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)

    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    usa_plan = planunit_shop(usa_str, parent_rope=nation_rope)
    nation_plan.add_kid(usa_plan)

    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    texas_plan = planunit_shop(texas_str, parent_rope=usa_rope)
    usa_plan.add_kid(texas_plan)

    iowa_str = "Iowa"
    iowa_rope = create_rope(usa_rope, iowa_str)
    iowa_plan = planunit_shop(iowa_str, parent_rope=usa_rope)
    usa_plan.add_kid(iowa_plan)

    # WHEN
    nation_descendants = nation_plan.get_descendant_ropes_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_rope) is not None
    assert nation_descendants.get(texas_rope) is not None
    assert nation_descendants.get(iowa_rope) is not None


def test_PlanUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)
    nation_plan.add_kid(nation_plan)
    max_count = 1000

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        nation_plan.get_descendant_ropes_from_kids()
    assert (
        str(excinfo.value)
        == f"Plan '{nation_plan.get_plan_rope()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_PlanUnit_clear_kids_SetsAttr():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)
    nation_plan.add_kid(planunit_shop("USA", parent_rope=nation_rope))
    nation_plan.add_kid(planunit_shop("France", parent_rope=nation_rope))
    assert len(nation_plan.kids) == 2

    # WHEN
    nation_plan.clear_kids()

    # THEN
    assert len(nation_plan.kids) == 0


def test_PlanUnit_get_kid_ReturnsObj():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)

    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    nation_plan.add_kid(planunit_shop(usa_str, parent_rope=nation_rope))

    france_str = "France"
    france_rope = create_rope(nation_rope, france_str)
    nation_plan.add_kid(planunit_shop(france_str, parent_rope=nation_rope))
    assert len(nation_plan.kids) == 2

    # WHEN
    france_plan = nation_plan.get_kid(france_str)

    # THEN
    assert france_plan.plan_label == france_str


def test_PlanUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)

    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    nation_plan.add_kid(planunit_shop(usa_str, parent_rope=nation_rope))

    france_str = "France"
    france_rope = create_rope(nation_rope, france_str)
    nation_plan.add_kid(planunit_shop(france_str, parent_rope=nation_rope))
    assert len(nation_plan.kids) == 2

    # WHEN
    nation_plan.del_kid(france_str)

    # THEN
    assert len(nation_plan.kids) == 1


def test_PlanUnit_get_kids_star_sum_ReturnsObj_Scenario0():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)
    usa_str = "USA"
    usa_plan = planunit_shop(usa_str, parent_rope=nation_rope)
    nation_plan.add_kid(usa_plan)
    france_str = "France"
    france_plan = planunit_shop(france_str, parent_rope=nation_rope)
    nation_plan.add_kid(france_plan)

    # WHEN / THEN
    assert nation_plan.get_kids_star_sum() == 2


def test_PlanUnit_get_kids_star_sum_ReturnsObj_Scenario1():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_plan = planunit_shop(nation_str, parent_rope=amy_str)
    usa_str = "USA"
    usa_plan = planunit_shop(usa_str, star=0, parent_rope=nation_rope)
    nation_plan.add_kid(usa_plan)
    france_str = "France"
    france_plan = planunit_shop(france_str, star=0, parent_rope=nation_rope)
    nation_plan.add_kid(france_plan)

    # WHEN / THEN
    assert nation_plan.get_kids_star_sum() == 0

    # WHEN
    france_str = "France"
    france_plan = planunit_shop(france_str, star=3, parent_rope=nation_rope)
    nation_plan.add_kid(france_plan)

    # WHEN / THEN
    assert nation_plan.get_kids_star_sum() == 3
