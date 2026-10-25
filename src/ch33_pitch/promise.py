from dataclasses import dataclass

PITCH_NUMERICAL_ARGS = {
    'active_requisite': {'sqlite_datatype': 'INTEGER'},
    'addin': {'sqlite_datatype': 'REAL'},
    'amount': {'sqlite_datatype': 'REAL'},
    'begin': {'sqlite_datatype': 'REAL'},
    'bud_time': {'sqlite_datatype': 'INTEGER'},
    'c400_number': {'sqlite_datatype': 'INTEGER'},
    'celldepth': {'sqlite_datatype': 'INTEGER'},
    'close': {'sqlite_datatype': 'REAL'},
    'contact_cred_mass': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'contact_debt_mass': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'credor_respect': {'sqlite_datatype': 'REAL'},
    'cumulative_day': {'sqlite_datatype': 'INTEGER'},
    'cumulative_minute': {'sqlite_datatype': 'INTEGER'},
    'debtor_respect': {'sqlite_datatype': 'REAL'},
    'denom': {'sqlite_datatype': 'INTEGER'},
    'fact_lower': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'fact_upper': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'fund_grain': {'sqlite_datatype': 'REAL'},
    'fund_pool': {'sqlite_datatype': 'REAL'},
    'give_force': {'sqlite_datatype': 'REAL'},
    'gogo_want': {'sqlite_datatype': 'REAL'},
    'group_cred_mass': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'group_debt_mass': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'inx_time': {'sqlite_datatype': 'INTEGER'},
    'job_listen_rotations': {'sqlite_datatype': 'INTEGER'},
    'mana_grain': {'sqlite_datatype': 'REAL'},
    'max_tree_traverse': {'sqlite_datatype': 'INTEGER'},
    'monthday_index': {'sqlite_datatype': 'INTEGER'},
    'morph': {'sqlite_datatype': 'INTEGER'},
    'numor': {'sqlite_datatype': 'INTEGER'},
    'offi_time': {'sqlite_datatype': 'INTEGER', 'pitch_num_type': 'common_change'},
    'otx_time': {'sqlite_datatype': 'INTEGER'},
    'pledge': {'sqlite_datatype': 'INTEGER'},
    'poynt': {'sqlite_datatype': 'INTEGER'},
    'problem_bool': {'sqlite_datatype': 'INTEGER'},
    'quota': {'sqlite_datatype': 'REAL'},
    'reason_divisor': {'sqlite_datatype': 'INTEGER'},
    'reason_lower': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'reason_upper': {'sqlite_datatype': 'REAL', 'pitch_num_type': 'common_change'},
    'respect_grain': {'sqlite_datatype': 'REAL'},
    'solo': {'sqlite_datatype': 'INTEGER'},
    'spark_num': {'sqlite_datatype': 'INTEGER'},
    'stop_want': {'sqlite_datatype': 'REAL'},
    'take_force': {'sqlite_datatype': 'REAL'},
    'tran_time': {'sqlite_datatype': 'INTEGER'},
    'weekday_order': {'sqlite_datatype': 'INTEGER'},
    'yr1_jan1_offset': {'sqlite_datatype': 'INTEGER'},
}


@dataclass
class PromiseUnit:
    ideas: dict[str,] = None


def promiseunit_shop() -> PromiseUnit:
    return PromiseUnit(ideas={})
