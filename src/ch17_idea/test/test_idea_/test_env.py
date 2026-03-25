from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from src.ch17_idea.test._util.ch17_env import (
    get_temp_dir,
    idea_moments_dir,
    src_chapter_dir,
)


def test_get_temp_dir_ReturnsObj():
    # ESTABLISH
    test_dir = create_path(src_chapter_dir(), "test")
    util_dir = create_path(test_dir, "_util")

    # WHEN / THEN
    assert get_temp_dir() == create_path(util_dir, "idea_examples")


def test_idea_moments_dir_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    moment_mstr_dir = create_path(get_temp_dir(), "moment_mstr")
    assert idea_moments_dir() == create_moments_dir_path(moment_mstr_dir)
