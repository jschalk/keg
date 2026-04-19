from ch09_person_lesson._ref.ch09_semantic_types import MomentRope
from inspect import getdoc as inspect_getdoc
from ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_MomentRope_Exists():
    # ESTABLISH
    # WHEN
    bob_MomentRope_str = MomentRope(exx.bob)
    # THEN
    assert bob_MomentRope_str == exx.bob
    doc_str = f"The {kw.RopeTerm} for a Moment. Must contain knots."
    assert inspect_getdoc(bob_MomentRope_str) == doc_str
