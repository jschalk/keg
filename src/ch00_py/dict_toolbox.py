from collections import deque
from compact_json import Formatter as compact_json_Formatter
from copy import deepcopy as copy_deepcopy
from csv import reader as csv_reader, writer as csv_writer
from enum import Enum
from io import StringIO as io_StringIO
from json import dumps as json_dumps, loads as json_loads
from re import fullmatch as re_fullmatch
from typing import Any, List, Union


def uppercase_in_str(x_str: str) -> bool:
    return any(c.isupper() for c in x_str)


def uppercase_is_first(x_str: str) -> bool:
    return x_str != "" and x_str[0].isupper()


def is_camel_case(s: str) -> bool:
    return bool(re_fullmatch(r"[A-Z][a-zA-Z0-9]*", s)) and "_" not in s


def get_empty_dict_if_None(x_dict: dict = None) -> dict:
    return {} if x_dict is None else x_dict


def get_empty_set_if_None(x_set: set = None) -> set:
    return set() if x_set is None else x_set


def get_None_if_nan(x_obj: any) -> any:
    if x_obj != x_obj:  # float("nan")
        x_obj = None
    return x_obj


def get_1_if_None(x_obj):
    x_obj = get_None_if_nan(x_obj)
    return 1 if x_obj is None else x_obj


def get_0_if_None(x_obj=None):
    x_obj = get_None_if_nan(x_obj)
    return 0 if x_obj is None else int(x_obj)


def get_empty_str_if_None(x_obj=None):
    x_obj = get_None_if_nan(x_obj)
    return "" if x_obj is None else str(x_obj)


def get_empty_list_if_None(x_obj=None):
    return [] if x_obj is None else x_obj


def get_False_if_None(x_obj=None):
    return False if x_obj is None else x_obj


def get_positive_int(x_obj: any = None):
    try:
        x_int = int(x_obj)
    except Exception:
        x_int = 0
    return max(x_int, 0)


def add_nested_dict_if_missing(x_dict: dict, x_keylist: list[any]):
    for x_key in x_keylist:
        if x_dict.get(x_key) is None:
            x_dict[x_key] = {}
        x_dict = x_dict.get(x_key)


def set_in_nested_dict(x_dict: dict, x_keylist: list[any], x_obj: any):
    z_keylist = copy_deepcopy(x_keylist)
    last_key = z_keylist.pop(-1)
    add_nested_dict_if_missing(x_dict, x_keylist=z_keylist)
    last_dict = x_dict
    for x_key in z_keylist:
        last_dict = last_dict[x_key]
    last_dict[last_key] = x_obj


class NestedValueError(Exception):
    pass


class Is2dWithUniqueKeysError(Exception):
    pass


def convert_enum_keys_to_strings(keys: List[Any]) -> List[str]:
    """
    Takes a list of keys and converts any enum objects to their string values.

    Args:
        keys: List that may contain enum objects, strings, or other types

    Returns:
        List with enum objects converted to their .value strings
    """
    result = []
    for key in keys:
        if isinstance(key, Enum):
            result.append(key.value)  # Use .value instead of str()
        else:
            result.append(key)
    return result


def get_from_nested_dict(
    x_dict: dict, x_keylist: list, if_missing_return_None: bool = False
) -> any:
    z_keylist = copy_deepcopy(x_keylist)
    z_keylist = convert_enum_keys_to_strings(z_keylist)

    if not if_missing_return_None:
        return _sub_get_from_nested_dict(x_dict, z_keylist)
    try:
        return _sub_get_from_nested_dict(x_dict, z_keylist)
    except Exception:
        return None


def change_nested_key(x_dict: dict, x_keylist: list, new_key: str):
    """
    Renames the final key in a nested dictionary.

    Args:
        d (dict): The dictionary to modify.
        key_path (list): List of keys leading to the target key to rename.
                         The last key in the list is the one to be renamed.
        new_key (str): The new name for the final key in key_path.

    Returns:
        dict: The modified dictionary.
    """
    current = x_dict
    for key in x_keylist[:-1]:
        current = current.get(key, {})

    if isinstance(current, dict):
        old_key = x_keylist[-1]
        if old_key in current:
            current[new_key] = current.pop(old_key)

    return x_dict


