from os import getcwd as os_getcwd
from src.ch00_py.db_toolbox import get_sorted_cols_only_list
from src.ch00_py.file_toolbox import create_path, get_json_filename, open_json


def idea_config_path() -> str:
    "Returns path: ch17_idea_logic/idea_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch17_idea")
    return create_path(chapter_dir, "idea_config.json")


def get_idea_config_dict(idea_categorys: set[str] = None) -> dict:
    """If idea_categorys is None/empty return entire idea_config_dict, otherwise filter on idea_category"""
    idea_config_dict = open_json(idea_config_path())
    if idea_categorys:
        return {
            x_dimen: dimen_config
            for x_dimen, dimen_config in idea_config_dict.items()
            if dimen_config.get("idea_category") in idea_categorys
        }
    else:
        return idea_config_dict


def get_allowed_curds() -> set[str]:
    return {
        "insert_one_time",
        "insert_multiple",
        "delete_insert_update",
        "insert_update",
        "delete_insert",
        "delete_update",
        "UPDATE",
        "DELETE",
        "INSERT",
    }


def get_idea_formats_dir() -> str:
    idea_dir = create_path("src", "ch17_idea")
    return create_path(idea_dir, "idea_formats")


def get_idea_elements_sort_order() -> list[str]:
    """Contains the standard sort order for all idea and person_calc columns"""
    return [
        "world_name",
        "idea_number",
        "source_dimen",
        "translate_spark_num",
        "spark_num",
        "face_name",
        "face_name_otx",
        "face_name_inx",
        "moment_rope",
        "moment_rope_otx",
        "moment_rope_inx",
        "epoch_label",
        "epoch_label_otx",
        "epoch_label_inx",
        "offi_time",
        "offi_time_otx",
        "offi_time_inx",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_index",
        "cumulative_day",
        "month_label",
        "month_label_otx",
        "month_label_inx",
        "cumulative_minute",
        "hour_label",
        "hour_label_otx",
        "hour_label_inx",
        "weekday_order",
        "weekday_label",
        "weekday_label_otx",
        "weekday_label_inx",
        "person_name",
        "person_name_otx",
        "person_name_inx",
        "person_name_ERASE",
        "person_name_ERASE_otx",
        "person_name_ERASE_inx",
        "partner_name",
        "partner_name_otx",
        "partner_name_inx",
        "partner_name_ERASE",
        "partner_name_ERASE_otx",
        "partner_name_ERASE_inx",
        "group_title",
        "group_title_otx",
        "group_title_inx",
        "group_title_ERASE",
        "group_title_ERASE_otx",
        "group_title_ERASE_inx",
        "plan_rope",
        "plan_rope_otx",
        "plan_rope_inx",
        "plan_rope_ERASE",
        "plan_rope_ERASE_otx",
        "plan_rope_ERASE_inx",
        "reason_context",
        "reason_context_otx",
        "reason_context_inx",
        "reason_context_ERASE",
        "reason_context_ERASE_otx",
        "reason_context_ERASE_inx",
        "fact_context",
        "fact_context_otx",
        "fact_context_inx",
        "fact_context_ERASE",
        "fact_context_ERASE_otx",
        "fact_context_ERASE_inx",
        "reason_state",
        "reason_state_otx",
        "reason_state_inx",
        "reason_state_ERASE",
        "reason_state_ERASE_otx",
        "reason_state_ERASE_inx",
        "fact_state",
        "fact_state_otx",
        "fact_state_inx",
        "party_title",
        "party_title_otx",
        "party_title_inx",
        "party_title_ERASE",
        "party_title_ERASE_otx",
        "party_title_ERASE_inx",
        "solo",
        "awardee_title",
        "awardee_title_otx",
        "awardee_title_inx",
        "awardee_title_ERASE",
        "awardee_title_ERASE_otx",
        "awardee_title_ERASE_inx",
        "healer_name",
        "healer_name_otx",
        "healer_name_inx",
        "healer_name_ERASE",
        "healer_name_ERASE_otx",
        "healer_name_ERASE_inx",
        "bud_time",
        "bud_time_otx",
        "bud_time_inx",
        "tran_time",
        "tran_time_otx",
        "tran_time_inx",
        "begin",
        "close",
        "addin",
        "numor",
        "denom",
        "morph",
        "gogo_want",
        "stop_want",
        "active_requisite",
        "partner_cred_lumen",
        "partner_debt_lumen",
        "group_cred_lumen",
        "group_debt_lumen",
        "credor_respect",
        "debtor_respect",
        "fact_lower",
        "fact_lower_otx",
        "fact_lower_inx",
        "fact_upper",
        "fact_upper_otx",
        "fact_upper_inx",
        "fund_pool",
        "give_force",
        "star",
        "max_tree_traverse",
        "reason_lower",
        "reason_lower_otx",
        "reason_lower_inx",
        "reason_upper",
        "reason_upper_otx",
        "reason_upper_inx",
        "reason_divisor",
        "pledge",
        "problem_bool",
        "take_force",
        "fund_grain",
        "mana_grain",
        "respect_grain",
        "amount",
        "otx_label",
        "inx_label",
        "otx_rope",
        "inx_rope",
        "otx_name",
        "inx_name",
        "otx_title",
        "inx_title",
        "otx_knot",
        "inx_knot",
        "otx_time",
        "inx_time",
        "knot",
        "groupmark",
        "unknown_str",
        "quota",
        "celldepth",
        "job_listen_rotations",
        "error_message",
        "person_name_is_labor",
        "plan_active",
        "plan_task",
        "case_task",
        "reason_active",
        "reason_task",
        "case_active",
        "credor_pool",
        "debtor_pool",
        "rational",
        "fund_give",
        "fund_take",
        "fund_onset",
        "fund_cease",
        "fund_ratio",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
        "inallocable_partner_debt_lumen",
        "gogo_calc",
        "stop_calc",
        "tree_level",
        "range_evaluated",
        "descendant_pledge_count",
        "healerunit_ratio",
        "all_partner_cred",
        "keeps_justified",
        "offtrack_fund",
        "parent_heir_active",
        "irrational_partner_debt_lumen",
        "sum_healerunit_plans_fund_total",
        "keeps_buildable",
        "all_partner_debt",
        "tree_traverse_count",
        "net_funds",
        "fund_rank",
        "pledges_count",
        "context_plan_close",
        "context_plan_denom",
        "context_plan_morph",
        "inx_epoch_diff",
    ]


