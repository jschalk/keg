from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_factunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_person.make_l1_rope("casa")
    fact_context_value = sue_person.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_person.make_rope(fact_context_value, "dirty")
    bowl_personatom = personatom_shop(dimen, kw.INSERT)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.fact_context, fact_context_value)
    bowl_personatom.set_arg(kw.fact_state, fact_state_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' created for reason_context '{fact_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_factunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_person.make_l1_rope("casa")
    reason_context_value = sue_person.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_person.make_rope(reason_context_value, "dirty")
    fact_upper_value = 13
    fact_lower_value = 17
    bowl_personatom = personatom_shop(dimen, kw.INSERT)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.fact_context, reason_context_value)
    bowl_personatom.set_arg(kw.fact_state, fact_state_value)
    bowl_personatom.set_arg(kw.fact_upper, fact_upper_value)
    bowl_personatom.set_arg(kw.fact_lower, fact_lower_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' created for reason_context '{reason_context_value}' for plan '{rope_value}'. fact_lower={fact_lower_value}. fact_upper={fact_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_factunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_person.make_l1_rope("casa")
    reason_context_value = sue_person.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_person.make_rope(reason_context_value, "dirty")
    bowl_personatom = personatom_shop(dimen, kw.UPDATE)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.fact_context, reason_context_value)
    bowl_personatom.set_arg(kw.fact_state, fact_state_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{reason_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_factunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_person.make_l1_rope("casa")
    reason_context_value = sue_person.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_person.make_rope(reason_context_value, "dirty")
    fact_upper_value = 13
    fact_lower_value = 17
    bowl_personatom = personatom_shop(dimen, kw.UPDATE)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.fact_context, reason_context_value)
    bowl_personatom.set_arg(kw.fact_state, fact_state_value)
    bowl_personatom.set_arg(kw.fact_upper, fact_upper_value)
    bowl_personatom.set_arg(kw.fact_lower, fact_lower_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{reason_context_value}' for plan '{rope_value}'. fact_lower={fact_lower_value}. fact_upper={fact_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_DELETE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_factunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_person.make_l1_rope("casa")
    reason_context_value = sue_person.make_rope(casa_rope, "fridge situation")
    bowl_personatom = personatom_shop(dimen, kw.DELETE)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.fact_context, reason_context_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"FactUnit reason_context '{reason_context_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
