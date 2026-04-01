from copy import deepcopy as copy_deepcopy
from csv import DictWriter as csv_DictWriter
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import StringIO as io_StringIO
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import (
    create_path,
    get_dir_filenames,
    get_level1_dirs,
    open_file,
    save_file,
)
from src.ch02_contact.contact import ContactUnit
from src.ch04_rope.rope import create_rope, is_sub_rope
from src.ch05_reason.reason_main import ReasonHeir
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PersonUnit, get_sorted_plan_list
from src.ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch10_person_listen._ref.ch10_path import create_job_path
from src.ch10_person_listen.keep_tool import open_job_file
from src.ch13_time.epoch_main import (
    add_epoch_planunit,
    get_default_epoch_config_dict,
    get_epoch_min_from_dt,
    get_epoch_rope,
)
from src.ch13_time.epoch_reason import set_epoch_fact
from src.ch14_moment.moment_main import open_moment_file
from src.ch20_kpi._ref.ch20_path import (
    create_day_punch_txt_path,
    create_dst_person_punch_path,
)
from src.ch20_kpi._ref.ch20_semantic_types import (
    GroupTitle,
    KnotTerm,
    LabelTerm,
    MomentRope,
    PersonName,
    RopeTerm,
)


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


def planunit_is_scheduled_in_day(reasonheir: ReasonHeir, epoch_rope) -> bool:
    case = reasonheir.get_case(reasonheir.reason_context)
    divisor_remainder = case.reason_divisor % 1440
    return bool(
        is_sub_rope(reasonheir.reason_context, epoch_rope) and divisor_remainder == 0
    )


def set_day_epoch_fact(person: PersonUnit, epoch_label: LabelTerm, day: datetime):
    epoch_min_lower = get_epoch_min_from_dt(person, epoch_label, day)
    next_day = day + timedelta(days=1)
    epoch_min_upper = get_epoch_min_from_dt(person, epoch_label, next_day)
    set_epoch_fact(person, epoch_label, epoch_min_lower, epoch_min_upper)


def get_dayevents(
    person: PersonUnit, epoch_label: LabelTerm, day: datetime
) -> list[DayEvent]:
    set_day_epoch_fact(person, epoch_label, day)

    moment_rope = person.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(moment_rope, epoch_label, person.knot)
    agenda_plans_dict = person.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict, "fund_ratio")
    dayevents = []
    for item_rank, agenda_item in enumerate(agenda_list, start=1):
        for reason_context, reasonheir in agenda_item.reasonheirs.items():
            if planunit_is_scheduled_in_day(reasonheir, epoch_rope):
                if epoch_reasonheir := agenda_item.get_reasonheir(reason_context):
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


def get_inflection_points_dict(dayevents: list[DayEvent]) -> dict[int, DayEvent | None]:
    """
    Returns a dict[day_minute, DayEvent] representing inflection day_minutes where the
    "most important active event" changes.

    An inflection point occurs when:
    - A more important event starts while another is ongoing
    - The current top event ends and a different one takes over (or nothing)
    - A gap exists between events (represented as day_minute: None)
    """
    # Collect all relevant timestamps
    timestamps = sorted(
        {t for event in dayevents for t in (event.day_min_lower, event.day_min_upper)}
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
    minute %= 1440
    hours, mins = divmod(minute, 60)
    period = "AM" if hours < 12 else "PM"
    hours_12 = hours % 12 or 12  # convert 0 -> 12
    return f"{hours_12}:{mins:02d} {period}"


def get_gcal_priorities_schedule_str(dayevents: list[DayEvent]) -> str:
    inflections_dict = get_inflection_points_dict(dayevents)
    x_str = "Schedule Priorities"
    for inflection_minute in sorted(list(inflections_dict.keys())):
        dayevent = inflections_dict.get(inflection_minute)
        clock_time = minute_to_clock_time(inflection_minute)
        if dayevent:
            precent_str = gcal_readable_percent(dayevent.plan.fund_ratio)
            x_str += f"\n{clock_time} {dayevent.item_rank}. {dayevent.plan.plan_label} {precent_str}"
        else:
            x_str += f"\n{clock_time} Nothing scheduled."
    return x_str


def get_gcal_all_agenda_str(
    x_person: PersonUnit, epoch_label: LabelTerm, day: datetime
) -> str:
    set_day_epoch_fact(x_person, epoch_label, day)

    agenda_plans_dict = x_person.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict, "fund_ratio")
    moment_rope = x_person.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(moment_rope, epoch_label, x_person.knot)
    gcal_agenda_list_str = "All Agenda Items"
    for item_rank, agenda_item in enumerate(agenda_list, start=1):
        item_fund_ratio_str = gcal_readable_percent(agenda_item.fund_ratio)
        event_subject = f"{item_rank}. {agenda_item.plan_label} ({item_fund_ratio_str})"

        for reason_context, reasonheir in agenda_item.reasonheirs.items():
            if planunit_is_scheduled_in_day(reasonheir, epoch_rope):
                epoch_reasonheir = agenda_item.get_reasonheir(reason_context)
                epoch_case = epoch_reasonheir.get_case(reason_context)
                day_reason_lower = epoch_case.reason_lower % 1440
                day_reason_upper = epoch_case.reason_upper % 1440
                clock_lower = minute_to_clock_time(day_reason_lower)
                clock_upper = minute_to_clock_time(day_reason_upper)
                clock_range = f" {clock_lower}-{clock_upper}"
                event_subject += clock_range
        gcal_agenda_list_str += f"\n{event_subject}"
    return gcal_agenda_list_str


