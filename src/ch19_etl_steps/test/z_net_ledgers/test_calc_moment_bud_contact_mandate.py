from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import count_dirs_files, create_path, open_json, save_json
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson._ref.ch09_path import (
    create_moment_json_path,
    create_moment_persons_dir_path,
)
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import create_personspark_path
from src.ch14_moment._ref.ch14_path import (
    create_bud_contact_mandate_ledger_path as bud_mandate_path,
)
from src.ch14_moment.moment_main import get_momentunit_from_dict, momentunit_shop
from src.ch14_moment.test._util.ch14_examples import example_casa_floor_clean_factunit
from src.ch18_etl_config._ref.ch18_path import (
    create_moment_mstr_path,
    create_moment_ote1_json_path,
)
from src.ch19_etl_steps.etl_main import calc_moment_bud_contact_mandate_net_ledgers
from src.ch19_etl_steps.test._util.ch19_examples import (
    get_bob_mop_reason_personunit_example,
)
from src.ref.keywords import ExampleStrs as exx


def test_calc_moment_bud_contact_mandate_net_ledgers_Scenaro0_BudEmpty(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = create_moment_mstr_path(str(temp3_fs))
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    a23_lasso = lassounit_shop(amy23_moment.moment_rope, amy23_moment.knot)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    print(f"{a23_json_path=}")
    a23_persons_path = create_moment_persons_dir_path(mstr_dir, a23_lasso)
    assert count_dirs_files(a23_persons_path) == 0

    # WHEN
    calc_moment_bud_contact_mandate_net_ledgers(mstr_dir)

    # THEN
    assert count_dirs_files(a23_persons_path) == 0


def test_calc_moment_bud_contact_mandate_net_ledgers_Scenaro1_SimpleBud(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = create_moment_mstr_path(str(temp3_fs))
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_moment.add_budunit(exx.bob, tp37, bud1_quota, celldepth=x_celldepth)
    a23_lasso = lassounit_shop(amy23_moment.moment_rope, amy23_moment.knot)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    # Create empty ote1 file
    a23_ote1_json_path = create_moment_ote1_json_path(mstr_dir, a23_lasso)
    save_json(a23_ote1_json_path, None, {})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    calc_moment_bud_contact_mandate_net_ledgers(mstr_dir)

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_contact_nets = {exx.bob: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_contact_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(exx.bob, tp37)
    assert gen_bob37_budunit.bud_contact_nets == expected_bud_contact_nets


def test_calc_moment_bud_contact_mandate_net_ledgers_Scenaro2_BudExists(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = create_moment_mstr_path(str(temp3_fs))

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    a23_lasso = lassounit_shop(amy23_moment.moment_rope, amy23_moment.knot)
    amy23_moment.add_budunit(exx.bob, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())

    # Create spark time mapping person_time_agg for time 37
    spark33 = 33
    spark44 = 44
    spark55 = 55
    bob55_personspark = get_bob_mop_reason_personunit_example()
    bob55_personspark.add_contactunit(exx.sue, 1)
    sue44_personspark = personunit_shop(exx.sue, exx.a23)
    sue44_personspark.set_person_name(exx.sue)
    sue44_personspark.add_contactunit(exx.yao, 1)
    yao44_personspark = get_bob_mop_reason_personunit_example()
    yao44_personspark.set_person_name(exx.yao)
    yao44_personspark.add_contactunit(exx.zia, 1)
    clean_fact = example_casa_floor_clean_factunit()
    yao44_personspark.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    zia33_personspark = get_bob_mop_reason_personunit_example()
    zia33_personspark.set_person_name(exx.zia)
    bob55_path = create_personspark_path(mstr_dir, a23_lasso, exx.bob, spark55)
    sue44_path = create_personspark_path(mstr_dir, a23_lasso, exx.sue, spark44)
    yao44_path = create_personspark_path(mstr_dir, a23_lasso, exx.yao, spark44)
    zia33_path = create_personspark_path(mstr_dir, a23_lasso, exx.zia, spark33)
    save_json(bob55_path, None, bob55_personspark.to_dict())
    save_json(sue44_path, None, sue44_personspark.to_dict())
    save_json(yao44_path, None, yao44_personspark.to_dict())
    save_json(zia33_path, None, zia33_personspark.to_dict())

    # Create empty ote1 file
    a23_ote1_dict = {
        exx.bob: {str(tp37): spark55},
        exx.sue: {str(tp37): spark44},
        exx.yao: {str(tp37): spark44},
        exx.zia: {str(tp37): spark33},
    }
    a23_ote1_json_path = create_moment_ote1_json_path(mstr_dir, a23_lasso)
    save_json(a23_ote1_json_path, None, a23_ote1_dict)

    # create result bud_contact_mandate_ledger file
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    calc_moment_bud_contact_mandate_net_ledgers(mstr_dir)

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_contact_nets = {exx.zia: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_contact_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(exx.bob, tp37)
    assert gen_bob37_budunit.bud_contact_nets == expected_bud_contact_nets
