from ch05_rope.rope import default_knot_if_None
from ch18_lingo.yap_term import (
    NameYap,
    # get_nameyap_from_dict,
    # inherit_nameyap,
    # nameyap_shop,
)
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
from numpy import int64 as numpy_int64
from pytest import raises as pytest_raises


def test_NameYap_Exists():
    # ESTABLISH
    x_nameyap = NameYap()

    # WHEN / THEN
    assert not x_nameyap.flare_audie
    assert not x_nameyap.flare_num
    assert not x_nameyap.iux2aux
    assert not x_nameyap.iux_knot
    assert not x_nameyap.aux_knot


# def test_nameyap_shop_ReturnsObj_Scenario0():
#     # ESTABLISH / WHEN
#     x_nameyap = nameyap_shop()

#     # THEN
#     assert not x_nameyap.flare_audie
#     assert x_nameyap.flare_num == 0
#     assert x_nameyap.iux2aux == {}
#     assert x_nameyap.unknown_str == default_unknown_str_if_None()
#     assert x_nameyap.iux_knot == default_knot_if_None()
#     assert x_nameyap.aux_knot == default_knot_if_None()


# def test_nameyap_shop_ReturnsObj_Scenario1_WithParameters():
#     # ESTABLISH
#     flare7 = 7
#     iux2aux = {exx.xio: exx.sue}
#     x_unknown_str = "UnknownTerm"
#     slash_iux_knot = "/"
#     colon_aux_knot = ":"

#     # WHEN
#     x_nameyap = nameyap_shop(
#         flare_audie=exx.bob,
#         flare_num=flare7,
#         iux2aux=iux2aux,
#         unknown_str=x_unknown_str,
#         iux_knot=slash_iux_knot,
#         aux_knot=colon_aux_knot,
#     )

#     # THEN
#     assert x_nameyap.flare_audie == exx.bob
#     assert x_nameyap.flare_num == flare7
#     assert x_nameyap.iux2aux == iux2aux
#     assert x_nameyap.unknown_str == x_unknown_str
#     assert x_nameyap.iux_knot == slash_iux_knot
#     assert x_nameyap.aux_knot == colon_aux_knot


# def test_nameyap_shop_ReturnsObj_Scenario2_LingoCoreAttrAreDefaultWhenGiven_float_nan():
#     # ESTABLISH
#     flare7 = numpy_int64(7)
#     iux2aux = {exx.xio: exx.sue}
#     x_nan = float("nan")

#     # WHEN
#     x_nameyap = nameyap_shop(
#         flare_audie=exx.bob,
#         flare_num=numpy_int64(flare7),
#         iux2aux=iux2aux,
#         unknown_str=x_nan,
#         iux_knot=x_nan,
#         aux_knot=x_nan,
#     )

#     # THEN
#     assert x_nameyap.flare_audie == exx.bob
#     assert x_nameyap.flare_num == flare7
#     assert str(type(x_nameyap.flare_num)) != "<class 'numpy.int64'>"
#     assert str(type(x_nameyap.flare_num)) == "<class 'int'>"
#     assert x_nameyap.iux2aux == iux2aux
#     assert x_nameyap.unknown_str == default_unknown_str_if_None()
#     assert x_nameyap.iux_knot == default_knot_if_None()
#     assert x_nameyap.aux_knot == default_knot_if_None()


# def test_NameYap_set_all_iux2aux_SetsAttr():
#     # ESTABLISH
#     x_nameyap = nameyap_shop()
#     x_iux2aux = {exx.xio: exx.sue, exx.zia: exx.zia}
#     assert x_nameyap.iux2aux != x_iux2aux

#     # WHEN
#     x_nameyap.set_all_iux2aux(x_iux2aux)

#     # THEN
#     assert x_nameyap.iux2aux == x_iux2aux


# def test_NameYap_set_all_iux2aux_RaisesErrorIf_unknown_str_IsKeyIn_iux2aux():
#     # ESTABLISH
#     x_unknown_str = "UnknownTerm"
#     x_nameyap = nameyap_shop(None, unknown_str=x_unknown_str)
#     x_iux2aux = {exx.xio: exx.sue, x_unknown_str: exx.zia}
#     assert x_nameyap.iux2aux != x_iux2aux

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         x_nameyap.set_all_iux2aux(x_iux2aux, True)
#     exception_str = f"iux2aux cannot have unknown_str '{x_unknown_str}' in any str. Affected keys include ['{x_unknown_str}']."
#     assert str(excinfo.value) == exception_str


