from ch07_person_logic.person_main import PersonUnit, personunit_shop
from ch13_time.epoch_main import (
    TimeNum,
    TimeShoe,
    ordinal_suffix,
    split_first_number,
    timeshoe_shop,
)
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


def test_split_first_number_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert "123", "abcdef456" == split_first_number("abc123def456")
    assert "123", "start" == split_first_number("123start")
    assert "456", "end" == split_first_number("end456")
    assert "1", "ab2c3" == split_first_number("a1b2c3")
    print(split_first_number("no numbers here"))
    assert ("", "no numbers here") == split_first_number("no numbers here")
    assert ("", "") == split_first_number("")
    assert "99", "xy99z" == split_first_number("x99y99z")
    assert "123", "abcdef" == split_first_number("abc123def")


def test_ordinal_suffix_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert ordinal_suffix(1) == "st"
    assert ordinal_suffix(2) == "nd"
    assert ordinal_suffix(3) == "rd"
    assert ordinal_suffix(4) == "th"
    assert ordinal_suffix(11) == "th"
    assert ordinal_suffix(22) == "nd"
    assert ordinal_suffix(103) == "rd"
    assert ordinal_suffix(-1) == "st"
    assert ordinal_suffix(-2) == "nd"
    assert ordinal_suffix(-3) == "rd"
    assert ordinal_suffix(-4) == "th"
    assert ordinal_suffix(-11) == "th"
    assert ordinal_suffix(-22) == "nd"
    assert ordinal_suffix(-103) == "rd"


def test_TimeShoe_Exists():
    # ESTABLISH / WHEN
    x_timeshoe = TimeShoe()

    # THEN
    assert not x_timeshoe.person
    assert not x_timeshoe.epoch_label
    assert not x_timeshoe.shoe_min
    assert not x_timeshoe._epoch_plan
    assert not x_timeshoe._weekday
    assert not x_timeshoe._monthday
    assert not x_timeshoe._month
    assert not x_timeshoe._hour_label
    assert not x_timeshoe._minute
    assert not x_timeshoe._c400_number
    assert not x_timeshoe._c100_count
    assert not x_timeshoe._yr4_count
    assert not x_timeshoe._year_count
    assert not x_timeshoe._year_num
    assert not x_timeshoe._datetime
    assert set(x_timeshoe.__dict__.keys()) == {
        "person",
        "epoch_label",
        "shoe_min",
        "_epoch_plan",
        "_weekday",
        "_monthday",
        "_month",
        "_hour_label",
        "_minute",
        "_c400_number",
        "_c100_count",
        "_yr4_count",
        "_year_count",
        "_year_num",
        "_datetime",
    }


def test_timeshoe_shop_ReturnsObj():
    # ESTABLISH
    x_epoch_label = "Fay07"
    x_epoch_min = 890000
    sue_person = personunit_shop("Sue")

    # WHEN
    x_timeshoe = timeshoe_shop(
        shoe_person=sue_person,
        epoch_label=x_epoch_label,
        shoe_min=x_epoch_min,
    )

    # THEN
    assert x_timeshoe.person == sue_person
    assert x_timeshoe.epoch_label == x_epoch_label
    assert x_timeshoe.shoe_min == x_epoch_min


def test_TimeShoe_set_epoch_plan_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 10000000)
    assert not x_timeshoe._epoch_plan

    # WHEN
    x_timeshoe._set_epoch_plan()

    # THEN
    assert x_timeshoe._epoch_plan


def test_TimeShoe_set_weekday_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 10001440)
    x_timeshoe._set_epoch_plan()
    assert not x_timeshoe._weekday

    # WHEN
    x_timeshoe._set_weekday()

    # THEN
    assert x_timeshoe._weekday == exx.Thursday


def test_TimeShoe_set_month_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 10060000)
    x_timeshoe._set_epoch_plan()
    assert not x_timeshoe._month
    assert not x_timeshoe._monthday

    # WHEN
    x_timeshoe._set_month()

    # THEN
    assert x_timeshoe._month == "April"
    # assert x_timeshoe._monthday == 16
    assert x_timeshoe._monthday == 17


def test_TimeShoe_set_hour_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 10000761)
    x_timeshoe._set_epoch_plan()
    assert not x_timeshoe._hour_label
    assert not x_timeshoe._minute

    # WHEN
    x_timeshoe._set_hour()

    # THEN
    assert x_timeshoe._hour_label == "11pm"
    assert x_timeshoe._minute == 21


