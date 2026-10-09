from ch00_py.file_toolbox import create_path
from ch17_jargon.jargon_config import (
    default_unknown_str,
    default_unknown_str_if_None,
    get_jargon_args_dimen_mapping,
    get_jargon_config_dict,
    get_jargon_dimens,
    get_jargon_filename,
    get_jargon_column_ref,
    jargon_config_path,
)
from ch99_glossary.ch_keyword import Ch17Keywords as kw
from os.path import join as os_path_join


def test_get_jargon_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_jargon_filename() == "jargon.json"


def test_jargon_config_path_ReturnsObj_Jargon() -> str:
    # ESTABLISH / WHEN / THEN
    chapter_dir = create_path(kw.src, "ch17_jargon")
    assert jargon_config_path() == create_path(chapter_dir, "jargon_config.json")


def test_get_jargon_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_config = get_jargon_config_dict()

    # THEN
    assert jargon_config
    jargon_config_dimens = set(jargon_config.keys())
    assert kw.jargon_name in jargon_config_dimens
    assert kw.jargon_title in jargon_config_dimens
    assert kw.jargon_label in jargon_config_dimens
    assert kw.jargon_rope in jargon_config_dimens
    assert len(jargon_config) == 4

    _validate_jargon_config(jargon_config)
    jargon_rope_dict = jargon_config.get(kw.jargon_rope)
    jargon_label_dict = jargon_config.get(kw.jargon_label)
    assert len(jargon_rope_dict.get(kw.jkeys)) == 1
    assert len(jargon_label_dict.get(kw.jkeys)) == 1
    assert len(jargon_rope_dict.get(kw.jvalues)) == 4
    assert len(jargon_label_dict.get(kw.jvalues)) == 4


def _validate_jargon_config(jargon_config: dict):
    x_possible_args = {
        kw.inx_knot,
        kw.otx_knot,
        kw.inx_title,
        kw.otx_title,
        kw.inx_name,
        kw.otx_name,
        kw.inx_label,
        kw.otx_label,
        kw.inx_rope,
        kw.otx_rope,
        kw.unknown_str,
    }

    # for every jargon_format file there exists a unique jargon_number with leading zeros to make 5 digits
    for jargon_dimen, dimen_dict in jargon_config.items():
        # print(f"_validate_jargon_config {jargon_dimen=}")
        assert dimen_dict.get(kw.jkeys)
        assert dimen_dict.get(kw.jvalues)
        assert dimen_dict.get("description")
        assert dimen_dict.get(kw.UPDATE) is None
        assert dimen_dict.get(kw.INSERT) is None
        assert dimen_dict.get(kw.DELETE) is None
        assert dimen_dict.get(kw.normal_specs) is None
        assert len(dimen_dict) == 3

        jargon_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
        expected_description_str = f"'{jargon_dimen}' is a translation dimen where"
        for jkey_key in jargon_jkeys_keys:
            # print(f"_validate_jargon_config {jargon_dimen=} {jkey_key=} ")
            expected_description_str += f" {jkey_key}"
            assert jkey_key in x_possible_args
        expected_description_str += " is translated by"
        jargon_jvalues_keys = sorted(list(dimen_dict.get(kw.jvalues).keys()))
        for jvalue_key in jargon_jvalues_keys:
            # print(f"_validate_jargon_config {jargon_dimen=} {jvalue_key=} ")
            expected_description_str += f" {jvalue_key},"
            assert jvalue_key in x_possible_args

        expected_description_str = expected_description_str[:-1]
        print(expected_description_str)
        assert dimen_dict.get("description") == expected_description_str


def test_get_jargon_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_config_dimens = get_jargon_dimens()

    # THEN
    assert kw.jargon_name in jargon_config_dimens
    assert kw.jargon_title in jargon_config_dimens
    assert kw.jargon_label in jargon_config_dimens
    assert kw.jargon_rope in jargon_config_dimens
    assert len(jargon_config_dimens) == 4
    expected_config_dimen = set(get_jargon_config_dict().keys())
    assert jargon_config_dimens == expected_config_dimen


def test_get_jargon_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_jargon_args_dimen_mapping = get_jargon_args_dimen_mapping()
    print(f"{x_jargon_args_dimen_mapping=}")

    # THEN
    assert x_jargon_args_dimen_mapping
    assert x_jargon_args_dimen_mapping.get(kw.otx_rope)
    rope_dimens = {kw.jargon_rope}
    assert x_jargon_args_dimen_mapping.get(kw.otx_rope) == rope_dimens
    assert x_jargon_args_dimen_mapping.get(kw.inx_knot)
    inx_knot_dimens = x_jargon_args_dimen_mapping.get(kw.inx_knot)
    assert len(inx_knot_dimens) == 4
    assert len(x_jargon_args_dimen_mapping) == 11


def _get_all_jargon_config_attrs() -> dict[str, set[str]]:
    jargon_config = get_jargon_config_dict()
    x_jargon_attrs = {}
    for jargon_dimen, jkeys_jvalues_dict in jargon_config.items():
        attrs_set = set(jkeys_jvalues_dict.get(kw.jkeys).keys())
        attrs_set.update(set(jkeys_jvalues_dict.get(kw.jvalues).keys()))
        x_jargon_attrs[jargon_dimen] = attrs_set
    return x_jargon_attrs


def test_get_jargon_column_ref_ReturnsObj():
    # ESTABLISH
    all_jargon_config_attrs = _get_all_jargon_config_attrs()
    # print(f"{all_jargon_config_attrs=}")

    # WHEN / THEN
    assert kw.jargon_rope in set(get_jargon_column_ref().keys())
    assert len(get_jargon_column_ref().keys()) == 4
    assert get_jargon_column_ref() == all_jargon_config_attrs


def test_default_unknown_str_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_str() == "UNKNOWN"


def test_default_unknown_str_if_None_ReturnsObj():
    # ESTABLISH
    unknown33_str = "unknown33"
    x_nan = float("nan")

    # WHEN / THEN
    assert default_unknown_str_if_None() == default_unknown_str()
    assert default_unknown_str_if_None(None) == default_unknown_str()
    assert default_unknown_str_if_None(unknown33_str) == unknown33_str
    assert default_unknown_str_if_None(x_nan) == default_unknown_str()
