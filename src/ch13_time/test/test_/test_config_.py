from copy import deepcopy as copy_deepcopy
from inspect import getdoc as inspect_getdoc
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time._ref.ch13_semantic_types import EpochLabel
from src.ch13_time.epoch_config import (
    get_creg_config,
    get_custom_epoch_config,
    get_squirt_config,
)
from src.ch13_time.epoch_main import (
    DEFAULT_EPOCH_LENGTH,
    C400Constants,
    EpochUnit,
    day_length,
    epoch_config_shop,
    epochunit_shop,
    get_c400_constants,
    get_day_rope,
    get_default_epoch_config_dict,
    get_epoch_length,
    get_epoch_rope,
    get_week_rope,
    get_year_rope,
    validate_epoch_config,
)
from src.ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_EpochLabel_Exists():
    # ESTABLISH
    empty_str = ""
    # WHEN
    x_epochlabel = EpochLabel(empty_str)
    # THEN
    assert x_epochlabel == empty_str
    doc_str = f"{kw.EpochLabel} is required for every EpochUnit. It is a LabelTerm that must not contain the {kw.knot}."
    assert inspect_getdoc(x_epochlabel) == doc_str


def test_get_epoch_rope_ReturnsObj_Scenario0_default_knot():
    # ESTABLISH
    fay_moment_rope = "Fay"
    bob_epoch_label = "Bob_time3"
    default_knot = default_knot_if_None()

    # WHEN
    bob_rope = get_epoch_rope(fay_moment_rope, bob_epoch_label, default_knot)

    # THEN
    assert bob_rope
    time_rope = create_rope(fay_moment_rope, "time")
    expected_bob_rope = create_rope(time_rope, bob_epoch_label)
    assert bob_rope == expected_bob_rope


def test_get_epoch_rope_ReturnsObj_Scenario1_slash_knot():
    # ESTABLISH
    fay_moment_rope = "Fay"
    bob_epoch_label = "Bob_time3"
    slash_knot = "/"
    assert slash_knot != default_knot_if_None()

    # WHEN
    bob_rope = get_epoch_rope(fay_moment_rope, bob_epoch_label, slash_knot)

    # THEN
    assert bob_rope
    time_rope = create_rope(fay_moment_rope, "time", slash_knot)
    expected_bob_rope = create_rope(time_rope, bob_epoch_label, slash_knot)
    assert bob_rope == expected_bob_rope


def test_C400Constants_Exists():
    # ESTABLISH / WHEN
    x_c400_constants = C400Constants("x1", "x2", "x3", "x4", "x5", "x6", "x7")

    # THEN
    assert x_c400_constants.day_length == "x1"
    assert x_c400_constants.c400_leap_length == "x2"
    assert x_c400_constants.c400_core_length == "x3"
    assert x_c400_constants.c100_length == "x4"
    assert x_c400_constants.yr4_leap_length == "x5"
    assert x_c400_constants.yr4_core_length == "x6"
    assert x_c400_constants.year_length == "x7"


def test_get_c400_constants_ReturnsObj():
    # ESTABLISH / WHEN
    x_c400_constants = get_c400_constants()

    # THEN
    assert x_c400_constants.day_length == 1440
    assert x_c400_constants.c400_leap_length == 210379680
    assert x_c400_constants.c400_core_length == 210378240
    assert x_c400_constants.c100_length == 52594560
    assert x_c400_constants.yr4_leap_length == 2103840
    assert x_c400_constants.yr4_core_length == 2102400
    assert x_c400_constants.year_length == 525600


def test_day_length_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert day_length() == get_c400_constants().day_length
    assert day_length() == 1440


def test_validate_epoch_config_ReturnsObj_CheckEachElementIsNecessary():
    # ESTABLISH / WHEN / THEN
    assert not validate_epoch_config({})

    # ESTABLISH / WHEN / THEN
    orig_creg_config = get_creg_config()
    x_squirt_config = get_squirt_config()
    assert validate_epoch_config(orig_creg_config)
    assert validate_epoch_config(x_squirt_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    assert validate_epoch_config(creg_config)
    creg_config.pop(kw.hours_config)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(kw.weekdays_config)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(kw.months_config)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(kw.monthday_index)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(kw.epoch_label)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(kw.c400_number)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config.pop(kw.yr1_jan1_offset)
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.hours_config] = []
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.months_config] = []
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.weekdays_config] = []
    assert not validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.yr1_jan1_offset] = None
    assert not validate_epoch_config(creg_config)
    creg_config[kw.yr1_jan1_offset] = 0
    assert validate_epoch_config(creg_config)


