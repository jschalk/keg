from src.ch00_py.dict_toolbox import (
    create_csv,
    get_1_if_None,
    get_empty_str_if_None,
    modular_addition,
)
from src.ch01_allot.allot import allot_scale
from src.ch02_partner.group import AwardUnit, MemberShip
from src.ch02_partner.partner import PartnerUnit, calc_give_take_net
from src.ch04_rope.rope import get_unique_short_ropes, is_sub_rope
from src.ch05_reason.reason_main import (
    CaseUnit,
    FactUnit,
    ReasonUnit,
    get_factunits_from_dict,
)
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic._ref.ch07_semantic_types import (
    FundNum,
    PartnerName,
    RespectNum,
    RopeTerm,
)
from src.ch07_person_logic.person_main import PersonUnit


def personunit_exists(x_person: PersonUnit) -> bool:
    return x_person is not None


def person_partnerunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_partner_name = jkeys.get("partner_name")
    return False if x_person is None else x_person.partner_exists(x_partner_name)


def person_partner_membership_exists(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> bool:
    x_partner_name = jkeys.get("partner_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        person_partnerunit_exists(x_person, jkeys)
        and x_person.get_partner(x_partner_name).membership_exists(x_group_title)
    )


def person_planunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    return False if x_person is None else bool(x_person.plan_exists(x_rope))


def person_plan_awardunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        person_planunit_exists(x_person, jkeys)
        and x_person.get_plan_obj(x_rope).awardunit_exists(x_awardee_title)
    )


def person_plan_reasonunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    return bool(
        person_planunit_exists(x_person, jkeys)
        and x_person.get_plan_obj(x_rope).reasonunit_exists(x_reason_context)
    )