def get_default_sorted_list(
    existing_columns: set[str], sorting_columns: list[str] = None
) -> list[str]:
    if sorting_columns is None:
        sorting_columns = get_idea_elements_sort_order()
    return get_sorted_cols_only_list(existing_columns, sorting_columns)


def get_idea_sqlite_types() -> dict[str, str]:
    """Returns dictionary of sqlite_type for all idea elements (reference source: get_idea_elements_sort_order)"""

    return {
        "world_name": "TEXT",
        "idea_number": "TEXT",
        "face_name": "TEXT",
        "face_name_otx": "TEXT",
        "face_name_inx": "TEXT",
        "source_dimen": "TEXT",
        "translate_spark_num": "INTEGER",
        "spark_num": "INTEGER",
        "moment_rope": "TEXT",
        "moment_rope_otx": "TEXT",
        "moment_rope_inx": "TEXT",
        "person_name": "TEXT",
        "person_name_otx": "TEXT",
        "person_name_inx": "TEXT",
        "person_name_ERASE": "TEXT",
        "person_name_ERASE_otx": "TEXT",
        "person_name_ERASE_inx": "TEXT",
        "partner_name": "TEXT",
        "partner_name_otx": "TEXT",
        "partner_name_inx": "TEXT",
        "partner_name_ERASE": "TEXT",
        "partner_name_ERASE_otx": "TEXT",
        "partner_name_ERASE_inx": "TEXT",
        "group_title": "TEXT",
        "group_title_otx": "TEXT",
        "group_title_inx": "TEXT",
        "group_title_ERASE": "TEXT",
        "group_title_ERASE_otx": "TEXT",
        "group_title_ERASE_inx": "TEXT",
        "plan_rope": "TEXT",
        "plan_rope_otx": "TEXT",
        "plan_rope_inx": "TEXT",
        "plan_rope_ERASE": "TEXT",
        "plan_rope_ERASE_otx": "TEXT",
        "plan_rope_ERASE_inx": "TEXT",
        "reason_context": "TEXT",
        "reason_context_otx": "TEXT",
        "reason_context_inx": "TEXT",
        "reason_context_ERASE": "TEXT",
        "reason_context_ERASE_otx": "TEXT",
        "reason_context_ERASE_inx": "TEXT",
        "fact_context": "TEXT",
        "fact_context_otx": "TEXT",
        "fact_context_inx": "TEXT",
        "fact_context_ERASE": "TEXT",
        "fact_context_ERASE_otx": "TEXT",
        "fact_context_ERASE_inx": "TEXT",
        "reason_state": "TEXT",
        "reason_state_otx": "TEXT",
        "reason_state_inx": "TEXT",
        "reason_state_ERASE": "TEXT",
        "reason_state_ERASE_otx": "TEXT",
        "reason_state_ERASE_inx": "TEXT",
        "fact_state": "TEXT",
        "fact_state_otx": "TEXT",
        "fact_state_inx": "TEXT",
        "party_title": "TEXT",
        "party_title_otx": "TEXT",
        "party_title_inx": "TEXT",
        "party_title_ERASE": "TEXT",
        "party_title_ERASE_otx": "TEXT",
        "party_title_ERASE_inx": "TEXT",
        "solo": "INTEGER",
        "awardee_title": "TEXT",
        "awardee_title_otx": "TEXT",
        "awardee_title_inx": "TEXT",
        "awardee_title_ERASE": "TEXT",
        "awardee_title_ERASE_otx": "TEXT",
        "awardee_title_ERASE_inx": "TEXT",
        "healer_name": "TEXT",
        "healer_name_otx": "TEXT",
        "healer_name_inx": "TEXT",
        "healer_name_ERASE": "TEXT",
        "healer_name_ERASE_otx": "TEXT",
        "healer_name_ERASE_inx": "TEXT",
        "bud_time": "INTEGER",
        "bud_time_otx": "INTEGER",
        "bud_time_inx": "INTEGER",
        "tran_time": "INTEGER",
        "tran_time_otx": "INTEGER",
        "tran_time_inx": "INTEGER",
        "offi_time": "INTEGER",
        "offi_time_otx": "INTEGER",
        "offi_time_inx": "INTEGER",
        "begin": "REAL",
        "close": "REAL",
        "addin": "REAL",
        "numor": "INTEGER",
        "denom": "INTEGER",
        "morph": "INTEGER",
        "gogo_want": "REAL",
        "stop_want": "REAL",
        "active_requisite": "INTEGER",
        "partner_cred_lumen": "REAL",
        "partner_debt_lumen": "REAL",
        "group_cred_lumen": "REAL",
        "group_debt_lumen": "REAL",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fact_lower": "REAL",
        "fact_lower_otx": "REAL",
        "fact_lower_inx": "REAL",
        "fact_upper": "REAL",
        "fact_upper_otx": "REAL",
        "fact_upper_inx": "REAL",
        "fund_pool": "REAL",
        "give_force": "REAL",
        "star": "INTEGER",
        "max_tree_traverse": "INTEGER",
        "reason_upper": "REAL",
        "reason_upper_otx": "REAL",
        "reason_upper_inx": "REAL",
        "reason_lower": "REAL",
        "reason_lower_otx": "REAL",
        "reason_lower_inx": "REAL",
        "reason_divisor": "INTEGER",
        "pledge": "INTEGER",
        "problem_bool": "INTEGER",
        "take_force": "REAL",
        "mana_grain": "REAL",
        "respect_grain": "REAL",
        "amount": "REAL",
        "month_label": "TEXT",
        "month_label_otx": "TEXT",
        "month_label_inx": "TEXT",
        "hour_label": "TEXT",
        "hour_label_otx": "TEXT",
        "hour_label_inx": "TEXT",
        "cumulative_minute": "INTEGER",
        "cumulative_day": "INTEGER",
        "weekday_label": "TEXT",
        "weekday_label_otx": "TEXT",
        "weekday_label_inx": "TEXT",
        "weekday_order": "INTEGER",
        "otx_knot": "TEXT",
        "inx_knot": "TEXT",
        "unknown_str": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "otx_rope": "TEXT",
        "inx_rope": "TEXT",
        "otx_name": "TEXT",
        "inx_name": "TEXT",
        "otx_title": "TEXT",
        "inx_title": "TEXT",
        "otx_time": "INTEGER",
        "inx_time": "INTEGER",
        "knot": "TEXT",
        "groupmark": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "celldepth": "INTEGER",
        "monthday_index": "INTEGER",
        "job_listen_rotations": "INTEGER",
        "epoch_label": "TEXT",
        "epoch_label_otx": "TEXT",
        "epoch_label_inx": "TEXT",
        "error_message": "TEXT",
        "credor_pool": "REAL",
        "debtor_pool": "REAL",
        "fund_cease": "REAL",
        "fund_onset": "REAL",
        "fund_ratio": "REAL",
        "fund_grain": "REAL",
        "fund_agenda_give": "REAL",
        "fund_agenda_ratio_give": "REAL",
        "fund_agenda_ratio_take": "REAL",
        "fund_agenda_take": "REAL",
        "fund_give": "REAL",
        "fund_take": "REAL",
        "gogo_calc": "REAL",
        "stop_calc": "REAL",
        "all_partner_cred": "INTEGER",
        "all_partner_debt": "INTEGER",
        "parent_heir_active": "INTEGER",
        "inallocable_partner_debt_lumen": "REAL",
        "irrational_partner_debt_lumen": "REAL",
        "reason_active": "INTEGER",
        "case_task": "INTEGER",
        "case_active": "INTEGER",
        "person_name_is_labor": "INTEGER",
        "plan_active": "INTEGER",
        "plan_task": "INTEGER",
        "case_task": "INTEGER",
        "reason_task": "INTEGER",
        "descendant_pledge_count": "INTEGER",
        "healerunit_ratio": "REAL",
        "tree_level": "INTEGER",
        "range_evaluated": "INTEGER",
        "keeps_buildable": "INTEGER",
        "keeps_justified": "INTEGER",
        "offtrack_fund": "REAL",
        "rational": "INTEGER",
        "sum_healerunit_plans_fund_total": "REAL",
        "tree_traverse_count": "INTEGER",
        "net_funds": "REAL",
        "fund_rank": "INTEGER",
        "pledges_count": "INTEGER",
        "context_plan_close": "REAL",
        "context_plan_denom": "REAL",
        "context_plan_morph": "REAL",
        "inx_epoch_diff": "INTEGER",
    }


