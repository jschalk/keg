from src.ch02_contact.group import awardunit_shop
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.person_tool import (
    person_contact_membership_get_obj,
    person_contactunit_get_obj,
    person_get_obj,
    person_plan_awardunit_get_obj,
    person_plan_factunit_get_obj,
    person_plan_reason_caseunit_get_obj as caseunit_get_obj,
    person_plan_reasonunit_get_obj,
    person_planunit_get_obj,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_person_contactunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao}
    sue_person.add_contactunit(exx.yao)

    # WHEN
    x_obj = person_contactunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_contact(exx.yao)


def test_person_contact_membership_get_obj_ReturnsObj():
    # ESTABLISH
    bowlers_str = ";bowlers"
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao, "group_title": bowlers_str}
    sue_person.add_contactunit(exx.yao)
    sue_person.get_contact(exx.yao).add_membership(bowlers_str)

    # WHEN
    x_obj = person_contact_membership_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_contact(exx.yao).get_membership(bowlers_str)


def test_person_planunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope}

    # WHEN
    x_obj = person_planunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope)


def test_person_plan_awardunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope, kw.awardee_title: exx.bowl}
    sue_person.add_plan(casa_rope)
    sue_person.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(exx.bowl))

    # WHEN
    x_obj = person_plan_awardunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope).get_awardunit(exx.bowl)


def test_person_plan_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope, kw.reason_context: wk_rope}
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(wk_rope)
    sue_person.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = person_plan_reasonunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope).get_reasonunit(wk_rope)


def test_person_plan_reason_caseunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.plan_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(wk_rope)
    sue_person.add_plan(thur_rope)
    casa_plan = sue_person.get_plan_obj(casa_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = caseunit_get_obj(sue_person, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_plan.get_reasonunit(wk_rope).get_case(thur_rope)


def test_person_plan_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope, kw.fact_context: wk_rope}
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(wk_rope)
    sue_person.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = person_plan_factunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope).factunits.get(wk_rope)


def test_person_get_obj_ReturnsObj_PersonUnit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao}
    sue_person.add_contactunit(exx.yao)

    # WHEN
    x_obj = person_get_obj(kw.personunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person


def test_person_get_obj_ReturnsObj_person_contactunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao}
    sue_person.add_contactunit(exx.yao)

    # WHEN
    x_obj = person_get_obj(kw.person_contactunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_contact(exx.yao)


def test_person_get_obj_ReturnsObj_person_contact_membership_get_obj():
    # ESTABLISH
    bowlers_str = ";bowlers"
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao, "group_title": bowlers_str}
    sue_person.add_contactunit(exx.yao)
    sue_person.get_contact(exx.yao).add_membership(bowlers_str)

    # WHEN
    x_obj = person_get_obj(kw.person_contact_membership, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_contact(exx.yao).get_membership(bowlers_str)


def test_person_get_obj_ReturnsObj_person_planunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope}

    # WHEN
    x_obj = person_get_obj(kw.person_planunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope)


def test_person_get_obj_ReturnsObj_person_plan_awardunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope, kw.awardee_title: exx.bowl}
    sue_person.add_plan(casa_rope)
    sue_person.get_plan_obj(casa_rope).set_awardunit(awardunit_shop(exx.bowl))

    # WHEN
    x_obj = person_get_obj(kw.person_plan_awardunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope).get_awardunit(exx.bowl)


def test_person_get_obj_ReturnsObj_person_plan_reasonunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope, kw.reason_context: wk_rope}
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(wk_rope)
    sue_person.get_plan_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = person_get_obj(kw.person_plan_reasonunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope).get_reasonunit(wk_rope)


def test_person_get_obj_ReturnsObj_person_plan_reason_caseunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.plan_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(wk_rope)
    sue_person.add_plan(thur_rope)
    casa_plan = sue_person.get_plan_obj(casa_rope)
    casa_plan.set_reasonunit(reasonunit_shop(wk_rope))
    casa_plan.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = person_get_obj(kw.person_plan_reason_caseunit, sue_person, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_plan.get_reasonunit(wk_rope).get_case(thur_rope)


def test_person_get_obj_ReturnsObj_person_plan_factunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_plan(casa_rope)
    jkeys = {kw.plan_rope: casa_rope, kw.fact_context: wk_rope}
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(wk_rope)
    sue_person.get_plan_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = person_get_obj(kw.person_plan_factunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_plan_obj(casa_rope).factunits.get(wk_rope)
