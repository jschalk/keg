# from ch17_jargon.yap_term import nameyap_shop, ropeyap_shop
# from ch17_jargon.test._util.ch17_examples import (
#     get_bowl_titleyap,
#     get_clean_ropeyap,
#     get_invalid_nameyap,
#     get_invalid_ropeyap,
#     get_invalid_titleyap,
#     get_suita_nameyap,
# )
# from ch17_jargon.jargon_main import jargonunit_shop
# from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_set_yapunit_SetsAttr():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     nameyap = nameyap_shop(spark_face=exx.sue)
#     nameyap.set_otx2inx("Bob", "Bob of Salem")
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN
#     sue_jargonunit.set_nameyap(nameyap)

#     # THEN
#     assert sue_jargonunit.nameyap == nameyap


# def test_JargonUnit_set_yapunit_SetsAttr_SpecialSituation_RopeTerm():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     ropeyap = ropeyap_shop(spark_face=exx.sue)
#     ropeyap.set_otx2inx("Bob", "Bob of Salem")
#     assert sue_jargonunit.ropeyap != ropeyap

#     # WHEN
#     sue_jargonunit.set_ropeyap(ropeyap)

#     # THEN
#     assert sue_jargonunit.ropeyap == ropeyap


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_otx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_otx_knot = "/"
#     nameyap = nameyap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.otx_knot != nameyap.otx_knot
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', YapCore is '{slash_otx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_inx_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_inx_knot = "/"
#     nameyap = nameyap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
#     assert sue_jargonunit.inx_knot != nameyap.inx_knot
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', YapCore is '{slash_inx_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     nameyap = nameyap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
#     assert sue_jargonunit.unknown_str != nameyap.unknown_str
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_spark_face_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     nameyap = nameyap_shop(spark_face=exx.yao)
#     assert sue_jargonunit.spark_face != nameyap.spark_face
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_yapunit_ReturnsObj():
#     # ESTABLISH
#     sue_pu = jargonunit_shop(exx.sue)
#     static_nameyap = nameyap_shop(spark_face=exx.sue)
#     static_nameyap.set_otx2inx("Bob", "Bob of Salem")
#     sue_pu.set_nameyap(static_nameyap)

#     # WHEN / THEN
#     assert sue_pu.get_yapunit(kw.NameTerm) == sue_pu.nameyap
#     assert sue_pu.get_yapunit(kw.TitleTerm) == sue_pu.titleyap
#     assert sue_pu.get_yapunit(kw.LabelTerm) == sue_pu.labelyap
#     assert sue_pu.get_yapunit(kw.RopeTerm) == sue_pu.ropeyap
#     assert not sue_pu.get_yapunit("testing")

#     assert sue_pu.get_yapunit(kw.NameTerm) != sue_pu.ropeyap
#     assert sue_pu.get_yapunit(kw.TitleTerm) != sue_pu.ropeyap
#     assert sue_pu.get_yapunit(kw.LabelTerm) != sue_pu.ropeyap


# def test_JargonUnit_is_valid_ReturnsObj():
#     # ESTABLISH
#     invalid_nameyap = get_invalid_nameyap()
#     invalid_titleyap = get_invalid_titleyap()
#     invalid_labelyap = get_invalid_ropeyap()
#     valid_nameyap = get_suita_nameyap()
#     valid_titleyap = get_bowl_titleyap()
#     valid_labelyap = get_clean_ropeyap()
#     assert valid_nameyap.is_valid()
#     assert valid_titleyap.is_valid()
#     assert valid_labelyap.is_valid()
#     assert invalid_labelyap.is_valid() is False
#     assert invalid_titleyap.is_valid() is False
#     assert invalid_nameyap.is_valid() is False

#     # WHEN / THEN
#     sue_jargonunit = jargonunit_shop("Sue")
#     assert sue_jargonunit.is_valid()
#     sue_jargonunit.set_nameyap(valid_nameyap)
#     sue_jargonunit.set_titleyap(valid_titleyap)
#     sue_jargonunit.set_ropeyap(valid_labelyap)
#     assert sue_jargonunit.is_valid()

#     # WHEN / THEN
#     sue_jargonunit.set_nameyap(invalid_nameyap)
#     assert sue_jargonunit.is_valid() is False
#     sue_jargonunit.set_nameyap(valid_nameyap)
#     assert sue_jargonunit.is_valid()

#     # WHEN / THEN
#     sue_jargonunit.set_titleyap(invalid_titleyap)
#     assert sue_jargonunit.is_valid() is False
#     sue_jargonunit.set_titleyap(valid_titleyap)
#     assert sue_jargonunit.is_valid()

#     # WHEN / THEN
#     sue_jargonunit.set_ropeyap(invalid_labelyap)
#     assert sue_jargonunit.is_valid() is False
#     sue_jargonunit.set_ropeyap(valid_labelyap)
#     assert sue_jargonunit.is_valid()


# def test_JargonUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     nameyap = zia_jargonunit.get_nameyap()
#     assert nameyap.otx2inx_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

#     # THEN
#     assert nameyap.otx2inx_exists(sue_otx, sue_inx)


# def test_JargonUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeyap = zia_jargonunit.get_ropeyap()
#     assert ropeyap.otx2inx_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_otx2inx(kw.RopeTerm, sue_otx, sue_inx)

#     # THEN
#     assert ropeyap.otx2inx_exists(sue_otx, sue_inx)


# def test_JargonUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeyap = zia_jargonunit.get_labelyap()
#     assert ropeyap.otx2inx_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

#     # THEN
#     assert ropeyap.otx2inx_exists(sue_otx, sue_inx)


# def test_JargonUnit_otx2inx_exists_ReturnsObj_Scenario0_LabelTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     rope_type = kw.LabelTerm
#     assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


# def test_JargonUnit_get_inx_value_ReturnsObj_Scenario0_NameTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit.get_inx_value(kw.NameTerm, sue_otx) != sue_inx

#     # WHEN
#     zia_jargonunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit.get_inx_value(kw.NameTerm, sue_otx) == sue_inx


# def test_JargonUnit_del_otx2inx_ReturnsObj_Scenario0_LabelTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     rope_type = kw.LabelTerm
#     zia_jargonunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)
#     zia_jargonunit.set_otx2inx(kw.LabelTerm, exx.zia, exx.zia)
#     assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
#     assert zia_jargonunit.otx2inx_exists(rope_type, exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_otx2inx(rope_type, sue_otx)

#     # THEN
#     assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
#     assert zia_jargonunit.otx2inx_exists(rope_type, exx.zia, exx.zia)


# def test_JargonUnit_set_roadyap_label_SetsAttr_Scenario1_RopeTerm():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeyap = zia_jargonunit.get_ropeyap()
#     assert ropeyap.label_exists(sue_otx, sue_inx) is False

#     # WHEN
#     zia_jargonunit.set_roadyap_label(sue_otx, sue_inx)

#     # THEN
#     assert ropeyap.label_exists(sue_otx, sue_inx)


# def test_JargonUnit_roadyap_label_exists_ReturnsObj():
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     sue_exists = zia_jargonunit.roadyap_label_exists(sue_otx, sue_inx)
#     assert sue_exists is False

#     # WHEN
#     zia_jargonunit.set_roadyap_label(sue_otx, sue_inx)

#     # THEN
#     assert zia_jargonunit.roadyap_label_exists(sue_otx, sue_inx)
