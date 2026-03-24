from datetime import datetime
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch10_person_listen.keep_tool import save_job_file
from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch14_moment.moment_main import momentunit_shop, save_moment_file
from src.ch20_kpi.gcalendar import (
    gcal_readable_percent,
    get_gcal_day_report_from_job_file,
    get_gcal_day_report_from_personunit,
    get_person_gcal_day_reports,
)
from src.ch20_kpi.test._util.ch20_env import get_temp_dir, temp_dir_setup
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


def get_a23_sue_clean_example() -> PersonUnit:
    sue_person = personunit_shop(exx.sue, exx.a23)
    add_epoch_planunit(sue_person)
    sue_person.add_partnerunit(exx.bob, 2)
    sue_person.add_partnerunit(exx.sue, 1)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sue_person.add_plan(clean_rope, 1, pledge=True)
    sue_person.get_partner(exx.sue).add_membership(exx.run)
    sue_person.conpute()
    return sue_person


def get_ep8_sue_clean_example() -> PersonUnit:
    sue_person = personunit_shop(exx.sue, exx.ep8)
    add_epoch_planunit(sue_person)
    sue_person.add_partnerunit(exx.zia, 2)
    sue_person.add_partnerunit(exx.yao, 1)
    sue_person.add_partnerunit(exx.sue, 1)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    mop_rope = sue_person.make_rope(casa_rope, exx.mop)
    sue_person.add_plan(mop_rope, 1, pledge=True)
    sue_person.get_partner(exx.sue).add_membership(exx.run)
    sue_person.conpute()
    return sue_person


def get_ep8_yao_clean_example() -> PersonUnit:
    yao_person = personunit_shop(exx.yao, exx.ep8)
    add_epoch_planunit(yao_person)
    yao_person.add_partnerunit(exx.zia, 2)
    yao_person.add_partnerunit(exx.yao, 1)
    yao_person.add_partnerunit(exx.sue, 1)
    casa_rope = yao_person.make_l1_rope(exx.casa)
    swim_rope = yao_person.make_rope(casa_rope, exx.swim)
    yao_person.add_plan(swim_rope, 1, pledge=True)
    yao_person.get_partner(exx.yao).add_membership(exx.run)
    yao_person.conpute()
    return yao_person


def test_get_gcal_day_report_from_personunit_ReturnsObj_Scenario1_NonEmptyPerson():
    # ESTABLISH
    sue_person = get_a23_sue_clean_example()
    apr7 = datetime(2010, 4, 7)

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


def test_get_gcal_day_report_from_job_file_ReturnsObj_Scenario1_NonEmptyPerson():
    # ESTABLISH
    sue_person = get_a23_sue_clean_example()
    epoch_config = get_default_epoch_config_dict()
    x_epoch_label = epoch_config.get("epoch_label")
    add_epoch_planunit(sue_person, epoch_config)
    sue_person.conpute()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    mmt_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, mmt_mstr_dir)
    a23_lasso = lassounit_shop(a23_moment.moment_rope, a23_moment.knot)
    assert a23_moment.epoch.epoch_label == x_epoch_label
    save_moment_file(a23_moment, a23_lasso)
    # save personunit json as job file
    save_job_file(mmt_mstr_dir, sue_person)

    # WHEN
    sue_day_report_str = get_gcal_day_report_from_job_file(
        moment_mstr_dir=mmt_mstr_dir,
        moment_lasso=a23_lasso,
        person_name=sue_person.person_name,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_report_str
    assert "Schedule Priorities" in sue_day_report_str


def test_get_person_gcal_day_reports_ReturnsObj_Scenario1_Two_day_reports(
    temp_dir_setup,
):
    # ESTABLISH
    sue_a23_person = get_a23_sue_clean_example()
    sue_ep8_person = get_ep8_sue_clean_example()
    epoch_config = get_default_epoch_config_dict()
    x_epoch_label = epoch_config.get("epoch_label")
    add_epoch_planunit(sue_a23_person, epoch_config)
    add_epoch_planunit(sue_ep8_person, epoch_config)
    sue_a23_person.conpute()
    sue_ep8_person.conpute()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    mmt_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, mmt_mstr_dir)
    ep8_moment = momentunit_shop(exx.ep8, mmt_mstr_dir)
    a23_lasso = lassounit_shop(a23_moment.moment_rope, a23_moment.knot)
    ep8_lasso = lassounit_shop(ep8_moment.moment_rope, ep8_moment.knot)
    assert a23_moment.epoch.epoch_label == x_epoch_label
    assert ep8_moment.epoch.epoch_label == x_epoch_label
    save_moment_file(a23_moment, a23_lasso)
    save_moment_file(ep8_moment, ep8_lasso)
    # save personunit json as job file
    save_job_file(mmt_mstr_dir, sue_a23_person)
    save_job_file(mmt_mstr_dir, sue_ep8_person)

    # WHEN
    sue_day_reports = get_person_gcal_day_reports(
        moment_mstr_dir=mmt_mstr_dir,
        moment_lasso=a23_lasso,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_reports
    assert set(sue_day_reports.keys()) == {exx.a23, exx.ep8}
    assert "Schedule Priorities" in sue_day_reports.get(exx.a23)


def test_get_person_gcal_day_reports_ReturnsObj_Scenario2_OnlySueReports(
    temp_dir_setup,
):
    # ESTABLISH
    sue_a23_person = get_a23_sue_clean_example()
    sue_ep8_person = get_ep8_sue_clean_example()
    yao_ep8_person = get_ep8_yao_clean_example()
    epoch_config = get_default_epoch_config_dict()
    x_epoch_label = epoch_config.get("epoch_label")
    add_epoch_planunit(sue_a23_person, epoch_config)
    add_epoch_planunit(sue_ep8_person, epoch_config)
    add_epoch_planunit(yao_ep8_person, epoch_config)
    sue_a23_person.conpute()
    sue_ep8_person.conpute()
    yao_ep8_person.conpute()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    mmt_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, mmt_mstr_dir)
    ep8_moment = momentunit_shop(exx.ep8, mmt_mstr_dir)
    a23_lasso = lassounit_shop(a23_moment.moment_rope, a23_moment.knot)
    ep8_lasso = lassounit_shop(ep8_moment.moment_rope, ep8_moment.knot)
    assert a23_moment.epoch.epoch_label == x_epoch_label
    assert ep8_moment.epoch.epoch_label == x_epoch_label
    save_moment_file(a23_moment, a23_lasso)
    save_moment_file(ep8_moment, ep8_lasso)
    # save personunit json as job file
    save_job_file(mmt_mstr_dir, sue_a23_person)
    save_job_file(mmt_mstr_dir, sue_ep8_person)
    save_job_file(mmt_mstr_dir, yao_ep8_person)

    # WHEN
    sue_day_reports = get_person_gcal_day_reports(
        moment_mstr_dir=mmt_mstr_dir,
        moment_lasso=a23_lasso,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_reports
    assert set(sue_day_reports.keys()) == {exx.a23, exx.ep8}
    assert "Schedule Priorities" in sue_day_reports.get(exx.a23)
    assert f"Day Report for {exx.sue}" in sue_day_reports.get(exx.a23)
    assert f"Day Report for {exx.sue}" in sue_day_reports.get(exx.ep8)
