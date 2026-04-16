from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch02_contact._ref.ch02_semantic_types import NameTerm
from src.ch02_contact.contact import (
    ContactUnit,
    contactunit_shop,
    default_groupmark_if_None,
    is_nameterm,
    validate_nameterm,
)
from src.ref.keywords import Ch02Keywords as kw, ExampleStrs as exx


def test_is_nameterm_ReturnsObj():
    # ESTABLISH
    x_groupmark = default_groupmark_if_None()

    # WHEN / THEN
    assert is_nameterm("", groupmark=x_groupmark) is False
    assert is_nameterm("casa", groupmark=x_groupmark)
    assert not is_nameterm(f"ZZ{x_groupmark}casa", x_groupmark)
    assert not is_nameterm(NameTerm(f"ZZ{x_groupmark}casa"), x_groupmark)
    assert is_nameterm(NameTerm("YY"), x_groupmark)


def test_validate_nameterm_Scenario0_RaisesErrorWhenNotNameTerm():
    # ESTABLISH
    bob_str = "Bob, Tom"
    assert bob_str == validate_nameterm(bob_str, x_groupmark=exx.slash)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_nameterm(bob_str, x_groupmark=comma_str)

    # THEN
    assert (
        str(excinfo.value)
        == f"'{bob_str}' must be a NameTerm. Cannot contain GroupMark: '{comma_str}'"
    )


def test_validate_nameterm_Scenario1_RaisesErrorWhenNameTerm():
    # ESTABLISH
    bob_str = f"Bob{exx.slash}Tom"
    assert bob_str == validate_nameterm(
        bob_str, x_groupmark=exx.slash, not_nameterm_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_nameterm(
            bob_str, x_groupmark=comma_str, not_nameterm_required=True
        )

    # THEN
    assert (
        str(excinfo.value)
        == f"'{bob_str}' must not be a NameTerm. Must contain GroupMark: '{comma_str}'"
    )


def test_ContactUnit_Exists():
    # ESTABLISH

    # WHEN
    bob_contactunit = ContactUnit(exx.bob)

    # THEN
    print(f"{exx.bob}")
    assert bob_contactunit
    assert bob_contactunit.contact_name
    assert bob_contactunit.contact_name == exx.bob
    assert not bob_contactunit.contact_cred_lumen
    assert not bob_contactunit.contact_debt_lumen
    # calculated fields
    assert not bob_contactunit.credor_pool
    assert not bob_contactunit.debtor_pool
    assert not bob_contactunit.memberships
    assert not bob_contactunit.irrational_contact_debt_lumen
    assert not bob_contactunit.inallocable_contact_debt_lumen
    assert not bob_contactunit.fund_give
    assert not bob_contactunit.fund_take
    assert not bob_contactunit.fund_agenda_give
    assert not bob_contactunit.fund_agenda_take
    assert not bob_contactunit.groupmark
    assert not bob_contactunit.respect_grain
    obj_attrs = set(bob_contactunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_agenda_take,
        kw.fund_give,
        kw.fund_take,
        kw.inallocable_contact_debt_lumen,
        kw.irrational_contact_debt_lumen,
        kw.memberships,
        kw.respect_grain,
        kw.contact_name,
        kw.groupmark,
        kw.contact_cred_lumen,
        kw.contact_debt_lumen,
    }


def test_ContactUnit_set_nameterm_SetsAttr():
    # ESTABLISH
    x_contactunit = ContactUnit()

    # WHEN
    x_contactunit.set_name(exx.bob)

    # THEN
    assert x_contactunit.contact_name == exx.bob


def test_ContactUnit_set_nameterm_RaisesErrorIfParameterContains_groupmark():
    # ESTABLISH
    texas_str = f"Texas{exx.slash}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contactunit_shop(contact_name=texas_str, groupmark=exx.slash)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' must be a NameTerm. Cannot contain {kw.GroupMark}: '{exx.slash}'"
    )


def test_contactunit_shop_SetsAttributes():
    # ESTABLISH

    # WHEN
    yao_contactunit = contactunit_shop(contact_name=exx.yao)

    # THEN
    assert yao_contactunit.contact_name == exx.yao
    assert yao_contactunit.contact_cred_lumen == 1
    assert yao_contactunit.contact_debt_lumen == 1
    # calculated fields
    assert yao_contactunit.credor_pool == 0
    assert yao_contactunit.debtor_pool == 0
    assert yao_contactunit.memberships == {}
    assert yao_contactunit.irrational_contact_debt_lumen == 0
    assert yao_contactunit.inallocable_contact_debt_lumen == 0
    assert yao_contactunit.fund_give == 0
    assert yao_contactunit.fund_take == 0
    assert yao_contactunit.fund_agenda_give == 0
    assert yao_contactunit.fund_agenda_take == 0
    assert yao_contactunit.fund_agenda_ratio_give == 0
    assert yao_contactunit.fund_agenda_ratio_take == 0
    assert yao_contactunit.groupmark == default_groupmark_if_None()
    assert yao_contactunit.respect_grain == default_grain_num_if_None()


