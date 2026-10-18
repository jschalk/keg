# from ch05_rope.rope import create_rope, to_rope
# from ch17_jargon.map_term import ropemap_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx


# def test_RopeMap_reveal_aux_ReturnsObjAndSetsAttr_rope_Scenario0():
#     # ESTABLISH
#     a45_str = "amy45"
#     iux_r_knot = "/"
#     iux_amy45_rope = to_rope(a45_str, iux_r_knot)
#     aux_r_knot = ":"
#     rope_ropemap = ropemap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
#     assert rope_ropemap.iux_exists(iux_amy45_rope) is False
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, iux_amy45_rope) is False

#     # WHEN
#     gen_aux_rope = rope_ropemap.reveal_aux(iux_amy45_rope)

#     # THEN
#     assert gen_aux_rope[1:-1] == iux_amy45_rope[1:-1]
#     assert rope_ropemap.iux_exists(iux_amy45_rope)
#     aux_amy45_rope = to_rope(a45_str, aux_r_knot)
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy45_rope)


# def test_RopeMap_reveal_aux_ReturnsObjAndSetsAttr_rope_Scenario1():
#     # ESTABLISH
#     iux_r_knot = "/"
#     aux_r_knot = ":"
#     iux_amy45_rope = to_rope("amy45", iux_r_knot)
#     aux_amy87_rope = to_rope("amy87", aux_r_knot)
#     clean_iux_str = "clean"
#     clean_iux_rope = f"{iux_amy45_rope}{clean_iux_str}{iux_r_knot}"
#     rope_ropemap = ropemap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
#     assert rope_ropemap.iux_exists(iux_amy45_rope) is False
#     assert rope_ropemap.iux_exists(clean_iux_rope) is False

#     # WHEN
#     gen_aux_rope = rope_ropemap.reveal_aux(clean_iux_rope)

#     # THEN
#     assert gen_aux_rope is None
#     assert rope_ropemap.iux_exists(iux_amy45_rope) is False
#     assert rope_ropemap.iux_exists(clean_iux_rope) is False
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope) is False

#     # ESTABLISH
#     rope_ropemap.set_iux2aux(iux_amy45_rope, aux_amy87_rope)
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope)
#     assert rope_ropemap.iux_exists(clean_iux_rope) is False

#     # WHEN
#     gen_aux_rope = rope_ropemap.reveal_aux(clean_iux_rope)

#     # THEN
#     assert rope_ropemap.iux_exists(clean_iux_rope)
#     assert rope_ropemap.iux2aux_exists(clean_iux_rope, gen_aux_rope)
#     assert gen_aux_rope == f"{aux_amy87_rope}{clean_iux_str}{aux_r_knot}"


# def test_RopeMap_reveal_aux_ReturnsObjAndSetsAttr_rope_Scenario2_With_label():
#     # ESTABLISH
#     iux_r_knot = "/"
#     aux_r_knot = ":"
#     iux_amy45_rope = to_rope("amy45", iux_r_knot)
#     aux_amy87_rope = to_rope("amy87", aux_r_knot)
#     clean_iux_str = "clean"
#     clean_aux_str = "prop"
#     clean_iux_rope = f"{iux_amy45_rope}{clean_iux_str}{iux_r_knot}"
#     rope_ropemap = ropemap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
#     rope_ropemap.set_label(clean_iux_str, clean_aux_str)
#     assert rope_ropemap.iux_exists(iux_amy45_rope) is False
#     assert rope_ropemap.iux_exists(clean_iux_rope) is False

#     # WHEN
#     gen_aux_rope = rope_ropemap.reveal_aux(clean_iux_rope)

#     # THEN
#     assert gen_aux_rope is None
#     assert rope_ropemap.iux_exists(iux_amy45_rope) is False
#     assert rope_ropemap.iux_exists(clean_iux_rope) is False
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope) is False

#     # ESTABLISH
#     rope_ropemap.set_iux2aux(iux_amy45_rope, aux_amy87_rope)
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope)
#     assert rope_ropemap.iux_exists(clean_iux_rope) is False

#     # WHEN
#     gen_aux_rope = rope_ropemap.reveal_aux(clean_iux_rope)

#     # THEN
#     assert rope_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope)
#     assert rope_ropemap.iux_exists(clean_iux_rope)
#     assert rope_ropemap.iux2aux_exists(clean_iux_rope, gen_aux_rope)
#     assert gen_aux_rope == f"{aux_amy87_rope}{clean_aux_str}{aux_r_knot}"


