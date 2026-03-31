from src.ch07_person_logic.person_main import personunit_shop
from src.ch12_keep.rivercycle import get_doctorledger, get_patientledger
from src.ch12_keep.riverrun import riverrun_shop
from src.ref.keywords import ExampleStrs as exx


def test_get_patientledger_ReturnsObj():
    # ESTABLISH
    yao_partner_cred_lumen = 8
    bob_partner_cred_lumen = 48
    sue_partner_cred_lumen = 66
    yao_person = personunit_shop(exx.yao)
    yao_person.add_partnerunit(exx.bob, yao_partner_cred_lumen)
    yao_person.add_partnerunit(exx.sue, bob_partner_cred_lumen)
    yao_person.add_partnerunit(exx.yao, sue_partner_cred_lumen)

    # WHEN
    yao_patientledger = get_patientledger(yao_person)

    # THEN
    assert len(yao_patientledger) == 3
    assert yao_patientledger.get(exx.bob) == yao_partner_cred_lumen
    assert yao_patientledger.get(exx.sue) == bob_partner_cred_lumen
    assert yao_patientledger.get(exx.yao) == sue_partner_cred_lumen


def test_get_patientledger_ReturnsObjWithNoEmpty_partner_cred_lumen():
    # ESTABLISH
    yao_partner_cred_lumen = 8
    bob_partner_cred_lumen = 0
    sue_partner_cred_lumen = 66
    yao_person = personunit_shop(exx.yao)
    yao_person.add_partnerunit(exx.bob, bob_partner_cred_lumen)
    yao_person.add_partnerunit(exx.sue, sue_partner_cred_lumen)
    yao_person.add_partnerunit(exx.yao, yao_partner_cred_lumen)

    # WHEN
    yao_patientledger = get_patientledger(yao_person)

    # THEN
    assert yao_patientledger.get(exx.bob) is None
    assert yao_patientledger.get(exx.sue) == sue_partner_cred_lumen
    assert yao_patientledger.get(exx.yao) == yao_partner_cred_lumen
    assert len(yao_patientledger) == 2


def test_get_doctorledger_ReturnsObj():
    # ESTABLISH
    yao_partner_debt_lumen = 8
    bob_partner_debt_lumen = 48
    sue_partner_debt_lumen = 66
    yao_person = personunit_shop(exx.yao)
    yao_person.add_partnerunit(exx.bob, 2, bob_partner_debt_lumen)
    yao_person.add_partnerunit(exx.sue, 2, sue_partner_debt_lumen)
    yao_person.add_partnerunit(exx.yao, 2, yao_partner_debt_lumen)

    # WHEN
    yao_doctorledger = get_doctorledger(yao_person)

    # THEN
    assert len(yao_doctorledger) == 3
    assert yao_doctorledger.get(exx.bob) == bob_partner_debt_lumen
    assert yao_doctorledger.get(exx.sue) == sue_partner_debt_lumen
    assert yao_doctorledger.get(exx.yao) == yao_partner_debt_lumen


def test_get_doctorledger_ReturnsObjWithNoEmpty_partner_debt_lumen():
    # ESTABLISH
    yao_partner_debt_lumen = 8
    bob_partner_debt_lumen = 48
    sue_partner_debt_lumen = 0
    yao_person = personunit_shop(exx.yao)
    yao_person.add_partnerunit(exx.bob, 2, bob_partner_debt_lumen)
    yao_person.add_partnerunit(exx.sue, 2, sue_partner_debt_lumen)
    yao_person.add_partnerunit(exx.yao, 2, yao_partner_debt_lumen)

    # WHEN
    yao_doctorledger = get_doctorledger(yao_person)

    # THEN
    assert yao_doctorledger.get(exx.bob) == bob_partner_debt_lumen
    assert yao_doctorledger.get(exx.sue) is None
    assert yao_doctorledger.get(exx.yao) == yao_partner_debt_lumen
    assert len(yao_doctorledger) == 2


def test_RiverRun_set_partner_need_due_SetsAttr(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    bob_riverrun = riverrun_shop(mstr_dir, None, exx.bob)
    assert bob_riverrun.need_dues.get(exx.yao) is None

    # WHEN
    yao_need_due = 7
    bob_riverrun.set_partner_need_due(exx.yao, yao_need_due)

    # THEN
    assert bob_riverrun.need_dues.get(exx.yao) == yao_need_due


def test_RiverRun_need_dues_unpaid_ReturnsObj(temp3_dir):
    # ESTABLISH
    mstr_dir = temp3_dir
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao)
    assert x_riverrun.need_dues_unpaid() is False

    # WHEN
    yao_need_due = 500
    x_riverrun.set_partner_need_due(exx.yao, yao_need_due)
    # THEN
    assert x_riverrun.need_dues_unpaid()

    # WHEN
    x_riverrun.delete_need_due(exx.yao)
    # THEN
    assert x_riverrun.need_dues_unpaid() is False

    # WHEN
    bob_need_due = 300
    x_riverrun.set_partner_need_due(exx.bob, bob_need_due)
    x_riverrun.set_partner_need_due(exx.yao, yao_need_due)
    # THEN
    assert x_riverrun.need_dues_unpaid()

    # WHEN
    x_riverrun.delete_need_due(exx.yao)
    # THEN
    assert x_riverrun.need_dues_unpaid()


