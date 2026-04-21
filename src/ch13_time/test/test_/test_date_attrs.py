from ch07_person_logic.person_main import PersonUnit, personunit_shop
from ch13_time.epoch_main import EpochHolder, epochholder_shop, TimeNum
from ch13_time.test._util.ch13_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
    display_creg_five_squirt_time_attrs,
    display_current_creg_five_time_attrs,
    get_creg_min_from_dt,
    get_five_min_from_dt,
)
from datetime import datetime
from ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_TimeNum_Exists():
    # ESTABLISH / WHEN / THEN
    assert TimeNum(8) == 8


def test_EpochHolder_Exists():
    # ESTABLISH / WHEN
    x_epochholder = EpochHolder()

    # THEN
    assert not x_epochholder.x_personunit
    assert not x_epochholder.epoch_label
    assert not x_epochholder.x_min
    assert not x_epochholder._epoch_plan
    assert not x_epochholder._weekday
    assert not x_epochholder._monthday
    assert not x_epochholder._month
    assert not x_epochholder._hour
    assert not x_epochholder._minute
    assert not x_epochholder._c400_number
    assert not x_epochholder._c100_count
    assert not x_epochholder._yr4_count
    assert not x_epochholder._year_count
    assert not x_epochholder._year_num


def test_epochholder_shop_ReturnsObj():
    # ESTABLISH
    x_epoch_label = "Fay07"
    x_epoch_min = 890000
    sue_person = personunit_shop("Sue")

    # WHEN
    x_epochholder = epochholder_shop(
        x_personunit=sue_person,
        epoch_label=x_epoch_label,
        x_min=x_epoch_min,
    )

    # THEN
    assert x_epochholder.x_personunit == sue_person
    assert x_epochholder.epoch_label == x_epoch_label
    assert x_epochholder.x_min == x_epoch_min


def test_EpochHolder_set_epoch_plan_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_epochholder = epochholder_shop(sue_person, kw.creg, 10000000)
    assert not x_epochholder._epoch_plan

    # WHEN
    x_epochholder._set_epoch_plan()

    # THEN
    assert x_epochholder._epoch_plan


def test_EpochHolder_set_weekday_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_epochholder = epochholder_shop(sue_person, kw.creg, 10001440)
    x_epochholder._set_epoch_plan()
    assert not x_epochholder._weekday

    # WHEN
    x_epochholder._set_weekday()

    # THEN
    assert x_epochholder._weekday == exx.Thursday


def test_EpochHolder_set_month_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_epochholder = epochholder_shop(sue_person, kw.creg, 10060000)
    x_epochholder._set_epoch_plan()
    assert not x_epochholder._month
    assert not x_epochholder._monthday

    # WHEN
    x_epochholder._set_month()

    # THEN
    assert x_epochholder._month == "April"
    # assert x_epochholder._monthday == 16
    assert x_epochholder._monthday == 17


def test_EpochHolder_set_hour_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_epochholder = epochholder_shop(sue_person, kw.creg, 10000001)
    x_epochholder._set_epoch_plan()
    assert not x_epochholder._hour
    assert not x_epochholder._hour
    assert not x_epochholder._minute

    # WHEN
    x_epochholder._set_hour()

    # THEN
    assert x_epochholder._hour == "10am"
    assert x_epochholder._minute == 41


def test_EpochHolder_set_year_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_epochholder = epochholder_shop(sue_person, kw.creg, 1030600100)
    x_epochholder._set_epoch_plan()
    assert not x_epochholder._c400_number
    assert not x_epochholder._c100_count
    assert not x_epochholder._yr4_count
    assert not x_epochholder._year_count
    assert not x_epochholder._year_num

    # WHEN
    x_epochholder._set_year()

    # THEN
    print(f"{x_epochholder._year_num=}")
    assert x_epochholder._c400_number == 4
    assert x_epochholder._c100_count == 3
    assert x_epochholder._yr4_count == 14
    assert x_epochholder._year_count == 3
    assert x_epochholder._year_num == 1959


def test_EpochHolder_calc_epoch_SetsAttrs_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_epochholder = epochholder_shop(sue_person, kw.creg, 1030600102)
    assert not x_epochholder._epoch_plan
    assert not x_epochholder._weekday
    assert not x_epochholder._monthday
    assert not x_epochholder._month
    assert not x_epochholder._hour
    assert not x_epochholder._minute
    assert not x_epochholder._year_num

    # WHEN
    x_epochholder.calc_epoch()

    # THEN
    assert x_epochholder._epoch_plan
    assert x_epochholder._weekday
    assert x_epochholder._monthday
    assert x_epochholder._month
    assert x_epochholder._hour
    assert x_epochholder._minute
    assert x_epochholder._year_num


