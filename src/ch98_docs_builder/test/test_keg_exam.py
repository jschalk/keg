from inspect import getdoc as inspect_getdoc
from re import fullmatch as re_fullmatch
from src.ch00_py.keyword_class_builder import get_keywords_src_config
from src.ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_config_dict,
)
from src.ch13_time.epoch_main import get_c400_constants, get_default_epoch_config_dict
from src.ch14_moment.moment_config import get_moment_config_args
from src.ch15_nabu.nabu_config import get_nabu_args, get_nabuable_args
from src.ch16_translate.translate_config import (
    get_translate_config_args,
    get_translate_config_dict,
)
from src.ch18_etl_config.etl_config import get_etl_stage_types_config_dict
from src.ch19_etl_steps.etl_main import etl_heard_raw_tables_to_moment_ote1_agg
from src.ch98_docs_builder._ref.ch98_semantic_types import (
    BreakTerm,
    ContactName,
    CRUD_command,
    EpochLabel,
    FaceName,
    FactNum,
    FirstLabel,
    FundGrain,
    FundNum,
    GrainNum,
    GroupMark,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    LobbyID,
    ManaGrain,
    ManaNum,
    MomentRope,
    NameTerm,
    PersonName,
    PoolNum,
    ReasonNum,
    RespectGrain,
    RespectNum,
    RopeTerm,
    SparkInt,
    TimeNum,
    TitleTerm,
    WeightNum,
    WorldName,
)
from src.ch98_docs_builder.keg_definitions_builder import (
    get_ch_sorted_keywords,
    get_chxx_prefix_path_dict,
    get_chxx_ref_blurb,
    get_keg_definitions,
    get_keg_exam,
    get_kegology_exam_grade,
    get_keywords_by_importance,
    get_person_dimen_config,
)
from src.ref.keywords import Ch98Keywords as kw


