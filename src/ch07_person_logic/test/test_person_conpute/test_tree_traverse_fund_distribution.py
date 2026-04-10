from dataclasses import dataclass
from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_pool_num
from src.ch02_contact.contact import contactunit_shop
from src.ch02_contact.group import awardline_shop, awardunit_shop
from src.ch04_rope.rope import RopeTerm, to_rope
from src.ch06_plan.plan import PlanUnit, planunit_shop
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_with7am_clean_table_reason,
    get_personunit_with_4_levels,
    personunit_v001,
    personunit_v001_with_large_agenda,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_conpute_Sets_planunit_fund_onset_fund_cease_Scenario0():
    # ESTABLISH
    x_personunit = get_personunit_with7am_clean_table_reason()
    casa_rope = x_personunit.make_l1_rope("casa")
    catt_rope = x_personunit.make_l1_rope("cat have dinner")
    wk_rope = x_personunit.make_l1_rope("sem_jours")
    x_personunit.planroot.fund_onset = 13
    x_personunit.planroot.fund_cease = 13
    x_personunit.get_plan_obj(casa_rope).fund_onset = 13
    x_personunit.get_plan_obj(casa_rope).fund_cease = 13
    x_personunit.get_plan_obj(catt_rope).fund_onset = 13
    x_personunit.get_plan_obj(catt_rope).fund_cease = 13
    x_personunit.get_plan_obj(wk_rope).fund_onset = 13
    x_personunit.get_plan_obj(wk_rope).fund_cease = 13

    assert x_personunit.planroot.fund_onset == 13
    assert x_personunit.planroot.fund_cease == 13
    assert x_personunit.get_plan_obj(casa_rope).fund_onset == 13
    assert x_personunit.get_plan_obj(casa_rope).fund_cease == 13
    assert x_personunit.get_plan_obj(catt_rope).fund_onset == 13
    assert x_personunit.get_plan_obj(catt_rope).fund_cease == 13
    assert x_personunit.get_plan_obj(wk_rope).fund_onset == 13
    assert x_personunit.get_plan_obj(wk_rope).fund_cease == 13

    # WHEN
    x_personunit.conpute()

    # THEN
    assert x_personunit.planroot.fund_onset != 13
    assert x_personunit.planroot.fund_cease != 13
    assert x_personunit.get_plan_obj(casa_rope).fund_onset != 13
    assert x_personunit.get_plan_obj(casa_rope).fund_cease != 13
    assert x_personunit.get_plan_obj(catt_rope).fund_onset != 13
    assert x_personunit.get_plan_obj(catt_rope).fund_cease != 13
    assert x_personunit.get_plan_obj(wk_rope).fund_onset != 13
    assert x_personunit.get_plan_obj(wk_rope).fund_cease != 13


def test_PersonUnit_conpute_Sets_planunit_fund_onset_fund_cease_Scenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_personunit = personunit_shop("Yao")

    auto_str = "auto"
    auto_rope = yao_personunit.make_l1_rope(auto_str)
    auto_plan = planunit_shop(auto_str, star=10)
    yao_personunit.set_l1_plan(auto_plan)

    carn_str = "carn"
    carn_rope = yao_personunit.make_l1_rope(carn_str)
    carn_plan = planunit_shop(carn_str, star=60)
    yao_personunit.set_l1_plan(carn_plan)
    lamb_str = "lambs"
    lamb_rope = yao_personunit.make_rope(carn_rope, lamb_str)
    lamb_plan = planunit_shop(lamb_str, star=1)
    yao_personunit.set_plan_obj(lamb_plan, parent_rope=carn_rope)
    duck_str = "ducks"
    duck_rope = yao_personunit.make_rope(carn_rope, duck_str)
    duck_plan = planunit_shop(duck_str, star=2)
    yao_personunit.set_plan_obj(duck_plan, parent_rope=carn_rope)

    coal_str = "coal"
    coal_rope = yao_personunit.make_l1_rope(coal_str)
    coal_plan = planunit_shop(coal_str, star=30)
    yao_personunit.set_l1_plan(coal_plan)

    assert yao_personunit.planroot.fund_onset is None
    assert yao_personunit.planroot.fund_cease is None
    assert yao_personunit.get_plan_obj(auto_rope).fund_onset is None
    assert yao_personunit.get_plan_obj(auto_rope).fund_cease is None
    assert yao_personunit.get_plan_obj(carn_rope).fund_onset is None
    assert yao_personunit.get_plan_obj(carn_rope).fund_cease is None
    assert yao_personunit.get_plan_obj(coal_rope).fund_onset is None
    assert yao_personunit.get_plan_obj(coal_rope).fund_cease is None
    lamb_before = yao_personunit.get_plan_obj(rope=lamb_rope)
    assert lamb_before.fund_onset is None
    assert lamb_before.fund_cease is None
    duck_before = yao_personunit.get_plan_obj(rope=duck_rope)
    assert duck_before.fund_onset is None
    assert duck_before.fund_cease is None

    # WHEN
    yao_personunit.conpute()

    # THEN
    assert yao_personunit.planroot.fund_onset == 0.0
    assert yao_personunit.planroot.fund_cease == default_pool_num()
    assert yao_personunit.get_plan_obj(auto_rope).fund_onset == 0.0
    assert yao_personunit.get_plan_obj(auto_rope).fund_cease == default_pool_num() * 0.1
    assert yao_personunit.get_plan_obj(carn_rope).fund_onset == default_pool_num() * 0.1
    assert yao_personunit.get_plan_obj(carn_rope).fund_cease == default_pool_num() * 0.7
    assert yao_personunit.get_plan_obj(coal_rope).fund_onset == default_pool_num() * 0.7
    assert yao_personunit.get_plan_obj(coal_rope).fund_cease == default_pool_num() * 1.0

    duck_after = yao_personunit.get_plan_obj(rope=duck_rope)
    assert duck_after.fund_onset == default_pool_num() * 0.1
    assert duck_after.fund_cease == default_pool_num() * 0.5
    lamb_after = yao_personunit.get_plan_obj(rope=lamb_rope)
    assert lamb_after.fund_onset == default_pool_num() * 0.5
    assert lamb_after.fund_cease == default_pool_num() * 0.7