def test_TimeShoe_set_year_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 1030600100)
    x_timeshoe._set_epoch_plan()
    assert not x_timeshoe._c400_number
    assert not x_timeshoe._c100_count
    assert not x_timeshoe._yr4_count
    assert not x_timeshoe._year_count
    assert not x_timeshoe._year_num

    # WHEN
    x_timeshoe._set_year()

    # THEN
    print(f"{x_timeshoe._year_num=}")
    assert x_timeshoe._c400_number == 4
    assert x_timeshoe._c100_count == 3
    assert x_timeshoe._yr4_count == 14
    assert x_timeshoe._year_count == 3
    assert x_timeshoe._year_num == 1959


def test_TimeShoe_set_datetime_SetsAttr_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person.thinkout()
    x_shoe_min = 1030600100
    creg_timeshoe = timeshoe_shop(sue_person, kw.creg, x_shoe_min)
    creg_timeshoe._set_epoch_plan()
    assert not creg_timeshoe._datetime
    # WHEN
    creg_timeshoe._set_datetime()
    # THEN
    print(f"{creg_timeshoe._weekday=}")
    print(f"{creg_timeshoe._monthday=}")
    print(f"{creg_timeshoe._month=}")
    print(f"{creg_timeshoe._hour_label=}")
    print(f"{creg_timeshoe._minute=}")
    print(f"{creg_timeshoe._year_num=}")
    assert creg_timeshoe._datetime == datetime(1959, 9, 2, 12, 20)


def test_TimeShoe_calc_epoch_SetsAttrs_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 1030600102)
    assert not x_timeshoe._epoch_plan
    assert not x_timeshoe._weekday
    assert not x_timeshoe._monthday
    assert not x_timeshoe._month
    assert not x_timeshoe._hour_label
    assert not x_timeshoe._minute
    assert not x_timeshoe._year_num

    # WHEN
    x_timeshoe.calc_epoch()

    # THEN
    assert x_timeshoe._epoch_plan
    assert x_timeshoe._weekday
    assert x_timeshoe._monthday
    assert x_timeshoe._month
    assert x_timeshoe._hour_label
    assert x_timeshoe._minute
    assert x_timeshoe._year_num


def test_TimeShoe_calc_epoch_SetsAttrs_Scenario1_FiveEpoch(graphics_bool):
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    sue_person = add_time_five_planunit(sue_person)
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_timeshoe = timeshoe_shop(sue_person, kw.creg, creg_min)
    five_timeshoe = timeshoe_shop(sue_person, kw.five, five_min)
    assert not creg_timeshoe._weekday
    assert not creg_timeshoe._monthday
    assert not creg_timeshoe._month
    assert not creg_timeshoe._hour_label
    assert not creg_timeshoe._minute
    assert not creg_timeshoe._year_num
    assert not five_timeshoe._weekday
    assert not five_timeshoe._monthday
    assert not five_timeshoe._month
    assert not five_timeshoe._hour_label
    assert not five_timeshoe._minute
    assert not five_timeshoe._year_num

    # WHEN
    creg_timeshoe.calc_epoch()
    five_timeshoe.calc_epoch()

    # THEN
    assert creg_timeshoe._weekday == exx.Wednesday
    assert creg_timeshoe._month == "March"
    assert creg_timeshoe._monthday == 1
    assert creg_timeshoe._hour_label == "12am"
    assert creg_timeshoe._minute == 0
    assert creg_timeshoe._year_num == 2000
    assert five_timeshoe._weekday == kw.Baileyday
    assert five_timeshoe._monthday == 0
    assert five_timeshoe._month == "Fredrick"
    assert five_timeshoe._hour_label == "0hr"
    assert five_timeshoe._minute == 0
    assert five_timeshoe._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_epoch_attr(x_person: PersonUnit, x_datetime: datetime):
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_timeshoe = timeshoe_shop(x_person, kw.creg, creg_min)
    creg_timeshoe.calc_epoch()
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
    if creg_timeshoe._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_timeshoe._weekday == dt_weekday
    assert creg_timeshoe._month == dt_month
    # assert creg_timeshoe._monthday == int(dt_monthday) - 1
    assert creg_timeshoe._monthday == int(dt_monthday)
    assert creg_timeshoe._hour_label == hour_str
    assert creg_timeshoe._minute == int(dt_minute)
    assert creg_timeshoe._year_num == int(dt_year)