def get_gcal_contacts_str(x_person: PersonUnit) -> str:
    x_str = "Person Contacts"
    contacts_list = list(x_person.contacts.values())
    return create_contacts_only_list_str(contacts_list, x_str)


def create_contacts_only_list_str(contacts_list: list[ContactUnit], x_str: str) -> str:
    contacts_list.sort(
        key=lambda pu: (
            -pu.fund_agenda_ratio_give - pu.fund_agenda_ratio_take,
            pu.contact_name,
        )
    )

    for contact in contacts_list:
        give_left = contact.fund_agenda_ratio_give - contact.fund_agenda_ratio_take
        agenda_relative_give = gcal_readable_percent(give_left)
        x_str += f"\n{agenda_relative_give} {contact.contact_name}"
    return x_str


def get_gcal_memberships_str(x_person: PersonUnit, group_title: GroupTitle) -> str:
    x_str = f"{group_title} Group"
    groupunit = x_person.get_groupunit(group_title)
    group_contact_names = []
    if not groupunit or len(groupunit.memberships) == 0:
        x_str += "\nNo memberships"
    else:
        group_contact_names.extend(iter(groupunit.memberships.keys()))
    contacts_list = []
    contacts_list.extend(
        x_person.get_contact(group_contact_name)
        for group_contact_name in group_contact_names
    )
    return create_contacts_only_list_str(contacts_list, x_str)


def get_gcal_day_punch_from_personunit(
    x_person: PersonUnit,
    day: datetime,
    epoch_label: LabelTerm = None,
    group_title: GroupTitle = None,
) -> str:
    """parameter x_person is assumed to have already conputed."""
    moment_rope = x_person.planroot.get_plan_rope()
    x_str = f"Day Report for {x_person.person_name} in the {moment_rope} Moment\n"
    if not epoch_label:
        epoch_label = get_default_epoch_config_dict().get("epoch_label")
    x_dayevents = get_dayevents(x_person, epoch_label, day)
    x_str += f"\n{get_gcal_priorities_schedule_str(x_dayevents)}"
    x_str += f"\n{get_gcal_all_agenda_str(x_person, epoch_label, day)}"
    x_str += f"\n{get_gcal_contacts_str(x_person)}"
    if group_title:
        x_str += f"\n{get_gcal_memberships_str(x_person, group_title)}"
    return x_str


