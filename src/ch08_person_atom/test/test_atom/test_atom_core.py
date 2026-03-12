from src.ch02_partner.partner import partnerunit_shop
from src.ch08_person_atom.atom_main import PersonAtom, personatom_shop
from src.ref.keywords import Ch08Keywords as kw, ExampleStrs as exx


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
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    bob_partnerunit = partnerunit_shop(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    cw_str = "_partner_cred_lumen"
    dw_str = "_partner_debt_lumen"
    bob_required_dict = {kw.partner_name: exx.sue}
    bob_optional_dict = {cw_str: bob_partnerunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.to_dict().get(dw_str)
    partnerunit_str = kw.person_partnerunit

    # WHEN
    x_personatom = personatom_shop(
        dimen=partnerunit_str,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_personatom=}")
    assert x_personatom.dimen == partnerunit_str
    assert x_personatom.crud_str == kw.INSERT
    assert x_personatom.jkeys == bob_required_dict
    assert x_personatom.jvalues == bob_optional_dict


def test_PersonAtom_set_jkey_SetsAttr():
    # ESTABLISH
    partnerunit_str = kw.person_partnerunit
    partnerunit_personatom = personatom_shop(partnerunit_str, kw.INSERT)
    assert partnerunit_personatom.jkeys == {}

    # WHEN
    partnerunit_personatom.set_jkey(x_key=kw.partner_name, x_value=exx.bob)

    # THEN
    assert partnerunit_personatom.jkeys == {kw.partner_name: exx.bob}


def test_PersonAtom_set_jvalue_SetsAttr():
    # ESTABLISH
    partnerunit_str = kw.person_partnerunit
    partnerunit_personatom = personatom_shop(partnerunit_str, kw.INSERT)
    assert partnerunit_personatom.jvalues == {}

    # WHEN
    partnerunit_personatom.set_jvalue(x_key=kw.partner_name, x_value=exx.bob)

    # THEN
    assert partnerunit_personatom.jvalues == {kw.partner_name: exx.bob}


def test_PersonAtom_get_value_ReturnsObj_Scenario0():
    # ESTABLISH
    partnerunit_str = kw.person_partnerunit
    partnerunit_personatom = personatom_shop(partnerunit_str, kw.INSERT)
    partnerunit_personatom.set_jkey(x_key=kw.partner_name, x_value=exx.bob)

    # WHEN / THEN
    assert partnerunit_personatom.get_value(kw.partner_name) == exx.bob


def test_PersonAtom_is_jvalues_valid_ReturnsBoolean():
    # ESTABLISH / WHEN
    partnerunit_str = kw.person_partnerunit
    bob_insert_personatom = personatom_shop(partnerunit_str, crud_str=kw.INSERT)
    assert bob_insert_personatom.is_jvalues_valid()

    # WHEN
    bob_insert_personatom.set_jvalue(kw.partner_cred_lumen, 55)
    # THEN
    assert len(bob_insert_personatom.jvalues) == 1
    assert bob_insert_personatom.is_jvalues_valid()

    # WHEN
    bob_insert_personatom.set_jvalue(kw.partner_debt_lumen, 66)
    # THEN
    assert len(bob_insert_personatom.jvalues) == 2
    assert bob_insert_personatom.is_jvalues_valid()

    # WHEN
    bob_insert_personatom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_personatom.jvalues) == 3
    assert bob_insert_personatom.is_jvalues_valid() is False


def test_PersonAtom_is_valid_ReturnsBoolean_PartnerUnit_INSERT():
    # ESTABLISH
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    bob_partnerunit = partnerunit_shop(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    partnerunit_str = kw.person_partnerunit

    # WHEN
    bob_insert_personatom = personatom_shop(partnerunit_str, crud_str=kw.INSERT)

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
    bob_insert_personatom.set_jkey(kw.partner_name, exx.bob)

    # THEN
    assert bob_insert_personatom.is_jkeys_valid()
    assert bob_insert_personatom.is_jvalues_valid() is False
    assert bob_insert_personatom.is_valid() is False

    # WHEN
    bob_insert_personatom.jvalues = {}
    cw_str = kw.partner_cred_lumen
    dw_str = kw.partner_debt_lumen
    bob_insert_personatom.set_jvalue(cw_str, bob_partnerunit.to_dict().get(cw_str))
    bob_insert_personatom.set_jvalue(dw_str, bob_partnerunit.to_dict().get(dw_str))

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
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    bob_partnerunit = partnerunit_shop(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    partnerunit_str = kw.person_partnerunit
    bob_insert_personatom = personatom_shop(partnerunit_str, kw.INSERT)
    cw_str = kw.partner_cred_lumen
    dw_str = kw.partner_debt_lumen
    print(f"{bob_partnerunit.to_dict()=}")
    # bob_partnerunit_dict = {kw.partner_name: bob_partnerunit.to_dict().get(kw.partner_name)}
    # print(f"{bob_partnerunit_dict=}")
    bob_insert_personatom.set_jkey(kw.partner_name, exx.bob)
    bob_insert_personatom.set_jvalue(cw_str, bob_partnerunit.to_dict().get(cw_str))
    bob_insert_personatom.set_jvalue(dw_str, bob_partnerunit.to_dict().get(dw_str))
    assert bob_insert_personatom.is_valid()

    # WHEN / THEN
    assert bob_insert_personatom.get_value(cw_str) == bob_partner_cred_lumen
    assert bob_insert_personatom.get_value(dw_str) == bob_partner_debt_lumen


def test_PersonAtom_is_valid_ReturnsBoolean_PartnerUnit_DELETE():
    # ESTABLISH
    partnerunit_str = kw.person_partnerunit
    delete_str = kw.DELETE

    # WHEN
    bob_delete_personatom = personatom_shop(partnerunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_personatom.is_jkeys_valid() is False
    assert bob_delete_personatom.is_valid() is False

    # WHEN
    bob_delete_personatom.set_jkey(kw.partner_name, exx.bob)

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
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    partnerunit_str = kw.person_partnerunit
    bob_insert_personatom = personatom_shop(partnerunit_str, kw.INSERT)
    cw_str = kw.partner_cred_lumen
    dw_str = kw.partner_debt_lumen
    bob_insert_personatom.set_jkey(kw.partner_name, exx.bob)
    bob_insert_personatom.set_jvalue(cw_str, bob_partner_cred_lumen)
    bob_insert_personatom.set_jvalue(dw_str, bob_partner_debt_lumen)
    assert bob_insert_personatom.is_valid()

    # WHEN / THEN
    assert bob_insert_personatom.get_value(cw_str) == bob_partner_cred_lumen
    assert bob_insert_personatom.get_value(dw_str) == bob_partner_debt_lumen


def test_PersonAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    partnerunit_str = kw.person_partnerunit
    bob_insert_personatom = personatom_shop(partnerunit_str, kw.INSERT)
    cw_str = kw.partner_cred_lumen
    dw_str = kw.partner_debt_lumen

    # WHEN
    bob_insert_personatom.set_arg(kw.partner_name, exx.bob)
    bob_insert_personatom.set_arg(cw_str, bob_partner_cred_lumen)
    bob_insert_personatom.set_arg(dw_str, bob_partner_debt_lumen)

    # THEN
    assert bob_insert_personatom.get_value(kw.partner_name) == exx.bob
    assert bob_insert_personatom.get_value(cw_str) == bob_partner_cred_lumen
    assert bob_insert_personatom.get_value(dw_str) == bob_partner_debt_lumen
    assert bob_insert_personatom.get_value(kw.partner_name) == exx.bob
    assert bob_insert_personatom.is_valid()


def test_PersonAtom_get_nesting_order_args_ReturnsObj_person_partnerunit():
    # ESTABLISH
    sue_insert_personatom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    sue_insert_personatom.set_arg(kw.partner_name, exx.sue)
    print(f"{sue_insert_personatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [exx.sue]
    assert sue_insert_personatom.get_nesting_order_args() == ordered_jkeys


def test_PersonAtom_get_nesting_order_args_ReturnsObj_person_partner_membership():
    # ESTABLISH
    iowa_str = ";Iowa"
    sue_insert_personatom = personatom_shop(kw.person_partner_membership, kw.INSERT)
    sue_insert_personatom.set_arg(kw.group_title, iowa_str)
    sue_insert_personatom.set_arg(kw.partner_name, exx.sue)
    print(f"{sue_insert_personatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [exx.sue, iowa_str]
    assert sue_insert_personatom.get_nesting_order_args() == ordered_jkeys
