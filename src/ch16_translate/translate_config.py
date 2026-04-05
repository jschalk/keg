from os import getcwd as os_getcwd
from src.ch00_py.dict_toolbox import get_from_nested_dict
from src.ch00_py.file_toolbox import create_path, open_json
from src.ch08_person_atom.atom_config import get_all_person_dimen_delete_keys


def translate_config_path() -> str:
    "Returns path: c16_translate/translate_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_translate")
    return create_path(chapter_dir, "translate_config.json")


def get_translate_filename() -> str:
    return "translate.json"


def get_translate_config_dict() -> dict:
    return open_json(translate_config_path())


def get_translate_dimens() -> set[str]:
    return set(get_translate_config_dict().keys())


def default_unknown_str() -> str:
    return "UNKNOWN"


def default_unknown_str_if_None(unknown_str: any = None) -> str:
    if unknown_str != unknown_str:
        unknown_str = None
    if unknown_str is None:
        unknown_str = default_unknown_str()
    return unknown_str


def get_translate_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_translate_config_dict(), jkeys_key_list)


def get_translate_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_translate_config_dict(), jvalues_key_list)


def get_translate_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_translate_config_jkeys(x_dimen)
    args_dict.update(get_translate_config_jvalues(x_dimen))
    return args_dict


def get_translate_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for translate_dimen in get_translate_config_dict().keys():
        args_set = set(get_translate_config_args(translate_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {translate_dimen}
            else:
                x_dimen_set = x_dict.get(x_arg)
                x_dimen_set.add(translate_dimen)
                x_dict[x_arg] = x_dimen_set
    return x_dict


def get_translate_args_class_types() -> dict[str, str]:
    return {
        "active_requisite": "bool",
        "addin": "float",
        "amount": "float",
        "awardee_title": "TitleTerm",
        "begin": "float",
        "person_name": "NameTerm",
        "bud_time": "TimeNum",
        "c400_number": "int",
        "celldepth": "int",
        "close": "float",
        "credor_respect": "float",
        "cumulative_day": "int",
        "cumulative_minute": "int",
        "debtor_respect": "float",
        "denom": "int",
        "epoch_label": "LabelTerm",
        "spark_face": "NameTerm",
        "fact_context": "RopeTerm",
        "fact_state": "RopeTerm",
        "fact_upper": "FactNum",
        "fact_lower": "FactNum",
        "fund_grain": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_cred_lumen": "float",
        "group_debt_lumen": "float",
        "group_title": "TitleTerm",
        "healer_name": "NameTerm",
        "hour_label": "LabelTerm",
        "job_listen_rotations": "int",
        "knot": "str",
        "mana_grain": "float",
        "max_tree_traverse": "int",
        "moment_rope": "RopeTerm",
        "month_label": "LabelTerm",
        "monthday_index": "int",
        "morph": "bool",
        "numor": "int",
        "offi_time": "TimeNum",
        "quota": "int",
        "labor_title": "TitleTerm",
        "plan_rope": "RopeTerm",
        "pledge": "bool",
        "problem_bool": "bool",
        "reason_context": "RopeTerm",
        "reason_divisor": "int",
        "reason_lower": "ReasonNum",
        "reason_upper": "ReasonNum",
        "reason_state": "RopeTerm",
        "star": "int",
        "respect_grain": "float",
        "solo": "int",
        "stop_want": "float",
        "take_force": "float",
        "tran_time": "TimeNum",
        "contact_name": "NameTerm",
        "contact_cred_lumen": "float",
        "contact_debt_lumen": "float",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_translates_column_ref() -> dict[str, set[str]]:
    """for each translate_config dimen contains the associated columns"""
    return {
        "translate_title": {
            "inx_title",
            "otx_title",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "translate_name": {
            "inx_name",
            "otx_name",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "translate_label": {
            "inx_label",
            "otx_label",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "translate_rope": {
            "inx_rope",
            "otx_rope",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
    }


def translateable_class_types() -> set:
    return {"NameTerm", "TitleTerm", "LabelTerm", "RopeTerm"}


def get_translateable_args() -> set:
    return {
        "awardee_title",
        "person_name",
        "epoch_label",
        "spark_face",
        "fact_context",
        "fact_state",
        "group_title",
        "healer_name",
        "hour_label",
        "moment_rope",
        "month_label",
        "labor_title",
        "plan_rope",
        "reason_context",
        "reason_state",
        "contact_name",
        "weekday_label",
    }


def set_translateable_otx_inx_args(args: set) -> set:
    """Receives set of args, returns a set with all "Translateable" args replaced with "_otx" and "_inx" """
    all_translateable = get_translateable_args()
    all_translateable.update(get_all_person_dimen_delete_keys())
    transformed_args = set()
    for arg in args:
        if arg in all_translateable:
            transformed_args.add(f"{arg}_otx")
            transformed_args.add(f"{arg}_inx")
        else:
            transformed_args.add(arg)
    return transformed_args


def get_translate_nameterm_args() -> set[str]:
    return {
        "contact_name",
        "spark_face",
        "healer_name",
        "person_name",
    }


def get_translate_titleterm_args() -> set[str]:
    return {
        "awardee_title",
        "group_title",
        "labor_title",
    }


def get_translate_labelterm_args() -> set[str]:
    return {
        "hour_label",
        "month_label",
        "epoch_label",
        "weekday_label",
    }


def get_translate_ropeterm_args() -> set[str]:
    return {
        "moment_rope",
        "fact_state",
        "fact_context",
        "plan_rope",
        "reason_state",
        "reason_context",
    }


def get_translate_timenum_args() -> set[str]:
    return {"bud_time", "offi_time", "tran_time"}
