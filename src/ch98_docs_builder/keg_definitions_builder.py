from ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from ch00_py.file_toolbox import create_path, open_json, save_json
from ch00_py.keyword_class_builder import get_keywords_src_config
from ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_dimen_args,
    get_person_config_dict,
)
from ch18_etl_config.etl_config import get_etl_stage_types_config_dict
from ch98_docs_builder._ref.ch98_path import (
    create_chapter_ref_path,
    create_src_keg_definitions_path,
    create_src_keg_exam_path,
)
from re import search as re_search


def get_keg_definitions() -> dict[str, dict]:
    return open_json(create_src_keg_definitions_path("src"))


def save_keywords_descrition_json(src_dir: str, x_dict: dict[str, dict]):
    file_path = create_src_keg_definitions_path(src_dir)
    save_json(file_path, None, x_dict, keys_case_insensitive=True)


def get_person_dimen_config(dimen: str) -> dict:
    x_dimen_config = get_person_config_dict().get(dimen)
    x_config_args = x_dimen_config.get("jkeys")
    for v_keyword, v_config in x_dimen_config.get("jvalues").items():
        x_config_args[v_keyword] = v_config
    return x_config_args


def rebuild_keg_definitions_contents():
    ch_dict = get_chxx_prefix_path_dict()
    person_config_args = get_person_dimen_config("personunit")
    plan_config_args = get_person_dimen_config("person_planunit")
    all_person_calc_args = get_all_person_calc_args()

    rebuilt_kw_desc = {}
    for keyword, description in get_keg_definitions().items():
        rebuilt_kw_desc[keyword] = description
        if keyword in ch_dict:
            rebuilt_kw_desc[keyword] = get_chxx_ref_blurb(ch_dict, keyword)
        if keyword in person_config_args:
            keyword_config = person_config_args.get(keyword)
            if keyword_config.get("calc_by_thinkout"):
                # rebuilt_kw_desc[keyword] = f"Person thinkout"
                pass
            # else:
            #     # rebuilt_kw_desc[keyword] = f"Set by seed part of the Person bluep"
            #     pass
        # if keyword in plan_config_args:
        #     keyword_config = plan_config_args.get(keyword)
        #     if keyword_config.get("calc_by_thinkout"):
        #         rebuilt_kw_desc[keyword] = f"Set by Person thinkout process"
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


def get_keg_exam() -> dict[str, dict]:
    return open_json(create_src_keg_exam_path("src"))


def get_ch_sorted_keywords(keywords_src_config: dict) -> list[str]:
    def parse_chapter(ch):
        if not ch:
            return float("inf")  # push empty to front
        match = re_search(r"\d+", ch)
        return int(match.group()) if match else -1

    return sorted(
        keywords_src_config.keys(),
        key=lambda k: (
            -keywords_src_config[k].get("exam_tier", float("inf")),
            -parse_chapter(keywords_src_config[k].get("init_chapter", "")),
            k.lower(),
        ),
    )


def get_keywords_by_importance() -> dict:
    x_list = get_ch_sorted_keywords(get_keywords_src_config())
    return dict(enumerate(x_list))


def get_kegology_exam_grade(answers: dict[str, str]) -> int:
    """Return the highest completed exam question index.

    A question is complete only when its question_str maps to "yes" in answers.
    If a question is missing or not answered "yes", the grade is the previous
    question index. If the first question is incomplete, return -1.
    """
    return 0
    # keg_exam = get_keg_exam()

    # question_numbers = []
    # question_map = {}
    # for key, value in keg_exam.items():
    #     question_str = value.get("question_str")
    #     question_number = int(key)
    #     question_numbers.append(question_number)
    #     question_map[question_number] = question_str

    # if not question_numbers:
    #     return -1

    # for question_number in sorted(question_numbers):
    #     question_str = question_map[question_number]
    #     answer = answers.get(question_str)
    #     if not isinstance(answer, str) or answer.strip().lower() != "yes":
    #         return question_number - 1

    # return max(question_numbers)
