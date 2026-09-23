from ch00_py.file_toolbox import create_path


def create_src_keywords_definitions_path(src_dir: str) -> str:
    """Returns path: src\\ch99_glossary\\keywords_definitions.json"""

    ref_dir = create_path(src_dir, "ch99_glossary")
    return create_path(ref_dir, "keywords_definitions.json")


def create_keg_exam_questions_path(src_dir: str) -> str:
    """Returns path: src\\ch99_glossary\\derived\\keg_exam_questions.csv"""

    ch99_dir = create_path(src_dir, "ch99_glossary")
    derived_dir = create_path(ch99_dir, "derived")
    return create_path(derived_dir, "keg_exam_questions.csv")


def create_question_tier_path(src_dir: str) -> str:
    """Returns path: src\\ch99_glossary\\derived\\question_tier.csv"""

    ch99_dir = create_path(src_dir, "ch99_glossary")
    derived_dir = create_path(ch99_dir, "derived")
    return create_path(derived_dir, "question_tier.csv")


def create_chapter_ref_path(chapter_dir: str, chapter_prefix: str) -> str:
    """Returns path: src\\chapter_dir\\_ref\\chXX_ref.json"""

    ref_dir = create_path(chapter_dir, "_ref")
    return create_path(ref_dir, f"{chapter_prefix}_ref.json")
