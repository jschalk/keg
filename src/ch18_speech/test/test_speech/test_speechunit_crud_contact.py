# from ch17_jargon.yap_term import nameyap_shop
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_nameyap_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     x_nameyap = nameyap_shop(spark_face=exx.sue)
#     x_nameyap.set_iux2aux("Bob", "Bob of Salem")
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
#         spark_face=exx.sue, iux_knot=x_nan, aux_knot=x_nan, unknown_str=x_nan
#     )
#     x_nameyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN
#     sue_jargonunit.set_nameyap(x_nameyap)

#     # THEN
#     assert sue_jargonunit.nameyap == x_nameyap


# def test_JargonUnit_set_nameyap_RaisesErrorIf_nameyap_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     x_nameyap = nameyap_shop(iux_knot=slash_iux_knot, spark_face=exx.sue)
#     assert sue_jargonunit.iux_knot != x_nameyap.iux_knot
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(x_nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit iux_knot is '{sue_jargonunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_nameyap_RaisesErrorIf_nameyap_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     x_nameyap = nameyap_shop(aux_knot=slash_aux_knot, spark_face=exx.sue)
#     assert sue_jargonunit.aux_knot != x_nameyap.aux_knot
#     assert sue_jargonunit.nameyap != x_nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(x_nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit aux_knot is '{sue_jargonunit.aux_knot}', YapCore is '{slash_aux_knot}'."
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
#     static_x_nameyap.set_iux2aux("Bob", "Bob of Salem")
#     sue_jargonunit.set_nameyap(static_x_nameyap)

#     # WHEN
#     gen_x_nameyap = sue_jargonunit.get_nameyap()

#     # THEN
#     assert gen_x_nameyap == static_x_nameyap


# def test_JargonUnit_set_nameterm_SetsAttr_Scenario0():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     contact_name_nameyap = zia_jargonunit.get_nameyap()
#     assert contact_name_nameyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_nameterm(sue_iux, sue_aux)

#     # THEN
#     assert contact_name_nameyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_nameterm_exists_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     assert zia_jargonunit.nameterm_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_nameterm(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit.nameterm_exists(sue_iux, sue_aux)


# def test_JargonUnit_get_aux_name_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit._get_aux_name(sue_iux) != sue_aux

#     # WHEN
#     zia_jargonunit.set_nameterm(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit._get_aux_name(sue_iux) == sue_aux


# def test_JargonUnit_del_nameterm_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)

#     zia_jargonunit.set_nameterm(sue_iux, sue_aux)
#     zia_jargonunit.set_nameterm(exx.zia, exx.zia)
#     assert zia_jargonunit.nameterm_exists(sue_iux, sue_aux)
#     assert zia_jargonunit.nameterm_exists(exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_nameterm(sue_iux)

#     # THEN
#     assert zia_jargonunit.nameterm_exists(sue_iux, sue_aux) is False
#     assert zia_jargonunit.nameterm_exists(exx.zia, exx.zia)
