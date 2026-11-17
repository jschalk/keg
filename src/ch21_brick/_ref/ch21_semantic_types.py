from ch02_allot._ref.ch02_semantic_types import GrainNum, PoolNum, WeightNum
from ch03_contact._ref.ch03_semantic_types import (
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
from ch05_rope._ref.ch05_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from ch08_person_logic._ref.ch08_semantic_types import ManaGrain, PersonName
from ch09_person_atom._ref.ch09_semantic_types import CRUD_command
from ch10_person_lesson._ref.ch10_semantic_types import FaceName, MomentRope
from ch12_bud._ref.ch12_semantic_types import SparkInt, TimeNum
from ch13_keep._ref.ch13_semantic_types import ManaNum
from ch14_time._ref.ch14_semantic_types import EpochLabel


class SheetName(str):
    """A string used as SheetName for SpreadSheet files."""

    pass
