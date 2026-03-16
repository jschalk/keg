from src.ch00_py.dict_toolbox import (
    get_1_if_None,
    get_empty_str_if_None,
    get_False_if_None,
    modular_addition,
)
from src.ch04_rope.rope import is_sub_rope
from src.ch05_reason.reason_main import CaseUnit, FactUnit, ReasonUnit
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PersonUnit
from src.ch07_person_logic.person_tool import (
    add_frame_to_personunit,
    person_plan_reason_caseunit_set_obj,
    person_planunit_exists,
    person_planunit_get_obj,
)
from src.ch13_time._ref.ch13_semantic_types import LabelTerm, RopeTerm, TimeNum
from src.ch13_time.epoch_main import (
    get_day_rope,
    get_epoch_rope,
    get_week_rope,
    get_year_rope,
)


def calculate_dayly_lower_min(dayly_lower_min: int, day_plan_denom: int) -> int:
    return dayly_lower_min % day_plan_denom


def calculate_days_upper_day_min(
    dayly_lower_min: int, dayly_duration_min: int, day_plan_denom: int
) -> int:
    return (dayly_lower_min + dayly_duration_min) % day_plan_denom


def set_epoch_base_case_dayly(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    dayly_lower_min: int,
    dayly_duration_min: int,
):
    """Given an epoch_label set reason for a plan that would make it a dayly occurance
    Example:
    Given: sue_personunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between 10am and 11:30am in lizzy9 epoch
    """
    if dayly_lower_min and dayly_duration_min:
        day_rope = get_day_rope(x_person, epoch_label)
        day_plan = x_person.get_plan_obj(day_rope)
        calc_dayly_lower_min = calculate_dayly_lower_min(
            dayly_lower_min, day_plan.denom
        )
        calc_days_upper_day_min = calculate_days_upper_day_min(
            dayly_lower_min, dayly_duration_min, day_plan.denom
        )
        case_args = {
            "plan_rope": plan_rope,
            "reason_context": day_rope,
            "reason_state": day_rope,
            "reason_lower": calc_dayly_lower_min,
            "reason_upper": calc_days_upper_day_min,
        }
        person_plan_reason_caseunit_set_obj(x_person, case_args)


def set_epoch_base_case_weekly(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    weekly_lower_min: int,
    weekly_duration_min: int,
):
    """Given an epoch_label set reason for a plan that would make it a weekly occurance
    Example:
    Given: sue_personunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=3000, duration=90
    Add a reason to mop_plan that indicates it's to be active between minute 3000 and minute 3090 of the week
    """
    if weekly_lower_min and weekly_duration_min:
        week_rope = get_week_rope(x_person, epoch_label)
        week_plan = x_person.get_plan_obj(week_rope)

        case_args = {
            "plan_rope": plan_rope,
            "reason_context": week_rope,
            "reason_state": week_rope,
            "reason_lower": weekly_lower_min,
            "reason_upper": (weekly_lower_min + weekly_duration_min) % week_plan.denom,
        }
        person_plan_reason_caseunit_set_obj(x_person, case_args)


def set_epoch_base_case_range(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    range_lower_min: int,
    range_duration_min: int,
):
    """Given an epoch_label set reason for a plan that would make it a weekly occurance
    Example:
    Given: sue_personunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between minute 600 and minute 690 of the week
    """
    if range_lower_min and range_duration_min:
        time_rope = x_person.make_l1_rope("time")
        epoch_rope = x_person.make_rope(time_rope, epoch_label)
        epoch_plan = x_person.get_plan_obj(epoch_rope)

        case_args = {
            "plan_rope": plan_rope,
            "reason_context": epoch_rope,
            "reason_state": epoch_rope,
            "reason_lower": range_lower_min,
            "reason_upper": (range_lower_min + range_duration_min) % epoch_plan.close,
            "reason_divisor": epoch_plan.close,
        }
        person_plan_reason_caseunit_set_obj(x_person, case_args)


def set_epoch_base_case_xweeks(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    weeks_lower_week: int,
    weeks_upper_week: int,
    every_xweeks: int,
):
    if weeks_lower_week and weeks_upper_week and every_xweeks:
        time_rope = x_person.make_l1_rope("time")
        epoch_rope = x_person.make_rope(time_rope, epoch_label)
        weeks_rope = x_person.make_rope(epoch_rope, "weeks")

        case_args = {
            "plan_rope": plan_rope,
            "reason_context": weeks_rope,
            "reason_state": weeks_rope,
            "reason_lower": weeks_lower_week % every_xweeks,
            "reason_upper": weeks_upper_week % every_xweeks,
            "reason_divisor": every_xweeks,
        }
        person_plan_reason_caseunit_set_obj(x_person, case_args)


