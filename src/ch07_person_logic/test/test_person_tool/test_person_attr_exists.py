from src.ch02_contact.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.person_tool import (
    person_attr_exists,
    person_contact_membership_exists,
    person_contactunit_exists,
    person_plan_awardunit_exists,
    person_plan_factunit_exists,
    person_plan_healerunit_exists,
    person_plan_laborunit_exists,
    person_plan_reason_caseunit_exists as caseunit_exists,
    person_plan_reasonunit_exists,
    person_planunit_exists,
    personunit_exists,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_personunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not personunit_exists(None)
    assert personunit_exists(personunit_shop("Sue"))


def test_person_contactunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao}

    # WHEN / THEN
    assert not person_contactunit_exists(None, {})
    assert not person_contactunit_exists(sue_person, jkeys)

    # WHEN
    sue_person.add_contactunit(exx.yao)

    # THEN
    assert person_contactunit_exists(sue_person, jkeys)


def test_person_contact_membership_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    bowlers_str = ";bowlers"
    sue_person = personunit_shop("Sue")
    jkeys = {kw.contact_name: exx.yao, kw.group_title: bowlers_str}

    # WHEN / THEN
    assert not person_contact_membership_exists(None, {})
    assert not person_contact_membership_exists(sue_person, jkeys)

    # WHEN
    sue_person.add_contactunit(exx.yao)
    # THEN
    assert not person_contact_membership_exists(sue_person, jkeys)

    # WHEN
    yao_plan = sue_person.get_contact(exx.yao)
    yao_plan.add_membership(";run")
    # THEN
    assert not person_contact_membership_exists(sue_person, jkeys)

    # WHEN
    yao_plan = sue_person.get_contact(exx.yao)
    yao_plan.add_membership(bowlers_str)
    # THEN
    assert person_contact_membership_exists(sue_person, jkeys)


def test_person_planunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    root_rope = sue_person.planroot.get_plan_rope()
    root_jkeys = {kw.plan_rope: root_rope}
    casa_jkeys = {kw.plan_rope: casa_rope}
    clean_jkeys = {kw.plan_rope: clean_rope}
    sweep_jkeys = {kw.plan_rope: sweep_rope}

    # WHEN / THEN
    assert not person_planunit_exists(None, {})
    assert not person_planunit_exists(sue_person, {})
    assert person_planunit_exists(sue_person, root_jkeys)
    assert not person_planunit_exists(sue_person, casa_jkeys)
    assert not person_planunit_exists(sue_person, clean_jkeys)
    assert not person_planunit_exists(sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_plan(casa_rope)
    # THEN
    assert not person_planunit_exists(sue_person, {})
    assert person_planunit_exists(sue_person, root_jkeys)
    assert person_planunit_exists(sue_person, casa_jkeys)
    assert not person_planunit_exists(sue_person, clean_jkeys)
    assert not person_planunit_exists(sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_plan(clean_rope)
    # THEN
    assert not person_planunit_exists(sue_person, {})
    assert person_planunit_exists(sue_person, root_jkeys)
    assert person_planunit_exists(sue_person, casa_jkeys)
    assert person_planunit_exists(sue_person, clean_jkeys)
    assert not person_planunit_exists(sue_person, sweep_jkeys)


def test_person_plan_awardunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    root_rope = sue_person.planroot.get_plan_rope()
    root_jkeys = {kw.plan_rope: root_rope, kw.awardee_title: exx.bowl}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.awardee_title: exx.bowl}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.awardee_title: exx.bowl}

    # WHEN / THEN
    assert not person_plan_awardunit_exists(None, {})
    assert not person_plan_awardunit_exists(sue_person, {})
    assert not person_plan_awardunit_exists(sue_person, root_jkeys)
    assert not person_plan_awardunit_exists(sue_person, casa_jkeys)
    assert not person_plan_awardunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.planroot.set_awardunit(awardunit_shop(exx.bowl))

    # THEN
    assert not person_plan_awardunit_exists(sue_person, {})
    assert person_plan_awardunit_exists(sue_person, root_jkeys)
    assert not person_plan_awardunit_exists(sue_person, casa_jkeys)
    assert not person_plan_awardunit_exists(sue_person, clean_jkeys)


