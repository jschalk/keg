from pandas import DataFrame
from src.ch04_rope.rope import create_rope, default_knot_if_None, to_rope
from src.ch16_translate.map_term import (
    LabelMap,
    NameMap,
    RopeMap,
    TitleMap,
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.ch16_translate.translate_config import default_unknown_str_if_None
from src.ch16_translate.translate_main import TranslateUnit, translateunit_shop
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def get_clean_labelmap() -> LabelMap:
    clean_otx = "clean"
    clean_inx = "propre"
    casa_otx = "casa1"
    casa_inx = "casa2"
    labelmap = labelmap_shop(spark_face="Sue")
    labelmap.set_otx2inx(clean_otx, clean_inx)
    labelmap.set_otx2inx(casa_otx, casa_inx)
    return labelmap


def get_clean_ropemap() -> RopeMap:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    knot = default_knot_if_None()
    clean_otx_rope = create_rope(otx_amy45_str, clean_otx_str, knot)
    # clean_otx_rope = f"{knot}{otx_amy45_str}{knot}{clean_otx_str}{knot}"
    rope_mapunit = ropemap_shop(spark_face="Sue")
    rope_mapunit.set_label(clean_otx_str, clean_inx_str)
    rope_mapunit.set_otx2inx(otx_amy45_rope, inx_amy87_rope)
    print(f"{rope_mapunit.otx2inx.keys()=}")
    rope_mapunit.reveal_inx(clean_otx_rope)
    return rope_mapunit


def get_swim_titlemap() -> TitleMap:
    knot = default_knot_if_None()
    swim_otx = f"swim{knot}"
    swim_inx = f"nage{knot}"
    climb_otx = f"climb{knot}"
    x_titlemap = titlemap_shop(spark_face="Sue")
    x_titlemap.set_otx2inx(swim_otx, swim_inx)
    x_titlemap.set_otx2inx(climb_otx, climb_otx)
    return x_titlemap


def get_suita_namemap() -> NameMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    contact_name_mapunit = namemap_shop(spark_face="Sue")
    contact_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    contact_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    contact_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    return contact_name_mapunit


# def get_invalid_contact_name_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_knot_if_None()}"
#     sue_inx = "Sue"
#     zia_otx = "Zia"
#     zia_inx = "Zia"
#     x_titlemap = mapunit_shop(kw.NameTerm, spark_face="Sue")
#     x_titlemap.set_otx2inx(sue_otx, sue_inx)
#     x_titlemap.set_otx2inx(zia_otx, zia_inx)
#     return x_titlemap


# def get_invalid_group_title_mapunit() -> MapUnit:
#     sue_otx = f"Xio{default_knot_if_None()}"
#     sue_inx = f"Sue{default_knot_if_None()}"
#     zia_otx = "Zia"
#     zia_inx = f"Zia{default_knot_if_None()}"
#     x_titlemap = mapunit_shop(kw.TitleTerm, spark_face="Sue")
#     x_titlemap.set_otx2inx(sue_otx, sue_inx)
#     x_titlemap.set_otx2inx(zia_otx, zia_inx)
#     return x_titlemap


# def get_invalid_rope_mapunit() -> MapUnit:
#     clean_inx = "propre"
#     casa_otx = f"casa{default_knot_if_None()}"
#     casa_inx = "casa"
#     labelmap = mapunit_shop(kw.LabelTerm, spark_face="Sue")
#     labelmap.set_otx2inx(exx.clean, clean_inx)
#     labelmap.set_otx2inx(casa_otx, casa_inx)
#     return labelmap


def get_sue_translateunit() -> TranslateUnit:
    sue_translateunit = translateunit_shop("Sue")
    sue_translateunit.set_namemap(get_suita_namemap())
    sue_translateunit.set_titlemap(get_swim_titlemap())
    sue_translateunit.set_labelmap(get_clean_labelmap())
    sue_translateunit.set_ropemap(get_clean_ropemap())
    sue_translateunit.ropemap.labelmap = get_clean_labelmap()
    return sue_translateunit


def get_suita_contact_name_otx_dt() -> DataFrame:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[kw.contact_name])
    otx_dt.loc[0, kw.contact_name] = zia_otx
    otx_dt.loc[1, kw.contact_name] = sue_otx
    otx_dt.loc[2, kw.contact_name] = bob_otx
    otx_dt.loc[3, kw.contact_name] = xio_otx
    return otx_dt