def test_get_default_epoch_config_dict_IsValid():
    # ESTABLISH / WHEN
    default_config = get_default_epoch_config_dict()
    # THEN
    assert validate_epoch_config(default_config)


def test_DEFAULT_EPOCH_LENGTH_ReturnsObj():
    # ESTABLISH
    default_epoch_config = get_default_epoch_config_dict()
    default_c400_number = default_epoch_config.get(kw.c400_number)
    c400_length_constant = get_c400_constants().c400_leap_length
    expected_epoch_length = default_c400_number * c400_length_constant

    # WHEN / THEN
    assert DEFAULT_EPOCH_LENGTH == expected_epoch_length


def test_get_epoch_length_ReturnsObj():
    # ESTABLISH
    default_epoch_config = get_default_epoch_config_dict()

    # WHEN
    gen_epoch_length = get_epoch_length(default_epoch_config)

    # THEN
    default_c400_number = default_epoch_config.get(kw.c400_number)
    c400_length_constant = get_c400_constants().c400_leap_length
    expected_epoch_length = default_c400_number * c400_length_constant
    assert gen_epoch_length == expected_epoch_length
    assert gen_epoch_length == DEFAULT_EPOCH_LENGTH


def test_is_epoch_config_valid_ReturnsObj_CheckObjsRepeat():
    # ESTABLISH / WHEN / THEN
    orig_creg_config = get_creg_config()
    assert validate_epoch_config(orig_creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.months_config] = [["x_str", 30], ["y_str", 180], ["x_str", 365]]
    assert not validate_epoch_config(creg_config)
    creg_config[kw.months_config] = [["x_str", 30], ["y_str", 180], ["z_str", 365]]
    assert validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.hours_config] = [["x_str", 30], ["y_str", 180], ["x_str", 1440]]
    assert not validate_epoch_config(creg_config)
    creg_config[kw.hours_config] = [["x_str", 30], ["y_str", 180], ["z_str", 1440]]
    assert validate_epoch_config(creg_config)

    # ESTABLISH / WHEN / THEN
    creg_config = copy_deepcopy(orig_creg_config)
    creg_config[kw.weekdays_config] = ["x_str", "y_str", "x_str"]
    assert not validate_epoch_config(creg_config)
    creg_config[kw.weekdays_config] = ["x_str", "y_str", "z_str"]
    assert validate_epoch_config(creg_config)


def test_epoch_config_shop_ReturnsObj_AllParameters():
    # ESTABLISH
    five_c400_number = 25
    five_yr1_jan1_offset = 1683037440 + 440640  # 3200 years + JanLen + FebLen
    five_hour_length = 144
    five_month_length = 25
    five_weekday_list = [kw.Anaday, kw.Baileyday, kw.Chiday, kw.Danceday, kw.Eastday]
    # months = ["B", "C", "E", "G", "H", "I", "K", "L", "N", "P", "Q", "R", "T", "U", "W"]
    # c_mons = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    five_months_list = [
        "Fredrick",
        "Geo",
        "Holocene",
        "Iguana",
        "Jesus",
        "Keel",
        "LeBron",
        "Mikayla",
        "Ninon",
        "Obama",
        "Preston",
        "Quorum",
        "RioGrande",
        "Simon",
        "Trump",
    ]
    assert len(five_months_list) == 15
    calc_months_day_length = (len(five_months_list) - 1) * five_month_length
    assert calc_months_day_length == 350
    print(f"{len(five_months_list)=} {calc_months_day_length=}")

    # WHEN
    five_dict = epoch_config_shop(
        epoch_label=kw.five,
        c400_number=five_c400_number,
        hour_length=five_hour_length,
        month_length=five_month_length,
        weekday_list=five_weekday_list,
        months_list=five_months_list,
        yr1_jan1_offset=five_yr1_jan1_offset,
        monthday_index=0,
    )

    # THEN
    assert validate_epoch_config(five_dict)
    assert five_dict.get(kw.epoch_label) == kw.five
    assert five_dict.get(kw.c400_number) == five_c400_number
    assert five_dict.get(kw.weekdays_config) == five_weekday_list
    x_months_config = five_dict.get(kw.months_config)
    gen_months = [mon_config[0] for mon_config in x_months_config]
    assert gen_months == five_months_list
    assert x_months_config[0][0] == "Fredrick"
    assert x_months_config[0][1] == 25
    assert x_months_config[6][0] == "LeBron"
    assert x_months_config[6][1] == 175
    assert x_months_config[13][0] == "Simon"
    assert x_months_config[13][1] == 350
    assert x_months_config[14][0] == "Trump"
    assert x_months_config[14][1] == 365
    x_hours_config = five_dict.get(kw.hours_config)
    assert len(x_hours_config) == 10
    assert x_hours_config[0] == ["0hr", 144]
    assert x_hours_config[4] == ["4hr", 720]
    assert five_dict.get(kw.yr1_jan1_offset) == five_yr1_jan1_offset

    # five_filename = f"epoch_config_{kw.five}.json"
    expected_config = get_custom_epoch_config(kw.five)
    assert validate_epoch_config(expected_config)
    assert expected_config.get(kw.hours_config) == x_hours_config
    assert expected_config == five_dict


