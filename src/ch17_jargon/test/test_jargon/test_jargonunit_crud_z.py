from ch17_jargon.map_term import namemap_shop, ropemap_shop
from ch17_jargon.test._util.ch17_examples import (
    get_bowl_titlemap,
    get_clean_ropemap,
    get_invalid_namemap,
    get_invalid_ropemap,
    get_invalid_titlemap,
    get_suita_namemap,
)
from ch17_jargon.jargon_main import jargonunit_shop
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
from pytest import raises as pytest_raises


def test_JargonUnit_set_mapunit_SetsAttr():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    namemap = namemap_shop(spark_face=exx.sue)
    namemap.set_otx2inx("Bob", "Bob of Salem")
    assert sue_jargonunit.namemap != namemap

    # WHEN
    sue_jargonunit.set_namemap(namemap)

    # THEN
    assert sue_jargonunit.namemap == namemap


def test_JargonUnit_set_mapunit_SetsAttr_SpecialSituation_RopeTerm():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    ropemap = ropemap_shop(spark_face=exx.sue)
    ropemap.set_otx2inx("Bob", "Bob of Salem")
    assert sue_jargonunit.ropemap != ropemap

    # WHEN
    sue_jargonunit.set_ropemap(ropemap)

    # THEN
    assert sue_jargonunit.ropemap == ropemap


def test_JargonUnit_set_mapunit_RaisesErrorIf_mapunit_otx_knot_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    slash_otx_knot = "/"
    namemap = namemap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_jargonunit.otx_knot != namemap.otx_knot
    assert sue_jargonunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_mapunit_RaisesErrorIf_mapunit_inx_knot_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    slash_inx_knot = "/"
    namemap = namemap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_jargonunit.inx_knot != namemap.inx_knot
    assert sue_jargonunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_str_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    namemap = namemap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_jargonunit.unknown_str != namemap.unknown_str
    assert sue_jargonunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_mapunit_RaisesErrorIf_mapunit_spark_face_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    namemap = namemap_shop(spark_face=exx.yao)
    assert sue_jargonunit.spark_face != namemap.spark_face
    assert sue_jargonunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_pu = jargonunit_shop(exx.sue)
    static_namemap = namemap_shop(spark_face=exx.sue)
    static_namemap.set_otx2inx("Bob", "Bob of Salem")
    sue_pu.set_namemap(static_namemap)

    # WHEN / THEN
    assert sue_pu.get_mapunit(kw.NameTerm) == sue_pu.namemap
    assert sue_pu.get_mapunit(kw.TitleTerm) == sue_pu.titlemap
    assert sue_pu.get_mapunit(kw.LabelTerm) == sue_pu.labelmap
    assert sue_pu.get_mapunit(kw.RopeTerm) == sue_pu.ropemap
    assert not sue_pu.get_mapunit("testing")

    assert sue_pu.get_mapunit(kw.NameTerm) != sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.TitleTerm) != sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.LabelTerm) != sue_pu.ropemap


def test_JargonUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_namemap = get_invalid_namemap()
    invalid_titlemap = get_invalid_titlemap()
    invalid_labelmap = get_invalid_ropemap()
    valid_namemap = get_suita_namemap()
    valid_titlemap = get_bowl_titlemap()
    valid_labelmap = get_clean_ropemap()
    assert valid_namemap.is_valid()
    assert valid_titlemap.is_valid()
    assert valid_labelmap.is_valid()
    assert invalid_labelmap.is_valid() is False
    assert invalid_titlemap.is_valid() is False
    assert invalid_namemap.is_valid() is False

    # WHEN / THEN
    sue_jargonunit = jargonunit_shop("Sue")
    assert sue_jargonunit.is_valid()
    sue_jargonunit.set_namemap(valid_namemap)
    sue_jargonunit.set_titlemap(valid_titlemap)
    sue_jargonunit.set_ropemap(valid_labelmap)
    assert sue_jargonunit.is_valid()

    # WHEN / THEN
    sue_jargonunit.set_namemap(invalid_namemap)
    assert sue_jargonunit.is_valid() is False
    sue_jargonunit.set_namemap(valid_namemap)
    assert sue_jargonunit.is_valid()

    # WHEN / THEN
    sue_jargonunit.set_titlemap(invalid_titlemap)
    assert sue_jargonunit.is_valid() is False
    sue_jargonunit.set_titlemap(valid_titlemap)
    assert sue_jargonunit.is_valid()

    # WHEN / THEN
    sue_jargonunit.set_ropemap(invalid_labelmap)
    assert sue_jargonunit.is_valid() is False
    sue_jargonunit.set_ropemap(valid_labelmap)
    assert sue_jargonunit.is_valid()


def test_JargonUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    namemap = zia_jargonunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_JargonUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    ropemap = zia_jargonunit.get_ropemap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_otx2inx(kw.RopeTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_JargonUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    ropemap = zia_jargonunit.get_labelmap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_JargonUnit_otx2inx_exists_ReturnsObj_Scenario0_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    rope_type = kw.LabelTerm
    assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


def test_JargonUnit_get_inx_value_ReturnsObj_Scenario0_NameTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    assert zia_jargonunit.get_inx_value(kw.NameTerm, sue_otx) != sue_inx

    # WHEN
    zia_jargonunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert zia_jargonunit.get_inx_value(kw.NameTerm, sue_otx) == sue_inx


def test_JargonUnit_del_otx2inx_ReturnsObj_Scenario0_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    rope_type = kw.LabelTerm
    zia_jargonunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)
    zia_jargonunit.set_otx2inx(kw.LabelTerm, exx.zia, exx.zia)
    assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
    assert zia_jargonunit.otx2inx_exists(rope_type, exx.zia, exx.zia)

    # WHEN
    zia_jargonunit.del_otx2inx(rope_type, sue_otx)

    # THEN
    assert zia_jargonunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
    assert zia_jargonunit.otx2inx_exists(rope_type, exx.zia, exx.zia)


def test_JargonUnit_set_roadmap_label_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    ropemap = zia_jargonunit.get_ropemap()
    assert ropemap.label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert ropemap.label_exists(sue_otx, sue_inx)


def test_JargonUnit_roadmap_label_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    sue_exists = zia_jargonunit.roadmap_label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_jargonunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert zia_jargonunit.roadmap_label_exists(sue_otx, sue_inx)
