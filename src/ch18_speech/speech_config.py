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
