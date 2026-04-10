from pytest import raises as pytest_raises
from src.ch04_rope.rope import default_knot_if_None
from src.ch16_translate.map_term import (
    LabelMap,
    get_labelmap_from_dict,
    inherit_labelmap,
    labelmap_shop,
)
from src.ch16_translate.translate_config import default_unknown_str_if_None
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_LabelMap_Exists():
    # ESTABLISH
    x_labelmap = LabelMap()

    # WHEN / THEN
    assert not x_labelmap.spark_face
    assert not x_labelmap.spark_num
    assert not x_labelmap.otx2inx
    assert not x_labelmap.unknown_str
    assert not x_labelmap.otx_knot
    assert not x_labelmap.inx_knot


def test_labelmap_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_labelmap = labelmap_shop()

    # THEN
    assert not x_labelmap.spark_face
    assert x_labelmap.spark_num == 0
    assert x_labelmap.otx2inx == {}
    assert x_labelmap.unknown_str == default_unknown_str_if_None()
    assert x_labelmap.otx_knot == default_knot_if_None()
    assert x_labelmap.inx_knot == default_knot_if_None()


def test_labelmap_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    spark7 = 7
    otx2inx = {exx.xio: exx.sue}
    x_unknown_str = "UnknownLabelId"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    x_labelmap = labelmap_shop(
        spark_face=exx.bob,
        spark_num=spark7,
        otx2inx=otx2inx,
        unknown_str=x_unknown_str,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
    )

    # THEN
    assert x_labelmap.spark_face == exx.bob
    assert x_labelmap.spark_num == spark7
    assert x_labelmap.otx2inx == otx2inx
    assert x_labelmap.unknown_str == x_unknown_str
    assert x_labelmap.otx_knot == slash_otx_knot
    assert x_labelmap.inx_knot == colon_inx_knot


