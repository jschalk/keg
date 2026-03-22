from src.ch00_py.file_toolbox import create_path, save_file
from src.linter.style import (
    env_file_has_required_elements,
    filename_style_is_correct,
    function_name_style_is_correct,
    get_filenames_with_wrong_style,
)
from src.linter.test._util.linter_env import get_temp_dir, temp_dir_setup


def test_filename_style_is_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert filename_style_is_correct("get_label.py")
    assert not filename_style_is_correct("get_labelN.py")
    assert not filename_style_is_correct("get_labels.py")
    assert filename_style_is_correct("get_labels.md")
    assert filename_style_is_correct("get_labelN.md")
    assert not filename_style_is_correct("fidels_MOM_IS_WHAT.py")


def test_filenames_style_arg_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_filenames_with_wrong_style({"get_label.py"}) == set()
    assert len(get_filenames_with_wrong_style({"get_labelN.py"})) == 1
    assert len(get_filenames_with_wrong_style({"get_labels.py"})) == 1
    assert get_filenames_with_wrong_style({"get_label.py", "style.json"}) == set()
    assert len(get_filenames_with_wrong_style({"get_label.py", "styles.py"})) == 1


def test_function_name_style_is_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert function_name_style_is_correct("get_label")
    assert not function_name_style_is_correct("get_label_No")
    assert function_name_style_is_correct("get_label_None")
    assert not function_name_style_is_correct("Get_label")
    assert not function_name_style_is_correct("test_get_label")
    assert function_name_style_is_correct("test_get_label_ReturnsObj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj_scenari")
    assert not function_name_style_is_correct("test_get_label_ReturnObj_scenario")
    assert not function_name_style_is_correct("test_GetLabel_exists")
    assert function_name_style_is_correct("test_GetLabel_Exists")
    assert not function_name_style_is_correct("test_get_label_Returnsobj")
    assert not function_name_style_is_correct("test_get_label_returnsobj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj")
    assert not function_name_style_is_correct("test_get_label_ReturnObj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj_correctly")


def test_env_file_has_required_elements_ReturnsObj_Scenario0(temp_dir_setup):
    # ESTBALISH

    ch04_prefix = "ch04"
    env4_filename = f"{ch04_prefix}_env.py"
    env4_file_str = """
def get_temp_dir():
    pass

@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(dir=env_dir)

"""
    env4_file_path = create_path(get_temp_dir(), env4_filename)
    save_file(env4_file_path, None, env4_file_str)

    # WHEN / THEN
    assert env_file_has_required_elements(env4_file_path)


def test_env_file_has_required_elements_ReturnsObj_Scenario1(temp_dir_setup):
    # ESTBALISH

    ch04_prefix = "ch04"
    env4_filename = f"{ch04_prefix}_env.py"
    env4_file_str = """

@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(dir=env_dir)

"""
    env4_file_path = create_path(get_temp_dir(), env4_filename)
    save_file(env4_file_path, None, env4_file_str)

    # WHEN / THEN
    assert not env_file_has_required_elements(env4_file_path)


def test_env_file_has_required_elements_ReturnsObj_Scenario2(temp_dir_setup):
    # ESTBALISH

    ch04_prefix = "ch04"
    env4_filename = f"{ch04_prefix}_env.py"
    env4_file_str = """
def get_temp_dir():
    pass


"""
    env4_file_path = create_path(get_temp_dir(), env4_filename)
    save_file(env4_file_path, None, env4_file_str)

    # WHEN / THEN
    assert not env_file_has_required_elements(env4_file_path)


def test_env_file_has_required_elements_ReturnsObj_Scenario3(temp_dir_setup):
    # ESTBALISH

    ch04_prefix = "ch04"
    env4_filename = f"{ch04_prefix}_env.py"
    env4_file_str = """

def get_temp_dir():
    pass

    
@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(env_dir)

"""
    env4_file_path = create_path(get_temp_dir(), env4_filename)
    save_file(env4_file_path, None, env4_file_str)

    # WHEN / THEN
    assert not env_file_has_required_elements(env4_file_path)