def test_person_plan_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    root_jkeys = {kw.plan_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not person_plan_reasonunit_exists(None, {})
    assert not person_plan_reasonunit_exists(sue_person, {})
    assert not person_plan_reasonunit_exists(sue_person, root_jkeys)
    assert not person_plan_reasonunit_exists(sue_person, casa_jkeys)
    assert not person_plan_reasonunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(wk_rope)
    sue_person.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not person_plan_reasonunit_exists(sue_person, {})
    assert person_plan_reasonunit_exists(sue_person, root_jkeys)
    assert not person_plan_reasonunit_exists(sue_person, casa_jkeys)
    assert not person_plan_reasonunit_exists(sue_person, clean_jkeys)


def test_person_plan_reason_caseunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    root_jkeys = {
        kw.plan_rope: root_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    casa_jkeys = {
        kw.plan_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    clean_jkeys = {
        kw.plan_rope: clean_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }

    # WHEN / THEN
    assert not caseunit_exists(None, {})
    assert not caseunit_exists(sue_person, {})
    assert not caseunit_exists(sue_person, root_jkeys)
    assert not caseunit_exists(sue_person, casa_jkeys)
    assert not caseunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(wk_rope)
    sue_person.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not caseunit_exists(sue_person, {})
    assert not caseunit_exists(sue_person, root_jkeys)
    assert not caseunit_exists(sue_person, casa_jkeys)
    assert not caseunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(thur_rope)
    sue_person.planroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not caseunit_exists(sue_person, {})
    assert caseunit_exists(sue_person, root_jkeys)
    assert not caseunit_exists(sue_person, casa_jkeys)
    assert not caseunit_exists(sue_person, clean_jkeys)


def test_person_plan_laborunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    root_jkeys = {kw.plan_rope: root_rope, kw.labor_title: exx.bowl}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.labor_title: exx.bowl}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.labor_title: exx.bowl}

    # WHEN / THEN
    assert not person_plan_laborunit_exists(None, {})
    assert not person_plan_laborunit_exists(sue_person, {})
    assert not person_plan_laborunit_exists(sue_person, root_jkeys)
    assert not person_plan_laborunit_exists(sue_person, casa_jkeys)
    assert not person_plan_laborunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.planroot.workforceunit.add_labor(exx.bowl)

    # THEN
    assert not person_plan_laborunit_exists(sue_person, {})
    assert person_plan_laborunit_exists(sue_person, root_jkeys)
    assert not person_plan_laborunit_exists(sue_person, casa_jkeys)
    assert not person_plan_laborunit_exists(sue_person, clean_jkeys)


def test_person_plan_healerunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    root_jkeys = {kw.plan_rope: root_rope, kw.healer_name: exx.bowl}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.healer_name: exx.bowl}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.healer_name: exx.bowl}

    # WHEN / THEN
    assert not person_plan_healerunit_exists(None, {})
    assert not person_plan_healerunit_exists(sue_person, {})
    assert not person_plan_healerunit_exists(sue_person, root_jkeys)
    assert not person_plan_healerunit_exists(sue_person, casa_jkeys)
    assert not person_plan_healerunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.planroot.healerunit.set_healer_name(exx.bowl)

    # THEN
    assert not person_plan_healerunit_exists(sue_person, {})
    assert person_plan_healerunit_exists(sue_person, root_jkeys)
    assert not person_plan_healerunit_exists(sue_person, casa_jkeys)
    assert not person_plan_healerunit_exists(sue_person, clean_jkeys)


