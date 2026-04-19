from ch00_py.dict_toolbox import get_0_if_None, get_1_if_None
from ch00_py.file_toolbox import create_path, open_json, save_json
from ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum
from copy import copy as copy_copy
from os.path import exists as os_path_exists
from pathlib import Path


def default_grain_num_if_None(grain_num: GrainNum = None) -> GrainNum:
    return get_1_if_None(grain_num)


def default_pool_num() -> PoolNum:
    return PoolNum(1000000000.0)


def validate_pool_num(x_pool_num: PoolNum = None) -> PoolNum:
    """Return default_pool_num if None passed. Check if pool_num is valid given grain_num"""

    x_pool_num = default_pool_num() if x_pool_num is None else x_pool_num
    return max(get_1_if_None(x_pool_num), default_grain_num_if_None())


def valid_allotment_ratio(big_number: float, grain_num: float) -> bool:
    """Checks that big_number is wholly divisible by grain_num"""
    return (big_number % grain_num) == 0


class MissingBaseResidualError(Exception):
    pass


def _get_missing_scale_list(
    missing_scale: PoolNum, grain_unit: GrainNum, list_length: int
) -> list[GrainNum]:
    if list_length == 0 or missing_scale == 0:
        return []
    missing_avg = missing_scale / list_length
    missing_base_multipler = int(missing_avg / grain_unit)
    missing_base_scale_unit = missing_base_multipler * grain_unit
    missing_scale_list = [missing_base_scale_unit for _ in range(list_length)]
    missing_base_residual = missing_scale - sum(missing_scale_list)

    x_count = 0
    if missing_base_residual > 0:
        while missing_base_residual > 0:
            missing_scale_list[x_count] += grain_unit
            missing_base_residual -= grain_unit
            x_count += 1

            if missing_base_residual < 0:
                raise MissingBaseResidualError(
                    f"missing_base_residual calculation failed probably due to missing_scale not being a multiple of grain_unit. missing_scale={missing_scale} grain_unit={grain_unit}."
                )
    else:
        while missing_base_residual < 0:
            missing_scale_list[x_count] -= grain_unit
            missing_base_residual += grain_unit
            x_count += 1

            if missing_base_residual > 0:
                raise MissingBaseResidualError(
                    f"missing_base_residual calculation failed probably due to missing_scale not being a multiple of grain_unit. missing_scale={missing_scale} grain_unit={grain_unit}."
                )

    return missing_scale_list


def _allot_missing_scale(
    ledger: dict[str, WeightNum],
    scale_number: PoolNum,
    grain_unit: GrainNum,
    missing_scale: PoolNum,
) -> dict[str, PoolNum]:
    missing_scale_list = _get_missing_scale_list(missing_scale, grain_unit, len(ledger))
    changes_ledger_list = []
    if missing_scale != 0:
        x_count = 0
        for x_key, x_float in sorted(ledger.items(), key=lambda kv: (-kv[1], kv[0])):
            difference_scale = missing_scale_list[x_count]
            changes_ledger_list.append([x_key, x_float + difference_scale])
            missing_scale -= difference_scale
            if missing_scale == 0:
                break
            x_count += 1

    for x_ledger_change in changes_ledger_list:
        ledger[x_ledger_change[0]] = x_ledger_change[1]

    allot_sum = sum(ledger.values())
    if ledger != {} and allot_sum != scale_number:
        raise ValueError(
            f"Summation of allots '{allot_sum}' is not equal to scale '{scale_number}'."
        )
    return ledger


def _calc_allot_value(
    obj, ledger_value_total: PoolNum, scale_number: PoolNum, grain_unit: GrainNum
):
    if ledger_value_total == 0:
        return 0
    # calculate the allot based on obj to total ratio
    allot_amt = (obj / ledger_value_total) * scale_number
    # Adjust to the nearest grain unit
    return round(allot_amt / grain_unit) * grain_unit


def _create_allot_dict(
    ledger: dict[str, WeightNum], scale_number: GrainNum, grain_unit: float
) -> dict[str, PoolNum]:
    # Calculate the total sum of ledger allots
    ledger_value_total = sum(ledger.values())
    return {
        x_key: _calc_allot_value(x_obj, ledger_value_total, scale_number, grain_unit)
        for x_key, x_obj in ledger.items()
    }


