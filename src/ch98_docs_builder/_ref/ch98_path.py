from src.ch00_py.file_toolbox import create_path


def create_src_keg_definitions_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keg_definitions.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keg_definitions.json")


def create_src_keg_exam_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keg_exam.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keg_exam.json")


def create_chapter_ref_path(chapter_dir: str, chapter_prefix: str) -> str:
    """Returns path: src\\chapter_dir\\_ref\\chXX_ref.json"""

    ref_dir = create_path(chapter_dir, "_ref")
    return create_path(ref_dir, f"{chapter_prefix}_ref.json")