def test_EpochHolder_get_blurb_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_epochholder = epochholder_shop(sue_person, kw.creg, 1030600102)
    x_epochholder.calc_epoch()
    assert x_epochholder._epoch_plan
    assert x_epochholder._weekday
    assert x_epochholder._monthday
    assert x_epochholder._month
    assert x_epochholder._hour
    assert x_epochholder._minute
    assert x_epochholder._year_num

    # WHEN
    epoch_blurb = x_epochholder.get_blurb()

    # THEN
    x_str = f"{x_epochholder._hour}"
    x_str += f":{x_epochholder._minute}"
    x_str += f", {x_epochholder._weekday}"
    x_str += f", {x_epochholder._monthday}"
    x_str += f" {x_epochholder._month}"
    x_str += f", {x_epochholder._year_num}"
    assert epoch_blurb == x_str


def test_EpochHolder_calc_epoch_SetsAttrs_Scenario1_FiveEpoch(graphics_bool):
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person = add_time_five_planunit(sue_person)
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_epochholder = epochholder_shop(sue_person, kw.creg, creg_min)
    five_epochholder = epochholder_shop(sue_person, kw.five, five_min)
    assert not creg_epochholder._weekday
    assert not creg_epochholder._monthday
    assert not creg_epochholder._month
    assert not creg_epochholder._hour
    assert not creg_epochholder._minute
    assert not creg_epochholder._year_num
    assert not five_epochholder._weekday
    assert not five_epochholder._monthday
    assert not five_epochholder._month
    assert not five_epochholder._hour
    assert not five_epochholder._minute
    assert not five_epochholder._year_num

    # WHEN
    creg_epochholder.calc_epoch()
    five_epochholder.calc_epoch()

    # THEN
    assert creg_epochholder._weekday == exx.Wednesday
    assert creg_epochholder._month == "March"
    assert creg_epochholder._monthday == 1
    assert creg_epochholder._hour == "12am"
    assert creg_epochholder._minute == 0
    assert creg_epochholder._year_num == 2000
    assert five_epochholder._weekday == kw.Baileyday
    assert five_epochholder._monthday == 0
    assert five_epochholder._month == "Fredrick"
    assert five_epochholder._hour == "0hr"
    assert five_epochholder._minute == 0
    assert five_epochholder._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_epoch_attr(x_person: PersonUnit, x_datetime: datetime):
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_epochholder = epochholder_shop(x_person, kw.creg, creg_min)
    creg_epochholder.calc_epoch()
    dt_hour = x_datetime.strftime("%H")
    dt_minute = x_datetime.strftime("%M")
    dt_weekday = x_datetime.strftime("%A")
    dt_month = x_datetime.strftime("%B")
    dt_monthday = x_datetime.strftime("%d")
    dt_year = x_datetime.strftime("%Y")
    hour_str = ""
    hour_int = int(dt_hour)
    if hour_int == 0:
        hour_str = "12am"
    elif hour_int < 12:
        hour_str = f"{hour_int}am"
    elif hour_int == 12:
        hour_str = "12pm"
    else:
        hour_str = f"{hour_int%12}pm"
    print(x_datetime.strftime("%H:%M, %A, %d %B, %Y"))
    if creg_epochholder._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_epochholder._weekday == dt_weekday
    assert creg_epochholder._month == dt_month
    # assert creg_epochholder._monthday == int(dt_monthday) - 1
    assert creg_epochholder._monthday == int(dt_monthday)
    assert creg_epochholder._hour == hour_str
    assert creg_epochholder._minute == int(dt_minute)
    assert creg_epochholder._year_num == int(dt_year)


def test_EpochHolder_calc_epoch_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    # WHEN / THEN
    check_creg_epoch_attr(sue_person, datetime(2000, 3, 1, 0, 21))
    check_creg_epoch_attr(sue_person, datetime(2000, 3, 1, 3, 21))
    check_creg_epoch_attr(sue_person, datetime(2000, 3, 1, 12, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 3, 1, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 4, 1, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 4, 20, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 4, 28, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 4, 29, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 4, 30, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 5, 1, 13, 00))
    check_creg_epoch_attr(sue_person, datetime(2000, 7, 1, 13, 56))
    check_creg_epoch_attr(sue_person, datetime(2003, 12, 28, 17, 56))
    check_creg_epoch_attr(sue_person, datetime(2003, 2, 28, 17, 56))
    check_creg_epoch_attr(sue_person, datetime(432, 3, 4, 2, 0))
