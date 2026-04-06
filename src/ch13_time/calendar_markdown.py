from copy import copy as copy_copy
from dataclasses import dataclass
from src.ch13_time.epoch_main import (
    EpochUnit,
    epochunit_shop,
    get_first_weekday_index_of_year,
)


def centered_to_len(length, x_str: str):
    return x_str[:length] if len(x_str) > length else x_str.center(length)


@dataclass
class MonthMarkDownUnit:
    label: str = None
    cumulative_days: str = None
    first_weekday: int = None
    week_length: int = None
    month_days_int: int = None
    monthday_index: int = None
    weekday_2char_abvs: list[str] = None
    max_monthday_rows: int = None
    year: int = None
    offset_year: bool = None

    def markdown_label(self) -> str:
        char_width = (self.week_length * 3) - 1
        if not self.offset_year:
            return centered_to_len(char_width, self.label)
        add1year = self.year + 1
        x_str = f"{self.label} ({add1year})"
        return centered_to_len(char_width, x_str)

    def markdown_weekdays(self) -> str:
        x_str = "".join(f"{abv} " for abv in self.weekday_2char_abvs)
        return x_str.rstrip()

    def markdown_day_numbers(self, row_int: int) -> str:
        starting_monthday = row_int * self.week_length
        starting_monthday = starting_monthday - self.first_weekday
        ending_monthday = starting_monthday + self.week_length
        x_str = ""
        for monthday in range(starting_monthday, ending_monthday):
            if monthday < 0 or monthday >= self.month_days_int:
                x_str += "   "
            else:
                display_monthday = monthday + self.monthday_index
                x_str += f"{display_monthday:2} "
        return x_str[:-1]

    def set_max_monthday_rows(self):
        row_int = 0
        while self.markdown_day_numbers(row_int).rstrip() != "":
            row_int += 1
        self.max_monthday_rows = row_int

    def get_next_month_first_weekday(self) -> int:
        right_days = self.month_days_int + self.first_weekday
        return right_days % self.week_length


@dataclass
class MonthMarkDownRow:
    months: list[MonthMarkDownUnit] = None
    max_monthday_numbers_row: int = None

    def set_max_monthday_numbers_row(self):
        x_max = 0
        for monthmarkdownunit in self.months:
            monthmarkdownunit.set_max_monthday_rows()
            if monthmarkdownunit.max_monthday_rows > x_max:
                x_max = monthmarkdownunit.max_monthday_rows
        self.max_monthday_numbers_row = x_max

    def markdown_str(self) -> str:
        x_str = "\n"
        for monthmarkdownunit in self.months:
            x_str += f"{monthmarkdownunit.markdown_label()}      "
        x_str = f"{x_str[:-6]}\n"
        for monthmarkdownunit in self.months:
            x_str += f"{monthmarkdownunit.markdown_weekdays()}      "
        x_str = f"{x_str[:-6]}\n"
        self.set_max_monthday_numbers_row()
        for row_int in range(self.max_monthday_numbers_row):
            for monthmarkdownunit in self.months:
                x_str += f"{monthmarkdownunit.markdown_day_numbers(row_int)}      "
            x_str = f"{x_str[:-6]}\n"
        return x_str[:-1]


@dataclass
class CalendarMarkDown:
    epoch_config: dict = None
    monthmarkdownrows: list[MonthMarkDownRow] = None
    epochunit: EpochUnit = None
    week_length: int = None
    monthmarkdownrow_length: int = None
    month_char_width: int = None
    max_md_width: int = 84  # default width
    display_md_width: int = None
    display_init_day: str = None
    yr1_jan1_offset_days: str = None

    def create_2char_weekday_list(self) -> list[str]:
        orig_weekdays = copy_copy(self.epochunit.weekdays_config)
        if self.display_init_day is None:
            self.display_init_day = list(self.epochunit.weekdays_config)[0]
        display_index = orig_weekdays.index(self.display_init_day)
        back_range = range(display_index, len(orig_weekdays))
        front_range = range(display_index)
        new_weekdays = [orig_weekdays[weekday_index] for weekday_index in back_range]
        new_weekdays.extend(orig_weekdays[wd_index] for wd_index in front_range)
        return [weekday[:2] for weekday in new_weekdays]

    def set_monthmarkdownrows(self, year_init_weekday: str, year: int):
        self.epochunit = epochunit_shop(self.epoch_config)
        self.week_length = len(self.epochunit.weekdays_config)
        # set the expected month_char_width with 5 extra charcters for space
        self.month_char_width = (self.week_length * 3) + 5
        self.monthmarkdownrow_length = int(self.max_md_width / self.month_char_width)
        # set the display_md_width to month_char_width * columns minus unnessary spaces on right
        # substract 6 spaces because length is 5 and each month number has additional space
        self.display_md_width = self.monthmarkdownrow_length * self.month_char_width - 6
        self.monthmarkdownrows = []
        x_monthmarkdownrow = MonthMarkDownRow([])
        previous_cumulative_days = 0
        x_monthday_index = self.epochunit.monthday_index
        self.yr1_jan1_offset_days = self.epochunit.yr1_jan1_offset / 1440
        x_weekday_2char_list = self.create_2char_weekday_list()
        year_init_2char = year_init_weekday[:2]
        month_first_weekday_index = x_weekday_2char_list.index(year_init_2char)

        for month_cumulative_list in self.epochunit.months_config:
            month_str = month_cumulative_list[0]
            cumulative_days = month_cumulative_list[1]
            new_monthmarkdownunit = MonthMarkDownUnit(month_str, cumulative_days)
            new_monthmarkdownunit.week_length = self.week_length
            new_monthmarkdownunit.month_days_int = (
                cumulative_days - previous_cumulative_days
            )
            new_monthmarkdownunit.monthday_index = x_monthday_index
            new_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_list

            new_monthmarkdownunit.first_weekday = month_first_weekday_index
            month_first_weekday_index = (
                new_monthmarkdownunit.get_next_month_first_weekday()
            )
            previous_cumulative_days = cumulative_days

            new_monthmarkdownunit.year = year
            if new_monthmarkdownunit.cumulative_days > self.yr1_jan1_offset_days:
                new_monthmarkdownunit.offset_year = True

            x_monthmarkdownrow.months.append(new_monthmarkdownunit)
            if len(x_monthmarkdownrow.months) == self.monthmarkdownrow_length:
                self.monthmarkdownrows.append(x_monthmarkdownrow)
                x_monthmarkdownrow = MonthMarkDownRow([])
        if len(x_monthmarkdownrow.months) > 0:
            self.monthmarkdownrows.append(x_monthmarkdownrow)
            x_monthmarkdownrow = MonthMarkDownRow([])

    def create_markdown(self, year: int) -> str:
        self.epochunit = epochunit_shop(self.epoch_config)
        self.week_length = len(self.epochunit.weekdays_config)
        first_weekday_index = get_first_weekday_index_of_year(self.week_length, year)
        first_weekday_str = self.epochunit.weekdays_config[first_weekday_index]
        self.set_monthmarkdownrows(first_weekday_str, year)
        markdown_str = f"""
{centered_to_len(self.display_md_width, f"Year {year}")}
"""
        for monthmarkdownrow in self.monthmarkdownrows:
            markdown_str += monthmarkdownrow.markdown_str()
            markdown_str += "\n"
        return markdown_str[:-1]


def get_calendarmarkdown_str(
    epoch_config: dict, year: int, display_init_day: str = None
) -> str:
    calendermarkdown = CalendarMarkDown(epoch_config, display_init_day=display_init_day)
    return calendermarkdown.create_markdown(year)
