from src.ch04_rope.rope import create_rope, to_rope
from src.ch08_person_atom.atom_config import get_atom_args_class_types
from src.ch08_person_atom.atom_main import AtomRow, atomrow_shop, personatom_shop
from src.ref.keywords import Ch08Keywords as kw


def test_AtomRow_Exists():
    # ESTABLISH /  WHEN
    x_atomrow = AtomRow()

    # THEN
    assert x_atomrow._atom_dimens is None
    assert x_atomrow._crud_command is None
    assert x_atomrow.contact_name is None
    assert x_atomrow.addin is None
    assert x_atomrow.reason_context is None
    assert x_atomrow.active_requisite is None
    assert x_atomrow.begin is None
    assert x_atomrow.respect_grain is None
    assert x_atomrow.close is None
    assert x_atomrow.contact_cred_lumen is None
    assert x_atomrow.group_cred_lumen is None
    assert x_atomrow.credor_respect is None
    assert x_atomrow.contact_debt_lumen is None
    assert x_atomrow.group_debt_lumen is None
    assert x_atomrow.debtor_respect is None
    assert x_atomrow.denom is None
    assert x_atomrow.reason_divisor is None
    assert x_atomrow.fact_context is None
    assert x_atomrow.fact_upper is None
    assert x_atomrow.fact_lower is None
    assert x_atomrow.fund_grain is None
    assert x_atomrow.fund_pool is None
    assert x_atomrow.give_force is None
    assert x_atomrow.gogo_want is None
    assert x_atomrow.group_title is None
    assert x_atomrow.healer_name is None
    assert x_atomrow.solo is None
    assert x_atomrow.star is None
    assert x_atomrow.max_tree_traverse is None
    assert x_atomrow.morph is None
    assert x_atomrow.reason_state is None
    assert x_atomrow.reason_upper is None
    assert x_atomrow.numor is None
    assert x_atomrow.reason_lower is None
    assert x_atomrow.mana_grain is None
    assert x_atomrow.fact_state is None
    assert x_atomrow.pledge is None
    assert x_atomrow.problem_bool is None
    assert x_atomrow.plan_rope is None
    assert x_atomrow.stop_want is None
    assert x_atomrow.take_force is None

    print(f"{set(x_atomrow.__dict__.keys())=}")
    print(f"{set(get_atom_args_class_types().keys())=}")
    atomrow_args_set = set(x_atomrow.__dict__.keys())
    atomrow_args_set.remove("_atom_dimens")
    atomrow_args_set.remove("_crud_command")
    config_args_set = set(get_atom_args_class_types().keys())
    assert atomrow_args_set == config_args_set


def test_atomrow_shop_ReturnsObj():
    # ESTABLISH
    x_atom_dimens = {kw.person_contactunit}

    # WHEN
    x_atomrow = atomrow_shop(x_atom_dimens, kw.INSERT)

    # THEN
    assert x_atomrow._atom_dimens == x_atom_dimens
    assert x_atomrow._crud_command == kw.INSERT


def test_AtomRow_set_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({kw.person_contactunit}, kw.INSERT)
    assert kw.person_contact_membership not in x_atomrow._atom_dimens

    # WHEN
    x_atomrow.set_atom_dimen(kw.person_contact_membership)

    # THEN
    assert kw.person_contact_membership in x_atomrow._atom_dimens


def test_AtomRow_atom_dimen_exists_ReturnsObj():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), kw.INSERT)
    assert not x_atomrow.atom_dimen_exists(kw.person_contactunit)
    assert not x_atomrow.atom_dimen_exists(kw.person_contact_membership)

    # WHEN
    x_atomrow.set_atom_dimen(kw.person_contact_membership)

    # THEN
    assert not x_atomrow.atom_dimen_exists(kw.person_contactunit)
    assert x_atomrow.atom_dimen_exists(kw.person_contact_membership)


def test_AtomRow_delete_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({kw.person_contactunit}, kw.INSERT)
    x_atomrow.set_atom_dimen(kw.person_contactunit)
    x_atomrow.set_atom_dimen(kw.person_contact_membership)
    assert x_atomrow.atom_dimen_exists(kw.person_contactunit)
    assert x_atomrow.atom_dimen_exists(kw.person_contact_membership)

    # WHEN
    x_atomrow.delete_atom_dimen(kw.person_contact_membership)

    # THEN
    assert x_atomrow.atom_dimen_exists(kw.person_contactunit)
    assert not x_atomrow.atom_dimen_exists(kw.person_contact_membership)


def test_AtomRow_set_class_types_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({}, kw.INSERT)
    x_atomrow.close = "4"
    x_parent_rope = "Fay_bob"
    x_plan_label = "Bobziy"
    x_morph_str = "True"
    x_morph_bool = True
    x_rope = create_rope(x_parent_rope, x_plan_label)
    x_atomrow.plan_rope = x_rope
    x_atomrow.morph = x_morph_str
    four_int = 4
    assert x_atomrow.close != four_int
    assert x_atomrow.plan_rope == x_rope
    assert x_atomrow.morph == x_morph_str

    # WHEN
    x_atomrow._set_class_types()

    # THEN
    assert x_atomrow.close == four_int
    assert x_atomrow.plan_rope == x_rope
    assert x_atomrow.morph == x_morph_bool


