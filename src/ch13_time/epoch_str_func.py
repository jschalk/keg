from ch04_rope.rope import (
    LabelTerm,
    RopeTerm,
    create_rope,
    get_first_label_from_rope,
    get_tail_label,
)
from ch05_reason.reason_main import CaseUnit, FactUnit
from ch07_person_logic.person_main import PersonUnit
from ch13_time.epoch_main import timeshoe_shop


def get_reason_case_readable_str(
    reason_context: RopeTerm,
    caseunit: CaseUnit,
    epoch_label: LabelTerm = None,
    personunit: PersonUnit = None,
) -> str:
    """Returns a string describing reason case in readable language. Will have special cases for time."""

    moment_rope = get_first_label_from_rope(reason_context)
    time_rope = create_rope(moment_rope, "time")
    epoch_rope = create_rope(time_rope, epoch_label)
    week_rope = create_rope(epoch_rope, "week")
    if reason_context == week_rope:
        week_plan = personunit.get_plan_obj(week_rope)
        for weekday_plan in week_plan.kids.values():
            week_lower_bool = caseunit.reason_lower == weekday_plan.gogo_want
            week_upper_bool = caseunit.reason_upper == weekday_plan.stop_want
            if week_lower_bool and week_upper_bool:
                return f"case: every {weekday_plan.plan_label}"

    x_str = f"case: {caseunit.reason_state.replace(reason_context, "", 1)}"
    if caseunit.reason_divisor:
        x_str += f" divided by {caseunit.reason_divisor} then"
    if caseunit.reason_lower is not None and caseunit.reason_upper is not None:
        x_str += f" from {caseunit.reason_lower} to {caseunit.reason_upper}"

    return x_str


def get_fact_state_readable_str(
    factunit: FactUnit,
    epoch_label: LabelTerm = None,
    personunit: PersonUnit = None,
) -> str:
    """Returns a string describing fact in readable language. Will have special cases for time."""

    context_rope = factunit.fact_context
    state_rope = factunit.fact_state
    lower_float = factunit.fact_lower
    upper_float = factunit.fact_upper
    context_tail = get_tail_label(context_rope)
    state_trailing = state_rope.replace(context_rope, "", 1)
    x_str = f"({context_tail}) fact: {state_trailing}"
    moment_rope = get_first_label_from_rope(context_rope)
    time_rope = create_rope(moment_rope, "time")
    if factunit.fact_context == create_rope(time_rope, epoch_label):
        lower_blurb = get_timenum_blurb(personunit, epoch_label, lower_float)
        upper_blurb = get_timenum_blurb(personunit, epoch_label, upper_float)
        return f"from {lower_blurb} to {upper_blurb}"

    if lower_float is not None and upper_float is not None:
        x_str += f" from {lower_float} to {upper_float}"

    return x_str


def get_timenum_blurb(personunit: PersonUnit, epoch_rope: RopeTerm, x_min: int) -> str:
    lower_btlp = timeshoe_shop(personunit, epoch_rope, x_min)
    lower_btlp.calc_epoch()
    return lower_btlp.get_blurb()