def test_labelmap_shop_ReturnsObj_Scenario2_TranslateCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    otx2inx = {exx.xio: exx.sue}
    x_nan = float("nan")

    # WHEN
    x_labelmap = labelmap_shop(
        spark_face=exx.bob,
        spark_num=spark7,
        otx2inx=otx2inx,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_labelmap.spark_face == exx.bob
    assert x_labelmap.spark_num == spark7
    assert x_labelmap.otx2inx == otx2inx
    assert x_labelmap.unknown_str == default_unknown_str_if_None()
    assert x_labelmap.otx_knot == default_knot_if_None()
    assert x_labelmap.inx_knot == default_knot_if_None()


def test_LabelMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    x_labelmap = labelmap_shop()
    x_otx2inx = {exx.xio: exx.sue, exx.zia: exx.zia}
    assert x_labelmap.otx2inx != x_otx2inx

    # WHEN
    x_labelmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_labelmap.otx2inx == x_otx2inx


def test_LabelMap_set_all_otx2inx_RaisesErrorIf_unknown_str_IsKeyIn_otx2inx():
    # ESTABLISH
    x_unknown_str = "UnknownLabelId"
    x_labelmap = labelmap_shop(None, unknown_str=x_unknown_str)
    x_otx2inx = {exx.xio: exx.sue, x_unknown_str: exx.zia}
    assert x_labelmap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_labelmap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_str '{x_unknown_str}' in any str. Affected keys include ['{x_unknown_str}']."
    assert str(excinfo.value) == exception_str


def test_LabelMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    x_unknown_str = "UnknownLabelId"
    x_labelmap = labelmap_shop(None)
    x_otx2inx = {exx.xio: exx.sue, x_unknown_str: exx.zia}
    assert x_labelmap.otx2inx != x_otx2inx

    # WHEN
    x_labelmap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_labelmap.otx2inx == x_otx2inx


def test_LabelMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    x_labelmap = labelmap_shop(None)
    assert x_labelmap.otx2inx == {}

    # WHEN
    x_labelmap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_labelmap.otx2inx == {exx.xio: exx.sue}


def test_LabelMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    x_labelmap = labelmap_shop(None)
    assert x_labelmap.get_inx_value(exx.xio) != exx.sue

    # WHEN
    x_labelmap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_labelmap.get_inx_value(exx.xio) == exx.sue


def test_LabelMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    x_labelmap = labelmap_shop(None)
    assert x_labelmap.otx2inx_exists(exx.xio, exx.sue) is False
    assert x_labelmap.otx2inx_exists(exx.xio, exx.zia) is False
    assert x_labelmap.otx2inx_exists(exx.xio, exx.bob) is False
    assert x_labelmap.otx2inx_exists(exx.zia, exx.zia) is False

    # WHEN
    x_labelmap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_labelmap.otx2inx_exists(exx.xio, exx.sue)
    assert x_labelmap.otx2inx_exists(exx.xio, exx.zia) is False
    assert x_labelmap.otx2inx_exists(exx.xio, exx.bob) is False
    assert x_labelmap.otx2inx_exists(exx.zia, exx.zia) is False

    # WHEN
    x_labelmap.set_otx2inx(exx.zia, exx.zia)

    # THEN
    assert x_labelmap.otx2inx_exists(exx.xio, exx.sue)
    assert x_labelmap.otx2inx_exists(exx.xio, exx.zia) is False
    assert x_labelmap.otx2inx_exists(exx.xio, exx.bob) is False
    assert x_labelmap.otx2inx_exists(exx.zia, exx.zia)


def test_LabelMap_otx_exists_ReturnsObj():
    # ESTABLISH
    x_labelmap = labelmap_shop(None)
    assert x_labelmap.otx_exists(exx.xio) is False
    assert x_labelmap.otx_exists(exx.sue) is False
    assert x_labelmap.otx_exists(exx.bob) is False
    assert x_labelmap.otx_exists(exx.zia) is False

    # WHEN
    x_labelmap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_labelmap.otx_exists(exx.xio)
    assert x_labelmap.otx_exists(exx.sue) is False
    assert x_labelmap.otx_exists(exx.bob) is False
    assert x_labelmap.otx_exists(exx.zia) is False

    # WHEN
    x_labelmap.set_otx2inx(exx.zia, exx.zia)

    # THEN
    assert x_labelmap.otx_exists(exx.xio)
    assert x_labelmap.otx_exists(exx.sue) is False
    assert x_labelmap.otx_exists(exx.bob) is False
    assert x_labelmap.otx_exists(exx.zia)


def test_LabelMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    x_labelmap = labelmap_shop(None)
    x_labelmap.set_otx2inx(exx.xio, exx.sue)
    assert x_labelmap.otx2inx_exists(exx.xio, exx.sue)

    # WHEN
    x_labelmap.del_otx2inx(exx.xio)

    # THEN
    assert x_labelmap.otx2inx_exists(exx.xio, exx.sue) is False


def test_LabelMap_unknown_str_in_otx2inx_ReturnsObj():
    # ESTABLISH
    x_unknown_str = "UnknownLabelId"
    x_labelmap = labelmap_shop(None, unknown_str=x_unknown_str)
    x_labelmap.set_otx2inx(exx.xio, exx.sue)
    assert x_labelmap.unknown_str_in_otx2inx() is False

    # WHEN
    x_labelmap.set_otx2inx(exx.zia, x_unknown_str)

    # THEN
    assert x_labelmap.unknown_str_in_otx2inx()


def test_LabelMap_reveal_inx_ReturnsObjAndSetsAttr_label():
    # ESTABLISH
    inx_r_knot = ":"
    otx_r_knot = "/"
    bowl_otx = f"bowl{otx_r_knot}"
    climb_otx = f"climb{otx_r_knot}_{inx_r_knot}"
    x_labelmap = labelmap_shop(otx_knot=otx_r_knot, inx_knot=inx_r_knot)
    x_labelmap.otx_exists(bowl_otx) is False
    x_labelmap.otx_exists(climb_otx) is False

    # WHEN
    bowl_inx = f"bowl{inx_r_knot}"
    assert x_labelmap.reveal_inx(bowl_otx) == bowl_inx

    # THEN
    assert x_labelmap.otx_exists(bowl_otx)
    assert x_labelmap.otx_exists(climb_otx) is False
    assert x_labelmap.get_inx_value(bowl_otx) == bowl_inx

    # WHEN
    assert x_labelmap.reveal_inx(climb_otx) is None
    # THEN
    assert x_labelmap.otx_exists(bowl_otx)
    assert x_labelmap.otx_exists(climb_otx) is False


def test_LabelMap_to_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    spark7 = 7
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    x_labelmap = labelmap_shop(
        exx.sue,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
    )
    x1_rope_map_dict = {
        kw.otx_knot: x_labelmap.otx_knot,
        kw.inx_knot: x_labelmap.inx_knot,
        kw.unknown_str: x_labelmap.unknown_str,
        kw.otx2inx: {},
        kw.spark_face: x_labelmap.spark_face,
        kw.spark_num: x_labelmap.spark_num,
    }
    assert x_labelmap.to_dict() == x1_rope_map_dict

    # WHEN
    x_labelmap.set_otx2inx(clean_otx, clean_inx)
    x_labelmap.spark_num = spark7
    # THEN
    x2_rope_map_dict = {
        kw.otx_knot: x_labelmap.otx_knot,
        kw.inx_knot: x_labelmap.inx_knot,
        kw.unknown_str: x_labelmap.unknown_str,
        kw.otx2inx: {clean_otx: clean_inx},
        kw.spark_face: exx.sue,
        kw.spark_num: spark7,
    }
    assert x_labelmap.to_dict() == x2_rope_map_dict


def test_get_labelmap_from_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    spark7 = 7
    slash_otx_knot = "/"
    x_labelmap = labelmap_shop(exx.sue, spark7, otx_knot=slash_otx_knot)
    x_labelmap.set_otx2inx(clean_otx, clean_inx)

    # WHEN
    gen_labelmap = get_labelmap_from_dict(x_labelmap.to_dict())

    # THEN
    assert gen_labelmap.spark_face == x_labelmap.spark_face
    assert gen_labelmap.spark_num == x_labelmap.spark_num
    assert gen_labelmap.spark_num == spark7
    assert gen_labelmap == x_labelmap


def test_LabelMap_is_inx_knot_inclusion_correct_ReturnsObj():
    # ESTABLISH
    inx_knot = "/"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_knot}"
    x_labelmap = labelmap_shop(inx_knot=inx_knot)
    assert x_labelmap._is_inx_knot_inclusion_correct()

    # WHEN
    x_labelmap.set_otx2inx(exx.xio, exx.sue)
    # THEN
    assert x_labelmap._is_inx_knot_inclusion_correct()

    # WHEN
    x_labelmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_labelmap._is_inx_knot_inclusion_correct() is False