# def test_RopeMap_reveal_aux_AddsMissingObjsTo_iux2aux_RopeTerm():
#     # ESTABLISH
#     iux_a45_str = "amy45"
#     aux_a87_str = "amy87"
#     iux_amy45_rope = to_rope(iux_a45_str)
#     aux_amy87_rope = to_rope(aux_a87_str)
#     casa_iux_str = "casa"
#     casa_aux_str = "maison"
#     casa_iux_rope = create_rope(iux_amy45_rope, casa_iux_str)
#     casa_aux_rope = create_rope(aux_amy87_rope, casa_aux_str)
#     clean_iux_str = "clean"
#     clean_aux_str = "propre"
#     clean_iux_rope = create_rope(casa_iux_rope, clean_iux_str)
#     clean_aux_rope = create_rope(casa_aux_rope, clean_aux_str)

#     sweep_iux_rope = create_rope(clean_iux_rope, exx.sweep)
#     sweep_aux_rope = create_rope(clean_aux_rope, exx.sweep)
#     x_ropemap = ropemap_shop()
#     x_ropemap.set_label(iux_a45_str, aux_a87_str)
#     x_ropemap.set_label(casa_iux_str, casa_aux_str)
#     x_ropemap.set_label(clean_iux_str, clean_aux_str)
#     print(f"{x_ropemap.labelmap.iux2aux=}")
#     print(f"{x_ropemap.iux2aux=}")
#     assert x_ropemap.iux_exists(iux_amy45_rope) is False
#     assert x_ropemap.iux_exists(casa_iux_rope) is False
#     assert x_ropemap.iux_exists(clean_iux_rope) is False
#     assert x_ropemap.iux_exists(sweep_iux_rope) is False
#     assert x_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope) is False
#     assert x_ropemap.iux2aux_exists(casa_iux_rope, casa_aux_rope) is False
#     assert x_ropemap.iux2aux_exists(clean_iux_rope, clean_aux_rope) is False
#     assert x_ropemap.iux2aux_exists(sweep_iux_rope, sweep_aux_rope) is False

#     # WHEN
#     assert x_ropemap.reveal_aux(iux_amy45_rope) == aux_amy87_rope
#     print(f"{x_ropemap.labelmap.iux2aux=}")
#     print(f"{x_ropemap.iux2aux=}")
#     # THEN
#     assert x_ropemap.iux_exists(iux_amy45_rope)
#     assert x_ropemap.iux_exists(casa_iux_rope) is False
#     assert x_ropemap.iux_exists(clean_iux_rope) is False
#     assert x_ropemap.iux_exists(sweep_iux_rope) is False
#     assert x_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope)
#     assert x_ropemap.iux2aux_exists(casa_iux_rope, casa_aux_rope) is False
#     assert x_ropemap.iux2aux_exists(clean_iux_rope, clean_aux_rope) is False
#     assert x_ropemap.iux2aux_exists(sweep_iux_rope, sweep_aux_rope) is False

#     # WHEN
#     assert x_ropemap.reveal_aux(casa_iux_rope) == casa_aux_rope
#     # THEN
#     assert x_ropemap.iux_exists(iux_amy45_rope)
#     assert x_ropemap.iux_exists(casa_iux_rope)
#     assert x_ropemap.iux_exists(clean_iux_rope) is False
#     assert x_ropemap.iux_exists(sweep_iux_rope) is False
#     assert x_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope)
#     assert x_ropemap.iux2aux_exists(casa_iux_rope, casa_aux_rope)
#     assert x_ropemap.iux2aux_exists(clean_iux_rope, clean_aux_rope) is False
#     assert x_ropemap.iux2aux_exists(sweep_iux_rope, sweep_aux_rope) is False

#     # WHEN
#     assert x_ropemap.reveal_aux(clean_iux_rope) == clean_aux_rope
#     assert x_ropemap.reveal_aux(sweep_iux_rope) == sweep_aux_rope
#     # THEN
#     assert x_ropemap.iux2aux_exists(iux_amy45_rope, aux_amy87_rope)
#     assert x_ropemap.iux2aux_exists(casa_iux_rope, casa_aux_rope)
#     assert x_ropemap.iux2aux_exists(clean_iux_rope, clean_aux_rope)
#     assert x_ropemap.iux2aux_exists(sweep_iux_rope, sweep_aux_rope)
