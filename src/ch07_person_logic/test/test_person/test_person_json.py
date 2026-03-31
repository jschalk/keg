from pytest import raises as pytest_raises
from src.ch03_workforce.workforce import laborunit_shop, workforceunit_shop
from src.ch04_rope.rope import default_knot_if_None
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import (
    get_dict_of_person_from_dict,
    get_personunit_from_dict,
    personunit_shop,
)
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_laundry_example1,
    get_personunit_reason_context_ziet_example,
    get_personunit_x1_3levels_1reason_1facts,
    personunit_v001,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PersonUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_person = get_personunit_laundry_example1()
    yao_fund_pool = 23000
    yao_person.fund_pool = yao_fund_pool
    yao_fund_grain = 23
    yao_person.fund_grain = yao_fund_grain
    x_last_lesson_id = 77
    yao_person.set_last_lesson_id(x_last_lesson_id)

    # WHEN
    person_dict = yao_person.to_dict()

    # THEN
    assert person_dict is not None
    assert str(type(person_dict)) == "<class 'dict'>"
    assert person_dict[kw.person_name] == yao_person.person_name
    assert person_dict[kw.fund_pool] == yao_fund_pool
    assert person_dict[kw.fund_grain] == yao_fund_grain
    assert person_dict[kw.max_tree_traverse] == yao_person.max_tree_traverse
    assert person_dict[kw.knot] == yao_person.knot
    assert person_dict[kw.credor_respect] == yao_person.credor_respect
    assert person_dict[kw.debtor_respect] == yao_person.debtor_respect
    assert person_dict[kw.last_lesson_id] == yao_person.last_lesson_id
    assert len(person_dict[kw.partners]) == len(yao_person.partners)
    assert len(person_dict[kw.partners]) != 12

    x_planroot = yao_person.planroot
    planroot_dict = person_dict[kw.planroot]
    assert planroot_dict[kw.plan_label] == x_planroot.plan_label
    assert planroot_dict[kw.star] == x_planroot.star
    assert len(planroot_dict[kw.kids]) == len(x_planroot.kids)


def test_PersonUnit_to_dict_ReturnsObj_Scenario1_planroot_workforceunit():
    # ESTABLISH
    run_str = "runners"
    sue_person = personunit_shop("Sue")
    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(labor_title=run_str)
    root_rope = sue_person.planroot.get_plan_rope()
    sue_person.edit_plan_attr(root_rope, workforceunit=x_workforceunit)
    root_plan = sue_person.get_plan_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_plan.gogo_want = x_gogo_want
    root_plan.stop_want = x_stop_want

    # WHEN
    person_dict = sue_person.to_dict()
    planroot_dict = person_dict.get(kw.planroot)

    # THEN
    assert planroot_dict[kw.workforceunit] == x_workforceunit.to_dict()
    run_laborunit = laborunit_shop(run_str)
    assert planroot_dict[kw.workforceunit] == {
        kw.labors: {run_str: run_laborunit.to_dict()}
    }
    assert planroot_dict.get(kw.gogo_want) == x_gogo_want
    assert planroot_dict.get(kw.stop_want) == x_stop_want


def test_PersonUnit_to_dict_ReturnsObj_Scenario2_With_planroot_healerunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_partnerunit(exx.yao)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)
    run_healerunit = healerunit_shop()
    run_healerunit.set_healer_name(x_healer_name=exx.run)
    root_rope = sue_person.planroot.get_plan_rope()
    sue_person.edit_plan_attr(root_rope, healerunit=run_healerunit)

    # WHEN
    person_dict = sue_person.to_dict()
    planroot_dict = person_dict.get(kw.planroot)

    # THEN
    assert planroot_dict[kw.healerunit] == run_healerunit.to_dict()


def test_PersonUnit_to_dict_ReturnsObj_Scenario3_plankid_WorkforceUnit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_partnerunit(exx.yao)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)

    morn_str = "morning"
    morn_rope = sue_person.make_l1_rope(morn_str)
    sue_person.set_l1_plan(planunit_shop(morn_str))
    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(labor_title=exx.run)
    sue_person.edit_plan_attr(morn_rope, workforceunit=x_workforceunit)

    # WHEN
    person_dict = sue_person.to_dict()
    planroot_dict = person_dict.get(kw.planroot)

    # THEN
    workforce_dict_x = planroot_dict[kw.kids][morn_str][kw.workforceunit]
    assert workforce_dict_x == x_workforceunit.to_dict()
    run_laborunit = laborunit_shop(exx.run)
    assert workforce_dict_x == {kw.labors: {exx.run: run_laborunit.to_dict()}}


