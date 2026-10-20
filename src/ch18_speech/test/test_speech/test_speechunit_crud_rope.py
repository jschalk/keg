# from ch17_jargon.yap_term import ropeyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_ropeyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_ropeyap = ropeyap_shop(spark_face=exx.sue)
#     x_ropeyap.set_otx2inx("Bob", "Bob of Salem")
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN
#     sue_jargonunit.set_ropeyap(x_ropeyap)

#     # THEN
#     assert sue_jargonunit.ropeyap == x_ropeyap


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_otx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_otx_knot = "/"
#     x_ropeyap = ropeyap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.otx_knot != x_ropeyap.otx_knot
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', YapCore is '{slash_otx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_inx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_inx_knot = "/"
#     x_ropeyap = ropeyap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.inx_knot != x_ropeyap.inx_knot
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', YapCore is '{slash_inx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     x_ropeyap = ropeyap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
#     assert sue_jargonunit.unknown_str != x_ropeyap.unknown_str
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_ropeyap_RaisesErrorIf_ropeyap_spark_face_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_ropeyap = ropeyap_shop(spark_face=exx.yao)
#     assert sue_jargonunit.spark_face != x_ropeyap.spark_face
#     assert sue_jargonunit.ropeyap != x_ropeyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_ropeyap(x_ropeyap)
#     exception_str = f"set_yapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_ropeyap_ReturnsObj():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     static_x_ropeyap = ropeyap_shop(spark_face=exx.sue)
#     static_x_ropeyap.set_otx2inx("Bob", "Bob of Salem")
#     sue_jargonunit.set_ropeyap(static_x_ropeyap)

#     # WHEN
#     gen_x_ropeyap = sue_jargonunit.get_ropeyap()

#     # THEN
#     assert gen_x_ropeyap == static_x_ropeyap


# def test_JargonUnit_set_rope_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeid_ropeyap = zia_jargonunit.get_ropeyap()
#     assert ropeid_ropeyap.otx2inx_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_rope(sue_otx, sue_inx)

#     # THEN
#     assert ropeid_ropeyap.otx2inx_exists(sue_otx, sue_inx)


# def test_JargonUnit_rope_exists_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     assert zia_jargonunit.rope_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_rope(sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit.rope_exists(sue_otx, sue_inx)


# def test_JargonUnit_get_inx_rope_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit._get_inx_rope(sue_otx) != sue_inx

#     # WHEN
#     zia_jargonunit.set_rope(sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit._get_inx_rope(sue_otx) == sue_inx


# def test_JargonUnit_del_rope_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_rope(sue_otx, sue_inx)
#     zia_jargonunit.set_rope(exx.zia, exx.zia)
#     assert zia_jargonunit.rope_exists(sue_otx, sue_inx)
#     assert zia_jargonunit.rope_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_rope(sue_otx)

#     # THEN
#     assert zia_jargonunit.rope_exists(sue_otx, sue_inx) is False
#     assert zia_jargonunit.rope_exists(exx.zia, exx.zia)
