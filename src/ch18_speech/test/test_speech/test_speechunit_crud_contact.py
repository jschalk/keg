from ch18_speech.yap_term import nameyap_shop
from ch18_speech.speech_main import speechunit_shop
from ch99_glossary.ch_keyword import ExampleStrs as exx
from pytest import raises as pytest_raises


def test_SpeechUnit_set_nameyap_SetsAttr():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    x_nameyap = nameyap_shop(flare_audie=exx.sue)
    x_nameyap.set_iux2aux("Bob", "Bob of Salem")
    assert sue_speechunit.nameyap != x_nameyap

    # WHEN
    sue_speechunit.set_nameyap(x_nameyap)

    # THEN
    assert sue_speechunit.nameyap == x_nameyap


def test_SpeechUnit_set_nameyap_SetsAttrWhenAttrIs_float_nan():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    x_nan = float("nan")
    x_nameyap = nameyap_shop(flare_audie=exx.sue, iux_knot=x_nan, aux_knot=x_nan)
    x_nameyap.set_iux2aux("Bob", "Bob of Salem")
    assert sue_speechunit.nameyap != x_nameyap

    # WHEN
    sue_speechunit.set_nameyap(x_nameyap)

    # THEN
    assert sue_speechunit.nameyap == x_nameyap


def test_SpeechUnit_set_nameyap_RaisesErrorIf_nameyap_iux_knot_IsNotSame():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    slash_iux_knot = "/"
    x_nameyap = nameyap_shop(iux_knot=slash_iux_knot, flare_audie=exx.sue)
    assert sue_speechunit.iux_knot != x_nameyap.iux_knot
    assert sue_speechunit.nameyap != x_nameyap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_speechunit.set_nameyap(x_nameyap)
    exception_str = f"set_yapcore Error: SpeechUnit iux_knot is '{sue_speechunit.iux_knot}', YapCore is '{slash_iux_knot}'."
    assert str(excinfo.value) == exception_str


def test_SpeechUnit_set_nameyap_RaisesErrorIf_nameyap_aux_knot_IsNotSame():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    slash_aux_knot = "/"
    x_nameyap = nameyap_shop(aux_knot=slash_aux_knot, flare_audie=exx.sue)
    assert sue_speechunit.aux_knot != x_nameyap.aux_knot
    assert sue_speechunit.nameyap != x_nameyap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_speechunit.set_nameyap(x_nameyap)
    exception_str = f"set_yapcore Error: SpeechUnit aux_knot is '{sue_speechunit.aux_knot}', YapCore is '{slash_aux_knot}'."
    assert str(excinfo.value) == exception_str


def test_SpeechUnit_set_nameyap_RaisesErrorIf_nameyap_flare_audie_IsNotSame():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    x_nameyap = nameyap_shop(flare_audie=exx.yao)
    assert sue_speechunit.flare_audie != x_nameyap.flare_audie
    assert sue_speechunit.nameyap != x_nameyap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_speechunit.set_nameyap(x_nameyap)
    exception_str = f"set_yapcore Error: SpeechUnit flare_audie is '{sue_speechunit.flare_audie}', YapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_SpeechUnit_get_nameyap_ReturnsObj():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    static_x_nameyap = nameyap_shop(flare_audie=exx.sue)
    static_x_nameyap.set_iux2aux("Bob", "Bob of Salem")
    sue_speechunit.set_nameyap(static_x_nameyap)

    # WHEN
    gen_x_nameyap = sue_speechunit.get_nameyap()

    # THEN
    assert gen_x_nameyap == static_x_nameyap


def test_SpeechUnit_set_speech_nameterm_SetsAttr_Scenario0():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)
    contact_name_nameyap = zia_speechunit.get_nameyap()
    assert contact_name_nameyap.iux2aux_exists(sue_iux, sue_aux) is False

    # WHEN
    zia_speechunit.set_speech_nameterm(sue_iux, sue_aux)

    # THEN
    assert contact_name_nameyap.iux2aux_exists(sue_iux, sue_aux)


def test_SpeechUnit_nameterm_speech_exists_ReturnsObj():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)

    assert zia_speechunit.nameterm_speech_exists(sue_iux, sue_aux) is False

    # WHEN
    zia_speechunit.set_speech_nameterm(sue_iux, sue_aux)

    # THEN
    assert zia_speechunit.nameterm_speech_exists(sue_iux, sue_aux)


def test_SpeechUnit_get_aux_name_ReturnsObj():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)
    assert zia_speechunit._get_aux_name(sue_iux) != sue_aux

    # WHEN
    zia_speechunit.set_speech_nameterm(sue_iux, sue_aux)

    # THEN
    assert zia_speechunit._get_aux_name(sue_iux) == sue_aux


def test_SpeechUnit_del_speech_nameterm_ReturnsObj():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)

    zia_speechunit.set_speech_nameterm(sue_iux, sue_aux)
    zia_speechunit.set_speech_nameterm(exx.zia, exx.zia)
    assert zia_speechunit.nameterm_speech_exists(sue_iux, sue_aux)
    assert zia_speechunit.nameterm_speech_exists(exx.zia, exx.zia)

    # WHEN
    zia_speechunit.del_speech_nameterm(sue_iux)

    # THEN
    assert zia_speechunit.nameterm_speech_exists(sue_iux, sue_aux) is False
    assert zia_speechunit.nameterm_speech_exists(exx.zia, exx.zia)
