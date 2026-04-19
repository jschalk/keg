from ch05_reason._ref.ch05_semantic_types import FactNum, ReasonNum
from inspect import getdoc as inspect_getdoc
from ref.keywords import Ch05Keywords as kw


def test_ReasonNum_Exists():
    # ESTABLISH
    four_int = 4
    # WHEN
    four_reasonnum = ReasonNum(four_int)
    # THEN
    assert four_int == four_reasonnum
    doc_str = """A numeric value that may converted to other Semantic Types by an external process driven by context."""
    assert inspect_getdoc(four_reasonnum) == doc_str


def test_FactNum_Exists():
    # ESTABLISH
    four_int = 4
    # WHEN
    four_factnum = FactNum(four_int)
    # THEN
    assert four_int == four_factnum
    doc_str = """A numeric value that may converted to other Semantic Types by an external process driven by context."""
    assert inspect_getdoc(four_factnum) == doc_str
