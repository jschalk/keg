import dataclasses
from src.ch00_py.dict_toolbox import get_serializable_dict
from src.ch02_partner.group import AwardHeir, AwardLine, AwardUnit
from src.ch03_workforce.workforce import LaborHeir, LaborUnit
from src.ch05_reason.reason_main import (
    CaseUnit,
    FactHeir,
    FactUnit,
    ReasonHeir,
    ReasonUnit,
)
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PersonUnit
from src.ch13_time.epoch_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from typing import Any


def add_small_dot(x_str: str) -> str:
    return f"&nbsp;&nbsp;<small>� {x_str}</small>"


def readable_percent(value: float) -> str:
    # if value is None:
    #     return 0
    pct = value * 100
    if abs(pct) >= 1:  # show as integer percent
        return f"{pct:.0f}%"
    elif abs(pct) >= 0.01:  # show with 2 decimal places
        return f"{pct:.2f}%"
    else:  # very small -> show in scientific-like format
        return f"{pct:.5f}%".rstrip("0").rstrip(".")


def person_objs_asdict(
    obj: Any, current_person: PersonUnit = None, current_reason: ReasonUnit = None
) -> dict:
    # sourcery skip: extract-duplicate-method
    """
    Convert a dataclass-like object to dict,
    including extra keys defined in a custom attribute.
    """
    if dataclasses.is_dataclass(obj):
        if isinstance(obj, PersonUnit):
            current_person = obj
        elif isinstance(obj, (ReasonUnit, ReasonHeir)):
            current_reason = obj
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            result[field.name] = person_objs_asdict(
                value, current_person, current_reason
            )
        if isinstance(obj, PlanUnit):
            set_readable_plan_values(obj, result)
        elif isinstance(obj, AwardUnit):
            obj_readable_str = (
                f"{obj.awardee_title}: Take {obj.take_force}, Give {obj.give_force}"
            )
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, AwardHeir):
            obj_readable_str = f"{obj.awardee_title}: Take {obj.take_force} ({obj.fund_take}), Give {obj.give_force} ({obj.fund_give})"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, AwardLine):
            obj_readable_str = f"{obj.awardee_title}: take_fund ({obj.fund_take}), give_fund ({obj.fund_give})"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, (FactUnit, FactHeir)):
            obj_readable_str = get_fact_state_readable_str(obj, None, current_person)
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, LaborUnit):
            solo_str = " Solo: True" if obj.solo else ""
            obj_readable_str = f"WorkforceUnit: {obj.labor_title}{solo_str}"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, LaborHeir):
            solo_str = " Solo: True" if obj.solo else ""
            obj_readable_str = f"WorkforceHeir: {obj.labor_title}{solo_str}"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, ReasonUnit):
            reason_case_readable_str = f"ReasonUnit: context is {obj.reason_context}"
            result["readable"] = add_small_dot(reason_case_readable_str)
        elif isinstance(obj, ReasonHeir):
            reason_case_readable_str = f"ReasonHeir: context is {obj.reason_context}"
            result["readable"] = add_small_dot(reason_case_readable_str)
        elif isinstance(obj, CaseUnit):
            reason_case_readable_str = get_reason_case_readable_str(
                reason_context=current_reason.reason_context,
                caseunit=obj,
                epoch_label=None,
                personunit=current_person,
            )
            result["readable"] = f"  {add_small_dot(reason_case_readable_str)}"

        return result
    elif isinstance(obj, (list, tuple)):
        b = current_person
        r = current_reason
        return [person_objs_asdict(v, b, r) for v in obj]
    elif isinstance(obj, dict):
        b = current_person
        r = current_reason
        return {k: person_objs_asdict(v, b, r) for k, v in obj.items()}
    else:
        return obj


