from ch00_py.dict_toolbox import get_empty_dict_if_None
from ch04_rope.rope import (
    KnotTerm,
    RopeTerm,
    default_knot_if_None,
    find_replace_rope_key_dict,
    is_heir_rope,
    rebuild_rope,
    replace_knot,
)
from ch05_reason._ref.ch05_semantic_types import FactNum, ReasonNum
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class InvalidReasonError(Exception):
    pass


@dataclass
class FactCore:
    fact_context: RopeTerm = None
    fact_state: RopeTerm = None
    fact_lower: FactNum = None
    fact_upper: FactNum = None

    def to_dict(self) -> dict[str,]:
        """Returns dict that is serializable to JSON."""
        x_dict = {
            "fact_context": self.fact_context,
            "fact_state": self.fact_state,
        }
        if self.fact_lower is not None:
            x_dict["fact_lower"] = self.fact_lower
        if self.fact_upper is not None:
            x_dict["fact_upper"] = self.fact_upper
        return x_dict

    def set_range_null(self):
        self.fact_lower = None
        self.fact_upper = None

    def set_attr(
        self,
        fact_state: RopeTerm = None,
        fact_lower: FactNum = None,
        fact_upper: FactNum = None,
    ):
        if fact_state is not None:
            self.fact_state = fact_state
        if fact_lower is not None:
            self.fact_lower = fact_lower
        if fact_upper is not None:
            self.fact_upper = fact_upper

    def set_fact_state_to_fact_context(self):
        self.set_attr(fact_state=self.fact_context)
        self.fact_lower = None
        self.fact_upper = None

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.fact_context = rebuild_rope(self.fact_context, old_rope, new_rope)
        self.fact_state = rebuild_rope(self.fact_state, old_rope, new_rope)

    def get_obj_key(self) -> RopeTerm:
        return self.fact_context

    def get_tuple(self) -> tuple[RopeTerm, RopeTerm, float, float]:
        return (self.fact_context, self.fact_state, self.fact_lower, self.fact_upper)


@dataclass
class FactUnit(FactCore):
    pass


def factunit_shop(
    fact_context: RopeTerm = None,
    fact_state: RopeTerm = None,
    fact_lower: FactNum = None,
    fact_upper: FactNum = None,
) -> FactUnit:
    return FactUnit(
        fact_context=fact_context,
        fact_state=fact_state,
        fact_lower=fact_lower,
        fact_upper=fact_upper,
    )


def get_factunits_from_dict(x_dict: dict) -> dict[RopeTerm, FactUnit]:
    facts = {}
    for fact_dict in x_dict.values():
        x_fact_context = fact_dict["fact_context"]
        x_fact_state = fact_dict["fact_state"]

        try:
            x_fact_lower = fact_dict["fact_lower"]
        except KeyError:
            x_fact_lower = None
        try:
            x_fact_upper = fact_dict["fact_upper"]
        except KeyError:
            x_fact_upper = None

        x_fact = factunit_shop(
            fact_context=x_fact_context,
            fact_state=x_fact_state,
            fact_lower=x_fact_lower,
            fact_upper=x_fact_upper,
        )

        facts[x_fact.fact_context] = x_fact
    return facts


def get_factunit_from_tuple(
    fact_tuple: tuple[RopeTerm, RopeTerm, float, float],
) -> FactUnit:
    return factunit_shop(fact_tuple[0], fact_tuple[1], fact_tuple[2], fact_tuple[3])


def get_dict_from_factunits(
    factunits: dict[RopeTerm, FactUnit],
) -> dict[RopeTerm, dict[str,]]:
    return {fact.fact_context: fact.to_dict() for fact in factunits.values()}


@dataclass
class FactHeir(FactCore):
    def mold(self, factunit: FactUnit):
        x_bool = self.fact_lower and factunit.fact_lower and self.fact_upper
        if (
            x_bool
            and self.fact_lower <= factunit.fact_lower
            and self.fact_upper >= factunit.fact_lower
        ):
            self.fact_lower = factunit.fact_lower

    def is_range(self) -> bool:
        return self.fact_lower is not None and self.fact_upper is not None


