from os import makedirs as os_makedirs
from pytest import fixture as pytest_fixture
from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.file_toolbox import delete_dir
from typing import Any, Generator


def get_temp_dir():
    return "src\\ch19_etl_main\\test\\_util\\etls"


@pytest_fixture()
def temp_dir_setup():
    env_dir = get_temp_dir()
    delete_dir(dir=env_dir)
    os_makedirs(env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


@pytest_fixture
def cursor0() -> Generator[Cursor, Any, None]:
    with sqlite3_connect(":memory:") as db_conn:
        yield db_conn.cursor()
