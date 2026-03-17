from copy import deepcopy as copy_deepcopy
from csv import DictWriter as csv_DictWriter
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import StringIO as io_StringIO
from src.ch04_rope.rope import is_sub_rope
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PersonUnit, get_sorted_plan_list
from src.ch13_time.epoch_main import (
    get_default_epoch_config_dict,
    get_epoch_min_from_dt,
    get_epoch_rope,
)
from src.ch13_time.epoch_reason import set_epoch_fact
from src.ch19_world_kpi._ref.ch19_semantic_types import LabelTerm, RopeTerm


def gcal_readable_percent(value: float, precision=2):
    """
    Convert a float into a readable percentage string.
    Handles very small and large values gracefully.
    """
    if value is None:
        return "0%"

    percent = value * 100

    if 0 < abs(percent) < 0.01:
        return f"{percent:.2e}%"

    formatted = f"{percent:.{precision}f}".rstrip("0").rstrip(".")
    return f"{formatted}%"


@dataclass
class DayEvent:
    plan: PlanUnit = None
    item_rank: int = None
    day_min_lower: int = None
    day_min_upper: int = None


def get_dayevents(
    person: PersonUnit, epoch_label: LabelTerm, day: datetime
) -> list[DayEvent]:
    epoch_min_lower = get_epoch_min_from_dt(person, epoch_label, day)
    next_day = day + timedelta(days=1)
    epoch_min_upper = get_epoch_min_from_dt(person, epoch_label, next_day)
    set_epoch_fact(person, epoch_label, epoch_min_lower, epoch_min_upper)

    moment_rope = person.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(moment_rope, epoch_label, person.knot)
    agenda_plans_dict = person.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict, "fund_ratio")
    dayevents = []
    for item_rank, agenda_item in enumerate(agenda_list, start=1):
        for reason_context, reasonheir in agenda_item.reasonheirs.items():
            epoch_case = reasonheir.get_case(reason_context)
            divisor_remainder = epoch_case.reason_divisor % 1440
            if is_sub_rope(reason_context, epoch_rope) and divisor_remainder == 0:
                epoch_reasonheir = agenda_item.get_reasonheir(reason_context)
                if epoch_reasonheir:
                    epoch_case = epoch_reasonheir.get_case(reason_context)
                    day_reason_lower = epoch_case.reason_lower % 1440
                    day_reason_upper = epoch_case.reason_upper % 1440
                    x_dayevent = DayEvent(
                        agenda_item,
                        item_rank,
                        day_min_lower=day_reason_lower,
                        day_min_upper=day_reason_upper,
                    )
                    dayevents.append(x_dayevent)
    return dayevents


def get_inflection_points_dict(dayevents: list[DayEvent]) -> dict[int, PlanUnit]:
    """
    Returns a list of (time, event) tuples representing inflection points �
    moments where the "most important active event" changes.

    An inflection point occurs when:
    - A more important event starts while another is ongoing
    - The current top event ends and a different one takes over (or nothing)
    - A gap exists between events (represented as (time, None))
    """
    # Collect all relevant timestamps
    timestamps = sorted(
        set(
            t for event in dayevents for t in (event.day_min_lower, event.day_min_upper)
        )
    )

    inflection_points = {}
    last_top_dayevent = None

    for t in timestamps:
        active = [e for e in dayevents if e.day_min_lower <= t < e.day_min_upper]
        top_dayevent = max(active, key=lambda e: e.plan.fund_ratio) if active else None

        if top_dayevent != last_top_dayevent:
            inflection_points[t] = top_dayevent
            last_top_dayevent = top_dayevent

    return inflection_points


def minute_to_clock_time(minute: int) -> str:
    """
    Converts a minute of the day (0-1439) to a clock time string.
    e.g. 0 -> "12:00 AM", 120 -> "2:00 AM", 780 -> "1:00 PM"
    """
    minute = minute % 1440  # wrap around if > 1 day
    hours, mins = divmod(minute, 60)
    period = "AM" if hours < 12 else "PM"
    hours_12 = hours % 12 or 12  # convert 0 -> 12
    return f"{hours_12}:{mins:02d} {period}"


def get_inflection_points_str(dayevents: list[DayEvent]) -> str:
    inflections_dict = get_inflection_points_dict(dayevents)
    x_str = "Schedule Inflections"
    for inflection_minute in sorted(list(inflections_dict.keys())):
        dayevent = inflections_dict.get(inflection_minute)
        clock_time = minute_to_clock_time(inflection_minute)
        if dayevent:
            precent_str = gcal_readable_percent(dayevent.plan.fund_ratio)
            x_str += f"\n{clock_time} {dayevent.item_rank}. {dayevent.plan.plan_label} {precent_str}"
        else:
            x_str += f"\n{clock_time} Nothing scheduled."
    return x_str


