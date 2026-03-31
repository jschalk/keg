from src.ch00_py.dict_toolbox import get_None_if_nan
from src.ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum


class BreakTerm(str):
    """All str separator classes are BreakTerms. Meant to envoke the analogy of the necessity to break experience reality into things so they can be understood."""

    pass


class GroupMark(BreakTerm):
    """GroupMark(s) exist in TitleTerms to indicate its a group, no GroupMark indicates it is a ContactName."""

    pass


def default_groupmark_if_None(groupmark: GroupMark = None) -> GroupMark:
    groupmark = get_None_if_nan(groupmark)
    return groupmark if groupmark is not None else ";"


class NameTerm(str):
    """All Name string classes should inherit from this class"""

    def is_name(self, groupmark: GroupMark = None) -> bool:
        return len(self) > 0 and self.contains_groupmark(groupmark)

    def contains_groupmark(self, groupmark: str = None) -> bool:
        return self.find(default_groupmark_if_None(groupmark)) == -1


class ContactName(NameTerm):
    """Every ContactName object is NameTerm, must follow NameTerm format."""

    pass


class TitleTerm(str):
    """If a TitleTerm contains SepartorTerms(s) it represents a group otherwise its a single member group of an ContactName."""


class GroupTitle(TitleTerm):
    """If contains SepartorTerms(s) it represents a group otherwise its a ContactName."""

    pass


class HealerName(NameTerm):
    """A NameTerm used to identify a Problem's Healer"""

    pass


class FundNum(float):
    """FundNum inherits from float class"""

    pass


class FundGrain(float):
    """Smallest Unit of fund_num"""

    pass


class RespectNum(float):
    """RespectNum inherits from float class"""

    pass


class RespectGrain(float):
    """Smallest Unit of score (RespectNum) ala 'the slightest bit of respect!'"""

    pass
