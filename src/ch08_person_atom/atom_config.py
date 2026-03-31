from os import getcwd as os_getcwd
from src.ch00_py.dict_toolbox import get_from_nested_dict
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch08_person_atom._ref.ch08_semantic_types import CRUD_command


def atom_config_path() -> str:
    "Returns Path: ch08_person_atom/atom_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch08_person_atom")
    return create_path(chapter_dir, "atom_config.json")


def get_atom_config_dict() -> dict:
    return open_json(atom_config_path())


def get_atom_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_atom_config_dict(), jkeys_key_list)


def get_atom_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_atom_config_dict(), jvalues_key_list)


def get_atom_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_atom_config_jkeys(x_dimen)
    args_dict.update(get_atom_config_jvalues(x_dimen))
    return args_dict


def get_atom_args_dimen_mapping() -> dict[str, set[str]]:
    x_dict = {}
    for atom_dimen in get_atom_config_dict().keys():
        args_set = set(get_atom_config_args(atom_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {atom_dimen}
            else:
                x_dimen_set = x_dict.get(x_arg)
                x_dimen_set.add(atom_dimen)
                x_dict[x_arg] = x_dimen_set
    return x_dict


def get_allowed_class_types() -> set[str]:
    return {
        "NameTerm",
        "bool",
        "float",
        "TitleTerm",
        "int",
        "LabelTerm",
        "RopeTerm",
        "KnotTerm",
        "ReasonNum",
        "FactNum",
    }


def get_atom_args_class_types() -> dict[str, str]:
    return {
        "partner_name": "NameTerm",
        "addin": "float",
        "awardee_title": "TitleTerm",
        "reason_context": "RopeTerm",
        "active_requisite": "bool",
        "begin": "float",
        "close": "float",
        "partner_cred_lumen": "float",
        "group_cred_lumen": "float",
        "credor_respect": "float",
        "partner_debt_lumen": "float",
        "group_debt_lumen": "float",
        "debtor_respect": "float",
        "denom": "int",
        "reason_divisor": "int",
        "fact_context": "RopeTerm",
        "fact_upper": "FactNum",
        "fact_lower": "FactNum",
        "fund_grain": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_title": "TitleTerm",
        "healer_name": "NameTerm",
        "max_tree_traverse": "int",
        "morph": "bool",
        "reason_state": "RopeTerm",
        "reason_upper": "ReasonNum",
        "numor": "int",
        "reason_lower": "ReasonNum",
        "mana_grain": "float",
        "fact_state": "RopeTerm",
        "pledge": "bool",
        "problem_bool": "bool",
        "respect_grain": "float",
        "plan_rope": "RopeTerm",
        "star": "int",
        "stop_want": "float",
        "solo": "int",
        "take_force": "float",
        "labor_title": "TitleTerm",
    }


def get_sorted_jkey_keys(atom_dimen: str) -> list[str]:
    atom_config = get_atom_config_dict()
    atom_dimen_config = atom_config.get(atom_dimen)
    atom_jkeys_config = atom_dimen_config.get("jkeys")
    if len(atom_jkeys_config) == 1:
        return list(atom_jkeys_config.keys())
    nesting_order_dict = {
        required_key: required_dict.get("nesting_order")
        for required_key, required_dict in atom_jkeys_config.items()
    }
    sorted_tuples = sorted(nesting_order_dict.items(), key=lambda x: x[1])
    return [x_tuple[0] for x_tuple in sorted_tuples]


def add_to_atom_table_columns(x_dict, atom_dimen, crud, arg_key, arg_value):
    x_dict[f"{atom_dimen}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_flattened_atom_table_build() -> dict[str, any]:
    atom_table_columns = {}
    atom_config = get_atom_config_dict()
    for atom_dimen, dimen_dict in atom_config.items():
        catergory_insert = dimen_dict.get("INSERT")
        catergory_update = dimen_dict.get("UPDATE")
        catergory_delete = dimen_dict.get("DELETE")
        if catergory_insert is not None:
            jkeys = dimen_dict.get("jkeys")
            jvalues = dimen_dict.get("jvalues")
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "INSERT",
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "INSERT",
                    jvalue,
                    x_value,
                )
        if catergory_update is not None:
            jkeys = dimen_dict.get("jkeys")
            jvalues = dimen_dict.get("jvalues")
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "UPDATE",
                    jkey,
                    x_value,
                )
            for jvalue, x_value in jvalues.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "UPDATE",
                    jvalue,
                    x_value,
                )
        if catergory_delete is not None:
            jkeys = dimen_dict.get("jkeys")
            for jkey, x_value in jkeys.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_dimen,
                    "DELETE",
                    jkey,
                    x_value,
                )
    return atom_table_columns