def _sub_get_from_nested_dict(x_dict: dict, x_keylist: list) -> any:
    last_key = x_keylist.pop(-1)
    temp_dict = x_dict
    x_count = 0
    for x_key in x_keylist:
        if temp_dict.get(x_key) is None:
            raise NestedValueError(f"'{x_key}' failed at level {x_count}.")
        x_count += 1
        temp_dict = temp_dict.get(x_key)

    if temp_dict.get(last_key) is None:
        raise NestedValueError(f"'{last_key}' failed at level {x_count}.")
    return temp_dict[last_key]


def get_all_nondictionary_objs(x_dict: dict) -> dict[str : list[any]]:
    level1_keys = x_dict.keys()
    z_dict = {}
    for level1_key in level1_keys:
        z_dict[level1_key] = []
        level1_list = z_dict.get(level1_key)
        eval_values = list(x_dict.get(level1_key).values())
        while eval_values != []:
            eval_value = eval_values.pop(0)
            if type(eval_value) == type({}):
                eval_values.extend(eval_value.values())
            else:
                level1_list.append(eval_value)
    return z_dict


def exists_in_nested_dict(x_dict: dict, x_keylist: list) -> bool:
    z_keylist = copy_deepcopy(x_keylist)
    return get_from_nested_dict(x_dict, z_keylist, True) != None


def del_in_nested_dict(x_dict: dict, x_keylist: list):
    z_keylist = copy_deepcopy(x_keylist)
    if exists_in_nested_dict(x_dict, z_keylist):
        parent_keylist = z_keylist
        del_key = parent_keylist.pop(-1)
        parent_dict = get_from_nested_dict(x_dict, parent_keylist)
        parent_dict.pop(del_key)
        while parent_dict == {} and len(parent_keylist) > 1:
            del_key = parent_keylist.pop(-1)
            parent_dict = get_from_nested_dict(x_dict, parent_keylist)
            parent_dict.pop(del_key)

        if len(parent_keylist) == 1 and x_dict.get(parent_keylist[0]) == {}:
            x_dict.pop(parent_keylist[0])


def sort_keys_case_insensitive(obj):
    if isinstance(obj, dict):
        return {
            k: sort_keys_case_insensitive(v)
            for k, v in sorted(
                obj.items(), key=lambda item: (item[0].casefold(), item[0])
            )
        }
    elif isinstance(obj, list):
        return [sort_keys_case_insensitive(v) for v in obj]
    else:
        return obj


def normalize_and_compact_json(data: dict, keys_case_insensitive: bool) -> str:
    json_str = json_dumps(data, sort_keys=True)
    if keys_case_insensitive:
        x_dict = sort_keys_case_insensitive(data)
        json_str = json_dumps(x_dict)

    normalized = json_loads(json_str)
    formatter = compact_json_Formatter()
    formatter.indent_spaces = 2
    formatter.max_inline_complexity = 10  # Can be adjusted
    return formatter.serialize(normalized)


def get_json_from_dict(x_dict: dict, keys_case_insensitive: bool = False) -> str:
    """Given serializable dict return JSON."""

    return normalize_and_compact_json(x_dict, keys_case_insensitive)


def get_dict_from_json(x_json: str) -> dict[str,]:
    return json_loads(x_json)


def extract_csv_headers(x_csv: str, delimiter: str = None) -> tuple[list[str], str]:
    x_reader = csv_reader(x_csv.splitlines(), delimiter=",")

    header_row = None
    si = io_StringIO()
    new_csv_writer = csv_writer(si, delimiter=",")
    for x_count, row in enumerate(x_reader):
        if x_count == 0:
            header_row = row
        else:
            new_csv_writer.writerow(row)
    headers_list = []
    if header_row is None:
        return headers_list
    headers_list.extend(header_row[column_num] for column_num in range(len(header_row)))
    x_csv = si.getvalue()
    y_csv = x_csv.replace("\r", "")
    return headers_list, y_csv


def add_headers_to_csv(
    headers_list: list[str], headersless_csv: str, delimiter: str = None
) -> str:
    if delimiter is None:
        delimiter = ","
    header_str = delimiter.join(str(header) for header in headers_list)
    return f"{header_str}\n{headersless_csv}"


