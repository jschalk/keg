# from ch17_jargon.yap_term import titleyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_titleyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_titleyap = titleyap_shop(spark_face=exx.sue)
#     x_titleyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_jargonunit.titleyap != x_titleyap

#     # WHEN
#     sue_jargonunit.set_titleyap(x_titleyap)

#     # THEN
#     assert sue_jargonunit.titleyap == x_titleyap


# def test_JargonUnit_set_titleyap_RaisesErrorIf_titleyap_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     x_titleyap = titleyap_shop(iux_knot=slash_iux_knot, spark_face=exx.sue)
#     assert sue_jargonunit.iux_knot != x_titleyap.iux_knot
#     assert sue_jargonunit.titleyap != x_titleyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_titleyap(x_titleyap)
#     exception_str = f"set_yapcore Error: JargonUnit iux_knot is '{sue_jargonunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_titleyap_RaisesErrorIf_titleyap_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     x_titleyap = titleyap_shop(aux_knot=slash_aux_knot, spark_face=exx.sue)
#     assert sue_jargonunit.aux_knot != x_titleyap.aux_knot
#     assert sue_jargonunit.titleyap != x_titleyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_titleyap(x_titleyap)
#     exception_str = f"set_yapcore Error: JargonUnit aux_knot is '{sue_jargonunit.aux_knot}', YapCore is '{slash_aux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_titleyap_RaisesErrorIf_titleyap_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     x_titleyap = titleyap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
#     assert sue_jargonunit.unknown_str != x_titleyap.unknown_str
#     assert sue_jargonunit.titleyap != x_titleyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_titleyap(x_titleyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_titleyap_RaisesErrorIf_titleyap_spark_face_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_titleyap = titleyap_shop(spark_face=exx.yao)
#     assert sue_jargonunit.spark_face != x_titleyap.spark_face
#     assert sue_jargonunit.titleyap != x_titleyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_titleyap(x_titleyap)
#     exception_str = f"set_yapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_titleyap_ReturnsObj():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     static_x_titleyap = titleyap_shop(spark_face=exx.sue)
#     static_x_titleyap.set_iux2aux("Bob", "Bob of Salem")
#     sue_jargonunit.set_titleyap(static_x_titleyap)

#     # WHEN
#     gen_x_titleyap = sue_jargonunit.get_titleyap()

#     # THEN
#     assert gen_x_titleyap == static_x_titleyap


# def test_JargonUnit_set_titleterm_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     contact_name_titleyap = zia_jargonunit.get_titleyap()
#     assert contact_name_titleyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_titleterm(sue_iux, sue_aux)

#     # THEN
#     assert contact_name_titleyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_titleterm_exists_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     assert zia_jargonunit.titleterm_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_titleterm(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit.titleterm_exists(sue_iux, sue_aux)


# def test_JargonUnit_get_aux_title_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit._get_aux_title(sue_iux) != sue_aux

#     # WHEN
#     zia_jargonunit.set_titleterm(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit._get_aux_title(sue_iux) == sue_aux


# def test_JargonUnit_del_titleterm_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_titleterm(sue_iux, sue_aux)
#     zia_jargonunit.set_titleterm(exx.zia, exx.zia)
#     assert zia_jargonunit.titleterm_exists(sue_iux, sue_aux)
#     assert zia_jargonunit.titleterm_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_titleterm(sue_iux)

#     # THEN
#     assert zia_jargonunit.titleterm_exists(sue_iux, sue_aux) is False
#     assert zia_jargonunit.titleterm_exists(exx.zia, exx.zia)
