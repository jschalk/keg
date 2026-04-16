from src.ch07_person_logic.person_main import personunit_shop
from src.ch24_person_viewer.person_viewer_tool import (
    add_small_dot,
    get_contacts_view_dict,
)
from src.ref.keywords import Ch24Keywords as kw, ExampleStrs as exx


def test_get_contacts_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_believer = personunit_shop(exx.sue)
    sue_believer.conpute()

    # WHEN
    contacts_view_dict = get_contacts_view_dict(sue_believer)

    # THEN
    assert contacts_view_dict == {}


def add_readable(str: str) -> str:
    return f"{str}_{kw.readable}"


def test_get_contacts_view_dict_ReturnsObj_Scenario1_contacts():
    # ESTABLISH
    sue_believer = personunit_shop(exx.sue)
    yao_cred_lumen = 110
    yao_debt_lumen = 130
    bob_cred_lumen = 230
    bob_debt_lumen = 290
    sue_believer.add_contactunit(exx.yao, yao_cred_lumen, yao_debt_lumen)
    sue_believer.add_contactunit(exx.bob, bob_cred_lumen, bob_debt_lumen)
    sue_believer.conpute()

    # WHEN
    contacts_view_dict = get_contacts_view_dict(sue_believer)

    # THEN
    assert set(contacts_view_dict.keys()) == {exx.yao, exx.bob}
    yao_contact_dict = contacts_view_dict.get(exx.yao)
    contact_cred_lumen_readable_key = add_readable(kw.contact_cred_lumen)
    contact_debt_lumen_readable_key = add_readable(kw.contact_debt_lumen)
    memberships_readable_key = add_readable(kw.memberships)
    credor_pool_readable_key = add_readable(kw.credor_pool)
    debtor_pool_readable_key = add_readable(kw.debtor_pool)
    irrational_contact_debt_lumen_readable_key = add_readable(
        kw.irrational_contact_debt_lumen
    )
    inallocable_contact_debt_lumen_readable_key = add_readable(
        kw.inallocable_contact_debt_lumen
    )
    fund_give_readable_key = add_readable(kw.fund_give)
    fund_take_readable_key = add_readable(kw.fund_take)
    fund_agenda_give_readable_key = add_readable(kw.fund_agenda_give)
    fund_agenda_take_readable_key = add_readable(kw.fund_agenda_take)
    fund_agenda_ratio_give_readable_key = add_readable(kw.fund_agenda_ratio_give)
    fund_agenda_ratio_take_readable_key = add_readable(kw.fund_agenda_ratio_take)

    assert set(yao_contact_dict.keys()) == {
        kw.contact_name,
        kw.contact_cred_lumen,
        kw.contact_debt_lumen,
        kw.memberships,
        kw.credor_pool,
        kw.debtor_pool,
        kw.irrational_contact_debt_lumen,
        kw.inallocable_contact_debt_lumen,
        kw.fund_give,
        kw.fund_take,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        contact_cred_lumen_readable_key,
        contact_debt_lumen_readable_key,
        memberships_readable_key,
        credor_pool_readable_key,
        debtor_pool_readable_key,
        irrational_contact_debt_lumen_readable_key,
        inallocable_contact_debt_lumen_readable_key,
        fund_give_readable_key,
        fund_take_readable_key,
        fund_agenda_give_readable_key,
        fund_agenda_take_readable_key,
        fund_agenda_ratio_give_readable_key,
        fund_agenda_ratio_take_readable_key,
    }
    ypu = sue_believer.get_contact(exx.yao)
    yp_dict = yao_contact_dict
    assert ypu.contact_name == yp_dict.get(kw.contact_name)
    assert ypu.contact_cred_lumen == yp_dict.get(kw.contact_cred_lumen)
    assert ypu.contact_debt_lumen == yp_dict.get(kw.contact_debt_lumen)
    assert ypu.credor_pool == yp_dict.get(kw.credor_pool)
    assert ypu.debtor_pool == yp_dict.get(kw.debtor_pool)
    assert ypu.irrational_contact_debt_lumen == yp_dict.get(
        kw.irrational_contact_debt_lumen
    )
    assert ypu.inallocable_contact_debt_lumen == yp_dict.get(
        kw.inallocable_contact_debt_lumen
    )
    assert ypu.fund_give == yp_dict.get(kw.fund_give)
    assert ypu.fund_take == yp_dict.get(kw.fund_take)
    assert ypu.fund_agenda_give == yp_dict.get(kw.fund_agenda_give)
    assert ypu.fund_agenda_take == yp_dict.get(kw.fund_agenda_take)
    assert ypu.fund_agenda_ratio_give == yp_dict.get(kw.fund_agenda_ratio_give)
    assert ypu.fund_agenda_ratio_take == yp_dict.get(kw.fund_agenda_ratio_take)

    expected_contact_cred_lumen_readable = (
        f"contact_cred_lumen: {ypu.contact_cred_lumen}"
    )
    expected_contact_debt_lumen_readable = (
        f"contact_debt_lumen: {ypu.contact_debt_lumen}"
    )
    expected_memberships_readable = f"memberships: {ypu.memberships}"
    expected_credor_pool_readable = f"credor_pool: {ypu.credor_pool}"
    expected_debtor_pool_readable = f"debtor_pool: {ypu.debtor_pool}"
    expected_irrational_contact_debt_lumen_readable = (
        f"irrational_contact_debt_lumen: {ypu.irrational_contact_debt_lumen}"
    )
    expected_inallocable_contact_debt_lumen_readable = (
        f"inallocable_contact_debt_lumen: {ypu.inallocable_contact_debt_lumen}"
    )
    expected_fund_give_readable = f"fund_give: {ypu.fund_give}"
    expected_fund_take_readable = f"fund_take: {ypu.fund_take}"
    expected_fund_agenda_give_readable = f"fund_agenda_give: {ypu.fund_agenda_give}"
    expected_fund_agenda_take_readable = f"fund_agenda_take: {ypu.fund_agenda_take}"
    expected_fund_agenda_ratio_give_readable = (
        f"fund_agenda_ratio_give: {ypu.fund_agenda_ratio_give}"
    )
    expected_fund_agenda_ratio_take_readable = (
        f"fund_agenda_ratio_take: {ypu.fund_agenda_ratio_take}"
    )

    assert (
        yp_dict.get(contact_cred_lumen_readable_key)
        == expected_contact_cred_lumen_readable
    )
    assert (
        yp_dict.get(contact_debt_lumen_readable_key)
        == expected_contact_debt_lumen_readable
    )
    assert yp_dict.get(memberships_readable_key) == expected_memberships_readable
    assert yp_dict.get(credor_pool_readable_key) == expected_credor_pool_readable
    assert yp_dict.get(debtor_pool_readable_key) == expected_debtor_pool_readable
    assert (
        yp_dict.get(irrational_contact_debt_lumen_readable_key)
        == expected_irrational_contact_debt_lumen_readable
    )
    assert (
        yp_dict.get(inallocable_contact_debt_lumen_readable_key)
        == expected_inallocable_contact_debt_lumen_readable
    )
    assert yp_dict.get(fund_give_readable_key) == expected_fund_give_readable
    assert yp_dict.get(fund_take_readable_key) == expected_fund_take_readable
    assert (
        yp_dict.get(fund_agenda_give_readable_key) == expected_fund_agenda_give_readable
    )
    assert (
        yp_dict.get(fund_agenda_take_readable_key) == expected_fund_agenda_take_readable
    )
    assert (
        yp_dict.get(fund_agenda_ratio_give_readable_key)
        == expected_fund_agenda_ratio_give_readable
    )
    assert (
        yp_dict.get(fund_agenda_ratio_take_readable_key)
        == expected_fund_agenda_ratio_take_readable
    )


