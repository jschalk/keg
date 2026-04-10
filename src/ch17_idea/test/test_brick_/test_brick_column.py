from src.ch17_idea.brick_main import BrickRef, brickref_shop
from src.ref.keywords import Ch17Keywords as kw


def test_BrickRef_Exists():
    # ESTABLISH / WHEN
    x_brickref = BrickRef()

    # THEN
    assert not x_brickref.brick_name
    assert not x_brickref.dimens
    assert not x_brickref.attributes


def test_brickref_shop_ReturnsObj():
    # ESTABLISH
    x1_brick_name = "0001"

    # WHEN
    x_brickref = brickref_shop(
        x_brick_name=x1_brick_name, x_dimens=[kw.person_contactunit]
    )

    # THEN
    assert x_brickref.brick_name == x1_brick_name
    assert x_brickref.dimens == [kw.person_contactunit]
    assert x_brickref.attributes == {}


def test_BrickRef_set_attribute_SetsAttr():
    # ESTABLISH
    x_brickref = brickref_shop("0003", kw.person_contactunit)
    x_attribute = "1"
    assert x_brickref.attributes == {}

    # WHEN
    x_brickref.set_attribute(x_attribute, True)

    # THEN
    assert x_brickref.attributes != {}
    assert x_brickref.attributes == {x_attribute: {"otx_key": True}}


def test_BrickRef_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_brickref = brickref_shop("0003", kw.person_contactunit)

    # WHEN
    x_headers_list = x_brickref.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_BrickRef_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", kw.person_contactunit)
    x3_brickref.set_attribute(kw.group_title, True)

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [kw.group_title]


def test_BrickRef_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", kw.person_contactunit)
    x3_brickref.set_attribute(kw.plan_rope, True)
    x3_brickref.set_attribute(kw.group_title, False)
    x3_brickref.set_attribute(kw.contact_name, True)

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [kw.contact_name, kw.group_title, kw.plan_rope]


def test_BrickRef_get_otx_keys_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_brickref = brickref_shop("0003", kw.person_contactunit)

    # WHEN
    x_otx_keys_list = x_brickref.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == []


def test_BrickRef_get_otx_keys_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", kw.person_contactunit)
    x3_brickref.set_attribute(kw.group_title, True)

    # WHEN
    x_otx_keys_list = x3_brickref.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [kw.group_title]


def test_BrickRef_get_otx_keys_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", kw.person_contactunit)
    x3_brickref.set_attribute(kw.plan_rope, True)
    x3_brickref.set_attribute(kw.group_title, False)
    x3_brickref.set_attribute(kw.contact_name, True)

    # WHEN
    x_otx_keys_list = x3_brickref.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [kw.contact_name, kw.plan_rope]


def test_BrickRef_get_otx_values_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_brickref = brickref_shop("0003", kw.person_contactunit)

    # WHEN
    x_otx_values_list = x_brickref.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_BrickRef_get_otx_values_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", kw.person_contactunit)
    x3_brickref.set_attribute(kw.group_title, True)

    # WHEN
    x_otx_values_list = x3_brickref.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_BrickRef_get_otx_values_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", kw.person_contactunit)
    x3_brickref.set_attribute(kw.plan_rope, True)
    x3_brickref.set_attribute(kw.group_title, False)
    x3_brickref.set_attribute(kw.reason_context, False)
    x3_brickref.set_attribute(kw.contact_name, False)

    # WHEN
    x_otx_values_list = x3_brickref.get_otx_values_list()

    # THEN
    assert x_otx_values_list == [
        kw.contact_name,
        kw.group_title,
        kw.reason_context,
    ]
