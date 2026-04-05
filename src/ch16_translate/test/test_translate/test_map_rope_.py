from pytest import raises as pytest_raises
from src.ch04_rope.rope import create_rope, default_knot_if_None, to_rope
from src.ch16_translate.map_term import (
    RopeMap,
    get_ropemap_from_dict,
    inherit_ropemap,
    labelmap_shop,
    ropemap_shop,
)
from src.ch16_translate.translate_config import default_unknown_str_if_None
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_RopeMap_Exists():
    # ESTABLISH
    x_ropemap = RopeMap()

    # WHEN / THEN
    assert not x_ropemap.spark_face
    assert not x_ropemap.spark_num
    assert not x_ropemap.otx2inx
    assert not x_ropemap.unknown_str
    assert not x_ropemap.otx_knot
    assert not x_ropemap.inx_knot
    assert not x_ropemap.labelmap


def test_ropemap_shop_ReturnsObj_Scenario0():
    # ESTABLISH
    spark7 = 7
    otx2inx = {exx.xio: exx.sue}
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    e7_ropemap = ropemap_shop(
        spark_face=exx.bob,
        spark_num=spark7,
        otx2inx=otx2inx,
        unknown_str=x_unknown_str,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
    )

    # THEN
    assert e7_ropemap.spark_face == exx.bob
    assert e7_ropemap.spark_num == spark7
    assert e7_ropemap.otx2inx == otx2inx
    assert e7_ropemap.unknown_str == x_unknown_str
    assert e7_ropemap.otx_knot == slash_otx_knot
    assert e7_ropemap.inx_knot == colon_inx_knot
    assert e7_ropemap.labelmap == labelmap_shop(
        spark_face=exx.bob,
        spark_num=spark7,
        unknown_str=x_unknown_str,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
    )


def test_ropemap_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    x_ropemap = ropemap_shop()

    # THEN
    assert x_ropemap.otx2inx == {}
    assert x_ropemap.unknown_str == default_unknown_str_if_None()
    assert x_ropemap.otx_knot == default_knot_if_None()
    assert x_ropemap.inx_knot == default_knot_if_None()
    assert x_ropemap.spark_face is None
    assert x_ropemap.spark_num == 0
    assert x_ropemap.labelmap == labelmap_shop(
        spark_num=0,
        unknown_str=default_unknown_str_if_None(),
        otx_knot=default_knot_if_None(),
        inx_knot=default_knot_if_None(),
    )


