from pytest import raises as pytest_raises
from pandas import DataFrame
from pandas import ExcelWriter as pandas_ExcelWriter
from io import BytesIO as io_BytesIO

from ch97_docs_builder.glossary_ranking import load_keg_knowledge as load_keg_knowledge

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_excel(rows: list[dict]) -> io_BytesIO:
    """Build an in-memory Excel file with a 'keg_knowledge' sheet."""
    df = DataFrame(rows, columns=["keg_question", "answer"])
    buf = io_BytesIO()
    with pandas_ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="keg_knowledge", index=False)
    buf.seek(0)
    return buf


def call(rows: list[dict]) -> DataFrame:
    """Convenience: build an Excel buffer and call load_keg_knowledge."""
    return load_keg_knowledge(make_excel(rows))


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------


def test_load_keg_knowledge_ReturnsDataFrame_Scenario00_SingleRow():
    # ESTABLISH / WHEN
    result = call([{"keg_question": "Q1", "answer": "yes"}])
    # THEN
    assert isinstance(result, DataFrame)


def test_load_keg_knowledge_ReturnsColumns_Scenario01_ColumnsAreKegQuestionAndAnswer():
    # ESTABLISH / WHEN
    result = call([{"keg_question": "Q1", "answer": "yes"}])
    # THEN
    assert list(result.columns) == ["keg_question", "answer"]


def test_load_keg_knowledge_ReturnsRow_Scenario02_SingleRowValuesPreserved():
    # ESTABLISH / WHEN
    result = call([{"keg_question": "Q1", "answer": "yes"}])
    # THEN
    assert len(result) == 1
    assert result.iloc[0]["keg_question"] == "Q1"
    assert result.iloc[0]["answer"] == "yes"


def test_load_keg_knowledge_ReturnsAllRows_Scenario03_MultipleDistinctQuestionsKept():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q2", "answer": "yes"},
        {"keg_question": "Q3", "answer": "yes"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert set(result["keg_question"]) == {"Q1", "Q2", "Q3"}


# ---------------------------------------------------------------------------
# Deduplication tests
# ---------------------------------------------------------------------------


def test_load_keg_knowledge_ReturnsOneRow_Scenario04_ExactDuplicatePairCollapsed():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q1", "answer": "yes"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert len(result) == 1


def test_load_keg_knowledge_ReturnsOneRow_Scenario05_ManyExactDuplicatesCollapsed():
    # ESTABLISH
    rows = [{"keg_question": "Q1", "answer": "yes"}] * 5
    # WHEN
    result = call(rows)
    # THEN
    assert len(result) == 1


# ---------------------------------------------------------------------------
# Conflict-removal tests (multiple distinct answers → drop)
# ---------------------------------------------------------------------------


def test_load_keg_knowledge_ReturnsEmpty_Scenario06_QuestionWithTwoDistinctAnswersRemoved():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q1", "answer": "no"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert "Q1" not in result["keg_question"].values


def test_load_keg_knowledge_ReturnsCleanQuestion_Scenario07_ConflictingRemovedButCleanKept():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q1", "answer": "no"},
        {"keg_question": "Q2", "answer": "yes"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert "Q1" not in result["keg_question"].values
    assert "Q2" in result["keg_question"].values


def test_load_keg_knowledge_ReturnsEmptyDataFrame_Scenario08_AllQuestionsConflicting():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q1", "answer": "no"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert len(result) == 0


# ---------------------------------------------------------------------------
# Whitespace normalisation tests
# ---------------------------------------------------------------------------


def test_load_keg_knowledge_ReturnsStrippedAnswer_Scenario09_AnswerWhitespaceStripped():
    # ESTABLISH
    rows = [{"keg_question": "Q1", "answer": "  yes  "}]
    # WHEN
    result = call(rows)
    # THEN
    assert result.iloc[0]["answer"] == "yes"


def test_load_keg_knowledge_ReturnsStrippedQuestion_Scenario10_QuestionWhitespaceStripped():
    # ESTABLISH
    rows = [{"keg_question": "  Q1  ", "answer": "yes"}]
    # WHEN
    result = call(rows)
    # THEN
    assert result.iloc[0]["keg_question"] == "Q1"


def test_load_keg_knowledge_ReturnsOneRow_Scenario11_WhitespaceVariantsTreatedAsDuplicates():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q1", "answer": " yes "},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert len(result) == 1


# ---------------------------------------------------------------------------
# Case normalisation tests
# ---------------------------------------------------------------------------


def test_load_keg_knowledge_ReturnsLowercasedAnswer_Scenario12_AnswerUppercaseLowercased():
    # ESTABLISH
    rows = [{"keg_question": "Q1", "answer": "YES"}]
    # WHEN
    result = call(rows)
    # THEN
    assert result.iloc[0]["answer"] == "yes"


def test_load_keg_knowledge_ReturnsOneRow_Scenario13_MixedCaseAnswersTreatedAsDuplicates():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "Yes"},
        {"keg_question": "Q1", "answer": "YES"},
        {"keg_question": "Q1", "answer": "yes"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert len(result) == 1


def test_load_keg_knowledge_ReturnsEmpty_Scenario14_MixedCaseYesAndNoTreatedAsConflict():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "Yes"},
        {"keg_question": "Q1", "answer": "NO"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert "Q1" not in result["keg_question"].values


# ---------------------------------------------------------------------------
# Edge-case tests
# ---------------------------------------------------------------------------


def test_load_keg_knowledge_ReturnsEmptyDataFrame_Scenario15_EmptySheetReturnsEmpty():
    # ESTABLISH / WHEN
    result = call([])
    # THEN
    assert isinstance(result, DataFrame)
    assert len(result) == 0


def test_load_keg_knowledge_ReturnsResetIndex_Scenario16_IndexIsResetAfterDrops():
    # ESTABLISH
    rows = [
        {"keg_question": "Q1", "answer": "yes"},
        {"keg_question": "Q1", "answer": "no"},
        {"keg_question": "Q2", "answer": "yes"},
    ]
    # WHEN
    result = call(rows)
    # THEN
    assert list(result.index) == list(range(len(result)))


def test_load_keg_knowledge_RaisesException_Scenario17_MissingSheetRaises():
    # ESTABLISH
    df = DataFrame([{"keg_question": "Q1", "answer": "yes"}])
    buf = io_BytesIO()
    with pandas_ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="wrong_sheet", index=False)
    buf.seek(0)
    # WHEN / THEN
    with pytest_raises(Exception):
        load_keg_knowledge(buf)
