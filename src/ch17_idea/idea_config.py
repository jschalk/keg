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
    """src/ch17_idea/idea_formats"""
    ch_dir = create_path("src", "ch17_idea")
    return create_path(ch_dir, "idea_formats")


def get_idea_elements_sort_order() -> list[str]:
    """Contains the standard sort order for all idea and person_calc columns"""
    return [
        "world_name",
        "idea_type",
        "source_dimen",
        "translate_spark_num",
        "spark_num",
        "spark_face",
        "spark_face_otx",
        "spark_face_inx",
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
        "contact_name",
        "contact_name_otx",
        "contact_name_inx",
        "contact_name_ERASE",
        "contact_name_ERASE_otx",
        "contact_name_ERASE_inx",
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
        "labor_title",
        "labor_title_otx",
        "labor_title_inx",
        "labor_title_ERASE",
        "labor_title_ERASE_otx",
        "labor_title_ERASE_inx",
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
        "contact_cred_lumen",
        "contact_debt_lumen",
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
        "person_name_is_workforce",
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
        "inallocable_contact_debt_lumen",
        "gogo_calc",
        "stop_calc",
        "tree_level",
        "range_evaluated",
        "descendant_pledge_count",
        "healerunit_ratio",
        "all_contact_cred",
        "keeps_justified",
        "offtrack_fund",
        "parent_heir_active",
        "irrational_contact_debt_lumen",
        "sum_healerunit_plans_fund_total",
        "keeps_buildable",
        "all_contact_debt",
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
        "active_requisite": "INTEGER",
        "addin": "REAL",
        "all_contact_cred": "INTEGER",
        "all_contact_debt": "INTEGER",
        "amount": "REAL",
        "awardee_title": "TEXT",
        "awardee_title_ERASE": "TEXT",
        "awardee_title_ERASE_inx": "TEXT",
        "awardee_title_ERASE_otx": "TEXT",
        "awardee_title_inx": "TEXT",
        "awardee_title_otx": "TEXT",
        "begin": "REAL",
        "bud_time": "INTEGER",
        "bud_time_inx": "INTEGER",
        "bud_time_otx": "INTEGER",
        "c400_number": "INTEGER",
        "case_active": "INTEGER",
        "case_task": "INTEGER",
        "celldepth": "INTEGER",
        "close": "REAL",
        "contact_cred_lumen": "REAL",
        "contact_debt_lumen": "REAL",
        "contact_name": "TEXT",
        "contact_name_ERASE": "TEXT",
        "contact_name_ERASE_inx": "TEXT",
        "contact_name_ERASE_otx": "TEXT",
        "contact_name_inx": "TEXT",
        "contact_name_otx": "TEXT",
        "context_plan_close": "REAL",
        "context_plan_denom": "REAL",
        "context_plan_morph": "REAL",
        "credor_pool": "REAL",
        "credor_respect": "REAL",
        "cumulative_day": "INTEGER",
        "cumulative_minute": "INTEGER",
        "debtor_pool": "REAL",
        "debtor_respect": "REAL",
        "denom": "INTEGER",
        "descendant_pledge_count": "INTEGER",
        "epoch_label": "TEXT",
        "epoch_label_inx": "TEXT",
        "epoch_label_otx": "TEXT",
        "error_message": "TEXT",
        "fact_context": "TEXT",
        "fact_context_ERASE": "TEXT",
        "fact_context_ERASE_inx": "TEXT",
        "fact_context_ERASE_otx": "TEXT",
        "fact_context_inx": "TEXT",
        "fact_context_otx": "TEXT",
        "fact_lower": "REAL",
        "fact_lower_inx": "REAL",
        "fact_lower_otx": "REAL",
        "fact_state": "TEXT",
        "fact_state_inx": "TEXT",
        "fact_state_otx": "TEXT",
        "fact_upper": "REAL",
        "fact_upper_inx": "REAL",
        "fact_upper_otx": "REAL",
        "fund_agenda_give": "REAL",
        "fund_agenda_ratio_give": "REAL",
        "fund_agenda_ratio_take": "REAL",
        "fund_agenda_take": "REAL",
        "fund_cease": "REAL",
        "fund_give": "REAL",
        "fund_grain": "REAL",
        "fund_onset": "REAL",
        "fund_pool": "REAL",
        "fund_rank": "INTEGER",
        "fund_ratio": "REAL",
        "fund_take": "REAL",
        "give_force": "REAL",
        "gogo_calc": "REAL",
        "gogo_want": "REAL",
        "group_cred_lumen": "REAL",
        "group_debt_lumen": "REAL",
        "group_title": "TEXT",
        "group_title_ERASE": "TEXT",
        "group_title_ERASE_inx": "TEXT",
        "group_title_ERASE_otx": "TEXT",
        "group_title_inx": "TEXT",
        "group_title_otx": "TEXT",
        "groupmark": "TEXT",
        "healer_name": "TEXT",
        "healer_name_ERASE": "TEXT",
        "healer_name_ERASE_inx": "TEXT",
        "healer_name_ERASE_otx": "TEXT",
        "healer_name_inx": "TEXT",
        "healer_name_otx": "TEXT",
        "healerunit_ratio": "REAL",
        "hour_label": "TEXT",
        "hour_label_inx": "TEXT",
        "hour_label_otx": "TEXT",
        "idea_type": "TEXT",
        "inallocable_contact_debt_lumen": "REAL",
        "inx_epoch_diff": "INTEGER",
        "inx_knot": "TEXT",
        "inx_label": "TEXT",
        "inx_name": "TEXT",
        "inx_rope": "TEXT",
        "inx_time": "INTEGER",
        "inx_title": "TEXT",
        "irrational_contact_debt_lumen": "REAL",
        "job_listen_rotations": "INTEGER",
        "keeps_buildable": "INTEGER",
        "keeps_justified": "INTEGER",
        "knot": "TEXT",
        "labor_title": "TEXT",
        "labor_title_ERASE": "TEXT",
        "labor_title_ERASE_inx": "TEXT",
        "labor_title_ERASE_otx": "TEXT",
        "labor_title_inx": "TEXT",
        "labor_title_otx": "TEXT",
        "mana_grain": "REAL",
        "max_tree_traverse": "INTEGER",
        "moment_rope": "TEXT",
        "moment_rope_inx": "TEXT",
        "moment_rope_otx": "TEXT",
        "month_label": "TEXT",
        "month_label_inx": "TEXT",
        "month_label_otx": "TEXT",
        "monthday_index": "INTEGER",
        "morph": "INTEGER",
        "net_funds": "REAL",
        "numor": "INTEGER",
        "offi_time": "INTEGER",
        "offi_time_inx": "INTEGER",
        "offi_time_otx": "INTEGER",
        "offtrack_fund": "REAL",
        "otx_knot": "TEXT",
        "otx_label": "TEXT",
        "otx_name": "TEXT",
        "otx_rope": "TEXT",
        "otx_time": "INTEGER",
        "otx_title": "TEXT",
        "parent_heir_active": "INTEGER",
        "person_name": "TEXT",
        "person_name_ERASE": "TEXT",
        "person_name_ERASE_inx": "TEXT",
        "person_name_ERASE_otx": "TEXT",
        "person_name_inx": "TEXT",
        "person_name_is_workforce": "INTEGER",
        "person_name_otx": "TEXT",
        "plan_active": "INTEGER",
        "plan_rope": "TEXT",
        "plan_rope_ERASE": "TEXT",
        "plan_rope_ERASE_inx": "TEXT",
        "plan_rope_ERASE_otx": "TEXT",
        "plan_rope_inx": "TEXT",
        "plan_rope_otx": "TEXT",
        "plan_task": "INTEGER",
        "pledge": "INTEGER",
        "pledges_count": "INTEGER",
        "problem_bool": "INTEGER",
        "quota": "REAL",
        "range_evaluated": "INTEGER",
        "rational": "INTEGER",
        "reason_active": "INTEGER",
        "reason_context": "TEXT",
        "reason_context_ERASE": "TEXT",
        "reason_context_ERASE_inx": "TEXT",
        "reason_context_ERASE_otx": "TEXT",
        "reason_context_inx": "TEXT",
        "reason_context_otx": "TEXT",
        "reason_divisor": "INTEGER",
        "reason_lower": "REAL",
        "reason_lower_inx": "REAL",
        "reason_lower_otx": "REAL",
        "reason_state": "TEXT",
        "reason_state_ERASE": "TEXT",
        "reason_state_ERASE_inx": "TEXT",
        "reason_state_ERASE_otx": "TEXT",
        "reason_state_inx": "TEXT",
        "reason_state_otx": "TEXT",
        "reason_task": "INTEGER",
        "reason_upper": "REAL",
        "reason_upper_inx": "REAL",
        "reason_upper_otx": "REAL",
        "respect_grain": "REAL",
        "solo": "INTEGER",
        "source_dimen": "TEXT",
        "spark_face": "TEXT",
        "spark_face_inx": "TEXT",
        "spark_face_otx": "TEXT",
        "spark_num": "INTEGER",
        "star": "INTEGER",
        "stop_calc": "REAL",
        "stop_want": "REAL",
        "sum_healerunit_plans_fund_total": "REAL",
        "take_force": "REAL",
        "tran_time": "INTEGER",
        "tran_time_inx": "INTEGER",
        "tran_time_otx": "INTEGER",
        "translate_spark_num": "INTEGER",
        "tree_level": "INTEGER",
        "tree_traverse_count": "INTEGER",
        "unknown_str": "TEXT",
        "weekday_label": "TEXT",
        "weekday_label_inx": "TEXT",
        "weekday_label_otx": "TEXT",
        "weekday_order": "INTEGER",
        "world_name": "TEXT",
        "yr1_jan1_offset": "INTEGER",
    }


