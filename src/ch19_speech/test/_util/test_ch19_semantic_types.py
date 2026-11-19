from ch19_speech._ref.ch19_semantic_types import AudieTitle, SongInt
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


def test_SongInt_Exists():
    # ESTABLISH
    # WHEN
    two_songint = SongInt(2)
    # THEN
    assert two_songint == 2
    doc_str = """Integer for tracking Songs."""
    assert inspect_getdoc(two_songint) == doc_str
