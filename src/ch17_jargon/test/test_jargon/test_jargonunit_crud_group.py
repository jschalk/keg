from ch17_jargon.map_term import titlemap_shop
from ch17_jargon.jargon_main import jargonunit_shop
from ch99_glossary.ch_keyword import ExampleStrs as exx
from pytest import raises as pytest_raises


def test_JargonUnit_set_titlemap_SetsAttr():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    x_titlemap = titlemap_shop(spark_face=exx.sue)
    x_titlemap.set_otx2inx("Bob", "Bob of Salem")
    assert sue_jargonunit.titlemap != x_titlemap

    # WHEN
    sue_jargonunit.set_titlemap(x_titlemap)

    # THEN
    assert sue_jargonunit.titlemap == x_titlemap


def test_JargonUnit_set_titlemap_RaisesErrorIf_titlemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_titlemap = titlemap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_jargonunit.otx_knot != x_titlemap.otx_knot
    assert sue_jargonunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_titlemap_RaisesErrorIf_titlemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_titlemap = titlemap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_jargonunit.inx_knot != x_titlemap.inx_knot
    assert sue_jargonunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_titlemap_RaisesErrorIf_titlemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_titlemap = titlemap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_jargonunit.unknown_str != x_titlemap.unknown_str
    assert sue_jargonunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_titlemap_RaisesErrorIf_titlemap_spark_face_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    x_titlemap = titlemap_shop(spark_face=exx.yao)
    assert sue_jargonunit.spark_face != x_titlemap.spark_face
    assert sue_jargonunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_get_titlemap_ReturnsObj():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    static_x_titlemap = titlemap_shop(spark_face=exx.sue)
    static_x_titlemap.set_otx2inx("Bob", "Bob of Salem")
    sue_jargonunit.set_titlemap(static_x_titlemap)

    # WHEN
    gen_x_titlemap = sue_jargonunit.get_titlemap()

    # THEN
    assert gen_x_titlemap == static_x_titlemap


def test_JargonUnit_set_titleterm_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    contact_name_titlemap = zia_jargonunit.get_titlemap()
    assert contact_name_titlemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert contact_name_titlemap.otx2inx_exists(sue_otx, sue_inx)


def test_JargonUnit_titleterm_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)

    assert zia_jargonunit.titleterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_jargonunit.titleterm_exists(sue_otx, sue_inx)


def test_JargonUnit_get_inx_title_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    assert zia_jargonunit._get_inx_title(sue_otx) != sue_inx

    # WHEN
    zia_jargonunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_jargonunit._get_inx_title(sue_otx) == sue_inx


def test_JargonUnit_del_titleterm_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)

    zia_jargonunit.set_titleterm(sue_otx, sue_inx)
    zia_jargonunit.set_titleterm(exx.zia, exx.zia)
    assert zia_jargonunit.titleterm_exists(sue_otx, sue_inx)
    assert zia_jargonunit.titleterm_exists(exx.zia, exx.zia)

    # WHEN
    zia_jargonunit.del_titleterm(sue_otx)

    # THEN
    assert zia_jargonunit.titleterm_exists(sue_otx, sue_inx) is False
    assert zia_jargonunit.titleterm_exists(exx.zia, exx.zia)
