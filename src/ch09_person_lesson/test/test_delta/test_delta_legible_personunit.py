from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObjEstablishWithEmptyPersonDelta():
    # ESTABLISH / WHEN
    x_persondelta = persondelta_shop()
    sue_person = personunit_shop("Sue")

    # THEN
    assert create_legible_list(x_persondelta, sue_person) == []


def test_create_legible_list_ReturnsObjEstablishWithPersonUpdate_credor_respect():
    # ESTABLISH
    dimen = kw.personunit
    credor_respect_int = 71
    credor_respect_personatom = personatom_shop(dimen, kw.UPDATE)
    credor_respect_personatom.set_arg(kw.credor_respect, credor_respect_int)

    print(f"{credor_respect_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(credor_respect_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{sue_person.person_name}'s credor pool is now {credor_respect_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPersonUpdate_debtor_respect():
    # ESTABLISH
    dimen = kw.personunit
    contact_debtor_pool_int = 78
    contact_debtor_pool_personatom = personatom_shop(dimen, kw.UPDATE)
    contact_debtor_pool_personatom.set_arg(kw.debtor_respect, contact_debtor_pool_int)

    print(f"{contact_debtor_pool_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(contact_debtor_pool_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{sue_person.person_name}'s debtor pool is now {contact_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPersonUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_persondelta = persondelta_shop()
    dimen = kw.personunit
    contact_pool_int = 83
    personunit_personatom = personatom_shop(dimen, kw.UPDATE)
    personunit_personatom.set_arg(kw.credor_respect, contact_pool_int)
    personunit_personatom.set_arg(kw.debtor_respect, contact_pool_int)
    x_persondelta.set_personatom(personunit_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{sue_person.person_name}'s total pool is now {contact_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPersonUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = kw.personunit
    max_tree_traverse_str = kw.max_tree_traverse
    max_tree_traverse_int = 71
    max_tree_traverse_personatom = personatom_shop(dimen, kw.UPDATE)
    max_tree_traverse_personatom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(max_tree_traverse_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{sue_person.person_name}'s maximum number of Person evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
