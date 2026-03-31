from copy import deepcopy as copy_deepcopy
from src.ch00_py.dict_toolbox import get_empty_list_if_None, get_from_nested_dict
from src.ch02_partner.group import awardunit_shop
from src.ch02_partner.partner import partnerunit_shop
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from src.ch09_person_lesson.delta import PersonDelta, persondelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def print_personatom_keys(x_persondelta: PersonDelta):
    for x_personatom in get_delete_personatom_list(x_persondelta):
        print(f"DELETE {x_personatom.dimen} {list(x_personatom.jkeys.values())}")
    for x_personatom in get_update_personatom_list(x_persondelta):
        print(f"UPDATE {x_personatom.dimen} {list(x_personatom.jkeys.values())}")
    for x_personatom in get_insert_personatom_list(x_persondelta):
        print(f"INSERT {x_personatom.dimen} {list(x_personatom.jkeys.values())}")


def get_delete_personatom_list(x_persondelta: PersonDelta) -> list:
    return get_empty_list_if_None(
        x_persondelta._get_crud_personatoms_list().get(kw.DELETE)
    )


def get_insert_personatom_list(x_persondelta: PersonDelta):
    return get_empty_list_if_None(
        x_persondelta._get_crud_personatoms_list().get(kw.INSERT)
    )


def get_update_personatom_list(x_persondelta: PersonDelta):
    return get_empty_list_if_None(
        x_persondelta._get_crud_personatoms_list().get(kw.UPDATE)
    )


def get_personatom_total_count(x_persondelta: PersonDelta) -> int:
    return (
        len(get_delete_personatom_list(x_persondelta))
        + len(get_insert_personatom_list(x_persondelta))
        + len(get_update_personatom_list(x_persondelta))
    )


