from ch00_py.file_toolbox import create_path
from ch16_tash.tash_config import get_tash_args, get_tash_config_dict, get_tash_dimens
from ch17_nabu._ref.ch17_semantic_types import TimeNum
from ch17_nabu.nabu_config import (
    create_nabu_config_path,
    get_nabu_args,
    get_nabu_config_dict,
    get_nabu_config_filename,
    get_nabu_dimens,
    get_nabuable_args,
)
from ch99_glossary.ch_keyword import Ch17Keywords as kw
from inspect import getdoc as inspect_getdoc
from pytest import mark as pytest_mark


def test_get_nabu_config_filename_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config_filename = get_nabu_config_filename()
    # THEN
    assert nabu_config_filename == "nabu_config.json"


def test_create_nabu_config_path_ReturnsObj() -> str:
    # ESTABLISH / WHEN
    chapter_dir = create_path(kw.src, "ch17_nabu")
    # THEN
    assert create_nabu_config_path() == create_path(chapter_dir, "nabu_config.json")


@pytest_mark.skip_on_linux
def test_create_nabu_config_path_HasDocString():
    # ESTABLISH
    chapter_dir = create_path(kw.src, "ch17_nabu")
    doc_str = create_path(chapter_dir, "nabu_config.json")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert inspect_getdoc(create_nabu_config_path) == doc_str


def test_get_nabu_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config = get_nabu_config_dict()

    # THEN
    assert nabu_config
    nabu_config_dimens = set(nabu_config.keys())
    assert kw.nabu_timenum in nabu_config_dimens
    assert set(nabu_config.keys()) == {kw.nabu_timenum}

    tash_config_dict = get_tash_config_dict()
    expected_nabu_config_keys = {
        tash_config_key.replace(kw.tash, kw.nabu)
        for tash_config_key in tash_config_dict.keys()
    }
    assert set(nabu_config.keys()) == expected_nabu_config_keys
    _validate_nabu_config(nabu_config)


def _validate_nabu_config(nabu_config: dict):
    tash_config_dict = get_tash_config_dict()
    x_possible_args = {}
    # for every tash_format file there exists a unique tash_number with leading zeros to make 5 digits
    for x_dimen, nabu_dimen_dict in nabu_config.items():
        # check dimen_dict
        assert nabu_dimen_dict.get(kw.jkeys) is not None
        nabu_dimen_jkeys = set(nabu_dimen_dict.get(kw.jkeys).keys())
        print(f"{nabu_dimen_jkeys=}")
        assert nabu_dimen_jkeys == {kw.iux_time, kw.moment_rope, kw.song_audie}

        assert nabu_dimen_dict.get(kw.jvalues) is not None
        assert nabu_dimen_dict.get("affected_semantic_types") is not None
        tash_dimen = x_dimen.replace(kw.nabu, kw.tash)
        tash_dimen_dict = tash_config_dict.get(tash_dimen)
        print(f"{x_dimen=} {tash_dimen_dict=}")
        tash_semantics_dict = tash_dimen_dict.get("affected_semantic_types")
        tash_semantics_keys = set(tash_semantics_dict.keys())
        nabu_semantics_dict = nabu_dimen_dict.get("affected_semantic_types")
        nabu_semantics_keys = set(nabu_semantics_dict.keys())
        assert nabu_semantics_keys == tash_semantics_keys

        for attr_key, attrs_dict in nabu_dimen_dict.items():
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


# #         print(f"_validate_tash_config {tash_dimens=}")
# #         assert dimen_dict.get(kw.jkeys)
# #         assert dimen_dict.get(kw.jvalues)
# #         assert dimen_dict.get(kw.UPDATE) is None
# #         assert dimen_dict.get(kw.INSERT) is None
# #         assert dimen_dict.get(kw.DELETE) is None
# #         assert dimen_dict.get(kw.normal_specs) is None
# #         assert len(dimen_dict) == 2

# #         tash_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
# #         for jkey_key in tash_jkeys_keys:
# #             print(f"_validate_tash_config {tash_dimens=} {jkey_key=} ")
# #             assert jkey_key in x_possible_args
# #         tash_jvalues_keys = set(dimen_dict.get(kw.jvalues).keys())
# #         for jvalue_key in tash_jvalues_keys:
# #             print(f"_validate_tash_config {tash_dimens=} {jvalue_key=} ")
# #             assert jvalue_key in x_possible_args


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


# def test_set_nabuable_iux_aux_args_ReturnsObj_Scenario0_All_nabuable_args():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     nabuable_args = get_nabuable_args()

#     # WHEN
#     iux_aux_args = set_nabuable_iux_aux_args(nabuable_args)

#     # THEN
#     expected_iux_aux_args = set()
#     for nabuable_arg in nabuable_args:
#         expected_iux_aux_args.add(f"{nabuable_arg}_iux")
#         expected_iux_aux_args.add(f"{nabuable_arg}_aux")
#     print(f"{iux_aux_args=}")
#     assert iux_aux_args == expected_iux_aux_args


# def test_set_nabuable_iux_aux_args_ReturnsObj_Scenario1_OtherArgsAreUntouched():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     run_str = "run"
#     x_nabuable_args = get_nabuable_args()
#     x_nabuable_args.add(run_str)

#     # WHEN
#     iux_aux_args = set_nabuable_iux_aux_args(x_nabuable_args)

#     # THEN
#     expected_iux_aux_args = set()
#     for nabuable_arg in get_nabuable_args():
#         expected_iux_aux_args.add(f"{nabuable_arg}_iux")
#         expected_iux_aux_args.add(f"{nabuable_arg}_aux")
#     expected_iux_aux_args.add(run_str)
#     print(f"{iux_aux_args=}")
#     assert iux_aux_args == expected_iux_aux_args


# def test_get_context_nabuable_args_ReturnsObj():
#     # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     context_args = get_context_nabuable_args()

#     # THEN
#     expected_context_args = set()
#     assert context_args
#     for category, category_dict in get_nabu_config_dict().items():
#         affected_semantic_types = category_dict.get("affected_semantic_types")
#         for semantic_type in affected_semantic_types.keys():
#             if semantic_type in {kw.ReasonNum, kw.FactNum}:
#                 nabu_convertion_type_dict = affected_semantic_types.get(semantic_type)
#                 nabuable_values_dict = nabu_convertion_type_dict.get("nabuable_values")
#                 assert nabuable_values_dict
#                 type_nabuable_args = set(nabuable_values_dict.keys())
#                 print(f"{type_nabuable_args=}")
#                 print(f"{context_args=}")
#                 assert type_nabuable_args.issubset(context_args)
#                 print(f"{category=} {semantic_type=} {nabuable_values_dict=}")
#                 expected_context_args.update(type_nabuable_args)

#     assert expected_context_args == context_args
