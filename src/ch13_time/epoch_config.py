from src.ch00_py.file_toolbox import open_json
from src.ch13_time._ref.ch13_semantic_types import LabelTerm


def get_custom_epoch_config(epoch_label: LabelTerm) -> dict:
    x_dir = "src/ch13_time/epoch_configs/"
    x_filename = f"epoch_config_{epoch_label}.json"
    return open_json(x_dir, x_filename)


def get_five_config() -> dict:
    return get_custom_epoch_config("five")


def get_creg_config() -> dict:
    return get_custom_epoch_config("creg")


def get_squirt_config() -> dict:
    return get_custom_epoch_config("squirt")


def get_lizzy9_config() -> dict:
    return get_custom_epoch_config("lizzy9")
