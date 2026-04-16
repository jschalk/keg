from src.ch06_plan.plan import planunit_shop
from src.ch20_kpi.gcalendar import (
    DayEvent,
    gcal_readable_percent,
    get_gcal_priorities_schedule_str,
    get_inflection_points_dict,
)
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_get_inflection_points_dict_ReturnsObj_Scenario0_EmptyList():
    # ESTABLISH / WHEN / THEN
    assert get_inflection_points_dict([]) == {}


def test_get_inflection_points_dict_ReturnsObj_Scenario1_One_dayevent():
    # ESTABLISH
    x1_plan = planunit_shop(exx.mop, fund_ratio=0.1)
    dayevent = DayEvent(x1_plan, 1, 0, day_min_upper=60)

    # WHEN
    points = get_inflection_points_dict([dayevent])

    # THEN
    assert points == {0: dayevent, 60: None}


def test_get_inflection_points_dict_ReturnsObj_Scenario2_TwoSequential_dayevents_NoOverlap():
    # ESTABLISH
    x_fund_ratio = 0.1
    x_plan = planunit_shop(exx.mop, fund_ratio=x_fund_ratio)
    y0_dayevent = DayEvent(x_plan, 1, 0, day_min_upper=30)
    y1_dayevent = DayEvent(x_plan, 2, 60, day_min_upper=90)

    # WHEN
    inflection_points = get_inflection_points_dict([y0_dayevent, y1_dayevent])

    # THEN
    print(inflection_points)
    assert inflection_points == {0: y0_dayevent, 30: None, 60: y1_dayevent, 90: None}


def test_get_inflection_points_dict_ReturnsObj_Scenario3_Higher_fund_ratio_dayevent_Interrupts():
    # ESTABLISH
    x1_fund_ratio = 0.1
    x1_plan = planunit_shop(exx.mop, fund_ratio=x1_fund_ratio)
    x2_fund_ratio = 0.2
    x2_plan = planunit_shop(exx.mop, fund_ratio=x2_fund_ratio)
    y60_dayevent = DayEvent(x1_plan, 1, 0, day_min_upper=60)
    y90_dayevent = DayEvent(x2_plan, 2, 30, day_min_upper=90)

    # WHEN
    inflection_points = get_inflection_points_dict([y60_dayevent, y90_dayevent])

    # THEN
    print(inflection_points)
    assert inflection_points == {0: y60_dayevent, 30: y90_dayevent, 90: None}


def test_get_inflection_points_dict_ReturnsObj_Scenario4_Lower_fund_ratio_dayevent_DoesNotInterrupt():
    # ESTABLISH
    x1_fund_ratio = 0.1
    x1_plan = planunit_shop(exx.mop, fund_ratio=x1_fund_ratio)
    x2_fund_ratio = 0.01
    x2_plan = planunit_shop(exx.mop, fund_ratio=x2_fund_ratio)
    y60_dayevent = DayEvent(x1_plan, 1, 0, day_min_upper=60)
    y90_dayevent = DayEvent(x2_plan, 2, 30, day_min_upper=90)

    # WHEN
    inflection_points = get_inflection_points_dict([y60_dayevent, y90_dayevent])

    # THEN
    print(inflection_points)
    assert inflection_points == {0: y60_dayevent, 60: y90_dayevent, 90: None}


def test_get_inflection_points_dict_ReturnsObj_Scenario5_Same_fund_ratio_dayevent_DoesNotInterrupt():
    # ESTABLISH
    x1_fund_ratio = 0.1
    x1_plan = planunit_shop(exx.mop, fund_ratio=x1_fund_ratio)
    x2_fund_ratio = 0.1
    assert x1_fund_ratio == x2_fund_ratio
    x2_plan = planunit_shop(exx.mop, fund_ratio=x2_fund_ratio)
    y60_dayevent = DayEvent(x1_plan, 1, 0, day_min_upper=60)
    y90_dayevent = DayEvent(x2_plan, 2, 30, day_min_upper=90)

    # WHEN
    inflection_points = get_inflection_points_dict([y60_dayevent, y90_dayevent])

    # THEN
    print(inflection_points)
    assert inflection_points == {0: y60_dayevent, 60: y90_dayevent, 90: None}


def test_get_gcal_priorities_schedule_str_ReturnsObj_Scenario1_Same_fund_ratio_DayEvent():
    # ESTABLISH
    x1_fund_ratio = 0.1
    x1_plan = planunit_shop(exx.mop, fund_ratio=x1_fund_ratio)
    x2_fund_ratio = 0.1
    assert x1_fund_ratio == x2_fund_ratio
    x2_plan = planunit_shop(exx.casa, fund_ratio=x2_fund_ratio)
    y60_dayevent = DayEvent(x1_plan, 1, 0, day_min_upper=60)
    y90_dayevent = DayEvent(x2_plan, 2, 30, day_min_upper=90)

    # WHEN
    inflection_points_str = get_gcal_priorities_schedule_str(
        [y60_dayevent, y90_dayevent]
    )

    # THEN
    print(inflection_points_str)
    y60_readable_fund_ratio = gcal_readable_percent(y60_dayevent.plan.fund_ratio)
    y90_readable_fund_ratio = gcal_readable_percent(y90_dayevent.plan.fund_ratio)
    expected_str = f"""Schedule Priorities
12:00 AM 1. {exx.mop} {y60_readable_fund_ratio}
1:00 AM 2. {exx.casa} {y90_readable_fund_ratio}
1:30 AM Nothing scheduled."""
    assert inflection_points_str == expected_str
