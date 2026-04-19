from ch02_contact.contact import (
    contactunit_get_from_dict,
    contactunit_shop,
    contactunits_get_from_dict,
)
from ch02_contact.group import membership_shop
from ref.keywords import Ch02Keywords as kw, ExampleStrs as exx


def test_ContactUnit_get_memberships_dict_ReturnsObj():
    # ESTABLISH
    sue_group_cred_lumen = 11
    sue_group_debt_lumen = 13
    run_group_cred_lumen = 17
    run_group_debt_lumen = 23
    sue_membership = membership_shop(
        exx.sue, sue_group_cred_lumen, sue_group_debt_lumen
    )
    run_membership = membership_shop(
        exx.run, run_group_cred_lumen, run_group_debt_lumen
    )
    sue_contactunit = contactunit_shop(exx.sue)
    sue_contactunit.set_membership(sue_membership)
    sue_contactunit.set_membership(run_membership)

    # WHEN
    sue_memberships_dict = sue_contactunit.get_memberships_dict()

    # THEN
    assert sue_memberships_dict.get(exx.sue) is not None
    assert sue_memberships_dict.get(exx.run) is not None
    sue_membership_dict = sue_memberships_dict.get(exx.sue)
    run_membership_dict = sue_memberships_dict.get(exx.run)
    assert sue_membership_dict == {
        kw.group_title: exx.sue,
        kw.group_cred_lumen: sue_group_cred_lumen,
        kw.group_debt_lumen: sue_group_debt_lumen,
    }
    assert run_membership_dict == {
        kw.group_title: exx.run,
        kw.group_cred_lumen: run_group_cred_lumen,
        kw.group_debt_lumen: run_group_debt_lumen,
    }


def test_ContactUnit_to_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_contactunit = contactunit_shop(exx.bob)

    bob_contact_cred_lumen = 13
    bob_contact_debt_lumen = 17
    bob_contactunit.set_contact_cred_lumen(bob_contact_cred_lumen)
    bob_contactunit.set_contact_debt_lumen(bob_contact_debt_lumen)

    print(f"{exx.bob}")

    bob_contactunit.set_membership(membership_shop(exx.bob))
    bob_contactunit.set_membership(membership_shop(exx.run))

    # WHEN
    x_dict = bob_contactunit.to_dict()

    # THEN
    bl_dict = x_dict.get("memberships")
    print(f"{bl_dict=}")
    assert x_dict is not None
    assert x_dict == {
        kw.contact_name: exx.bob,
        kw.contact_cred_lumen: bob_contact_cred_lumen,
        kw.contact_debt_lumen: bob_contact_debt_lumen,
        kw.memberships: {
            exx.bob: {
                kw.group_title: exx.bob,
                kw.group_cred_lumen: 1,
                kw.group_debt_lumen: 1,
            },
            exx.run: {
                kw.group_title: exx.run,
                kw.group_cred_lumen: 1,
                kw.group_debt_lumen: 1,
            },
        },
    }


