from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch01_allot.allot import allot_nested_scale
from src.ref.keywords import ExampleStrs as exx


def test_allot_nested_scale_ReturnsObj_Scenari0_depth0(
    temp3_fs,
):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    x_filename = "ledger.json"
    save_json(x_dir, x_filename, root_ledger)
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=0,
    )

    # THEN
    assert nested_allot_scale == {exx.bob: 40, exx.sue: 160}


def test_allot_nested_scale_ReturnsObj_Scenari1_depth0_NestedFilesExist(
    temp3_fs,
):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    bob_ledger = {exx.sue: 1, exx.yao: 1}
    sue_ledger = {exx.sue: 1, exx.yao: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, exx.bob)
    sue_dir = create_path(x_dir, exx.sue)
    save_json(x_dir, x_filename, root_ledger)
    save_json(bob_dir, x_filename, bob_ledger)
    save_json(sue_dir, x_filename, sue_ledger)
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=0,
    )

    # THEN
    assert nested_allot_scale == {exx.bob: 40, exx.sue: 160}


def test_allot_nested_scale_ReturnsObj_Scenari2_depth1_NestedFilesExist(
    temp3_fs,
):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    bob_ledger = {exx.sue: 1, exx.yao: 1}
    sue_ledger = {exx.sue: 1, exx.yao: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, exx.bob)
    sue_dir = create_path(x_dir, exx.sue)
    save_json(x_dir, x_filename, root_ledger)
    save_json(bob_dir, x_filename, bob_ledger)
    save_json(sue_dir, x_filename, sue_ledger)
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=1,
    )

    # THEN
    assert set(nested_allot_scale.keys()) == {exx.sue, exx.yao}
    print(set(nested_allot_scale.keys()))
    assert nested_allot_scale == {exx.sue: 60, exx.yao: 140}


def test_allot_nested_scale_ReturnsObj_Scenari3_depth1_NoNestedFiles(
    temp3_fs,
):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    x_filename = "ledger.json"
    save_json(x_dir, x_filename, root_ledger)
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=0,
    )

    # THEN
    assert nested_allot_scale == {exx.bob: 40, exx.sue: 160}


def test_allot_nested_scale_ReturnsObj_Scenari4_depth1_NestedFilesExist(
    temp3_fs,
):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    bob_ledger = {exx.sue: 1, exx.yao: 1}
    sue_ledger = {exx.sue: 1, exx.yao: 3}
    sue_yao_ledger = {exx.sue: 1, exx.yao: 1, exx.xio: 3}
    bob_yao_ledger = {exx.sue: 1, exx.yao: 1, exx.zia: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, exx.bob)
    sue_dir = create_path(x_dir, exx.sue)
    bob_yao_dir = create_path(bob_dir, exx.yao)
    sue_yao_dir = create_path(sue_dir, exx.yao)
    save_json(x_dir, x_filename, root_ledger)
    save_json(bob_dir, x_filename, bob_ledger)
    save_json(sue_dir, x_filename, sue_ledger)
    save_json(bob_yao_dir, x_filename, bob_yao_ledger)
    save_json(sue_yao_dir, x_filename, sue_yao_ledger)
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=3,
    )

    # THEN
    assert set(nested_allot_scale.keys()) == {exx.sue, exx.yao, exx.xio, exx.zia}
    print(set(nested_allot_scale.keys()))
    assert nested_allot_scale == {exx.sue: 88, exx.yao: 28, exx.xio: 72, exx.zia: 12}