def test_ropemap_shop_ReturnsObj_Scenario3_TranslateCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    otx2inx = {exx.xio: exx.sue}
    x_nan = float("nan")

    # WHEN
    x_ropemap = ropemap_shop(
        spark_face=exx.bob,
        spark_num=spark7,
        otx2inx=otx2inx,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_ropemap.spark_face == exx.bob
    assert x_ropemap.spark_num == spark7
    assert x_ropemap.otx2inx == otx2inx
    assert x_ropemap.unknown_str == default_unknown_str_if_None()
    assert x_ropemap.otx_knot == default_knot_if_None()
    assert x_ropemap.inx_knot == default_knot_if_None()


def test_RopeMap_set_all_otx2inx_SetsAttr():
    # ESTABLISH
    contact_name_ropemap = ropemap_shop()
    x_otx2inx = {exx.xio: exx.sue, exx.zia: exx.zia}
    assert contact_name_ropemap.otx2inx != x_otx2inx

    # WHEN
    contact_name_ropemap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert contact_name_ropemap.otx2inx == x_otx2inx


def test_RopeMap_set_all_otx2inx_RaisesErrorIf_unknown_str_IsKeyIn_otx2inx():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    contact_name_ropemap = ropemap_shop(unknown_str=x_unknown_str)
    x_otx2inx = {exx.xio: exx.sue, x_unknown_str: exx.zia}
    assert contact_name_ropemap.otx2inx != x_otx2inx

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contact_name_ropemap.set_all_otx2inx(x_otx2inx, True)
    exception_str = f"otx2inx cannot have unknown_str '{x_unknown_str}' in any str. Affected keys include ['{x_unknown_str}']."
    assert str(excinfo.value) == exception_str


def test_RopeMap_set_all_otx2inx_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    x_ropemap = ropemap_shop(None)
    x_otx2inx = {exx.xio: exx.sue, x_unknown_str: exx.zia}
    assert x_ropemap.otx2inx != x_otx2inx

    # WHEN
    x_ropemap.set_all_otx2inx(x_otx2inx)

    # THEN
    assert x_ropemap.otx2inx == x_otx2inx


def test_RopeMap_set_otx2inx_SetsAttr():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx2inx == {}

    # WHEN
    x_ropemap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.otx2inx == {exx.xio: exx.sue}


def test_RopeMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.get_inx_value(exx.xio) != exx.sue

    # WHEN
    x_ropemap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.get_inx_value(exx.xio) == exx.sue


def test_RopeMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx2inx_exists(exx.xio, exx.sue) is False
    assert x_ropemap.otx2inx_exists(exx.xio, exx.zia) is False
    assert x_ropemap.otx2inx_exists(exx.xio, exx.bob) is False
    assert x_ropemap.otx2inx_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropemap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.otx2inx_exists(exx.xio, exx.sue)
    assert x_ropemap.otx2inx_exists(exx.xio, exx.zia) is False
    assert x_ropemap.otx2inx_exists(exx.xio, exx.bob) is False
    assert x_ropemap.otx2inx_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropemap.set_otx2inx(exx.zia, exx.zia)

    # THEN
    assert x_ropemap.otx2inx_exists(exx.xio, exx.sue)
    assert x_ropemap.otx2inx_exists(exx.xio, exx.zia) is False
    assert x_ropemap.otx2inx_exists(exx.xio, exx.bob) is False
    assert x_ropemap.otx2inx_exists(exx.zia, exx.zia)


def test_RopeMap_otx_exists_ReturnsObj():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx_exists(exx.xio) is False
    assert x_ropemap.otx_exists(exx.sue) is False
    assert x_ropemap.otx_exists(exx.bob) is False
    assert x_ropemap.otx_exists(exx.zia) is False

    # WHEN
    x_ropemap.set_otx2inx(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.otx_exists(exx.xio)
    assert x_ropemap.otx_exists(exx.sue) is False
    assert x_ropemap.otx_exists(exx.bob) is False
    assert x_ropemap.otx_exists(exx.zia) is False

    # WHEN
    x_ropemap.set_otx2inx(exx.zia, exx.zia)

    # THEN
    assert x_ropemap.otx_exists(exx.xio)
    assert x_ropemap.otx_exists(exx.sue) is False
    assert x_ropemap.otx_exists(exx.bob) is False
    assert x_ropemap.otx_exists(exx.zia)


def test_RopeMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    x_ropemap.set_otx2inx(exx.xio, exx.sue)
    assert x_ropemap.otx2inx_exists(exx.xio, exx.sue)

    # WHEN
    x_ropemap.del_otx2inx(exx.xio)

    # THEN
    assert x_ropemap.otx2inx_exists(exx.xio, exx.sue) is False


def test_RopeMap_unknown_str_in_otx2inx_ReturnsObj():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    x_ropemap = ropemap_shop(unknown_str=x_unknown_str)
    x_ropemap.set_otx2inx(exx.xio, exx.sue)
    assert x_ropemap.unknown_str_in_otx2inx() is False

    # WHEN
    x_ropemap.set_otx2inx(exx.zia, x_unknown_str)

    # THEN
    assert x_ropemap.unknown_str_in_otx2inx()


def test_RopeMap_set_label_SetsAttr():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.labelmap.otx2inx == {}

    # WHEN
    x_ropemap.set_label(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.labelmap.otx2inx == {exx.xio: exx.sue}


def test_RopeMap_set_label_RaisesExceptionWhen_knot_In_otx_label():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    sue_otx = f"Sue{x_ropemap.otx_knot}"
    sue_inx = "Sue"
    assert x_ropemap.labelmap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ropemap.set_label(sue_otx, sue_inx)
    exception_str = f"label cannot have otx_label '{sue_otx}'. It must be not have knot {x_ropemap.otx_knot}."
    assert str(excinfo.value) == exception_str


def test_RopeMap_set_label_RaisesExceptionWhen_knot_In_inx_label():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    sue_inx = f"Sue{x_ropemap.otx_knot}"
    sue_otx = "Sue"
    assert x_ropemap.labelmap.otx2inx == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ropemap.set_label(sue_otx, sue_inx)
    exception_str = f"label cannot have inx_label '{sue_inx}'. It must be not have knot {x_ropemap.inx_knot}."
    assert str(excinfo.value) == exception_str


def test_RopeTranslate_label_exists_ReturnsObj():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.label_exists(exx.xio, exx.sue) is False
    assert x_ropemap.label_exists(exx.xio, exx.zia) is False
    assert x_ropemap.label_exists(exx.xio, exx.bob) is False
    assert x_ropemap.label_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropemap.set_label(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.label_exists(exx.xio, exx.sue)
    assert x_ropemap.label_exists(exx.xio, exx.zia) is False
    assert x_ropemap.label_exists(exx.xio, exx.bob) is False
    assert x_ropemap.label_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropemap.set_label(exx.zia, exx.zia)

    # THEN
    assert x_ropemap.label_exists(exx.xio, exx.sue)
    assert x_ropemap.label_exists(exx.xio, exx.zia) is False
    assert x_ropemap.label_exists(exx.xio, exx.bob) is False
    assert x_ropemap.label_exists(exx.zia, exx.zia)


def test_RopeMap_otx_label_exists_ReturnsObj():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    assert x_ropemap.otx_label_exists(exx.xio) is False
    assert x_ropemap.otx_label_exists(exx.sue) is False
    assert x_ropemap.otx_label_exists(exx.bob) is False
    assert x_ropemap.otx_label_exists(exx.zia) is False

    # WHEN
    x_ropemap.set_label(exx.xio, exx.sue)

    # THEN
    assert x_ropemap.otx_label_exists(exx.xio)
    assert x_ropemap.otx_label_exists(exx.sue) is False
    assert x_ropemap.otx_label_exists(exx.bob) is False
    assert x_ropemap.otx_label_exists(exx.zia) is False

    # WHEN
    x_ropemap.set_label(exx.zia, exx.zia)

    # THEN
    assert x_ropemap.otx_label_exists(exx.xio)
    assert x_ropemap.otx_label_exists(exx.sue) is False
    assert x_ropemap.otx_label_exists(exx.bob) is False
    assert x_ropemap.otx_label_exists(exx.zia)


def test_RopeMap_del_label_SetsAttr():
    # ESTABLISH
    x_ropemap = ropemap_shop(None)
    x_ropemap.set_label(exx.xio, exx.sue)
    assert x_ropemap.label_exists(exx.xio, exx.sue)

    # WHEN
    x_ropemap.del_label(exx.xio)

    # THEN
    assert x_ropemap.label_exists(exx.xio, exx.sue) is False


def test_RopeMap_set_label_Edits_otx2inx():
    # ESTABLISH
    otx_amy45_str = to_rope("amy45")
    inx_amy87_str = to_rope("amy87")
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    sweep_inx_rope = create_rope(clean_inx_rope, exx.sweep)
    x_ropemap = ropemap_shop()
    x_ropemap.set_otx2inx(otx_amy45_str, inx_amy87_str)
    x_ropemap.set_otx2inx(casa_otx_rope, casa_inx_rope)
    x_ropemap.set_otx2inx(clean_otx_rope, clean_inx_rope)
    x_ropemap.set_otx2inx(sweep_otx_rope, sweep_inx_rope)
    assert x_ropemap.otx2inx_exists(otx_amy45_str, inx_amy87_str)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope)
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope)
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_inx_rope)

    # WHEN
    menage_inx_str = "menage"
    x_ropemap.set_label(clean_otx_str, menage_inx_str)

    # THEN
    menage_inx_rope = create_rope(casa_inx_rope, menage_inx_str)
    sweep_menage_inx_rope = create_rope(menage_inx_rope, exx.sweep)
    assert x_ropemap.otx2inx_exists(otx_amy45_str, inx_amy87_str)
    assert x_ropemap.otx2inx_exists(casa_otx_rope, casa_inx_rope)
    assert x_ropemap.otx2inx_exists(clean_otx_rope, menage_inx_rope)
    assert x_ropemap.otx2inx_exists(sweep_otx_rope, sweep_menage_inx_rope)


def test_RopeMap_to_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(exx.sue, otx_knot=slash_otx_knot)
    x1_rope_map_dict = {
        kw.spark_num: 0,
        kw.spark_face: exx.sue,
        kw.inx_knot: x_ropemap.inx_knot,
        kw.otx2inx: {},
        kw.otx_knot: x_ropemap.otx_knot,
        kw.unknown_str: x_ropemap.unknown_str,
    }
    # print(f"           {x1_rope_map_json=}")
    assert x_ropemap.to_dict() == x1_rope_map_dict

    # WHEN
    spark7 = 7
    x_ropemap.set_otx2inx(clean_otx, clean_inx)
    x_ropemap.spark_num = spark7
    # THEN
    x2_rope_map_dict = {
        kw.spark_num: spark7,
        kw.spark_face: exx.sue,
        kw.inx_knot: x_ropemap.inx_knot,
        kw.otx2inx: {clean_otx: clean_inx},
        kw.otx_knot: x_ropemap.otx_knot,
        kw.unknown_str: x_ropemap.unknown_str,
    }
    print(f"           {x2_rope_map_dict=}")
    print(f"{x_ropemap.to_dict()=}")
    assert x_ropemap.to_dict() == x2_rope_map_dict


def test_get_ropemap_from_dict_ReturnsObj():
    # ESTABLISH
    clean_otx = "clean"
    clean_inx = "propre"
    spark7 = 7
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(exx.sue, spark7, otx_knot=slash_otx_knot)
    x_ropemap.set_otx2inx(clean_otx, clean_inx)
    x_ropemap.set_label("bob", "bobito")

    # WHEN
    gen_ropemap = get_ropemap_from_dict(x_ropemap.to_dict())

    # THEN
    assert gen_ropemap.spark_face == x_ropemap.spark_face
    assert gen_ropemap.spark_num == x_ropemap.spark_num
    assert gen_ropemap.spark_num == spark7
    assert gen_ropemap.labelmap.spark_face == x_ropemap.labelmap.spark_face
    assert gen_ropemap.labelmap.otx2inx != x_ropemap.labelmap.otx2inx
    assert gen_ropemap.labelmap != x_ropemap.labelmap
    assert gen_ropemap.otx2inx == x_ropemap.otx2inx
    assert gen_ropemap.otx_knot == x_ropemap.otx_knot
    assert gen_ropemap.inx_knot == x_ropemap.inx_knot
    assert gen_ropemap.unknown_str == x_ropemap.unknown_str


def test_RopeMap_all_otx_parent_ropes_exist_ReturnsObj_RopeTerm():
    # ESTABLISH
    otx_r_knot = "/"
    clean_otx_parent_rope = to_rope("amy45", otx_r_knot)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(clean_otx_parent_rope, clean_otx_str, otx_r_knot)

    x_ropemap = ropemap_shop(otx_knot=otx_r_knot)
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.all_otx_parent_ropes_exist()

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_rope, to_rope("any", otx_r_knot))
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist() is False

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_parent_rope, to_rope("any"))
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope)
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist()


