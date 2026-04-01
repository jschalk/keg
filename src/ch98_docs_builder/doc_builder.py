from ast import (
    ClassDef as ast_ClassDef,
    FunctionDef as ast_FunctionDef,
    Name as ast_Name,
    parse as ast_parse,
    walk as ast_walk,
)
from src.ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from src.ch00_py.file_toolbox import (
    create_path,
    get_dir_filenames,
    open_json,
    save_file,
    save_json,
)
from src.ch00_py.keyword_class_builder import (
    create_src_example_strs_path,
    create_src_keywords_main_path,
)
from src.ch04_rope._ref.ch04_doc_builder import get_ropeterm_description_md
from src.ch17_idea._ref.ch17_doc_builder import get_brick_formats_md, get_idea_brick_mds
from src.ch98_docs_builder._ref.ch98_path import create_chapter_ref_path
from src.ch98_docs_builder.keg_terminology_builder import (
    rebuild_keg_terminology_contents,
)


def get_func_names_and_class_bases_from_file(
    file_path: str, suffix: str = None
) -> tuple[list, dict[str, bool]]:
    """
    Parses a Python file and returns a list of all top-level function names.

    :param file_path: Path to the .py file
    :return: List of function names, dict key: Class Name, value: list of class bases
    """

    with open(file_path, "r", encoding="utf-8") as file:
        node = ast_parse(file.read(), filename=file_path)
    file_funcs = []
    class_bases = {}
    for n in ast_walk(node):
        if isinstance(n, ast_FunctionDef):
            file_funcs.append(n.name)
        if isinstance(n, ast_ClassDef):
            bases = [b.id for b in n.bases if isinstance(b, ast_Name)]
            class_bases[n.name] = bases
    return file_funcs, class_bases


def get_chapter_blurbs_md() -> str:
    lines = ["# Chapter Overview\n", "What does each one do?\n", ""]
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_ref_path = create_chapter_ref_path(chapter_dir, chapter_prefix)
        chapter_ref_dict = open_json(chapter_ref_path)
        chapter_description_str = "chapter_description"
        chapter_blurb_str = "chapter_blurb"
        mod_blurb = chapter_ref_dict.get(chapter_blurb_str)
        ref_chapter_desc = chapter_ref_dict.get(chapter_description_str)

        lines.append(f"- **{ref_chapter_desc}**: {mod_blurb}")

    return "\n".join(lines)


def save_chapter_blurbs_md(x_dir: str):
    save_file(x_dir, "chapter_blurbs.md", get_chapter_blurbs_md())


def save_ropeterm_description_md(x_dir: str):
    save_file(x_dir, "ropeterm_breakdown.md", get_ropeterm_description_md())


def save_idea_brick_mds(dest_dir: str):
    idea_brick_mds = get_idea_brick_mds()
    dest_dir = create_path(dest_dir, "ch17_brick_formats")

    for idea_number, idea_brick_md in idea_brick_mds.items():
        save_file(dest_dir, f"{idea_number}.md", idea_brick_md)


def save_brick_formats_md(dest_dir: str):
    brick_formats_md = get_brick_formats_md()
    save_file(dest_dir, "brick_formats.md", brick_formats_md)


def resave_chapter_and_keyword_json_files():
    for chapter_dir in get_chapter_descs().values():
        json_file_tuples = get_dir_filenames(chapter_dir, {"json"})
        for x_dir, x_filename in json_file_tuples:
            json_dir = create_path(chapter_dir, x_dir)
            save_json(json_dir, x_filename, open_json(json_dir, x_filename))
    keywords_main_json_path = create_src_keywords_main_path("src")
    ex_strs_json_path = create_src_example_strs_path("src")
    save_json(keywords_main_json_path, None, open_json(keywords_main_json_path))
    save_json(ex_strs_json_path, None, open_json(ex_strs_json_path))
    rebuild_keg_terminology_contents()
