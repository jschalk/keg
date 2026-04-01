from pytest import raises as pytest_raises
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import create_rope, get_default_rope
from src.ch09_person_lesson._ref.ch09_semantic_types import default_knot_if_None
from src.ch09_person_lesson.lasso import LassoUnit, default_knot_if_None, lassounit_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_LassoUnit_Exists():
    # ESTABLISH / WHEN
    x_lasso = LassoUnit()

    # THEN
    assert not x_lasso.moment_rope
    assert not x_lasso.knot
    assert set(x_lasso.__dict__.keys()) == {kw.moment_rope, kw.knot}


def test_lassounit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_lasso = lassounit_shop()

    # THEN
    assert x_lasso.moment_rope == get_default_rope()
    assert x_lasso.knot == default_knot_if_None()


def test_lassounit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    slash_knot = "/"
    casa_rope = create_rope(exx.sue, exx.casa, slash_knot)

    # WHEN
    casa_lasso = lassounit_shop(casa_rope, slash_knot)

    # THEN
    assert casa_lasso.moment_rope == casa_rope
    assert casa_lasso.knot == slash_knot


def test_lassounit_shop_ReturnsObj_Scenario2_RaisesErrorIfKnotNotAtPostionZeroOf_parent_rope():
    # ESTABLISH
    tulip_str = "tulip"
    semicolon_knot = ";"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        lassounit_shop(tulip_str, semicolon_knot)
    exception_str = f"{kw.moment_rope} '{tulip_str}' must have {kw.knot} '{semicolon_knot}' at position 0 in string"
    assert str(excinfo.value) == exception_str


def test_LassoUnit_make_path_ReturnsObj_Scenario0_SimpleRope():
    # ESTABLISH
    casa_rope = create_rope(exx.sue, exx.casa)
    casa_lasso = lassounit_shop(casa_rope)

    # WHEN
    casa_path = casa_lasso.make_path()

    # THEN
    assert casa_path
    expected_casa_path = create_path(exx.sue, exx.casa)
    assert casa_path == expected_casa_path


def test_LassoUnit_make_path_ReturnsObj_Scenario1_DifferentKnot():
    # ESTABLISH
    casa_rope = create_rope(exx.sue, exx.casa, exx.dash)
    casa_lasso = lassounit_shop(casa_rope, knot=exx.dash)

    # WHEN
    casa_path = casa_lasso.make_path()

    # THEN
    assert casa_path
    expected_casa_path = create_path(exx.sue, exx.casa)
    assert casa_path == expected_casa_path


def test_LassoUnit_first_label_ReturnsObj_Scenario0_DifferentKnot():
    # ESTABLISH
    clean_rope = create_rope(exx.casa, exx.clean, exx.dash)
    clean_lasso = lassounit_shop(clean_rope, knot=exx.dash)

    # WHEN
    clean_rope_first_label = clean_lasso.get_first_label()

    # THEN
    assert clean_rope_first_label
    assert clean_rope_first_label == exx.casa