def test_RopeMap_is_valid_ReturnsObj_Scenario0_plan_label_str():
    # ESTABLISH
    x_otx_knot = "/"
    x_inx_knot = ":"
    labelterm_ropemap = ropemap_shop(otx_knot=x_otx_knot, inx_knot=x_inx_knot)

    clean_inx = to_rope("propre", x_inx_knot)
    casa_otx = to_rope("casa", x_otx_knot)
    mop_otx = create_rope(casa_otx, "mop", x_otx_knot)
    mop_inx = "mop"
    casa_inx = "casa"
    assert labelterm_ropemap.is_valid()

    # WHEN
    labelterm_ropemap.set_otx2inx(exx.clean, clean_inx)
    # THEN
    assert labelterm_ropemap.is_valid()

    # WHEN
    labelterm_ropemap.set_otx2inx(mop_otx, mop_inx)
    # THEN
    assert labelterm_ropemap.is_valid() is False


def test_RopeMap_is_valid_ReturnsObj_Scenario1_rope_str():
    # ESTABLISH
    amy45_str = "amy45"
    otx_r_knot = "/"
    inx_r_knot = ":"
    clean_otx_str = "clean"
    clean_otx_rope = f"{amy45_str}{otx_r_knot}{clean_otx_str}"
    clean_inx_str = "prop"
    clean_inx_rope = f"{amy45_str}{inx_r_knot}{clean_inx_str}"
    # casa_otx = f"casa{otx_knot}"
    # casa_inx = f"casa"
    x_ropemap = ropemap_shop(otx_knot=otx_r_knot, inx_knot=inx_r_knot)
    x_ropemap.set_otx2inx(amy45_str, amy45_str)
    assert x_ropemap.is_valid()
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope) is False

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_rope, clean_inx_rope)
    # THEN
    assert x_ropemap.is_valid()
    assert x_ropemap.otx2inx_exists(clean_otx_rope, clean_inx_rope)


