from ch04_rope.rope import create_rope
from ch05_reason.reason_main import caseunit_shop, factunit_shop, reasonunit_shop
from ch06_plan.plan import planunit_shop


def test_PlanUnit_find_replace_rope_Modifies_parent_rope():
    # ESTABLISH Plan with _parent_rope that will be different
    old_casa_str = "casa1"
    old_first_label = "YY"
    old_casa_rope = create_rope(old_first_label, old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_rope = create_rope(old_casa_rope, bloomers_str)
    tulips_str = "tulips"
    old_tulips_rope = create_rope(old_bloomers_rope, tulips_str)
    x_plan = planunit_shop(tulips_str, parent_rope=old_bloomers_rope)
    assert create_rope(x_plan.parent_rope) == old_bloomers_rope
    assert create_rope(x_plan.parent_rope, x_plan.plan_label) == old_tulips_rope

    # WHEN
    new_casa = "casa2"
    new_casa_rope = create_rope(old_first_label, new_casa)
    x_plan.find_replace_rope(old_rope=old_casa_rope, new_rope=new_casa_rope)

    # THEN
    new_bloomers_rope = create_rope(new_casa_rope, bloomers_str)
    new_tulips_rope = create_rope(new_bloomers_rope, tulips_str)
    assert create_rope(x_plan.parent_rope) == new_bloomers_rope
    assert create_rope(x_plan.parent_rope, x_plan.plan_label) == new_tulips_rope


def test_PlanUnit_find_replace_rope_Modifies_reasonunits():
    # ESTABLISH Plan with reason that will be different
    casa_str = "casa1"
    old_first_label = "YY"
    casa_rope = create_rope(old_first_label, casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = create_rope(casa_rope, bloomers_str)
    tulips_str = "tulips"
    tulips_rope = create_rope(bloomers_rope, tulips_str)
    # reason ropes
    old_water_str = "water"
    old_water_rope = create_rope(old_first_label, old_water_str)
    rain_str = "rain"
    old_rain_rope = create_rope(old_water_rope, rain_str)
    # create reasonunit
    case_x = caseunit_shop(reason_state=old_rain_rope)
    cases_x = {case_x.reason_state: case_x}
    x_reason = reasonunit_shop(old_water_rope, cases=cases_x)
    reasons_x = {x_reason.reason_context: x_reason}
    x_plan = planunit_shop(tulips_str, reasonunits=reasons_x)
    # check asserts
    assert x_plan.reasonunits.get(old_water_rope) is not None
    old_water_rain_reason = x_plan.reasonunits[old_water_rope]
    assert old_water_rain_reason.reason_context == old_water_rope
    assert old_water_rain_reason.cases.get(old_rain_rope) is not None
    water_rain_l_case = old_water_rain_reason.cases[old_rain_rope]
    assert water_rain_l_case.reason_state == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = create_rope(old_first_label, new_water_str)
    assert x_plan.reasonunits.get(new_water_rope) is None
    x_plan.find_replace_rope(old_rope=old_water_rope, new_rope=new_water_rope)

    # THEN
    assert x_plan.reasonunits.get(old_water_rope) is None
    assert x_plan.reasonunits.get(new_water_rope) is not None
    new_water_rain_reason = x_plan.reasonunits[new_water_rope]
    assert new_water_rain_reason.reason_context == new_water_rope
    new_rain_rope = create_rope(new_water_rope, rain_str)
    assert new_water_rain_reason.cases.get(old_rain_rope) is None
    assert new_water_rain_reason.cases.get(new_rain_rope) is not None
    new_water_rain_l_case = new_water_rain_reason.cases[new_rain_rope]
    assert new_water_rain_l_case.reason_state == new_rain_rope

    print(f"{len(x_plan.reasonunits)=}")
    reason_obj = x_plan.reasonunits.get(new_water_rope)
    assert reason_obj is not None

    print(f"{len(reason_obj.cases)=}")
    case_obj = reason_obj.cases.get(new_rain_rope)
    assert case_obj is not None
    assert case_obj.reason_state == new_rain_rope


def test_PlanUnit_find_replace_rope_Modifies_factunits():
    # ESTABLISH Plan with factunit that will be different
    tulips_str = "tulips"
    old_water_str = "water"
    old_first_label = "YY"
    old_water_rope = create_rope(old_first_label, old_water_str)
    rain_str = "rain"
    old_rain_rope = create_rope(old_water_rope, rain_str)

    x_factunit = factunit_shop(fact_context=old_water_rope, fact_state=old_rain_rope)
    factunits_x = {x_factunit.fact_context: x_factunit}
    x_plan = planunit_shop(tulips_str, factunits=factunits_x)
    assert x_plan.factunits[old_water_rope] is not None
    old_water_rain_factunit = x_plan.factunits[old_water_rope]
    assert old_water_rain_factunit.fact_context == old_water_rope
    assert old_water_rain_factunit.fact_state == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = create_rope(old_first_label, new_water_str)
    assert x_plan.factunits.get(new_water_rope) is None
    x_plan.find_replace_rope(old_rope=old_water_rope, new_rope=new_water_rope)

    # THEN
    assert x_plan.factunits.get(old_water_rope) is None
    assert x_plan.factunits.get(new_water_rope) is not None
    new_water_rain_factunit = x_plan.factunits[new_water_rope]
    assert new_water_rain_factunit.fact_context == new_water_rope
    new_rain_rope = create_rope(new_water_rope, rain_str)
    assert new_water_rain_factunit.fact_state == new_rain_rope

    print(f"{len(x_plan.factunits)=}")
    x_factunit = x_plan.factunits.get(new_water_rope)
    assert x_factunit is not None
    assert x_factunit.fact_context == new_water_rope
    assert x_factunit.fact_state == new_rain_rope
