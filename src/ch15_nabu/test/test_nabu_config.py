from ch00_py.file_toolbox import create_path
from ch15_nabu._ref.ch15_semantic_types import TimeNum
from ch15_nabu.nabu_config import (
    get_context_nabuable_args,
    get_nabu_args,
    get_nabu_config_dict,
    get_nabu_dimens,
    get_nabuable_args,
    nabu_config_path,
    set_nabuable_otx_inx_args,
)
from os import getcwd as os_getcwd
from ref.keywords import Ch15Keywords as kw


def test_nabu_config_path_ReturnsObj_Nabu() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch15_nabu")
    assert nabu_config_path() == create_path(chapter_dir, "nabu_config.json")


def test_get_nabu_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config = get_nabu_config_dict()

    # THEN
    assert nabu_config
    nabu_config_dimens = set(nabu_config.keys())
    assert kw.nabu_timenum in nabu_config_dimens
    assert len(nabu_config) == 1

    _validate_nabu_config(nabu_config)


#     nabu_rope_dict = nabu_config.get(kw.nabu_rope)
#     nabu_label_dict = nabu_config.get(kw.nabu_label)
#     assert len(nabu_rope_dict.get(kw.jkeys)) == 1
#     assert len(nabu_label_dict.get(kw.jkeys)) == 1
#     assert len(nabu_rope_dict.get(kw.jvalues)) == 4
#     assert len(nabu_label_dict.get(kw.jvalues)) == 4


def _validate_nabu_config(nabu_config: dict):
    x_possible_args = {}

    # for every nabu_format file there exists a unique nabu_number with leading zeros to make 5 digits
    for dimen_dict in nabu_config.values():
        assert dimen_dict.get(kw.jkeys)
        assert dimen_dict.get(kw.jvalues) is not None
        assert dimen_dict.get("affected_semantic_types") is not None
        for attr_key, attrs_dict in dimen_dict.items():
            if attr_key == "affected_semantic_types":
                if kw.TimeNum in set(attrs_dict.keys()):
                    TimeNum_dict = attrs_dict.get(kw.TimeNum)
                    TimeNum_args = TimeNum_dict.get("nabuable_values")
                    expected_TimeNum_args = {kw.tran_time, kw.offi_time, kw.bud_time}
                    assert set(TimeNum_args.keys()) == expected_TimeNum_args
                if kw.ReasonNum in set(attrs_dict.keys()):
                    ReasonNum_dict = attrs_dict.get(kw.ReasonNum)
                    ReasonNum_args = ReasonNum_dict.get("nabuable_values")
                    expected_ReasonNum_args = {kw.reason_lower, kw.reason_upper}
                    assert set(ReasonNum_args.keys()) == expected_ReasonNum_args
                if kw.FactNum in set(attrs_dict.keys()):
                    FactNum_dict = attrs_dict.get(kw.FactNum)
                    FactNum_args = FactNum_dict.get("nabuable_values")
                    expected_FactNum_args = {kw.fact_lower, kw.fact_upper}
                    assert set(FactNum_args.keys()) == expected_FactNum_args
            # print(f"{x_dimen=} {attrs_dict=}")


#         print(f"_validate_nabu_config {nabu_dimens=}")
#         assert dimen_dict.get(kw.jkeys)
#         assert dimen_dict.get(kw.jvalues)
#         assert dimen_dict.get(kw.UPDATE) is None
#         assert dimen_dict.get(kw.INSERT) is None
#         assert dimen_dict.get(kw.DELETE) is None
#         assert dimen_dict.get(kw.normal_specs) is None
#         assert len(dimen_dict) == 2

#         nabu_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
#         for jkey_key in nabu_jkeys_keys:
#             print(f"_validate_nabu_config {nabu_dimens=} {jkey_key=} ")
#             assert jkey_key in x_possible_args
#         nabu_jvalues_keys = set(dimen_dict.get(kw.jvalues).keys())
#         for jvalue_key in nabu_jvalues_keys:
#             print(f"_validate_nabu_config {nabu_dimens=} {jvalue_key=} ")
#             assert jvalue_key in x_possible_args