def test_PersonUnit_conpute_Sets_planunit_fund_onset_fund_cease_Scenario2_DifferentOrderOfPlans():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_personunit = personunit_shop("Yao")

    auto_str = "auto"
    auto_rope = yao_personunit.make_l1_rope(auto_str)
    auto_plan = planunit_shop(auto_str, star=10)
    yao_personunit.set_l1_plan(auto_plan)

    yarn_str = "yarn"
    yarn_rope = yao_personunit.make_l1_rope(yarn_str)
    yarn_plan = planunit_shop(yarn_str, star=60)
    yao_personunit.set_l1_plan(yarn_plan)
    lamb_str = "lambs"
    lamb_rope = yao_personunit.make_rope(yarn_rope, lamb_str)
    lamb_plan = planunit_shop(lamb_str, star=1)
    yao_personunit.set_plan_obj(lamb_plan, parent_rope=yarn_rope)
    duck_str = "ducks"
    duck_rope = yao_personunit.make_rope(yarn_rope, duck_str)
    duck_plan = planunit_shop(duck_str, star=2)
    yao_personunit.set_plan_obj(duck_plan, parent_rope=yarn_rope)

    coal_str = "coal"
    coal_rope = yao_personunit.make_l1_rope(coal_str)
    coal_plan = planunit_shop(coal_str, star=30)
    yao_personunit.set_l1_plan(coal_plan)

    assert yao_personunit.planroot.fund_onset is None
    assert yao_personunit.planroot.fund_cease is None
    assert yao_personunit.get_plan_obj(auto_rope).fund_onset is None
    assert yao_personunit.get_plan_obj(auto_rope).fund_cease is None
    assert yao_personunit.get_plan_obj(yarn_rope).fund_onset is None
    assert yao_personunit.get_plan_obj(yarn_rope).fund_cease is None
    assert yao_personunit.get_plan_obj(coal_rope).fund_onset is None
    assert yao_personunit.get_plan_obj(coal_rope).fund_cease is None
    lamb_before = yao_personunit.get_plan_obj(rope=lamb_rope)
    assert lamb_before.fund_onset is None
    assert lamb_before.fund_cease is None
    duck_before = yao_personunit.get_plan_obj(rope=duck_rope)
    assert duck_before.fund_onset is None
    assert duck_before.fund_cease is None

    # WHEN
    yao_personunit.conpute()

    # THEN
    assert yao_personunit.planroot.fund_onset == 0.0
    assert yao_personunit.planroot.fund_cease == default_pool_num()
    assert yao_personunit.get_plan_obj(auto_rope).fund_onset == 0.0
    assert yao_personunit.get_plan_obj(auto_rope).fund_cease == default_pool_num() * 0.1
    assert yao_personunit.get_plan_obj(coal_rope).fund_onset == default_pool_num() * 0.1
    assert yao_personunit.get_plan_obj(coal_rope).fund_cease == default_pool_num() * 0.4
    assert yao_personunit.get_plan_obj(yarn_rope).fund_onset == default_pool_num() * 0.4
    assert yao_personunit.get_plan_obj(yarn_rope).fund_cease == default_pool_num() * 1.0

    duck_after = yao_personunit.get_plan_obj(rope=duck_rope)
    assert duck_after.fund_onset == default_pool_num() * 0.4
    assert duck_after.fund_cease == default_pool_num() * 0.8
    lamb_after = yao_personunit.get_plan_obj(rope=lamb_rope)
    assert lamb_after.fund_onset == default_pool_num() * 0.8
    assert lamb_after.fund_cease == default_pool_num() * 1.0


def test_PersonUnit_conpute_Sets_fund_ratio_WithSomePlansOfZero_starScenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_person.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, pledge=True)
    sue_person.set_plan_obj(floor_plan, casa_rope)
    sue_person.set_l1_plan(planunit_shop("unimportant"))

    situation_str = "cleaniness situation"
    situation_rope = sue_person.make_rope(casa_rope, situation_str)
    sue_person.set_plan_obj(planunit_shop(situation_str, star=0), casa_rope)

    non_str = "not clean"
    yes_str = "yes clean"
    non_rope = sue_person.make_rope(situation_rope, non_str)
    yes_rope = sue_person.make_rope(situation_rope, yes_str)
    sue_person.set_plan_obj(planunit_shop(non_str), situation_rope)
    sue_person.set_plan_obj(planunit_shop(yes_str, star=2), situation_rope)

    assert sue_person.planroot.fund_ratio is None
    assert sue_person.get_plan_obj(casa_rope).fund_ratio is None
    assert sue_person.get_plan_obj(floor_rope).fund_ratio is None
    assert sue_person.get_plan_obj(situation_rope).fund_ratio is None
    assert sue_person.get_plan_obj(non_rope).fund_ratio is None
    assert sue_person.get_plan_obj(yes_rope).fund_ratio is None

    # WHEN
    sue_person.conpute()

    # THEN
    print(f"{sue_person.fund_pool=}")
    assert sue_person.planroot.fund_ratio == 1
    assert sue_person.get_plan_obj(casa_rope).fund_ratio == 0.5
    assert sue_person.get_plan_obj(floor_rope).fund_ratio == 0.5
    assert sue_person.get_plan_obj(situation_rope).fund_ratio == 0.0
    assert sue_person.get_plan_obj(non_rope).fund_ratio == 0.0
    assert sue_person.get_plan_obj(yes_rope).fund_ratio == 0.0


def test_PersonUnit_conpute_Sets_fund_ratio_WithSomePlansOfZero_starScenario1():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_person.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, pledge=True)
    sue_person.set_plan_obj(floor_plan, casa_rope)
    sue_person.set_l1_plan(planunit_shop("unimportant"))

    situation_str = "cleaniness situation"
    situation_rope = sue_person.make_rope(casa_rope, situation_str)
    sue_person.set_plan_obj(planunit_shop(situation_str), casa_rope)

    situation_plan = sue_person.get_plan_obj(situation_rope)
    print(f"{situation_plan.star=}")
    print("This should raise error: 'Planunit._'")

    clean_rope = sue_person.make_rope(situation_rope, exx.clean)
    very_str = "very_much"
    mod_str = "moderately"
    dirty_str = "dirty"

    sue_person.set_plan_obj(planunit_shop(exx.clean, star=0), situation_rope)
    sue_person.set_plan_obj(planunit_shop(very_str), clean_rope)
    sue_person.set_plan_obj(planunit_shop(mod_str, star=2), clean_rope)
    sue_person.set_plan_obj(planunit_shop(dirty_str), clean_rope)

    very_rope = sue_person.make_rope(clean_rope, very_str)
    mod_rope = sue_person.make_rope(clean_rope, mod_str)
    dirty_rope = sue_person.make_rope(clean_rope, dirty_str)
    assert sue_person.get_plan_obj(casa_rope).fund_ratio is None
    assert sue_person.get_plan_obj(floor_rope).fund_ratio is None
    assert sue_person.get_plan_obj(situation_rope).fund_ratio is None
    assert sue_person.get_plan_obj(clean_rope).fund_ratio is None
    assert sue_person.get_plan_obj(very_rope).fund_ratio is None
    assert sue_person.get_plan_obj(mod_rope).fund_ratio is None
    assert sue_person.get_plan_obj(dirty_rope).fund_ratio is None

    # WHEN
    sue_person.conpute()

    # THEN
    print(f"{sue_person.fund_pool=}")
    assert sue_person.get_plan_obj(casa_rope).fund_ratio == 0.5
    assert sue_person.get_plan_obj(floor_rope).fund_ratio == 0.25
    assert sue_person.get_plan_obj(situation_rope).fund_ratio == 0.25
    assert sue_person.get_plan_obj(clean_rope).fund_ratio == 0
    assert sue_person.get_plan_obj(very_rope).fund_ratio == 0
    assert sue_person.get_plan_obj(mod_rope).fund_ratio == 0
    assert sue_person.get_plan_obj(dirty_rope).fund_ratio == 0


