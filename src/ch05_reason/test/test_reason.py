from ch04_rope.rope import create_rope, default_knot_if_None
from ch05_reason.reason_main import (
    ReasonCore,
    ReasonHeir,
    ReasonUnit,
    caseunit_shop,
    factheir_shop,
    get_reasonunits_from_dict,
    reasoncore_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from ref.keywords import Ch05Keywords as kw, ExampleStrs as exx


def test_ReasonCore_Exists():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wed_rope = create_rope(wk_rope, exx.wed)
    wed_case = caseunit_shop(reason_state=wed_rope)
    cases = {wed_case.reason_state: wed_case}

    # WHEN
    wk_reason = ReasonCore(wk_rope, cases=cases, active_requisite=False)

    # THEN
    assert wk_reason.reason_context == wk_rope
    assert wk_reason.cases == cases
    assert wk_reason.active_requisite is False
    assert wk_reason.knot is None
    obj_attrs = set(wk_reason.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.knot,
        kw.cases,
        kw.active_requisite,
        kw.reason_context,
    }


def test_reasoncore_shop_ReturnsAttrWith_knot():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa, knot=exx.slash)
    print(f"{casa_rope=} ")

    # WHEN
    casa_reason = reasonheir_shop(casa_rope, knot=exx.slash)

    # THEN
    assert casa_reason.knot == exx.slash


def test_ReasonHeir_Exists():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wed_rope = create_rope(wk_rope, exx.wed)
    wed_case = caseunit_shop(reason_state=wed_rope)
    cases = {wed_case.reason_state: wed_case}

    # WHEN
    wk_reason = ReasonHeir(wk_rope, cases=cases, active_requisite=False)

    # THEN
    assert wk_reason.reason_context == wk_rope
    assert wk_reason.cases == cases
    assert wk_reason.active_requisite is False
    assert wk_reason.knot is None
    obj_attrs = set(wk_reason.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.knot,
        kw.cases,
        kw.active_requisite,
        kw.reason_context,
        kw.reason_active,
        kw.parent_heir_active,
        kw.reason_task,
    }


def test_reasonheir_shop_ReturnsObj():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    casa_reason = reasonheir_shop(casa_rope)

    # THEN
    assert casa_reason.cases == {}
    assert casa_reason.knot == default_knot_if_None()


def test_ReasonHeir_clear_SetsAttrs():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)
    email_case = caseunit_shop(reason_state=email_rope)
    email_cases = {email_case.reason_state: email_case}

    # WHEN
    casa_reason = reasonheir_shop(reason_context=casa_rope, cases=email_cases)
    # THEN
    assert casa_reason.reason_active is None

    # ESTABLISH
    casa_reason.reason_active = True
    assert casa_reason.reason_active
    # WHEN
    casa_reason.clear_reason_active()
    # THEN
    assert casa_reason.reason_active is None
    assert casa_reason.parent_heir_active is None


