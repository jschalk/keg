from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import reasonunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import get_sorted_plan_list, personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from src.ch07_person_logic.tree_metric import TreeMetrics, treemetrics_shop
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_TreeMetrics_Exists():
    # ESTABLISH / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count is None
    assert x_tree_metrics.tree_level_count is None
    assert x_tree_metrics.reason_contexts is None
    assert x_tree_metrics.awardunits_metrics is None
    assert x_tree_metrics.plan_uid_max is None
    assert x_tree_metrics.plan_uid_dict is None
    assert x_tree_metrics.all_plan_plan_uids_are_unique is None


def test_treemetrics_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics is not None
    assert x_tree_metrics.label_count == 0
    assert x_tree_metrics.tree_level_count == {}
    assert x_tree_metrics.reason_contexts == {}
    assert x_tree_metrics.awardunits_metrics == {}
    assert x_tree_metrics.plan_uid_max == 0
    assert x_tree_metrics.plan_uid_dict == {}
    assert x_tree_metrics.all_plan_plan_uids_are_unique

    # # could create tests for these methods?
    # def evaluate_label(
    # def evaluate_pledge(self, pledge: bool, plan_rope: RopeTerm):
    # def evaluate_level(self, tree_level):
    # def evaluate_reasonunits(self, reasons: dict[RopeTerm, ReasonUnit]):
    # def evaluate_awardunits(self, awardunits: dict[GroupTitle, AwardUnit]):
    # def evaluate_plan_uid_max(self, plan_uid):


def test_PersonUnit_set_plan_dict_Scenario0():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    root_rope = yao_person.planroot.get_plan_rope()
    root_plan = yao_person.get_plan_obj(root_rope)
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert yao_person._plan_dict == {}
    assert yao_person.reason_contexts == set()

    # WHEN
    yao_person._set_plan_dict()

    # THEN
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert yao_person._plan_dict == {root_plan.get_plan_rope(): root_plan}
    assert yao_person.reason_contexts == set()


def test_PersonUnit_set_plan_dict_Scenario1():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    ziet0_begin = 7
    ziet0_close = 31
    root_rope = yao_person.planroot.get_plan_rope()
    yao_person.edit_plan_attr(root_rope, begin=ziet0_begin, close=ziet0_close)
    root_rope = yao_person.planroot.get_plan_rope()
    root_plan = yao_person.get_plan_obj(root_rope)
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_person._set_plan_dict()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc


def test_PersonUnit_set_plan_dict_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    root_rope = sue_person.planroot.get_plan_rope()
    root_plan = sue_person.get_plan_obj(root_rope)
    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_person.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = sue_person.make_rope(usa_rope, texas_str)
    texas_plan = sue_person.get_plan_obj(texas_rope)
    texas_plan.gogo_calc = 7
    texas_plan.stop_calc = 11
    texas_plan.range_evaluated = True
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert texas_plan.range_evaluated
    assert texas_plan.gogo_calc
    assert texas_plan.stop_calc

    # WHEN
    sue_person._set_plan_dict()

    # THEN
    assert not root_plan.begin
    assert not root_plan.close
    assert not texas_plan.range_evaluated
    assert not texas_plan.gogo_calc
    assert not texas_plan.stop_calc


def test_PersonUnit_set_plan_dict_Sets_reason_contexts():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    polis_str = "polis"
    polis_rope = sue_person.make_l1_rope(polis_str)
    sue_person.add_plan(polis_rope)
    sue_person.add_plan(nation_rope)
    sue_person.edit_plan_attr(
        nation_rope, reason_context=polis_rope, reason_case=polis_rope
    )
    nation_plan = sue_person.get_plan_obj(nation_rope)
    assert nation_plan.reason_context_reasonunit_exists(polis_rope)
    assert sue_person.reason_contexts == set()

    # WHEN
    sue_person._set_plan_dict()

    # THEN
    assert sue_person.reason_contexts == {polis_rope}


def test_PersonUnit_set_plan_CreatesPlanUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope("casa")
    cleaning_rope = sue_person.make_rope(casa_rope, "cleaning")
    clean_cuisine_str = "clean_cuisine"
    clean_cuisine_plan = planunit_shop(clean_cuisine_str, star=40, pledge=True)

    buildings_str = "buildings"
    buildings_rope = sue_person.make_l1_rope(buildings_str)
    cuisine_room_str = "cuisine"
    cuisine_room_rope = sue_person.make_rope(buildings_rope, cuisine_room_str)
    cuisine_dirty_str = "dirty"
    cuisine_dirty_rope = sue_person.make_rope(cuisine_room_rope, cuisine_dirty_str)
    cuisine_reasonunit = reasonunit_shop(reason_context=cuisine_room_rope)
    cuisine_reasonunit.set_case(case=cuisine_dirty_rope)
    clean_cuisine_plan.set_reasonunit(cuisine_reasonunit)

    assert sue_person.plan_exists(buildings_rope) is False

    # WHEN
    sue_person.set_plan_obj(
        clean_cuisine_plan, cleaning_rope, create_missing_plans=True
    )

    # THEN
    assert sue_person.plan_exists(buildings_rope)


