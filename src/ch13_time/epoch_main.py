from dataclasses import dataclass
from datetime import datetime
from os import getcwd as os_getcwd
from src.ch00_py.dict_toolbox import get_1_if_None
from src.ch00_py.file_toolbox import create_path, open_json
from src.ch04_rope.rope import create_rope, get_first_label_from_rope
from src.ch06_plan.plan import (
    PlanUnit,
    all_plans_between,
    get_rangeunit_from_lineage_of_plans as calc_range,
    planunit_shop,
)
from src.ch07_person_logic.person_main import PersonUnit
from src.ch13_time._ref.ch13_semantic_types import (
    EpochLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    TimeNum,
)

DEFAULT_EPOCH_LENGTH = 1472657760


@dataclass
class C400Constants:
    day_length: int
    c400_leap_length: int
    c400_core_length: int
    c100_length: int
    yr4_leap_length: int
    yr4_core_length: int
    year_length: int


def get_c400_constants() -> C400Constants:
    c400_constants_path = create_path("src/ch13_time", "c400_constants.json")
    c400_dict = open_json(c400_constants_path)
    return C400Constants(
        day_length=c400_dict.get("day_length"),
        c400_leap_length=c400_dict.get("c400_leap_length"),
        c400_core_length=c400_dict.get("c400_core_length"),
        c100_length=c400_dict.get("c100_length"),
        yr4_leap_length=c400_dict.get("yr4_leap_length"),
        yr4_core_length=c400_dict.get("yr4_core_length"),
        year_length=c400_dict.get("year_length"),
    )


def day_length() -> int:
    return 1440


def stan_c400_leap_planunit() -> PlanUnit:
    x_denom = get_c400_constants().c400_leap_length
    return planunit_shop("c400_leap", denom=x_denom, morph=True)


def stan_c400_core_planunit() -> PlanUnit:
    x_denom = get_c400_constants().c400_core_length
    return planunit_shop("c400_core", denom=x_denom, morph=True)


def stan_c100_planunit() -> PlanUnit:
    x_denom = get_c400_constants().c100_length
    return planunit_shop("c100", denom=x_denom, morph=True)


def stan_yr4_leap_planunit() -> PlanUnit:
    x_denom = get_c400_constants().yr4_leap_length
    return planunit_shop("yr4_leap", denom=x_denom, morph=True)


def stan_yr4_core_planunit() -> PlanUnit:
    x_denom = get_c400_constants().yr4_core_length
    return planunit_shop("yr4_core", denom=x_denom, morph=True)


def stan_year_planunit() -> PlanUnit:
    x_denom = get_c400_constants().year_length
    return planunit_shop("year", denom=x_denom, morph=True)


def stan_day_planunit() -> PlanUnit:
    x_denom = get_c400_constants().day_length
    return planunit_shop("day", denom=x_denom, morph=True)


def stan_days_planunit() -> PlanUnit:
    x_denom = get_c400_constants().day_length
    return planunit_shop("days", denom=x_denom)


def week_length(x_int: int) -> int:
    """Return the length of a week in minutes."""
    return day_length() * x_int


def create_weekday_planunits(x_weekdays: list[str]) -> dict[str, PlanUnit]:
    x_dict = {}
    for x_weekday_num in range(len(x_weekdays)):
        x_plan = planunit_shop(
            x_weekdays[x_weekday_num],
            gogo_want=x_weekday_num * day_length(),
            stop_want=(x_weekday_num + 1) * day_length(),
        )
        x_dict[x_weekdays[x_weekday_num]] = x_plan
    return x_dict


def create_month_planunits(
    x_months_list: list[list[str, int]], monthday_index: int
) -> dict[str, PlanUnit]:
    x_dict = {}
    current_day = 0
    for x_month_list in x_months_list:
        x_month_str = x_month_list[0]
        x_month_days = x_month_list[1]
        x_gogo = current_day * day_length()
        x_stop = x_month_days * day_length()
        x_addin = monthday_index * day_length()
        x_plan = planunit_shop(
            x_month_str, gogo_want=x_gogo, stop_want=x_stop, addin=x_addin
        )
        x_dict[x_month_str] = x_plan
        current_day = x_month_days
    return x_dict


