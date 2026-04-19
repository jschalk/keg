from ch00_py.dict_toolbox import get_from_nested_dict
from ch00_py.file_toolbox import create_path, open_json
from os import getcwd as os_getcwd


def nabu_config_path():
    "Returns path: c15_nabu/nabu_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch15_nabu")
    return create_path(chapter_dir, "nabu_config.json")


def get_nabu_config_dict():
    return open_json(nabu_config_path())


def get_nabu_dimens() -> set:
    return {"nabu_timenum"}


def get_nabu_args() -> set:
    return {"otx_time", "inx_time", "moment_rope"}


def get_nabuable_args() -> set:
    return {
        "bud_time",
        "fact_lower",
        "fact_upper",
        "offi_time",
        "reason_lower",
        "reason_upper",
        "tran_time",
    }


def get_context_nabuable_args() -> set:
    return {
        "fact_lower",
        "fact_upper",
        "reason_lower",
        "reason_upper",
    }


def set_nabuable_otx_inx_args(args: set) -> set:
    """Receives set of args, returns a set with all "Nabuable" args replaced with "_otx" and "_inx" """
    all_nabuable = get_nabuable_args()
    transformed_args = set()
    for arg in args:
        if arg in all_nabuable:
            transformed_args.add(f"{arg}_otx")
            transformed_args.add(f"{arg}_inx")
        else:
            transformed_args.add(arg)
    return transformed_args
