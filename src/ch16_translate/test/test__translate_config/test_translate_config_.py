from os import getcwd as os_getcwd
from src.ch00_py.file_toolbox import create_path
from src.ch16_translate.translate_config import (
    default_unknown_str,
    default_unknown_str_if_None,
    get_translate_args_dimen_mapping,
    get_translate_config_dict,
    get_translate_dimens,
    get_translate_filename,
    get_translates_column_ref,
    translate_config_path,
)
from src.ref.keywords import Ch16Keywords as kw


def test_get_translate_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_translate_filename() == "translate.json"


def test_translate_config_path_ReturnsObj_Translate() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_translate")
    assert translate_config_path() == create_path(chapter_dir, "translate_config.json")


def test_get_translate_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    translate_config = get_translate_config_dict()

    # THEN
    assert translate_config
    translate_config_dimens = set(translate_config.keys())
    assert kw.translate_name in translate_config_dimens
    assert kw.translate_title in translate_config_dimens
    assert kw.translate_label in translate_config_dimens
    assert kw.translate_rope in translate_config_dimens
    assert len(translate_config) == 4

    _validate_translate_config(translate_config)
    translate_rope_dict = translate_config.get(kw.translate_rope)
    translate_label_dict = translate_config.get(kw.translate_label)
    assert len(translate_rope_dict.get(kw.jkeys)) == 1
    assert len(translate_label_dict.get(kw.jkeys)) == 1
    assert len(translate_rope_dict.get(kw.jvalues)) == 4
    assert len(translate_label_dict.get(kw.jvalues)) == 4


def _validate_translate_config(translate_config: dict):
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

    # for every translate_format file there exists a unique translate_number with leading zeros to make 5 digits
    for translate_dimen, dimen_dict in translate_config.items():
        # print(f"_validate_translate_config {translate_dimen=}")
        assert dimen_dict.get(kw.jkeys)
        assert dimen_dict.get(kw.jvalues)
        assert dimen_dict.get("description")
        assert dimen_dict.get(kw.UPDATE) is None
        assert dimen_dict.get(kw.INSERT) is None
        assert dimen_dict.get(kw.DELETE) is None
        assert dimen_dict.get(kw.normal_specs) is None
        assert len(dimen_dict) == 3

        translate_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
        expected_description_str = f"'{translate_dimen}' is a translation dimen where"
        for jkey_key in translate_jkeys_keys:
            # print(f"_validate_translate_config {translate_dimen=} {jkey_key=} ")
            expected_description_str += f" {jkey_key}"
            assert jkey_key in x_possible_args
        expected_description_str += " is translated by"
        translate_jvalues_keys = sorted(list(dimen_dict.get(kw.jvalues).keys()))
        for jvalue_key in translate_jvalues_keys:
            # print(f"_validate_translate_config {translate_dimen=} {jvalue_key=} ")
            expected_description_str += f" {jvalue_key},"
            assert jvalue_key in x_possible_args

        expected_description_str = expected_description_str[:-1]
        print(expected_description_str)
        assert dimen_dict.get("description") == expected_description_str


def test_get_translate_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    translate_config_dimens = get_translate_dimens()

    # THEN
    assert kw.translate_name in translate_config_dimens
    assert kw.translate_title in translate_config_dimens
    assert kw.translate_label in translate_config_dimens
    assert kw.translate_rope in translate_config_dimens
    assert len(translate_config_dimens) == 4
    expected_config_dimen = set(get_translate_config_dict().keys())
    assert translate_config_dimens == expected_config_dimen


def test_get_translate_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_translate_args_dimen_mapping = get_translate_args_dimen_mapping()
    print(f"{x_translate_args_dimen_mapping=}")

    # THEN
    assert x_translate_args_dimen_mapping
    assert x_translate_args_dimen_mapping.get(kw.otx_rope)
    rope_dimens = {kw.translate_rope}
    assert x_translate_args_dimen_mapping.get(kw.otx_rope) == rope_dimens
    assert x_translate_args_dimen_mapping.get(kw.inx_knot)
    inx_knot_dimens = x_translate_args_dimen_mapping.get(kw.inx_knot)
    assert len(inx_knot_dimens) == 4
    assert len(x_translate_args_dimen_mapping) == 11


def _get_all_translate_config_attrs() -> dict[str, set[str]]:
    translate_config = get_translate_config_dict()
    x_translate_attrs = {}
    for translate_dimen, jkeys_jvalues_dict in translate_config.items():
        attrs_set = set(jkeys_jvalues_dict.get(kw.jkeys).keys())
        attrs_set.update(set(jkeys_jvalues_dict.get(kw.jvalues).keys()))
        x_translate_attrs[translate_dimen] = attrs_set
    return x_translate_attrs


def test_get_translates_column_ref_ReturnsObj():
    # ESTABLISH
    all_translate_config_attrs = _get_all_translate_config_attrs()
    # print(f"{all_translate_config_attrs=}")

    # WHEN / THEN
    assert kw.translate_rope in set(get_translates_column_ref().keys())
    assert len(get_translates_column_ref().keys()) == 4
    assert get_translates_column_ref() == all_translate_config_attrs


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
