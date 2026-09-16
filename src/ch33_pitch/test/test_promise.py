from ch20_brick.brick_config import get_brick_sqlite_types, get_default_sorted_list
from ch22_etl_config.etl_config import get_brick_config_dict
from ch33_pitch.promise import PITCH_NUMERICAL_ARGS, PromiseUnit, promiseunit_shop
from ch99_glossary.ch_keyword import Ch23Keywords as kw, ExampleStrs as exx
from ch99_glossary.sorter import get_keg_elements_sort_order


def get_arg_pitch_num_type(dimen_arg) -> str:
    common_change_args = {
        kw.offi_time,
        kw.fact_lower,
        kw.fact_upper,
        kw.reason_lower,
        kw.reason_upper,
        kw.contact_debt_mass,
        kw.contact_cred_mass,
        kw.group_cred_mass,
        kw.group_debt_mass,
    }
    return "common_change" if dimen_arg in common_change_args else None


def create_expected_pitch_numerical_args():
    brick_config = get_brick_config_dict()
    expected_pitch_numerical_args = {}
    all_dimen_args = set()
    for dimen, dimen_config in brick_config.items():
        dimen_config = brick_config.get(dimen)
        dimen_jkeys = dimen_config.get(kw.jkeys)
        dimen_jvals = dimen_config.get(kw.jvalues)
        dimen_args = set(dimen_jkeys.keys()).union(set(dimen_jvals.keys()))
        all_dimen_args = all_dimen_args.union(dimen_args)

    brick_sqlite_types = get_brick_sqlite_types()
    for dimen_arg in sorted(all_dimen_args):
        print(f"{dimen_arg=}")
        dimen_type = brick_sqlite_types.get(dimen_arg)
        if dimen_type in {"INTEGER", "REAL"}:
            arg_pitch_num_type = get_arg_pitch_num_type(dimen_arg)
            expected_config = {"sqlite_datatype": dimen_type}
            if arg_pitch_num_type:
                expected_config["pitch_num_type"] = arg_pitch_num_type
            expected_pitch_numerical_args[dimen_arg] = expected_config
    return expected_pitch_numerical_args


def test_PITCH_NUMERICAL_ARGS_Exists():
    # ESTABLISH / WHEN
    x_pitch_numerical_args = PITCH_NUMERICAL_ARGS
    # THEN
    # print(x_pitch_numerical_args)
    expected_pitch_numerical_args = create_expected_pitch_numerical_args()
    print(expected_pitch_numerical_args)
    assert x_pitch_numerical_args == expected_pitch_numerical_args


# get a list of all prime tables
# def test_IdeaPrime_Exists():
#     # ESTABLISH / WHEN
#     brick_sqlite_types = get_brick_sqlite_types()
#     # TODO create tool that gets the difference between two momentunits?

#     brick_config = get_brick_config_dict()
#     for dimen, dimen_config in brick_config.items():
#         # print(f"{dimen=}")
#         dimen_config = brick_config.get(dimen)
#         dimen_jkeys = dimen_config.get(kw.jkeys)
#         dimen_jvals = dimen_config.get(kw.jvalues)
#         dimen_args = set(dimen_jkeys.keys()).union(set(dimen_jvals.keys()))
#         dimen_args = get_default_sorted_list(dimen_args)
#         print(f'{dimen:27} {" ".join(dimen_args)}')
#         for dimen_arg in dimen_args:
#             dimen_type = brick_sqlite_types.get(dimen_arg)
#             if dimen_type in {"INTEGER", "REAL"}:
#                 print(f"{dimen_arg} {dimen_type}")

#     # ideaprime = IdeaPrime()
#     # THEN
#     # assert not ideaprime
#     # assert set(ideaprime.__dict__.keys()) == {f"{kw.}s"}
#     assert 1 == 2


def test_PromiseUnit_Exists():
    # ESTABLISH / WHEN
    promiseunit = PromiseUnit()
    # THEN
    assert not promiseunit.ideas
    assert set(promiseunit.__dict__.keys()) == {f"{kw.idea}s"}


def test_promiseunit_shop_ReturnsObj():
    # ESTABLISH / WHEN
    x_promiseunit = promiseunit_shop()
    # THEN
    assert x_promiseunit
    assert x_promiseunit.ideas == {}


# def test_PromiseUnit_add_IdeaPrime():
#     # ESTABLISH / WHEN
#     x_promiseunit = promiseunit_shop()
#     # THEN
#     assert x_promiseunit
#     assert x_promiseunit.ideas == {}
#     # assert 1 == 2