def create_hour_planunits(x_hours_list: list[str]) -> dict[str, PlanUnit]:
    x_dict = {}
    current_min = 0
    for x_hour_list in x_hours_list:
        x_hour_str = x_hour_list[0]
        x_stop = x_hour_list[1]
        x_plan = planunit_shop(x_hour_str, gogo_want=current_min, stop_want=x_stop)
        x_dict[x_hour_str] = x_plan
        current_min = x_stop
    return x_dict


def create_week_planunits(x_weekdays_list) -> dict[str, PlanUnit]:
    x_week_lenth = week_length(len(x_weekdays_list))
    week_str = "week"
    weeks_str = "weeks"
    return {
        week_str: planunit_shop(week_str, denom=x_week_lenth, morph=True),
        weeks_str: planunit_shop(weeks_str, denom=x_week_lenth),
    }


def new_epoch_planunit(epoch_label: EpochLabel, c400_number: int) -> PlanUnit:
    epoch_length = c400_number * get_c400_constants().c400_leap_length
    return planunit_shop(epoch_label, begin=0, close=epoch_length)


def get_epoch_rope(
    moment_rope: str, epoch_label: LabelTerm, knot: KnotTerm
) -> RopeTerm:
    time_rope = create_rope(moment_rope, "time", knot)
    return create_rope(time_rope, epoch_label, knot)


def get_epoch_length(epoch_config: dict) -> int:
    c400_number = epoch_config.get("c400_number")
    return c400_number * get_c400_constants().c400_leap_length


def epoch_config_path() -> str:
    "Returns path: src/ch13_time/epoch_configs/default_epoch_config.json"

    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch13_time")
    epoch_configs_dir = create_path(chapter_dir, "epoch_configs")
    return create_path(epoch_configs_dir, "default_epoch_config.json")


def get_default_epoch_config_dict() -> dict:
    return open_json(epoch_config_path())


def add_epoch_planunit(x_personunit: PersonUnit, epoch_config: dict = None):
    """Add epoch plan to PersonUnit from epoch_config. epoch_config defaults to creg epoch_config"""
    if epoch_config is None:
        epoch_config = get_default_epoch_config_dict()

    x_plan_label = epoch_config.get("epoch_label")
    x_c400_number = epoch_config.get("c400_number")
    x_months = epoch_config.get("months_config")
    x_mday = epoch_config.get("monthday_index")
    x_hours_list = epoch_config.get("hours_config")
    x_weekdays_list = epoch_config.get("weekdays_config")
    x_yr1_jan1_offset = epoch_config.get("yr1_jan1_offset")

    planroot_label = get_first_label_from_rope(
        rope=x_personunit.planroot.get_plan_rope(), knot=x_personunit.knot
    )
    epoch_rope = get_epoch_rope(
        moment_rope=planroot_label,
        epoch_label=x_plan_label,
        knot=x_personunit.knot,
    )
    day_rope = x_personunit.make_rope(epoch_rope, "day")
    week_rope = x_personunit.make_rope(epoch_rope, "week")
    year_rope = get_year_rope(x_personunit, x_plan_label)

    add_stan_planunits(x_personunit, x_plan_label, x_c400_number)
    add_planunits(x_personunit, day_rope, create_hour_planunits(x_hours_list))
    add_planunits(x_personunit, epoch_rope, create_week_planunits(x_weekdays_list))
    add_planunits(x_personunit, week_rope, create_weekday_planunits(x_weekdays_list))
    add_planunits(x_personunit, year_rope, create_month_planunits(x_months, x_mday))
    offset_plan = planunit_shop("yr1_jan1_offset", addin=x_yr1_jan1_offset)
    x_personunit.set_plan_obj(offset_plan, epoch_rope)
    time_rope = x_personunit.make_l1_rope("time")
    x_personunit.edit_plan_attr(time_rope, star=0)


def add_planunits(
    x_personunit: PersonUnit,
    parent_rope: RopeTerm,
    config_dict: dict[str, PlanUnit],
):
    for x_time_planunit in config_dict.values():
        x_personunit.set_plan_obj(x_time_planunit, parent_rope)


