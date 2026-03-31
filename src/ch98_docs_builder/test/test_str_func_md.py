from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch00_py.keyword_class_builder import (
    get_keywords_by_chapter_md,
    save_keywords_by_chapter_md,
)


def test_get_keywords_by_chapter_md_SetsFile_CheckMarkdownHasAllStrFunctions():
    # ESTABLISH / WHEN
    keywords_by_chapter_md = get_keywords_by_chapter_md()

    # THEN
    print(keywords_by_chapter_md)
    assert keywords_by_chapter_md.find("words by Chapter") > 0
    ch09_person_lesson_index = keywords_by_chapter_md.find("ch09_person_lesson")
    assert ch09_person_lesson_index > 0
    spark_num_index = keywords_by_chapter_md.find("spark_num")
    assert spark_num_index > 0
    assert ch09_person_lesson_index < spark_num_index


def test_save_keywords_by_chapter_md_SavesFile_get_keywords_by_chapter_md_ToGivenDirectory(
    temp3_fs,
):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    keywords_by_chapter_md_path = create_path(temp_dir, "keywords_by_chapter.md")
    assert not os_path_exists(keywords_by_chapter_md_path)

    # WHEN
    keywords_by_chapter_md = save_keywords_by_chapter_md(temp_dir)

    # THEN
    assert os_path_exists(keywords_by_chapter_md_path)
    keywords_by_chapter_md = get_keywords_by_chapter_md()
    assert open_file(keywords_by_chapter_md_path) == keywords_by_chapter_md
