from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, save_file
from src.ch20_world_apex.test._util.ch20_env import (
    get_temp_dir as worlds_dir,
    temp_dir_setup,
)
from src.ch20_world_apex.world import WorldDir, WorldName, worlddir_shop
from src.ref.keywords import ExampleStrs as exx


def test_WorldName_Exists():
    # ESTABLISH / WHEN / THEN
    assert WorldName() == ""
    assert WorldName("cuisine") == "cuisine"


def test_WorldDir_Exists():
    # ESTABLISH / WHEN
    x_wdir = WorldDir()

    # THEN
    assert not x_wdir.world_name
    assert not x_wdir.worlds_dir
    assert not x_wdir.output_dir
    assert not x_wdir._world_dir
    assert not x_wdir._input_dir
    assert not x_wdir._brick_dir
    assert not x_wdir._moment_mstr_dir


def test_WorldDir_set_input_dir_SetsDirsAndFiles(temp_dir_setup):
    # ESTABLISH
    fay_wdir = WorldDir("Fay")
    x_example_dir = create_path(worlds_dir(), "example_dir")
    x_input_dir = create_path(x_example_dir, "input")

    assert not fay_wdir._world_dir
    assert not fay_wdir._input_dir
    assert not fay_wdir._brick_dir
    assert not fay_wdir._moment_mstr_dir
    assert os_path_exists(x_input_dir) is False

    # WHEN
    fay_wdir.set_input_dir(x_input_dir)

    # THEN
    assert not fay_wdir._world_dir
    assert fay_wdir._input_dir == x_input_dir
    assert not fay_wdir._brick_dir
    assert not fay_wdir._moment_mstr_dir
    assert os_path_exists(x_input_dir)


def test_WorldDir_set_world_dirs_SetsDirsAndFiles(temp_dir_setup):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = WorldDir(world_name=fay_str, worlds_dir=worlds_dir())
    x_world_dir = create_path(worlds_dir(), fay_str)
    x_input_dir = create_path(x_world_dir, "input")
    x_brick_dir = create_path(x_world_dir, "brick")
    x_moment_mstr_dir = create_path(x_world_dir, "moment_mstr")

    assert not fay_wdir._world_dir
    assert not fay_wdir._input_dir
    assert not fay_wdir._brick_dir
    assert not fay_wdir._moment_mstr_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_input_dir) is False
    assert os_path_exists(x_brick_dir) is False
    assert os_path_exists(x_moment_mstr_dir) is False

    # WHEN
    fay_wdir._set_world_dirs()

    # THEN
    assert fay_wdir._world_dir == x_world_dir
    assert not fay_wdir._input_dir
    assert fay_wdir._brick_dir == x_brick_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_input_dir) is False
    assert os_path_exists(x_brick_dir)
    assert os_path_exists(x_moment_mstr_dir)


def test_worlddir_shop_ReturnsObj_Scenario0_WithParameters(temp_dir_setup):
    # ESTABLISH
    worlds2_dir = create_path(worlds_dir(), "worlds2")
    example_input_dir = create_path(worlds_dir(), "example_input")
    output_dir = create_path(worlds_dir(), "output")
    five_world_name = "five"

    # WHEN
    x_wdir = worlddir_shop(
        world_name=five_world_name,
        worlds_dir=worlds2_dir,
        output_dir=output_dir,
        input_dir=example_input_dir,
    )

    # THEN
    assert x_wdir.world_name == five_world_name
    assert x_wdir.worlds_dir == worlds2_dir
    assert x_wdir.output_dir == output_dir
    assert x_wdir._input_dir == example_input_dir


def test_worlddir_shop_ReturnsObj_Scenario1_WithoutParameters(temp_dir_setup):
    # ESTABLISH

    # WHEN
    x_wdir = worlddir_shop(exx.a23, worlds_dir())

    # THEN
    assert x_wdir.world_name == exx.a23
    assert x_wdir.worlds_dir == worlds_dir()
    assert not x_wdir.output_dir
    assert x_wdir._input_dir == create_path(x_wdir._world_dir, "input")


def test_worlddir_shop_ReturnsObj_Scenario2_ThirdParameterIs_output_dir(
    temp_dir_setup,
):
    # ESTABLISH
    output_dir = create_path(worlds_dir(), "output")

    # WHEN
    x_wdir = worlddir_shop(exx.a23, worlds_dir(), output_dir)

    # THEN
    assert x_wdir.world_name == exx.a23
    assert x_wdir.worlds_dir == worlds_dir()
    assert x_wdir.output_dir == output_dir


def test_WorldDir_get_world_db_path_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    a23_wdir = worlddir_shop(exx.a23, worlds_dir())

    # WHEN
    a23_db_path = a23_wdir.get_world_db_path()

    # THEN
    assert a23_db_path == create_path(a23_wdir._world_dir, "world.db")


def test_WorldDir_delete_world_db_DeletesFile(temp_dir_setup):
    # ESTABLISH
    a23_wdir = worlddir_shop(exx.a23, worlds_dir())
    a23_db_path = a23_wdir.get_world_db_path()
    print(f"{a23_db_path=}")
    save_file(a23_db_path, None, "example_text")
    assert os_path_exists(a23_db_path)

    # WHEN
    a23_wdir.delete_world_db()

    # THEN
    assert not os_path_exists(a23_db_path)
