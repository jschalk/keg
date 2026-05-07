from ch00_py._ref.ch00_path import (
    create_src_example_strs_path,
    create_src_keywords_main_path,
)
from ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from ch00_py.file_toolbox import create_path, open_json, save_file
from copy import copy as copy_copy
from enum import Enum
from re import fullmatch as re_fullmatch
from typing import Any, List, Set, Tuple


def get_example_strs_config() -> dict[str, dict]:
    return open_json(create_src_example_strs_path("src"))


def get_keywords_src_config() -> dict[str, dict]:
    return open_json(create_src_keywords_main_path("src"))


def get_possible_keyword_config_keys() -> set:
    return {"valid_ch", "semantic_type", "exam_tier", "sort_ordinal"}


def parse_valid_ch_str(
    all_chapters: Set[int],
    selection_str: str,
) -> Set[int]:
    """
    Examples:
        "" -> set()
        "0:" -> all chapters from 0 upward that exist in all_chapters
        "0, 1, 98" -> {0, 1, 98}
        "3:" -> all chapters >= 3
    """
    selection_str = selection_str.strip()
    if not selection_str:
        return set()
    result: Set[int] = set()
    for part in selection_str.split(","):
        part = part.strip()

        # Range syntax: "N:"
        if part.endswith(":"):
            split_str = part[:-1].strip()
            if not split_str.isdigit():
                raise ValueError(f"Invalid range split: {part}")
            split_int = int(split_str)
            result.update(chapter for chapter in all_chapters if chapter >= split_int)
        elif part.isdigit():
            result.add(int(part))
        else:
            raise ValueError(f"Invalid chapter: {part}")
    return result


def get_keywords_by_chapter(keywords_dict: dict[str, dict[str]]) -> dict:
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {int(chapter_desc[2:4]) for chapter_desc in chapter_descs}
    chapters_keywords = {ch_int: set() for ch_int in ch_ints}
    for x_keyword, config_dict in keywords_dict.items():
        valid_ch_str = config_dict.get("valid_ch")
        keyword_valid_chs = parse_valid_ch_str(ch_ints, valid_ch_str)
        for valid_ch_int in keyword_valid_chs:
            chapter_set = chapters_keywords.get(valid_ch_int)
            chapter_set.add(x_keyword)
    return chapters_keywords


def get_cumlative_keywords_main_dict(keywords_by_chapter: dict[int, set[str]]) -> dict:
    cumlative_keywords_main_dict = {}
    for chapter_num in sorted(list(keywords_by_chapter.keys())):
        keywords_main_set = keywords_by_chapter.get(chapter_num)
        cumlative_keywords_main_dict[chapter_num] = copy_copy(keywords_main_set)
    return cumlative_keywords_main_dict


def get_chapter_keyword_classes(cumlative_keywords_main_dict: dict) -> dict[int,]:
    chXX_keyword_classes = {}
    word_str = "word"
    for chapter_int in sorted(list(cumlative_keywords_main_dict.keys())):
        keywords_main = cumlative_keywords_main_dict.get(chapter_int)
        chapter_prefix = f"Ch{chapter_int:02d}"
        class_name = f"C{chapter_prefix[1:]}Key{word_str}s"
        ExpectedClass = Enum(class_name, {t: t for t in keywords_main}, type=str)
        chXX_keyword_classes[chapter_prefix] = ExpectedClass
    return chXX_keyword_classes


def create_keywords_enum_class_file_str(chapter_prefix: str, keywords_set: set) -> str:
    keywords_str = ""
    if not keywords_set:
        keywords_str += "\n    pass"
    else:
        for keyword_str in sorted(keywords_set):
            keywords_str += f'\n    {keyword_str} = "{keyword_str}"'

    chXX_str = f"{chapter_prefix.upper()[:1]}{chapter_prefix.lower()[1:]}"
    key_str = "Key"
    dunder_str_func_str = """
    def __str__(self):
        return self.value
"""
    return f"""

class {chXX_str}{key_str}words(str, Enum):{keywords_str}
{dunder_str_func_str}"""


def create_examplestrs_class_str(example_strs_dict: dict) -> str:
    enum_attrs = ""
    for key_str in sorted(example_strs_dict.keys()):
        value_str = example_strs_dict.get(key_str)
        enum_attrs += f"""    {key_str} = "{value_str}"\n"""

    return f"""class ExampleStrs(str, Enum):
{enum_attrs}
    def __str__(self):
        return self.value"""


def create_all_enum_keyword_classes_str() -> str:
    examples_strs = get_example_strs_config()
    keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
    cumlative_keywords = get_cumlative_keywords_main_dict(keywords_by_chapter)
    import_enum_line = f"""from enum import Enum


{create_examplestrs_class_str(examples_strs)}
"""
    classes_str = copy_copy(import_enum_line)
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        ch_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_int = int(chapter_desc[2:4])
        keywords_main = cumlative_keywords.get(ch_int)
        enum_class_str = create_keywords_enum_class_file_str(ch_prefix, keywords_main)
        classes_str += enum_class_str
    return classes_str


def get_keywords_by_chapter_md() -> str:
    words_str = "words"
    keywords_title_str = f"Key{words_str} by Chapter"
    func_lines = [f"## {keywords_title_str}"]
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {int(chapter_desc[2:4]) for chapter_desc in chapter_descs}
    keywords_init_ch = {int(ch_desc[2:4]): set() for ch_desc in chapter_descs}
    keywords_init_ch["No Chapter"] = set()
    for keyword_str, kw_config in get_keywords_src_config().items():
        if ch_list := parse_valid_ch_str(ch_ints, kw_config.get("valid_ch")):
            first_ch = sorted(ch_list)[0]
            keywords_init_ch.get(first_ch).add(keyword_str)
        else:
            keywords_init_ch.get("No Chapter").add(keyword_str)

    for chapter_desc in chapter_descs:
        ch_int = int(chapter_desc[2:4])
        chapter_keywords = keywords_init_ch.get(ch_int)
        chapter_keywords = sorted(list(chapter_keywords))
        _line = f"- {chapter_desc}: " + ", ".join(chapter_keywords)
        func_lines.append(_line)
    return f"# {keywords_title_str}\n\n" + "\n".join(func_lines)


def save_keywords_by_chapter_md(x_dir: str):
    keywords_by_chapter_md_path = create_path(x_dir, "keywords_by_chapter.md")
    save_file(keywords_by_chapter_md_path, None, get_keywords_by_chapter_md())


def check_relative_order(subset: List[Any], full: List[Any]) -> Tuple[bool, str]:
    index_map = {value: i for i, value in enumerate(full)}

    try:
        subset_indices = [index_map[x] for x in subset]
    except KeyError as e:
        return False, f"Element {e.args[0]!r} not found in full list"

    for i in range(len(subset_indices) - 1):
        if subset_indices[i] > subset_indices[i + 1]:
            correct_order = sorted(subset, key=lambda x: index_map[x])
            return (False, f"Incorrect order. Expected order: {correct_order}")
    return True, ""