def create_gcalendar_events_list(x_person: PersonUnit, day: datetime) -> list[dict]:
    x_person = copy_deepcopy(x_person)
    default_epoch_config = get_default_epoch_config_dict()
    epoch_label = default_epoch_config.get("epoch_label")

    gcal_agenda_list_str = ""
    day_events = []
    dayevent_objs = get_dayevents(x_person, epoch_label, day)
    for dayevent_obj in dayevent_objs:
        item_fund_ratio_str = gcal_readable_percent(dayevent_obj.plan.fund_ratio)
        event_subject = f"{dayevent_obj.item_rank}. {dayevent_obj.plan.plan_label} ({item_fund_ratio_str})"
        start_date = day + timedelta(minutes=dayevent_obj.day_min_lower)
        end_date = day + timedelta(minutes=dayevent_obj.day_min_upper)
        event_dict = {
            "Subject": event_subject,
            "Start Date": start_date.strftime("%m/%d/%Y"),
            "Start Time": start_date.strftime("%I:%M %p"),
            "End Date": end_date.strftime("%m/%d/%Y"),
            "End Time": end_date.strftime("%I:%M %p"),
            "All Day Event": "False",
            "Description": dayevent_obj.plan.get_plan_rope(),
        }
        day_events.append(event_dict)
    gcal_agenda_list_str = get_gcal_all_agenda_str(x_person, epoch_label, day)
    all_day_events = {
        "Subject": "Pledges",
        "Start Date": day.strftime("%m/%d/%Y"),
        "End Date": day.strftime("%m/%d/%Y"),
        "All Day Event": "True",
        "Description": gcal_agenda_list_str,
    }
    if x_person.get_agenda_dict() != {}:
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


def get_gcal_day_punch_from_job_file(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    day: datetime,
    focus_group_title: GroupTitle = None,
) -> str:
    momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
    epoch_label = momentunit.epoch.epoch_label
    job = open_job_file(moment_mstr_dir, moment_lasso, person_name)
    epoch_rope = get_epoch_rope(momentunit.moment_rope, epoch_label, momentunit.knot)
    if not job.plan_exists(epoch_rope):
        add_epoch_planunit(job, momentunit.get_epoch_config())
    return get_gcal_day_punch_from_personunit(job, day, epoch_label, focus_group_title)


def add_gcal_day_punch_to_dict(
    day_punchs: dict,
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    day: datetime,
    focus_group_title: GroupTitle,
):
    mmt_job_path = create_job_path(moment_mstr_dir, moment_lasso, person_name)
    if os_path_exists(mmt_job_path):
        day_punch_str = get_gcal_day_punch_from_job_file(
            moment_mstr_dir, moment_lasso, person_name, day, focus_group_title
        )
        report_path = create_day_punch_txt_path(
            moment_mstr_dir, moment_lasso, person_name
        )
        day_punchs[moment_lasso.moment_rope] = {
            "day_punch": day_punch_str,
            "file_path": report_path,
        }


def get_person_gcal_day_punchs(
    moment_mstr_dir: str,
    person_name: PersonName,
    day: datetime,
    focus_group_title: GroupTitle = None,
) -> dict[PersonName, dict[str, str]]:
    day_punchs = {}
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        moment_path = create_path(moments_dir, moment_lasso.make_path())
        persons_path = create_path(moment_path, "persons")
        for dir_person in get_level1_dirs(persons_path):
            if dir_person == person_name:
                add_gcal_day_punch_to_dict(
                    day_punchs,
                    moment_mstr_dir,
                    moment_lasso,
                    person_name,
                    day,
                    focus_group_title,
                )
    return day_punchs


def save_person_gcal_day_punchs(
    moment_mstr_dir: str,
    person_name: PersonName,
    day: datetime,
    focus_group_title: GroupTitle = None,
):
    day_punchs = get_person_gcal_day_punchs(
        moment_mstr_dir, person_name, day, focus_group_title
    )
    for person_name, report_dict in day_punchs.items():
        file_path = report_dict.get("file_path")
        day_punch = report_dict.get("day_punch")
        save_file(file_path, None, day_punch)


def copy_person_day_punches_to_dst_dir(
    moment_mstr_dir: str, dst_dir: str, person_name: PersonName
):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        moment_path = create_path(moments_dir, moment_lasso.make_path())
        day_punchs_path = create_path(moment_path, "day_punchs")

        for sub_dir, person_filename in get_dir_filenames(day_punchs_path):
            if person_filename == f"{person_name}.txt":
                dst_person_punch_path = create_dst_person_punch_path(
                    dst_dir, moment_lasso, person_name
                )
                day_punch_file_path = create_path(day_punchs_path, person_filename)
                save_file(dst_person_punch_path, None, open_file(day_punch_file_path))