def test_epoch_config_shop_ReturnsObj_NoParameters():
    # ESTABLISH
    h_c400_number = 7
    h_hours_config = [
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
    h_months_config = [
        [exx.March, 31],
        [exx.April, 61],
        [exx.May, 92],
        [exx.June, 122],
        [exx.July, 153],
        [exx.August, 184],
        [exx.September, 214],
        [exx.October, 245],
        [exx.November, 275],
        [exx.December, 306],
        [exx.January, 337],
        [exx.February, 365],
    ]
    h_monthday_index = 1
    h_epoch_label = "creg"
    h_weekdays_config = [
        exx.Wednesday,
        exx.Thursday,
        exx.Friday,
        exx.Saturday,
        exx.Sunday,
        exx.Monday,
        exx.Tuesday,
    ]
    h_yr1_jan1_offset = 440640

    # WHEN
    generated_dict = epoch_config_shop()

    # THEN
    print(f"{generated_dict=}")
    print(f"{set(generated_dict.keys())=}")
    print(f"{kw.epoch_label=}")
    print(f"{generated_dict.get(kw.epoch_label)=}")
    assert generated_dict.get(kw.c400_number) == h_c400_number

    assert generated_dict.get(kw.epoch_label) == h_epoch_label
    assert generated_dict.get(kw.c400_number) == h_c400_number
    assert generated_dict.get(kw.hours_config) == h_hours_config
    assert generated_dict.get(kw.months_config) == h_months_config
    assert generated_dict.get(kw.monthday_index) == h_monthday_index
    assert generated_dict.get(kw.epoch_label) == h_epoch_label
    assert generated_dict.get(kw.weekdays_config) == h_weekdays_config
    assert generated_dict.get(kw.yr1_jan1_offset) == h_yr1_jan1_offset
    assert validate_epoch_config(generated_dict)


def test_get_year_rope_ReturnsObj():
    # ESTABLISH
    epoch_fay_str = "Fay34"
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    fay_rope = sue_personunit.make_rope(time_rope, epoch_fay_str)
    c400_leap_rope = sue_personunit.make_rope(fay_rope, kw.c400_leap)
    c400_core_rope = sue_personunit.make_rope(c400_leap_rope, kw.c400_core)
    c100_rope = sue_personunit.make_rope(c400_core_rope, kw.c100)
    yr4_leap_rope = sue_personunit.make_rope(c100_rope, kw.yr4_leap)
    yr4_core_rope = sue_personunit.make_rope(yr4_leap_rope, kw.yr4_core)
    year_rope = sue_personunit.make_rope(yr4_core_rope, kw.year)

    # WHEN / THEN
    assert year_rope == get_year_rope(sue_personunit, epoch_fay_str)


def test_get_week_rope_ReturnsObj():
    # ESTABLISH
    epoch_fay_str = "Fay34"
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    fay_rope = sue_personunit.make_rope(time_rope, epoch_fay_str)
    week_rope = sue_personunit.make_rope(fay_rope, kw.week)

    # WHEN / THEN
    assert week_rope == get_week_rope(sue_personunit, epoch_fay_str)


def test_get_day_rope_ReturnsObj():
    # ESTABLISH
    epoch_fay_str = "Fay34"
    sue_personunit = personunit_shop("Sue")
    time_rope = sue_personunit.make_l1_rope(kw.time)
    fay_rope = sue_personunit.make_rope(time_rope, epoch_fay_str)
    day_rope = sue_personunit.make_rope(fay_rope, kw.day)

    # WHEN / THEN
    assert day_rope == get_day_rope(sue_personunit, epoch_fay_str)


def test_EpochUnit_Exists():
    # ESTABLISH / WHEN
    x_epochunit = EpochUnit()

    # THEN
    assert x_epochunit
    assert not x_epochunit.c400_number
    assert not x_epochunit.hours_config
    assert not x_epochunit.months_config
    assert not x_epochunit.monthday_index
    assert not x_epochunit.epoch_label
    assert not x_epochunit.weekdays_config
    assert not x_epochunit.yr1_jan1_offset


def test_epochunit_shop_ReturnsObj_Scenario0_Default():
    # ESTABLISH
    creg_config = get_creg_config()

    # WHEN
    x_epochunit = epochunit_shop()

    # THEN
    creg_c400_number = creg_config.get(kw.c400_number)
    creg_hours_config = creg_config.get(kw.hours_config)
    creg_months_config = creg_config.get(kw.months_config)
    creg_epoch_label = creg_config.get(kw.epoch_label)
    creg_weekdays_config = creg_config.get(kw.weekdays_config)
    creg_monthday_index = creg_config.get(kw.monthday_index)
    creg_yr1_jan1_offset = creg_config.get(kw.yr1_jan1_offset)

    assert x_epochunit
    assert x_epochunit.c400_number == creg_c400_number
    assert x_epochunit.hours_config == creg_hours_config
    assert x_epochunit.months_config == creg_months_config
    assert x_epochunit.monthday_index == creg_monthday_index
    assert x_epochunit.epoch_label == creg_epoch_label
    assert x_epochunit.weekdays_config == creg_weekdays_config
    assert x_epochunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_epochunit_shop_ReturnsObj_Scenario1_WhenEpochUnitAttributesAreNone():
    # ESTABLISH
    incomplete_creg_config = get_creg_config()
    incomplete_creg_config.pop(kw.c400_number)
    incomplete_creg_config.pop(kw.hours_config)
    incomplete_creg_config.pop(kw.months_config)
    incomplete_creg_config.pop(kw.monthday_index)
    incomplete_creg_config.pop(kw.weekdays_config)
    incomplete_creg_config.pop(kw.yr1_jan1_offset)
    assert incomplete_creg_config

    # WHEN
    x_epochunit = epochunit_shop(incomplete_creg_config)

    # THEN
    creg_config = get_creg_config()
    creg_c400_number = creg_config.get(kw.c400_number)
    creg_hours_config = creg_config.get(kw.hours_config)
    creg_months_config = creg_config.get(kw.months_config)
    creg_epoch_label = creg_config.get(kw.epoch_label)
    creg_weekdays_config = creg_config.get(kw.weekdays_config)
    creg_monthday_index = creg_config.get(kw.monthday_index)
    creg_yr1_jan1_offset = creg_config.get(kw.yr1_jan1_offset)

    assert x_epochunit
    assert x_epochunit.c400_number == creg_c400_number
    assert x_epochunit.hours_config == creg_hours_config
    assert x_epochunit.months_config == creg_months_config
    assert x_epochunit.monthday_index == creg_monthday_index
    assert x_epochunit.epoch_label == creg_epoch_label
    assert x_epochunit.weekdays_config == creg_weekdays_config
    assert x_epochunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_epochunit_shop_ReturnsObj_Scenario2_epoch_label_Missing():
    # ESTABLISH
    incomplete_creg_config = get_creg_config()
    incomplete_creg_config.pop(kw.epoch_label)
    incomplete_creg_config.pop(kw.hours_config)
    assert incomplete_creg_config

    # WHEN
    x_epochunit = epochunit_shop(incomplete_creg_config)

    # THEN
    creg_config = get_creg_config()
    creg_c400_number = creg_config.get(kw.c400_number)
    creg_hours_config = creg_config.get(kw.hours_config)
    creg_months_config = creg_config.get(kw.months_config)
    creg_epoch_label = creg_config.get(kw.epoch_label)
    creg_weekdays_config = creg_config.get(kw.weekdays_config)
    creg_monthday_index = creg_config.get(kw.monthday_index)
    creg_yr1_jan1_offset = creg_config.get(kw.yr1_jan1_offset)

    assert x_epochunit
    assert x_epochunit.c400_number == creg_c400_number
    assert x_epochunit.hours_config == creg_hours_config
    assert x_epochunit.months_config == creg_months_config
    assert x_epochunit.monthday_index == creg_monthday_index
    assert x_epochunit.epoch_label == creg_epoch_label
    assert x_epochunit.weekdays_config == creg_weekdays_config
    assert x_epochunit.yr1_jan1_offset == creg_yr1_jan1_offset


def test_EpochUnit_to_dict_ReturnsObj():
    # ESTABLISH
    x_epochunit = epochunit_shop()

    # WHEN
    x_config = x_epochunit.to_dict()

    # THEN
    assert x_config
    assert x_config == get_creg_config()
