from ch05_rope.rope import default_knot_if_None
from ch18_lingo.yap_term import (
    TitleYap,
    get_titleyap_from_dict,
    inherit_titleyap,
    titleyap_shop,
)
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
from pytest import raises as pytest_raises
from src.ch99_glossary.ch_keyword import Ch18Keywords as kw


def test_TitleYap_Exists():
    # ESTABLISH
    x_titleyap = TitleYap()

    # WHEN / THEN
    assert not x_titleyap.flare_audie
    assert not x_titleyap.flare_num
    assert not x_titleyap.iux2aux
    assert not x_titleyap.iux_knot
    assert not x_titleyap.aux_knot
    assert set(x_titleyap.__dict__.keys()) == {
        kw.flare_audie,
        kw.flare_num,
        kw.iux2aux,
        kw.iux_knot,
        kw.aux_knot,
    }


def test_titleyap_shop_ReturnsObj_Scenario0_NoParameters():
    # ESTABLISH / WHEN
    x_titleyap = titleyap_shop()

    # THEN
    assert not x_titleyap.flare_audie
    assert x_titleyap.flare_num == 0
    assert x_titleyap.iux2aux == {}
    assert x_titleyap.iux_knot == default_knot_if_None()
    assert x_titleyap.aux_knot == default_knot_if_None()


def test_titleyap_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    spark7 = 7
    iux2aux = {exx.xio: exx.sue}
    slash_iux_knot = "/"
    colon_aux_knot = ":"

    # WHEN
    x_titleyap = titleyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux2aux=iux2aux,
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
    )

    # THEN
    assert x_titleyap.flare_audie == exx.bob
    assert x_titleyap.flare_num == spark7
    assert x_titleyap.iux2aux == iux2aux
    assert x_titleyap.iux_knot == slash_iux_knot
    assert x_titleyap.aux_knot == colon_aux_knot


def test_titleyap_shop_ReturnsObj_Scenario2_lingoCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    iux2aux = {exx.xio: exx.sue}
    x_nan = float("nan")

    # WHEN
    x_titleyap = titleyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux2aux=iux2aux,
        iux_knot=x_nan,
        aux_knot=x_nan,
    )

    # THEN
    assert x_titleyap.flare_audie == exx.bob
    assert x_titleyap.flare_num == spark7
    assert x_titleyap.iux2aux == iux2aux
    assert x_titleyap.iux_knot == default_knot_if_None()
    assert x_titleyap.aux_knot == default_knot_if_None()


def test_TitleYap_set_all_iux2aux_SetsAttr():
    # ESTABLISH
    x_titleyap = titleyap_shop()
    x_iux2aux = {exx.xio: exx.sue, exx.zia: exx.zia}
    assert x_titleyap.iux2aux != x_iux2aux

    # WHEN
    x_titleyap.set_all_iux2aux(x_iux2aux)

    # THEN
    assert x_titleyap.iux2aux == x_iux2aux


def test_TitleYap_set_iux2aux_SetsAttr():
    # ESTABLISH
    x_titleyap = titleyap_shop(None)
    assert x_titleyap.iux2aux == {}

    # WHEN
    x_titleyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_titleyap.iux2aux == {exx.xio: exx.sue}


def test_TitleYap_get_aux_value_ReturnsObj():
    # ESTABLISH
    x_titleyap = titleyap_shop(None)
    assert x_titleyap.get_aux_value(exx.xio) != exx.sue

    # WHEN
    x_titleyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_titleyap.get_aux_value(exx.xio) == exx.sue


def test_TitleYap_iux2aux_exists_ReturnsObj():
    # ESTABLISH
    x_titleyap = titleyap_shop(None)
    assert x_titleyap.iux2aux_exists(exx.xio, exx.sue) is False
    assert x_titleyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_titleyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_titleyap.iux2aux_exists(exx.zia, exx.zia) is False

    # WHEN
    x_titleyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_titleyap.iux2aux_exists(exx.xio, exx.sue)
    assert x_titleyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_titleyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_titleyap.iux2aux_exists(exx.zia, exx.zia) is False

    # WHEN
    x_titleyap.set_iux2aux(exx.zia, exx.zia)

    # THEN
    assert x_titleyap.iux2aux_exists(exx.xio, exx.sue)
    assert x_titleyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_titleyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_titleyap.iux2aux_exists(exx.zia, exx.zia)


