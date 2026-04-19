from ch02_contact.contact import contactunit_shop
from ch08_person_atom.atom_main import PersonAtom, personatom_shop
from ref.keywords import Ch08Keywords as kw, ExampleStrs as exx


def test_PersonAtom_Exists():
    # ESTABLISH / WHEN
    x_personatom = PersonAtom()

    # THEN
    assert not x_personatom.dimen
    assert not x_personatom.crud_str
    assert not x_personatom.jkeys
    assert not x_personatom.jvalues
    assert not x_personatom.atom_order


def test_personatom_shop_ReturnsObj():
    # ESTABLISH
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    bob_contactunit = contactunit_shop(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    cw_str = "_contact_cred_lumen"
    dw_str = "_contact_debt_lumen"
    bob_required_dict = {kw.contact_name: exx.sue}
    bob_optional_dict = {cw_str: bob_contactunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_contactunit.to_dict().get(dw_str)
    contactunit_str = kw.person_contactunit

    # WHEN
    x_personatom = personatom_shop(
        dimen=contactunit_str,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_personatom=}")
    assert x_personatom.dimen == contactunit_str
    assert x_personatom.crud_str == kw.INSERT
    assert x_personatom.jkeys == bob_required_dict
    assert x_personatom.jvalues == bob_optional_dict


def test_PersonAtom_set_jkey_SetsAttr():
    # ESTABLISH
    contactunit_str = kw.person_contactunit
    contactunit_personatom = personatom_shop(contactunit_str, kw.INSERT)
    assert contactunit_personatom.jkeys == {}

    # WHEN
    contactunit_personatom.set_jkey(x_key=kw.contact_name, x_value=exx.bob)

    # THEN
    assert contactunit_personatom.jkeys == {kw.contact_name: exx.bob}


def test_PersonAtom_set_jvalue_SetsAttr():
    # ESTABLISH
    contactunit_str = kw.person_contactunit
    contactunit_personatom = personatom_shop(contactunit_str, kw.INSERT)
    assert contactunit_personatom.jvalues == {}

    # WHEN
    contactunit_personatom.set_jvalue(x_key=kw.contact_name, x_value=exx.bob)

    # THEN
    assert contactunit_personatom.jvalues == {kw.contact_name: exx.bob}


def test_PersonAtom_get_value_ReturnsObj_Scenario0():
    # ESTABLISH
    contactunit_str = kw.person_contactunit
    contactunit_personatom = personatom_shop(contactunit_str, kw.INSERT)
    contactunit_personatom.set_jkey(x_key=kw.contact_name, x_value=exx.bob)

    # WHEN / THEN
    assert contactunit_personatom.get_value(kw.contact_name) == exx.bob


def test_PersonAtom_is_jvalues_valid_ReturnsBoolean():
    # ESTABLISH / WHEN
    contactunit_str = kw.person_contactunit
    bob_insert_personatom = personatom_shop(contactunit_str, crud_str=kw.INSERT)
    assert bob_insert_personatom.is_jvalues_valid()

    # WHEN
    bob_insert_personatom.set_jvalue(kw.contact_cred_lumen, 55)
    # THEN
    assert len(bob_insert_personatom.jvalues) == 1
    assert bob_insert_personatom.is_jvalues_valid()

    # WHEN
    bob_insert_personatom.set_jvalue(kw.contact_debt_lumen, 66)
    # THEN
    assert len(bob_insert_personatom.jvalues) == 2
    assert bob_insert_personatom.is_jvalues_valid()

    # WHEN
    bob_insert_personatom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_personatom.jvalues) == 3
    assert bob_insert_personatom.is_jvalues_valid() is False


def test_PersonAtom_is_valid_ReturnsBoolean_ContactUnit_INSERT():
    # ESTABLISH
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    bob_contactunit = contactunit_shop(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    contactunit_str = kw.person_contactunit

    # WHEN
    bob_insert_personatom = personatom_shop(contactunit_str, crud_str=kw.INSERT)

    # THEN
    assert bob_insert_personatom.is_jkeys_valid() is False
    assert bob_insert_personatom.is_jvalues_valid()
    assert bob_insert_personatom.is_valid() is False

    # WHEN
    bob_insert_personatom.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_personatom.is_jkeys_valid() is False
    assert bob_insert_personatom.is_jvalues_valid() is False
    assert bob_insert_personatom.is_valid() is False

    # WHEN
    bob_insert_personatom.set_jkey(kw.contact_name, exx.bob)

    # THEN
    assert bob_insert_personatom.is_jkeys_valid()
    assert bob_insert_personatom.is_jvalues_valid() is False
    assert bob_insert_personatom.is_valid() is False

    # WHEN
    bob_insert_personatom.jvalues = {}
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen
    bob_insert_personatom.set_jvalue(cw_str, bob_contactunit.to_dict().get(cw_str))
    bob_insert_personatom.set_jvalue(dw_str, bob_contactunit.to_dict().get(dw_str))

    # THEN
    assert bob_insert_personatom.is_jkeys_valid()
    assert bob_insert_personatom.is_jvalues_valid()
    assert bob_insert_personatom.is_valid()

    # WHEN
    bob_insert_personatom.crud_str = None

    # THEN
    assert bob_insert_personatom.is_jkeys_valid() is False
    assert bob_insert_personatom.is_valid() is False

    # WHEN
    bob_insert_personatom.crud_str = kw.INSERT

    # THEN
    assert bob_insert_personatom.is_jkeys_valid()
    assert bob_insert_personatom.is_valid()


def test_PersonAtom_get_value_ReturnsObj_Scenario1():
    # ESTABLISH
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    bob_contactunit = contactunit_shop(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    contactunit_str = kw.person_contactunit
    bob_insert_personatom = personatom_shop(contactunit_str, kw.INSERT)
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen
    print(f"{bob_contactunit.to_dict()=}")
    # bob_contactunit_dict = {kw.contact_name: bob_contactunit.to_dict().get(kw.contact_name)}
    # print(f"{bob_contactunit_dict=}")
    bob_insert_personatom.set_jkey(kw.contact_name, exx.bob)
    bob_insert_personatom.set_jvalue(cw_str, bob_contactunit.to_dict().get(cw_str))
    bob_insert_personatom.set_jvalue(dw_str, bob_contactunit.to_dict().get(dw_str))
    assert bob_insert_personatom.is_valid()

    # WHEN / THEN
    assert bob_insert_personatom.get_value(cw_str) == bob_contact_cred_lumen
    assert bob_insert_personatom.get_value(dw_str) == bob_contact_debt_lumen


def test_PersonAtom_is_valid_ReturnsBoolean_ContactUnit_DELETE():
    # ESTABLISH
    contactunit_str = kw.person_contactunit
    delete_str = kw.DELETE

    # WHEN
    bob_delete_personatom = personatom_shop(contactunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_personatom.is_jkeys_valid() is False
    assert bob_delete_personatom.is_valid() is False

    # WHEN
    bob_delete_personatom.set_jkey(kw.contact_name, exx.bob)

    # THEN
    assert bob_delete_personatom.is_jkeys_valid()
    assert bob_delete_personatom.is_valid()


def test_PersonAtom_is_valid_ReturnsBoolean_personunit():
    # ESTABLISH / WHEN
    bob_update_personatom = personatom_shop(kw.personunit, kw.INSERT)

    # THEN
    assert bob_update_personatom.is_jkeys_valid()
    assert bob_update_personatom.is_valid() is False

    # WHEN
    bob_update_personatom.set_jvalue(kw.max_tree_traverse, 14)

    # THEN
    assert bob_update_personatom.is_jkeys_valid()
    assert bob_update_personatom.is_valid()


def test_PersonAtom_set_atom_order_SetsAttr():
    # ESTABLISH
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    contactunit_str = kw.person_contactunit
    bob_insert_personatom = personatom_shop(contactunit_str, kw.INSERT)
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen
    bob_insert_personatom.set_jkey(kw.contact_name, exx.bob)
    bob_insert_personatom.set_jvalue(cw_str, bob_contact_cred_lumen)
    bob_insert_personatom.set_jvalue(dw_str, bob_contact_debt_lumen)
    assert bob_insert_personatom.is_valid()

    # WHEN / THEN
    assert bob_insert_personatom.get_value(cw_str) == bob_contact_cred_lumen
    assert bob_insert_personatom.get_value(dw_str) == bob_contact_debt_lumen


def test_PersonAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    contactunit_str = kw.person_contactunit
    bob_insert_personatom = personatom_shop(contactunit_str, kw.INSERT)
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen

    # WHEN
    bob_insert_personatom.set_arg(kw.contact_name, exx.bob)
    bob_insert_personatom.set_arg(cw_str, bob_contact_cred_lumen)
    bob_insert_personatom.set_arg(dw_str, bob_contact_debt_lumen)

    # THEN
    assert bob_insert_personatom.get_value(kw.contact_name) == exx.bob
    assert bob_insert_personatom.get_value(cw_str) == bob_contact_cred_lumen
    assert bob_insert_personatom.get_value(dw_str) == bob_contact_debt_lumen
    assert bob_insert_personatom.get_value(kw.contact_name) == exx.bob
    assert bob_insert_personatom.is_valid()


def test_PersonAtom_get_nesting_order_args_ReturnsObj_person_contactunit():
    # ESTABLISH
    sue_insert_personatom = personatom_shop(kw.person_contactunit, kw.INSERT)
    sue_insert_personatom.set_arg(kw.contact_name, exx.sue)
    print(f"{sue_insert_personatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [exx.sue]
    assert sue_insert_personatom.get_nesting_order_args() == ordered_jkeys


def test_PersonAtom_get_nesting_order_args_ReturnsObj_person_contact_membership():
    # ESTABLISH
    iowa_str = ";Iowa"
    sue_insert_personatom = personatom_shop(kw.person_contact_membership, kw.INSERT)
    sue_insert_personatom.set_arg(kw.group_title, iowa_str)
    sue_insert_personatom.set_arg(kw.contact_name, exx.sue)
    print(f"{sue_insert_personatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [exx.sue, iowa_str]
    assert sue_insert_personatom.get_nesting_order_args() == ordered_jkeys
