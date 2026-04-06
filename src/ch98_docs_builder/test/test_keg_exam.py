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
    get_keg_definitions,
    get_keg_exam,
    get_person_dimen_config,
    get_kegology_exam_grade,
)
from src.ref.keywords import Ch98Keywords as kw


def test_get_keg_exam_ReturnsObj_ObjExists():
    # ESTABLISH

    # WHEN
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
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    required_fields = {"question_type", "question_str"}

    for key, value in keg_exam.items():
        assert_dict_fails_str = (
            f"Expected keg_exam[{key!r}] to be a dict, but got {type(value).__name__}"
        )
        assert isinstance(value, dict), assert_dict_fails_str
        missing_fields = required_fields - value.keys()
        assertion_missing_fields_fails = (
            f"keg_exam[{key!r}] is missing required field(s): {sorted(missing_fields)}"
        )
        assert not missing_fields, assertion_missing_fields_fails


# TODO get this workings
# def test_get_keg_definitions_keywords_have_unique_keyword_definition_questions():
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()

#     # THEN
#     keg_definitions = get_keg_definitions()
#     keyword_definition_questions = [
#         value["question_str"]
#         for value in keg_exam.values()
#         if isinstance(value, dict)
#         and value.get("question_type") == "Keyword Definition"
#     ]
#     definition_fail_str = "No Keyword Definition questions found in keg_exam"
#     assert keyword_definition_questions, definition_fail_str

#     expected_keyword_definition_questions = {}
#     int_keys = set()
#     for key in keg_exam.keys():
#         int_keys.add(int(key))
#     x_count = max(int_keys) + 1
#     for keyword_term, keyword_desc in keg_definitions.items():
#         x_question_str = f"Do know what {keyword_term} is about this?: {keyword_desc}"
#         question_dict = {
#             "question_type": "Keyword Definition",
#             "question_str": x_question_str,
#         }
#         expected_keyword_definition_questions[str(x_count)] = question_dict
#         x_count += 1
#     print(expected_keyword_definition_questions)

#     for keyword in sorted(keg_definitions):
#         matches = [
#             question_str
#             for question_str in keyword_definition_questions
#             if keyword in question_str
#         ]
#         assert len(matches) == 1, (
#             f"Expected exactly one Keyword Definition question for keyword {keyword!r}, "
#             f"found {len(matches)} matches: {matches}"
#         )


# # TODO get these tests working
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