def test_TitleYap_iux_exists_ReturnsObj():
    # ESTABLISH
    x_titleyap = titleyap_shop(None)
    assert x_titleyap.iux_exists(exx.xio) is False
    assert x_titleyap.iux_exists(exx.sue) is False
    assert x_titleyap.iux_exists(exx.bob) is False
    assert x_titleyap.iux_exists(exx.zia) is False

    # WHEN
    x_titleyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_titleyap.iux_exists(exx.xio)
    assert x_titleyap.iux_exists(exx.sue) is False
    assert x_titleyap.iux_exists(exx.bob) is False
    assert x_titleyap.iux_exists(exx.zia) is False

    # WHEN
    x_titleyap.set_iux2aux(exx.zia, exx.zia)

    # THEN
    assert x_titleyap.iux_exists(exx.xio)
    assert x_titleyap.iux_exists(exx.sue) is False
    assert x_titleyap.iux_exists(exx.bob) is False
    assert x_titleyap.iux_exists(exx.zia)


def test_TitleYap_del_iux2aux_SetsAttr():
    # ESTABLISH
    x_titleyap = titleyap_shop(None)
    x_titleyap.set_iux2aux(exx.xio, exx.sue)
    assert x_titleyap.iux2aux_exists(exx.xio, exx.sue)

    # WHEN
    x_titleyap.del_iux2aux(exx.xio)

    # THEN
    assert x_titleyap.iux2aux_exists(exx.xio, exx.sue) is False


def test_TitleYap_reveal_aux_ReturnsObjAndSetsAttr_group_title():
    # ESTABLISH
    aux_r_knot = ":"
    iux_r_knot = "/"
    bowl_iux = f"bowl{iux_r_knot}"
    boulder_iux = f"boulder{iux_r_knot}_{aux_r_knot}"
    x_titleyap = titleyap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
    x_titleyap.iux_exists(bowl_iux) is False
    x_titleyap.iux_exists(boulder_iux) is False

    # WHEN
    bowl_aux = f"bowl{aux_r_knot}"
    assert x_titleyap.reveal_aux(bowl_iux) == bowl_aux

    # THEN
    assert x_titleyap.iux_exists(bowl_iux)
    assert x_titleyap.iux_exists(boulder_iux) is False
    assert x_titleyap.get_aux_value(bowl_iux) == bowl_aux

    # WHEN
    assert x_titleyap.reveal_aux(boulder_iux) is None
    # THEN
    assert x_titleyap.iux_exists(bowl_iux)
    assert x_titleyap.iux_exists(boulder_iux) is False


def test_TitleYap_to_dict_ReturnsObj():
    # ESTABLISH
    clean_iux = "clean"
    clean_aux = "propre"
    slash_iux_knot = "/"
    colon_aux_knot = ":"
    x_titleyap = titleyap_shop(
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
        flare_audie=exx.sue,
    )
    x1_rope_yap_dict = {
        kw.iux_knot: x_titleyap.iux_knot,
        kw.aux_knot: x_titleyap.aux_knot,
        kw.iux2aux: {},
        kw.flare_num: x_titleyap.flare_num,
        kw.flare_audie: x_titleyap.flare_audie,
    }
    assert x_titleyap.to_dict() == x1_rope_yap_dict

    # WHEN
    x_titleyap.set_iux2aux(clean_iux, clean_aux)
    # THEN
    x2_rope_yap_dict = {
        kw.iux_knot: x_titleyap.iux_knot,
        kw.aux_knot: x_titleyap.aux_knot,
        kw.iux2aux: {clean_iux: clean_aux},
        kw.flare_num: x_titleyap.flare_num,
        kw.flare_audie: exx.sue,
    }
    assert x_titleyap.to_dict() == x2_rope_yap_dict


def test_get_titleyap_from_dict_ReturnsObj():
    # ESTABLISH
    clean_iux = "clean"
    clean_aux = "propre"
    spark7 = 7
    slash_iux_knot = "/"
    x_titleyap = titleyap_shop(exx.sue, spark7, iux_knot=slash_iux_knot)
    x_titleyap.set_iux2aux(clean_iux, clean_aux)

    # WHEN
    gen_titleyap = get_titleyap_from_dict(x_titleyap.to_dict())

    # THEN
    assert gen_titleyap.flare_audie == x_titleyap.flare_audie
    assert gen_titleyap.flare_num == x_titleyap.flare_num
    assert gen_titleyap.flare_num == spark7
    assert gen_titleyap == x_titleyap


