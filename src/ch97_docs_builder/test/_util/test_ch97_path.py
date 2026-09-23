from ch00_py.file_toolbox import create_path, get_json_filename
from ch97_docs_builder._ref.ch97_path import (
    create_chapter_ref_path,
    create_keg_exam_questions_path,
    create_question_tier_path,
    create_src_keywords_definitions_path,
)
from inspect import getdoc as inspect_getdoc
from pytest import mark as pytest_mark


def test_create_src_keywords_definitions_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    src_dir = temp3_dir

    # WHEN
    keywords_class_file_path = create_src_keywords_definitions_path(src_dir)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ch99_glossary")
    expected_filename = get_json_filename("keywords_definitions")
    expected_file_path = create_path(ref_dir, expected_filename)
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skip_on_linux
def test_create_src_keywords_definitions_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ref_dir = create_path(src_dir, "ch99_glossary")
    doc_str = create_path(ref_dir, get_json_filename("keywords_definitions"))
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_src_keywords_definitions_path) == doc_str


def test_create_chapter_ref_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    src_dir = temp3_dir
    chapter_prefix = "ch05"

    # WHEN
    keywords_class_file_path = create_chapter_ref_path(src_dir, chapter_prefix)

    # THEN
    assert keywords_class_file_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "_ref")
    expected_filename = get_json_filename(f"{chapter_prefix}_ref")
    expected_file_path = create_path(ref_dir, expected_filename)
    assert keywords_class_file_path == expected_file_path


@pytest_mark.skip_on_linux
def test_create_chapter_ref_path_HasDocString():
    # GIVEN the expected docstring with literal src/ path
    doc_str = "Returns path: src\\chapter_dir\\_ref\\chXX_ref.json"

    # WHEN / THEN
    assert inspect_getdoc(create_chapter_ref_path) == doc_str


def test_create_keg_exam_questions_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    src_dir = temp3_dir

    # WHEN
    keg_exam_csv_path = create_keg_exam_questions_path(src_dir)

    # THEN
    assert keg_exam_csv_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ch99_glossary")
    derived_dir = create_path(ref_dir, "derived")
    expected_filename = "keg_exam_questions.csv"
    expected_file_path = create_path(derived_dir, expected_filename)
    print(f"{expected_file_path=}")
    print(f"{keg_exam_csv_path=}")
    assert keg_exam_csv_path == expected_file_path


@pytest_mark.skip_on_linux
def test_create_keg_exam_questions_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ch99_dir = create_path(src_dir, "ch99_glossary")
    derived_dir = create_path(ch99_dir, "derived")
    doc_str = create_path(derived_dir, "keg_exam_questions.csv")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keg_exam_questions_path) == doc_str


def test_create_question_tier_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    src_dir = temp3_dir

    # WHEN
    keg_exam_csv_path = create_question_tier_path(src_dir)

    # THEN
    assert keg_exam_csv_path
    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ch99_glossary")
    derived_dir = create_path(ref_dir, "derived")
    expected_filename = "question_tier.csv"
    expected_file_path = create_path(derived_dir, expected_filename)
    print(f"{expected_file_path=}")
    print(f"{keg_exam_csv_path=}")
    assert keg_exam_csv_path == expected_file_path


@pytest_mark.skip_on_linux
def test_create_question_tier_path_HasDocString():
    # ESTABLISH
    src_dir = "src"
    ch99_dir = create_path(src_dir, "ch99_glossary")
    derived_dir = create_path(ch99_dir, "derived")
    doc_str = create_path(derived_dir, "question_tier.csv")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_question_tier_path) == doc_str
