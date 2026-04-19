from ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum
from ch01_allot.allot import (
    default_grain_num_if_None,
    default_pool_num,
    valid_allotment_ratio,
    validate_pool_num,
)
from inspect import getdoc as inspect_getdoc


def test_GrainNum_Exists():
    # ESTABLISH
    x_float = 2.45
    # WHEN
    x_GrainNum = GrainNum(x_float)
    # THEN
    assert x_float == x_GrainNum
    doc_str = "GrainNum represents the smallest fraction allowed"
    assert inspect_getdoc(x_GrainNum) == doc_str


def test_default_grain_num_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_grain_num_if_None() == 1
    assert default_grain_num_if_None(5) == 5
    assert default_grain_num_if_None(0.03) == 0.03


def test_default_pool_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_pool_num() == 1000000000


def test_validate_pool_num_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert validate_pool_num() == default_pool_num()
    assert validate_pool_num(None) == default_pool_num()
    assert validate_pool_num(0.5) == default_grain_num_if_None()
    assert (
        validate_pool_num(default_grain_num_if_None() - 0.01)
        == default_grain_num_if_None()
    )
    assert validate_pool_num(1) == 1
    assert validate_pool_num(25) == 25


def test_valid_allotment_ratio_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert valid_allotment_ratio(10, 1)
    assert valid_allotment_ratio(10, 3) is False
    assert valid_allotment_ratio(10.1, 1) is False
    assert valid_allotment_ratio(10.1, 0.1) is False
    inspect_str = """Checks that big_number is wholly divisible by grain_num"""
    assert inspect_getdoc(valid_allotment_ratio) == inspect_str
