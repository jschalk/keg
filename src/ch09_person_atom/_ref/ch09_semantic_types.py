from ch02_allot._ref.ch02_semantic_types import GrainNum, PoolNum, WeightNum
from ch03_contact._ref.ch03_semantic_types import (
    BossMass,
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
    TrustMass,
)
from ch05_rope._ref.ch05_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from ch06_reason._ref.ch06_semantic_types import FactNum, ReasonNum
from ch08_person_logic._ref.ch08_semantic_types import ManaGrain, PersonName


class CRUD_command(str):
    """database CRUD commands"""

    pass
