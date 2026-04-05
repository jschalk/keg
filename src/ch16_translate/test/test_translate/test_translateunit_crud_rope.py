from pytest import raises as pytest_raises
from src.ch16_translate.map_term import ropemap_shop
from src.ch16_translate.translate_main import translateunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_TranslateUnit_set_ropemap_SetsAttr():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    x_ropemap = ropemap_shop(spark_face=exx.sue)
    x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN
    sue_translateunit.set_ropemap(x_ropemap)

    # THEN
    assert sue_translateunit.ropemap == x_ropemap


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_translateunit.otx_knot != x_ropemap.otx_knot
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_ropemap = ropemap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_translateunit.inx_knot != x_ropemap.inx_knot
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_ropemap = ropemap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_translateunit.unknown_str != x_ropemap.unknown_str
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_ropemap_RaisesErrorIf_ropemap_spark_face_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    x_ropemap = ropemap_shop(spark_face=exx.yao)
    assert sue_translateunit.spark_face != x_ropemap.spark_face
    assert sue_translateunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: TranslateUnit spark_face is '{sue_translateunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_ropemap_ReturnsObj():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    static_x_ropemap = ropemap_shop(spark_face=exx.sue)
    static_x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    sue_translateunit.set_ropemap(static_x_ropemap)

    # WHEN
    gen_x_ropemap = sue_translateunit.get_ropemap()

    # THEN
    assert gen_x_ropemap == static_x_ropemap


def test_TranslateUnit_set_rope_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    ropeid_ropemap = zia_translateunit.get_ropemap()
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_rope_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)

    assert zia_translateunit.rope_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.rope_exists(sue_otx, sue_inx)


def test_TranslateUnit_get_inx_rope_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    assert zia_translateunit._get_inx_rope(sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit._get_inx_rope(sue_otx) == sue_inx


def test_TranslateUnit_del_rope_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)

    zia_translateunit.set_rope(sue_otx, sue_inx)
    zia_translateunit.set_rope(exx.zia, exx.zia)
    assert zia_translateunit.rope_exists(sue_otx, sue_inx)
    assert zia_translateunit.rope_exists(exx.zia, exx.zia)

    # WHEN
    zia_translateunit.del_rope(sue_otx)

    # THEN
    assert zia_translateunit.rope_exists(sue_otx, sue_inx) is False
    assert zia_translateunit.rope_exists(exx.zia, exx.zia)
