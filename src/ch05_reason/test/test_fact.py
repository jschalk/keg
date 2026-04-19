from ch04_rope.rope import create_rope
from ch05_reason.reason_main import (
    FactCore,
    FactUnit,
    factheir_shop,
    factunit_shop,
    get_factunit_from_tuple,
    get_factunits_from_dict,
)
from ref.keywords import Ch05Keywords as kw, ExampleStrs as exx


def test_FactUnit_Exists():
    # ESTABLISH / WHEN
    x_fact = FactUnit()

    # THEN
    assert not x_fact.fact_context
    assert not x_fact.fact_state
    assert not x_fact.fact_lower
    assert not x_fact.fact_upper
    obj_attrs = set(x_fact.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.fact_context,
        kw.fact_upper,
        kw.fact_lower,
        kw.fact_state,
    }


def test_FactUnit_DataClass_function():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)

    # WHEN
    sun_fact = FactUnit(
        fact_context=wk_rope, fact_state=sun_rope, fact_lower=1.9, fact_upper=2.3
    )

    # THEN
    print(sun_fact)
    assert sun_fact is not None
    assert sun_fact.fact_context == wk_rope
    assert sun_fact.fact_state == sun_rope
    assert sun_fact.fact_lower == 1.9
    assert sun_fact.fact_upper == 2.3


def test_FactUnit_set_range_null_SetsAttr_1():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_fact = factunit_shop(wk_rope, wk_rope, fact_lower=1.0, fact_upper=5.0)
    assert wk_fact.fact_lower == 1.0
    assert wk_fact.fact_upper == 5.0

    # WHEN
    wk_fact.set_range_null()

    # THEN
    assert wk_fact.fact_lower is None
    assert wk_fact.fact_upper is None


def test_FactUnit_set_fact_state_to_fact_context_SetsAttr_1():
    # ESTABLISH
    floor_str = "floor"
    floor_rope = create_rope(exx.a23, floor_str)
    dirty_str = "dirty"
    dirty_rope = create_rope(exx.a23, dirty_str)
    floor_fact = factunit_shop(floor_rope, dirty_rope)
    assert floor_fact.fact_context == floor_rope
    assert floor_fact.fact_state == dirty_rope

    # WHEN
    floor_fact.set_fact_state_to_fact_context()

    # THEN
    assert floor_fact.fact_context == floor_rope
    assert floor_fact.fact_state == floor_rope


def test_FactUnit_set_fact_state_to_fact_context_SetsAttr_2():
    # ESTABLISH
    floor_str = "floor"
    floor_rope = create_rope(exx.a23, floor_str)
    dirty_str = "dirty"
    dirty_rope = create_rope(exx.a23, dirty_str)
    floor_fact = factunit_shop(floor_rope, dirty_rope, 1, 6)
    assert floor_fact.fact_lower is not None
    assert floor_fact.fact_upper is not None

    # WHEN
    floor_fact.set_fact_state_to_fact_context()

    # THEN
    assert floor_fact.fact_lower is None
    assert floor_fact.fact_upper is None


def test_FactUnit_set_attr_SetsAttr_2():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_fact = factunit_shop(wk_rope, wk_rope, fact_lower=1.0, fact_upper=5.0)

    # WHEN
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    wk_fact.set_attr(fact_state=sun_rope)
    # THEN
    assert wk_fact.fact_state == sun_rope

    # WHEN
    wk_fact.set_attr(fact_lower=45)
    # THEN
    assert wk_fact.fact_lower == 45

    # WHEN
    wk_fact.set_attr(fact_upper=65)
    # THEN
    assert wk_fact.fact_upper == 65


def test_FactUnit_to_dict_ReturnsDict():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    x_fact_lower = 35
    x_fact_upper = 50
    sun_fact = factunit_shop(
        fact_context=wk_rope,
        fact_state=sun_rope,
        fact_lower=x_fact_lower,
        fact_upper=x_fact_upper,
    )
    print(sun_fact)

    # WHEN
    fact_dict = sun_fact.to_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        kw.fact_context: wk_rope,
        kw.fact_state: sun_rope,
        "fact_lower": x_fact_lower,
        "fact_upper": x_fact_upper,
    }
    assert fact_dict == static_dict


def test_FactUnit_to_dict_ReturnsPartialDict():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact = factunit_shop(fact_context=wk_rope, fact_state=sun_rope)
    print(sun_fact)

    # WHEN
    fact_dict = sun_fact.to_dict()

    # THEN
    assert fact_dict is not None
    static_dict = {
        kw.fact_context: wk_rope,
        kw.fact_state: sun_rope,
    }
    assert fact_dict == static_dict


def test_FactUnit_find_replace_rope_SetsAttr():
    # ESTABLISH
    old_rope = create_rope("old_new")
    old_wk_rope = create_rope(old_rope, exx.wk)
    sun_str = "Sun"
    old_sun_rope = create_rope(old_wk_rope, sun_str)
    sun_fact = factunit_shop(fact_context=old_wk_rope, fact_state=old_sun_rope)
    print(sun_fact)
    assert sun_fact.fact_context == old_wk_rope
    assert sun_fact.fact_state == old_sun_rope

    # WHEN
    new_rope = create_rope("new_fun")
    sun_fact.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    # THEN
    new_wk_rope = create_rope(new_rope, exx.wk)
    new_sun_rope = create_rope(new_wk_rope, sun_str)
    assert sun_fact.fact_context == new_wk_rope
    assert sun_fact.fact_state == new_sun_rope


