from ch04_rope.rope import create_rope, default_knot_if_None, get_unique_short_ropes
from ref.keywords import ExampleStrs as exx


def test_get_unique_short_ropes_ReturnsObj_Scenario0_RootOnly():
    # ESTABLISH
    knot = default_knot_if_None()
    rope_set = {exx.a23}

    # WHEN
    unique_short_ropes = get_unique_short_ropes(rope_set, knot)

    # THEN
    assert unique_short_ropes == {exx.a23: "Amy23"}


def test_get_unique_short_ropess_ReturnsObj_Scenario1_WithUniqueLabels():
    # ESTABLISH
    knot = default_knot_if_None()
    a23_rope = create_rope(exx.a23, None, knot)
    casa_rope = create_rope(a23_rope, exx.casa)
    mop_rope = create_rope(a23_rope, exx.mop)
    rope_set = {a23_rope, casa_rope, mop_rope}

    # WHEN
    unique_short_ropes = get_unique_short_ropes(rope_set, knot)

    # THEN
    assert unique_short_ropes == {
        a23_rope: "Amy23",
        casa_rope: exx.casa,
        mop_rope: exx.mop,
    }


def test_get_unique_short_ropess_ReturnsObj_Scenario2_WithCommonLabels():
    # ESTABLISH
    knot = default_knot_if_None()
    a23_rope = create_rope(exx.a23, None, knot)
    casa_rope = create_rope(a23_rope, exx.casa)
    casa_mop_rope = create_rope(casa_rope, exx.mop)
    sports_str = "sports"
    sports_rope = create_rope(a23_rope, sports_str)
    sports_mop_rope = create_rope(sports_rope, exx.mop)
    rope_set = {a23_rope, casa_rope, casa_mop_rope, sports_rope, sports_mop_rope}

    # WHEN
    unique_short_ropes = get_unique_short_ropes(rope_set, knot)

    # THEN
    expected_short_casa_mop = f"{exx.casa}{knot}{exx.mop}"
    assert unique_short_ropes.get(casa_mop_rope) == expected_short_casa_mop
    assert unique_short_ropes == {
        a23_rope: "Amy23",
        casa_rope: exx.casa,
        casa_mop_rope: expected_short_casa_mop,
        sports_rope: sports_str,
        sports_mop_rope: f"{sports_str}{knot}{exx.mop}",
    }