def test_RopeMap_is_valid_ReturnsObj_Scenario3_RopeTerm():
    # ESTABLISH
    otx_r_knot = "/"
    clean_otx_parent_rope = to_rope("amy45", otx_r_knot)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(clean_otx_parent_rope, clean_otx_str, otx_r_knot)

    x_ropemap = ropemap_shop(otx_knot=otx_r_knot)
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope) is False
    assert x_ropemap.all_otx_parent_ropes_exist()
    assert x_ropemap.is_valid()

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_rope, "any")
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope) is False
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist() is False
    assert x_ropemap.is_valid() is False

    # WHEN
    x_ropemap.set_otx2inx(clean_otx_parent_rope, "any")
    # THEN
    assert x_ropemap.otx_exists(clean_otx_parent_rope)
    assert x_ropemap.otx_exists(clean_otx_rope)
    assert x_ropemap.all_otx_parent_ropes_exist()
    assert x_ropemap.is_valid()


def test_inherit_ropemap_ReturnsObj_Scenario0():
    # ESTABLISH
    old_ropemap = ropemap_shop(exx.zia, 3)
    new_ropemap = ropemap_shop(exx.zia, 5)
    # WHEN
    inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert new_ropemap
    assert new_ropemap == ropemap_shop(exx.zia, 5)


