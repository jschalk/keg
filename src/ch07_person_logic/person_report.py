from pandas import DataFrame
from src.ch04_rope.rope import RopeTerm
from src.ch07_person_logic.person_main import PersonUnit


def get_person_contactunits_dataframe(x_person: PersonUnit) -> DataFrame:
    if x_person.contacts == {}:
        return DataFrame(
            columns=[
                "contact_name",
                "contact_cred_lumen",
                "contact_debt_lumen",
                "fund_give",
                "fund_take",
                "fund_agenda_give",
                "fund_agenda_take",
                "fund_agenda_ratio_give",
                "fund_agenda_ratio_take",
            ]
        )
    x_contactunits_list = list(x_person.get_contactunits_dict(all_attrs=True).values())
    return DataFrame(x_contactunits_list)


def get_person_agenda_dataframe(
    x_person: PersonUnit, reason_context: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_person.get_agenda_dict(necessary_reason_context=reason_context)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "person_name",
                "fund_ratio",
                "plan_label",
                "parent_rope",
                "begin",
                "close",
                "addin",
                "denom",
                "numor",
                "morph",
            ]
        )
    x_plan_list = []
    for x_plan in agenda_dict.values():
        plan_dict = {
            "person_name": x_person.person_name,
            "fund_ratio": x_plan.fund_ratio,
            "plan_label": x_plan.plan_label,
            "parent_rope": x_plan.parent_rope,
            "begin": x_plan.begin,
            "close": x_plan.close,
            "addin": x_plan.addin,
            "denom": x_plan.denom,
            "numor": x_plan.numor,
            "morph": x_plan.morph,
        }
        x_plan_list.append(plan_dict)
    return DataFrame(x_plan_list)
