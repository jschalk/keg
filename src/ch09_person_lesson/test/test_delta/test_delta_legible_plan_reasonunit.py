from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_With_active_requisite():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_reasonunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_person.knot}bowlers"
    active_requisite_value = True
    bowl_personatom = personatom_shop(dimen, kw.INSERT)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.reason_context, reason_context_value)
    bowl_personatom.set_arg(kw.active_requisite, active_requisite_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with reason_context '{reason_context_value}'. active_requisite={active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_INSERT_Without_active_requisite():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_reasonunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_person.knot}bowlers"
    bowl_personatom = personatom_shop(dimen, kw.INSERT)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"ReasonUnit created for plan '{rope_value}' with reason_context '{reason_context_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_active_requisite_IsTrue():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_reasonunit
    reason_context_value = f"{sue_person.knot}bowlers"
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    active_requisite_value = True
    bowl_personatom = personatom_shop(dimen, kw.UPDATE)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.reason_context, reason_context_value)
    bowl_personatom.set_arg(kw.active_requisite, active_requisite_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' set with active_requisite={active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_UPDATE_active_requisite_IsNone():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_reasonunit
    reason_context_value = f"{sue_person.knot}bowlers"
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    bowl_personatom = personatom_shop(dimen, kw.UPDATE)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' and no longer checks reason_context active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reasonunit_DELETE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_reasonunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_person.knot}bowlers"
    bowl_personatom = personatom_shop(dimen, kw.DELETE)
    bowl_personatom.set_arg(kw.plan_rope, rope_value)
    bowl_personatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{bowl_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(bowl_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
