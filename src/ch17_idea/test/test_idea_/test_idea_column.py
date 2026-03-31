from src.ch17_idea.idea_main import IdeaRef, idearef_shop
from src.ref.keywords import Ch17Keywords as kw


def test_IdeaRef_Exists():
    # ESTABLISH / WHEN
    x_idearef = IdeaRef()

    # THEN
    assert not x_idearef.idea_name
    assert not x_idearef.dimens
    assert not x_idearef.attributes


def test_idearef_shop_ReturnsObj():
    # ESTABLISH
    x1_idea_name = "0001"

    # WHEN
    x_idearef = idearef_shop(x_idea_name=x1_idea_name, x_dimens=[kw.person_contactunit])

    # THEN
    assert x_idearef.idea_name == x1_idea_name
    assert x_idearef.dimens == [kw.person_contactunit]
    assert x_idearef.attributes == {}


def test_IdeaRef_set_attribute_SetsAttr():
    # ESTABLISH
    x_idearef = idearef_shop("0003", kw.person_contactunit)
    x_attribute = "1"
    assert x_idearef.attributes == {}

    # WHEN
    x_idearef.set_attribute(x_attribute, True)

    # THEN
    assert x_idearef.attributes != {}
    assert x_idearef.attributes == {x_attribute: {"otx_key": True}}


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_idearef = idearef_shop("0003", kw.person_contactunit)

    # WHEN
    x_headers_list = x_idearef.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", kw.person_contactunit)
    x3_idearef.set_attribute(kw.group_title, True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [kw.group_title]


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", kw.person_contactunit)
    x3_idearef.set_attribute(kw.plan_rope, True)
    x3_idearef.set_attribute(kw.group_title, False)
    x3_idearef.set_attribute(kw.contact_name, True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [kw.contact_name, kw.group_title, kw.plan_rope]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", kw.person_contactunit)

    # WHEN
    x_otx_keys_list = x_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == []


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", kw.person_contactunit)
    x3_idearef.set_attribute(kw.group_title, True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [kw.group_title]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", kw.person_contactunit)
    x3_idearef.set_attribute(kw.plan_rope, True)
    x3_idearef.set_attribute(kw.group_title, False)
    x3_idearef.set_attribute(kw.contact_name, True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [kw.contact_name, kw.plan_rope]


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", kw.person_contactunit)

    # WHEN
    x_otx_values_list = x_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", kw.person_contactunit)
    x3_idearef.set_attribute(kw.group_title, True)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", kw.person_contactunit)
    x3_idearef.set_attribute(kw.plan_rope, True)
    x3_idearef.set_attribute(kw.group_title, False)
    x3_idearef.set_attribute(kw.reason_context, False)
    x3_idearef.set_attribute(kw.contact_name, False)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == [
        kw.contact_name,
        kw.group_title,
        kw.reason_context,
    ]
