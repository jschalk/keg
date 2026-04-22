from ch07_person_logic.person_main import personunit_shop
from ch13_time.epoch_main import (
    add_epoch_planunit,
    get_default_epoch_config_dict,
    get_epoch_min_from_dt,
    timeshoe_shop,
)
from ch13_time.epoch_reason import set_epoch_base_case_dayly
from ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from ch20_kpi.gcalendar import (
    DayEvent,
    gcal_readable_percent,
    get_dayevents,
    get_gcal_all_agenda_str,
)
from datetime import datetime
from ref.keywords import Ch20Keywords as kw


def test_DayEvents_Exists():
    # ESTABLISH / WHEN
    x_dayevent = DayEvent()
    # THEN
    assert not x_dayevent.plan
    assert not x_dayevent.item_rank
    assert not x_dayevent.day_min_lower
    assert not x_dayevent.day_min_upper
    assert not x_dayevent.clock_lower
    assert not x_dayevent.clock_upper
    assert set(x_dayevent.__dict__.keys()) == {
        kw.plan,
        "item_rank",
        "day_min_lower",
        "day_min_upper",
        f"{kw.clock}_lower",
        f"{kw.clock}_upper",
    }


def test_get_dayevents_ReturnsObj_Scenario0_EmptyList():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)
    epoch_config = get_default_epoch_config_dict()
    add_epoch_planunit(bob_person, epoch_config)
    epoch_label = epoch_config.get(kw.epoch_label)
    apr7 = datetime(2010, 5, 7)

    # WHEN
    bob_dayevents = get_dayevents(bob_person, epoch_label, apr7)

    # THEN
    assert bob_dayevents == []


def test_get_dayevents_ReturnsObj_Scenario1_OneElementList():
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
    bob_dayevents = get_dayevents(bob_person, default_epoch_label, apr7)

    # THEN
    assert bob_dayevents
    assert len(bob_dayevents) == 1
    mop_plan = bob_person.get_plan_obj(wx.mop_rope)
    mop_dayevent = bob_dayevents[0]
    assert mop_dayevent.plan == mop_plan
    assert mop_dayevent.item_rank == 1
    assert mop_dayevent.day_min_lower == 600
    assert mop_dayevent.day_min_upper == 690
    assert mop_dayevent.clock_lower == "10:00am"
    assert mop_dayevent.clock_upper == "11:30am"


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
    assert gcal_readable_percent(None) == "0% (None)"


def test_get_gcal_all_agenda_str_ReturnsObj_Scenario1_1AllDayPledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    default_epoch_config = get_default_epoch_config_dict()
    epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    bob_person.add_plan(wx.mop_rope, pledge=True, star=1)
    apr7_dt = datetime(2010, 5, 7, 9)
    print(f"{apr7_dt=}")

    # WHEN
    bob_agenda_str = get_gcal_all_agenda_str(bob_person, epoch_label, apr7_dt)

    # THEN
    expected_gcal_agenda_list_str = f"""All Agenda Items\n1. {wx.mop_str} (100%)"""
    assert bob_agenda_str == expected_gcal_agenda_list_str


def test_get_gcal_all_agenda_str_ReturnsObj_Scenario2_3AllDayPledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    default_epoch_config = get_default_epoch_config_dict()
    epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)
    bob_person.add_plan(wx.scrub_rope, pledge=True, star=1)
    apr7_dt = datetime(2010, 5, 7, 9)
    print(f"{apr7_dt=}")

    # WHEN
    bob_agenda_str = get_gcal_all_agenda_str(bob_person, epoch_label, apr7_dt)

    # THEN
    expected_gcal_agenda_list_str = f"""All Agenda Items\n1. {wx.mop_str} (50%)
2. {wx.scrub_str} (25%)
3. {wx.sweep_str} (25%)"""
    assert bob_agenda_str == expected_gcal_agenda_list_str


def test_get_gcal_all_agenda_str_ReturnsObj_Scenario3_OneEpoch_pledge():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_plan(wx.sweep_rope, pledge=True, star=1)

    # add mop task but only at a point during the day
    bob_person.add_plan(wx.mop_rope, pledge=True, star=2)
    default_epoch_config = get_default_epoch_config_dict()
    default_epoch_label = default_epoch_config.get(kw.epoch_label)
    add_epoch_planunit(bob_person, default_epoch_config)
    set_epoch_base_case_dayly(bob_person, wx.mop_rope, default_epoch_label, 600, 90)
    apr7_dt = datetime(2010, 5, 7)
    print(f"{apr7_dt=}")

    # WHEN
    bob_agenda_str = get_gcal_all_agenda_str(bob_person, default_epoch_label, apr7_dt)

    # THEN
    expected_gcal_agenda_list_str = f"""All Agenda Items\n1. {wx.mop_str} (66.67%) 10:00am-11:30am
2. {wx.sweep_str} (33.33%)"""
    print(f"{bob_agenda_str=}")
    assert bob_agenda_str == expected_gcal_agenda_list_str