def add_stan_planunits(
    x_personunit: PersonUnit,
    epoch_label: EpochLabel,
    epoch_c400_number: int,
):
    time_rope = x_personunit.make_l1_rope("time")
    planroot_label = get_first_label_from_rope(
        rope=x_personunit.planroot.get_plan_rope(), knot=x_personunit.knot
    )
    epoch_rope = get_epoch_rope(
        moment_rope=planroot_label,
        epoch_label=epoch_label,
        knot=x_personunit.knot,
    )
    c400_leap_rope = x_personunit.make_rope(epoch_rope, "c400_leap")
    c400_core_rope = x_personunit.make_rope(c400_leap_rope, "c400_core")
    c100_rope = x_personunit.make_rope(c400_core_rope, "c100")
    yr4_leap_rope = x_personunit.make_rope(c100_rope, "yr4_leap")
    yr4_core_rope = x_personunit.make_rope(yr4_leap_rope, "yr4_core")

    if not x_personunit.plan_exists(time_rope):
        x_personunit.set_l1_plan(planunit_shop("time"))
    epoch_planunit = new_epoch_planunit(epoch_label, epoch_c400_number)
    x_personunit.set_plan_obj(epoch_planunit, time_rope)
    x_personunit.set_plan_obj(stan_c400_leap_planunit(), epoch_rope)
    x_personunit.set_plan_obj(stan_c400_core_planunit(), c400_leap_rope)
    x_personunit.set_plan_obj(stan_c100_planunit(), c400_core_rope)
    x_personunit.set_plan_obj(stan_yr4_leap_planunit(), c100_rope)
    x_personunit.set_plan_obj(stan_yr4_core_planunit(), yr4_leap_rope)
    x_personunit.set_plan_obj(stan_year_planunit(), yr4_core_rope)
    x_personunit.set_plan_obj(stan_day_planunit(), epoch_rope)
    x_personunit.set_plan_obj(stan_days_planunit(), epoch_rope)


def get_c400_core_rope(x_personunit: PersonUnit, epoch_label: LabelTerm) -> RopeTerm:
    root_plan_rope = x_personunit.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(root_plan_rope, epoch_label, x_personunit.knot)
    c400_leap_rope = x_personunit.make_rope(epoch_rope, "c400_leap")
    return x_personunit.make_rope(c400_leap_rope, "c400_core")


def get_c100_rope(x_personunit: PersonUnit, epoch_label: LabelTerm) -> RopeTerm:
    c400_core_rope = get_c400_core_rope(x_personunit, epoch_label)
    return x_personunit.make_rope(c400_core_rope, "c100")


def get_yr4_core_rope(x_personunit: PersonUnit, epoch_label: LabelTerm) -> RopeTerm:
    c100_rope = get_c100_rope(x_personunit, epoch_label)
    yr4_leap_rope = x_personunit.make_rope(c100_rope, "yr4_leap")
    return x_personunit.make_rope(yr4_leap_rope, "yr4_core")


def get_year_rope(x_personunit: PersonUnit, epoch_label: LabelTerm) -> RopeTerm:
    yr4_core_rope = get_yr4_core_rope(x_personunit, epoch_label)
    return x_personunit.make_rope(yr4_core_rope, "year")


def get_week_rope(x_personunit: PersonUnit, epoch_label: LabelTerm) -> RopeTerm:
    root_plan_rope = x_personunit.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(root_plan_rope, epoch_label, x_personunit.knot)
    return x_personunit.make_rope(epoch_rope, "week")


def get_day_rope(x_personunit: PersonUnit, epoch_label: LabelTerm) -> RopeTerm:
    root_plan_rope = x_personunit.planroot.get_plan_rope()
    epoch_rope = get_epoch_rope(root_plan_rope, epoch_label, x_personunit.knot)
    return x_personunit.make_rope(epoch_rope, "day")


def validate_epoch_config(config_dict: dict) -> bool:
    config_elements = [
        "hours_config",
        "weekdays_config",
        "months_config",
        "monthday_index",
        "epoch_label",
        "c400_number",
        "yr1_jan1_offset",
    ]
    for config_key in config_elements:
        config_element = config_dict.get(config_key)
        len_elements = {"hours_config", "weekdays_config", "months_config"}
        if config_element is None:
            return False
        elif config_key in len_elements and len(config_element) == 0:
            return False
        elif config_key in "weekdays_config":
            if _duplicate_exists(config_element):
                return False
        elif config_key in {"months_config", "hours_config"}:
            str_list = [x_config[0] for x_config in config_element]
            if _duplicate_exists(str_list):
                return False
    return True


