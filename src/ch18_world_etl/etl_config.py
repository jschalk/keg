from copy import copy as copy_copy
from os import getcwd as os_getcwd
from src.ch00_py.db_toolbox import get_create_table_sqlstr
from src.ch00_py.dict_toolbox import get_empty_set_if_None, get_from_nested_dict
from src.ch00_py.file_toolbox import create_path, open_json
from src.ch08_person_atom.atom_config import get_delete_key_name
from src.ch15_nabu.nabu_config import (
    get_context_nabuable_args,
    set_nabuable_otx_inx_args,
)
from src.ch16_translate.translate_config import set_translateable_otx_inx_args
from src.ch17_idea.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)

ALL_DIMEN_ABBV7 = {
    "MMTPAYY",
    "MMTBUDD",
    "MMTHOUR",
    "MMTMONT",
    "MMTWEEK",
    "MMTOFFI",
    "MMTUNIT",
    "PRNMEMB",
    "PRNPTNR",
    "PRNAWAR",
    "PRNFACT",
    "PRNHEAL",
    "PRNCASE",
    "PRNREAS",
    "PRNLABO",
    "PRNPLAN",
    "PRNUNIT",
    "NABTIME",
    "TRLTITL",
    "TRLNAME",
    "TRLROPE",
    "TRLLABE",
    "TRLCORE",
}
ALL_DIMEN_ABBV2 = {
    "MP",
    "MB",
    "MH",
    "MM",
    "MW",
    "MO",
    "MU",
    "PM",
    "PT",
    "PA",
    "PF",
    "PH",
    "PC",
    "PR",
    "PL",
    "PP",
    "PU",
    "NT",
    "TT",
    "TN",
    "TR",
    "TL",
    "TC",
}


def get_dimen_abbv7(dimen: str) -> str:
    return {
        "moment_paybook": "MMTPAYY",
        "moment_budunit": "MMTBUDD",
        "moment_epoch_hour": "MMTHOUR",
        "moment_epoch_month": "MMTMONT",
        "moment_epoch_weekday": "MMTWEEK",
        "moment_timeoffi": "MMTOFFI",
        "momentunit": "MMTUNIT",
        "person_partner_membership": "PRNMEMB",
        "person_partnerunit": "PRNPTNR",
        "person_plan_awardunit": "PRNAWAR",
        "person_plan_factunit": "PRNFACT",
        "person_plan_healerunit": "PRNHEAL",
        "person_plan_reason_caseunit": "PRNCASE",
        "person_plan_reasonunit": "PRNREAS",
        "person_plan_partyunit": "PRNLABO",
        "person_planunit": "PRNPLAN",
        "personunit": "PRNUNIT",
        "nabu_timenum": "NABTIME",
        "translate_title": "TRLTITL",
        "translate_name": "TRLNAME",
        "translate_rope": "TRLROPE",
        "translate_label": "TRLLABE",
        "translate_core": "TRLCORE",
    }.get(dimen)


def get_dimen_abbv2(dimen: str) -> str:
    return {
        "moment_paybook": "MP",
        "moment_budunit": "MB",
        "moment_epoch_hour": "MH",
        "moment_epoch_month": "MM",
        "moment_epoch_weekday": "MW",
        "moment_timeoffi": "MO",
        "momentunit": "MU",
        "person_partner_membership": "PM",
        "person_partnerunit": "PT",
        "person_plan_awardunit": "PA",
        "person_plan_factunit": "PF",
        "person_plan_healerunit": "PH",
        "person_plan_reason_caseunit": "PC",
        "person_plan_reasonunit": "PR",
        "person_plan_partyunit": "PL",
        "person_planunit": "PP",
        "personunit": "PU",
        "nabu_timenum": "NT",
        "translate_title": "TT",
        "translate_name": "TN",
        "translate_rope": "TR",
        "translate_label": "TL",
        "translate_core": "TC",
    }.get(dimen)


class prime_tablenameException(Exception):
    pass


