from pytest import raises as pytest_raises
from src.ch02_contact.contact import contactunit_shop
from src.ch04_rope.rope import create_rope, to_rope
from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import (
    PersonDelta,
    get_persondelta_from_ordered_dict,
    person_built_from_delta_is_valid,
    persondelta_shop,
)
from src.ch09_person_lesson.test._util.ch09_examples import get_persondelta_example1
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PersonDelta_Exists():
    # ESTABLISH / WHEN
    x_persondelta = PersonDelta()

    # THEN
    assert x_persondelta.personatoms is None
    assert x_persondelta.person_build_validated is None


def test_persondelta_shop_ReturnsObj():
    # ESTABLISH / WHEN
    ex1_persondelta = persondelta_shop()

    # THEN
    assert ex1_persondelta.personatoms == {}
    assert ex1_persondelta.person_build_validated is False


def test_PersonDelta_set_personatom_Sets_PersonUnitSimpleAttrs():
    # ESTABLISH
    ex1_persondelta = persondelta_shop()
    attribute_value = 55
    dimen = kw.personunit
    opt1_arg = kw.mana_grain
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    person_star_personatom = personatom_shop(
        dimen,
        kw.UPDATE,
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_persondelta.personatoms == {}
    assert person_star_personatom.atom_order is None

    # WHEN
    ex1_persondelta.set_personatom(person_star_personatom)

    # THEN
    assert len(ex1_persondelta.personatoms) == 1
    x_update_dict = ex1_persondelta.personatoms.get(kw.UPDATE)
    # print(f"{x_update_dict=}")
    x_dimen_personatom = x_update_dict.get(dimen)
    print(f"{x_dimen_personatom=}")
    assert x_dimen_personatom == person_star_personatom
    assert person_star_personatom.atom_order is not None


def test_PersonDelta_set_personatom_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_persondelta = persondelta_shop()
    x_dimen = kw.person_contactunit
    person_star_personatom = personatom_shop(x_dimen, kw.UPDATE)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_persondelta.set_personatom(person_star_personatom)

    # THEN
    exception_str = f"""'{x_dimen}' UPDATE PersonAtom is invalid
                x_personatom.is_jkeys_valid()=False
                x_personatom.is_jvalues_valid()=True"""
    assert str(excinfo.value) == exception_str


def test_ChangUnit_c_personatom_exists_ReturnsObj_person_contactunit_str():
    # ESTABLISH
    x_persondelta = persondelta_shop()
    bob_personatom = personatom_shop(kw.person_contactunit, kw.INSERT)
    bob_personatom.set_arg(kw.contact_name, exx.bob)
    assert not x_persondelta.c_personatom_exists(bob_personatom)

    # WHEN
    x_persondelta.set_personatom(bob_personatom)

    # THEN
    assert x_persondelta.c_personatom_exists(bob_personatom)


def test_ChangUnit_c_personatom_exists_ReturnsObj_person_contact_membership_str():
    # ESTABLISH
    iowa_str = ";Iowa"
    x_persondelta = persondelta_shop()
    bob_iowa_personatom = personatom_shop(kw.person_contact_membership, kw.INSERT)
    bob_iowa_personatom.set_arg(kw.group_title, iowa_str)
    bob_iowa_personatom.set_arg(kw.contact_name, exx.bob)
    assert not x_persondelta.c_personatom_exists(bob_iowa_personatom)

    # WHEN
    x_persondelta.set_personatom(bob_iowa_personatom)

    # THEN
    assert x_persondelta.c_personatom_exists(bob_iowa_personatom)


def test_PersonDelta_get_atom_ReturnsObj():
    # ESTABLISH
    ex1_persondelta = persondelta_shop()
    opt_arg1 = kw.mana_grain
    opt_value = 55
    personunit_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    personunit_personatom.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_persondelta.set_personatom(personunit_personatom)

    # WHEN
    gen_personatom = ex1_persondelta.get_personatom(
        kw.UPDATE, dimen=kw.personunit, jkeys=[]
    )

    # THEN
    assert gen_personatom == personunit_personatom


def test_PersonDelta_add_personatom_Sets_PersonUnitSimpleAttrs():
    # ESTABLISH
    ex1_persondelta = persondelta_shop()
    assert ex1_persondelta.personatoms == {}

    # WHEN
    op2_arg = kw.mana_grain
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_persondelta.add_personatom(
        kw.personunit,
        kw.UPDATE,
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_persondelta.personatoms) == 1
    x_update_dict = ex1_persondelta.personatoms.get(kw.UPDATE)
    x_personatom = x_update_dict.get(kw.personunit)
    assert x_personatom is not None
    assert x_personatom.dimen == kw.personunit


def test_PersonDelta_add_personatom_Sets_PersonUnit_contactunits():
    # ESTABLISH
    ex1_persondelta = persondelta_shop()
    assert ex1_persondelta.personatoms == {}

    # WHEN
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    bob_contactunit = contactunit_shop(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen
    print(f"{bob_contactunit.to_dict()=}")
    bob_required_dict = {
        kw.contact_name: bob_contactunit.to_dict().get(kw.contact_name)
    }
    bob_optional_dict = {cw_str: bob_contactunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_contactunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    contactunit_str = kw.person_contactunit
    ex1_persondelta.add_personatom(
        dimen=contactunit_str,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_persondelta.personatoms) == 1
    assert (
        ex1_persondelta.personatoms.get(kw.INSERT).get(contactunit_str).get(exx.bob)
        is not None
    )


def test_PersonDelta_get_crud_personatoms_list_ReturnsObj():
    # ESTABLISH
    ex1_persondelta = get_persondelta_example1()
    assert len(ex1_persondelta.personatoms.get(kw.UPDATE).keys()) == 1
    assert ex1_persondelta.personatoms.get(kw.INSERT) is None
    assert len(ex1_persondelta.personatoms.get(kw.DELETE).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_persondelta._get_crud_personatoms_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(kw.UPDATE)=}")
    assert len(sue_atom_order_dict.get(kw.UPDATE)) == 1
    assert len(sue_atom_order_dict.get(kw.DELETE)) == 1
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PersonDelta_get_dimen_sorted_personatoms_list_ReturnsObj_Scenario0_rope():
    # ESTABLISH
    ex1_persondelta = get_persondelta_example1()
    update_dict = ex1_persondelta.personatoms.get(kw.UPDATE)
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_persondelta.personatoms.get(kw.INSERT) is None
    delete_dict = ex1_persondelta.personatoms.get(kw.DELETE)
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_persondelta.get_dimen_sorted_personatoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(kw.personunit)
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(kw.person_contactunit).keys())
    zia_contactunit_delete = delete_dict.get(kw.person_contactunit).get("Zia")
    assert sue_atoms_list[1] == zia_contactunit_delete


# def test_PersonDelta_add_personatom_Sets_PersonUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_persondelta = persondelta_shop(get_sue_rope())
#     assert ex1_persondelta.personatoms == {}

#     # WHEN
#     opt2_value = 55
#     dimen = kw.personunit
#     opt2_arg = kw.star
#     star_personatom = personatom_shop(dimen, kw.UPDATE)
#     star_personatom.set_jvalue(opt2_arg, opt2_value)
#     ex1_persondelta.set_personatom(star_personatom)
#     # THEN
#     assert len(ex1_persondelta.personatoms.get(kw.UPDATE).keys()) == 1
#     sue_personunit_dict = ex1_persondelta.personatoms.get(kw.UPDATE)
#     sue_star_personatom = sue_personunit_dict.get(dimen)
#     print(f"{sue_star_personatom=}")
#     assert star_personatom == sue_star_personatom

#     # WHEN
#     new2_value = 66
#     x_attribute = kw.max_tree_traverse
#     jkeys = {x_attribute: new2_value}
#     x_personatom = personatom_shop(x_attribute, kw.UPDATE, None, jkeys)
#     ex1_persondelta.set_personatom(x_personatom)
#     # THEN
#     print(f"{ex1_persondelta.personatoms.keys()=}")
#     print(f"{ex1_persondelta.personatoms.get(kw.UPDATE).keys()=}")
#     assert len(ex1_persondelta.personatoms.get(kw.UPDATE).keys()) == 2
#     assert x_personatom == ex1_persondelta.personatoms.get(kw.UPDATE).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = kw.credor_respect
#     jkeys = {x_attribute: new3_value}
#     x_personatom = personatom_shop(x_attribute, kw.UPDATE, None, jkeys)
#     ex1_persondelta.set_personatom(x_personatom)
#     # THEN
#     assert len(ex1_persondelta.personatoms.get(kw.UPDATE).keys()) == 3
#     assert x_personatom == ex1_persondelta.personatoms.get(kw.UPDATE).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = kw.debtor_respect
#     jkeys = {x_attribute: new4_value}
#     x_personatom = personatom_shop(x_attribute, kw.UPDATE, None, jkeys)
#     ex1_persondelta.set_personatom(x_personatom)
#     # THEN
#     assert len(ex1_persondelta.personatoms.get(kw.UPDATE).keys()) == 4
#     assert x_personatom == ex1_persondelta.personatoms.get(kw.UPDATE).get(x_attribute)


def test_PersonDelta_get_sorted_personatoms_ReturnsObj():
    # ESTABLISH
    ex1_persondelta = get_persondelta_example1()
    update_dict = ex1_persondelta.personatoms.get(kw.UPDATE)
    assert len(update_dict.keys()) == 1
    assert update_dict.get(kw.personunit) is not None
    print(f"atom_order 28 {ex1_persondelta.personatoms.get(kw.UPDATE).keys()=}")
    delete_dict = ex1_persondelta.personatoms.get(kw.DELETE)
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(kw.person_contactunit) is not None
    print(f"atom_order 26 {ex1_persondelta.personatoms.get(kw.DELETE).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_persondelta.get_sorted_personatoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(kw.person_contactunit).keys())
    zia_contactunit_delete = delete_dict.get(kw.person_contactunit).get("Zia")
    # for personatom in sue_atom_order_list:
    #     print(f"{personatom.atom_order=}")
    assert sue_atom_order_list[0] == zia_contactunit_delete
    assert sue_atom_order_list[1] == update_dict.get(kw.personunit)
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PersonDelta_get_sorted_personatoms_ReturnsObj_PlanUnitsSorted():
    # ESTABLISH
    x_moment_rope = exx.a23
    root_rope = to_rope(x_moment_rope)
    sports_str = "sports"
    sports_rope = create_rope(x_moment_rope, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(x_moment_rope, knee_str)
    x_dimen = kw.person_planunit
    sports_insert_planunit_personatom = personatom_shop(x_dimen, kw.INSERT)
    sports_insert_planunit_personatom.set_jkey(kw.plan_rope, sports_rope)
    knee_insert_planunit_personatom = personatom_shop(x_dimen, kw.INSERT)
    knee_insert_planunit_personatom.set_jkey(kw.plan_rope, knee_rope)
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(knee_insert_planunit_personatom)
    x_persondelta.set_personatom(sports_insert_planunit_personatom)

    # WHEN
    x_atom_order_list = x_persondelta.get_sorted_personatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for personatom in x_atom_order_list:
    #     print(f"{personatom.jkeys=}")
    assert x_atom_order_list[0] == knee_insert_planunit_personatom
    assert x_atom_order_list[1] == sports_insert_planunit_personatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PersonDelta_get_sorted_personatoms_ReturnsObj_Rope_Sorted():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(x_moment_rope, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(sports_rope, knee_str)
    x_dimen = kw.person_plan_awardunit
    bowlers_str = ",bowlers"
    sports_awardunit_personatom = personatom_shop(x_dimen, kw.INSERT)
    sports_awardunit_personatom.set_jkey(kw.awardee_title, bowlers_str)
    sports_awardunit_personatom.set_jkey(kw.plan_rope, sports_rope)
    knee_awardunit_personatom = personatom_shop(x_dimen, kw.INSERT)
    knee_awardunit_personatom.set_jkey(kw.awardee_title, bowlers_str)
    knee_awardunit_personatom.set_jkey(kw.plan_rope, knee_rope)
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(knee_awardunit_personatom)
    x_persondelta.set_personatom(sports_awardunit_personatom)

    # WHEN
    x_atom_order_list = x_persondelta.get_sorted_personatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for personatom in x_atom_order_list:
    #     print(f"{personatom.jkeys=}")
    assert x_atom_order_list[0] == sports_awardunit_personatom
    assert x_atom_order_list[1] == knee_awardunit_personatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_person_built_from_delta_is_valid_ReturnsObjEstablishWithNoPerson_Scenario1():
    # ESTABLISH
    sue_persondelta = persondelta_shop()

    x_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    x_attribute = kw.credor_respect
    x_personatom.set_jvalue(x_attribute, 100)
    sue_persondelta.set_personatom(x_personatom)

    dimen = kw.person_contactunit
    x_personatom = personatom_shop(dimen, kw.INSERT)
    x_personatom.set_arg(kw.contact_name, exx.zia)
    x_personatom.set_arg(kw.contact_cred_lumen, "70 is the number")
    sue_persondelta.set_personatom(x_personatom)
    print(f"{sue_persondelta=}")

    # WHEN / THEN
    assert person_built_from_delta_is_valid(sue_persondelta) is False


def test_person_built_from_delta_is_valid_ReturnsObjEstablishWithNoPerson_Scenario2():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_persondelta = persondelta_shop()
    dimen = kw.person_contactunit
    # WHEN
    x_personatom = personatom_shop(dimen, kw.INSERT)
    x_personatom.set_arg(kw.contact_name, exx.yao)
    x_personatom.set_arg(kw.contact_cred_lumen, 30)
    sue_persondelta.set_personatom(x_personatom)

    # THEN
    assert person_built_from_delta_is_valid(sue_persondelta)

    # WHEN
    x_personatom = personatom_shop(dimen, kw.INSERT)
    x_personatom.set_arg(kw.contact_name, exx.bob)
    x_personatom.set_arg(kw.contact_cred_lumen, "70 is the number")
    sue_persondelta.set_personatom(x_personatom)

    # THEN
    assert person_built_from_delta_is_valid(sue_persondelta) is False


def test_PersonDelta_get_ordered_personatoms_ReturnsObj_EstablishWithNoStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_persondelta = persondelta_shop()
    pool_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_personatom.set_jvalue(pool_attribute, 100)
    sue_persondelta.set_personatom(pool_personatom)
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    sue_persondelta.set_personatom(zia_personatom)
    sue_person = personunit_shop(exx.sue)
    sue_person.set_credor_respect(100)
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(kw.contact_cred_lumen, 30)
    sue_persondelta.set_personatom(yao_personatom)

    sue_person = personunit_shop(exx.sue)
    assert person_built_from_delta_is_valid(sue_persondelta, sue_person)

    # WHEN
    persondelta_dict = sue_persondelta.get_ordered_personatoms()

    # THEN
    # delta_zia = persondelta_dict.get(0)
    # delta_yao = persondelta_dict.get(1)
    # delta_pool = persondelta_dict.get(2)
    # assert delta_zia == zia_personatom
    # assert delta_yao == yao_personatom
    # assert delta_pool == pool_personatom
    assert persondelta_dict.get(0) == zia_personatom
    assert persondelta_dict.get(1) == yao_personatom
    assert persondelta_dict.get(2) == pool_personatom


def test_PersonDelta_get_ordered_personatoms_ReturnsObj_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_persondelta = persondelta_shop()
    pool_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_personatom.set_jvalue(pool_attribute, 100)
    sue_persondelta.set_personatom(pool_personatom)
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    sue_persondelta.set_personatom(zia_personatom)
    sue_person = personunit_shop(exx.sue)
    sue_person.set_credor_respect(100)
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(kw.contact_cred_lumen, 30)
    sue_persondelta.set_personatom(yao_personatom)

    sue_person = personunit_shop(exx.sue)
    assert person_built_from_delta_is_valid(sue_persondelta, sue_person)

    # WHEN
    persondelta_dict = sue_persondelta.get_ordered_personatoms(5)

    # THEN
    # delta_zia = persondelta_dict.get(0)
    # delta_yao = persondelta_dict.get(1)
    # delta_pool = persondelta_dict.get(2)
    # assert delta_zia == zia_personatom
    # assert delta_yao == yao_personatom
    # assert delta_pool == pool_personatom
    assert persondelta_dict.get(5) == zia_personatom
    assert persondelta_dict.get(6) == yao_personatom
    assert persondelta_dict.get(7) == pool_personatom


def test_PersonDelta_get_ordered_dict_ReturnsObj_Scenario0_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_persondelta = persondelta_shop()
    pool_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_personatom.set_jvalue(pool_attribute, 100)
    sue_persondelta.set_personatom(pool_personatom)
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    sue_persondelta.set_personatom(zia_personatom)
    sue_person = personunit_shop(exx.sue)
    sue_person.set_credor_respect(100)
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(kw.contact_cred_lumen, 30)
    sue_persondelta.set_personatom(yao_personatom)

    sue_person = personunit_shop(exx.sue)
    assert person_built_from_delta_is_valid(sue_persondelta, sue_person)

    # WHEN
    persondelta_dict = sue_persondelta.get_ordered_dict(5)

    # THEN
    # delta_zia = persondelta_dict.get(0)
    # delta_yao = persondelta_dict.get(1)
    # delta_pool = persondelta_dict.get(2)
    # assert delta_zia == zia_personatom
    # assert delta_yao == yao_personatom
    # assert delta_pool == pool_personatom
    assert persondelta_dict.get(5) == zia_personatom.to_dict()
    assert persondelta_dict.get(6) == yao_personatom.to_dict()
    assert persondelta_dict.get(7) == pool_personatom.to_dict()


def test_PersonDelta_get_ordered_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_persondelta = persondelta_shop()
    pool_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_personatom.set_jvalue(pool_attribute, 100)
    sue_persondelta.set_personatom(pool_personatom)
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    sue_persondelta.set_personatom(zia_personatom)
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(kw.contact_cred_lumen, 30)
    sue_persondelta.set_personatom(yao_personatom)

    # WHEN
    delta_start_int = 5
    persondelta_ordered_dict = sue_persondelta.get_ordered_dict(delta_start_int)

    # THEN
    assert persondelta_ordered_dict


def test_get_persondelta_from_ordered_dict_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    expected_persondelta = persondelta_shop()
    pool_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_personatom.set_jvalue(pool_attribute, 100)
    expected_persondelta.set_personatom(pool_personatom)
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    expected_persondelta.set_personatom(zia_personatom)
    sue_person = personunit_shop(exx.sue)
    sue_person.set_credor_respect(100)
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(kw.contact_cred_lumen, 30)
    expected_persondelta.set_personatom(yao_personatom)
    persondelta_dict = expected_persondelta.get_ordered_dict(5)

    # WHEN
    generated_persondelta = get_persondelta_from_ordered_dict(persondelta_dict)

    # THEN
    # delta_zia = persondelta_dict.get(0)
    # delta_yao = persondelta_dict.get(1)
    # delta_pool = persondelta_dict.get(2)
    # assert delta_zia == zia_personatom
    # assert delta_yao == yao_personatom
    # assert delta_pool == pool_personatom
    # assert persondelta_dict.get(5) == zia_personatom.to_dict()
    # assert persondelta_dict.get(6) == yao_personatom.to_dict()
    # assert persondelta_dict.get(7) == pool_personatom.to_dict()
    assert generated_persondelta == expected_persondelta


def test_PersonDelta_c_personatom_exists_ReturnsObj():
    # ESTABLISH
    x_persondelta = persondelta_shop()

    # WHEN / THEN
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    assert x_persondelta.c_personatom_exists(zia_personatom) is False

    # WHEN
    x_persondelta.set_personatom(zia_personatom)

    # THEN
    assert x_persondelta.c_personatom_exists(zia_personatom)


def test_PersonDelta_is_empty_ReturnsObj():
    # ESTABLISH
    x_persondelta = persondelta_shop()

    # WHEN / THEN
    dimen = kw.person_contactunit
    zia_personatom = personatom_shop(dimen, kw.INSERT)
    zia_personatom.set_arg(kw.contact_name, exx.zia)
    zia_personatom.set_arg(kw.contact_cred_lumen, 70)
    assert x_persondelta.atoms_empty()

    # WHEN
    x_persondelta.set_personatom(zia_personatom)

    # THEN
    assert x_persondelta.atoms_empty() is False
