from os import name as os_name
from pathlib import Path
import platform
from platform import system as platform_system
from pytest import MonkeyPatch
from src.ch21_world.world import worlddir_shop
from src.ch30_etl_app.etl_gui_tool import (
    ETLAppSettings,
    get_app_default_dir,
    get_app_default_dirs,
    get_app_default_me_personname,
    get_app_default_world_name,
    get_app_default_you_personname,
    get_app_glb_attrs,
)
import sys


def test_ETLAppSettings_Exists():
    # ESTABLISH
    x_mono = "xx_mono"
    x_bg = "xx_bg"
    x_bg_card = "xx_bg_card"
    x_border = "xx_border"
    x_accent = "xx_accent"
    x_accent_dim = "xx_accent_dim"
    x_fg = "xx_fg"
    x_fg_dim = "xx_fg_dim"
    x_fg_black = "xx_fg_black"
    x_entry_bg = "xx_entry_bg"
    x_btn_active = "xx_btn_active"
    x_platform_font = "xx_platform_font"
    # WHEN
    app_settings = ETLAppSettings(
        mono=x_mono,
        bg=x_bg,
        bg_card=x_bg_card,
        border=x_border,
        accent=x_accent,
        accent_dim=x_accent_dim,
        fg=x_fg,
        fg_dim=x_fg_dim,
        fg_black=x_fg_black,
        entry_bg=x_entry_bg,
        btn_active=x_btn_active,
        platform_font=x_platform_font,
    )
    # THEN
    assert app_settings
    assert app_settings.mono
    assert app_settings.bg
    assert app_settings.bg_card
    assert app_settings.border
    assert app_settings.accent
    assert app_settings.accent_dim
    assert app_settings.fg
    assert app_settings.fg_dim
    assert app_settings.entry_bg
    assert app_settings.btn_active


def test_get_app_glb_attrs_ReturnsObj():
    # ESTABLISH / WHEN
    app_glb_attrs = get_app_glb_attrs()

    # THEN
    assert app_glb_attrs
    assert set(app_glb_attrs.__dict__.keys()) == {
        "mono",
        "bg",
        "bg_card",
        "border",
        "accent",
        "accent_dim",
        "fg",
        "fg_dim",
        "entry_bg",
        "btn_active",
        "fg_black",
        "platform_font",
    }
    expected_platform_font = (
        ("Courier New", 17, "bold")
        if platform_system() == "Windows"
        else ("Menlo", 16, "bold")
    )
    expected_app_settings = ETLAppSettings(
        mono=("Courier New", 9) if platform_system() == "Windows" else ("Menlo", 10),
        bg="#1a1a1f",
        bg_card="#22222a",
        border="#33333d",
        accent="#e8c547",
        accent_dim="#b89a2f",
        fg="#e4e4e8",
        fg_dim="#7a7a88",
        fg_black="#0d0d10",
        entry_bg="#13131a",
        btn_active="#f0d060",
        platform_font=expected_platform_font,
    )
    assert app_glb_attrs == expected_app_settings


def test_get_app_default_me_personname_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_app_default_me_personname() == "Emmanuel"


def test_get_app_default_you_personname_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_app_default_you_personname() == "Steve"


def test_get_app_default_world_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_app_default_world_name() == "my_first_world"


# # this test is failing when github actions run it. Probably same issue: monkeypath is failing for platform
# def test_get_app_default_dir_ReturnsObj_WindowsPath(monkeypatch: MonkeyPatch):
#     # ESTABLISH
#     monkeypatch.setattr(platform, "system", lambda: "Windows")
#     # WHEN
#     path = get_app_default_dir()
#     # THEN
#     assert path == Path("C:/keg/worlds")


def test_get_app_default_dir_ReturnsObj_UnixPath(monkeypatch):
    # ESTABLISH
    fake_home = Path("/home/testuser")
    monkeypatch.setattr("src.ch30_etl_app.etl_gui_tool.Path.home", lambda: fake_home)
    # WHEN
    path = get_app_default_dir(is_windows=False)
    # THEN
    assert path == fake_home / "keg" / "worlds"


# def test_get_app_default_dir_ReturnsObj_MacosPath(monkeypatch: MonkeyPatch):
#     # ESTABLISH
#     # monkeypatch setattr for platform isn't working
#     monkeypatch.setattr(platform, "system", lambda: "darwin")
#     fake_home = Path("/Users/testuser")
#     monkeypatch.setattr(Path, "home", lambda: fake_home)
#     # WHEN
#     path = get_app_default_dir()
#     # THEN
#     assert path == fake_home / "keg" / "worlds"


def test_get_app_default_dir_ReturnsObj_Scenari0_app_default_dir():
    # ESTABLISH
    x_root_dir = get_app_default_dir()
    # WHEN
    x_default_dirs = get_app_default_dirs(x_root_dir)
    # THEN
    assert x_default_dirs
    example_world_name = get_app_default_world_name()
    default_dir = get_app_default_dir()
    example_worlddir = worlddir_shop(example_world_name, worlds_dir=default_dir)
    assert x_default_dirs == {
        "world_name": example_worlddir.world_name,
        "working": example_worlddir.worlds_dir,
        "beliefs_src": example_worlddir.beliefs_src_dir,
        "ideas_src": example_worlddir.ideas_src_dir,
        "output": example_worlddir.output_dir,
    }
