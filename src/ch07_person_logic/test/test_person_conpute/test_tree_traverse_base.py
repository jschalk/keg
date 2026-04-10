from pytest import raises as pytest_raises
from src.ch02_contact.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factheir_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_with_4_levels,
    get_personunit_with_4_levels_and_2reasons,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_clear_plan_dict_and_person_obj_settle_attrs_SetsAttrs_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_plan_dict = {1: 2, 2: 4}
    sue_person.rational = x_rational
    sue_person.tree_traverse_count = x_tree_traverse_count
    sue_person._plan_dict = x_plan_dict
    sue_person.offtrack_kids_star_set = "example"
    sue_person.reason_contexts = {"example2"}
    sue_person.range_inheritors = {"example2": 1}
    assert sue_person.rational == x_rational
    assert sue_person.tree_traverse_count == x_tree_traverse_count
    assert sue_person._plan_dict == x_plan_dict
    assert sue_person.offtrack_kids_star_set != set()
    assert sue_person.reason_contexts != set()
    assert sue_person.range_inheritors != {}

    # WHEN
    sue_person._clear_plan_dict_and_person_obj_settle_attrs()

    # THEN
    assert sue_person.rational != x_rational
    assert not sue_person.rational
    assert sue_person.tree_traverse_count != x_tree_traverse_count
    assert sue_person.tree_traverse_count == 0
    assert sue_person._plan_dict != x_plan_dict
    assert sue_person._plan_dict == {
        sue_person.planroot.get_plan_rope(): sue_person.planroot
    }
    assert sue_person.offtrack_kids_star_set == set()
    assert not sue_person.reason_contexts
    assert not sue_person.range_inheritors


def test_PersonUnit_clear_plan_dict_and_person_obj_settle_attrs_SetsAttrs_Scenario1():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    x_keep_justifed = False
    x_sum_healerunit_plans_fund_total = 140
    sue_person.keeps_justified = x_keep_justifed
    sue_person.keeps_buildable = "bowlers"
    sue_person.sum_healerunit_plans_fund_total = x_sum_healerunit_plans_fund_total
    sue_person._keep_dict = {"run": "run"}
    sue_person._healers_dict = {"run": "run"}
    assert sue_person.keeps_justified == x_keep_justifed
    assert sue_person.keeps_buildable
    assert (
        sue_person.sum_healerunit_plans_fund_total == x_sum_healerunit_plans_fund_total
    )
    assert sue_person._keep_dict != {}
    assert sue_person._healers_dict != {}

    # WHEN
    sue_person._clear_plan_dict_and_person_obj_settle_attrs()

    # THEN
    assert sue_person.keeps_justified != x_keep_justifed
    assert sue_person.keeps_justified
    assert sue_person.keeps_buildable is False
    assert sue_person.sum_healerunit_plans_fund_total == 0
    assert not sue_person._keep_dict
    assert not sue_person._healers_dict


def test_PersonUnit_conpute_ClearsDescendantAttributes():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    casa_plan = sue_person.get_plan_obj(casa_rope)
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = sue_person.make_rope(wk_rope, mon_str)
    mon_plan = sue_person.get_plan_obj(mon_rope)
    assert sue_person.planroot.descendant_pledge_count is None
    assert sue_person.planroot.all_contact_cred is None
    assert sue_person.planroot.all_contact_debt is None
    assert casa_plan.descendant_pledge_count is None
    assert casa_plan.all_contact_cred is None
    assert casa_plan.all_contact_debt is None
    assert mon_plan.descendant_pledge_count is None
    assert mon_plan.all_contact_cred is None
    assert mon_plan.all_contact_debt is None

    sue_person.planroot.descendant_pledge_count = -2
    sue_person.planroot.all_contact_cred = -2
    sue_person.planroot.all_contact_debt = -2
    casa_plan.descendant_pledge_count = -2
    casa_plan.all_contact_cred = -2
    casa_plan.all_contact_debt = -2
    mon_plan.descendant_pledge_count = -2
    mon_plan.all_contact_cred = -2
    mon_plan.all_contact_debt = -2

    assert sue_person.planroot.descendant_pledge_count == -2
    assert sue_person.planroot.all_contact_cred == -2
    assert sue_person.planroot.all_contact_debt == -2
    assert casa_plan.descendant_pledge_count == -2
    assert casa_plan.all_contact_cred == -2
    assert casa_plan.all_contact_debt == -2
    assert mon_plan.descendant_pledge_count == -2
    assert mon_plan.all_contact_cred == -2
    assert mon_plan.all_contact_debt == -2

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.planroot.descendant_pledge_count == 2
    assert casa_plan.descendant_pledge_count == 0
    assert mon_plan.descendant_pledge_count == 0

    assert mon_plan.all_contact_cred is True
    assert mon_plan.all_contact_debt is True
    assert casa_plan.all_contact_cred is True
    assert casa_plan.all_contact_debt is True
    assert sue_person.planroot.all_contact_cred is True
    assert sue_person.planroot.all_contact_debt is True