# def ii00100_momentunit_v0_0_0()->str: return "ii00100_momentunit_v0_0_0"
# def ii00101_moment_budunit_v0_0_0()->str: return "ii00101_moment_budunit_v0_0_0"
# def ii00102_moment_paybook_v0_0_0()->str: return "ii00102_moment_paybook_v0_0_0"
# def ii00103_moment_epoch_hour_v0_0_0()->str: return "ii00103_moment_epoch_hour_v0_0_0"
# def ii00104_moment_epoch_month_v0_0_0()->str: return "ii00104_moment_epoch_month_v0_0_0"
# def ii00105_moment_epoch_weekday_v0_0_0()->str: return "ii00105_moment_epoch_weekday_v0_0_0"


def ii00001_contact_v0_0_0() -> str:
    return "ii00001_contact_v0_0_0"


def ii00002_planunit_v0_0_0() -> str:
    return "ii00002_planunit_v0_0_0"


def ii00005_plan_reason() -> str:
    return "ii00005_plan_reason"


def ii00007_moment_fact() -> str:
    return "ii00007_moment_fact"


def ii00100_momentunit_v0_0_0() -> str:
    return "ii00100_momentunit_v0_0_0"


def ii00101_moment_budunit_v0_0_0() -> str:
    return "ii00101_moment_budunit_v0_0_0"


