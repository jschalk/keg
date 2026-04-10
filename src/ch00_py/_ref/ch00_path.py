from src.ch00_py.file_toolbox import create_path


def create_src_example_strs_path(src_dir: str) -> str:
    """Returns path: src\\ref\\example_strs.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "example_strs.json")


def create_src_ch_keywords_path(src_dir: str) -> str:
    """Returns path: src\\ref\\ch_keywords.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "ch_keywords.json")


def create_keywords_classes_file_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keywords.py"""

    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keywords.py")
