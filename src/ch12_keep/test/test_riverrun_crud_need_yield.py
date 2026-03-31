from src.ch07_person_logic.person_main import personunit_shop
from src.ch12_keep.rivercycle import get_doctorledger
from src.ch12_keep.riverrun import riverrun_shop
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_set_partner_need_yield_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.bob)
    assert bob_riverrun.need_yields.get(exx.yao) is None

    # WHEN
    yao_need_yield = 7
    bob_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)

    # THEN
    assert bob_riverrun.need_yields.get(exx.yao) == yao_need_yield


def test_RiverRun_need_yields_is_empty_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    assert x_riverrun.need_yields_is_empty()

    # WHEN
    yao_need_yield = 500
    x_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)
    # THEN
    assert x_riverrun.need_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_need_yield(exx.yao)
    # THEN
    assert x_riverrun.need_yields_is_empty()

    # WHEN
    bob_need_yield = 300
    x_riverrun.set_partner_need_yield(exx.yao, bob_need_yield)
    x_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)
    # THEN
    assert x_riverrun.need_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_need_yield(exx.yao)
    # THEN
    assert x_riverrun.need_yields_is_empty()


def test_RiverRun_reset_need_yields_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        exx.a23,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_riverrun.set_partner_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_partner_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.need_yields_is_empty() is False

    # WHEN
    bob_riverrun.reset_need_yields()

    # THEN
    assert bob_riverrun.need_yields_is_empty()


