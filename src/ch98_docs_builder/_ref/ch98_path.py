from src.ch00_py.file_toolbox import create_path


def create_src_keg_terminology_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keg_terminology.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keg_terminology.json")


def create_chapter_ref_path(chapter_dir: str, chapter_prefix: str) -> str:
    """Returns path: src\\chapter_dir\\_ref\\chXX_ref.json"""

    ref_dir = create_path(chapter_dir, "_ref")
    return create_path(ref_dir, f"{chapter_prefix}_ref.json")