def test_PersonUnit_conpute_RootOnlySetsDescendantAttributes():
    # ESTABLISH
    yao_person = personunit_shop(person_name="Yao")
    assert yao_person.planroot.descendant_pledge_count is None
    assert yao_person.planroot.all_contact_cred is None
    assert yao_person.planroot.all_contact_debt is None

    # WHEN
    yao_person.conpute()

    # THEN
    assert yao_person.planroot.descendant_pledge_count == 0
    assert yao_person.planroot.all_contact_cred is True
    assert yao_person.planroot.all_contact_debt is True


def test_PersonUnit_conpute_NLevelSetsDescendantAttributes_1():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope(exx.casa)
    casa_plan = sue_person.get_plan_obj(casa_rope)
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    wk_plan = sue_person.get_plan_obj(wk_rope)
    mon_str = "Mon"
    mon_rope = sue_person.make_rope(wk_rope, mon_str)
    mon_plan = sue_person.get_plan_obj(mon_rope)

    email_str = "email"
    email_plan = planunit_shop(email_str, pledge=True)
    sue_person.set_plan_obj(email_plan, parent_rope=casa_rope)

    root_rope = sue_person.planroot.get_plan_rope()
    x_planroot = sue_person.get_plan_obj(root_rope)
    assert x_planroot.descendant_pledge_count is None
    assert x_planroot.all_contact_cred is None
    assert x_planroot.all_contact_debt is None
    assert casa_plan.descendant_pledge_count is None
    assert casa_plan.all_contact_cred is None
    assert casa_plan.all_contact_debt is None
    assert mon_plan.descendant_pledge_count is None
    assert mon_plan.all_contact_cred is None
    assert mon_plan.all_contact_debt is None

    # WHEN
    sue_person.conpute()

    # THEN
    assert x_planroot.descendant_pledge_count == 3
    assert casa_plan.descendant_pledge_count == 1
    assert casa_plan.kids[email_str].descendant_pledge_count == 0
    assert mon_plan.descendant_pledge_count == 0
    assert x_planroot.all_contact_cred is True
    assert x_planroot.all_contact_debt is True
    assert casa_plan.all_contact_cred is True
    assert casa_plan.all_contact_debt is True
    assert mon_plan.all_contact_cred is True
    assert mon_plan.all_contact_debt is True


