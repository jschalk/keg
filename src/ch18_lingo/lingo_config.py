from ch00_py.file_toolbox import create_path, open_json


def get_lingo_filename():
    return "lingo.json"


def lingo_config_path():
    "Returns path: c18_lingo/lingo_config.json"
    return create_path("src", "ch18_lingo", "lingo_config.json")


def get_lingo_config_dict() -> dict:
    return open_json(lingo_config_path())


def get_lingo_column_ref() -> dict[str, set[str]]:
    """for each lingo_config dimen contains the associated columns"""
    return {
        "lingo_title": {
            "iux_title",
            "aux_title",
            "iux_knot",
            "aux_knot",
        },
        "lingo_name": {
            "iux_name",
            "aux_name",
            "iux_knot",
            "aux_knot",
        },
        "lingo_label": {
            "iux_label",
            "aux_label",
            "iux_knot",
            "aux_knot",
        },
        "lingo_rope": {
            "iux_rope",
            "aux_rope",
            "iux_knot",
            "aux_knot",
        },
    }