def create_prime_tablename(
    idea_dimen_or_abbv7: str, stage0: str, stage1: str, put_del: str = None
) -> str:
    """
    stage0 must be one: 's', 'h', 'job'
    stage1 must be one: 'raw', 'agg', 'vld'
    """

    abbv_references = {
        "MMTPAYY": "moment_paybook",
        "MMTBUDD": "moment_budunit",
        "MMTHOUR": "moment_epoch_hour",
        "MMTMONT": "moment_epoch_month",
        "MMTWEEK": "moment_epoch_weekday",
        "MMTOFFI": "moment_timeoffi",
        "MMTUNIT": "momentunit",
        "PRNMEMB": "person_partner_membership",
        "PRNPTNR": "person_partnerunit",
        "PRNAWAR": "person_plan_awardunit",
        "PRNFACT": "person_plan_factunit",
        "PRNGROU": "person_groupunit",
        "PRNHEAL": "person_plan_healerunit",
        "PRNCASE": "person_plan_reason_caseunit",
        "PRNREAS": "person_plan_reasonunit",
        "PRNLABO": "person_plan_partyunit",
        "PRNPLAN": "person_planunit",
        "PRNUNIT": "personunit",
        "NABTIME": "nabu_timenum",
        "TRLTITL": "translate_title",
        "TRLNAME": "translate_name",
        "TRLROPE": "translate_rope",
        "TRLLABE": "translate_label",
        "TRLCORE": "translate_core",
    }
    tablename = idea_dimen_or_abbv7
    if abbv_references.get(idea_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(idea_dimen_or_abbv7.upper())
    if stage0 in {"s", "h", "job"}:
        tablename = f"{tablename}_{stage0}"
    if stage1 is None:
        return tablename
    if stage1 not in {"raw", "agg", "vld"}:
        raise prime_tablenameException(f"'{stage1}' is not a valid stage")

    return f"{tablename}_{put_del}_{stage1}" if put_del else f"{tablename}_{stage1}"


def etl_idea_category_config_path() -> str:
    "Returns path: ch18_world_etl/etl_idea_category_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch18_world_etl")
    return create_path(chapter_dir, "etl_idea_category_config.json")


def etl_idea_category_config_dict() -> dict:
    """Config data for etl dimenensions (translate, moment, person...) including required columns per stage"""
    return open_json(etl_idea_category_config_path())


def get_etl_category_stages_dict() -> dict:
    return {
        "person_h_agg_put": {
            "idea_category": "person",
            "stage0": "h",
            "stage1": "agg",
            "put_del": "put",
        },
        "person_h_agg_del": {
            "idea_category": "person",
            "stage0": "h",
            "stage1": "agg",
            "put_del": "del",
        },
        "person_h_raw_put": {
            "idea_category": "person",
            "stage0": "h",
            "stage1": "raw",
            "put_del": "put",
        },
        "person_h_raw_del": {
            "idea_category": "person",
            "stage0": "h",
            "stage1": "raw",
            "put_del": "del",
        },
        "person_h_vld_put": {
            "idea_category": "person",
            "stage0": "h",
            "stage1": "vld",
            "put_del": "put",
        },
        "person_h_vld_del": {
            "idea_category": "person",
            "stage0": "h",
            "stage1": "vld",
            "put_del": "del",
        },
        "person_s_agg_put": {
            "idea_category": "person",
            "stage0": "s",
            "stage1": "agg",
            "put_del": "put",
        },
        "person_s_agg_del": {
            "idea_category": "person",
            "stage0": "s",
            "stage1": "agg",
            "put_del": "del",
        },
        "person_s_raw_put": {
            "idea_category": "person",
            "stage0": "s",
            "stage1": "raw",
            "put_del": "put",
        },
        "person_s_raw_del": {
            "idea_category": "person",
            "stage0": "s",
            "stage1": "raw",
            "put_del": "del",
        },
        "person_s_vld_put": {
            "idea_category": "person",
            "stage0": "s",
            "stage1": "vld",
            "put_del": "put",
        },
        "person_s_vld_del": {
            "idea_category": "person",
            "stage0": "s",
            "stage1": "vld",
            "put_del": "del",
        },
        "moment_h_agg": {"idea_category": "moment", "stage0": "h", "stage1": "agg"},
        "moment_h_raw": {"idea_category": "moment", "stage0": "h", "stage1": "raw"},
        "moment_h_vld": {"idea_category": "moment", "stage0": "h", "stage1": "vld"},
        "moment_s_agg": {"idea_category": "moment", "stage0": "s", "stage1": "agg"},
        "moment_s_raw": {"idea_category": "moment", "stage0": "s", "stage1": "raw"},
        "moment_s_vld": {"idea_category": "moment", "stage0": "s", "stage1": "vld"},
        "nabu_h_agg": {"idea_category": "nabu", "stage0": "h", "stage1": "agg"},
        "nabu_h_raw": {"idea_category": "nabu", "stage0": "h", "stage1": "raw"},
        "nabu_s_agg": {"idea_category": "nabu", "stage0": "s", "stage1": "agg"},
        "nabu_s_raw": {"idea_category": "nabu", "stage0": "s", "stage1": "raw"},
        "nabu_s_vld": {"idea_category": "nabu", "stage0": "s", "stage1": "vld"},
        "translate_s_agg": {
            "idea_category": "translate",
            "stage0": "s",
            "stage1": "agg",
        },
        "translate_s_raw": {
            "idea_category": "translate",
            "stage0": "s",
            "stage1": "raw",
        },
        "translate_s_vld": {
            "idea_category": "translate",
            "stage0": "s",
            "stage1": "vld",
        },
        "translate_core_s_agg": {
            "idea_category": "translate_core",
            "stage0": "s",
            "stage1": "agg",
        },
        "translate_core_s_raw": {
            "idea_category": "translate_core",
            "stage0": "s",
            "stage1": "raw",
        },
        "translate_core_s_vld": {
            "idea_category": "translate_core",
            "stage0": "s",
            "stage1": "vld",
        },
    }


