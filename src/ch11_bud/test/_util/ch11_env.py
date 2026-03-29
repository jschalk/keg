from os import makedirs as os_makedirs
from pytest import fixture as pytest_fixture
from src.ch00_py.file_toolbox import delete_dir


def get_temp_dir():
    return "src\\ch11_bud\\test\\_util\\temp"


# TODO move all temp_dir_setup to conftest.py
# replace delete_dir with context manager that yields temp dir path, and deletes after use
# if os_path_exists(dir):
#     if os_path_isdir(dir):
#         shutil_rmtree(path=dir)
#     elif os_path_isfile(dir):
#         os_remove(dir)


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