def get_suita_contact_name_inx_dt() -> DataFrame:
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    zia_otx = "Zia"
    inx_dt = DataFrame(columns=[kw.contact_name])
    inx_dt.loc[0, kw.contact_name] = xio_inx
    inx_dt.loc[1, kw.contact_name] = sue_inx
    inx_dt.loc[2, kw.contact_name] = bob_inx
    inx_dt.loc[3, kw.contact_name] = zia_otx
    return inx_dt


def get_casa_maison_translateunit_set_by_otx2inx() -> TranslateUnit:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_rope, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_rope, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    sweep_inx_rope = create_rope(clean_inx_rope, exx.sweep)

    sue_translateunit = translateunit_shop("Sue", 7)
    rx = kw.RopeTerm
    sue_translateunit.set_otx2inx(rx, otx_amy45_rope, inx_amy87_rope)
    sue_translateunit.set_otx2inx(rx, casa_otx_rope, casa_inx_rope)
    sue_translateunit.set_otx2inx(rx, clean_otx_rope, clean_inx_rope)
    sue_translateunit.set_otx2inx(rx, sweep_otx_rope, sweep_inx_rope)
    return sue_translateunit


def get_casa_maison_translateunit_set_by_label() -> TranslateUnit:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
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

    sue_translateunit = translateunit_shop("Sue", 7)
    sue_translateunit.set_roadmap_label(otx_amy45_str, inx_amy87_str)
    sue_translateunit.set_roadmap_label(casa_otx_str, casa_inx_str)
    sue_translateunit.set_roadmap_label(clean_otx_str, clean_inx_str)
    return sue_translateunit


def get_casa_maison_rope_otx_dt() -> DataFrame:
    otx_amy45_str = "amy45"
    otx_amy45_rope = to_rope(otx_amy45_str)
    casa_otx_str = "casa"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    otx_dt = DataFrame(columns=[kw.reason_context])
    otx_dt.loc[0, kw.reason_context] = otx_amy45_rope
    otx_dt.loc[1, kw.reason_context] = casa_otx_rope
    otx_dt.loc[2, kw.reason_context] = clean_otx_rope
    otx_dt.loc[3, kw.reason_context] = sweep_otx_rope
    return otx_dt


def get_casa_maison_rope_inx_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_inx_rope = create_rope(inx_amy87_rope, "maison")
    clean_inx_rope = create_rope(casa_inx_rope, "propre")
    sweep_inx_rope = create_rope(clean_inx_rope, "sweep")
    inx_dt = DataFrame(columns=[kw.reason_context])
    inx_dt.loc[0, kw.reason_context] = inx_amy87_rope
    inx_dt.loc[1, kw.reason_context] = casa_inx_rope
    inx_dt.loc[2, kw.reason_context] = clean_inx_rope
    inx_dt.loc[3, kw.reason_context] = sweep_inx_rope
    return inx_dt


def get_casa_maison_rope_otx2inx_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_inx_rope = create_rope(inx_amy87_str, "maison")
    clean_inx_rope = create_rope(casa_inx_rope, "propre")
    sweep_inx_rope = create_rope(clean_inx_rope, "sweep")
    otx_amy45_str = "amy45"
    otx_amy45_rope = to_rope(otx_amy45_str)
    casa_otx_rope = create_rope(otx_amy45_rope, "casa")
    clean_otx_rope = create_rope(casa_otx_rope, "clean")
    sweep_otx_rope = create_rope(clean_otx_rope, "sweep")
    x_rd = default_knot_if_None()
    e7 = 7
    uw = default_unknown_str_if_None()

    inx_dt = DataFrame(
        columns=[
            kw.spark_face,
            kw.spark_num,
            kw.otx_knot,
            kw.inx_knot,
            kw.unknown_str,
            kw.otx_rope,
            kw.inx_rope,
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_amy45_rope, inx_amy87_rope]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_rope, casa_inx_rope]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_rope, clean_inx_rope]
    inx_dt.loc[3] = ["Sue", e7, x_rd, x_rd, uw, sweep_otx_rope, sweep_inx_rope]
    return inx_dt


def get_casa_maison_label_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    casa_inx_str = "maison"
    clean_inx_str = "propre"
    sweep_inx_str = "sweep"
    otx_amy45_str = "amy45"
    casa_otx_str = "casa"
    clean_otx_str = "clean"
    sweep_otx_str = "sweep"
    x_rd = default_knot_if_None()
    uw = default_unknown_str_if_None()
    e7 = 7

    inx_dt = DataFrame(
        columns=[
            kw.spark_face,
            kw.spark_num,
            kw.otx_knot,
            kw.inx_knot,
            kw.unknown_str,
            kw.otx_label,
            kw.inx_label,
        ]
    )
    inx_dt.loc[0] = ["Sue", e7, x_rd, x_rd, uw, otx_amy45_str, inx_amy87_str]
    inx_dt.loc[1] = ["Sue", e7, x_rd, x_rd, uw, casa_otx_str, casa_inx_str]
    inx_dt.loc[2] = ["Sue", e7, x_rd, x_rd, uw, clean_otx_str, clean_inx_str]
    return inx_dt


