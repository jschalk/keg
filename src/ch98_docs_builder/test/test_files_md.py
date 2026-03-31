from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import count_dirs_files, create_path, open_file
from src.ch04_rope._ref.ch04_doc_builder import get_ropeterm_description_md
from src.ch98_docs_builder.doc_builder import (
    get_chapter_blurbs_md,
    save_brick_formats_md,
    save_chapter_blurbs_md,
    save_idea_brick_mds,
    save_ropeterm_description_md,
)
from src.ref.keywords import Ch98Keywords as kw


def test_get_chapter_blurbs_md_ReturnsObj():
    # ESTABLISH / WHEN
    chapter_blurbs_md = get_chapter_blurbs_md()

    # THEN
    assert chapter_blurbs_md
    assert chapter_blurbs_md.find("ch02") > 0


def test_save_chapter_blurbs_md_CreatesFile(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    chapter_blurbs_path = create_path(temp_dir, "chapter_blurbs.md")
    assert not os_path_exists(chapter_blurbs_path)

    # WHEN
    save_chapter_blurbs_md(temp_dir)

    # THEN
    assert os_path_exists(chapter_blurbs_path)
    expected_chapter_blurbs_md = get_chapter_blurbs_md()
    assert open_file(chapter_blurbs_path) == expected_chapter_blurbs_md


def test_save_ropeterm_description_md_CreatesFile(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    file_path = create_path(temp_dir, "ropeterm_explanation.md")
    assert not os_path_exists(file_path)

    # WHEN
    save_ropeterm_description_md(temp_dir)

    # THEN
    assert os_path_exists(file_path)
    assert open_file(file_path) == get_ropeterm_description_md()


def test_save_idea_brick_mds_CreatesFiles(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    assert count_dirs_files(temp_dir) == 0

    # WHEN
    save_idea_brick_mds(temp_dir)

    # THEN
    assert count_dirs_files(temp_dir) == 42


def test_save_idea_brick_formats_CreatesFile(temp3_fs):
    # ESTABLISH
    doc_main_dir = str(temp3_fs)
    idea_brick_formats_path = create_path(doc_main_dir, "idea_brick_formats.md")
    assert not os_path_exists(idea_brick_formats_path)

    # WHEN
    save_brick_formats_md(doc_main_dir)

    # THEN
    assert os_path_exists(idea_brick_formats_path)
    idea_brick_formats_md = open_file(idea_brick_formats_path)
    assert idea_brick_formats_md.find("br00004") > 0