def factheir_shop(
    fact_context: RopeTerm = None,
    fact_state: RopeTerm = None,
    fact_lower: FactNum = None,
    fact_upper: FactNum = None,
) -> FactHeir:
    return FactHeir(
        fact_context=fact_context,
        fact_state=fact_state,
        fact_lower=fact_lower,
        fact_upper=fact_upper,
    )


class CaseActiveFinderError(Exception):
    pass


@dataclass
class CaseActiveFinder:
    # between 0 and reason_divisor, can be more than reason_upper
    reason_lower: ReasonNum
    # between 0 and reason_divisor, can be less than reason_lower
    reason_upper: ReasonNum
    reason_divisor: float  # greater than zero
    fact_lower_full: FactNum  # less than fact_upper
    fact_upper_full: FactNum

    def check_attr(self):
        if None in (
            self.reason_lower,
            self.reason_upper,
            self.reason_divisor,
            self.fact_lower_full,
            self.fact_upper_full,
        ):
            raise CaseActiveFinderError("No parameter can be None")

        if self.fact_lower_full > self.fact_upper_full:
            raise CaseActiveFinderError(
                f"{self.fact_lower_full=} cannot be greater than {self.fact_upper_full=}"
            )

        if self.reason_divisor <= 0:
            raise CaseActiveFinderError(
                f"{self.reason_divisor=} cannot be less/equal to zero"
            )

        if self.reason_lower < 0 or self.reason_lower > self.reason_divisor:
            raise CaseActiveFinderError(
                f"{self.reason_lower=} cannot be less than zero or greater than {self.reason_divisor=}"
            )

        if self.reason_upper < 0 or self.reason_upper > self.reason_divisor:
            raise CaseActiveFinderError(
                f"{self.reason_upper=} cannot be less than zero or greater than {self.reason_divisor=}"
            )

    def get_fact_lower_remainder(self) -> float:
        return self.fact_lower_full % self.reason_divisor

    def get_fact_upper_remainder(self) -> float:
        return self.fact_upper_full % self.reason_divisor

    def get_active_bool(self) -> bool:
        if self.fact_upper_full - self.fact_lower_full >= self.reason_divisor:
            return True
        elif get_range_less_than_reason_divisor_active(
            fact_lower_remainder=self.get_fact_lower_remainder(),
            fact_upper_remainder=self.get_fact_upper_remainder(),
            reason_lower=self.reason_lower,
            reason_upper=self.reason_upper,
        ):
            return True
        return False

    def get_case_task_bool(self) -> bool:
        if self.get_active_bool():
            x_collasped_fact_range_active = get_collasped_fact_range_active(
                self.reason_lower,
                self.reason_upper,
                self.reason_divisor,
                self.fact_upper_full,
            )
        return self.get_active_bool() and not x_collasped_fact_range_active


def get_range_less_than_reason_divisor_active(
    fact_lower_remainder, fact_upper_remainder, reason_lower, reason_upper
) -> bool:
    fact_lower = fact_lower_remainder
    fact_upper = fact_upper_remainder
    x_bool = False
    if fact_lower <= fact_upper and reason_lower <= reason_upper:
        if (
            (fact_lower >= reason_lower and fact_lower < reason_upper)
            or (fact_upper > reason_lower and fact_upper < reason_upper)
            or (fact_lower < reason_lower and fact_upper > reason_upper)
            or (fact_lower == reason_lower)
        ):
            x_bool = True
    elif fact_lower > fact_upper and reason_lower <= reason_upper:
        if (
            (fact_upper > reason_lower)
            or (fact_lower < reason_upper)
            or (fact_lower == reason_lower)
        ):
            x_bool = True
    elif fact_lower <= fact_upper:
        if (
            (fact_lower < reason_upper)
            or (fact_upper > reason_lower)
            or (fact_lower == reason_lower)
        ):
            x_bool = True
    else:
        x_bool = True
    return x_bool


def get_collasped_fact_range_active(
    reason_lower: ReasonNum,
    reason_upper: ReasonNum,
    reason_divisor: float,
    fact_upper_full: FactNum,
) -> bool:
    x_caseactivefinder = caseactivefinder_shop(
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
        fact_lower_full=fact_upper_full,
        fact_upper_full=fact_upper_full,
    )
    return x_caseactivefinder.get_active_bool()