def test_ContactUnit_to_dict_ReturnsDictWithAllAttrDataForJSON():
    # ESTABLISH
    bob_contactunit = contactunit_shop(exx.bob)

    bob_contact_cred_lumen = 13
    bob_contact_debt_lumen = 17
    bob_contactunit.set_contact_cred_lumen(bob_contact_cred_lumen)
    bob_contactunit.set_contact_debt_lumen(bob_contact_debt_lumen)
    bob_irrational_contact_debt_lumen = 87
    bob_inallocable_contact_debt_lumen = 97
    bob_contactunit.add_irrational_contact_debt_lumen(bob_irrational_contact_debt_lumen)
    bob_contactunit.add_inallocable_contact_debt_lumen(
        bob_inallocable_contact_debt_lumen
    )

    bob_fund_give = 55
    bob_fund_take = 47
    bob_fund_agenda_give = 51
    bob_fund_agenda_take = 67
    bob_fund_agenda_ratio_give = 71
    bob_fund_agenda_ratio_take = 73

    bob_contactunit.fund_give = bob_fund_give
    bob_contactunit.fund_take = bob_fund_take
    bob_contactunit.fund_agenda_give = bob_fund_agenda_give
    bob_contactunit.fund_agenda_take = bob_fund_agenda_take
    bob_contactunit.fund_agenda_ratio_give = bob_fund_agenda_ratio_give
    bob_contactunit.fund_agenda_ratio_take = bob_fund_agenda_ratio_take

    bob_contactunit.set_membership(membership_shop(exx.bob))
    bob_contactunit.set_membership(membership_shop(exx.run))

    print(f"{exx.bob}")

    # WHEN
    x_dict = bob_contactunit.to_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict is not None
    assert x_dict == {
        kw.contact_name: exx.bob,
        kw.contact_cred_lumen: bob_contact_cred_lumen,
        kw.contact_debt_lumen: bob_contact_debt_lumen,
        kw.memberships: bob_contactunit.get_memberships_dict(),
        kw.irrational_contact_debt_lumen: bob_irrational_contact_debt_lumen,
        kw.inallocable_contact_debt_lumen: bob_inallocable_contact_debt_lumen,
        kw.fund_give: bob_fund_give,
        kw.fund_take: bob_fund_take,
        kw.fund_agenda_give: bob_fund_agenda_give,
        kw.fund_agenda_take: bob_fund_agenda_take,
        kw.fund_agenda_ratio_give: bob_fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take: bob_fund_agenda_ratio_take,
    }


def test_ContactUnit_to_dict_ReturnsDictWith_irrational_contact_debt_lumen_ValuesIsZero():
    # ESTABLISH
    bob_contactunit = contactunit_shop(exx.bob)
    assert bob_contactunit.irrational_contact_debt_lumen == 0
    assert bob_contactunit.inallocable_contact_debt_lumen == 0

    # WHEN
    x_dict = bob_contactunit.to_dict(all_attrs=True)

    # THEN
    assert x_dict.get(kw.irrational_contact_debt_lumen) is None
    assert x_dict.get(kw.inallocable_contact_debt_lumen) is None
    assert len(x_dict.keys()) == 10


def test_ContactUnit_to_dict_ReturnsDictWith_irrational_contact_debt_lumen_ValuesIsNumber():
    # ESTABLISH
    bob_contactunit = contactunit_shop(exx.bob)
    bob_irrational_contact_debt_lumen = 87
    bob_inallocable_contact_debt_lumen = 97
    bob_contactunit.add_irrational_contact_debt_lumen(bob_irrational_contact_debt_lumen)
    bob_contactunit.add_inallocable_contact_debt_lumen(
        bob_inallocable_contact_debt_lumen
    )

    # WHEN
    x_dict = bob_contactunit.to_dict(all_attrs=True)

    # THEN
    assert (
        x_dict.get(kw.irrational_contact_debt_lumen)
        == bob_irrational_contact_debt_lumen
    )
    assert (
        x_dict.get(kw.inallocable_contact_debt_lumen)
        == bob_inallocable_contact_debt_lumen
    )
    assert len(x_dict.keys()) == 12


def test_ContactUnit_to_dict_ReturnsDictWith_irrational_contact_debt_lumen_ValuesIsNone():
    # ESTABLISH
    bob_contactunit = contactunit_shop(exx.bob)
    bob_contactunit.irrational_contact_debt_lumen = None
    bob_contactunit.inallocable_contact_debt_lumen = None

    # WHEN
    x_dict = bob_contactunit.to_dict(all_attrs=True)

    # THEN
    assert x_dict.get(kw.irrational_contact_debt_lumen) is None
    assert x_dict.get(kw.inallocable_contact_debt_lumen) is None
    assert len(x_dict.keys()) == 10