def test_PersonUnit_to_dict_ReturnsObj_Scenario4_planunit_WithLevels():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_person = get_personunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_person.fund_pool = x_fund_pool
    x_fund_grain = 66
    zia_person.fund_grain = x_fund_grain
    x_respect_grain = 7
    zia_person.respect_grain = x_respect_grain
    x_mana_grain = 0.3
    zia_person.mana_grain = x_mana_grain
    override_str = "override"
    zia_person.add_partnerunit(exx.yao)
    yao_partnerunit = zia_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)
    run_healerunit = healerunit_shop({exx.run})
    root_rope = zia_person.planroot.get_plan_rope()
    zia_person.edit_plan_attr(root_rope, healerunit=run_healerunit)
    zia_person.edit_plan_attr(root_rope, problem_bool=True)

    # WHEN
    person_dict = zia_person.to_dict()

    # THEN
    assert person_dict is not None
    assert person_dict[kw.person_name] == zia_person.person_name
    assert person_dict[kw.fund_pool] == zia_person.fund_pool
    assert person_dict[kw.fund_grain] == zia_person.fund_grain
    assert person_dict[kw.respect_grain] == zia_person.respect_grain
    assert person_dict[kw.mana_grain] == zia_person.mana_grain
    assert person_dict[kw.credor_respect] == zia_person.credor_respect
    assert person_dict[kw.debtor_respect] == zia_person.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     person_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     person_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        person_dict[kw.last_lesson_id]

    x_planroot = zia_person.planroot
    planroot_dict = person_dict.get(kw.planroot)

    assert len(planroot_dict[kw.kids]) == len(x_planroot.kids)

    shave_str = "shave"
    shave_dict = planroot_dict[kw.kids][shave_str]
    shave_factunits = shave_dict[kw.factunits]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_planroot.kids[shave_str].factunits)
    planroot_healerunit = planroot_dict[kw.healerunit]
    print(f"{planroot_healerunit=}")
    assert len(planroot_healerunit) == 1
    assert x_planroot.healerunit.any_healer_name_exists()
    assert x_planroot.problem_bool


def test_PersonUnit_to_dict_ReturnsJSON_Scenario5_BigExample():
    # ESTABLISH
    yao_person = personunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_person.make_l1_rope(hr_number_str)
    yao_person.add_fact(
        fact_context=hr_number_rope,
        fact_state=hr_number_rope,
        fact_lower=0,
        fact_upper=23,
    )
    jour_min_str = "jour_minute"
    jour_min_rope = yao_person.make_l1_rope(jour_min_str)
    yao_person.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=59,
    )
    x_factunit = factunit_shop(jour_min_rope, jour_min_rope, 5, 59)
    yao_person.edit_plan_attr(x_factunit.fact_context, factunit=x_factunit)
    yao_person.set_max_tree_traverse(2)

    # WHEN
    person_dict = yao_person.to_dict()

    # THEN
    assert person_dict[kw.person_name] == yao_person.person_name
    assert person_dict[kw.max_tree_traverse] == 2
    assert person_dict[kw.max_tree_traverse] == yao_person.max_tree_traverse
    assert person_dict[kw.knot] == yao_person.knot

    x_planroot = yao_person.planroot
    planroot_dict = person_dict.get(kw.planroot)
    assert len(planroot_dict[kw.kids]) == len(x_planroot.kids)

    kids_dict = planroot_dict[kw.kids]
    jour_min_dict = kids_dict[jour_min_str]
    jour_min_factunits_dict = jour_min_dict[kw.factunits]
    jour_min_plan_x = yao_person.get_plan_obj(jour_min_rope)
    print(f"{jour_min_factunits_dict=}")
    assert len(jour_min_factunits_dict) == 1
    assert len(jour_min_factunits_dict) == len(jour_min_plan_x.factunits)

    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_person.make_l1_rope(cont_str)
    ulti_rope = yao_person.make_l1_rope(ulti_str)
    cont_plan = yao_person.get_plan_obj(cont_rope)
    ulti_plan = yao_person.get_plan_obj(ulti_rope)
    cont_reasonunits_dict = planroot_dict[kw.kids][cont_str][kw.reasonunits]
    ulti_reasonunits_dict = planroot_dict[kw.kids][ulti_str][kw.reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_plan.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_plan.reasonunits)

    anna_str = "Anna"
    anna_partnerunit = yao_person.get_partner(anna_str)
    assert anna_partnerunit.get_membership(";Family").group_cred_lumen == 6.2
    assert yao_person.partners is not None
    assert len(yao_person.partners) == 22


