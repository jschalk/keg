from copy import deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_False_if_None,
    get_positive_int,
)
from src.ch01_allot.allot import allot_scale, default_grain_num_if_None
from src.ch02_contact.group import (
    AwardHeir,
    AwardLine,
    AwardUnit,
    GroupUnit,
    awardheir_shop,
    awardline_shop,
    get_awardunits_from_dict,
)
from src.ch03_workforce.workforce import (
    WorkforceHeir,
    WorkforceUnit,
    get_workforceunit_from_dict,
    workforceheir_shop,
    workforceunit_shop,
)
from src.ch04_rope.rope import (
    all_ropes_between,
    create_rope,
    find_replace_rope_key_dict,
    is_sub_rope,
    rebuild_rope,
    replace_knot,
)
from src.ch05_reason.reason_main import (
    FactCore,
    FactHeir,
    FactUnit,
    ReasonCore,
    ReasonHeir,
    ReasonUnit,
    RopeTerm,
    factheir_shop,
    factunit_shop,
    get_dict_from_factunits,
    get_factunits_from_dict,
    get_reasonunits_from_dict,
    reasonheir_shop,
    reasonunit_shop,
)
from src.ch06_plan._ref.ch06_semantic_types import (
    ContactName,
    FundGrain,
    FundNum,
    GroupTitle,
    KnotTerm,
    LabelTerm,
    ReasonNum,
    RopeTerm,
    default_knot_if_None,
)
from src.ch06_plan.healer import HealerUnit, get_healerunit_from_dict, healerunit_shop
from src.ch06_plan.range_toolbox import RangeUnit, get_morphed_rangeunit


class InvalidPlanError(Exception):
    pass


class PlanetDescendantsError(Exception):
    pass


class PlanLabelNotEmptyError(Exception):
    pass


class RangedFactPlanError(Exception):
    pass


@dataclass
class PlanAttrHolder:
    star: int = None
    plan_uid: int = None
    reason: ReasonUnit = None
    reason_context: RopeTerm = None
    reason_case: RopeTerm = None
    reason_lower: ReasonNum = None
    reason_upper: ReasonNum = None
    reason_divisor: int = None
    reason_del_case_reason_context: RopeTerm = None
    reason_del_case_reason_state: RopeTerm = None
    reason_requisite_active: str = None
    workforceunit: WorkforceUnit = None
    healerunit: HealerUnit = None
    begin: float = None
    close: float = None
    gogo_want: float = None
    stop_want: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    morph: bool = None
    pledge: bool = None
    factunit: FactUnit = None
    awardunit: AwardUnit = None
    awardunit_del: GroupTitle = None
    is_expanded: bool = None
    problem_bool: bool = None

    def set_case_range_influenced_by_case_plan(
        self,
        reason_lower,
        reason_upper,
        case_denom,
    ):
        if self.reason_case is not None:
            if self.reason_lower is None:
                self.reason_lower = reason_lower
            if self.reason_upper is None:
                self.reason_upper = reason_upper
            if self.reason_divisor is None:
                self.reason_divisor = case_denom


def planattrholder_shop(
    star: int = None,
    plan_uid: int = None,
    reason: ReasonUnit = None,
    reason_context: RopeTerm = None,
    reason_case: RopeTerm = None,
    reason_lower: ReasonNum = None,
    reason_upper: ReasonNum = None,
    reason_divisor: int = None,
    reason_del_case_reason_context: RopeTerm = None,
    reason_del_case_reason_state: RopeTerm = None,
    reason_requisite_active: str = None,
    workforceunit: WorkforceUnit = None,
    healerunit: HealerUnit = None,
    begin: float = None,
    close: float = None,
    gogo_want: float = None,
    stop_want: float = None,
    addin: float = None,
    numor: float = None,
    denom: float = None,
    morph: bool = None,
    pledge: bool = None,
    factunit: FactUnit = None,
    awardunit: AwardUnit = None,
    awardunit_del: GroupTitle = None,
    is_expanded: bool = None,
    problem_bool: bool = None,
) -> PlanAttrHolder:
    return PlanAttrHolder(
        star=star,
        plan_uid=plan_uid,
        reason=reason,
        reason_context=reason_context,
        reason_case=reason_case,
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
        reason_del_case_reason_context=reason_del_case_reason_context,
        reason_del_case_reason_state=reason_del_case_reason_state,
        reason_requisite_active=reason_requisite_active,
        workforceunit=workforceunit,
        healerunit=healerunit,
        begin=begin,
        close=close,
        gogo_want=gogo_want,
        stop_want=stop_want,
        addin=addin,
        numor=numor,
        denom=denom,
        morph=morph,
        pledge=pledge,
        factunit=factunit,
        awardunit=awardunit,
        awardunit_del=awardunit_del,
        is_expanded=is_expanded,
        problem_bool=problem_bool,
    )