def test_PersonUnit_conpute_NLevelSetsDescendantAttributes_2():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    email_str = "email"
    wk_str = "sem_jours"
    mon_str = "Mon"
    tue_str = "Tue"
    vacuum_str = "vacuum"

    casa_rope = sue_person.make_l1_rope(exx.casa)
    email_plan = planunit_shop(email_str, pledge=True)
    sue_person.set_plan_obj(email_plan, parent_rope=casa_rope)
    vacuum_plan = planunit_shop(vacuum_str, pledge=True)
    sue_person.set_plan_obj(vacuum_plan, parent_rope=casa_rope)

    sue_person.add_contactunit(contact_name=exx.sue)
    x_awardunit = awardunit_shop(awardee_title=exx.sue)

    sue_person.planroot.kids[exx.casa].kids[email_str].set_awardunit(
        awardunit=x_awardunit
    )
    # print(sue_person.kids[exx.casa].kids[email_str])
    # print(sue_person.kids[exx.casa].kids[email_str].awardunit)

    # WHEN
    sue_person.conpute()
    # print(sue_person.kids[exx.casa].kids[email_str])
    # print(sue_person.kids[exx.casa].kids[email_str].awardunit)

    # THEN
    assert sue_person.planroot.all_contact_cred is False
    assert sue_person.planroot.all_contact_debt is False
    casa_plan = sue_person.planroot.kids[exx.casa]
    assert casa_plan.all_contact_cred is False
    assert casa_plan.all_contact_debt is False
    assert casa_plan.kids[email_str].all_contact_cred is False
    assert casa_plan.kids[email_str].all_contact_debt is False
    assert casa_plan.kids[vacuum_str].all_contact_cred is True
    assert casa_plan.kids[vacuum_str].all_contact_debt is True
    wk_plan = sue_person.planroot.kids[wk_str]
    assert wk_plan.all_contact_cred is True
    assert wk_plan.all_contact_debt is True
    assert wk_plan.kids[mon_str].all_contact_cred is True
    assert wk_plan.kids[mon_str].all_contact_debt is True
    assert wk_plan.kids[tue_str].all_contact_cred is True
    assert wk_plan.kids[tue_str].all_contact_debt is True


def test_PersonUnit_conpute_SetsPlanUnitAttr_awardunits():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.zia)
    sue_person.add_contactunit(exx.xio)

    assert len(sue_person.contacts) == 3
    assert len(sue_person.get_contactunit_group_titles_dict()) == 3
    sue_person.set_l1_plan(planunit_shop(exx.bowl))
    awardunit_yao = awardunit_shop(exx.yao, give_force=10)
    awardunit_zia = awardunit_shop(exx.zia, give_force=10)
    awardunit_Xio = awardunit_shop(exx.xio, give_force=10)
    bowl_rope = sue_person.make_l1_rope(exx.bowl)
    sue_person.edit_plan_attr(bowl_rope, awardunit=awardunit_yao)
    sue_person.edit_plan_attr(bowl_rope, awardunit=awardunit_zia)
    sue_person.edit_plan_attr(bowl_rope, awardunit=awardunit_Xio)

    street_str = "streets"
    sue_person.set_plan_obj(planunit_shop(street_str), parent_rope=bowl_rope)
    assert sue_person.planroot.awardunits in (None, {})
    assert len(sue_person.planroot.kids[exx.bowl].awardunits) == 3

    # WHEN
    sue_person.conpute()

    # THEN
    print(f"{sue_person._plan_dict.keys()=} ")
    bowl_plan = sue_person._plan_dict.get(bowl_rope)
    street_plan = sue_person._plan_dict.get(sue_person.make_rope(bowl_rope, street_str))

    assert len(bowl_plan.awardunits) == 3
    assert len(bowl_plan.awardheirs) == 3
    assert street_plan.awardunits in (None, {})
    assert len(street_plan.awardheirs) == 3

    print(f"{len(sue_person._plan_dict)}")
    print(f"{bowl_plan.awardunits}")
    print(f"{bowl_plan.awardheirs}")
    print(f"{bowl_plan.awardheirs}")
    assert len(sue_person.planroot.kids["bowl"].awardheirs) == 3


def test_PersonUnit_conpute_TreeTraverseSetsClearsAwardLineestors():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sue_person.conpute()
    # plan tree has no awardunits
    assert sue_person.planroot.awardlines == {}
    sue_person.planroot.awardlines = {1: "testtest"}
    assert sue_person.planroot.awardlines != {}

    # WHEN
    sue_person.conpute()

    # THEN
    assert not sue_person.planroot.awardlines

    # WHEN
    # test for level 1 and level n
    casa_plan = sue_person.planroot.kids[exx.casa]
    casa_plan.awardlines = {1: "testtest"}
    assert casa_plan.awardlines != {}
    sue_person.conpute()

    # THEN
    assert not sue_person.planroot.kids[exx.casa].awardlines


