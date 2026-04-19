from ch13_time.calendar_markdown import (
    CalendarMarkDown,
    MonthMarkDownRow,
    MonthMarkDownUnit,
    centered_to_len,
    get_calendarmarkdown_str,
)
from ch13_time.epoch_main import epochunit_shop, get_default_epoch_config_dict
from ch13_time.test._util.ch13_examples import (
    get_expected_creg_2024_markdown,
    get_expected_creg_year0_markdown,
    get_expected_five_5524_markdown,
    get_five_config,
)
from ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_centered_to_len_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert centered_to_len(10, "fay") == "   fay    "
    assert centered_to_len(15, "fay") == "      fay      "
    assert centered_to_len(6, "fay") == " fay  "
    assert centered_to_len(5, "faybob") == "faybo"


def test_MonthMarkDownUnit_Exists():
    # ESTABLISH / WHEN
    x_monthmarkdownunit = MonthMarkDownUnit()

    # THEN
    assert not x_monthmarkdownunit.label
    assert not x_monthmarkdownunit.cumulative_days
    assert not x_monthmarkdownunit.first_weekday
    assert not x_monthmarkdownunit.week_length
    assert not x_monthmarkdownunit.month_days_int
    assert not x_monthmarkdownunit.monthday_index
    assert not x_monthmarkdownunit.weekday_2char_abvs
    assert not x_monthmarkdownunit.max_monthday_rows
    assert not x_monthmarkdownunit.year
    assert not x_monthmarkdownunit.offset_year


def test_MonthMarkDownUnit_markdown_label_ReturnsObj_Scenario0_No_offset_year():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    jan_monthmarkdownunit.year = 1999

    # WHEN
    markdown_label = jan_monthmarkdownunit.markdown_label()

    # THEN
    assert markdown_label == "      January       "
    assert len(markdown_label) == 3 * 7 - 1


def test_MonthMarkDownUnit_markdown_label_ReturnsObj_Scenario1_Yes_offset_year():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    jan_monthmarkdownunit.offset_year = True
    jan_monthmarkdownunit.year = 1999

    # WHEN
    markdown_label = jan_monthmarkdownunit.markdown_label()

    # THEN
    assert markdown_label == "   January (2000)   "
    assert len(markdown_label) == 3 * 7 - 1


def test_MonthMarkDownUnit_markdown_weekdays_ReturnsObj():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    jan_monthmarkdownunit.weekday_2char_abvs = [
        "Mo",
        "Tu",
        "We",
        "Th",
        "Fr",
        "Sa",
        "Su",
    ]

    # WHEN
    markdown_weekdays = jan_monthmarkdownunit.markdown_weekdays()

    # THEN
    assert markdown_weekdays == "Mo Tu We Th Fr Sa Su"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario0_Row0():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_index=0,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == " 0  1  2  3  4  5  6"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario1_Row1():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_index=0,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=1)

    # THEN
    assert markdown_day_numbers == " 7  8  9 10 11 12 13"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario2_monthday_index():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_index=1,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == " 1  2  3  4  5  6  7"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario3_first_weekday():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_index=1,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == "          1  2  3  4"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario4_first_weekday():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_index=1,
    )

    # WHEN / THEN
    assert (
        jan_monthmarkdownunit.markdown_day_numbers(row_int=1) == " 5  6  7  8  9 10 11"
    )
    assert (
        jan_monthmarkdownunit.markdown_day_numbers(row_int=4) == "26 27 28 29 30 31   "
    )


def test_MonthMarkDownUnit_set_max_monthday_rows_ReturnsObj_Scenario0():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_index=1,
    )
    assert not jan_monthmarkdownunit.max_monthday_rows

    # WHEN
    jan_monthmarkdownunit.set_max_monthday_rows()

    # THEN
    assert jan_monthmarkdownunit.max_monthday_rows == 5


def test_MonthMarkDownUnit_get_next_month_first_weekday_ReturnsObj_Scenario0():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        exx.February,
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=28,
    )

    # WHEN / THEN
    assert jan_monthmarkdownunit.get_next_month_first_weekday() == 3


def test_MonthMarkDownUnit_get_next_month_first_weekday_ReturnsObj_Scenario1():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        exx.February,
        None,
        first_weekday=6,
        week_length=7,
        month_days_int=28,
    )

    # WHEN / THEN
    assert jan_monthmarkdownunit.get_next_month_first_weekday() == 6


def test_MonthMarkDownUnit_get_next_month_first_weekday_ReturnsObj_Scenario2():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        exx.February,
        None,
        first_weekday=6,
        week_length=7,
        month_days_int=31,
    )

    # WHEN / THEN
    assert jan_monthmarkdownunit.get_next_month_first_weekday() == 2


def test_MonthMarkDownRow_Exists():
    # ESTABLISH / WHEN
    x_monthmarkdownrow = MonthMarkDownRow()

    # THEN
    assert not x_monthmarkdownrow.months
    assert not x_monthmarkdownrow.max_monthday_numbers_row


