from csv import DictReader as csv_DictReader
from datetime import datetime, timedelta
from io import StringIO as io_StringIO
from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.epoch_main import (
    add_epoch_planunit,
    get_default_epoch_config_dict,
    get_epoch_rope,
)
from src.ch13_time.epoch_reason import (
    set_epoch_base_case_dayly,
    set_epoch_base_case_weekly,
)
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch20_kpi.gcalendar import (
    create_gcalendar_csv_from_list,
    create_gcalendar_csv_from_person,
    create_gcalendar_events_list,
)
from src.ref.keywords import Ch20Keywords as kw


def test_create_gcalendar_events_list_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    default_epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(bob_person, default_epoch_config)
    apr7 = datetime(2010, 5, 7, 9)
    moment_rope = bob_person.planroot.get_plan_rope()
    epoch_label = default_epoch_config.get(kw.epoch_label)
    epoch_rope = get_epoch_rope(moment_rope, epoch_label, bob_person.knot)

    assert not bob_person.get_fact(epoch_rope)
    print(f"{apr7=}")

    # WHEN
    bob_gcal_events = create_gcalendar_events_list(bob_person, apr7)

    # THEN
    assert bob_gcal_events == []
    assert not bob_person.get_fact(epoch_rope)


def test_create_gcalendar_events_list_ReturnsObj_Scenario1_1AllDayPledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    default_epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(bob_person, default_epoch_config)
    bob_person.add_plan(wx.mop_rope, pledge=True, star=1)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    bob_gcal_events = create_gcalendar_events_list(bob_person, day=apr7)

    # THEN
    gcal_agenda_list_str = f"""All Agenda Items\n1. {wx.mop_str} (100%)"""
    description_str = "Description"
    expected_apr7str = "05/07/2010"
    expected_event_dict = {
        "Subject": "Pledges",
        "Start Date": expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_agenda_list_str,
    }
    init_gcal_event = bob_gcal_events[0]
    assert len(bob_gcal_events) == 1
    assert init_gcal_event.keys() == expected_event_dict.keys()
    assert init_gcal_event.get(description_str) == gcal_agenda_list_str
    assert bob_gcal_events == [expected_event_dict]


def test_create_gcalendar_events_list_ReturnsObj_Scenario2_3AllDayPledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    default_epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(bob_person, default_epoch_config)
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)
    bob_person.add_plan(wx.scrub_rope, pledge=True, star=1)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    bob_gcal_events = create_gcalendar_events_list(bob_person, day=apr7)

    # THEN
    assert len(bob_gcal_events) == 1
    gcal_agenda_list_str = f"""All Agenda Items\n1. {wx.mop_str} (50%)
2. {wx.scrub_str} (25%)
3. {wx.sweep_str} (25%)"""
    description_str = "Description"
    start_date_str = "Start Date"
    expected_apr7str = "05/07/2010"
    expected_event_dict = {
        "Subject": "Pledges",
        start_date_str: expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_agenda_list_str,
    }
    init_gcal_event = bob_gcal_events[0]
    assert init_gcal_event.keys() == expected_event_dict.keys()
    assert init_gcal_event.get(description_str) == gcal_agenda_list_str
    assert init_gcal_event.get(start_date_str) == expected_apr7str
    print(bob_gcal_events)
    print([expected_event_dict])
    assert bob_gcal_events == [expected_event_dict]


def test_create_gcalendar_events_list_ReturnsObj_Scenario3_OneEpoch_pledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    set_epoch_base_case_dayly(bob_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)
    print(f"{apr7=}")

    # WHEN
    bob_gcal_events = create_gcalendar_events_list(bob_person, apr7)

    # THEN
    gcal_agenda_list_str = f"""All Agenda Items\n1. {wx.mop_str} (66.67%) 10:00 AM-11:30 AM
2. {wx.sweep_str} (33.33%)"""
    description_str = "Description"
    start_date_str = "Start Date"
    expected_apr7str = "05/07/2010"
    expected_all_day_event_dict = {
        "Subject": "Pledges",
        start_date_str: expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_agenda_list_str,
    }
    init_gcal_event = bob_gcal_events[1]
    assert len(bob_gcal_events) == 2
    assert init_gcal_event.get(description_str) == gcal_agenda_list_str
    assert init_gcal_event.get(start_date_str) == expected_apr7str
    assert init_gcal_event == expected_all_day_event_dict
    print(bob_gcal_events[0])
    expected_mop_event = {
        "Subject": f"1. {wx.mop_str} (66.67%)",
        start_date_str: expected_apr7str,
        "Start Time": "10:00 AM",
        "End Date": expected_apr7str,
        "End Time": "11:30 AM",
        "All Day Event": "False",
        description_str: wx.mop_rope,
    }
    assert bob_gcal_events == [expected_mop_event, expected_all_day_event_dict]


def test_create_gcalendar_csv_from_list_ReturnsObj():
    # ESTABLISH
    events = [
        {
            "Subject": "Team Meeting",
            "Start Date": "10/08/2025",
            "Start Time": "09:00:00",
            "End Date": "10/08/2025",
            "End Time": "10:00:00",
            "All Day Event": "False",
            "Description": "Quarterly planning session",
        },
        {
            "Subject": "All Hands Day",
            "Start Date": "10/10/2025",
            "End Date": "10/10/2025",
            "All Day Event": "True",
            "Description": "Company-wide offsite",
        },
    ]

    # WHEN
    csv_str = create_gcalendar_csv_from_list(events)

    # THEN
    # Assert CSV contains expected headers and data
    assert isinstance(csv_str, str)
    header_str = (
        "Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description"
    )
    assert header_str in csv_str
    assert "Team Meeting" in csv_str
    assert "All Hands Day" in csv_str
    assert "Company-wide offsite" in csv_str

    # Parse it back to verify structure
    reader = list(csv_DictReader(io_StringIO(csv_str)))
    assert reader[0]["All Day Event"] == "False"
    assert reader[1]["All Day Event"] == "True"
    assert reader[1]["Start Time"] == ""  # blank for all-day event
    print(csv_str)


