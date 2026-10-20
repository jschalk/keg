# from ch17_jargon.yap_term import labelyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_labelyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_labelyap = labelyap_shop(spark_face=exx.sue)
#     x_labelyap.set_otx2inx("Bob", "Bob of Salem")
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN
#     sue_jargonunit.set_labelyap(x_labelyap)

#     # THEN
#     assert sue_jargonunit.labelyap == x_labelyap


# def test_JargonUnit_set_labelyap_RaisesErrorIf_labelyap_otx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_otx_knot = "/"
#     x_labelyap = labelyap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.otx_knot != x_labelyap.otx_knot
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', YapCore is '{slash_otx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_labelyap_RaisesErrorIf_labelyap_inx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_inx_knot = "/"
#     x_labelyap = labelyap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.inx_knot != x_labelyap.inx_knot
#     assert sue_jargonunit.labelyap != x_labelyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_labelyap(x_labelyap)
#     exception_str = f"set_yapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', YapCore is '{slash_inx_knot}'."
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
#     static_x_labelyap.set_otx2inx("Bob", "Bob of Salem")
#     sue_jargonunit.set_labelyap(static_x_labelyap)

#     # WHEN
#     gen_x_labelyap = sue_jargonunit.get_labelyap()

#     # THEN
#     assert gen_x_labelyap == static_x_labelyap


# def test_JargonUnit_set_label_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     labelid_labelyap = zia_jargonunit.get_labelyap()
#     assert labelid_labelyap.otx2inx_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_roadyap_label(sue_otx, sue_inx)

#     # THEN
#     assert labelid_labelyap.otx2inx_exists(sue_otx, sue_inx)


# def test_JargonUnit_del_roadyap_label_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_roadyap_label(sue_otx, sue_inx)
#     zia_jargonunit.set_roadyap_label(exx.zia, exx.zia)
#     assert zia_jargonunit.roadyap_label_exists(sue_otx, sue_inx)
#     assert zia_jargonunit.roadyap_label_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_roadyap_label(sue_otx)

#     # THEN
#     assert zia_jargonunit.roadyap_label_exists(sue_otx, sue_inx) is False
#     assert zia_jargonunit.roadyap_label_exists(exx.zia, exx.zia)