def test_PersonUnit_conpute_DoesNotKeepNonRequired_awardheirs():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao)
    yao_person.add_contactunit(exx.zia)
    yao_person.add_contactunit(exx.xio)

    bowl_rope = yao_person.make_l1_rope(exx.bowl)

    yao_person.set_l1_plan(planunit_shop(exx.bowl))
    awardunit_yao = awardunit_shop(exx.yao, give_force=10)
    awardunit_zia = awardunit_shop(exx.zia, give_force=10)
    awardunit_Xio = awardunit_shop(exx.xio, give_force=10)

    bowl_plan = yao_person.get_plan_obj(bowl_rope)
    yao_person.edit_plan_attr(bowl_rope, awardunit=awardunit_yao)
    yao_person.edit_plan_attr(bowl_rope, awardunit=awardunit_zia)
    yao_person.edit_plan_attr(bowl_rope, awardunit=awardunit_Xio)

    assert len(bowl_plan.awardunits) == 3
    assert len(bowl_plan.awardheirs) == 0

    # WHEN
    yao_person.conpute()

    # THEN
    assert len(bowl_plan.awardunits) == 3
    assert len(bowl_plan.awardheirs) == 3
    yao_person.edit_plan_attr(bowl_rope, awardunit_del=exx.yao)
    assert len(bowl_plan.awardunits) == 2
    assert len(bowl_plan.awardheirs) == 3

    # WHEN
    yao_person.conpute()

    # THEN
    assert len(bowl_plan.awardunits) == 2
    assert len(bowl_plan.awardheirs) == 2


def test_PersonUnit_get_plan_tree_ordered_rope_list_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    wk_str = "sem_jours"
    assert sue_person.get_plan_tree_ordered_rope_list()

    # WHEN
    ordered_label_list = sue_person.get_plan_tree_ordered_rope_list()

    # THEN
    assert len(ordered_label_list) == 17
    x_1st_rope_in_ordered_list = sue_person.get_plan_tree_ordered_rope_list()[0]
    root_rope = sue_person.planroot.get_plan_rope()
    assert x_1st_rope_in_ordered_list == root_rope
    x_8th_rope_in_ordered_list = sue_person.get_plan_tree_ordered_rope_list()[9]
    assert x_8th_rope_in_ordered_list == sue_person.make_l1_rope(wk_str)


def test_PersonUnit_get_plan_tree_ordered_rope_list_ReturnsObj_Scenario1():
    # ESTABLISH
    y_person = personunit_shop("Bob", exx.a23)
    root_rope = y_person.planroot.get_plan_rope()

    # WHEN
    y_1st_rope_in_ordered_list = y_person.get_plan_tree_ordered_rope_list()[0]
    # THEN
    assert y_1st_rope_in_ordered_list == root_rope


def test_PersonUnit_get_plan_tree_ordered_rope_list_Scenario2_CleansRangedPlanRopeTerms():
    # ESTABLISH
    yao_person = personunit_shop("Yao")

    # WHEN
    ziet_str = "zietline"
    ziet_rope = yao_person.make_l1_rope(ziet_str)
    yao_person.set_l1_plan(planunit_shop(ziet_str, begin=0, close=700))
    wks_str = "wks"
    yao_person.set_plan_obj(planunit_shop(wks_str, denom=7), ziet_rope)

    # THEN
    assert len(yao_person.get_plan_tree_ordered_rope_list()) == 3
    assert (
        len(yao_person.get_plan_tree_ordered_rope_list(no_range_descendants=True)) == 2
    )


def test_PersonUnit_get_plan_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    texas_str = "Texas"
    sue_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    sue_person.set_l1_plan(planunit_shop(exx.casa))

    # WHEN
    problems_dict = sue_person.get_plan_dict(problem=True)

    # THEN
    assert sue_person.keeps_justified
    texas_rope = sue_person.make_l1_rope(texas_str)
    texas_plan = sue_person.get_plan_obj(texas_rope)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_rope: texas_plan}


