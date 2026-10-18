from ch05_rope.rope import default_knot_if_None
from ch18_lingo.yap_term import (
    LabelYap,
    get_labelyap_from_dict,
    inherit_labelyap,
    labelyap_shop,
)
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
from pytest import raises as pytest_raises
from src.ch99_glossary.ch_keyword import Ch18Keywords as kw


def test_LabelYap_Exists():
    # ESTABLISH
    x_labelyap = LabelYap()

    # WHEN / THEN
    assert not x_labelyap.flare_audie
    assert not x_labelyap.flare_num
    assert not x_labelyap.iux2aux
    assert not x_labelyap.iux_knot
    assert not x_labelyap.aux_knot
    assert set(x_labelyap.__dict__.keys()) == {
        kw.flare_audie,
        kw.flare_num,
        kw.iux2aux,
        kw.iux_knot,
        kw.aux_knot,
    }


def test_labelyap_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_labelyap = labelyap_shop()

    # THEN
    assert not x_labelyap.flare_audie
    assert x_labelyap.flare_num == 0
    assert x_labelyap.iux2aux == {}
    assert x_labelyap.iux_knot == default_knot_if_None()
    assert x_labelyap.aux_knot == default_knot_if_None()


def test_labelyap_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    spark7 = 7
    iux2aux = {exx.xio: exx.sue}
    slash_iux_knot = "/"
    colon_aux_knot = ":"

    # WHEN
    x_labelyap = labelyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux2aux=iux2aux,
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
    )

    # THEN
    assert x_labelyap.flare_audie == exx.bob
    assert x_labelyap.flare_num == spark7
    assert x_labelyap.iux2aux == iux2aux
    assert x_labelyap.iux_knot == slash_iux_knot
    assert x_labelyap.aux_knot == colon_aux_knot


def test_labelyap_shop_ReturnsObj_Scenario2_LingoCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    iux2aux = {exx.xio: exx.sue}
    x_nan = float("nan")

    # WHEN
    x_labelyap = labelyap_shop(
        flare_audie=exx.bob,
        flare_num=spark7,
        iux2aux=iux2aux,
        iux_knot=x_nan,
        aux_knot=x_nan,
    )

    # THEN
    assert x_labelyap.flare_audie == exx.bob
    assert x_labelyap.flare_num == spark7
    assert x_labelyap.iux2aux == iux2aux
    assert x_labelyap.iux_knot == default_knot_if_None()
    assert x_labelyap.aux_knot == default_knot_if_None()


def test_LabelYap_set_all_iux2aux_SetsAttr():
    # ESTABLISH
    x_labelyap = labelyap_shop()
    x_iux2aux = {exx.xio: exx.sue, exx.zia: exx.zia}
    assert x_labelyap.iux2aux != x_iux2aux

    # WHEN
    x_labelyap.set_all_iux2aux(x_iux2aux)

    # THEN
    assert x_labelyap.iux2aux == x_iux2aux


def test_LabelYap_set_all_iux2aux_DoesNotRaiseErrorIfParameterSetToTrue():
    # ESTABLISH
    x_labelyap = labelyap_shop(None)
    x_iux2aux = {exx.xio: exx.sue}
    assert x_labelyap.iux2aux != x_iux2aux

    # WHEN
    x_labelyap.set_all_iux2aux(x_iux2aux)

    # THEN
    assert x_labelyap.iux2aux == x_iux2aux


def test_LabelYap_set_iux2aux_SetsAttr():
    # ESTABLISH
    x_labelyap = labelyap_shop(None)
    assert x_labelyap.iux2aux == {}

    # WHEN
    x_labelyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_labelyap.iux2aux == {exx.xio: exx.sue}


def test_LabelYap_get_aux_value_ReturnsObj():
    # ESTABLISH
    x_labelyap = labelyap_shop(None)
    assert x_labelyap.get_aux_value(exx.xio) != exx.sue

    # WHEN
    x_labelyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_labelyap.get_aux_value(exx.xio) == exx.sue


def test_LabelYap_iux2aux_exists_ReturnsObj():
    # ESTABLISH
    x_labelyap = labelyap_shop(None)
    assert x_labelyap.iux2aux_exists(exx.xio, exx.sue) is False
    assert x_labelyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_labelyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_labelyap.iux2aux_exists(exx.zia, exx.zia) is False

    # WHEN
    x_labelyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_labelyap.iux2aux_exists(exx.xio, exx.sue)
    assert x_labelyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_labelyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_labelyap.iux2aux_exists(exx.zia, exx.zia) is False

    # WHEN
    x_labelyap.set_iux2aux(exx.zia, exx.zia)

    # THEN
    assert x_labelyap.iux2aux_exists(exx.xio, exx.sue)
    assert x_labelyap.iux2aux_exists(exx.xio, exx.zia) is False
    assert x_labelyap.iux2aux_exists(exx.xio, exx.bob) is False
    assert x_labelyap.iux2aux_exists(exx.zia, exx.zia)