def test_MonthMarkDownRow_set_max_monthday_numbers_row_SetsAttr():
    # ESTABLISH
    x_monthmarkdownrow = MonthMarkDownRow([])
    jan_monthmarkdownunit = MonthMarkDownUnit(exx.January, None, 5, 7, 31, 1)
    feb_monthmarkdownunit = MonthMarkDownUnit(exx.February, None, 1, 7, 29, 1)
    mar_monthmarkdownunit = MonthMarkDownUnit(exx.March, None, 2, 7, 31, 1)
    x_monthmarkdownrow.months.append(jan_monthmarkdownunit)
    x_monthmarkdownrow.months.append(feb_monthmarkdownunit)
    x_monthmarkdownrow.months.append(mar_monthmarkdownunit)
    assert not x_monthmarkdownrow.max_monthday_numbers_row

    # WHEN
    x_monthmarkdownrow.set_max_monthday_numbers_row()

    # THEN
    assert x_monthmarkdownrow.max_monthday_numbers_row == 6


def test_MonthMarkDownRow_markdown_str_ReturnsObj():
    # ESTABLISH
    x_monthmarkdownrow = MonthMarkDownRow([])
    jan_monthmarkdownunit = MonthMarkDownUnit(exx.January, None, 0, 7, 31, 1)
    feb_monthmarkdownunit = MonthMarkDownUnit(exx.February, None, 3, 7, 29, 1)
    mar_monthmarkdownunit = MonthMarkDownUnit(exx.March, None, 4, 7, 31, 1)
    x_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    jan_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_abvs
    feb_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_abvs
    mar_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_abvs
    x_monthmarkdownrow.months.append(jan_monthmarkdownunit)
    x_monthmarkdownrow.months.append(feb_monthmarkdownunit)
    x_monthmarkdownrow.months.append(mar_monthmarkdownunit)

    # WHEN
    x_str = x_monthmarkdownrow.markdown_str()

    # THEN
    print(f"{x_str}")
    expected_str = """
      January                   February                   March        
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
 1  2  3  4  5  6  7                1  2  3  4                   1  2  3
 8  9 10 11 12 13 14       5  6  7  8  9 10 11       4  5  6  7  8  9 10
15 16 17 18 19 20 21      12 13 14 15 16 17 18      11 12 13 14 15 16 17
22 23 24 25 26 27 28      19 20 21 22 23 24 25      18 19 20 21 22 23 24
29 30 31                  26 27 28 29               25 26 27 28 29 30 31"""
    assert x_str == expected_str


def test_CalendarMarkDown_Exists():
    # ESTABLISH / WHEN
    x_calendarmarkdown = CalendarMarkDown()

    # THEN
    assert not x_calendarmarkdown.epochunit
    assert not x_calendarmarkdown.epoch_config
    assert not x_calendarmarkdown.monthmarkdownrows
    assert not x_calendarmarkdown.week_length
    assert not x_calendarmarkdown.month_char_width
    assert not x_calendarmarkdown.monthmarkdownrow_length
    assert not x_calendarmarkdown.display_md_width
    assert not x_calendarmarkdown.display_init_day
    assert not x_calendarmarkdown.yr1_jan1_offset_days
    assert x_calendarmarkdown.max_md_width == 84


def test_CalendarMarkDown_create_2char_weekday_list_ReturnsObj_Scenario0_display_init_day_ParameterPassed():
    # ESTABLISH
    creg_config = get_default_epoch_config_dict()
    creg_calendermarkdown = CalendarMarkDown(epoch_config=creg_config)
    creg_calendermarkdown.display_init_day = exx.Monday
    creg_calendermarkdown.set_monthmarkdownrows(exx.Wednesday, 1997)

    # WHEN
    weekday_2char_list = creg_calendermarkdown.create_2char_weekday_list()

    # THEN
    expected_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    assert weekday_2char_list == expected_weekday_2char_abvs


def test_CalendarMarkDown_create_2char_weekday_list_ReturnsObj_Scenario1_display_init_day_ParameterNotPassed():
    # ESTABLISH
    creg_config = get_default_epoch_config_dict()
    creg_calendermarkdown = CalendarMarkDown(epoch_config=creg_config)
    creg_calendermarkdown.set_monthmarkdownrows(exx.Wednesday, 1997)

    # WHEN
    weekday_2char_list = creg_calendermarkdown.create_2char_weekday_list()

    # THEN
    expected_weekday_2char_abvs = ["We", "Th", "Fr", "Sa", "Su", "Mo", "Tu"]
    assert weekday_2char_list == expected_weekday_2char_abvs