def test_ReasonHeir_set_reason_active_Setsreason_active():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    fri_str = "fri"
    fri_rope = create_rope(wk_rope, fri_str)
    thu_str = "thur"
    thu_rope = create_rope(wk_rope, thu_str)
    wed_rope = create_rope(wk_rope, exx.wed)
    wed_noon_str = "noon"
    wed_noon_rope = create_rope(wed_rope, wed_noon_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_cases = {wed_case.reason_state: wed_case}
    wk_reason = reasonheir_shop(reason_context=wk_rope, cases=wed_cases)
    assert wk_reason.reason_active is None
    # WHEN
    wk_fact = factheir_shop(fact_context=wk_rope, fact_state=wed_noon_rope)
    wk_facts = {wk_fact.fact_context: wk_fact}
    wk_reason.set_reason_active(factheirs=wk_facts)
    # THEN
    assert wk_reason.reason_active is True

    # ESTABLISH
    thu_case = caseunit_shop(reason_state=thu_rope)
    two_cases = {wed_case.reason_state: wed_case, thu_case.reason_state: thu_case}
    two_reason = reasonheir_shop(reason_context=wk_rope, cases=two_cases)
    assert two_reason.reason_active is None
    # WHEN
    noon_fact = factheir_shop(fact_context=wk_rope, fact_state=wed_noon_rope)
    noon_facts = {noon_fact.fact_context: noon_fact}
    two_reason.set_reason_active(factheirs=noon_facts)
    # THEN
    assert two_reason.reason_active is True

    # ESTABLISH
    two_reason.clear_reason_active()
    assert two_reason.reason_active is None
    # WHEN
    fri_fact = factheir_shop(fact_context=wk_rope, fact_state=fri_rope)
    fri_facts = {fri_fact.fact_context: fri_fact}
    two_reason.set_reason_active(factheirs=fri_facts)
    # THEN
    assert two_reason.reason_active is False


def test_ReasonHeir_set_reason_active_EmptyFactSetsreason_active():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wed_rope = create_rope(wk_rope, exx.wed)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_cases = {wed_case.reason_state: wed_case}
    wk_reason = reasonheir_shop(reason_context=wk_rope, cases=wed_cases)
    assert wk_reason.reason_active is None

    # WHEN
    wk_reason.set_reason_active(factheirs=None)

    # THEN
    assert wk_reason.reason_active is False


def test_ReasonHeir_set_heir_active_SetsAttr():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasonheir_shop(reason_context=wk_rope)
    assert wk_reason.parent_heir_active is None

    # WHEN
    wk_reason.set_heir_active(bool_x=True)

    # THEN
    assert wk_reason.parent_heir_active


def test_ReasonHeir_set_reason_active_PersonTrueSets_reason_activeTrue():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasonheir_shop(reason_context=wk_rope, active_requisite=True)
    wk_reason.set_heir_active(bool_x=True)
    assert wk_reason.reason_active is None

    # WHEN
    wk_reason.set_reason_active(factheirs=None)

    # THEN
    assert wk_reason.reason_active is True


def test_ReasonHeir_set_reason_active_PersonFalseSetsreason_activeTrue():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasonheir_shop(wk_rope, active_requisite=False)
    wk_reason.set_heir_active(bool_x=False)
    assert wk_reason.reason_active is None

    # WHEN
    wk_reason.set_reason_active(factheirs=None)

    # THEN
    assert wk_reason.reason_active is True


def test_ReasonHeir_set_reason_active_PersonTrueSetsreason_activeFalse():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasonheir_shop(wk_rope, active_requisite=True)
    wk_reason.set_heir_active(bool_x=False)
    assert wk_reason.reason_active is None

    # WHEN
    wk_reason.set_reason_active(factheirs=None)

    # THEN
    assert wk_reason.reason_active is False


def test_ReasonHeir_set_reason_active_PersonNoneSetsreason_activeFalse():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasonheir_shop(wk_rope, active_requisite=True)
    wk_reason.set_heir_active(bool_x=None)
    assert wk_reason.reason_active is None

    # WHEN
    wk_reason.set_reason_active(factheirs={})

    # THEN
    assert wk_reason.reason_active is False


def test_ReasonUnit_Exists():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wed_rope = create_rope(wk_rope, exx.wed)
    wed_case = caseunit_shop(reason_state=wed_rope)
    cases = {wed_case.reason_state: wed_case}

    # WHEN
    wk_reason = ReasonUnit(wk_rope, cases=cases, active_requisite=False)

    # THEN
    assert wk_reason.reason_context == wk_rope
    assert wk_reason.cases == cases
    assert wk_reason.active_requisite is False
    assert wk_reason.knot is None
    obj_attrs = set(wk_reason.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.knot,
        kw.cases,
        kw.active_requisite,
        kw.reason_context,
    }


def test_reasonunit_shop_ReturnsObj():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)

    # WHEN
    wk_reasonunit = reasonunit_shop(wk_rope)

    # THEN
    assert wk_reasonunit.cases == {}
    assert wk_reasonunit.knot == default_knot_if_None()


def test_ReasonUnit_to_dict_ReturnsDictWithSinglethu_caseequireds():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wed_rope = create_rope(wk_rope, exx.wed)
    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_cases = {wed_case.reason_state: wed_case}
    wk_reason = reasonunit_shop(wk_rope, cases=wed_cases)

    # WHEN
    wk_reason_dict = wk_reason.to_dict()

    # THEN
    assert wk_reason_dict is not None
    static_wk_reason_dict = {
        "reason_context": wk_rope,
        kw.cases: {wed_rope: {kw.reason_state: wed_rope}},
    }
    print(wk_reason_dict)
    assert wk_reason_dict == static_wk_reason_dict


def test_ReasonUnit_to_dict_ReturnsDictWith_active_requisite():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_active_requisite = True
    wk_reason = reasonunit_shop(
        wk_rope,
        active_requisite=wk_active_requisite,
    )

    # WHEN
    wk_reason_dict = wk_reason.to_dict()

    # THEN
    assert wk_reason_dict is not None
    static_wk_reason_dict = {
        "reason_context": wk_rope,
        kw.active_requisite: wk_active_requisite,
    }
    print(wk_reason_dict)
    assert wk_reason_dict == static_wk_reason_dict


