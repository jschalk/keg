from src.ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_dimen_args,
    get_person_config_dict,
)
from src.ch18_etl_config.etl_config import get_etl_stage_types_config_dict
from src.ch98_docs_builder._ref.ch98_path import (
    create_chapter_ref_path,
    create_src_keywords_description_path,
)


def get_keywords_description() -> dict[str, dict]:
    return open_json(create_src_keywords_description_path("src"))


def save_keywords_descrition_json(src_dir: str, x_dict: dict[str, dict]):
    file_path = create_src_keywords_description_path(src_dir)
    save_json(file_path, None, x_dict, keys_case_insensitive=True)


def get_person_dimen_config(dimen: str) -> dict:
    x_dimen_config = get_person_config_dict().get(dimen)
    x_config_args = x_dimen_config.get("jkeys")
    for v_keyword, v_config in x_dimen_config.get("jvalues").items():
        x_config_args[v_keyword] = v_config
    return x_config_args


def rebuild_keywords_description_contents():
    ch_dict = get_chxx_prefix_path_dict()
    person_config_args = get_person_dimen_config("personunit")
    plan_config_args = get_person_dimen_config("person_planunit")
    all_person_calc_args = get_all_person_calc_args()

    rebuilt_kw_desc = {}
    for keyword, description in get_keywords_description().items():
        rebuilt_kw_desc[keyword] = description
        if keyword in ch_dict:
            rebuilt_kw_desc[keyword] = get_chxx_ref_blurb(ch_dict, keyword)
        if keyword in person_config_args:
            keyword_config = person_config_args.get(keyword)
            if keyword_config.get("calc_by_conpute"):
                # rebuilt_kw_desc[keyword] = f"Person conpute"
                pass
            else:
                # rebuilt_kw_desc[keyword] = f"Set by seed part of the Person bluep"
                pass
        # if keyword in plan_config_args:
        #     keyword_config = plan_config_args.get(keyword)
        #     if keyword_config.get("calc_by_conpute"):
        #         rebuilt_kw_desc[keyword] = f"Set by Person conpute process"
        #     else:
        #         rebuilt_kw_desc[keyword] = f"Plan seed data"

    save_keywords_descrition_json("src", rebuilt_kw_desc)


def get_chxx_prefix_path_dict() -> dict[str, str]:
    ch_dict = {}
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_ref_path = create_chapter_ref_path(chapter_dir, chapter_desc_prefix)
        ch_dict[chapter_desc_prefix] = ch_ref_path
    return ch_dict


def get_chxx_ref_blurb(ch_dict, keyword) -> str:
    ch_ref_dict = open_json(ch_dict[keyword])
    return ch_ref_dict.get("chapter_blurb")


# def get_keywords_by_chapter(keywords_dict: dict[str, dict[str]]) -> dict:
#     chapter_descs = get_chapter_descs().keys()
#     chapters_keywords = {get_chapter_desc_prefix(chxx): set() for chxx in chapter_descs}
#     for x_keyword, ref_dict in keywords_dict.items():
#         keyworld_init_chapter_num = ref_dict.get("init_chapter")
#         chapter_set = chapters_keywords.get(keyworld_init_chapter_num)
#         chapter_set.add(x_keyword)
#     return chapters_keywords


# def get_cumlative_ch_keywords_dict(keywords_by_chapter: dict[int, set[str]]) -> dict:
#     allowed_keywords_set = set()
#     cumlative_ch_keywords_dict = {}
#     for chapter_num in sorted(list(keywords_by_chapter.keys())):
#         ch_keywords_set = keywords_by_chapter.get(chapter_num)
#         allowed_keywords_set.update(ch_keywords_set)
#         cumlative_ch_keywords_dict[chapter_num] = copy_copy(allowed_keywords_set)
#     return cumlative_ch_keywords_dict


# def get_chapter_keyword_classes(cumlative_ch_keywords_dict: dict) -> dict[int,]:
#     chXX_keyword_classes = {}
#     word_str = "word"
#     for chapter_prefix in sorted(list(cumlative_ch_keywords_dict.keys())):
#         ch_keywords = cumlative_ch_keywords_dict.get(chapter_prefix)
#         class_name = f"C{chapter_prefix[1:]}Key{word_str}s"
#         ExpectedClass = Enum(class_name, {t: t for t in ch_keywords}, type=str)
#         chXX_keyword_classes[chapter_prefix] = ExpectedClass
#     return chXX_keyword_classes


# def create_keywords_enum_class_file_str(chapter_prefix: str, keywords_set: set) -> str:
#     keywords_str = ""
#     if not keywords_set:
#         keywords_str += "\n    pass"
#     else:
#         for keyword_str in sorted(keywords_set):
#             keywords_str += f'\n    {keyword_str} = "{keyword_str}"'

#     chXX_str = f"{chapter_prefix.upper()[:1]}{chapter_prefix.lower()[1:]}"
#     key_str = "Key"
#     dunder_str_func_str = """
#     def __str__(self):
#         return self.value
# """
#     return f"""

# class {chXX_str}{key_str}words(str, Enum):{keywords_str}
# {dunder_str_func_str}"""


# def create_examplestrs_class_str(example_strs_dict: dict) -> str:
#     enum_attrs = ""
#     for key_str in sorted(example_strs_dict.keys()):
#         value_str = example_strs_dict.get(key_str)
#         enum_attrs += f"""    {key_str} = "{value_str}"\n"""

#     return f"""class ExampleStrs(str, Enum):
# {enum_attrs}
#     def __str__(self):
#         return self.value"""


# def create_all_enum_keyword_classes_str() -> str:
#     examples_strs = get_example_strs_config()
#     keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
#     cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
#     import_enum_line = f"""from enum import Enum


# {create_examplestrs_class_str(examples_strs)}
# """
#     classes_str = copy_copy(import_enum_line)
#     for chapter_desc, chapter_dir in get_chapter_descs().items():
#         ch_prefix = get_chapter_desc_prefix(chapter_desc)
#         ch_keywords = cumlative_keywords.get(ch_prefix)
#         enum_class_str = create_keywords_enum_class_file_str(ch_prefix, ch_keywords)
#         classes_str += enum_class_str
#     return classes_str


# def get_keywords_by_chapter_md() -> str:
#     words_str = "words"
#     keywords_title_str = f"Key{words_str} by Chapter"
#     func_lines = [f"## {keywords_title_str}"]
#     keywords_src_config = get_keywords_src_config()
#     keywords_by_chapter = get_keywords_by_chapter(keywords_src_config)
#     for chapter_desc in get_chapter_descs().keys():
#         chapter_prefix = get_chapter_desc_prefix(chapter_desc)
#         chapter_keywords = keywords_by_chapter.get(chapter_prefix)
#         chapter_keywords = sorted(list(chapter_keywords))
#         _line = f"- {chapter_desc}: " + ", ".join(chapter_keywords)
#         func_lines.append(_line)
#     return f"# {keywords_title_str}\n\n" + "\n".join(func_lines)


# def save_keywords_by_chapter_md(x_dir: str):
#     keywords_by_chapter_md_path = create_path(x_dir, "keywords_by_chapter.md")
#     save_file(keywords_by_chapter_md_path, None, get_keywords_by_chapter_md())
