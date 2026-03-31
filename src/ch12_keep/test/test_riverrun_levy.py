from src.ch12_keep.riverrun import riverrun_shop
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_levy_need_dues_Molds_cycleledger_Scenario01(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_need_due = 222
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_partner_need_due(exx.yao, yao_need_due)

    yao_paid = 500
    x_cycleledger = {exx.yao: yao_paid}
    assert x_riverrun.get_partner_need_due(exx.yao) == yao_need_due
    assert x_cycleledger.get(exx.yao) == yao_paid

    # WHEN
    y_cycleledger, need_got = x_riverrun.levy_need_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert need_got == 222
    assert y_cycleledger.get(exx.yao) == yao_paid - yao_need_due


def test_RiverRun_levy_need_dues_Molds_cycleledger_Scenario02(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_need_due = 222
    bob_need_due = 127
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_partner_need_due(exx.yao, yao_need_due)
    x_riverrun.set_partner_need_due(exx.bob, bob_need_due)

    yao_paid = 500
    bob_paid = 100
    x_cycleledger = {exx.yao: yao_paid, exx.bob: bob_paid}
    assert x_riverrun.get_partner_need_due(exx.yao) == yao_need_due
    assert x_riverrun.get_partner_need_due(exx.bob) == bob_need_due
    assert x_cycleledger.get(exx.yao) == yao_paid
    assert x_cycleledger.get(exx.bob) == bob_paid

    # WHEN
    y_cycleledger, need_got = x_riverrun.levy_need_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_due(exx.bob) == 27
    assert y_cycleledger.get(exx.yao) == yao_paid - yao_need_due
    assert y_cycleledger.get(exx.bob) is None
    assert need_got == 322


def test_RiverRun_cycle_carees_vary_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    # WHEN / THEN
    assert x_riverrun._cycle_carees_vary() is False

    x_riverrun.cycle_carees_prev = {exx.yao}
    assert x_riverrun.cycle_carees_prev == {exx.yao}
    assert x_riverrun.cycle_carees_curr == set()

    # WHEN / THEN
    assert x_riverrun._cycle_carees_vary()


def test_RiverRun_cycles_vary_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    yao_need_got = 5
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    assert x_riverrun._cycle_carees_vary() is False
    assert x_riverrun._need_gotten() is False
    assert x_riverrun.cycles_vary() is False

    # WHEN
    x_riverrun.cycle_carees_prev = {exx.yao}
    # THEN
    assert x_riverrun._cycle_carees_vary()
    assert x_riverrun._need_gotten() is False
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun._set_need_got_attrs(yao_need_got)
    # THEN
    assert x_riverrun._cycle_carees_vary()
    assert x_riverrun._need_gotten()
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun.cycle_carees_curr = {exx.yao}
    # THEN
    assert x_riverrun._cycle_carees_vary() is False
    assert x_riverrun._need_gotten()
    assert x_riverrun.cycles_vary()