def _duplicate_exists(config_element: list) -> bool:
    return len(config_element) != len(set(config_element))


def get_default_hours_config() -> list[list[str, int]]:
    return [
        ["12am", 60],
        ["1am", 120],
        ["2am", 180],
        ["3am", 240],
        ["4am", 300],
        ["5am", 360],
        ["6am", 420],
        ["7am", 480],
        ["8am", 540],
        ["9am", 600],
        ["10am", 660],
        ["11am", 720],
        ["12pm", 780],
        ["1pm", 840],
        ["2pm", 900],
        ["3pm", 960],
        ["4pm", 1020],
        ["5pm", 1080],
        ["6pm", 1140],
        ["7pm", 1200],
        ["8pm", 1260],
        ["9pm", 1320],
        ["10pm", 1380],
        ["11pm", 1440],
    ]


def get_default_months_config() -> list[list[str, int]]:
    return [
        ["March", 31],
        ["April", 61],
        ["May", 92],
        ["June", 122],
        ["July", 153],
        ["August", 184],
        ["September", 214],
        ["October", 245],
        ["November", 275],
        ["December", 306],
        ["January", 337],
        ["February", 365],
    ]


def get_default_weekdays_config() -> list[list[str, int]]:
    return [
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
    ]


def epoch_config_shop(
    epoch_label: EpochLabel = None,
    c400_number: int = None,
    hour_length: int = None,
    month_length: int = None,
    weekday_list: list[str] = None,
    months_list: list[str] = None,
    monthday_index: int = None,
    yr1_jan1_offset: int = None,
) -> dict:
    if epoch_label is None:
        epoch_label = "creg"
    if c400_number is None:
        c400_number = 7
    if yr1_jan1_offset is None:
        yr1_jan1_offset = 440640

    if hour_length:
        hours_count = round(1440 / hour_length)
        hours_range = range(hours_count)
        hour_config = [_hour_config(x, hours_count, hour_length) for x in hours_range]
    else:
        hour_config = get_default_hours_config()
    if not weekday_list:
        weekday_list = get_default_weekdays_config()
    if months_list:
        months_range = range(len(months_list))
        month_config = [
            _month_config(x, months_list, month_length) for x in months_range
        ]
    else:
        month_config = get_default_months_config()
    return {
        "hours_config": hour_config,
        "weekdays_config": weekday_list,
        "months_config": month_config,
        "epoch_label": epoch_label,
        "c400_number": c400_number,
        "monthday_index": get_1_if_None(monthday_index),
        "yr1_jan1_offset": yr1_jan1_offset,
    }


def _month_config(month_num, months_list, month_length) -> list[str, int]:
    stop_minute = (month_num + 1) * month_length
    is_last_month = month_num == len(months_list) - 1
    return [months_list[month_num], (365 if is_last_month else stop_minute)]


def _hour_config(hour_num, hours_count, hour_length) -> list[str, int]:
    hour_str = f"{hour_num}hr"
    hour_stop = 1440 if hour_num == hours_count - 1 else (hour_num + 1) * hour_length
    return [hour_str, hour_stop]


def get_min_from_dt_offset(dt: datetime, yr1_jan1_offset: int) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    difference_min_dt = dt - ce_src
    return round(difference_min_dt.total_seconds() / 60) + yr1_jan1_offset


def get_epoch_min_from_dt(
    x_person: PersonUnit, epoch_label: LabelTerm, x_datetime: datetime
) -> int:
    time_rope = x_person.make_l1_rope("time")
    epoch_rope = x_person.make_rope(time_rope, epoch_label)
    offset_rope = x_person.make_rope(epoch_rope, "yr1_jan1_offset")
    offset_plan = x_person.get_plan_obj(offset_rope)
    offset_addin = offset_plan.addin
    return get_min_from_dt_offset(x_datetime, offset_addin)


def get_epoch_min_difference(epoch_config0: dict, epoch_config1: dict) -> int:
    offset_x0 = epoch_config0.get("yr1_jan1_offset")
    offset_x1 = epoch_config1.get("yr1_jan1_offset")
    return offset_x0 - offset_x1


