from pytest import raises as pytest_raises
from src.ch16_translate.map_term import titlemap_shop
from src.ch16_translate.translate_main import translateunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_TranslateUnit_set_titlemap_SetsAttr():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    x_titlemap = titlemap_shop(spark_face=exx.sue)
    x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_translateunit.titlemap != x_titlemap

    # WHEN
    sue_translateunit.set_titlemap(x_titlemap)

    # THEN
    assert sue_translateunit.titlemap == x_titlemap


def test_TranslateUnit_set_titlemap_RaisesErrorIf_titlemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_titlemap = titlemap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_translateunit.otx_knot != x_titlemap.otx_knot
    assert sue_translateunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: TranslateUnit otx_knot is '{sue_translateunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_titlemap_RaisesErrorIf_titlemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_titlemap = titlemap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_translateunit.inx_knot != x_titlemap.inx_knot
    assert sue_translateunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: TranslateUnit inx_knot is '{sue_translateunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_titlemap_RaisesErrorIf_titlemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_titlemap = titlemap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_translateunit.unknown_str != x_titlemap.unknown_str
    assert sue_translateunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: TranslateUnit unknown_str is '{sue_translateunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_set_titlemap_RaisesErrorIf_titlemap_spark_face_IsNotSame():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    x_titlemap = titlemap_shop(spark_face=exx.yao)
    assert sue_translateunit.spark_face != x_titlemap.spark_face
    assert sue_translateunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_translateunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: TranslateUnit spark_face is '{sue_translateunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_TranslateUnit_get_titlemap_ReturnsObj():
    # ESTABLISH
    sue_translateunit = translateunit_shop(exx.sue)
    static_x_titlemap = titlemap_shop(spark_face=exx.sue)
    static_x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    sue_translateunit.set_titlemap(static_x_titlemap)

    # WHEN
    gen_x_titlemap = sue_translateunit.get_titlemap()

    # THEN
    assert gen_x_titlemap == static_x_titlemap


def test_TranslateUnit_set_titleterm_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    contact_name_titlemap = zia_translateunit.get_titlemap()
    assert contact_name_titlemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert contact_name_titlemap.otx2inx_exists(sue_otx, sue_inx)


def test_TranslateUnit_titleterm_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)

    assert zia_translateunit.titleterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_translateunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit.titleterm_exists(sue_otx, sue_inx)


def test_TranslateUnit_get_inx_title_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)
    assert zia_translateunit._get_inx_title(sue_otx) != sue_inx

    # WHEN
    zia_translateunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_translateunit._get_inx_title(sue_otx) == sue_inx


def test_TranslateUnit_del_titleterm_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_translateunit = translateunit_shop(exx.zia)

    zia_translateunit.set_titleterm(sue_otx, sue_inx)
    zia_translateunit.set_titleterm(exx.zia, exx.zia)
    assert zia_translateunit.titleterm_exists(sue_otx, sue_inx)
    assert zia_translateunit.titleterm_exists(exx.zia, exx.zia)

    # WHEN
    zia_translateunit.del_titleterm(sue_otx)

    # THEN
    assert zia_translateunit.titleterm_exists(sue_otx, sue_inx) is False
    assert zia_translateunit.titleterm_exists(exx.zia, exx.zia)
