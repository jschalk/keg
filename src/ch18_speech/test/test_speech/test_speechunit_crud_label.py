# from ch17_jargon.yap_term import labelyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_labelyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_labelyap = labelyap_shop(spark_face=exx.sue)
#     x_labelyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN
#     sue_jargonunit.set_labelyap(x_labelyap)

#     # THEN
#     assert sue_jargonunit.labelyap == x_labelyap


# def test_JargonUnit_set_labelyap_RaisesErrorIf_labelyap_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     x_labelyap = labelyap_shop(iux_knot=slash_iux_knot, spark_face=exx.sue)
#     assert sue_jargonunit.iux_knot != x_labelyap.iux_knot
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: JargonUnit iux_knot is '{sue_jargonunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_labelyap_RaisesErrorIf_labelyap_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     x_labelyap = labelyap_shop(aux_knot=slash_aux_knot, spark_face=exx.sue)
#     assert sue_jargonunit.aux_knot != x_labelyap.aux_knot
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: JargonUnit aux_knot is '{sue_jargonunit.aux_knot}', YapCore is '{slash_aux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_labelyap_RaisesErrorIf_labelyap_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     x_labelyap = labelyap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
#     assert sue_jargonunit.unknown_str != x_labelyap.unknown_str
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_labelyap_RaisesErrorIf_labelyap_spark_face_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_labelyap = labelyap_shop(spark_face=exx.yao)
#     assert sue_jargonunit.spark_face != x_labelyap.spark_face
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_labelyap_ReturnsObj():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     static_x_labelyap = labelyap_shop(spark_face=exx.sue)
#     static_x_labelyap.set_iux2aux("Bob", "Bob of Salem")
#     sue_jargonunit.set_labelyap(static_x_labelyap)

#     # WHEN
#     gen_x_labelyap = sue_jargonunit.get_labelyap()

#     # THEN
#     assert gen_x_labelyap == static_x_labelyap


# def test_JargonUnit_set_label_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     labelid_labelyap = zia_jargonunit.get_labelyap()
#     assert labelid_labelyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_roadyap_label(sue_iux, sue_aux)

#     # THEN
#     assert labelid_labelyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_del_roadyap_label_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_roadyap_label(sue_iux, sue_aux)
#     zia_jargonunit.set_roadyap_label(exx.zia, exx.zia)
#     assert zia_jargonunit.roadyap_label_exists(sue_iux, sue_aux)
#     assert zia_jargonunit.roadyap_label_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_roadyap_label(sue_iux)

#     # THEN
#     assert zia_jargonunit.roadyap_label_exists(sue_iux, sue_aux) is False
#     assert zia_jargonunit.roadyap_label_exists(exx.zia, exx.zia)