def get_csv_column1_column2_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[str, dict[str, int]]:
    y_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        column2_count = get_from_nested_dict(y_dict, [row[0], row[1]], True)
        if not column2_count:
            column2_count = 1
        else:
            column2_count += 1
        set_in_nested_dict(y_dict, [row[0], row[1]], column2_count)
    return y_dict


def create_l2nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[str, dict[str, str]]:
    io_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        csv_io = get_from_nested_dict(io_dict, [row[2], row[3]], True) or io_StringIO()
        new_csv_writer = csv_writer(csv_io, delimiter=",")
        new_csv_writer.writerow(row)
        set_in_nested_dict(io_dict, [row[2], row[3]], csv_io)

    x_dict = {}
    for l1_key, l1_dict in io_dict.items():
        for l2_key, io_function in l1_dict.items():
            l1_l2_csv = io_function.getvalue()
            l1_l2_csv = l1_l2_csv.replace("\r", "")
            set_in_nested_dict(x_dict, [l1_key, l2_key], l1_l2_csv)
    return x_dict


def create_sorted_concatenated_str(y_list: list[str]) -> str:
    x_list = sorted(y_list)
    x_str = "".join(f",{x_header}" for x_header in x_list)
    return x_str[1:]


def get_positional_dict(x_list: list[str]) -> dict[str, int]:
    return {x_element: x_count for x_count, x_element in enumerate(x_list)}


def create_csv(x_headers: list[str], x2d_array: list[list]) -> str:
    x2d_array.insert(0, x_headers)
    si = io_StringIO()
    new_csv_writer = csv_writer(si, delimiter=",")
    for row in x2d_array:
        new_csv_writer.writerow(row)
    x_csv = si.getvalue()
    return x_csv.replace("\r", "")


def get_nested_dict_keys_by_level(x_dict: dict) -> dict[int, set]:
    keys_by_level = {}
    queue = deque([(x_dict, 0)])  # Store (dictionary, current_level)
    while queue:
        current_dict, level = queue.popleft()
        # Traverse the current dictionary
        for key, value in current_dict.items():
            if isinstance(value, dict):
                # If value is a dictionary, add it to the queue for further processing
                queue.append((value, level + 1))
                if level not in keys_by_level:
                    keys_by_level[level] = set()
                keys_by_level[level].add(key)
    return keys_by_level


def get_nested_keys_by_level(x_dict: dict) -> dict[int, set]:
    keys_by_level = {}
    # Queue for traversing the dictionary
    queue = deque([(x_dict, 0)])  # Store (dictionary, current_level)
    while queue:
        current_dict, level = queue.popleft()
        # Traverse the current dictionary
        for key, value in current_dict.items():
            if isinstance(value, dict):
                # If value is a dictionary, add it to the queue for further processing
                queue.append((value, level + 1))
            if level not in keys_by_level:
                keys_by_level[level] = set()
            keys_by_level[level].add(key)
    return keys_by_level


def get_nested_non_dict_keys_by_level(x_dict: dict) -> dict[int, set]:
    keys_by_level = {}
    # Queue for traversing the dictionary
    queue = deque([(x_dict, 0)])  # Store (dictionary, current_level)
    while queue:
        current_dict, level = queue.popleft()
        # Traverse the current dictionary
        for key, value in current_dict.items():
            if level not in keys_by_level:
                keys_by_level[level] = set()
            if isinstance(value, dict):
                # If value is a dictionary, add it to the queue for further processing
                queue.append((value, level + 1))
            else:
                keys_by_level[level].add(key)
    return keys_by_level


def get_nested_non_dict_keys_list(x_dict: dict) -> list:
    levels = get_nested_non_dict_keys_by_level(x_dict)
    x_list = []
    for level_set in levels.values():
        x_list.extend(iter(level_set))
    return x_list


def is_2d_with_unique_keys(x_dict: dict) -> bool:
    key_set_by_level = get_nested_dict_keys_by_level(x_dict).values()
    one_dict_per_level = all(len(x_key_set) <= 1 for x_key_set in key_set_by_level)
    if not one_dict_per_level:
        return False
    prev_keys = set()
    for x_set in get_nested_keys_by_level(x_dict).values():
        if prev_keys & (x_set) != set():
            return False
        prev_keys = prev_keys.union(x_set)
    return True


