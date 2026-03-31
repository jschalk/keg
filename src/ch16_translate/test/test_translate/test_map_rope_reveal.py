from src.ch04_rope.rope import create_rope, to_rope
from src.ch16_translate.map_term import ropemap_shop
from src.ref.keywords import ExampleStrs as exx


def test_RopeMap_reveal_inx_ReturnsObjAndSetsAttr_rope_Scenario0():
    # ESTABLISH
    a45_str = "amy45"
    otx_r_knot = "/"
    otx_amy45_rope = to_rope(a45_str, otx_r_knot)
    inx_r_knot = ":"
    rope_ropemap = ropemap_shop(otx_knot=otx_r_knot, inx_knot=inx_r_knot)
    assert rope_ropemap.otx_exists(otx_amy45_rope) is False
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, otx_amy45_rope) is False

    # WHEN
    gen_inx_rope = rope_ropemap.reveal_inx(otx_amy45_rope)

    # THEN
    assert gen_inx_rope[1:-1] == otx_amy45_rope[1:-1]
    assert rope_ropemap.otx_exists(otx_amy45_rope)
    inx_amy45_rope = to_rope(a45_str, inx_r_knot)
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy45_rope)


def test_RopeMap_reveal_inx_ReturnsObjAndSetsAttr_rope_Scenario1():
    # ESTABLISH
    otx_r_knot = "/"
    inx_r_knot = ":"
    otx_amy45_rope = to_rope("amy45", otx_r_knot)
    inx_amy87_rope = to_rope("amy87", inx_r_knot)
    clean_otx_str = "clean"
    clean_otx_rope = f"{otx_amy45_rope}{clean_otx_str}{otx_r_knot}"
    rope_ropemap = ropemap_shop(otx_knot=otx_r_knot, inx_knot=inx_r_knot)
    assert rope_ropemap.otx_exists(otx_amy45_rope) is False
    assert rope_ropemap.otx_exists(clean_otx_rope) is False

    # WHEN
    gen_inx_rope = rope_ropemap.reveal_inx(clean_otx_rope)

    # THEN
    assert gen_inx_rope is None
    assert rope_ropemap.otx_exists(otx_amy45_rope) is False
    assert rope_ropemap.otx_exists(clean_otx_rope) is False
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope) is False

    # ESTABLISH
    rope_ropemap.set_otx2inx(otx_amy45_rope, inx_amy87_rope)
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope)
    assert rope_ropemap.otx_exists(clean_otx_rope) is False

    # WHEN
    gen_inx_rope = rope_ropemap.reveal_inx(clean_otx_rope)

    # THEN
    assert rope_ropemap.otx_exists(clean_otx_rope)
    assert rope_ropemap.otx2inx_exists(clean_otx_rope, gen_inx_rope)
    assert gen_inx_rope == f"{inx_amy87_rope}{clean_otx_str}{inx_r_knot}"


def test_RopeMap_reveal_inx_ReturnsObjAndSetsAttr_rope_Scenario2_With_label():
    # ESTABLISH
    otx_r_knot = "/"
    inx_r_knot = ":"
    otx_amy45_rope = to_rope("amy45", otx_r_knot)
    inx_amy87_rope = to_rope("amy87", inx_r_knot)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    clean_otx_rope = f"{otx_amy45_rope}{clean_otx_str}{otx_r_knot}"
    rope_ropemap = ropemap_shop(otx_knot=otx_r_knot, inx_knot=inx_r_knot)
    rope_ropemap.set_label(clean_otx_str, clean_inx_str)
    assert rope_ropemap.otx_exists(otx_amy45_rope) is False
    assert rope_ropemap.otx_exists(clean_otx_rope) is False

    # WHEN
    gen_inx_rope = rope_ropemap.reveal_inx(clean_otx_rope)

    # THEN
    assert gen_inx_rope is None
    assert rope_ropemap.otx_exists(otx_amy45_rope) is False
    assert rope_ropemap.otx_exists(clean_otx_rope) is False
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope) is False

    # ESTABLISH
    rope_ropemap.set_otx2inx(otx_amy45_rope, inx_amy87_rope)
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope)
    assert rope_ropemap.otx_exists(clean_otx_rope) is False

    # WHEN
    gen_inx_rope = rope_ropemap.reveal_inx(clean_otx_rope)

    # THEN
    assert rope_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope)
    assert rope_ropemap.otx_exists(clean_otx_rope)
    assert rope_ropemap.otx2inx_exists(clean_otx_rope, gen_inx_rope)
    assert gen_inx_rope == f"{inx_amy87_rope}{clean_inx_str}{inx_r_knot}"


def test_RopeMap_reveal_inx_AddsMissingObjsTo_otx2inx_RopeTerm():
    # ESTABLISH
    otx_a45_str = "amy45"
    inx_a87_str = "amy87"
    otx_amy45_rope = to_rope(otx_a45_str)
    inx_amy87_rope = to_rope(inx_a87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_rope, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_rope, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    sweep_inx_rope = create_rope(clean_inx_rope, exx.sweep)
    x_ropemap = ropemap_shop()
    x_ropemap.set_label(otx_a45_str, inx_a87_str)
    x_ropemap.set_label(casa_otx_str, casa_inx_str)
    x_ropemap.set_label(clean_otx_str, clean_inx_str)
    print(f"{x_ropemap.labelmap.otx2inx=}")
    print(f"{x_ropemap.otx2inx=}")
    assert x_ropemap.otx_exists(otx_amy45_rope) is False
    assert x_ropemap.otx_exists(casa_otx_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.otx_exists(sweep_otx_rope) is False
    assert x_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope) is False
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope) is False
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope) is False
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_inx_rope) is False

    # WHEN
    assert x_ropemap.reveal_inx(otx_amy45_rope) == inx_amy87_rope
    print(f"{x_ropemap.labelmap.otx2inx=}")
    print(f"{x_ropemap.otx2inx=}")
    # THEN
    assert x_ropemap.otx_exists(otx_amy45_rope)
    assert x_ropemap.otx_exists(casa_otx_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.otx_exists(sweep_otx_rope) is False
    assert x_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope) is False
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope) is False
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_inx_rope) is False

    # WHEN
    assert x_ropemap.reveal_inx(casa_otx_rope) == casa_inx_rope
    # THEN
    assert x_ropemap.otx_exists(otx_amy45_rope)
    assert x_ropemap.otx_exists(casa_otx_rope)
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.otx_exists(sweep_otx_rope) is False
    assert x_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope)
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope) is False
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_inx_rope) is False

    # WHEN
    assert x_ropemap.reveal_inx(clean_otx_rope) == clean_inx_rope
    assert x_ropemap.reveal_inx(sweep_otx_rope) == sweep_inx_rope
    # THEN
    assert x_ropemap.otx2inx_exists(otx_amy45_rope, inx_amy87_rope)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope)
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope)
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_inx_rope)