def test_PersonUnit_conpute_WhenPlanUnitHasFundsBut_kidsHaveNostarDistributeFundsToContactUnits_Scenario0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue")
    sue_personunit.add_contactunit(exx.yao)
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

    assert sue_personunit.get_plan_obj(casa_rope).fund_ratio is None
    assert sue_personunit.get_plan_obj(bowl_rope).fund_ratio is None
    assert sue_personunit.get_plan_obj(clean_rope).fund_ratio is None
    assert sue_personunit.get_plan_obj(sweep_rope).fund_ratio is None
    assert sue_personunit.get_plan_obj(vacuum_rope).fund_ratio is None
    assert sue_personunit.get_groupunit(exx.yao) is None

    assert not sue_personunit.offtrack_fund
    assert sue_personunit.get_contact(exx.yao).fund_give == 0
    assert sue_personunit.get_contact(exx.yao).fund_take == 0

    # WHEN
    sue_personunit.conpute()

    # THEN
    print(f"{sue_personunit.fund_pool=}")
    clean_fund_ratio = 0.2
    assert sue_personunit.get_plan_obj(casa_rope).fund_ratio == 1
    assert sue_personunit.get_plan_obj(bowl_rope).fund_ratio == 0.8
    assert sue_personunit.get_plan_obj(clean_rope).fund_ratio == clean_fund_ratio
    assert sue_personunit.get_plan_obj(sweep_rope).fund_ratio == 0
    assert sue_personunit.get_plan_obj(vacuum_rope).fund_ratio == 0
    assert sue_personunit.get_groupunit(exx.yao).fund_give == 0
    assert sue_personunit.get_groupunit(exx.yao).fund_take == 0

    assert sue_personunit.offtrack_fund == clean_fund_ratio * default_pool_num()
    assert sue_personunit.get_contact(exx.yao).fund_give == default_pool_num()
    assert sue_personunit.get_contact(exx.yao).fund_take == default_pool_num()


def test_PersonUnit_conpute_TreeTraverseSetsAwardLine_fundFromRoot():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sue_person.conpute()
    # plan tree has no awardunits
    assert sue_person.planroot.awardlines == {}
    wk_str = "sem_jours"
    nation_str = "nation"
    sue_awardunit = awardunit_shop(awardee_title=exx.sue)
    sue_person.add_contactunit(contact_name=exx.sue)
    sue_person.planroot.set_awardunit(awardunit=sue_awardunit)
    # plan tree has awardlines
    assert sue_person.planroot.awardheirs.get(exx.sue) is None

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.planroot.awardheirs.get(exx.sue) is not None
    assert sue_person.planroot.awardheirs.get(exx.sue).awardee_title == exx.sue
    assert sue_person.planroot.awardlines != {}
    root_rope = to_rope(sue_person.planroot.plan_label)
    root_plan = sue_person.get_plan_obj(rope=root_rope)
    sue_awardline = sue_person.planroot.awardlines.get(exx.sue)
    print(f"{sue_awardline.fund_give=} {root_plan.fund_ratio=} ")
    print(f"  {sue_awardline.fund_take=} {root_plan.fund_ratio=} ")
    sum_x = 0
    cat_rope = sue_person.make_l1_rope("cat have dinner")
    cat_plan = sue_person.get_plan_obj(cat_rope)
    wk_rope = sue_person.make_l1_rope(wk_str)
    wk_plan = sue_person.get_plan_obj(wk_rope)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    casa_plan = sue_person.get_plan_obj(casa_rope)
    nation_rope = sue_person.make_l1_rope(nation_str)
    nation_plan = sue_person.get_plan_obj(nation_rope)
    sum_x = cat_plan.fund_ratio
    print(f"{cat_plan.fund_ratio=} {sum_x} ")
    sum_x += wk_plan.fund_ratio
    print(f"{wk_plan.fund_ratio=} {sum_x} ")
    sum_x += casa_plan.fund_ratio
    print(f"{casa_plan.fund_ratio=} {sum_x} ")
    sum_x += nation_plan.fund_ratio
    print(f"{nation_plan.fund_ratio=} {sum_x} ")
    tolerance = 1e-10
    assert sum_x < 1.0 + tolerance

    # for kid_plan in root_plan.kids.values():
    #     sum_x += kid_plan.fund_ratio
    #     print(f"  {kid_plan.fund_ratio=} {sum_x=} {kid_plan.get_plan_rope()=}")
    assert round(sue_awardline.fund_give, 15) == default_pool_num()
    assert round(sue_awardline.fund_take, 15) == default_pool_num()
    x_awardline = awardline_shop(exx.sue, default_pool_num(), default_pool_num())
    assert sue_person.planroot.awardlines == {x_awardline.awardee_title: x_awardline}


def test_PersonUnit_conpute_TreeTraverseSets_awardlines_To_planroot_FromNon_planroot_PlanUnit():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    sue_person.conpute()
    sue_person.add_contactunit(exx.sue)
    casa_rope = sue_person.make_l1_rope("casa")
    sue_person.get_plan_obj(casa_rope).set_awardunit(
        awardunit_shop(awardee_title=exx.sue)
    )
    assert sue_person.planroot.awardlines == {}

    # WHEN
    sue_person.conpute()

    # THEN
    assert sue_person.planroot.awardlines != {}
    print(f"{sue_person.planroot.awardlines=}")
    x_awardline = awardline_shop(
        awardee_title=exx.sue,
        fund_give=0.230769231 * default_pool_num(),
        fund_take=0.230769231 * default_pool_num(),
    )
    assert sue_person.planroot.awardlines == {x_awardline.awardee_title: x_awardline}
    casa_planunit = sue_person.get_plan_obj(casa_rope)
    assert casa_planunit.awardlines != {}
    assert casa_planunit.awardlines == {x_awardline.awardee_title: x_awardline}


