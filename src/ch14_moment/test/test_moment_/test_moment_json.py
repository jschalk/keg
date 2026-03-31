from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.ch00_py.file_toolbox import create_path, save_json
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch13_time.epoch_main import get_default_epoch_config_dict
from src.ch14_moment.moment_main import (
    get_momentunit_from_dict,
    momentunit_shop,
    open_moment_file,
    save_moment_file,
)
from src.ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_MomentUnit_to_dict_ReturnsObjWith_paybook(temp3_dir):
    # ESTABLISH
    moment_mstr_dir = create_path(temp3_dir, "temp1")
    a45_rope = create_rope("amy45")
    a45_offi_times = {17, 37}
    amy_moment = momentunit_shop(a45_rope, moment_mstr_dir, offi_times=a45_offi_times)
    amy_offi_time_max_int = 23
    bob_x0_tran_time = 702
    bob_x0_quota = 33
    sue_x4_tran_time = 404
    sue_x4_quota = 55
    sue_x7_tran_time = 505
    sue_x7_quota = 66
    pay_tran_time = 15
    bob_sue_amount = 30000
    amy_moment.set_offi_time_max(amy_offi_time_max_int)
    amy_moment.add_budunit(exx.bob, bob_x0_tran_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x4_tran_time, sue_x4_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_tran_time, sue_x7_quota)
    amy_moment.add_paypurchase(
        person_name=exx.bob,
        contact_name=exx.sue,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = amy_moment.to_dict()

    # THEN
    print(f"{ amy_moment._get_personbudhistorys_dict()=}")
    print(f"{ amy_moment.paybook.to_dict()=}")
    assert x_dict.get(kw.moment_rope) == a45_rope
    assert x_dict.get(kw.moment_mstr_dir) == moment_mstr_dir
    assert x_dict.get(kw.epoch) == get_default_epoch_config_dict()
    assert x_dict.get(kw.offi_times) == list(a45_offi_times)
    assert x_dict.get(kw.knot) == default_knot_if_None()
    assert x_dict.get(kw.fund_grain) == default_grain_num_if_None()
    assert x_dict.get(kw.respect_grain) == default_grain_num_if_None()
    assert x_dict.get(kw.mana_grain) == default_grain_num_if_None()
    assert x_dict.get(kw.personbudhistorys) == amy_moment._get_personbudhistorys_dict()
    assert x_dict.get(kw.paybook) == amy_moment.paybook.to_dict()
    assert set(x_dict.keys()) == {
        kw.moment_rope,
        kw.moment_mstr_dir,
        kw.epoch,
        kw.offi_times,
        kw.personbudhistorys,
        kw.knot,
        kw.fund_grain,
        kw.respect_grain,
        kw.mana_grain,
        kw.paybook,
    }


def test_MomentUnit_to_dict_ReturnsObjWithOut_paybook(temp3_dir):
    # ESTABLISH
    amy45_rope = create_rope("amy45")
    amy_moment = momentunit_shop(amy45_rope, temp3_dir)

    # WHEN
    x_dict = amy_moment.to_dict(include_paybook=False)

    # THEN
    assert not x_dict.get(kw.paybook)
    assert set(x_dict.keys()) == {
        kw.moment_rope,
        kw.moment_mstr_dir,
        kw.epoch,
        f"{kw.offi_time}s",
        kw.personbudhistorys,
        kw.knot,
        kw.fund_grain,
        kw.respect_grain,
        kw.mana_grain,
    }


def test_get_momentunit_from_dict_ReturnsObj_Scenario0_WithParameters(temp3_dir):
    # ESTABLISH
    sue_knot = "/"
    amy45_rope = create_rope("amy45", None, sue_knot)
    moment_mstr_dir = create_path(temp3_dir, "temp1")
    a45_offi_times = {17, 37}
    amy_moment = momentunit_shop(
        amy45_rope, moment_mstr_dir, knot=sue_knot, offi_times=a45_offi_times
    )
    sue_epoch_label = "sue casa"
    amy_moment.epoch.epoch_label = sue_epoch_label
    sue_fund_grain = 0.3
    sue_respect_grain = 2
    sue_mana_grain = 3
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    pay_tran_time = 15
    bob_sue_amount = 30000
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)
    amy_moment.knot = sue_knot
    amy_moment.fund_grain = sue_fund_grain
    amy_moment.respect_grain = sue_respect_grain
    amy_moment.mana_grain = sue_mana_grain
    amy_moment.add_paypurchase(
        person_name=exx.bob,
        contact_name=exx.sue,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )
    x_dict = amy_moment.to_dict()

    # WHEN
    x_moment = get_momentunit_from_dict(x_dict)

    # THEN
    assert x_moment.moment_rope == amy45_rope
    assert x_moment.moment_mstr_dir == moment_mstr_dir
    assert x_moment.epoch.epoch_label == sue_epoch_label
    assert x_moment.offi_times == a45_offi_times
    assert x_moment.knot == sue_knot
    assert x_moment.fund_grain == sue_fund_grain
    assert x_moment.respect_grain == sue_respect_grain
    assert x_moment.mana_grain == sue_mana_grain
    assert x_moment.personbudhistorys == amy_moment.personbudhistorys
    assert x_moment.paybook == amy_moment.paybook
    assert x_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert x_moment != amy_moment
    x_moment.offi_time_max = 0
    assert x_moment == amy_moment