def test_PersonUnit_conpute_CreatesFullyPopulated_plan_dict():
    # ESTABLISH
    sue_personunit = get_personunit_with_4_levels_and_2reasons()

    # WHEN
    sue_personunit.conpute()

    # THEN
    assert len(sue_personunit._plan_dict) == 17


def test_PersonUnit_conpute_Resets_offtrack_kids_star_set():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    sue_personunit.offtrack_kids_star_set = set("YY")
    x_set = set()

    assert sue_personunit.offtrack_kids_star_set != x_set

    # WHEN
    sue_personunit.conpute()

    # THEN
    assert sue_personunit.offtrack_kids_star_set == x_set


def test_PersonUnit_conpute_WhenPlanRootHas_starButAll_kidsHaveZero_starAddTo_offtrack_kids_star_set_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_plan = planunit_shop(exx.casa, star=0)
    sue_personunit.set_l1_plan(casa_plan)
    assert sue_personunit.offtrack_kids_star_set == set()

    # WHEN
    sue_personunit.conpute()

    # THEN
    root_rope = sue_personunit.planroot.get_plan_rope()
    assert sue_personunit.offtrack_kids_star_set == {root_rope}

    # WHEN
    sue_personunit.edit_plan_attr(casa_rope, star=2)
    sue_personunit.conpute()

    # THEN
    assert sue_personunit.offtrack_kids_star_set == set()


def test_PersonUnit_conpute_WhenPlanUnitHas_starButAll_kidsHaveZero_starAddTo_offtrack_kids_star_set():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_plan = planunit_shop(exx.casa, star=1)

    bowl_rope = sue_personunit.make_rope(casa_rope, exx.bowl)
    bowl_plan = planunit_shop(exx.bowl, star=8)

    clean_str = "cleaning"
    clean_rope = sue_personunit.make_rope(casa_rope, clean_str)
    clean_plan = planunit_shop(clean_str, star=2)
    sue_personunit.set_plan_obj(planunit_shop(clean_str), casa_rope)

    sweep_rope = sue_personunit.make_rope(clean_rope, exx.sweep)
    sweep_plan = planunit_shop(exx.sweep, star=0)
    vacuum_str = "vacuum"
    vacuum_rope = sue_personunit.make_rope(clean_rope, vacuum_str)
    vacuum_plan = planunit_shop(vacuum_str, star=0)

    sue_personunit.set_l1_plan(casa_plan)
    sue_personunit.set_plan_obj(bowl_plan, casa_rope)
    sue_personunit.set_plan_obj(clean_plan, casa_rope)
    sue_personunit.set_plan_obj(sweep_plan, clean_rope)  # _star=0
    sue_personunit.set_plan_obj(vacuum_plan, clean_rope)  # _star=0

    assert sue_personunit.offtrack_kids_star_set == set()

    # WHEN
    sue_personunit.conpute()

    # THEN
    assert sue_personunit.offtrack_kids_star_set == {clean_rope}