def test_ReasonUnit_to_dict_ReturnsDictWithTwoCasesReasons():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wed_rope = create_rope(wk_rope, exx.wed)
    thu_str = "thur"
    thu_rope = create_rope(wk_rope, thu_str)
    wed_case = caseunit_shop(reason_state=wed_rope)
    thu_case = caseunit_shop(reason_state=thu_rope)
    two_cases = {wed_case.reason_state: wed_case, thu_case.reason_state: thu_case}
    wk_reason = reasonunit_shop(wk_rope, cases=two_cases)

    # WHEN
    wk_reason_dict = wk_reason.to_dict()

    # THEN
    assert wk_reason_dict is not None
    static_wk_reason_dict = {
        "reason_context": wk_rope,
        kw.cases: {
            wed_rope: {kw.reason_state: wed_rope},
            thu_rope: {kw.reason_state: thu_rope},
        },
    }
    print(wk_reason_dict)
    assert wk_reason_dict == static_wk_reason_dict


def test_get_reasonunits_from_dict_ReturnsObj():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_active_requisite = False
    wk_reasonunit = reasonunit_shop(
        wk_rope,
        active_requisite=wk_active_requisite,
    )
    x_wk_reasonunits_dict = {wk_reasonunit.reason_context: wk_reasonunit.to_dict()}
    assert x_wk_reasonunits_dict is not None
    static_wk_reason_dict = {
        wk_rope: {
            "reason_context": wk_rope,
            kw.active_requisite: wk_active_requisite,
        }
    }
    assert x_wk_reasonunits_dict == static_wk_reason_dict

    # WHEN
    reasonunits_dict = get_reasonunits_from_dict(x_wk_reasonunits_dict)

    # THEN
    assert len(reasonunits_dict) == 1
    assert reasonunits_dict.get(wk_reasonunit.reason_context) == wk_reasonunit


def test_ReasonHeir_correctSetsPledgeState():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    range_3_to_6_case = caseunit_shop(
        reason_state=wk_rope, reason_lower=3, reason_upper=6
    )
    range_3_to_6_cases = {range_3_to_6_case.reason_state: range_3_to_6_case}
    range_3_to_6_reason = reasonheir_shop(wk_rope, range_3_to_6_cases)
    assert range_3_to_6_reason.reason_active is None

    # WHEN
    range_5_to_8_fact = factheir_shop(wk_rope, wk_rope, fact_lower=5, fact_upper=8)
    range_5_to_8_facts = {range_5_to_8_fact.fact_context: range_5_to_8_fact}
    range_3_to_6_reason.set_reason_active(factheirs=range_5_to_8_facts)
    # THEN
    assert range_3_to_6_reason.reason_active is True
    assert range_3_to_6_reason.reason_task is True

    # WHEN
    range_5_to_6_fact = factheir_shop(wk_rope, wk_rope, fact_lower=5, fact_upper=6)
    range_5_to_6_facts = {range_5_to_6_fact.fact_context: range_5_to_6_fact}
    range_3_to_6_reason.set_reason_active(factheirs=range_5_to_6_facts)
    # THEN
    assert range_3_to_6_reason.reason_active is True
    assert range_3_to_6_reason.reason_task is False

    # WHEN
    range_0_to_1_fact = factheir_shop(wk_rope, wk_rope, fact_lower=0, fact_upper=1)
    range_0_to_1_facts = {range_0_to_1_fact.fact_context: range_0_to_1_fact}
    range_3_to_6_reason.set_reason_active(factheirs=range_0_to_1_facts)
    # THEN
    assert range_3_to_6_reason.reason_active is False
    assert range_3_to_6_reason.reason_task is None


def test_ReasonCore_get_cases_count():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)

    # WHEN
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    # THEN
    assert wk_reason.get_cases_count() == 0

    # WHEN
    range_3_to_6_case = caseunit_shop(
        reason_state=wk_rope, reason_lower=3, reason_upper=6
    )
    range_3_to_6_cases = {range_3_to_6_case.reason_state: range_3_to_6_case}
    wk_reason = reasoncore_shop(reason_context=wk_rope, cases=range_3_to_6_cases)
    # THEN
    assert wk_reason.get_cases_count() == 1