def test_PersonUnit_conpute_WithRootLevelAwardUnitSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    sue_person.set_contactunit(contactunit_shop(exx.yao))
    sue_person.set_contactunit(contactunit_shop(exx.zia))
    sue_person.set_contactunit(contactunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    root_rope = to_rope(sue_person.planroot.plan_label)
    x_planroot = sue_person.get_plan_obj(root_rope)
    x_planroot.set_awardunit(awardunit=yao_awardunit)
    x_planroot.set_awardunit(awardunit=zia_awardunit)
    x_planroot.set_awardunit(awardunit=xio_awardunit)
    assert len(sue_person.get_contactunit_group_titles_dict()) == 3

    # WHEN
    sue_person.conpute()

    # THEN
    yao_groupunit = sue_person.get_groupunit(exx.yao)
    zia_groupunit = sue_person.get_groupunit(exx.zia)
    xio_groupunit = sue_person.get_groupunit(exx.xio)
    assert yao_groupunit.fund_give == 0.5 * default_pool_num()
    assert yao_groupunit.fund_take == 0.75 * default_pool_num()
    assert zia_groupunit.fund_give == 0.25 * default_pool_num()
    assert zia_groupunit.fund_take == 0.125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.25 * default_pool_num()
    assert xio_groupunit.fund_take == 0.125 * default_pool_num()
    cred_sum1 = yao_groupunit.fund_give
    cred_sum1 += zia_groupunit.fund_give + xio_groupunit.fund_give
    assert cred_sum1 == 1 * default_pool_num()
    debt_sum1 = yao_groupunit.fund_take
    debt_sum1 += zia_groupunit.fund_take + xio_groupunit.fund_take
    assert debt_sum1 == 1 * default_pool_num()

    # ESTABLISH
    sue_person.set_contactunit(contactunit_shop(exx.sue))
    sue_awardunit = awardunit_shop(exx.sue, give_force=37)
    x_planroot.set_awardunit(sue_awardunit)
    assert len(x_planroot.awardunits) == 4
    assert len(sue_person.get_contactunit_group_titles_dict()) == 4

    # WHEN
    sue_person.conpute()

    # THEN
    yao_groupunit = sue_person.get_groupunit(exx.yao)
    zia_groupunit = sue_person.get_groupunit(exx.zia)
    xio_groupunit = sue_person.get_groupunit(exx.xio)
    sue_groupunit = sue_person.get_groupunit(exx.sue)
    assert yao_groupunit.fund_give != 0.5 * default_pool_num()
    assert yao_groupunit.fund_take != 0.75 * default_pool_num()
    assert zia_groupunit.fund_give != 0.25 * default_pool_num()
    assert zia_groupunit.fund_take != 0.125 * default_pool_num()
    assert xio_groupunit.fund_give != 0.25 * default_pool_num()
    assert xio_groupunit.fund_take != 0.125 * default_pool_num()
    assert sue_groupunit.fund_give is not None
    assert sue_groupunit.fund_take is not None
    cred_sum1 = yao_groupunit.fund_give + zia_groupunit.fund_give
    cred_sum1 += xio_groupunit.fund_give + sue_groupunit.fund_give
    assert cred_sum1 == 1 * default_pool_num()
    debt_sum1 = yao_groupunit.fund_take + zia_groupunit.fund_take
    debt_sum1 += xio_groupunit.fund_take + sue_groupunit.fund_take
    assert round(debt_sum1) == 1 * default_pool_num()


def test_PersonUnit_conpute_WithLevel3AwardUnitSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    x_person = personunit_shop(exx.bob)
    bowl_rope = x_person.make_l1_rope(exx.bowl)
    x_person.set_l1_plan(planunit_shop(exx.bowl))

    x_person.set_contactunit(contactunit_shop(exx.yao))
    x_person.set_contactunit(contactunit_shop(exx.zia))
    x_person.set_contactunit(contactunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    bowl_plan = x_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(yao_awardunit)
    bowl_plan.set_awardunit(zia_awardunit)
    bowl_plan.set_awardunit(xio_awardunit)
    assert len(x_person.get_contactunit_group_titles_dict()) == 3

    # WHEN
    x_person.conpute()

    # THEN
    yao_groupunit = x_person.get_groupunit(exx.yao)
    zia_groupunit = x_person.get_groupunit(exx.zia)
    xio_groupunit = x_person.get_groupunit(exx.xio)
    assert yao_groupunit.fund_give == 0.5 * default_pool_num()
    assert yao_groupunit.fund_take == 0.75 * default_pool_num()
    assert zia_groupunit.fund_give == 0.25 * default_pool_num()
    assert zia_groupunit.fund_take == 0.125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.25 * default_pool_num()
    assert xio_groupunit.fund_take == 0.125 * default_pool_num()
    groupunit_fund_give_sum = (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_pool_num()
    assert groupunit_fund_take_sum == 1 * default_pool_num()


def test_PersonUnit_conpute_CreatesNewGroupUnitAndSetsGroup_fund_give_fund_take():
    # ESTABLISH
    x_person = personunit_shop(exx.yao)
    bowl_rope = x_person.make_l1_rope(exx.bowl)
    x_person.set_l1_plan(planunit_shop(exx.bowl))

    x_person.set_contactunit(contactunit_shop(exx.yao))
    x_person.set_contactunit(contactunit_shop(exx.zia))
    # x_person.set_contactunit(contactunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    bowl_plan = x_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(yao_awardunit)
    bowl_plan.set_awardunit(zia_awardunit)
    bowl_plan.set_awardunit(xio_awardunit)
    assert len(x_person.get_contactunit_group_titles_dict()) == 2

    # WHEN
    x_person.conpute()

    # THEN
    yao_groupunit = x_person.get_groupunit(exx.yao)
    zia_groupunit = x_person.get_groupunit(exx.zia)
    xio_groupunit = x_person.get_groupunit(exx.xio)
    assert len(x_person.get_contactunit_group_titles_dict()) != len(x_person.groupunits)
    assert yao_groupunit.fund_give == 0.5 * default_pool_num()
    assert yao_groupunit.fund_take == 0.75 * default_pool_num()
    assert zia_groupunit.fund_give == 0.25 * default_pool_num()
    assert zia_groupunit.fund_take == 0.125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.25 * default_pool_num()
    assert xio_groupunit.fund_take == 0.125 * default_pool_num()
    groupunit_fund_give_sum = (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_pool_num()
    assert groupunit_fund_take_sum == 1 * default_pool_num()


def test_PersonUnit_conpute_WithLevel3AwardUnitAndEmptyAncestorsSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    x_person = personunit_shop(exx.yao)
    bowl_rope = x_person.make_l1_rope(exx.bowl)
    x_person.set_l1_plan(planunit_shop(exx.bowl))

    x_person.set_contactunit(contactunit_shop(exx.yao))
    x_person.set_contactunit(contactunit_shop(exx.zia))
    x_person.set_contactunit(contactunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    bowl_plan = x_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(yao_awardunit)
    bowl_plan.set_awardunit(zia_awardunit)
    bowl_plan.set_awardunit(xio_awardunit)

    # no awardunits attached to this one
    x_person.set_l1_plan(planunit_shop("hunt", star=3))

    # WHEN
    x_person.conpute()

    # THEN
    x_planroot = x_person.get_plan_obj(x_person.planroot.get_plan_rope())
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardunits[str(exx.yao)]
    print(f"{excinfo.value=}")
    assert str(excinfo.value) == f"'{exx.yao}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardunits[str(exx.zia)]
    assert str(excinfo.value) == f"'{exx.zia}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.awardunits[str(exx.xio)]
    assert str(excinfo.value) == f"'{exx.xio}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.kids["hunt"].awardheirs[str(exx.yao)]
    assert str(excinfo.value) == f"'{exx.yao}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.kids["hunt"].awardheirs[str(exx.zia)]
    assert str(excinfo.value) == f"'{exx.zia}'"
    with pytest_raises(Exception) as excinfo:
        x_planroot.kids["hunt"].awardheirs[str(exx.xio)]
    assert str(excinfo.value) == f"'{exx.xio}'"

    # THEN
    yao_groupunit = x_person.get_groupunit(exx.yao)
    zia_groupunit = x_person.get_groupunit(exx.zia)
    xio_groupunit = x_person.get_groupunit(exx.xio)
    assert yao_groupunit.fund_give == 0.125 * default_pool_num()
    assert yao_groupunit.fund_take == 0.1875 * default_pool_num()
    assert zia_groupunit.fund_give == 0.0625 * default_pool_num()
    assert zia_groupunit.fund_take == 0.03125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.0625 * default_pool_num()
    assert xio_groupunit.fund_take == 0.03125 * default_pool_num()
    assert (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
        == 0.25 * default_pool_num()
    )
    assert (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
        == 0.25 * default_pool_num()
    )


def test_PersonUnit_set_awardunit_CalculatesInheritedAwardUnitPersonFund():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    sue_person.set_contactunit(contactunit_shop(exx.yao))
    sue_person.set_contactunit(contactunit_shop(exx.zia))
    sue_person.set_contactunit(contactunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    Xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    sue_person.planroot.set_awardunit(yao_awardunit)
    sue_person.planroot.set_awardunit(zia_awardunit)
    sue_person.planroot.set_awardunit(Xio_awardunit)
    assert len(sue_person.planroot.awardunits) == 3

    # WHEN
    plan_dict = sue_person.get_plan_dict()

    # THEN
    print(f"{plan_dict.keys()=}")
    plan_bob = plan_dict.get(sue_person.planroot.get_plan_rope())
    assert len(plan_bob.awardheirs) == 3

    bheir_yao = plan_bob.awardheirs.get(exx.yao)
    bheir_zia = plan_bob.awardheirs.get(exx.zia)
    bheir_Xio = plan_bob.awardheirs.get(exx.xio)
    assert bheir_yao.fund_give == 0.5 * default_pool_num()
    assert bheir_yao.fund_take == 0.75 * default_pool_num()
    assert bheir_zia.fund_give == 0.25 * default_pool_num()
    assert bheir_zia.fund_take == 0.125 * default_pool_num()
    assert bheir_Xio.fund_give == 0.25 * default_pool_num()
    assert bheir_Xio.fund_take == 0.125 * default_pool_num()
    assert (
        bheir_yao.fund_give + bheir_zia.fund_give + bheir_Xio.fund_give
        == 1 * default_pool_num()
    )
    assert (
        bheir_yao.fund_take + bheir_zia.fund_take + bheir_Xio.fund_take
        == 1 * default_pool_num()
    )

    # fund_give_sum = 0
    # fund_take_sum = 0
    # for group in x_person.planroot.awardheirs.values():
    #     print(f"{group=}")
    #     assert group.fund_give is not None
    #     assert group.fund_give in [0.25, 0.5]
    #     assert group.fund_take is not None
    #     assert group.fund_take in [0.75, 0.125]
    #     fund_give_sum += group.fund_give
    #     fund_take_sum += group.fund_take

    # assert fund_give_sum == 1
    # assert fund_take_sum == 1


def test_PersonUnit_conpute_SetsGroupLinkPersonCredAndDebt():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    yao_person.set_contactunit(contactunit_shop(exx.sue))
    yao_person.set_contactunit(contactunit_shop(exx.bob))
    yao_person.set_contactunit(contactunit_shop(exx.zia))
    sue_awardunit = awardunit_shop(exx.sue, 20, take_force=40)
    bob_awardunit = awardunit_shop(exx.bob, 10, take_force=5)
    zia_awardunit = awardunit_shop(exx.zia, 10, take_force=5)
    root_rope = yao_person.planroot.get_plan_rope()
    yao_person.edit_plan_attr(root_rope, awardunit=sue_awardunit)
    yao_person.edit_plan_attr(root_rope, awardunit=bob_awardunit)
    yao_person.edit_plan_attr(root_rope, awardunit=zia_awardunit)

    sue_contactunit = yao_person.get_contact(exx.sue)
    bob_contactunit = yao_person.get_contact(exx.bob)
    zia_contactunit = yao_person.get_contact(exx.zia)
    sue_sue_membership = sue_contactunit.get_membership(exx.sue)
    bob_bob_membership = bob_contactunit.get_membership(exx.bob)
    zia_zia_membership = zia_contactunit.get_membership(exx.zia)
    assert sue_sue_membership.fund_give is None
    assert sue_sue_membership.fund_take is None
    assert bob_bob_membership.fund_give is None
    assert bob_bob_membership.fund_take is None
    assert zia_zia_membership.fund_give is None
    assert zia_zia_membership.fund_take is None

    # WHEN
    yao_person.conpute()

    # THEN
    assert sue_sue_membership.fund_give == 0.5 * default_pool_num()
    assert sue_sue_membership.fund_take == 0.8 * default_pool_num()
    assert bob_bob_membership.fund_give == 0.25 * default_pool_num()
    assert bob_bob_membership.fund_take == 0.1 * default_pool_num()
    assert zia_zia_membership.fund_give == 0.25 * default_pool_num()
    assert zia_zia_membership.fund_take == 0.1 * default_pool_num()

    membership_cred_sum = (
        sue_sue_membership.fund_give
        + bob_bob_membership.fund_give
        + zia_zia_membership.fund_give
    )
    assert membership_cred_sum == 1.0 * default_pool_num()
    membership_debt_sum = (
        sue_sue_membership.fund_take
        + bob_bob_membership.fund_take
        + zia_zia_membership.fund_take
    )
    assert membership_debt_sum == 1.0 * default_pool_num()

    # ESTABLISH another pledge, check metrics are as expected
    yao_person.set_contactunit(contactunit_shop(exx.xio))
    yao_person.planroot.set_awardunit(awardunit_shop(exx.xio, 20, take_force=13))

    # WHEN
    yao_person.conpute()

    # THEN
    xio_groupunit = yao_person.get_groupunit(exx.xio)
    xio_xio_membership = xio_groupunit.get_contact_membership(exx.xio)
    sue_contactunit = yao_person.get_contact(exx.sue)
    bob_contactunit = yao_person.get_contact(exx.bob)
    zia_contactunit = yao_person.get_contact(exx.zia)
    sue_sue_membership = sue_contactunit.get_membership(exx.sue)
    bob_bob_membership = bob_contactunit.get_membership(exx.bob)
    zia_zia_membership = zia_contactunit.get_membership(exx.zia)
    assert sue_sue_membership.fund_give != 0.25 * default_pool_num()
    assert sue_sue_membership.fund_take != 0.8 * default_pool_num()
    assert bob_bob_membership.fund_give != 0.25 * default_pool_num()
    assert bob_bob_membership.fund_take != 0.1 * default_pool_num()
    assert zia_zia_membership.fund_give != 0.5 * default_pool_num()
    assert zia_zia_membership.fund_take != 0.1 * default_pool_num()
    assert xio_xio_membership.fund_give is not None
    assert xio_xio_membership.fund_take is not None

    x_fund_give_sum = (
        sue_sue_membership.fund_give
        + bob_bob_membership.fund_give
        + zia_zia_membership.fund_give
        + xio_xio_membership.fund_give
    )
    print(f"{x_fund_give_sum=}")
    assert x_fund_give_sum == 1.0 * default_pool_num()
    x_fund_take_sum = (
        sue_sue_membership.fund_take
        + bob_bob_membership.fund_take
        + zia_zia_membership.fund_take
        + xio_xio_membership.fund_take
    )
    assert x_fund_take_sum == 1.0 * default_pool_num()


def test_PersonUnit_conpute_SetsContactUnitPerson_fund():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    bowl_rope = yao_person.make_l1_rope(exx.bowl)
    yao_person.set_l1_plan(planunit_shop(exx.bowl))
    yao_person.set_contactunit(contactunit_shop(exx.sue))
    yao_person.set_contactunit(contactunit_shop(exx.bob))
    yao_person.set_contactunit(contactunit_shop(exx.zia))
    bl_sue = awardunit_shop(exx.sue, 20, take_force=40)
    bl_bob = awardunit_shop(exx.bob, 10, take_force=5)
    bl_zia = awardunit_shop(exx.zia, 10, take_force=5)
    yao_person.get_plan_obj(bowl_rope).set_awardunit(bl_sue)
    yao_person.get_plan_obj(bowl_rope).set_awardunit(bl_bob)
    yao_person.get_plan_obj(bowl_rope).set_awardunit(bl_zia)

    sue_contactunit = yao_person.get_contact(exx.sue)
    bob_contactunit = yao_person.get_contact(exx.bob)
    zia_contactunit = yao_person.get_contact(exx.zia)

    assert sue_contactunit.fund_give == 0
    assert sue_contactunit.fund_take == 0
    assert bob_contactunit.fund_give == 0
    assert bob_contactunit.fund_take == 0
    assert zia_contactunit.fund_give == 0
    assert zia_contactunit.fund_take == 0

    # WHEN
    yao_person.conpute()

    # THEN
    assert sue_contactunit.fund_give == 0.5 * default_pool_num()
    assert sue_contactunit.fund_take == 0.8 * default_pool_num()
    assert bob_contactunit.fund_give == 0.25 * default_pool_num()
    assert bob_contactunit.fund_take == 0.1 * default_pool_num()
    assert zia_contactunit.fund_give == 0.25 * default_pool_num()
    assert zia_contactunit.fund_take == 0.1 * default_pool_num()

    assert (
        sue_contactunit.fund_give
        + bob_contactunit.fund_give
        + zia_contactunit.fund_give
        == 1.0 * default_pool_num()
    )
    assert (
        sue_contactunit.fund_take
        + bob_contactunit.fund_take
        + zia_contactunit.fund_take
        == 1.0 * default_pool_num()
    )

    # WHEN another pledge, check metrics are as expected
    yao_person.set_contactunit(contactunit_shop(exx.xio))
    yao_person.planroot.set_awardunit(awardunit_shop(exx.xio, 20, take_force=10))
    yao_person.conpute()

    # THEN
    xio_contactunit = yao_person.get_contact(exx.xio)

    assert sue_contactunit.fund_give != 0.5 * default_pool_num()
    assert sue_contactunit.fund_take != 0.8 * default_pool_num()
    assert bob_contactunit.fund_give != 0.25 * default_pool_num()
    assert bob_contactunit.fund_take != 0.1 * default_pool_num()
    assert zia_contactunit.fund_give != 0.25 * default_pool_num()
    assert zia_contactunit.fund_take != 0.1 * default_pool_num()
    assert xio_contactunit.fund_give is not None
    assert xio_contactunit.fund_take is not None

    sum_contactunit_fund_give = (
        sue_contactunit.fund_give
        + bob_contactunit.fund_give
        + zia_contactunit.fund_give
    )
    assert sum_contactunit_fund_give < 1.0 * default_pool_num()
    assert (
        sue_contactunit.fund_give
        + bob_contactunit.fund_give
        + zia_contactunit.fund_give
        + xio_contactunit.fund_give
        == 1.0 * default_pool_num()
    )
    assert (
        sue_contactunit.fund_take
        + bob_contactunit.fund_take
        + zia_contactunit.fund_take
        < 1.0 * default_pool_num()
    )
    assert (
        sue_contactunit.fund_take
        + bob_contactunit.fund_take
        + zia_contactunit.fund_take
        + xio_contactunit.fund_take
        == 1.0 * default_pool_num()
    )


def test_PersonUnit_conpute_SetsPartGroupedLWContactUnitPerson_fund():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    bowl_rope = yao_person.make_l1_rope(exx.bowl)
    yao_person.set_l1_plan(planunit_shop(exx.bowl))
    yao_person.set_contactunit(contactunit_shop(exx.sue))
    yao_person.set_contactunit(contactunit_shop(exx.bob))
    yao_person.set_contactunit(contactunit_shop(exx.zia))
    sue_awardunit = awardunit_shop(exx.sue, 20, take_force=40)
    bob_awardunit = awardunit_shop(exx.bob, 10, take_force=5)
    zia_awardunit = awardunit_shop(exx.zia, 10, take_force=5)
    bowl_plan = yao_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(sue_awardunit)
    bowl_plan.set_awardunit(bob_awardunit)
    bowl_plan.set_awardunit(zia_awardunit)

    # no awardunits attached to this one
    hunt_str = "hunt"
    yao_person.set_l1_plan(planunit_shop(hunt_str, star=3))

    # WHEN
    yao_person.conpute()

    # THEN
    sue_groupunit = yao_person.get_groupunit(exx.sue)
    bob_groupunit = yao_person.get_groupunit(exx.bob)
    zia_groupunit = yao_person.get_groupunit(exx.zia)
    assert sue_groupunit.fund_give != 0.5 * default_pool_num()
    assert sue_groupunit.fund_take != 0.8 * default_pool_num()
    assert bob_groupunit.fund_give != 0.25 * default_pool_num()
    assert bob_groupunit.fund_take != 0.1 * default_pool_num()
    assert zia_groupunit.fund_give != 0.25 * default_pool_num()
    assert zia_groupunit.fund_take != 0.1 * default_pool_num()
    assert (
        sue_groupunit.fund_give + bob_groupunit.fund_give + zia_groupunit.fund_give
        == 0.25 * default_pool_num()
    )
    assert (
        sue_groupunit.fund_take + bob_groupunit.fund_take + zia_groupunit.fund_take
        == 0.25 * default_pool_num()
    )

    sue_contactunit = yao_person.get_contact(exx.sue)
    bob_contactunit = yao_person.get_contact(exx.bob)
    zia_contactunit = yao_person.get_contact(exx.zia)

    assert sue_contactunit.fund_give == 0.375 * default_pool_num()
    assert sue_contactunit.fund_take == 0.45 * default_pool_num()
    assert bob_contactunit.fund_give == 0.3125 * default_pool_num()
    assert bob_contactunit.fund_take == 0.275 * default_pool_num()
    assert zia_contactunit.fund_give == 0.3125 * default_pool_num()
    assert zia_contactunit.fund_take == 0.275 * default_pool_num()

    assert (
        sue_contactunit.fund_give
        + bob_contactunit.fund_give
        + zia_contactunit.fund_give
        == 1.0 * default_pool_num()
    )
    assert (
        sue_contactunit.fund_take
        + bob_contactunit.fund_take
        + zia_contactunit.fund_take
        == 1.0 * default_pool_num()
    )


def test_PersonUnit_conpute_CreatesNewGroupUnitAndSetsContact_fund_give_fund_take():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob)
    bowl_rope = bob_person.make_l1_rope(exx.bowl)
    bob_person.set_l1_plan(planunit_shop(exx.bowl))

    bob_person.set_contactunit(contactunit_shop(exx.yao))
    bob_person.set_contactunit(contactunit_shop(exx.zia))
    # bob_person.set_contactunit(contactunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    bowl_plan = bob_person.get_plan_obj(bowl_rope)
    bowl_plan.set_awardunit(yao_awardunit)
    bowl_plan.set_awardunit(zia_awardunit)
    bowl_plan.set_awardunit(xio_awardunit)
    assert len(bob_person.get_contactunit_group_titles_dict()) == 2

    # WHEN
    bob_person.conpute()

    # THEN
    assert len(bob_person.get_contactunit_group_titles_dict()) != len(
        bob_person.groupunits
    )
    assert not bob_person.contact_exists(exx.xio)
    yao_contactunit = bob_person.get_contact(exx.yao)
    zia_contactunit = bob_person.get_contact(exx.zia)
    contactunit_fund_give_sum = yao_contactunit.fund_give + zia_contactunit.fund_give
    contactunit_fund_take_sum = yao_contactunit.fund_take + zia_contactunit.fund_take
    assert contactunit_fund_give_sum == default_pool_num()
    assert contactunit_fund_take_sum == default_pool_num()


def test_PersonUnit_conpute_SetsContactUnit_fund_give_fund_take():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    yao_person.set_l1_plan(planunit_shop("bowl"))
    yao_person.set_contactunit(contactunit_shop(exx.sue, 8))
    yao_person.set_contactunit(contactunit_shop(exx.bob))
    yao_person.set_contactunit(contactunit_shop(exx.zia))
    sue_contactunit = yao_person.get_contact(exx.sue)
    bob_contactunit = yao_person.get_contact(exx.bob)
    zia_contactunit = yao_person.get_contact(exx.zia)
    assert sue_contactunit.fund_give == 0
    assert sue_contactunit.fund_take == 0
    assert bob_contactunit.fund_give == 0
    assert bob_contactunit.fund_take == 0
    assert zia_contactunit.fund_give == 0
    assert zia_contactunit.fund_take == 0

    # WHEN
    yao_person.conpute()

    # THEN
    fund_give_sum = (
        sue_contactunit.fund_give
        + bob_contactunit.fund_give
        + zia_contactunit.fund_give
    )
    assert fund_give_sum == 1.0 * default_pool_num()
    fund_take_sum = (
        sue_contactunit.fund_take
        + bob_contactunit.fund_take
        + zia_contactunit.fund_take
    )
    assert fund_take_sum == 1.0 * default_pool_num()


def clear_all_contactunits_groupunits_fund_agenda_give_take(x_person: PersonUnit):
    # delete person_agenda_debt and person_agenda_cred
    for x_groupunit in x_person.groupunits.values():
        x_groupunit.clear_group_fund_give_take()
        # for membership_x in groupunit_x._contacts.values():
        #     print(f"{groupunit_x.} {membership_x.}  {membership_x.fund_give:.6f} {membership_x.contact_debt_lumen=} {membership_fund_take:t:.6f} {membership_x.} ")

    # delete person_agenda_debt and person_agenda_cred
    for x_contactunit in x_person.contacts.values():
        x_contactunit.clear_fund_give_take()


@dataclass
class GroupAgendaMetrics:
    sum_groupunit_give: float = 0
    sum_groupunit_take: float = 0
    sum_membership_cred: float = 0
    sum_membership_debt: float = 0
    membership_count: int = 0

    def set_groupagendametrics_sums(self, x_person: PersonUnit):
        for x_groupunit in x_person.groupunits.values():
            self.sum_groupunit_give += x_groupunit.fund_agenda_give
            self.sum_groupunit_take += x_groupunit.fund_agenda_take
            for membership_x in x_groupunit.memberships.values():
                self.sum_membership_cred += membership_x.fund_agenda_give
                self.sum_membership_debt += membership_x.fund_agenda_take
                self.membership_count += 1


@dataclass
class ContactAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_contactagendametrics_sums(self, x_person: PersonUnit):
        for contactunit in x_person.contacts.values():
            self.sum_agenda_cred += contactunit.fund_agenda_give
            self.sum_agenda_debt += contactunit.fund_agenda_take
            self.sum_agenda_ratio_cred += contactunit.fund_agenda_ratio_give
            self.sum_agenda_ratio_debt += contactunit.fund_agenda_ratio_take


@dataclass
class AwardAgendaMetrics:
    sum_person_agenda_plans_fund_total = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_person_i_sum = 0
    agenda_yes_person_i_sum = 0

    def set_awardagendametrics_sums(self, agenda_dict: dict[RopeTerm, PlanUnit]):
        for agenda_plan in agenda_dict.values():
            self.sum_person_agenda_plans_fund_total += agenda_plan.get_plan_fund_total()
            if agenda_plan.awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_person_i_sum += agenda_plan.get_plan_fund_total()
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_person_i_sum += agenda_plan.get_plan_fund_total()


def test_PersonUnit_agenda_cred_debt_SetAttrs():
    # ESTABLISH
    yao_person = personunit_v001_with_large_agenda()
    clear_all_contactunits_groupunits_fund_agenda_give_take(yao_person)

    # TEST person_agenda_debt and person_agenda_cred are empty
    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_groupagendametrics_sums(yao_person)
    assert x_groupagendametrics.sum_groupunit_give == 0
    assert x_groupagendametrics.sum_groupunit_take == 0
    assert x_groupagendametrics.sum_membership_cred == 0
    assert x_groupagendametrics.sum_membership_debt == 0

    # TEST person_agenda_debt and person_agenda_cred are empty
    x_contactagendametrics = ContactAgendaMetrics()
    x_contactagendametrics.set_contactagendametrics_sums(yao_person)
    assert x_contactagendametrics.sum_agenda_cred == 0
    assert x_contactagendametrics.sum_agenda_debt == 0
    assert x_contactagendametrics.sum_agenda_ratio_cred == 0
    assert x_contactagendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = yao_person.get_agenda_dict()
    # for plan_rope in yao_person._plan_dict.keys():
    #     print(f"{plan_rope=}")
    # for x_contact in yao_person.contacts.values():
    #     for x_membership in x_contact.memberships.values():
    #         print(f"{x_membership.group_title=}")

    # THEN
    print(f"{yao_person.get_reason_contexts()=}")
    assert len(agenda_dict) == 69
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_awardagendametrics_sums(agenda_dict=agenda_dict)
    # print(f"{sum_person_agenda_plans_fund_total=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    predicted_agenda_no_person_i_sum = int(0.004908864 * default_pool_num())
    assert (
        x_awardagendametrics.agenda_no_person_i_sum == predicted_agenda_no_person_i_sum
    )
    predicted_agenda_yes_person_i_sum = int(0.003065400 * default_pool_num())
    assert (
        x_awardagendametrics.agenda_yes_person_i_sum
        == predicted_agenda_yes_person_i_sum
    )
    assert are_equal(
        x_awardagendametrics.agenda_no_person_i_sum
        + x_awardagendametrics.agenda_yes_person_i_sum,
        x_awardagendametrics.sum_person_agenda_plans_fund_total,
    )
    predicted_sum_person_agenda_plans_fund_total = 0.007974264 * default_pool_num()
    assert (
        x_awardagendametrics.sum_person_agenda_plans_fund_total
        == predicted_sum_person_agenda_plans_fund_total
    )

    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_groupagendametrics_sums(yao_person)
    assert x_groupagendametrics.membership_count == 81
    x_sum = 3065400
    print(f"{x_groupagendametrics.sum_groupunit_give=}")
    assert are_equal(x_groupagendametrics.sum_groupunit_give, x_sum)
    assert are_equal(x_groupagendametrics.sum_groupunit_take, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_cred, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_person_i_sum,
        x_groupagendametrics.sum_groupunit_give,
    )

    assert all_contactunits_have_legitimate_values(yao_person)

    x_contactagendametrics = ContactAgendaMetrics()
    x_contactagendametrics.set_contactagendametrics_sums(yao_person)
    assert are_equal(
        x_contactagendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_person_agenda_plans_fund_total,
    )
    assert are_equal(
        x_contactagendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_person_agenda_plans_fund_total,
    )
    assert are_equal(x_contactagendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_contactagendametrics.sum_agenda_ratio_debt, 1)

    # contactunit_fund_give_sum = 0.0
    # contactunit_fund_take_sum = 0.0

    # assert contactunit_fund_give_sum == 1.0
    # assert contactunit_fund_take_sum > 0.9999999
    # assert contactunit_fund_take_sum < 1.00000001


def all_contactunits_have_legitimate_values(x_person: PersonUnit):
    return not any(
        (
            contactunit.fund_give is None
            or contactunit.fund_give in [0.25, 0.5]
            or contactunit.fund_take is None
            or contactunit.fund_take in [0.8, 0.1]
        )
        for contactunit in x_person.contacts.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_PersonUnit_conpute_SetsAttrsWhenNoFactUnitsNoReasonUnitsEmpty_agenda_ratio_cred_debt():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    sue_contactunit = contactunit_shop(exx.sue, 0.5, contact_debt_lumen=2)
    bob_contactunit = contactunit_shop(exx.bob, 1.5, contact_debt_lumen=3)
    zia_contactunit = contactunit_shop(exx.zia, 8, contact_debt_lumen=5)
    yao_person.set_contactunit(sue_contactunit)
    yao_person.set_contactunit(bob_contactunit)
    yao_person.set_contactunit(zia_contactunit)
    sue_contact = yao_person.get_contact(exx.sue)
    bob_contact = yao_person.get_contact(exx.bob)
    zia_contact = yao_person.get_contact(exx.zia)

    assert not sue_contact.fund_give
    assert not sue_contact.fund_take
    assert not bob_contact.fund_give
    assert not bob_contact.fund_take
    assert not zia_contact.fund_give
    assert not zia_contact.fund_take
    assert not sue_contact.fund_agenda_give
    assert not sue_contact.fund_agenda_take
    assert not bob_contact.fund_agenda_give
    assert not bob_contact.fund_agenda_take
    assert not zia_contact.fund_agenda_give
    assert not zia_contact.fund_agenda_take
    assert not sue_contact.fund_agenda_ratio_give
    assert not sue_contact.fund_agenda_ratio_take
    assert not bob_contact.fund_agenda_ratio_give
    assert not bob_contact.fund_agenda_ratio_take
    assert not zia_contact.fund_agenda_ratio_give
    assert not zia_contact.fund_agenda_ratio_take

    # WHEN
    yao_person.conpute()

    # THEN
    assert yao_person.reason_contexts == set()
    assert sue_contact.fund_give == 50000000
    assert sue_contact.fund_take == 200000000
    assert bob_contact.fund_give == 150000000
    assert bob_contact.fund_take == 300000000
    assert zia_contact.fund_give == 800000000
    assert zia_contact.fund_take == 500000000
    assert sue_contact.fund_agenda_give == 50000000
    assert sue_contact.fund_agenda_take == 200000000
    assert bob_contact.fund_agenda_give == 150000000
    assert bob_contact.fund_agenda_take == 300000000
    assert zia_contact.fund_agenda_give == 800000000
    assert zia_contact.fund_agenda_take == 500000000
    assert sue_contact.fund_agenda_give == sue_contact.fund_give
    assert sue_contact.fund_agenda_take == sue_contact.fund_take
    assert bob_contact.fund_agenda_give == bob_contact.fund_give
    assert bob_contact.fund_agenda_take == bob_contact.fund_take
    assert zia_contact.fund_agenda_give == zia_contact.fund_give
    assert zia_contact.fund_agenda_take == zia_contact.fund_take
    assert sue_contact.fund_agenda_ratio_give == 0.05
    assert sue_contact.fund_agenda_ratio_take == 0.2
    assert bob_contact.fund_agenda_ratio_give == 0.15
    assert bob_contact.fund_agenda_ratio_take == 0.3
    assert zia_contact.fund_agenda_ratio_give == 0.8
    assert zia_contact.fund_agenda_ratio_take == 0.5


def test_PersonUnit_conpute_CreatesGroupUnitWith_personunit_v001():
    # ESTABLISH / WHEN
    yao_person = personunit_v001()
    yao_person.conpute()

    # THEN
    assert yao_person.groupunits is not None
    assert len(yao_person.groupunits) == 34
    everyone_contacts_len = None
    everyone_group = yao_person.get_groupunit(";Everyone")
    everyone_contacts_len = len(everyone_group.memberships)
    assert everyone_contacts_len == 22

    # WHEN
    yao_person.conpute()
    plan_dict = yao_person._plan_dict

    # THEN
    # print(f"{len(plan_dict)=}")
    db_plan = plan_dict.get(yao_person.make_l1_rope("D&B"))
    assert len(db_plan.awardunits) == 3
    # for plan_key in plan_dict:
    #     print(f"{plan_key=}")
    #     if plan.plan_label == "D&B":
    #         print(f"{plan.plan_label=} {plan.awardunits=}")
    #         db_awardunit_len = len(plan.awardunits)
    # assert db_awardunit_len == 3