# def test_NameYap_set_all_iux2aux_DoesNotRaiseErrorIfParameterSetToTrue():
#     # ESTABLISH
#     x_unknown_str = "UnknownTerm"
#     x_nameyap = nameyap_shop(None)
#     x_iux2aux = {exx.xio: exx.sue, x_unknown_str: exx.zia}
#     assert x_nameyap.iux2aux != x_iux2aux

#     # WHEN
#     x_nameyap.set_all_iux2aux(x_iux2aux)

#     # THEN
#     assert x_nameyap.iux2aux == x_iux2aux


# def test_NameYap_set_iux2aux_SetsAttr():
#     # ESTABLISH
#     x_nameyap = nameyap_shop(None)
#     assert x_nameyap.iux2aux == {}

#     # WHEN
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)

#     # THEN
#     assert x_nameyap.iux2aux == {exx.xio: exx.sue}


# def test_NameYap_get_aux_value_ReturnsObj():
#     # ESTABLISH
#     x_nameyap = nameyap_shop(None)
#     assert x_nameyap.get_aux_value(exx.xio) != exx.sue

#     # WHEN
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)

#     # THEN
#     assert x_nameyap.get_aux_value(exx.xio) == exx.sue


# def test_NameYap_iux2aux_exists_ReturnsObj():
#     # ESTABLISH
#     x_nameyap = nameyap_shop(None)
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.sue) is False
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.zia) is False
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.bob) is False
#     assert x_nameyap.iux2aux_exists(exx.zia, exx.zia) is False

#     # WHEN
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)

#     # THEN
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.sue)
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.zia) is False
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.bob) is False
#     assert x_nameyap.iux2aux_exists(exx.zia, exx.zia) is False

#     # WHEN
#     x_nameyap.set_iux2aux(exx.zia, exx.zia)

#     # THEN
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.sue)
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.zia) is False
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.bob) is False
#     assert x_nameyap.iux2aux_exists(exx.zia, exx.zia)


# def test_NameYap_iux_exists_ReturnsObj():
#     # ESTABLISH
#     x_nameyap = nameyap_shop(None)
#     assert x_nameyap.iux_exists(exx.xio) is False
#     assert x_nameyap.iux_exists(exx.sue) is False
#     assert x_nameyap.iux_exists(exx.bob) is False
#     assert x_nameyap.iux_exists(exx.zia) is False

#     # WHEN
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)

#     # THEN
#     assert x_nameyap.iux_exists(exx.xio)
#     assert x_nameyap.iux_exists(exx.sue) is False
#     assert x_nameyap.iux_exists(exx.bob) is False
#     assert x_nameyap.iux_exists(exx.zia) is False

#     # WHEN
#     x_nameyap.set_iux2aux(exx.zia, exx.zia)

#     # THEN
#     assert x_nameyap.iux_exists(exx.xio)
#     assert x_nameyap.iux_exists(exx.sue) is False
#     assert x_nameyap.iux_exists(exx.bob) is False
#     assert x_nameyap.iux_exists(exx.zia)


# def test_NameYap_del_iux2aux_SetsAttr():
#     # ESTABLISH
#     x_nameyap = nameyap_shop(None)
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.sue)

#     # WHEN
#     x_nameyap.del_iux2aux(exx.xio)

#     # THEN
#     assert x_nameyap.iux2aux_exists(exx.xio, exx.sue) is False


# def test_NameYap_unknown_str_in_iux2aux_ReturnsObj():
#     # ESTABLISH
#     x_unknown_str = "UnknownTerm"
#     x_nameyap = nameyap_shop(None, unknown_str=x_unknown_str)
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)
#     assert x_nameyap.unknown_str_in_iux2aux() is False

#     # WHEN
#     x_nameyap.set_iux2aux(exx.zia, x_unknown_str)

#     # THEN
#     assert x_nameyap.unknown_str_in_iux2aux()


