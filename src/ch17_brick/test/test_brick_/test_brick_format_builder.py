from ch00_py.file_toolbox import save_json
from ch08_person_atom.atom_config import get_atom_config_args
from ch17_brick._ref.ch17_doc_builder import (
    get_brick_formats_md,
    get_brick_md,
    get_brick_mds,
)
from ch17_brick.brick_config import get_brick_config_dict
from ref.keywords import Ch17Keywords as kw


def create_dimens_brick_format_dict() -> dict:
    brick_format_files_dict = {}
    x_count = 120
    for brick_dimen, dimen_dict in get_brick_config_dict().items():
        if dimen_dict.get(kw.brick_category) == "person":
            brick_filename = f"bk{x_count:05}_{brick_dimen}_v0_0_0.json"
            attributes_set = {kw.moment_rope, kw.person_name}
            args_dict = get_atom_config_args(brick_dimen)
            attributes_set.update(set(args_dict.keys()))

            brick_format = {"dimens": [brick_dimen], "attributes": attributes_set}
            brick_format_files_dict[brick_filename] = brick_format
            x_count += 1
    return brick_format_files_dict


def test_create_dimens_brick_format_dict_ReturnsObj(rebuild_jsons):
    # ESTABLISH / WHEN
    dimens_brick_format_dict = create_dimens_brick_format_dict()

    # THEN
    for brick_format in sorted(dimens_brick_format_dict.keys()):
        print(f"{brick_format=}")
    assert len(dimens_brick_format_dict) == 10
    person_planunit_filename = f"bk00128_{kw.person_planunit}_v0_0_0.json"
    print(f"{person_planunit_filename=}")
    assert dimens_brick_format_dict.get(person_planunit_filename)
    person_planunit_dict = dimens_brick_format_dict.get(person_planunit_filename)
    assert person_planunit_dict.get(kw.dimens) == [kw.person_planunit]
    assert person_planunit_dict.get(kw.attributes)
    person_planunit_attributes = person_planunit_dict.get(kw.attributes)
    assert kw.moment_rope in person_planunit_attributes
    assert kw.person_name in person_planunit_attributes
    assert kw.plan_rope in person_planunit_attributes
    assert kw.gogo_want in person_planunit_attributes


def test_get_brick_md_ReturnsObj():
    # ESTABLISH
    brick_config = {
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
        kw.brick_type: "bk00100",
        kw.dimens: ["momentunit"],
    }

    # WHEN
    brick_md = get_brick_md(brick_config)

    # THEN
    print(brick_md)
    expected_brick_md = f"""# Brick `bk00100`

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
    assert (brick_md) == expected_brick_md


def test_get_brick_mds_ReturnsObj(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    bk00100_str = "bk00100"
    brick_config = {
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
        kw.brick_type: bk00100_str,
        kw.dimens: ["momentunit"],
    }
    save_json(temp_dir, f"{bk00100_str}.json", brick_config)

    # WHEN
    brick_mds = get_brick_mds(temp_dir)

    # THEN
    expected_brick_md = f"""# Brick `bk00100`

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
    assert set(brick_mds.keys()) == {bk00100_str}
    assert brick_mds == {bk00100_str: expected_brick_md}


def test_get_brick_formats_md_ReturnsObj():
    # ESTABLISH / WHEN
    brick_formats_md = get_brick_formats_md()

    # THEN
    assert brick_formats_md
    assert brick_formats_md.find("bk00104") > 0