def get_nested_dict_key_by_level(x_dict: dict) -> list:
    if is_2d_with_unique_keys(x_dict) is False:
        raise Is2dWithUniqueKeysError("dictionary is not 2d_with_unique_keys.")
    key_set_by_level = get_nested_dict_keys_by_level(x_dict)
    ordered_keys = sorted(key_set_by_level.keys())
    return [max(key_set_by_level[key]) for key in ordered_keys]


def create_2d_array_from_dict(x_dict: dict) -> list[list]:
    dict_key_by_level = get_nested_dict_key_by_level(x_dict)
    non_dict_keys = get_nested_non_dict_keys_list(x_dict)
    x_rows = [non_dict_keys]
    level_count = len(dict_key_by_level)
    to_eval_dicts = [[x_dict, 0, {}]]
    while to_eval_dicts != []:
        y0_list = to_eval_dicts.pop()
        y0_dict = y0_list[0]
        y0_level = y0_list[1]
        y0_ancestor_attrs = y0_list[2]
        for y0_key, y0_value in y0_dict.items():
            if isinstance(y0_value, dict):
                to_eval_obj = [y0_value, y0_level + 1, y0_ancestor_attrs]
                to_eval_dicts.append(to_eval_obj)
            else:
                y0_ancestor_attrs[y0_key] = y0_value
        if y0_level == level_count or y0_dict == {}:
            x_rows.append([y0_ancestor_attrs.get(x_key) for x_key in non_dict_keys])

    return x_rows


def str_in_dict_keys(x_str: str, x_dict: dict[str, str]) -> bool:
    return any(x_str in x_key for x_key in x_dict)


def str_in_dict_values(x_str: str, x_dict: dict[str, str]) -> bool:
    return any(x_str in x_value for x_value in x_dict.values())


def str_in_dict(x_str: str, x_dict: dict[str, str]) -> bool:
    return any(x_str in x_key or x_str in x_value for x_key, x_value in x_dict.items())


def str_in_all_dict_keys(x_str: str, x_dict: dict[str, str]) -> bool:
    return all(x_str in x_key for x_key in x_dict)


def str_in_all_dict_values(x_str: str, x_dict: dict[str, str]) -> bool:
    return all(x_str in x_value for x_value in x_dict.values())


def str_in_all_dict(x_str: str, x_dict: dict[str, str]) -> bool:
    return all((x_str in x_key and x_str in x_val) for x_key, x_val in x_dict.items())


def get_str_in_all_sub_dict(x_str: str, x_dict: dict[str, str]) -> dict[str, str]:
    return {
        x_key: x_value
        for x_key, x_value in x_dict.items()
        if x_str not in x_key or x_str not in x_value
    }


def get_str_in_sub_dict(x_str: str, x_dict: dict[str, str]) -> dict[str, str]:
    return {
        x_key: x_value
        for x_key, x_value in x_dict.items()
        if x_str in x_key or x_str in x_value
    }


def get_sorted_list_of_dict_keys(
    x_dict: dict[any, dict], nested_value_key: str, include_sort_values: bool = False
) -> list[str]:
    sorted_keys = sorted(x_dict.keys(), key=lambda k: x_dict[k][nested_value_key])
    if include_sort_values:
        sorted_keys = [[key, x_dict[key][nested_value_key]] for key in sorted_keys]
    return sorted_keys


def get_max_key(x_dict: dict) -> any:
    if not x_dict:
        return None
    max_value = max(x_dict.values())  # Find max value
    return min((k for k in x_dict if x_dict[k] == max_value), key=lambda x: x)


def get_serializable_dict(obj):
    if isinstance(obj, dict):
        return {k: get_serializable_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [get_serializable_dict(v) for v in obj]
    elif isinstance(obj, set):
        return sorted(get_serializable_dict(v) for v in obj)
    elif isinstance(obj, Enum):
        return obj.value
    else:
        return obj


def modular_addition(x_int: int, y_int: int, modulus: int) -> int:
    return (x_int + y_int) % modulus


def set_modular_dict_values(x_dict: dict[int, int]) -> dict[int, int]:
    """Given a dictionary with number keys and values"""
    return {
        x_key: x_value % x_key if x_key else x_value
        for x_key, x_value in x_dict.items()
    }
