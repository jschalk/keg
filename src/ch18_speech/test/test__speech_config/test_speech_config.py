from ch00_py.file_toolbox import create_path
from ch17_jargon.jargon_config import get_jargon_config_dict
from ch18_speech.speech_config import (
    get_speech_filename,
    speech_config_path,
    get_speech_config_dict,
    get_speech_column_ref,
)
from ch99_glossary.ch_keyword import Ch18Keywords as kw


def test_get_speech_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_speech_filename() == f"{kw.speech}.json"


def test_speech_config_path_ReturnsObj_Speech() -> str:
    # ESTABLISH
    chapter_dir = create_path(kw.src, "ch18_speech")
    print(f'{speech_config_path()=}')
    # WHEN / THEN
    assert speech_config_path() == create_path(chapter_dir, "speech_config.json")


def test_get_speech_config_dict_ReturnsObj():
    # ESTABLISH
    jargon_config_dict = get_jargon_config_dict()

    # WHEN
    speech_config_dict = get_speech_config_dict()

    # THEN
    assert speech_config_dict
    speech_l0_keys = set(speech_config_dict.keys())
    for jargon_l0_key, jargon_dimen_dict in jargon_config_dict.items():
        print(f"{jargon_l0_key=}")
        expected_speech_key = jargon_l0_key.replace(kw.jargon, kw.speech)
        assert expected_speech_key in speech_l0_keys
        speech_dict = speech_config_dict.get(expected_speech_key)
        assert set(speech_dict.keys()) == set(jargon_dimen_dict.keys())
        speech_description = speech_dict.get("description")
        assert expected_speech_key in speech_description
        assert kw.aux in speech_description
        assert kw.iux in speech_description

        speech_iux = expected_speech_key.replace("speech_", "iux_")
        assert {speech_iux} == set(speech_dict.get(kw.jkeys).keys())
        speech_aux = expected_speech_key.replace("speech_", "aux_")
        expected_jvalues_keys = {kw.aux_knot, kw.iux_knot, speech_aux}
        print(f"{expected_jvalues_keys=}")
        assert expected_jvalues_keys == set(speech_dict.get(kw.jvalues).keys())

    assert len(speech_config_dict) == len(jargon_config_dict)


def _get_all_speech_config_attrs() -> dict[str, set[str]]:
    speech_config = get_speech_config_dict()
    x_speech_attrs = {}
    for speech_dimen, jkeys_jvalues_dict in speech_config.items():
        attrs_set = set(jkeys_jvalues_dict.get(kw.jkeys).keys())
        attrs_set.update(set(jkeys_jvalues_dict.get(kw.jvalues).keys()))
        x_speech_attrs[speech_dimen] = attrs_set
    return x_speech_attrs


def test_get_speech_column_ref_ReturnsObj():
    # ESTABLISH
    all_speech_config_attrs = _get_all_speech_config_attrs()
    print(f"{all_speech_config_attrs=}")
    print(f"{get_speech_column_ref()=}")
    print(f"{all_speech_config_attrs.get(kw.speech_name)=}")
    print(f"{get_speech_column_ref().get(kw.speech_name)=}")

    # WHEN / THEN
    assert kw.speech_rope in set(get_speech_column_ref().keys())
    assert len(get_speech_column_ref().keys()) == 4
    assert get_speech_column_ref() == all_speech_config_attrs
