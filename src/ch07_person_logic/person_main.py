from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_False_if_None,
)
from src.ch01_allot.allot import (
    allot_scale,
    default_grain_num_if_None as grain_num,
    valid_allotment_ratio,
    validate_pool_num,
)
from src.ch02_partner.group import AwardUnit, GroupUnit, groupunit_shop, membership_shop
from src.ch02_partner.partner import (
    PartnerUnit,
    partnerunit_shop,
    partnerunits_get_from_dict,
)
from src.ch03_workforce.workforce import WorkforceUnit
from src.ch04_rope.rope import (
    all_ropes_between,
    create_rope,
    default_knot_if_None,
    get_all_rope_labels,
    get_ancestor_ropes,
    get_default_rope,
    get_first_label_from_rope,
    get_forefather_ropes,
    get_parent_rope,
    get_tail_label,
    is_labelterm,
    is_string_in_rope,
    is_sub_rope,
    rebuild_rope,
    rope_is_valid_dir_path,
    to_rope,
)
from src.ch05_reason.reason_main import FactUnit, ReasonUnit, RopeTerm, factunit_shop
from src.ch06_plan.healer import HealerUnit
from src.ch06_plan.plan import (
    PlanAttrHolder,
    PlanUnit,
    get_obj_from_plan_dict,
    planattrholder_shop,
    planunit_shop,
)
from src.ch07_person_logic._ref.ch07_semantic_types import (
    FactNum,
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    ManaGrain,
    PartnerName,
    PersonName,
    ReasonNum,
    RespectGrain,
    RespectNum,
    RopeTerm,
)
from src.ch07_person_logic.person_config import max_tree_traverse_default
from src.ch07_person_logic.tree_metric import TreeMetrics, treemetrics_shop


class InvalidPersonError(Exception):
    pass


class InvalidLabelError(Exception):
    pass


class NewKnotError(Exception):
    pass


class ReasonCaseError(Exception):
    pass


class PartnerMissingError(Exception):
    pass


class KeepJustError(Exception):
    pass


class BitRatioError(Exception):
    pass


class LastLessonIDError(Exception):
    pass


class HealerunitGroupTitleError(Exception):
    pass


class GogoCalcStopCalcError(Exception):
    pass


class IsRopeTermError(Exception):
    pass


