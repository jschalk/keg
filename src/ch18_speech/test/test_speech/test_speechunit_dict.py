# from ch05_rope.rope import default_knot_if_None
# from ch17_jargon.test._util.ch17_examples import (
#     get_slash_labelyap,
#     get_slash_nameyap,
#     get_slash_ropeyap,
#     get_slash_titleyap,
# )
# from ch17_jargon.jargon_config import default_unknown_str_if_None
# from ch17_jargon.jargon_main import (
#     _get_rid_of_jargon_core_keys,
#     get_jargonunit_from_dict,
#     jargonunit_shop,
# )
# from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx


# def test_JargonUnit_to_dict_ReturnsObj_Scenario0():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)

#     # WHEN
#     sue_dict = sue_jargonunit.to_dict()

#     # THEN
#     print(sue_dict)
#     assert sue_dict
#     assert sue_dict.get(kw.flare_audie) == exx.sue
#     assert sue_dict.get(kw.spark_num) == sue_jargonunit.spark_num
#     assert sue_dict.get(kw.iux_knot) == default_knot_if_None()
#     assert sue_dict.get(kw.aux_knot) == default_knot_if_None()
#     assert sue_dict.get(kw.unknown_str) == default_unknown_str_if_None()
#     sue_nameyap = sue_jargonunit.nameyap.to_dict()
#     sue_titleyap = sue_jargonunit.titleyap.to_dict()
#     sue_labelyap = sue_jargonunit.labelyap.to_dict()
#     sue_ropeyap = sue_jargonunit.ropeyap.to_dict()
#     assert sue_dict.get(kw.nameyap) == _get_rid_of_jargon_core_keys(sue_nameyap)
#     assert sue_dict.get(kw.titleyap) == _get_rid_of_jargon_core_keys(sue_titleyap)
#     assert sue_dict.get(kw.labelyap) == _get_rid_of_jargon_core_keys(sue_labelyap)
#     assert sue_dict.get(kw.ropeyap) == _get_rid_of_jargon_core_keys(sue_ropeyap)
#     assert sue_dict.keys() == sue_jargonunit.__dict__.keys()


# def test_JargonUnit_to_dict_ReturnsObj_Scenario1():
#     # ESTABLISH
#     x_unknown_str = "UnknownTerm"
#     slash_iux_knot = "/"
#     colon_aux_knot = ":"
#     sue_jargonunit = jargonunit_shop(
#         exx.sue, 0, slash_iux_knot, colon_aux_knot, x_unknown_str
#     )
#     sue_jargonunit.set_nameyap(get_slash_nameyap())
#     sue_jargonunit.set_titleyap(get_slash_titleyap())
#     sue_jargonunit.set_labelyap(get_slash_labelyap())
#     sue_jargonunit.set_ropeyap(get_slash_ropeyap())

#     # WHEN
#     sue_dict = sue_jargonunit.to_dict()

#     # THEN
#     assert sue_dict.get(kw.flare_audie) == exx.sue
#     assert sue_dict.get(kw.iux_knot) == slash_iux_knot
#     assert sue_dict.get(kw.aux_knot) == colon_aux_knot
#     assert sue_dict.get(kw.unknown_str) == x_unknown_str
#     sue_nameyap = sue_jargonunit.nameyap.to_dict()
#     sue_titleyap = sue_jargonunit.titleyap.to_dict()
#     sue_labelyap = sue_jargonunit.labelyap.to_dict()
#     sue_ropeyap = sue_jargonunit.ropeyap.to_dict()
#     assert sue_dict.get(kw.nameyap) == _get_rid_of_jargon_core_keys(sue_nameyap)
#     assert sue_dict.get(kw.titleyap) == _get_rid_of_jargon_core_keys(sue_titleyap)
#     assert sue_dict.get(kw.labelyap) == _get_rid_of_jargon_core_keys(sue_labelyap)
#     assert sue_dict.get(kw.ropeyap) == _get_rid_of_jargon_core_keys(sue_ropeyap)


# def test_get_jargonunit_from_dict_ReturnsObj():
#     # ESTABLISH
#     sue_spark_num = 7
#     x_unknown_str = "UnknownTerm"
#     slash_iux_knot = "/"
#     colon_aux_knot = ":"
#     sue_jargonunit = jargonunit_shop(
#         exx.sue,
#         sue_spark_num,
#         slash_iux_knot,
#         colon_aux_knot,
#         x_unknown_str,
#     )
#     sue_jargonunit.set_nameyap(get_slash_nameyap())
#     sue_jargonunit.set_labelyap(get_slash_labelyap())
#     sue_jargonunit.set_ropeyap(get_slash_ropeyap())
#     sue_jargonunit.set_titleyap(get_slash_titleyap())

#     # WHEN
#     gen_jargonunit = get_jargonunit_from_dict(sue_jargonunit.to_dict())

#     # THEN
#     assert gen_jargonunit
#     assert gen_jargonunit.flare_audie == exx.sue
#     assert gen_jargonunit.spark_num == sue_spark_num
#     assert gen_jargonunit.iux_knot == slash_iux_knot
#     assert gen_jargonunit.aux_knot == colon_aux_knot
#     assert gen_jargonunit.unknown_str == x_unknown_str
#     assert gen_jargonunit.nameyap == get_slash_nameyap()
#     assert gen_jargonunit.ropeyap == get_slash_ropeyap()
#     assert gen_jargonunit.titleyap == get_slash_titleyap()
