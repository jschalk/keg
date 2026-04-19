from ch07_person_logic.person_main import get_sorted_plan_list, personunit_shop
from ch07_person_logic.person_tool import (
    get_person_root_facts_dict,
    person_plan_reason_caseunit_exists,
    person_plan_reason_caseunit_get_obj,
    person_plan_reasonunit_exists,
    person_plan_reasonunit_get_obj,
)
from ch13_time.epoch_reason import (
    set_epoch_base_case_dayly,
    set_epoch_base_case_monthday,
    set_epoch_base_case_monthly,
    set_epoch_base_case_range,
    set_epoch_base_case_weekly,
    set_epoch_base_case_xdays,
    set_epoch_base_case_xweeks,
)
from ch13_time.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_person,
)
from ref.keywords import Ch13Keywords as kw


def test_set_epoch_base_case_dayly_SetsAttr_Scenario0_NoWarppingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_dayly_lower_min = 600
    mop_dayly_duration_min = 90
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)

    # WHEN
    set_epoch_base_case_dayly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_dayly_duration_min,
    )

    # THEN
    print(f"{get_person_root_facts_dict(bob_person)=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_dayly_args)
    assert day_case.reason_state == wx.day_rope
    assert day_case.reason_lower == mop_dayly_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_epoch_base_case_dayly_SetsAttr_Scenario1_WarppingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    bob_person.conpute()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_dayly_lower_min = 2000
    mop_day_duration = 95
    assert bob_person.plan_exists(wx.day_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)

    # WHEN
    set_epoch_base_case_dayly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
    )

    # THEN
    print(f"{wx.day_rope=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_dayly_args)
    assert day_case.reason_state == wx.day_rope
    assert day_case.reason_lower == mop_dayly_lower_min % 1440
    assert day_case.reason_lower == 560
    assert day_case.reason_upper == 655
    assert day_case.reason_divisor == 1440
    # for x_plan in get_sorted_plan_list(bob_person._plan_dict):
    #     print(f"{x_plan.get_plan_rope()=}")


def test_set_epoch_base_case_dayly_SetsAttr_Scenario2_ParametersAreNone():
    # ESTABLISH
    bob_person = get_bob_five_person()
    bob_person.conpute()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    assert bob_person.plan_exists(wx.day_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)

    # WHEN
    set_epoch_base_case_dayly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=None,
        dayly_duration_min=None,
    )

    # THEN
    assert not person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)


def test_set_epoch_base_case_xdays_SetsAttr_Scenario0_NoWarppingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    days_rope = bob_person.make_rope(wx.five_rope, kw.days)
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: days_rope,
        kw.reason_state: days_rope,
    }
    mop_every_xdays = 7
    mop_days_lower_day = 3
    mop_days_upper_day = 5
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)
    bob_person.conpute()
    for x_plan in get_sorted_plan_list(bob_person._plan_dict):
        print(f"{x_plan.get_plan_rope()=}")

    # WHEN
    set_epoch_base_case_xdays(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        days_lower_day=mop_days_lower_day,
        days_upper_day=mop_days_upper_day,
        every_xdays=mop_every_xdays,
    )

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)
    xdays_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xdays_args)
    assert xdays_case.reason_state == days_rope
    assert xdays_case.reason_lower == mop_days_lower_day
    assert xdays_case.reason_upper == mop_days_upper_day
    assert xdays_case.reason_upper == 5
    assert xdays_case.reason_divisor == mop_every_xdays


def test_set_epoch_base_case_xdays_SetsAttr_Scenario1_WarppingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    days_rope = bob_person.make_rope(wx.five_rope, kw.days)
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: days_rope,
        kw.reason_state: days_rope,
    }
    mop_every_xdays = 7
    mop_days_lower_day = 30
    mop_days_upper_day = 56
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)

    # WHEN
    set_epoch_base_case_xdays(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        days_lower_day=mop_days_lower_day,
        days_upper_day=mop_days_upper_day,
        every_xdays=mop_every_xdays,
    )

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)
    xdays_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xdays_args)
    assert xdays_case.reason_state == days_rope
    assert xdays_case.reason_lower == mop_days_lower_day % 7
    assert xdays_case.reason_upper == mop_days_upper_day % 7
    assert xdays_case.reason_upper == 0
    assert xdays_case.reason_divisor == mop_every_xdays


