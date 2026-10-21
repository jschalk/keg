from ch05_rope.rope import create_rope, default_knot_if_None, to_rope
from ch18_speech.yap_term import (
    LabelYap,
    NameYap,
    RopeYap,
    TitleYap,
    labelyap_shop,
    nameyap_shop,
    ropeyap_shop,
    titleyap_shop,
)
from ch18_speech.speech_main import SpeechUnit, speechunit_shop
from ch99_glossary.ch_keyword import Ch18Keywords as kw, ExampleStrs as exx
from pandas import DataFrame


def get_clean_labelyap() -> LabelYap:
    clean_iux = "clean"
    clean_aux = "propre"
    casa_iux = "casa1"
    casa_aux = "casa2"
    labelyap = labelyap_shop(flare_audie="Sue")
    labelyap.set_iux2aux(clean_iux, clean_aux)
    labelyap.set_iux2aux(casa_iux, casa_aux)
    return labelyap


def get_clean_ropeyap() -> RopeYap:
    iux_amy45_str = "amy45"
    aux_amy87_str = "amy87"
    iux_amy45_rope = to_rope(iux_amy45_str)
    aux_amy87_rope = to_rope(aux_amy87_str)
    clean_iux_str = "clean"
    clean_aux_str = "prop"
    knot = default_knot_if_None()
    clean_iux_rope = create_rope(iux_amy45_str, clean_iux_str, knot)
    # clean_iux_rope = f"{knot}{iux_amy45_str}{knot}{clean_iux_str}{knot}"
    rope_yapunit = ropeyap_shop(flare_audie="Sue")
    rope_yapunit.set_label(clean_iux_str, clean_aux_str)
    rope_yapunit.set_iux2aux(iux_amy45_rope, aux_amy87_rope)
    print(f"{rope_yapunit.iux2aux.keys()=}")
    rope_yapunit.reveal_aux(clean_iux_rope)
    return rope_yapunit


def get_bowl_titleyap() -> TitleYap:
    knot = default_knot_if_None()
    bowl_iux = f"bowl{knot}"
    bowl_aux = f"nage{knot}"
    boulder_iux = f"boulder{knot}"
    x_titleyap = titleyap_shop(flare_audie="Sue")
    x_titleyap.set_iux2aux(bowl_iux, bowl_aux)
    x_titleyap.set_iux2aux(boulder_iux, boulder_iux)
    return x_titleyap


def get_suita_nameyap() -> NameYap:
    xio_iux = "Xio"
    sue_iux = "Sue"
    bob_iux = "Bob"
    zia_iux = "Zia"
    xio_aux = "Xioita"
    sue_aux = "Suita"
    bob_aux = "Bobita"
    contact_name_yapunit = nameyap_shop(flare_audie="Sue")
    contact_name_yapunit.set_iux2aux(xio_iux, xio_aux)
    contact_name_yapunit.set_iux2aux(sue_iux, sue_aux)
    contact_name_yapunit.set_iux2aux(bob_iux, bob_aux)
    return contact_name_yapunit


# def get_invalid_contact_name_yapunit() -> YapUnit:
#     sue_iux = f"Xio{default_knot_if_None()}"
#     sue_aux = "Sue"
#     zia_iux = "Zia"
#     zia_aux = "Zia"
#     x_titleyap = yapunit_shop(kw.NameTerm, flare_audie="Sue")
#     x_titleyap.set_iux2aux(sue_iux, sue_aux)
#     x_titleyap.set_iux2aux(zia_iux, zia_aux)
#     return x_titleyap


# def get_invalid_group_title_yapunit() -> YapUnit:
#     sue_iux = f"Xio{default_knot_if_None()}"
#     sue_aux = f"Sue{default_knot_if_None()}"
#     zia_iux = "Zia"
#     zia_aux = f"Zia{default_knot_if_None()}"
#     x_titleyap = yapunit_shop(kw.TitleTerm, flare_audie="Sue")
#     x_titleyap.set_iux2aux(sue_iux, sue_aux)
#     x_titleyap.set_iux2aux(zia_iux, zia_aux)
#     return x_titleyap


# def get_invalid_rope_yapunit() -> YapUnit:
#     clean_aux = "propre"
#     casa_iux = f"casa{default_knot_if_None()}"
#     casa_aux = "casa"
#     labelyap = yapunit_shop(kw.LabelTerm, flare_audie="Sue")
#     labelyap.set_iux2aux(exx.clean, clean_aux)
#     labelyap.set_iux2aux(casa_iux, casa_aux)
#     return labelyap


