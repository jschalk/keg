from src.ch12_keep.rivercycle import rivergrade_shop
from src.ch12_keep.riverrun import riverrun_shop
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_set_initial_rivergrade_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao, number=yao_number)
    x_doctor_count = 5
    x_patient_count = 8
    yao_riverrun.doctor_count = x_doctor_count
    yao_riverrun.patient_count = x_patient_count
    assert yao_riverrun.rivergrades.get(exx.bob) is None

    # WHEN
    yao_riverrun.set_initial_rivergrade(exx.bob)

    # THEN
    bob_rivergrade = rivergrade_shop(
        exx.a23,
        exx.yao,
        None,
        exx.bob,
        yao_number,
        x_doctor_count,
        x_patient_count,
    )
    bob_rivergrade.care_amount = 0
    assert yao_riverrun.rivergrades.get(exx.bob) is not None
    gen_rivergrade = yao_riverrun.rivergrades.get(exx.bob)
    assert gen_rivergrade.doctor_count == x_doctor_count
    assert gen_rivergrade.patient_count == x_patient_count
    assert gen_rivergrade == bob_rivergrade


def test_RiverRun_rivergrades_is_empty_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao, number=yao_number)

    assert yao_riverrun.rivergrades_is_empty()

    # WHEN
    yao_riverrun.set_initial_rivergrade(exx.bob)

    # THEN
    assert yao_riverrun.rivergrades_is_empty() is False


def test_RiverRun_rivergrade_exists_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao, yao_number)
    yao_riverrun.set_initial_rivergrade(exx.yao)

    assert yao_riverrun.rivergrade_exists(exx.bob) is False
    assert yao_riverrun.rivergrades_is_empty() is False

    # WHEN
    yao_riverrun.set_initial_rivergrade(exx.bob)

    # THEN
    assert yao_riverrun.rivergrade_exists(exx.bob)
    assert yao_riverrun.rivergrades_is_empty() is False


def test_RiverRun_set_all_initial_rivergrades_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_keep_patientledger(exx.yao, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.zia, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.xio, exx.sue, 1)
    all_contacts_ids = x_riverrun.get_all_keep_patientledger_contact_names()
    assert all_contacts_ids == {exx.yao, exx.bob, exx.zia, exx.xio, exx.sue}
    assert x_riverrun.rivergrades_is_empty()
    assert x_riverrun.rivergrade_exists(exx.yao) is False
    assert x_riverrun.rivergrade_exists(exx.bob) is False
    assert x_riverrun.rivergrade_exists(exx.zia) is False

    # WHEN
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrades_is_empty() is False
    assert x_riverrun.rivergrade_exists(exx.yao)
    assert x_riverrun.rivergrade_exists(exx.bob)
    assert x_riverrun.rivergrade_exists(exx.zia)


def test_RiverRun_set_all_initial_rivergrades_OverWritesPrevious(temp3_dir):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_keep_patientledger(exx.yao, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.zia, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.xio, exx.sue, 1)
    x_riverrun.set_all_initial_rivergrades()
    assert x_riverrun.rivergrade_exists(exx.yao)
    assert x_riverrun.rivergrade_exists(exx.bob)
    assert x_riverrun.rivergrade_exists(exx.zia)
    assert x_riverrun.rivergrade_exists(exx.xio)
    assert x_riverrun.rivergrade_exists(exx.sue)

    # WHEN
    x_riverrun.delete_keep_patientledgers_person(exx.xio)
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrade_exists(exx.yao)
    assert x_riverrun.rivergrade_exists(exx.bob)
    assert x_riverrun.rivergrade_exists(exx.zia)
    assert x_riverrun.rivergrade_exists(exx.xio) is False
    assert x_riverrun.rivergrade_exists(exx.sue) is False
