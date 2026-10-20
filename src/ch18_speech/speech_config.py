from ch00_py.file_toolbox import create_path, open_json


def get_speech_filename():
    return "speech.json"


def speech_config_path():
    "Returns path: c18_speech/speech_config.json"
    return create_path("src", "ch18_speech", "speech_config.json")


def get_speech_config_dict() -> dict:
    return open_json(speech_config_path())


def get_speech_column_ref() -> dict[str, set[str]]:
    """for each speech_config dimen contains the associated columns"""
    return {
        "speech_title": {
            "iux_title",
            "aux_title",
            "iux_knot",
            "aux_knot",
        },
        "speech_name": {
            "iux_name",
            "aux_name",
            "iux_knot",
            "aux_knot",
        },
        "speech_label": {
            "iux_label",
            "aux_label",
            "iux_knot",
            "aux_knot",
        },
        "speech_rope": {
            "iux_rope",
            "aux_rope",
            "iux_knot",
            "aux_knot",
        },
    }


def get_speech_args_obj_types() -> dict[str, str]:
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
        "group_cred_mass": "float",
        "group_debt_mass": "float",
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
        "poynt": "int",
        "respect_grain": "float",
        "solo": "int",
        "stop_want": "float",
        "take_force": "float",
        "tran_time": "TimeNum",
        "contact_name": "NameTerm",
        "contact_cred_mass": "float",
        "contact_debt_mass": "float",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def speechable_obj_types() -> set:
    return {"NameTerm", "TitleTerm", "LabelTerm", "RopeTerm"}


def get_speechable_args() -> set:
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