# def idea_format_00000_momentunit_v0_0_0()->str: return "idea_format_00000_momentunit_v0_0_0"
# def idea_format_00001_moment_budunit_v0_0_0()->str: return "idea_format_00001_moment_budunit_v0_0_0"
# def idea_format_00002_moment_paybook_v0_0_0()->str: return "idea_format_00002_moment_paybook_v0_0_0"
# def idea_format_00003_moment_epoch_hour_v0_0_0()->str: return "idea_format_00003_moment_epoch_hour_v0_0_0"
# def idea_format_00004_moment_epoch_month_v0_0_0()->str: return "idea_format_00004_moment_epoch_month_v0_0_0"
# def idea_format_00005_moment_epoch_weekday_v0_0_0()->str: return "idea_format_00005_moment_epoch_weekday_v0_0_0"


def idea_format_00000_momentunit_v0_0_0() -> str:
    return "idea_format_00000_momentunit_v0_0_0"


def idea_format_00001_moment_budunit_v0_0_0() -> str:
    return "idea_format_00001_moment_budunit_v0_0_0"


def idea_format_00002_moment_paybook_v0_0_0() -> str:
    return "idea_format_00002_moment_paybook_v0_0_0"


def idea_format_00003_moment_epoch_hour_v0_0_0() -> str:
    return "idea_format_00003_moment_epoch_hour_v0_0_0"


