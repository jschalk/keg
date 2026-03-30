from platform import system
from pytest import mark as pytest_mark

import shutil
from pathlib import Path
from uuid import uuid4
from pyperclip import copy as pyperclip_copy
import pytest
import subprocess

_config = None


def pytest_configure(config):
    config.addinivalue_line("markers", "skip_on_linux: skip test on Linux")
    global _config
    _config = config


def pytest_collection_modifyitems(items):
    skip_linux = pytest_mark.skip(reason="conflict in file path str")
    for item in items:
        if "skip_on_linux" in item.keywords and system() == "Linux":
            item.add_marker(skip_linux)


def pytest_addoption(parser):
    parser.addoption("--graphics_bool", action="store", default=False)
    parser.addoption("--run_big_tests", action="store", default=False)
    parser.addoption("--rebuild_bool", action="store", default=False)
    parser.addoption("--clip", action="store_true", default=False)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    graphics_bool_value = metafunc.config.option.graphics_bool
    graphics_bool_value = str(graphics_bool_value).lower() == "true"
    if "graphics_bool" in metafunc.fixturenames and graphics_bool_value is not None:
        metafunc.parametrize("graphics_bool", [graphics_bool_value])
    run_big_tests_value = metafunc.config.option.run_big_tests
    run_big_tests_value = run_big_tests_value == "True"
    if "run_big_tests" in metafunc.fixturenames and run_big_tests_value is not None:
        metafunc.parametrize("run_big_tests", [run_big_tests_value])
    rebuild_bool_value = metafunc.config.option.rebuild_bool
    rebuild_bool_value = rebuild_bool_value == "True"
    if "rebuild_bool" in metafunc.fixturenames and rebuild_bool_value is not None:
        metafunc.parametrize("rebuild_bool", [rebuild_bool_value])


# Create an isolated scratch directory for every test and switch cwd into it.
# The directory is removed after the test, ensuring empty state for each test.

# TODO delete if not used
# @pytest.fixture(scope="session")
# def temp3_fs_root(tmp_path_factory):
#     root = tmp_path_factory.mktemp("temp3_fs_root")
#     yield root
#     shutil.rmtree(root, ignore_errors=True)


@pytest.fixture(scope="session")
def workspace_root():
    # project root (C:\dev\keg)
    return Path(__file__).resolve().parent


@pytest.fixture
def ws_src(workspace_root):
    return workspace_root / "src"


# TODO replace all get_temp_dir() calls with temp3_dir and delete get_temp_dir
@pytest.fixture
def temp3_dir(tmp_path):
    return tmp_path / uuid4().hex


# TODO replace all temp_dir_setup calls with temp3_dir and delete temp_dir_setup
@pytest.fixture
def temp3_fs(temp3_dir):
    # per-test isolated writable temp folder (opt-in, not autouse)
    test_dir = temp3_dir
    test_dir.mkdir()
    yield test_dir
    # defer cleanup to pytest's tmp_path cleanup instead of recursive rmtree


def pytest_runtest_logreport(report):
    if report.failed and _config.getoption("--clip"):
        test_name = report.nodeid.split("::")[-1]
        print(f"\n📋 Copied to clipboard: {test_name}")
        pyperclip_copy(test_name)