def ii00102_moment_paybook_v0_0_0() -> str:
    return "ii00102_moment_paybook_v0_0_0"


def ii00103_moment_epoch_hour_v0_0_0() -> str:
    return "ii00103_moment_epoch_hour_v0_0_0"


def ii00104_moment_epoch_month_v0_0_0() -> str:
    return "ii00104_moment_epoch_month_v0_0_0"


def ii00105_moment_epoch_weekday_v0_0_0() -> str:
    return "ii00105_moment_epoch_weekday_v0_0_0"


def ii00106_moment_timeoffi_v0_0_0() -> str:
    return "ii00106_moment_timeoffi_v0_0_0"


def ii00112_membership_v0_0_0() -> str:
    return "ii00112_membership_v0_0_0"


def ii00119_planunit_v0_0_0() -> str:
    return "ii00119_planunit_v0_0_0"


# def ii00120_person_contact_membership_v0_0_0()-> str: return "ii00120_person_contact_membership_v0_0_0"
# def ii00121_person_contactunit_v0_0_0()-> str: return "ii00121_person_contactunit_v0_0_0"
# def ii00122_person_plan_awardunit_v0_0_0()-> str: return "ii00122_person_plan_awardunit_v0_0_0"
# def ii00123_person_plan_factunit_v0_0_0()-> str: return "ii00123_person_plan_factunit_v0_0_0"
# def ii00124_person_plan_laborunit_v0_0_0()-> str: return "ii00124_person_plan_laborunit_v0_0_0"
# def ii00125_person_plan_healerunit_v0_0_0()-> str: return "ii00125_person_plan_healerunit_v0_0_0"
# def ii00126_person_plan_reason_caseunit_v0_0_0()-> str: return "ii00126_person_plan_reason_caseunit_v0_0_0"
# def ii00127_person_plan_reasonunit_v0_0_0()-> str: return "ii00127_person_plan_reasonunit_v0_0_0"
# def ii00128_person_planunit_v0_0_0()-> str: return "ii00128_person_planunit_v0_0_0"
# def ii00129_personunit_v0_0_0()-> str: return "ii00129_personunit_v0_0_0"