@dataclass
class EpochHolder:
    """Given person, epoch_rope, and TimeNum, returns time technology attrs
    _c400_number: count of 400 year cycles
    _c100_count: count of 100 year cycles after _c400_number years removed
    _hour
    _minute
    _monthday
    _month
    _yr4_count: 4 year cycles after _c100_count, _c100 years removed
    _year_count:  1 year after _c100_count, _c100_count, _yr4_count years removed
    _year_num: calculated year from c400, c100, yr4, year_count
    _weekday
    _epoch_plan PlanUnit
    readable time blurb from PersonUnit, epoch_label, and minute integer."""

    x_personunit: PersonUnit = None
    epoch_label: LabelTerm = None
    x_min: TimeNum = None
    # calculated fields
    _epoch_plan: PlanUnit = None
    _weekday: str = None
    _monthday: str = None
    _month: str = None
    _hour: str = None
    _minute: str = None
    _c400_number: str = None
    _c100_count: str = None
    _yr4_count: str = None
    _year_count: str = None
    _year_num: str = None

    def _set_epoch_plan(self):
        epoch_rope = get_epoch_rope(
            self.x_personunit.planroot.plan_label,
            self.epoch_label,
            self.x_personunit.knot,
        )
        self._epoch_plan = self.x_personunit.get_plan_obj(epoch_rope)

    def _set_weekday(self):
        week_rope = get_week_rope(self.x_personunit, self.epoch_label)
        week_plan = self.x_personunit.get_plan_obj(week_rope)
        x_plan_list = [self._epoch_plan, week_plan]
        reason_lower_rangeunit = calc_range(x_plan_list, self.x_min, self.x_min)
        reason_lower_weekday_dict = week_plan.get_kids_in_range(
            reason_lower_rangeunit.gogo
        )
        for x_weekday in reason_lower_weekday_dict.keys():
            self._weekday = x_weekday

    def _set_month(self):
        year_rope = get_year_rope(self.x_personunit, self.epoch_label)
        year_plan = self.x_personunit.get_plan_obj(year_rope)
        moment_rope = self.x_personunit.planroot.plan_label
        x_knot = self.x_personunit.knot
        epoch_rope = get_epoch_rope(moment_rope, self.epoch_label, x_knot)
        x_plan_dict = self.x_personunit._plan_dict
        plan_list = all_plans_between(x_plan_dict, epoch_rope, year_rope, x_knot)
        reason_lower_rangeunit = calc_range(plan_list, self.x_min, self.x_min)
        gogo_month_dict = year_plan.get_kids_in_range(reason_lower_rangeunit.gogo)
        month_plan = None
        for x_monthname, month_plan in gogo_month_dict.items():
            self._month = x_monthname
            month_plan = month_plan

        self._monthday = (
            reason_lower_rangeunit.gogo - month_plan.gogo_calc + month_plan.addin
        )
        self._monthday = self._monthday // 1440

    def _set_hour(self):
        day_rope = get_day_rope(self.x_personunit, self.epoch_label)
        day_plan = self.x_personunit.get_plan_obj(day_rope)
        x_plan_list = [self._epoch_plan, day_plan]
        rangeunit = calc_range(x_plan_list, self.x_min, self.x_min)
        hour_dict = day_plan.get_kids_in_range(rangeunit.gogo)
        for x_hour, hour_plan in hour_dict.items():
            self._hour = x_hour
            hour_plan = hour_plan

        self._minute = rangeunit.gogo - hour_plan.gogo_calc

    def _set_year(self):
        c400_constants = get_c400_constants()
        x_time_rope = self.x_personunit.make_l1_rope("time")
        x_plan_dict = self.x_personunit._plan_dict
        # count 400 year blocks
        self._c400_number = self.x_min // c400_constants.c400_leap_length

        # count 100 year blocks
        c400_core_rope = get_c400_core_rope(self.x_personunit, self.epoch_label)
        c400_core_plan_list = all_plans_between(
            x_plan_dict, x_time_rope, c400_core_rope, knot=self.x_personunit.knot
        )
        c400_core_range = calc_range(c400_core_plan_list, self.x_min, self.x_min)
        self._c100_count = c400_core_range.gogo // c400_constants.c100_length
        # count 4 year blocks
        c100_rope = get_c100_rope(self.x_personunit, self.epoch_label)
        c100_plan_list = all_plans_between(
            x_plan_dict, x_time_rope, c100_rope, knot=self.x_personunit.knot
        )
        c100_range = calc_range(c100_plan_list, self.x_min, self.x_min)
        self._yr4_count = c100_range.gogo // c400_constants.yr4_leap_length

        # count 1 year blocks
        yr4_core_rope = get_yr4_core_rope(self.x_personunit, self.epoch_label)
        yr4_core_plans = all_plans_between(
            x_plan_dict, x_time_rope, yr4_core_rope, knot=self.x_personunit.knot
        )
        yr4_core_range = calc_range(yr4_core_plans, self.x_min, self.x_min)
        self._year_count = yr4_core_range.gogo // c400_constants.year_length

        self._year_num = self._c400_number * 400
        self._year_num += self._c100_count * 100
        self._year_num += self._yr4_count * 4
        self._year_num += self._year_count

    def calc_epoch(self):
        self.x_personunit.conpute()
        self._set_epoch_plan()
        self._set_weekday()
        self._set_month()
        self._set_hour()
        self._set_year()

    def get_blurb(self) -> str:
        x_str = f"{self._hour}"
        x_str += f":{self._minute}"
        x_str += f", {self._weekday}"
        x_str += f", {self._monthday}"
        x_str += f" {self._month}"
        x_str += f", {self._year_num}"
        return x_str