def test_PersonDelta_create_personatoms_EmptyPersons():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sue_persondelta = persondelta_shop()
    assert sue_persondelta.personatoms == {}

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(sue_person, sue_person)

    # THEN
    assert sue_persondelta.personatoms == {}


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_partnerunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    after_sue_person = copy_deepcopy(before_sue_person)
    xio_partner_cred_lumen = 33
    xio_partner_debt_lumen = 44
    xio_partnerunit = partnerunit_shop(
        exx.xio, xio_partner_cred_lumen, xio_partner_debt_lumen
    )
    after_sue_person.set_partnerunit(xio_partnerunit, auto_set_membership=False)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    assert (
        len(sue_persondelta.personatoms.get(kw.INSERT).get(kw.person_partnerunit)) == 1
    )
    sue_insert_dict = sue_persondelta.personatoms.get(kw.INSERT)
    sue_partnerunit_dict = sue_insert_dict.get(kw.person_partnerunit)
    xio_personatom = sue_partnerunit_dict.get(exx.xio)
    assert xio_personatom.get_value(kw.partner_name) == exx.xio
    assert xio_personatom.get_value("partner_cred_lumen") == xio_partner_cred_lumen
    assert xio_personatom.get_value("partner_debt_lumen") == xio_partner_debt_lumen

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_partnerunit_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit("Yao")
    before_sue_person.add_partnerunit("Zia")

    after_sue_person = copy_deepcopy(before_sue_person)

    before_sue_person.add_partnerunit(exx.xio)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    xio_personatom = get_from_nested_dict(
        sue_persondelta.personatoms,
        [kw.DELETE, kw.person_partnerunit, exx.xio],
    )
    assert xio_personatom.get_value(kw.partner_name) == exx.xio

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    print_personatom_keys(sue_persondelta)
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_partnerunit_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    after_sue_person = copy_deepcopy(before_sue_person)
    before_sue_person.add_partnerunit(exx.xio)
    xio_partner_cred_lumen = 33
    xio_partner_debt_lumen = 44
    after_sue_person.add_partnerunit(
        exx.xio, xio_partner_cred_lumen, xio_partner_debt_lumen
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    x_keylist = [kw.UPDATE, kw.person_partnerunit, exx.xio]
    xio_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert xio_personatom.get_value(kw.partner_name) == exx.xio
    assert xio_personatom.get_value("partner_cred_lumen") == xio_partner_cred_lumen
    assert xio_personatom.get_value("partner_debt_lumen") == xio_partner_debt_lumen

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_PersonUnit_simple_attrs_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    after_sue_person = copy_deepcopy(before_sue_person)
    x_fund_pool = 8000000
    x_fund_grain = 8
    x_respect_grain = 5
    x_max_tree_traverse = 66
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_person.fund_pool = x_fund_pool
    after_sue_person.fund_grain = x_fund_grain
    after_sue_person.respect_grain = x_respect_grain
    after_sue_person.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_person.set_credor_respect(x_credor_respect)
    after_sue_person.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    x_keylist = [kw.UPDATE, kw.personunit]
    xio_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert xio_personatom.get_value(kw.max_tree_traverse) == x_max_tree_traverse
    assert xio_personatom.get_value(kw.credor_respect) == x_credor_respect
    assert xio_personatom.get_value(kw.debtor_respect) == x_debtor_respect
    assert xio_personatom.get_value(kw.fund_pool) == x_fund_pool
    assert xio_personatom.get_value(kw.fund_grain) == x_fund_grain
    assert xio_personatom.get_value(kw.respect_grain) == x_respect_grain

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_partner_membership_insert():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    after_sue_person = copy_deepcopy(before_sue_person)
    temp_yao_partnerunit = partnerunit_shop(exx.yao)
    temp_zia_partnerunit = partnerunit_shop(exx.zia)
    after_sue_person.set_partnerunit(temp_yao_partnerunit, auto_set_membership=False)
    after_sue_person.set_partnerunit(temp_zia_partnerunit, auto_set_membership=False)
    after_yao_partnerunit = after_sue_person.get_partner(exx.yao)
    after_zia_partnerunit = after_sue_person.get_partner(exx.zia)
    zia_run_credit_w = 77
    zia_run_debt_w = 88
    after_zia_partnerunit.add_membership(exx.run, zia_run_credit_w, zia_run_debt_w)
    print(f"{after_sue_person.get_partnerunit_group_titles_dict()=}")

    # WHEN
    sue_persondelta = persondelta_shop()
    print(f"{after_sue_person.get_partner(exx.zia).memberships=}")
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)
    # print(f"{sue_persondelta.personatoms.get(kw.INSERT).keys()=}")
    # print(
    #     sue_persondelta.personatoms.get(kw.INSERT).get(kw.person_partner_membership).keys()
    # )

    # THEN
    x_keylist = [kw.INSERT, kw.person_partnerunit, exx.yao]
    yao_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert yao_personatom.get_value(kw.partner_name) == exx.yao

    x_keylist = [kw.INSERT, kw.person_partnerunit, exx.zia]
    zia_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert zia_personatom.get_value(kw.partner_name) == exx.zia
    print(f"\n{sue_persondelta.personatoms=}")
    # print(f"\n{zia_personatom=}")

    x_keylist = [kw.INSERT, kw.person_partner_membership, exx.zia, exx.run]
    run_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert run_personatom.get_value(kw.partner_name) == exx.zia
    assert run_personatom.get_value(kw.group_title) == exx.run
    assert run_personatom.get_value(kw.group_cred_lumen) == zia_run_credit_w
    assert run_personatom.get_value(kw.group_debt_lumen) == zia_run_debt_w

    print_personatom_keys(sue_persondelta)
    print(f"{get_personatom_total_count(sue_persondelta)=}")
    assert len(get_delete_personatom_list(sue_persondelta)) == 0
    assert len(get_insert_personatom_list(sue_persondelta)) == 3
    assert len(get_delete_personatom_list(sue_persondelta)) == 0
    assert get_personatom_total_count(sue_persondelta) == 3


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_partner_membership_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    before_sue_person.add_partnerunit(exx.zia)
    before_xio_credit_w = 77
    before_xio_debt_w = 88
    before_xio_partner = before_sue_person.get_partner(exx.xio)
    before_xio_partner.add_membership(exx.run, before_xio_credit_w, before_xio_debt_w)
    after_sue_person = copy_deepcopy(before_sue_person)
    after_xio_partnerunit = after_sue_person.get_partner(exx.xio)
    after_xio_credit_w = 55
    after_xio_debt_w = 66
    after_xio_partnerunit.add_membership(exx.run, after_xio_credit_w, after_xio_debt_w)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    # x_keylist = [kw.UPDATE, kw.person_partnerunit, exx.xio]
    # xio_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    # assert xio_personatom.get_value(kw.partner_name) == exx.xio
    # print(f"\n{sue_persondelta.personatoms=}")
    # print(f"\n{xio_personatom=}")

    x_keylist = [kw.UPDATE, kw.person_partner_membership, exx.xio, exx.run]
    xio_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert xio_personatom.get_value(kw.partner_name) == exx.xio
    assert xio_personatom.get_value(kw.group_title) == exx.run
    assert xio_personatom.get_value(kw.group_cred_lumen) == after_xio_credit_w
    assert xio_personatom.get_value(kw.group_debt_lumen) == after_xio_debt_w

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_partner_membership_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    before_sue_person.add_partnerunit(exx.zia)
    before_sue_person.add_partnerunit(exx.bob)
    before_xio_partnerunit = before_sue_person.get_partner(exx.xio)
    before_zia_partnerunit = before_sue_person.get_partner(exx.zia)
    before_bob_partnerunit = before_sue_person.get_partner(exx.bob)
    before_xio_partnerunit.add_membership(exx.run)
    before_zia_partnerunit.add_membership(exx.run)
    fly_str = ";flyers"
    before_xio_partnerunit.add_membership(fly_str)
    before_zia_partnerunit.add_membership(fly_str)
    before_bob_partnerunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_person.get_partnerunit_group_titles_dict()

    after_sue_person = copy_deepcopy(before_sue_person)
    after_xio_partnerunit = after_sue_person.get_partner(exx.xio)
    after_zia_partnerunit = after_sue_person.get_partner(exx.zia)
    after_bob_partnerunit = after_sue_person.get_partner(exx.bob)
    after_xio_partnerunit.delete_membership(exx.run)
    after_zia_partnerunit.delete_membership(exx.run)
    after_bob_partnerunit.delete_membership(fly_str)
    after_group_titles_dict = after_sue_person.get_partnerunit_group_titles_dict()
    assert len(before_group_titles_dict.get(fly_str)) == 3
    assert len(before_group_titles_dict.get(exx.run)) == 2
    assert len(after_group_titles_dict.get(fly_str)) == 2
    assert after_group_titles_dict.get(exx.run) is None

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    x_keylist = [kw.DELETE, kw.person_partner_membership, exx.bob, fly_str]
    xio_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert xio_personatom.get_value(kw.partner_name) == exx.bob
    assert xio_personatom.get_value(kw.group_title) == fly_str

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    print_personatom_keys(sue_persondelta)
    assert len(get_delete_personatom_list(sue_persondelta)) == 3
    assert len(get_insert_personatom_list(sue_persondelta)) == 0
    assert len(get_update_personatom_list(sue_persondelta)) == 0
    assert get_personatom_total_count(sue_persondelta) == 3


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_person.make_rope(ball_rope, street_str)
    before_sue_person.set_plan_obj(planunit_shop(street_str), ball_rope)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_person.make_rope(sports_rope, disc_str)
    amy45_str = "amy45"
    before_sue_person.set_l1_plan(planunit_shop(amy45_str))
    before_sue_person.set_plan_obj(planunit_shop(disc_str), sports_rope)
    # create after without ball_plan and street_plan
    after_sue_person = copy_deepcopy(before_sue_person)
    after_sue_person.del_plan_obj(ball_rope)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    x_dimen = kw.person_planunit
    print(f"{sue_persondelta.personatoms.get(kw.DELETE).get(x_dimen).keys()=}")

    x_keylist = [kw.DELETE, kw.person_planunit, street_rope]
    street_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert street_personatom.get_value(kw.plan_rope) == street_rope

    x_keylist = [kw.DELETE, kw.person_planunit, ball_rope]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope

    print(f"{get_personatom_total_count(sue_persondelta)=}")
    assert get_personatom_total_count(sue_persondelta) == 2


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_person.make_rope(ball_rope, street_str)
    before_sue_person.set_plan_obj(planunit_shop(street_str), ball_rope)

    after_sue_person = copy_deepcopy(before_sue_person)
    disc_str = "Ultimate Disc"
    disc_rope = after_sue_person.make_rope(sports_rope, disc_str)
    after_sue_person.set_plan_obj(planunit_shop(disc_str), sports_rope)
    amy45_str = "amy45"
    amy_begin = 34
    amy_close = 78
    amy_star = 55
    amy_pledge = True
    amy_rope = after_sue_person.make_l1_rope(amy45_str)
    after_sue_person.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=amy_begin,
            close=amy_close,
            star=amy_star,
            pledge=amy_pledge,
        )
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print_personatom_keys(sue_persondelta)

    x_keylist = [kw.INSERT, kw.person_planunit, disc_rope]
    street_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert street_personatom.get_value(kw.plan_rope) == disc_rope

    a45_rope = after_sue_person.make_l1_rope(amy45_str)
    x_keylist = [kw.INSERT, kw.person_planunit, a45_rope]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == a45_rope
    assert ball_personatom.get_value(kw.begin) == amy_begin
    assert ball_personatom.get_value(kw.close) == amy_close
    assert ball_personatom.get_value(kw.star) == amy_star
    assert ball_personatom.get_value(kw.pledge) == amy_pledge

    assert get_personatom_total_count(sue_persondelta) == 2


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    amy45_str = "amy45"
    amy45_rope = before_sue_person.make_l1_rope(amy45_str)
    before_amy_begin = 34
    before_amy_close = 78
    before_amy_star = 55
    before_amy_pledge = True
    amy_rope = before_sue_person.make_l1_rope(amy45_str)
    before_sue_person.set_l1_plan(
        planunit_shop(
            amy45_str,
            begin=before_amy_begin,
            close=before_amy_close,
            star=before_amy_star,
            pledge=before_amy_pledge,
        )
    )

    after_sue_person = copy_deepcopy(before_sue_person)
    after_amy_begin = 99
    after_amy_close = 111
    after_amy_star = 22
    after_amy_pledge = False
    after_sue_person.edit_plan_attr(
        amy_rope,
        begin=after_amy_begin,
        close=after_amy_close,
        star=after_amy_star,
        pledge=after_amy_pledge,
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print_personatom_keys(sue_persondelta)

    x_keylist = [kw.UPDATE, kw.person_planunit, amy45_rope]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == amy45_rope
    assert ball_personatom.get_value(kw.begin) == after_amy_begin
    assert ball_personatom.get_value(kw.close) == after_amy_close
    assert ball_personatom.get_value(kw.star) == after_amy_star
    assert ball_personatom.get_value(kw.pledge) == after_amy_pledge

    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_awardunit_delete():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.xio)
    before_sue_au.add_partnerunit(exx.zia)
    before_sue_au.add_partnerunit(exx.bob)
    xio_partnerunit = before_sue_au.get_partner(exx.xio)
    zia_partnerunit = before_sue_au.get_partner(exx.zia)
    bob_partnerunit = before_sue_au.get_partner(exx.bob)
    xio_partnerunit.add_membership(exx.run)
    zia_partnerunit.add_membership(exx.run)
    fly_str = ";flyers"
    xio_partnerunit.add_membership(fly_str)
    zia_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_sue_au.set_plan_obj(planunit_shop(disc_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    before_sue_au.edit_plan_attr(disc_rope, awardunit=awardunit_shop(exx.run))
    before_sue_au.edit_plan_attr(disc_rope, awardunit=awardunit_shop(fly_str))

    after_sue_person = copy_deepcopy(before_sue_au)
    after_sue_person.edit_plan_attr(disc_rope, awardunit_del=exx.run)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_au, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")

    x_keylist = [kw.DELETE, kw.person_plan_awardunit, disc_rope, exx.run]
    run_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert run_personatom.get_value(kw.plan_rope) == disc_rope
    assert run_personatom.get_value(kw.awardee_title) == exx.run

    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_awardunit_insert():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.xio)
    before_sue_au.add_partnerunit(exx.zia)
    before_sue_au.add_partnerunit(exx.bob)
    xio_partnerunit = before_sue_au.get_partner(exx.xio)
    zia_partnerunit = before_sue_au.get_partner(exx.zia)
    bob_partnerunit = before_sue_au.get_partner(exx.bob)
    xio_partnerunit.add_membership(exx.run)
    zia_partnerunit.add_membership(exx.run)
    fly_str = ";flyers"
    xio_partnerunit.add_membership(fly_str)
    zia_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_sue_au.set_plan_obj(planunit_shop(disc_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    before_sue_au.edit_plan_attr(disc_rope, awardunit=awardunit_shop(fly_str))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    after_run_give_force = 44
    after_run_take_force = 66
    x_awardunit = awardunit_shop(exx.run, after_run_give_force, after_run_take_force)
    after_sue_au.edit_plan_attr(disc_rope, awardunit=x_awardunit)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")

    x_keylist = [kw.INSERT, kw.person_plan_awardunit, disc_rope, exx.run]
    run_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert run_personatom.get_value(kw.plan_rope) == disc_rope
    assert run_personatom.get_value(kw.awardee_title) == exx.run
    assert run_personatom.get_value(kw.plan_rope) == disc_rope
    assert run_personatom.get_value(kw.awardee_title) == exx.run
    assert run_personatom.get_value(kw.give_force) == after_run_give_force
    assert run_personatom.get_value(kw.take_force) == after_run_take_force

    assert get_personatom_total_count(sue_persondelta) == 2


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_awardunit_update():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.xio)
    before_sue_au.add_partnerunit(exx.zia)
    xio_partnerunit = before_sue_au.get_partner(exx.xio)
    xio_partnerunit.add_membership(exx.run)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_sue_au.edit_plan_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    run_awardunit = before_sue_au.get_plan_obj(ball_rope).awardunits.get(exx.run)

    after_sue_person = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_person.edit_plan_attr(
        ball_rope,
        awardunit=awardunit_shop(
            awardee_title=exx.run,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_au, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")

    x_keylist = [kw.UPDATE, kw.person_plan_awardunit, ball_rope, exx.run]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.awardee_title) == exx.run
    assert ball_personatom.get_value(kw.give_force) == after_give_force
    assert ball_personatom.get_value(kw.take_force) == after_take_force
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_factunit_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    bend_str = "bendable"
    bend_rope = before_sue_person.make_rope(knee_rope, bend_str)
    before_sue_person.set_plan_obj(planunit_shop(bend_str), knee_rope)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_person.make_rope(knee_rope, damaged_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    before_sue_person.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_fact_lower = 11
    before_fact_upper = 22
    before_fact = factunit_shop(
        knee_rope, bend_rope, before_fact_lower, before_fact_upper
    )
    before_sue_person.edit_plan_attr(ball_rope, factunit=before_fact)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_fact_lower = 55
    after_fact_upper = 66
    knee_fact = factunit_shop(
        knee_rope, damaged_rope, after_fact_lower, after_fact_upper
    )
    after_sue_person.edit_plan_attr(ball_rope, factunit=knee_fact)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")

    x_keylist = [kw.UPDATE, kw.person_plan_factunit, ball_rope, knee_rope]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.fact_context) == knee_rope
    assert ball_personatom.get_value(kw.fact_state) == damaged_rope
    assert ball_personatom.get_value(kw.fact_lower) == after_fact_lower
    assert ball_personatom.get_value(kw.fact_upper) == after_fact_upper
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_factunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_person.make_rope(knee_rope, damaged_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    before_sue_person.set_plan_obj(planunit_shop(damaged_str), knee_rope)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_fact_lower = 55
    after_fact_upper = 66
    after_fact = factunit_shop(
        knee_rope, damaged_rope, after_fact_lower, after_fact_upper
    )
    after_sue_person.edit_plan_attr(ball_rope, factunit=after_fact)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [kw.INSERT, kw.person_plan_factunit, ball_rope, knee_rope]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    print(f"{ball_personatom=}")
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.fact_context) == knee_rope
    assert ball_personatom.get_value(kw.fact_state) == damaged_rope
    assert ball_personatom.get_value(kw.fact_lower) == after_fact_lower
    assert ball_personatom.get_value(kw.fact_upper) == after_fact_upper
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_factunit_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_person.make_rope(knee_rope, damaged_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    before_sue_person.set_plan_obj(planunit_shop(damaged_str), knee_rope)

    after_sue_person = copy_deepcopy(before_sue_person)
    before_damaged_reason_lower = 55
    before_damaged_reason_upper = 66
    before_fact = factunit_shop(
        fact_context=knee_rope,
        fact_state=damaged_rope,
        fact_lower=before_damaged_reason_lower,
        fact_upper=before_damaged_reason_upper,
    )
    before_sue_person.edit_plan_attr(ball_rope, factunit=before_fact)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [kw.DELETE, kw.person_plan_factunit, ball_rope, knee_rope]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.fact_context) == knee_rope
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_reason_caseunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_person.make_rope(knee_rope, damaged_str)
    before_sue_person.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_person.make_rope(knee_rope, bend_str)
    before_sue_person.set_plan_obj(planunit_shop(bend_str), knee_rope)
    before_sue_person.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )

    after_sue_person = copy_deepcopy(before_sue_person)
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    after_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=damaged_reason_lower,
        reason_upper=damaged_reason_upper,
        reason_divisor=damaged_reason_divisor,
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.person_plan_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.reason_context) == knee_rope
    assert ball_personatom.get_value(kw.reason_state) == damaged_rope
    assert ball_personatom.get_value(kw.reason_lower) == damaged_reason_lower
    assert ball_personatom.get_value(kw.reason_upper) == damaged_reason_upper
    assert ball_personatom.get_value(kw.reason_divisor) == damaged_reason_divisor
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_reason_caseunit_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_person.make_rope(knee_rope, damaged_str)
    before_sue_person.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_person.make_rope(knee_rope, bend_str)
    before_sue_person.set_plan_obj(planunit_shop(bend_str), knee_rope)
    before_sue_person.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    before_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=damaged_reason_lower,
        reason_upper=damaged_reason_upper,
        reason_divisor=damaged_reason_divisor,
    )
    after_sue_person = copy_deepcopy(before_sue_person)
    after_sue_person.edit_plan_attr(
        ball_rope,
        reason_del_case_reason_context=knee_rope,
        reason_del_case_reason_state=damaged_rope,
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.person_plan_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.reason_context) == knee_rope
    assert ball_personatom.get_value(kw.reason_state) == damaged_rope
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_reason_caseunit_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_person.make_rope(knee_rope, damaged_str)
    before_sue_person.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_person.make_rope(knee_rope, bend_str)
    before_sue_person.set_plan_obj(planunit_shop(bend_str), knee_rope)
    before_sue_person.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )
    before_damaged_reason_lower = 111
    before_damaged_reason_upper = 777
    before_damaged_reason_divisor = 13
    before_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=before_damaged_reason_lower,
        reason_upper=before_damaged_reason_upper,
        reason_divisor=before_damaged_reason_divisor,
    )

    after_sue_person = copy_deepcopy(before_sue_person)
    after_damaged_reason_lower = 333
    after_damaged_reason_upper = 555
    after_damaged_reason_divisor = 78
    after_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=after_damaged_reason_lower,
        reason_upper=after_damaged_reason_upper,
        reason_divisor=after_damaged_reason_divisor,
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.UPDATE,
        kw.person_plan_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.reason_context) == knee_rope
    assert ball_personatom.get_value(kw.reason_state) == damaged_rope
    assert ball_personatom.get_value(kw.reason_lower) == after_damaged_reason_lower
    assert ball_personatom.get_value(kw.reason_upper) == after_damaged_reason_upper
    assert ball_personatom.get_value(kw.reason_divisor) == after_damaged_reason_divisor
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_reasonunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_person.make_rope(knee_rope, medical_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    before_sue_person.set_plan_obj(planunit_shop(medical_str), knee_rope)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_medical_active_requisite = False
    after_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=after_medical_active_requisite,
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.person_plan_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)

    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value("reason_context") == medical_rope
    assert (
        ball_personatom.get_value(kw.active_requisite) == after_medical_active_requisite
    )
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_reasonunit_update():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_person.make_rope(knee_rope, medical_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    before_sue_person.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_medical_active_requisite = True
    before_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=before_medical_active_requisite,
    )

    after_sue_person = copy_deepcopy(before_sue_person)
    after_medical_active_requisite = False
    after_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=after_medical_active_requisite,
    )

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.UPDATE,
        kw.person_plan_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value("reason_context") == medical_rope
    assert (
        ball_personatom.get_value(kw.active_requisite) == after_medical_active_requisite
    )
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_reasonunit_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_person.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_person.make_rope(knee_rope, medical_str)
    before_sue_person.set_l1_plan(planunit_shop(knee_str))
    before_sue_person.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_medical_active_requisite = True
    before_sue_person.edit_plan_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=before_medical_active_requisite,
    )

    after_sue_person = copy_deepcopy(before_sue_person)
    after_ball_plan = after_sue_person.get_plan_obj(ball_rope)
    after_ball_plan.del_reasonunit_reason_context(medical_rope)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.person_plan_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value("reason_context") == medical_rope
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_laborunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_ball_planunit = after_sue_person.get_plan_obj(ball_rope)
    after_ball_planunit.workforceunit.add_labor(exx.xio)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.person_plan_laborunit,
        ball_rope,
        exx.xio,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.labor_title) == exx.xio
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_laborunit_delete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_person.get_plan_obj(ball_rope)
    before_ball_planunit.workforceunit.add_labor(exx.xio)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_ball_planunit = after_sue_person.get_plan_obj(ball_rope)
    after_ball_planunit.workforceunit.del_laborunit(exx.xio)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.person_plan_laborunit,
        ball_rope,
        exx.xio,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.labor_title) == exx.xio
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_healerunit_insert_PlanUnitUpdate():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_ball_planunit = after_sue_person.get_plan_obj(ball_rope)
    after_ball_planunit.healerunit.set_healer_name(exx.xio)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.person_plan_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist)
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.healer_name) == exx.xio
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_healerunit_insert_PlanUnitInsert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)

    after_sue_person = copy_deepcopy(before_sue_person)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    after_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_person.get_plan_obj(ball_rope)
    after_ball_planunit.healerunit.set_healer_name(exx.xio)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.person_plan_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_personatom = get_from_nested_dict(sue_persondelta.personatoms, x_keylist, True)
    assert ball_personatom
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.healer_name) == exx.xio
    assert get_personatom_total_count(sue_persondelta) == 3


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_healerunit_delete_PlanUnitUpdate():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_person.get_plan_obj(ball_rope)
    before_ball_planunit.healerunit.set_healer_name(exx.xio)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_ball_planunit = after_sue_person.get_plan_obj(ball_rope)
    after_ball_planunit.healerunit.del_healer_name(exx.xio)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.person_plan_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_personatom = get_from_nested_dict(
        sue_persondelta.personatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_personatom
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.healer_name) == exx.xio
    assert get_personatom_total_count(sue_persondelta) == 1