def test_RiverRun_set_need_dues_SetsAttr():
    # ESTABLISH
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        person_name=exx.bob,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    bob_partner_debt_lumen = 38
    sue_partner_debt_lumen = 56
    yao_partner_debt_lumen = 6
    bob_person = personunit_shop(exx.bob)
    bob_person.add_partnerunit(exx.bob, 2, bob_partner_debt_lumen)
    bob_person.add_partnerunit(exx.sue, 2, sue_partner_debt_lumen)
    bob_person.add_partnerunit(exx.yao, 2, yao_partner_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_person)
    assert bob_riverrun.need_dues_unpaid() is False

    # WHEN
    bob_riverrun.set_need_dues(bob_doctorledger)

    # THEN
    assert bob_riverrun.need_dues_unpaid()
    bob_riverrun = bob_riverrun.need_dues
    assert bob_riverrun.get(exx.bob) == 380
    assert bob_riverrun.get(exx.sue) == 560
    assert bob_riverrun.get(exx.yao) == 60


def test_RiverRun_partner_has_need_due_ReturnsBool():
    # ESTABLISH
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        person_name=exx.bob,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    yao_partner_debt_lumen = 6
    bob_partner_debt_lumen = 38
    sue_partner_debt_lumen = 56
    bob_person = personunit_shop(exx.bob)
    bob_person.add_partnerunit(exx.bob, 2, bob_partner_debt_lumen)
    bob_person.add_partnerunit(exx.sue, 2, sue_partner_debt_lumen)
    bob_person.add_partnerunit(exx.yao, 2, yao_partner_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_person)
    assert bob_riverrun.partner_has_need_due(exx.bob) is False
    assert bob_riverrun.partner_has_need_due(exx.sue) is False
    assert bob_riverrun.partner_has_need_due(exx.yao) is False
    assert bob_riverrun.partner_has_need_due(exx.zia) is False

    # WHEN
    bob_riverrun.set_need_dues(bob_doctorledger)

    # THEN
    assert bob_riverrun.partner_has_need_due(exx.bob)
    assert bob_riverrun.partner_has_need_due(exx.sue)
    assert bob_riverrun.partner_has_need_due(exx.yao)
    assert bob_riverrun.partner_has_need_due(exx.zia) is False


def test_RiverRun_delete_need_due_SetsAttr():
    # ESTABLISH
    bob_mana_amount = 88
    bob_mana_grain = 11
    bob_riverrun = riverrun_shop(
        None,
        None,
        person_name=exx.bob,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    bob_riverrun.set_partner_need_due(exx.yao, 5)
    assert bob_riverrun.partner_has_need_due(exx.yao)

    # WHEN
    bob_riverrun.delete_need_due(exx.yao)

    # THEN
    assert bob_riverrun.partner_has_need_due(exx.yao) is False


def test_RiverRun_get_partner_need_due_ReturnsObj():
    # ESTABLISH
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        person_name=exx.bob,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    bob_partner_debt_lumen = 38
    sue_partner_debt_lumen = 56
    yao_partner_debt_lumen = 6
    bob_person = personunit_shop(exx.bob)
    bob_person.add_partnerunit(exx.bob, 2, bob_partner_debt_lumen)
    bob_person.add_partnerunit(exx.sue, 2, sue_partner_debt_lumen)
    bob_person.add_partnerunit(exx.yao, 2, yao_partner_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_person)
    assert bob_riverrun.partner_has_need_due(exx.bob) is False
    assert bob_riverrun.get_partner_need_due(exx.bob) == 0
    assert bob_riverrun.partner_has_need_due(exx.zia) is False
    assert bob_riverrun.get_partner_need_due(exx.zia) == 0

    # WHEN
    bob_riverrun.set_need_dues(bob_doctorledger)

    # THEN
    assert bob_riverrun.partner_has_need_due(exx.bob)
    assert bob_riverrun.get_partner_need_due(exx.bob) == 380
    assert bob_riverrun.partner_has_need_due(exx.zia) is False
    assert bob_riverrun.get_partner_need_due(exx.zia) == 0


def test_RiverRun_levy_need_due_SetsAttr_ScenarioX():
    # ESTABLISH
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        person_name=exx.bob,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    bob_partner_debt_lumen = 38
    sue_partner_debt_lumen = 56
    yao_partner_debt_lumen = 6
    bob_person = personunit_shop(exx.bob)
    bob_person.add_partnerunit(exx.bob, 2, bob_partner_debt_lumen)
    bob_person.add_partnerunit(exx.sue, 2, sue_partner_debt_lumen)
    bob_person.add_partnerunit(exx.yao, 2, yao_partner_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_person)
    bob_riverrun.set_need_dues(bob_doctorledger)
    assert bob_riverrun.get_partner_need_due(exx.bob) == 380, 0

    # WHEN / THEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.bob, 5)
    assert excess_carer_points == 0
    assert need_got == 5
    assert bob_riverrun.get_partner_need_due(exx.bob) == 375

    # WHEN /THEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.bob, 375)
    assert excess_carer_points == 0
    assert need_got == 375
    assert bob_riverrun.get_partner_need_due(exx.bob) == 0
    assert bob_riverrun.partner_has_need_due(exx.bob) is False

    # WHEN / THEN
    assert bob_riverrun.get_partner_need_due(exx.sue) == 560
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.sue, 1000)
    assert excess_carer_points == 440
    assert need_got == 560
    assert bob_riverrun.get_partner_need_due(exx.sue) == 0
    assert bob_riverrun.need_dues.get(exx.sue) is None

    # WHEN / THEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.zia, 1000)
    assert excess_carer_points == 1000
    assert need_got == 0
    assert bob_riverrun.get_partner_need_due(exx.zia) == 0

    # WHEN / THEN
    assert bob_riverrun.get_partner_need_due(exx.yao) == 60
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.yao, 81)
    assert excess_carer_points == 21
    assert need_got == 60
    assert bob_riverrun.get_partner_need_due(exx.yao) == 0
