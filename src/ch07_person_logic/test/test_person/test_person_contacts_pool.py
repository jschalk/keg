from pytest import raises as pytest_raises
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_credor_respect_SetsAttr():
    # ESTABLISH
    zia_person = personunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_person.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_person.credor_respect == x_credor_respect


def test_PersonUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_person = personunit_shop(exx.zia)
    x_credor_respect = 23
    zia_person.set_credor_respect(x_credor_respect)
    assert zia_person.respect_grain == 1
    assert zia_person.credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_person.set_credor_respect(new_credor_respect)

    # THEN
    assert (
        str(excinfo.value)
        == f"Person '{exx.zia}' cannot set credor_respect='{new_credor_respect}'. It is not divisible byrespect_grain'{zia_person.respect_grain}'"
    )


def test_PersonUnit_set_debtor_respect_SetsInt():
    # ESTABLISH
    zia_person = personunit_shop(person_name=exx.zia)
    zia_debtor_respect = 13
    assert zia_person.debtor_respect != zia_debtor_respect

    # WHEN
    zia_person.set_debtor_respect(zia_debtor_respect)
    # THEN
    assert zia_person.debtor_respect == zia_debtor_respect


def test_PersonUnit_set_debtor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_person = personunit_shop(exx.zia)
    x_debtor_respect = 23
    zia_person.set_debtor_respect(x_debtor_respect)
    assert zia_person.respect_grain == 1
    assert zia_person.debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_person.set_debtor_respect(new_debtor_respect)

    # THEN
    assert (
        str(excinfo.value)
        == f"Person '{exx.zia}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible byrespect_grain'{zia_person.respect_grain}'"
    )


def test_PersonUnit_set_contact_respect_SetsAttrs():
    # ESTABLISH
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_person = personunit_shop(exx.zia)
    zia_person.set_credor_respect(old_credor_respect)
    zia_person.set_debtor_respect(old_debtor_respect)
    zia_person.set_fund_pool(old_fund_pool)
    assert zia_person.credor_respect == old_credor_respect
    assert zia_person.debtor_respect == old_debtor_respect
    assert zia_person.fund_pool == old_fund_pool

    # WHEN
    new_contact_pool = 200
    zia_person.set_contact_respect(new_contact_pool)

    # THEN
    assert zia_person.credor_respect == new_contact_pool
    assert zia_person.debtor_respect == new_contact_pool
    assert zia_person.fund_pool == new_contact_pool