def allot_scale(
    ledger: dict[str, WeightNum], scale_number: PoolNum, grain_unit: GrainNum
) -> dict[str, PoolNum]:
    """
    allots the scale_number among ledger as float values with a resolution of the grain_unit.

    :param ledger: Dictionary of str key with a relative strength attribute.
    :param scale_number: The total number to allot.
    :param grain_unit: The smallest unit of distribution.
    :raises ValueError: If the scale number is not a multiple of the grain unit.
    :return: Dictionary with alloted values.
    """
    # Check if the scale number is a multiple of the grain unit
    if scale_number % grain_unit != 0:
        raise ValueError(
            f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
        )
    if not ledger:
        return {}
    # any ledger key with value zero will be not be alloted any scale_number
    zero_values = {x_key for x_key, x_value in ledger.items() if x_value == 0}
    for x_key in zero_values:
        ledger.pop(x_key)
    allot_dict = _create_allot_dict(ledger, scale_number, grain_unit)
    x_missing = scale_number - sum(allot_dict.values())
    allot_dict = _allot_missing_scale(allot_dict, scale_number, grain_unit, x_missing)
    # add back in ledger keys that by definition were to have    value zero
    for x_key in zero_values:
        allot_dict[x_key] = 0
    return allot_dict


def allot_nested_scale(
    x_dir: str,
    src_filename: str,
    scale_number: GrainNum,
    grain_unit: float,
    depth: int,
    dst_filename: str = None,
) -> dict[str, PoolNum]:
    root_file_path = create_path(x_dir, src_filename)
    root_ledger = open_json(root_file_path)
    root_allot = allot_scale(root_ledger, scale_number, grain_unit)
    if not dst_filename:
        dst_filename = "alloted.json"
    save_json(x_dir, dst_filename, root_allot)
    evalutable_allot_dirs = [x_dir]
    final_allots = {(): root_allot}

    while evalutable_allot_dirs != []:
        parent_dir = evalutable_allot_dirs.pop()
        parent_allot_path = create_path(parent_dir, dst_filename)
        parent_allot = open_json(parent_allot_path)
        for x_dst, x_scale in parent_allot.items():
            child_dir = create_path(parent_dir, x_dst)
            local_dir_parts = _local_path_parts(x_dir, child_dir)
            child_ledger_path = create_path(child_dir, src_filename)
            if os_path_exists(child_ledger_path) and len(local_dir_parts) <= depth:
                child_ledger = open_json(child_ledger_path)
                child_allot = allot_scale(child_ledger, x_scale, grain_unit)
                save_json(child_dir, dst_filename, child_allot)
                final_allots[local_dir_parts] = child_allot
                evalutable_allot_dirs.append(child_dir)

    return _calc_final_allot(final_allots)


def _calc_final_allot(final_allots: dict[str, dict]) -> dict[str, PoolNum]:
    final_allot_keys = list(final_allots.keys())
    x_count = 0
    while final_allot_keys != [] and x_count < 1000:
        # pop longest element in list
        # max_element_length = 0
        # for x_element in final_allot_keys:
        #     if len(x_element) > max_element_length:
        #         max_element_length = len(x_element)
        calc_allot_up_to_parent = final_allot_keys.pop(-1)
        # assert len(calc_allot_up_to_parent) == max_element_length
        child_to_push = final_allots.get(calc_allot_up_to_parent)
        calc_allot_up_to_parent = list(calc_allot_up_to_parent)

        if calc_allot_up_to_parent != []:
            parent_allot_key = calc_allot_up_to_parent.pop(-1)
            parent_to_update = final_allots.get(tuple(calc_allot_up_to_parent))
            del parent_to_update[parent_allot_key]
            for x_key, x_scale in child_to_push.items():
                parent_to_update[x_key] = (
                    get_0_if_None(parent_to_update.get(x_key)) + x_scale
                )
        x_count += 1
    return final_allots.get(())


def _local_path_parts(root_dir: str, y_dir: str) -> tuple[str]:
    local_path = copy_copy(y_dir)
    local_path = local_path.replace(root_dir, "")
    path_obj = Path(local_path)
    return tuple(path_obj.parts[1:])
