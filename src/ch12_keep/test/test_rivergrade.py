from src.ch12_keep.rivercycle import RiverGrade, rivergrade_shop
from src.ref.keywords import Ch12Keywords as kw, ExampleStrs as exx


def test_RiverGrade_Exists():
    # ESTABLISH / WHEN
    x_rivergrade = RiverGrade()

    # THEN
    #: Healer gut get_contact._contact_debt_lumen (SELECT need_due_amount FROM contact WHERE contact_name = exx.bob)
    assert not x_rivergrade.moment_rope
    assert not x_rivergrade.person_name
    assert not x_rivergrade.keep_rope
    assert not x_rivergrade.contact_name
    assert not x_rivergrade.number
    #: Healer gut get_contact._contact_debt_lumen (SELECT need_due_amount FROM contact WHERE contact_name = exx.bob)
    assert x_rivergrade.need_bill_amount is None
    #: Healer gut get_contact._contact_cred_lumen (SELECT care_amount FROM contact WHERE contact_name = exx.bob)
    assert x_rivergrade.care_amount is None
    #: SELECT COUNT(*) FROM contact WHERE need_due_amount > (SELECT need_due_amount FROM contact WHERE contact_name = exx.bob)
    assert x_rivergrade.doctor_rank_num is None
    #: SELECT COUNT(*) FROM contact WHERE care_amount > (SELECT need_due_amount FROM contact WHERE contact_name = exx.bob)
    assert x_rivergrade.patient_rank_num is None
    #: SELECT amount_paid FROM need_ledger WHERE contact_name = exx.bob
    assert x_rivergrade.need_paid_amount is None
    #: bool (if need_due_amount == need_paid_amount)
    assert x_rivergrade.need_paid_bool is None
    #: SELECT COUNT(*) FROM contact WHERE need_paid_amount > (SELECT need_paid_amount FROM contact WHERE contact_name = exx.bob)
    assert x_rivergrade.need_paid_rank_num is None
    #: need_paid_rank_num / (SELECT COUNT(*) FROM contact WHERE need_paid_amount>0)
    assert x_rivergrade.need_paid_rank_percent is None
    #: SELECT COUNT(*) FROM contact WHERE need_due_amount > 0
    assert x_rivergrade.doctor_count is None
    #: SELECT COUNT(*) FROM contact WHERE care_amount > 0
    assert x_rivergrade.patient_count is None
    #: doctor_rank_num / SELECT COUNT(*) FROM contact WHERE need_due_amount > 0
    assert x_rivergrade.doctor_rank_percent is None
    #: patient_rank_num / SELECT COUNT(*) FROM contact WHERE care_amount > 0
    assert x_rivergrade.patient_rank_percent is None
    # SELECT COUNT(*) FROM rewards WHERE dst_contact_name = exx.bob
    assert x_rivergrade.rewards_count is None
    # SELECT SUM(mana_amount) FROM rewards WHERE dst_contact_name = exx.bob
    assert x_rivergrade.rewards_magnitude is None
    assert set(x_rivergrade.__dict__.keys()) == {
        kw.moment_rope,
        kw.person_name,
        kw.keep_rope,
        kw.contact_name,
        "number",
        kw.need_bill_amount,
        kw.care_amount,
        kw.doctor_rank_num,
        kw.patient_rank_num,
        kw.need_paid_amount,
        kw.need_paid_bool,
        kw.need_paid_rank_num,
        kw.need_paid_rank_percent,
        kw.doctor_count,
        kw.patient_count,
        kw.doctor_rank_percent,
        kw.patient_rank_percent,
        kw.rewards_count,
        kw.rewards_magnitude,
    }


def test_rivergrade_shop_ReturnsObjWithArg():
    # ESTABLISH
    x_keep_rope = None
    ten_int = 10
    x_doctor_count = 7
    x_patient_count = 9

    # WHEN
    x_rivergrade = rivergrade_shop(
        exx.a23, exx.yao, x_keep_rope, exx.bob, ten_int, x_doctor_count, x_patient_count
    )

    # THEN
    assert x_rivergrade.moment_rope == exx.a23
    assert x_rivergrade.person_name == exx.yao
    assert x_rivergrade.keep_rope == x_keep_rope
    assert x_rivergrade.contact_name == exx.bob
    assert x_rivergrade.number == ten_int
    assert not x_rivergrade.need_bill_amount
    assert not x_rivergrade.care_amount
    assert not x_rivergrade.doctor_rank_num
    assert not x_rivergrade.patient_rank_num
    assert not x_rivergrade.need_paid_amount
    assert not x_rivergrade.need_paid_bool
    assert not x_rivergrade.need_paid_rank_num
    assert not x_rivergrade.need_paid_rank_percent
    assert x_rivergrade.doctor_count == x_doctor_count
    assert x_rivergrade.patient_count == x_patient_count
    assert not x_rivergrade.doctor_rank_percent
    assert not x_rivergrade.patient_rank_percent
    assert not x_rivergrade.rewards_count
    assert not x_rivergrade.rewards_magnitude


