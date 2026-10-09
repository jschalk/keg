from ch05_rope.rope import default_knot_if_None
from ch17_jargon.test._util.ch17_examples import (
    get_slash_labelmap,
    get_slash_namemap,
    get_slash_ropemap,
    get_slash_titlemap,
)
from ch17_jargon.jargon_config import default_unknown_str_if_None
from ch17_jargon.jargon_main import (
    _get_rid_of_jargon_core_keys,
    get_jargonunit_from_dict,
    jargonunit_shop,
)
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx


def test_JargonUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_jargonunit = jargonunit_shop(exx.sue)

    # WHEN
    sue_dict = sue_jargonunit.to_dict()

    # THEN
    print(sue_dict)
    assert sue_dict
    assert sue_dict.get(kw.spark_face) == exx.sue
    assert sue_dict.get(kw.spark_num) == sue_jargonunit.spark_num
    assert sue_dict.get(kw.otx_knot) == default_knot_if_None()
    assert sue_dict.get(kw.inx_knot) == default_knot_if_None()
    assert sue_dict.get(kw.unknown_str) == default_unknown_str_if_None()
    sue_namemap = sue_jargonunit.namemap.to_dict()
    sue_titlemap = sue_jargonunit.titlemap.to_dict()
    sue_labelmap = sue_jargonunit.labelmap.to_dict()
    sue_ropemap = sue_jargonunit.ropemap.to_dict()
    assert sue_dict.get(kw.namemap) == _get_rid_of_jargon_core_keys(sue_namemap)
    assert sue_dict.get(kw.titlemap) == _get_rid_of_jargon_core_keys(sue_titlemap)
    assert sue_dict.get(kw.labelmap) == _get_rid_of_jargon_core_keys(sue_labelmap)
    assert sue_dict.get(kw.ropemap) == _get_rid_of_jargon_core_keys(sue_ropemap)
    assert sue_dict.keys() == sue_jargonunit.__dict__.keys()


def test_JargonUnit_to_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_jargonunit = jargonunit_shop(
        exx.sue, 0, slash_otx_knot, colon_inx_knot, x_unknown_str
    )
    sue_jargonunit.set_namemap(get_slash_namemap())
    sue_jargonunit.set_titlemap(get_slash_titlemap())
    sue_jargonunit.set_labelmap(get_slash_labelmap())
    sue_jargonunit.set_ropemap(get_slash_ropemap())

    # WHEN
    sue_dict = sue_jargonunit.to_dict()

    # THEN
    assert sue_dict.get(kw.spark_face) == exx.sue
    assert sue_dict.get(kw.otx_knot) == slash_otx_knot
    assert sue_dict.get(kw.inx_knot) == colon_inx_knot
    assert sue_dict.get(kw.unknown_str) == x_unknown_str
    sue_namemap = sue_jargonunit.namemap.to_dict()
    sue_titlemap = sue_jargonunit.titlemap.to_dict()
    sue_labelmap = sue_jargonunit.labelmap.to_dict()
    sue_ropemap = sue_jargonunit.ropemap.to_dict()
    assert sue_dict.get(kw.namemap) == _get_rid_of_jargon_core_keys(sue_namemap)
    assert sue_dict.get(kw.titlemap) == _get_rid_of_jargon_core_keys(sue_titlemap)
    assert sue_dict.get(kw.labelmap) == _get_rid_of_jargon_core_keys(sue_labelmap)
    assert sue_dict.get(kw.ropemap) == _get_rid_of_jargon_core_keys(sue_ropemap)


def test_get_jargonunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_spark_num = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_jargonunit = jargonunit_shop(
        exx.sue,
        sue_spark_num,
        slash_otx_knot,
        colon_inx_knot,
        x_unknown_str,
    )
    sue_jargonunit.set_namemap(get_slash_namemap())
    sue_jargonunit.set_labelmap(get_slash_labelmap())
    sue_jargonunit.set_ropemap(get_slash_ropemap())
    sue_jargonunit.set_titlemap(get_slash_titlemap())

    # WHEN
    gen_jargonunit = get_jargonunit_from_dict(sue_jargonunit.to_dict())

    # THEN
    assert gen_jargonunit
    assert gen_jargonunit.spark_face == exx.sue
    assert gen_jargonunit.spark_num == sue_spark_num
    assert gen_jargonunit.otx_knot == slash_otx_knot
    assert gen_jargonunit.inx_knot == colon_inx_knot
    assert gen_jargonunit.unknown_str == x_unknown_str
    assert gen_jargonunit.namemap == get_slash_namemap()
    assert gen_jargonunit.ropemap == get_slash_ropemap()
    assert gen_jargonunit.titlemap == get_slash_titlemap()