def test_contactunit_get_from_dict_ReturnsObjWith_groupmark():
    # ESTABLISH
    yao_str = ",Yao"
    before_yao_contactunit = contactunit_shop(yao_str, groupmark=exx.slash)
    yao_dict = before_yao_contactunit.to_dict()

    # WHEN
    after_yao_contactunit = contactunit_get_from_dict(yao_dict, exx.slash)

    # THEN
    assert before_yao_contactunit == after_yao_contactunit
    assert after_yao_contactunit.groupmark == exx.slash


def test_contactunit_get_from_dict_Returns_memberships():
    # ESTABLISH
    yao_str = ",Yao"
    before_yao_contactunit = contactunit_shop(yao_str, groupmark=exx.slash)
    ohio_str = f"{exx.slash}ohio"
    iowa_str = f"{exx.slash}iowa"
    ohio_group_cred_lumen = 90
    ohio_group_debt_lumen = 901
    iowa_group_cred_lumen = 902
    iowa_group_debt_lumen = 903
    ohio_membership = membership_shop(
        ohio_str, ohio_group_cred_lumen, ohio_group_debt_lumen
    )
    iowa_membership = membership_shop(
        iowa_str, iowa_group_cred_lumen, iowa_group_debt_lumen
    )
    before_yao_contactunit.set_membership(ohio_membership)
    before_yao_contactunit.set_membership(iowa_membership)
    yao_dict = before_yao_contactunit.to_dict()

    # WHEN
    after_yao_contactunit = contactunit_get_from_dict(yao_dict, exx.slash)

    # THEN
    assert before_yao_contactunit.memberships == after_yao_contactunit.memberships
    assert before_yao_contactunit == after_yao_contactunit
    assert after_yao_contactunit.groupmark == exx.slash


def test_contactunits_get_from_dict_ReturnsObj_Scenario0_With_groupmark():
    # ESTABLISH
    yao_str = ",Yao"
    yao_contactunit = contactunit_shop(yao_str, groupmark=exx.slash)
    yao_dict = yao_contactunit.to_dict()
    x_contactunits_dict = {yao_str: yao_dict}

    # WHEN
    x_contactunits_objs = contactunits_get_from_dict(x_contactunits_dict, exx.slash)

    # THEN
    assert x_contactunits_objs.get(yao_str) == yao_contactunit
    assert x_contactunits_objs.get(yao_str).groupmark == exx.slash


def test_contactunits_get_from_dict_ReturnsObj_Scenario1_SimpleExampleWith_IncompleteData():
    # ESTABLISH
    yao_contact_cred_lumen = 13
    yao_contact_debt_lumen = 17
    yao_irrational_contact_debt_lumen = 87
    yao_inallocable_contact_debt_lumen = 97
    yao_contactunits_dict = {
        exx.yao: {
            kw.contact_name: exx.yao,
            kw.contact_cred_lumen: yao_contact_cred_lumen,
            kw.contact_debt_lumen: yao_contact_debt_lumen,
            kw.memberships: {},
            kw.irrational_contact_debt_lumen: yao_irrational_contact_debt_lumen,
            kw.inallocable_contact_debt_lumen: yao_inallocable_contact_debt_lumen,
        }
    }

    # WHEN
    yao_obj_dict = contactunits_get_from_dict(yao_contactunits_dict)

    # THEN
    assert yao_obj_dict[exx.yao] is not None
    yao_contactunit = yao_obj_dict[exx.yao]

    assert yao_contactunit.contact_name == exx.yao
    assert yao_contactunit.contact_cred_lumen == yao_contact_cred_lumen
    assert yao_contactunit.contact_debt_lumen == yao_contact_debt_lumen
    assert (
        yao_contactunit.irrational_contact_debt_lumen
        == yao_irrational_contact_debt_lumen
    )
    assert (
        yao_contactunit.inallocable_contact_debt_lumen
        == yao_inallocable_contact_debt_lumen
    )