def test_AtomRow_get_personatoms_ReturnsObj_Scenario0_person_contactunit_str_INSERT():
    # ESTABLISH
    x_dimen = kw.person_contactunit
    x_atomrow = atomrow_shop({x_dimen}, kw.INSERT)
    x_atomrow.contact_name = "Bob"

    # WHEN
    x_personatoms = x_atomrow.get_personatoms()

    # THEN
    assert len(x_personatoms) == 1
    static_atom = personatom_shop(x_dimen, kw.INSERT)
    static_atom.set_arg(kw.contact_name, "Bob")
    assert x_personatoms[0] == static_atom


def test_AtomRow_get_personatoms_ReturnsObj_Scenario1_person_contactunit_str_INSERT():
    # ESTABLISH
    x_dimen = kw.person_contactunit
    x_atomrow = atomrow_shop({x_dimen}, kw.INSERT)
    x_atomrow.contact_name = "Bob"
    x_atomrow.contact_cred_lumen = 5

    # WHEN
    x_personatoms = x_atomrow.get_personatoms()

    # THEN
    assert len(x_personatoms) == 1
    static_atom = personatom_shop(x_dimen, kw.INSERT)
    static_atom.set_arg(kw.contact_name, "Bob")
    static_atom.set_arg("contact_cred_lumen", 5)
    assert x_personatoms[0] == static_atom


def test_AtomRow_get_personatoms_ReturnsObj_Scenario2_person_contactunit_NSERT_Fails():
    # ESTABLISH
    x_dimen = kw.person_contactunit
    x_atomrow = atomrow_shop({x_dimen}, kw.INSERT)

    # WHEN
    x_personatoms = x_atomrow.get_personatoms()

    # THEN
    assert len(x_personatoms) == 0


def test_AtomRow_get_personatoms_ReturnsObj_Scenario3_person_contactunit_INSERT():
    # ESTABLISH
    x_dimen = kw.person_contactunit
    x_atomrow = atomrow_shop({x_dimen}, kw.INSERT)
    x_atomrow.contact_name = "Bob"
    four_str = "4"
    x_atomrow.contact_cred_lumen = four_str

    # WHEN
    x_personatoms = x_atomrow.get_personatoms()

    # THEN
    assert len(x_personatoms) == 1
    static_atom = personatom_shop(x_dimen, kw.INSERT)
    static_atom.set_arg(kw.contact_name, "Bob")
    four_int = 4
    static_atom.set_arg("contact_cred_lumen", four_int)
    assert x_personatoms[0] == static_atom


def test_AtomRow_get_personatoms_ReturnsObj_Scenario4_IfDimenIsCorrect():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), kw.INSERT)
    x_atomrow.contact_name = "Bob"
    four_str = "4"
    x_atomrow.contact_cred_lumen = four_str
    assert len(x_atomrow.get_personatoms()) == 0

    # WHEN / THEN
    x_atomrow.set_atom_dimen(kw.person_contact_membership)
    assert len(x_atomrow.get_personatoms()) == 0

    # THEN
    x_atomrow.set_atom_dimen(kw.person_contactunit)
    assert len(x_atomrow.get_personatoms()) == 1


def test_AtomRow_get_personatoms_ReturnsObj_Scenario5_person_planunit_INSERT_pledge_False():
    # ESTABLISH
    x_atomrow = atomrow_shop({kw.person_planunit}, kw.INSERT)
    x_atomrow.plan_rope = create_rope("amy78", "casa")
    x_atomrow.pledge = False
    assert len(x_atomrow.get_personatoms()) == 1

    # WHEN / THEN
    x_personatom = x_atomrow.get_personatoms()[0]

    # THEN
    static_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    static_personatom.set_arg(kw.plan_rope, create_rope("amy78", "casa"))
    static_personatom.set_arg(kw.pledge, False)
    print(static_personatom)
    print(x_personatom)
    assert x_personatom == static_personatom


def test_AtomRow_get_personatoms_ReturnsObj_Scenario6_person_planunit_INSERT_pledge_False():
    # ESTABLISH
    x_dimens = {kw.person_planunit, kw.person_plan_healerunit}
    x_atomrow = atomrow_shop(x_dimens, kw.INSERT)
    x_atomrow.plan_rope = create_rope("amy78", "casa")
    x_atomrow.pledge = False
    x_atomrow.healer_name = "Bob"

    # WHEN / THEN
    x_personatoms = x_atomrow.get_personatoms()

    # THEN
    assert len(x_personatoms) == 2
    y_plan_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    casa_rope = create_rope("amy78", "casa")
    y_plan_personatom.set_arg(kw.plan_rope, casa_rope)
    y_plan_personatom.set_arg(kw.pledge, False)
    assert y_plan_personatom in x_personatoms
    healerunit_personatom = personatom_shop(kw.person_plan_healerunit, kw.INSERT)
    healerunit_personatom.set_arg(kw.plan_rope, casa_rope)
    healerunit_personatom.set_arg("healer_name", "Bob")
    assert healerunit_personatom in x_personatoms
