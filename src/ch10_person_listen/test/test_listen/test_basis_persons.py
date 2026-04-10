from src.ch01_allot.allot import default_pool_num, validate_pool_num
from src.ch02_contact.contact import RespectNum
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch10_person_listen.basis_person import (
    create_empty_person_from_person,
    create_listen_basis,
    get_default_job,
)
from src.ref.keywords import ExampleStrs as exx


def test_create_empty_person_from_person_ReturnsObj():
    # ESTABLISH
    mana_grain_float = 0.7
    yao_gut = personunit_shop(exx.yao, knot=exx.slash, mana_grain=mana_grain_float)
    yao_gut.set_l1_plan(planunit_shop("Iowa"))
    zia_contact_cred_lumen = 47
    zia_contact_debt_lumen = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_gut.add_contactunit(exx.zia, zia_contact_cred_lumen, zia_contact_debt_lumen)
    zia_irrational_contact_debt_lumen = 11
    zia_inallocable_contact_debt_lumen = 22
    duty_zia_contactunit = yao_gut.get_contact(exx.zia)
    duty_zia_contactunit.add_irrational_contact_debt_lumen(
        zia_irrational_contact_debt_lumen
    )
    duty_zia_contactunit.add_inallocable_contact_debt_lumen(
        zia_inallocable_contact_debt_lumen
    )
    zia_contactunit = yao_gut.get_contact(exx.zia)
    zia_contactunit.add_membership(f"{exx.slash}bowlers")
    yao_gut.set_credor_respect(zia_credor_pool)
    yao_gut.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_vision = create_empty_person_from_person(yao_gut, x_person_name=exx.zia)

    # THEN
    assert yao_empty_vision.person_name != yao_gut.person_name
    assert yao_empty_vision.person_name == exx.zia
    assert yao_empty_vision.planroot.get_plan_rope() == yao_gut.planroot.get_plan_rope()
    assert yao_empty_vision.last_lesson_id is None
    assert yao_empty_vision.get_contactunits_dict() == {}
    assert yao_empty_vision.knot == yao_gut.knot
    assert yao_empty_vision.fund_pool == yao_gut.fund_pool
    assert yao_empty_vision.fund_grain == yao_gut.fund_grain
    assert yao_empty_vision.respect_grain == yao_gut.respect_grain
    assert yao_empty_vision.mana_grain == yao_gut.mana_grain
    assert yao_empty_vision.credor_respect != yao_gut.credor_respect
    assert yao_empty_vision.credor_respect == RespectNum(validate_pool_num())
    assert yao_empty_vision.debtor_respect != yao_gut.debtor_respect
    assert yao_empty_vision.debtor_respect == RespectNum(validate_pool_num())
    yao_empty_vision.conpute()
    assert yao_empty_vision.contacts == {}


def test_create_listen_basis_ReturnsObj():
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, knot=exx.slash)
    yao_duty.set_l1_plan(planunit_shop("Iowa"))
    zia_contact_cred_lumen = 47
    zia_contact_debt_lumen = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_contactunit(exx.zia, zia_contact_cred_lumen, zia_contact_debt_lumen)
    zia_irrational_contact_debt_lumen = 11
    zia_inallocable_contact_debt_lumen = 22
    duty_zia_contactunit = yao_duty.get_contact(exx.zia)
    duty_zia_contactunit.add_irrational_contact_debt_lumen(
        zia_irrational_contact_debt_lumen
    )
    duty_zia_contactunit.add_inallocable_contact_debt_lumen(
        zia_inallocable_contact_debt_lumen
    )
    zia_contactunit = yao_duty.get_contact(exx.zia)
    zia_contactunit.add_membership(f"{exx.slash}bowlers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_vision = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_vision.person_name == yao_duty.person_name
    assert (
        yao_basis_vision.planroot.get_plan_rope() == yao_duty.planroot.get_plan_rope()
    )
    assert yao_basis_vision.last_lesson_id == yao_duty.last_lesson_id
    assert yao_basis_vision.get_contactunits_dict() == yao_duty.get_contactunits_dict()
    assert yao_basis_vision.knot == yao_duty.knot
    assert yao_basis_vision.fund_pool == yao_duty.fund_pool
    assert yao_basis_vision.fund_grain == yao_duty.fund_grain
    assert yao_basis_vision.respect_grain == yao_duty.respect_grain
    assert yao_basis_vision.credor_respect == yao_duty.credor_respect
    assert yao_basis_vision.debtor_respect == yao_duty.debtor_respect
    yao_basis_vision.conpute()
    assert len(yao_basis_vision._plan_dict) != len(yao_duty._plan_dict)
    assert len(yao_basis_vision._plan_dict) == 1
    vision_zia_contactunit = yao_basis_vision.get_contact(exx.zia)
    assert (
        yao_basis_vision.get_contactunits_dict().keys()
        == yao_duty.get_contactunits_dict().keys()
    )
    assert vision_zia_contactunit.irrational_contact_debt_lumen == 0
    assert vision_zia_contactunit.inallocable_contact_debt_lumen == 0


def test_get_default_job_ReturnsObj():
    # ESTABLISH
    x_fund_pool = 99000
    x_fund_grain = 80
    x_respect_grain = 5
    sue_contact_pool = 800
    last_lesson_id = 7
    sue_max_tree_traverse = 9
    sue_personunit = personunit_shop(
        exx.sue, exx.a23_slash, exx.slash, x_fund_pool, x_fund_grain, x_respect_grain
    )
    sue_personunit.set_last_lesson_id(last_lesson_id)
    sue_personunit.add_contactunit(exx.bob, 3, 4)
    bob_contactunit = sue_personunit.get_contact(exx.bob)
    bob_contactunit.add_membership(f"{exx.slash}bowlers")
    sue_personunit.set_contact_respect(sue_contact_pool)
    sue_personunit.set_l1_plan(planunit_shop(exx.casa))
    sue_personunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_job = get_default_job(sue_personunit)

    # THEN
    default_job.conpute()
    assert default_job.person_name == sue_personunit.person_name
    assert default_job.person_name == exx.sue
    assert (
        default_job.planroot.get_plan_rope() == sue_personunit.planroot.get_plan_rope()
    )
    assert default_job.planroot.get_plan_rope() == exx.a23_slash
    assert default_job.knot == exx.slash
    assert default_job.fund_pool == sue_contact_pool
    assert default_job.fund_grain == x_fund_grain
    assert default_job.respect_grain == x_respect_grain
    assert default_job.credor_respect == RespectNum(default_pool_num())
    assert default_job.debtor_respect == RespectNum(default_pool_num())
    assert default_job.max_tree_traverse == sue_max_tree_traverse
    assert len(default_job.get_contactunits_dict()) == 1
    assert len(default_job._plan_dict) == 1
