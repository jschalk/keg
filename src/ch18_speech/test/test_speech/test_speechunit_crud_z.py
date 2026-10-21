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
#     nameyap = nameyap_shop(flare_audie=exx.sue)
#     nameyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_jargonunit.nameyap != nameyap
#     # WHEN
#     sue_jargonunit.set_nameyap(nameyap)

#     # THEN
#     assert sue_jargonunit.nameyap == nameyap


# def test_JargonUnit_set_yapunit_SetsAttr_SpecialSituation_RopeTerm():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     ropeyap = ropeyap_shop(flare_audie=exx.sue)
#     ropeyap.set_iux2aux("Bob", "Bob of Salem")
#     assert sue_jargonunit.ropeyap != ropeyap

#     # WHEN
#     sue_jargonunit.set_ropeyap(ropeyap)

#     # THEN
#     assert sue_jargonunit.ropeyap == ropeyap


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_iux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_iux_knot = "/"
#     nameyap = nameyap_shop(iux_knot=slash_iux_knot, flare_audie=exx.sue)
#     assert sue_jargonunit.iux_knot != nameyap.iux_knot
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit iux_knot is '{sue_jargonunit.iux_knot}', YapCore is '{slash_iux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_aux_knot_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     slash_aux_knot = "/"
#     nameyap = nameyap_shop(aux_knot=slash_aux_knot, flare_audie=exx.sue)
#     assert sue_jargonunit.aux_knot != nameyap.aux_knot
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit aux_knot is '{sue_jargonunit.aux_knot}', YapCore is '{slash_aux_knot}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_unknown_str_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     casa_unknown_str = "Unknown_casa"
#     nameyap = nameyap_shop(unknown_str=casa_unknown_str, flare_audie=exx.sue)
#     assert sue_jargonunit.unknown_str != nameyap.unknown_str
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', YapCore is '{casa_unknown_str}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_set_yapunit_RaisesErrorIf_yapunit_flare_audie_IsNotSame():
#     # ESTABLISH
#     sue_jargonunit = jargonunit_shop(exx.sue)
#     nameyap = nameyap_shop(flare_audie=exx.yao)
#     assert sue_jargonunit.flare_audie != nameyap.flare_audie
#     assert sue_jargonunit.nameyap != nameyap

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         sue_jargonunit.set_nameyap(nameyap)
#     exception_str = f"set_yapcore Error: JargonUnit flare_audie is '{sue_jargonunit.flare_audie}', YapCore is '{exx.yao}'."
#     assert str(excinfo.value) == exception_str


# def test_JargonUnit_get_yapunit_ReturnsObj():
#     # ESTABLISH
#     sue_pu = jargonunit_shop(exx.sue)
#     static_nameyap = nameyap_shop(flare_audie=exx.sue)
#     static_nameyap.set_iux2aux("Bob", "Bob of Salem")
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


# def test_JargonUnit_set_iux2aux_SetsAttr_Scenario0_NameTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     nameyap = zia_jargonunit.get_nameyap()
#     assert nameyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_iux2aux(kw.NameTerm, sue_iux, sue_aux)

#     # THEN
#     assert nameyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_set_iux2aux_SetsAttr_Scenario1_RopeTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeyap = zia_jargonunit.get_ropeyap()
#     assert ropeyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_iux2aux(kw.RopeTerm, sue_iux, sue_aux)

#     # THEN
#     assert ropeyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_set_iux2aux_SetsAttr_Scenario2_LabelTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeyap = zia_jargonunit.get_labelyap()
#     assert ropeyap.iux2aux_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_iux2aux(kw.LabelTerm, sue_iux, sue_aux)

#     # THEN
#     assert ropeyap.iux2aux_exists(sue_iux, sue_aux)


# def test_JargonUnit_iux2aux_exists_ReturnsObj_Scenario0_LabelTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     rope_type = kw.LabelTerm
#     assert zia_jargonunit.iux2aux_exists(rope_type, sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_iux2aux(kw.LabelTerm, sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit.iux2aux_exists(rope_type, sue_iux, sue_aux)


# def test_JargonUnit_get_aux_value_ReturnsObj_Scenario0_NameTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     assert zia_jargonunit.get_aux_value(kw.NameTerm, sue_iux) != sue_aux

#     # WHEN
#     zia_jargonunit.set_iux2aux(kw.NameTerm, sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit.get_aux_value(kw.NameTerm, sue_iux) == sue_aux


# def test_JargonUnit_del_iux2aux_ReturnsObj_Scenario0_LabelTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     rope_type = kw.LabelTerm
#     zia_jargonunit.set_iux2aux(kw.LabelTerm, sue_iux, sue_aux)
#     zia_jargonunit.set_iux2aux(kw.LabelTerm, exx.zia, exx.zia)
#     assert zia_jargonunit.iux2aux_exists(rope_type, sue_iux, sue_aux)
#     assert zia_jargonunit.iux2aux_exists(rope_type, exx.zia, exx.zia)

#     # WHEN
#     zia_jargonunit.del_iux2aux(rope_type, sue_iux)

#     # THEN
#     assert zia_jargonunit.iux2aux_exists(rope_type, sue_iux, sue_aux) is False
#     assert zia_jargonunit.iux2aux_exists(rope_type, exx.zia, exx.zia)


# def test_JargonUnit_set_roadyap_label_SetsAttr_Scenario1_RopeTerm():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     ropeyap = zia_jargonunit.get_ropeyap()
#     assert ropeyap.label_exists(sue_iux, sue_aux) is False

#     # WHEN
#     zia_jargonunit.set_roadyap_label(sue_iux, sue_aux)

#     # THEN
#     assert ropeyap.label_exists(sue_iux, sue_aux)


# def test_JargonUnit_roadyap_label_exists_ReturnsObj():
#     # ESTABLISH
#     sue_iux = "Sue"
#     sue_aux = "Suita"
#     zia_jargonunit = jargonunit_shop(exx.zia)
#     sue_exists = zia_jargonunit.roadyap_label_exists(sue_iux, sue_aux)
#     assert sue_exists is False

#     # WHEN
#     zia_jargonunit.set_roadyap_label(sue_iux, sue_aux)

#     # THEN
#     assert zia_jargonunit.roadyap_label_exists(sue_iux, sue_aux)
