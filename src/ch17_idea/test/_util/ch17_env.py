from os import makedirs as os_makedirs
from pytest import fixture as pytest_fixture
from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.file_toolbox import create_path, delete_dir
from typing import Any, Generator


@pytest_fixture
def cursor0() -> Generator[Cursor, Any, None]:
    with sqlite3_connect(":memory:") as db_conn:
        yield db_conn.cursor()
