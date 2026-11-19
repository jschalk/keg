from ch00_py.file_toolbox import create_path, open_json


def get_nabu_config_filename() -> str:
    return "nabu_config.json"


def create_nabu_config_path():
    "Returns path: src\\ch17_nabu\\nabu_config.json"
    chapter_dir = create_path("src", "ch17_nabu")
    return create_path(chapter_dir, "nabu_config.json")


def get_nabu_config_dict():
    return open_json(create_nabu_config_path())


def get_nabu_dimens() -> set:
    return {"nabu_timenum"}


def get_nabu_args() -> set:
    return {"iux_time", "aux_time", "moment_rope", "song_audie"}


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


# def get_context_nabuable_args() -> set:
#     return {
#         "fact_lower",
#         "fact_upper",
#         "reason_lower",
#         "reason_upper",
#     }


# def set_nabuable_iux_aux_args(args: set) -> set:
#     """Receives set of args, returns a set with all "Nabuable" args replaced with "_iux" and "_aux" """
#     all_nabuable = get_nabuable_args()
#     transformed_args = set()
#     for arg in args:
#         if arg in all_nabuable:
#             transformed_args.add(f"{arg}_iux")
#             transformed_args.add(f"{arg}_aux")
#         else:
#             transformed_args.add(arg)
#     return transformed_args


# TODO create Nabu config file functions get_nabu_config_path/get_nabu_config_dict
# TODO create test where nabu_config has the same dimens as nabu_config so anything added to nabu is added to nabu


# def create_bud_contact_mandate_ledger_path(
#     moment_mstr_dir: str,
#     moment_lasso: LassoUnit,
#     person_name: PersonName,
#     bud_time: int,
# ) -> str:
#     """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\bud_contact_mandate_ledger.json"""
#     timenum_dir = create_bud_dir_path(
#         moment_mstr_dir, moment_lasso, person_name, bud_time
#     )
#     return create_path(timenum_dir, "bud_contact_mandate_ledger.json")