def idea_format_00004_moment_epoch_month_v0_0_0() -> str:
    return "idea_format_00004_moment_epoch_month_v0_0_0"


def idea_format_00005_moment_epoch_weekday_v0_0_0() -> str:
    return "idea_format_00005_moment_epoch_weekday_v0_0_0"


def idea_format_00006_moment_timeoffi_v0_0_0() -> str:
    return "idea_format_00006_moment_timeoffi_v0_0_0"


def idea_format_00011_partner_v0_0_0() -> str:
    return "idea_format_00011_partner_v0_0_0"


def idea_format_00012_membership_v0_0_0() -> str:
    return "idea_format_00012_membership_v0_0_0"


def idea_format_00013_planunit_v0_0_0() -> str:
    return "idea_format_00013_planunit_v0_0_0"


def idea_format_00019_planunit_v0_0_0() -> str:
    return "idea_format_00019_planunit_v0_0_0"


# def idea_format_00020_person_partner_membership_v0_0_0()-> str: return "idea_format_00020_person_partner_membership_v0_0_0"
# def idea_format_00021_person_partnerunit_v0_0_0()-> str: return "idea_format_00021_person_partnerunit_v0_0_0"
# def idea_format_00022_person_plan_awardunit_v0_0_0()-> str: return "idea_format_00022_person_plan_awardunit_v0_0_0"
# def idea_format_00023_person_plan_factunit_v0_0_0()-> str: return "idea_format_00023_person_plan_factunit_v0_0_0"
# def idea_format_00024_person_plan_partyunit_v0_0_0()-> str: return "idea_format_00024_person_plan_partyunit_v0_0_0"
# def idea_format_00025_person_plan_healerunit_v0_0_0()-> str: return "idea_format_00025_person_plan_healerunit_v0_0_0"
# def idea_format_00026_person_plan_reason_caseunit_v0_0_0()-> str: return "idea_format_00026_person_plan_reason_caseunit_v0_0_0"
# def idea_format_00027_person_plan_reasonunit_v0_0_0()-> str: return "idea_format_00027_person_plan_reasonunit_v0_0_0"
# def idea_format_00028_person_planunit_v0_0_0()-> str: return "idea_format_00028_person_planunit_v0_0_0"
# def idea_format_00029_personunit_v0_0_0()-> str: return "idea_format_00029_personunit_v0_0_0"


def idea_format_00020_person_partner_membership_v0_0_0() -> str:
    return "idea_format_00020_person_partner_membership_v0_0_0"


def idea_format_00021_person_partnerunit_v0_0_0() -> str:
    return "idea_format_00021_person_partnerunit_v0_0_0"


def idea_format_00022_person_plan_awardunit_v0_0_0() -> str:
    return "idea_format_00022_person_plan_awardunit_v0_0_0"


def idea_format_00023_person_plan_factunit_v0_0_0() -> str:
    return "idea_format_00023_person_plan_factunit_v0_0_0"


