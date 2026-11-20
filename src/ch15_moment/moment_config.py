from ch00_py.dict_toolbox import get_from_nested_dict
from ch00_py.file_toolbox import create_path, open_json
from os.path import join as os_path_join


def moment_config_path() -> str:
    "Returns Path: a15_moment_logic/moment_config.json"
    return create_path("src", "ch15_moment", "moment_config.json")


def get_moment_config_dict() -> dict:
    return open_json(moment_config_path())


def get_moment_dimens() -> set[str]:
    return {
        "momentunit",
        "moment_budunit",
        "moment_ceckbook",
        "moment_epoch_hour",
        "moment_epoch_month",
        "moment_epoch_weekday",
        "moment_timeoffi",
    }


def get_moment_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_moment_config_dict(), jkeys_key_list)


def get_moment_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_moment_config_dict(), jvalues_key_list)


def get_moment_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_moment_config_jkeys(x_dimen)
    args_dict.update(get_moment_config_jvalues(x_dimen))
    return args_dict


def get_moment_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for moment_dimen in get_moment_config_dict().keys():
        args_set = set(get_moment_config_args(moment_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = set()
            x_dimen_set = x_dict.get(x_arg)
            x_dimen_set.add(moment_dimen)
            x_dict[x_arg] = x_dimen_set
    return x_dict


def get_moment_args_obj_types() -> dict[str, str]:
    return {
        "amount": "FundNum",
        "bud_time": "TimeNum",
        "c400_number": "int",
        "celldepth": "int",
        "contact_name": "NameTerm",
        "cumulative_day": "int",
        "cumulative_minute": "int",
        "epoch_label": "LabelTerm",
        "fund_grain": "float",
        "hour_label": "LabelTerm",
        "job_listen_rotations": "int",
        "knot": "str",
        "moment_rope": "RopeTerm",
        "month_label": "LabelTerm",
        "monthday_index": "int",
        "mana_grain": "float",
        "offi_time": "TimeNum",
        "person_name": "NameTerm",
        "quota": "FundNum",
        "respect_grain": "float",
        "tran_time": "TimeNum",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_moment_args_set() -> set[str]:
    return {
        "amount",
        "bud_time",
        "c400_number",
        "celldepth",
        "contact_name",
        "cumulative_day",
        "cumulative_minute",
        "epoch_label",
        "fund_grain",
        "hour_label",
        "job_listen_rotations",
        "knot",
        "moment_rope",
        "month_label",
        "monthday_index",
        "mana_grain",
        "offi_time",
        "person_name",
        "quota",
        "respect_grain",
        "tran_time",
        "weekday_label",
        "weekday_order",
        "yr1_jan1_offset",
    }