# def test_NameYap_reveal_aux_ReturnsObjAndSetsAttr_contact_name():
#     # ESTABLISH
#     aux_r_knot = ":"
#     iux_r_knot = "/"
#     bowl_iux = f"bowl{iux_r_knot}"
#     boulder_iux = f"boulder{iux_r_knot}_{aux_r_knot}"
#     x_nameyap = nameyap_shop(iux_knot=iux_r_knot, aux_knot=aux_r_knot)
#     x_nameyap.iux_exists(bowl_iux) is False
#     x_nameyap.iux_exists(boulder_iux) is False

#     # WHEN
#     bowl_aux = f"bowl{aux_r_knot}"
#     assert x_nameyap.reveal_aux(bowl_iux) == bowl_aux

#     # THEN
#     assert x_nameyap.iux_exists(bowl_iux)
#     assert x_nameyap.iux_exists(boulder_iux) is False
#     assert x_nameyap.get_aux_value(bowl_iux) == bowl_aux

#     # WHEN
#     assert x_nameyap.reveal_aux(boulder_iux) is None
#     # THEN
#     assert x_nameyap.iux_exists(bowl_iux)
#     assert x_nameyap.iux_exists(boulder_iux) is False


# def test_NameYap_to_dict_ReturnsObj():
#     # ESTABLISH
#     clean_iux = "clean"
#     clean_aux = "propre"
#     flare7 = 7
#     slash_iux_knot = "/"
#     colon_aux_knot = ":"
#     x_nameyap = nameyap_shop(
#         iux_knot=slash_iux_knot,
#         aux_knot=colon_aux_knot,
#         flare_audie=exx.sue,
#         flare_num=flare7,
#     )
#     x1_rope_yap_dict = {
#         kw.iux_knot: x_nameyap.iux_knot,
#         kw.aux_knot: x_nameyap.aux_knot,
#         kw.unknown_str: x_nameyap.unknown_str,
#         kw.iux2aux: {},
#         kw.flare_audie: x_nameyap.flare_audie,
#         kw.flare_num: x_nameyap.flare_num,
#     }
#     assert x_nameyap.to_dict() == x1_rope_yap_dict

#     # WHEN
#     x_nameyap.set_iux2aux(clean_iux, clean_aux)
#     # THEN
#     x2_rope_yap_dict = {
#         kw.iux_knot: x_nameyap.iux_knot,
#         kw.aux_knot: x_nameyap.aux_knot,
#         kw.unknown_str: x_nameyap.unknown_str,
#         kw.iux2aux: {clean_iux: clean_aux},
#         kw.flare_audie: exx.sue,
#         kw.flare_num: flare7,
#     }
#     assert x_nameyap.to_dict() == x2_rope_yap_dict


# def test_get_nameyap_from_dict_ReturnsObj():
#     # ESTABLISH
#     clean_iux = "clean"
#     clean_aux = "propre"
#     slash_iux_knot = "/"
#     flare7 = 7
#     x_nameyap = nameyap_shop(exx.sue, flare7, iux_knot=slash_iux_knot)
#     x_nameyap.set_iux2aux(clean_iux, clean_aux)

#     # WHEN
#     gen_nameyap = get_nameyap_from_dict(x_nameyap.to_dict())

#     # THEN
#     assert gen_nameyap.flare_audie == x_nameyap.flare_audie
#     assert gen_nameyap.flare_num == x_nameyap.flare_num
#     assert gen_nameyap.flare_num == flare7
#     assert gen_nameyap == x_nameyap


# def test_NameYap_is_aux_knot_inclusion_correct_ReturnsObj():
#     # ESTABLISH
#     aux_knot = "/"
#     zia_iux = "Zia"
#     zia_aux = f"Zia{aux_knot}"
#     x_nameyap = nameyap_shop(aux_knot=aux_knot)
#     assert x_nameyap._is_aux_knot_inclusion_correct()

#     # WHEN
#     x_nameyap.set_iux2aux(exx.xio, exx.sue)
#     # THEN
#     assert x_nameyap._is_aux_knot_inclusion_correct()

#     # WHEN
#     x_nameyap.set_iux2aux(zia_iux, zia_aux)
#     # THEN
#     assert x_nameyap._is_aux_knot_inclusion_correct() is False


