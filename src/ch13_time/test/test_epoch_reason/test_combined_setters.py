from ch07_person_logic.person_tool import (
    person_plan_reason_caseunit_exists,
    person_plan_reason_caseunit_get_obj,
    person_plan_reasonunit_exists,
    person_plan_reasonunit_get_obj,
)
from ch13_time.epoch_reason import (
    set_epoch_cases_by_args_dict,
    set_epoch_cases_for_dayly,
    set_epoch_cases_for_monthly,
    set_epoch_cases_for_weekly,
    set_epoch_cases_for_yearly_monthday,
)
from ch13_time.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_person,
)
from ref.keywords import Ch13Keywords as kw


def test_set_epoch_cases_for_dayly_SetsAttr_Scenario0_MiddleDayEvery3Days():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
    }
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_days_lower_day = 1
    mop_days_upper_day = 2
    mop_every_xdays = 3
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_xdays_args)

    # WHEN
    set_epoch_cases_for_dayly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
        days_lower_day=mop_days_lower_day,
        days_upper_day=mop_days_upper_day,
        every_xdays=mop_every_xdays,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_xdays_args)
    assert person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)
    day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_dayly_args)
    assert day_case.reason_state == wx.day_rope
    assert day_case.reason_lower == mop_dayly_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_epoch_cases_for_dayly_SetsAttr_Scenario1_IncludeRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_days_lower_day = 1
    mop_days_upper_day = 2
    mop_every_xdays = 3
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_xdays_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_cases_for_dayly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
        days_lower_day=mop_days_lower_day,
        days_upper_day=mop_days_upper_day,
        every_xdays=mop_every_xdays,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_xdays_args)
    assert person_plan_reasonunit_exists(bob_person, mop_range_args)
    assert person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)
    range_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert range_case.reason_state == wx.five_rope
    assert range_case.reason_lower == 200
    assert range_case.reason_upper == 500
    assert range_case.reason_divisor == 5259492000


def test_set_epoch_cases_for_weekly_SetsAttr_Scenario0_ThirdDayEvery7Weeks():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
    }
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
    }
    mop_weekly_lower_min = 600
    mop_weekly_duration_min = 90
    mop_week_lower = 2
    mop_week_upper = 3
    mop_every_xweeks = 7
    assert not person_plan_reasonunit_exists(bob_person, mop_weekly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_xweeks_args)

    # WHEN
    set_epoch_cases_for_weekly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weekly_lower_min=mop_weekly_lower_min,
        weekly_duration_min=mop_weekly_duration_min,
        weeks_lower_week=mop_week_lower,
        weeks_upper_week=mop_week_upper,
        every_xweeks=mop_every_xweeks,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_weekly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_xweeks_args)
    assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
    week_case = person_plan_reason_caseunit_get_obj(bob_person, mop_weekly_args)
    assert week_case.reason_state == wx.week_rope
    assert week_case.reason_lower == mop_weekly_lower_min
    assert week_case.reason_lower == 600
    assert week_case.reason_upper == 690
    assert week_case.reason_divisor == 7200


def test_set_epoch_cases_for_weekly_SetsAttr_Scenario1_IncludeRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
    }
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_weekly_lower_min = 600
    mop_weekly_duration_min = 90
    mop_week_lower = 2
    mop_week_upper = 3
    mop_every_xweeks = 7
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not person_plan_reasonunit_exists(bob_person, mop_weekly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_xweeks_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_cases_for_weekly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        weekly_lower_min=mop_weekly_lower_min,
        weekly_duration_min=mop_weekly_duration_min,
        weeks_lower_week=mop_week_lower,
        weeks_upper_week=mop_week_upper,
        every_xweeks=mop_every_xweeks,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_weekly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_xweeks_args)
    assert person_plan_reasonunit_exists(bob_person, mop_range_args)
    assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
    five_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert five_case.reason_state == wx.five_rope
    assert five_case.reason_lower == mop_range_lower_min
    assert five_case.reason_lower == 200
    assert five_case.reason_upper == mop_range_lower_min + mop_range_duration
    assert five_case.reason_upper == 500
    assert five_case.reason_divisor == 5259492000


def test_set_epoch_cases_for_yearly_monthday_SetsAttr_Scenario0_NoRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    assert not person_plan_reasonunit_exists(bob_person, mop_monthday_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_cases_for_yearly_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
        month_label=wx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_monthday_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)


def test_set_epoch_cases_for_yearly_monthday_SetsAttr_Scenario1_IncludesRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not person_plan_reasonunit_exists(bob_person, mop_monthday_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_cases_for_yearly_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
        month_label=wx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_monthday_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario0_AllDays_within_month_range():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)

    # WHEN
    set_epoch_cases_for_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    year_reasonunit = person_plan_reasonunit_get_obj(bob_person, mop_year_args)
    year_cases = year_reasonunit.cases
    print(f"{year_cases.keys()=}")
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 15


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario1_OneDayNot_within_month_range():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_monthday = 20
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)

    # WHEN
    set_epoch_cases_for_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    year_reasonunit = person_plan_reasonunit_get_obj(bob_person, mop_year_args)
    year_cases = year_reasonunit.cases
    for month_case in year_cases.values():
        print(f"{month_case.reason_state} {month_case.reason_upper=}")
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario2_Include_epoch_five_range():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_monthday = 20
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_cases_for_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_range_args)
    year_reasonunit = person_plan_reasonunit_get_obj(bob_person, mop_year_args)
    year_cases = year_reasonunit.cases
    for month_case in year_cases.values():
        print(f"{month_case.reason_state} {month_case.reason_upper=}")
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14
    range_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert range_case.reason_state == wx.five_rope
    assert range_case.reason_lower == 200
    assert range_case.reason_upper == 500
    assert range_case.reason_divisor == 5259492000