def test_ReasonCore_set_case_SetsCase():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    assert wk_reason.get_cases_count() == 0

    # WHEN
    wk_reason.set_case(case=wk_rope, reason_lower=3, reason_upper=6)

    # THEN
    assert wk_reason.get_cases_count() == 1
    range_3_to_6_case = caseunit_shop(
        reason_state=wk_rope, reason_lower=3, reason_upper=6
    )
    cases = {range_3_to_6_case.reason_state: range_3_to_6_case}
    assert wk_reason.cases == cases


def test_ReasonCore_case_exists_ReturnsObj():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    assert not wk_reason.case_exists(wk_rope)

    # WHEN
    wk_reason.set_case(wk_rope, reason_lower=3, reason_upper=6)

    # THEN
    assert wk_reason.case_exists(wk_rope)


def test_ReasonCore_get_single_premis_ReturnsObj():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, "wk")
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    wk_reason.set_case(case=wk_rope, reason_lower=3, reason_upper=6)
    wk_reason.set_case(case=wk_rope, reason_lower=7, reason_upper=10)
    noon_rope = create_rope(wk_rope, "noon")
    wk_reason.set_case(case=noon_rope)
    assert wk_reason.get_cases_count() == 2

    # WHEN / THEN
    assert wk_reason.get_case(case=wk_rope).reason_lower == 7
    assert wk_reason.get_case(case=noon_rope).reason_lower is None


def test_ReasonCore_del_case_DeletesCase():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason = reasoncore_shop(reason_context=wk_rope)
    wk_reason.set_case(case=wk_rope, reason_lower=3, reason_upper=6)
    assert wk_reason.get_cases_count() == 1

    # WHEN
    wk_reason.del_case(case=wk_rope)

    # THEN
    assert wk_reason.get_cases_count() == 0


def test_ReasonCore_find_replace_rope_casas():
    # ESTABLISH
    sun_str = "Sun"
    old_rope = create_rope("old_fun")
    old_wk_rope = create_rope(old_rope, exx.wk)
    old_sun_rope = create_rope(old_wk_rope, sun_str)
    x_reason = reasoncore_shop(reason_context=old_wk_rope)
    x_reason.set_case(case=old_sun_rope)
    # print(f"{x_reason=}")
    assert x_reason.reason_context == old_wk_rope
    assert len(x_reason.cases) == 1
    print(f"{x_reason.cases=}")
    new_rope = create_rope("fun")
    assert x_reason.cases.get(old_sun_rope).reason_state == old_sun_rope

    # WHEN
    x_reason.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    # THEN
    new_wk_rope = create_rope(new_rope, exx.wk)
    new_sun_rope = create_rope(new_wk_rope, sun_str)
    assert x_reason.reason_context == new_wk_rope
    assert len(x_reason.cases) == 1
    assert x_reason.cases.get(new_sun_rope) is not None
    assert x_reason.cases.get(old_sun_rope) is None
    print(f"{x_reason.cases=}")
    assert x_reason.cases.get(new_sun_rope).reason_state == new_sun_rope


def test_ReasonCore_set_knot_SetsAttrs():
    # ESTABLISH
    sun_str = "Sun"
    slash_wk_rope = create_rope(exx.a23, exx.wk, knot=exx.slash)
    slash_sun_rope = create_rope(slash_wk_rope, sun_str, knot=exx.slash)
    wk_reasonunit = reasoncore_shop(slash_wk_rope, knot=exx.slash)
    wk_reasonunit.set_case(slash_sun_rope)
    assert wk_reasonunit.knot == exx.slash
    assert wk_reasonunit.reason_context == slash_wk_rope
    assert wk_reasonunit.cases.get(slash_sun_rope).reason_state == slash_sun_rope

    # WHEN
    colon_str = ":"
    wk_reasonunit.set_knot(new_knot=colon_str)

    # THEN
    assert wk_reasonunit.knot == colon_str
    colon_wk_rope = create_rope(exx.a23, exx.wk, knot=colon_str)
    colon_sun_rope = create_rope(colon_wk_rope, sun_str, knot=colon_str)
    assert wk_reasonunit.reason_context == colon_wk_rope
    assert wk_reasonunit.cases.get(colon_sun_rope) is not None
    assert wk_reasonunit.cases.get(colon_sun_rope).reason_state == colon_sun_rope


def test_ReasonCore_get_obj_key():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    email_str = "check email"
    email_rope = create_rope(casa_rope, email_str)
    email_case = caseunit_shop(reason_state=email_rope)
    cases_x = {email_case.reason_state: email_case}

    # WHEN
    x_reason = reasonheir_shop(casa_rope, cases=cases_x)

    # THEN
    assert x_reason.get_obj_key() == casa_rope