def ii00120_person_contact_membership_v0_0_0() -> str:
    return "ii00120_person_contact_membership_v0_0_0"


def ii00121_person_contactunit_v0_0_0() -> str:
    return "ii00121_person_contactunit_v0_0_0"


def ii00122_person_plan_awardunit_v0_0_0() -> str:
    return "ii00122_person_plan_awardunit_v0_0_0"


def ii00123_person_plan_factunit_v0_0_0() -> str:
    return "ii00123_person_plan_factunit_v0_0_0"


def ii00124_person_plan_laborunit_v0_0_0() -> str:
    return "ii00124_person_plan_laborunit_v0_0_0"


def ii00125_person_plan_healerunit_v0_0_0() -> str:
    return "ii00125_person_plan_healerunit_v0_0_0"


def ii00126_person_plan_reason_caseunit_v0_0_0() -> str:
    return "ii00126_person_plan_reason_caseunit_v0_0_0"


def ii00127_person_plan_reasonunit_v0_0_0() -> str:
    return "ii00127_person_plan_reasonunit_v0_0_0"


def ii00128_person_planunit_v0_0_0() -> str:
    return "ii00128_person_planunit_v0_0_0"


def ii00129_personunit_v0_0_0() -> str:
    return "ii00129_personunit_v0_0_0"


def ii00136_problem_healer_v0_0_0() -> str:
    return "ii00136_problem_healer_v0_0_0"


def ii00140_map_otx2inx_v0_0_0() -> str:
    return "ii00140_map_otx2inx_v0_0_0"


def ii00142_translate_title_v0_0_0() -> str:
    return "ii00142_translate_title_v0_0_0"


def ii00143_translate_name_v0_0_0() -> str:
    return "ii00143_translate_name_v0_0_0"


def ii00144_translate_label_v0_0_0() -> str:
    return "ii00144_translate_label_v0_0_0"


def ii00145_translate_rope_v0_0_0() -> str:
    return "ii00145_translate_rope_v0_0_0"


def ii00150_delete_person_contact_membership_v0_0_0() -> str:
    return "ii00150_delete_person_contact_membership_v0_0_0"


def ii00151_delete_person_contactunit_v0_0_0() -> str:
    return "ii00151_delete_person_contactunit_v0_0_0"


def ii00152_delete_person_plan_awardunit_v0_0_0() -> str:
    return "ii00152_delete_person_plan_awardunit_v0_0_0"


def ii00153_delete_person_plan_factunit_v0_0_0() -> str:
    return "ii00153_delete_person_plan_factunit_v0_0_0"


def ii00154_delete_person_plan_laborunit_v0_0_0() -> str:
    return "ii00154_delete_person_plan_laborunit_v0_0_0"


def ii00155_delete_person_plan_healerunit_v0_0_0() -> str:
    return "ii00155_delete_person_plan_healerunit_v0_0_0"