def test_create_gcalendar_csv_from_person_ReturnsObj_Scenario0_OneEpoch_pledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    set_epoch_base_case_dayly(bob_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)

    # WHEN
    bob_gcal_csv = create_gcalendar_csv_from_person(bob_person, apr7)

    # THEN
    print(bob_gcal_csv)
    expected_csv_line1 = (
        "Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description"
    )
    expected_csv_line2 = (
        "1. mop (66.67%),05/07/2010,10:00 AM,05/07/2010,11:30 AM,False,;YY;mop;"
    )
    expected_csv_line3 = """Pledges,05/07/2010,,05/07/2010,,True,"All Agenda Items\n1. mop (66.67%) 10:00 AM-11:30 AM\n2. sweep (33.33%)"""
    assert expected_csv_line1 in bob_gcal_csv
    assert expected_csv_line2 in bob_gcal_csv
    assert expected_csv_line3 in bob_gcal_csv


def test_create_gcalendar_csv_from_person_ReturnsObj_Scenario1_Non_all_day_EventExists():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    set_epoch_base_case_dayly(bob_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)
    print(f"{apr7=}")

    # WHEN
    bob_gcal_csv = create_gcalendar_csv_from_person(bob_person, apr7)

    # THEN
    reader = csv_DictReader(io_StringIO(bob_gcal_csv))
    rows = list(reader)

    chore_row = next((r for r in rows if r["Subject"].startswith("1. mop")), None)
    assert chore_row is not None, "Expected a chore row starting with '1. mop'"
    assert chore_row["Start Date"] == "05/07/2010"
    assert chore_row["Start Time"] == "10:00 AM"
    assert chore_row["End Date"] == "05/07/2010"
    assert chore_row["End Time"] == "11:30 AM"
    assert chore_row["All Day Event"] == "False"
    assert ";YY;mop;" in chore_row["Description"]
    assert "66.67%" in chore_row["Subject"]

    pledges_row = next((r for r in rows if r["Subject"] == "Pledges"), None)
    assert pledges_row is not None, "Expected a Pledges row"
    assert pledges_row["Start Date"] == "05/07/2010"
    assert pledges_row["All Day Event"] == "True"
    assert "1. mop (66.67%)" in pledges_row["Description"]
    assert "2. sweep (33.33%)" in pledges_row["Description"]


def test_create_gcalendar_csv_from_person_ReturnsObj_Scenario2_DiferentEvents():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    set_epoch_base_case_dayly(bob_person, wx.mop_rope, default_epoch_label, 600, 90)

    # WHEN
    bob_gcal_csv = create_gcalendar_csv_from_person(bob_person)

    # THEN
    now_date_str = datetime.now().date().strftime("%m/%d/%Y")

    reader = csv_DictReader(io_StringIO(bob_gcal_csv))
    rows = list(reader)

    chore_row = next((r for r in rows if r["Subject"].startswith("1. mop")), None)
    assert chore_row is not None, "Expected a chore row starting with '1. mop'"
    assert chore_row["Start Date"] == now_date_str
    assert chore_row["Start Time"] == "10:00 AM"
    assert chore_row["End Date"] == now_date_str
    assert chore_row["End Time"] == "11:30 AM"
    assert chore_row["All Day Event"] == "False"
    assert ";YY;mop;" in chore_row["Description"]
    assert "66.67%" in chore_row["Subject"]

    pledges_row = next((r for r in rows if r["Subject"] == "Pledges"), None)
    assert pledges_row is not None, "Expected a Pledges row"
    assert pledges_row["Start Date"] == now_date_str
    assert pledges_row["All Day Event"] == "True"
    assert "1. mop (66.67%)" in pledges_row["Description"]
    assert "2. sweep (33.33%)" in pledges_row["Description"]


def test_create_gcalendar_csv_from_person_ReturnsObj_Scenario3_WeeklyEventDisplayed():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    set_epoch_base_case_weekly(bob_person, wx.mop_rope, default_epoch_label, 3700, 90)
    apr7 = datetime(2010, 5, 7)
    print(f"{apr7=}")

    # WHEN
    bob_gcal_csv = create_gcalendar_csv_from_person(bob_person, apr7)

    # THEN
    reader = csv_DictReader(io_StringIO(bob_gcal_csv))
    rows = list(reader)

    chore_row = next((r for r in rows if r["Subject"].startswith("1. mop")), None)
    assert chore_row is not None, "Expected a chore row starting with '1. mop'"
    assert chore_row["Start Date"] == "05/07/2010"
    assert chore_row["Start Time"] == "01:40 PM"
    assert chore_row["End Date"] == "05/07/2010"
    assert chore_row["End Time"] == "03:10 PM"

    pledges_row = next((r for r in rows if r["Subject"] == "Pledges"), None)
    assert pledges_row is not None, "Expected a Pledges row"
    assert pledges_row["Start Date"] == "05/07/2010"
    assert pledges_row["All Day Event"] == "True"
    assert "1. mop (66.67%)" in pledges_row["Description"]
    assert "2. sweep (33.33%)" in pledges_row["Description"]