def test_set_epoch_base_case_xdays_SetsAttr_Scenario2_ParametersAreNone():
    # ESTABLISH
    bob_person = get_bob_five_person()
    days_rope = bob_person.make_rope(wx.five_rope, kw.days)
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: days_rope,
        kw.reason_state: days_rope,
    }
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)

    # WHEN
    set_epoch_base_case_xdays(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        days_lower_day=None,
        days_upper_day=None,
        every_xdays=None,
    )

    # THEN
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)


def test_set_epoch_base_case_weekly_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    week_rope = bob_person.make_rope(wx.five_rope, kw.week)
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: week_rope,
        kw.reason_state: week_rope,
    }
    mop_weekly_lower_min = 600
    mop_weekly_duration = 90
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)

    # WHEN
    set_epoch_base_case_weekly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weekly_lower_min=mop_weekly_lower_min,
        weekly_duration_min=mop_weekly_duration,
    )

    # THEN
    print(f"{week_rope=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_weekly_args)
    assert day_case.reason_state == week_rope
    assert day_case.reason_lower == mop_weekly_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 7200


def test_set_epoch_base_case_weekly_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    week_rope = bob_person.make_rope(wx.five_rope, kw.week)
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: week_rope,
        kw.reason_state: week_rope,
    }
    mop_weekly_lower_min = 7000
    mop_weekly_duration = 800
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)

    # WHEN
    set_epoch_base_case_weekly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weekly_lower_min=mop_weekly_lower_min,
        weekly_duration_min=mop_weekly_duration,
    )

    # THEN
    print(f"{week_rope=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_weekly_args)
    assert day_case.reason_state == week_rope
    assert day_case.reason_lower == mop_weekly_lower_min
    assert day_case.reason_lower == 7000
    assert day_case.reason_upper == 600
    assert day_case.reason_divisor == 7200


def test_set_epoch_base_case_weekly_SetsAttr_Scenario2_ParametersAreNone():
    # ESTABLISH
    bob_person = get_bob_five_person()
    week_rope = bob_person.make_rope(wx.five_rope, kw.week)
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: week_rope,
        kw.reason_state: week_rope,
    }
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)

    # WHEN
    set_epoch_base_case_weekly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weekly_lower_min=None,
        weekly_duration_min=None,
    )

    # THEN
    print(f"{week_rope=}")
    assert not person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)


def test_set_epoch_base_case_xweeks_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    weeks_rope = bob_person.make_rope(wx.five_rope, kw.weeks)
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: weeks_rope,
        kw.reason_state: weeks_rope,
    }
    mop_every_xweeks = 7
    mop_week_lower = 3
    mop_week_upper = 5
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)

    # WHEN
    set_epoch_base_case_xweeks(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weeks_lower_week=mop_week_lower,
        weeks_upper_week=mop_week_upper,
        every_xweeks=mop_every_xweeks,
    )

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)
    xweeks_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xweeks_args)
    assert xweeks_case.reason_state == weeks_rope
    assert xweeks_case.reason_lower == mop_week_lower
    assert xweeks_case.reason_upper == mop_week_upper
    assert xweeks_case.reason_upper == 5
    assert xweeks_case.reason_divisor == mop_every_xweeks


def test_set_epoch_base_case_xweeks_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    weeks_rope = bob_person.make_rope(wx.five_rope, kw.weeks)
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: weeks_rope,
        kw.reason_state: weeks_rope,
    }
    mop_every_xweeks = 7
    mop_week_lower = 30
    mop_week_upper = 56
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)

    # WHEN
    set_epoch_base_case_xweeks(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weeks_lower_week=mop_week_lower,
        weeks_upper_week=mop_week_upper,
        every_xweeks=mop_every_xweeks,
    )

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)
    xweeks_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xweeks_args)
    assert xweeks_case.reason_state == weeks_rope
    assert xweeks_case.reason_lower == mop_week_lower % 7
    assert xweeks_case.reason_upper == mop_week_upper % 7
    assert xweeks_case.reason_upper == 0
    assert xweeks_case.reason_divisor == mop_every_xweeks


