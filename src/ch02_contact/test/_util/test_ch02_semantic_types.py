from inspect import getdoc as inspect_getdoc
from src.ch02_contact._ref.ch02_semantic_types import (
    BreakTerm,
    ContactName,
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    RespectGrain,
    RespectNum,
    TitleTerm,
    default_groupmark_if_None,
)
from src.ref.keywords import Ch02Keywords as kw, ExampleStrs as exx


def test_BreakTerm_Exists():
    # ESTABLISH
    semi_colon_str = ";"
    # WHEN
    semi_colon_break = BreakTerm(semi_colon_str)
    # THEN
    assert semi_colon_break == semi_colon_str
    doc_str = "All str separator classes are BreakTerms. Meant to envoke the analogy of the necessity to break experience reality into things so they can be understood."
    assert inspect_getdoc(semi_colon_break) == doc_str


def test_NameTerm_Exists():
    # ESTABLISH
    # WHEN
    bob_nameterm = NameTerm(exx.bob)
    # THEN
    assert bob_nameterm == exx.bob
    doc_str = "All Name string classes should inherit from this class"
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_NameTerm_is_name_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN / THEN
    assert NameTerm("").is_name() is False
    assert NameTerm("A").is_name()

    # WHEN / THEN
    x_s = default_groupmark_if_None()
    x_nameterm = NameTerm(f"casa{x_s}kitchen")
    assert x_nameterm.is_name() is False


def test_HealerName_Exists():
    # ESTABLISH
    # WHEN
    bob_healer_str = HealerName(exx.bob)
    # THEN
    assert bob_healer_str == exx.bob
    doc_str = "A NameTerm used to identify a Problem's Healer"
    assert inspect_getdoc(bob_healer_str) == doc_str


def test_ContactName_Exists():
    # ESTABLISH
    # WHEN
    bob_ContactName = ContactName(exx.bob)
    # THEN
    assert bob_ContactName == exx.bob
    doc_str = "Every ContactName object is NameTerm, must follow NameTerm format."
    assert inspect_getdoc(bob_ContactName) == doc_str


def test_TitleTerm_Exists():
    # ESTABLISH
    # WHEN
    bob_nameterm = TitleTerm(exx.bob)
    # THEN
    assert bob_nameterm == exx.bob
    doc_str = f"""If a TitleTerm contains SepartorTerms(s) it represents a group otherwise its a single member group of an ContactName."""
    assert inspect_getdoc(bob_nameterm) == doc_str


def test_GroupTitle_Exists():
    # ESTABLISH / WHEN
    bikers_GroupTitle = GroupTitle(";bikers")

    # THEN
    assert bikers_GroupTitle is not None


def test_GroupMark_Exists():
    # ESTABLISH / WHEN
    slash_groupmark = GroupMark("/")

    # THEN
    assert slash_groupmark is not None
    doc_str = f"""GroupMark(s) exist in TitleTerms to indicate its a group, no GroupMark indicates it is a ContactName."""
    assert inspect_getdoc(slash_groupmark) == doc_str


def test_default_groupmark_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_groupmark_if_None()
    assert default_groupmark_if_None() == ";"
    assert default_groupmark_if_None(None) == ";"
    assert default_groupmark_if_None("/") == "/"


def test_FundNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_num = FundNum(x_float)
    # THEN
    assert y_fund_num == x_float
    inspect_str = "FundNum inherits from float class"
    assert inspect_getdoc(y_fund_num) == inspect_str


def test_FundGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_fund_grainnum = FundGrain(x_float)
    # THEN
    assert y_fund_grainnum == x_float
    inspect_str = "Smallest Unit of fund_num"
    assert inspect_getdoc(y_fund_grainnum) == inspect_str


def test_RespectGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectGrain = RespectGrain(x_float)
    # THEN
    assert y_RespectGrain == x_float
    inspect_str = (
        "Smallest Unit of score (RespectNum) ala 'the slightest bit of respect!'"
    )
    assert inspect_getdoc(y_RespectGrain) == inspect_str


def test_RespectNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_RespectNum = RespectNum(x_float)
    # THEN
    assert y_RespectNum == x_float
    assert inspect_getdoc(y_RespectNum) == "RespectNum inherits from float class"