def test_allot_nested_scale_SetsFiles_Scenario0(temp3_fs):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    bob_ledger = {exx.sue: 1, exx.yao: 1}
    sue_ledger = {exx.sue: 1, exx.yao: 3}
    sue_yao_ledger = {exx.sue: 1, exx.yao: 1, exx.xio: 3}
    bob_yao_ledger = {exx.sue: 1, exx.yao: 1, exx.zia: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, exx.bob)
    sue_dir = create_path(x_dir, exx.sue)
    bob_yao_dir = create_path(bob_dir, exx.yao)
    sue_yao_dir = create_path(sue_dir, exx.yao)
    save_json(x_dir, x_filename, root_ledger)
    save_json(bob_dir, x_filename, bob_ledger)
    save_json(sue_dir, x_filename, sue_ledger)
    save_json(bob_yao_dir, x_filename, bob_yao_ledger)
    save_json(sue_yao_dir, x_filename, sue_yao_ledger)
    x_scale = 200
    x_grain = 1
    alloted_filename = "alloted.json"
    x_alloted_path = create_path(x_dir, alloted_filename)
    bob_alloted_path = create_path(bob_dir, alloted_filename)
    sue_alloted_path = create_path(sue_dir, alloted_filename)
    bob_yao_alloted_path = create_path(bob_yao_dir, alloted_filename)
    sue_yao_alloted_path = create_path(sue_yao_dir, alloted_filename)
    assert os_path_exists(x_alloted_path) is False
    assert os_path_exists(bob_alloted_path) is False
    assert os_path_exists(sue_alloted_path) is False
    assert os_path_exists(bob_yao_alloted_path) is False
    assert os_path_exists(sue_yao_alloted_path) is False

    # WHEN
    allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=3,
    )

    # THEN
    assert os_path_exists(x_alloted_path)
    assert os_path_exists(bob_alloted_path)
    assert os_path_exists(sue_alloted_path)
    assert os_path_exists(bob_yao_alloted_path)
    assert os_path_exists(sue_yao_alloted_path)
    x_alloted_dict = open_json(x_alloted_path)
    bob_alloted_dict = open_json(bob_alloted_path)
    sue_alloted_dict = open_json(sue_alloted_path)
    bob_yao_alloted_dict = open_json(bob_yao_alloted_path)
    sue_yao_alloted_dict = open_json(sue_yao_alloted_path)
    assert x_alloted_dict == {exx.sue: 160, exx.bob: 40}
    assert bob_alloted_dict == {exx.sue: 20, exx.yao: 20}
    assert sue_alloted_dict == {exx.sue: 40, exx.yao: 120}
    assert bob_yao_alloted_dict == {exx.sue: 4, exx.yao: 4, exx.zia: 12}
    assert sue_yao_alloted_dict == {exx.sue: 24, exx.yao: 24, exx.xio: 72}


def test_allot_nested_scale_SetsFiles_Scenario1_Custom_dst_filename(
    temp3_fs,
):
    # ESTABLISH
    x_dir = str(temp3_fs)
    root_ledger = {exx.bob: 10, exx.sue: 40}
    bob_ledger = {exx.sue: 1, exx.yao: 1}
    sue_ledger = {exx.sue: 1, exx.yao: 3}
    sue_yao_ledger = {exx.sue: 1, exx.yao: 1, exx.xio: 3}
    bob_yao_ledger = {exx.sue: 1, exx.yao: 1, exx.zia: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, exx.bob)
    sue_dir = create_path(x_dir, exx.sue)
    bob_yao_dir = create_path(bob_dir, exx.yao)
    sue_yao_dir = create_path(sue_dir, exx.yao)
    save_json(x_dir, x_filename, root_ledger)
    save_json(bob_dir, x_filename, bob_ledger)
    save_json(sue_dir, x_filename, sue_ledger)
    save_json(bob_yao_dir, x_filename, bob_yao_ledger)
    save_json(sue_yao_dir, x_filename, sue_yao_ledger)
    x_scale = 200
    x_grain = 1
    dst_filename = "dst_alloted.json"
    x_dst_path = create_path(x_dir, dst_filename)
    bob_dest_path = create_path(bob_dir, dst_filename)
    sue_dst_path = create_path(sue_dir, dst_filename)
    bob_yao_dst_path = create_path(bob_yao_dir, dst_filename)
    sue_yao_dst_path = create_path(sue_yao_dir, dst_filename)
    assert os_path_exists(x_dst_path) is False
    assert os_path_exists(bob_dest_path) is False
    assert os_path_exists(sue_dst_path) is False
    assert os_path_exists(bob_yao_dst_path) is False
    assert os_path_exists(sue_yao_dst_path) is False

    # WHEN
    allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=3,
        dst_filename=dst_filename,
    )

    # THEN
    assert os_path_exists(x_dst_path)
    assert os_path_exists(bob_dest_path)
    assert os_path_exists(sue_dst_path)
    assert os_path_exists(bob_yao_dst_path)
    assert os_path_exists(sue_yao_dst_path)
    assert open_json(x_dst_path) == {exx.sue: 160, exx.bob: 40}
    assert open_json(bob_dest_path) == {exx.sue: 20, exx.yao: 20}
    assert open_json(sue_dst_path) == {exx.sue: 40, exx.yao: 120}
    assert open_json(bob_yao_dst_path) == {exx.sue: 4, exx.yao: 4, exx.zia: 12}
    assert open_json(sue_yao_dst_path) == {exx.sue: 24, exx.yao: 24, exx.xio: 72}
