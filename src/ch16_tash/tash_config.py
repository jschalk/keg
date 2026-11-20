from ch00_py.file_toolbox import create_path, open_json


# TODO consider Tash converion for FundNum
def create_tash_config_path():
    "Returns path: c16_tash/tash_config.json"
    return create_path("src", "ch16_tash", "tash_config.json")


def get_tash_config_dict():
    return open_json(create_tash_config_path())


def get_tash_dimens() -> set:
    return {"tash_timenum"}


def get_tash_args() -> set:
    return {"otx_time", "inx_time", "moment_rope"}


def get_tashable_args() -> set:
    return {
        "bud_time",
        "fact_lower",
        "fact_upper",
        "offi_time",
        "reason_lower",
        "reason_upper",
        "tran_time",
    }


def get_context_tashable_args() -> set:
    return {
        "fact_lower",
        "fact_upper",
        "reason_lower",
        "reason_upper",
    }


def set_tashable_otx_inx_args(args: set) -> set:
    """Receives set of args, returns a set with all "Tashable" args replaced with "_otx" and "_inx" """
    all_tashable = get_tashable_args()
    transformed_args = set()
    for arg in args:
        if arg in all_tashable:
            transformed_args.add(f"{arg}_otx")
            transformed_args.add(f"{arg}_inx")
        else:
            transformed_args.add(arg)
    return transformed_args