def ii00156_delete_person_plan_reason_caseunit_v0_0_0() -> str:
    return "ii00156_delete_person_plan_reason_caseunit_v0_0_0"


def ii00157_delete_person_plan_reasonunit_v0_0_0() -> str:
    return "ii00157_delete_person_plan_reasonunit_v0_0_0"


def ii00158_delete_person_planunit_v0_0_0() -> str:
    return "ii00158_delete_person_planunit_v0_0_0"


def ii00159_delete_personunit_v0_0_0() -> str:
    return "ii00159_delete_personunit_v0_0_0"


def ii00170_nabu_epochtime_v0_0_0() -> str:
    return "ii00170_nabu_epochtime_v0_0_0"


def ii00171_contact_map1_v0_0_0() -> str:
    return "ii00171_contact_map1_v0_0_0"


def ii00172_group_map1_v0_0_0() -> str:
    return "ii00172_group_map1_v0_0_0"


def ii00173_label_map1_v0_0_0() -> str:
    return "ii00173_label_map1_v0_0_0"


def ii00174_rope_map1_v0_0_0() -> str:
    return "ii00174_rope_map1_v0_0_0"


def get_idea_format_filenames() -> set[str]:
    return {
        ii00001_contact_v0_0_0(),
        ii00002_planunit_v0_0_0(),
        ii00005_plan_reason(),
        ii00007_moment_fact(),
        ii00100_momentunit_v0_0_0(),
        ii00101_moment_budunit_v0_0_0(),
        ii00102_moment_paybook_v0_0_0(),
        ii00103_moment_epoch_hour_v0_0_0(),
        ii00104_moment_epoch_month_v0_0_0(),
        ii00105_moment_epoch_weekday_v0_0_0(),
        ii00106_moment_timeoffi_v0_0_0(),
        ii00112_membership_v0_0_0(),
        ii00119_planunit_v0_0_0(),
        ii00120_person_contact_membership_v0_0_0(),
        ii00121_person_contactunit_v0_0_0(),
        ii00122_person_plan_awardunit_v0_0_0(),
        ii00123_person_plan_factunit_v0_0_0(),
        ii00124_person_plan_laborunit_v0_0_0(),
        ii00125_person_plan_healerunit_v0_0_0(),
        ii00126_person_plan_reason_caseunit_v0_0_0(),
        ii00127_person_plan_reasonunit_v0_0_0(),
        ii00128_person_planunit_v0_0_0(),
        ii00129_personunit_v0_0_0(),
        ii00136_problem_healer_v0_0_0(),
        ii00142_translate_title_v0_0_0(),
        ii00143_translate_name_v0_0_0(),
        ii00144_translate_label_v0_0_0(),
        ii00145_translate_rope_v0_0_0(),
        ii00150_delete_person_contact_membership_v0_0_0(),
        ii00151_delete_person_contactunit_v0_0_0(),
        ii00152_delete_person_plan_awardunit_v0_0_0(),
        ii00153_delete_person_plan_factunit_v0_0_0(),
        ii00154_delete_person_plan_laborunit_v0_0_0(),
        ii00155_delete_person_plan_healerunit_v0_0_0(),
        ii00156_delete_person_plan_reason_caseunit_v0_0_0(),
        ii00157_delete_person_plan_reasonunit_v0_0_0(),
        ii00158_delete_person_planunit_v0_0_0(),
        ii00159_delete_personunit_v0_0_0(),
        ii00170_nabu_epochtime_v0_0_0(),
        ii00171_contact_map1_v0_0_0(),
        ii00172_group_map1_v0_0_0(),
        ii00173_label_map1_v0_0_0(),
        ii00174_rope_map1_v0_0_0(),
    }


