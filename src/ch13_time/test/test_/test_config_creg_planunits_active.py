from ch06_plan.plan import planunit_shop
from ch07_person_logic.person_main import PersonUnit, personunit_shop
from ch13_time.epoch_main import get_year_rope
from ch13_time.test._util.ch13_examples import (
    add_time_creg_planunit,
    creg_weekday_planunits,
    get_creg_min_from_dt,
    get_thu,
    get_wed,
)
from datetime import datetime
from ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_day_plan_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    day_rope = sue_personunit.make_rope(creg_rope, kw.day)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # day_plan = sue_personunit.get_plan_obj(day_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_day_plan_Scenario1():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    day_rope = sue_personunit.make_rope(creg_rope, kw.day)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # day_plan = sue_personunit.get_plan_obj(day_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=day_rope,
        reason_case=day_rope,
        reason_lower=0,
        reason_upper=1,
        reason_divisor=1,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_day_plan_Scenario2():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    day_rope = sue_personunit.make_rope(creg_rope, kw.day)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # day_plan = sue_personunit.get_plan_obj(day_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=day_rope,
        reason_case=day_rope,
        reason_lower=360,
        reason_upper=420,
        reason_divisor=1440,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 14400300, 14400480)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope) != None


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_days_plan_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    days_rope = sue_personunit.make_rope(creg_rope, kw.days)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # days_plan = sue_personunit.get_plan_obj(days_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=days_rope,
        reason_case=days_rope,
        reason_lower=4,
        reason_upper=5,
        reason_divisor=7,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 11 * 1400, 12 * 1400)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()

    # THEN
    clean_plan = sue_personunit.get_plan_obj(clean_rope)
    print(f"{clean_plan.factheirs.keys()=}")
    print(f"{clean_plan.factheirs.get(days_rope)=}")
    assert sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_week_plan_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    week_rope = sue_personunit.make_rope(creg_rope, kw.week)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # week_plan = sue_personunit.get_plan_obj(week_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=week_rope,
        reason_case=week_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=10080,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_week_plan_Scenario1():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    week_rope = sue_personunit.make_rope(creg_rope, kw.week)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # week_plan = sue_personunit.get_plan_obj(week_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=week_rope,
        reason_case=week_rope,
        reason_lower=2880,
        reason_upper=4220,
        reason_divisor=10080,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 100802880, 100804220)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope) != None


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_weeks_plan_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    weeks_rope = sue_personunit.make_rope(creg_rope, kw.weeks)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    creg_plan = sue_personunit.get_plan_obj(creg_rope)
    print(f"{creg_plan.begin=} {creg_plan.close=}")
    # weeks_plan = sue_personunit.get_plan_obj(weeks_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=weeks_rope,
        reason_case=weeks_rope,
        reason_lower=4,
        reason_upper=5,
        reason_divisor=7,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 11 * 10080, 12 * 10080)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_year_plan_Scenario0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(sue_personunit, kw.creg)
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # year_plan = sue_personunit.get_plan_obj(year_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=525600,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 0, 1440)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)

    # WHEN
    sue_personunit.add_fact(creg_rope, creg_rope, 1444, 2880)
    sue_agenda = sue_personunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert not sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_year_plan_Scenario1():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(sue_personunit, kw.creg)

    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # year_plan = sue_personunit.get_plan_obj(year_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=525600,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)


def test_PersonUnit_get_agenda_dict_ReturnsDictWith_year_plan_Scenario2():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(sue_personunit, kw.creg)

    sue_personunit = add_time_creg_planunit(sue_personunit)
    creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # year_plan = sue_personunit.get_plan_obj(year_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1440,
        reason_divisor=525600,
    )
    sue_personunit.add_fact(creg_rope, creg_rope, 525600, 525600 + 1440)

    # WHEN
    sue_agenda = sue_personunit.get_agenda_dict()
    print(f"{sue_agenda=}")

    # THEN
    assert sue_agenda.get(clean_rope)

    # WHEN / THEN
    yr2000mar1 = get_creg_min_from_dt(dt=datetime(2000, 3, 1, 0, 0))
    yr2000mar2 = get_creg_min_from_dt(dt=datetime(2000, 3, 2, 0, 0))
    yr2000dec1 = get_creg_min_from_dt(dt=datetime(2000, 12, 1, 0, 0))
    yr2000dec2 = get_creg_min_from_dt(dt=datetime(2000, 12, 2, 0, 0))
    yr2004mar1 = get_creg_min_from_dt(dt=datetime(2004, 3, 1, 0, 0))
    yr2004mar2 = get_creg_min_from_dt(dt=datetime(2004, 3, 2, 0, 0))

    sue_personunit.add_fact(creg_rope, creg_rope, yr2000mar1, yr2000mar1 + 1440)
    assert len(sue_personunit.get_agenda_dict()) == 1
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000mar2, yr2000mar2 + 1440)
    assert len(sue_personunit.get_agenda_dict()) == 0
    sue_personunit.add_fact(creg_rope, creg_rope, yr2004mar1, yr2004mar1 + 1440)
    assert len(sue_personunit.get_agenda_dict()) == 1
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000mar2, yr2004mar2 + 1440)
    assert len(sue_personunit.get_agenda_dict()) == 1