def test_LabelYap_iux_exists_ReturnsObj():
    # ESTABLISH
    x_labelyap = labelyap_shop(None)
    assert x_labelyap.iux_exists(exx.xio) is False
    assert x_labelyap.iux_exists(exx.sue) is False
    assert x_labelyap.iux_exists(exx.bob) is False
    assert x_labelyap.iux_exists(exx.zia) is False

    # WHEN
    x_labelyap.set_iux2aux(exx.xio, exx.sue)

    # THEN
    assert x_labelyap.iux_exists(exx.xio)
    assert x_labelyap.iux_exists(exx.sue) is False
    assert x_labelyap.iux_exists(exx.bob) is False
    assert x_labelyap.iux_exists(exx.zia) is False

    # WHEN
    x_labelyap.set_iux2aux(exx.zia, exx.zia)

    # THEN
    assert x_labelyap.iux_exists(exx.xio)
    assert x_labelyap.iux_exists(exx.sue) is False
    assert x_labelyap.iux_exists(exx.bob) is False
    assert x_labelyap.iux_exists(exx.zia)


def test_LabelYap_del_iux2aux_SetsAttr():
    # ESTABLISH
    x_labelyap = labelyap_shop(None)
    x_labelyap.set_iux2aux(exx.xio, exx.sue)
    assert x_labelyap.iux2aux_exists(exx.xio, exx.sue)

    # WHEN
    x_labelyap.del_iux2aux(exx.xio)

    # THEN
    assert x_labelyap.iux2aux_exists(exx.xio, exx.sue) is False


def test_LabelYap_reveal_aux_ReturnsObjAndSetsAttr_label():
    # ESTABLISH
    aux_r_knot = ":"
    iux_r_knot = "/"
    bowl_iux = f"bowl{iux_r_knot}"
    boulder_iux = f"boulder{iux_r_knot}_{aux_r_knot}"
    x_labelyap = labelyap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
    x_labelyap.iux_exists(bowl_iux) is False
    x_labelyap.iux_exists(boulder_iux) is False

    # WHEN
    bowl_aux = f"bowl{aux_r_knot}"
    assert x_labelyap.reveal_aux(bowl_iux) == bowl_aux

    # THEN
    assert x_labelyap.iux_exists(bowl_iux)
    assert x_labelyap.iux_exists(boulder_iux) is False
    assert x_labelyap.get_aux_value(bowl_iux) == bowl_aux

    # WHEN
    assert x_labelyap.reveal_aux(boulder_iux) is None
    # THEN
    assert x_labelyap.iux_exists(bowl_iux)
    assert x_labelyap.iux_exists(boulder_iux) is False


def test_LabelYap_to_dict_ReturnsObj():
    # ESTABLISH
    clean_iux = "clean"
    clean_aux = "propre"
    spark7 = 7
    slash_iux_knot = "/"
    colon_aux_knot = ":"
    x_labelyap = labelyap_shop(
        exx.sue,
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
    )
    x1_rope_yap_dict = {
        kw.iux_knot: x_labelyap.iux_knot,
        kw.aux_knot: x_labelyap.aux_knot,
        kw.iux2aux: {},
        kw.flare_audie: x_labelyap.flare_audie,
        kw.flare_num: x_labelyap.flare_num,
    }
    assert x_labelyap.to_dict() == x1_rope_yap_dict

    # WHEN
    x_labelyap.set_iux2aux(clean_iux, clean_aux)
    x_labelyap.flare_num = spark7
    # THEN
    x2_rope_yap_dict = {
        kw.iux_knot: x_labelyap.iux_knot,
        kw.aux_knot: x_labelyap.aux_knot,
        kw.iux2aux: {clean_iux: clean_aux},
        kw.flare_audie: exx.sue,
        kw.flare_num: spark7,
    }
    assert x_labelyap.to_dict() == x2_rope_yap_dict


def test_get_labelyap_from_dict_ReturnsObj():
    # ESTABLISH
    clean_iux = "clean"
    clean_aux = "propre"
    spark7 = 7
    slash_iux_knot = "/"
    x_labelyap = labelyap_shop(exx.sue, spark7, iux_knot=slash_iux_knot)
    x_labelyap.set_iux2aux(clean_iux, clean_aux)

    # WHEN
    gen_labelyap = get_labelyap_from_dict(x_labelyap.to_dict())

    # THEN
    assert gen_labelyap.flare_audie == x_labelyap.flare_audie
    assert gen_labelyap.flare_num == x_labelyap.flare_num
    assert gen_labelyap.flare_num == spark7
    assert gen_labelyap == x_labelyap


