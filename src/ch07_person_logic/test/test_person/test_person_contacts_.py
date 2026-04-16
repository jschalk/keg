from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch02_contact.contact import contactunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_contactunit_SetsAttr():
    # ESTABLISH
    yao_contactunit = contactunit_shop(exx.yao)
    yao_contactunit.add_membership(exx.yao)
    deepcopy_yao_contactunit = copy_deepcopy(yao_contactunit)
    bob_person = personunit_shop("Bob", knot=exx.slash)

    # WHEN
    bob_person.set_contactunit(yao_contactunit)

    # THEN
    assert bob_person.contacts.get(exx.yao).groupmark == exx.slash
    x_contacts = {yao_contactunit.contact_name: deepcopy_yao_contactunit}
    assert bob_person.contacts != x_contacts
    deepcopy_yao_contactunit.groupmark = bob_person.knot
    assert bob_person.contacts == x_contacts


def test_PersonUnit_set_contact_DoesNotSet_contact_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_person = personunit_shop(exx.yao, respect_grain=x_respect_grain)

    # WHEN
    yao_person.set_contactunit(contactunit_shop(exx.zia), auto_set_membership=False)

    # THEN
    assert yao_person.get_contact(exx.zia).get_membership(exx.zia) is None


def test_PersonUnit_set_contact_DoesSet_contact_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_person = personunit_shop(exx.yao, respect_grain=x_respect_grain)

    # WHEN
    yao_person.set_contactunit(contactunit_shop(exx.zia))

    # THEN
    zia_zia_membership = yao_person.get_contact(exx.zia).get_membership(exx.zia)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_lumen == 1
    assert zia_zia_membership.group_debt_lumen == 1


def test_PersonUnit_set_contact_DoesNotOverRide_contact_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_person = personunit_shop(exx.yao, respect_grain=x_respect_grain)
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_contactunit = contactunit_shop(exx.zia)
    zia_contactunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_person.set_contactunit(zia_contactunit)

    # THEN
    zia_ohio_membership = yao_person.get_contact(exx.zia).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_lumen == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_lumen == zia_ohio_debt_w
    zia_zia_membership = yao_person.get_contact(exx.zia).get_membership(exx.zia)
    assert zia_zia_membership is None


def test_PersonUnit_add_contactunit_Sets_contacts():
    # ESTABLISH
    x_respect_grain = 6
    yao_person = personunit_shop(exx.yao, respect_grain=x_respect_grain)

    # WHEN
    yao_person.add_contactunit(exx.zia, contact_cred_lumen=13, contact_debt_lumen=8)
    yao_person.add_contactunit(exx.sue, contact_debt_lumen=5)
    yao_person.add_contactunit(exx.xio, contact_cred_lumen=17)

    # THEN
    assert len(yao_person.contacts) == 3
    assert len(yao_person.get_contactunit_group_titles_dict()) == 3
    assert yao_person.contacts.get(exx.xio).contact_cred_lumen == 17
    assert yao_person.contacts.get(exx.sue).contact_debt_lumen == 5
    assert yao_person.contacts.get(exx.xio).respect_grain == x_respect_grain


def test_PersonUnit_contact_exists_ReturnsObj():
    # ESTABLISH
    bob_person = personunit_shop("Bob")

    # WHEN / THEN
    assert bob_person.contact_exists(exx.yao) is False

    # ESTABLISH
    bob_person.add_contactunit(exx.yao)

    # WHEN / THEN
    assert bob_person.contact_exists(exx.yao)


def test_PersonUnit_set_contact_Creates_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    before_zia_credit = 7
    before_zia_debt = 17
    yao_person.add_contactunit(exx.zia, before_zia_credit, before_zia_debt)
    zia_contactunit = yao_person.get_contact(exx.zia)
    zia_membership = zia_contactunit.get_membership(exx.zia)
    assert zia_membership.group_cred_lumen != before_zia_credit
    assert zia_membership.group_debt_lumen != before_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_person.set_contactunit(
        contactunit_shop(exx.zia, after_zia_credit, after_zia_debt)
    )

    # THEN
    assert zia_membership.group_cred_lumen != after_zia_credit
    assert zia_membership.group_debt_lumen != after_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1


def test_PersonUnit_edit_contact_RaiseExceptionWhenContactDoesNotExist():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    zia_contact_cred_lumen = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_person.edit_contactunit(exx.zia, contact_cred_lumen=zia_contact_cred_lumen)

    # THEN
    assert str(excinfo.value) == f"ContactUnit '{exx.zia}' does not exist."


def test_PersonUnit_edit_contact_UpdatesObj():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    old_zia_contact_cred_lumen = 55
    old_zia_contact_debt_lumen = 66
    yao_person.set_contactunit(
        contactunit_shop(
            exx.zia,
            old_zia_contact_cred_lumen,
            old_zia_contact_debt_lumen,
        )
    )
    zia_contactunit = yao_person.get_contact(exx.zia)
    assert zia_contactunit.contact_cred_lumen == old_zia_contact_cred_lumen
    assert zia_contactunit.contact_debt_lumen == old_zia_contact_debt_lumen

    # WHEN
    new_zia_contact_cred_lumen = 22
    new_zia_contact_debt_lumen = 33
    yao_person.edit_contactunit(
        contact_name=exx.zia,
        contact_cred_lumen=new_zia_contact_cred_lumen,
        contact_debt_lumen=new_zia_contact_debt_lumen,
    )

    # THEN
    assert zia_contactunit.contact_cred_lumen == new_zia_contact_cred_lumen
    assert zia_contactunit.contact_debt_lumen == new_zia_contact_debt_lumen


def test_PersonUnit_get_contact_ReturnsObj():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.zia)
    yao_person.add_contactunit(exx.sue)

    # WHEN
    zia_contact = yao_person.get_contact(exx.zia)
    sue_contact = yao_person.get_contact(exx.sue)

    # THEN
    assert zia_contact == yao_person.contacts.get(exx.zia)
    assert sue_contact == yao_person.contacts.get(exx.sue)
