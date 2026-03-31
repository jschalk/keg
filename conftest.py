from platform import system
from pytest import mark as pytest_mark
from sqlite3 import Cursor, connect as sqlite3_connect
from typing import Any, Generator
from pathlib import Path
from uuid import uuid4
from pyperclip import copy as pyperclip_copy
import pytest
import subprocess
import shutil


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


@pytest.fixture
def temp3_dir(tmp_path):
    return tmp_path / uuid4().hex


@pytest.fixture
def temp3_fs(temp3_dir):
    """Temporary filesystem for a test, created in pytest's tmp_path. Yields the path to the temp directory."""
    # per-test isolated writable temp folder (opt-in, not autouse)
    test_dir = temp3_dir
    test_dir.mkdir()
    yield test_dir
    # defer cleanup to pytest's tmp_path cleanup instead of recursive rmtree


@pytest.fixture
def cursor0() -> Generator[Cursor, Any, None]:
    """Provides a SQLite cursor connected to an in-memory database."""
    with sqlite3_connect(":memory:") as db_conn:
        yield db_conn.cursor()


def pytest_runtest_logreport(report):
    """Called after each test phase (setup, call, teardown). If the test failed and --clip is set, copies the test name to clipboard."""
    if report.failed and _config.getoption("--clip"):
        test_name = report.nodeid.split("::")[-1]
        print(f"\n📋 Copied to clipboard: {test_name}")
        pyperclip_copy(test_name)
