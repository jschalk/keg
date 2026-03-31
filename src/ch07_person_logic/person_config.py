from os import getcwd as os_getcwd
from src.ch00_py.file_toolbox import create_path, open_json


def max_tree_traverse_default() -> int:
    return 20


def person_config_path() -> str:
    """src/ch07_person_logic/person_config.json"""
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch07_person_logic")
    return create_path(chapter_dir, "person_config.json")


def get_person_config_dict() -> dict[str, dict]:
    return open_json(person_config_path())


def get_person_calc_dimen_args(dimen: str) -> set:
    config_dict = get_person_config_dict()
    dimen_dict = config_dict.get(dimen)
    all_args = set(dimen_dict.get("jkeys").keys())
    all_args = all_args.union(set(dimen_dict.get("jvalues").keys()))
    return all_args


def get_all_person_calc_args() -> dict[str, set[str]]:
    person_config_dict = get_person_config_dict()
    all_args = {}
    for person_calc_dimen, dimen_dict in person_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg in arg_dict.keys():
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(person_calc_dimen)
    return all_args


def get_person_calc_args_type_dict() -> dict[str, str]:
    return {
        "active_requisite": "bool",
        "addin": "float",
        "all_partner_cred": "int",
        "all_partner_debt": "int",
        "awardee_title": "TitleTerm",
        "begin": "float",
        "case_active": "int",
        "case_task": "bool",
        "close": "float",
        "credor_pool": "float",
        "credor_respect": "float",
        "debtor_pool": "float",
        "debtor_respect": "float",
        "denom": "int",
        "descendant_pledge_count": "int",
        "fact_lower": "FactNum",
        "fact_state": "RopeTerm",
        "fact_upper": "FactNum",
        "fund_agenda_give": "float",
        "fund_agenda_ratio_give": "float",
        "fund_agenda_ratio_take": "float",
        "fund_agenda_take": "float",
        "fund_cease": "float",
        "fund_give": "float",
        "fund_grain": "float",
        "fund_onset": "float",
        "fund_pool": "float",
        "fund_ratio": "float",
        "fund_take": "float",
        "give_force": "float",
        "gogo_calc": "float",
        "gogo_want": "float",
        "group_cred_lumen": "int",
        "group_debt_lumen": "int",
        "group_title": "TitleTerm",
        "healer_name": "NameTerm",
        "healerunit_ratio": "float",
        "inallocable_partner_debt_lumen": "float",
        "irrational_partner_debt_lumen": "float",
        "keeps_buildable": "int",
        "keeps_justified": "int",
        "knot": "KnotTerm",
        "mana_grain": "float",
        "max_tree_traverse": "int",
        "morph": "bool",
        "numor": "int",
        "offtrack_fund": "int",
        "parent_heir_active": "int",
        "partner_cred_lumen": "float",
        "partner_debt_lumen": "float",
        "partner_name": "NameTerm",
        "labor_title": "TitleTerm",
        "person_name_is_workforce": "int",
        "plan_active": "bool",
        "plan_rope": "RopeTerm",
        "plan_task": "bool",
        "pledge": "bool",
        "problem_bool": "bool",
        "range_evaluated": "int",
        "rational": "bool",
        "reason_active": "int",
        "reason_context": "RopeTerm",
        "reason_divisor": "int",
        "reason_lower": "ReasonNum",
        "reason_state": "RopeTerm",
        "reason_task": "bool",
        "reason_upper": "ReasonNum",
        "respect_grain": "float",
        "star": "int",
        "stop_calc": "float",
        "stop_want": "float",
        "sum_healerunit_plans_fund_total": "float",
        "take_force": "float",
        "tree_level": "int",
        "tree_traverse_count": "int",
    }


def get_person_calc_args_sqlite_datatype_dict() -> dict[str, str]:
    return {
        "active_requisite": "INTEGER",
        "addin": "REAL",
        "all_partner_cred": "INTEGER",
        "all_partner_debt": "INTEGER",
        "awardee_title": "TEXT",
        "begin": "REAL",
        "case_active": "INTEGER",
        "case_task": "INTEGER",
        "close": "REAL",
        "credor_pool": "REAL",
        "credor_respect": "REAL",
        "debtor_pool": "REAL",
        "debtor_respect": "REAL",
        "denom": "INTEGER",
        "descendant_pledge_count": "INTEGER",
        "fact_context": "TEXT",
        "fact_lower": "REAL",
        "fact_state": "TEXT",
        "fact_upper": "REAL",
        "fund_agenda_give": "REAL",
        "fund_agenda_ratio_give": "REAL",
        "fund_agenda_ratio_take": "REAL",
        "fund_agenda_take": "REAL",
        "fund_cease": "REAL",
        "fund_give": "REAL",
        "fund_grain": "REAL",
        "fund_onset": "REAL",
        "fund_pool": "REAL",
        "fund_ratio": "REAL",
        "fund_take": "REAL",
        "give_force": "REAL",
        "gogo_calc": "REAL",
        "gogo_want": "REAL",
        "group_cred_lumen": "REAL",
        "group_debt_lumen": "REAL",
        "group_title": "TEXT",
        "groupmark": "TEXT",
        "healer_name": "TEXT",
        "healerunit_ratio": "REAL",
        "inallocable_partner_debt_lumen": "REAL",
        "irrational_partner_debt_lumen": "REAL",
        "keeps_buildable": "INTEGER",
        "keeps_justified": "INTEGER",
        "knot": "TEXT",
        "mana_grain": "REAL",
        "max_tree_traverse": "INTEGER",
        "morph": "INTEGER",
        "numor": "INTEGER",
        "offtrack_fund": "REAL",
        "parent_heir_active": "INTEGER",
        "partner_cred_lumen": "REAL",
        "partner_debt_lumen": "REAL",
        "partner_name": "TEXT",
        "labor_title": "TEXT",
        "person_name": "TEXT",
        "person_name_is_workforce": "INTEGER",
        "plan_active": "INTEGER",
        "plan_rope": "TEXT",
        "plan_task": "INTEGER",
        "pledge": "INTEGER",
        "problem_bool": "INTEGER",
        "range_evaluated": "INTEGER",
        "rational": "INTEGER",
        "reason_active": "INTEGER",
        "reason_context": "TEXT",
        "reason_divisor": "INTEGER",
        "reason_lower": "REAL",
        "reason_state": "TEXT",
        "reason_task": "INTEGER",
        "reason_upper": "REAL",
        "respect_grain": "REAL",
        "solo": "INTEGER",
        "star": "INTEGER",
        "stop_calc": "REAL",
        "stop_want": "REAL",
        "sum_healerunit_plans_fund_total": "REAL",
        "take_force": "REAL",
        "tree_level": "INTEGER",
        "tree_traverse_count": "INTEGER",
    }


def get_person_calc_dimens() -> dict[str, str]:
    return {
        "personunit",
        "person_partnerunit",
        "person_partner_membership",
        "person_planunit",
        "person_plan_awardunit",
        "person_plan_reasonunit",
        "person_plan_reason_caseunit",
        "person_plan_laborunit",
        "person_plan_healerunit",
        "person_plan_factunit",
        "person_groupunit",
    }
