from ch11_bud.bud_main import personbudhistory_shop
from ch13_time.epoch_main import DEFAULT_EPOCH_LENGTH, epochunit_shop, get_epoch_length
from ch13_time.test._util.ch13_examples import get_creg_config
from ch14_moment.moment_frame import (
    add_epoch_frame_to_momentunit,
    get_moment_epochholder,
)
from ch14_moment.moment_main import momentunit_shop
from ref.keywords import ExampleStrs as exx


def test_get_moment_epochholder_ReturnsObj_Scenario0_Empty_offi_time(temp3_dir):
    # ESTABLISH
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir)
    assert a23_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not a23_momentunit.offi_time_max

    # WHEN
    a23_epochholder = get_moment_epochholder(a23_momentunit)

    # THEN
    assert a23_momentunit.offi_time_max == 0
    assert a23_epochholder.x_min == 0
    # assert a23_epochholder.x_min == a23_offi_time_max
    assert a23_epochholder
    assert a23_epochholder._month == "March"
    assert a23_epochholder._hour == "12am"
    assert a23_epochholder._minute == 0
    assert a23_epochholder._monthday == 1
    assert a23_epochholder._c400_number == 0
    assert a23_epochholder._year_num == 0


def test_get_moment_epochholder_ReturnsObj_Scenario1_MomentUnit_NonDefaultAttrs(
    temp3_dir,
):
    # ESTABLISH
    a23_fund_grain = 5
    a23_respect_grain = 4
    a23_mana_grain = 7
    a23_momentunit = momentunit_shop(
        exx.a23_slash,
        temp3_dir,
        knot=exx.slash,
        fund_grain=a23_fund_grain,
        respect_grain=a23_respect_grain,
        mana_grain=a23_mana_grain,
    )
    assert a23_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not a23_momentunit.offi_time_max

    # WHEN
    a23_epochholder = get_moment_epochholder(a23_momentunit)

    # THEN
    assert a23_momentunit.offi_time_max == 0
    assert a23_epochholder.x_min == 0

    assert a23_epochholder
    # assert a23_epochholder.x_min == a23_offi_time_max
    a23_personunit = a23_epochholder.x_personunit
    assert a23_personunit.person_name == "for_EpochHolder_calculation"
    assert a23_personunit.planroot.get_plan_rope() == a23_momentunit.moment_rope
    assert a23_personunit.knot == a23_momentunit.knot
    assert a23_personunit.fund_grain == a23_momentunit.fund_grain
    assert a23_personunit.respect_grain == a23_momentunit.respect_grain
    assert a23_personunit.mana_grain == a23_momentunit.mana_grain
    assert a23_epochholder._month == "March"
    assert a23_epochholder._hour == "12am"
    assert a23_epochholder._minute == 0
    assert a23_epochholder._monthday == 1
    assert a23_epochholder._c400_number == 0
    assert a23_epochholder._year_num == 0
    #  personunit_shop()
    #  epochholder_shop()


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario0_tran_time(temp3_dir):
    # ESTABLISH
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir)
    t55 = 55
    a23_momentunit.paybook.add_tranunit(exx.a23, exx.yao, t55, 3)
    epoch_frame_min = 6
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, epoch_frame_min)

    # THEN
    assert not a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)
    expected_time = t55 + epoch_frame_min
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, expected_time)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario1_tran_time_ModularAddition(
    temp3_dir,
):
    # ESTABLISH
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir)
    t55 = 55
    a23_momentunit.paybook.add_tranunit(exx.a23, exx.yao, t55, 3)
    frame_min = DEFAULT_EPOCH_LENGTH + 300
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, frame_min)

    # THEN
    assert not a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)
    expected_time = (t55 + frame_min) % DEFAULT_EPOCH_LENGTH
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, expected_time)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario2_tran_time_DifferentEpochUnit(
    temp3_dir,
):
    # ESTABLISH
    creg_epochunit = epochunit_shop(get_creg_config())
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir, creg_epochunit)
    t55 = 55
    a23_momentunit.paybook.add_tranunit(exx.a23, exx.yao, t55, 3)
    epoch_length = get_epoch_length(get_creg_config())
    frame_min = epoch_length + 300
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, frame_min)

    # THEN
    assert not a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)
    expected_time = (t55 + frame_min) % epoch_length
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, expected_time)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario3_tran_time_NoErrorWhenUsingSameTIme(
    temp3_dir,
):
    # ESTABLISH
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir)
    t55 = 55
    t65 = 65
    t75 = 75
    a23_momentunit.paybook.add_tranunit(exx.a23, exx.yao, t55, 3)
    a23_momentunit.paybook.add_tranunit(exx.a23, exx.yao, t65, 3)
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t65)
    assert not a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t75)

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, 10)

    # THEN
    assert not a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t55)
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t65)
    assert a23_momentunit.paybook.tranunit_exists(exx.a23, exx.yao, t75)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario4_bud_time(temp3_dir):
    # ESTABLISH
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir)
    t55_quota = 4
    t55_time = 55
    epoch_frame_min = 10
    t65_time = t55_time + epoch_frame_min
    a23_bud_hx = personbudhistory_shop(exx.a23)
    a23_bud_hx.add_bud(x_bud_time=t55_time, x_quota=t55_quota)
    a23_momentunit.set_personbudhistory(a23_bud_hx)
    assert a23_momentunit.bud_quota_exists(exx.a23, t55_time, t55_quota)
    assert not a23_momentunit.bud_quota_exists(exx.a23, t65_time, t55_quota)

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, epoch_frame_min)

    # THEN
    assert not a23_momentunit.bud_quota_exists(exx.a23, t55_time, t55_quota)
    assert a23_momentunit.bud_quota_exists(exx.a23, t65_time, t55_quota)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario5_bud_time_ModularAddition(
    temp3_dir,
):
    # ESTABLISH
    creg_epochunit = epochunit_shop(get_creg_config())
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir, creg_epochunit)
    t55_quota = 4
    t55_time = 55
    epoch_frame_min = 10
    epoch_length = get_epoch_length(get_creg_config())
    t0x_time = t55_time + epoch_frame_min + epoch_length
    a23_bud_hx = personbudhistory_shop(exx.a23)
    a23_bud_hx.add_bud(x_bud_time=t55_time, x_quota=t55_quota)
    a23_momentunit.set_personbudhistory(a23_bud_hx)
    assert a23_momentunit.bud_quota_exists(exx.a23, t55_time, t55_quota)
    assert not a23_momentunit.bud_quota_exists(exx.a23, t0x_time, t55_quota)

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, epoch_frame_min)

    # THEN
    assert not a23_momentunit.bud_quota_exists(exx.a23, t55_time, t55_quota)
    expected_time = t0x_time % epoch_length
    assert t0x_time != expected_time
    assert a23_momentunit.bud_quota_exists(exx.a23, expected_time, t55_quota)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario6_offi_time(temp3_dir):
    # ESTABLISH
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir)
    epoch_frame_min = 10
    t55_offi_time = 55
    t65_offi_time = t55_offi_time + epoch_frame_min
    a23_momentunit.offi_times.add(t55_offi_time)
    assert t55_offi_time in a23_momentunit.offi_times
    assert t65_offi_time not in a23_momentunit.offi_times

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, epoch_frame_min)

    # THEN
    assert t55_offi_time not in a23_momentunit.offi_times
    assert t65_offi_time in a23_momentunit.offi_times


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario7_offi_time_Set(temp3_dir):
    # ESTABLISH
    creg_epochunit = epochunit_shop(get_creg_config())
    a23_momentunit = momentunit_shop(exx.a23, temp3_dir, creg_epochunit)
    epoch_length = get_epoch_length(get_creg_config())
    epoch_frame_min = 10 + epoch_length
    t55_offi_time = 55
    epected_offi_time = t55_offi_time + epoch_frame_min % epoch_length
    a23_momentunit.offi_times.add(t55_offi_time)
    assert t55_offi_time in a23_momentunit.offi_times
    assert epected_offi_time not in a23_momentunit.offi_times

    # WHEN
    add_epoch_frame_to_momentunit(a23_momentunit, epoch_frame_min)

    # THEN
    assert t55_offi_time not in a23_momentunit.offi_times
    assert epected_offi_time in a23_momentunit.offi_times
