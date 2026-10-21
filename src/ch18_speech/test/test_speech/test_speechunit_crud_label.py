# from ch18_speech.yap_term import labelyap_shop
# from ch18_speech.speech_main import speechunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_SpeechUnit_set_labelyap_SetsAttr():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     x_labelyap = labelyap_shop(flare_audie=exx.sue)
#     x_labelyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_speechunit.labelyap != x_labelyap

#     # WHEN
#     sue_speechunit.set_labelyap(x_labelyap)

#     # THEN
#     assert sue_speechunit.labelyap == x_labelyap


# def test_SpeechUnit_set_labelyap_RaisesErrorIf_labelyap_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     x_labelyap = labelyap_shop(iux_knot=slash_iux_knot, flare_audie=exx.sue)
#     assert sue_speechunit.iux_knot != x_labelyap.iux_knot
#     assert sue_speechunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: SpeechUnit iux_knot is '{sue_speechunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_set_labelyap_RaisesErrorIf_labelyap_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     x_labelyap = labelyap_shop(aux_knot=slash_aux_knot, flare_audie=exx.sue)
#     assert sue_speechunit.aux_knot != x_labelyap.aux_knot
#     assert sue_speechunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: SpeechUnit aux_knot is '{sue_speechunit.aux_knot}', YapCore is '{slash_aux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_set_labelyap_RaisesErrorIf_labelyap_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     x_labelyap = labelyap_shop(unknown_str=casa_unknown_str, flare_audie=exx.sue)
#     assert sue_speechunit.unknown_str != x_labelyap.unknown_str
#     assert sue_speechunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: SpeechUnit unknown_str is '{sue_speechunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_set_labelyap_RaisesErrorIf_labelyap_flare_audie_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     x_labelyap = labelyap_shop(flare_audie=exx.yao)
#     assert sue_speechunit.flare_audie != x_labelyap.flare_audie
#     assert sue_speechunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: SpeechUnit flare_audie is '{sue_speechunit.flare_audie}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_get_labelyap_ReturnsObj():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     static_x_labelyap = labelyap_shop(flare_audie=exx.sue)
#     static_x_labelyap.set_iux2aux("Bob", "Bob of Salem")
#     sue_speechunit.set_labelyap(static_x_labelyap)

#     # WHEN
#     gen_x_labelyap = sue_speechunit.get_labelyap()

#     # THEN
#     assert gen_x_labelyap == static_x_labelyap


# def test_SpeechUnit_set_label_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_speechunit = speechunit_shop(exx.zia)
#     labelid_labelyap = zia_speechunit.get_labelyap()
#     assert labelid_labelyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_speechunit.set_roadyap_label(sue_iux, sue_aux)

#     # THEN
#     assert labelid_labelyap.iux2aux_exists(sue_iux, sue_aux)


# def test_SpeechUnit_del_roadyap_label_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_speechunit = speechunit_shop(exx.zia)

#     zia_speechunit.set_roadyap_label(sue_iux, sue_aux)
#     zia_speechunit.set_roadyap_label(exx.zia, exx.zia)
#     assert zia_speechunit.roadyap_label_exists(sue_iux, sue_aux)
#     assert zia_speechunit.roadyap_label_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_speechunit.del_roadyap_label(sue_iux)

#     # THEN
#     assert zia_speechunit.roadyap_label_exists(sue_iux, sue_aux) is False
#     assert zia_speechunit.roadyap_label_exists(exx.zia, exx.zia)