def wed_gogo_want():
    return creg_weekday_planunits().get(get_wed()).gogo_want


def thu_gogo_want():
    return creg_weekday_planunits().get(get_thu()).gogo_want


def test_PersonUnit_add_time_creg_planunit_SyncsWeekDayAndYear_Wednesday_March1_2000():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(sue_personunit, kw.creg)
    week_rope = sue_personunit.make_rope(creg_rope, kw.week)
    # sun_rope = sue_personunit.make_rope(week_rope, get_sun())
    # mon_rope = sue_personunit.make_rope(week_rope, get_mon())
    # tue_rope = sue_personunit.make_rope(week_rope, get_tue())
    wed_rope = sue_personunit.make_rope(week_rope, get_wed())
    # thu_rope = sue_personunit.make_rope(week_rope, get_thu())
    # fri_rope = sue_personunit.make_rope(week_rope, get_fri())
    # sat_rope = sue_personunit.make_rope(week_rope, get_sat())
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # week_plan = sue_personunit.get_plan_obj(week_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=wed_rope,
        reason_case=wed_rope,
        reason_lower=wed_gogo_want(),
        reason_upper=wed_gogo_want() + 1440,
    )
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=0,
        reason_upper=1400,
    )

    yr2000_mar1day = get_creg_min_from_dt(datetime(2000, 3, 1, 0, 0))
    yr2000_mar2day = get_creg_min_from_dt(datetime(2000, 3, 2, 0, 0))
    yr2000_mar3day = get_creg_min_from_dt(datetime(2000, 3, 3, 0, 0))
    yr2000_mar4day = get_creg_min_from_dt(datetime(2000, 3, 4, 0, 0))
    yr2000_mar5day = get_creg_min_from_dt(datetime(2000, 3, 5, 0, 0))
    yr2000_mar6day = get_creg_min_from_dt(datetime(2000, 3, 6, 0, 0))
    yr2000_mar7day = get_creg_min_from_dt(datetime(2000, 3, 7, 0, 0))
    yr2000_mar8day = get_creg_min_from_dt(datetime(2000, 3, 8, 0, 0))
    print(f"{wed_gogo_want()=}")
    print(f"{wed_gogo_want()+1440=}")
    clean_plan = sue_personunit.get_plan_obj(clean_rope)
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(year_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(year_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar6day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar7day, yr2000_mar8day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar7day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar1day, yr2000_mar2day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar1day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 1

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar2day, yr2000_mar3day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar2day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar3day, yr2000_mar4day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar3day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar4day, yr2000_mar5day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar4day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 0

    # WHEN / THEN
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar5day, yr2000_mar6day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(sue_personunit.get_agenda_dict())=} {yr2000_mar5day=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")
    assert len(sue_personunit.get_agenda_dict()) == 0


def change_fact_print_attrs(x_personunit: PersonUnit, x_lower: float, x_upper: float):
    casa_rope = x_personunit.make_l1_rope(exx.casa)
    clean_rope = x_personunit.make_rope(casa_rope, exx.clean)
    clean_plan = x_personunit.get_plan_obj(clean_rope)
    time_rope = x_personunit.make_l1_rope(kw.time)
    creg_rope = x_personunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(x_personunit, kw.creg)
    week_rope = x_personunit.make_rope(creg_rope, kw.week)
    wed_rope = x_personunit.make_rope(week_rope, get_wed())
    x_personunit.add_fact(creg_rope, creg_rope, x_lower, x_upper)
    x_personunit.thinkout()

    print(f"{clean_plan.factheirs.get(wed_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(wed_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(wed_rope).reason_active=}")
    print(f"{len(x_personunit.get_agenda_dict())=} {x_upper=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")


def test_PersonUnit_add_time_creg_planunit_SyncsWeekDayAndYear_Thursday_March2_2000():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    creg_rope = sue_personunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(sue_personunit, kw.creg)
    week_rope = sue_personunit.make_rope(creg_rope, kw.week)
    # sun_rope = sue_personunit.make_rope(week_rope, get_sun())
    # mon_rope = sue_personunit.make_rope(week_rope, get_mon())
    # tue_rope = sue_personunit.make_rope(week_rope, get_tue())
    wed_rope = sue_personunit.make_rope(week_rope, get_wed())
    # thu_rope = sue_personunit.make_rope(week_rope, get_thu())
    # fri_rope = sue_personunit.make_rope(week_rope, get_fri())
    # sat_rope = sue_personunit.make_rope(week_rope, get_sat())
    sue_personunit = add_time_creg_planunit(sue_personunit)
    # creg_plan = sue_personunit.get_plan_obj(creg_rope)
    # week_plan = sue_personunit.get_plan_obj(week_rope)
    sue_personunit._set_plantree_range_attrs()
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=wed_rope,
        reason_case=wed_rope,
        reason_lower=thu_gogo_want(),
        reason_upper=thu_gogo_want() + 1440,
    )
    sue_personunit.edit_plan_attr(
        clean_rope,
        reason_context=year_rope,
        reason_case=year_rope,
        reason_lower=1400,
        reason_upper=2800,
    )

    yr2000_mar1day = get_creg_min_from_dt(datetime(2000, 3, 1, 0, 0))
    yr2000_mar2day = get_creg_min_from_dt(datetime(2000, 3, 2, 0, 0))
    yr2000_mar3day = get_creg_min_from_dt(datetime(2000, 3, 3, 0, 0))
    yr2000_mar4day = get_creg_min_from_dt(datetime(2000, 3, 4, 0, 0))
    yr2000_mar5day = get_creg_min_from_dt(datetime(2000, 3, 5, 0, 0))
    yr2000_mar6day = get_creg_min_from_dt(datetime(2000, 3, 6, 0, 0))
    yr2000_mar7day = get_creg_min_from_dt(datetime(2000, 3, 7, 0, 0))
    yr2000_mar8day = get_creg_min_from_dt(datetime(2000, 3, 8, 0, 0))
    print(f"{wed_gogo_want()=}")
    print(f"{wed_gogo_want()+1440=}")
    clean_plan = sue_personunit.get_plan_obj(clean_rope)
    sue_personunit.add_fact(creg_rope, creg_rope, yr2000_mar6day, yr2000_mar7day)
    sue_personunit.thinkout()
    print(f"{clean_plan.factheirs.get(year_rope).fact_lower=}")
    print(f"{clean_plan.factheirs.get(year_rope).fact_upper=}")
    print(f"{clean_plan.get_reasonheir(year_rope).reason_active=} \n")

    # WHEN / THEN
    change_fact_print_attrs(sue_personunit, yr2000_mar6day, yr2000_mar7day)
    assert len(sue_personunit.get_agenda_dict()) == 0
    change_fact_print_attrs(sue_personunit, yr2000_mar7day, yr2000_mar8day)
    assert len(sue_personunit.get_agenda_dict()) == 0
    change_fact_print_attrs(sue_personunit, yr2000_mar1day, yr2000_mar2day)
    assert len(sue_personunit.get_agenda_dict()) == 1
    change_fact_print_attrs(sue_personunit, yr2000_mar2day, yr2000_mar3day)
    assert len(sue_personunit.get_agenda_dict()) == 1
    change_fact_print_attrs(sue_personunit, yr2000_mar3day, yr2000_mar4day)
    assert len(sue_personunit.get_agenda_dict()) == 0
    change_fact_print_attrs(sue_personunit, yr2000_mar4day, yr2000_mar5day)
    change_fact_print_attrs(sue_personunit, yr2000_mar5day, yr2000_mar6day)
    assert len(sue_personunit.get_agenda_dict()) == 0