def test_person_plan_factunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    root_jkeys = {kw.plan_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not person_plan_factunit_exists(None, {})
    assert not person_plan_factunit_exists(sue_person, {})
    assert not person_plan_factunit_exists(sue_person, root_jkeys)
    assert not person_plan_factunit_exists(sue_person, casa_jkeys)
    assert not person_plan_factunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(wk_rope)
    sue_person.planroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not person_plan_factunit_exists(sue_person, {})
    assert person_plan_factunit_exists(sue_person, root_jkeys)
    assert not person_plan_factunit_exists(sue_person, casa_jkeys)
    assert not person_plan_factunit_exists(sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_personunit():
    # ESTABLISH / WHEN / THEN
    assert not person_attr_exists(kw.personunit, None, {})
    assert person_attr_exists(kw.personunit, personunit_shop("Sue"), {})


def test_person_attr_exists_ReturnsObj_person_contactunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    x_jkeys = {kw.contact_name: exx.yao}

    # WHEN / THEN
    assert not person_attr_exists(kw.person_contactunit, None, {})
    assert not person_attr_exists(kw.person_contactunit, sue_person, x_jkeys)

    # WHEN
    sue_person.add_contactunit(exx.yao)

    # THEN
    assert person_attr_exists(kw.person_contactunit, sue_person, x_jkeys)


def test_person_attr_exists_ReturnsObj_person_contact_membership():
    # ESTABLISH
    bowlers_str = ";bowlers"
    sue_person = personunit_shop("Sue")
    x_jkeys = {kw.contact_name: exx.yao, kw.group_title: bowlers_str}
    x_dimen = kw.person_contact_membership

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, x_jkeys)

    # WHEN
    sue_person.add_contactunit(exx.yao)
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, x_jkeys)

    # WHEN
    yao_plan = sue_person.get_contact(exx.yao)
    yao_plan.add_membership(";run")
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, x_jkeys)

    # WHEN
    yao_plan = sue_person.get_contact(exx.yao)
    yao_plan.add_membership(bowlers_str)
    # THEN
    assert person_attr_exists(x_dimen, sue_person, x_jkeys)


def test_person_attr_exists_ReturnsObj_person_planunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    x_parent_rope = sue_person.planroot.get_plan_rope()
    root_jkeys = {kw.plan_rope: x_parent_rope}
    casa_jkeys = {kw.plan_rope: casa_rope}
    clean_jkeys = {kw.plan_rope: clean_rope}
    sweep_jkeys = {kw.plan_rope: sweep_rope}
    x_dimen = kw.person_planunit

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_plan(casa_rope)
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_plan(clean_rope)
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert person_attr_exists(x_dimen, sue_person, clean_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, sweep_jkeys)


def test_person_attr_exists_ReturnsObj_person_plan_awardunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    x_dimen = kw.person_plan_awardunit
    root_jkeys = {kw.plan_rope: root_rope, kw.awardee_title: exx.bowl}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.awardee_title: exx.bowl}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.awardee_title: exx.bowl}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.planroot.set_awardunit(awardunit_shop(exx.bowl))

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_plan_reasonunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    x_dimen = kw.person_plan_reasonunit
    root_jkeys = {kw.plan_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(wk_rope)
    sue_person.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_plan_reason_caseunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    x_dimen = kw.person_plan_reason_caseunit
    root_jkeys = {
        kw.plan_rope: root_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    casa_jkeys = {
        kw.plan_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    clean_jkeys = {
        kw.plan_rope: clean_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(wk_rope)
    sue_person.planroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(thur_rope)
    sue_person.planroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_plan_laborunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    x_dimen = kw.person_plan_laborunit
    root_jkeys = {kw.plan_rope: root_rope, kw.labor_title: exx.bowl}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.labor_title: exx.bowl}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.labor_title: exx.bowl}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.planroot.workforceunit.add_labor(exx.bowl)

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_plan_healerunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    x_dimen = kw.person_plan_healerunit
    root_jkeys = {kw.plan_rope: root_rope, kw.healer_name: exx.bowl}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.healer_name: exx.bowl}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.healer_name: exx.bowl}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.planroot.healerunit.set_healer_name(exx.bowl)

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_plan_factunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.planroot.get_plan_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    x_dimen = kw.person_plan_factunit
    root_jkeys = {kw.plan_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.plan_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.plan_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_plan(wk_rope)
    sue_person.planroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)
