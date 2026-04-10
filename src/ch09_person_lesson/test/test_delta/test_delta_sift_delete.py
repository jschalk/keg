# from src.ch07_person_logic.person_tool import pass
from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import get_minimal_persondelta, persondelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_get_minimal_persondelta_ReturnsObjWithoutUnecessaryDELETE_person_contactunit():
    # ESTABLISH persondelta with 2 contactunits, persondelta DELETE 3 persondeltas,
    # assert persondelta has 3 atoms
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)

    contacts_persondelta = persondelta_shop()
    bob_atom = personatom_shop(kw.person_contactunit, kw.DELETE)
    bob_atom.set_arg(kw.contact_name, exx.bob)
    yao_atom = personatom_shop(kw.person_contactunit, kw.DELETE)
    yao_atom.set_arg(kw.contact_name, exx.yao)
    zia_atom = personatom_shop(kw.person_contactunit, kw.DELETE)
    zia_atom.set_arg(kw.contact_name, exx.zia)
    contacts_persondelta.set_personatom(bob_atom)
    contacts_persondelta.set_personatom(yao_atom)
    contacts_persondelta.set_personatom(zia_atom)
    assert len(contacts_persondelta.get_sorted_personatoms()) == 3
    assert len(sue_person.contacts) == 2

    # WHEN
    new_persondelta = get_minimal_persondelta(contacts_persondelta, sue_person)

    # THEN
    assert len(new_persondelta.get_sorted_personatoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_person_contact_membership():
    # ESTABLISH persondelta with 2 contactunits, persondelta DELETE 3 persondeltas,
    # assert persondelta has 3 atoms
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    yao_contactunit = sue_person.get_contact(exx.yao)
    bowlers_str = ";bowlers"
    yao_contactunit.add_membership(exx.run)
    yao_contactunit.add_membership(bowlers_str)
    print(f"{yao_contactunit.memberships.keys()=}")

    contacts_persondelta = persondelta_shop()
    bob_run_atom = personatom_shop(kw.person_contact_membership, kw.DELETE)
    bob_run_atom.set_arg(kw.contact_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = personatom_shop(kw.person_contact_membership, kw.DELETE)
    yao_run_atom.set_arg(kw.contact_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)
    zia_run_atom = personatom_shop(kw.person_contact_membership, kw.DELETE)
    zia_run_atom.set_arg(kw.contact_name, exx.zia)
    zia_run_atom.set_arg(kw.group_title, exx.run)
    contacts_persondelta.set_personatom(bob_run_atom)
    contacts_persondelta.set_personatom(yao_run_atom)
    contacts_persondelta.set_personatom(zia_run_atom)
    print(f"{len(contacts_persondelta.get_dimen_sorted_personatoms_list())=}")
    assert len(contacts_persondelta.get_dimen_sorted_personatoms_list()) == 3

    # WHEN
    new_persondelta = get_minimal_persondelta(contacts_persondelta, sue_person)

    # THEN
    assert len(new_persondelta.get_dimen_sorted_personatoms_list()) == 1