def remove_otx_columns(columns_set: set) -> set:
    return {x_col for x_col in columns_set if x_col[-3:] != "otx"}


def remove_inx_columns(columns_set: set) -> set:
    return {x_col for x_col in columns_set if x_col[-3:] != "inx"}


def get_temp_staging_columns() -> set:
    return {
        "context_plan_close",
        "context_plan_denom",
        "context_plan_morph",
        "inx_epoch_diff",
    }


def remove_staging_columns(columns_set: set) -> set:
    staging_columns = get_temp_staging_columns()
    return {x_col for x_col in columns_set if x_col not in staging_columns}


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    if x_dimen == "translate_core":
        translate_core_dict = etl_idea_category_config_dict().get("translate_core")
        return set(translate_core_dict.get("override_columns"))
    x_config = get_idea_config_dict().get(x_dimen)
    columns = set(x_config.get("jkeys").keys())
    columns.update(set(x_config.get("jvalues").keys()))
    return columns


def get_del_dimen_columns_set(x_dimen: str) -> set[str]:
    x_config = get_idea_config_dict().get(x_dimen)
    columns_set = set(x_config.get("jkeys").keys())
    columns_list = get_default_sorted_list(columns_set)
    columns_list[-1] = get_delete_key_name(columns_list[-1])
    return set(columns_list)


def get_prime_columns(
    x_dimen: str, table_keylist: list[str], etl_idea_category_config: dict
) -> set[str]:
    """Given dimen and config_keylist (ala ["s", "agg", put_del] )
    Return list of columns for that prime table"""
    if not table_keylist or not etl_idea_category_config:
        return set()
    columns = get_all_dimen_columns_set(x_dimen)
    if table_keylist[-1] == "del":
        columns = get_del_dimen_columns_set(x_dimen)

    if x_dimen == "translate_core":
        idea_category = "translate_core"
    elif x_dimen.find("translate") == 0:
        idea_category = "translate"
    elif x_dimen.find("nabu") == 0:
        idea_category = "nabu"
    elif x_dimen.find("moment") == 0:
        idea_category = "moment"
    elif x_dimen.find("person") == 0:
        idea_category = "person"
    config_keylist = [idea_category, "stages", *table_keylist]

    otx_keylist = copy_copy(config_keylist)
    otx_keylist.append("set_translateable_otx_inx_args")
    if get_from_nested_dict(etl_idea_category_config, otx_keylist, True):
        columns = set_translateable_otx_inx_args(columns)

    nabuable_keylist = copy_copy(config_keylist)
    nabuable_keylist.append("set_nabuable_otx_inx_args")
    if get_from_nested_dict(etl_idea_category_config, nabuable_keylist, True):
        context_nabuable_args = get_context_nabuable_args()

        if any(c_arg in columns for c_arg in context_nabuable_args):
            columns.update(get_temp_staging_columns())

        columns = set_nabuable_otx_inx_args(columns)

    update_keylist = copy_copy(config_keylist)
    update_keylist.append("add")
    update_cols = get_from_nested_dict(etl_idea_category_config, update_keylist, True)
    columns.update(get_empty_set_if_None(update_cols))

    update_keylist = copy_copy(config_keylist)
    update_keylist.append("remove")
    remove_cols = get_from_nested_dict(etl_idea_category_config, update_keylist, True)
    columns -= set(get_empty_set_if_None(remove_cols))

    return columns


def create_prime_table_sqlstr(
    x_dimen: str, stage0: str, stage1: str, put_del: str = None
) -> str:
    """Given dimen and stages return the Create Table sqlstr
    stage0 must be one: 's', 'h', 'job'
    stage1 must be one: 'raw', 'agg', 'vld'
    """
    tablename = create_prime_tablename(x_dimen, stage0, stage1, put_del)
    table_keylist = [stage0, stage1, put_del] if put_del else [stage0, stage1]
    etl_idea_category_config = etl_idea_category_config_dict()
    columns_set = get_prime_columns(x_dimen, table_keylist, etl_idea_category_config)
    columns_list = get_default_sorted_list(columns_set)
    return get_create_table_sqlstr(tablename, columns_list, get_idea_sqlite_types())