# def test_NameYap_is_iux_knot_inclusion_correct_ReturnsObj():
#     # ESTABLISH
#     xio_iux = "Xio"
#     xio_aux = "XioXio"
#     iux_knot = "/"
#     zia_iux = f"Zia{iux_knot}"
#     zia_aux = "Zia"
#     x_nameyap = nameyap_shop(iux_knot=iux_knot)
#     assert x_nameyap._is_iux_knot_inclusion_correct()

#     # WHEN
#     x_nameyap.set_iux2aux(xio_iux, xio_aux)
#     # THEN
#     assert x_nameyap._is_iux_knot_inclusion_correct()

#     # WHEN
#     x_nameyap.set_iux2aux(zia_iux, zia_aux)
#     # THEN
#     assert x_nameyap._is_iux_knot_inclusion_correct() is False


# def test_NameYap_is_valid_ReturnsObj():
#     # ESTABLISH
#     iux_knot = ":"
#     aux_knot = "/"
#     sue_iux = f"Xio{iux_knot}"
#     sue_with_knot = f"Sue{aux_knot}"
#     sue_without_knot = f"Sue{iux_knot}"
#     zia_iux = "Zia"
#     zia_aux = f"Zia{aux_knot}"
#     x_nameyap = nameyap_shop(iux_knot=iux_knot, aux_knot=aux_knot)
#     assert x_nameyap.is_valid()

#     # WHEN
#     x_nameyap.set_iux2aux(sue_iux, sue_with_knot)
#     # THEN
#     assert x_nameyap.is_valid() is False

#     # WHEN
#     x_nameyap.set_iux2aux(zia_iux, zia_aux)
#     # THEN
#     assert x_nameyap.is_valid() is False

#     # WHEN
#     x_nameyap.set_iux2aux(sue_iux, sue_without_knot)
#     # THEN
#     assert x_nameyap.is_valid() is False


# def test_inherit_nameyap_ReturnsObj_Scenario0():
#     # ESTABLISH
#     old_nameyap = nameyap_shop(exx.zia, 3)
#     new_nameyap = nameyap_shop(exx.zia, 5)
#     # WHEN
#     inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert new_nameyap
#     assert new_nameyap == nameyap_shop(exx.zia, 5)


# def test_inherit_nameyap_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_iux_knot():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     old_nameyap = nameyap_shop(exx.sue, 0, iux_knot=slash_iux_knot)
#     new_nameyap = nameyap_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_inherit_nameyap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_aux_knot():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     old_nameyap = nameyap_shop(exx.sue, 0, aux_knot=slash_iux_knot)
#     new_nameyap = nameyap_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_inherit_nameyap_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
#     # ESTABLISH
#     x_unknown_str = "UnknownTerm"
#     old_nameyap = nameyap_shop(exx.sue, 0, unknown_str=x_unknown_str)
#     new_nameyap = nameyap_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_inherit_nameyap_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_flare_audie():
#     # ESTABLISH
#     old_nameyap = nameyap_shop(exx.sue, 0)
#     new_nameyap = nameyap_shop(exx.bob, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_inherit_nameyap_ReturnsObj_Scenario5_RaiseErrorWhenFlareIntsOutOfOrder():
#     # ESTABLISH
#     old_nameyap = nameyap_shop(exx.sue, 5)
#     new_nameyap = nameyap_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert str(excinfo.value) == "older yapunit is not older"


# def test_inherit_nameyap_ReturnsObj_Scenario6_inheritFromOld():
#     # ESTABLISH
#     xio_iux = "Xio"
#     xio_aux = "Xioito"
#     old_nameyap = nameyap_shop(exx.zia, 3)
#     old_nameyap.set_iux2aux(xio_iux, xio_aux)
#     new_nameyap = nameyap_shop(exx.zia, 7)
#     assert new_nameyap.iux2aux_exists(xio_iux, xio_aux) is False

#     # WHEN
#     inherited_nameyap = inherit_nameyap(new_nameyap, old_nameyap)

#     # THEN
#     assert inherited_nameyap.iux2aux_exists(xio_iux, xio_aux)
