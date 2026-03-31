from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import (
    create_cell_dir_path as cell_dir,
    create_cell_json_path as node_path,
)
from src.ch11_bud.bud_filehandler import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    save_arbitrary_personspark as save_personspark,
)
from src.ch11_bud.cell_main import cellunit_shop
from src.ch14_moment.moment_cell import create_cell_tree
from src.ref.keywords import ExampleStrs as exx


def test_create_cell_tree_Scenaro0_timenum_Empty(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = create_path(str(temp3_fs), "Fay_mstr")
    tp37 = 37
    a23_lasso = lassounit_shop(exx.a23)
    a23_bob_tp37_path = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    print(f"{a23_bob_tp37_path=}")
    assert os_path_exists(a23_bob_tp37_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_lasso, exx.bob, tp37)

    # THEN
    assert os_path_exists(a23_bob_tp37_path) is False


def test_create_cell_tree_Scenaro1_LedgerDepth0(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = create_path(str(temp3_fs), "Fay_mstr")
    tp37 = 37  # timenum
    bud1_quota = 450
    bud1_celldepth = 0
    spark56 = 56
    a23_lasso = lassounit_shop(exx.a23)
    x_cell = cellunit_shop(exx.bob, [], spark56, bud1_celldepth, quota=bud1_quota)
    bob37_root_cell_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    cellunit_save_to_dir(bob37_root_cell_dir, x_cell)
    save_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark56, [[exx.yao], [exx.bob]]
    )
    assert (
        cellunit_get_from_dir(bob37_root_cell_dir).get_personsparks_quota_ledger() == {}
    )

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_lasso, exx.bob, tp37)

    # THEN
    bob37_root_cell = cellunit_get_from_dir(bob37_root_cell_dir)
    generated_bob37_quota_ledger = bob37_root_cell.get_personsparks_quota_ledger()
    assert generated_bob37_quota_ledger == {"Bob": 225, exx.yao: 225}


def test_create_cell_tree_Scenaro2_LedgerDepth1(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = create_path(str(temp3_fs), "Fay_mstr")
    tp37 = 37  # timenum
    x_quota = 450
    x_celldepth = 1
    spark56 = 56
    a23_lasso = lassounit_shop(exx.a23)
    x_cell = cellunit_shop(exx.bob, [], spark56, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_partners = [[exx.yao], [exx.bob], [exx.zia]]
    yao_partners = [[exx.zia]]
    zia_partners = [[exx.bob], [exx.yao]]
    bob_e56_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark56, bob_partners
    )
    yao_e56_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark56, yao_partners
    )
    zia_e56_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.zia, spark56, zia_partners
    )
    assert os_path_exists(bob_e56_path)
    assert os_path_exists(yao_e56_path)
    assert os_path_exists(zia_e56_path)
    bob37_node_path = node_path(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    bob37_bob_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob]
    )
    bob37_yao_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao]
    )
    bob37_zia_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia]
    )
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False
    assert cellunit_get_from_dir(bob37_dir).get_personsparks_quota_ledger() == {}

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_lasso, exx.bob, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao])
    bob37_zia_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    assert bob37_cell.ancestors == []
    assert bob37_cell.spark_num == 56
    assert bob37_cell.celldepth == 1
    assert bob37_cell.bud_person_name == exx.bob
    assert bob37_cell.mana_grain == 1
    assert bob37_cell.quota == 450
    assert bob37_bob_cell.ancestors == [exx.bob]
    assert bob37_bob_cell.spark_num == 56
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_person_name == exx.bob
    assert bob37_bob_cell.mana_grain == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [exx.yao]
    assert bob37_yao_cell.spark_num == 56
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_person_name == exx.bob
    assert bob37_yao_cell.mana_grain == 1
    assert bob37_yao_cell.quota == 150
    assert bob37_zia_cell.ancestors == [exx.zia]
    assert bob37_zia_cell.spark_num == 56
    assert bob37_zia_cell.celldepth == 0
    assert bob37_zia_cell.bud_person_name == exx.bob
    assert bob37_zia_cell.mana_grain == 1
    assert bob37_zia_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_personsparks_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_personsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_personsparks_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_personsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {exx.bob: 150, exx.yao: 150, exx.zia: 150}
    assert gen_bob37_bob_quota_ledger == {exx.bob: 50, exx.yao: 50, exx.zia: 50}
    assert gen_bob37_yao_quota_ledger == {exx.zia: 150}
    assert gen_bob37_zia_quota_ledger == {exx.bob: 75, exx.yao: 75}