def caseactivefinder_shop(
    reason_lower: ReasonNum,
    reason_upper: ReasonNum,
    reason_divisor: float,
    fact_lower_full: FactNum,
    fact_upper_full: FactNum,
):
    x_caseactivefinder = CaseActiveFinder(
        reason_lower,
        reason_upper,
        reason_divisor,
        fact_lower_full,
        fact_upper_full,
    )
    x_caseactivefinder.check_attr()
    return x_caseactivefinder


@dataclass
class CaseUnit:
    reason_state: RopeTerm
    reason_lower: ReasonNum = None
    reason_upper: ReasonNum = None
    reason_divisor: int = None
    case_active: bool = None
    case_task: bool = None
    knot: KnotTerm = None

    def get_obj_key(self):
        return self.reason_state

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"reason_state": self.reason_state}
        if self.reason_lower is not None:
            x_dict["reason_lower"] = self.reason_lower
        if self.reason_upper is not None:
            x_dict["reason_upper"] = self.reason_upper

        if self.reason_divisor is not None:
            x_dict["reason_divisor"] = self.reason_divisor

        return x_dict

    def clear_case_active(self):
        self.case_active = None

    def set_knot(self, new_knot: KnotTerm):
        old_knot = copy_deepcopy(self.knot)
        self.knot = new_knot
        self.reason_state = replace_knot(
            rope=self.reason_state, old_knot=old_knot, new_knot=self.knot
        )

    def is_in_lineage(self, fact_state: RopeTerm):
        return is_heir_rope(
            src=self.reason_state, heir=fact_state, knot=self.knot
        ) or is_heir_rope(src=fact_state, heir=self.reason_state, knot=self.knot)

    def set_case_active(self, x_factheir: FactHeir):
        self.case_active = self._get_active(factheir=x_factheir)
        self.case_task = self._get_case_task_bool(factheir=x_factheir)

    def _get_active(self, factheir: FactHeir) -> bool:
        x_case_active = None
        # case_active might be true if case is in lineage of fact
        if factheir is None:
            x_case_active = False
        elif self.is_in_lineage(fact_state=factheir.fact_state):
            if self._is_range_or_segregate() is False:
                x_case_active = True
            elif self._is_range_or_segregate() and factheir.is_range() is False:
                x_case_active = False
            elif self._is_range_or_segregate() and factheir.is_range():
                x_case_active = self._get_range_segregate_case_active(factheir=factheir)
        elif self.is_in_lineage(fact_state=factheir.fact_state) is False:
            x_case_active = False

        return x_case_active

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return (
            self.reason_divisor is not None
            and self.reason_lower is not None
            and self.reason_upper is not None
        )

    def _is_range(self):
        return (
            self.reason_divisor is None
            and self.reason_lower is not None
            and self.reason_upper is not None
        )

    def _get_case_task_bool(self, factheir: FactHeir) -> bool:
        x_case_task = None
        if self.case_active and self._is_range():
            x_case_task = factheir.fact_upper > self.reason_upper
        elif self.case_active and self._is_segregate():
            segr_obj = caseactivefinder_shop(
                reason_lower=self.reason_lower,
                reason_upper=self.reason_upper,
                reason_divisor=self.reason_divisor,
                fact_lower_full=factheir.fact_lower,
                fact_upper_full=factheir.fact_upper,
            )
            x_case_task = segr_obj.get_case_task_bool()
        elif self.case_active in [True, False]:
            x_case_task = False

        return x_case_task

    def _get_range_segregate_case_active(self, factheir: FactHeir) -> bool:
        x_case_active = None
        if self._is_range():
            x_case_active = self._get_range_case_active(factheir=factheir)
        elif self._is_segregate():
            x_case_active = self._get_segregate_case_active(factheir=factheir)

        return x_case_active

    def _get_segregate_case_active(self, factheir: FactHeir) -> bool:
        segr_obj = caseactivefinder_shop(
            reason_lower=self.reason_lower,
            reason_upper=self.reason_upper,
            reason_divisor=self.reason_divisor,
            fact_lower_full=factheir.fact_lower,
            fact_upper_full=factheir.fact_upper,
        )
        return segr_obj.get_active_bool()

    def _get_range_case_active(self, factheir: FactHeir) -> bool:
        return (
            (
                self.reason_lower <= factheir.fact_lower
                and self.reason_upper > factheir.fact_lower
            )
            or (
                self.reason_lower <= factheir.fact_upper
                and self.reason_upper > factheir.fact_upper
            )
            or (
                self.reason_lower >= factheir.fact_lower
                and self.reason_upper < factheir.fact_upper
            )
        )

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.reason_state = rebuild_rope(self.reason_state, old_rope, new_rope)


