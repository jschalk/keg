from src.ch01_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch12_keep._ref.ch12_semantic_types import default_knot_if_None
from src.ch12_keep.riverrun import RiverRun, riverrun_shop
from src.ch12_keep.test._util.ch12_examples import (
    example_yao_bob_zia_need_dues,
    example_yao_bob_zia_patientledgers,
)
from src.ref.keywords import Ch12Keywords as kw, ExampleStrs as exx


def test_RiverRun_Exists():
    # ESTABLISH / WHEN
    x_riverrun = RiverRun()

    # THEN
    assert not x_riverrun.moment_mstr_dir
    assert not x_riverrun.moment_rope
    assert not x_riverrun.person_name
    assert not x_riverrun.keep_rope
    assert not x_riverrun.knot
    assert not x_riverrun.keep_point_magnitude
    assert not x_riverrun.mana_grain
    assert not x_riverrun.number
    assert not x_riverrun.keep_patientledgers
    assert not x_riverrun.need_dues
    assert not x_riverrun.cycle_max
    # calculated fields
    assert not x_riverrun.rivergrades
    assert not x_riverrun.cares
    assert not x_riverrun.need_yields
    assert not x_riverrun.need_got_prev
    assert not x_riverrun.need_got_curr
    assert not x_riverrun.cycle_count
    assert not x_riverrun.cycle_carees_prev
    assert not x_riverrun.cycle_carees_curr
    assert not x_riverrun.doctor_count
    assert not x_riverrun.patient_count
    assert set(x_riverrun.__dict__.keys()) == {
        kw.moment_mstr_dir,
        kw.moment_rope,
        kw.person_name,
        kw.keep_rope,
        kw.knot,
        kw.keep_point_magnitude,
        kw.mana_grain,
        "number",
        kw.keep_patientledgers,
        kw.need_dues,
        kw.cycle_max,
        kw.rivergrades,
        kw.cares,
        kw.need_yields,
        kw.need_got_prev,
        kw.need_got_curr,
        kw.cycle_count,
        kw.cycle_carees_prev,
        kw.cycle_carees_curr,
        kw.doctor_count,
        kw.patient_count,
    }


def test_RiverRun_set_cycle_max_SetsAttr():
    # ESTABLISH
    x_riverrun = RiverRun()
    assert not x_riverrun.cycle_max

    # WHEN / THEN
    x_riverrun.set_cycle_max(10)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.0)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(-10.0)
    assert x_riverrun.cycle_max == 0

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.8)
    assert x_riverrun.cycle_max == 10


def test_riverrun_shop_ReturnsObj_Scenario0_WithArgs(temp3_dir):
    # ESTABLISH
    ten_int = 10
    mstr_dir = temp3_dir
    x_keep_rope = ";fizz;"
    x_knot = ";"
    x_keep_point_magnitude = 333
    x_mana_grain = 3
    keep_patientledgers = example_yao_bob_zia_patientledgers()
    x_cycle_max = 10
    x_need_dues = example_yao_bob_zia_need_dues()

    # WHEN
    x_riverrun = riverrun_shop(
        moment_mstr_dir=mstr_dir,
        moment_rope=exx.a23,
        person_name=exx.yao,
        keep_rope=x_keep_rope,
        knot=x_knot,
        keep_point_magnitude=x_keep_point_magnitude,
        mana_grain=x_mana_grain,
        number=ten_int,
        keep_patientledgers=keep_patientledgers,
        need_dues=x_need_dues,
        cycle_max=x_cycle_max,
    )

    # THEN
    assert x_riverrun.moment_mstr_dir == mstr_dir
    assert x_riverrun.moment_rope == exx.a23
    assert x_riverrun.person_name == exx.yao
    assert x_riverrun.keep_rope == x_keep_rope
    assert x_riverrun.knot == x_knot
    assert x_riverrun.keep_point_magnitude == x_keep_point_magnitude
    assert x_riverrun.mana_grain == x_mana_grain
    assert x_riverrun.number == ten_int
    assert x_riverrun.keep_patientledgers == keep_patientledgers
    assert x_riverrun.need_dues == x_need_dues
    assert x_riverrun.cycle_max == x_cycle_max
    assert x_riverrun.rivergrades == {}
    assert x_riverrun.cares == {}
    assert x_riverrun.need_yields == {}
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_carees_prev == set()
    assert x_riverrun.cycle_carees_curr == set()


def test_riverrun_shop_ReturnsObj_Scenario1_WithoutArgs(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir

    # WHEN
    x_riverrun = riverrun_shop(
        moment_mstr_dir=mstr_dir,
        moment_rope=exx.a23,
        person_name=exx.yao,
    )

    # THEN
    assert x_riverrun.moment_mstr_dir == mstr_dir
    assert x_riverrun.moment_rope == exx.a23
    assert x_riverrun.person_name == exx.yao
    assert not x_riverrun.keep_rope
    assert x_riverrun.knot == default_knot_if_None()
    assert x_riverrun.keep_point_magnitude == validate_pool_num()
    assert x_riverrun.mana_grain == default_grain_num_if_None()
    assert x_riverrun.number == 0
    assert x_riverrun.keep_patientledgers == {}
    assert x_riverrun.need_dues == {}
    assert x_riverrun.rivergrades == {}
    assert x_riverrun.cares == {}
    assert x_riverrun.need_yields == {}
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_max == 10


def test_RiverRun_set_keep_patientledger_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    yao_partner_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    assert x_riverrun.keep_patientledgers == {}

    # WHEN
    x_riverrun.set_keep_patientledger(
        person_name=exx.yao,
        partner_name=exx.yao,
        mana_ledger=yao_partner_cred_lumen,
    )

    # THEN
    assert x_riverrun.keep_patientledgers == {
        exx.yao: {exx.yao: yao_partner_cred_lumen}
    }


def test_RiverRun_delete_keep_patientledgers_person_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_keep_patientledger(exx.bob, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.bob, exx.sue, 1)
    assert x_riverrun.keep_patientledgers == {
        exx.yao: {exx.yao: 1},
        exx.bob: {exx.bob: 1, exx.sue: 1},
    }

    # WHEN
    x_riverrun.delete_keep_patientledgers_person(exx.bob)

    # THEN
    assert x_riverrun.keep_patientledgers == {exx.yao: {exx.yao: 1}}


def test_RiverRun_get_all_keep_patientledger_partner_names_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)

    # WHEN
    all_partners_ids = x_riverrun.get_all_keep_patientledger_partner_names()
    # THEN
    assert all_partners_ids == set()

    # WHEN
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_keep_patientledger(exx.yao, exx.bob, 1)
    all_partners_ids = x_riverrun.get_all_keep_patientledger_partner_names()
    # THEN
    assert all_partners_ids == {exx.yao, exx.bob}

    # WHEN
    x_riverrun.set_keep_patientledger(exx.zia, exx.bob, 1)
    all_partners_ids = x_riverrun.get_all_keep_patientledger_partner_names()
    # THEN
    assert all_partners_ids == {exx.yao, exx.bob, exx.zia}

    # WHEN
    x_riverrun.set_keep_patientledger(exx.xio, exx.sue, 1)
    all_partners_ids = x_riverrun.get_all_keep_patientledger_partner_names()
    # THEN
    assert all_partners_ids == {exx.yao, exx.bob, exx.zia, exx.xio, exx.sue}
