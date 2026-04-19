from ch06_plan.range_toolbox import RangeUnit, get_morphed_rangeunit, morph_rangeunit


def test_RangeUnit_Exists():
    # ESTABLISH
    x_gogo = 0
    x_stop = 20

    # WHEN
    x_rangeunit = RangeUnit(x_gogo, x_stop)

    # THEN
    assert x_rangeunit.gogo == x_gogo
    assert x_rangeunit.stop == x_stop


def test_morph_rangeunit_ReturnsObj_Scenario0():
    # ESTABLISH
    x_gogo = 0
    x_stop = 20
    x_rangeunit = RangeUnit(x_gogo, x_stop)
    x_denom = 5
    assert x_rangeunit.gogo == 0
    assert x_rangeunit.stop == 20

    # WHEN
    morph_rangeunit(x_rangeunit, x_denom)

    # THEN
    assert x_rangeunit.gogo == 0
    assert x_rangeunit.stop == 5


def test_morph_rangeunit_ReturnsObj_Scenario1():
    # ESTABLISH
    x_gogo = 17
    x_stop = 20
    x_rangeunit = RangeUnit(x_gogo, x_stop)
    x_denom = 5
    assert x_rangeunit.gogo == x_gogo
    assert x_rangeunit.stop == x_stop

    # WHEN
    morph_rangeunit(x_rangeunit, x_denom)

    # THEN
    assert x_rangeunit.gogo == x_gogo % x_denom
    assert x_rangeunit.stop == x_denom
    assert x_rangeunit.gogo == 2
    assert x_rangeunit.stop == 5


def test_morph_rangeunit_ReturnsObj_Scenario2():
    # ESTABLISH
    x_gogo = 17
    x_stop = 19
    x_rangeunit = RangeUnit(x_gogo, x_stop)
    x_denom = 5
    assert x_rangeunit.gogo == x_gogo
    assert x_rangeunit.stop == x_stop

    # WHEN
    morph_rangeunit(x_rangeunit, x_denom)

    # THEN
    assert x_rangeunit.gogo == x_gogo % x_denom
    assert x_rangeunit.stop == x_stop % x_denom
    assert x_rangeunit.gogo == 2
    assert x_rangeunit.stop == 4


def test_get_morphed_rangeunit_ReturnsObj_Scenario0():
    # ESTABLISH
    x_gogo = 17
    x_stop = 20
    x_denom = 5

    # WHEN
    x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_denom)

    # THEN
    assert x_rangeunit.gogo == 2
    assert x_rangeunit.stop == 5


def test_get_morphed_rangeunit_ReturnsObj_Scenario1():
    # ESTABLISH
    x_gogo = 0
    x_stop = 0
    x_denom = 5

    # WHEN
    x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_denom)

    # THEN
    assert x_rangeunit.gogo == x_gogo
    assert x_rangeunit.stop == x_stop


def test_get_morphed_rangeunit_ReturnsObj_Scenario2():
    # ESTABLISH
    x_int = 7

    # WHEN
    x_rangeunit = get_morphed_rangeunit(x_int, x_int, x_int)

    # THEN
    assert x_rangeunit.gogo == x_int
    assert x_rangeunit.stop == x_int
