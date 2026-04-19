from ch06_plan.plan import planunit_shop
from ch07_person_logic.person_main import personunit_shop
from ch07_person_logic.person_tool import (
    person_plan_reason_caseunit_exists,
    person_plan_reason_caseunit_get_obj,
    person_plan_reason_caseunit_set_obj,
)
from ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_person_plan_reason_caseunit_set_obj_SetAttr_Scenario0_Pass_reason_case():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob, knot=exx.slash)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    wk_rope = bob_person.make_l1_rope(exx.wk)
    wed_rope = bob_person.make_rope(wk_rope, exx.wed)
    bob_person.set_l1_plan(planunit_shop(exx.casa))
    bob_person.set_l1_plan(planunit_shop(exx.wk))
    bob_person.set_plan_obj(planunit_shop(exx.wed), wk_rope)
    wed_jkeys = {
        kw.plan_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: wed_rope,
    }
    assert not person_plan_reason_caseunit_exists(bob_person, wed_jkeys)

    # WHEN
    person_plan_reason_caseunit_set_obj(bob_person, wed_jkeys)

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, wed_jkeys)


def test_person_plan_reason_caseunit_set_obj_SetAttr_Scenario1_Pass_reason_lower_reason_upper():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob, knot=exx.slash)
    mop_rope = bob_person.make_l1_rope(exx.mop)
    clean_rope = bob_person.make_l1_rope(exx.clean)
    dirtyness_rope = bob_person.make_rope(clean_rope, exx.dirtyness)
    bob_person.add_plan(dirtyness_rope)
    bob_person.add_plan(mop_rope)
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_args = {
        kw.plan_rope: mop_rope,
        kw.reason_context: dirtyness_rope,
        kw.reason_state: dirtyness_rope,
        kw.reason_lower: dirtyness_reason_lower,
        kw.reason_upper: dirtyness_reason_upper,
    }
    assert not person_plan_reason_caseunit_exists(bob_person, dirtyness_args)

    # WHEN
    person_plan_reason_caseunit_set_obj(person=bob_person, args=dirtyness_args)

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, dirtyness_args)
    dirtyness_case = person_plan_reason_caseunit_get_obj(bob_person, dirtyness_args)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper


def test_person_plan_reason_caseunit_set_obj_SetAttr_Scenario2_Pass_reason_divisor():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob, knot=exx.slash)
    mop_rope = bob_person.make_l1_rope(exx.mop)
    clean_rope = bob_person.make_l1_rope(exx.clean)
    dirtyness_rope = bob_person.make_rope(clean_rope, exx.dirtyness)
    bob_person.add_plan(dirtyness_rope)
    bob_person.add_plan(mop_rope)
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_reason_divisor = 11
    dirtyness_args = {
        kw.plan_rope: mop_rope,
        kw.reason_context: dirtyness_rope,
        kw.reason_state: dirtyness_rope,
        kw.reason_lower: dirtyness_reason_lower,
        kw.reason_upper: dirtyness_reason_upper,
        kw.reason_divisor: dirtyness_reason_divisor,
    }
    assert not person_plan_reason_caseunit_exists(bob_person, dirtyness_args)

    # WHEN
    person_plan_reason_caseunit_set_obj(bob_person, dirtyness_args)

    # THEN
    assert person_plan_reason_caseunit_exists(bob_person, dirtyness_args)
    dirtyness_case = person_plan_reason_caseunit_get_obj(bob_person, dirtyness_args)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper
    assert dirtyness_case.reason_divisor == dirtyness_reason_divisor
