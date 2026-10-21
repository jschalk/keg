# from ch05_rope.rope import default_knot_if_None
# from ch18_speech.test._util.ch17_examples import (
#     get_slash_labelyap,
#     get_slash_nameyap,
#     get_slash_ropeyap,
#     get_slash_titleyap,
# )
# from ch18_speech.speech_main import (
#     _get_rid_of_speech_core_keys,
#     get_speechunit_from_dict,
#     speechunit_shop,
# )
# from ch99_glossary.ch_keyword import Ch18Keywords as kw, ExampleStrs as exx


# def test_SpeechUnit_to_dict_ReturnsObj_Scenario0():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)

#     # WHEN
#     sue_dict = sue_speechunit.to_dict()

#     # THEN
#     print(sue_dict)
#     assert sue_dict
#     assert sue_dict.get(kw.flare_audie) == exx.sue
#     assert sue_dict.get(kw.spark_num) == sue_speechunit.spark_num
#     assert sue_dict.get(kw.iux_knot) == default_knot_if_None()
#     assert sue_dict.get(kw.aux_knot) == default_knot_if_None()
#     sue_nameyap = sue_speechunit.nameyap.to_dict()
#     sue_titleyap = sue_speechunit.titleyap.to_dict()
#     sue_labelyap = sue_speechunit.labelyap.to_dict()
#     sue_ropeyap = sue_speechunit.ropeyap.to_dict()
#     assert sue_dict.get(kw.nameyap) == _get_rid_of_speech_core_keys(sue_nameyap)
#     assert sue_dict.get(kw.titleyap) == _get_rid_of_speech_core_keys(sue_titleyap)
#     assert sue_dict.get(kw.labelyap) == _get_rid_of_speech_core_keys(sue_labelyap)
#     assert sue_dict.get(kw.ropeyap) == _get_rid_of_speech_core_keys(sue_ropeyap)
#     assert sue_dict.keys() == sue_speechunit.__dict__.keys()


# def test_SpeechUnit_to_dict_ReturnsObj_Scenario1():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     colon_aux_knot = ":"
#     sue_speechunit = speechunit_shop(
#         exx.sue, 0, slash_iux_knot, colon_aux_knot
#     )
#     sue_speechunit.set_nameyap(get_slash_nameyap())
#     sue_speechunit.set_titleyap(get_slash_titleyap())
#     sue_speechunit.set_labelyap(get_slash_labelyap())
#     sue_speechunit.set_ropeyap(get_slash_ropeyap())

#     # WHEN
#     sue_dict = sue_speechunit.to_dict()

#     # THEN
#     assert sue_dict.get(kw.flare_audie) == exx.sue
#     assert sue_dict.get(kw.iux_knot) == slash_iux_knot
#     assert sue_dict.get(kw.aux_knot) == colon_aux_knot
#     sue_nameyap = sue_speechunit.nameyap.to_dict()
#     sue_titleyap = sue_speechunit.titleyap.to_dict()
#     sue_labelyap = sue_speechunit.labelyap.to_dict()
#     sue_ropeyap = sue_speechunit.ropeyap.to_dict()
#     assert sue_dict.get(kw.nameyap) == _get_rid_of_speech_core_keys(sue_nameyap)
#     assert sue_dict.get(kw.titleyap) == _get_rid_of_speech_core_keys(sue_titleyap)
#     assert sue_dict.get(kw.labelyap) == _get_rid_of_speech_core_keys(sue_labelyap)
#     assert sue_dict.get(kw.ropeyap) == _get_rid_of_speech_core_keys(sue_ropeyap)


# def test_get_speechunit_from_dict_ReturnsObj():
#     # ESTABLISH
#     sue_spark_num = 7
#     slash_iux_knot = "/"
#     colon_aux_knot = ":"
#     sue_speechunit = speechunit_shop(
#         exx.sue,
#         sue_spark_num,
#         slash_iux_knot,
#         colon_aux_knot,
#     )
#     sue_speechunit.set_nameyap(get_slash_nameyap())
#     sue_speechunit.set_labelyap(get_slash_labelyap())
#     sue_speechunit.set_ropeyap(get_slash_ropeyap())
#     sue_speechunit.set_titleyap(get_slash_titleyap())

#     # WHEN
#     gen_speechunit = get_speechunit_from_dict(sue_speechunit.to_dict())

#     # THEN
#     assert gen_speechunit
#     assert gen_speechunit.flare_audie == exx.sue
#     assert gen_speechunit.spark_num == sue_spark_num
#     assert gen_speechunit.iux_knot == slash_iux_knot
#     assert gen_speechunit.aux_knot == colon_aux_knot
#     assert gen_speechunit.nameyap == get_slash_nameyap()
#     assert gen_speechunit.ropeyap == get_slash_ropeyap()
#     assert gen_speechunit.titleyap == get_slash_titleyap()