def test_LabelYap_is_aux_knot_inclusion_correct_ReturnsObj():
    # ESTABLISH
    aux_knot = "/"
    zia_iux = "Zia"
    zia_aux = f"Zia{aux_knot}"
    x_labelyap = labelyap_shop(aux_knot=aux_knot)
    assert x_labelyap._is_aux_knot_inclusion_correct()

    # WHEN
    x_labelyap.set_iux2aux(exx.xio, exx.sue)
    # THEN
    assert x_labelyap._is_aux_knot_inclusion_correct()

    # WHEN
    x_labelyap.set_iux2aux(zia_iux, zia_aux)
    # THEN
    assert x_labelyap._is_aux_knot_inclusion_correct() is False


def test_LabelYap_is_iux_knot_inclusion_correct_ReturnsObj():
    # ESTABLISH
    xio_iux = "Xio"
    xio_aux = "XioXio"
    iux_knot = "/"
    zia_iux = f"Zia{iux_knot}"
    zia_aux = "Zia"
    x_labelyap = labelyap_shop(iux_knot=iux_knot)
    assert x_labelyap._is_iux_knot_inclusion_correct()

    # WHEN
    x_labelyap.set_iux2aux(xio_iux, xio_aux)
    # THEN
    assert x_labelyap._is_iux_knot_inclusion_correct()

    # WHEN
    x_labelyap.set_iux2aux(zia_iux, zia_aux)
    # THEN
    assert x_labelyap._is_iux_knot_inclusion_correct() is False


def test_LabelYap_is_valid_ReturnsObj():
    # ESTABLISH
    iux_knot = ":"
    aux_knot = "/"
    sue_iux = f"Xio{iux_knot}"
    sue_with_knot = f"Sue{aux_knot}"
    sue_without_knot = f"Sue{iux_knot}"
    zia_iux = "Zia"
    zia_aux = f"Zia{aux_knot}"
    x_labelyap = labelyap_shop(iux_knot=iux_knot, aux_knot=aux_knot)
    assert x_labelyap.is_valid()

    # WHEN
    x_labelyap.set_iux2aux(sue_iux, sue_with_knot)
    # THEN
    assert x_labelyap.is_valid() is False

    # WHEN
    x_labelyap.set_iux2aux(zia_iux, zia_aux)
    # THEN
    assert x_labelyap.is_valid() is False

    # WHEN
    x_labelyap.set_iux2aux(sue_iux, sue_without_knot)
    # THEN
    assert x_labelyap.is_valid() is False


def test_inherit_labelyap_ReturnsObj_Scenario0():
    # ESTABLISH
    old_labelyap = labelyap_shop(exx.zia, 3)
    new_labelyap = labelyap_shop(exx.zia, 5)

    # WHEN
    inherit_labelyap(new_labelyap, old_labelyap)

    # THEN
    assert new_labelyap
    assert new_labelyap == labelyap_shop(exx.zia, 5)


def test_inherit_labelyap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_iux_knot():
    # ESTABLISH
    slash_iux_knot = "/"
    old_labelyap = labelyap_shop(exx.sue, 0, iux_knot=slash_iux_knot)
    new_labelyap = labelyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelyap(new_labelyap, old_labelyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelyap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_aux_knot():
    # ESTABLISH
    slash_iux_knot = "/"
    old_labelyap = labelyap_shop(exx.sue, 0, aux_knot=slash_iux_knot)
    new_labelyap = labelyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelyap(new_labelyap, old_labelyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelyap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_flare_audie():
    # ESTABLISH
    old_labelyap = labelyap_shop(exx.sue, 0)
    new_labelyap = labelyap_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelyap(new_labelyap, old_labelyap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_labelyap_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_labelyap = labelyap_shop(exx.sue, 5)
    new_labelyap = labelyap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_labelyap(new_labelyap, old_labelyap)

    # THEN
    assert str(excinfo.value) == "older yapunit is not older"


def test_inherit_labelyap_ReturnsObj_Scenario6_inheritFromOld():
    # ESTABLISH
    xio_iux = "Xio"
    xio_aux = "Xioito"
    old_labelyap = labelyap_shop(exx.zia, 3)
    old_labelyap.set_iux2aux(xio_iux, xio_aux)
    new_labelyap = labelyap_shop(exx.zia, 7)
    assert new_labelyap.iux2aux_exists(xio_iux, xio_aux) is False

    # WHEN
    inherited_labelyap = inherit_labelyap(new_labelyap, old_labelyap)

    # THEN
    assert inherited_labelyap.iux2aux_exists(xio_iux, xio_aux)