def get_invalid_namemap() -> NameMap:
    sue_otx = f"Xio{default_knot_if_None()}"
    sue_inx = "Sue"
    zia_otx = "Zia"
    zia_inx = "Zia"
    namemap = namemap_shop(spark_face="Sue")
    namemap.set_otx2inx(sue_otx, sue_inx)
    namemap.set_otx2inx(zia_otx, zia_inx)
    return namemap


def get_invalid_titlemap() -> TitleMap:
    sue_otx = f"Xio{default_knot_if_None()}"
    sue_inx = f"Sue{default_knot_if_None()}"
    zia_otx = "Zia"
    zia_inx = f"Zia{default_knot_if_None()}"
    x_titlemap = titlemap_shop(spark_face="Sue")
    x_titlemap.set_otx2inx(sue_otx, sue_inx)
    x_titlemap.set_otx2inx(zia_otx, zia_inx)
    return x_titlemap


def get_invalid_ropemap() -> RopeMap:
    casa_otx = create_rope(exx.casa)
    casa_inx = create_rope(exx.casa)
    clean_str = create_rope(casa_otx, "clean")
    clean_inx = create_rope(casa_inx, "propre")
    ropemap = ropemap_shop(spark_face="Sue")
    ropemap.set_otx2inx(clean_str, clean_inx)
    # ropemap.set_otx2inx(casa_otx, casa_inx)
    return ropemap


def get_slash_labelmap() -> LabelMap:
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    x_labelmap = labelmap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        spark_face="Sue",
        spark_num=7,
    )
    x_labelmap.set_otx2inx(otx_amy45_str, inx_amy87_str)
    x_labelmap.set_otx2inx(clean_otx_str, clean_inx_str)
    x_labelmap.reveal_inx("running")
    return x_labelmap


def get_slash_ropemap() -> RopeMap:
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str, slash_otx_knot)
    inx_amy87_rope = to_rope(inx_amy87_str, colon_inx_knot)
    clean_otx_str = "clean"
    clean_inx_str = "prop"
    x_unknown_str = "UnknownTerm"
    clean_otx_rope = create_rope(otx_amy45_rope, clean_otx_str, slash_otx_knot)
    clean_inx_rope = create_rope(inx_amy87_rope, clean_otx_str, colon_inx_knot)
    x_ropemap = ropemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        spark_face="Sue",
        spark_num=7,
        x_labelmap=get_slash_labelmap(),
    )
    x_ropemap.set_label(clean_otx_str, clean_inx_str)
    x_ropemap.set_otx2inx(otx_amy45_rope, inx_amy87_rope)
    x_ropemap.reveal_inx(clean_otx_rope)
    return x_ropemap


def get_slash_titlemap() -> TitleMap:
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    swim_otx = f"swim{slash_otx_knot}"
    swim_inx = f"nage{colon_inx_knot}"
    climb_otx = f"climb{slash_otx_knot}"
    climb_inx = f"climb{colon_inx_knot}"
    x_titlemap = titlemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        spark_face="Sue",
        spark_num=7,
    )
    x_titlemap.set_otx2inx(swim_otx, swim_inx)
    x_titlemap.set_otx2inx(climb_otx, climb_inx)
    return x_titlemap


def get_slash_namemap() -> NameMap:
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_namemap = namemap_shop(
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
        spark_face="Sue",
        spark_num=7,
    )
    x_namemap.set_otx2inx(xio_otx, xio_inx)
    x_namemap.set_otx2inx(sue_otx, sue_inx)
    x_namemap.set_otx2inx(bob_otx, bob_inx)
    return x_namemap


def get_translate_core_attrs_are_none_namemap() -> NameMap:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    x_nan = float("nan")
    x_namemap = namemap_shop(
        spark_face="Sue",
        spark_num=7,
        otx_knot=x_nan,
        inx_knot=x_nan,
        unknown_str=x_nan,
    )
    x_namemap.set_otx2inx(xio_otx, xio_inx)
    x_namemap.set_otx2inx(sue_otx, sue_inx)
    x_namemap.set_otx2inx(bob_otx, bob_inx)
    return x_namemap