def person_plan_reason_caseunit_exists(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    x_reason_state = jkeys.get("reason_state")
    return bool(
        person_plan_reasonunit_exists(x_person, jkeys)
        and x_person.get_plan_obj(x_rope)
        .get_reasonunit(x_reason_context)
        .case_exists(x_reason_state)
    )


def person_plan_partyunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_party_title = jkeys.get("party_title")
    x_rope = jkeys.get("plan_rope")
    return bool(
        person_planunit_exists(x_person, jkeys)
        and x_person.get_plan_obj(x_rope).laborunit.partyunit_exists(x_party_title)
    )


def person_plan_healerunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_rope = jkeys.get("plan_rope")
    return bool(
        person_planunit_exists(x_person, jkeys)
        and x_person.get_plan_obj(x_rope).healerunit.healer_name_exists(x_healer_name)
    )


def person_plan_factunit_exists(x_person: PersonUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("plan_rope")
    x_fact_context = jkeys.get("fact_context")
    return bool(
        person_planunit_exists(x_person, jkeys)
        and x_person.get_plan_obj(x_rope).factunit_exists(x_fact_context)
    )


def person_attr_exists(
    x_dimen: str, x_person: PersonUnit, jkeys: dict[str, any]
) -> bool:
    if x_dimen == "person_partner_membership":
        return person_partner_membership_exists(x_person, jkeys)
    elif x_dimen == "person_partnerunit":
        return person_partnerunit_exists(x_person, jkeys)
    elif x_dimen == "person_plan_awardunit":
        return person_plan_awardunit_exists(x_person, jkeys)
    elif x_dimen == "person_plan_factunit":
        return person_plan_factunit_exists(x_person, jkeys)
    elif x_dimen == "person_plan_healerunit":
        return person_plan_healerunit_exists(x_person, jkeys)
    elif x_dimen == "person_plan_reason_caseunit":
        return person_plan_reason_caseunit_exists(x_person, jkeys)
    elif x_dimen == "person_plan_reasonunit":
        return person_plan_reasonunit_exists(x_person, jkeys)
    elif x_dimen == "person_plan_partyunit":
        return person_plan_partyunit_exists(x_person, jkeys)
    elif x_dimen == "person_planunit":
        return person_planunit_exists(x_person, jkeys)
    elif x_dimen == "personunit":
        return personunit_exists(x_person)
    return True


def person_partnerunit_get_obj(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> PartnerUnit:
    return x_person.get_partner(jkeys.get("partner_name"))


def person_partner_membership_get_obj(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> MemberShip:
    x_partner_name = jkeys.get("partner_name")
    x_group_title = jkeys.get("group_title")
    return x_person.get_partner(x_partner_name).get_membership(x_group_title)


def person_planunit_get_obj(x_person: PersonUnit, jkeys: dict[str, any]) -> PlanUnit:
    x_rope = jkeys.get("plan_rope")
    return x_person.get_plan_obj(x_rope)


def person_plan_awardunit_get_obj(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> AwardUnit:
    x_rope = jkeys.get("plan_rope")
    x_awardee_title = jkeys.get("awardee_title")
    return x_person.get_plan_obj(x_rope).get_awardunit(x_awardee_title)


def person_plan_reasonunit_get_obj(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> ReasonUnit:
    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    return x_person.get_plan_obj(x_rope).get_reasonunit(x_reason_context)


def person_plan_reason_caseunit_get_obj(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> CaseUnit:
    """jkeys: plan_rope, reason_context, reason_state"""

    x_rope = jkeys.get("plan_rope")
    x_reason_context = jkeys.get("reason_context")
    x_reason_state = jkeys.get("reason_state")
    return (
        x_person.get_plan_obj(x_rope)
        .get_reasonunit(x_reason_context)
        .get_case(x_reason_state)
    )


def person_plan_factunit_get_obj(
    x_person: PersonUnit, jkeys: dict[str, any]
) -> FactUnit:
    x_rope = jkeys.get("plan_rope")
    x_fact_context = jkeys.get("fact_context")
    return x_person.get_plan_obj(x_rope).factunits.get(x_fact_context)


def person_get_obj(x_dimen: str, x_person: PersonUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "personunit":
        return x_person

    x_dimens = {
        "person_partnerunit": person_partnerunit_get_obj,
        "person_partner_membership": person_partner_membership_get_obj,
        "person_planunit": person_planunit_get_obj,
        "person_plan_awardunit": person_plan_awardunit_get_obj,
        "person_plan_reasonunit": person_plan_reasonunit_get_obj,
        "person_plan_reason_caseunit": person_plan_reason_caseunit_get_obj,
        "person_plan_factunit": person_plan_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_person, jkeys)


def get_person_partner_agenda_award_array(
    x_person: PersonUnit, conpute: bool = None
) -> list[list]:
    if conpute:
        x_person.conpute()

    x_list = [
        [
            x_partner.partner_name,
            x_partner.fund_agenda_take,
            x_partner.fund_agenda_give,
        ]
        for x_partner in x_person.partners.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_person_partner_agenda_award_csv(
    x_person: PersonUnit, conpute: bool = None
) -> str:
    x_partner_agenda_award_array = get_person_partner_agenda_award_array(
        x_person, conpute
    )
    x_headers = ["partner_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_partner_agenda_award_array)


def get_partner_mandate_ledger(
    x_person: PersonUnit, conpute: bool = None
) -> dict[PartnerName, FundNum]:
    if not x_person:
        return {}
    if len(x_person.partners) == 0:
        return {x_person.person_name: x_person.fund_pool}

    if conpute:
        x_person.conpute()
    person_partners = x_person.partners.values()
    mandates = {
        x_partner.partner_name: x_partner.fund_agenda_give
        for x_partner in person_partners
    }
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = reset_mandates_to_minimum(mandates, x_person.mana_grain)
    if mandate_sum != x_person.fund_pool:
        mandates = allot_scale(mandates, x_person.fund_pool, x_person.fund_grain)
    return mandates


def reset_mandates_to_minimum(
    mandates: dict[PartnerName, FundNum], mana_grain: FundNum
) -> dict[PartnerName, FundNum]:
    """Reset all mandates to the minimum value (mana_grain)."""

    partner_names = set(mandates.keys())
    for partner_name in partner_names:
        mandates[partner_name] = mana_grain
    return mandates


def get_partner_agenda_net_ledger(
    x_person: PersonUnit, conpute: bool = None
) -> dict[PartnerName, FundNum]:
    if conpute:
        x_person.conpute()

    x_dict = {}
    for x_partner in x_person.partners.values():
        settle_net = calc_give_take_net(
            x_partner.fund_agenda_give, x_partner.fund_agenda_take
        )
        if settle_net != 0:
            x_dict[x_partner.partner_name] = settle_net
    return x_dict


def get_credit_ledger(x_person: PersonUnit) -> dict[PartnerUnit, RespectNum]:
    credit_ledger, debt_ledger = x_person.get_credit_ledger_debt_ledger()
    return credit_ledger


def get_person_root_facts_dict(
    x_person: PersonUnit,
) -> dict[RopeTerm, dict[str,]]:
    return x_person.get_planroot_factunits_dict()


def set_factunits_to_person(x_person: PersonUnit, x_facts_dict: dict[RopeTerm, dict]):
    """Sets dict of FactUnits to PersonUnit planroot"""
    factunits_dict = get_factunits_from_dict(x_facts_dict)
    missing_fact_reason_contexts = set(
        x_person.get_missing_fact_reason_contexts().keys()
    )
    not_missing_fact_reason_contexts = set(
        x_person.get_planroot_factunits_dict().keys()
    )
    person_fact_reason_contexts = not_missing_fact_reason_contexts.union(
        missing_fact_reason_contexts
    )
    for factunit in factunits_dict.values():
        if factunit.fact_context in person_fact_reason_contexts:
            x_person.add_fact(
                factunit.fact_context,
                factunit.fact_state,
                factunit.fact_lower,
                factunit.fact_upper,
                create_missing_plans=True,
            )


def clear_factunits_from_person(x_person: PersonUnit):
    """Deletes all PersonUnit planroot FactUnits"""
    for fact_reason_context in get_person_root_facts_dict(x_person).keys():
        x_person.del_fact(fact_reason_context)


def person_plan_reason_caseunit_set_obj(person: PersonUnit, args: dict[str,]):
    """Wrapper for method that edit personunit plan nodes reasonunits.
    plan_rope: required jkeys
    reason_context: required jkeys
    reason_state: required jkeys
    reason_lower: optional jvalues
    reason_upper: optional jvalues
    reason_divisor: optional jvalues
    """
    plan_rope = args.get("plan_rope")
    reason_context = args.get("reason_context")
    reason_state = args.get("reason_state")
    reason_lower = args.get("reason_lower")
    reason_upper = args.get("reason_upper")
    reason_divisor = args.get("reason_divisor")
    person.edit_plan_attr(
        plan_rope=plan_rope,
        reason_context=reason_context,
        reason_case=reason_state,
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
    )


def get_person_unique_short_ropes(person: PersonUnit) -> dict[RopeTerm, RopeTerm]:
    """Return dict of all plan_ropes and the shortest possible term for that Plan that is unique."""
    return get_unique_short_ropes(set(person.get_plan_dict().keys()), person.knot)


def add_frame_to_caseunit(
    x_case: CaseUnit,
    x_frame: int,
    context_plan_denom: int,
    context_plan_morph: bool,
):
    """Given any case append number to caseunit reason_lower and reason_upper

    Step 0: calculate modulus:
        If it exists set to the caseunit's reason_divisor
        Else if it exists set to the context plan's denom
    Step 1: morph x_frame
        If context plan's morph is True then divide frame by context_plan_denom
    Step 2: define CaseUnit attrs
        Change CaseUnit's reason_lower and reason_upper range attrs by adding frame
        to each and use modulus to make result is not negative or more then modulus.


    """
    modulus = x_case.reason_divisor or context_plan_denom
    if not context_plan_morph:
        x_frame //= get_1_if_None(context_plan_denom)
    x_case.reason_lower = modular_addition(x_case.reason_lower, x_frame, modulus)
    x_case.reason_upper = modular_addition(x_case.reason_upper, x_frame, modulus)


def add_frame_to_reasonunit(
    x_reason: ReasonUnit,
    x_int: int,
    context_plan_denom: int,
    context_plan_morph: bool,
):
    for x_case in x_reason.cases.values():
        if x_case.reason_lower and x_case.reason_upper:
            add_frame_to_caseunit(x_case, x_int, context_plan_denom, context_plan_morph)


def add_frame_to_factunit(x_factunit: FactUnit, x_int: int, context_plan_close: int):
    if x_factunit.fact_lower and x_factunit.fact_upper:
        x_lower = modular_addition(x_factunit.fact_lower, x_int, context_plan_close)
        x_upper = modular_addition(x_factunit.fact_upper, x_int, context_plan_close)
        x_factunit.fact_lower = x_lower
        x_factunit.fact_upper = x_upper


def add_frame_to_personunit(
    x_person: PersonUnit, x_int: int, required_context_subrope: RopeTerm = None
):
    required_context_subrope = get_empty_str_if_None(required_context_subrope)
    for x_plan in x_person.get_plan_dict().values():
        for x_reason in x_plan.reasonunits.values():
            if is_sub_rope(x_reason.reason_context, required_context_subrope):
                reason_context_plan = x_person.get_plan_obj(x_reason.reason_context)
                denom = reason_context_plan.denom
                morph = reason_context_plan.morph
                add_frame_to_reasonunit(x_reason, x_int, denom, morph)
        for x_fact in x_plan.factunits.values():
            if is_sub_rope(x_fact.fact_context, required_context_subrope):
                fact_context_plan = x_person.get_plan_obj(x_fact.fact_context)
                add_frame_to_factunit(x_fact, x_int, fact_context_plan.close)
