from ch00_py.file_toolbox import create_path
from ch17_jargon.jargon_config import get_jargon_config_dict
from ch18_lingo.lingo_config import (
    get_lingo_filename,
    lingo_config_path,
    get_lingo_config_dict,
    get_lingo_column_ref,
)
from ch99_glossary.ch_keyword import Ch18Keywords as kw


def test_get_lingo_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_lingo_filename() == f"{kw.lingo}.json"


def test_lingo_config_path_ReturnsObj_Lingo() -> str:
    # ESTABLISH
    chapter_dir = create_path(kw.src, "ch18_lingo")
    print(f'{lingo_config_path()=}')
    # WHEN / THEN
    assert lingo_config_path() == create_path(chapter_dir, "lingo_config.json")


def test_get_lingo_config_dict_ReturnsObj():
    # ESTABLISH
    jargon_config_dict = get_jargon_config_dict()

    # WHEN
    lingo_config_dict = get_lingo_config_dict()

    # THEN
    assert lingo_config_dict
    lingo_l0_keys = set(lingo_config_dict.keys())
    for jargon_l0_key, jargon_dimen_dict in jargon_config_dict.items():
        print(f"{jargon_l0_key=}")
        expected_lingo_key = jargon_l0_key.replace(kw.jargon, kw.lingo)
        assert expected_lingo_key in lingo_l0_keys
        lingo_dict = lingo_config_dict.get(expected_lingo_key)
        assert set(lingo_dict.keys()) == set(jargon_dimen_dict.keys())
        lingo_description = lingo_dict.get("description")
        assert expected_lingo_key in lingo_description
        assert kw.aux in lingo_description
        assert kw.iux in lingo_description

        lingo_iux = expected_lingo_key.replace("lingo_", "iux_")
        assert {lingo_iux} == set(lingo_dict.get(kw.jkeys).keys())
        lingo_aux = expected_lingo_key.replace("lingo_", "aux_")
        expected_jvalues_keys = {kw.aux_knot, kw.iux_knot, lingo_aux}
        print(f"{expected_jvalues_keys=}")
        assert expected_jvalues_keys == set(lingo_dict.get(kw.jvalues).keys())

    assert len(lingo_config_dict) == len(jargon_config_dict)


def _get_all_lingo_config_attrs() -> dict[str, set[str]]:
    lingo_config = get_lingo_config_dict()
    x_lingo_attrs = {}
    for lingo_dimen, jkeys_jvalues_dict in lingo_config.items():
        attrs_set = set(jkeys_jvalues_dict.get(kw.jkeys).keys())
        attrs_set.update(set(jkeys_jvalues_dict.get(kw.jvalues).keys()))
        x_lingo_attrs[lingo_dimen] = attrs_set
    return x_lingo_attrs


def test_get_lingo_column_ref_ReturnsObj():
    # ESTABLISH
    all_lingo_config_attrs = _get_all_lingo_config_attrs()
    print(f"{all_lingo_config_attrs=}")
    print(f"{get_lingo_column_ref()=}")
    print(f"{all_lingo_config_attrs.get(kw.lingo_name)=}")
    print(f"{get_lingo_column_ref().get(kw.lingo_name)=}")

    # WHEN / THEN
    assert kw.lingo_rope in set(get_lingo_column_ref().keys())
    assert len(get_lingo_column_ref().keys()) == 4
    assert get_lingo_column_ref() == all_lingo_config_attrs