def set_epoch_base_case_xdays(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    days_lower_day: int,
    days_upper_day: int,
    every_xdays: int,
):
    """Given an epoch_label set reason for a plan that would make it a occurance across entire week(s)
    Example:
    Given: sue_personunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, every_xdays=5, days_duration=3
    Add a reason to mop_plan that indicates it's to be active between every 5 days for a length of 3 days
    """
    if days_lower_day and days_upper_day and every_xdays:
        time_rope = x_person.make_l1_rope("time")
        epoch_rope = x_person.make_rope(time_rope, epoch_label)
        days_rope = x_person.make_rope(epoch_rope, "days")
        epoch_plan = x_person.get_plan_obj(epoch_rope)
        days_plan = x_person.get_plan_obj(days_rope)

        case_args = {
            "plan_rope": plan_rope,
            "reason_context": days_rope,
            "reason_state": days_rope,
            "reason_lower": days_lower_day % every_xdays,
            "reason_upper": days_upper_day % every_xdays,
            "reason_divisor": every_xdays,
        }
        person_plan_reason_caseunit_set_obj(x_person, case_args)


def set_epoch_base_case_monthly(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    monthly_monthday_lower: int,
    monthly_duration_days: int,
):
    if monthly_monthday_lower and monthly_duration_days:
        year_rope = get_year_rope(x_person, epoch_label)
        year_plan = x_person.get_plan_obj(year_rope)
        for month_label, month_plan in year_plan.kids.items():
            month_rope = x_person.make_rope(year_rope, month_label)
            year_lower_min, year_upper_min = get_calc_year_lower_upper(
                month_plan,
                monthly_monthday_lower,
                monthly_duration_days,
                True,
                year_plan.denom,
            )
            if year_lower_min and year_upper_min:
                case_args = {
                    "plan_rope": plan_rope,
                    "reason_context": year_rope,
                    "reason_state": month_rope,
                    "reason_lower": year_lower_min,
                    "reason_upper": year_upper_min,
                }
                person_plan_reason_caseunit_set_obj(x_person, case_args)


def get_calc_year_lower_upper(
    month_plan: PlanUnit,
    year_monthday_lower: int,
    year_monthday_duration_days,
    range_must_be_within_month: bool,
    year_plan_denom: int,
):
    month_minutes = month_plan.stop_want - month_plan.gogo_want
    monthdayly_lower_minutes = year_monthday_lower * 1440
    if range_must_be_within_month and month_minutes < monthdayly_lower_minutes:
        return None, None
    year_lower_min = monthdayly_lower_minutes + month_plan.gogo_want
    length_minutes = year_monthday_duration_days * 1440
    year_upper_min = year_lower_min + length_minutes
    if range_must_be_within_month and year_upper_min > month_plan.stop_want:
        year_upper_min = month_plan.stop_want
    year_lower_min = year_lower_min % year_plan_denom
    year_upper_min = year_upper_min % year_plan_denom
    return year_lower_min, year_upper_min


def set_epoch_base_case_monthday(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    month_label: LabelTerm,
    year_monthday_lower: int,
    year_monthday_duration_days: int,
    range_must_be_within_month: bool = None,
):
    """Given an epoch_label set reason for a plan that would make it a occurance across entire week(s)
    Example:
    Given: sue_personunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, every_xdays=5, days_duration=3
    Add a reason to mop_plan that indicates it's to be active between every 5 days for a length of 3 days
    """
    if month_label and year_monthday_lower and year_monthday_duration_days:
        range_must_be_within_month = get_False_if_None(range_must_be_within_month)
        year_rope = get_year_rope(x_person, epoch_label)
        month_rope = x_person.make_rope(year_rope, month_label)
        month_plan = x_person.get_plan_obj(month_rope)
        year_plan = x_person.get_plan_obj(year_rope)
        year_lower_min, year_upper_min = get_calc_year_lower_upper(
            month_plan,
            year_monthday_lower,
            year_monthday_duration_days,
            range_must_be_within_month,
            year_plan.denom,
        )
        if year_lower_min is None:
            return

        case_args = {
            "plan_rope": plan_rope,
            "reason_context": month_rope,
            "reason_state": month_rope,
            "reason_lower": year_lower_min,
            "reason_upper": year_upper_min,
        }
        person_plan_reason_caseunit_set_obj(x_person, case_args)