def test_FactUnit_get_tuple_ReturnsObj_Scenario0_reason_context_fact_state_only():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact = factunit_shop(fact_context=wk_rope, fact_state=sun_rope)

    # WHEN
    sun_tuple = sun_fact.get_tuple()

    # THEN
    assert sun_tuple
    assert sun_tuple == (wk_rope, sun_rope, None, None)


def test_FactUnit_get_tuple_ReturnsObj_Scenario1_ValuesIn_fact_lower_fact_upper():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact_lower = 6
    sun_fact_upper = 9
    sun_fact = factunit_shop(wk_rope, sun_rope, sun_fact_lower, sun_fact_upper)

    # WHEN
    sun_tuple = sun_fact.get_tuple()

    # THEN
    assert sun_tuple
    assert sun_tuple == (wk_rope, sun_rope, sun_fact_lower, sun_fact_upper)


def test_get_factunit_from_tuple_ReturnsObj_Scenario0_reason_context_fact_state_only():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact = factunit_shop(fact_context=wk_rope, fact_state=sun_rope)
    sun_tuple = sun_fact.get_tuple()

    # WHEN
    gen_sun_factunit = get_factunit_from_tuple(sun_tuple)

    # THEN
    assert gen_sun_factunit
    assert gen_sun_factunit == sun_fact


def test_get_factunit_from_tuple_ReturnsObj_Scenario1_ValuesIn_fact_lower_fact_upper():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    sun_fact_lower = 6
    sun_fact_upper = 9
    sun_fact = factunit_shop(wk_rope, sun_rope, sun_fact_lower, sun_fact_upper)
    sun_tuple = sun_fact.get_tuple()

    # WHEN
    gen_sun_factunit = get_factunit_from_tuple(sun_tuple)

    # THEN
    assert gen_sun_factunit
    assert gen_sun_factunit == sun_fact


def test_FactHeir_IsModifiedByFactUnit():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(exx.a23, ced_min_str)
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 20.0, 30.0)
    assert ced_factheir.fact_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.fact_lower == 20

    # ESTABLISH
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 30.0, 30.0)
    assert ced_factheir.fact_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)
    assert ced_factheir.fact_lower == 30

    # ESTABLISH
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 35.0, 57.0)
    assert ced_factheir.fact_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.fact_lower == 10

    # ESTABLISH
    ced_factheir = factheir_shop(min_rope, min_rope, 10.0, 30.0)
    ced_factunit = factunit_shop(min_rope, min_rope, 5.0, 7.0)
    assert ced_factheir.fact_lower == 10

    # WHEN
    ced_factheir.mold(factunit=ced_factunit)

    # THEN
    assert ced_factheir.fact_lower == 10


def test_FactHeir_is_range_ReturnsObj():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(exx.a23, ced_min_str)

    # WHEN
    x_factheir = factheir_shop(fact_context=min_rope, fact_state=min_rope)

    # THEN
    assert x_factheir.is_range() is False

    # WHEN
    x_factheir = factheir_shop(
        min_rope, fact_state=min_rope, fact_lower=10.0, fact_upper=30.0
    )

    # THEN
    assert x_factheir.is_range() is True


def test_FactCore_get_obj_key_SetsAttr():
    # ESTABLISH
    ced_min_str = "ced_minute"
    min_rope = create_rope(exx.a23, ced_min_str)
    secs_str = "secs"
    secs_rope = create_rope(min_rope, secs_str)

    # WHEN
    x_factcore = FactCore(fact_context=min_rope, fact_state=secs_rope)

    # THEN
    assert x_factcore.get_obj_key() == min_rope


def test_get_factunits_from_dict_BuildsObj():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    static_dict = {
        wk_rope: {
            kw.fact_context: wk_rope,
            kw.fact_state: sun_rope,
            kw.fact_lower: None,
            kw.fact_upper: None,
        }
    }

    # WHEN
    facts_dict = get_factunits_from_dict(static_dict)

    # THEN
    assert len(facts_dict) == 1
    wk_fact = facts_dict.get(wk_rope)
    assert wk_fact == factunit_shop(fact_context=wk_rope, fact_state=sun_rope)


def test_get_factunits_from_dict_BuildsObjFromIncompleteDict():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    sun_str = "Sun"
    sun_rope = create_rope(wk_rope, sun_str)
    static_dict = {
        wk_rope: {
            kw.fact_context: wk_rope,
            kw.fact_state: sun_rope,
        }
    }

    # WHEN
    facts_dict = get_factunits_from_dict(static_dict)

    # THEN
    wk_fact = facts_dict.get(wk_rope)
    assert wk_fact == factunit_shop(fact_context=wk_rope, fact_state=sun_rope)