def test_create_cell_tree_Scenaro3_LedgerDepth1_MostRecentSpark(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = create_path(str(temp3_fs), "Fay_mstr")
    a23_lasso = lassounit_shop(exx.a23)
    tp37 = 37  # timenum
    x_quota = 450
    x_celldepth = 1
    spark33 = 33
    spark44 = 44
    spark55 = 55
    x_cell = cellunit_shop(exx.bob, [], spark55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_partners = [[exx.yao], [exx.bob], [exx.zia]]
    yao_partners = [[exx.zia]]
    zia_partners = [[exx.bob], [exx.yao]]
    bob_e55_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark55, bob_partners
    )
    yao_e44_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark44, yao_partners
    )
    yao_e33_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark33, yao_partners
    )
    zia_e33_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.zia, spark33, zia_partners
    )
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    a23_lasso = lassounit_shop(exx.a23)
    bob37_node_path = node_path(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    bob37_bob_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob]
    )
    bob37_yao_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao]
    )
    bob37_zia_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia]
    )
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_lasso, exx.bob, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao])
    bob37_zia_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    assert bob37_cell.ancestors == []
    assert bob37_cell.spark_num == 55
    assert bob37_cell.celldepth == 1
    assert bob37_cell.bud_person_name == exx.bob
    assert bob37_cell.mana_grain == 1
    assert bob37_cell.quota == 450
    assert bob37_bob_cell.ancestors == [exx.bob]
    assert bob37_bob_cell.spark_num == 55
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_person_name == exx.bob
    assert bob37_bob_cell.mana_grain == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [exx.yao]
    assert bob37_yao_cell.spark_num == 44
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_person_name == exx.bob
    assert bob37_yao_cell.mana_grain == 1
    assert bob37_yao_cell.quota == 150
    assert bob37_zia_cell.ancestors == [exx.zia]
    assert bob37_zia_cell.spark_num == 33
    assert bob37_zia_cell.celldepth == 0
    assert bob37_zia_cell.bud_person_name == exx.bob
    assert bob37_zia_cell.mana_grain == 1
    assert bob37_zia_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_personsparks_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_personsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_personsparks_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_personsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {exx.bob: 150, exx.yao: 150, exx.zia: 150}
    assert gen_bob37_bob_quota_ledger == {exx.bob: 50, exx.yao: 50, exx.zia: 50}
    assert gen_bob37_yao_quota_ledger == {exx.zia: 150}
    assert gen_bob37_zia_quota_ledger == {exx.bob: 75, exx.yao: 75}


def test_create_cell_tree_Scenaro4_LedgerDepth1_OnePersonHasNoPast_personspark(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = create_path(str(temp3_fs), "Fay_mstr")
    tp37 = 37  # timenum
    x_quota = 450
    x_celldepth = 1
    spark33 = 33
    spark44 = 44
    spark55 = 55
    spark66 = 66
    a23_lasso = lassounit_shop(exx.a23)
    x_cell = cellunit_shop(exx.bob, [], spark55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_partners = [[exx.yao], [exx.bob], [exx.zia]]
    yao_partners = [[exx.zia]]
    zia_partners = [[exx.bob], [exx.yao]]
    bob_e55_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark55, bob_partners
    )
    yao_e44_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark44, yao_partners
    )
    yao_e33_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark33, yao_partners
    )
    zia_e66_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.zia, spark66, zia_partners
    )
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e66_path)
    bob37_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    bob37_node_path = node_path(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    bob37_bob_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob]
    )
    bob37_yao_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao]
    )
    bob37_zia_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia]
    )
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_lasso, exx.bob, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path) is False
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    assert bob37_bob_cell.ancestors == [exx.bob]
    assert bob37_bob_cell.spark_num == 55
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_person_name == exx.bob
    assert bob37_bob_cell.mana_grain == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [exx.yao]
    assert bob37_yao_cell.spark_num == 44
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_person_name == exx.bob
    assert bob37_yao_cell.mana_grain == 1
    assert bob37_yao_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_personsparks_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_personsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_personsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {exx.bob: 150, exx.yao: 150, exx.zia: 150}
    assert gen_bob37_bob_quota_ledger == {exx.bob: 50, exx.yao: 50, exx.zia: 50}
    assert gen_bob37_yao_quota_ledger == {exx.zia: 150}


def test_create_cell_tree_Scenaro5_LedgerDepth1_ZeroQuotaDoesNotGetCreated(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = create_path(str(temp3_fs), "Fay_mstr")
    a23_lasso = lassounit_shop(exx.a23)
    tp37 = 37  # timenum
    x_quota = 2
    x_celldepth = 1
    spark33 = 33
    spark44 = 44
    spark55 = 55
    x_cell = cellunit_shop(exx.bob, [], spark55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_partners = [[exx.yao], [exx.bob], [exx.zia]]
    yao_partners = [[exx.zia]]
    zia_partners = [[exx.bob], [exx.yao]]
    bob_e55_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.bob, spark55, bob_partners
    )
    yao_e44_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark44, yao_partners
    )
    yao_e33_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.yao, spark33, yao_partners
    )
    zia_e33_path = save_personspark(
        moment_mstr_dir, a23_lasso, exx.zia, spark33, zia_partners
    )
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    a23_lasso = lassounit_shop(exx.a23)
    bob37_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    bob37_node_path = node_path(moment_mstr_dir, a23_lasso, exx.bob, tp37, [])
    bob37_bob_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob]
    )
    bob37_yao_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao]
    )
    bob37_zia_node_path = node_path(
        moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia]
    )
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_lasso, exx.bob, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.bob])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao])
    bob37_zia_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, tp37, [exx.zia])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    gen_bob37_quota_ledger = bob37_cell.get_personsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_personsparks_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_personsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {exx.bob: 0, exx.yao: 1, exx.zia: 1}
    assert gen_bob37_yao_quota_ledger == {exx.zia: 1}
    assert gen_bob37_zia_quota_ledger == {exx.bob: 1, exx.yao: 0}