def test_get_sorted_plan_list_ReturnsObj_Scenario0_DefaultOrder_plan_plan_rope():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels()
    casa_rope = sue_person.make_l1_rope("casa")
    cat_rope = sue_person.make_l1_rope("cat have dinner")
    wk_rope = sue_person.make_l1_rope("sem_jours")
    sun_rope = sue_person.make_rope(wk_rope, "Sun")
    mon_rope = sue_person.make_rope(wk_rope, "Mon")
    tue_rope = sue_person.make_rope(wk_rope, "Tue")
    wed_rope = sue_person.make_rope(wk_rope, "Wed")
    thu_rope = sue_person.make_rope(wk_rope, "Thur")
    fri_rope = sue_person.make_rope(wk_rope, "Fri")
    sat_rope = sue_person.make_rope(wk_rope, "Sat")
    nation_rope = sue_person.make_l1_rope("nation")
    usa_rope = sue_person.make_rope(nation_rope, "USA")
    france_rope = sue_person.make_rope(nation_rope, "France")
    brazil_rope = sue_person.make_rope(nation_rope, "Brazil")
    texas_rope = sue_person.make_rope(usa_rope, "Texas")
    oregon_rope = sue_person.make_rope(usa_rope, "Oregon")
    sue_person._set_plan_dict()

    # WHEN
    x_sorted_plan_list = get_sorted_plan_list(sue_person._plan_dict)

    # THEN
    assert x_sorted_plan_list is not None
    assert len(x_sorted_plan_list) == 17
    assert x_sorted_plan_list[0] == sue_person.planroot
    assert x_sorted_plan_list[1] == sue_person.get_plan_obj(casa_rope)
    assert x_sorted_plan_list[11] == sue_person.get_plan_obj(mon_rope)


def test_get_sorted_plan_list_ReturnsObj_Scenario1_SortBy_fund_ratio():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    sem_jours_rope = sue_person.make_l1_rope("sem_jours")
    sun_plan = planunit_shop("Sun", parent_rope=sem_jours_rope)
    mon_plan = planunit_shop("Mon", parent_rope=sem_jours_rope)
    tue_plan = planunit_shop("Tue", parent_rope=sem_jours_rope)
    wed_plan = planunit_shop("Wed", parent_rope=sem_jours_rope)
    thu_plan = planunit_shop("Thur", parent_rope=sem_jours_rope)
    fri_plan = planunit_shop("Fri", parent_rope=sem_jours_rope)
    sat_plan = planunit_shop("Sat", parent_rope=sem_jours_rope)
    sun_plan.fund_ratio = 0.33
    mon_plan.fund_ratio = 0.033
    tue_plan.fund_ratio = 0.0033
    thu_plan.fund_ratio = 0.0022
    wed_plan.fund_ratio = 0.00033
    fri_plan.fund_ratio = 0.0000044
    sat_plan.fund_ratio = 0.00000055
    example_dict = {
        sun_plan.get_plan_rope(): sun_plan,
        mon_plan.get_plan_rope(): mon_plan,
        tue_plan.get_plan_rope(): tue_plan,
        wed_plan.get_plan_rope(): wed_plan,
        thu_plan.get_plan_rope(): thu_plan,
        fri_plan.get_plan_rope(): fri_plan,
        sat_plan.get_plan_rope(): sat_plan,
    }

    # WHEN
    x_sorted_plan_list = get_sorted_plan_list(example_dict, sorting_key=kw.fund_ratio)

    # THEN
    assert x_sorted_plan_list is not None
    assert len(x_sorted_plan_list) == 7
    assert x_sorted_plan_list[0] == sun_plan
    assert x_sorted_plan_list[1] == mon_plan
    assert x_sorted_plan_list[2] == tue_plan
    assert x_sorted_plan_list[3] == thu_plan
    assert x_sorted_plan_list[4] == wed_plan
    assert x_sorted_plan_list[5] == fri_plan
    assert x_sorted_plan_list[6] == sat_plan


def test_get_sorted_plan_list_ReturnsObj_Scenario2_2ndSortBy_plan_rope():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    sem_jours_rope = sue_person.make_l1_rope("sem_jours")
    sun_plan = planunit_shop("Sun", parent_rope=sem_jours_rope)
    mon_plan = planunit_shop("Mon", parent_rope=sem_jours_rope)
    sun_plan.fund_ratio = 0.25
    mon_plan.fund_ratio = 0.25
    example_dict = {
        sun_plan.get_plan_rope(): sun_plan,
        mon_plan.get_plan_rope(): mon_plan,
    }

    # WHEN
    x_sorted_plan_list = get_sorted_plan_list(example_dict, sorting_key=kw.fund_ratio)

    # THEN
    assert x_sorted_plan_list is not None
    assert len(x_sorted_plan_list) == 2
    assert x_sorted_plan_list[0] == mon_plan
    assert x_sorted_plan_list[1] == sun_plan
