from pytest import raises as pytest_raises
from src.ch16_translate.map_term import namemap_shop, ropemap_shop
from src.ch16_translate.test._util.ch16_examples import (
    get_bowl_titlemap,
    get_clean_ropemap,
    get_invalid_namemap,
    get_invalid_ropemap,
    get_invalid_titlemap,
    get_suita_namemap,
)
from src.ch16_translate.translate_main import translateunit_shop
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_TranslateUnit_set_mapunit_SetsAttr():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    namemap = namemap_shop(spark_face=exx.sue)
    namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.namemap != namemap

    # WHEN
    sue_translateunit.set_namemap(namemap)

    # THEN
    assert sue_translateunit.namemap == namemap


def test_TranslateUnit_set_mapunit_SetsAttr_SpecialSituation_RopeTerm():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    ropemap = ropemap_shop(spark_face=exx.sue)
    ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.ropemap != ropemap

    # WHEN
    sue_translateunit.set_ropemap(ropemap)

    # THEN
    assert sue_translateunit.ropemap == ropemap


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_otx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_otx_knot = "/"
    namemap = namemap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_translateunit.otx_knot != namemap.otx_knot
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_inx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_inx_knot = "/"
    namemap = namemap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_translateunit.inx_knot != namemap.inx_knot
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_str_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    namemap = namemap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_translateunit.unknown_str != namemap.unknown_str
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_mapunit_RaisesErrorIf_mapunit_spark_face_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    namemap = namemap_shop(spark_face=exx.yao)
    assert sue_translateunit.spark_face != namemap.spark_face
    assert sue_translateunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: TranslateUnit spark_face is '{sue_translateunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_pu = translateunit_shop(exx.sue)
    static_namemap = namemap_shop(spark_face=exx.sue)
    static_namemap.set_otx2inx("Bob", "Bob of Portland")
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


def test_TranslateUnit_is_valid_ReturnsObj():
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
    sue_translateunit = translateunit_shop("Sue")
    assert sue_translateunit.is_valid()
    sue_translateunit.set_namemap(valid_namemap)
    sue_translateunit.set_titlemap(valid_titlemap)
    sue_translateunit.set_ropemap(valid_labelmap)
    assert sue_translateunit.is_valid()

    # WHEN / THEN
    sue_translateunit.set_namemap(invalid_namemap)
    assert sue_translateunit.is_valid() is False
    sue_translateunit.set_namemap(valid_namemap)
    assert sue_translateunit.is_valid()

    # WHEN / THEN
    sue_translateunit.set_titlemap(invalid_titlemap)
    assert sue_translateunit.is_valid() is False
    sue_translateunit.set_titlemap(valid_titlemap)
    assert sue_translateunit.is_valid()

    # WHEN / THEN
    sue_translateunit.set_ropemap(invalid_labelmap)
    assert sue_translateunit.is_valid() is False
    sue_translateunit.set_ropemap(valid_labelmap)
    assert sue_translateunit.is_valid()


def test_TranslateUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    namemap = zia_translateunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    ropemap = zia_translateunit.get_ropemap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.RopeTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    ropemap = zia_translateunit.get_labelmap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_otx2inx_exists_ReturnsObj_Scenario0_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    rope_type = kw.LabelTerm
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


def test_TranslateUnit_get_inx_value_ReturnsObj_Scenario0_NameTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    assert zia_translateunit.get_inx_value(kw.NameTerm, sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.get_inx_value(kw.NameTerm, sue_otx) == sue_inx


def test_TranslateUnit_del_otx2inx_ReturnsObj_Scenario0_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    rope_type = kw.LabelTerm
    zia_translateunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)
    zia_translateunit.set_otx2inx(kw.LabelTerm, exx.zia, exx.zia)
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
    assert zia_translateunit.otx2inx_exists(rope_type, exx.zia, exx.zia)

    # WHEN
    zia_translateunit.del_otx2inx(rope_type, sue_otx)

    # THEN
    assert zia_translateunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
    assert zia_translateunit.otx2inx_exists(rope_type, exx.zia, exx.zia)


def test_TranslateUnit_set_roadmap_label_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    ropemap = zia_translateunit.get_ropemap()
    assert ropemap.label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert ropemap.label_exists(sue_otx, sue_inx)


def test_TranslateUnit_roadmap_label_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    sue_exists = zia_translateunit.roadmap_label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_translateunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.roadmap_label_exists(sue_otx, sue_inx)
