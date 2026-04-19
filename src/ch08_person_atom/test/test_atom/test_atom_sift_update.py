from ch02_contact.group import awardunit_shop
from ch05_reason.reason_main import factunit_shop, reasonunit_shop
from ch07_person_logic.person_main import personunit_shop
from ch07_person_logic.person_tool import (
    person_plan_factunit_get_obj,
    person_plan_reason_caseunit_get_obj as caseunit_get_obj,
    person_plan_reasonunit_get_obj,
)
from ch08_person_atom.atom_main import personatom_shop, sift_personatom
from ref.keywords import Ch08Keywords as kw, ExampleStrs as exx


def test_sift_atom_ReturnsNoneIfGivenPersonAtomIsUPDATE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    casa_atom = personatom_shop(kw.person_planunit, kw.UPDATE)
    casa_atom.set_arg(kw.parent_rope, sue_person.planroot.plan_label)
    casa_atom.set_arg(kw.plan_label, exx.casa)
    casa_atom.set_arg(kw.star, 8)

    # WHEN
    new_casa_atom = sift_personatom(sue_person, casa_atom)

    # THEN
    assert not new_casa_atom


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_personunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_bit = 34
    sue_credor_respect = 44
    sue_debtor_respect = 54
    sue_fund_grain = 66
    sue_fund_pool = 69
    sue_max_tree_traverse = 72
    sue_mana_grain = 2
    zia_atom = personatom_shop(kw.personunit, kw.INSERT)
    zia_atom.set_arg(kw.respect_grain, sue_bit)
    zia_atom.set_arg(kw.credor_respect, sue_credor_respect)
    zia_atom.set_arg(kw.debtor_respect, sue_debtor_respect)
    zia_atom.set_arg(kw.fund_grain, sue_fund_grain)
    zia_atom.set_arg(kw.fund_pool, sue_fund_pool)
    zia_atom.set_arg(kw.max_tree_traverse, sue_max_tree_traverse)
    zia_atom.set_arg(kw.mana_grain, sue_mana_grain)

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, zia_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    assert zia_jvalues == {
        kw.respect_grain: sue_bit,
        kw.credor_respect: sue_credor_respect,
        kw.debtor_respect: sue_debtor_respect,
        kw.fund_grain: sue_fund_grain,
        kw.fund_pool: sue_fund_pool,
        kw.max_tree_traverse: sue_max_tree_traverse,
        kw.mana_grain: sue_mana_grain,
    }


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_contactunit():
    # ESTABLISH
    zia_contact_debt_lumen = 51
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.zia)

    zia_atom = personatom_shop(kw.person_contactunit, kw.INSERT)
    zia_atom.set_arg(kw.contact_name, exx.zia)
    zia_atom.set_arg(kw.contact_debt_lumen, zia_contact_debt_lumen)

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, zia_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    assert zia_jvalues == {kw.contact_debt_lumen: 51}


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_contact_membership():
    # ESTABLISH
    zia_run_group_debt_lumen = 76
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.zia)
    sue_person.get_contact(exx.zia).add_membership(exx.run)

    zia_atom = personatom_shop(kw.person_contact_membership, kw.INSERT)
    zia_atom.set_arg(kw.contact_name, exx.zia)
    zia_atom.set_arg(kw.group_title, exx.run)
    zia_atom.set_arg(kw.group_debt_lumen, zia_run_group_debt_lumen)

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, zia_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    assert zia_jvalues == {kw.group_debt_lumen: zia_run_group_debt_lumen}


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_planunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)

    sue_addin = 23
    sue_begin = 37
    sue_close = 43
    sue_denom = 47
    sue_gogo_want = 59
    sue_star = 67
    sue_morph = 79
    sue_numor = 83
    sue_pledge = 97
    sue_problem_bool = True
    sue_stop_want = 107
    old_casa_atom = personatom_shop(kw.person_planunit, kw.INSERT)
    old_casa_atom.set_arg(kw.plan_rope, casa_rope)
    old_casa_atom.set_arg(kw.addin, sue_addin)
    old_casa_atom.set_arg(kw.begin, sue_begin)
    old_casa_atom.set_arg(kw.close, sue_close)
    old_casa_atom.set_arg(kw.denom, sue_denom)
    old_casa_atom.set_arg(kw.gogo_want, sue_gogo_want)
    old_casa_atom.set_arg(kw.star, sue_star)
    old_casa_atom.set_arg(kw.morph, sue_morph)
    old_casa_atom.set_arg(kw.numor, sue_numor)
    old_casa_atom.set_arg(kw.pledge, sue_pledge)
    old_casa_atom.set_arg(kw.problem_bool, sue_problem_bool)
    old_casa_atom.set_arg(kw.stop_want, sue_stop_want)

    # WHEN
    new_casa_atom = sift_personatom(sue_person, old_casa_atom)

    # THEN
    assert new_casa_atom
    assert new_casa_atom.crud_str == kw.UPDATE
    assert new_casa_atom.get_jvalues_dict()
    zia_jvalues = new_casa_atom.get_jvalues_dict()
    assert zia_jvalues.get(kw.addin) == sue_addin
    assert zia_jvalues.get(kw.begin) == sue_begin
    assert zia_jvalues.get(kw.close) == sue_close
    assert zia_jvalues.get(kw.denom) == sue_denom
    assert zia_jvalues.get(kw.gogo_want) == sue_gogo_want
    assert zia_jvalues.get(kw.star) == sue_star
    assert zia_jvalues.get(kw.morph) == sue_morph
    assert zia_jvalues.get(kw.numor) == sue_numor
    assert zia_jvalues.get(kw.pledge) == sue_pledge
    assert zia_jvalues.get(kw.problem_bool) == sue_problem_bool
    assert zia_jvalues.get(kw.stop_want) == sue_stop_want


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_plan_awardunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    zia_run_give_force = 72
    zia_run_take_force = 76
    sue_person.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(exx.run, 2, 3))

    zia_atom = personatom_shop(kw.person_plan_awardunit, kw.INSERT)
    zia_atom.set_arg(kw.plan_rope, casa_rope)
    zia_atom.set_arg(kw.awardee_title, exx.run)
    zia_atom.set_arg(kw.give_force, zia_run_give_force)
    zia_atom.set_arg(kw.take_force, zia_run_take_force)

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, zia_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    assert zia_jvalues.get(kw.give_force) == zia_run_give_force
    assert zia_jvalues.get(kw.take_force) == zia_run_take_force


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_plan_reasonunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    sue_person.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    new_active_requisite = True
    casa_atom = personatom_shop(kw.person_plan_reasonunit, kw.INSERT)
    casa_atom.set_arg(kw.plan_rope, casa_rope)
    casa_atom.set_arg(kw.reason_context, wk_rope)
    casa_atom.set_arg(kw.active_requisite, new_active_requisite)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_reasonunit = person_plan_reasonunit_get_obj(sue_person, casa_jkeys)
    assert casa_reasonunit.active_requisite != new_active_requisite
    assert casa_reasonunit.active_requisite is None

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, casa_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    zia_requisite_value = zia_jvalues.get(kw.active_requisite)
    assert zia_requisite_value == new_active_requisite


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_plan_reason_caseunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    wk_rope = sue_person.make_l1_rope("wk")
    thur_str = "thur"
    thur_rope = sue_person.make_rope(wk_rope, thur_str)
    sue_person.add_plan(clean_rope)
    sue_person.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))
    clean_plan = sue_person.get_plan_obj(clean_rope)
    clean_plan.set_reasonunit(reasonunit_shop(wk_rope))
    clean_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    thur_reason_divisor = 39
    thur_atom = personatom_shop(kw.person_plan_reason_caseunit, kw.INSERT)
    thur_atom.set_arg(kw.plan_rope, clean_rope)
    thur_atom.set_arg(kw.reason_context, wk_rope)
    thur_atom.set_arg(kw.reason_state, thur_rope)
    assert thur_atom.is_valid()
    thur_atom.set_arg(kw.reason_divisor, thur_reason_divisor)
    thur_jkeys = thur_atom.get_jkeys_dict()
    thur_caseunit = caseunit_get_obj(sue_person, thur_jkeys)
    assert thur_caseunit.reason_divisor != thur_reason_divisor
    assert thur_caseunit.reason_divisor is None

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, thur_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    assert zia_jvalues.get(kw.reason_divisor) == thur_reason_divisor


def test_sift_atom_ReturnsObj_PersonAtom_UPDATE_person_plan_factunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_plan(casa_rope)
    sue_person.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    casa_fact_lower = 32
    casa_atom = personatom_shop(kw.person_plan_factunit, kw.INSERT)
    casa_atom.set_arg(kw.plan_rope, casa_rope)
    casa_atom.set_arg(kw.fact_context, wk_rope)
    casa_atom.set_arg(kw.fact_lower, casa_fact_lower)
    casa_jkeys = casa_atom.get_jkeys_dict()
    casa_factunit = person_plan_factunit_get_obj(sue_person, casa_jkeys)
    assert casa_factunit.fact_lower != casa_fact_lower
    assert casa_factunit.fact_lower is None

    # WHEN
    new_zia_personatom = sift_personatom(sue_person, casa_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom.crud_str == kw.UPDATE
    assert new_zia_personatom.get_jvalues_dict() != {}
    zia_jvalues = new_zia_personatom.get_jvalues_dict()
    assert zia_jvalues.get(kw.fact_lower) == casa_fact_lower
