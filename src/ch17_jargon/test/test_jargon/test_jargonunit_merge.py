from ch17_jargon.test._util.ch17_examples import (
    get_bowl_titlemap,
    get_clean_labelmap,
    get_clean_ropemap,
    get_suita_namemap,
)
from ch17_jargon.jargon_main import inherit_jargonunit, jargonunit_shop
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
from pytest import raises as pytest_raises


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario0_EmptyJargonUnits():
    # ESTABLISH
    old_jargonunit = jargonunit_shop(exx.sue, 0)
    new_jargonunit = jargonunit_shop(exx.sue, 1)

    # WHEN
    merged_jargonunit = inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert merged_jargonunit
    assert merged_jargonunit == new_jargonunit


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_jargonunit = jargonunit_shop(exx.sue, 0, otx_knot=slash_otx_knot)
    new_jargonunit = jargonunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_jargonunit = jargonunit_shop(exx.sue, 0, inx_knot=slash_otx_knot)
    new_jargonunit = jargonunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    old_jargonunit = jargonunit_shop(exx.sue, 0, unknown_str=x_unknown_str)
    new_jargonunit = jargonunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_spark_face():
    # ESTABLISH
    old_jargonunit = jargonunit_shop(exx.sue, 0)
    new_jargonunit = jargonunit_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_jargonunit = jargonunit_shop(exx.sue, 5)
    new_jargonunit = jargonunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert str(excinfo.value) == "older jargonunit is not older"


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario6_namemap_Inherited():
    # ESTABLISH
    spark1 = 1
    old_jargonunit = jargonunit_shop(exx.sue, 0)
    old_jargonunit.set_namemap(get_suita_namemap())
    old_jargonunit.set_titlemap(get_bowl_titlemap())
    old_jargonunit.set_labelmap(get_clean_labelmap())
    old_jargonunit.set_ropemap(get_clean_ropemap())
    new_jargonunit = jargonunit_shop(exx.sue, spark1)
    assert new_jargonunit.namemap != get_suita_namemap()

    # WHEN
    merged_jargonunit = inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert merged_jargonunit
    merged_contactbridge = get_suita_namemap()
    merged_contactbridge.spark_num = spark1
    assert merged_jargonunit.namemap == merged_contactbridge
    merged_groupbridge = get_bowl_titlemap()
    merged_groupbridge.spark_num = spark1
    assert merged_jargonunit.titlemap == merged_groupbridge
    merged_labelbridge = get_clean_labelmap()
    merged_labelbridge.spark_num = spark1
    assert merged_jargonunit.labelmap == merged_labelbridge
    merged_ropebridge = get_clean_ropemap()
    merged_ropebridge.spark_num = spark1
    merged_ropebridge.labelmap = merged_labelbridge
    assert merged_jargonunit.ropemap == merged_ropebridge


def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario7_namemap_Inherited():
    # ESTABLISH
    spark1 = 1
    old_jargonunit = jargonunit_shop(exx.sue, 0)
    old_jargonunit.set_namemap(get_suita_namemap())
    old_jargonunit.set_titlemap(get_bowl_titlemap())
    new_jargonunit = jargonunit_shop(exx.sue, spark1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_jargonunit.set_otx2inx(kw.NameTerm, bob_otx, bob_inx)
    assert new_jargonunit.namemap != get_suita_namemap()
    assert new_jargonunit.nameterm_exists(bob_otx, bob_inx)

    # WHEN
    merged_jargonunit = inherit_jargonunit(old_jargonunit, new_jargonunit)

    # THEN
    assert merged_jargonunit
    assert new_jargonunit.nameterm_exists(bob_otx, bob_inx)
    merged_contactbridge = get_suita_namemap()
    merged_contactbridge.spark_num = spark1
    merged_contactbridge.set_otx2inx(bob_otx, bob_inx)
    assert merged_jargonunit.namemap == merged_contactbridge
    merged_groupbridge = get_bowl_titlemap()
    merged_groupbridge.spark_num = spark1
    assert merged_jargonunit.titlemap == merged_groupbridge
