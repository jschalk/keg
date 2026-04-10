from src.ch02_contact.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop, sift_personatom
from src.ref.keywords import Ch08Keywords as kw, ExampleStrs as exx


def test_sift_atom_ReturnsObj_PersonAtom_DELETE_person_contactunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.zia)

    bob_atom = personatom_shop(kw.person_contactunit, kw.DELETE)
    bob_atom.set_arg(kw.contact_name, exx.bob)
    zia_atom = personatom_shop(kw.person_contactunit, kw.DELETE)
    zia_atom.set_arg(kw.contact_name, exx.zia)

    # WHEN
    new_bob_personatom = sift_personatom(sue_person, bob_atom)
    new_zia_personatom = sift_personatom(sue_person, zia_atom)

    # THEN
    assert new_zia_personatom
    assert new_zia_personatom == zia_atom
    assert not new_bob_personatom


def test_sift_atom_ReturnsObj_PersonAtom_DELETE_person_contact_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    yao_contactunit = sue_person.get_contact(exx.yao)
    yao_contactunit.add_membership(exx.run)
    print(f"{yao_contactunit.memberships.keys()=}")

    bob_run_atom = personatom_shop(kw.person_contact_membership, kw.DELETE)
    bob_run_atom.set_arg(kw.contact_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = personatom_shop(kw.person_contact_membership, kw.DELETE)
    yao_run_atom.set_arg(kw.contact_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)

    # WHEN
    new_bob_run_personatom = sift_personatom(sue_person, bob_run_atom)
    new_yao_run_personatom = sift_personatom(sue_person, yao_run_atom)

    # THEN
    assert new_yao_run_personatom
    assert new_yao_run_personatom == yao_run_atom
    assert not new_bob_run_personatom


def test_sift_atom_ReturnsObj_PersonAtom_DELETE_person_planunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    root_rope = sue_person.planroot.get_plan_rope()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)

    sweep_rope = sue_person.make_rope(clean_rope, exx.sweep)

    root_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    root_atom.set_arg(kw.plan_rope, root_rope)
    casa_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    casa_atom.set_arg(kw.plan_rope, casa_rope)
    clean_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    clean_atom.set_arg(kw.plan_rope, clean_rope)
    sweep_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    sweep_atom.set_arg(kw.plan_rope, sweep_rope)
    assert sift_personatom(sue_person, root_atom)
    assert not sift_personatom(sue_person, casa_atom)
    assert not sift_personatom(sue_person, clean_atom)
    assert not sift_personatom(sue_person, sweep_atom)

    # WHEN
    sue_person.add_plan(casa_rope)
    # THEN
    assert sift_personatom(sue_person, root_atom)
    assert sift_personatom(sue_person, casa_atom)
    assert not sift_personatom(sue_person, clean_atom)
    assert not sift_personatom(sue_person, sweep_atom)

    # WHEN
    sue_person.add_plan(clean_rope)
    # THEN
    assert sift_personatom(sue_person, root_atom)
    assert sift_personatom(sue_person, casa_atom)
    assert sift_personatom(sue_person, clean_atom)
    assert not sift_personatom(sue_person, sweep_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_planunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    root_rope = sue_person.planroot.get_plan_rope()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)

    sweep_rope = sue_person.make_rope(clean_rope, exx.sweep)

    casa_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    casa_atom.set_arg(kw.plan_rope, casa_rope)
    clean_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    clean_atom.set_arg(kw.plan_rope, clean_rope)
    sweep_atom = personatom_shop(kw.person_planunit, kw.DELETE)
    sweep_atom.set_arg(kw.plan_rope, sweep_rope)
    assert not sift_personatom(sue_person, casa_atom)
    assert not sift_personatom(sue_person, clean_atom)
    assert not sift_personatom(sue_person, sweep_atom)

    # WHEN
    sue_person.add_plan(casa_rope)
    # THEN
    assert sift_personatom(sue_person, casa_atom)
    assert not sift_personatom(sue_person, clean_atom)
    assert not sift_personatom(sue_person, sweep_atom)

    # WHEN
    sue_person.add_plan(clean_rope)
    # THEN
    assert sift_personatom(sue_person, casa_atom)
    assert sift_personatom(sue_person, clean_atom)
    assert not sift_personatom(sue_person, sweep_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_plan_awardunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    bowlers_str = "bowlers"

    casa_bowl_atom = personatom_shop(kw.person_plan_awardunit, kw.DELETE)
    casa_bowl_atom.set_arg(kw.plan_rope, casa_rope)
    casa_bowl_atom.set_arg(kw.awardee_title, bowlers_str)
    clean_bowl_atom = personatom_shop(kw.person_plan_awardunit, kw.DELETE)
    clean_bowl_atom.set_arg(kw.plan_rope, clean_rope)
    clean_bowl_atom.set_arg(kw.awardee_title, bowlers_str)
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    assert not sift_personatom(sue_person, casa_bowl_atom)
    assert not sift_personatom(sue_person, clean_bowl_atom)

    # WHEN
    sue_person.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(bowlers_str))

    # THEN
    assert sift_personatom(sue_person, casa_bowl_atom)
    assert not sift_personatom(sue_person, clean_bowl_atom)

    # WHEN
    sue_person.get_plan_obj(clean_rope).set_awardunit(awardunit_shop(bowlers_str))
    # THEN
    assert sift_personatom(sue_person, casa_bowl_atom)
    assert sift_personatom(sue_person, clean_bowl_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_plan_reasonunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    wk_rope = sue_person.make_l1_rope("wk")

    casa_wk_atom = personatom_shop(kw.person_plan_reasonunit, kw.DELETE)
    casa_wk_atom.set_arg(kw.plan_rope, casa_rope)
    casa_wk_atom.set_arg(kw.reason_context, wk_rope)
    clean_wk_atom = personatom_shop(kw.person_plan_reasonunit, kw.DELETE)
    clean_wk_atom.set_arg(kw.plan_rope, clean_rope)
    clean_wk_atom.set_arg(kw.reason_context, wk_rope)
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    assert not sift_personatom(sue_person, casa_wk_atom)
    assert not sift_personatom(sue_person, clean_wk_atom)

    # WHEN
    sue_person.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert sift_personatom(sue_person, casa_wk_atom)
    assert not sift_personatom(sue_person, clean_wk_atom)

    # WHEN
    sue_person.get_plan_obj(clean_rope).set_reasonunit(reasonunit_shop(wk_rope))
    # THEN
    assert sift_personatom(sue_person, casa_wk_atom)
    assert sift_personatom(sue_person, clean_wk_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_plan_reason_caseunit_Exists():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    wk_rope = sue_person.make_l1_rope("wk")
    thur_str = "thur"
    thur_rope = sue_person.make_rope(wk_rope, thur_str)

    casa_wk_atom = personatom_shop(kw.person_plan_reason_caseunit, kw.DELETE)
    casa_wk_atom.set_arg(kw.plan_rope, casa_rope)
    casa_wk_atom.set_arg(kw.reason_context, wk_rope)
    casa_wk_atom.set_arg(kw.reason_state, thur_rope)
    clean_wk_atom = personatom_shop(kw.person_plan_reason_caseunit, kw.DELETE)
    clean_wk_atom.set_arg(kw.plan_rope, clean_rope)
    clean_wk_atom.set_arg(kw.reason_context, wk_rope)
    clean_wk_atom.set_arg(kw.reason_state, thur_rope)
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    casa_plan = sue_person.get_plan_obj(casa_rope)
    clean_plan = sue_person.get_plan_obj(clean_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    clean_plan.set_reasonunit(reasonunit_shop(wk_rope))
    assert not sift_personatom(sue_person, casa_wk_atom)
    assert not sift_personatom(sue_person, clean_wk_atom)

    # WHEN
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert sift_personatom(sue_person, casa_wk_atom)
    assert not sift_personatom(sue_person, clean_wk_atom)

    # WHEN
    clean_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert sift_personatom(sue_person, casa_wk_atom)
    assert sift_personatom(sue_person, clean_wk_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_plan_laborunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    bowlers_str = "bowlers"

    casa_bowl_atom = personatom_shop(kw.person_plan_laborunit, kw.DELETE)
    casa_bowl_atom.set_arg(kw.plan_rope, casa_rope)
    casa_bowl_atom.set_arg(kw.labor_title, bowlers_str)
    clean_bowl_atom = personatom_shop(kw.person_plan_laborunit, kw.DELETE)
    clean_bowl_atom.set_arg(kw.plan_rope, clean_rope)
    clean_bowl_atom.set_arg(kw.labor_title, bowlers_str)
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    assert not sift_personatom(sue_person, casa_bowl_atom)
    assert not sift_personatom(sue_person, clean_bowl_atom)

    # WHEN
    sue_person.get_plan_obj(casa_rope).workforceunit.add_labor(bowlers_str)

    # THEN
    assert sift_personatom(sue_person, casa_bowl_atom)
    assert not sift_personatom(sue_person, clean_bowl_atom)

    # WHEN
    sue_person.get_plan_obj(clean_rope).workforceunit.add_labor(bowlers_str)
    # THEN
    assert sift_personatom(sue_person, casa_bowl_atom)
    assert sift_personatom(sue_person, clean_bowl_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_plan_healerunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    bowlers_str = "bowlers"

    casa_bowl_atom = personatom_shop(kw.person_plan_healerunit, kw.DELETE)
    casa_bowl_atom.set_arg(kw.plan_rope, casa_rope)
    casa_bowl_atom.set_arg(kw.healer_name, bowlers_str)
    clean_bowl_atom = personatom_shop(kw.person_plan_healerunit, kw.DELETE)
    clean_bowl_atom.set_arg(kw.plan_rope, clean_rope)
    clean_bowl_atom.set_arg(kw.healer_name, bowlers_str)
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    assert not sift_personatom(sue_person, casa_bowl_atom)
    assert not sift_personatom(sue_person, clean_bowl_atom)

    # WHEN
    sue_person.get_plan_obj(casa_rope).healerunit.set_healer_name(bowlers_str)

    # THEN
    assert sift_personatom(sue_person, casa_bowl_atom)
    assert not sift_personatom(sue_person, clean_bowl_atom)

    # WHEN
    sue_person.get_plan_obj(clean_rope).healerunit.set_healer_name(bowlers_str)
    # THEN
    assert sift_personatom(sue_person, casa_bowl_atom)
    assert sift_personatom(sue_person, clean_bowl_atom)


def test_sift_atom_SetsPersonDeltaPersonAtom_person_plan_factunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    wk_rope = sue_person.make_l1_rope("wk")

    casa_wk_atom = personatom_shop(kw.person_plan_factunit, kw.DELETE)
    casa_wk_atom.set_arg(kw.plan_rope, casa_rope)
    casa_wk_atom.set_arg(kw.fact_context, wk_rope)
    clean_wk_atom = personatom_shop(kw.person_plan_factunit, kw.DELETE)
    clean_wk_atom.set_arg(kw.plan_rope, clean_rope)
    clean_wk_atom.set_arg(kw.fact_context, wk_rope)
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    assert not sift_personatom(sue_person, casa_wk_atom)
    assert not sift_personatom(sue_person, clean_wk_atom)

    # WHEN
    sue_person.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # THEN
    assert sift_personatom(sue_person, casa_wk_atom)
    assert not sift_personatom(sue_person, clean_wk_atom)

    # WHEN
    sue_person.get_plan_obj(clean_rope).set_factunit(factunit_shop(wk_rope))
    # THEN
    assert sift_personatom(sue_person, casa_wk_atom)
    assert sift_personatom(sue_person, clean_wk_atom)