def test_contactunit_shop_SetsAttributes_groupmark():
    # ESTABLISH

    # WHEN
    yao_contactunit = contactunit_shop(exx.yao, groupmark=exx.slash)

    # THEN
    assert yao_contactunit.groupmark == exx.slash


def test_contactunit_shop_SetsAttributes_respect_grain():
    # ESTABLISH
    respect_grain_float = 00.45

    # WHEN
    yao_contactunit = contactunit_shop(exx.yao, respect_grain=respect_grain_float)

    # THEN
    assert yao_contactunit.respect_grain == respect_grain_float


def test_ContactUnit_set_respect_grain_SetsAttribute():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    assert bob_contactunit.respect_grain == 1

    # WHEN
    x_respect_grain = 5
    bob_contactunit.set_respect_grain(x_respect_grain)

    # THEN
    assert bob_contactunit.respect_grain == x_respect_grain


def test_ContactUnit_set_contact_cred_lumen_SetsAttribute():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")

    # WHEN
    x_contact_cred_lumen = 23
    bob_contactunit.set_contact_cred_lumen(x_contact_cred_lumen)

    # THEN
    assert bob_contactunit.contact_cred_lumen == x_contact_cred_lumen


def test_ContactUnit_set_contact_debt_lumen_SetsAttribute():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")

    # WHEN
    x_contact_debt_lumen = 23
    bob_contactunit.set_contact_debt_lumen(x_contact_debt_lumen)

    # THEN
    assert bob_contactunit.contact_debt_lumen == x_contact_debt_lumen


def test_ContactUnit_set_credor_contact_debt_lumen_SetsAttr_Scenario0():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    assert bob_contactunit.contact_cred_lumen == 1
    assert bob_contactunit.contact_debt_lumen == 1

    # WHEN
    bob_contactunit.set_credor_contact_debt_lumen(
        contact_cred_lumen=23, contact_debt_lumen=34
    )

    # THEN
    assert bob_contactunit.contact_cred_lumen == 23
    assert bob_contactunit.contact_debt_lumen == 34


def test_ContactUnit_set_credor_contact_debt_lumen_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_contactunit = contactunit_shop(
        "Bob", contact_cred_lumen=45, contact_debt_lumen=56
    )
    assert bob_contactunit.contact_cred_lumen == 45
    assert bob_contactunit.contact_debt_lumen == 56

    # WHEN
    bob_contactunit.set_credor_contact_debt_lumen(
        contact_cred_lumen=None, contact_debt_lumen=None
    )

    # THEN
    assert bob_contactunit.contact_cred_lumen == 45
    assert bob_contactunit.contact_debt_lumen == 56


def test_ContactUnit_set_credor_contact_debt_lumen_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    assert bob_contactunit.contact_cred_lumen == 1
    assert bob_contactunit.contact_debt_lumen == 1

    # WHEN
    bob_contactunit.set_credor_contact_debt_lumen(
        contact_cred_lumen=None, contact_debt_lumen=None
    )

    # THEN
    assert bob_contactunit.contact_cred_lumen == 1
    assert bob_contactunit.contact_debt_lumen == 1


def test_ContactUnit_add_irrational_contact_debt_lumen_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    assert bob_contactunit.irrational_contact_debt_lumen == 0

    # WHEN
    bob_int1 = 11
    bob_contactunit.add_irrational_contact_debt_lumen(bob_int1)

    # THEN
    assert bob_contactunit.irrational_contact_debt_lumen == bob_int1

    # WHEN
    bob_int2 = 22
    bob_contactunit.add_irrational_contact_debt_lumen(bob_int2)

    # THEN
    assert bob_contactunit.irrational_contact_debt_lumen == bob_int1 + bob_int2


def test_ContactUnit_add_inallocable_contact_debt_lumen_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    assert bob_contactunit.inallocable_contact_debt_lumen == 0

    # WHEN
    bob_int1 = 11
    bob_contactunit.add_inallocable_contact_debt_lumen(bob_int1)

    # THEN
    assert bob_contactunit.inallocable_contact_debt_lumen == bob_int1

    # WHEN
    bob_int2 = 22
    bob_contactunit.add_inallocable_contact_debt_lumen(bob_int2)

    # THEN
    assert bob_contactunit.inallocable_contact_debt_lumen == bob_int1 + bob_int2


