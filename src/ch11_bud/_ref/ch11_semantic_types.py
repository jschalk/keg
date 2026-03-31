from src.ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum
from src.ch02_contact._ref.ch02_semantic_types import (
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
from src.ch04_rope._ref.ch04_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from src.ch07_person_logic._ref.ch07_semantic_types import ManaGrain, PersonName
from src.ch08_person_atom._ref.ch08_semantic_types import CRUD_command
from src.ch09_person_lesson._ref.ch09_semantic_types import FaceName, MomentRope


class TimeNum(int):
    """An Integar that can represent a instant on the TimeNumLine"""

    pass


class SparkInt(int):
    """Each Spark is a int that describes the order of data ingestion"""

    pass
