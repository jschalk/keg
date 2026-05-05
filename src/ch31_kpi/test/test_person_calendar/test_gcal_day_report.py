from ch00_py.file_toolbox import create_path, open_file, save_file
from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.lasso import lassounit_shop
from ch10_person_listen.keep_tool import save_job_file
from ch13_time.epoch_main import (
    add_epoch_planunit,
    get_default_epoch_config_dict,
    get_epoch_min_from_dt,
    timeshoe_shop,
)
from ch14_moment.moment_main import momentunit_shop, save_moment_file
from ch18_etl_config._ref.ch18_path import create_moment_mstr_path, create_world_db_path
from ch27_mind.mind_core import CREATE_MOMENT_TRANBOOK_NETS_SQLSTR
from ch31_kpi._ref.ch31_path import (
    create_day_punch_txt_path as day_punch_path,
    create_dst_person_punch_path as dst_punch_path,
)
from ch31_kpi.gcalendar import (
    copy_person_day_punches_to_dst_dir,
    get_gcal_day_punch_from_job_file,
    get_gcal_day_punch_from_personunit,
    get_person_gcal_day_punchs,
    mind_to_person_gcal_day_punchs,
    persontranbookmetric_shop,
)
from ch31_kpi.test._util.ch31_examples import (
    get_a23_sue_clean_example,
    get_ep8_sue_clean_example,
    get_ep8_yao_clean_example,
)
from datetime import datetime
from os.path import exists as os_path_exists
from ref.keywords import Ch31Keywords as kw, ExampleStrs as exx
from sqlite3 import Cursor, connect as sqlite3_connect


def test_get_gcal_day_punch_from_personunit_ReturnsObj_Scenario0_EmptyPerson():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue, exx.a23)
    add_epoch_planunit(sue_person)
    apr7 = datetime(2010, 4, 7)
    sue_person.thinkout()

    # WHEN
    sue_day_punch_str = get_gcal_day_punch_from_personunit(sue_person, apr7)

    # THEN
    assert sue_day_punch_str
    ap7_epoch_min = get_epoch_min_from_dt(sue_person, kw.creg, apr7)
    ap7_timeshoe = timeshoe_shop(sue_person, kw.creg, ap7_epoch_min)
    expected_str = f"{ap7_timeshoe.get_long_date_blurb()} Agenda for {exx.sue}"
    assert expected_str in sue_day_punch_str
    assert "Schedule Priorities" in sue_day_punch_str
    assert "All Agenda Items" in sue_day_punch_str
    assert "Contacts" in sue_day_punch_str
    assert "Group" not in sue_day_punch_str


def test_get_gcal_day_punch_from_personunit_ReturnsObj_Scenario1_NonEmptyPerson():
    # ESTABLISH
    sue_person = get_a23_sue_clean_example()
    apr7 = datetime(2010, 4, 7)

    # WHEN
    sue_day_punch_str = get_gcal_day_punch_from_personunit(
        sue_person, apr7, group_title=exx.run
    )

    # THEN
    assert sue_day_punch_str
    assert f"Agenda for {exx.sue}" in sue_day_punch_str
    assert "Schedule Priorities" in sue_day_punch_str
    assert "All Agenda Items" in sue_day_punch_str
    assert "Contacts" in sue_day_punch_str
    assert "Group" in sue_day_punch_str
    assert exx.run in sue_day_punch_str


def test_get_gcal_day_punch_from_personunit_ReturnsObj_Scenario2_PersonTranBookMetric_Passed():
    # ESTABLISH
    sue_person = get_a23_sue_clean_example()
    apr7 = datetime(2010, 4, 7)
    sue_net = 70
    a23_circulation_total = 5000
    sue_tranmetric = persontranbookmetric_shop(
        exx.a23, exx.sue, net=sue_net, circulation_total=a23_circulation_total
    )

    # WHEN
    sue_day_punch_str = get_gcal_day_punch_from_personunit(
        sue_person, apr7, group_title=exx.run, persontranbookmetric=sue_tranmetric
    )

    # THEN
    print(sue_day_punch_str)
    assert sue_day_punch_str
    assert str(sue_net) in sue_day_punch_str
    assert str(a23_circulation_total) in sue_day_punch_str


