from csv import DictWriter as csv_DictWriter
from datetime import datetime, timedelta
from io import StringIO as io_StringIO
from src.ch04_rope.rope import is_sub_rope
from src.ch07_person_logic.person_main import PersonUnit, get_sorted_plan_list
from src.ch13_time.epoch_main import (
    get_day_rope,
    get_default_epoch_config_dict,
    get_epoch_min_from_dt,
    get_epoch_rope,
)
from src.ch13_time.epoch_reason import set_epoch_fact


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


def create_gcalendar_events_list(x_person: PersonUnit, day: datetime) -> list[dict]:
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get("epoch_label")
    epoch_min_lower = get_epoch_min_from_dt(x_person, default_epoch_label, day)
    next_day = day + timedelta(days=1)
    epoch_min_upper = get_epoch_min_from_dt(x_person, default_epoch_label, next_day)
    set_epoch_fact(x_person, default_epoch_label, epoch_min_lower, epoch_min_upper)
    epoch_rope = get_epoch_rope(
        x_person.planroot.get_plan_rope(), default_epoch_label, x_person.knot
    )

    agenda_plans_dict = x_person.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict, "fund_ratio")
    gcal_tobe_description = ""
    day_events = []
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
        gcal_tobe_description += f"{event_subject}\n"
    all_day_events = {
        "Subject": "Pledges",
        "Start Date": day.strftime("%m/%d/%Y"),
        "End Date": day.strftime("%m/%d/%Y"),
        "All Day Event": "True",
        "Description": gcal_tobe_description,
    }
    if gcal_tobe_description != "":
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
