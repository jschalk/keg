from ch00_py.file_toolbox import open_json, save_json
from ch01_keyword.chapter_desc_main import (
    get_ch_int,
    get_chapter_desc_prefix,
    get_chapter_descs,
)
from ch01_keyword.keyword_class_builder import (
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch08_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_config_dict,
)
from ch97_docs_builder._ref.ch97_path import (
    create_chapter_ref_path,
    create_src_keywords_definitions_path,
)
from collections import defaultdict
from pathlib import Path


def get_keywords_definitions() -> dict[str, dict]:
    return open_json(create_src_keywords_definitions_path("src"))


def save_keg_descriptions_json(src_dir: str, x_dict: dict[str, dict]):
    file_path = create_src_keywords_definitions_path(src_dir)
    save_json(file_path, None, x_dict, keys_case_insensitive=True)


def get_person_dimen_config(dimen: str) -> dict:
    x_dimen_config = get_person_config_dict().get(dimen)
    x_config_args = x_dimen_config.get("jkeys")
    for v_keyword, v_config in x_dimen_config.get("jvalues").items():
        x_config_args[v_keyword] = v_config
    return x_config_args


def rebuild_keywords_definitions_contents():
    ch_dict = get_chxx_prefix_path_dict()
    person_config_args = get_person_dimen_config("personunit")
    plan_config_args = get_person_dimen_config("person_planunit")
    all_person_calc_args = get_all_person_calc_args()

    rebuilt_kw_desc = {}
    for keyword, description in get_keywords_definitions().items():
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

    save_keg_descriptions_json("src", rebuilt_kw_desc)


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


def get_count_strs_by_dirs(
    ch_dirs: dict[int, str | Path],
    keg_terms: set[str],
    excluded_path_strs: set[str] | None = None,
) -> dict[str, dict[int, int]]:
    """
    Returns:
        {
            "SomeTerm": {
                1: 4,
                2: 0,
                3: 9,
            },
            ...
        }
    """
    excluded_path_strs = excluded_path_strs or set()

    term_counts = defaultdict(dict)

    for ch_int, ch_dir in ch_dirs.items():
        ch_dir = Path(ch_dir)

        chapter_text_parts = []

        for file_path in ch_dir.rglob("*"):
            if not file_path.is_file():
                continue

            file_path_str = str(file_path)

            if any(
                excluded_path_str in file_path_str
                for excluded_path_str in excluded_path_strs
            ):
                continue

            try:
                file_text = file_path.read_text(
                    encoding="utf-8",
                )
                chapter_text_parts.append(file_text)

            except UnicodeDecodeError:
                continue

        chapter_text = "\n".join(chapter_text_parts)

        for keg_term in keg_terms:
            count = chapter_text.count(keg_term)
            term_counts[keg_term][ch_int] = count

    return dict(term_counts)


def get_count_keg_terms_by_chapters():
    ch_dirs = {}
    for ch_desc, ch_dir in get_chapter_descs().items():
        ch_int = get_ch_int(ch_desc)
        if ch_int != 99:
            ch_dirs[ch_int] = ch_dir
    keg_terms = set(get_keywords_definitions().keys())
    excluded_substrs = {"semantic"}
    count_strs_by_dirs = get_count_strs_by_dirs(ch_dirs, keg_terms, excluded_substrs)
    return {
        keg_term: {ch_int: count for ch_int, count in ch_counts.items() if count != 0}
        for keg_term, ch_counts in count_strs_by_dirs.items()
    }


def get_focus_keyword_frequency(focus_keywords: set) -> dict[str, tuple[list, list]]:
    focus_keyword_frequency = {}
    # This part finds all keg_terms used only in one chapter and changes
    # valid_ch from range to single chapter
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {get_ch_int(chapter_desc) for chapter_desc in chapter_descs}
    keywords_src_config = get_keywords_src_config()
    keg_terms_by_chapters = get_count_keg_terms_by_chapters()

    for keg_term in sorted(keg_terms_by_chapters.keys()):
        ch_dir_dict = keg_terms_by_chapters.get(keg_term)
        # if len(ch_dir_dict) == 2:
        if keyword_config := keywords_src_config.get(keg_term):
            if len(ch_dir_dict) > 0:
                lone_ch = list(ch_dir_dict.keys())[0]
                x_valid_ch = keyword_config.get("valid_ch")
                valid_chapters = sorted(parse_valid_ch_str(ch_ints, x_valid_ch))
                if str(lone_ch) != x_valid_ch:
                    # if len(valid_chapters) - len(ch_dir_dict) > 20:
                    if keg_term in focus_keywords:
                        term_current_and_allowed_chs = (ch_dir_dict, valid_chapters)
                        focus_keyword_frequency[keg_term] = term_current_and_allowed_chs
                    keyword_config["valid_ch"] = str(lone_ch)
    return focus_keyword_frequency