def test_get_gcal_day_punch_from_job_file_ReturnsObj_Scenario1_NonEmptyPerson(temp3_fs):
    # ESTABLISH
    sue_person = get_a23_sue_clean_example()
    epoch_config = get_default_epoch_config_dict()
    x_epoch_label = epoch_config.get("epoch_label")
    add_epoch_planunit(sue_person, epoch_config)
    sue_person.thinkout()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    world_dir = str(temp3_fs)
    mmt_mstr_dir = create_moment_mstr_path(world_dir)

    a23_moment = momentunit_shop(exx.a23, mmt_mstr_dir)
    a23_lasso = lassounit_shop(a23_moment.moment_rope, a23_moment.knot)
    assert a23_moment.epoch.epoch_label == x_epoch_label
    save_moment_file(a23_moment, a23_lasso)
    # save personunit json as job file
    save_job_file(mmt_mstr_dir, sue_person)

    # WHEN
    sue_day_punch_str = get_gcal_day_punch_from_job_file(
        moment_mstr_dir=mmt_mstr_dir,
        moment_lasso=a23_lasso,
        person_name=sue_person.person_name,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_punch_str
    assert "Schedule Priorities" in sue_day_punch_str


def test_get_person_gcal_day_punchs_ReturnsObj_Scenario0_NoData(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    apr7 = datetime(2010, 4, 7)

    # WHEN
    sue_day_punchs = get_person_gcal_day_punchs(
        world_dir=world_dir,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_punchs == {}


def test_get_person_gcal_day_punchs_ReturnsObj_Scenario1_Two_day_punchs(
    temp3_fs,
):
    # ESTABLISH
    sue_a23_person = get_a23_sue_clean_example()
    sue_ep8_person = get_ep8_sue_clean_example()
    epoch_config = get_default_epoch_config_dict()
    x_epoch_label = epoch_config.get("epoch_label")
    add_epoch_planunit(sue_a23_person, epoch_config)
    add_epoch_planunit(sue_ep8_person, epoch_config)
    sue_a23_person.thinkout()
    sue_ep8_person.thinkout()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    world_dir = str(temp3_fs)
    mmt_mstr_dir = create_moment_mstr_path(world_dir)
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
    sue_day_punchs = get_person_gcal_day_punchs(
        world_dir=world_dir,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_punchs
    assert set(sue_day_punchs.keys()) == {exx.a23, exx.ep8}
    sue_a23_dict = sue_day_punchs.get(exx.a23)
    assert "Schedule Priorities" in sue_a23_dict.get("day_punch")


def test_get_person_gcal_day_punchs_ReturnsObj_Scenario2_OnlySueReports(
    temp3_fs,
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
    sue_a23_person.thinkout()
    sue_ep8_person.thinkout()
    yao_ep8_person.thinkout()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    world_dir = str(temp3_fs)
    mmt_mstr_dir = create_moment_mstr_path(world_dir)
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
    sue_day_punchs = get_person_gcal_day_punchs(
        world_dir=world_dir,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert sue_day_punchs
    assert set(sue_day_punchs.keys()) == {exx.a23, exx.ep8}
    sue_a23_dict = sue_day_punchs.get(exx.a23)
    sue_ep8_dict = sue_day_punchs.get(exx.ep8)
    assert "Schedule Priorities" in sue_a23_dict.get("day_punch")
    assert "Schedule Priorities" in sue_ep8_dict.get("day_punch")
    assert f"Agenda for {exx.sue}" in sue_a23_dict.get("day_punch")
    assert f"Agenda for {exx.sue}" in sue_ep8_dict.get("day_punch")
    sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
    sue_ep8_day_punch_path = day_punch_path(mmt_mstr_dir, ep8_lasso, exx.sue)
    assert sue_a23_day_punch_path == sue_a23_dict.get("file_path")
    assert sue_ep8_day_punch_path == sue_ep8_dict.get("file_path")


def test_mind_to_person_gcal_day_punchs_SavesFiles_Scenario0_TwoSueReports(
    temp3_fs,
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
    sue_a23_person.thinkout()
    sue_ep8_person.thinkout()
    yao_ep8_person.thinkout()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    world_dir = str(temp3_fs)
    mmt_mstr_dir = create_moment_mstr_path(world_dir)

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
    sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
    sue_ep8_day_punch_path = day_punch_path(mmt_mstr_dir, ep8_lasso, exx.sue)
    assert not os_path_exists(sue_a23_day_punch_path)
    assert not os_path_exists(sue_ep8_day_punch_path)

    # WHEN
    mind_to_person_gcal_day_punchs(
        world_dir=world_dir,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert os_path_exists(sue_a23_day_punch_path)
    assert os_path_exists(sue_ep8_day_punch_path)
    sue_a23_day_punch_str = open_file(sue_a23_day_punch_path)
    sue_ep8_day_punch_str = open_file(sue_ep8_day_punch_path)
    assert "Schedule Priorities" in sue_ep8_day_punch_str
    assert f"Agenda for {exx.sue}" in sue_a23_day_punch_str
    assert f"Agenda for {exx.sue}" in sue_ep8_day_punch_str


def test_mind_to_person_gcal_day_punchs_SavesFiles_Scenario1_IncludesTranBook(temp3_fs):
    # ESTABLISH
    sue_a23_person = get_a23_sue_clean_example()
    epoch_config = get_default_epoch_config_dict()
    x_epoch_label = epoch_config.get("epoch_label")
    add_epoch_planunit(sue_a23_person, epoch_config)
    sue_a23_person.thinkout()
    apr7 = datetime(2010, 4, 7)
    # save momentunit json
    world_dir = str(temp3_fs)
    mmt_mstr_dir = create_moment_mstr_path(world_dir)

    a23_moment = momentunit_shop(exx.a23, mmt_mstr_dir)
    a23_lasso = lassounit_shop(a23_moment.moment_rope, a23_moment.knot)
    assert a23_moment.epoch.epoch_label == x_epoch_label
    save_moment_file(a23_moment, a23_lasso)
    # save personunit json as job file
    save_job_file(mmt_mstr_dir, sue_a23_person)
    sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
    world_db_path = create_world_db_path(str(temp3_fs))
    with sqlite3_connect(world_db_path) as conn:
        conn.execute(CREATE_MOMENT_TRANBOOK_NETS_SQLSTR)
        sue_funds = 55
        insert_sqlstr = f"""
INSERT INTO {kw.moment_tranbook_nets} ({kw.moment_rope}, {kw.person_name}, {kw.person_net_amount}) 
VALUES 
  ('{exx.a23}', '{exx.sue}', {sue_funds})
, ('{exx.a23}', '{exx.yao}', {3000 - sue_funds})
;
"""
        conn.execute(insert_sqlstr)
    assert not os_path_exists(sue_a23_day_punch_path)

    # WHEN
    mind_to_person_gcal_day_punchs(
        world_dir=world_dir,
        person_name=exx.sue,
        day=apr7,
        focus_group_title=exx.run,
    )

    # THEN
    assert os_path_exists(sue_a23_day_punch_path)
    sue_a23_day_punch_str = open_file(sue_a23_day_punch_path)
    print(sue_a23_day_punch_str)
    assert "funds" in sue_a23_day_punch_str
    assert str(sue_funds) in sue_a23_day_punch_str
    assert str(3000) in sue_a23_day_punch_str


def test_copy_person_day_punches_to_dst_dir_SavesFiles_Scenario0_TwoSueReports(
    temp3_fs,
):
    # ESTABLISH
    # save momentunit json
    world_dir = str(temp3_fs)
    mmt_mstr_dir = create_moment_mstr_path(world_dir)

    a23_moment = momentunit_shop(exx.a23, mmt_mstr_dir)
    ep8_moment = momentunit_shop(exx.ep8, mmt_mstr_dir)
    a23_lasso = lassounit_shop(a23_moment.moment_rope, a23_moment.knot)
    ep8_lasso = lassounit_shop(ep8_moment.moment_rope, ep8_moment.knot)
    save_moment_file(a23_moment, a23_lasso)
    save_moment_file(ep8_moment, ep8_lasso)
    sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
    sue_ep8_day_punch_path = day_punch_path(mmt_mstr_dir, ep8_lasso, exx.sue)
    save_file(sue_a23_day_punch_path, None, "example sue_a23")
    save_file(sue_ep8_day_punch_path, None, "example sue_ep8")
    dst_dir = create_path(mmt_mstr_dir, "dst")
    sue_a23_dst_punch_path = dst_punch_path(dst_dir, a23_lasso, exx.sue)
    sue_ep8_dst_punch_path = dst_punch_path(dst_dir, ep8_lasso, exx.sue)
    assert not os_path_exists(sue_a23_dst_punch_path)
    assert not os_path_exists(sue_ep8_dst_punch_path)

    # WHEN
    dst_person_punch_paths = copy_person_day_punches_to_dst_dir(
        moment_mstr_dir=mmt_mstr_dir,
        dst_dir=dst_dir,
        person_name=exx.sue,
    )

    # THEN
    assert os_path_exists(sue_a23_dst_punch_path)
    assert os_path_exists(sue_ep8_dst_punch_path)
    for dst_person_punch_path in dst_person_punch_paths:
        print(f"{dst_person_punch_path=}")
    print(f"{sue_a23_dst_punch_path=}")
    print(f"{sue_ep8_dst_punch_path=}")
    assert dst_person_punch_paths == {
        exx.a23: {sue_a23_dst_punch_path},
        exx.ep8: {sue_ep8_dst_punch_path},
    }
