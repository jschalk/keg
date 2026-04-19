from ch04_rope.rope import create_rope, default_knot_if_None
from ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from ch10_person_listen.keep_tool import (
    get_vision_person,
    save_vision_person,
    vision_file_exists,
)
from ch10_person_listen.test._util.ch10_examples import ch10_example_moment_rope
from ref.keywords import ExampleStrs as exx


def test_save_vision_person_SavesFile(temp3_fs):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)

    bob_person = get_personunit_with_4_levels()
    bob_person.set_person_name(exx.bob)
    x_knot = default_knot_if_None()
    assert not vision_file_exists(
        str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )

    # WHEN
    save_vision_person(str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, bob_person)

    # THEN
    assert vision_file_exists(
        str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )


def test_vision_file_exists_ReturnsBool(temp3_fs):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)

    bob_person = get_personunit_with_4_levels()
    bob_person.set_person_name(exx.bob)
    x_knot = default_knot_if_None()
    assert not (
        vision_file_exists(str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, exx.bob)
    )

    # WHEN
    save_vision_person(str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, bob_person)

    # THEN
    assert vision_file_exists(
        str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )


def test_get_vision_person_reason_lowersFile(temp3_fs):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)

    bob_person = get_personunit_with_4_levels()
    bob_person.set_person_name(exx.bob)
    x_knot = default_knot_if_None()
    save_vision_person(str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, bob_person)

    # WHEN
    bob_vision = get_vision_person(
        str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )

    # THEN
    assert bob_vision.to_dict() == bob_person.to_dict()


def test_get_vision_person_ReturnsNoneIfFileDoesNotExist(
    temp3_fs,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    x_knot = default_knot_if_None()

    # WHEN
    bob_vision = get_vision_person(
        str(temp3_fs), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )

    # THEN
    assert not bob_vision
