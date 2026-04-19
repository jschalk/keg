from ch07_person_logic.person_main import personunit_shop
from ref.keywords import ExampleStrs as exx


def test_create_groupunits_metrics_SetsAttrScenario0():
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.groupunits = None
    assert not sue_personunit.groupunits

    # WHEN
    sue_personunit._create_groupunits_metrics()

    # THEN
    assert sue_personunit.groupunits == {}


def test_create_groupunits_metrics_SetsAttrScenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.add_contactunit(exx.yao)
    yao_contactunit = sue_personunit.get_contact(exx.yao)
    yao_contactunit.add_membership(exx.yao)
    ohio_str = ";Ohio"
    yao_contactunit.add_membership(ohio_str)
    yao_yao_membership = yao_contactunit.get_membership(exx.yao)
    yao_ohio_membership = yao_contactunit.get_membership(ohio_str)
    yao_yao_membership.credor_pool = 66
    yao_yao_membership.debtor_pool = 44
    yao_ohio_membership.credor_pool = 77
    yao_ohio_membership.debtor_pool = 88
    # assert sue_personunit.groupunits == {}

    # WHEN
    sue_personunit._create_groupunits_metrics()

    # THEN
    assert len(sue_personunit.groupunits) == 2
    assert set(sue_personunit.groupunits.keys()) == {exx.yao, ohio_str}
    ohio_groupunit = sue_personunit.get_groupunit(ohio_str)
    assert ohio_groupunit.credor_pool == 77
    assert ohio_groupunit.debtor_pool == 88
    yao_groupunit = sue_personunit.get_groupunit(exx.yao)
    assert yao_groupunit.credor_pool == 66
    assert yao_groupunit.debtor_pool == 44


def test_PersonUnit_set_contactunit_groupunit_respect_ledgers_SetsAttr_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    assert sue_personunit.groupunits == {}

    # WHEN
    sue_personunit._set_contactunit_groupunit_respect_ledgers()

    # THEN
    assert sue_personunit.groupunits == {}


def test_PersonUnit_set_contactunit_groupunit_respect_ledgers_Clears_groupunits():
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.groupunits = "ohio"
    assert sue_personunit.groupunits != {}

    # WHEN
    sue_personunit._set_contactunit_groupunit_respect_ledgers()

    # THEN
    assert sue_personunit.groupunits == {}


def test_PersonUnit_set_contactunit_groupunit_respect_ledgers_SetsAttr_Scenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.add_contactunit(exx.yao)
    yao_contactunit = sue_personunit.get_contact(exx.yao)
    yao_contactunit.add_membership(exx.yao)
    assert yao_contactunit.credor_pool == 0
    assert yao_contactunit.debtor_pool == 0
    assert yao_contactunit.get_membership(exx.yao).credor_pool == 0
    assert yao_contactunit.get_membership(exx.yao).debtor_pool == 0
    # assert sue_personunit.groupunits == {}

    # WHEN
    sue_personunit._set_contactunit_groupunit_respect_ledgers()

    # THEN
    assert yao_contactunit.credor_pool != 0
    assert yao_contactunit.debtor_pool != 0
    assert yao_contactunit.credor_pool == sue_personunit.credor_respect
    assert yao_contactunit.debtor_pool == sue_personunit.debtor_respect
    yao_membership = yao_contactunit.get_membership(exx.yao)
    assert yao_membership.credor_pool != 0
    assert yao_membership.debtor_pool != 0
    assert yao_membership.credor_pool == sue_personunit.credor_respect
    assert yao_membership.debtor_pool == sue_personunit.debtor_respect
    assert yao_membership.credor_pool == 1000000000
    assert yao_membership.debtor_pool == 1000000000
    yao_groupunit = sue_personunit.get_groupunit(exx.yao)
    groupunit_yao_membership = yao_groupunit.get_contact_membership(exx.yao)
    assert yao_membership == groupunit_yao_membership


