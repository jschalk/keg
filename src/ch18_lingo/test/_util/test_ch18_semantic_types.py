from ch18_lingo._ref.ch18_semantic_types import AudieTitle, FlareInt
from ch99_glossary.ch_keyword import Ch03Keywords as kw, ExampleStrs as exx
from inspect import getdoc as inspect_getdoc


def test_AudieTitle_Exists():
    # ESTABLISH
    # WHEN
    bob_audietitle = AudieTitle(exx.bob)
    # THEN
    assert bob_audietitle == exx.bob
    doc_str = """If a AudieTitle contains SepartorTerms(s) it represents a group otherwise its a single member group of an ContactName."""
    assert inspect_getdoc(bob_audietitle) == doc_str


def test_FlareInt_Exists():
    # ESTABLISH
    # WHEN
    two_flareint = FlareInt(2)
    # THEN
    assert two_flareint == 2
    doc_str = """Integer for tracking Flares."""
    assert inspect_getdoc(two_flareint) == doc_str