def test_rivergrade_shop_ReturnsObjWithoutArgs():
    # ESTABLISH
    x_keep_rope = None

    # WHEN
    x_rivergrade = rivergrade_shop(exx.a23, exx.yao, x_keep_rope, exx.bob)

    # THEN
    assert x_rivergrade.moment_rope == exx.a23
    assert x_rivergrade.person_name == exx.yao
    assert x_rivergrade.keep_rope == x_keep_rope
    assert x_rivergrade.contact_name == exx.bob
    assert x_rivergrade.number == 0
    assert not x_rivergrade.need_bill_amount
    assert not x_rivergrade.care_amount
    assert not x_rivergrade.doctor_rank_num
    assert not x_rivergrade.patient_rank_num
    assert not x_rivergrade.need_paid_amount
    assert not x_rivergrade.need_paid_bool
    assert not x_rivergrade.need_paid_rank_num
    assert not x_rivergrade.need_paid_rank_percent
    assert not x_rivergrade.doctor_count
    assert not x_rivergrade.patient_count
    assert not x_rivergrade.doctor_rank_percent
    assert not x_rivergrade.patient_rank_percent
    assert not x_rivergrade.rewards_count
    assert not x_rivergrade.rewards_magnitude


def test_RiverGrade_set_need_due_amount_SetsAttrs():
    # ESTABLISH
    x_rivergrade = RiverGrade()
    assert not x_rivergrade.need_bill_amount
    assert not x_rivergrade.need_paid_amount
    assert not x_rivergrade.need_paid_bool

    # WHEN
    x_need_due_amount = 88
    x_rivergrade.set_need_bill_amount(x_need_due_amount)
    # THEN
    assert x_rivergrade.need_bill_amount == x_need_due_amount
    assert not x_rivergrade.need_paid_amount
    assert not x_rivergrade.need_paid_bool

    # WHEN
    x_need_paid_amount = 77
    x_rivergrade.set_need_paid_amount(x_need_paid_amount)
    # THEN
    assert x_rivergrade.need_bill_amount == x_need_due_amount
    assert x_rivergrade.need_paid_amount == x_need_paid_amount
    assert x_rivergrade.need_paid_bool is False

    # WHEN
    x_rivergrade.set_need_paid_amount(x_need_due_amount)
    # THEN
    assert x_rivergrade.need_bill_amount == x_rivergrade.need_paid_amount
    assert x_rivergrade.need_paid_bool is True


def test_RiverGrade_to_dict_ReturnsObj():
    # ESTABLISH
    x_keep_rope = None
    ten_int = 10
    x_need_bill_amount = 90
    x_care_amount = 91
    x_doctor_rank_num = 92
    x_patient_rank_num = 93
    x_need_paid_amount = 94
    x_need_paid_bool = 95
    x_need_paid_rank_num = 97
    x_need_paid_rank_percent = 99
    x_doctor_count = 101
    x_patient_count = 103
    x_doctor_rank_percent = 105
    x_patient_rank_percent = 107
    x_rewards_count = 108
    x_rewards_magnitude = 109
    x_rivergrade = rivergrade_shop(
        exx.a23, exx.yao, x_keep_rope, exx.bob, ten_int, x_doctor_count, x_patient_count
    )
    x_rivergrade.need_bill_amount = x_need_bill_amount
    x_rivergrade.care_amount = x_care_amount
    x_rivergrade.doctor_rank_num = x_doctor_rank_num
    x_rivergrade.patient_rank_num = x_patient_rank_num
    x_rivergrade.need_paid_amount = x_need_paid_amount
    x_rivergrade.need_paid_bool = x_need_paid_bool
    x_rivergrade.need_paid_rank_num = x_need_paid_rank_num
    x_rivergrade.need_paid_rank_percent = x_need_paid_rank_percent
    x_rivergrade.doctor_count = x_doctor_count
    x_rivergrade.patient_count = x_patient_count
    x_rivergrade.doctor_rank_percent = x_doctor_rank_percent
    x_rivergrade.patient_rank_percent = x_patient_rank_percent
    x_rivergrade.rewards_count = x_rewards_count
    x_rivergrade.rewards_magnitude = x_rewards_magnitude

    # WHEN
    rivergrade_dict = x_rivergrade.to_dict()

    # THEN
    assert rivergrade_dict.get(kw.moment_rope) == exx.a23
    assert rivergrade_dict.get(kw.healer_name) == exx.yao
    assert rivergrade_dict.get(kw.keep_rope) == x_keep_rope
    assert rivergrade_dict.get(kw.need_bill_amount) == x_need_bill_amount
    assert rivergrade_dict.get(kw.care_amount) == x_care_amount
    assert rivergrade_dict.get(kw.doctor_rank_num) == x_doctor_rank_num
    assert rivergrade_dict.get(kw.patient_rank_num) == x_patient_rank_num
    assert rivergrade_dict.get(kw.need_paid_amount) == x_need_paid_amount
    assert rivergrade_dict.get(kw.need_paid_bool) == x_need_paid_bool
    assert rivergrade_dict.get(kw.need_paid_rank_num) == x_need_paid_rank_num
    assert rivergrade_dict.get(kw.need_paid_rank_percent) == x_need_paid_rank_percent
    assert rivergrade_dict.get(kw.doctor_count) == x_doctor_count
    assert rivergrade_dict.get(kw.patient_count) == x_patient_count
    assert rivergrade_dict.get(kw.doctor_rank_percent) == x_doctor_rank_percent
    assert rivergrade_dict.get(kw.patient_rank_percent) == x_patient_rank_percent
    assert rivergrade_dict.get(kw.rewards_count) == x_rewards_count
    assert rivergrade_dict.get(kw.rewards_magnitude) == x_rewards_magnitude
