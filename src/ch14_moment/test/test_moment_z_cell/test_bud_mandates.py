from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import open_json, save_json
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import (
    create_cell_partner_mandate_ledger_path as cell_mandate_path,
)
from src.ch11_bud.bud_main import tranbook_shop
from src.ch14_moment._ref.ch14_path import (
    create_bud_partner_mandate_ledger_path as bud_mandate_path,
)
from src.ch14_moment.moment_cell import create_bud_mandate_ledgers
from src.ch14_moment.moment_main import get_momentunit_from_dict, momentunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_create_bud_mandate_ledgers_Scenaro0_BudEmpty(temp3_fs):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    timenum9 = 9
    bob9_bud_mandate_path = bud_mandate_path(mstr_dir, a23_lasso, exx.bob, timenum9)
    assert os_path_exists(bob9_bud_mandate_path) is False

    # WHEN
    create_bud_mandate_ledgers(mstr_dir, a23_lasso)

    # THEN
    assert os_path_exists(bob9_bud_mandate_path) is False


def test_create_bud_mandate_ledgers_Scenaro1_BudExists(temp3_fs):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    tp37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(exx.bob, tp37, bud1_quota)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    bob37_cell_mandate_path = cell_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37)
    bob_mandate = 777
    assert bud1_quota != bob_mandate
    save_json(bob37_cell_mandate_path, None, {exx.bob: bob_mandate})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False
    bob37_budunit = amy23_moment.get_budunit(exx.bob, tp37)
    assert bob37_budunit.bud_partner_nets == {}

    # WHEN
    create_bud_mandate_ledgers(mstr_dir, a23_lasso)

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_partner_nets = {exx.bob: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_partner_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_a23_momentunit.set_all_tranbook()
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(exx.bob, tp37)
    assert gen_bob37_budunit.bud_partner_nets == expected_bud_partner_nets
    expected_a23_all_tranbook = tranbook_shop(exx.a23)
    expected_a23_all_tranbook.add_tranunit(exx.bob, exx.bob, tp37, 450)
    assert gen_a23_momentunit.all_tranbook == expected_a23_all_tranbook


def test_create_bud_mandate_ledgers_Scenaro2_Mutliple_cell_partner_mandate_ledgers(
    temp3_fs,
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    tp37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(exx.bob, tp37, bud1_quota)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    b37_cell_mandate = cell_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37)
    b37_sue_cell_path = cell_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37, [exx.sue])
    b37_yao_cell_path = cell_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37, [exx.yao])
    yz_anc = [exx.yao, exx.zia]
    b37_yao_zia_cell_path = cell_mandate_path(
        mstr_dir, a23_lasso, exx.bob, tp37, yz_anc
    )
    save_json(b37_cell_mandate, None, {exx.sue: 1, exx.yao: 3})
    save_json(b37_sue_cell_path, None, {exx.zia: 1, exx.sue: 3})
    save_json(b37_yao_cell_path, None, {exx.zia: 1, exx.yao: 3})
    save_json(b37_yao_zia_cell_path, None, {exx.xio: 1})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_lasso, exx.bob, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False
    bob37_budunit = amy23_moment.get_budunit(exx.bob, tp37)
    assert bob37_budunit.bud_partner_nets == {}

    # WHEN
    create_bud_mandate_ledgers(mstr_dir, a23_lasso)

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_partner_nets = {
        exx.yao: 254,
        exx.xio: 84,
        exx.sue: 84,
        exx.zia: 28,
    }
    print(f"{open_json(bob37_bud_mandate_path)=}")
    assert open_json(bob37_bud_mandate_path) == expected_bud_partner_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(exx.bob, tp37)
    assert gen_bob37_budunit.bud_partner_nets == expected_bud_partner_nets
    expected_a23_all_tranbook = tranbook_shop(exx.a23)
    expected_a23_all_tranbook.add_tranunit(exx.bob, exx.sue, tp37, 84)
    expected_a23_all_tranbook.add_tranunit(exx.bob, exx.xio, tp37, 84)
    expected_a23_all_tranbook.add_tranunit(exx.bob, exx.zia, tp37, 28)
    expected_a23_all_tranbook.add_tranunit(exx.bob, exx.yao, tp37, 254)
    gen_a23_momentunit.set_all_tranbook()
    gen_all_tranbook = gen_a23_momentunit.all_tranbook
    assert gen_all_tranbook.tranunits == expected_a23_all_tranbook.tranunits
