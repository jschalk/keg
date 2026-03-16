from csv import DictReader as csv_DictReader
from datetime import datetime, timedelta
from io import StringIO as io_StringIO
from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch13_time.epoch_reason import set_epoch_base_case_dayly
from src.ch24_person_viewer.test._util.ch24_examples import ExampleValuesRef as wx
from src.ch25_google_calendar.gcalendar import (
    create_gcalendar_csv_from_list,
    create_gcalendar_csv_from_person,
    create_gcalendar_events_list,
    gcal_readable_percent,
)
from src.ref.keywords import Ch25Keywords as kw


def test_gcal_readable_percent_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gcal_readable_percent(1.0) == "100%"
    """Ensure trailing zeros and decimal points are removed properly."""
    assert gcal_readable_percent(0.5) == "50%"
    assert gcal_readable_percent(0.505) == "50.5%"
    assert gcal_readable_percent(0.5001) == "50.01%"
    """Ensure extremely small numbers use scientific notation."""
    result = gcal_readable_percent(1e-10)
    assert "e" in result
    assert result.endswith("%")
    """Ensure custom precision works correctly."""
    assert gcal_readable_percent(0.123456, precision=1) == "12.3%"
    assert gcal_readable_percent(0.123456, precision=4) == "12.3456%"
    assert gcal_readable_percent(0.00123456, precision=4) == "0.1235%"
    assert gcal_readable_percent(0.0000123456, precision=4) == "1.23e-03%"
    assert gcal_readable_percent(0.000123456) == "0.01%"


def test_create_gcalendar_events_list_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    default_epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(sue_person, default_epoch_config)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_person, apr7)

    # THEN
    assert sue_gcal_events == []


def test_PersonUnit_conpute_SetsAttr_ScenarioX_SingleBranch_fund_ratio():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    sue_person.add_plan(wx.mop_rope, pledge=True, star=1)
    mop_plan = sue_person.get_plan_obj(wx.mop_rope)
    assert not sue_person.planroot.fund_onset
    assert not sue_person.planroot.fund_cease
    assert not sue_person.planroot.fund_ratio
    assert not mop_plan.fund_onset
    assert not mop_plan.fund_cease
    assert not mop_plan.fund_ratio

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.planroot.fund_onset == 0
    assert sue_person.planroot.fund_cease == 1000000000.0
    assert sue_person.planroot.fund_ratio == 1.0
    assert mop_plan.fund_onset == 0
    assert mop_plan.fund_cease == sue_person.fund_pool
    assert mop_plan.fund_ratio
    assert mop_plan.fund_ratio == 1.0


def test_create_gcalendar_events_list_ReturnsObj_Scenario1_1AllDayPledge():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    default_epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(sue_person, default_epoch_config)
    sue_person.add_plan(wx.mop_rope, pledge=True, star=1)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_person, day=apr7)

    # THEN
    gcal_tobe_description = f"""1. {wx.mop_str} (100%)
"""
    description_str = "Description"
    expected_apr7str = "05/07/2010"
    expected_event_dict = {
        "Subject": "Pledges",
        "Start Date": expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_tobe_description,
    }
    init_gcal_event = sue_gcal_events[0]
    assert len(sue_gcal_events) == 1
    assert init_gcal_event.keys() == expected_event_dict.keys()
    assert init_gcal_event.get(description_str) == gcal_tobe_description
    assert sue_gcal_events == [expected_event_dict]


def test_create_gcalendar_events_list_ReturnsObj_Scenario2_3AllDayPledge():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    default_epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(sue_person, default_epoch_config)
    sue_person.add_plan(wx.mop_rope, pledge=True, star=2)
    sue_person.add_plan(wx.sweep_rope, pledge=True, star=1)
    sue_person.add_plan(wx.scrub_rope, pledge=True, star=1)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_person, day=apr7)

    # THEN
    assert len(sue_gcal_events) == 1
    gcal_tobe_description = f"""1. {wx.mop_str} (50%)
2. {wx.scrub_str} (25%)
3. {wx.sweep_str} (25%)
"""
    description_str = "Description"
    start_date_str = "Start Date"
    expected_apr7str = "05/07/2010"
    expected_event_dict = {
        "Subject": "Pledges",
        start_date_str: expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_tobe_description,
    }
    init_gcal_event = sue_gcal_events[0]
    assert init_gcal_event.keys() == expected_event_dict.keys()
    assert init_gcal_event.get(description_str) == gcal_tobe_description
    assert init_gcal_event.get(start_date_str) == expected_apr7str
    print(sue_gcal_events)
    print([expected_event_dict])
    assert sue_gcal_events == [expected_event_dict]


