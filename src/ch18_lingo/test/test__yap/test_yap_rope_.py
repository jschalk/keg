from ch05_rope.rope import create_rope, default_knot_if_None, to_rope
from ch18_lingo.yap_term import (
    RopeYap,
    get_ropeyap_from_dict,
    inherit_ropeyap,
    labelyap_shop,
    ropeyap_shop,
)
from pytest import raises as pytest_raises
from src.ch99_glossary.ch_keyword import Ch18Keywords as kw, ExampleStrs as exx


def test_RopeYap_Exists():
    # ESTABLISH
    x_ropeyap = RopeYap()

    # WHEN / THEN
    assert not x_ropeyap.flare_audie
    assert not x_ropeyap.flare_num
    assert not x_ropeyap.iux2aux
    assert not x_ropeyap.iux_knot
    assert not x_ropeyap.aux_knot
    assert not x_ropeyap.labelyap
    assert set(x_ropeyap.__dict__.keys()) == {
        kw.flare_audie,
        kw.flare_num,
        kw.iux2aux,
        kw.iux_knot,
        kw.aux_knot,
        "labelyap",
    }


def test_ropeyap_shop_ReturnsObj_Scenario0():
    # ESTABLISH
    spark7 = 7
    iux2aux = {exx.xio: exx.sue}
    slash_iux_knot = "/"
    colon_aux_knot = ":"

    # WHEN
    e7_ropeyap = ropeyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux2aux=iux2aux,
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
    )

    # THEN
    assert e7_ropeyap.flare_audie == exx.bob
    assert e7_ropeyap.flare_num == spark7
    assert e7_ropeyap.iux2aux == iux2aux
    assert e7_ropeyap.iux_knot == slash_iux_knot
    assert e7_ropeyap.aux_knot == colon_aux_knot
    assert e7_ropeyap.labelyap == labelyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
    )


def test_ropeyap_shop_ReturnsObj_Scenario2():
    # ESTABLISH / WHEN
    x_ropeyap = ropeyap_shop()

    # THEN
    assert x_ropeyap.iux2aux == {}
    assert x_ropeyap.iux_knot == default_knot_if_None()
    assert x_ropeyap.aux_knot == default_knot_if_None()
    assert x_ropeyap.flare_audie is None
    assert x_ropeyap.flare_num == 0
    assert x_ropeyap.labelyap == labelyap_shop(
        flare_num=0,
        iux_knot=default_knot_if_None(),
        aux_knot=default_knot_if_None(),
    )


def test_ropeyap_shop_ReturnsObj_Scenario3_JargonCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    iux2aux = {exx.xio: exx.sue}
    x_nan = float("nan")

    # WHEN
    x_ropeyap = ropeyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux2aux=iux2aux,
        iux_knot=x_nan,
        aux_knot=x_nan,
    )

    # THEN
    assert x_ropeyap.flare_audie == exx.bob
    assert x_ropeyap.flare_num == spark7
    assert x_ropeyap.iux2aux == iux2aux
    assert x_ropeyap.iux_knot == default_knot_if_None()
    assert x_ropeyap.aux_knot == default_knot_if_None()


def test_RopeYap_set_all_iux2aux_SetsAttr():
    # ESTABLISH
    contact_name_ropeyap = ropeyap_shop()
    x_iux2aux = {exx.xio: exx.sue, exx.zia: exx.zia}
    assert contact_name_ropeyap.iux2aux != x_iux2aux

    # WHEN
    contact_name_ropeyap.set_all_iux2aux(x_iux2aux)

    # THEN
    assert contact_name_ropeyap.iux2aux == x_iux2aux


def test_RopeYap_set_iux2aux_SetsAttr():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.iux2aux == {}

    # WHEN
    x_ropeyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.iux2aux == {exx.xio: exx.sue}


def test_RopeYap_get_aux_value_ReturnsObj():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.get_aux_value(exx.xio) != exx.sue

    # WHEN
    x_ropeyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.get_aux_value(exx.xio) == exx.sue


def test_RopeYap_iux2aux_exists_ReturnsObj():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.sue) is False
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_ropeyap.iux2aux_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropeyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.sue)
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_ropeyap.iux2aux_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropeyap.set_iux2aux(exx.zia, exx.zia)

    # THEN
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.sue)
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_ropeyap.iux2aux_exists(exx.zia, exx.zia)