def set_readable_plan_values(x_plan: PlanUnit, result: dict):
    result["parent_rope"] = (
        add_small_dot(x_plan.parent_rope)
        if result.get("parent_rope") != ""
        else add_small_dot("Root Plan parent_rope is empty str")
    )
    result["plan_fund_total"] = x_plan.get_plan_fund_total()
    all_partner_cred_str = f"all_partner_cred = {x_plan.all_partner_cred}"
    all_partner_debt_str = f"all_partner_debt = {x_plan.all_partner_debt}"
    all_partner_cred_str = add_small_dot(all_partner_cred_str)
    all_partner_debt_str = add_small_dot(all_partner_debt_str)
    result["all_partner_cred"] = all_partner_cred_str
    result["all_partner_debt"] = all_partner_debt_str
    result["fund_ratio"] = readable_percent(result.get("fund_ratio"))
    result_gogo_want = result.get("gogo_want")
    result_stop_want = result.get("stop_want")
    result_gogo_calc = result.get("gogo_calc")
    result_stop_calc = result.get("stop_calc")
    result["gogo_want"] = add_small_dot(f"gogo_want: {result_gogo_want}")
    result["stop_want"] = add_small_dot(f"stop_want: {result_stop_want}")
    result["gogo_calc"] = add_small_dot(f"gogo_calc: {result_gogo_calc}")
    result["stop_calc"] = add_small_dot(f"stop_calc: {result_stop_calc}")
    result_addin = result.get("addin")
    result_begin = result.get("begin")
    result_close = result.get("close")
    result_denom = result.get("denom")
    result_morph = result.get("morph")
    result_numor = result.get("numor")
    result["addin"] = add_small_dot(f"addin: {result_addin}")
    result["begin"] = add_small_dot(f"begin: {result_begin}")
    result["close"] = add_small_dot(f"close: {result_close}")
    result["denom"] = add_small_dot(f"denom: {result_denom}")
    result["morph"] = add_small_dot(f"morph: {result_morph}")
    result["numor"] = add_small_dot(f"numor: {result_numor}")
    result["plan_active_hx"] = add_small_dot(f"plan_active_hx: {x_plan.plan_active_hx}")


def get_plan_view_dict(x_plan: PlanUnit) -> dict[str,]:
    """Returns a dictionary of only base value types and dictionarys"""

    # return get_serializable_dict(dataclasses_asdict(x_plan))
    return get_serializable_dict(person_objs_asdict(x_plan))


