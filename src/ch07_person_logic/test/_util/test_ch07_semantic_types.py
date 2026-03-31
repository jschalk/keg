from inspect import getdoc as inspect_getdoc
from src.ch07_person_logic._ref.ch07_semantic_types import ManaGrain, PersonName
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PersonName_Exists():
    # ESTABLISH
    # WHEN
    bob_PersonName_str = PersonName(exx.bob)
    # THEN
    assert bob_PersonName_str == exx.bob
    doc_str = f"""The {kw.LabelTerm} used to identify a PersonUnit.
Must be a {kw.LabelTerm}/{kw.NameTerm} because when identifying if a PlanUnit is an active {kw.pledge} the {kw.PersonName} will be compared
against {kw.ContactName}s. If they match the {kw.pledge} will be active."""
    assert inspect_getdoc(bob_PersonName_str) == doc_str


def test_ManaGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_mana_grain = ManaGrain(x_float)
    # THEN
    assert y_mana_grain == x_float
    assert inspect_getdoc(y_mana_grain) == "Smallest Unit of Mana"