def get_idea_types() -> set[str]:
    return {
        "ii00001",
        "ii00002",
        "ii00005",
        "ii00007",
        "ii00100",
        "ii00101",
        "ii00102",
        "ii00103",
        "ii00104",
        "ii00105",
        "ii00106",
        "ii00112",
        "ii00119",
        "ii00120",
        "ii00121",
        "ii00122",
        "ii00123",
        "ii00124",
        "ii00125",
        "ii00126",
        "ii00127",
        "ii00128",
        "ii00129",
        "ii00136",
        "ii00142",
        "ii00143",
        "ii00144",
        "ii00145",
        "ii00150",
        "ii00151",
        "ii00152",
        "ii00153",
        "ii00154",
        "ii00155",
        "ii00156",
        "ii00157",
        "ii00158",
        "ii00159",
        "ii00170",
        "ii00171",
        "ii00172",
        "ii00173",
        "ii00174",
    }


def get_idea_format_filename(idea_type: str) -> str:
    idea_type_substring = idea_type[2:]
    for idea_format_filename in get_idea_format_filenames():
        if idea_format_filename[2:7] == idea_type_substring:
            return idea_format_filename


def get_idea_format_headers() -> dict[str, list[str]]:
    return {
        "moment_rope,person_name,contact_name": ii00001_contact_v0_0_0(),
        "moment_rope,person_name,plan_rope,star,pledge": ii00002_planunit_v0_0_0(),
        "moment_rope,person_name,plan_rope,reason_context,reason_state,star,pledge": ii00005_plan_reason(),
        "moment_rope,person_name,plan_rope,fact_context,fact_state": ii00007_moment_fact(),
        "moment_rope,epoch_label,c400_number,yr1_jan1_offset,monthday_index,fund_grain,mana_grain,respect_grain,knot,job_listen_rotations": ii00100_momentunit_v0_0_0(),
        "moment_rope,person_name,bud_time,knot,quota,celldepth": ii00101_moment_budunit_v0_0_0(),
        "moment_rope,person_name,contact_name,tran_time,amount,knot": ii00102_moment_paybook_v0_0_0(),
        "moment_rope,cumulative_minute,hour_label,knot": ii00103_moment_epoch_hour_v0_0_0(),
        "moment_rope,cumulative_day,month_label,knot": ii00104_moment_epoch_month_v0_0_0(),
        "moment_rope,weekday_order,weekday_label,knot": ii00105_moment_epoch_weekday_v0_0_0(),
        "moment_rope,offi_time,knot": ii00106_moment_timeoffi_v0_0_0(),
        "moment_rope,person_name,contact_name,group_title": ii00112_membership_v0_0_0(),
        "moment_rope,person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want": ii00119_planunit_v0_0_0(),
        "moment_rope,person_name,contact_name,group_title,group_cred_lumen,group_debt_lumen,knot": ii00120_person_contact_membership_v0_0_0(),
        "moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot": ii00121_person_contactunit_v0_0_0(),
        "person_name,plan_rope,awardee_title,give_force,take_force,knot": ii00122_person_plan_awardunit_v0_0_0(),
        "person_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper,knot": ii00123_person_plan_factunit_v0_0_0(),
        "person_name,plan_rope,labor_title,solo,knot": ii00124_person_plan_laborunit_v0_0_0(),
        "person_name,plan_rope,healer_name,knot": ii00125_person_plan_healerunit_v0_0_0(),
        "person_name,plan_rope,reason_context,reason_state,reason_lower,reason_upper,reason_divisor,knot": ii00126_person_plan_reason_caseunit_v0_0_0(),
        "person_name,plan_rope,reason_context,active_requisite,knot": ii00127_person_plan_reasonunit_v0_0_0(),
        "person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool,knot": ii00128_person_planunit_v0_0_0(),
        "moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain,knot": ii00129_personunit_v0_0_0(),
        "moment_rope,person_name,plan_rope,healer_name,problem_bool": ii00136_problem_healer_v0_0_0(),
        "otx_title,inx_title,otx_knot,inx_knot,unknown_str": ii00142_translate_title_v0_0_0(),
        "otx_name,inx_name,otx_knot,inx_knot,unknown_str": ii00143_translate_name_v0_0_0(),
        "otx_label,inx_label,otx_knot,inx_knot,unknown_str": ii00144_translate_label_v0_0_0(),
        "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str": ii00145_translate_rope_v0_0_0(),
        "moment_rope,person_name,contact_name,group_title_ERASE": ii00150_delete_person_contact_membership_v0_0_0(),
        "moment_rope,person_name,contact_name_ERASE": ii00151_delete_person_contactunit_v0_0_0(),
        "person_name,plan_rope,awardee_title_ERASE": ii00152_delete_person_plan_awardunit_v0_0_0(),
        "person_name,plan_rope,fact_context_ERASE": ii00153_delete_person_plan_factunit_v0_0_0(),
        "person_name,plan_rope,labor_title_ERASE": ii00154_delete_person_plan_laborunit_v0_0_0(),
        "person_name,plan_rope,healer_name_ERASE": ii00155_delete_person_plan_healerunit_v0_0_0(),
        "person_name,plan_rope,reason_context,reason_state_ERASE": ii00156_delete_person_plan_reason_caseunit_v0_0_0(),
        "person_name,plan_rope,reason_context_ERASE": ii00157_delete_person_plan_reasonunit_v0_0_0(),
        "person_name,plan_rope_ERASE": ii00158_delete_person_planunit_v0_0_0(),
        "moment_rope,person_name_ERASE": ii00159_delete_personunit_v0_0_0(),
        "moment_rope,otx_time,inx_time": ii00170_nabu_epochtime_v0_0_0(),
        "moment_rope,person_name,contact_name,otx_name,inx_name": ii00171_contact_map1_v0_0_0(),
        "moment_rope,person_name,contact_name,otx_title,inx_title": ii00172_group_map1_v0_0_0(),
        "moment_rope,person_name,contact_name,otx_label,inx_label": ii00173_label_map1_v0_0_0(),
        "moment_rope,person_name,contact_name,otx_rope,inx_rope": ii00174_rope_map1_v0_0_0(),
    }