def idea_format_00024_person_plan_partyunit_v0_0_0() -> str:
    return "idea_format_00024_person_plan_partyunit_v0_0_0"


def idea_format_00025_person_plan_healerunit_v0_0_0() -> str:
    return "idea_format_00025_person_plan_healerunit_v0_0_0"


def idea_format_00026_person_plan_reason_caseunit_v0_0_0() -> str:
    return "idea_format_00026_person_plan_reason_caseunit_v0_0_0"


def idea_format_00027_person_plan_reasonunit_v0_0_0() -> str:
    return "idea_format_00027_person_plan_reasonunit_v0_0_0"


def idea_format_00028_person_planunit_v0_0_0() -> str:
    return "idea_format_00028_person_planunit_v0_0_0"


def idea_format_00029_personunit_v0_0_0() -> str:
    return "idea_format_00029_personunit_v0_0_0"


def idea_format_00036_problem_healer_v0_0_0() -> str:
    return "idea_format_00036_problem_healer_v0_0_0"


def idea_format_00040_map_otx2inx_v0_0_0() -> str:
    return "idea_format_00040_map_otx2inx_v0_0_0"


def idea_format_00042_translate_title_v0_0_0() -> str:
    return "idea_format_00042_translate_title_v0_0_0"


def idea_format_00043_translate_name_v0_0_0() -> str:
    return "idea_format_00043_translate_name_v0_0_0"


def idea_format_00044_translate_label_v0_0_0() -> str:
    return "idea_format_00044_translate_label_v0_0_0"


def idea_format_00045_translate_rope_v0_0_0() -> str:
    return "idea_format_00045_translate_rope_v0_0_0"


def idea_format_00050_delete_person_partner_membership_v0_0_0() -> str:
    return "idea_format_00050_delete_person_partner_membership_v0_0_0"


def idea_format_00051_delete_person_partnerunit_v0_0_0() -> str:
    return "idea_format_00051_delete_person_partnerunit_v0_0_0"


def idea_format_00052_delete_person_plan_awardunit_v0_0_0() -> str:
    return "idea_format_00052_delete_person_plan_awardunit_v0_0_0"


def idea_format_00053_delete_person_plan_factunit_v0_0_0() -> str:
    return "idea_format_00053_delete_person_plan_factunit_v0_0_0"


def idea_format_00054_delete_person_plan_partyunit_v0_0_0() -> str:
    return "idea_format_00054_delete_person_plan_partyunit_v0_0_0"


def idea_format_00055_delete_person_plan_healerunit_v0_0_0() -> str:
    return "idea_format_00055_delete_person_plan_healerunit_v0_0_0"


def idea_format_00056_delete_person_plan_reason_caseunit_v0_0_0() -> str:
    return "idea_format_00056_delete_person_plan_reason_caseunit_v0_0_0"


def idea_format_00057_delete_person_plan_reasonunit_v0_0_0() -> str:
    return "idea_format_00057_delete_person_plan_reasonunit_v0_0_0"


def idea_format_00058_delete_person_planunit_v0_0_0() -> str:
    return "idea_format_00058_delete_person_planunit_v0_0_0"


def idea_format_00059_delete_personunit_v0_0_0() -> str:
    return "idea_format_00059_delete_personunit_v0_0_0"


def idea_format_00070_nabu_epochtime_v0_0_0() -> str:
    return "idea_format_00070_nabu_epochtime_v0_0_0"


def idea_format_00113_partner_map1_v0_0_0() -> str:
    return "idea_format_00113_partner_map1_v0_0_0"


def idea_format_00115_group_map1_v0_0_0() -> str:
    return "idea_format_00115_group_map1_v0_0_0"


def idea_format_00116_label_map1_v0_0_0() -> str:
    return "idea_format_00116_label_map1_v0_0_0"


def idea_format_00117_rope_map1_v0_0_0() -> str:
    return "idea_format_00117_rope_map1_v0_0_0"