def test_set_epoch_base_case_xweeks_SetsAttr_Scenario2_NoParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    weeks_rope = bob_person.make_rope(wx.five_rope, kw.weeks)
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: weeks_rope,
        kw.reason_state: weeks_rope,
    }
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)

    # WHEN
    set_epoch_base_case_xweeks(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weeks_lower_week=None,
        weeks_upper_week=None,
        every_xweeks=None,
    )

    # THEN
    assert not person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)


def test_set_epoch_base_case_range_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_range_lower_min = 600
    mop_range_duration = 90
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_base_case_range(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        range_lower_min=mop_range_lower_min,
        range_duration_min=mop_range_duration,
    )

    # THEN
    print(f"{wx.five_rope=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_range_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert day_case.reason_state == wx.five_rope
    assert day_case.reason_lower == mop_range_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 5259492000
    assert day_case.reason_divisor == bob_person.get_plan_obj(wx.five_rope).close


def test_set_epoch_base_case_range_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    week_rope = bob_person.make_rope(wx.five_rope, kw.week)
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_range_lower_min = 5259490000
    mop_range_duration = 8000
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_base_case_range(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        range_lower_min=mop_range_lower_min,
        range_duration_min=mop_range_duration,
    )

    # THEN
    print(f"{week_rope=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_range_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert day_case.reason_state == wx.five_rope
    assert day_case.reason_lower == mop_range_lower_min
    assert day_case.reason_lower == 5259490000
    assert day_case.reason_upper == 6000
    assert day_case.reason_divisor == 5259492000


def test_set_epoch_base_case_range_SetsAttr_Scenario2_ParametersAreNone():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_base_case_range(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        range_lower_min=None,
        range_duration_min=None,
    )

    # THEN
    assert not person_plan_reason_caseunit_exists(bob_person, mop_range_args)


def test_set_epoch_base_case_monthday_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_fred_rope = bob_person.make_rope(wx.five_year_rope, wx.Fredrick)
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    print(f"geo rope  ='{month_geo_rope}")
    # bob_person.conpute()
    # for x_plan in get_sorted_plan_list(bob_person._plan_dict):
    #     print(f"{x_plan.get_plan_rope()=}")
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        month_label=wx.Geo,
        year_monthday_lower=mop_monthday,
        year_monthday_duration_days=mop_length_days,
    )

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_monthday_args)
    assert day_case.reason_state == month_geo_rope
    month_geo_plan = bob_person.get_plan_obj(month_geo_rope)
    print(f"{month_geo_plan.gogo_want=} {month_geo_plan.stop_want=}")
    expected_monthdayly_lower_min = mop_monthday * 1440 + month_geo_plan.gogo_want
    expected_monthdays_upper_day_min = day_case.reason_lower + (mop_length_days * 1440)
    assert day_case.reason_lower == expected_monthdayly_lower_min
    assert day_case.reason_lower == 40320
    assert day_case.reason_upper == expected_monthdays_upper_day_min
    assert day_case.reason_divisor is None


def test_set_epoch_base_case_monthday_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_trump_rope,
        kw.reason_state: month_trump_rope,
    }
    mop_monthday = 40
    mop_length_days = 3
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        month_label=wx.Trump,
        year_monthday_lower=mop_monthday,
        year_monthday_duration_days=mop_length_days,
    )

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)
    monthday_case = person_plan_reason_caseunit_get_obj(bob_person, mop_monthday_args)
    month_trump_plan = bob_person.get_plan_obj(month_trump_rope)
    year_plan = bob_person.get_plan_obj(wx.five_year_rope)
    expected_lower = month_trump_plan.gogo_want + (mop_monthday * 1440)
    expected_upper = monthday_case.reason_lower + (mop_length_days * 1440)
    expected_lower = expected_lower % year_plan.denom
    expected_upper = expected_upper % year_plan.denom

    print(f"{month_trump_plan.gogo_want=} {month_trump_plan.stop_want=}")
    print(f"{monthday_case.reason_lower=} {monthday_case.reason_upper=}")
    print(f"            {expected_lower=}             {expected_upper=}")
    # print(f"{get_range_attrs(year_plan)=}")
    print(f"{year_plan.denom=}")
    assert monthday_case.reason_state == month_trump_rope
    assert monthday_case.reason_lower == expected_lower
    assert monthday_case.reason_lower == 36000
    assert monthday_case.reason_upper == expected_upper
    assert monthday_case.reason_upper == 40320
    assert monthday_case.reason_divisor is None


