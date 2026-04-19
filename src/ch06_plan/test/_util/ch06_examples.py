from ch06_plan.plan import PlanUnit
from dataclasses import dataclass


@dataclass
class RangeAttrHolder:
    begin: float = None
    close: float = None
    addin: float = None
    denom: int = None
    numor: int = None
    morph: bool = None
    gogo_want: float = None
    stop_want: float = None
    gogo_calc: float = None
    stop_calc: float = None


def get_range_attrs(x_plan: PlanUnit) -> RangeAttrHolder:
    return RangeAttrHolder(
        begin=x_plan.begin,
        close=x_plan.close,
        addin=x_plan.addin,
        denom=x_plan.denom,
        numor=x_plan.numor,
        morph=x_plan.morph,
        gogo_want=x_plan.gogo_want,
        stop_want=x_plan.stop_want,
        gogo_calc=x_plan.gogo_calc,
        stop_calc=x_plan.stop_calc,
    )