def test_TimeShoe_calc_epoch_SetsAttr_Scenario1():
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


def test_TimeShoe_calc_epoch_SetsAttrs_Scenario2_five():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_five_planunit(sue_person)
    five_timeshoe = timeshoe_shop(sue_person, kw.five, 1030600102)
    assert not five_timeshoe._epoch_plan
    assert not five_timeshoe._weekday
    assert not five_timeshoe._monthday
    assert not five_timeshoe._month
    assert not five_timeshoe._hour_label
    assert not five_timeshoe._minute
    assert not five_timeshoe._year_num

    # WHEN
    five_timeshoe.calc_epoch()

    # THEN
    print(f"{five_timeshoe._weekday=}")
    print(f"{five_timeshoe._monthday=}")
    print(f"{five_timeshoe._month=}")
    print(f"{five_timeshoe._hour_label=}")
    print(f"{five_timeshoe._minute=}")
    print(f"{five_timeshoe._year_num=}")
    assert five_timeshoe._epoch_plan
    assert five_timeshoe._weekday == "Eastday"
    assert five_timeshoe._monthday == 10
    assert five_timeshoe._month == "Mikayla"
    assert five_timeshoe._hour_label == "5hr"
    assert five_timeshoe._minute == 22
    assert five_timeshoe._year_num == 1959


def test_TimeShoe_calc_epoch_SetsAttrs_Scenario3_creg_datetime():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    creg_timeshoe = timeshoe_shop(sue_person, kw.creg, 1030600102)
    creg_timeshoe.calc_epoch()
    assert creg_timeshoe._datetime == datetime(1959, 9, 2, 12, 22)
    new_show_min = 1030600102 + 600

    # WHEN
    creg_timeshoe.calc_epoch(new_show_min)

    # THEN
    print(f"{creg_timeshoe._monthday=}")
    print(f"{creg_timeshoe._month=}")
    print(f"{creg_timeshoe._hour_label=}")
    print(f"{creg_timeshoe._minute=}")
    print(f"{creg_timeshoe._year_num=}")
    assert creg_timeshoe.shoe_min == new_show_min
    assert creg_timeshoe._datetime == datetime(1959, 9, 2, 22, 22)


def test_TimeShoe_get_full_blurb_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 1030600102)
    x_timeshoe.calc_epoch()
    assert x_timeshoe._epoch_plan
    assert x_timeshoe._weekday
    assert x_timeshoe._monthday
    assert x_timeshoe._month
    assert x_timeshoe._hour_label
    assert x_timeshoe._minute
    assert x_timeshoe._year_num

    # WHEN
    epoch_blurb = x_timeshoe.get_full_blurb()

    # THEN
    x_str = f"{x_timeshoe._hour_label}"
    x_str += f":{x_timeshoe._minute}"
    x_str += f", {x_timeshoe._weekday}"
    x_str += f", {x_timeshoe._monthday}"
    x_str += f" {x_timeshoe._month}"
    x_str += f", {x_timeshoe._year_num}"
    assert epoch_blurb == x_str


def test_TimeShoe_clock_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 1030600102)
    assert not x_timeshoe._hour_label
    # WHEN / THEN
    assert x_timeshoe.clock() == ""
    # WHEN / THEN
    x_timeshoe._hour_label = "12pm"
    x_timeshoe._minute = "33"
    assert x_timeshoe.clock() == f"12:{x_timeshoe._minute}pm"
    # WHEN / THEN
    x_timeshoe._hour_label = "1pm"
    assert x_timeshoe.clock() == f"1:{x_timeshoe._minute}pm"
    # WHEN / THEN
    x_timeshoe._hour_label = "hr1up"
    assert x_timeshoe.clock() == f"1:{x_timeshoe._minute}hrup"


def test_TimeShoe_get_long_date_blurb_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person = add_time_creg_planunit(sue_person)
    x_timeshoe = timeshoe_shop(sue_person, kw.creg, 1030600102)
    x_timeshoe.calc_epoch()

    # WHEN
    date_blurb = x_timeshoe.get_long_date_blurb()

    # THEN
    expected_monthday = f"{x_timeshoe._monthday}{ordinal_suffix(x_timeshoe._monthday)}"
    expected_long_date_blurb = (
        f"{x_timeshoe._month} {expected_monthday} {x_timeshoe._year_num}"
    )
    assert date_blurb == expected_long_date_blurb