def test_ContactUnit_reset_listen_calculated_attrs_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_contactunit.add_irrational_contact_debt_lumen(bob_int1)
    bob_contactunit.add_inallocable_contact_debt_lumen(bob_int2)
    assert bob_contactunit.irrational_contact_debt_lumen == bob_int1
    assert bob_contactunit.inallocable_contact_debt_lumen == bob_int2

    # WHEN
    bob_contactunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_contactunit.irrational_contact_debt_lumen == 0
    assert bob_contactunit.inallocable_contact_debt_lumen == 0


def test_ContactUnit_clear_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    bob_contactunit.fund_give = 0.27
    bob_contactunit.fund_take = 0.37
    bob_contactunit.fund_agenda_give = 0.41
    bob_contactunit.fund_agenda_take = 0.51
    bob_contactunit.fund_agenda_ratio_give = 0.433
    bob_contactunit.fund_agenda_ratio_take = 0.533
    assert bob_contactunit.fund_give == 0.27
    assert bob_contactunit.fund_take == 0.37
    assert bob_contactunit.fund_agenda_give == 0.41
    assert bob_contactunit.fund_agenda_take == 0.51
    assert bob_contactunit.fund_agenda_ratio_give == 0.433
    assert bob_contactunit.fund_agenda_ratio_take == 0.533

    # WHEN
    bob_contactunit.clear_fund_give_take()

    # THEN
    assert bob_contactunit.fund_give == 0
    assert bob_contactunit.fund_take == 0
    assert bob_contactunit.fund_agenda_give == 0
    assert bob_contactunit.fund_agenda_take == 0
    assert bob_contactunit.fund_agenda_ratio_give == 0
    assert bob_contactunit.fund_agenda_ratio_take == 0


def test_ContactUnit_add_fund_agenda_give_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    bob_contactunit.fund_agenda_give = 0.41
    assert bob_contactunit.fund_agenda_give == 0.41

    # WHEN
    bob_contactunit.add_fund_agenda_give(0.3)

    # THEN
    assert bob_contactunit.fund_agenda_give == 0.71


def test_ContactUnit_add_fund_agenda_take_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    bob_contactunit.fund_agenda_take = 0.41
    assert bob_contactunit.fund_agenda_take == 0.41

    # WHEN
    bob_contactunit.add_fund_agenda_take(0.3)

    # THEN
    assert bob_contactunit.fund_agenda_take == 0.71


def test_ContactUnit_add_contact_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop("Bob")
    bob_contactunit.fund_give = 0.4106
    bob_contactunit.fund_take = 0.1106
    bob_contactunit.fund_agenda_give = 0.41
    bob_contactunit.fund_agenda_take = 0.51
    assert bob_contactunit.fund_agenda_give == 0.41
    assert bob_contactunit.fund_agenda_take == 0.51

    # WHEN
    bob_contactunit.add_contact_fund_give_take(
        fund_give=0.33,
        fund_take=0.055,
        fund_agenda_give=0.3,
        fund_agenda_take=0.05,
    )

    # THEN
    assert bob_contactunit.fund_give == 0.7406
    assert bob_contactunit.fund_take == 0.1656
    assert bob_contactunit.fund_agenda_give == 0.71
    assert bob_contactunit.fund_agenda_take == 0.56


def test_ContactUnit_set_contactunits_fund_agenda_ratios_SetsAttr():
    # ESTABLISH
    bob_contactunit = contactunit_shop(
        "Bob", contact_cred_lumen=15, contact_debt_lumen=7
    )
    bob_contactunit.fund_give = 0.4106
    bob_contactunit.fund_take = 0.1106
    bob_contactunit.fund_agenda_give = 0.041
    bob_contactunit.fund_agenda_take = 0.051
    bob_contactunit.fund_agenda_ratio_give = 0
    bob_contactunit.fund_agenda_ratio_take = 0
    assert bob_contactunit.fund_agenda_ratio_give == 0
    assert bob_contactunit.fund_agenda_ratio_take == 0

    # WHEN
    bob_contactunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0.2,
        fund_agenda_ratio_take_sum=0.5,
        contactunits_contact_cred_lumen_sum=20,
        contactunits_contact_debt_lumen_sum=14,
    )

    # THEN
    assert bob_contactunit.fund_agenda_ratio_give == 0.205
    assert bob_contactunit.fund_agenda_ratio_take == 0.102

    # WHEN
    bob_contactunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        contactunits_contact_cred_lumen_sum=20,
        contactunits_contact_debt_lumen_sum=14,
    )

    # THEN
    assert bob_contactunit.fund_agenda_ratio_give == 0.75
    assert bob_contactunit.fund_agenda_ratio_take == 0.5
