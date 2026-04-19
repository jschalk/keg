from src.ch00_py.file_toolbox import save_json
from src.ch08_person_atom.atom_config import get_atom_config_args
from src.ch17_idea._ref.ch17_doc_builder import (
    get_idea_formats_md,
    get_idea_md,
    get_idea_mds,
)
from src.ch17_idea.idea_config import get_idea_config_dict
from src.ref.keywords import Ch17Keywords as kw


def create_dimens_idea_format_dict() -> dict:
    idea_format_files_dict = {}
    x_count = 120
    for idea_dimen, dimen_dict in get_idea_config_dict().items():
        if dimen_dict.get(kw.idea_category) == "person":
            idea_filename = f"ii{x_count:05}_{idea_dimen}_v0_0_0.json"
            attributes_set = {kw.moment_rope, kw.person_name}
            args_dict = get_atom_config_args(idea_dimen)
            attributes_set.update(set(args_dict.keys()))

            idea_format = {"dimens": [idea_dimen], "attributes": attributes_set}
            idea_format_files_dict[idea_filename] = idea_format
            x_count += 1
    return idea_format_files_dict


def test_create_dimens_idea_format_dict_ReturnsObj(rebuild_jsons):
    # ESTABLISH / WHEN
    dimens_idea_format_dict = create_dimens_idea_format_dict()

    # THEN
    for idea_format in sorted(dimens_idea_format_dict.keys()):
        print(f"{idea_format=}")
    assert len(dimens_idea_format_dict) == 10
    person_planunit_filename = f"ii00128_{kw.person_planunit}_v0_0_0.json"
    print(f"{person_planunit_filename=}")
    assert dimens_idea_format_dict.get(person_planunit_filename)
    person_planunit_dict = dimens_idea_format_dict.get(person_planunit_filename)
    assert person_planunit_dict.get(kw.dimens) == [kw.person_planunit]
    assert person_planunit_dict.get(kw.attributes)
    person_planunit_attributes = person_planunit_dict.get(kw.attributes)
    assert kw.moment_rope in person_planunit_attributes
    assert kw.person_name in person_planunit_attributes
    assert kw.plan_rope in person_planunit_attributes
    assert kw.gogo_want in person_planunit_attributes


def test_get_idea_md_ReturnsObj():
    # ESTABLISH
    idea_config = {
        "attributes": {
            kw.knot: {kw.otx_key: False},
            kw.c400_number: {kw.otx_key: False},
            kw.spark_num: {kw.otx_key: True},
            kw.spark_face: {kw.otx_key: True},
            kw.moment_rope: {kw.otx_key: True},
            kw.fund_grain: {kw.otx_key: False},
            kw.job_listen_rotations: {kw.otx_key: False},
            kw.monthday_index: {kw.otx_key: False},
            kw.mana_grain: {kw.otx_key: False},
            kw.respect_grain: {kw.otx_key: False},
            kw.epoch_label: {kw.otx_key: False},
            kw.yr1_jan1_offset: {kw.otx_key: False},
        },
        kw.idea_type: "ii00100",
        kw.dimens: ["momentunit"],
    }

    # WHEN
    idea_md = get_idea_md(idea_config)

    # THEN
    print(idea_md)
    expected_idea_md = f"""# Idea `ii00100`

## Dimens `['momentunit']`

## Attributes
- `{kw.spark_num}`
- `{kw.spark_face}`
- `{kw.moment_rope}`
- `{kw.epoch_label}`
- `{kw.c400_number}`
- `{kw.yr1_jan1_offset}`
- `{kw.monthday_index}`
- `{kw.fund_grain}`
- `{kw.mana_grain}`
- `{kw.respect_grain}`
- `{kw.knot}`
- `{kw.job_listen_rotations}`
"""
    assert (idea_md) == expected_idea_md


def test_get_idea_mds_ReturnsObj(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    ii00100_str = "ii00100"
    idea_config = {
        "attributes": {
            kw.knot: {kw.otx_key: False},
            kw.c400_number: {kw.otx_key: False},
            kw.spark_num: {kw.otx_key: True},
            kw.spark_face: {kw.otx_key: True},
            kw.moment_rope: {kw.otx_key: True},
            kw.fund_grain: {kw.otx_key: False},
            kw.job_listen_rotations: {kw.otx_key: False},
            kw.monthday_index: {kw.otx_key: False},
            kw.mana_grain: {kw.otx_key: False},
            kw.respect_grain: {kw.otx_key: False},
            kw.epoch_label: {kw.otx_key: False},
            kw.yr1_jan1_offset: {kw.otx_key: False},
        },
        kw.idea_type: ii00100_str,
        kw.dimens: ["momentunit"],
    }
    save_json(temp_dir, f"{ii00100_str}.json", idea_config)

    # WHEN
    idea_mds = get_idea_mds(temp_dir)

    # THEN
    expected_idea_md = f"""# Idea `ii00100`

## Dimens `['momentunit']`

## Attributes
- `{kw.spark_num}`
- `{kw.spark_face}`
- `{kw.moment_rope}`
- `{kw.epoch_label}`
- `{kw.c400_number}`
- `{kw.yr1_jan1_offset}`
- `{kw.monthday_index}`
- `{kw.fund_grain}`
- `{kw.mana_grain}`
- `{kw.respect_grain}`
- `{kw.knot}`
- `{kw.job_listen_rotations}`
"""
    assert set(idea_mds.keys()) == {ii00100_str}
    assert idea_mds == {ii00100_str: expected_idea_md}


def test_get_idea_formats_md_ReturnsObj():
    # ESTABLISH / WHEN
    idea_formats_md = get_idea_formats_md()

    # THEN
    assert idea_formats_md
    assert idea_formats_md.find("ii00104") > 0
