from src.ch00_py.dict_toolbox import get_None_if_nan
from src.ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum
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
)


class KnotTerm(BreakTerm):
    """A string to used as a delimiter in RopeTerms."""


def default_knot_if_None(knot: any = None) -> str:
    knot = get_None_if_nan(knot)
    return knot if knot is not None else ";"


class LabelTerm(str):
    """A string representation of a tree node. Nodes cannot contain RopeTerm knot"""

    def is_label(self, knot: KnotTerm = None) -> bool:
        return len(self) > 0 and self.contains_knot(knot)

    def contains_knot(self, knot: KnotTerm = None) -> bool:
        return self.find(default_knot_if_None(knot)) == -1


class RopeTerm(str):
    """A string representation of a tree path. LabelTerms are seperated by knots."""

    pass


class FirstLabel(LabelTerm):
    """The first LabelTerm in a RopeTerm. FirstLabel cannot contain knot."""

    pass
