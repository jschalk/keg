from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import open_json
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import create_cell_json_path, create_personspark_path
from src.ch11_bud.bud_filehandler import (
    cellunit_add_json_file,
    save_arbitrary_personspark,
)
from src.ch14_moment.moment_cell import load_cells_personspark
from src.ch14_moment.test._util.ch14_examples import example_casa_floor_clean_factunit
from src.ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_load_cells_personspark_SetsFiles_Scenario0_NoFacts(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    spark300 = 300
    time5 = 5
    save_arbitrary_personspark(moment_mstr_dir, a23_lasso, exx.bob, spark300)
    bob3_personspark_path = create_personspark_path(
        moment_mstr_dir, a23_lasso, exx.bob, spark300
    )
    print(f"{bob3_personspark_path=}")
    cellunit_add_json_file(moment_mstr_dir, a23_lasso, exx.bob, time5, spark300, [])
    bob5_cell_path = create_cell_json_path(moment_mstr_dir, a23_lasso, exx.bob, time5)
    assert open_json(bob5_cell_path).get(kw.personspark_facts) == {}

    # WHEN
    load_cells_personspark(moment_mstr_dir, a23_lasso)

    # THEN
    assert os_path_exists(bob5_cell_path)
    assert open_json(bob5_cell_path).get(kw.personspark_facts) == {}


def test_load_cells_personspark_SetsFiles_Scenario1_WithFacts(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    spark300 = 300
    time5 = 5
    clean_fact = example_casa_floor_clean_factunit()
    x_facts = [clean_fact.get_tuple()]
    save_arbitrary_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark300, facts=x_facts
    )
    bob3_personspark_path = create_personspark_path(
        moment_mstr_dir, a23_lasso, exx.bob, spark300
    )
    print(f"{bob3_personspark_path=}")
    cellunit_add_json_file(moment_mstr_dir, a23_lasso, exx.bob, time5, spark300, [])
    bob5_cell_path = create_cell_json_path(moment_mstr_dir, a23_lasso, exx.bob, time5)
    assert open_json(bob5_cell_path).get(kw.personspark_facts) == {}

    # WHEN
    load_cells_personspark(moment_mstr_dir, a23_lasso)

    # THEN
    expected_personspark_facts = {clean_fact.fact_context: clean_fact.to_dict()}
    assert (
        open_json(bob5_cell_path).get(kw.personspark_facts)
        == expected_personspark_facts
    )


def test_load_cells_personspark_SetsFiles_Scenario2_WithFacts_NotAtRoot(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    spark300 = 300
    time5 = 5
    clean_fact = example_casa_floor_clean_factunit()
    x_facts = [(clean_fact.fact_context, clean_fact.fact_state, None, None)]
    save_arbitrary_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark300, facts=x_facts
    )
    das = [exx.yao, exx.bob]
    cellunit_add_json_file(moment_mstr_dir, a23_lasso, exx.bob, time5, spark300, das)
    bob5_cell_path = create_cell_json_path(
        moment_mstr_dir, a23_lasso, exx.bob, time5, das
    )
    assert open_json(bob5_cell_path).get(kw.personspark_facts) == {}

    # WHEN
    load_cells_personspark(moment_mstr_dir, a23_lasso)

    # THEN
    expected_personspark_facts = {clean_fact.fact_context: clean_fact.to_dict()}
    assert (
        open_json(bob5_cell_path).get(kw.personspark_facts)
        == expected_personspark_facts
    )
