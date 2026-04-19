from ch04_rope.rope import create_rope, default_knot_if_None
from ch05_reason.reason_main import factunit_shop, reasonunit_shop
from ch07_person_logic.person_main import personunit_shop
from ch13_time.epoch_main import add_epoch_planunit
from ch13_time.epoch_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from ch13_time.test._util.ch13_examples import get_creg_config, get_thu
from ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_get_reason_case_readable_str_ReturnsObj_Scenario0_Level1():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation casa"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    situation_casa_reason = reasonunit_shop(situation_casa_rope)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(situation_casa_rope, dirty_floors_str)
    situation_casa_reason.set_case(dirty_floors_rope)
    dirty_floors_case = situation_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        situation_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    expected_str = f"case: {dirty_floors_str}{default_knot_if_None()}"
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario1_TwoLevel_state():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    situation_casa_reason = reasonunit_shop(situation_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(situation_casa_rope, non_furniture_str)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(non_furniture_rope, dirty_floors_str)
    situation_casa_reason.set_case(dirty_floors_rope)
    dirty_floors_case = situation_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        reason_context=situation_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    default_knot = default_knot_if_None()
    expected_str = (
        f"case: {non_furniture_str}{default_knot}{dirty_floors_str}{default_knot}"
    )
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario2_CaseRange():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    situation_casa_reason = reasonunit_shop(situation_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(situation_casa_rope, non_furniture_str)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(non_furniture_rope, dirty_floors_str)
    dirtiness_lower_int = 4
    dirtiness_upper_int = 8
    situation_casa_reason.set_case(
        dirty_floors_rope,
        reason_lower=dirtiness_lower_int,
        reason_upper=dirtiness_upper_int,
    )
    dirty_floors_case = situation_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        reason_context=situation_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario3_CaseRangeAnd_reason_divisor():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    situation_casa_reason = reasonunit_shop(situation_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(situation_casa_rope, non_furniture_str)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(non_furniture_rope, dirty_floors_str)
    dirtiness_lower_int = 4
    dirtiness_upper_int = 8
    dirtiness_divisor_int = 2
    situation_casa_reason.set_case(
        dirty_floors_rope,
        reason_lower=dirtiness_lower_int,
        reason_upper=dirtiness_upper_int,
        reason_divisor=dirtiness_divisor_int,
    )
    dirty_floors_case = situation_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        situation_casa_rope, dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} divided by {dirtiness_divisor_int} then from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario4_creg_config():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    add_epoch_planunit(sue_person, get_creg_config())
    time_rope = sue_person.make_l1_rope(kw.time)
    creg_rope = sue_person.make_rope(time_rope, kw.creg)
    week_rope = sue_person.make_rope(creg_rope, kw.week)
    thu_rope = sue_person.make_rope(week_rope, get_thu())
    thu_plan = sue_person.get_plan_obj(thu_rope)

    casa_rope = sue_person.make_l1_rope(exx.casa)
    mop_rope = sue_person.make_rope(casa_rope, exx.mop)
    sue_person.add_plan(mop_rope, pledge=True)
    sue_person.edit_plan_attr(
        mop_rope,
        reason_context=week_rope,
        reason_case=week_rope,
        reason_lower=1440,
        reason_upper=2880,
    )
    mop_plan = sue_person.get_plan_obj(mop_rope)
    week_reason = mop_plan.get_reasonunit(week_rope)
    week_case = week_reason.get_case(week_rope)

    # WHEN
    display_str = get_reason_case_readable_str(
        week_rope, week_case, kw.creg, sue_person
    )

    # THEN
    assert display_str
    expected_str = f"case: every {get_thu()}"
    assert display_str == expected_str


def test_get_fact_state_readable_str_ReturnsObj_Scenario0_Level1():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation casa"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    dirty_str = "dirty floors"
    dirty_rope = create_rope(situation_casa_rope, dirty_str)
    situation_casa_fact = factunit_shop(situation_casa_rope, dirty_rope)

    # WHEN
    dirty_fact_str = get_fact_state_readable_str(factunit=situation_casa_fact)

    # THEN
    assert dirty_fact_str
    default_knot = default_knot_if_None()
    expected_str = f"({situation_casa_str}) fact: {dirty_str}{default_knot}"
    assert dirty_fact_str == expected_str


def test_get_fact_state_readable_str_ReturnsObj_Scenario1_TwoLevel_state():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    situation_casa_reason = reasonunit_shop(situation_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(situation_casa_rope, non_furniture_str)
    dirty_str = "dirty floors"
    dirty_rope = create_rope(non_furniture_rope, dirty_str)
    situation_casa_reason.set_case(dirty_rope)
    situation_casa_fact = factunit_shop(situation_casa_rope, dirty_rope)

    # WHEN
    dirty_fact_str = get_fact_state_readable_str(situation_casa_fact)

    # THEN
    assert dirty_fact_str
    default_knot = default_knot_if_None()
    expected_str = f"({situation_casa_str}) fact: {non_furniture_str}{default_knot}{dirty_str}{default_knot}"
    assert dirty_fact_str == expected_str


def test_get_fact_state_readable_str_ReturnsObj_Scenario2_CaseRange():
    # ESTABLISH
    casa_rope = create_rope(exx.a23, exx.casa)
    situation_casa_str = "situation"
    situation_casa_rope = create_rope(casa_rope, situation_casa_str)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(situation_casa_rope, non_furniture_str)
    dirty_str = "dirty floors"
    dirty_rope = create_rope(non_furniture_rope, dirty_str)
    dirtiness_lower_int = 4
    dirtiness_upper_int = 8
    situation_casa_fact = factunit_shop(
        fact_context=situation_casa_rope,
        fact_state=dirty_rope,
        fact_lower=dirtiness_lower_int,
        fact_upper=dirtiness_upper_int,
    )

    # WHEN
    dirty_fact_str = get_fact_state_readable_str(situation_casa_fact)

    # THEN
    assert dirty_fact_str
    x1 = default_knot_if_None()
    expected_str = f"({situation_casa_str}) fact: {non_furniture_str}{x1}{dirty_str}{x1} from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_fact_str == expected_str


def test_get_fact_state_readable_str_ReturnsObj_Scenario3_creg_config():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    time_rope = sue_person.make_l1_rope(kw.time)
    creg_rope = sue_person.make_rope(time_rope, kw.creg)
    add_epoch_planunit(sue_person, get_creg_config())
    sue_person.add_fact(creg_rope, creg_rope, 1234567890, 1334567890)
    root_creg_fact = sue_person.planroot.factunits.get(creg_rope)
    print(f"{root_creg_fact=}")

    # WHEN
    epoch_fact_str = get_fact_state_readable_str(root_creg_fact, kw.creg, sue_person)

    # THEN
    assert epoch_fact_str
    expected_str = (
        "from 7pm:30, Tuesday, 24 June, 2347 to 6am:10, Sunday, 11 August, 2537"
    )
    assert epoch_fact_str == expected_str