def test_inherit_ropemap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_ropemap = ropemap_shop(exx.sue, 0, otx_knot=slash_otx_knot)
    new_ropemap = ropemap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_ropemap = ropemap_shop(exx.sue, 0, inx_knot=slash_otx_knot)
    new_ropemap = ropemap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    old_ropemap = ropemap_shop(exx.sue, 0, unknown_str=x_unknown_str)
    new_ropemap = ropemap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_spark_face():
    # ESTABLISH
    old_ropemap = ropemap_shop(exx.sue, 0)
    new_ropemap = ropemap_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropemap_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_ropemap = ropemap_shop(exx.sue, 5)
    new_ropemap = ropemap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert str(excinfo.value) == "older mapunit is not older"


def test_inherit_ropemap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    xio_otx = "Xio"
    xio_inx = "Xioito"
    old_ropemap = ropemap_shop(exx.zia, 3)
    old_ropemap.set_otx2inx(xio_otx, xio_inx)
    new_ropemap = ropemap_shop(exx.zia, 7)
    assert new_ropemap.otx2inx_exists(xio_otx, xio_inx) is False

    # WHEN
    inherited_ropemap = inherit_ropemap(new_ropemap, old_ropemap)

    # THEN
    assert inherited_ropemap.otx2inx_exists(xio_otx, xio_inx)
