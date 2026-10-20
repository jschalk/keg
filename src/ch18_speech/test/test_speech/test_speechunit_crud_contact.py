# from ch17_jargon.yap_term import nameyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_nameyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_nameyap = nameyap_shop(spark_face=exx.sue)
#     x_nameyap.set_otx2inx("Bob", "Bob of Salem")
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN
#     sue_jargonunit.set_nameyap(x_nameyap)

#     # THEN
#     assert sue_jargonunit.nameyap == x_nameyap


# def test_JargonUnit_set_nameyap_SetsAttrWhenAttrIs_float_nan():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_nan = float("nan")
#     x_nameyap = nameyap_shop(
#         spark_face=exx.sue, otx_knot=x_nan, inx_knot=x_nan, unknown_str=x_nan
#     )
#     x_nameyap.set_otx2inx("Bob", "Bob of Salem")
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN
#     sue_jargonunit.set_nameyap(x_nameyap)

#     # THEN
#     assert sue_jargonunit.nameyap == x_nameyap


# def test_JargonUnit_set_nameyap_RaisesErrorIf_nameyap_otx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_otx_knot = "/"
#     x_nameyap = nameyap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.otx_knot != x_nameyap.otx_knot
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(x_nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', YapCore is '{slash_otx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_nameyap_RaisesErrorIf_nameyap_inx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_inx_knot = "/"
#     x_nameyap = nameyap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.inx_knot != x_nameyap.inx_knot
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(x_nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', YapCore is '{slash_inx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_nameyap_RaisesErrorIf_nameyap_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     x_nameyap = nameyap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
#     assert sue_jargonunit.unknown_str != x_nameyap.unknown_str
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(x_nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_nameyap_RaisesErrorIf_nameyap_spark_face_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_nameyap = nameyap_shop(spark_face=exx.yao)
#     assert sue_jargonunit.spark_face != x_nameyap.spark_face
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(x_nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_nameyap_ReturnsObj():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     static_x_nameyap = nameyap_shop(spark_face=exx.sue)
#     static_x_nameyap.set_otx2inx("Bob", "Bob of Salem")
#     sue_jargonunit.set_nameyap(static_x_nameyap)

#     # WHEN
#     gen_x_nameyap = sue_jargonunit.get_nameyap()

#     # THEN
#     assert gen_x_nameyap == static_x_nameyap


# def test_JargonUnit_set_nameterm_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     contact_name_nameyap = zia_jargonunit.get_nameyap()
#     assert contact_name_nameyap.otx2inx_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_nameterm(sue_otx, sue_inx)

#     # THEN
#     assert contact_name_nameyap.otx2inx_exists(sue_otx, sue_inx)


# def test_JargonUnit_nameterm_exists_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     assert zia_jargonunit.nameterm_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_nameterm(sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit.nameterm_exists(sue_otx, sue_inx)


# def test_JargonUnit_get_inx_name_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit._get_inx_name(sue_otx) != sue_inx

#     # WHEN
#     zia_jargonunit.set_nameterm(sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit._get_inx_name(sue_otx) == sue_inx


# def test_JargonUnit_del_nameterm_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_nameterm(sue_otx, sue_inx)
#     zia_jargonunit.set_nameterm(exx.zia, exx.zia)
#     assert zia_jargonunit.nameterm_exists(sue_otx, sue_inx)
#     assert zia_jargonunit.nameterm_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_nameterm(sue_otx)

#     # THEN
#     assert zia_jargonunit.nameterm_exists(sue_otx, sue_inx) is False
#     assert zia_jargonunit.nameterm_exists(exx.zia, exx.zia)