def test_get_ch_sorted_keywords_ReturnsObj_Scenario0_basic_sorting():
    # ESTABLISH
    data = {
        "Excel": {kw.exam_tier: 0, kw.init_chapter: kw.ch17},
        "Word": {kw.exam_tier: 0, kw.init_chapter: kw.ch02},
        "Access": {kw.exam_tier: 1, kw.init_chapter: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["Access", "Excel", "Word"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario1_empty_chapter_goes_first_within_tier():
    # ESTABLISH
    data = {
        "Excel": {kw.exam_tier: 0, kw.init_chapter: kw.ch17},
        "Word": {kw.exam_tier: 0, kw.init_chapter: ""},
        "PowerPoint": {kw.exam_tier: 0, kw.init_chapter: kw.ch02},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["Word", "Excel", "PowerPoint"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario2_empty_vs_other_tiers():
    # ESTABLISH
    data = {
        "A": {kw.exam_tier: 1, kw.init_chapter: ""},
        "B": {kw.exam_tier: 0, kw.init_chapter: kw.ch01},
        "C": {kw.exam_tier: 0, kw.init_chapter: ""},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    # Tier first, then chapter (empty first within same tier)
    assert result == ["A", "C", "B"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario3_malformed_chapter_treated_like_empty():
    # ESTABLISH
    data = {
        "A": {kw.exam_tier: 0, kw.init_chapter: "foo"},
        "B": {kw.exam_tier: 0, kw.init_chapter: kw.ch02},
        "C": {kw.exam_tier: 0, kw.init_chapter: ""},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    # A and C both treated as -1 → alphabetical between them
    assert result == ["C", "B", "A"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario4_alphabetical_tiebreaker():
    # ESTABLISH
    data = {
        "beta": {kw.exam_tier: 0, kw.init_chapter: kw.ch01},
        "Alpha": {kw.exam_tier: 0, kw.init_chapter: kw.ch01},
        "gamma": {kw.exam_tier: 0, kw.init_chapter: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["Alpha", "beta", "gamma"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario5_missing_fields():
    # ESTABLISH
    data = {
        "A": {},  # missing both fields
        "B": {kw.exam_tier: 0},
        "C": {kw.init_chapter: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    # A: tier=inf, ch=-1 → last tier but first within that tier
    # C: tier=inf, ch=1
    # B: tier=0, ch=-1 → comes first overall
    assert result == ["A", "C", "B"]


def test_get_keywords_by_importance_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    kws_by_importance = get_keywords_by_importance()

    # THEN
    ch_sorted_keywords = get_ch_sorted_keywords(get_keywords_src_config())
    assert len(ch_sorted_keywords) == len(kws_by_importance)
    for sorted_count, sorted_keyword in enumerate(ch_sorted_keywords):
        assert kws_by_importance.get(sorted_count) == sorted_keyword

    keywords_src_config = get_keywords_src_config()
    for kw_index, kw_with_i in kws_by_importance.items():
        kw_src_config = keywords_src_config.get(kw_with_i)
        tier_str = kw_src_config.get(kw.exam_tier)
        init_chapter_str = kw_src_config.get(kw.init_chapter)
        # if kw_index < 30:
        #     print(f"{kw_index} {tier_str} {init_chapter_str} {kw_with_i=}")


def test_get_keg_exam_ReturnsObj_ObjExists():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    assert keg_exam
    assert len(keg_exam) > 1


def test_get_keg_exam_ReturnsObj_KeysAreSequentialInts():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    keys = list(keg_exam.keys())
    assert keys, "keg_exam should not be empty"

    int_keys = []
    for key in keys:
        assertion_failure_str = f"Expected string keys for keg_exam, but found key of type {type(key).__name__}: {key}"
        assert isinstance(key, str), assertion_failure_str
        assert key.isdigit(), f"Expected numeric string keys, but found: {key}"
        int_keys.append(int(key))

    sorted_keys = sorted(int_keys)
    start = sorted_keys[0]
    for expected, actual in zip(range(start, start + len(sorted_keys)), sorted_keys):
        assert expected == actual, (
            f"keg_exam first-level keys are not sequential: expected {expected} but found {actual}. "
            f"Break in sequence after {expected - 1}."
        )


def test_get_keg_exam_ReturnsObj_DictionariesHavekeys():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    required_fields = {"question_type", "question_str"}

    for exam_level, exam_dict in keg_exam.items():
        assert_dict_fails_str = f"Expected keg_exam[{exam_level!r}] to be a dict, but got {type(exam_dict).__name__}"
        assert isinstance(exam_dict, dict), assert_dict_fails_str
        missing_fields = required_fields - exam_dict.keys()
        assertion_missing_fields_fails = f"keg_exam[{exam_level!r}] is missing required field(s): {sorted(missing_fields)}"
        assert not missing_fields, assertion_missing_fields_fails

        if exam_dict.get("question_type") == "Keyword Definition":
            assert exam_dict.get("keyword")


def test_get_keg_exam_HasAll_keywords_DefinitionQuestions():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    keywords_with_index_key = {
        key: value["keyword"]
        for key, value in keg_exam.items()
        if isinstance(value, dict)
        and value.get("question_type") == "Keyword Definition"
    }
    definition_fail_str = "No Keyword Definition questions found in keg_exam"
    assert keywords_with_index_key, definition_fail_str

    keg_definitions = get_keg_definitions()
    for keyword in keywords_with_index_key.values():
        assert keg_definitions.get(keyword) != None, keyword


# def first_out_of_order(
#     sorting_order: dict[int, str], exam_order: dict[int, str]
# ) -> str | None:
#     # Step 1: build expected ranking
#     expected_sequence = [keyword for _, keyword in sorted(sorting_order.items())]
#     rank = {keyword: i for i, keyword in enumerate(expected_sequence)}

#     # Step 2: iterate through exam order
#     last_rank = -1
#     for _, keyword in sorted(exam_order.items()):
#         if keyword not in rank:
#             # skip or raise depending on your use case
#             continue

#         current_rank = rank[keyword]

#         # Step 3: detect violation
#         if current_rank < last_rank:
#             print(f"{keyword} {current_rank=} {last_rank=}")
#             return keyword

#         last_rank = current_rank

#     return None


# TODO write keg_exam_doc_builder that passes this test
# follow keywords_main model: On every test run rewrite key_exam.json. Then run
# the tests so that it's clear it satisfies requirements.
# def test_get_keg_exam_DefinitionQuestionsAreInOrder():
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()
#     # THEN
#     definition_exam_keywords = {
#         key: value["keyword"]
#         for key, value in keg_exam.items()
#         if isinstance(value, dict)
#         and value.get("question_type") == "Keyword Definition"
#     }

#     sorted_keywords = dict(enumerate(get_ch_sorted_keywords(get_keywords_src_config())))
#     # print(f"{sorted_keywords=}")
#     assert not first_out_of_order(sorted_keywords, definition_exam_keywords)
#     # for keyword_term in sorted_keywords:
#     #     x_question_str = f"Have you read the Kegology definition of '{keyword_term}'?"
#     #     question_dict = {
#     #         "question_type": "Keyword Definition",
#     #         "question_str": x_question_str,
#     #         "keyword": keyword_term,
#     #     }
#     #     expected_keyword_definition_questions[str(x_count)] = question_dict
#     #     x_count += 1

#     # for exam_level, question_dict2 in expected_keyword_definition_questions.items():
#     #     print(f""""{exam_level}": {question_dict2},""")
#     # need to create new asserts that all keyword_terms have exam question


# The concept is that a set of statements like "I have read about the keg definition of 'plan'
# and the function will return the highest completed keg exam level.
# if new terms are introduced that could change a keg exam level measurement.
# Thus each exam measurement is associated with a keg version.
# def test_get_kegology_exam_grade_ReturnsHighestCompletedQuestionNum():
#     # ESTABLISH
#     # Simulating answers dict with question_str as key, answer as value
#     answers = {
#         "Have you heard of 'Kegology'?": "yes",
#         "Have you heard of 'Philosophy'?": "no",
#         # Question 2 is not answered
#     }

#     # WHEN
#     from src.ch98_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return 1 (the highest question number that is complete, which is before 2)
#     assert result == 1, f"Expected grade 1, but got {result}"

# # TODO get these tests working
# def test_get_kegology_exam_grade_AllQuestionsAnswered():
#     # ESTABLISH
#     keg_exam = get_keg_exam()
#     answers = {
#         value["question_str"]: "yes"
#         for value in keg_exam.values()
#         if isinstance(value, dict)
#     }

#     # WHEN
#     from src.ch98_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return the highest question number (len - 1 since we start from 0)
#     expected = len(keg_exam) - 1
#     assert (
#         result == expected
#     ), f"Expected grade {expected} (all questions), but got {result}"


# # TODO get these tests working
# def test_get_kegology_exam_grade_NoQuestionsAnswered():
#     # ESTABLISH
#     answers = {}

#     # WHEN
#     from src.ch98_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return -1 (no questions completed, so return before first question 0)
#     assert result == -1, f"Expected grade -1 (no questions), but got {result}"