def test_RiverRun_partner_has_need_yield_ReturnsBool(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        exx.a23,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    yao_need_yield = 6
    bob_need_yield = 38
    sue_need_yield = 56
    bob_riverrun.set_partner_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_partner_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.partner_has_need_yield(exx.bob)
    assert bob_riverrun.partner_has_need_yield(exx.sue)
    assert bob_riverrun.partner_has_need_yield(exx.yao)
    assert bob_riverrun.partner_has_need_yield(exx.zia) is False

    # WHEN
    bob_riverrun.reset_need_yields()

    # THEN
    assert bob_riverrun.partner_has_need_yield(exx.bob) is False
    assert bob_riverrun.partner_has_need_yield(exx.sue) is False
    assert bob_riverrun.partner_has_need_yield(exx.yao) is False
    assert bob_riverrun.partner_has_need_yield(exx.zia) is False


def test_RiverRun_delete_need_yield_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_mana_amount = 88
    bob_mana_grain = 11

    bob_riverrun = riverrun_shop(
        mstr_dir,
        exx.a23,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_riverrun.set_partner_need_yield(exx.yao, 5)
    assert bob_riverrun.partner_has_need_yield(exx.yao)

    # WHEN
    bob_riverrun.delete_need_yield(exx.yao)

    # THEN
    assert bob_riverrun.partner_has_need_yield(exx.yao) is False


def test_RiverRun_get_partner_need_yield_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_mana_amount = 1000
    bob_mana_grain = 1

    bob_riverrun = riverrun_shop(
        mstr_dir,
        exx.a23,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_riverrun.set_partner_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_partner_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.partner_has_need_yield(exx.bob)
    assert bob_riverrun.get_partner_need_yield(exx.bob) == bob_need_yield
    assert bob_riverrun.partner_has_need_yield(exx.zia) is False
    assert bob_riverrun.get_partner_need_yield(exx.zia) == 0

    # WHEN
    bob_riverrun.reset_need_yields()

    # THEN
    assert bob_riverrun.partner_has_need_yield(exx.bob) is False
    assert bob_riverrun.get_partner_need_yield(exx.bob) == 0
    assert bob_riverrun.partner_has_need_yield(exx.zia) is False
    assert bob_riverrun.get_partner_need_yield(exx.zia) == 0


def test_RiverRun_add_partner_need_yield_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        exx.a23,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_riverrun.set_partner_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_partner_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_partner_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.get_partner_need_yield(exx.bob) == bob_need_yield
    assert bob_riverrun.get_partner_need_yield(exx.sue) == sue_need_yield
    assert bob_riverrun.get_partner_need_yield(exx.zia) == 0

    # WHEN
    bob_riverrun.add_partner_need_yield(exx.sue, 5)
    bob_riverrun.add_partner_need_yield(exx.zia, 10)

    # THEN
    assert bob_riverrun.get_partner_need_yield(exx.bob) == bob_need_yield
    assert bob_riverrun.get_partner_need_yield(exx.sue) == sue_need_yield + 5
    assert bob_riverrun.get_partner_need_yield(exx.zia) == 10


def test_RiverRun_levy_need_due_SetsAttr_ScenarioY(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        exx.a23,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_person = personunit_shop(exx.bob)
    bob_person.add_partnerunit(exx.bob, 2, bob_need_yield)
    bob_person.add_partnerunit(exx.sue, 2, sue_need_yield)
    bob_person.add_partnerunit(exx.yao, 2, yao_need_yield)
    bob_doctorledger = get_doctorledger(bob_person)
    bob_riverrun.set_need_dues(bob_doctorledger)
    assert bob_riverrun.get_partner_need_due(exx.bob) == 380
    assert bob_riverrun.get_partner_need_yield(exx.bob) == 0

    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.bob, 5)
    # THEN
    assert excess_carer_points == 0
    assert bob_riverrun.get_partner_need_due(exx.bob) == 375
    assert bob_riverrun.get_partner_need_yield(exx.bob) == 5

    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.bob, 375)
    # THEN
    assert excess_carer_points == 0
    assert bob_riverrun.get_partner_need_due(exx.bob) == 0
    assert bob_riverrun.get_partner_need_yield(exx.bob) == 380

    # ESTABLISH
    assert bob_riverrun.get_partner_need_due(exx.sue) == 560
    assert bob_riverrun.get_partner_need_yield(exx.sue) == 0
    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.sue, 1000)
    # THEN
    assert excess_carer_points == 440
    assert bob_riverrun.get_partner_need_due(exx.sue) == 0
    assert bob_riverrun.get_partner_need_yield(exx.sue) == 560

    # ESTABLISH
    assert bob_riverrun.get_partner_need_due(exx.zia) == 0
    assert bob_riverrun.get_partner_need_yield(exx.zia) == 0
    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.zia, 1000)
    # THEN
    assert excess_carer_points == 1000
    assert bob_riverrun.get_partner_need_due(exx.zia) == 0
    assert bob_riverrun.get_partner_need_yield(exx.zia) == 0

    # ESTABLISH
    assert bob_riverrun.get_partner_need_due(exx.yao) == 60
    assert bob_riverrun.get_partner_need_yield(exx.yao) == 0
    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.yao, 81)
    # THEN
    assert excess_carer_points == 21
    assert bob_riverrun.get_partner_need_due(exx.yao) == 0
    assert bob_riverrun.get_partner_need_yield(exx.yao) == 60


def test_RiverRun_set_need_got_attrs_SetsAttrs(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    six_need_got = 6
    ten_need_got = 10
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun.need_got_prev == 0

    # WHEN
    x_riverrun._set_need_got_attrs(six_need_got)
    # THEN
    assert x_riverrun.need_got_curr == six_need_got
    assert x_riverrun.need_got_prev == 0

    # WHEN
    x_riverrun._set_need_got_attrs(ten_need_got)
    # THEN
    assert x_riverrun.need_got_curr == ten_need_got
    assert x_riverrun.need_got_prev == six_need_got


def test_RiverRun_need_gotten_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    six_need_got = 6
    ten_need_got = 10
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun._need_gotten() is False

    # WHEN
    x_riverrun._set_need_got_attrs(six_need_got)
    # THEN
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == six_need_got
    assert x_riverrun._need_gotten()

    # ESTABLISH
    x_riverrun._set_need_got_attrs(six_need_got)
    # THEN
    assert x_riverrun.need_got_prev == six_need_got
    assert x_riverrun.need_got_curr == six_need_got
    assert x_riverrun._need_gotten()

    # WHEN
    x_riverrun._set_need_got_attrs(0)
    # THEN
    assert x_riverrun.need_got_prev == six_need_got
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun._need_gotten()

    # WHEN
    x_riverrun._set_need_got_attrs(0)
    # THEN
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun._need_gotten() is False
