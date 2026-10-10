from ch17_jargon.map_term import labelmap_shop
from ch17_jargon.jargon_main import jargonunit_shop
from ch99_glossary.ch_keyword import ExampleStrs as exx
from pytest import raises as pytest_raises


def test_JargonUnit_set_labelmap_SetsAttr():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    x_labelmap = labelmap_shop(spark_face=exx.sue)
    x_labelmap.set_otx2inx("Bob", "Bob of Salem")
    assert sue_jargonunit.labelmap != x_labelmap

    # WHEN
    sue_jargonunit.set_labelmap(x_labelmap)

    # THEN
    assert sue_jargonunit.labelmap == x_labelmap


def test_JargonUnit_set_labelmap_RaisesErrorIf_labelmap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_labelmap = labelmap_shop(otx_knot=slash_otx_knot, spark_face=exx.sue)
    assert sue_jargonunit.otx_knot != x_labelmap.otx_knot
    assert sue_jargonunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: JargonUnit otx_knot is '{sue_jargonunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_labelmap_RaisesErrorIf_labelmap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_labelmap = labelmap_shop(inx_knot=slash_inx_knot, spark_face=exx.sue)
    assert sue_jargonunit.inx_knot != x_labelmap.inx_knot
    assert sue_jargonunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: JargonUnit inx_knot is '{sue_jargonunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_labelmap_RaisesErrorIf_labelmap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_labelmap = labelmap_shop(unknown_str=casa_unknown_str, spark_face=exx.sue)
    assert sue_jargonunit.unknown_str != x_labelmap.unknown_str
    assert sue_jargonunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: JargonUnit unknown_str is '{sue_jargonunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_set_labelmap_RaisesErrorIf_labelmap_spark_face_IsNotSame():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    x_labelmap = labelmap_shop(spark_face=exx.yao)
    assert sue_jargonunit.spark_face != x_labelmap.spark_face
    assert sue_jargonunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_jargonunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: JargonUnit spark_face is '{sue_jargonunit.spark_face}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_JargonUnit_get_labelmap_ReturnsObj():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)
    static_x_labelmap = labelmap_shop(spark_face=exx.sue)
    static_x_labelmap.set_otx2inx("Bob", "Bob of Salem")
    sue_jargonunit.set_labelmap(static_x_labelmap)

    # WHEN
    gen_x_labelmap = sue_jargonunit.get_labelmap()

    # THEN
    assert gen_x_labelmap == static_x_labelmap


def test_JargonUnit_set_label_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)
    labelid_labelmap = zia_jargonunit.get_labelmap()
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_jargonunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx)


def test_JargonUnit_del_roadmap_label_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_jargonunit = jargonunit_shop(exx.zia)

    zia_jargonunit.set_roadmap_label(sue_otx, sue_inx)
    zia_jargonunit.set_roadmap_label(exx.zia, exx.zia)
    assert zia_jargonunit.roadmap_label_exists(sue_otx, sue_inx)
    assert zia_jargonunit.roadmap_label_exists(exx.zia, exx.zia)

    # WHEN
    zia_jargonunit.del_roadmap_label(sue_otx)

    # THEN
    assert zia_jargonunit.roadmap_label_exists(sue_otx, sue_inx) is False
    assert zia_jargonunit.roadmap_label_exists(exx.zia, exx.zia)