def test_get_momentunit_from_dict_ReturnsObj_Scenario1_WithOutParameters(temp3_dir):
    # ESTABLISH
    amy45_rope = create_rope("amy45")
    amy_moment = momentunit_shop(amy45_rope, temp3_dir)
    x_dict = amy_moment.to_dict()
    x_dict[kw.epoch] = {}
    x_dict.pop(kw.knot)
    x_dict.pop(kw.fund_grain)
    x_dict.pop(kw.respect_grain)
    x_dict.pop(kw.mana_grain)

    # WHEN
    generated_moment = get_momentunit_from_dict(x_dict)

    # THEN
    assert generated_moment.moment_rope == amy45_rope
    print(f"{generated_moment.epoch=}")
    print(f"   {amy_moment.epoch=}")
    assert generated_moment.epoch == amy_moment.epoch
    assert generated_moment.offi_times == set()
    assert generated_moment.knot == default_knot_if_None()
    assert generated_moment.fund_grain == default_grain_num_if_None()
    assert generated_moment.respect_grain == default_grain_num_if_None()
    assert generated_moment.mana_grain == 1
    assert generated_moment.personbudhistorys == amy_moment.personbudhistorys
    assert generated_moment.paybook == amy_moment.paybook
    assert generated_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert generated_moment == amy_moment


def test_get_momentunit_from_dict_ReturnsObj_Scenario2(temp3_dir):
    # ESTABLISH
    amy45_rope = create_rope("amy45", None, exx.slash)
    temp_moment_mstr_dir = create_path(temp3_dir, "temp")
    amy_moment = momentunit_shop(amy45_rope, temp_moment_mstr_dir, knot=exx.slash)
    sue_epoch_label = "sue casa"
    amy_moment.epoch.epoch_label = sue_epoch_label
    sue_offi_time_max = 23
    sue_knot = exx.slash
    sue_fund_grain = 0.3
    sue_respect_grain = 2
    sue_mana_grain = 3
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)
    amy_moment.knot = sue_knot
    amy_moment.fund_grain = sue_fund_grain
    amy_moment.respect_grain = sue_respect_grain
    amy_moment.mana_grain = sue_mana_grain
    amy_dict = amy_moment.to_dict()

    # WHEN
    x_moment = get_momentunit_from_dict(amy_dict)

    # THEN
    assert x_moment.moment_rope == amy45_rope
    assert x_moment.moment_mstr_dir == temp_moment_mstr_dir
    assert x_moment.epoch.epoch_label == sue_epoch_label
    assert x_moment.knot == sue_knot
    assert x_moment.fund_grain == sue_fund_grain
    assert x_moment.respect_grain == sue_respect_grain
    assert x_moment.mana_grain == sue_mana_grain
    assert x_moment.personbudhistorys == amy_moment.personbudhistorys
    assert x_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert x_moment != amy_moment
    x_moment.offi_time_max = 0
    assert x_moment == amy_moment


def test_open_moment_file_ReturnsObj_MomentUnit(temp3_fs):
    # ESTABLISH
    amy45_str = "Amy"
    amy45_rope = create_rope(amy45_str)
    amy45_moment = momentunit_shop(amy45_rope, str(temp3_fs))
    sue_epoch_label = "sue casa"
    amy45_moment.epoch.epoch_label = sue_epoch_label
    sue_respect_grain = 2
    amy45_moment.respect_grain = sue_respect_grain
    x_moment_mstr_dir = create_path(str(temp3_fs), "Fay_bob")
    amy45_lasso = lassounit_shop(amy45_rope)
    amy45_json_path = create_moment_json_path(x_moment_mstr_dir, amy45_lasso)
    save_json(amy45_json_path, None, amy45_moment.to_dict())
    assert amy45_moment.moment_mstr_dir != x_moment_mstr_dir

    # WHEN
    generated_a45_moment = open_moment_file(x_moment_mstr_dir, amy45_lasso)

    # THEN
    assert generated_a45_moment.moment_mstr_dir == x_moment_mstr_dir
    assert generated_a45_moment.moment_rope == amy45_rope
    assert generated_a45_moment.epoch.epoch_label == sue_epoch_label
    assert generated_a45_moment.respect_grain == sue_respect_grain
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    expected_a45_moment_dir = create_path(x_moments_dir, amy45_str)
    assert generated_a45_moment.moment_dir == expected_a45_moment_dir


def test_save_moment_file_ReturnsObj_Scenario0_MomentUnit(temp3_fs):
    # ESTABLISH
    x_moment_mstr_dir = create_path(str(temp3_fs), "Fay_bob")
    amy45_str = "Amy"
    amy45_rope = create_rope(amy45_str)
    amy45_moment = momentunit_shop(amy45_rope, x_moment_mstr_dir)
    sue_epoch_label = "sue casa"
    amy45_moment.epoch.epoch_label = sue_epoch_label
    amy45_lasso = lassounit_shop(amy45_rope)
    amy45_json_path = create_moment_json_path(x_moment_mstr_dir, amy45_lasso)
    assert not os_path_exists(amy45_json_path)

    # WHEN
    save_moment_file(amy45_moment, amy45_lasso)

    # THEN
    assert os_path_exists(amy45_json_path)
    assert open_moment_file(x_moment_mstr_dir, amy45_lasso) == amy45_moment


def test_save_moment_file_RaisesException_WhenMomentUnitMomentMstrDirIsNone(
    temp3_fs,
):
    # ESTABLISH
    amy45_str = "Amy"
    amy45_rope = create_rope(amy45_str)
    amy45_moment = momentunit_shop(amy45_rope, None)
    amy45_lasso = lassounit_shop(amy45_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_moment_file(amy45_moment, amy45_lasso)
    assert str(excinfo.value) == "moment_mstr_dir is None"