# TODO create test for this
# TODO create test get_gcal_agenda_list_by_time_str
# TODO create test get_gcal_inflection_point_str
def get_gcal_agenda_list_str(
    x_person: PersonUnit, epoch_label: LabelTerm, day: datetime
) -> str:
    epoch_min_lower = get_epoch_min_from_dt(x_person, epoch_label, day)
    next_day = day + timedelta(days=1)
    epoch_min_upper = get_epoch_min_from_dt(x_person, epoch_label, next_day)
    set_epoch_fact(x_person, epoch_label, epoch_min_lower, epoch_min_upper)

    moment_rope = x_person.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(moment_rope, epoch_label, x_person.knot)
    agenda_plans_dict = x_person.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict, "fund_ratio")
    gcal_agenda_list_str = ""
    # TODO replace for loop with iteration through get_dayevents list
    for item_rank, agenda_item in enumerate(agenda_list, start=1):
        item_fund_ratio_str = gcal_readable_percent(agenda_item.fund_ratio)
        event_subject = f"{item_rank}. {agenda_item.plan_label} ({item_fund_ratio_str})"
        for reason_context, reasonheir in agenda_item.reasonheirs.items():
            epoch_case = reasonheir.get_case(reason_context)
            divisor_remainder = epoch_case.reason_divisor % 1440
            if is_sub_rope(reason_context, epoch_rope) and divisor_remainder == 0:
                epoch_reasonheir = agenda_item.get_reasonheir(reason_context)
                if epoch_reasonheir:
                    epoch_case = epoch_reasonheir.get_case(reason_context)
                    day_reason_lower = epoch_case.reason_lower % 1440
                    day_reason_upper = epoch_case.reason_upper % 1440
                    start_date = day + timedelta(minutes=day_reason_lower)
                    end_date = day + timedelta(minutes=day_reason_upper)
        gcal_agenda_list_str += f"{event_subject}\n"
    return gcal_agenda_list_str


def create_gcalendar_events_list(x_person: PersonUnit, day: datetime) -> list[dict]:
    x_person = copy_deepcopy(x_person)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get("epoch_label")
    epoch_min_lower = get_epoch_min_from_dt(x_person, default_epoch_label, day)
    next_day = day + timedelta(days=1)
    epoch_min_upper = get_epoch_min_from_dt(x_person, default_epoch_label, next_day)
    set_epoch_fact(x_person, default_epoch_label, epoch_min_lower, epoch_min_upper)
    moment_rope = x_person.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(moment_rope, default_epoch_label, x_person.knot)

    agenda_plans_dict = x_person.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict, "fund_ratio")
    gcal_agenda_list_str = ""
    day_events = []
    # TODO replace for loop with iteration through get_dayevents list
    for item_rank, agenda_item in enumerate(agenda_list, start=1):
        item_fund_ratio_str = gcal_readable_percent(agenda_item.fund_ratio)
        event_subject = f"{item_rank}. {agenda_item.plan_label} ({item_fund_ratio_str})"
        for reason_context, reasonheir in agenda_item.reasonheirs.items():
            if (
                is_sub_rope(reason_context, epoch_rope)
                and (reasonheir.get_case(reason_context).reason_divisor % 1440) == 0
            ):
                epoch_reasonheir = agenda_item.get_reasonheir(reason_context)
                if epoch_reasonheir:
                    epoch_case = epoch_reasonheir.get_case(reason_context)
                    day_reason_lower = epoch_case.reason_lower % 1440
                    day_reason_upper = epoch_case.reason_upper % 1440
                    start_date = day + timedelta(minutes=day_reason_lower)
                    end_date = day + timedelta(minutes=day_reason_upper)
                    event_dict = {
                        "Subject": event_subject,
                        "Start Date": start_date.strftime("%m/%d/%Y"),
                        "Start Time": start_date.strftime("%I:%M %p"),
                        "End Date": end_date.strftime("%m/%d/%Y"),
                        "End Time": end_date.strftime("%I:%M %p"),
                        "All Day Event": "False",
                        "Description": agenda_item.get_plan_rope(),
                    }
                    day_events.append(event_dict)
    gcal_agenda_list_str = get_gcal_agenda_list_str(x_person, default_epoch_label, day)
    all_day_events = {
        "Subject": "Pledges",
        "Start Date": day.strftime("%m/%d/%Y"),
        "End Date": day.strftime("%m/%d/%Y"),
        "All Day Event": "True",
        "Description": gcal_agenda_list_str,
    }
    if gcal_agenda_list_str != "":
        day_events.append(all_day_events)
    return day_events


def create_gcalendar_csv_from_list(events: list[dict]) -> str:
    """Create a Google Calendar-compatible CSV file."""
    fieldnames = [
        "Subject",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "All Day Event",
        "Description",
    ]

    # Use StringIO to build in memory
    output = io_StringIO()
    writer = csv_DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(events)

    return output.getvalue()


def create_gcalendar_csv_from_person(x_person: PersonUnit, day: datetime = None) -> str:
    if day is None:
        day = datetime.combine(datetime.now().date(), datetime.min.time())
    events_list = create_gcalendar_events_list(x_person, day)
    return create_gcalendar_csv_from_list(events_list)
