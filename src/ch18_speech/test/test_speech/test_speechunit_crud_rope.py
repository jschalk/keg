# from ch18_speech.yap_term import ropeyap_shop
# from ch18_speech.speech_main import speechunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_SpeechUnit_set_ropeyap_SetsAttr():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     x_ropeyap = ropeyap_shop(flare_audie=exx.sue)
#     x_ropeyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_speechunit.ropeyap != x_ropeyap

#     # WHEN
#     sue_speechunit.set_ropeyap(x_ropeyap)

#     # THEN
#     assert sue_speechunit.ropeyap == x_ropeyap


# def test_SpeechUnit_set_ropeyap_RaisesErrorIf_ropeyap_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     x_ropeyap = ropeyap_shop(iux_knot=slash_iux_knot, flare_audie=exx.sue)
#     assert sue_speechunit.iux_knot != x_ropeyap.iux_knot
#     assert sue_speechunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: SpeechUnit iux_knot is '{sue_speechunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_set_ropeyap_RaisesErrorIf_ropeyap_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     x_ropeyap = ropeyap_shop(aux_knot=slash_aux_knot, flare_audie=exx.sue)
#     assert sue_speechunit.aux_knot != x_ropeyap.aux_knot
#     assert sue_speechunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: SpeechUnit aux_knot is '{sue_speechunit.aux_knot}', YapCore is '{slash_aux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_set_ropeyap_RaisesErrorIf_ropeyap_flare_audie_IsNotSame():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     x_ropeyap = ropeyap_shop(flare_audie=exx.yao)
#     assert sue_speechunit.flare_audie != x_ropeyap.flare_audie
#     assert sue_speechunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_speechunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: SpeechUnit flare_audie is '{sue_speechunit.flare_audie}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_SpeechUnit_get_ropeyap_ReturnsObj():
#     # ESTABLISH
#     sue_speechunit = speechunit_shop(exx.sue)
#     static_x_ropeyap = ropeyap_shop(flare_audie=exx.sue)
#     static_x_ropeyap.set_iux2aux("Bob", "Bob of Salem")
#     sue_speechunit.set_ropeyap(static_x_ropeyap)

#     # WHEN
#     gen_x_ropeyap = sue_speechunit.get_ropeyap()

#     # THEN
#     assert gen_x_ropeyap == static_x_ropeyap


# def test_SpeechUnit_set_rope_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_speechunit = speechunit_shop(exx.zia)
#     ropeid_ropeyap = zia_speechunit.get_ropeyap()
#     assert ropeid_ropeyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_speechunit.set_rope(sue_iux, sue_aux)

#     # THEN
#     assert ropeid_ropeyap.iux2aux_exists(sue_iux, sue_aux)


# def test_SpeechUnit_rope_exists_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_speechunit = speechunit_shop(exx.zia)

#     assert zia_speechunit.rope_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_speechunit.set_rope(sue_iux, sue_aux)

#     # THEN
#     assert zia_speechunit.rope_exists(sue_iux, sue_aux)


# def test_SpeechUnit_get_aux_rope_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_speechunit = speechunit_shop(exx.zia)
#     assert zia_speechunit._get_aux_rope(sue_iux) != sue_aux

#     # WHEN
#     zia_speechunit.set_rope(sue_iux, sue_aux)

#     # THEN
#     assert zia_speechunit._get_aux_rope(sue_iux) == sue_aux


# def test_SpeechUnit_del_rope_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_speechunit = speechunit_shop(exx.zia)

#     zia_speechunit.set_rope(sue_iux, sue_aux)
#     zia_speechunit.set_rope(exx.zia, exx.zia)
#     assert zia_speechunit.rope_exists(sue_iux, sue_aux)
#     assert zia_speechunit.rope_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_speechunit.del_rope(sue_iux)

#     # THEN
#     assert zia_speechunit.rope_exists(sue_iux, sue_aux) is False
#     assert zia_speechunit.rope_exists(exx.zia, exx.zia)