def test_PersonUnit_set_contactunit_groupunit_respect_ledgers_SetsAttr_Scenario2():
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.add_contactunit(exx.yao)
    yao_contactunit = sue_personunit.get_contact(exx.yao)
    yao_contactunit.add_membership(exx.yao, 1, 4)
    ohio_str = ";Ohio"
    yao_contactunit.add_membership(ohio_str, 3, 1)
    assert yao_contactunit.credor_pool == 0
    assert yao_contactunit.debtor_pool == 0
    assert yao_contactunit.get_membership(exx.yao).credor_pool == 0
    assert yao_contactunit.get_membership(exx.yao).debtor_pool == 0

    # WHEN
    sue_personunit._set_contactunit_groupunit_respect_ledgers()

    # THEN
    assert sue_personunit.get_contact(exx.yao).credor_pool != 0
    assert sue_personunit.get_contact(exx.yao).debtor_pool != 0
    assert yao_contactunit.get_membership(exx.yao).credor_pool != 0
    assert yao_contactunit.get_membership(exx.yao).debtor_pool != 0
    yao_yao_membership = yao_contactunit.get_membership(exx.yao)
    assert yao_yao_membership.credor_pool != 0
    assert yao_yao_membership.debtor_pool != 0
    assert yao_yao_membership.credor_pool == sue_personunit.credor_respect * 0.25
    assert yao_yao_membership.debtor_pool == sue_personunit.debtor_respect * 0.8
    assert yao_yao_membership.credor_pool == 250000000
    assert yao_yao_membership.debtor_pool == 800000000
    yao_ohio_membership = yao_contactunit.get_membership(ohio_str)
    assert yao_ohio_membership.credor_pool != 0
    assert yao_ohio_membership.debtor_pool != 0
    assert yao_ohio_membership.credor_pool == sue_personunit.credor_respect * 0.75
    assert yao_ohio_membership.debtor_pool == sue_personunit.debtor_respect * 0.2
    assert yao_ohio_membership.credor_pool == 750000000
    assert yao_ohio_membership.debtor_pool == 200000000
    assert len(sue_personunit.groupunits) == 2
    ohio_groupunit = sue_personunit.get_groupunit(ohio_str)
    assert len(ohio_groupunit.memberships) == 1


def test_PersonUnit_set_contactunit_groupunit_respect_ledgers_ResetContactUnitsAttrs():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.add_contactunit(exx.yao, 55, 55)
    sue_personunit.add_contactunit(exx.zia, 55, 55)
    yao_contactunit = sue_personunit.get_contact(exx.yao)
    zia_contactunit = sue_personunit.get_contact(exx.zia)
    yao_contactunit.add_contact_fund_give_take(0.5, 0.6, 0.1, 0.22)
    zia_contactunit.add_contact_fund_give_take(0.2, 0.1, 0.1, 0.22)
    zia_1 = 0.8
    zia_2 = 0.5
    zia_3 = 200
    zia_4 = 140
    zia_contactunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=zia_1,
        fund_agenda_ratio_take_sum=zia_2,
        contactunits_contact_cred_lumen_sum=zia_3,
        contactunits_contact_debt_lumen_sum=zia_4,
    )
    yao_1 = 0.2
    yao_2 = 0.5
    yao_3 = 204
    yao_4 = 144
    yao_contactunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=yao_1,
        fund_agenda_ratio_take_sum=yao_2,
        contactunits_contact_cred_lumen_sum=yao_3,
        contactunits_contact_debt_lumen_sum=yao_4,
    )
    assert zia_contactunit.fund_agenda_ratio_give == 0.125
    assert zia_contactunit.fund_agenda_ratio_take == 0.44
    assert yao_contactunit.fund_agenda_ratio_give == 0.5
    assert yao_contactunit.fund_agenda_ratio_take == 0.44

    # WHEN
    sue_personunit._set_contactunit_groupunit_respect_ledgers()

    # THEN
    assert zia_contactunit.fund_agenda_ratio_give == 0
    assert zia_contactunit.fund_agenda_ratio_take == 0
    assert yao_contactunit.fund_agenda_ratio_give == 0
    assert yao_contactunit.fund_agenda_ratio_take == 0