@dataclass
class PersonUnit:
    person_name: PersonName = None
    partners: dict[PartnerName, PartnerUnit] = None
    planroot: PlanUnit = None  # planroot.get_rope defines planroot_rope
    knot: KnotTerm = None  # often must defined by creator class
    fund_pool: FundNum = None  # often must defined by creator class
    fund_grain: FundGrain = None  # often must defined by creator class
    respect_grain: RespectGrain = None  # often must defined by creator class
    mana_grain: ManaGrain = None  # often must defined by creator class
    credor_respect: RespectNum = None  # mostly set by default
    debtor_respect: RespectNum = None  # mostly set by default
    max_tree_traverse: int = None  # mostly set by default
    last_lesson_id: int = None  #
    # fields calculated by conpute
    _plan_dict: dict[RopeTerm, PlanUnit] = None
    _keep_dict: dict[RopeTerm, PlanUnit] = None
    _healers_dict: dict[HealerName, dict[RopeTerm, PlanUnit]] = None
    tree_traverse_count: int = None
    rational: bool = None
    keeps_justified: bool = None
    keeps_buildable: bool = None
    sum_healerunit_plans_fund_total: float = None
    groupunits: dict[GroupTitle, GroupUnit] = None
    offtrack_kids_star_set: set[RopeTerm] = None
    offtrack_fund: float = None
    reason_contexts: set[RopeTerm] = None
    range_inheritors: dict[RopeTerm, RopeTerm] = None

    def del_last_lesson_id(self):
        self.last_lesson_id = None

    def set_last_lesson_id(self, x_last_lesson_id: int):
        if self.last_lesson_id is not None and x_last_lesson_id < self.last_lesson_id:
            exception_str = f"Cannot set _last_lesson_id to {x_last_lesson_id} because it is less than {self.last_lesson_id}."
            raise LastLessonIDError(exception_str)
        self.last_lesson_id = x_last_lesson_id

    def set_fund_pool(self, x_fund_pool):
        if valid_allotment_ratio(x_fund_pool, self.fund_grain) is False:
            exception_str = f"Person '{self.person_name}' cannot set fund_pool='{x_fund_pool}'. It is not divisible by fund_grain '{self.fund_grain}'"
            raise BitRatioError(exception_str)

        self.fund_pool = validate_pool_num(x_fund_pool)

    def set_partner_respect(self, x_partner_pool: int):
        self.set_credor_respect(x_partner_pool)
        self.set_debtor_respect(x_partner_pool)
        self.set_fund_pool(x_partner_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_allotment_ratio(new_credor_respect, self.respect_grain) is False:
            exception_str = f"Person '{self.person_name}' cannot set credor_respect='{new_credor_respect}'. It is not divisible byrespect_grain'{self.respect_grain}'"
            raise BitRatioError(exception_str)
        self.credor_respect = new_credor_respect

    def set_debtor_respect(self, new_debtor_respect: int):
        if valid_allotment_ratio(new_debtor_respect, self.respect_grain) is False:
            exception_str = f"Person '{self.person_name}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible byrespect_grain'{self.respect_grain}'"
            raise BitRatioError(exception_str)
        self.debtor_respect = new_debtor_respect

    def make_rope(
        self,
        parent_rope: RopeTerm = None,
        tail_label: LabelTerm = None,
    ) -> RopeTerm:
        return create_rope(
            parent_rope=parent_rope,
            tail_label=tail_label,
            knot=self.knot,
        )

    def make_l1_rope(self, l1_label: LabelTerm):
        return self.make_rope(self.planroot.plan_label, l1_label)

    def set_knot(self, new_knot: KnotTerm):
        self.conpute()
        if self.knot != new_knot:
            for x_plan_rope in self._plan_dict.keys():
                if is_string_in_rope(new_knot, x_plan_rope):
                    exception_str = f"Cannot modify knot to '{new_knot}' because it exists an plan plan_label '{x_plan_rope}'"
                    raise NewKnotError(exception_str)

            # modify all rope attrs in planunits
            self.knot = default_knot_if_None(new_knot)
            for x_plan in self._plan_dict.values():
                x_plan.set_knot(self.knot)

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidPersonError(
                f"set_max_tree_traverse: '{x_int}' must be number that is 2 or greater"
            )
        else:
            self.max_tree_traverse = x_int

    def _get_relevant_ropes(self, ropes: dict[RopeTerm,]) -> set[RopeTerm]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for x_rope in ropes:
            to_evaluate_list.append(x_rope)
            to_evaluate_hx_dict[x_rope] = "to_evaluate"
        evaluated_ropes = set()

        # while ropes_to_evaluate != [] and count_x <= tree_metrics.label_count:
        # Why count_x? because count_x might be wrong attr to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            x_rope = to_evaluate_list.pop()
            x_plan = self.get_plan_obj(x_rope)
            for reasonunit_obj in x_plan.reasonunits.values():
                reason_context = reasonunit_obj.reason_context
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_rope=reason_context,
                    rope_type="reasonunit_reason_context",
                )
            forefather_ropes = get_forefather_ropes(x_rope)
            for forefather_rope in forefather_ropes:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_rope=forefather_rope,
                    rope_type="forefather",
                )

            evaluated_ropes.add(x_rope)
        return evaluated_ropes

    def _evaluate_relevancy(
        self,
        to_evaluate_list: list[RopeTerm],
        to_evaluate_hx_dict: dict[RopeTerm, int],
        to_evaluate_rope: RopeTerm,
        rope_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_rope) is None:
            to_evaluate_list.append(to_evaluate_rope)
            to_evaluate_hx_dict[to_evaluate_rope] = rope_type

            if rope_type == "reasonunit_reason_context":
                ru_reason_context_plan = self.get_plan_obj(to_evaluate_rope)
                for (
                    descendant_rope
                ) in ru_reason_context_plan.get_descendant_ropes_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_rope=descendant_rope,
                        rope_type="reasonunit_descendant",
                    )

    def all_plans_relevant_to_pledge_plan(self, rope: RopeTerm) -> bool:
        pledge_plan_assoc_set = set(self._get_relevant_ropes({rope}))
        all_plans_set = set(self.get_plan_tree_ordered_rope_list())
        return all_plans_set == all_plans_set & (pledge_plan_assoc_set)

    def get_awardunits_metrics(self) -> dict[GroupTitle, AwardUnit]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.awardunits_metrics

    def add_to_groupunit_fund_give_fund_take(
        self,
        group_title: GroupTitle,
        awardheir_fund_give: float,
        awardheir_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_title)
        if x_groupunit is not None:
            x_groupunit.fund_give += awardheir_fund_give
            x_groupunit.fund_take += awardheir_fund_take

    def add_to_groupunit_fund_agenda_give_take(
        self,
        group_title: GroupTitle,
        awardline_fund_give: float,
        awardline_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_title)
        if awardline_fund_give is not None and awardline_fund_take is not None:
            x_groupunit.fund_agenda_give += awardline_fund_give
            x_groupunit.fund_agenda_take += awardline_fund_take

    def add_to_partnerunit_fund_give_take(
        self,
        partnerunit_partner_name: PartnerName,
        fund_give,
        fund_take: float,
        fund_agenda_give: float,
        fund_agenda_take: float,
    ):
        x_partnerunit = self.get_partner(partnerunit_partner_name)
        x_partnerunit.add_partner_fund_give_take(
            fund_give=fund_give,
            fund_take=fund_take,
            fund_agenda_give=fund_agenda_give,
            fund_agenda_take=fund_agenda_take,
        )

    def del_partnerunit(self, partner_name: str):
        self.partners.pop(partner_name)

    def add_partnerunit(
        self,
        partner_name: PartnerName,
        partner_cred_lumen: int = None,
        partner_debt_lumen: int = None,
    ):
        x_knot = self.knot
        partnerunit = partnerunit_shop(
            partner_name, partner_cred_lumen, partner_debt_lumen, x_knot
        )
        self.set_partnerunit(partnerunit)

    def set_partnerunit(
        self, x_partnerunit: PartnerUnit, auto_set_membership: bool = True
    ):
        if x_partnerunit.groupmark != self.knot:
            x_partnerunit.groupmark = self.knot
        if x_partnerunit.respect_grain != self.respect_grain:
            x_partnerunit.respect_grain = self.respect_grain
        if auto_set_membership and x_partnerunit.memberships_exist() is False:
            x_partnerunit.add_membership(x_partnerunit.partner_name)
        self.partners[x_partnerunit.partner_name] = x_partnerunit

    def partner_exists(self, partner_name: PartnerName) -> bool:
        return self.get_partner(partner_name) is not None

    def edit_partnerunit(
        self,
        partner_name: PartnerName,
        partner_cred_lumen: int = None,
        partner_debt_lumen: int = None,
    ):
        if self.partners.get(partner_name) is None:
            raise PartnerMissingError(f"PartnerUnit '{partner_name}' does not exist.")
        x_partnerunit = self.get_partner(partner_name)
        if partner_cred_lumen is not None:
            x_partnerunit.set_partner_cred_lumen(partner_cred_lumen)
        if partner_debt_lumen is not None:
            x_partnerunit.set_partner_debt_lumen(partner_debt_lumen)
        self.set_partnerunit(x_partnerunit)

    def clear_partnerunits_memberships(self):
        for x_partnerunit in self.partners.values():
            x_partnerunit.clear_memberships()

    def get_partner(self, partner_name: PartnerName) -> PartnerUnit:
        return self.partners.get(partner_name)

    def get_partnerunit_group_titles_dict(self) -> dict[GroupTitle, set[PartnerName]]:
        x_dict = {}
        for x_partnerunit in self.partners.values():
            for x_group_title in x_partnerunit.memberships.keys():
                partner_name_set = x_dict.get(x_group_title)
                if partner_name_set is None:
                    x_dict[x_group_title] = {x_partnerunit.partner_name}
                else:
                    partner_name_set.add(x_partnerunit.partner_name)
                    x_dict[x_group_title] = partner_name_set
        return x_dict

    def set_groupunit(self, x_groupunit: GroupUnit):
        x_groupunit.fund_grain = self.fund_grain
        self.groupunits[x_groupunit.group_title] = x_groupunit

    def groupunit_exists(self, group_title: GroupTitle) -> bool:
        return self.groupunits.get(group_title) is not None

    def get_groupunit(self, x_group_title: GroupTitle) -> GroupUnit:
        return self.groupunits.get(x_group_title)

    def create_symmetry_groupunit(self, x_group_title: GroupTitle) -> GroupUnit:
        x_groupunit = groupunit_shop(x_group_title)
        for x_partnerunit in self.partners.values():
            x_membership = membership_shop(
                group_title=x_group_title,
                group_cred_lumen=x_partnerunit.partner_cred_lumen,
                group_debt_lumen=x_partnerunit.partner_debt_lumen,
                partner_name=x_partnerunit.partner_name,
            )
            x_groupunit.set_g_membership(x_membership)
        return x_groupunit

    def get_tree_traverse_generated_groupunits(self) -> set[GroupTitle]:
        x_partnerunit_group_titles = set(
            self.get_partnerunit_group_titles_dict().keys()
        )
        all_group_titles = set(self.groupunits.keys())
        return all_group_titles.difference(x_partnerunit_group_titles)

    def _is_plan_rangeroot(self, plan_rope: RopeTerm) -> bool:
        parent_rope = get_parent_rope(plan_rope)
        parent_plan = self.get_plan_obj(parent_rope)
        return not parent_plan.has_begin_close()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self.planroot.factunits.values()
            if fact.fact_lower is not None
            and fact.fact_upper is not None
            and self._is_plan_rangeroot(plan_rope=fact.fact_context)
        ]

    def add_fact(
        self,
        fact_context: RopeTerm,
        fact_state: RopeTerm = None,
        fact_lower: FactNum = None,
        fact_upper: FactNum = None,
        create_missing_plans: bool = None,
    ):
        """Sets planroot factunit"""
        fact_state = fact_context if fact_state is None else fact_state
        if create_missing_plans:
            self._create_plankid_if_empty(rope=fact_context)
            self._create_plankid_if_empty(rope=fact_state)

        fact_context_plan = self.get_plan_obj(fact_context)
        x_planroot = self.planroot
        x_fact_lower = None
        if fact_upper is not None and fact_lower is None:
            x_fact_lower = x_planroot.factunits.get(fact_context).fact_lower
        else:
            x_fact_lower = fact_lower
        x_fact_upper = None
        if fact_lower is not None and fact_upper is None:
            x_fact_upper = x_planroot.factunits.get(fact_context).fact_upper
        else:
            x_fact_upper = fact_upper
        x_factunit = factunit_shop(
            fact_context=fact_context,
            fact_state=fact_state,
            fact_lower=x_fact_lower,
            fact_upper=x_fact_upper,
        )

        if fact_context_plan.has_begin_close() is False:
            x_planroot.set_factunit(x_factunit)
        # if fact's plan no range or is a "rangeroot" then allow fact to be set
        elif (
            fact_context_plan.has_begin_close()
            and self._is_plan_rangeroot(fact_context) is False
        ):
            raise InvalidPersonError(
                f"Non rangeroot fact:{fact_context} can only be set by rangeroot fact"
            )
        elif fact_context_plan.has_begin_close() and self._is_plan_rangeroot(
            fact_context
        ):
            # WHEN plan is "rangeroot" identify any reason.reason_contexts that are descendants
            # calculate and set those descendant facts
            # example: zietline range (0-, 1.5e9) is rangeroot
            # example: "zietline,wks" (spllt 10080) is range-descendant
            # there exists a reason reason_context "zietline,wks" with case.reason_state = "zietline,wks"
            # and (1,2) reason_divisor=2 (every other wk)
            #
            # should not set "zietline,wks" fact, only "zietline" fact and
            # "zietline,wks" should be set automatica_lly since there exists a reason
            # that has that reason_context.
            x_planroot.set_factunit(x_factunit)

    def get_fact(self, fact_context: RopeTerm) -> FactUnit:
        return self.planroot.factunits.get(fact_context)

    def del_fact(self, fact_context: RopeTerm):
        self.planroot.del_factunit(fact_context)

    def get_plan_dict(self, problem: bool = None) -> dict[RopeTerm, PlanUnit]:
        self.conpute()
        if not problem:
            return self._plan_dict
        if self.keeps_justified is False:
            exception_str = f"Cannot return problem set because keeps_justified={self.keeps_justified}."
            raise KeepJustError(exception_str)

        x_plans = self._plan_dict.values()
        return {
            x_plan.get_plan_rope(): x_plan for x_plan in x_plans if x_plan.problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        self.conpute()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_label(
            tree_level=self.planroot.tree_level,
            reasons=self.planroot.reasonunits,
            awardunits=self.planroot.awardunits,
            plan_uid=self.planroot.plan_uid,
            pledge=self.planroot.pledge,
            plan_rope=self.planroot.get_plan_rope(),
        )

        x_plan_list = [self.planroot]
        while x_plan_list != []:
            parent_plan = x_plan_list.pop()
            for plan_kid in parent_plan.kids.values():
                self._eval_tree_metrics(
                    parent_plan, plan_kid, tree_metrics, x_plan_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_plan, plan_kid, tree_metrics, x_plan_list):
        plan_kid.tree_level = parent_plan.tree_level + 1
        tree_metrics.evaluate_label(
            tree_level=plan_kid.tree_level,
            reasons=plan_kid.reasonunits,
            awardunits=plan_kid.awardunits,
            plan_uid=plan_kid.plan_uid,
            pledge=plan_kid.pledge,
            plan_rope=plan_kid.get_plan_rope(),
        )
        x_plan_list.append(plan_kid)

    def get_plan_plan_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.plan_uid_max

    def set_all_plan_plan_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        plan_plan_uid_max = tree_metrics.plan_uid_max
        plan_plan_uid_dict = tree_metrics.plan_uid_dict

        for x_plan in self.get_plan_dict().values():
            if x_plan.plan_uid is None or plan_plan_uid_dict.get(x_plan.plan_uid) > 1:
                new_plan_plan_uid_max = plan_plan_uid_max + 1
                self.edit_plan_attr(
                    plan_rope=x_plan.get_plan_rope(), plan_uid=new_plan_plan_uid_max
                )
                plan_plan_uid_max = new_plan_plan_uid_max

    def get_reason_contexts(self) -> set[RopeTerm]:
        return set(self.get_tree_metrics().reason_contexts.keys())

    def get_missing_fact_reason_contexts(self) -> dict[RopeTerm, int]:
        tree_metrics = self.get_tree_metrics()
        reason_contexts = tree_metrics.reason_contexts
        missing_reason_contexts = {}
        for reason_context, reason_context_count in reason_contexts.items():
            try:
                self.planroot.factunits[reason_context]
            except KeyError:
                missing_reason_contexts[reason_context] = reason_context_count
        return missing_reason_contexts

    def add_plan(
        self, plan_rope: RopeTerm, star: float = None, pledge: bool = None
    ) -> PlanUnit:
        """default star is 0, pledges will have weight of 0 if star is not passed"""
        x_plan_label = get_tail_label(plan_rope, self.knot)
        x_parent_rope = get_parent_rope(plan_rope, self.knot)
        x_planunit = planunit_shop(x_plan_label, star=star)
        if pledge:
            x_planunit.pledge = True
        self.set_plan_obj(x_planunit, x_parent_rope)
        return x_planunit

    def set_l1_plan(
        self,
        plan_kid: PlanUnit,
        create_missing_plans: bool = None,
        get_rid_of_missing_awardunits_awardee_titles: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.set_plan_obj(
            plan_kid=plan_kid,
            parent_rope=self.planroot.get_plan_rope(),
            create_missing_plans=create_missing_plans,
            get_rid_of_missing_awardunits_awardee_titles=get_rid_of_missing_awardunits_awardee_titles,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def set_plan_obj(
        self,
        plan_kid: PlanUnit,
        parent_rope: RopeTerm,
        get_rid_of_missing_awardunits_awardee_titles: bool = None,
        create_missing_plans: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        parent_rope = to_rope(parent_rope, self.knot)
        if LabelTerm(plan_kid.plan_label).is_label(self.knot) is False:
            x_str = (
                f"set_plan failed because '{plan_kid.plan_label}' is not a LabelTerm."
            )
            raise InvalidPersonError(x_str)

        x_first_label = get_first_label_from_rope(parent_rope, self.knot)
        if self.planroot.plan_label != x_first_label:
            exception_str = f"set_plan failed because parent_rope '{parent_rope}' has an invalid root rope. Should be {self.planroot.get_plan_rope()}."
            raise InvalidPersonError(exception_str)

        plan_kid.knot = self.knot
        if plan_kid.fund_grain != self.fund_grain:
            plan_kid.fund_grain = self.fund_grain
        if not get_rid_of_missing_awardunits_awardee_titles:
            plan_kid = self._get_filtered_awardunits_plan(plan_kid)
        plan_kid.set_parent_rope(parent_rope=parent_rope)

        # create any missing plans
        if not create_missing_ancestors and self.plan_exists(parent_rope) is False:
            x_str = f"set_plan failed because '{parent_rope}' plan does not exist."
            raise InvalidPersonError(x_str)
        parent_rope_plan = self.get_plan_obj(parent_rope, create_missing_ancestors)
        parent_rope_plan.add_kid(plan_kid)

        kid_rope = self.make_rope(parent_rope, plan_kid.plan_label)
        if adoptees is not None:
            star_sum = 0
            for adoptee_plan_label in adoptees:
                adoptee_rope = self.make_rope(parent_rope, adoptee_plan_label)
                adoptee_plan = self.get_plan_obj(adoptee_rope)
                star_sum += adoptee_plan.star
                new_adoptee_parent_rope = self.make_rope(kid_rope, adoptee_plan_label)
                self.set_plan_obj(adoptee_plan, new_adoptee_parent_rope)
                self.edit_plan_attr(new_adoptee_parent_rope, star=adoptee_plan.star)
                self.del_plan_obj(adoptee_rope)

            if bundling:
                self.edit_plan_attr(kid_rope, star=star_sum)

        if create_missing_plans:
            self._create_missing_plans(rope=kid_rope)

    def _get_filtered_awardunits_plan(self, x_plan: PlanUnit) -> PlanUnit:
        awardunits_to_delete = [
            awardunit_awardee_title
            for awardunit_awardee_title in x_plan.awardunits.keys()
            if self.get_partnerunit_group_titles_dict().get(awardunit_awardee_title)
            is None
        ]
        for awardunit_awardee_title in awardunits_to_delete:
            x_plan.awardunits.pop(awardunit_awardee_title)
        if x_plan.workforceunit is not None:
            labors_to_delete = [
                _laborunit_labor_title
                for _laborunit_labor_title in x_plan.workforceunit.labors
                if self.get_partnerunit_group_titles_dict().get(_laborunit_labor_title)
                is None
            ]
            for _laborunit_labor_title in labors_to_delete:
                x_plan.workforceunit.del_laborunit(_laborunit_labor_title)
        return x_plan

    def _create_missing_plans(self, rope):
        self._set_plan_dict()
        posted_plan = self.get_plan_obj(rope)

        for x_reason in posted_plan.reasonunits.values():
            self._create_plankid_if_empty(rope=x_reason.reason_context)
            for case_x in x_reason.cases.values():
                self._create_plankid_if_empty(rope=case_x.reason_state)

    def _create_plankid_if_empty(self, rope: RopeTerm):
        if self.plan_exists(rope) is False:
            self.add_plan(rope)

    def del_plan_obj(self, rope: RopeTerm, del_children: bool = True):
        if rope == self.planroot.get_plan_rope():
            raise InvalidPersonError("Planroot cannot be deleted")
        parent_rope = get_parent_rope(rope)
        if self.plan_exists(rope):
            if not del_children:
                self._shift_plan_kids(x_rope=rope)
            parent_plan = self.get_plan_obj(parent_rope)
            parent_plan.del_kid(get_tail_label(rope, self.knot))
        self.conpute()

    def _shift_plan_kids(self, x_rope: RopeTerm):
        parent_rope = get_parent_rope(x_rope)
        d_temp_plan = self.get_plan_obj(x_rope)
        for kid in d_temp_plan.kids.values():
            self.set_plan_obj(kid, parent_rope=parent_rope)

    def set_person_name(self, new_person_name):
        self.person_name = new_person_name

    def edit_plan_label(self, old_rope: RopeTerm, new_plan_label: LabelTerm):
        if self.knot in new_plan_label:
            exception_str = f"Cannot modify '{old_rope}' because new_plan_label {new_plan_label} contains knot {self.knot}"
            raise InvalidLabelError(exception_str)
        if self.plan_exists(old_rope) is False:
            raise InvalidPersonError(f"Plan {old_rope=} does not exist")

        parent_rope = get_parent_rope(rope=old_rope)
        new_rope = (
            self.make_rope(new_plan_label)
            if parent_rope == ""
            else self.make_rope(parent_rope, new_plan_label)
        )
        if old_rope != new_rope:
            if parent_rope == "":
                self.planroot.set_plan_label(new_plan_label)
            else:
                self._non_root_plan_label_edit(old_rope, new_plan_label, parent_rope)
            self._planroot_find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    def _non_root_plan_label_edit(
        self, old_rope: RopeTerm, new_plan_label: LabelTerm, parent_rope: RopeTerm
    ):
        x_plan = self.get_plan_obj(old_rope)
        x_plan.set_plan_label(new_plan_label)
        x_plan.parent_rope = parent_rope
        plan_parent = self.get_plan_obj(get_parent_rope(old_rope))
        plan_parent.kids.pop(get_tail_label(old_rope, self.knot))
        plan_parent.kids[x_plan.plan_label] = x_plan

    def _planroot_find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.planroot.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

        plan_iter_list = [self.planroot]
        while plan_iter_list != []:
            listed_plan = plan_iter_list.pop()
            # add all plan_children in plan list
            if listed_plan.kids is not None:
                for plan_kid in listed_plan.kids.values():
                    plan_iter_list.append(plan_kid)
                    if is_sub_rope(plan_kid.parent_rope, sub_rope=old_rope):
                        plan_kid.parent_rope = rebuild_rope(
                            subj_rope=plan_kid.parent_rope,
                            old_rope=old_rope,
                            new_rope=new_rope,
                        )
                    plan_kid.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    def _set_planattrholder_case_ranges(self, x_planattrholder: PlanAttrHolder):
        case_plan = self.get_plan_obj(x_planattrholder.reason_case)
        x_planattrholder.set_case_range_influenced_by_case_plan(
            reason_lower=case_plan.begin,
            reason_upper=case_plan.close,
            case_denom=case_plan.denom,
        )

    def edit_reason(
        self,
        plan_rope: RopeTerm,
        reason_context: RopeTerm = None,
        reason_case: RopeTerm = None,
        reason_lower: ReasonNum = None,
        reason_upper: ReasonNum = None,
        reason_divisor: int = None,
    ):
        self.edit_plan_attr(
            plan_rope=plan_rope,
            reason_context=reason_context,
            reason_case=reason_case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
        )

    def edit_plan_attr(
        self,
        plan_rope: RopeTerm,
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
    ):
        if healerunit is not None:
            for x_healer_name in healerunit.healer_names:
                if self.get_partnerunit_group_titles_dict().get(x_healer_name) is None:
                    exception_str = f"Plan cannot edit healerunit because group_title '{x_healer_name}' does not exist as group in Person"
                    raise HealerunitGroupTitleError(exception_str)

        if (
            reason_context
            and reason_case
            and not is_sub_rope(reason_case, reason_context)
        ):
            raise ReasonCaseError(
                f"""Plan cannot edit reason because reason_case is not sub_rope to reason_context 
reason_context: {reason_context}
reason_case:    {reason_case}"""
            )

        x_planattrholder = planattrholder_shop(
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
            awardunit=awardunit,
            awardunit_del=awardunit_del,
            is_expanded=is_expanded,
            pledge=pledge,
            factunit=factunit,
            problem_bool=problem_bool,
        )
        if reason_case is not None:
            self._set_planattrholder_case_ranges(x_planattrholder)
        x_plan = self.get_plan_obj(plan_rope)
        x_plan._set_attrs_to_planunit(plan_attr=x_planattrholder)

    def get_agenda_dict(
        self, necessary_reason_context: RopeTerm = None
    ) -> dict[RopeTerm, PlanUnit]:
        self.conpute()
        return {
            x_plan.get_plan_rope(): x_plan
            for x_plan in self._plan_dict.values()
            if x_plan.is_agenda_plan(necessary_reason_context)
        }

    def get_all_pledges(self) -> dict[RopeTerm, PlanUnit]:
        self.conpute()
        all_plans = self._plan_dict.values()
        return {x_plan.get_plan_rope(): x_plan for x_plan in all_plans if x_plan.pledge}

    def set_agenda_plan_task_complete(
        self, plan_task_rope: RopeTerm, reason_context: RopeTerm
    ):
        pledge_plan = self.get_plan_obj(plan_task_rope)
        pledge_plan.set_factunit_to_complete(self.planroot.factunits[reason_context])

    def get_credit_ledger_debt_ledger(
        self,
    ) -> tuple[dict[str, float], dict[str, float]]:
        credit_ledger = {}
        debt_ledger = {}
        for x_partnerunit in self.partners.values():
            credit_ledger[x_partnerunit.partner_name] = x_partnerunit.partner_cred_lumen
            debt_ledger[x_partnerunit.partner_name] = x_partnerunit.partner_debt_lumen
        return credit_ledger, debt_ledger

    def _allot_offtrack_fund(self):
        self._add_to_partnerunits_fund_give_take(self.offtrack_fund)

    def get_partnerunits_partner_cred_lumen_sum(self) -> float:
        return sum(
            partnerunit.get_partner_cred_lumen()
            for partnerunit in self.partners.values()
        )

    def get_partnerunits_partner_debt_lumen_sum(self) -> float:
        return sum(
            partnerunit.get_partner_debt_lumen()
            for partnerunit in self.partners.values()
        )

    def _add_to_partnerunits_fund_give_take(self, plan_plan_fund_total: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(
            credor_ledger, plan_plan_fund_total, self.fund_grain
        )
        fund_take_allot = allot_scale(
            debtor_ledger, plan_plan_fund_total, self.fund_grain
        )
        for x_partner_name, partner_fund_give in fund_give_allot.items():
            self.get_partner(x_partner_name).add_fund_give(partner_fund_give)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self.reason_contexts:
                self.get_partner(x_partner_name).add_fund_agenda_give(partner_fund_give)
        for x_partner_name, partner_fund_take in fund_take_allot.items():
            self.get_partner(x_partner_name).add_fund_take(partner_fund_take)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self.reason_contexts:
                self.get_partner(x_partner_name).add_fund_agenda_take(partner_fund_take)

    def _add_to_partnerunits_fund_agenda_give_take(self, plan_plan_fund_total: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(
            credor_ledger, plan_plan_fund_total, self.fund_grain
        )
        fund_take_allot = allot_scale(
            debtor_ledger, plan_plan_fund_total, self.fund_grain
        )
        for x_partner_name, partner_fund_give in fund_give_allot.items():
            self.get_partner(x_partner_name).add_fund_agenda_give(partner_fund_give)
        for x_partner_name, partner_fund_take in fund_take_allot.items():
            self.get_partner(x_partner_name).add_fund_agenda_take(partner_fund_take)

    def _reset_groupunits_fund_give_take(self):
        for groupunit_obj in self.groupunits.values():
            groupunit_obj.clear_group_fund_give_take()

    def _set_groupunits_plan_fund_total(self, awardheirs: dict[GroupTitle, AwardUnit]):
        for awardunit_obj in awardheirs.values():
            x_awardee_title = awardunit_obj.awardee_title
            if not self.groupunit_exists(x_awardee_title):
                self.set_groupunit(self.create_symmetry_groupunit(x_awardee_title))
            self.add_to_groupunit_fund_give_fund_take(
                group_title=awardunit_obj.awardee_title,
                awardheir_fund_give=awardunit_obj.fund_give,
                awardheir_fund_take=awardunit_obj.fund_take,
            )

    def _allot_fund_person_agenda(self):
        for plan in self._plan_dict.values():
            # If there are no awardlines associated with plan
            # allot plan_fund_total via general partnerunit
            # cred ratio and debt ratio
            # if plan.is_agenda_plan() and plan.awardlines == {}:
            if plan.is_agenda_plan():
                if plan.awardheir_exists():
                    for x_awardline in plan.awardlines.values():
                        self.add_to_groupunit_fund_agenda_give_take(
                            group_title=x_awardline.awardee_title,
                            awardline_fund_give=x_awardline.fund_give,
                            awardline_fund_take=x_awardline.fund_take,
                        )
                else:
                    self._add_to_partnerunits_fund_agenda_give_take(
                        plan.get_plan_fund_total()
                    )

    def _allot_groupunits_fund(self):
        for x_groupunit in self.groupunits.values():
            x_groupunit._set_membership_fund_give_fund_take()
            for x_membership in x_groupunit.memberships.values():
                self.add_to_partnerunit_fund_give_take(
                    partnerunit_partner_name=x_membership.partner_name,
                    fund_give=x_membership.fund_give,
                    fund_take=x_membership.fund_take,
                    fund_agenda_give=x_membership.fund_agenda_give,
                    fund_agenda_take=x_membership.fund_agenda_take,
                )

    def _set_partnerunits_fund_agenda_ratios(self):
        fund_agenda_ratio_give_sum = sum(
            x_partnerunit.fund_agenda_give for x_partnerunit in self.partners.values()
        )
        fund_agenda_ratio_take_sum = sum(
            x_partnerunit.fund_agenda_take for x_partnerunit in self.partners.values()
        )
        x_partnerunits_partner_cred_lumen_sum = (
            self.get_partnerunits_partner_cred_lumen_sum()
        )
        x_partnerunits_partner_debt_lumen_sum = (
            self.get_partnerunits_partner_debt_lumen_sum()
        )
        for x_partnerunit in self.partners.values():
            x_partnerunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                partnerunits_partner_cred_lumen_sum=x_partnerunits_partner_cred_lumen_sum,
                partnerunits_partner_debt_lumen_sum=x_partnerunits_partner_debt_lumen_sum,
            )

    def _reset_partnerunit_fund_give_take(self):
        for partnerunit in self.partners.values():
            partnerunit.clear_fund_give_take()

    def plan_exists(self, rope: RopeTerm) -> bool:
        if rope in {"", None}:
            return False
        root_rope_plan_label = get_first_label_from_rope(rope, self.knot)
        if root_rope_plan_label != self.planroot.plan_label:
            return False

        labels = get_all_rope_labels(rope, knot=self.knot)
        root_rope_plan_label = labels.pop(0)
        if labels == []:
            return True

        plan_label = labels.pop(0)
        x_plan = self.planroot.get_kid(plan_label)
        if x_plan is None:
            return False
        while labels != []:
            plan_label = labels.pop(0)
            x_plan = x_plan.get_kid(plan_label)
            if x_plan is None:
                return False
        return True

    def get_plan_obj(self, rope: RopeTerm, if_missing_create: bool = False) -> PlanUnit:
        if rope is None:
            raise InvalidPersonError("get_plan_obj received rope=None")
        if self.plan_exists(rope) is False and not if_missing_create:
            raise InvalidPersonError(f"get_plan_obj failed. no plan at '{rope}'")
        labelterms = get_all_rope_labels(rope, knot=self.knot)
        if len(labelterms) == 1:
            return self.planroot

        labelterms.pop(0)
        plan_label = labelterms.pop(0)
        x_plan = self.planroot.get_kid(plan_label, if_missing_create)
        while labelterms != []:
            x_plan = x_plan.get_kid(labelterms.pop(0), if_missing_create)

        return x_plan

    def get_plan_ranged_kids(
        self, plan_rope: str, x_gogo_calc: float = None, x_stop_calc: float = None
    ) -> dict[PlanUnit]:
        x_plan = self.get_plan_obj(plan_rope)
        return x_plan.get_kids_in_range(x_gogo_calc, x_stop_calc)

    def get_inheritor_plan_list(
        self, range_rope: RopeTerm, inheritor_rope: RopeTerm
    ) -> list[PlanUnit]:
        plan_ropes = all_ropes_between(range_rope, inheritor_rope)
        return [self.get_plan_obj(x_plan_rope) for x_plan_rope in plan_ropes]

    def _set_plan_dict(self):
        plan_list = [self.planroot]
        while plan_list != []:
            x_plan = plan_list.pop()
            x_plan.clear_gogo_calc_stop_calc()
            for plan_kid in x_plan.kids.values():
                plan_kid.set_parent_rope(x_plan.get_plan_rope())
                plan_kid.set_tree_level(x_plan.tree_level)
                plan_list.append(plan_kid)
            self._plan_dict[x_plan.get_plan_rope()] = x_plan
            for x_reason_context in x_plan.reasonunits.keys():
                self.reason_contexts.add(x_reason_context)

    def _distribute_range_attrs(self, rangeroot_plan: PlanUnit):
        """Populates PersonUnit.range_inheritors, sets PlanUnit.gogo_calc, PlanUnit.stop_calc"""
        single_rangeroot_plan_list = [rangeroot_plan]
        while single_rangeroot_plan_list != []:
            x_planunit = single_rangeroot_plan_list.pop()
            x_plan_rope = x_planunit.get_plan_rope()
            if x_planunit.range_evaluated:
                exception_str = f"Error has occurred, Plan '{x_plan_rope}' is having gogo_calc and stop_calc set twice"
                raise GogoCalcStopCalcError(exception_str)
            if x_planunit.has_begin_close():
                x_planunit.gogo_calc = x_planunit.begin
                x_planunit.stop_calc = x_planunit.close
            else:
                parent_rope = get_parent_rope(x_plan_rope, x_planunit.knot)
                parent_plan = self.get_plan_obj(parent_rope)
                x_planunit.gogo_calc = parent_plan.gogo_calc
                x_planunit.stop_calc = parent_plan.stop_calc
                self.range_inheritors[x_plan_rope] = rangeroot_plan.get_plan_rope()
            x_planunit._mold_gogo_calc_stop_calc()
            single_rangeroot_plan_list.extend(iter(x_planunit.kids.values()))

    def _set_plantree_range_attrs(self):
        for x_plan in self._plan_dict.values():
            if x_plan.has_begin_close():
                self._distribute_range_attrs(x_plan)

            if (
                not x_plan.is_kidless()
                and x_plan.get_kids_star_sum() == 0
                and x_plan.star != 0
            ):
                self.offtrack_kids_star_set.add(x_plan.get_plan_rope())

    def _set_groupunit_partnerunit_funds(self, keep_exceptions):
        for x_plan in self._plan_dict.values():
            x_plan.set_awardheirs_fund_give_fund_take()
            if x_plan.is_kidless():
                self._set_ancestors_pledge_fund_keep_attrs(
                    x_plan.get_plan_rope(), keep_exceptions
                )
                self._allot_plan_fund_total(x_plan)

    def _set_ancestors_pledge_fund_keep_attrs(
        self, rope: RopeTerm, keep_exceptions: bool = False
    ):
        x_descendant_pledge_count = 0
        child_awardlines = None
        group_everyone = None
        ancestor_ropes = get_ancestor_ropes(rope, self.knot)
        keep_justified_by_problem = True
        healerunit_count = 0

        while ancestor_ropes != []:
            youngest_rope = ancestor_ropes.pop(0)
            x_plan_obj = self.get_plan_obj(youngest_rope)
            x_plan_obj.add_to_descendant_pledge_count(x_descendant_pledge_count)
            if x_plan_obj.is_kidless():
                x_plan_obj.set_kidless_awardlines()
                child_awardlines = x_plan_obj.awardlines
            else:
                x_plan_obj.set_awardlines(child_awardlines)

            if x_plan_obj.plan_task:
                x_descendant_pledge_count += 1

            if (
                group_everyone != False
                and x_plan_obj.all_partner_cred != False
                and x_plan_obj.all_partner_debt != False
                and x_plan_obj.awardheirs != {}
            ) or (
                group_everyone != False
                and x_plan_obj.all_partner_cred is False
                and x_plan_obj.all_partner_debt is False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_plan_obj.all_partner_cred = group_everyone
            x_plan_obj.all_partner_debt = group_everyone

            if x_plan_obj.healerunit.any_healer_name_exists():
                keep_justified_by_problem = False
                healerunit_count += 1
                self.sum_healerunit_plans_fund_total += x_plan_obj.get_plan_fund_total()
            if x_plan_obj.problem_bool:
                keep_justified_by_problem = True

        if keep_justified_by_problem is False or healerunit_count > 1:
            if keep_exceptions:
                exception_str = f"PlanUnit '{rope}' cannot sponsor ancestor keeps."
                raise KeepJustError(exception_str)
            self.keeps_justified = False

    def _clear_plantree_fund_and_plan_active(self):
        for x_plan in self._plan_dict.values():
            x_plan.clear_awardlines()
            x_plan.clear_descendant_pledge_count()
            x_plan.clear_all_partner_cred_debt()

    def _set_kids_plan_active(self, x_plan: PlanUnit, parent_plan: PlanUnit):
        x_plan.set_reasonheirs(self._plan_dict, parent_plan.reasonheirs)
        x_plan.set_range_inheritors_factheirs(self._plan_dict, self.range_inheritors)
        tt_count = self.tree_traverse_count
        x_plan.set_plan_active(tt_count, self.groupunits, self.person_name)

    def _allot_plan_fund_total(self, plan: PlanUnit):
        if plan.awardheir_exists():
            self._set_groupunits_plan_fund_total(plan.awardheirs)
        elif plan.awardheir_exists() is False:
            self._add_to_partnerunits_fund_give_take(plan.get_plan_fund_total())

    def _create_groupunits_metrics(self):
        self.groupunits = {}
        for (
            group_title,
            partner_name_set,
        ) in self.get_partnerunit_group_titles_dict().items():
            x_groupunit = groupunit_shop(group_title)
            for x_partner_name in partner_name_set:
                x_membership = self.get_partner(x_partner_name).get_membership(
                    group_title
                )
                x_groupunit.set_g_membership(x_membership)
                self.set_groupunit(x_groupunit)

    def _set_partnerunit_groupunit_respect_ledgers(self):
        self.credor_respect = RespectNum(validate_pool_num(self.credor_respect))
        self.debtor_respect = RespectNum(validate_pool_num(self.debtor_respect))
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        credor_allot = allot_scale(
            credor_ledger, self.credor_respect, self.respect_grain
        )
        debtor_allot = allot_scale(
            debtor_ledger, self.debtor_respect, self.respect_grain
        )
        for x_partner_name, partner_credor_pool in credor_allot.items():
            self.get_partner(x_partner_name).set_credor_pool(partner_credor_pool)
        for x_partner_name, partner_debtor_pool in debtor_allot.items():
            self.get_partner(x_partner_name).set_debtor_pool(partner_debtor_pool)
        self._create_groupunits_metrics()
        self._reset_partnerunit_fund_give_take()

    def _clear_plan_dict_and_person_obj_settle_attrs(self):
        self._plan_dict = {self.planroot.get_plan_rope(): self.planroot}
        self.rational = False
        self.tree_traverse_count = 0
        self.offtrack_kids_star_set = set()
        self.reason_contexts = set()
        self.range_inheritors = {}
        self.keeps_justified = True
        self.keeps_buildable = False
        self.sum_healerunit_plans_fund_total = 0
        self._keep_dict = {}
        self._healers_dict = {}

    def _set_plantree_factheirs_workforceheir_awardheirs(self):
        for x_plan in get_sorted_plan_list(self._plan_dict):
            if x_plan == self.planroot:
                x_plan.set_factheirs(x_plan.factunits)
                x_plan.set_root_plan_reasonheirs()
                x_plan.set_workforceheir(None, self.groupunits)
                x_plan.inherit_awardheirs()
            else:
                parent_plan = self.get_plan_obj(x_plan.parent_rope)
                x_plan.set_factheirs(parent_plan.factheirs)
                x_plan.set_workforceheir(parent_plan.workforceheir, self.groupunits)
                x_plan.inherit_awardheirs(parent_plan.awardheirs)
            x_plan.set_awardheirs_fund_give_fund_take()

    def conpute(self, keep_exceptions: bool = False):
        self._clear_plan_dict_and_person_obj_settle_attrs()
        self._set_plan_dict()
        self._set_plantree_range_attrs()
        self._set_partnerunit_groupunit_respect_ledgers()
        self._clear_partnerunit_fund_attrs()
        self._clear_plantree_fund_and_plan_active()
        self._set_plantree_factheirs_workforceheir_awardheirs()

        max_count = self.max_tree_traverse
        while not self.rational and self.tree_traverse_count < max_count:
            self._set_plantree_plan_active()
            self._set_rational_attr()
            self.tree_traverse_count += 1

        self._set_plantree_fund_attrs(self.planroot)
        self._set_groupunit_partnerunit_funds(keep_exceptions)
        self._set_partnerunit_fund_related_attrs()
        self._set_person_keep_attrs()

    def _set_plantree_plan_active(self):
        """For every planunit in the PlanTree set plan_active to True or False.
        Assumes self.range_inheritors is set with set of ropes for all PlanUnits that
        inherit from a ranged PlanUnit.
        """

        for x_plan in get_sorted_plan_list(self._plan_dict):
            if x_plan == self.planroot:
                tt_count = self.tree_traverse_count
                root_plan = self.planroot
                root_plan.set_plan_active(tt_count, self.groupunits, self.person_name)
            else:
                parent_plan = self.get_plan_obj(x_plan.parent_rope)
                self._set_kids_plan_active(x_plan, parent_plan)

    def _set_plantree_fund_attrs(self, root_plan: PlanUnit):
        root_plan.set_fund_attr(0, self.fund_pool, self.fund_pool)
        # no function recursion, recursion by iterateing over list that can be added to by iterations
        cache_plan_list = [root_plan]
        while cache_plan_list != []:
            parent_plan = cache_plan_list.pop()
            kids_plans = parent_plan.kids.items()
            x_ledger = {x_rope: plan_kid.star for x_rope, plan_kid in kids_plans}
            parent_fund_num = parent_plan.fund_cease - parent_plan.fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self.fund_grain)

            fund_onset = None
            fund_cease = None
            for x_plan in parent_plan.kids.values():
                if fund_onset is None:
                    fund_onset = parent_plan.fund_onset
                    fund_cease = fund_onset + alloted_fund_num.get(x_plan.plan_label)
                else:
                    fund_onset = fund_cease
                    fund_cease += alloted_fund_num.get(x_plan.plan_label)
                x_plan.set_fund_attr(fund_onset, fund_cease, self.fund_pool)
                cache_plan_list.append(x_plan)

    def _set_rational_attr(self):
        any_plan_active_has_altered = False
        for plan in self._plan_dict.values():
            if plan.plan_active_hx.get(self.tree_traverse_count) is not None:
                any_plan_active_has_altered = True

        if any_plan_active_has_altered is False:
            self.rational = True

    def _set_partnerunit_fund_related_attrs(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_person_agenda()
        self._allot_groupunits_fund()
        self._set_partnerunits_fund_agenda_ratios()

    def _set_person_keep_attrs(self):
        self._set_keep_dict()
        self._healers_dict = self._get_healers_dict()
        self.keeps_buildable = self._get_buildable_keeps()

    def _set_keep_dict(self):
        if self.keeps_justified is False:
            self.sum_healerunit_plans_fund_total = 0
        for x_plan in self._plan_dict.values():
            if self.sum_healerunit_plans_fund_total == 0:
                x_plan.healerunit_ratio = 0
            else:
                x_sum = self.sum_healerunit_plans_fund_total
                x_plan.healerunit_ratio = x_plan.get_plan_fund_total() / x_sum
            if self.keeps_justified and x_plan.healerunit.any_healer_name_exists():
                self._keep_dict[x_plan.get_plan_rope()] = x_plan

    def _get_healers_dict(self) -> dict[HealerName, dict[RopeTerm, PlanUnit]]:
        _healers_dict = {}
        for x_keep_rope, x_keep_plan in self._keep_dict.items():
            for x_healer_name in x_keep_plan.healerunit.healer_names:
                x_groupunit = self.get_groupunit(x_healer_name)
                for x_partner_name in x_groupunit.memberships.keys():
                    if _healers_dict.get(x_partner_name) is None:
                        _healers_dict[x_partner_name] = {x_keep_rope: x_keep_plan}
                    else:
                        healer_dict = _healers_dict.get(x_partner_name)
                        healer_dict[x_keep_rope] = x_keep_plan
        return _healers_dict

    def _get_buildable_keeps(self) -> bool:
        return all(
            rope_is_valid_dir_path(keep_rope, self.knot) != False
            for keep_rope in self._keep_dict.keys()
        )

    def _clear_partnerunit_fund_attrs(self):
        self._reset_groupunits_fund_give_take()
        self._reset_partnerunit_fund_give_take()

    def get_plan_tree_ordered_rope_list(
        self, no_range_descendants: bool = False
    ) -> list[RopeTerm]:
        plan_list = list(self.get_plan_dict().values())
        label_dict = {
            plan.get_plan_rope().lower(): plan.get_plan_rope() for plan in plan_list
        }
        label_same_capitalization_ordered_list = sorted(list(label_dict))
        label_orginalcapitalization_ordered_list = [
            label_dict[label_l] for label_l in label_same_capitalization_ordered_list
        ]

        list_x = []
        for rope in label_orginalcapitalization_ordered_list:
            if not no_range_descendants:
                list_x.append(rope)
            else:
                anc_list = get_ancestor_ropes(rope=rope)
                if len(anc_list) == 1:
                    list_x.append(rope)
                elif len(anc_list) == 2:
                    if self.planroot.begin is None and self.planroot.close is None:
                        list_x.append(rope)
                else:
                    parent_plan = self.get_plan_obj(rope=anc_list[1])
                    if parent_plan.begin is None and parent_plan.close is None:
                        list_x.append(rope)

        return list_x

    def get_planroot_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self.planroot.factunits is not None:
            for fact_rope, fact_obj in self.planroot.factunits.items():
                x_dict[fact_rope] = fact_obj.to_dict()
        return x_dict

    def get_partnerunits_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {}
        if self.partners is not None:
            for partner_name, partner_obj in self.partners.items():
                x_dict[partner_name] = partner_obj.to_dict(all_attrs)
        return x_dict

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "person_name": self.person_name,
            "fund_grain": self.fund_grain,
            "fund_pool": self.fund_pool,
            "knot": self.knot,
            "mana_grain": self.mana_grain,
            "max_tree_traverse": self.max_tree_traverse,
            "planroot": self.planroot.to_dict(),
            "respect_grain": self.respect_grain,
            "partners": self.get_partnerunits_dict(),
        }
        if self.credor_respect is not None:
            x_dict["credor_respect"] = self.credor_respect
        if self.debtor_respect is not None:
            x_dict["debtor_respect"] = self.debtor_respect
        if self.last_lesson_id is not None:
            x_dict["last_lesson_id"] = self.last_lesson_id

        return x_dict

    def set_dominate_pledge_plan(self, plan_kid: PlanUnit):
        plan_kid.pledge = True
        self.set_plan_obj(
            plan_kid=plan_kid,
            parent_rope=self.make_rope(plan_kid.parent_rope),
            get_rid_of_missing_awardunits_awardee_titles=True,
            create_missing_plans=True,
        )

    def set_offtrack_fund(self) -> float:
        star_set = self.offtrack_kids_star_set
        self.offtrack_fund = sum(
            self.get_plan_obj(rope).get_plan_fund_total() for rope in star_set
        )


def personunit_shop(
    person_name: PersonName = None,
    planroot_rope: RopeTerm = None,
    knot: KnotTerm = None,
    fund_pool: FundNum = None,
    fund_grain: FundGrain = None,
    respect_grain: RespectGrain = None,
    mana_grain: ManaGrain = None,
) -> PersonUnit:
    knot = default_knot_if_None(knot)
    person_name = "" if person_name is None else person_name
    planroot_rope = get_default_rope(knot) if planroot_rope is None else planroot_rope
    if is_labelterm(planroot_rope, knot):
        exception_str = f"Person '{person_name}' cannot set planroot_rope='{planroot_rope}' where knot='{knot}'"
        raise IsRopeTermError(exception_str)
    x_person = PersonUnit(
        person_name=person_name,
        partners=get_empty_dict_if_None(),
        groupunits={},
        knot=knot,
        credor_respect=RespectNum(validate_pool_num()),
        debtor_respect=RespectNum(validate_pool_num()),
        fund_pool=validate_pool_num(fund_pool),
        fund_grain=grain_num(fund_grain),
        respect_grain=grain_num(respect_grain),
        mana_grain=grain_num(mana_grain),
        _plan_dict=get_empty_dict_if_None(),
        _keep_dict=get_empty_dict_if_None(),
        _healers_dict=get_empty_dict_if_None(),
        keeps_justified=get_False_if_None(),
        keeps_buildable=get_False_if_None(),
        sum_healerunit_plans_fund_total=get_0_if_None(),
        offtrack_kids_star_set=set(),
        reason_contexts=set(),
        range_inheritors={},
    )
    x_person.planroot = planunit_shop(
        plan_label=get_tail_label(planroot_rope, knot),
        plan_uid=1,
        tree_level=0,
        knot=x_person.knot,
        fund_grain=x_person.fund_grain,
        parent_rope=get_parent_rope(planroot_rope, knot),
    )
    x_person.set_max_tree_traverse(3)
    x_person.rational = False
    return x_person


def get_personunit_from_dict(person_dict: dict) -> PersonUnit:
    x_person = personunit_shop()
    x_person.set_person_name(obj_from_person_dict(person_dict, "person_name"))
    x_person.set_max_tree_traverse(
        obj_from_person_dict(person_dict, "max_tree_traverse")
    )
    person_knot = obj_from_person_dict(person_dict, "knot")
    x_person.knot = default_knot_if_None(person_knot)
    x_person.fund_pool = validate_pool_num(
        obj_from_person_dict(person_dict, "fund_pool")
    )
    x_person.fund_grain = grain_num(obj_from_person_dict(person_dict, "fund_grain"))
    x_person.respect_grain = grain_num(
        obj_from_person_dict(person_dict, "respect_grain")
    )
    x_person.mana_grain = grain_num(obj_from_person_dict(person_dict, "mana_grain"))
    x_person.credor_respect = obj_from_person_dict(person_dict, "credor_respect")
    x_person.debtor_respect = obj_from_person_dict(person_dict, "debtor_respect")
    x_person.last_lesson_id = obj_from_person_dict(person_dict, "last_lesson_id")
    x_knot = x_person.knot
    x_partners = obj_from_person_dict(person_dict, "partners", x_knot).values()
    for x_partnerunit in x_partners:
        x_person.set_partnerunit(x_partnerunit)
    create_planroot_from_person_dict(x_person, person_dict)

    return x_person


def create_planroot_from_person_dict(x_person: PersonUnit, person_dict: dict):
    planroot_dict = person_dict.get("planroot")
    x_person.planroot = planunit_shop(
        plan_label=get_obj_from_plan_dict(planroot_dict, "plan_label"),
        parent_rope="",
        tree_level=0,
        plan_uid=get_obj_from_plan_dict(planroot_dict, "plan_uid"),
        star=get_obj_from_plan_dict(planroot_dict, "star"),
        begin=get_obj_from_plan_dict(planroot_dict, "begin"),
        close=get_obj_from_plan_dict(planroot_dict, "close"),
        numor=get_obj_from_plan_dict(planroot_dict, "numor"),
        denom=get_obj_from_plan_dict(planroot_dict, "denom"),
        morph=get_obj_from_plan_dict(planroot_dict, "morph"),
        addin=get_obj_from_plan_dict(planroot_dict, "addin"),
        gogo_want=get_obj_from_plan_dict(planroot_dict, "gogo_want"),
        stop_want=get_obj_from_plan_dict(planroot_dict, "stop_want"),
        problem_bool=get_obj_from_plan_dict(planroot_dict, "problem_bool"),
        reasonunits=get_obj_from_plan_dict(planroot_dict, "reasonunits"),
        workforceunit=get_obj_from_plan_dict(planroot_dict, "workforceunit"),
        healerunit=get_obj_from_plan_dict(planroot_dict, "healerunit"),
        factunits=get_obj_from_plan_dict(planroot_dict, "factunits"),
        awardunits=get_obj_from_plan_dict(planroot_dict, "awardunits"),
        is_expanded=get_obj_from_plan_dict(planroot_dict, "is_expanded"),
        knot=x_person.knot,
        fund_grain=grain_num(x_person.fund_grain),
    )
    create_planroot_kids_from_dict(x_person, planroot_dict)


def create_planroot_kids_from_dict(x_person: PersonUnit, planroot_dict: dict):
    to_evaluate_plan_dicts = []
    parent_rope_str = "parent_rope"
    # for every kid dict, set parent_rope in dict, add to to_evaluate_list
    for x_dict in get_obj_from_plan_dict(planroot_dict, "kids").values():
        x_dict[parent_rope_str] = x_person.planroot.get_plan_rope()
        to_evaluate_plan_dicts.append(x_dict)

    while to_evaluate_plan_dicts != []:
        plan_dict = to_evaluate_plan_dicts.pop(0)
        # for every kid dict, set parent_rope in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_plan_dict(plan_dict, "kids").values():
            parent_rope = get_obj_from_plan_dict(plan_dict, parent_rope_str)
            kid_plan_label = get_obj_from_plan_dict(plan_dict, "plan_label")
            kid_dict[parent_rope_str] = x_person.make_rope(parent_rope, kid_plan_label)
            to_evaluate_plan_dicts.append(kid_dict)
        x_plankid = planunit_shop(
            plan_label=get_obj_from_plan_dict(plan_dict, "plan_label"),
            star=get_obj_from_plan_dict(plan_dict, "star"),
            plan_uid=get_obj_from_plan_dict(plan_dict, "plan_uid"),
            begin=get_obj_from_plan_dict(plan_dict, "begin"),
            close=get_obj_from_plan_dict(plan_dict, "close"),
            numor=get_obj_from_plan_dict(plan_dict, "numor"),
            denom=get_obj_from_plan_dict(plan_dict, "denom"),
            morph=get_obj_from_plan_dict(plan_dict, "morph"),
            addin=get_obj_from_plan_dict(plan_dict, "addin"),
            gogo_want=get_obj_from_plan_dict(plan_dict, "gogo_want"),
            stop_want=get_obj_from_plan_dict(plan_dict, "stop_want"),
            pledge=get_obj_from_plan_dict(plan_dict, "pledge"),
            problem_bool=get_obj_from_plan_dict(plan_dict, "problem_bool"),
            reasonunits=get_obj_from_plan_dict(plan_dict, "reasonunits"),
            workforceunit=get_obj_from_plan_dict(plan_dict, "workforceunit"),
            healerunit=get_obj_from_plan_dict(plan_dict, "healerunit"),
            awardunits=get_obj_from_plan_dict(plan_dict, "awardunits"),
            factunits=get_obj_from_plan_dict(plan_dict, "factunits"),
            is_expanded=get_obj_from_plan_dict(plan_dict, "is_expanded"),
        )
        x_person.set_plan_obj(x_plankid, parent_rope=plan_dict[parent_rope_str])


def obj_from_person_dict(
    x_dict: dict[str, dict], dict_key: str, _knot: KnotTerm = None
) -> any:
    if dict_key == "partners":
        return partnerunits_get_from_dict(x_dict[dict_key], _knot)
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) is not None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def get_dict_of_person_from_dict(x_dict: dict[str, dict]) -> dict[str, PersonUnit]:
    personunits = {}
    for personunit_dict in x_dict.values():
        x_person = get_personunit_from_dict(person_dict=personunit_dict)
        personunits[x_person.person_name] = x_person
    return personunits


def get_sorted_plan_list(
    x_dict: dict[RopeTerm, PlanUnit], sorting_key: str = None
) -> list[PlanUnit]:
    """Returns sorted list of PlanUnits. Default sort is by plan_rope.
    "fund_ratio" is passable key"""
    x_list = list(x_dict.values())
    if sorting_key in {"fund_ratio"}:
        x_list.sort(key=lambda x: (-x.fund_ratio, x.get_plan_rope()))
    else:
        x_list.sort(key=lambda x: x.get_plan_rope(), reverse=False)
    return x_list
