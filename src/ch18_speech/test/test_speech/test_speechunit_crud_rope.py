# from ch17_jargon.yap_term import ropeyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_ropeyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_ropeyap = ropeyap_shop(flare_audie=exx.sue)
#     x_ropeyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN
#     sue_jargonunit.set_ropeyap(x_ropeyap)

#     # THEN
#     assert sue_jargonunit.ropeyap == x_ropeyap


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     x_ropeyap = ropeyap_shop(iux_knot=slash_iux_knot, flare_audie=exx.sue)
#     assert sue_jargonunit.iux_knot != x_ropeyap.iux_knot
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit iux_knot is '{sue_jargonunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     x_ropeyap = ropeyap_shop(aux_knot=slash_aux_knot, flare_audie=exx.sue)
#     assert sue_jargonunit.aux_knot != x_ropeyap.aux_knot
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit aux_knot is '{sue_jargonunit.aux_knot}', YapCore is '{slash_aux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     x_ropeyap = ropeyap_shop(unknown_str=casa_unknown_str, flare_audie=exx.sue)
#     assert sue_jargonunit.unknown_str != x_ropeyap.unknown_str
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_flare_audie_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_ropeyap = ropeyap_shop(flare_audie=exx.yao)
#     assert sue_jargonunit.flare_audie != x_ropeyap.flare_audie
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit flare_audie is '{sue_jargonunit.flare_audie}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_ropeyap_ReturnsObj():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     static_x_ropeyap = ropeyap_shop(flare_audie=exx.sue)
#     static_x_ropeyap.set_iux2aux("Bob", "Bob of Salem")
#     sue_jargonunit.set_ropeyap(static_x_ropeyap)

#     # WHEN
#     gen_x_ropeyap = sue_jargonunit.get_ropeyap()

#     # THEN
#     assert gen_x_ropeyap == static_x_ropeyap


# def test_JargonUnit_set_rope_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeid_ropeyap = zia_jargonunit.get_ropeyap()
#     assert ropeid_ropeyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_rope(sue_iux, sue_aux)

#     # THEN
#     assert ropeid_ropeyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_rope_exists_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     assert zia_jargonunit.rope_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_rope(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit.rope_exists(sue_iux, sue_aux)


# def test_JargonUnit_get_aux_rope_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit._get_aux_rope(sue_iux) != sue_aux

#     # WHEN
#     zia_jargonunit.set_rope(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit._get_aux_rope(sue_iux) == sue_aux


# def test_JargonUnit_del_rope_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_rope(sue_iux, sue_aux)
#     zia_jargonunit.set_rope(exx.zia, exx.zia)
#     assert zia_jargonunit.rope_exists(sue_iux, sue_aux)
#     assert zia_jargonunit.rope_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_rope(sue_iux)

#     # THEN
#     assert zia_jargonunit.rope_exists(sue_iux, sue_aux) is False
#     assert zia_jargonunit.rope_exists(exx.zia, exx.zia)