def test_get_nabu_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config_dimens = get_nabu_dimens()

    # THEN
    assert kw.nabu_timenum in nabu_config_dimens
    assert len(nabu_config_dimens) == 1
    gen_nabu_dimens = set(get_nabu_config_dict().keys())
    assert gen_nabu_dimens == get_nabu_dimens()


def test_get_nabu_args_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_args = get_nabu_args()

    # THEN
    expected_nabu_args = set()
    for dimen_dict in get_nabu_config_dict().values():
        expected_nabu_args.update(set(dimen_dict.get(kw.jkeys).keys()))
        expected_nabu_args.update(set(dimen_dict.get(kw.jvalues).keys()))
    print(f"{expected_nabu_args=}")
    assert nabu_args
    assert nabu_args == expected_nabu_args


def test_get_nabuable_args_ReturnsObj():
    # ESTABLISH / WHEN
    gen_nabuable_args = get_nabuable_args()

    # THEN
    expected_nabuable_args = set()
    assert gen_nabuable_args
    for category, category_dict in get_nabu_config_dict().items():
        affected_semantic_types = category_dict.get("affected_semantic_types")
        for x_key, nabu_convertion_type_dict in affected_semantic_types.items():
            nabuable_values_dict = nabu_convertion_type_dict.get("nabuable_values")
            assert nabuable_values_dict
            type_nabuable_args = set(nabuable_values_dict.keys())
            print(f"{type_nabuable_args=}")
            print(f"{gen_nabuable_args=}")
            assert type_nabuable_args.issubset(gen_nabuable_args)
            print(f"{category=} {x_key=} {nabuable_values_dict=}")
            expected_nabuable_args.update(type_nabuable_args)

    assert expected_nabuable_args == gen_nabuable_args


def test_set_nabuable_otx_inx_args_ReturnsObj_Scenario0_All_nabuable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    nabuable_args = get_nabuable_args()

    # WHEN
    otx_inx_args = set_nabuable_otx_inx_args(nabuable_args)

    # THEN
    expected_otx_inx_args = set()
    for nabuable_arg in nabuable_args:
        expected_otx_inx_args.add(f"{nabuable_arg}_otx")
        expected_otx_inx_args.add(f"{nabuable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_nabuable_otx_inx_args_ReturnsObj_Scenario1_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    x_nabuable_args = get_nabuable_args()
    x_nabuable_args.add(run_str)

    # WHEN
    otx_inx_args = set_nabuable_otx_inx_args(x_nabuable_args)

    # THEN
    expected_otx_inx_args = set()
    for nabuable_arg in get_nabuable_args():
        expected_otx_inx_args.add(f"{nabuable_arg}_otx")
        expected_otx_inx_args.add(f"{nabuable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_context_nabuable_args_ReturnsObj():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    context_args = get_context_nabuable_args()

    # THEN
    expected_context_args = set()
    assert context_args
    for category, category_dict in get_nabu_config_dict().items():
        affected_semantic_types = category_dict.get("affected_semantic_types")
        for semantic_type in affected_semantic_types.keys():
            if semantic_type in {kw.ReasonNum, kw.FactNum}:
                nabu_convertion_type_dict = affected_semantic_types.get(semantic_type)
                nabuable_values_dict = nabu_convertion_type_dict.get("nabuable_values")
                assert nabuable_values_dict
                type_nabuable_args = set(nabuable_values_dict.keys())
                print(f"{type_nabuable_args=}")
                print(f"{context_args=}")
                assert type_nabuable_args.issubset(context_args)
                print(f"{category=} {semantic_type=} {nabuable_values_dict=}")
                expected_context_args.update(type_nabuable_args)

    assert expected_context_args == context_args