def get_idea_format_filenames() -> set[str]:
    return {
        idea_format_00000_momentunit_v0_0_0(),
        idea_format_00001_moment_budunit_v0_0_0(),
        idea_format_00002_moment_paybook_v0_0_0(),
        idea_format_00003_moment_epoch_hour_v0_0_0(),
        idea_format_00004_moment_epoch_month_v0_0_0(),
        idea_format_00005_moment_epoch_weekday_v0_0_0(),
        idea_format_00006_moment_timeoffi_v0_0_0(),
        idea_format_00011_partner_v0_0_0(),
        idea_format_00012_membership_v0_0_0(),
        idea_format_00013_planunit_v0_0_0(),
        idea_format_00019_planunit_v0_0_0(),
        idea_format_00020_person_partner_membership_v0_0_0(),
        idea_format_00021_person_partnerunit_v0_0_0(),
        idea_format_00022_person_plan_awardunit_v0_0_0(),
        idea_format_00023_person_plan_factunit_v0_0_0(),
        idea_format_00024_person_plan_partyunit_v0_0_0(),
        idea_format_00025_person_plan_healerunit_v0_0_0(),
        idea_format_00026_person_plan_reason_caseunit_v0_0_0(),
        idea_format_00027_person_plan_reasonunit_v0_0_0(),
        idea_format_00028_person_planunit_v0_0_0(),
        idea_format_00029_personunit_v0_0_0(),
        idea_format_00036_problem_healer_v0_0_0(),
        idea_format_00042_translate_title_v0_0_0(),
        idea_format_00043_translate_name_v0_0_0(),
        idea_format_00044_translate_label_v0_0_0(),
        idea_format_00045_translate_rope_v0_0_0(),
        idea_format_00050_delete_person_partner_membership_v0_0_0(),
        idea_format_00051_delete_person_partnerunit_v0_0_0(),
        idea_format_00052_delete_person_plan_awardunit_v0_0_0(),
        idea_format_00053_delete_person_plan_factunit_v0_0_0(),
        idea_format_00054_delete_person_plan_partyunit_v0_0_0(),
        idea_format_00055_delete_person_plan_healerunit_v0_0_0(),
        idea_format_00056_delete_person_plan_reason_caseunit_v0_0_0(),
        idea_format_00057_delete_person_plan_reasonunit_v0_0_0(),
        idea_format_00058_delete_person_planunit_v0_0_0(),
        idea_format_00059_delete_personunit_v0_0_0(),
        idea_format_00070_nabu_epochtime_v0_0_0(),
        idea_format_00113_partner_map1_v0_0_0(),
        idea_format_00115_group_map1_v0_0_0(),
        idea_format_00116_label_map1_v0_0_0(),
        idea_format_00117_rope_map1_v0_0_0(),
    }


def get_idea_numbers() -> set[str]:
    return {
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        "br00006",
        "br00011",
        "br00012",
        "br00013",
        "br00019",
        "br00020",
        "br00021",
        "br00022",
        "br00023",
        "br00024",
        "br00025",
        "br00026",
        "br00027",
        "br00028",
        "br00029",
        "br00036",
        "br00042",
        "br00043",
        "br00044",
        "br00045",
        "br00050",
        "br00051",
        "br00052",
        "br00053",
        "br00054",
        "br00055",
        "br00056",
        "br00057",
        "br00058",
        "br00059",
        "br00070",
        "br00113",
        "br00115",
        "br00116",
        "br00117",
    }


def get_idea_format_filename(idea_number: str) -> str:
    idea_number_substring = idea_number[2:]
    for idea_format_filename in get_idea_format_filenames():
        if idea_format_filename[12:17] == idea_number_substring:
            return idea_format_filename