def test_CalendarMarkDown_set_monthmarkdownrows_SetsAttr():
    # ESTABLISH
    creg_config = get_default_epoch_config_dict()
    creg_calendermarkdown = CalendarMarkDown(epoch_config=creg_config)
    monday_str = exx.Monday
    creg_calendermarkdown.display_init_day = monday_str
    x_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    yr1997_int = 1997
    assert not creg_calendermarkdown.epochunit

    # WHEN
    creg_calendermarkdown.set_monthmarkdownrows(exx.Tuesday, yr1997_int)

    # THEN
    expected_epochunit = epochunit_shop(creg_config)
    assert creg_calendermarkdown.epochunit == expected_epochunit
    assert creg_calendermarkdown.week_length == 7
    assert creg_calendermarkdown.month_char_width == 26
    assert creg_calendermarkdown.monthmarkdownrow_length == 3
    assert creg_calendermarkdown.display_md_width == 72
    assert len(creg_calendermarkdown.monthmarkdownrows) == 4
    assert len(creg_calendermarkdown.monthmarkdownrows[0].months) == 3
    monthmarkdownunit0 = creg_calendermarkdown.monthmarkdownrows[0].months[0]
    assert monthmarkdownunit0.label == "March"
    assert monthmarkdownunit0.cumulative_days == 31
    assert monthmarkdownunit0.month_days_int == 31
    assert monthmarkdownunit0.week_length == 7
    assert monthmarkdownunit0.monthday_index == 1
    assert monthmarkdownunit0.weekday_2char_abvs == x_weekday_2char_abvs
    assert monthmarkdownunit0.first_weekday == 1
    assert monthmarkdownunit0.year == yr1997_int
    assert not monthmarkdownunit0.offset_year
    monthmarkdownunit7 = creg_calendermarkdown.monthmarkdownrows[2].months[0]
    assert monthmarkdownunit7.label == "September"
    assert monthmarkdownunit7.cumulative_days == 214
    assert monthmarkdownunit7.month_days_int == 30
    assert monthmarkdownunit7.week_length == 7
    assert monthmarkdownunit7.monthday_index == 1
    assert monthmarkdownunit7.weekday_2char_abvs == x_weekday_2char_abvs
    assert monthmarkdownunit7.first_weekday == 3
    assert monthmarkdownunit7.year == yr1997_int
    assert not monthmarkdownunit7.offset_year
    monthmarkdownunit11 = creg_calendermarkdown.monthmarkdownrows[3].months[1]
    assert monthmarkdownunit11.label == "January"
    assert monthmarkdownunit11.year == yr1997_int
    assert monthmarkdownunit11.offset_year
    # assert monthmarkdownunit7.first_weekday == 4


def test_CalendarMarkDown_create_markdown_ReturnsObj_Scernario0_creg_config():
    # ESTABLISH
    creg_config = get_default_epoch_config_dict()
    creg_calendermarkdown = CalendarMarkDown(epoch_config=creg_config)
    creg_calendermarkdown.display_init_day = exx.Monday
    year_int = 2024

    # WHEN
    cal_markdown = creg_calendermarkdown.create_markdown(year_int)

    # THEN
    print(cal_markdown)
    expected_calendar_markdown = get_expected_creg_2024_markdown()
    print("")
    print(expected_calendar_markdown)
    assert cal_markdown == expected_calendar_markdown


def test_CalendarMarkDown_create_markdown_ReturnsObj_Scernario1_five_config():
    # ESTABLISH
    five_calendermarkdown = CalendarMarkDown(epoch_config=get_five_config())
    five_calendermarkdown.display_init_day = kw.Anaday
    year_int = 5224

    # WHEN
    cal_markdown = five_calendermarkdown.create_markdown(year_int)

    # THEN
    print(cal_markdown)
    expected_calendar_markdown = get_expected_five_5524_markdown()
    print("")
    print(expected_calendar_markdown)
    assert cal_markdown == expected_calendar_markdown


def test_get_calendarmarkdown_str_ReturnsObj_Scenario0_display_init_day_ParameterNotPassed():
    # ESTABLISH
    five_epoch_config = get_five_config()
    yr5524 = 5224

    # WHEN
    five_calendarmarkdown_str = get_calendarmarkdown_str(five_epoch_config, yr5524)

    # THEN
    assert five_calendarmarkdown_str == get_expected_five_5524_markdown()


def test_get_calendarmarkdown_str_ReturnsObj_Scenario1_display_init_day_ParameterPassed():
    # ESTABLISH
    five_config = get_five_config()
    yr5524 = 5224
    chiday_str = kw.Chiday
    anaday_str = kw.Anaday
    expected_str = get_expected_five_5524_markdown()

    # WHEN / THEN
    assert expected_str != get_calendarmarkdown_str(five_config, yr5524, chiday_str)
    assert expected_str == get_calendarmarkdown_str(five_config, yr5524, anaday_str)


def test_get_calendarmarkdown_str_ReturnsObj_Scenario2_AllDefaults():
    # ESTABLISH
    creg_config = get_default_epoch_config_dict()
    year = 0
    expected_creg_year0_markdow = get_expected_creg_year0_markdown()

    # WHEN / THEN
    print(get_calendarmarkdown_str(creg_config, year))
    assert expected_creg_year0_markdow == get_calendarmarkdown_str(creg_config, year)