def test_set_epoch_cases_by_args_dict_SetsAttr_Scenario0_dayly_AndIncludeRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_days_lower_day = 1
    mop_days_upper_day = 2
    mop_every_xdays = 3
    mop_range_lower_min = 200
    mop_range_duration = 300
    mop_epoch_cases_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.dayly_lower_min: mop_dayly_lower_min,
        kw.dayly_duration_min: mop_day_duration,
        kw.days_lower_day: mop_days_lower_day,
        kw.days_upper_day: mop_days_upper_day,
        kw.every_xdays: mop_every_xdays,
        kw.range_lower_min: mop_range_lower_min,
        kw.range_duration: mop_range_duration,
    }
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_xdays_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_cases_by_args_dict(bob_person, mop_epoch_cases_args)

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_xdays_args)
    assert person_plan_reasonunit_exists(bob_person, mop_range_args)
    assert person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)
    range_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert range_case.reason_state == wx.five_rope
    assert range_case.reason_lower == 200
    assert range_case.reason_upper == 500
    assert range_case.reason_divisor == 5259492000


def test_set_epoch_cases_by_args_dict_SetsAttr_Scenario1_weekly_AndIncludeRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
    }
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_weekly_lower_min = 600
    mop_weekly_duration_min = 90
    mop_weeks_lower_week = 2
    mop_weeks_upper_week = 3
    mop_every_xweeks = 7
    mop_range_lower_min = 200
    mop_range_duration = 300
    mop_epoch_cases_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.weekly_lower_min: mop_weekly_lower_min,
        kw.weekly_duration_min: mop_weekly_duration_min,
        kw.weeks_lower_week: mop_weeks_lower_week,
        kw.weeks_upper_week: mop_weeks_upper_week,
        kw.every_xweeks: mop_every_xweeks,
        kw.range_lower_min: mop_range_lower_min,
        kw.range_duration: mop_range_duration,
    }
    assert not person_plan_reasonunit_exists(bob_person, mop_weekly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_xweeks_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_cases_by_args_dict(bob_person, mop_epoch_cases_args)

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_weekly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_xweeks_args)
    assert person_plan_reasonunit_exists(bob_person, mop_range_args)
    assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
    five_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert five_case.reason_state == wx.five_rope
    assert five_case.reason_lower == mop_range_lower_min
    assert five_case.reason_lower == 200
    assert five_case.reason_upper == mop_range_lower_min + mop_range_duration
    assert five_case.reason_upper == 500
    assert five_case.reason_divisor == 5259492000


def test_set_epoch_cases_by_args_dict_SetsAttr_Scenario2_yearly_monthday_AndIncludeRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_range_lower_min = 200
    mop_range_duration = 300
    mop_epoch_cases_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.dayly_lower_min: mop_dayly_lower_min,
        kw.dayly_duration_min: mop_day_duration,
        kw.month_label: wx.Geo,
        kw.year_monthday_lower: mop_monthday,
        kw.year_monthday_duration_days: mop_length_days,
        kw.range_lower_min: mop_range_lower_min,
        kw.range_duration: mop_range_duration,
    }
    assert not person_plan_reasonunit_exists(bob_person, mop_monthday_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)
    assert not person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)

    # WHEN
    set_epoch_cases_by_args_dict(bob_person, mop_epoch_cases_args)

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_monthday_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)


def test_set_epoch_cases_by_args_dict_SetsAttr_Scenario3_monthly_AndIncludeRange():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_monthday = 20
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    mop_range_lower_min = 200
    mop_range_duration = 300
    mop_epoch_cases_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.monthly_monthday_lower: mop_monthday,
        kw.monthly_duration_days: mop_length_days,
        kw.dayly_lower_min: mop_dayly_lower_min,
        kw.dayly_duration_min: mop_day_duration,
        kw.range_lower_min: mop_range_lower_min,
        kw.range_duration: mop_range_duration,
    }
    assert not person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert not person_plan_reasonunit_exists(bob_person, mop_range_args)

    # WHEN
    set_epoch_cases_by_args_dict(bob_person, mop_epoch_cases_args)

    # THEN
    assert person_plan_reasonunit_exists(bob_person, mop_year_args)
    assert person_plan_reasonunit_exists(bob_person, mop_dayly_args)
    assert person_plan_reasonunit_exists(bob_person, mop_range_args)
    year_reasonunit = person_plan_reasonunit_get_obj(bob_person, mop_year_args)
    year_cases = year_reasonunit.cases
    for month_case in year_cases.values():
        print(f"{month_case.reason_state} {month_case.reason_upper=}")
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_person.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14
    range_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
    assert range_case.reason_state == wx.five_rope
    assert range_case.reason_lower == 200
    assert range_case.reason_upper == 500
    assert range_case.reason_divisor == 5259492000