def test_PersonUnit_conpute_CreatesNewGroupUnits_Scenario0():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_contact_cred_lumen = 3
    yao_contact_debt_lumen = 2
    zia_contact_cred_lumen = 4
    zia_contact_debt_lumen = 5
    yao_person.add_contactunit(exx.yao, yao_contact_cred_lumen, yao_contact_debt_lumen)
    yao_person.add_contactunit(exx.zia, zia_contact_cred_lumen, zia_contact_debt_lumen)
    root_rope = yao_person.planroot.get_plan_rope()
    x_planroot = yao_person.get_plan_obj(root_rope)
    x_planroot.set_awardunit(awardunit_shop(exx.yao))
    x_planroot.set_awardunit(awardunit_shop(exx.zia))
    x_planroot.set_awardunit(awardunit_shop(exx.xio))
    assert len(yao_person.get_contactunit_group_titles_dict()) == 2
    assert not yao_person.groupunit_exists(exx.yao)
    assert not yao_person.groupunit_exists(exx.zia)
    assert not yao_person.groupunit_exists(exx.xio)

    # WHEN
    yao_person.conpute()

    # THEN
    assert yao_person.groupunit_exists(exx.yao)
    assert yao_person.groupunit_exists(exx.zia)
    assert yao_person.groupunit_exists(exx.xio)
    assert len(yao_person.get_contactunit_group_titles_dict()) == 2
    assert len(yao_person.get_contactunit_group_titles_dict()) != len(
        yao_person.groupunits
    )
    assert len(yao_person.groupunits) == 3
    xio_groupunit = yao_person.get_groupunit(exx.xio)
    xio_symmerty_groupunit = yao_person.create_symmetry_groupunit(exx.xio)
    assert xio_groupunit.memberships.keys() == xio_symmerty_groupunit.memberships.keys()
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert not xio_groupunit.group_membership_exists(exx.xio)
    yao_membership = xio_groupunit.get_contact_membership(exx.yao)
    zia_membership = xio_groupunit.get_contact_membership(exx.zia)
    assert yao_membership.group_cred_lumen == yao_contact_cred_lumen
    assert zia_membership.group_cred_lumen == zia_contact_cred_lumen
    assert yao_membership.group_debt_lumen == yao_contact_debt_lumen
    assert zia_membership.group_debt_lumen == zia_contact_debt_lumen


def test_PersonUnit_conpute_CreatesNewGroupUnits_Scenario1():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    bowl_rope = yao_person.make_l1_rope(exx.bowl)
    yao_person.set_l1_plan(planunit_shop(exx.bowl))
    yao_person.add_contactunit(exx.yao)
    yao_person.add_contactunit(exx.zia)
    bowl_plan = yao_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(awardunit_shop(exx.yao))
    bowl_plan.set_awardunit(awardunit_shop(exx.zia))
    bowl_plan.set_awardunit(awardunit_shop(exx.xio))
    assert len(yao_person.get_contactunit_group_titles_dict()) == 2
    assert not yao_person.groupunit_exists(exx.yao)
    assert not yao_person.groupunit_exists(exx.zia)
    assert not yao_person.groupunit_exists(exx.xio)

    # WHEN
    yao_person.conpute()

    # THEN
    assert yao_person.groupunit_exists(exx.yao)
    assert yao_person.groupunit_exists(exx.zia)
    assert yao_person.groupunit_exists(exx.xio)
    assert len(yao_person.get_contactunit_group_titles_dict()) == 2
    assert len(yao_person.get_contactunit_group_titles_dict()) != len(
        yao_person.groupunits
    )
    assert len(yao_person.groupunits) == 3
    xio_groupunit = yao_person.get_groupunit(exx.xio)
    xio_symmerty_groupunit = yao_person.create_symmetry_groupunit(exx.xio)
    assert xio_groupunit.memberships.keys() == xio_symmerty_groupunit.memberships.keys()
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert not xio_groupunit.group_membership_exists(exx.xio)


def test_PersonUnit_get_tree_traverse_generated_groupunits_ReturnsObj():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    bowl_rope = yao_person.make_l1_rope(exx.bowl)
    yao_person.set_l1_plan(planunit_shop(exx.bowl))
    yao_person.add_contactunit(exx.yao)
    yao_person.add_contactunit(exx.zia)
    bowl_plan = yao_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(awardunit_shop(exx.yao))
    bowl_plan.set_awardunit(awardunit_shop(exx.zia))
    bowl_plan.set_awardunit(awardunit_shop(exx.xio))
    yao_person.conpute()
    assert yao_person.groupunit_exists(exx.yao)
    assert yao_person.groupunit_exists(exx.zia)
    assert yao_person.groupunit_exists(exx.xio)
    assert len(yao_person.get_contactunit_group_titles_dict()) == 2
    assert len(yao_person.get_contactunit_group_titles_dict()) != len(
        yao_person.groupunits
    )

    # WHEN
    symmerty_group_titles = yao_person.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 1
    assert symmerty_group_titles == {exx.xio}

    # ESTABLISH
    bowl_plan.set_awardunit(awardunit_shop(exx.run))
    assert not yao_person.groupunit_exists(exx.run)
    yao_person.conpute()
    assert yao_person.groupunit_exists(exx.run)

    # WHEN
    symmerty_group_titles = yao_person.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 2
    assert symmerty_group_titles == {exx.xio, exx.run}