def test_RopeYap_iux_exists_ReturnsObj():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.iux_exists(exx.xio) is False
    assert x_ropeyap.iux_exists(exx.sue) is False
    assert x_ropeyap.iux_exists(exx.bob) is False
    assert x_ropeyap.iux_exists(exx.zia) is False

    # WHEN
    x_ropeyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.iux_exists(exx.xio)
    assert x_ropeyap.iux_exists(exx.sue) is False
    assert x_ropeyap.iux_exists(exx.bob) is False
    assert x_ropeyap.iux_exists(exx.zia) is False

    # WHEN
    x_ropeyap.set_iux2aux(exx.zia, exx.zia)

    # THEN
    assert x_ropeyap.iux_exists(exx.xio)
    assert x_ropeyap.iux_exists(exx.sue) is False
    assert x_ropeyap.iux_exists(exx.bob) is False
    assert x_ropeyap.iux_exists(exx.zia)


def test_RopeYap_del_iux2aux_SetsAttr():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    x_ropeyap.set_iux2aux(exx.xio, exx.sue)
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.sue)

    # WHEN
    x_ropeyap.del_iux2aux(exx.xio)

    # THEN
    assert x_ropeyap.iux2aux_exists(exx.xio, exx.sue) is False


def test_RopeYap_set_label_SetsAttr():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.labelyap.iux2aux == {}

    # WHEN
    x_ropeyap.set_label(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.labelyap.iux2aux == {exx.xio: exx.sue}


def test_RopeYap_set_label_RaisesExceptionWhen_knot_In_iux_label():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    sue_iux = f"Sue{x_ropeyap.iux_knot}"
    sue_aux = "Sue"
    assert x_ropeyap.labelyap.iux2aux == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ropeyap.set_label(sue_iux, sue_aux)
    exception_str = f"label cannot have iux_label '{sue_iux}'. It must be not have knot {x_ropeyap.iux_knot}."
    assert str(excinfo.value) == exception_str


def test_RopeYap_set_label_RaisesExceptionWhen_knot_In_aux_label():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    sue_aux = f"Sue{x_ropeyap.iux_knot}"
    sue_iux = "Sue"
    assert x_ropeyap.labelyap.iux2aux == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_ropeyap.set_label(sue_iux, sue_aux)
    exception_str = f"label cannot have aux_label '{sue_aux}'. It must be not have knot {x_ropeyap.aux_knot}."
    assert str(excinfo.value) == exception_str


def test_RopeJargon_label_exists_ReturnsObj():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.label_exists(exx.xio, exx.sue) is False
    assert x_ropeyap.label_exists(exx.xio, exx.zia) is False
    assert x_ropeyap.label_exists(exx.xio, exx.bob) is False
    assert x_ropeyap.label_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropeyap.set_label(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.label_exists(exx.xio, exx.sue)
    assert x_ropeyap.label_exists(exx.xio, exx.zia) is False
    assert x_ropeyap.label_exists(exx.xio, exx.bob) is False
    assert x_ropeyap.label_exists(exx.zia, exx.zia) is False

    # WHEN
    x_ropeyap.set_label(exx.zia, exx.zia)

    # THEN
    assert x_ropeyap.label_exists(exx.xio, exx.sue)
    assert x_ropeyap.label_exists(exx.xio, exx.zia) is False
    assert x_ropeyap.label_exists(exx.xio, exx.bob) is False
    assert x_ropeyap.label_exists(exx.zia, exx.zia)


def test_RopeYap_iux_label_exists_ReturnsObj():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    assert x_ropeyap.iux_label_exists(exx.xio) is False
    assert x_ropeyap.iux_label_exists(exx.sue) is False
    assert x_ropeyap.iux_label_exists(exx.bob) is False
    assert x_ropeyap.iux_label_exists(exx.zia) is False

    # WHEN
    x_ropeyap.set_label(exx.xio, exx.sue)

    # THEN
    assert x_ropeyap.iux_label_exists(exx.xio)
    assert x_ropeyap.iux_label_exists(exx.sue) is False
    assert x_ropeyap.iux_label_exists(exx.bob) is False
    assert x_ropeyap.iux_label_exists(exx.zia) is False

    # WHEN
    x_ropeyap.set_label(exx.zia, exx.zia)

    # THEN
    assert x_ropeyap.iux_label_exists(exx.xio)
    assert x_ropeyap.iux_label_exists(exx.sue) is False
    assert x_ropeyap.iux_label_exists(exx.bob) is False
    assert x_ropeyap.iux_label_exists(exx.zia)


def test_RopeYap_del_label_SetsAttr():
    # ESTABLISH
    x_ropeyap = ropeyap_shop(None)
    x_ropeyap.set_label(exx.xio, exx.sue)
    assert x_ropeyap.label_exists(exx.xio, exx.sue)

    # WHEN
    x_ropeyap.del_label(exx.xio)

    # THEN
    assert x_ropeyap.label_exists(exx.xio, exx.sue) is False


def test_RopeYap_set_label_Edits_iux2aux():
    # ESTABLISH
    iux_amy45_str = to_rope("amy45")
    aux_amy87_str = to_rope("amy87")
    casa_iux_str = "casa"
    casa_aux_str = "maison"
    casa_iux_rope = create_rope(iux_amy45_str, casa_iux_str)
    casa_aux_rope = create_rope(aux_amy87_str, casa_aux_str)
    clean_iux_str = "clean"
    clean_aux_str = "propre"
    clean_iux_rope = create_rope(casa_iux_rope, clean_iux_str)
    clean_aux_rope = create_rope(casa_aux_rope, clean_aux_str)

    sweep_iux_rope = create_rope(clean_iux_rope, exx.sweep)
    sweep_aux_rope = create_rope(clean_aux_rope, exx.sweep)
    x_ropeyap = ropeyap_shop()
    x_ropeyap.set_iux2aux(iux_amy45_str, aux_amy87_str)
    x_ropeyap.set_iux2aux(casa_iux_rope, casa_aux_rope)
    x_ropeyap.set_iux2aux(clean_iux_rope, clean_aux_rope)
    x_ropeyap.set_iux2aux(sweep_iux_rope, sweep_aux_rope)
    assert x_ropeyap.iux2aux_exists(iux_amy45_str, aux_amy87_str)
    assert x_ropeyap.iux2aux_exists(casa_iux_rope, casa_aux_rope)
    assert x_ropeyap.iux2aux_exists(clean_iux_rope, clean_aux_rope)
    assert x_ropeyap.iux2aux_exists(sweep_iux_rope, sweep_aux_rope)

    # WHEN
    menage_aux_str = "menage"
    x_ropeyap.set_label(clean_iux_str, menage_aux_str)

    # THEN
    menage_aux_rope = create_rope(casa_aux_rope, menage_aux_str)
    sweep_menage_aux_rope = create_rope(menage_aux_rope, exx.sweep)
    assert x_ropeyap.iux2aux_exists(iux_amy45_str, aux_amy87_str)
    assert x_ropeyap.iux2aux_exists(casa_iux_rope, casa_aux_rope)
    assert x_ropeyap.iux2aux_exists(clean_iux_rope, menage_aux_rope)
    assert x_ropeyap.iux2aux_exists(sweep_iux_rope, sweep_menage_aux_rope)


def test_RopeYap_to_dict_ReturnsObj():
    # ESTABLISH
    clean_iux = "clean"
    clean_aux = "propre"
    casa_iux = "casa1"
    casa_aux = "casa2"
    slash_iux_knot = "/"
    x_ropeyap = ropeyap_shop(exx.sue, iux_knot=slash_iux_knot)
    x1_rope_yap_dict = {
        kw.flare_num: 0,
        kw.flare_audie: exx.sue,
        kw.aux_knot: x_ropeyap.aux_knot,
        kw.iux2aux: {},
        kw.iux_knot: x_ropeyap.iux_knot,
    }
    # print(f"           {x1_rope_yap_json=}")
    assert x_ropeyap.to_dict() == x1_rope_yap_dict

    # WHEN
    spark7 = 7
    x_ropeyap.set_iux2aux(clean_iux, clean_aux)
    x_ropeyap.flare_num = spark7
    # THEN
    x2_rope_yap_dict = {
        kw.flare_num: spark7,
        kw.flare_audie: exx.sue,
        kw.aux_knot: x_ropeyap.aux_knot,
        kw.iux2aux: {clean_iux: clean_aux},
        kw.iux_knot: x_ropeyap.iux_knot,
    }
    print(f"           {x2_rope_yap_dict=}")
    print(f"{x_ropeyap.to_dict()=}")
    assert x_ropeyap.to_dict() == x2_rope_yap_dict


def test_get_ropeyap_from_dict_ReturnsObj():
    # ESTABLISH
    clean_iux = "clean"
    clean_aux = "propre"
    spark7 = 7
    slash_iux_knot = "/"
    x_ropeyap = ropeyap_shop(exx.sue, spark7, iux_knot=slash_iux_knot)
    x_ropeyap.set_iux2aux(clean_iux, clean_aux)
    x_ropeyap.set_label("bob", "bobito")

    # WHEN
    gen_ropeyap = get_ropeyap_from_dict(x_ropeyap.to_dict())

    # THEN
    assert gen_ropeyap.flare_audie == x_ropeyap.flare_audie
    assert gen_ropeyap.flare_num == x_ropeyap.flare_num
    assert gen_ropeyap.flare_num == spark7
    assert gen_ropeyap.labelyap.flare_audie == x_ropeyap.labelyap.flare_audie
    assert gen_ropeyap.labelyap.iux2aux != x_ropeyap.labelyap.iux2aux
    assert gen_ropeyap.labelyap != x_ropeyap.labelyap
    assert gen_ropeyap.iux2aux == x_ropeyap.iux2aux
    assert gen_ropeyap.iux_knot == x_ropeyap.iux_knot
    assert gen_ropeyap.aux_knot == x_ropeyap.aux_knot


def test_RopeYap_all_iux_parent_ropes_exist_ReturnsObj_RopeTerm():
    # ESTABLISH
    iux_r_knot = "/"
    clean_iux_parent_rope = to_rope("amy45", iux_r_knot)
    clean_iux_str = "clean"
    clean_iux_rope = create_rope(clean_iux_parent_rope, clean_iux_str, iux_r_knot)

    x_ropeyap = ropeyap_shop(iux_knot=iux_r_knot)
    assert x_ropeyap.iux_exists(clean_iux_parent_rope) is False
    assert x_ropeyap.iux_exists(clean_iux_rope) is False
    assert x_ropeyap.all_iux_parent_ropes_exist()

    # WHEN
    x_ropeyap.set_iux2aux(clean_iux_rope, to_rope("any", iux_r_knot))
    # THEN
    assert x_ropeyap.iux_exists(clean_iux_parent_rope) is False
    assert x_ropeyap.iux_exists(clean_iux_rope)
    assert x_ropeyap.all_iux_parent_ropes_exist() is False

    # WHEN
    x_ropeyap.set_iux2aux(clean_iux_parent_rope, to_rope("any"))
    # THEN
    assert x_ropeyap.iux_exists(clean_iux_parent_rope)
    assert x_ropeyap.iux_exists(clean_iux_rope)
    assert x_ropeyap.all_iux_parent_ropes_exist()


def test_RopeYap_is_valid_ReturnsObj_Scenario0_plan_label_str():
    # ESTABLISH
    x_iux_knot = "/"
    x_aux_knot = ":"
    labelterm_ropeyap = ropeyap_shop(iux_knot=x_iux_knot, aux_knot=x_aux_knot)

    clean_aux = to_rope("propre", x_aux_knot)
    casa_iux = to_rope("casa", x_iux_knot)
    mop_iux = create_rope(casa_iux, "mop", x_iux_knot)
    mop_aux = "mop"
    casa_aux = "casa"
    assert labelterm_ropeyap.is_valid()

    # WHEN
    labelterm_ropeyap.set_iux2aux(exx.clean, clean_aux)
    # THEN
    assert labelterm_ropeyap.is_valid()

    # WHEN
    labelterm_ropeyap.set_iux2aux(mop_iux, mop_aux)
    # THEN
    assert labelterm_ropeyap.is_valid() is False


def test_RopeYap_is_valid_ReturnsObj_Scenario1_rope_str():
    # ESTABLISH
    amy45_str = "amy45"
    iux_r_knot = "/"
    aux_r_knot = ":"
    clean_iux_str = "clean"
    clean_iux_rope = f"{amy45_str}{iux_r_knot}{clean_iux_str}"
    clean_aux_str = "prop"
    clean_aux_rope = f"{amy45_str}{aux_r_knot}{clean_aux_str}"
    # casa_iux = f"casa{iux_knot}"
    # casa_aux = f"casa"
    x_ropeyap = ropeyap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
    x_ropeyap.set_iux2aux(amy45_str, amy45_str)
    assert x_ropeyap.is_valid()
    assert x_ropeyap.iux2aux_exists(clean_iux_rope, clean_aux_rope) is False

    # WHEN
    x_ropeyap.set_iux2aux(clean_iux_rope, clean_aux_rope)
    # THEN
    assert x_ropeyap.is_valid()
    assert x_ropeyap.iux2aux_exists(clean_iux_rope, clean_aux_rope)


def test_RopeYap_is_valid_ReturnsObj_Scenario3_RopeTerm():
    # ESTABLISH
    iux_r_knot = "/"
    clean_iux_parent_rope = to_rope("amy45", iux_r_knot)
    clean_iux_str = "clean"
    clean_iux_rope = create_rope(clean_iux_parent_rope, clean_iux_str, iux_r_knot)

    x_ropeyap = ropeyap_shop(iux_knot=iux_r_knot)
    assert x_ropeyap.iux_exists(clean_iux_parent_rope) is False
    assert x_ropeyap.iux_exists(clean_iux_rope) is False
    assert x_ropeyap.all_iux_parent_ropes_exist()
    assert x_ropeyap.is_valid()

    # WHEN
    x_ropeyap.set_iux2aux(clean_iux_rope, "any")
    # THEN
    assert x_ropeyap.iux_exists(clean_iux_parent_rope) is False
    assert x_ropeyap.iux_exists(clean_iux_rope)
    assert x_ropeyap.all_iux_parent_ropes_exist() is False
    assert x_ropeyap.is_valid() is False

    # WHEN
    x_ropeyap.set_iux2aux(clean_iux_parent_rope, "any")
    # THEN
    assert x_ropeyap.iux_exists(clean_iux_parent_rope)
    assert x_ropeyap.iux_exists(clean_iux_rope)
    assert x_ropeyap.all_iux_parent_ropes_exist()
    assert x_ropeyap.is_valid()


def test_inherit_ropeyap_ReturnsObj_Scenario0():
    # ESTABLISH
    old_ropeyap = ropeyap_shop(exx.zia, 3)
    new_ropeyap = ropeyap_shop(exx.zia, 5)
    # WHEN
    inherit_ropeyap(new_ropeyap, old_ropeyap)

    # THEN
    assert new_ropeyap
    assert new_ropeyap == ropeyap_shop(exx.zia, 5)


def test_inherit_ropeyap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_iux_knot():
    # ESTABLISH
    slash_iux_knot = "/"
    old_ropeyap = ropeyap_shop(exx.sue, 0, iux_knot=slash_iux_knot)
    new_ropeyap = ropeyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropeyap(new_ropeyap, old_ropeyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropeyap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_aux_knot():
    # ESTABLISH
    slash_iux_knot = "/"
    old_ropeyap = ropeyap_shop(exx.sue, 0, aux_knot=slash_iux_knot)
    new_ropeyap = ropeyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropeyap(new_ropeyap, old_ropeyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropeyap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_flare_audie():
    # ESTABLISH
    old_ropeyap = ropeyap_shop(exx.sue, 0)
    new_ropeyap = ropeyap_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropeyap(new_ropeyap, old_ropeyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_ropeyap_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_ropeyap = ropeyap_shop(exx.sue, 5)
    new_ropeyap = ropeyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_ropeyap(new_ropeyap, old_ropeyap)

    # THEN
    assert str(excinfo.value) == "older yapunit is not older"


def test_inherit_ropeyap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    xio_iux = "Xio"
    xio_aux = "Xioito"
    old_ropeyap = ropeyap_shop(exx.zia, 3)
    old_ropeyap.set_iux2aux(xio_iux, xio_aux)
    new_ropeyap = ropeyap_shop(exx.zia, 7)
    assert new_ropeyap.iux2aux_exists(xio_iux, xio_aux) is False

    # WHEN
    inherited_ropeyap = inherit_ropeyap(new_ropeyap, old_ropeyap)

    # THEN
    assert inherited_ropeyap.iux2aux_exists(xio_iux, xio_aux)