def test_get_contacts_view_dict_ReturnsObj_Scenario2_memberships():
    # ESTABLISH
    sue_believer = personunit_shop(exx.sue)
    sue_believer.add_contactunit(exx.yao)
    bowlers_str = ";bowlers"
    yao_bowl_cred_lumen = 311
    yao_bowl_debt_lumen = 313
    yao_contactunit = sue_believer.get_contact(exx.yao)
    yao_contactunit.add_membership(
        bowlers_str, yao_bowl_cred_lumen, yao_bowl_debt_lumen
    )
    sue_believer.conpute()

    # WHEN
    contacts_view_dict = get_contacts_view_dict(sue_believer)

    # THEN
    assert set(contacts_view_dict.keys()) == {exx.yao}
    yao_contact_dict = contacts_view_dict.get(exx.yao)
    assert kw.memberships in set(yao_contact_dict.keys())
    yao_memberships_dict = yao_contact_dict.get(kw.memberships)
    assert {bowlers_str, exx.yao} == set(yao_memberships_dict.keys())
    yao_bowl_dict = yao_memberships_dict.get(bowlers_str)

    group_title_readable_key = add_readable(kw.group_title)
    group_cred_lumen_readable_key = add_readable(kw.group_cred_lumen)
    group_debt_lumen_readable_key = add_readable(kw.group_debt_lumen)
    credor_pool_readable_key = add_readable(kw.credor_pool)
    debtor_pool_readable_key = add_readable(kw.debtor_pool)
    fund_agenda_give_readable_key = add_readable(kw.fund_agenda_give)
    fund_agenda_ratio_give_readable_key = add_readable(kw.fund_agenda_ratio_give)
    fund_agenda_ratio_take_readable_key = add_readable(kw.fund_agenda_ratio_take)
    fund_agenda_take_readable_key = add_readable(kw.fund_agenda_take)
    fund_give_readable_key = add_readable(kw.fund_give)
    fund_take_readable_key = add_readable(kw.fund_take)
    assert set(yao_bowl_dict.keys()) == {
        kw.contact_name,
        kw.group_title,
        kw.group_cred_lumen,
        kw.group_debt_lumen,
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_agenda_take,
        kw.fund_give,
        kw.fund_take,
        group_title_readable_key,
        group_cred_lumen_readable_key,
        group_debt_lumen_readable_key,
        credor_pool_readable_key,
        debtor_pool_readable_key,
        fund_agenda_give_readable_key,
        fund_agenda_ratio_give_readable_key,
        fund_agenda_ratio_take_readable_key,
        fund_agenda_take_readable_key,
        fund_give_readable_key,
        fund_take_readable_key,
    }
    yao_bowl_mu = yao_contactunit.get_membership(bowlers_str)

    expected_group_title_readable = f"{kw.group_title}: {yao_bowl_mu.group_title}"
    expected_group_cred_lumen_readable = (
        f"{kw.group_cred_lumen}: {yao_bowl_mu.group_cred_lumen}"
    )
    expected_group_debt_lumen_readable = (
        f"{kw.group_debt_lumen}: {yao_bowl_mu.group_debt_lumen}"
    )
    expected_credor_pool_readable = f"{kw.credor_pool}: {yao_bowl_mu.credor_pool}"
    expected_debtor_pool_readable = f"{kw.debtor_pool}: {yao_bowl_mu.debtor_pool}"
    expected_fund_agenda_give_readable = (
        f"{kw.fund_agenda_give}: {yao_bowl_mu.fund_agenda_give}"
    )
    expected_fund_agenda_ratio_give_readable = (
        f"{kw.fund_agenda_ratio_give}: {yao_bowl_mu.fund_agenda_ratio_give}"
    )
    expected_fund_agenda_ratio_take_readable = (
        f"{kw.fund_agenda_ratio_take}: {yao_bowl_mu.fund_agenda_ratio_take}"
    )
    expected_fund_agenda_take_readable = (
        f"{kw.fund_agenda_take}: {yao_bowl_mu.fund_agenda_take}"
    )
    expected_fund_give_readable = f"{kw.fund_give}: {yao_bowl_mu.fund_give}"
    expected_fund_take_readable = f"{kw.fund_take}: {yao_bowl_mu.fund_take}"

    expected_group_title_readable = add_small_dot(expected_group_title_readable)
    expected_group_cred_lumen_readable = add_small_dot(
        expected_group_cred_lumen_readable
    )
    expected_group_debt_lumen_readable = add_small_dot(
        expected_group_debt_lumen_readable
    )
    expected_credor_pool_readable = add_small_dot(expected_credor_pool_readable)
    expected_debtor_pool_readable = add_small_dot(expected_debtor_pool_readable)
    expected_fund_agenda_give_readable = add_small_dot(
        expected_fund_agenda_give_readable
    )
    expected_fund_agenda_ratio_give_readable = add_small_dot(
        expected_fund_agenda_ratio_give_readable
    )
    expected_fund_agenda_ratio_take_readable = add_small_dot(
        expected_fund_agenda_ratio_take_readable
    )
    expected_fund_agenda_take_readable = add_small_dot(
        expected_fund_agenda_take_readable
    )
    expected_fund_give_readable = add_small_dot(expected_fund_give_readable)
    expected_fund_take_readable = add_small_dot(expected_fund_take_readable)

    assert yao_bowl_dict.get(kw.contact_name) == yao_bowl_mu.contact_name
    assert yao_bowl_dict.get(kw.group_title) == yao_bowl_mu.group_title
    assert yao_bowl_dict.get(kw.group_cred_lumen) == yao_bowl_mu.group_cred_lumen
    assert yao_bowl_dict.get(kw.group_debt_lumen) == yao_bowl_mu.group_debt_lumen
    assert yao_bowl_dict.get(kw.credor_pool) == yao_bowl_mu.credor_pool
    assert yao_bowl_dict.get(kw.debtor_pool) == yao_bowl_mu.debtor_pool
    assert yao_bowl_dict.get(kw.fund_agenda_give) == yao_bowl_mu.fund_agenda_give
    assert (
        yao_bowl_dict.get(kw.fund_agenda_ratio_give)
        == yao_bowl_mu.fund_agenda_ratio_give
    )
    assert (
        yao_bowl_dict.get(kw.fund_agenda_ratio_take)
        == yao_bowl_mu.fund_agenda_ratio_take
    )
    assert yao_bowl_dict.get(kw.fund_agenda_take) == yao_bowl_mu.fund_agenda_take
    assert yao_bowl_dict.get(kw.fund_give) == yao_bowl_mu.fund_give
    assert yao_bowl_dict.get(kw.fund_take) == yao_bowl_mu.fund_take
    assert yao_bowl_dict.get(group_title_readable_key) == expected_group_title_readable
    assert (
        yao_bowl_dict.get(group_cred_lumen_readable_key)
        == expected_group_cred_lumen_readable
    )
    assert (
        yao_bowl_dict.get(group_debt_lumen_readable_key)
        == expected_group_debt_lumen_readable
    )
    assert yao_bowl_dict.get(credor_pool_readable_key) == expected_credor_pool_readable
    assert yao_bowl_dict.get(debtor_pool_readable_key) == expected_debtor_pool_readable
    assert (
        yao_bowl_dict.get(fund_agenda_give_readable_key)
        == expected_fund_agenda_give_readable
    )
    assert (
        yao_bowl_dict.get(fund_agenda_ratio_give_readable_key)
        == expected_fund_agenda_ratio_give_readable
    )
    assert (
        yao_bowl_dict.get(fund_agenda_ratio_take_readable_key)
        == expected_fund_agenda_ratio_take_readable
    )
    assert (
        yao_bowl_dict.get(fund_agenda_take_readable_key)
        == expected_fund_agenda_take_readable
    )
    assert yao_bowl_dict.get(fund_give_readable_key) == expected_fund_give_readable
    assert yao_bowl_dict.get(fund_take_readable_key) == expected_fund_take_readable

    # sue_believer = personunit_shop(exx.sue)
    # exx.yao = exx.yao
    # exx.bob = "Bob"
    # yao_cred_lumen = 110
    # yao_debt_lumen = 130
    # bob_cred_lumen = 230
    # bob_debt_lumen = 290
    # sue_believer.add_contactunit(exx.yao, yao_cred_lumen, yao_debt_lumen)
    # sue_believer.add_contactunit(exx.bob, bob_cred_lumen, bob_debt_lumen)
    # bowlers_str = ";bowlers"
    # yao_bowl_cred_lumen = 311
    # yao_bowl_debt_lumen = 313
    # bob_bowl_cred_lumen = 411
    # bob_bowl_debt_lumen = 413
    # clea_str = ";cleaners"
    # cleaners_cred_lumen = 511
    # cleaners_debt_lumen = 513
    # yao_contactunit = sue_believer.get_contact(exx.yao)
    # bob_contactunit = sue_believer.get_contact(exx.bob)
    # bob_contactunit.add_membership(bowlers_str, bob_bowl_cred_lumen, bob_bowl_debt_lumen)
    # yao_contactunit.add_membership(bowlers_str, yao_bowl_cred_lumen, yao_bowl_debt_lumen)
    # yao_contactunit.add_membership(clea_str, cleaners_cred_lumen, cleaners_debt_lumen)
    # sue_believer.get_contact(exx.yao).add_membership()