def epochholder_shop(x_personunit: PersonUnit, epoch_label: LabelTerm, x_min: int):
    return EpochHolder(x_personunit, epoch_label, x_min=x_min)


@dataclass
class EpochUnit:
    c400_number: int = None
    hours_config: list[list[str, int]] = None
    months_config: list[list[str, int]] = None
    monthday_index: int = None
    epoch_label: EpochLabel = None
    weekdays_config: list[str] = None
    yr1_jan1_offset: int = None

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        return {
            "c400_number": self.c400_number,
            "hours_config": self.hours_config,
            "months_config": self.months_config,
            "monthday_index": self.monthday_index,
            "epoch_label": self.epoch_label,
            "weekdays_config": self.weekdays_config,
            "yr1_jan1_offset": self.yr1_jan1_offset,
        }


def epochunit_shop(epoch_config: dict = None) -> EpochUnit:
    default_epoch = get_default_epoch_config_dict()
    if not epoch_config:
        epoch_config = default_epoch
    if epoch_config.get("epoch_label") is None:
        epoch_config["epoch_label"] = default_epoch.get("epoch_label")
    if epoch_config.get("c400_number") is None:
        epoch_config["c400_number"] = default_epoch.get("c400_number")
    if epoch_config.get("monthday_index") is None:
        x_monthday_index = default_epoch.get("monthday_index")
        epoch_config["monthday_index"] = x_monthday_index
    if epoch_config.get("hours_config") is None:
        epoch_config["hours_config"] = default_epoch.get("hours_config")
    if epoch_config.get("months_config") is None:
        epoch_config["months_config"] = default_epoch.get("months_config")
    if epoch_config.get("weekdays_config") is None:
        epoch_config["weekdays_config"] = default_epoch.get("weekdays_config")
    if epoch_config.get("yr1_jan1_offset") is None:
        epoch_config["yr1_jan1_offset"] = default_epoch.get("yr1_jan1_offset")
    return EpochUnit(
        c400_number=epoch_config.get("c400_number"),
        hours_config=epoch_config.get("hours_config"),
        months_config=epoch_config.get("months_config"),
        monthday_index=epoch_config.get("monthday_index"),
        epoch_label=epoch_config.get("epoch_label"),
        weekdays_config=epoch_config.get("weekdays_config"),
        yr1_jan1_offset=epoch_config.get("yr1_jan1_offset"),
    )


def get_first_weekday_index_of_year(week_length, year: int) -> int:
    # Count leap years between year 0 and year N - 1
    leaps = (year // 4) - (year // 100) + (year // 400)
    total_days = (year - leaps) * 365 + leaps * 366
    return total_days % week_length
