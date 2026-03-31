from copy import copy as copy_copy
from enum import Enum
from re import fullmatch as re_fullmatch
from src.ch00_py._ref.ch00_path import (
    create_src_example_strs_path,
    create_src_keywords_main_path,
)
from src.ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from src.ch00_py.file_toolbox import create_path, open_json, save_file


def get_example_strs_config() -> dict[str, dict]:
    return open_json(create_src_example_strs_path("src"))


def get_keywords_src_config() -> dict[str, dict]:
    return open_json(create_src_keywords_main_path("src"))


def get_keywords_by_chapter(keywords_dict: dict[str, dict[str]]) -> dict:
    chapter_descs = get_chapter_descs().keys()
    chapters_keywords = {get_chapter_desc_prefix(chxx): set() for chxx in chapter_descs}
    for x_keyword, ref_dict in keywords_dict.items():
        keyworld_init_chapter_num = ref_dict.get("init_chapter")
        if bool(re_fullmatch(r"ch\d{2}", keyworld_init_chapter_num)):
            chapter_set = chapters_keywords.get(keyworld_init_chapter_num)
            chapter_set.add(x_keyword)
    return chapters_keywords


def get_cumlative_ch_keywords_dict(keywords_by_chapter: dict[int, set[str]]) -> dict:
    allowed_keywords_set = set()
    cumlative_ch_keywords_dict = {}
    for chapter_num in sorted(list(keywords_by_chapter.keys())):
        ch_keywords_set = keywords_by_chapter.get(chapter_num)
        allowed_keywords_set.update(ch_keywords_set)
        cumlative_ch_keywords_dict[chapter_num] = copy_copy(allowed_keywords_set)
    return cumlative_ch_keywords_dict


def get_chapter_keyword_classes(cumlative_ch_keywords_dict: dict) -> dict[int,]:
    chXX_keyword_classes = {}
    word_str = "word"
    for chapter_prefix in sorted(list(cumlative_ch_keywords_dict.keys())):
        ch_keywords = cumlative_ch_keywords_dict.get(chapter_prefix)
        class_name = f"C{chapter_prefix[1:]}Key{word_str}s"
        ExpectedClass = Enum(class_name, {t: t for t in ch_keywords}, type=str)
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
    cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
    import_enum_line = f"""from enum import Enum


{create_examplestrs_class_str(examples_strs)}
"""
    classes_str = copy_copy(import_enum_line)
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        ch_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_keywords = cumlative_keywords.get(ch_prefix)
        enum_class_str = create_keywords_enum_class_file_str(ch_prefix, ch_keywords)
        classes_str += enum_class_str
    return classes_str


def get_keywords_by_chapter_md() -> str:
    words_str = "words"
    keywords_title_str = f"Key{words_str} by Chapter"
    func_lines = [f"## {keywords_title_str}"]
    keywords_src_config = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_src_config)
    for chapter_desc in get_chapter_descs().keys():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_keywords = keywords_by_chapter.get(chapter_prefix)
        chapter_keywords = sorted(list(chapter_keywords))
        _line = f"- {chapter_desc}: " + ", ".join(chapter_keywords)
        func_lines.append(_line)
    return f"# {keywords_title_str}\n\n" + "\n".join(func_lines)


def save_keywords_by_chapter_md(x_dir: str):
    keywords_by_chapter_md_path = create_path(x_dir, "keywords_by_chapter.md")
    save_file(keywords_by_chapter_md_path, None, get_keywords_by_chapter_md())
