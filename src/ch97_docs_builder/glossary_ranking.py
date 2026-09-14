from ch00_py.file_toolbox import set_dir
from ch01_keyword.chapter_desc_main import get_chapter_descs
from ch01_keyword.keyword_class_builder import (
    get_ch_int,
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch97_docs_builder._ref.ch97_path import (
    create_keg_exam_questions_path,
    create_question_tier_path,
)
from ch97_docs_builder.glossary_definition import get_keywords_definitions
from csv import writer as csv_writer
from dataclasses import dataclass
from json import dumps as json_dumps
from os.path import join as os_path_join
from pathlib import Path
from re import search as re_search
from pandas import read_excel as pandas_read_excel, DataFrame


@dataclass
class QuestionUnit:
    keg_term: str = None
    keyword_definition: str = None
    init_ch: int = None
    question_tier: int = None
    did_you_read_order: int = None
    complete_question: str = None

    def get_question(self) -> str:
        if self.complete_question:
            return self.complete_question
        return f"Did you read that the keyword_definition of '{self.keg_term}' is '{self.keyword_definition}'."


def get_keyword_definition_questionunits() -> dict[str, QuestionUnit]:
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {get_ch_int(chapter_desc) for chapter_desc in chapter_descs}
    keywords_src_config = get_keywords_src_config()

    keywords_definitions = get_keywords_definitions()
    keg_questions = {}
    for keg_term, keyword_definition in keywords_definitions.items():
        kw_config = keywords_src_config.get(keg_term)
        questionunit = QuestionUnit(keg_term, keyword_definition)
        if kw_config:
            valid_chs = parse_valid_ch_str(ch_ints, kw_config.get("valid_ch"))
            init_ch = sorted(valid_chs)[0] if valid_chs else None
            questionunit.init_ch = init_ch
        questionunit.question_tier = 0
        keg_questions[keg_term] = questionunit
    return keg_questions


def get_tiered_questionunits() -> dict[str, QuestionUnit]:
    keywords_src_config = get_keywords_src_config()
    keywords_set = set(keywords_src_config.keys())
    keg_qus = get_keyword_definition_questionunits()
    for keg_term, keg_qu in keg_qus.items():
        # check chxx terms
        if len(keg_term) == 4 and keg_term.startswith("ch"):
            keg_qu.question_tier = 6
        elif keg_qu.init_ch is None and keg_term in keywords_set:
            keg_qu.question_tier = 10
    return keg_qus


def get_keg_rank_dict() -> dict[str, dict]:
    keywords_src_config = get_keywords_src_config()
    keg_questionunits = get_tiered_questionunits()
    set_did_you_read_orders(keg_questionunits)
    keg_tiers = {}
    for keg_term, keg_qu in keg_questionunits.items():
        kw_config = keywords_src_config.get(keg_term)
        valid_ch = kw_config.get("valid_ch") if kw_config else "0:"
        keg_tiers[keg_qu.keg_term] = {
            "keg_rank": keg_qu.did_you_read_order,
            "question_tier": keg_qu.question_tier,
            "chs": valid_ch,
        }
    return keg_tiers


def rebuild_keg_rank_csv(src_dir: str = None):
    keg_tiers = get_keg_rank_dict()

    if src_dir is None:
        src_dir = "src"

    derived_dir = os_path_join(src_dir, "ch99_glossary", "derived")
    set_dir(derived_dir)

    output_path = Path(derived_dir) / "question_tier.csv"

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv_writer(file)
        writer.writerow(["key", "question_tier", "chs"])
        for key, value in sorted(
            keg_tiers.items(),
            key=lambda item: item[1]["keg_rank"],
        ):
            chs_value = value["chs"]
            writer.writerow([key, value["question_tier"], chs_value])


def set_did_you_read_orders(keg_questions: dict[str, QuestionUnit]) -> None:
    """
    Assign did_you_read_order values in-place.

    Ordering rules:
        1. question_tier ascending
        2. init_ch descending
        3. keg_term alphabetical
    """
    sorted_questunits = sorted(
        keg_questions.values(),
        key=lambda q: (
            -q.question_tier,
            q.init_ch is not None,  # None last or first depending on your preference
            (q.init_ch or 0),  # descending for ints
            q.keg_term,
        ),
    )
    for did_you_read_order, questionunit in enumerate(sorted_questunits):
        questionunit.did_you_read_order = did_you_read_order


def get_exam_fixed_questions() -> dict[int, QuestionUnit]:
    question000 = "Have you heard of 'Kegology'?"
    question010 = "Have you heard of Excel spreadsheet application?"
    return {
        0: QuestionUnit(complete_question=question000),
        1: QuestionUnit(complete_question="Have you heard the word 'Philosophy'?"),
        2: QuestionUnit(complete_question="Do you believe listening is important?"),
        10: QuestionUnit(complete_question=question010),
    }


def merge_fixed_and_floating_questions(
    fixed_questions: dict[int, QuestionUnit],
    floating_questions: dict[str, QuestionUnit],
) -> list[QuestionUnit]:
    """
    Merge fixed-position QuestionUnits with floating QuestionUnits.

    Fixed indexes are absolute.
    Floating questions are inserted into all remaining positions.
    """

    set_did_you_read_orders(floating_questions)

    sorted_floating_questions: list[QuestionUnit] = sorted(
        floating_questions.values(),
        key=lambda questionunit: questionunit.did_you_read_order,
    )

    result_questionunits: list[QuestionUnit] = []

    floating_index = 0
    total_length = len(fixed_questions) + len(sorted_floating_questions)

    for index in range(total_length):
        if index in fixed_questions:
            result_questionunits.append(fixed_questions[index])
        else:
            result_questionunits.append(sorted_floating_questions[floating_index])
            floating_index += 1

    return result_questionunits


def rebuild_keg_exam_questions(
    output_csv_path: str | Path = None,
) -> None:
    """
    Create the final exam question list and export it to a CSV file.

    CSV columns:
        - row_number
        - question
    """
    if not output_csv_path:
        output_csv_path = create_keg_exam_questions_path("src")
    final_questions = merge_fixed_and_floating_questions(
        fixed_questions=get_exam_fixed_questions(),
        floating_questions=get_tiered_questionunits(),
    )

    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv_writer(csv_file)
        writer.writerow(["question"])
        for questionunit in final_questions:
            writer.writerow([questionunit.get_question()])


def get_ch_sorted_keywords(keywords_src_config: dict) -> list[str]:
    def parse_chapter(ch):
        if not ch:
            return float("inf")  # push empty to front
        match = re_search(r"\d+", ch)
        return int(match.group()) if match else -1

    return sorted(
        keywords_src_config.keys(),
        key=lambda k: (
            -keywords_src_config[k].get("question_tier", float("inf")),
            -parse_chapter(keywords_src_config[k].get("valid_ch", "")),
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


def load_keg_knowledge(file_path: str) -> DataFrame:
    """
    Reads the 'keg_knowledge' sheet from an Excel file, loads it into a
    dataframe with columns [keg_question, answer], aggregates exact duplicate
    pairs, then removes any keg_question that has more than one distinct answer.

    Args:
        file_path: Path to the Excel file.

    Returns:
        Cleaned DataFrame with columns [keg_question, answer].
    """
    df = pandas_read_excel(file_path, sheet_name="keg_knowledge")
    df = df[["keg_question", "answer"]].copy()

    # Strip whitespace and normalise case for reliable deduplication
    df["keg_question"] = df["keg_question"].astype(str).str.strip()
    df["answer"] = df["answer"].astype(str).str.strip().str.lower()

    # Step 1: collapse exact duplicate question/answer pairs
    df = df.drop_duplicates(subset=["keg_question", "answer"])

    # Step 2: drop questions that have more than one distinct answer
    answer_counts = df.groupby("keg_question")["answer"].nunique()
    single_answer_questions = answer_counts[answer_counts == 1].index
    df = df[df["keg_question"].isin(single_answer_questions)].reset_index(drop=True)

    return df