def get_sue_speechunit() -> SpeechUnit:
    sue_speechunit = speechunit_shop("Sue")
    sue_speechunit.set_nameyap(get_suita_nameyap())
    sue_speechunit.set_titleyap(get_bowl_titleyap())
    sue_speechunit.set_labelyap(get_clean_labelyap())
    sue_speechunit.set_ropeyap(get_clean_ropeyap())
    sue_speechunit.ropeyap.labelyap = get_clean_labelyap()
    return sue_speechunit


def get_casa_maison_speechunit_set_by_iux2aux() -> SpeechUnit:
    iux_amy45_str = "amy45"
    aux_amy87_str = "amy87"
    iux_amy45_rope = to_rope(iux_amy45_str)
    aux_amy87_rope = to_rope(aux_amy87_str)
    casa_iux_str = "casa"
    casa_aux_str = "maison"
    casa_iux_rope = create_rope(iux_amy45_rope, casa_iux_str)
    casa_aux_rope = create_rope(aux_amy87_rope, casa_aux_str)
    clean_iux_str = "clean"
    clean_aux_str = "propre"
    clean_iux_rope = create_rope(casa_iux_rope, clean_iux_str)
    clean_aux_rope = create_rope(casa_aux_rope, clean_aux_str)

    sweep_iux_rope = create_rope(clean_iux_rope, exx.sweep)
    sweep_aux_rope = create_rope(clean_aux_rope, exx.sweep)

    sue_speechunit = speechunit_shop("Sue", 7)
    rx = kw.RopeTerm
    sue_speechunit.set_iux2aux(rx, iux_amy45_rope, aux_amy87_rope)
    sue_speechunit.set_iux2aux(rx, casa_iux_rope, casa_aux_rope)
    sue_speechunit.set_iux2aux(rx, clean_iux_rope, clean_aux_rope)
    sue_speechunit.set_iux2aux(rx, sweep_iux_rope, sweep_aux_rope)
    return sue_speechunit


def get_casa_maison_speechunit_set_by_label() -> SpeechUnit:
    iux_amy45_str = "amy45"
    aux_amy87_str = "amy87"
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

    sue_speechunit = speechunit_shop("Sue", 7)
    sue_speechunit.set_roadyap_label(iux_amy45_str, aux_amy87_str)
    sue_speechunit.set_roadyap_label(casa_iux_str, casa_aux_str)
    sue_speechunit.set_roadyap_label(clean_iux_str, clean_aux_str)
    return sue_speechunit


def get_casa_maison_rope_iux2aux_dt() -> DataFrame:
    aux_amy87_str = "amy87"
    aux_amy87_rope = to_rope(aux_amy87_str)
    casa_aux_rope = create_rope(aux_amy87_str, "maison")
    clean_aux_rope = create_rope(casa_aux_rope, "propre")
    sweep_aux_rope = create_rope(clean_aux_rope, "sweep")
    iux_amy45_str = "amy45"
    iux_amy45_rope = to_rope(iux_amy45_str)
    casa_iux_rope = create_rope(iux_amy45_rope, "casa")
    clean_iux_rope = create_rope(casa_iux_rope, "clean")
    sweep_iux_rope = create_rope(clean_iux_rope, "sweep")
    x_rd = default_knot_if_None()
    e7 = 7

    aux_dt = DataFrame(
        columns=[
            kw.flare_audie,
            kw.flare_num,
            kw.iux_knot,
            kw.aux_knot,
            kw.iux_rope,
            kw.aux_rope,
        ]
    )
    aux_dt.loc[0] = ["Sue", e7, x_rd, x_rd, iux_amy45_rope, aux_amy87_rope]
    aux_dt.loc[1] = ["Sue", e7, x_rd, x_rd, casa_iux_rope, casa_aux_rope]
    aux_dt.loc[2] = ["Sue", e7, x_rd, x_rd, clean_iux_rope, clean_aux_rope]
    aux_dt.loc[3] = ["Sue", e7, x_rd, x_rd, sweep_iux_rope, sweep_aux_rope]
    return aux_dt


def get_invalid_nameyap() -> NameYap:
    sue_iux = f"Xio{default_knot_if_None()}"
    sue_aux = "Sue"
    zia_iux = "Zia"
    zia_aux = "Zia"
    nameyap = nameyap_shop(flare_audie="Sue")
    nameyap.set_iux2aux(sue_iux, sue_aux)
    nameyap.set_iux2aux(zia_iux, zia_aux)
    return nameyap


