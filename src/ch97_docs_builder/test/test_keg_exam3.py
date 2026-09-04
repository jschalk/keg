from ch00_py.file_toolbox import open_json, save_json
from ch01_keyword.keyword_class_builder import (
    get_ch_int,
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch97_docs_builder._ref.ch97_path import (
    create_question_tier_path,
    create_keg_exam_questions_path,
)
from ch97_docs_builder.glossary_ranking import (
    QuestionUnit,
    get_ch_sorted_keywords,
    get_exam_fixed_questions,
    get_tiered_questionunits,
    merge_fixed_and_floating_questions,
    rebuild_keg_exam_questions,
    rebuild_keg_rank_csv,
    set_did_you_read_orders,
    rebuild_keg_exam_questions,
)
from ch99_glossary.ch_keyword import Ch97Keywords as kw
from os.path import exists as os_path_exists
from ch20_brick.brick_db_tool import open_csv


def test_rebuild_keg_rank_csv_SavesFile_Scenario0_NoFileExists(temp3_fs):
    # ESTABLISH
    src_dir = str(temp3_fs)
    question_tier_path = create_question_tier_path(src_dir)
    print(f"{question_tier_path=}")
    assert not os_path_exists(question_tier_path)
    # WHEN
    rebuild_keg_rank_csv(src_dir)
    # THEN
    assert os_path_exists(question_tier_path)


# def test_rebuild_keg_rank_csv_SavesFile_Scenario1_NoFileExists(temp3_fs):
#     # ESTABLISH
#     src_dir = str(temp3_fs)
#     question_tier_path = create_question_tier_path(src_dir)
#     assert not os_path_exists(question_tier_path)
#     # WHEN
#     rebuild_keg_rank_csv(src_dir)
#     # THEN
#     assert os_path_exists(question_tier_path)
#     question_tier_dict = open_json(question_tier_path)

#     keywords_src_config = get_keywords_src_config()
#     chapter_descs = get_chapter_descs().keys()
#     ch_ints = {get_ch_int(chapter_desc) for chapter_desc in chapter_descs}
#     keg_questionunits = get_keg_definition_questionunits()
#     expected_keg_tiers = {}
#     for keg_term, keg_qu in keg_questionunits.items():
#         kw_config = keywords_src_config.get(keg_term)
#         # if kw_config:
#         #     ch_list = parse_valid_ch_str(ch_ints, kw_config.get("valid_ch"))
#         # else:
#         #     ch_list = set(ch_ints)
#         valid_ch = kw_config.get("valid_ch") if kw_config else "0:"
#         expected_keg_tiers[keg_qu.keg_term] = {
#             "question_tier": keg_qu.question_tier,
#             "chs": valid_ch,
#         }
#     for keg_term, exam_dict in expected_keg_tiers.items():
#         print(f"{keg_term=} {exam_dict=}")
#     assert question_tier_dict == expected_keg_tiers


def test_get_exam_fixed_questions_ReturnsObj():
    # ESTABLISH / WHEN
    exam_fixed_questions = get_exam_fixed_questions()

    # THEN
    assert len(exam_fixed_questions) > 3
    for int_key in exam_fixed_questions.keys():
        assert int_key >= 0


def test_merge_fixed_and_floating_questions_ReturnsObj_Scenario0_OnlyFloatingQuestions():
    # ESTABLISH
    alpha_question = QuestionUnit(keg_term="alpha", question_tier=0, init_ch=1)
    beta_question = QuestionUnit(keg_term="beta", question_tier=1, init_ch=10)
    floating_questions = {"beta": beta_question, "alpha": alpha_question}
    fixed_questions = {}

    # WHEN
    result = merge_fixed_and_floating_questions(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [beta_question, alpha_question]


def test_merge_fixed_and_floating_questions_ReturnsObj_Scenario1_FixedQuestionInsertedAtAbsoluteIndex():
    # ESTABLISH
    fixed_question = QuestionUnit(complete_question="Fixed Question")
    alpha_question = QuestionUnit(keg_term="alpha", question_tier=0, init_ch=1)
    beta_question = QuestionUnit(keg_term="beta", question_tier=1, init_ch=10)
    fixed_questions = {1: fixed_question}
    floating_questions = {"beta": beta_question, "alpha": alpha_question}

    # WHEN
    result = merge_fixed_and_floating_questions(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [beta_question, fixed_question, alpha_question]


def test_merge_fixed_and_floating_questions_ReturnsObj_Scenario2_MultipleFixedIndexesRemainAbsolute():
    # ESTABLISH
    fixed_question_b = QuestionUnit(complete_question="Fixed B")
    fixed_question_d = QuestionUnit(complete_question="Fixed D")
    alpha_question = QuestionUnit(keg_term="alpha", question_tier=0, init_ch=1)
    beta_question = QuestionUnit(keg_term="beta", question_tier=1, init_ch=5)
    gamma_question = QuestionUnit(keg_term="gamma", question_tier=1, init_ch=10)

    fixed_questions = {1: fixed_question_b, 3: fixed_question_d}
    floating_questions = {
        "gamma": gamma_question,
        "alpha": alpha_question,
        "beta": beta_question,
    }

    # WHEN
    result = merge_fixed_and_floating_questions(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [
        beta_question,
        fixed_question_b,
        gamma_question,
        fixed_question_d,
        alpha_question,
    ]


def test_rebuild_keg_exam_questions_ReturnsNone_Scenario3_CreatesCsvFile(
    tmp_path,
):
    # ESTABLISH
    output_csv_path = tmp_path / "final_exam_questions.csv"
    # WHEN
    rebuild_keg_exam_questions(output_csv_path=output_csv_path)
    # THEN
    assert output_csv_path.exists()
    kg_df = open_csv(output_csv_path)
    assert list(kg_df.columns) == ["question"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario0_basic_sorting():
    # ESTABLISH
    data = {
        "E": {kw.question_tier: 0, kw.valid_ch: kw.ch20},
        "W": {kw.question_tier: 0, kw.valid_ch: kw.ch03},
        "A": {kw.question_tier: 1, kw.valid_ch: kw.ch02},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["A", "E", "W"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario1_empty_chapter_goes_first_within_tier():
    # ESTABLISH
    data = {
        "E": {kw.question_tier: 0, kw.valid_ch: kw.ch20},
        "W": {kw.question_tier: 0, kw.valid_ch: ""},
        "A": {kw.question_tier: 0, kw.valid_ch: kw.ch03},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["W", "E", "A"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario2_empty_vs_other_tiers():
    # ESTABLISH
    data = {
        "A": {kw.question_tier: 1, kw.valid_ch: ""},
        "B": {kw.question_tier: 0, kw.valid_ch: kw.ch02},
        "C": {kw.question_tier: 0, kw.valid_ch: ""},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    # Tier first, then chapter (empty first within same tier)
    assert result == ["A", "C", "B"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario3_malformed_chapter_treated_like_empty():
    # ESTABLISH
    data = {
        "A": {kw.question_tier: 0, kw.valid_ch: "foo"},
        "B": {kw.question_tier: 0, kw.valid_ch: kw.ch03},
        "C": {kw.question_tier: 0, kw.valid_ch: ""},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
