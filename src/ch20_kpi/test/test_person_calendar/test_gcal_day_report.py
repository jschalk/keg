from datetime import datetime
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch20_kpi.gcalendar import (
    gcal_readable_percent,
    get_gcal_day_report_from_personunit,
)
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_get_gcal_day_report_from_personunit_ReturnsObj_Scenario0_EmptyPerson():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue, exx.a23)
    add_epoch_planunit(sue_person)
    apr7 = datetime(2010, 4, 7)
    sue_person.conpute()

    # WHEN
    sue_day_report_str = get_gcal_day_report_from_personunit(sue_person, apr7)

    # THEN
    assert sue_day_report_str
    assert f"Day Report for {exx.sue}" in sue_day_report_str
    assert "Schedule Priorities" in sue_day_report_str
    assert "All Agenda Items" in sue_day_report_str
    assert "Partners" in sue_day_report_str
    assert "Group" not in sue_day_report_str


def test_get_gcal_day_report_from_personunit_ReturnsObj_Scenario1_NonEmptyPerson():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue, exx.a23)
    add_epoch_planunit(sue_person)
    apr7 = datetime(2010, 4, 7)
    sue_person.add_partnerunit(exx.bob, 2)
    sue_person.add_partnerunit(exx.sue, 1)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sue_person.add_plan(clean_rope, 1, pledge=True)
    sue_person.get_partner(exx.sue).add_membership(exx.run)
    sue_person.conpute()

    # WHEN
    sue_day_report_str = get_gcal_day_report_from_personunit(
        sue_person, apr7, group_title=exx.run
    )

    # THEN
    assert sue_day_report_str
    assert f"Day Report for {exx.sue}" in sue_day_report_str
    assert "Schedule Priorities" in sue_day_report_str
    assert "All Agenda Items" in sue_day_report_str
    assert "Partners" in sue_day_report_str
    assert "Group" in sue_day_report_str
    assert exx.run in sue_day_report_str
