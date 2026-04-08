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
    get_chxx_prefix_path_dict,
    get_chxx_ref_blurb,
    get_keg_ch_sorted_terms,
    get_keg_definitions,
    get_keg_exam,
    get_kegology_exam_grade,
    get_person_dimen_config,
)
from src.ref.keywords import Ch98Keywords as kw


def test_get_keg_ch_sorted_terms_ReturnsObj_Scenario0_BasicSorting():
    # ESTABLISH
    data = {
        "apple": {kw.init_chapter: "ch03"},
        "banana": {kw.init_chapter: "ch05"},
        "cherry": {kw.init_chapter: "ch05"},
        "date": {kw.init_chapter: "ch02"},
    }
    # WHEN
    result = get_keg_ch_sorted_terms(data)
    # THEN
    assert result == ["banana", "cherry", "apple", "date"]


def test_get_keg_ch_sorted_terms_ReturnsObj_Scenario1_AlphabeticalTiebreak():
    # ESTABLISH
    data = {
        "zebra": {kw.init_chapter: "ch10"},
        "alpha": {kw.init_chapter: "ch10"},
        "middle": {kw.init_chapter: "ch10"},
    }
    # WHEN
    result = get_keg_ch_sorted_terms(data)
    # THEN
    assert result == ["alpha", "middle", "zebra"]


def test_get_keg_ch_sorted_terms_ReturnsObj_Scenario2_SingleItem():
    # ESTABLISH
    data = {
        "only": {kw.init_chapter: "ch01"},
    }
    # WHEN
    result = get_keg_ch_sorted_terms(data)
    # THEN
    assert result == ["only"]


def test_get_keg_ch_sorted_terms_ReturnsObj_Scenario3_EmptyDict():
    # ESTABLISH
    data = {}
    # WHEN
    result = get_keg_ch_sorted_terms(data)
    # THEN
    assert result == []


def test_get_keg_ch_sorted_terms_ReturnsObj_Scenario4_NegativeAndZeroValues():
    # ESTABLISH
    data = {
        "a": {kw.init_chapter: "ch00"},
        "b": {kw.init_chapter: "ch-1"},
        "c": {kw.init_chapter: "ch02"},
    }
    # WHEN
    result = get_keg_ch_sorted_terms(data)
    # THEN
    assert result == ["c", "a", "b"]


def test_get_keg_ch_sorted_terms_ReturnsObj_Scenario5_NoneValue():
    # ESTABLISH
    data = {
        "a": {kw.init_chapter: "ch01"},
        "b": {kw.init_chapter: ""},  # missing key
    }
    # WHEN
    result = get_keg_ch_sorted_terms(data)
    # THEN
    assert result == ["b", "a"]


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
        assert isinstance(
            key, str
        ), f"Expected string keys for keg_exam, but found key of type {type(key).__name__}: {key}"
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


# TODO get this workings
def test_get_keg_exam_HasAll_keywordsDefinitionQuestions():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    keyword_definition_questions = [
        value["question_str"]
        for value in keg_exam.values()
        if isinstance(value, dict)
        and value.get("question_type") == "Keyword Definition"
    ]
    definition_fail_str = "No Keyword Definition questions found in keg_exam"
    assert keyword_definition_questions, definition_fail_str

    keg_definitions = get_keg_definitions()

    expected_keyword_definition_questions = {}
    int_keys = {int(key) for key in keg_exam.keys()}
    x_count = max(int_keys) + 1
    sorted_keywords = get_keg_ch_sorted_terms(get_keywords_src_config())
    for keyword_term in sorted_keywords:
        x_question_str = f"Have you read the Kegology definition of '{keyword_term}'?"
        question_dict = {
            "question_type": "Keyword Definition",
            "question_str": x_question_str,
            "keyword": keyword_term,
        }
        expected_keyword_definition_questions[str(x_count)] = question_dict
        x_count += 1

    # for exam_level, question_dict2 in expected_keyword_definition_questions.items():
    #     print(f""""{exam_level}": {question_dict2},""")
    # need to create new asserts that all keyword_terms have exam question


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