def get_partners_view_dict(person: PersonUnit) -> dict[str,]:
    partners_dict = {}
    for partner in person.partners.values():
        partner_cred_lumen_readable = (
            f"partner_cred_lumen: {partner.partner_cred_lumen}"
        )
        partner_debt_lumen_readable = (
            f"partner_debt_lumen: {partner.partner_debt_lumen}"
        )
        memberships_readable = f"memberships: {partner.memberships}"
        credor_pool_readable = f"credor_pool: {partner.credor_pool}"
        debtor_pool_readable = f"debtor_pool: {partner.debtor_pool}"
        irrational_partner_debt_lumen_readable = (
            f"irrational_partner_debt_lumen: {partner.irrational_partner_debt_lumen}"
        )
        inallocable_partner_debt_lumen_readable = (
            f"inallocable_partner_debt_lumen: {partner.inallocable_partner_debt_lumen}"
        )
        fund_give_readable = f"fund_give: {partner.fund_give}"
        fund_take_readable = f"fund_take: {partner.fund_take}"
        fund_agenda_give_readable = f"fund_agenda_give: {partner.fund_agenda_give}"
        fund_agenda_take_readable = f"fund_agenda_take: {partner.fund_agenda_take}"
        fund_agenda_ratio_give_readable = (
            f"fund_agenda_ratio_give: {partner.fund_agenda_ratio_give}"
        )
        fund_agenda_ratio_take_readable = (
            f"fund_agenda_ratio_take: {partner.fund_agenda_ratio_take}"
        )
        x_members_dict = {
            x_membership.group_title: {
                "partner_name": x_membership.partner_name,
                "group_title": x_membership.group_title,
                "group_cred_lumen": x_membership.group_cred_lumen,
                "group_debt_lumen": x_membership.group_debt_lumen,
                "credor_pool": x_membership.credor_pool,
                "debtor_pool": x_membership.debtor_pool,
                "fund_agenda_give": x_membership.fund_agenda_give,
                "fund_agenda_ratio_give": x_membership.fund_agenda_ratio_give,
                "fund_agenda_ratio_take": x_membership.fund_agenda_ratio_take,
                "fund_agenda_take": x_membership.fund_agenda_take,
                "fund_give": x_membership.fund_give,
                "fund_take": x_membership.fund_take,
                "group_title_readable": add_small_dot(
                    f"group_title: {x_membership.group_title}"
                ),
                "group_cred_lumen_readable": add_small_dot(
                    f"group_cred_lumen: {x_membership.group_cred_lumen}"
                ),
                "group_debt_lumen_readable": add_small_dot(
                    f"group_debt_lumen: {x_membership.group_debt_lumen}"
                ),
                "credor_pool_readable": add_small_dot(
                    f"credor_pool: {x_membership.credor_pool}"
                ),
                "debtor_pool_readable": add_small_dot(
                    f"debtor_pool: {x_membership.debtor_pool}"
                ),
                "fund_agenda_give_readable": add_small_dot(
                    f"fund_agenda_give: {x_membership.fund_agenda_give}"
                ),
                "fund_agenda_ratio_give_readable": add_small_dot(
                    f"fund_agenda_ratio_give: {x_membership.fund_agenda_ratio_give}"
                ),
                "fund_agenda_ratio_take_readable": add_small_dot(
                    f"fund_agenda_ratio_take: {x_membership.fund_agenda_ratio_take}"
                ),
                "fund_agenda_take_readable": add_small_dot(
                    f"fund_agenda_take: {x_membership.fund_agenda_take}"
                ),
                "fund_give_readable": add_small_dot(
                    f"fund_give: {x_membership.fund_give}"
                ),
                "fund_take_readable": add_small_dot(
                    f"fund_take: {x_membership.fund_take}"
                ),
            }
            for x_membership in partner.memberships.values()
        }
        partner_dict = {
            "partner_name": partner.partner_name,
            "partner_cred_lumen": partner.partner_cred_lumen,
            "partner_debt_lumen": partner.partner_debt_lumen,
            "memberships": x_members_dict,
            "credor_pool": partner.credor_pool,
            "debtor_pool": partner.debtor_pool,
            "irrational_partner_debt_lumen": partner.irrational_partner_debt_lumen,
            "inallocable_partner_debt_lumen": partner.inallocable_partner_debt_lumen,
            "fund_give": partner.fund_give,
            "fund_take": partner.fund_take,
            "fund_agenda_give": partner.fund_agenda_give,
            "fund_agenda_take": partner.fund_agenda_take,
            "fund_agenda_ratio_give": partner.fund_agenda_ratio_give,
            "fund_agenda_ratio_take": partner.fund_agenda_ratio_take,
            "partner_cred_lumen_readable": partner_cred_lumen_readable,
            "partner_debt_lumen_readable": partner_debt_lumen_readable,
            "memberships_readable": memberships_readable,
            "credor_pool_readable": credor_pool_readable,
            "debtor_pool_readable": debtor_pool_readable,
            "irrational_partner_debt_lumen_readable": irrational_partner_debt_lumen_readable,
            "inallocable_partner_debt_lumen_readable": inallocable_partner_debt_lumen_readable,
            "fund_give_readable": fund_give_readable,
            "fund_take_readable": fund_take_readable,
            "fund_agenda_give_readable": fund_agenda_give_readable,
            "fund_agenda_take_readable": fund_agenda_take_readable,
            "fund_agenda_ratio_give_readable": fund_agenda_ratio_give_readable,
            "fund_agenda_ratio_take_readable": fund_agenda_ratio_take_readable,
        }
        partners_dict[partner.partner_name] = partner_dict

    return partners_dict


