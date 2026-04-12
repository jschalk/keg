from os import name as os_name
from pathlib import Path
from pytest import MonkeyPatch
from src.ch21_world.world import worlddir_shop
from src.ch30_etl_app.etl_gui_tool import (
    get_app_default_dir,
    get_app_default_person_name,
    get_app_default_world_name,
    get_workspace_dirs,
)
import sys


def test_get_app_default_person_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_app_default_person_name() == "Steve"


def test_get_app_default_world_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_app_default_world_name() == "my_first_world"


def test_get_app_default_dir_ReturnsObj_WindowsPath(monkeypatch: MonkeyPatch):
    # ESTABLISH
    monkeypatch.setattr(sys, "platform", "win32")
    # WHEN
    path = get_app_default_dir()
    # THEN
    assert path == Path("C:/keg/worlds")


def test_get_app_default_dir_ReturnsObj_UnixPath(monkeypatch):
    # ESTABLISH
    fake_home = Path("/home/testuser")
    monkeypatch.setattr("src.ch30_etl_app.etl_gui_tool.Path.home", lambda: fake_home)
    # WHEN
    path = get_app_default_dir(is_windows=False)
    # THEN
    assert path == fake_home / "keg" / "worlds"


def testget_app_default_dir_ReturnsObj_MacosPath(monkeypatch: MonkeyPatch):
    # ESTABLISH
    monkeypatch.setattr(sys, "platform", "darwin")
    fake_home = Path("/Users/testuser")
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # WHEN
    path = get_app_default_dir()
    # THEN
    assert path == fake_home / "keg" / "worlds"


def test_get_app_default_dir_ReturnsObj_Scenari0_app_default_dir():
    # ESTABLISH
    x_root_dir = get_app_default_dir()
    # WHEN
    x_default_dirs = get_workspace_dirs(x_root_dir)
    # THEN
    assert x_default_dirs
    example_worlddir = worlddir_shop(
        world_name=get_app_default_world_name(), worlds_dir=get_app_default_dir()
    )
    assert x_default_dirs == {
        "working": example_worlddir.worlds_dir,
        "beliefs_src": example_worlddir.beliefs_src_dir,
        "ideas_src": example_worlddir.ideas_src_dir,
        "output": example_worlddir.output_dir,
    }