def test_LabelMap_is_otx_knot_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "XioXio"
    otx_knot = "/"
    zia_otx = f"Zia{otx_knot}"
    zia_inx = "Zia"
    x_labelmap = labelmap_shop(otx_knot=otx_knot)
    assert x_labelmap._is_otx_knot_inclusion_correct()

    # WHEN
    x_labelmap.set_otx2inx(xio_otx, xio_inx)
    # THEN
    assert x_labelmap._is_otx_knot_inclusion_correct()

    # WHEN
    x_labelmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_labelmap._is_otx_knot_inclusion_correct() is False


def test_LabelMap_is_valid_ReturnsObj():
    # ESTABLISH
    otx_knot = ":"
    inx_knot = "/"
    sue_otx = f"Xio{otx_knot}"
    sue_with_knot = f"Sue{inx_knot}"
    sue_without_knot = f"Sue{otx_knot}"
    zia_otx = "Zia"
    zia_inx = f"Zia{inx_knot}"
    x_labelmap = labelmap_shop(otx_knot=otx_knot, inx_knot=inx_knot)
    assert x_labelmap.is_valid()

    # WHEN
    x_labelmap.set_otx2inx(sue_otx, sue_with_knot)
    # THEN
    assert x_labelmap.is_valid() is False

    # WHEN
    x_labelmap.set_otx2inx(zia_otx, zia_inx)
    # THEN
    assert x_labelmap.is_valid() is False

    # WHEN
    x_labelmap.set_otx2inx(sue_otx, sue_without_knot)
    # THEN
    assert x_labelmap.is_valid() is False


def test_inherit_labelmap_ReturnsObj_Scenario0():
    # ESTABLISH
    old_labelmap = labelmap_shop(exx.zia, 3)
    new_labelmap = labelmap_shop(exx.zia, 5)

    # WHEN
    inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert new_labelmap
    assert new_labelmap == labelmap_shop(exx.zia, 5)


def test_inherit_labelmap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_labelmap = labelmap_shop(exx.sue, 0, otx_knot=slash_otx_knot)
    new_labelmap = labelmap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelmap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_labelmap = labelmap_shop(exx.sue, 0, inx_knot=slash_otx_knot)
    new_labelmap = labelmap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelmap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    old_labelmap = labelmap_shop(exx.sue, 0, unknown_str=x_unknown_str)
    new_labelmap = labelmap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelmap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_spark_face():
    # ESTABLISH
    old_labelmap = labelmap_shop(exx.sue, 0)
    new_labelmap = labelmap_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelmap_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_labelmap = labelmap_shop(exx.sue, 5)
    new_labelmap = labelmap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_labelmap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_labelmap = labelmap_shop(exx.zia, 3)
    old_labelmap.set_otx2inx(xio_otx, xio_inx)
    new_labelmap = labelmap_shop(exx.zia, 7)
    assert new_labelmap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_labelmap = inherit_labelmap(new_labelmap, old_labelmap)

    # THEN
    assert inherited_labelmap.otx2inx_exists(xio_otx, xio_inx)
