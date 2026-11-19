from ch00_py.file_toolbox import create_path
from ch16_tash._ref.ch16_semantic_types import TimeNum
from ch16_tash.tash_config import (
    create_tash_config_path,
    get_context_tashable_args,
    get_tash_args,
    get_tash_config_dict,
    get_tash_dimens,
    get_tashable_args,
    set_tashable_otx_inx_args,
)
from ch99_glossary.ch_keyword import Ch16Keywords as kw


def test_create_tash_config_path_ReturnsObj_Tash() -> str:
    # ESTABLISH / WHEN
    chapter_dir = create_path(kw.src, "ch16_tash")
    # THEN
    assert create_tash_config_path() == create_path(chapter_dir, "tash_config.json")


def test_get_tash_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    tash_config = get_tash_config_dict()

    # THEN
    assert tash_config
    tash_config_dimens = set(tash_config.keys())
    assert kw.tash_timenum in tash_config_dimens
    assert len(tash_config) == 1

    _validate_tash_config(tash_config)


#     tash_rope_dict = tash_config.get(kw.tash_rope)
#     tash_label_dict = tash_config.get(kw.tash_label)
#     assert len(tash_rope_dict.get(kw.jkeys)) == 1
#     assert len(tash_label_dict.get(kw.jkeys)) == 1
#     assert len(tash_rope_dict.get(kw.jvalues)) == 4
#     assert len(tash_label_dict.get(kw.jvalues)) == 4


def _validate_tash_config(tash_config: dict):
    x_possible_args = {}

    # for every tash_format file there exists a unique tash_number with leading zeros to make 5 digits
    for dimen_dict in tash_config.values():
        assert dimen_dict.get(kw.jkeys)
        assert dimen_dict.get(kw.jvalues) is not None
        assert dimen_dict.get("affected_semantic_types") is not None
        for attr_key, attrs_dict in dimen_dict.items():
            if attr_key == "affected_semantic_types":
                if kw.TimeNum in set(attrs_dict.keys()):
                    TimeNum_dict = attrs_dict.get(kw.TimeNum)
                    TimeNum_args = TimeNum_dict.get("tashable_values")
                    expected_TimeNum_args = {kw.tran_time, kw.offi_time, kw.bud_time}
                    assert set(TimeNum_args.keys()) == expected_TimeNum_args
                if kw.ReasonNum in set(attrs_dict.keys()):
                    ReasonNum_dict = attrs_dict.get(kw.ReasonNum)
                    ReasonNum_args = ReasonNum_dict.get("tashable_values")
                    expected_ReasonNum_args = {kw.reason_lower, kw.reason_upper}
                    assert set(ReasonNum_args.keys()) == expected_ReasonNum_args
                if kw.FactNum in set(attrs_dict.keys()):
                    FactNum_dict = attrs_dict.get(kw.FactNum)
                    FactNum_args = FactNum_dict.get("tashable_values")
                    expected_FactNum_args = {kw.fact_lower, kw.fact_upper}
                    assert set(FactNum_args.keys()) == expected_FactNum_args
            # print(f"{x_dimen=} {attrs_dict=}")


#         print(f"_validate_tash_config {tash_dimens=}")
#         assert dimen_dict.get(kw.jkeys)
#         assert dimen_dict.get(kw.jvalues)
#         assert dimen_dict.get(kw.UPDATE) is None
#         assert dimen_dict.get(kw.INSERT) is None
#         assert dimen_dict.get(kw.DELETE) is None
#         assert dimen_dict.get(kw.normal_specs) is None
#         assert len(dimen_dict) == 2

#         tash_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
#         for jkey_key in tash_jkeys_keys:
#             print(f"_validate_tash_config {tash_dimens=} {jkey_key=} ")
#             assert jkey_key in x_possible_args
#         tash_jvalues_keys = set(dimen_dict.get(kw.jvalues).keys())
#         for jvalue_key in tash_jvalues_keys:
#             print(f"_validate_tash_config {tash_dimens=} {jvalue_key=} ")
#             assert jvalue_key in x_possible_args


def test_get_tash_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    tash_config_dimens = get_tash_dimens()

    # THEN
    assert kw.tash_timenum in tash_config_dimens
    assert len(tash_config_dimens) == 1
    gen_tash_dimens = set(get_tash_config_dict().keys())
    assert gen_tash_dimens == get_tash_dimens()


def test_get_tash_args_ReturnsObj():
    # ESTABLISH / WHEN
    tash_args = get_tash_args()

    # THEN
    expected_tash_args = set()
    for dimen_dict in get_tash_config_dict().values():
        expected_tash_args.update(set(dimen_dict.get(kw.jkeys).keys()))
        expected_tash_args.update(set(dimen_dict.get(kw.jvalues).keys()))
    print(f"{expected_tash_args=}")
    assert tash_args
    assert tash_args == expected_tash_args


def test_get_tashable_args_ReturnsObj():
    # ESTABLISH / WHEN
    gen_tashable_args = get_tashable_args()

    # THEN
    expected_tashable_args = set()
    assert gen_tashable_args
    for category, category_dict in get_tash_config_dict().items():
        affected_semantic_types = category_dict.get("affected_semantic_types")
        for x_key, tash_convertion_type_dict in affected_semantic_types.items():
            tashable_values_dict = tash_convertion_type_dict.get("tashable_values")
            assert tashable_values_dict
            type_tashable_args = set(tashable_values_dict.keys())
            print(f"{type_tashable_args=}")
            print(f"{gen_tashable_args=}")
            assert type_tashable_args.issubset(gen_tashable_args)
            print(f"{category=} {x_key=} {tashable_values_dict=}")
            expected_tashable_args.update(type_tashable_args)

    assert expected_tashable_args == gen_tashable_args


def test_set_tashable_otx_inx_args_ReturnsObj_Scenario0_All_tashable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    tashable_args = get_tashable_args()

    # WHEN
    otx_inx_args = set_tashable_otx_inx_args(tashable_args)

    # THEN
    expected_otx_inx_args = set()
    for tashable_arg in tashable_args:
        expected_otx_inx_args.add(f"{tashable_arg}_otx")
        expected_otx_inx_args.add(f"{tashable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_tashable_otx_inx_args_ReturnsObj_Scenario1_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    x_tashable_args = get_tashable_args()
    x_tashable_args.add(run_str)

    # WHEN
    otx_inx_args = set_tashable_otx_inx_args(x_tashable_args)

    # THEN
    expected_otx_inx_args = set()
    for tashable_arg in get_tashable_args():
        expected_otx_inx_args.add(f"{tashable_arg}_otx")
        expected_otx_inx_args.add(f"{tashable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_context_tashable_args_ReturnsObj():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    context_args = get_context_tashable_args()

    # THEN
    expected_context_args = set()
    assert context_args
    for category, category_dict in get_tash_config_dict().items():
        affected_semantic_types = category_dict.get("affected_semantic_types")
        for semantic_type in affected_semantic_types.keys():
            if semantic_type in {kw.ReasonNum, kw.FactNum}:
                tash_convertion_type_dict = affected_semantic_types.get(semantic_type)
                tashable_values_dict = tash_convertion_type_dict.get("tashable_values")
                assert tashable_values_dict
                type_tashable_args = set(tashable_values_dict.keys())
                print(f"{type_tashable_args=}")
                print(f"{context_args=}")
                assert type_tashable_args.issubset(context_args)
                print(f"{category=} {semantic_type=} {tashable_values_dict=}")
                expected_context_args.update(type_tashable_args)

    assert expected_context_args == context_args