def test_create_gcalendar_events_list_ReturnsObj_Scenario3_OneEpoch_pledge():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    sue_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    sue_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(sue_person, default_epoch_config)
    set_epoch_base_case_dayly(sue_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_person, apr7)

    # THEN
    gcal_tobe_description = f"""1. {wx.mop_str} (66.67%)
2. {wx.sweep_str} (33.33%)
"""
    description_str = "Description"
    start_date_str = "Start Date"
    expected_apr7str = "05/07/2010"
    expected_all_day_event_dict = {
        "Subject": "Pledges",
        start_date_str: expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_tobe_description,
    }
    init_gcal_event = sue_gcal_events[1]
    assert len(sue_gcal_events) == 2
    assert init_gcal_event.get(description_str) == gcal_tobe_description
    assert init_gcal_event.get(start_date_str) == expected_apr7str
    assert init_gcal_event == expected_all_day_event_dict
    print(sue_gcal_events[0])
    expected_mop_event = {
        "Subject": f"1. {wx.mop_str} (66.67%)",
        start_date_str: expected_apr7str,
        "Start Time": "10:00 AM",
        "End Date": expected_apr7str,
        "End Time": "11:30 AM",
        "All Day Event": "False",
        description_str: wx.mop_rope,
    }
    assert sue_gcal_events == [expected_mop_event, expected_all_day_event_dict]


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
    sue_person = personunit_shop(wx.sue, wx.a23)
    sue_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    sue_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(sue_person, default_epoch_config)
    set_epoch_base_case_dayly(sue_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)

    # WHEN
    sue_gcal_csv = create_gcalendar_csv_from_person(sue_person, apr7)

    # THEN
    print(sue_gcal_csv)
    expected_csv_line1 = (
        "Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description"
    )
    expected_csv_line2 = "1. mop (66.67%),05/07/2010,10:00 AM,05/07/2010,11:30 AM,False,;Amy23;casa;clean;mop;"
    expected_csv_line3 = (
        """Pledges,05/07/2010,,05/07/2010,,True,"1. mop (66.67%)\n2. sweep (33.33%)\n"""
    )
    assert expected_csv_line1 in sue_gcal_csv
    assert expected_csv_line2 in sue_gcal_csv
    assert expected_csv_line3 in sue_gcal_csv


def test_create_gcalendar_csv_from_person_ReturnsObj_Scenario1_Non_all_day_EventExists():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    sue_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    sue_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(sue_person, default_epoch_config)
    set_epoch_base_case_dayly(sue_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_csv = create_gcalendar_csv_from_person(sue_person, apr7)

    # THEN
    print(sue_gcal_csv)
    expected_csv_line1 = (
        "Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description"
    )
    expected_csv_line2 = "1. mop (66.67%),05/07/2010,10:00 AM,05/07/2010,11:30 AM,False,;Amy23;casa;clean;mop;"
    expected_csv_line3 = (
        """Pledges,05/07/2010,,05/07/2010,,True,"1. mop (66.67%)\n2. sweep (33.33%)\n"""
    )
    assert expected_csv_line1 in sue_gcal_csv
    assert expected_csv_line2 in sue_gcal_csv
    assert expected_csv_line3 in sue_gcal_csv


def test_create_gcalendar_csv_from_person_ReturnsObj_Scenario2_TodayEvents():
    # ESTABLISH
    sue_person = personunit_shop(wx.sue, wx.a23)
    sue_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    sue_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(sue_person, default_epoch_config)
    set_epoch_base_case_dayly(sue_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7 = datetime(2010, 5, 7)

    # WHEN
    sue_gcal_csv = create_gcalendar_csv_from_person(sue_person)

    # THEN
    expected_start_date = datetime.now().date()
    expected_start_date_str = expected_start_date.strftime("%m/%d/%Y")
    expected_end_date = expected_start_date + timedelta(days=1)
    expected_end_date_str = expected_end_date.strftime("%m/%d/%Y")
    print(sue_gcal_csv)
    expected_csv_line1 = (
        "Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description"
    )
    expected_csv_lv2 = f"1. mop (66.67%),03/15/2026,10:00 AM,03/15/2026,11:30 AM,False,;Amy23;casa;clean;mop;"
    expected_csv_line2 = f"1. mop (66.67%),{expected_start_date_str},10:00 AM,{expected_start_date_str},11:30 AM,False,;Amy23;casa;clean;mop;"
    expected_csv_line3 = f"""Pledges,{expected_start_date_str},,{expected_start_date_str},,True,"1. mop (66.67%)\n2. sweep (33.33%)\n"""
    assert expected_csv_line1 in sue_gcal_csv
    assert expected_csv_lv2 in sue_gcal_csv
    assert expected_csv_lv2 == expected_csv_line2
    assert expected_csv_line2 in sue_gcal_csv
    assert expected_csv_line3 in sue_gcal_csv