def get_idea_format_headers() -> dict[str, list[str]]:
    return {
        "moment_rope,epoch_label,c400_number,yr1_jan1_offset,monthday_index,fund_grain,mana_grain,respect_grain,knot,job_listen_rotations": idea_format_00000_momentunit_v0_0_0(),
        "moment_rope,person_name,bud_time,knot,quota,celldepth": idea_format_00001_moment_budunit_v0_0_0(),
        "moment_rope,person_name,partner_name,tran_time,amount,knot": idea_format_00002_moment_paybook_v0_0_0(),
        "moment_rope,cumulative_minute,hour_label,knot": idea_format_00003_moment_epoch_hour_v0_0_0(),
        "moment_rope,cumulative_day,month_label,knot": idea_format_00004_moment_epoch_month_v0_0_0(),
        "moment_rope,weekday_order,weekday_label,knot": idea_format_00005_moment_epoch_weekday_v0_0_0(),
        "moment_rope,offi_time,knot": idea_format_00006_moment_timeoffi_v0_0_0(),
        "moment_rope,person_name,partner_name": idea_format_00011_partner_v0_0_0(),
        "moment_rope,person_name,partner_name,group_title": idea_format_00012_membership_v0_0_0(),
        "moment_rope,person_name,plan_rope,star,pledge": idea_format_00013_planunit_v0_0_0(),
        "moment_rope,person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want": idea_format_00019_planunit_v0_0_0(),
        "moment_rope,person_name,partner_name,group_title,group_cred_lumen,group_debt_lumen,knot": idea_format_00020_person_partner_membership_v0_0_0(),
        "moment_rope,person_name,partner_name,partner_cred_lumen,partner_debt_lumen,knot": idea_format_00021_person_partnerunit_v0_0_0(),
        "person_name,plan_rope,awardee_title,give_force,take_force,knot": idea_format_00022_person_plan_awardunit_v0_0_0(),
        "person_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper,knot": idea_format_00023_person_plan_factunit_v0_0_0(),
        "person_name,plan_rope,party_title,solo,knot": idea_format_00024_person_plan_partyunit_v0_0_0(),
        "person_name,plan_rope,healer_name,knot": idea_format_00025_person_plan_healerunit_v0_0_0(),
        "person_name,plan_rope,reason_context,reason_state,reason_lower,reason_upper,reason_divisor,knot": idea_format_00026_person_plan_reason_caseunit_v0_0_0(),
        "person_name,plan_rope,reason_context,active_requisite,knot": idea_format_00027_person_plan_reasonunit_v0_0_0(),
        "person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool,knot": idea_format_00028_person_planunit_v0_0_0(),
        "moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain,knot": idea_format_00029_personunit_v0_0_0(),
        "moment_rope,person_name,plan_rope,healer_name,problem_bool": idea_format_00036_problem_healer_v0_0_0(),
        "otx_title,inx_title,otx_knot,inx_knot,unknown_str": idea_format_00042_translate_title_v0_0_0(),
        "otx_name,inx_name,otx_knot,inx_knot,unknown_str": idea_format_00043_translate_name_v0_0_0(),
        "otx_label,inx_label,otx_knot,inx_knot,unknown_str": idea_format_00044_translate_label_v0_0_0(),
        "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str": idea_format_00045_translate_rope_v0_0_0(),
        "moment_rope,person_name,partner_name,group_title_ERASE": idea_format_00050_delete_person_partner_membership_v0_0_0(),
        "moment_rope,person_name,partner_name_ERASE": idea_format_00051_delete_person_partnerunit_v0_0_0(),
        "person_name,plan_rope,awardee_title_ERASE": idea_format_00052_delete_person_plan_awardunit_v0_0_0(),
        "person_name,plan_rope,fact_context_ERASE": idea_format_00053_delete_person_plan_factunit_v0_0_0(),
        "person_name,plan_rope,party_title_ERASE": idea_format_00054_delete_person_plan_partyunit_v0_0_0(),
        "person_name,plan_rope,healer_name_ERASE": idea_format_00055_delete_person_plan_healerunit_v0_0_0(),
        "person_name,plan_rope,reason_context,reason_state_ERASE": idea_format_00056_delete_person_plan_reason_caseunit_v0_0_0(),
        "person_name,plan_rope,reason_context_ERASE": idea_format_00057_delete_person_plan_reasonunit_v0_0_0(),
        "person_name,plan_rope_ERASE": idea_format_00058_delete_person_planunit_v0_0_0(),
        "moment_rope,person_name_ERASE": idea_format_00059_delete_personunit_v0_0_0(),
        "moment_rope,otx_time,inx_time": idea_format_00070_nabu_epochtime_v0_0_0(),
        "moment_rope,person_name,partner_name,otx_name,inx_name": idea_format_00113_partner_map1_v0_0_0(),
        "moment_rope,person_name,partner_name,otx_title,inx_title": idea_format_00115_group_map1_v0_0_0(),
        "moment_rope,person_name,partner_name,otx_label,inx_label": idea_format_00116_label_map1_v0_0_0(),
        "moment_rope,person_name,partner_name,otx_rope,inx_rope": idea_format_00117_rope_map1_v0_0_0(),
    }


def get_idearef_from_file(idea_format_filename: str) -> dict:
    idearef_filename = get_json_filename(idea_format_filename)
    return open_json(get_idea_formats_dir(), idearef_filename)


def get_quick_ideas_column_ref() -> dict[str, set[str]]:
    idea_number_dict = {}
    for idea_format_filename in get_idea_format_filenames():
        idearef_dict = get_idearef_from_file(idea_format_filename)
        idea_number = idearef_dict.get("idea_number")
        idea_number_dict[idea_number] = set(idearef_dict.get("attributes").keys())
    return idea_number_dict