def test_set_epoch_base_case_monthday_SetsAttr_Scenario2_monthday_MustBeWithinMonth():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_monthday = 40
    mop_length_days = 3
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        month_label=wx.Geo,
        year_monthday_lower=mop_monthday,
        year_monthday_duration_days=mop_length_days,
        range_must_be_within_month=True,
    )

    # THEN
    month_geo_plan = bob_person.get_plan_obj(month_geo_rope)
    month_geo_minutes = month_geo_plan.stop_want - month_geo_plan.gogo_want
    print(f"{month_geo_minutes=} {mop_monthday*1440=}")
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)


def test_set_epoch_base_case_monthday_SetsAttr_Scenario3_monthday_Reduce_length_days_ToBeWithinMonth():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_monthday = 20
    mop_length_days = 40
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        month_label=wx.Geo,
        year_monthday_lower=mop_monthday,
        year_monthday_duration_days=mop_length_days,
        range_must_be_within_month=True,
    )

    # THEN
    month_geo_plan = bob_person.get_plan_obj(month_geo_rope)
    month_geo_minutes = month_geo_plan.stop_want - month_geo_plan.gogo_want
    print(f"{month_geo_minutes=} {mop_monthday*1440=}")
    assert person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)
    monthday_case = person_plan_reason_caseunit_get_obj(bob_person, mop_monthday_args)
    month_geo_plan = bob_person.get_plan_obj(month_geo_rope)
    year_plan = bob_person.get_plan_obj(wx.five_year_rope)
    expected_lower = month_geo_plan.gogo_want + (mop_monthday * 1440)
    not_expected_upper = monthday_case.reason_lower + (mop_length_days * 1440)
    expected_lower = expected_lower % year_plan.denom
    not_expected_upper = not_expected_upper % year_plan.denom

    print(f"{month_geo_plan.gogo_want=} {month_geo_plan.stop_want=}")
    print(f"{monthday_case.reason_lower=} {monthday_case.reason_upper=}")
    print(f"            {expected_lower=}         {not_expected_upper=}")
    # print(f"{get_range_attrs(year_plan)=}")
    print(f"{year_plan.denom=}")
    assert monthday_case.reason_state == month_geo_rope
    assert monthday_case.reason_lower == expected_lower
    assert monthday_case.reason_lower == 64800
    assert monthday_case.reason_upper == month_geo_plan.stop_want
    assert monthday_case.reason_upper == 72000
    assert monthday_case.reason_upper != not_expected_upper
    assert monthday_case.reason_divisor is None


def test_set_epoch_base_case_monthday_SetsAttr_Scenario4_ParametersAreNone():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    assert bob_person.plan_exists(wx.five_rope)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        month_label=None,
        year_monthday_lower=None,
        year_monthday_duration_days=None,
    )

    # THEN
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)


def test_set_epoch_base_case_monthly_SetsAttr_Scenario0_AllDays_within_month_range():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_monthday = 3
    mop_monthly_duration_days = 4
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)

    # WHEN
    set_epoch_base_case_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthly_monthday_lower=mop_monthday,
        monthly_duration_days=mop_monthly_duration_days,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_year_args)
    year_reasonunit = person_plan_reasonunit_get_obj(bob_person, mop_year_args)
    year_cases = year_reasonunit.cases
    print(f"{year_cases.keys()=}")
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 15


def test_set_epoch_base_case_monthly_SetsAttr_Scenario1_OneDayNot_within_month_range():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_monthday = 20
    mop_duration_days = 4
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)

    # WHEN
    set_epoch_base_case_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthly_monthday_lower=mop_monthday,
        monthly_duration_days=mop_duration_days,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_year_args)
    year_reasonunit = person_plan_reasonunit_get_obj(bob_person, mop_year_args)
    year_cases = year_reasonunit.cases
    for month_case in year_cases.values():
        print(f"{month_case.reason_state} {month_case.reason_upper=}")
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14


def test_set_epoch_base_case_monthly_SetsAttr_Scenario2_ParametersAreNone():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)

    # WHEN
    set_epoch_base_case_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthly_monthday_lower=None,
        monthly_duration_days=None,
    )

    # THEN
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)
