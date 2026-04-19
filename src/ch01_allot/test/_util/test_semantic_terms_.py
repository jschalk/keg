from ch01_allot._ref.ch01_semantic_types import PoolNum, WeightNum
from inspect import getdoc as inspect_getdoc


def test_PoolNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_PoolNum = PoolNum(x_float)
    # THEN
    assert y_PoolNum == x_float
    inspect_str = (
        """PoolNum represents any possible subset of the sum of numbers in the pool."""
    )
    assert inspect_getdoc(y_PoolNum) == inspect_str


def test_WeightNum_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_weightunit = WeightNum(x_float)
    # THEN
    assert y_weightunit == x_float
    doc_str = """WeightNum represents the unnormalized value of a ledger key. The sum of all WeightNum values in a ledger is not defined."""
    assert inspect_getdoc(y_weightunit) == doc_str