# class casesshop:
def caseunit_shop(
    reason_state: RopeTerm,
    reason_lower: ReasonNum = None,
    reason_upper: ReasonNum = None,
    reason_divisor: float = None,
    knot: KnotTerm = None,
) -> CaseUnit:
    return CaseUnit(
        reason_state=reason_state,
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
        knot=default_knot_if_None(knot),
    )


def cases_get_from_dict(x_dict: dict) -> dict[str, CaseUnit]:
    cases = {}
    for case_dict in x_dict.values():
        try:
            x_reason_lower = case_dict["reason_lower"]
        except KeyError:
            x_reason_lower = None
        try:
            x_reason_upper = case_dict["reason_upper"]
        except KeyError:
            x_reason_upper = None
        try:
            x_reason_divisor = case_dict["reason_divisor"]
        except KeyError:
            x_reason_divisor = None

        case_x = caseunit_shop(
            reason_state=case_dict["reason_state"],
            reason_lower=x_reason_lower,
            reason_upper=x_reason_upper,
            reason_divisor=x_reason_divisor,
        )
        cases[case_x.reason_state] = case_x
    return cases


@dataclass
class ReasonCore:
    reason_context: RopeTerm
    cases: dict[RopeTerm, CaseUnit]
    active_requisite: bool = None
    knot: KnotTerm = None

    def set_knot(self, new_knot: KnotTerm):
        old_knot = copy_deepcopy(self.knot)
        self.knot = new_knot
        self.reason_context = replace_knot(self.reason_context, old_knot, new_knot)

        new_cases = {}
        for case_rope, case_obj in self.cases.items():
            new_case_rope = replace_knot(
                rope=case_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            case_obj.set_knot(self.knot)
            new_cases[new_case_rope] = case_obj
        self.cases = new_cases

    def get_obj_key(self):
        return self.reason_context

    def get_cases_count(self):
        return sum(1 for _ in self.cases.values())

    def set_case(
        self,
        case: RopeTerm,
        reason_lower: ReasonNum = None,
        reason_upper: ReasonNum = None,
        reason_divisor: int = None,
    ):
        self.cases[case] = caseunit_shop(
            reason_state=case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
            knot=self.knot,
        )

    def case_exists(self, reason_state: RopeTerm) -> bool:
        return self.cases.get(reason_state) != None

    def get_case(self, case: RopeTerm) -> CaseUnit:
        return self.cases.get(case)

    def del_case(self, case: RopeTerm):
        try:
            self.cases.pop(case)
        except KeyError as e:
            raise InvalidReasonError(f"Reason unable to delete case {e}") from e

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.reason_context = rebuild_rope(self.reason_context, old_rope, new_rope)
        self.cases = find_replace_rope_key_dict(
            dict_x=self.cases, old_rope=old_rope, new_rope=new_rope
        )


def reasoncore_shop(
    reason_context: RopeTerm,
    cases: dict[RopeTerm, CaseUnit] = None,
    active_requisite: bool = None,
    knot: KnotTerm = None,
):
    return ReasonCore(
        reason_context=reason_context,
        cases=get_empty_dict_if_None(cases),
        active_requisite=active_requisite,
        knot=default_knot_if_None(knot),
    )


@dataclass
class ReasonUnit(ReasonCore):
    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        cases_dict = {
            case_rope: case.to_dict() for case_rope, case in self.cases.items()
        }
        x_dict = {"reason_context": self.reason_context}
        if cases_dict != {}:
            x_dict["cases"] = cases_dict
        if self.active_requisite is not None:
            x_dict["active_requisite"] = self.active_requisite
        return x_dict


def reasonunit_shop(
    reason_context: RopeTerm,
    cases: dict[RopeTerm, CaseUnit] = None,
    active_requisite: bool = None,
    knot: KnotTerm = None,
):
    return ReasonUnit(
        reason_context=reason_context,
        cases=get_empty_dict_if_None(cases),
        active_requisite=active_requisite,
        knot=default_knot_if_None(knot),
    )


@dataclass
class ReasonHeir(ReasonCore):
    reason_active: bool = None
    reason_task: bool = None
    parent_heir_active: bool = None

    def inherit_from_reasonheir(self, x_reasonunit: ReasonUnit):
        x_cases = {}
        for x_caseunit in x_reasonunit.cases.values():
            case_x = caseunit_shop(
                reason_state=x_caseunit.reason_state,
                reason_lower=x_caseunit.reason_lower,
                reason_upper=x_caseunit.reason_upper,
                reason_divisor=x_caseunit.reason_divisor,
            )
            x_cases[case_x.reason_state] = case_x
        self.cases = x_cases

    def clear_reason_active(self):
        self.reason_active = None
        for case in self.cases.values():
            case.clear_case_active()

    def set_cases_case_active(self, factheir: FactHeir):
        for case in self.cases.values():
            case.set_case_active(factheir)

    def _get_fact_context(self, factheirs: dict[RopeTerm, FactHeir]) -> FactHeir:
        fact_context = None
        factheirs = get_empty_dict_if_None(factheirs)
        for y_factheir in factheirs.values():
            if self.reason_context == y_factheir.fact_context:
                fact_context = y_factheir
        return fact_context

    def set_heir_active(self, bool_x: bool):
        self.parent_heir_active = bool_x

    def is_active_requisite_operational(self) -> bool:
        return (
            self.parent_heir_active is not None
            and self.parent_heir_active == self.active_requisite
        )

    def is_any_case_true(self) -> tuple[bool, bool]:
        any_case_true = False
        any_case_task_true = False
        for x_caseunit in self.cases.values():
            if x_caseunit.case_active:
                any_case_true = True
                if x_caseunit.case_task:
                    any_case_task_true = True
        return any_case_true, any_case_task_true

    def set_attr_reason_active(self, any_case_true: bool):
        self.reason_active = any_case_true or self.is_active_requisite_operational()

    def set_attr_reason_task(self, any_case_task_true: bool):
        self.reason_task = True if any_case_task_true else None
        if self.reason_active and self.reason_task is None:
            self.reason_task = False

    def set_reason_active(self, factheirs: dict[RopeTerm, FactHeir]):
        self.clear_reason_active()
        self.set_cases_case_active(self._get_fact_context(factheirs))
        any_case_true, any_case_task_true = self.is_any_case_true()
        self.set_attr_reason_active(any_case_true)
        self.set_attr_reason_task(any_case_task_true)


def reasonheir_shop(
    reason_context: RopeTerm,
    cases: dict[RopeTerm, CaseUnit] = None,
    active_requisite: bool = None,
    reason_active: bool = None,
    reason_task: bool = None,
    parent_heir_active: bool = None,
    knot: KnotTerm = None,
):
    return ReasonHeir(
        reason_context=reason_context,
        cases=get_empty_dict_if_None(cases),
        active_requisite=active_requisite,
        reason_active=reason_active,
        reason_task=reason_task,
        parent_heir_active=parent_heir_active,
        knot=default_knot_if_None(knot),
    )


def get_reasonunits_from_dict(reasons_dict: dict) -> dict[RopeTerm, ReasonUnit]:
    x_dict = {}
    for reason_dict in reasons_dict.values():
        x_reasonunit = reasonunit_shop(reason_context=reason_dict["reason_context"])
        if reason_dict.get("cases") is not None:
            x_reasonunit.cases = cases_get_from_dict(x_dict=reason_dict["cases"])
        if reason_dict.get("active_requisite") is not None:
            x_reasonunit.active_requisite = reason_dict.get("active_requisite")
        x_dict[x_reasonunit.reason_context] = x_reasonunit
    return x_dict