def get_idea_dimen_ref() -> dict[str, set[str]]:
    """dictionary with key=dimen and value=set of all idea_numbers with that dimen's data"""
    return {
        "moment_budunit": {"br00001"},
        "moment_epoch_hour": {"br00003"},
        "moment_epoch_month": {"br00004"},
        "moment_epoch_weekday": {"br00005"},
        "moment_paybook": {"br00002"},
        "moment_timeoffi": {"br00006"},
        "momentunit": {
            "br00000",
            "br00001",
            "br00002",
            "br00003",
            "br00004",
            "br00005",
            "br00006",
            "br00011",
            "br00012",
            "br00013",
            "br00019",
            "br00020",
            "br00021",
            "br00029",
            "br00036",
            "br00050",
            "br00051",
            "br00059",
            "br00070",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        },
        "nabu_timenum": {"br00070"},
        "person_partner_membership": {"br00012", "br00020", "br00050"},
        "person_partnerunit": {
            "br00002",
            "br00011",
            "br00012",
            "br00020",
            "br00021",
            "br00050",
            "br00051",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        },
        "person_plan_awardunit": {"br00022", "br00052"},
        "person_plan_factunit": {"br00023", "br00053"},
        "person_plan_healerunit": {"br00025", "br00036", "br00055"},
        "person_plan_partyunit": {"br00024", "br00054"},
        "person_plan_reason_caseunit": {"br00026", "br00056"},
        "person_plan_reasonunit": {"br00026", "br00027", "br00056", "br00057"},
        "person_planunit": {
            "br00013",
            "br00019",
            "br00022",
            "br00023",
            "br00024",
            "br00025",
            "br00026",
            "br00027",
            "br00028",
            "br00036",
            "br00052",
            "br00053",
            "br00054",
            "br00055",
            "br00056",
            "br00057",
            "br00058",
        },
        "personunit": {
            "br00001",
            "br00002",
            "br00011",
            "br00012",
            "br00013",
            "br00019",
            "br00020",
            "br00021",
            "br00029",
            "br00036",
            "br00050",
            "br00051",
            "br00059",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        },
        "translate_label": {"br00044", "br00116"},
        "translate_name": {"br00043", "br00113"},
        "translate_rope": {"br00045", "br00117"},
        "translate_title": {"br00042", "br00115"},
    }


def get_dimens_with_idea_element(x_arg: str) -> set[str]:
    x_set = set()
    for x_dimen, dimen_dict in get_idea_config_dict().items():
        dimen_args = set(dimen_dict.get("jkeys"))
        dimen_args.update(dimen_dict.get("jvalues"))
        if x_arg in dimen_args:
            x_set.add(x_dimen)
    return x_set


def get_dimen_minimum_put_idea_names() -> dict[str, str]:
    """Returns all dimens and the idea format with only the args for that dimen."""

    return {
        "moment_budunit": idea_format_00001_moment_budunit_v0_0_0(),
        "moment_epoch_hour": idea_format_00003_moment_epoch_hour_v0_0_0(),
        "moment_epoch_month": idea_format_00004_moment_epoch_month_v0_0_0(),
        "moment_epoch_weekday": idea_format_00005_moment_epoch_weekday_v0_0_0(),
        "moment_paybook": idea_format_00002_moment_paybook_v0_0_0(),
        "moment_timeoffi": idea_format_00006_moment_timeoffi_v0_0_0(),
        "momentunit": idea_format_00000_momentunit_v0_0_0(),
        "nabu_timenum": idea_format_00070_nabu_epochtime_v0_0_0(),
        "person_partner_membership": idea_format_00020_person_partner_membership_v0_0_0(),
        "person_partnerunit": idea_format_00021_person_partnerunit_v0_0_0(),
        "person_plan_awardunit": idea_format_00022_person_plan_awardunit_v0_0_0(),
        "person_plan_factunit": idea_format_00023_person_plan_factunit_v0_0_0(),
        "person_plan_healerunit": idea_format_00025_person_plan_healerunit_v0_0_0(),
        "person_plan_partyunit": idea_format_00024_person_plan_partyunit_v0_0_0(),
        "person_plan_reason_caseunit": idea_format_00026_person_plan_reason_caseunit_v0_0_0(),
        "person_plan_reasonunit": idea_format_00027_person_plan_reasonunit_v0_0_0(),
        "person_planunit": idea_format_00028_person_planunit_v0_0_0(),
        "personunit": idea_format_00029_personunit_v0_0_0(),
        "translate_label": idea_format_00044_translate_label_v0_0_0(),
        "translate_name": idea_format_00043_translate_name_v0_0_0(),
        "translate_title": idea_format_00042_translate_title_v0_0_0(),
        "translate_rope": idea_format_00045_translate_rope_v0_0_0(),
    }


def get_dimen_minimum_del_idea_names() -> dict[str, str]:
    """Returns all dimens and the idea format with only the args for that dimen."""

    return {
        "person_partner_membership": idea_format_00050_delete_person_partner_membership_v0_0_0(),
        "person_partnerunit": idea_format_00051_delete_person_partnerunit_v0_0_0(),
        "person_plan_awardunit": idea_format_00052_delete_person_plan_awardunit_v0_0_0(),
        "person_plan_factunit": idea_format_00053_delete_person_plan_factunit_v0_0_0(),
        "person_plan_healerunit": idea_format_00055_delete_person_plan_healerunit_v0_0_0(),
        "person_plan_partyunit": idea_format_00054_delete_person_plan_partyunit_v0_0_0(),
        "person_plan_reason_caseunit": idea_format_00056_delete_person_plan_reason_caseunit_v0_0_0(),
        "person_plan_reasonunit": idea_format_00057_delete_person_plan_reasonunit_v0_0_0(),
        "person_planunit": idea_format_00058_delete_person_planunit_v0_0_0(),
        "personunit": idea_format_00059_delete_personunit_v0_0_0(),
    }