def test_get_personunit_from_dict_ReturnsObj_Scenario0_PlanRoot():
    # ESTABLISH
    zia_person = get_personunit_x1_3levels_1reason_1facts()
    zia_person.set_max_tree_traverse(23)
    root_plan = zia_person.planroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_plan.gogo_want = zia_gogo_want
    root_plan.stop_want = zia_stop_want

    # WHEN
    json_person = get_personunit_from_dict(zia_person.to_dict())

    # THEN
    json_planroot = json_person.get_plan_obj(zia_person.planroot.get_plan_rope())
    assert json_planroot.gogo_want == zia_gogo_want
    assert json_planroot.stop_want == zia_stop_want


def test_get_personunit_from_dict_ReturnsObj_Scenario1_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_person = personunit_shop("Bob", knot=slash_knot)
    assert before_bob_person.knot != default_knot_if_None()

    # WHEN
    after_bob_person = get_personunit_from_dict(before_bob_person.to_dict())

    # THEN
    assert after_bob_person.knot != default_knot_if_None()
    assert after_bob_person.knot == slash_knot
    assert after_bob_person.knot == before_bob_person.knot


def test_get_personunit_from_dict_ReturnsObj_Scenario2_knot_PartnerExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_person = personunit_shop("Bob", knot=slash_knot)
    bob_comma_str = ",Bob"
    before_bob_person.add_partnerunit(bob_comma_str)
    assert before_bob_person.partner_exists(bob_comma_str)

    # WHEN
    after_bob_person = get_personunit_from_dict(before_bob_person.to_dict())

    # THEN
    after_bob_partnerunit = after_bob_person.get_partner(bob_comma_str)
    assert after_bob_partnerunit.groupmark == slash_knot


def test_get_personunit_from_dict_ReturnsObj_Scenario3_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_person = personunit_shop("Bob", knot=slash_knot)
    swim_str = f"{slash_knot}Swimmers"
    before_bob_person.add_partnerunit(exx.yao)
    yao_partnerunit = before_bob_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(swim_str)

    # WHEN
    after_bob_person = get_personunit_from_dict(before_bob_person.to_dict())

    # THEN
    after_yao_partnerunit = after_bob_person.get_partner(exx.yao)
    assert after_yao_partnerunit.groupmark == slash_knot


def test_get_personunit_from_dict_ReturnsObj_Scenario4_planroot_knot_IsApplied():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue", knot=exx.slash)
    root_rope = sue_person.planroot.get_plan_rope()
    hr_number_str = "hr_number"
    hr_number_rope = sue_person.make_l1_rope(hr_number_str)
    sue_person.add_plan(hr_number_rope)
    assert sue_person.knot == exx.slash
    assert sue_person.get_plan_obj(root_rope).knot == exx.slash
    assert sue_person.get_plan_obj(hr_number_rope).knot == exx.slash

    # WHEN
    after_bob_person = get_personunit_from_dict(sue_person.to_dict())

    # THEN
    assert after_bob_person.knot == exx.slash
    assert after_bob_person.get_plan_obj(root_rope).knot == exx.slash
    assert after_bob_person.get_plan_obj(hr_number_rope).knot == exx.slash


def test_get_personunit_from_dict_ReturnsObj_Scenario5_ExportsPersonUnit_star():
    # ESTABLISH
    x1_person = personunit_v001()
    assert x1_person.planroot.star == 1

    # WHEN
    x2_person = get_personunit_from_dict(x1_person.to_dict())

    # THEN
    assert x1_person.planroot.star == 1
    assert x1_person.planroot.star == x2_person.planroot.star
    assert x1_person.planroot.kids == x2_person.planroot.kids


