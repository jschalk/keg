from ch00_py.db_toolbox import get_sorted_cols_only_list
from ch00_py.file_toolbox import create_path, get_json_filename, open_json
from enum import Enum
from os import getcwd as os_getcwd


def brick_config_path() -> str:
    "Returns path: ch17_brick_logic/brick_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch17_brick")
    return create_path(chapter_dir, "brick_config.json")


def get_brick_config_dict(brick_categorys: set[str] = None) -> dict:
    """If brick_categorys is None/empty return entire brick_config_dict, otherwise filter on brick_category"""
    brick_config_dict = open_json(brick_config_path())
    if brick_categorys:
        return {
            x_dimen: dimen_config
            for x_dimen, dimen_config in brick_config_dict.items()
            if dimen_config.get("brick_category") in brick_categorys
        }
    else:
        return brick_config_dict


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


def get_brick_formats_dir() -> str:
    """src/ch17_brick/brick_formats"""
    ch_dir = create_path("src", "ch17_brick")
    return create_path(ch_dir, "brick_formats")


def get_brick_elements_sort_order() -> list[str]:
    """Contains the standard sort order for all brick and person_calc columns"""
    return [
        "world_name",
        "brick_type",
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
        sorting_columns = get_brick_elements_sort_order()
    return get_sorted_cols_only_list(existing_columns, sorting_columns)


def get_brick_sqlite_types() -> dict[str, str]:
    """Returns dictionary of sqlite_type for all brick elements (reference source: get_brick_elements_sort_order)"""

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
        "brick_type": "TEXT",
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


class BrickFormatsEnum(str, Enum):
    bk00001_contact_v0_0_0 = "bk00001_contact_v0_0_0"
    bk00002_planunit_v0_0_0 = "bk00002_planunit_v0_0_0"
    bk00005_plan_reason = "bk00005_plan_reason"
    bk00007_moment_fact = "bk00007_moment_fact"
    bk00100_momentunit_v0_0_0 = "bk00100_momentunit_v0_0_0"
    bk00101_moment_budunit_v0_0_0 = "bk00101_moment_budunit_v0_0_0"
    bk00102_moment_paybook_v0_0_0 = "bk00102_moment_paybook_v0_0_0"
    bk00103_moment_epoch_hour_v0_0_0 = "bk00103_moment_epoch_hour_v0_0_0"
    bk00104_moment_epoch_month_v0_0_0 = "bk00104_moment_epoch_month_v0_0_0"
    bk00105_moment_epoch_weekday_v0_0_0 = "bk00105_moment_epoch_weekday_v0_0_0"
    bk00106_moment_timeoffi_v0_0_0 = "bk00106_moment_timeoffi_v0_0_0"
    bk00112_membership_v0_0_0 = "bk00112_membership_v0_0_0"
    bk00119_planunit_v0_0_0 = "bk00119_planunit_v0_0_0"
    bk00120_person_contact_membership_v0_0_0 = (
        "bk00120_person_contact_membership_v0_0_0"
    )
    bk00121_person_contactunit_v0_0_0 = "bk00121_person_contactunit_v0_0_0"
    bk00122_person_plan_awardunit_v0_0_0 = "bk00122_person_plan_awardunit_v0_0_0"
    bk00123_person_plan_factunit_v0_0_0 = "bk00123_person_plan_factunit_v0_0_0"
    bk00124_person_plan_laborunit_v0_0_0 = "bk00124_person_plan_laborunit_v0_0_0"
    bk00125_person_plan_healerunit_v0_0_0 = "bk00125_person_plan_healerunit_v0_0_0"
    bk00126_person_plan_reason_caseunit_v0_0_0 = (
        "bk00126_person_plan_reason_caseunit_v0_0_0"
    )
    bk00127_person_plan_reasonunit_v0_0_0 = "bk00127_person_plan_reasonunit_v0_0_0"
    bk00128_person_planunit_v0_0_0 = "bk00128_person_planunit_v0_0_0"
    bk00129_personunit_v0_0_0 = "bk00129_personunit_v0_0_0"
    bk00136_problem_healer_v0_0_0 = "bk00136_problem_healer_v0_0_0"
    bk00140_map_otx2inx_v0_0_0 = "bk00140_map_otx2inx_v0_0_0"
    bk00142_translate_title_v0_0_0 = "bk00142_translate_title_v0_0_0"
    bk00143_translate_name_v0_0_0 = "bk00143_translate_name_v0_0_0"
    bk00144_translate_label_v0_0_0 = "bk00144_translate_label_v0_0_0"
    bk00145_translate_rope_v0_0_0 = "bk00145_translate_rope_v0_0_0"
    bk00150_delete_person_contact_membership_v0_0_0 = (
        "bk00150_delete_person_contact_membership_v0_0_0"
    )
    bk00151_delete_person_contactunit_v0_0_0 = (
        "bk00151_delete_person_contactunit_v0_0_0"
    )
    bk00152_delete_person_plan_awardunit_v0_0_0 = (
        "bk00152_delete_person_plan_awardunit_v0_0_0"
    )
    bk00153_delete_person_plan_factunit_v0_0_0 = (
        "bk00153_delete_person_plan_factunit_v0_0_0"
    )
    bk00154_delete_person_plan_laborunit_v0_0_0 = (
        "bk00154_delete_person_plan_laborunit_v0_0_0"
    )
    bk00155_delete_person_plan_healerunit_v0_0_0 = (
        "bk00155_delete_person_plan_healerunit_v0_0_0"
    )
    bk00156_delete_person_plan_reason_caseunit_v0_0_0 = (
        "bk00156_delete_person_plan_reason_caseunit_v0_0_0"
    )
    bk00157_delete_person_plan_reasonunit_v0_0_0 = (
        "bk00157_delete_person_plan_reasonunit_v0_0_0"
    )
    bk00158_delete_person_planunit_v0_0_0 = "bk00158_delete_person_planunit_v0_0_0"
    bk00159_delete_personunit_v0_0_0 = "bk00159_delete_personunit_v0_0_0"
    bk00170_nabu_time_v0_0_0 = "bk00170_nabu_time_v0_0_0"
    bk00171_contact_map1_v0_0_0 = "bk00171_contact_map1_v0_0_0"
    bk00172_group_map1_v0_0_0 = "bk00172_group_map1_v0_0_0"
    bk00173_label_map1_v0_0_0 = "bk00173_label_map1_v0_0_0"
    bk00174_rope_map1_v0_0_0 = "bk00174_rope_map1_v0_0_0"

    def __str__(self):
        return self.value


def get_brick_format_filenames() -> set[str]:
    ifx = BrickFormatsEnum
    return {
        ifx.bk00001_contact_v0_0_0,
        ifx.bk00002_planunit_v0_0_0,
        ifx.bk00005_plan_reason,
        ifx.bk00007_moment_fact,
        ifx.bk00100_momentunit_v0_0_0,
        ifx.bk00101_moment_budunit_v0_0_0,
        ifx.bk00102_moment_paybook_v0_0_0,
        ifx.bk00103_moment_epoch_hour_v0_0_0,
        ifx.bk00104_moment_epoch_month_v0_0_0,
        ifx.bk00105_moment_epoch_weekday_v0_0_0,
        ifx.bk00106_moment_timeoffi_v0_0_0,
        ifx.bk00112_membership_v0_0_0,
        ifx.bk00119_planunit_v0_0_0,
        ifx.bk00120_person_contact_membership_v0_0_0,
        ifx.bk00121_person_contactunit_v0_0_0,
        ifx.bk00122_person_plan_awardunit_v0_0_0,
        ifx.bk00123_person_plan_factunit_v0_0_0,
        ifx.bk00124_person_plan_laborunit_v0_0_0,
        ifx.bk00125_person_plan_healerunit_v0_0_0,
        ifx.bk00126_person_plan_reason_caseunit_v0_0_0,
        ifx.bk00127_person_plan_reasonunit_v0_0_0,
        ifx.bk00128_person_planunit_v0_0_0,
        ifx.bk00129_personunit_v0_0_0,
        ifx.bk00136_problem_healer_v0_0_0,
        ifx.bk00142_translate_title_v0_0_0,
        ifx.bk00143_translate_name_v0_0_0,
        ifx.bk00144_translate_label_v0_0_0,
        ifx.bk00145_translate_rope_v0_0_0,
        ifx.bk00150_delete_person_contact_membership_v0_0_0,
        ifx.bk00151_delete_person_contactunit_v0_0_0,
        ifx.bk00152_delete_person_plan_awardunit_v0_0_0,
        ifx.bk00153_delete_person_plan_factunit_v0_0_0,
        ifx.bk00154_delete_person_plan_laborunit_v0_0_0,
        ifx.bk00155_delete_person_plan_healerunit_v0_0_0,
        ifx.bk00156_delete_person_plan_reason_caseunit_v0_0_0,
        ifx.bk00157_delete_person_plan_reasonunit_v0_0_0,
        ifx.bk00158_delete_person_planunit_v0_0_0,
        ifx.bk00159_delete_personunit_v0_0_0,
        ifx.bk00170_nabu_time_v0_0_0,
        ifx.bk00171_contact_map1_v0_0_0,
        ifx.bk00172_group_map1_v0_0_0,
        ifx.bk00173_label_map1_v0_0_0,
        ifx.bk00174_rope_map1_v0_0_0,
    }


def get_brick_types() -> set[str]:
    return {
        "bk00001",
        "bk00002",
        "bk00005",
        "bk00007",
        "bk00100",
        "bk00101",
        "bk00102",
        "bk00103",
        "bk00104",
        "bk00105",
        "bk00106",
        "bk00112",
        "bk00119",
        "bk00120",
        "bk00121",
        "bk00122",
        "bk00123",
        "bk00124",
        "bk00125",
        "bk00126",
        "bk00127",
        "bk00128",
        "bk00129",
        "bk00136",
        "bk00142",
        "bk00143",
        "bk00144",
        "bk00145",
        "bk00150",
        "bk00151",
        "bk00152",
        "bk00153",
        "bk00154",
        "bk00155",
        "bk00156",
        "bk00157",
        "bk00158",
        "bk00159",
        "bk00170",
        "bk00171",
        "bk00172",
        "bk00173",
        "bk00174",
    }


def get_brick_format_filename(brick_type: str) -> str:
    brick_type_substring = brick_type[2:]
    for brick_format_filename in get_brick_format_filenames():
        if brick_format_filename[2:7] == brick_type_substring:
            return brick_format_filename


def get_brick_format_headers() -> dict[str, list[str]]:
    ifx = BrickFormatsEnum
    return {
        "moment_rope,person_name,contact_name": ifx.bk00001_contact_v0_0_0,
        "moment_rope,person_name,plan_rope,star,pledge": ifx.bk00002_planunit_v0_0_0,
        "moment_rope,person_name,plan_rope,reason_context,reason_state,star,pledge": ifx.bk00005_plan_reason,
        "moment_rope,person_name,plan_rope,fact_context,fact_state": ifx.bk00007_moment_fact,
        "moment_rope,epoch_label,c400_number,yr1_jan1_offset,monthday_index,fund_grain,mana_grain,respect_grain,knot,job_listen_rotations": ifx.bk00100_momentunit_v0_0_0,
        "moment_rope,person_name,bud_time,knot,quota,celldepth": ifx.bk00101_moment_budunit_v0_0_0,
        "moment_rope,person_name,contact_name,tran_time,amount,knot": ifx.bk00102_moment_paybook_v0_0_0,
        "moment_rope,cumulative_minute,hour_label,knot": ifx.bk00103_moment_epoch_hour_v0_0_0,
        "moment_rope,cumulative_day,month_label,knot": ifx.bk00104_moment_epoch_month_v0_0_0,
        "moment_rope,weekday_order,weekday_label,knot": ifx.bk00105_moment_epoch_weekday_v0_0_0,
        "moment_rope,offi_time,knot": ifx.bk00106_moment_timeoffi_v0_0_0,
        "moment_rope,person_name,contact_name,group_title": ifx.bk00112_membership_v0_0_0,
        "moment_rope,person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want": ifx.bk00119_planunit_v0_0_0,
        "moment_rope,person_name,contact_name,group_title,group_cred_lumen,group_debt_lumen,knot": ifx.bk00120_person_contact_membership_v0_0_0,
        "moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot": ifx.bk00121_person_contactunit_v0_0_0,
        "person_name,plan_rope,awardee_title,give_force,take_force,knot": ifx.bk00122_person_plan_awardunit_v0_0_0,
        "person_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper,knot": ifx.bk00123_person_plan_factunit_v0_0_0,
        "person_name,plan_rope,labor_title,solo,knot": ifx.bk00124_person_plan_laborunit_v0_0_0,
        "person_name,plan_rope,healer_name,knot": ifx.bk00125_person_plan_healerunit_v0_0_0,
        "person_name,plan_rope,reason_context,reason_state,reason_lower,reason_upper,reason_divisor,knot": ifx.bk00126_person_plan_reason_caseunit_v0_0_0,
        "person_name,plan_rope,reason_context,active_requisite,knot": ifx.bk00127_person_plan_reasonunit_v0_0_0,
        "person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool,knot": ifx.bk00128_person_planunit_v0_0_0,
        "moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain,knot": ifx.bk00129_personunit_v0_0_0,
        "moment_rope,person_name,plan_rope,healer_name,problem_bool": ifx.bk00136_problem_healer_v0_0_0,
        "otx_title,inx_title,otx_knot,inx_knot,unknown_str": ifx.bk00142_translate_title_v0_0_0,
        "otx_name,inx_name,otx_knot,inx_knot,unknown_str": ifx.bk00143_translate_name_v0_0_0,
        "otx_label,inx_label,otx_knot,inx_knot,unknown_str": ifx.bk00144_translate_label_v0_0_0,
        "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str": ifx.bk00145_translate_rope_v0_0_0,
        "moment_rope,person_name,contact_name,group_title_ERASE": ifx.bk00150_delete_person_contact_membership_v0_0_0,
        "moment_rope,person_name,contact_name_ERASE": ifx.bk00151_delete_person_contactunit_v0_0_0,
        "person_name,plan_rope,awardee_title_ERASE": ifx.bk00152_delete_person_plan_awardunit_v0_0_0,
        "person_name,plan_rope,fact_context_ERASE": ifx.bk00153_delete_person_plan_factunit_v0_0_0,
        "person_name,plan_rope,labor_title_ERASE": ifx.bk00154_delete_person_plan_laborunit_v0_0_0,
        "person_name,plan_rope,healer_name_ERASE": ifx.bk00155_delete_person_plan_healerunit_v0_0_0,
        "person_name,plan_rope,reason_context,reason_state_ERASE": ifx.bk00156_delete_person_plan_reason_caseunit_v0_0_0,
        "person_name,plan_rope,reason_context_ERASE": ifx.bk00157_delete_person_plan_reasonunit_v0_0_0,
        "person_name,plan_rope_ERASE": ifx.bk00158_delete_person_planunit_v0_0_0,
        "moment_rope,person_name_ERASE": ifx.bk00159_delete_personunit_v0_0_0,
        "moment_rope,otx_time,inx_time": ifx.bk00170_nabu_time_v0_0_0,
        "moment_rope,person_name,contact_name,otx_name,inx_name": ifx.bk00171_contact_map1_v0_0_0,
        "moment_rope,person_name,contact_name,otx_title,inx_title": ifx.bk00172_group_map1_v0_0_0,
        "moment_rope,person_name,contact_name,otx_label,inx_label": ifx.bk00173_label_map1_v0_0_0,
        "moment_rope,person_name,contact_name,otx_rope,inx_rope": ifx.bk00174_rope_map1_v0_0_0,
    }


def get_brickref_from_file(brick_format_filename: str) -> dict:
    brickref_filename = get_json_filename(brick_format_filename)
    return open_json(get_brick_formats_dir(), brickref_filename)


def get_quick_bricks_column_ref() -> dict[str, set[str]]:
    brick_type_dict = {}
    for brick_format_filename in get_brick_format_filenames():
        brickref_dict = get_brickref_from_file(brick_format_filename)
        brick_type = brickref_dict.get("brick_type")
        brick_type_dict[brick_type] = set(brickref_dict.get("attributes").keys())
    return brick_type_dict


def get_brick_dimen_ref() -> dict[str, set[str]]:
    """dictionary with key=dimen and value=set of all brick_types with that dimen's data"""
    return {
        "moment_budunit": {"bk00101"},
        "moment_epoch_hour": {"bk00103"},
        "moment_epoch_month": {"bk00104"},
        "moment_epoch_weekday": {"bk00105"},
        "moment_paybook": {"bk00102"},
        "moment_timeoffi": {"bk00106"},
        "momentunit": {
            "bk00001",
            "bk00002",
            "bk00005",
            "bk00007",
            "bk00100",
            "bk00101",
            "bk00102",
            "bk00103",
            "bk00104",
            "bk00105",
            "bk00106",
            "bk00112",
            "bk00119",
            "bk00120",
            "bk00121",
            "bk00129",
            "bk00136",
            "bk00150",
            "bk00151",
            "bk00159",
            "bk00170",
            "bk00171",
            "bk00172",
            "bk00173",
            "bk00174",
        },
        "nabu_timenum": {"bk00170"},
        "person_contact_membership": {"bk00112", "bk00120", "bk00150"},
        "person_contactunit": {
            "bk00001",
            "bk00102",
            "bk00112",
            "bk00120",
            "bk00121",
            "bk00150",
            "bk00151",
            "bk00171",
            "bk00172",
            "bk00173",
            "bk00174",
        },
        "person_plan_awardunit": {"bk00122", "bk00152"},
        "person_plan_factunit": {"bk00007", "bk00123", "bk00153"},
        "person_plan_healerunit": {"bk00125", "bk00136", "bk00155"},
        "person_plan_laborunit": {"bk00124", "bk00154"},
        "person_plan_reason_caseunit": {"bk00005", "bk00126", "bk00156"},
        "person_plan_reasonunit": {
            "bk00005",
            "bk00126",
            "bk00127",
            "bk00156",
            "bk00157",
        },
        "person_planunit": {
            "bk00002",
            "bk00005",
            "bk00007",
            "bk00119",
            "bk00122",
            "bk00123",
            "bk00124",
            "bk00125",
            "bk00126",
            "bk00127",
            "bk00128",
            "bk00136",
            "bk00152",
            "bk00153",
            "bk00154",
            "bk00155",
            "bk00156",
            "bk00157",
            "bk00158",
        },
        "personunit": {
            "bk00001",
            "bk00002",
            "bk00005",
            "bk00007",
            "bk00101",
            "bk00102",
            "bk00112",
            "bk00119",
            "bk00120",
            "bk00121",
            "bk00129",
            "bk00136",
            "bk00150",
            "bk00151",
            "bk00159",
            "bk00171",
            "bk00172",
            "bk00173",
            "bk00174",
        },
        "translate_label": {"bk00144", "bk00173"},
        "translate_name": {"bk00143", "bk00171"},
        "translate_rope": {"bk00145", "bk00174"},
        "translate_title": {"bk00142", "bk00172"},
    }


def get_dimens_with_brick_element(x_arg: str) -> set[str]:
    x_set = set()
    for x_dimen, dimen_dict in get_brick_config_dict().items():
        dimen_args = set(dimen_dict.get("jkeys"))
        dimen_args.update(dimen_dict.get("jvalues"))
        if x_arg in dimen_args:
            x_set.add(x_dimen)
    return x_set


def get_dimen_minimum_put_brick_names() -> dict[str, str]:
    """Returns all dimens and the brick format with only the args for that dimen."""
    ifx = BrickFormatsEnum
    return {
        "moment_budunit": ifx.bk00101_moment_budunit_v0_0_0,
        "moment_epoch_hour": ifx.bk00103_moment_epoch_hour_v0_0_0,
        "moment_epoch_month": ifx.bk00104_moment_epoch_month_v0_0_0,
        "moment_epoch_weekday": ifx.bk00105_moment_epoch_weekday_v0_0_0,
        "moment_paybook": ifx.bk00102_moment_paybook_v0_0_0,
        "moment_timeoffi": ifx.bk00106_moment_timeoffi_v0_0_0,
        "momentunit": ifx.bk00100_momentunit_v0_0_0,
        "nabu_timenum": ifx.bk00170_nabu_time_v0_0_0,
        "person_contact_membership": ifx.bk00120_person_contact_membership_v0_0_0,
        "person_contactunit": ifx.bk00121_person_contactunit_v0_0_0,
        "person_plan_awardunit": ifx.bk00122_person_plan_awardunit_v0_0_0,
        "person_plan_factunit": ifx.bk00123_person_plan_factunit_v0_0_0,
        "person_plan_healerunit": ifx.bk00125_person_plan_healerunit_v0_0_0,
        "person_plan_laborunit": ifx.bk00124_person_plan_laborunit_v0_0_0,
        "person_plan_reason_caseunit": ifx.bk00126_person_plan_reason_caseunit_v0_0_0,
        "person_plan_reasonunit": ifx.bk00127_person_plan_reasonunit_v0_0_0,
        "person_planunit": ifx.bk00128_person_planunit_v0_0_0,
        "personunit": ifx.bk00129_personunit_v0_0_0,
        "translate_label": ifx.bk00144_translate_label_v0_0_0,
        "translate_name": ifx.bk00143_translate_name_v0_0_0,
        "translate_title": ifx.bk00142_translate_title_v0_0_0,
        "translate_rope": ifx.bk00145_translate_rope_v0_0_0,
    }


def get_dimen_minimum_del_brick_names() -> dict[str, str]:
    """Returns all dimens and the brick format with only the args for that dimen."""
    ifx = BrickFormatsEnum
    return {
        "person_contact_membership": ifx.bk00150_delete_person_contact_membership_v0_0_0,
        "person_contactunit": ifx.bk00151_delete_person_contactunit_v0_0_0,
        "person_plan_awardunit": ifx.bk00152_delete_person_plan_awardunit_v0_0_0,
        "person_plan_factunit": ifx.bk00153_delete_person_plan_factunit_v0_0_0,
        "person_plan_healerunit": ifx.bk00155_delete_person_plan_healerunit_v0_0_0,
        "person_plan_laborunit": ifx.bk00154_delete_person_plan_laborunit_v0_0_0,
        "person_plan_reason_caseunit": ifx.bk00156_delete_person_plan_reason_caseunit_v0_0_0,
        "person_plan_reasonunit": ifx.bk00157_delete_person_plan_reasonunit_v0_0_0,
        "person_planunit": ifx.bk00158_delete_person_planunit_v0_0_0,
        "personunit": ifx.bk00159_delete_personunit_v0_0_0,
    }
