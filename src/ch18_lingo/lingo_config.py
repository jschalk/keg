from ch00_py.file_toolbox import create_path, open_json


def get_lingo_filename():
    return "lingo.json"


def lingo_config_path():
    "Returns path: c18_lingo/lingo_config.json"
    return create_path("src", "ch18_lingo", "lingo_config.json")


def get_lingo_config_dict() -> dict:
    return open_json(lingo_config_path())