def get_idearef_from_file(idea_format_filename: str) -> dict:
    idearef_filename = get_json_filename(idea_format_filename)
    return open_json(get_idea_formats_dir(), idearef_filename)


def get_quick_ideas_column_ref() -> dict[str, set[str]]:
    idea_type_dict = {}
    for idea_format_filename in get_idea_format_filenames():
        idearef_dict = get_idearef_from_file(idea_format_filename)
        idea_type = idearef_dict.get("idea_type")
        idea_type_dict[idea_type] = set(idearef_dict.get("attributes").keys())
    return idea_type_dict


def get_idea_dimen_ref() -> dict[str, set[str]]:
    """dictionary with key=dimen and value=set of all idea_types with that dimen's data"""
    return {
        "moment_budunit": {"ii00101"},
        "moment_epoch_hour": {"ii00103"},
        "moment_epoch_month": {"ii00104"},
        "moment_epoch_weekday": {"ii00105"},
        "moment_paybook": {"ii00102"},
        "moment_timeoffi": {"ii00106"},
        "momentunit": {
            "ii00001",
            "ii00002",
            "ii00005",
            "ii00007",
            "ii00100",
            "ii00101",
            "ii00102",
            "ii00103",
            "ii00104",
            "ii00105",
            "ii00106",
            "ii00112",
            "ii00119",
            "ii00120",
            "ii00121",
            "ii00129",
            "ii00136",
            "ii00150",
            "ii00151",
            "ii00159",
            "ii00170",
            "ii00171",
            "ii00172",
            "ii00173",
            "ii00174",
        },
        "nabu_timenum": {"ii00170"},
        "person_contact_membership": {"ii00112", "ii00120", "ii00150"},
        "person_contactunit": {
            "ii00001",
            "ii00102",
            "ii00112",
            "ii00120",
            "ii00121",
            "ii00150",
            "ii00151",
            "ii00171",
            "ii00172",
            "ii00173",
            "ii00174",
        },
        "person_plan_awardunit": {"ii00122", "ii00152"},
        "person_plan_factunit": {"ii00007", "ii00123", "ii00153"},
        "person_plan_healerunit": {"ii00125", "ii00136", "ii00155"},
        "person_plan_laborunit": {"ii00124", "ii00154"},
        "person_plan_reason_caseunit": {"ii00005", "ii00126", "ii00156"},
        "person_plan_reasonunit": {
            "ii00005",
            "ii00126",
            "ii00127",
            "ii00156",
            "ii00157",
        },
        "person_planunit": {
            "ii00002",
            "ii00005",
            "ii00007",
            "ii00119",
            "ii00122",
            "ii00123",
            "ii00124",
            "ii00125",
            "ii00126",
            "ii00127",
            "ii00128",
            "ii00136",
            "ii00152",
            "ii00153",
            "ii00154",
            "ii00155",
            "ii00156",
            "ii00157",
            "ii00158",
        },
        "personunit": {
            "ii00001",
            "ii00002",
            "ii00005",
            "ii00007",
            "ii00101",
            "ii00102",
            "ii00112",
            "ii00119",
            "ii00120",
            "ii00121",
            "ii00129",
            "ii00136",
            "ii00150",
            "ii00151",
            "ii00159",
            "ii00171",
            "ii00172",
            "ii00173",
            "ii00174",
        },
        "translate_label": {"ii00144", "ii00173"},
        "translate_name": {"ii00143", "ii00171"},
        "translate_rope": {"ii00145", "ii00174"},
        "translate_title": {"ii00142", "ii00172"},
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
        "moment_budunit": ii00101_moment_budunit_v0_0_0(),
        "moment_epoch_hour": ii00103_moment_epoch_hour_v0_0_0(),
        "moment_epoch_month": ii00104_moment_epoch_month_v0_0_0(),
        "moment_epoch_weekday": ii00105_moment_epoch_weekday_v0_0_0(),
        "moment_paybook": ii00102_moment_paybook_v0_0_0(),
        "moment_timeoffi": ii00106_moment_timeoffi_v0_0_0(),
        "momentunit": ii00100_momentunit_v0_0_0(),
        "nabu_timenum": ii00170_nabu_epochtime_v0_0_0(),
        "person_contact_membership": ii00120_person_contact_membership_v0_0_0(),
        "person_contactunit": ii00121_person_contactunit_v0_0_0(),
        "person_plan_awardunit": ii00122_person_plan_awardunit_v0_0_0(),
        "person_plan_factunit": ii00123_person_plan_factunit_v0_0_0(),
        "person_plan_healerunit": ii00125_person_plan_healerunit_v0_0_0(),
        "person_plan_laborunit": ii00124_person_plan_laborunit_v0_0_0(),
        "person_plan_reason_caseunit": ii00126_person_plan_reason_caseunit_v0_0_0(),
        "person_plan_reasonunit": ii00127_person_plan_reasonunit_v0_0_0(),
        "person_planunit": ii00128_person_planunit_v0_0_0(),
        "personunit": ii00129_personunit_v0_0_0(),
        "translate_label": ii00144_translate_label_v0_0_0(),
        "translate_name": ii00143_translate_name_v0_0_0(),
        "translate_title": ii00142_translate_title_v0_0_0(),
        "translate_rope": ii00145_translate_rope_v0_0_0(),
    }


def get_dimen_minimum_del_idea_names() -> dict[str, str]:
    """Returns all dimens and the idea format with only the args for that dimen."""

    return {
        "person_contact_membership": ii00150_delete_person_contact_membership_v0_0_0(),
        "person_contactunit": ii00151_delete_person_contactunit_v0_0_0(),
        "person_plan_awardunit": ii00152_delete_person_plan_awardunit_v0_0_0(),
        "person_plan_factunit": ii00153_delete_person_plan_factunit_v0_0_0(),
        "person_plan_healerunit": ii00155_delete_person_plan_healerunit_v0_0_0(),
        "person_plan_laborunit": ii00154_delete_person_plan_laborunit_v0_0_0(),
        "person_plan_reason_caseunit": ii00156_delete_person_plan_reason_caseunit_v0_0_0(),
        "person_plan_reasonunit": ii00157_delete_person_plan_reasonunit_v0_0_0(),
        "person_planunit": ii00158_delete_person_planunit_v0_0_0(),
        "personunit": ii00159_delete_personunit_v0_0_0(),
    }
