from src.ch12_keep.riverrun import riverrun_shop
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_calc_metrics_SetsAttrsScenario01(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_partner_cred_lumen = 500
    x_keep_point_magnitude = 444
    x_riverrun = riverrun_shop(
        mstr_dir, exx.a23, exx.yao, keep_point_magnitude=x_keep_point_magnitude
    )
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    assert x_riverrun.get_partner_need_due(exx.yao) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.cycle_count == 1
    assert x_riverrun.doctor_count == 0
    assert x_riverrun.patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(exx.yao)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_rope == exx.a23
    assert yao_rivergrade.person_name == exx.yao
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == x_keep_point_magnitude
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario02(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_partner_cred_lumen = 500
    bob_partner_debt_lumen = 350
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    x_riverrun.set_need_dues({exx.bob: bob_partner_debt_lumen})
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount
    assert x_riverrun.cycle_count == 1
    assert x_riverrun.doctor_count == 1
    assert x_riverrun.patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(exx.yao)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_rope == exx.a23
    assert yao_rivergrade.person_name == exx.yao
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == keep_mana_amount
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario03(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_partner_cred_lumen = 500
    bob_partner_debt_lumen = 25
    sue_partner_debt_lumen = 75
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    doctorledger = {exx.bob: bob_partner_debt_lumen, exx.sue: sue_partner_debt_lumen}
    x_riverrun.set_need_dues(doctorledger)
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount * 0.25
    assert x_riverrun.get_partner_need_due(exx.sue) == keep_mana_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount * 0.25
    assert x_riverrun.get_partner_need_due(exx.sue) == keep_mana_amount * 0.75
    assert x_riverrun.cycle_count == 1
    assert x_riverrun.doctor_count == 2
    assert x_riverrun.patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(exx.yao)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_rope == exx.a23
    assert yao_rivergrade.person_name == exx.yao
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == keep_mana_amount
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario04(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_yao_partner_cred_lumen = 500
    yao_sue_partner_cred_lumen = 2000
    bob_partner_debt_lumen = 25
    sue_partner_debt_lumen = 75
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_yao_partner_cred_lumen)
    x_riverrun.set_keep_patientledger(exx.yao, exx.sue, yao_sue_partner_cred_lumen)
    doctorledger = {exx.bob: bob_partner_debt_lumen, exx.sue: sue_partner_debt_lumen}
    x_riverrun.set_need_dues(doctorledger)
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount * 0.25
    assert x_riverrun.get_partner_need_due(exx.sue) == keep_mana_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount * 0.25
    assert x_riverrun.get_partner_need_due(exx.sue) == 0
    assert x_riverrun.get_partner_need_yield(exx.sue) == keep_mana_amount * 0.75
    assert x_riverrun.cycle_count == 2
    assert x_riverrun.doctor_count == 2
    assert x_riverrun.patient_count == 2
    yao_rivergrade = x_riverrun.get_rivergrade(exx.yao)
    sue_rivergrade = x_riverrun.get_rivergrade(exx.sue)
    assert yao_rivergrade.care_amount == keep_mana_amount * 0.2
    assert sue_rivergrade.care_amount == keep_mana_amount * 0.8
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario05(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_partner_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    x_riverrun.set_need_dues({exx.yao: 1})
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_partner_need_due(exx.yao) == keep_mana_amount
    assert x_riverrun.get_partner_need_yield(exx.yao) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_yield(exx.yao) == keep_mana_amount
    assert x_riverrun.cycle_count == 2
    assert x_riverrun.doctor_count == 1
    assert x_riverrun.patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(exx.yao)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_rope == exx.a23
    assert yao_rivergrade.person_name == exx.yao
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == keep_mana_amount
    assert yao_rivergrade.need_bill_amount == keep_mana_amount
    assert yao_rivergrade.need_paid_amount == keep_mana_amount
    assert yao_rivergrade.need_paid_bool


def test_RiverRun_calc_metrics_Resets_need_yield(temp3_dir):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    yao_partner_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    x_riverrun.set_need_dues({exx.yao: 1})
    keep_mana_amount = x_riverrun.keep_point_magnitude
    x_riverrun.calc_metrics()
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_yield(exx.yao) == keep_mana_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_yield(exx.yao) == keep_mana_amount


def test_RiverRun_calc_metrics_EndsRiverCycleLoopIfNoDifferencesBetweenCycles(
    temp3_dir,
):
    # ESTABLISH / WHEN
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_need_dues({exx.bob: 1})
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_carees_prev == set()
    assert x_riverrun.cycle_carees_curr == set()

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.cycle_carees_prev == {exx.yao}
    assert x_riverrun.cycle_carees_curr == {exx.yao}
    assert x_riverrun.get_partner_need_due(exx.yao) == 0
    assert x_riverrun.get_partner_need_due(exx.bob) == keep_mana_amount
    assert x_riverrun.cycle_count == 1