def test_PersonDelta_add_all_different_personatoms_Creates_PersonAtom_plan_healerunit_delete_PlanUnitDelete():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_person.make_rope(sports_rope, ball_str)
    before_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_person.get_plan_obj(ball_rope)
    before_ball_planunit.healerunit.set_healer_name(exx.xio)

    after_sue_person = copy_deepcopy(before_sue_person)
    after_sue_person.del_plan_obj(ball_rope)

    # WHEN
    sue_persondelta = persondelta_shop()
    sue_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    # THEN
    print(f"{print_personatom_keys(sue_persondelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.person_plan_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_personatom = get_from_nested_dict(
        sue_persondelta.personatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_personatom
    assert ball_personatom.get_value(kw.plan_rope) == ball_rope
    assert ball_personatom.get_value(kw.healer_name) == exx.xio
    assert get_personatom_total_count(sue_persondelta) == 2


def test_PersonDelta_add_all_personatoms_Creates_PersonAtoms():
    # ESTABLISH

    after_sue_person = personunit_shop(exx.sue)
    temp_xio_partnerunit = partnerunit_shop(exx.xio)
    after_sue_person.set_partnerunit(temp_xio_partnerunit, auto_set_membership=False)
    sports_str = "sports"
    sports_rope = after_sue_person.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = after_sue_person.make_rope(sports_rope, ball_str)
    after_sue_person.set_plan_obj(planunit_shop(ball_str), sports_rope)
    after_ball_planunit = after_sue_person.get_plan_obj(ball_rope)
    after_ball_planunit.workforceunit.add_labor(exx.xio)

    before_sue_person = personunit_shop(exx.sue)
    sue1_persondelta = persondelta_shop()
    sue1_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)
    print(f"{sue1_persondelta.get_ordered_personatoms()}")
    assert len(sue1_persondelta.get_ordered_personatoms()) == 4

    # WHEN
    sue2_persondelta = persondelta_shop()
    sue2_persondelta.add_all_personatoms(after_sue_person)

    # THEN
    assert len(sue2_persondelta.get_ordered_personatoms()) == 4
    assert sue2_persondelta == sue1_persondelta
