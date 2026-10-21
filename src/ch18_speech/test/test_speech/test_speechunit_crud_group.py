from ch18_speech.yap_term import titleyap_shop
from ch18_speech.speech_main import speechunit_shop
from ch99_glossary.ch_keyword import ExampleStrs as exx
from pytest import raises as pytest_raises


def test_SpeechUnit_set_titleyap_SetsAttr():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    x_titleyap = titleyap_shop(flare_audie=exx.sue)
    x_titleyap.set_iux2aux("Bob", "Bob of Salem")
    assert sue_speechunit.titleyap != x_titleyap

    # WHEN
    sue_speechunit.set_titleyap(x_titleyap)

    # THEN
    assert sue_speechunit.titleyap == x_titleyap


def test_SpeechUnit_set_titleyap_RaisesErrorIf_titleyap_iux_knot_IsNotSame():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    slash_iux_knot = "/"
    x_titleyap = titleyap_shop(iux_knot=slash_iux_knot, flare_audie=exx.sue)
    assert sue_speechunit.iux_knot != x_titleyap.iux_knot
    assert sue_speechunit.titleyap != x_titleyap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_speechunit.set_titleyap(x_titleyap)
    exception_str = f"set_yapcore Error: SpeechUnit iux_knot is '{sue_speechunit.iux_knot}', YapCore is '{slash_iux_knot}'."
    assert str(excinfo.value) == exception_str


def test_SpeechUnit_set_titleyap_RaisesErrorIf_titleyap_aux_knot_IsNotSame():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    slash_aux_knot = "/"
    x_titleyap = titleyap_shop(aux_knot=slash_aux_knot, flare_audie=exx.sue)
    assert sue_speechunit.aux_knot != x_titleyap.aux_knot
    assert sue_speechunit.titleyap != x_titleyap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_speechunit.set_titleyap(x_titleyap)
    exception_str = f"set_yapcore Error: SpeechUnit aux_knot is '{sue_speechunit.aux_knot}', YapCore is '{slash_aux_knot}'."
    assert str(excinfo.value) == exception_str


def test_SpeechUnit_set_titleyap_RaisesErrorIf_titleyap_flare_audie_IsNotSame():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    x_titleyap = titleyap_shop(flare_audie=exx.yao)
    assert sue_speechunit.flare_audie != x_titleyap.flare_audie
    assert sue_speechunit.titleyap != x_titleyap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_speechunit.set_titleyap(x_titleyap)
    exception_str = f"set_yapcore Error: SpeechUnit flare_audie is '{sue_speechunit.flare_audie}', YapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_SpeechUnit_get_titleyap_ReturnsObj():
    # ESTABLISH
    sue_speechunit = speechunit_shop(exx.sue)
    static_x_titleyap = titleyap_shop(flare_audie=exx.sue)
    static_x_titleyap.set_iux2aux("Bob", "Bob of Salem")
    sue_speechunit.set_titleyap(static_x_titleyap)

    # WHEN
    gen_x_titleyap = sue_speechunit.get_titleyap()

    # THEN
    assert gen_x_titleyap == static_x_titleyap


def test_SpeechUnit_set_titleterm_SetsAttr_Scenario0():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)
    contact_name_titleyap = zia_speechunit.get_titleyap()
    assert contact_name_titleyap.iux2aux_exists(sue_iux, sue_aux) is False

    # WHEN
    zia_speechunit.set_titleterm(sue_iux, sue_aux)

    # THEN
    assert contact_name_titleyap.iux2aux_exists(sue_iux, sue_aux)


def test_SpeechUnit_titleterm_exists_ReturnsObj():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)

    assert zia_speechunit.titleterm_exists(sue_iux, sue_aux) is False

    # WHEN
    zia_speechunit.set_titleterm(sue_iux, sue_aux)

    # THEN
    assert zia_speechunit.titleterm_exists(sue_iux, sue_aux)


def test_SpeechUnit_get_aux_title_ReturnsObj():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)
    assert zia_speechunit._get_aux_title(sue_iux) != sue_aux

    # WHEN
    zia_speechunit.set_titleterm(sue_iux, sue_aux)

    # THEN
    assert zia_speechunit._get_aux_title(sue_iux) == sue_aux


def test_SpeechUnit_del_titleterm_ReturnsObj():
    # ESTABLISH
    sue_iux = "Sue"
    sue_aux = "Suita"
    zia_speechunit = speechunit_shop(exx.zia)

    zia_speechunit.set_titleterm(sue_iux, sue_aux)
    zia_speechunit.set_titleterm(exx.zia, exx.zia)
    assert zia_speechunit.titleterm_exists(sue_iux, sue_aux)
    assert zia_speechunit.titleterm_exists(exx.zia, exx.zia)

    # WHEN
    zia_speechunit.del_titleterm(sue_iux)

    # THEN
    assert zia_speechunit.titleterm_exists(sue_iux, sue_aux) is False
    assert zia_speechunit.titleterm_exists(exx.zia, exx.zia)