def get_groups_view_dict(person: PersonUnit) -> dict[str,]:
    groups_dict = {}
    group_title_readable_key = "group_title_readable"
    for group in person.groupunits.values():
        #     group_cred_lumen_readable_key = f"group_cred_lumen_readable"
        #     group_debt_lumen_readable_key = f"group_debt_lumen_readable"
        #     credor_pool_readable_key = f"credor_pool_readable"
        #     debtor_pool_readable_key = f"debtor_pool_readable"
        #     fund_agenda_give_readable_key = f"fund_agenda_give_readable"
        #     fund_agenda_ratio_give_readable_key = f"fund_agenda_ratio_give_readable"
        #     fund_agenda_ratio_take_readable_key = f"fund_agenda_ratio_take_readable"
        #     fund_agenda_take_readable_key = f"fund_agenda_take_readable"
        #     fund_give_readable_key = f"fund_give_readable"
        #     fund_take_readable_key = f"fund_take_readable"

        #     group_group_title_readable = f"group_title_readable: {group.group_title}"
        #     group_memberships_readable = f"memberships_readable: {group.memberships}"
        #     group_fund_give_readable = f"fund_give_readable: {group.fund_give}"
        #     group_fund_take_readable = f"fund_take_readable: {group.fund_take}"
        #     group_fund_agenda_give_readable = (
        #         f"fund_agenda_give_readable: {group.fund_agenda_give}"
        #     )
        #     group_fund_agenda_take_readable = (
        #         f"fund_agenda_take_readable: {group.fund_agenda_take}"
        #     )
        #     group_credor_pool_readable = f"credor_pool_readable: {group.credor_pool}"
        #     group_debtor_pool_readable = f"debtor_pool_readable: {group.debtor_pool}"

        #     x_members_dict = {
        #         # x_membership.partner_name: {
        #         #     "partner_name": x_membership.partner_name,
        #         #     "group_title": x_membership.group_title,
        #         #     "group_cred_lumen": x_membership.group_cred_lumen,
        #         #     "group_debt_lumen": x_membership.group_debt_lumen,
        #         #     "credor_pool": x_membership.credor_pool,
        #         #     "debtor_pool": x_membership.debtor_pool,
        #         #     "fund_agenda_give": x_membership.fund_agenda_give,
        #         #     "fund_agenda_ratio_give": x_membership.fund_agenda_ratio_give,
        #         #     "fund_agenda_ratio_take": x_membership.fund_agenda_ratio_take,
        #         #     "fund_agenda_take": x_membership.fund_agenda_take,
        #         #     "fund_give": x_membership.fund_give,
        #         #     "fund_take": x_membership.fund_take,
        #         #     "partner_name_readable": add_small_dot(
        #         #         f"partner name: {x_membership.partner_name}"
        #         #     ),
        #         #     "group_cred_lumen_readable": add_small_dot(
        #         #         f"group_cred_lumen: {x_membership.group_cred_lumen}"
        #         #     ),
        #         #     "group_debt_lumen_readable": add_small_dot(
        #         #         f"group_debt_lumen: {x_membership.group_debt_lumen}"
        #         #     ),
        #         #     "credor_pool_readable": add_small_dot(
        #         #         f"credor_pool: {x_membership.credor_pool}"
        #         #     ),
        #         #     "debtor_pool_readable": add_small_dot(
        #         #         f"debtor_pool: {x_membership.debtor_pool}"
        #         #     ),
        #         #     "fund_agenda_give_readable": add_small_dot(
        #         #         f"fund_agenda_give: {x_membership.fund_agenda_give}"
        #         #     ),
        #         #     "fund_agenda_ratio_give_readable": add_small_dot(
        #         #         f"fund_agenda_ratio_give: {x_membership.fund_agenda_ratio_give}"
        #         #     ),
        #         #     "fund_agenda_ratio_take_readable": add_small_dot(
        #         #         f"fund_agenda_ratio_take: {x_membership.fund_agenda_ratio_take}"
        #         #     ),
        #         #     "fund_agenda_take_readable": add_small_dot(
        #         #         f"fund_agenda_take: {x_membership.fund_agenda_take}"
        #         #     ),
        #         #     "fund_give_readable": add_small_dot(
        #         #         f"fund_give: {x_membership.fund_give}"
        #         #     ),
        #         #     "fund_take_readable": add_small_dot(
        #         #         f"fund_take: {x_membership.fund_take}"
        #         #     ),
        #         # }
        #         # for x_membership in group.memberships.values()
        #     }
        group_dict = {
            "group_title": group.group_title,
            #         "partner_name": 1,
            #         "group_title": 1,
            #         "group_cred_lumen": 1,
            #         "group_debt_lumen": 1,
            #         "credor_pool": 1,
            #         "debtor_pool": 1,
            "fund_agenda_give": 1,
            #         "fund_agenda_ratio_give": 1,
            #         "fund_agenda_ratio_take": 1,
            #         "fund_agenda_take": 1,
            #         "fund_give": 1,
            "fund_take": 1,
            #         group_title_readable_key: 1,
            #         group_cred_lumen_readable_key: 1,
            #         group_debt_lumen_readable_key: 1,
            #         credor_pool_readable_key: 1,
            #         debtor_pool_readable_key: 1,
            #         fund_agenda_give_readable_key: 1,
            #         fund_agenda_ratio_give_readable_key: 1,
            #         fund_agenda_ratio_take_readable_key: 1,
            #         fund_agenda_take_readable_key: 1,
            #         fund_give_readable_key: 1,
            #         fund_take_readable_key: 1,
            #         # "memberships": x_members_dict,
        }
        groups_dict[group.group_title] = group_dict

    return groups_dict


def get_person_view_dict(person: PersonUnit) -> dict[str,]:
    return {
        "planroot": get_plan_view_dict(person.planroot),
        "partners": get_partners_view_dict(person),
    }
