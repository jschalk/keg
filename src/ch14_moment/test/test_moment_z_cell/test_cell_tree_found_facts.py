from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.lasso import lassounit_shop
from ch11_bud._ref.ch11_path import create_cell_dir_path as cell_dir
from ch11_bud.bud_filehandler import cellunit_get_from_dir, cellunit_save_to_dir
from ch11_bud.cell_main import cellunit_shop
from ch14_moment.moment_cell import set_cell_trees_found_facts
from ch14_moment.test._util.ch14_examples import example_casa_floor_clean_factunit
from ref.keywords import ExampleStrs as exx


def test_set_cell_trees_found_facts_Scenario0_RootOnly_NoFacts(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    time5 = 5
    das = []
    bob5_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, time5, das)
    bob5_cell = cellunit_shop(exx.bob, personspark_facts={})
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    assert bob5_cell.get_personsparks_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(moment_mstr_dir, a23_lasso)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}


def test_set_cell_trees_found_facts_Scenario1_ChildNode_NoFacts(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    time5 = 5
    das = []
    das_y = [exx.yao]
    das_ys = [exx.yao, exx.sue]
    bob5_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_ys)
    cellunit_save_to_dir(bob5_dir, cellunit_shop(exx.bob, das))
    cellunit_save_to_dir(bob5_yao_dir, cellunit_shop(exx.bob, das_y))
    cellunit_save_to_dir(bob5_yao_sue_dir, cellunit_shop(exx.bob, das_ys))
    cellunit_get_from_dir(bob5_dir).get_personsparks_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_dir).get_personsparks_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_sue_dir).get_personsparks_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(mstr_dir, a23_lasso)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}


def test_set_cell_trees_found_facts_Scenario2_ChildNodeWithOneFactIsAssignedToAncestors(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    time5 = 5
    clean_fact = example_casa_floor_clean_factunit()
    das = []
    das_y = [exx.yao]
    das_ys = [exx.yao, exx.sue]
    bob5_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_ys)
    bob5_personspark = personunit_shop(exx.bob, exx.a23)
    bob5_yao_personspark = personunit_shop(exx.yao, exx.a23)
    bob5_yao_sue_personspark = personunit_shop(exx.sue, exx.a23)
    bob5_personspark.add_contactunit(exx.yao)
    bob5_yao_personspark.add_contactunit(exx.sue)
    bob5_yao_sue_personspark.add_contactunit(exx.bob)
    bob5_yao_sue_personspark.add_plan(clean_fact.fact_state, 1)
    bob5_yao_sue_personspark.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    bob5_cell = cellunit_shop(exx.bob, das, personadjust=bob5_personspark)
    bob5_yao_cell = cellunit_shop(exx.bob, das_y, personadjust=bob5_yao_personspark)
    clean_facts = {clean_fact.fact_context: clean_fact}
    bob5_yao_sue_cell = cellunit_shop(
        exx.bob,
        das_ys,
        personadjust=bob5_yao_sue_personspark,
        personspark_facts=clean_facts,
    )
    assert bob5_cell.get_personsparks_quota_ledger() == {exx.yao: 1000}
    assert bob5_yao_cell.get_personsparks_quota_ledger() == {exx.sue: 1000}
    assert bob5_yao_sue_cell.get_personsparks_quota_ledger() == {exx.bob: 1000}
    assert bob5_cell.personspark_facts == {}
    assert bob5_yao_cell.personspark_facts == {}
    assert bob5_yao_sue_cell.personspark_facts == clean_facts
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    cellunit_save_to_dir(bob5_yao_dir, bob5_yao_cell)
    cellunit_save_to_dir(bob5_yao_sue_dir, bob5_yao_sue_cell)
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == {}
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(mstr_dir, a23_lasso)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == clean_facts
