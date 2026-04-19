from ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum
from ch02_contact._ref.ch02_semantic_types import (
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
from ch04_rope._ref.ch04_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from ch05_reason._ref.ch05_semantic_types import FactNum, ReasonNum


class PersonName(LabelTerm):
    """The LabelTerm used to identify a PersonUnit.
    Must be a LabelTerm/NameTerm because when identifying if a PlanUnit is an active pledge the PersonName will be compared
    against ContactNames. If they match the pledge will be active."""

    pass


class ManaGrain(float):
    """Smallest Unit of Mana"""

    pass