def test_TitleYap_is_aux_knot_inclusion_correct_ReturnsObj():
    # ESTABLISH
    aux_knot = "/"
    zia_iux = "Zia"
    zia_aux = f"Zia{aux_knot}"
    x_titleyap = titleyap_shop(aux_knot=aux_knot)
    assert x_titleyap._is_aux_knot_inclusion_correct()

    # WHEN
    x_titleyap.set_iux2aux(zia_iux, zia_aux)
    # THEN
    assert x_titleyap._is_aux_knot_inclusion_correct()

    # WHEN
    x_titleyap.set_iux2aux(exx.xio, exx.sue)
    # THEN
    assert x_titleyap._is_aux_knot_inclusion_correct() is False


def test_TitleYap_is_iux_knot_inclusion_correct_ReturnsObj():
    # ESTABLISH
    iux_knot = "/"
    zia_aux = "Zia"
    zia_iux = f"Zia{iux_knot}"
    x_titleyap = titleyap_shop(iux_knot=iux_knot)
    assert x_titleyap._is_iux_knot_inclusion_correct()

    # WHEN
    x_titleyap.set_iux2aux(zia_iux, zia_aux)
    # THEN
    assert x_titleyap._is_iux_knot_inclusion_correct()

    # WHEN
    x_titleyap.set_iux2aux(exx.xio, exx.sue)
    # THEN
    assert x_titleyap._is_iux_knot_inclusion_correct() is False


def test_TitleYap_is_valid_ReturnsObj():
    # ESTABLISH
    iux_knot = ":"
    aux_knot = "/"
    sue_iux = f"Xio{iux_knot}"
    sue_aux = f"Sue{aux_knot}"
    zia_iux = "Zia"
    zia_aux = f"Zia{aux_knot}"
    x_titleyap = titleyap_shop(iux_knot=iux_knot, aux_knot=aux_knot)
    assert x_titleyap.is_valid()

    # WHEN
    x_titleyap.set_iux2aux(sue_iux, sue_aux)
    # THEN
    assert x_titleyap.is_valid()

    # WHEN
    x_titleyap.set_iux2aux(zia_iux, zia_aux)
    # THEN
    assert x_titleyap.is_valid() is False


def test_inherit_titleyap_ReturnsObj_Scenario0():
    # ESTABLISH
    old_titleyap = titleyap_shop(exx.zia, 3)
    new_titleyap = titleyap_shop(exx.zia, 5)
    # WHEN
    inherit_titleyap(new_titleyap, old_titleyap)

    # THEN
    assert new_titleyap
    assert new_titleyap == titleyap_shop(exx.zia, 5)


def test_inherit_titleyap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_iux_knot():
    # ESTABLISH
    slash_iux_knot = "/"
    old_titleyap = titleyap_shop(exx.sue, 0, iux_knot=slash_iux_knot)
    new_titleyap = titleyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_titleyap(new_titleyap, old_titleyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_titleyap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_aux_knot():
    # ESTABLISH
    slash_iux_knot = "/"
    old_titleyap = titleyap_shop(exx.sue, 0, aux_knot=slash_iux_knot)
    new_titleyap = titleyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_titleyap(new_titleyap, old_titleyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_titleyap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_flare_audie():
    # ESTABLISH
    old_titleyap = titleyap_shop(exx.sue, 0)
    new_titleyap = titleyap_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_titleyap(new_titleyap, old_titleyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_titleyap_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_titleyap = titleyap_shop(exx.sue, 5)
    new_titleyap = titleyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_titleyap(new_titleyap, old_titleyap)

    # THEN
    assert str(excinfo.value) == "older yapunit is not older"


def test_inherit_titleyap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    xio_iux = "Xio"
    xio_aux = "Xioito"
    old_titleyap = titleyap_shop(exx.zia, 3)
    old_titleyap.set_iux2aux(xio_iux, xio_aux)
    new_titleyap = titleyap_shop(exx.zia, 7)
    assert new_titleyap.iux2aux_exists(xio_iux, xio_aux) is False

    # WHEN
    inherited_titleyap = inherit_titleyap(new_titleyap, old_titleyap)

    # THEN
    assert inherited_titleyap.iux2aux_exists(xio_iux, xio_aux)