def set_epoch_cases_for_dayly(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    dayly_lower_min: int,
    dayly_duration_min: int,
    days_lower_day: int,
    days_upper_day: int,
    every_xdays: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_dayly(
        x_person, plan_rope, epoch_label, dayly_lower_min, dayly_duration_min
    )
    set_epoch_base_case_xdays(
        x_person, plan_rope, epoch_label, days_lower_day, days_upper_day, every_xdays
    )
    set_epoch_base_case_range(
        x_person, plan_rope, epoch_label, range_lower_min, range_duration
    )


def set_epoch_cases_for_weekly(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    weekly_lower_min: int,
    weekly_duration_min: int,
    weeks_lower_week: int,
    weeks_upper_week: int,
    every_xweeks: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_weekly(
        x_person=x_person,
        plan_rope=plan_rope,
        epoch_label=epoch_label,
        weekly_lower_min=weekly_lower_min,
        weekly_duration_min=weekly_duration_min,
    )
    set_epoch_base_case_xweeks(
        x_person=x_person,
        plan_rope=plan_rope,
        epoch_label=epoch_label,
        weeks_lower_week=weeks_lower_week,
        weeks_upper_week=weeks_upper_week,
        every_xweeks=every_xweeks,
    )
    set_epoch_base_case_range(
        x_person, plan_rope, epoch_label, range_lower_min, range_duration
    )


def set_epoch_cases_for_yearly_monthday(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    dayly_lower_min: int,
    dayly_duration_min: int,
    month_label: LabelTerm,
    monthday: int,
    length_days: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_dayly(
        x_person, plan_rope, epoch_label, dayly_lower_min, dayly_duration_min
    )
    set_epoch_base_case_monthday(
        x_person, plan_rope, epoch_label, month_label, monthday, length_days
    )
    set_epoch_base_case_range(
        x_person, plan_rope, epoch_label, range_lower_min, range_duration
    )


def set_epoch_cases_for_monthly(
    x_person: PersonUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    dayly_lower_min: int,
    dayly_duration_min: int,
    monthday: int,
    length_days: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_monthly(x_person, plan_rope, epoch_label, monthday, length_days)
    set_epoch_base_case_dayly(
        x_person, plan_rope, epoch_label, dayly_lower_min, dayly_duration_min
    )
    set_epoch_base_case_range(
        x_person, plan_rope, epoch_label, range_lower_min, range_duration
    )


def set_epoch_cases_by_args_dict(
    x_person: PersonUnit,
    epoch_cases_args: dict[str],
):
    x_plan_rope = epoch_cases_args.get("plan_rope")
    x_epoch_label = epoch_cases_args.get("epoch_label")
    set_epoch_base_case_dayly(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        dayly_lower_min=epoch_cases_args.get("dayly_lower_min"),
        dayly_duration_min=epoch_cases_args.get("dayly_duration_min"),
    )
    set_epoch_base_case_xdays(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        days_lower_day=epoch_cases_args.get("days_lower_day"),
        days_upper_day=epoch_cases_args.get("days_upper_day"),
        every_xdays=epoch_cases_args.get("every_xdays"),
    )
    set_epoch_base_case_weekly(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        weekly_lower_min=epoch_cases_args.get("weekly_lower_min"),
        weekly_duration_min=epoch_cases_args.get("weekly_duration_min"),
    )
    set_epoch_base_case_xweeks(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        weeks_lower_week=epoch_cases_args.get("weeks_lower_week"),
        weeks_upper_week=epoch_cases_args.get("weeks_upper_week"),
        every_xweeks=epoch_cases_args.get("every_xweeks"),
    )
    set_epoch_base_case_monthday(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        month_label=epoch_cases_args.get("month_label"),
        year_monthday_lower=epoch_cases_args.get("year_monthday_lower"),
        year_monthday_duration_days=epoch_cases_args.get("year_monthday_duration_days"),
    )
    set_epoch_base_case_monthly(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        monthly_monthday_lower=epoch_cases_args.get("monthly_monthday_lower"),
        monthly_duration_days=epoch_cases_args.get("monthly_duration_days"),
    )
    set_epoch_base_case_range(
        x_person=x_person,
        plan_rope=x_plan_rope,
        epoch_label=x_epoch_label,
        range_lower_min=epoch_cases_args.get("range_lower_min"),
        range_duration_min=epoch_cases_args.get("range_duration"),
    )


def add_epoch_frame_to_personunit(
    x_person: PersonUnit, epoch_label: LabelTerm, epoch_frame_min: int
):
    root_plan_label = x_person.planroot.plan_label
    epoch_rope = get_epoch_rope(root_plan_label, epoch_label, x_person.knot)
    add_frame_to_personunit(x_person, epoch_frame_min, epoch_rope)


# TODO create tests for set_epoch_fact
def set_epoch_fact(
    person: PersonUnit, epoch_label: LabelTerm, timeline_lower: int, timeline_upper: int
):
    """assumes epoch_planunit exists"""
    time_rope = person.make_l1_rope("time")
    creg_rope = person.make_rope(time_rope, epoch_label)
    person.add_fact(creg_rope, creg_rope, timeline_lower, timeline_upper)
