from ch07_person_logic.person_main import PersonUnit, personunit_shop
from ch13_time.epoch_main import EpochHolder, TimeNum, epochholder_shop
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
    x_TimeNum = EpochHolder()

    # THEN
    assert not x_TimeNum.x_personunit
    assert not x_TimeNum.epoch_label
    assert not x_TimeNum.x_min
    assert not x_TimeNum._epoch_plan
    assert not x_TimeNum._weekday
    assert not x_TimeNum._monthday
    assert not x_TimeNum._month
    assert not x_TimeNum._hour
    assert not x_TimeNum._minute
    assert not x_TimeNum._c400_number
    assert not x_TimeNum._c100_count
    assert not x_TimeNum._yr4_count
    assert not x_TimeNum._year_count
    assert not x_TimeNum._year_num


def test_epochholder_shop_ReturnsObj():
    # ESTABLISH
    x_epoch_label = "Fay07"
    x_epoch_min = 890000
    sue_person = personunit_shop("Sue")

    # WHEN
    x_TimeNum = epochholder_shop(
        x_personunit=sue_person,
        epoch_label=x_epoch_label,
        x_min=x_epoch_min,
    )

    # THEN
    assert x_TimeNum.x_personunit == sue_person
    assert x_TimeNum.epoch_label == x_epoch_label
    assert x_TimeNum.x_min == x_epoch_min


def test_EpochHolder_set_epoch_plan_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 10000000)
    assert not x_TimeNum._epoch_plan

    # WHEN
    x_TimeNum._set_epoch_plan()

    # THEN
    assert x_TimeNum._epoch_plan


def test_EpochHolder_set_weekday_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 10001440)
    x_TimeNum._set_epoch_plan()
    assert not x_TimeNum._weekday

    # WHEN
    x_TimeNum._set_weekday()

    # THEN
    assert x_TimeNum._weekday == exx.Thursday


def test_EpochHolder_set_month_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 10060000)
    x_TimeNum._set_epoch_plan()
    assert not x_TimeNum._month
    assert not x_TimeNum._monthday

    # WHEN
    x_TimeNum._set_month()

    # THEN
    assert x_TimeNum._month == "April"
    # assert x_TimeNum._monthday == 16
    assert x_TimeNum._monthday == 17


def test_EpochHolder_set_hour_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 10000001)
    x_TimeNum._set_epoch_plan()
    assert not x_TimeNum._hour
    assert not x_TimeNum._hour
    assert not x_TimeNum._minute

    # WHEN
    x_TimeNum._set_hour()

    # THEN
    assert x_TimeNum._hour == "10am"
    assert x_TimeNum._minute == 41


def test_EpochHolder_set_year_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 1030600100)
    x_TimeNum._set_epoch_plan()
    assert not x_TimeNum._c400_number
    assert not x_TimeNum._c100_count
    assert not x_TimeNum._yr4_count
    assert not x_TimeNum._year_count
    assert not x_TimeNum._year_num

    # WHEN
    x_TimeNum._set_year()

    # THEN
    print(f"{x_TimeNum._year_num=}")
    assert x_TimeNum._c400_number == 4
    assert x_TimeNum._c100_count == 3
    assert x_TimeNum._yr4_count == 14
    assert x_TimeNum._year_count == 3
    assert x_TimeNum._year_num == 1959


def test_EpochHolder_calc_epoch_SetsAttrs():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 1030600102)
    assert not x_TimeNum._epoch_plan
    assert not x_TimeNum._weekday
    assert not x_TimeNum._monthday
    assert not x_TimeNum._month
    assert not x_TimeNum._hour
    assert not x_TimeNum._minute
    assert not x_TimeNum._year_num

    # WHEN
    x_TimeNum.calc_epoch()

    # THEN
    assert x_TimeNum._epoch_plan
    assert x_TimeNum._weekday
    assert x_TimeNum._monthday
    assert x_TimeNum._month
    assert x_TimeNum._hour
    assert x_TimeNum._minute
    assert x_TimeNum._year_num


def test_EpochHolder_get_blurb_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_TimeNum = epochholder_shop(sue_person, kw.creg, 1030600102)
    x_TimeNum.calc_epoch()
    assert x_TimeNum._epoch_plan
    assert x_TimeNum._weekday
    assert x_TimeNum._monthday
    assert x_TimeNum._month
    assert x_TimeNum._hour
    assert x_TimeNum._minute
    assert x_TimeNum._year_num

    # WHEN
    epoch_blurb = x_TimeNum.get_blurb()

    # THEN
    x_str = f"{x_TimeNum._hour}"
    x_str += f":{x_TimeNum._minute}"
    x_str += f", {x_TimeNum._weekday}"
    x_str += f", {x_TimeNum._monthday}"
    x_str += f" {x_TimeNum._month}"
    x_str += f", {x_TimeNum._year_num}"
    assert epoch_blurb == x_str


def test_calc_epoch_SetsAttrFiveEpoch(graphics_bool):
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person = add_time_five_planunit(sue_person)
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_TimeNum = epochholder_shop(sue_person, kw.creg, creg_min)
    five_TimeNum = epochholder_shop(sue_person, kw.five, five_min)
    assert not creg_TimeNum._weekday
    assert not creg_TimeNum._monthday
    assert not creg_TimeNum._month
    assert not creg_TimeNum._hour
    assert not creg_TimeNum._minute
    assert not creg_TimeNum._year_num
    assert not five_TimeNum._weekday
    assert not five_TimeNum._monthday
    assert not five_TimeNum._month
    assert not five_TimeNum._hour
    assert not five_TimeNum._minute
    assert not five_TimeNum._year_num

    # WHEN
    creg_TimeNum.calc_epoch()
    five_TimeNum.calc_epoch()

    # THEN
    assert creg_TimeNum._weekday == exx.Wednesday
    assert creg_TimeNum._month == "March"
    assert creg_TimeNum._monthday == 1
    assert creg_TimeNum._hour == "12am"
    assert creg_TimeNum._minute == 0
    assert creg_TimeNum._year_num == 2000
    assert five_TimeNum._weekday == kw.Baileyday
    assert five_TimeNum._monthday == 0
    assert five_TimeNum._month == "Fredrick"
    assert five_TimeNum._hour == "0hr"
    assert five_TimeNum._minute == 0
    assert five_TimeNum._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_epoch_attr(x_person: PersonUnit, x_datetime: datetime):
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_TimeNum = epochholder_shop(x_person, kw.creg, creg_min)
    creg_TimeNum.calc_epoch()
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
    if creg_TimeNum._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_TimeNum._weekday == dt_weekday
    assert creg_TimeNum._month == dt_month
    # assert creg_TimeNum._monthday == int(dt_monthday) - 1
    assert creg_TimeNum._monthday == int(dt_monthday)
    assert creg_TimeNum._hour == hour_str
    assert creg_TimeNum._minute == int(dt_minute)
    assert creg_TimeNum._year_num == int(dt_year)


def test_EpochHolder_calc_epoch_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")

    # WHEN
    sue_person = add_time_creg_planunit(sue_person)

    # THEN
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