def get_normalized_person_table_build() -> dict[str : dict[str, any]]:
    normal_tables_dict = {}
    atom_config = get_atom_config_dict()
    for x_dimen, dimen_dict in atom_config.items():
        normal_tables_dict[x_dimen] = {}
        normal_table_dict = normal_tables_dict.get(x_dimen)

        normal_table_dict["columns"] = {}
        normal_columns_dict = normal_table_dict.get("columns")
        normal_columns_dict["plan_uid"] = {
            "sqlite_datatype": "INTEGER",
            "nullable": False,
            "primary_key": True,
        }
        jkeys = dimen_dict.get("jkeys")
        jvalues = dimen_dict.get("jvalues")
        if jkeys is not None:
            for jkey, x_value in jkeys.items():
                normal_columns_dict[jkey] = {
                    "sqlite_datatype": x_value.get("sqlite_datatype"),
                    "nullable": False,
                }

        if jvalues is not None:
            for jvalue, x_value in jvalues.items():
                normal_columns_dict[jvalue] = {
                    "sqlite_datatype": x_value.get("sqlite_datatype"),
                    "nullable": True,
                }

        normal_table_dict["normal_specs"] = {}
        normal_specs_dict = normal_table_dict.get("normal_specs")
        config_normal_dict = dimen_dict.get("normal_specs")
        table_name = config_normal_dict.get("normal_table_name")
        normal_specs_dict["normal_table_name"] = table_name

    return normal_tables_dict


def save_atom_config_file(atom_config_dict):
    save_json(atom_config_path(), None, atom_config_dict)


def get_person_dimens() -> set:
    return {
        "personunit",
        "person_partnerunit",
        "person_partner_membership",
        "person_planunit",
        "person_plan_awardunit",
        "person_plan_reasonunit",
        "person_plan_reason_caseunit",
        "person_plan_laborunit",
        "person_plan_healerunit",
        "person_plan_factunit",
    }


def get_all_person_dimen_keys() -> set:
    return {
        "partner_name",
        "awardee_title",
        "reason_context",
        "fact_context",
        "group_title",
        "healer_name",
        "reason_state",
        "person_name",
        "plan_rope",
        "labor_title",
    }


def get_delete_key_name(key: str) -> str:
    return f"{key}_ERASE" if key else None


def get_all_person_dimen_delete_keys() -> set:
    return {
        "partner_name_ERASE",
        "awardee_title_ERASE",
        "reason_context_ERASE",
        "fact_context_ERASE",
        "group_title_ERASE",
        "healer_name_ERASE",
        "reason_state_ERASE",
        "person_name_ERASE",
        "plan_rope_ERASE",
        "labor_title_ERASE",
    }


def is_person_dimen(dimen_str: str) -> bool:
    return dimen_str in get_person_dimens()


def get_atom_order(crud_str: str, dimen: str) -> int:
    return get_from_nested_dict(get_atom_config_dict(), [dimen, crud_str, "atom_order"])


def get_normal_table_name(dimen: str) -> str:
    nested_list = [dimen, "normal_specs", "normal_table_name"]
    return get_from_nested_dict(get_atom_config_dict(), nested_list)


def set_mog(
    crud_str: str,
    dimen: str,
    atom_order_int: int,
) -> int:
    atom_config_dict = get_atom_config_dict()
    dimen_dict = atom_config_dict.get(dimen)
    crud_dict = dimen_dict.get(crud_str)
    crud_dict["atom_order"] = atom_order_int
    save_atom_config_file(atom_config_dict)


def get_dimen_from_dict(x_row_dict: dict) -> str:
    x_get_person_dimens = get_person_dimens()
    for x_columnname in x_row_dict:
        for x_dimen in x_get_person_dimens:
            if x_columnname.find(x_dimen) == 0:
                dimen_len = len(x_dimen)
                return x_dimen, x_columnname[dimen_len + 1 : dimen_len + 7]
