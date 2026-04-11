from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, save_file
from src.ch21_world.world import WorldDir, WorldName, worlddir_shop
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


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
    assert not x_wdir.world_dir
    assert not x_wdir.ideas_src_dir
    assert not x_wdir.beliefs_src_dir
    assert not x_wdir.db_path
    assert not x_wdir.moment_mstr_dir
    assert set(x_wdir.__dict__.keys()) == {
        kw.world_name,
        "worlds_dir",
        "output_dir",
        "world_dir",
        "beliefs_src_dir",
        "ideas_src_dir",
        "db_path",
        kw.moment_mstr_dir,
    }


def test_WorldDir_set_ideas_src_dir_SetsDirsAndFiles(temp3_fs):
    # ESTABLISH
    fay_wdir = WorldDir("Fay")
    x_example_dir = create_path(str(temp3_fs), "example_dir")
    x_ideas_src_dir = create_path(x_example_dir, kw.i_src)
    assert not fay_wdir.world_dir
    assert not fay_wdir.ideas_src_dir
    assert not fay_wdir.beliefs_src_dir
    assert not fay_wdir.db_path
    assert not fay_wdir.moment_mstr_dir
    assert os_path_exists(x_ideas_src_dir) is False

    # WHEN
    fay_wdir.set_ideas_src_dir(x_ideas_src_dir)

    # THEN
    assert not fay_wdir.world_dir
    assert fay_wdir.ideas_src_dir == x_ideas_src_dir
    assert not fay_wdir.beliefs_src_dir
    assert not fay_wdir.db_path
    assert not fay_wdir.moment_mstr_dir
    assert os_path_exists(x_ideas_src_dir)


def test_WorldDir_set_beliefs_src_dir_SetsDirsAndFiles(temp3_fs):
    # ESTABLISH
    fay_wdir = WorldDir("Fay")
    x_example_dir = create_path(str(temp3_fs), "example_dir")
    x_ideas_src_dir = create_path(x_example_dir, kw.i_src)
    x_beliefs_src_dir = create_path(x_example_dir, kw.b_src)
    assert not fay_wdir.world_dir
    assert not fay_wdir.ideas_src_dir
    assert not fay_wdir.beliefs_src_dir
    assert not fay_wdir.moment_mstr_dir
    assert os_path_exists(x_ideas_src_dir) is False

    # WHEN
    fay_wdir.set_beliefs_src_dir(x_beliefs_src_dir)

    # THEN
    assert not fay_wdir.world_dir
    assert not fay_wdir.ideas_src_dir
    assert fay_wdir.beliefs_src_dir == x_beliefs_src_dir
    assert not fay_wdir.moment_mstr_dir
    assert os_path_exists(x_beliefs_src_dir)


def test_WorldDir_set_world_dirs_SetsDirsAndFiles(temp3_fs):
    # ESTABLISH
    fay_str = "Fay"
    fay_wdir = WorldDir(world_name=fay_str, worlds_dir=str(temp3_fs))
    x_world_dir = create_path(str(temp3_fs), fay_str)
    x_ideas_src_dir = create_path(x_world_dir, kw.i_src)
    x_beliefs_src_dir = create_path(x_world_dir, kw.b_src)
    x_moment_mstr_dir = create_path(x_world_dir, "moment_mstr")

    assert not fay_wdir.world_dir
    assert not fay_wdir.ideas_src_dir
    assert not fay_wdir.beliefs_src_dir
    assert not fay_wdir.moment_mstr_dir
    assert os_path_exists(x_world_dir) is False
    assert os_path_exists(x_ideas_src_dir) is False
    assert os_path_exists(x_beliefs_src_dir) is False
    assert os_path_exists(x_moment_mstr_dir) is False

    # WHEN
    fay_wdir._set_world_dirs()

    # THEN
    assert fay_wdir.world_dir == x_world_dir
    assert not fay_wdir.ideas_src_dir
    assert os_path_exists(x_world_dir)
    assert os_path_exists(x_ideas_src_dir) is False
    assert os_path_exists(x_beliefs_src_dir) is False
    assert os_path_exists(x_moment_mstr_dir)


def test_worlddir_shop_ReturnsObj_Scenario0_WithParameters(temp3_fs):
    # ESTABLISH
    worlds2_dir = create_path(str(temp3_fs), "worlds2")
    example_ideas_src_dir = create_path(str(temp3_fs), "example_ideas_src_dir")
    example_beliefs_src_dir = create_path(str(temp3_fs), "example_beliefs_src_dir")
    output_dir = create_path(str(temp3_fs), "output")
    five_world_name = "five"

    # WHEN
    x_wdir = worlddir_shop(
        world_name=five_world_name,
        worlds_dir=worlds2_dir,
        output_dir=output_dir,
        ideas_src_dir=example_ideas_src_dir,
        beliefs_src_dir=example_beliefs_src_dir,
    )

    # THEN
    assert x_wdir.world_name == five_world_name
    assert x_wdir.worlds_dir == worlds2_dir
    assert x_wdir.output_dir == output_dir
    assert x_wdir.ideas_src_dir == example_ideas_src_dir
    assert x_wdir.beliefs_src_dir == example_beliefs_src_dir
    world_db_path = create_path(x_wdir.world_dir, "world.db")
    assert x_wdir.db_path == world_db_path


def test_worlddir_shop_ReturnsObj_Scenario1_WithoutParameters(temp3_fs):
    # ESTABLISH

    # WHEN
    x_wdir = worlddir_shop(exx.a23, str(temp3_fs))

    # THEN
    assert x_wdir.world_name == exx.a23
    assert x_wdir.worlds_dir == str(temp3_fs)
    assert not x_wdir.output_dir
    assert x_wdir.ideas_src_dir == create_path(x_wdir.world_dir, kw.i_src)
    assert x_wdir.beliefs_src_dir == create_path(x_wdir.world_dir, kw.b_src)
    assert x_wdir.db_path == create_path(x_wdir.world_dir, "world.db")


def test_worlddir_shop_ReturnsObj_Scenario2_ThirdParameterIs_output_dir(
    temp3_fs,
):
    # ESTABLISH
    output_dir = create_path(str(temp3_fs), "output")

    # WHEN
    x_wdir = worlddir_shop(exx.a23, str(temp3_fs), output_dir)

    # THEN
    assert x_wdir.world_name == exx.a23
    assert x_wdir.worlds_dir == str(temp3_fs)
    assert x_wdir.output_dir == output_dir


def test_WorldDir_get_world_db_path_ReturnsObj(temp3_fs):
    # ESTABLISH
    a23_wdir = worlddir_shop(exx.a23, str(temp3_fs))

    # WHEN
    a23_db_path = a23_wdir.get_world_db_path()

    # THEN
    assert a23_db_path == create_path(a23_wdir.world_dir, "world.db")


def test_WorldDir_delete_world_db_DeletesFile(temp3_fs):
    # ESTABLISH
    a23_wdir = worlddir_shop(exx.a23, str(temp3_fs))
    a23_db_path = a23_wdir.get_world_db_path()
    print(f"{a23_db_path=}")
    save_file(a23_db_path, None, "example_text")
    assert os_path_exists(a23_db_path)

    # WHEN
    a23_wdir.delete_world_db()

    # THEN
    assert not os_path_exists(a23_db_path)