def get_invalid_titleyap() -> TitleYap:
    sue_iux = f"Xio{default_knot_if_None()}"
    sue_aux = f"Sue{default_knot_if_None()}"
    zia_iux = "Zia"
    zia_aux = f"Zia{default_knot_if_None()}"
    x_titleyap = titleyap_shop(flare_audie="Sue")
    x_titleyap.set_iux2aux(sue_iux, sue_aux)
    x_titleyap.set_iux2aux(zia_iux, zia_aux)
    return x_titleyap


def get_invalid_ropeyap() -> RopeYap:
    casa_iux = create_rope(exx.casa)
    casa_aux = create_rope(exx.casa)
    clean_str = create_rope(casa_iux, "clean")
    clean_aux = create_rope(casa_aux, "propre")
    ropeyap = ropeyap_shop(flare_audie="Sue")
    ropeyap.set_iux2aux(clean_str, clean_aux)
    # ropeyap.set_iux2aux(casa_iux, casa_aux)
    return ropeyap


def get_slash_labelyap() -> LabelYap:
    iux_amy45_str = "amy45"
    aux_amy87_str = "amy87"
    clean_iux_str = "clean"
    clean_aux_str = "prop"
    slash_iux_knot = "/"
    colon_aux_knot = ":"
    x_labelyap = labelyap_shop(
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
        flare_audie="Sue",
        flare_num=7,
    )
    x_labelyap.set_iux2aux(iux_amy45_str, aux_amy87_str)
    x_labelyap.set_iux2aux(clean_iux_str, clean_aux_str)
    x_labelyap.reveal_aux("running")
    return x_labelyap


def get_slash_ropeyap() -> RopeYap:
    slash_iux_knot = "/"
    colon_aux_knot = ":"
    iux_amy45_str = "amy45"
    aux_amy87_str = "amy87"
    iux_amy45_rope = to_rope(iux_amy45_str, slash_iux_knot)
    aux_amy87_rope = to_rope(aux_amy87_str, colon_aux_knot)
    clean_iux_str = "clean"
    clean_aux_str = "prop"
    clean_iux_rope = create_rope(iux_amy45_rope, clean_iux_str, slash_iux_knot)
    clean_aux_rope = create_rope(aux_amy87_rope, clean_iux_str, colon_aux_knot)
    x_ropeyap = ropeyap_shop(
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
        flare_audie="Sue",
        flare_num=7,
        x_labelyap=get_slash_labelyap(),
    )
    x_ropeyap.set_label(clean_iux_str, clean_aux_str)
    x_ropeyap.set_iux2aux(iux_amy45_rope, aux_amy87_rope)
    x_ropeyap.reveal_aux(clean_iux_rope)
    return x_ropeyap


def get_slash_titleyap() -> TitleYap:
    slash_iux_knot = "/"
    colon_aux_knot = ":"
    bowl_iux = f"bowl{slash_iux_knot}"
    bowl_aux = f"nage{colon_aux_knot}"
    boulder_iux = f"boulder{slash_iux_knot}"
    boulder_aux = f"boulder{colon_aux_knot}"
    x_titleyap = titleyap_shop(
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
        flare_audie="Sue",
        flare_num=7,
    )
    x_titleyap.set_iux2aux(bowl_iux, bowl_aux)
    x_titleyap.set_iux2aux(boulder_iux, boulder_aux)
    return x_titleyap


def get_slash_nameyap() -> NameYap:
    slash_iux_knot = "/"
    colon_aux_knot = ":"
    xio_iux = "Xio"
    sue_iux = "Sue"
    bob_iux = "Bob"
    zia_iux = "Zia"
    xio_aux = "Xioita"
    sue_aux = "Suita"
    bob_aux = "Bobita"
    x_nameyap = nameyap_shop(
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
        flare_audie="Sue",
        flare_num=7,
    )
    x_nameyap.set_iux2aux(xio_iux, xio_aux)
    x_nameyap.set_iux2aux(sue_iux, sue_aux)
    x_nameyap.set_iux2aux(bob_iux, bob_aux)
    return x_nameyap


def get_speech_core_attrs_are_none_nameyap() -> NameYap:
    xio_iux = "Xio"
    sue_iux = "Sue"
    bob_iux = "Bob"
    xio_aux = "Xioita"
    sue_aux = "Suita"
    bob_aux = "Bobita"
    x_nan = float("nan")
    x_nameyap = nameyap_shop(
        flare_audie="Sue",
        flare_num=7,
        iux_knot=x_nan,
        aux_knot=x_nan,
    )
    x_nameyap.set_iux2aux(xio_iux, xio_aux)
    x_nameyap.set_iux2aux(sue_iux, sue_aux)
    x_nameyap.set_iux2aux(bob_iux, bob_aux)
    return x_nameyap
