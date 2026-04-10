from src.ch04_rope.rope import create_rope
from src.ch17_idea.brick_main import (
    get_csv_moment_rope_person_name_metrics,
    moment_rope_person_name_nested_csv_dict,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_csv_moment_rope_person_name_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    headerless_csv = f"""{amy_moment_rope},{exx.sue},Bob,13,29
{amy_moment_rope},{exx.sue},Sue,11,23
{amy_moment_rope},{exx.sue},Yao,41,37
{amy_moment_rope},{exx.sue},Zia,41,37
{amy_moment_rope},{exx.bob},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_moment_rope_person_name_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {amy_moment_rope: {exx.sue: 1}}
    assert u_dict == {amy_moment_rope: {exx.sue: 4, exx.bob: 1}}


def test_moment_rope_person_name_nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    headerless_csv = f"""face_x,spark_x,{amy_moment_rope},{exx.sue},Bob,13,29
,,{amy_moment_rope},{exx.sue},Sue,11,23
,,{amy_moment_rope},{exx.sue},Yao,41,37
,,{amy_moment_rope},{exx.sue},Zia,41,37
,,{amy_moment_rope},{exx.bob},Yao,41,37
"""

    # WHEN
    u_dict = moment_rope_person_name_nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""face_x,spark_x,{amy_moment_rope},{exx.sue},Bob,13,29
,,{amy_moment_rope},{exx.sue},Sue,11,23
,,{amy_moment_rope},{exx.sue},Yao,41,37
,,{amy_moment_rope},{exx.sue},Zia,41,37
"""
    static_bob_csv = f""",,{amy_moment_rope},{exx.bob},Yao,41,37
"""
    generated_person_name_dict = u_dict.get(amy_moment_rope)
    assert generated_person_name_dict
    assert list(generated_person_name_dict.keys()) == [exx.sue, exx.bob]
    generated_bob_csv = generated_person_name_dict.get(exx.bob)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_person_name_dict.get(exx.sue)
    assert generated_sue_csv == static_sue_csv
    person_name_csv_dict = {exx.sue: static_sue_csv, exx.bob: static_bob_csv}
    assert u_dict == {amy_moment_rope: person_name_csv_dict}
