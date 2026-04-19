from ch07_person_logic.person_main import personunit_shop
from ch08_person_atom.atom_main import personatom_shop
from ch09_person_lesson.delta import persondelta_shop
from ch09_person_lesson.legible import create_legible_list
from ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_planunit_INSERT():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_planunit
    _problem_bool_str = kw.problem_bool
    clean_label = "clean fridge"
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    star_value = 43
    pledge_value = False
    clean_personatom = personatom_shop(dimen, kw.INSERT)
    clean_personatom.set_arg(kw.plan_rope, clean_rope)
    clean_personatom.set_arg(kw.addin, addin_value)
    clean_personatom.set_arg(kw.begin, begin_value)
    clean_personatom.set_arg(kw.close, close_value)
    clean_personatom.set_arg(kw.denom, denom_value)
    clean_personatom.set_arg(kw.numor, numor_value)
    clean_personatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_personatom.set_arg(kw.morph, morph_value)
    clean_personatom.set_arg(kw.star, star_value)
    clean_personatom.set_arg(kw.pledge, pledge_value)

    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(clean_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Created Plan '{clean_rope}'. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.star={star_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_UPDATE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_planunit
    _problem_bool_str = kw.problem_bool
    clean_label = "clean fridge"
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    star_value = 43
    pledge_value = False
    clean_personatom = personatom_shop(dimen, kw.UPDATE)
    clean_personatom.set_arg(kw.plan_rope, clean_rope)
    clean_personatom.set_arg(kw.addin, addin_value)
    clean_personatom.set_arg(kw.begin, begin_value)
    clean_personatom.set_arg(kw.close, close_value)
    clean_personatom.set_arg(kw.denom, denom_value)
    clean_personatom.set_arg(kw.numor, numor_value)
    clean_personatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_personatom.set_arg(kw.morph, morph_value)
    clean_personatom.set_arg(kw.star, star_value)
    clean_personatom.set_arg(kw.pledge, pledge_value)

    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(clean_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Plan '{clean_rope}' set these attrs: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.star={star_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_planunit_DELETE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_planunit
    clean_label = "clean fridge"
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, clean_label)
    clean_personatom = personatom_shop(dimen, kw.DELETE)
    clean_personatom.set_arg(kw.plan_rope, clean_rope)

    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(clean_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Plan '{clean_rope}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
