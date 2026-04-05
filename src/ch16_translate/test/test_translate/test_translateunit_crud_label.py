from pytest import raises as pytest_raises
from src.ch16_translate.map_term import labelmap_shop
from src.ch16_translate.translate_main import translateunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_TranslateUnit_set_labelmap_SetsAttr():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    x_labelmap = labelmap_shop(spark_face=exx.sue)
    x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN
    sue_translateunit.set_labelmap(x_labelmap)

    # THEN
    assert sue_translateunit.labelmap == x_labelmap


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_labelmap = labelmap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_translateunit.otx_knot != x_labelmap.otx_knot
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_labelmap = labelmap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_translateunit.inx_knot != x_labelmap.inx_knot
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_labelmap = labelmap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_translateunit.unknown_str != x_labelmap.unknown_str
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_labelmap_RaisesErrorIf_labelmap_spark_face_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    x_labelmap = labelmap_shop(spark_face=exx.yao)
    assert sue_translateunit.spark_face != x_labelmap.spark_face
    assert sue_translateunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: TranslateUnit spark_face is '{sue_translateunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_labelmap_ReturnsObj():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    static_x_labelmap = labelmap_shop(spark_face=exx.sue)
    static_x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    sue_translateunit.set_labelmap(static_x_labelmap)

    # WHEN
    gen_x_labelmap = sue_translateunit.get_labelmap()

    # THEN
    assert gen_x_labelmap == static_x_labelmap


def test_TranslateUnit_set_label_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    labelid_labelmap = zia_translateunit.get_labelmap()
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_del_roadmap_label_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)

    zia_translateunit.set_roadmap_label(sue_otx, sue_inx)
    zia_translateunit.set_roadmap_label(exx.zia, exx.zia)
    assert zia_translateunit.roadmap_label_exists(sue_otx, sue_inx)
    assert zia_translateunit.roadmap_label_exists(exx.zia, exx.zia)

    # WHEN
    zia_translateunit.del_roadmap_label(sue_otx)

    # THEN
    assert zia_translateunit.roadmap_label_exists(sue_otx, sue_inx) is False
    assert zia_translateunit.roadmap_label_exists(exx.zia, exx.zia)