@dataclass
class PlanUnit:
    """
    Represents a planual unit within keg. Can represent a pledge, a plan_task, a different plan's
    reason or fact, a parent plan of other plans.
    Funds: Funds come from the parent plan and go to the child plans.
    Awards: Desribes whom the funding comes from and whome it goes to.
    Pledges: A plan can declare itself a pledge. It can be active or not active.
      Pledge Reason: A plan can require that all reasons be active to be active. (No reasons=active)
      Pledge Fact: Each reason checks facts to determine if it is active.


    funding, and hierarchical relationships.

    Attributes
    ----------
    plan_label : LabelTerm of plan.
    parent_rope : RopeTerm that this plan stems from. Empty string for root plans.
    knot : str Identifier or label for bridging plans.
    optional:
    star : int weight that is arbitrary used by parent plan to calculated relative importance.
    kids : dict[LabelTerm, PlanUnit], mapping of child plans by their LabelTerm
    plan_uid : int Unique identifier, forgot how I use this.
    awardunits : dict[GroupTitle, AwardUnit] that describe who funds and who is funded
    reasonunits : dict[RopeTerm, ReasonUnit] that stores all reasons
    workforceunit : WorkforceUnit that describes whom this pledge is for. WorkforceUnit.labors: dict[GroupTitle, LaborUnit]
    factunits : dict[RopeTerm, FactUnit] that stores all facts
    healerunit : HealerUnit, if a ancestor plan is a problem, this can donote a healing plan.
    begin : float that describes the begin of a numerical range if it exists
    close : float that describes the close of a numerical range if it exists
    addin : float that describes addition to parent range calculations
    denom : int that describes denominator to parent range calculations
    numor : int that describes numerator to parent range calculations
    morph : bool that describes how to change parent range in calculations.
    gogo_want : float
    stop_want : float
    pledge : bool that describes if the plan is a pledge.
    problem_bool : bool that describes if the plan is a problem.
    is_expanded : bool flag that can be used by UI to display or high tree branch.

    active : bool that describes if the plan pledge is plan_active, conpute.
    active_hx : dict[int, bool] Historical record of active state, used to track changes between tree_traverses
    all_contact_cred : bool Flag indicating there are not explicitley defined awardunits
    all_contact_debt : bool Flag indicating there are not explicitley defined awardunits
    awardheirs : dict[GroupTitle, AwardHeir] parent plan provided awards.
    awardlines : dict[GroupTitle, AwardLine] child plan provided awards.
    descendant_pledge_count : int Count of descendant plans marked as pledges.
    factheirs : dict[RopeTerm, FactHeir] parent plan provided facts.
    fund_ratio : float
    fund_grain : FundGrain Smallest indivisible funding component.
    fund_onset : FundNum number at which funding onsets inside master funding range, conpute
    fund_cease : FundNum number at which funding ceases inside master funding range, conpute
    healerunit_ratio : float
    tree_level : int that describes Depth tree_level in plan hierarchy.
    range_evaluated : bool Flag indicating whether range has been evaluated.
    reasonheirs : dict[RopeTerm, ReasonHeir] parent plan provided reasoning branches.
    plan_task : bool describes if a unit can be changed to inactive with fact range change.
    workforceheir : WorkforceHeir parent plan provided workforce relationships
    gogo_calc : float
    stop_calc : float
    """

    plan_label: LabelTerm = None
    parent_rope: RopeTerm = None
    knot: KnotTerm = None
    kids: dict[LabelTerm,] = None
    star: int = None
    plan_uid: int = None  # Calculated field?
    awardunits: dict[GroupTitle, AwardUnit] = None
    reasonunits: dict[RopeTerm, ReasonUnit] = None
    workforceunit: WorkforceUnit = None
    factunits: dict[RopeTerm, FactUnit] = None
    healerunit: HealerUnit = None
    begin: float = None
    close: float = None
    addin: float = None
    denom: int = None
    numor: int = None
    morph: bool = None
    gogo_want: float = None
    stop_want: float = None
    pledge: bool = None
    problem_bool: bool = None
    is_expanded: bool = None
    # Calculated fields
    plan_active: bool = None
    plan_active_hx: dict[int, bool] = None
    all_contact_cred: bool = None
    all_contact_debt: bool = None
    awardheirs: dict[GroupTitle, AwardHeir] = None
    awardlines: dict[GroupTitle, AwardLine] = None
    descendant_pledge_count: int = None
    factheirs: dict[RopeTerm, FactHeir] = None
    fund_ratio: float = None
    fund_grain: FundGrain = None
    fund_onset: FundNum = None
    fund_cease: FundNum = None
    healerunit_ratio: float = None
    tree_level: int = None
    range_evaluated: bool = None
    reasonheirs: dict[RopeTerm, ReasonHeir] = None
    plan_task: bool = None
    workforceheir: WorkforceHeir = None
    gogo_calc: float = None
    stop_calc: float = None

    def is_agenda_plan(self, necessary_reason_context: RopeTerm = None) -> bool:
        reason_context_reasonunit_exists = self.reason_context_reasonunit_exists(
            necessary_reason_context
        )
        return self.pledge and self.plan_active and reason_context_reasonunit_exists

    def reason_context_reasonunit_exists(
        self, necessary_reason_context: RopeTerm = None
    ) -> bool:
        x_reasons = self.reasonunits.values()
        x_reason_context = necessary_reason_context
        return x_reason_context is None or any(
            reason.reason_context == x_reason_context for reason in x_reasons
        )

    def record_plan_active_hx(
        self, tree_traverse_count: int, prev_plan_active: bool, now_plan_active: bool
    ):
        if tree_traverse_count == 0:
            self.plan_active_hx = {0: now_plan_active}
        elif prev_plan_active != now_plan_active:
            self.plan_active_hx[tree_traverse_count] = now_plan_active

    def set_factheirs(self, facts: dict[RopeTerm, FactCore]):
        facts_dict = get_empty_dict_if_None(facts)
        self.factheirs = {}
        for x_factcore in facts_dict.values():
            self._set_factheir(x_factcore)

    def _set_factheir(self, x_fact: FactCore):
        if (
            x_fact.fact_context == self.get_plan_rope()
            and self.gogo_calc is not None
            and self.stop_calc is not None
            and self.begin is None
            and self.close is None
        ):
            raise RangedFactPlanError(
                f"Cannot have fact for range inheritor '{self.get_plan_rope()}'. A ranged fact plan must have _begin, _close"
            )
        x_factheir = factheir_shop(
            x_fact.fact_context, x_fact.fact_state, x_fact.fact_lower, x_fact.fact_upper
        )
        self.delete_factunit_if_past(x_factheir)
        x_factheir = self.apply_factunit_moldations(x_factheir)
        self.factheirs[x_factheir.fact_context] = x_factheir

    def apply_factunit_moldations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self.factunits.values():
            if factunit.fact_context == factheir.fact_context:
                factheir.mold(factunit)
        return factheir

    def delete_factunit_if_past(self, factheir: FactHeir):
        delete_factunit = False
        for factunit in self.factunits.values():
            if (
                factunit.fact_context == factheir.fact_context
                and factunit.fact_upper is not None
                and factheir.fact_lower is not None
            ) and factunit.fact_upper < factheir.fact_lower:
                delete_factunit = True

        if delete_factunit:
            del self.factunits[factunit.fact_context]

    def set_factunit(self, factunit: FactUnit):
        self.factunits[factunit.fact_context] = factunit

    def factunit_exists(self, x_fact_context: RopeTerm) -> bool:
        return self.factunits.get(x_fact_context) != None

    def get_factunits_dict(self) -> dict[RopeTerm, str]:
        return get_dict_from_factunits(self.factunits)

    def set_factunit_to_complete(self, fact_contextunit: FactUnit):
        # if a plan is considered a plan_task then a factheir.fact_lower attribute can be increased to
        # a number <= factheir.fact_upper so the plan no longer is a plan_task. This method finds
        # the minimal factheir.fact_lower to modify plan.plan_task is False. plan_core.factheir cannot be straight up manipulated
        # so it is mandatory that plan.factunit is different.
        # self.set_factunits(reason_context=fact, fact=reason_context, reason_lower=reason_upper, reason_upper=fact_upper)
        self.factunits[fact_contextunit.fact_context] = factunit_shop(
            fact_context=fact_contextunit.fact_context,
            fact_state=fact_contextunit.fact_context,
            fact_lower=fact_contextunit.fact_upper,
            fact_upper=fact_contextunit.fact_upper,
        )

    def del_factunit(self, fact_context: RopeTerm):
        self.factunits.pop(fact_context)

    def set_fund_attr(
        self,
        x_fund_onset: FundNum,
        x_fund_cease: FundNum,
        fund_pool: FundNum,
    ):
        self.fund_onset = x_fund_onset
        self.fund_cease = x_fund_cease
        self.fund_ratio = self.get_plan_fund_total() / fund_pool
        self.set_awardheirs_fund_give_fund_take()

    def get_plan_fund_total(self) -> float:
        """Return plan fund plan total. Equal to difference of fund_cease and fund_onset"""
        if self.fund_onset is None or self.fund_cease is None:
            return 0
        else:
            return self.fund_cease - self.fund_onset

    def get_kids_in_range(
        self, x_gogo: float = None, x_stop: float = None
    ) -> dict[LabelTerm,]:
        if x_gogo is None and x_stop is None:
            x_gogo = self.gogo_want
            x_gogo = self.stop_want
        elif x_gogo is not None and x_stop is None:
            x_stop = x_gogo

        if x_gogo is None and x_stop is None:
            return self.kids.values()

        x_dict = {}
        for x_plan in self.kids.values():
            x_gogo_in_range = x_gogo >= x_plan.gogo_calc and x_gogo < x_plan.stop_calc
            x_stop_in_range = x_stop > x_plan.gogo_calc and x_stop < x_plan.stop_calc
            both_in_range = x_gogo <= x_plan.gogo_calc and x_stop >= x_plan.stop_calc

            if x_gogo_in_range or x_stop_in_range or both_in_range:
                x_dict[x_plan.plan_label] = x_plan
        return x_dict

    def get_obj_key(self) -> LabelTerm:
        return self.plan_label

    def get_plan_rope(self) -> RopeTerm:
        if self.parent_rope in (None, ""):
            return create_rope(self.plan_label, knot=self.knot)
        else:
            return create_rope(self.parent_rope, self.plan_label, knot=self.knot)

    def clear_descendant_pledge_count(self):
        self.descendant_pledge_count = None

    def set_descendant_pledge_count_zero_if_None(self):
        if self.descendant_pledge_count is None:
            self.descendant_pledge_count = 0

    def add_to_descendant_pledge_count(self, x_int: int):
        self.set_descendant_pledge_count_zero_if_None()
        self.descendant_pledge_count += x_int

    def get_descendant_ropes_from_kids(self) -> dict[RopeTerm, int]:
        descendant_ropes = {}
        to_evaluate_plans = list(self.kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_plans != [] and count_x < max_count:
            x_plan = to_evaluate_plans.pop()
            descendant_ropes[x_plan.get_plan_rope()] = -1
            to_evaluate_plans.extend(x_plan.kids.values())
            count_x += 1

        if count_x == max_count:
            raise PlanetDescendantsError(
                f"Plan '{self.get_plan_rope()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_ropes

    def clear_all_contact_cred_debt(self):
        self.all_contact_cred = None
        self.all_contact_debt = None

    def set_tree_level(self, parent_tree_level):
        self.tree_level = parent_tree_level + 1

    def set_parent_rope(self, parent_rope):
        self.parent_rope = parent_rope

    def inherit_awardheirs(self, parent_awardheirs: dict[GroupTitle, AwardHeir] = None):
        parent_awardheirs = {} if parent_awardheirs is None else parent_awardheirs
        self.awardheirs = {}
        for ib in parent_awardheirs.values():
            awardheir = awardheir_shop(
                awardee_title=ib.awardee_title,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self.awardheirs[awardheir.awardee_title] = awardheir

        for ib in self.awardunits.values():
            awardheir = awardheir_shop(
                awardee_title=ib.awardee_title,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self.awardheirs[awardheir.awardee_title] = awardheir

    def set_kidless_awardlines(self):
        # get awardlines from self
        for bh in self.awardheirs.values():
            x_awardline = awardline_shop(
                awardee_title=bh.awardee_title,
                fund_give=bh.fund_give,
                fund_take=bh.fund_take,
            )
            self.awardlines[x_awardline.awardee_title] = x_awardline

    def set_awardlines(self, child_awardlines: dict[GroupTitle, AwardLine] = None):
        if child_awardlines is None:
            child_awardlines = {}

        # get awardlines from child
        for bl in child_awardlines.values():
            if self.awardlines.get(bl.awardee_title) is None:
                self.awardlines[bl.awardee_title] = awardline_shop(
                    awardee_title=bl.awardee_title,
                    fund_give=0,
                    fund_take=0,
                )

            self.awardlines[bl.awardee_title].add_fund_give_take(
                fund_give=bl.fund_give, fund_take=bl.fund_take
            )

    def set_awardheirs_fund_give_fund_take(self):
        give_ledger = {}
        take_ledger = {}
        for x_awardee_title, x_awardheir in self.awardheirs.items():
            give_ledger[x_awardee_title] = x_awardheir.give_force
            take_ledger[x_awardee_title] = x_awardheir.take_force
        x_plan_fund_total = self.get_plan_fund_total()
        give_allot = allot_scale(give_ledger, x_plan_fund_total, self.fund_grain)
        take_allot = allot_scale(take_ledger, x_plan_fund_total, self.fund_grain)
        for x_awardee_title, x_awardheir in self.awardheirs.items():
            x_awardheir.fund_give = give_allot.get(x_awardee_title)
            x_awardheir.fund_take = take_allot.get(x_awardee_title)

    def clear_awardlines(self):
        self.awardlines = {}

    def set_plan_label(self, plan_label: str):
        if plan_label in {None, ""}:
            exception_str = "Cannot set Plan's Label empty or None"
            raise PlanLabelNotEmptyError(exception_str)
        else:
            self.plan_label = plan_label

    def set_knot(self, new_knot: KnotTerm):
        old_knot = deepcopy(self.knot)
        if old_knot is None:
            old_knot = default_knot_if_None()
        self.knot = default_knot_if_None(new_knot)
        if old_knot != self.knot:
            self._find_replace_knot(old_knot)

    def _find_replace_knot(self, old_knot):
        self.parent_rope = replace_knot(self.parent_rope, old_knot, self.knot)

        new_reasonunits = {}
        for reasonunit_rope, reasonunit_obj in self.reasonunits.items():
            new_reasonunit_rope = replace_knot(
                rope=reasonunit_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            reasonunit_obj.set_knot(self.knot)
            new_reasonunits[new_reasonunit_rope] = reasonunit_obj
        self.reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_rope, x_factunit in self.factunits.items():
            new_reason_context_rope = replace_knot(
                rope=factunit_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            x_factunit.fact_context = new_reason_context_rope
            new_fact_state_rope = replace_knot(
                rope=x_factunit.fact_state,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            x_factunit.set_attr(fact_state=new_fact_state_rope)
            new_factunits[new_reason_context_rope] = x_factunit
        self.factunits = new_factunits

    def _set_attrs_to_planunit(self, plan_attr: PlanAttrHolder):
        if plan_attr.star is not None:
            self.star = plan_attr.star
        if plan_attr.plan_uid is not None:
            self.plan_uid = plan_attr.plan_uid
        if plan_attr.reason is not None:
            self.set_reasonunit(reason=plan_attr.reason)
        if plan_attr.reason_context is not None and plan_attr.reason_case is not None:
            self.set_reason_case(
                reason_context=plan_attr.reason_context,
                case=plan_attr.reason_case,
                reason_lower=plan_attr.reason_lower,
                reason_upper=plan_attr.reason_upper,
                reason_divisor=plan_attr.reason_divisor,
            )
        if (
            plan_attr.reason_context is not None
            and plan_attr.reason_requisite_active is not None
        ):
            self.set_reason_requisite_active(
                reason_context=plan_attr.reason_context,
                active_requisite=plan_attr.reason_requisite_active,
            )
        if plan_attr.workforceunit is not None:
            self.workforceunit = plan_attr.workforceunit
        if plan_attr.healerunit is not None:
            self.healerunit = plan_attr.healerunit
        if plan_attr.begin is not None:
            self.begin = plan_attr.begin
        if plan_attr.close is not None:
            self.close = plan_attr.close
        if plan_attr.gogo_want is not None:
            self.gogo_want = plan_attr.gogo_want
        if plan_attr.stop_want is not None:
            self.stop_want = plan_attr.stop_want
        if plan_attr.addin is not None:
            self.addin = plan_attr.addin
        if plan_attr.numor is not None:
            self.numor = plan_attr.numor
        if plan_attr.denom is not None:
            self.denom = plan_attr.denom
        if plan_attr.morph is not None:
            self.morph = plan_attr.morph
        if plan_attr.awardunit is not None:
            self.set_awardunit(awardunit=plan_attr.awardunit)
        if plan_attr.awardunit_del is not None:
            self.del_awardunit(awardee_title=plan_attr.awardunit_del)
        if plan_attr.is_expanded is not None:
            self.is_expanded = plan_attr.is_expanded
        if plan_attr.pledge is not None:
            self.pledge = plan_attr.pledge
        if plan_attr.factunit is not None:
            self.set_factunit(plan_attr.factunit)
        if plan_attr.problem_bool is not None:
            self.problem_bool = plan_attr.problem_bool

        self._del_reasonunit_all_cases(
            reason_context=plan_attr.reason_del_case_reason_context,
            case=plan_attr.reason_del_case_reason_state,
        )
        self._set_addin_to_zero_if_any_moldations_exist()

    def _set_addin_to_zero_if_any_moldations_exist(self):
        if (
            self.begin is not None
            and self.close is not None
            and (self.numor is not None or self.denom is not None)
            and self.addin is None
        ):
            self.addin = 0

    def clear_gogo_calc_stop_calc(self):
        self.range_evaluated = False
        self.gogo_calc = None
        self.stop_calc = None

    def _mold_gogo_calc_stop_calc(self):
        r_plan_numor = get_1_if_None(self.numor)
        r_plan_denom = get_1_if_None(self.denom)
        r_plan_addin = get_0_if_None(self.addin)

        if self.gogo_calc is None or self.stop_calc is None:
            pass
        elif self.gogo_want != None and self.stop_want != None:
            stop_want_less_than_gogo_calc = self.stop_want < self.gogo_calc
            gogo_want_greater_than_stop_calc = self.gogo_want > self.stop_calc
            if stop_want_less_than_gogo_calc or gogo_want_greater_than_stop_calc:
                self.gogo_calc = None
                self.stop_calc = None
            else:
                self.gogo_calc = max(self.gogo_calc, self.gogo_want)
                self.stop_calc = min(self.stop_calc, self.stop_want)
        elif get_False_if_None(self.morph):
            x_gogo = self.gogo_calc
            x_stop = self.stop_calc
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, self.denom)
            self.gogo_calc = x_rangeunit.gogo
            self.stop_calc = x_rangeunit.stop
        else:
            self.gogo_calc = self.gogo_calc + r_plan_addin
            self.stop_calc = self.stop_calc + r_plan_addin
            self.gogo_calc = (self.gogo_calc * r_plan_numor) / r_plan_denom
            self.stop_calc = (self.stop_calc * r_plan_numor) / r_plan_denom
        self.range_evaluated = True

    def _del_reasonunit_all_cases(self, reason_context: RopeTerm, case: RopeTerm):
        if reason_context is not None and case is not None:
            self.del_reasonunit_case(reason_context=reason_context, case=case)
            if len(self.reasonunits[reason_context].cases) == 0:
                self.del_reasonunit_reason_context(reason_context=reason_context)

    def set_reason_requisite_active(
        self, reason_context: RopeTerm, active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(reason_context=reason_context)
        if active_requisite is False:
            x_reasonunit.active_requisite = False
        elif active_requisite == "Set to Ignore":
            x_reasonunit.active_requisite = None
        elif active_requisite:
            x_reasonunit.active_requisite = True

    def _get_or_create_reasonunit(self, reason_context: RopeTerm) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[reason_context]
        except Exception:
            x_reasonunit = reasonunit_shop(reason_context, knot=self.knot)
            self.reasonunits[reason_context] = x_reasonunit
        return x_reasonunit

    def set_reason_case(
        self,
        reason_context: RopeTerm,
        case: RopeTerm,
        reason_lower: ReasonNum,
        reason_upper: ReasonNum,
        reason_divisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(reason_context=reason_context)
        x_reasonunit.set_case(
            case=case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
        )

    def del_reasonunit_reason_context(self, reason_context: RopeTerm):
        try:
            self.reasonunits.pop(reason_context)
        except KeyError as e:
            raise InvalidPlanError(f"No ReasonUnit at '{reason_context}'") from e

    def del_reasonunit_case(self, reason_context: RopeTerm, case: RopeTerm):
        reason_unit = self.reasonunits[reason_context]
        reason_unit.del_case(case=case)

    def add_kid(self, plan_kid):
        self.kids[plan_kid.plan_label] = plan_kid
        self.kids = dict(sorted(self.kids.items()))

    def get_kid(self, plan_kid_plan_label: LabelTerm, if_missing_create=False):
        if if_missing_create is False:
            return self.kids.get(plan_kid_plan_label)
        try:
            return self.kids[plan_kid_plan_label]
        except Exception:
            KeyError
            self.add_kid(planunit_shop(plan_kid_plan_label))
            return_plan = self.kids.get(plan_kid_plan_label)
        return return_plan

    def del_kid(self, plan_kid_plan_label: LabelTerm):
        self.kids.pop(plan_kid_plan_label)

    def clear_kids(self):
        self.kids = {}

    def get_kids_star_sum(self) -> float:
        return sum(x_kid.star for x_kid in self.kids.values())

    def set_awardunit(self, awardunit: AwardUnit):
        self.awardunits[awardunit.awardee_title] = awardunit

    def get_awardunit(self, awardee_title: GroupTitle) -> AwardUnit:
        return self.awardunits.get(awardee_title)

    def del_awardunit(self, awardee_title: GroupTitle):
        try:
            self.awardunits.pop(awardee_title)
        except KeyError as e:
            raise (f"Cannot delete awardunit '{awardee_title}'.") from e

    def awardunit_exists(self, x_awardee_title: GroupTitle) -> bool:
        return self.awardunits.get(x_awardee_title) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.knot = self.knot
        self.reasonunits[reason.reason_context] = reason

    def reasonunit_exists(self, x_reason_context: RopeTerm) -> bool:
        return self.reasonunits.get(x_reason_context) != None

    def get_reasonunit(self, reason_context: RopeTerm) -> ReasonUnit:
        return self.reasonunits.get(reason_context)

    def set_reasonheirs_reason_active(self):
        self.clear_reasonheirs_reason_active()
        for x_reasonheir in self.reasonheirs.values():
            x_reasonheir.set_reason_active(factheirs=self.factheirs)

    def set_plan_active(
        self,
        tree_traverse_count: int,
        groupunits: dict[GroupTitle, GroupUnit] = None,
        person_name: ContactName = None,
    ):
        prev_to_now_active = deepcopy(self.plan_active)
        self.plan_active = self._create_active_bool(groupunits, person_name)
        self.set_plan_task()
        self.record_plan_active_hx(
            tree_traverse_count, prev_to_now_active, self.plan_active
        )

    def set_plan_task(self):
        self.plan_task = False
        if self.pledge and self.plan_active and self.reasonheirs_satisfied():
            self.plan_task = True

    def reasonheirs_satisfied(self) -> bool:
        return self.reasonheirs == {} or self._any_reasonheir_reason_task_true()

    def _any_reasonheir_reason_task_true(self) -> bool:
        return any(
            x_reasonheir.reason_task for x_reasonheir in self.reasonheirs.values()
        )

    def _create_active_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        person_name: ContactName,
    ) -> bool:
        self.set_reasonheirs_reason_active()
        active_bool = self.all_reasonheirs_are_active()
        if active_bool and groupunits != {} and person_name is not None:
            self.workforceheir.set_person_name_is_workforce(groupunits, person_name)
            if self.workforceheir.person_name_is_workforce is False:
                active_bool = False
        return active_bool

    def set_range_inheritors_factheirs(
        self,
        person_plan_dict: dict[RopeTerm,],
        range_inheritors: dict[RopeTerm, RopeTerm],
    ):
        for reason_context in self.reasonheirs.keys():
            if rangeroot_rope := range_inheritors.get(reason_context):
                all_plans = all_plans_between(
                    person_plan_dict=person_plan_dict,
                    src_rope=rangeroot_rope,
                    dst_reason_context=reason_context,
                    knot=self.knot,
                )
                self._set_range_inheritor_factheir(
                    all_plans=all_plans,
                    rangeroot_rope=rangeroot_rope,
                    fact_context=reason_context,
                )

    def _set_range_inheritor_factheir(
        self, all_plans: list, rangeroot_rope: RopeTerm, fact_context: RopeTerm
    ):
        if rangeroot_factheir := self.factheirs.get(rangeroot_rope):
            new_factheir_obj = create_range_inheritor_factheir(
                rangeroot_factheir=rangeroot_factheir,
                all_plans=all_plans,
                fact_context=fact_context,
            )
            self._set_factheir(new_factheir_obj)

    def all_reasonheirs_are_active(self) -> bool:
        x_reasonheirs = self.reasonheirs.values()
        return all(
            x_reasonheir.reason_active != False for x_reasonheir in x_reasonheirs
        )

    def clear_reasonheirs_reason_active(self):
        for reason in self.reasonheirs.values():
            reason.clear_reason_active()

    def _coalesce_with_reasonunits(
        self, reasonheirs: dict[RopeTerm, ReasonHeir]
    ) -> dict[RopeTerm, ReasonHeir]:
        new_reasonheirs = deepcopy(reasonheirs)
        new_reasonheirs |= self.reasonunits
        return new_reasonheirs

    def set_reasonheirs(
        self,
        person_plan_dict: dict[RopeTerm,],
        reasonheirs: dict[RopeTerm, ReasonCore],
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self.reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_reason_context = old_reasonheir.reason_context
            old_active_requisite = old_reasonheir.active_requisite
            new_reasonheir = reasonheir_shop(
                old_reason_context, None, old_active_requisite
            )
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if reason_context_plan := person_plan_dict.get(
                old_reasonheir.reason_context
            ):
                new_reasonheir.set_heir_active(reason_context_plan.plan_active)
            self.reasonheirs[new_reasonheir.reason_context] = new_reasonheir

    def set_root_plan_reasonheirs(self):
        self.reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.reason_context)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self.reasonheirs[new_reasonheir.reason_context] = new_reasonheir

    def get_reasonheir(self, reason_context: RopeTerm) -> ReasonHeir:
        return self.reasonheirs.get(reason_context)

    def get_reasonunits_dict(self):
        return {
            reason_context: reason.to_dict()
            for reason_context, reason in self.reasonunits.items()
        }

    def get_kids_dict(self) -> dict[RopeTerm,]:
        return {c_rope: kid.to_dict() for c_rope, kid in self.kids.items()}

    def get_awardunits_dict(self) -> dict[GroupTitle, dict]:
        x_awardunits = self.awardunits.items()
        return {
            x_awardee_title: awardunit.to_dict()
            for x_awardee_title, awardunit in x_awardunits
        }

    def is_kidless(self) -> bool:
        return self.kids == {}

    def has_begin_close(self) -> bool:
        return self.begin is not None and self.close is not None

    def awardheir_exists(self) -> bool:
        return self.awardheirs != {}

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"star": self.star}

        if self.plan_label is not None:
            x_dict["plan_label"] = self.plan_label
        if self.plan_uid is not None:
            x_dict["plan_uid"] = self.plan_uid
        if self.kids not in [{}, None]:
            x_dict["kids"] = self.get_kids_dict()
        if self.reasonunits not in [{}, None]:
            x_dict["reasonunits"] = self.get_reasonunits_dict()
        if self.workforceunit not in [None, workforceunit_shop()]:
            x_dict["workforceunit"] = self.get_workforceunit_dict()
        if self.healerunit not in [None, healerunit_shop()]:
            x_dict["healerunit"] = self.healerunit.to_dict()
        if self.awardunits not in [{}, None]:
            x_dict["awardunits"] = self.get_awardunits_dict()
        if self.begin is not None:
            x_dict["begin"] = self.begin
        if self.close is not None:
            x_dict["close"] = self.close
        if self.addin is not None:
            x_dict["addin"] = self.addin
        if self.numor is not None:
            x_dict["numor"] = self.numor
        if self.denom is not None:
            x_dict["denom"] = self.denom
        if self.morph is not None:
            x_dict["morph"] = self.morph
        if self.gogo_want is not None:
            x_dict["gogo_want"] = self.gogo_want
        if self.stop_want is not None:
            x_dict["stop_want"] = self.stop_want
        if self.pledge:
            x_dict["pledge"] = self.pledge
        if self.problem_bool:
            x_dict["problem_bool"] = self.problem_bool
        if self.factunits not in [{}, None]:
            x_dict["factunits"] = self.get_factunits_dict()
        if self.is_expanded is False:
            x_dict["is_expanded"] = self.is_expanded

        return x_dict

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        if is_sub_rope(ref_rope=self.parent_rope, sub_rope=old_rope):
            self.parent_rope = rebuild_rope(self.parent_rope, old_rope, new_rope)

        self.reasonunits == find_replace_rope_key_dict(
            dict_x=self.reasonunits, old_rope=old_rope, new_rope=new_rope
        )

        self.factunits == find_replace_rope_key_dict(
            dict_x=self.factunits, old_rope=old_rope, new_rope=new_rope
        )

    def set_workforceunit_empty_if_None(self):
        if self.workforceunit is None:
            self.workforceunit = workforceunit_shop()

    def set_workforceheir(
        self,
        parent_workforceheir: WorkforceHeir,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        self.workforceheir = workforceheir_shop()
        self.workforceheir.set_labors(
            parent_workforceheir=parent_workforceheir,
            workforceunit=self.workforceunit,
            groupunits=groupunits,
        )

    def get_workforceunit_dict(self) -> dict:
        return self.workforceunit.to_dict()


def planunit_shop(
    plan_label: LabelTerm,
    plan_uid: int = None,  # Calculated field?
    parent_rope: RopeTerm = None,
    kids: dict = None,
    star: int = 1,
    awardunits: dict[GroupTitle, AwardUnit] = None,
    awardheirs: dict[GroupTitle, AwardHeir] = None,  # Calculated field
    awardlines: dict[GroupTitle, AwardUnit] = None,  # Calculated field
    reasonunits: dict[RopeTerm, ReasonUnit] = None,
    reasonheirs: dict[RopeTerm, ReasonHeir] = None,  # Calculated field
    workforceunit: WorkforceUnit = None,
    workforceheir: WorkforceHeir = None,  # Calculated field
    factunits: dict[FactUnit] = None,
    factheirs: dict[FactHeir] = None,  # Calculated field
    healerunit: HealerUnit = None,
    begin: float = None,
    close: float = None,
    gogo_want: float = None,
    stop_want: float = None,
    addin: float = None,
    denom: int = None,
    numor: int = None,
    morph: bool = None,
    pledge: bool = None,
    problem_bool: bool = None,
    # Calculated fields
    tree_level: int = None,
    fund_ratio: float = None,
    fund_grain: FundGrain = None,
    fund_onset: FundNum = None,
    fund_cease: FundNum = None,
    plan_task: bool = None,
    plan_active: bool = None,
    descendant_pledge_count: int = None,
    all_contact_cred: bool = None,
    all_contact_debt: bool = None,
    is_expanded: bool = True,
    plan_active_hx: dict[int, bool] = None,
    knot: KnotTerm = None,
    healerunit_ratio: float = None,
) -> PlanUnit:
    x_healerunit = healerunit_shop() if healerunit is None else healerunit

    x_plankid = PlanUnit(
        plan_label=None,
        plan_uid=plan_uid,
        parent_rope=parent_rope,
        kids=get_empty_dict_if_None(kids),
        star=get_positive_int(star),
        awardunits=get_empty_dict_if_None(awardunits),
        awardheirs=get_empty_dict_if_None(awardheirs),
        awardlines=get_empty_dict_if_None(awardlines),
        reasonunits=get_empty_dict_if_None(reasonunits),
        reasonheirs=get_empty_dict_if_None(reasonheirs),
        workforceunit=workforceunit,
        workforceheir=workforceheir,
        factunits=get_empty_dict_if_None(factunits),
        factheirs=get_empty_dict_if_None(factheirs),
        healerunit=x_healerunit,
        begin=begin,
        close=close,
        gogo_want=gogo_want,
        stop_want=stop_want,
        addin=addin,
        denom=denom,
        numor=numor,
        morph=morph,
        pledge=get_False_if_None(pledge),
        problem_bool=get_False_if_None(problem_bool),
        # Calculated fields
        tree_level=tree_level,
        fund_ratio=fund_ratio,
        fund_grain=default_grain_num_if_None(fund_grain),
        fund_onset=fund_onset,
        fund_cease=fund_cease,
        plan_task=plan_task,
        plan_active=plan_active,
        descendant_pledge_count=descendant_pledge_count,
        all_contact_cred=all_contact_cred,
        all_contact_debt=all_contact_debt,
        is_expanded=is_expanded,
        plan_active_hx=get_empty_dict_if_None(plan_active_hx),
        knot=default_knot_if_None(knot),
        healerunit_ratio=get_0_if_None(healerunit_ratio),
    )
    x_plankid.set_plan_label(plan_label=plan_label)
    x_plankid.set_workforceunit_empty_if_None()
    return x_plankid


def get_obj_from_plan_dict(x_dict: dict[str, dict], dict_key: str) -> any:
    if dict_key == "reasonunits":
        return (
            get_reasonunits_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else None
        )
    elif dict_key == "workforceunit":
        return (
            get_workforceunit_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else workforceunit_shop()
        )
    elif dict_key == "healerunit":
        return (
            get_healerunit_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else healerunit_shop()
        )
    elif dict_key == "factunits":
        facts_dict = get_empty_dict_if_None(x_dict.get(dict_key))
        return get_factunits_from_dict(facts_dict)
    elif dict_key == "awardunits":
        return (
            get_awardunits_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else get_awardunits_from_dict({})
        )
    elif dict_key in {"kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else {}
    elif dict_key in {"pledge", "problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else False
    elif dict_key in {"is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else True
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def all_plans_between(
    person_plan_dict: dict[RopeTerm, PlanUnit],
    src_rope: RopeTerm,
    dst_reason_context: RopeTerm,
    knot: KnotTerm,
) -> list[PlanUnit]:
    all_ropes = all_ropes_between(src_rope, dst_reason_context, knot)
    return [person_plan_dict.get(x_rope) for x_rope in all_ropes]


def get_rangeunit_from_lineage_of_plans(
    plan_list: list[PlanUnit], x_gogo: float, x_stop: float
) -> RangeUnit:
    for x_plan in plan_list:
        if x_plan.addin:
            x_gogo += get_0_if_None(x_plan.addin)
            x_stop += get_0_if_None(x_plan.addin)
        if (x_plan.numor or x_plan.denom) and not x_plan.morph:
            x_gogo *= get_1_if_None(x_plan.numor) / get_1_if_None(x_plan.denom)
            x_stop *= get_1_if_None(x_plan.numor) / get_1_if_None(x_plan.denom)
        if x_plan.denom and x_plan.morph:
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_plan.denom)
            x_gogo = x_rangeunit.gogo
            x_stop = x_rangeunit.stop
    return RangeUnit(x_gogo, x_stop)


def create_range_inheritor_factheir(
    rangeroot_factheir: FactHeir, all_plans: list[PlanUnit], fact_context: RopeTerm
) -> FactHeir:
    x_rangeunit = get_rangeunit_from_lineage_of_plans(
        plan_list=all_plans,
        x_gogo=rangeroot_factheir.fact_lower,
        x_stop=rangeroot_factheir.fact_upper,
    )
    return factheir_shop(
        fact_context=fact_context,
        fact_state=fact_context,
        fact_lower=x_rangeunit.gogo,
        fact_upper=x_rangeunit.stop,
    )