def test_PersonUnit_conpute_Sets_planroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    wk_rope = yao_person.make_l1_rope(exx.wk)
    wk_addin = 10
    wk_plan = planunit_shop(exx.wk, begin=10, close=15, addin=wk_addin)
    yao_person.set_l1_plan(wk_plan)
    tue_str = "Tue"
    tue_rope = yao_person.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_person.set_plan_obj(planunit_shop(tue_str, addin=tue_addin), wk_rope)
    root_rope = yao_person.planroot.get_plan_rope()
    yao_person.edit_plan_attr(root_rope, reason_context=tue_rope, reason_case=tue_rope)

    wk_reason_lower = 3
    wk_reason_upper = 7
    yao_person.add_fact(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # assert len(ball_plan.reasonheirs) == 1
    # assert ball_plan.factheirs == {wk_rope: wk_factheir}
    # assert ball_plan.factheirs.get(wk_rope)
    # assert len(ball_plan.factheirs) == 1
    # assert ball_plan.factheirs.get(tue_rope) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_person.conpute()

    # THEN
    exception_str = f"Cannot have fact for range inheritor '{tue_rope}'. A ranged fact plan must have _begin, _close"
    assert str(excinfo.value) == exception_str

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_person_plan_dict = {wk_plan.get_plan_rope(): wk_plan, tue_plan.get_plan_rope(): tue_plan}
    # ball_plan.set_reasonheirs(x_person_plan_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_rope: wk_rope}
    # wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # tue_reason_lower = 113
    # tue_reason_upper = 117
    # tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    # root_plan = yao_person.get_plan_obj(root_rope)
    # print(f"{wk_rope=} {root_plan.factheirs.keys()=}")
    # assert root_plan.factheirs.get(wk_rope) == wk_factheir
    # assert len(root_plan.factheirs) == 2
    # assert root_plan.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_PersonUnit_conpute_SetsPlanUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    wk_rope = yao_person.make_l1_rope(exx.wk)
    wk_addin = 10
    wk_plan = planunit_shop(exx.wk, begin=10, close=15, addin=wk_addin)
    yao_person.set_l1_plan(wk_plan)
    tue_str = "Tue"
    tue_rope = yao_person.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_person.set_plan_obj(planunit_shop(tue_str, addin=tue_addin), wk_rope)
    ball_str = "ball"
    ball_rope = yao_person.make_l1_rope(ball_str)
    yao_person.set_l1_plan(planunit_shop(ball_str))
    yao_person.edit_plan_attr(ball_rope, reason_context=tue_rope, reason_case=tue_rope)

    wk_reason_lower = 3
    wk_reason_upper = 7
    yao_person.add_fact(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # assert len(ball_plan.reasonheirs) == 1
    # assert ball_plan.factheirs == {wk_rope: wk_factheir}
    # assert ball_plan.factheirs.get(wk_rope)
    # assert len(ball_plan.factheirs) == 1
    # assert ball_plan.factheirs.get(tue_rope) is None

    # WHEN
    yao_person.conpute()

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_person_plan_dict = {wk_plan.get_plan_rope(): wk_plan, tue_plan.get_plan_rope(): tue_plan}
    # ball_plan.set_reasonheirs(x_person_plan_dict, tue_reasonheirs)
    x_range_inheritors = {tue_rope: wk_rope}
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    tue_reason_lower = 113
    tue_reason_upper = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    ball_plan = yao_person.get_plan_obj(ball_rope)
    print(f"{wk_rope=} {ball_plan.factheirs.keys()=}")
    assert ball_plan.factheirs.get(wk_rope) == wk_factheir
    assert len(ball_plan.factheirs) == 2
    assert ball_plan.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}