def test_get_personunit_from_dict_ReturnsObj_Scenario6_CheckNumericalPlanUnitAttrs():
    # ESTABLISH
    before_person = personunit_v001()
    casa_rope = before_person.make_l1_rope(exx.casa)
    before_person.add_plan(casa_rope)
    before_casa_plan = before_person.get_plan_obj(casa_rope)
    x_star = 11
    x_begin = 12
    x_close = 13
    x_numor = 14
    x_denom = 15
    x_morph = 16
    x_addin = 19
    x_gogo_want = 17
    x_stop_want = 18
    before_casa_plan.star = x_star
    before_casa_plan.begin = x_begin
    before_casa_plan.close = x_close
    before_casa_plan.numor = x_numor
    before_casa_plan.denom = x_denom
    before_casa_plan.morph = x_morph
    before_casa_plan.addin = x_addin
    before_casa_plan.gogo_want = x_gogo_want
    before_casa_plan.stop_want = x_stop_want
    assert before_casa_plan.star == x_star
    assert before_casa_plan.begin == x_begin
    assert before_casa_plan.close == x_close
    assert before_casa_plan.numor == x_numor
    assert before_casa_plan.denom == x_denom
    assert before_casa_plan.morph == x_morph
    assert before_casa_plan.addin == x_addin
    assert before_casa_plan.gogo_want == x_gogo_want
    assert before_casa_plan.stop_want == x_stop_want

    # WHEN
    after_person = get_personunit_from_dict(before_person.to_dict())

    # THEN
    after_casa_plan = after_person.get_plan_obj(casa_rope)
    assert after_casa_plan.star == x_star
    assert after_casa_plan.begin == x_begin
    assert after_casa_plan.close == x_close
    assert after_casa_plan.numor == x_numor
    assert after_casa_plan.denom == x_denom
    assert after_casa_plan.morph == x_morph
    assert after_casa_plan.addin == x_addin
    assert after_casa_plan.gogo_want == x_gogo_want
    assert after_casa_plan.stop_want == x_stop_want


def test_get_dict_of_person_from_dict_ReturnsDictOfPersonUnits():
    # ESTABLISH
    x1_person = personunit_v001()
    x2_person = get_personunit_x1_3levels_1reason_1facts()
    x3_person = get_personunit_reason_context_ziet_example()
    print(f"{x1_person.person_name}")
    print(f"{x2_person.person_name}")
    print(f"{x3_person.person_name}")

    cn_dict_of_dicts = {
        x1_person.person_name: x1_person.to_dict(),
        x2_person.person_name: x2_person.to_dict(),
        x3_person.person_name: x3_person.to_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_person_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_person.person_name) is not None
    assert ccn_dict_of_obj.get(x2_person.person_name) is not None
    assert ccn_dict_of_obj.get(x3_person.person_name) is not None

    ccn2_person = ccn_dict_of_obj.get(x2_person.person_name)
    assert ccn2_person.planroot.plan_label == x2_person.planroot.plan_label
    assert ccn2_person.planroot.parent_rope == x2_person.planroot.parent_rope
    assert ccn2_person.planroot.fund_grain == x2_person.planroot.fund_grain
    shave_rope = ccn2_person.make_l1_rope("shave")
    wk_rope = ccn2_person.make_l1_rope("sem_jours")
    # assert ccn2_person.get_plan_obj(shave_rope) == x2_person.get_plan_obj(shave_rope)
    # assert ccn2_person.get_plan_obj(wk_rope) == x2_person.get_plan_obj(wk_rope)
    # assert ccn2_person.planroot == x2_person.planroot
    assert ccn2_person.to_dict() == x2_person.to_dict()

    ccn_person3 = ccn_dict_of_obj.get(x3_person.person_name)
    assert ccn_person3.to_dict() == x3_person.to_dict()

    cc1_plan_root = ccn_dict_of_obj.get(x1_person.person_name).planroot
    ccn_person1 = ccn_dict_of_obj.get(x1_person.person_name)
    assert ccn_person1._plan_dict == x1_person._plan_dict
    philipa_str = "Philipa"
    ccn_philipa_partnerunit = ccn_person1.get_partner(philipa_str)
    x1_philipa_partnerunit = x1_person.get_partner(philipa_str)
    assert ccn_philipa_partnerunit.memberships == x1_philipa_partnerunit.memberships
    assert ccn_person1 == x1_person
    assert ccn_dict_of_obj.get(x1_person.person_name) == x1_person
