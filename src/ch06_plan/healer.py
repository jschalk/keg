from ch00_py.dict_toolbox import get_empty_set_if_None
from ch06_plan._ref.ch06_semantic_types import GroupTitle
from dataclasses import dataclass


@dataclass
class HealerUnit:
    healer_names: set[GroupTitle]

    def set_healer_name(self, x_healer_name: GroupTitle):
        self.healer_names.add(x_healer_name)

    def healer_name_exists(self, x_healer_name: GroupTitle) -> bool:
        return x_healer_name in self.healer_names

    def any_healer_name_exists(self) -> bool:
        return len(self.healer_names) > 0

    def del_healer_name(self, x_healer_name: GroupTitle):
        self.healer_names.remove(x_healer_name)

    def to_dict(self) -> dict[str, list[GroupTitle]]:
        """Returns dict that is serializable to JSON."""

        return {"healerunit_healer_names": list(self.healer_names)}


def healerunit_shop(healer_names: set[GroupTitle] = None) -> HealerUnit:
    return HealerUnit(healer_names=get_empty_set_if_None(healer_names))


def get_healerunit_from_dict(x_dict: dict[str, set]) -> HealerUnit:
    x_healerunit = healerunit_shop()
    if x_dict.get("healerunit_healer_names") is not None:
        for x_healer_name in x_dict.get("healerunit_healer_names"):
            x_healerunit.set_healer_name(x_healer_name=x_healer_name)
    return x_healerunit
