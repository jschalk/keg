from ch06_plan.test._util.ch06_examples import get_range_attrs
from ch07_person_logic.person_main import PersonUnit, PlanUnit, RopeTerm
from ch13_time._ref.ch13_semantic_types import FactNum, ReasonNum
from ch13_time.epoch_reason import (
    set_epoch_base_case_dayly,
    set_epoch_cases_for_monthly,
    set_epoch_cases_for_yearly_monthday,
)
from ch13_time.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_person,
)
from ref.keywords import Ch13Keywords as kw


def test_set_epoch_base_case_dayly_ChangesPersonUnit_agenda():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    bob_person.add_fact(wx.five_rope, wx.five_rope, 500, 500)
    assert len(bob_person.get_agenda_dict()) == 1

    # WHEN
    set_epoch_base_case_dayly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
    )

    # THEN
    assert len(bob_person.get_agenda_dict()) == 0
    # WHEN
    bob_person.add_fact(wx.five_rope, wx.five_rope, 500, 1000)

    # THEN
    bob_person.thinkout()
    print(f"{bob_person.planroot.factheirs.keys()=}")
    mop_plan = bob_person.get_plan_obj(wx.mop_rope)
    day_factheir = mop_plan.factheirs.get(wx.day_rope)
    day_reasonheir = mop_plan.reasonheirs.get(wx.day_rope)
    day_heir_case = day_reasonheir.cases.get(wx.day_rope)
    print(f" {day_factheir=}")
    print(f"{day_heir_case=}")
    assert len(bob_person.get_agenda_dict()) == 1


def test_set_epoch_cases_for_yearly_monthday_ChangesPersonUnit_agenda():
    # ESTABLISH
    bob_person = get_bob_five_person()
    month_geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday = 3
    mop_length_days = 4
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    bob_person.add_fact(wx.five_rope, wx.five_rope, 400, 440)
    assert len(bob_person.get_agenda_dict()) == 1

    # WHEN 1
    set_epoch_cases_for_yearly_monthday(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
        month_label=wx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN 1
    assert len(bob_person.get_agenda_dict()) == 0

    # WHEN 2
    bob_person.add_fact(wx.five_rope, wx.five_rope, 400, 100000)

    # THEN 2
    print("epoch fact changed")
    bob_person.thinkout()
    mop_plan = bob_person.get_plan_obj(wx.mop_rope)
    day_reasonheir = mop_plan.reasonheirs.get(wx.day_rope)
    day_caseunit = day_reasonheir.cases.get(wx.day_rope)
    day_factheir = mop_plan.factheirs.get(wx.day_rope)
    print(f"{day_factheir=}")
    print(f"{day_caseunit=}")
    assert len(bob_person.get_agenda_dict()) == 1
    # geo_reasonheir = mop_plan.reasonheirs.get(month_geo_rope)
    # geo_factheir = mop_plan.factheirs.get(month_geo_rope)
    # print(f"{geo_factheir=}")
    # print(f"{day_reasonheir=}")
    # print(f"{geo_reasonheir.reason_active=}")
    # print(f"{mop_plan.factheirs.keys()=}")


def expected_ag_count_fact_set(
    mop_plan: PlanUnit,
    x_person: PersonUnit,
    fact_lower: FactNum,
    fact_upper: FactNum,
    expected: int,
) -> dict[RopeTerm, PlanUnit]:
    x_person.add_fact(wx.five_rope, wx.five_rope, fact_lower, fact_upper)
    x_person.thinkout()
    is_as_expected = expected == len(x_person.get_agenda_dict())
    if not is_as_expected:
        display_out_factheir_attrs(mop_plan)
        # for month_case in year_reasonheir.cases.values():
        #     print(
        #         f"{get_tail_label(month_case.reason_state):10} {month_case.reason_lower=} {month_case.reason_upper=} {month_case.case_active=}"
        #     )
    return is_as_expected


def display_out_factheir_attrs(mop_plan: PlanUnit):
    five_factheir = mop_plan.factheirs.get(wx.five_rope)
    year_factheir = mop_plan.factheirs.get(wx.five_year_rope)
    day_factheir = mop_plan.factheirs.get(wx.day_rope)
    print(f"{mop_plan.factheirs.keys()=}")
    print(f"mop_plan factheir {five_factheir.fact_lower=} {five_factheir.fact_upper}")
    print(f"mop_plan factheir {year_factheir.fact_lower=} {year_factheir.fact_upper}")
    print(f"mop_plan factheir {day_factheir.fact_lower=} {day_factheir.fact_upper}")


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario1_ChangesPersonUnit_agenda():
    # ESTABLISH
    bob_person = get_bob_five_person()
    mop_monthday = 5
    mop_length_days = 1
    mop_dayly_lower_min = 600
    mop_day_duration = 90
    set_epoch_cases_for_monthly(
        x_person=bob_person,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        dayly_lower_min=mop_dayly_lower_min,
        dayly_duration_min=mop_day_duration,
    )
    mop_plan = bob_person.get_plan_obj(wx.mop_rope)

    # WHEN / THEN
    assert expected_ag_count_fact_set(mop_plan, bob_person, 0, 0, 0)
    year_plan = bob_person.get_plan_obj(wx.five_year_rope)
    print(f"{get_range_attrs(year_plan)=}")
    assert expected_ag_count_fact_set(mop_plan, bob_person, 525600, 525600, 0)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 0, 1, expected=0)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 7200, 30240, expected=1)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 30240, 30240, expected=0)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 187200, 187520, expected=0)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 189820, 189820, expected=0)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 246240, 280800, expected=1)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 7200, 30240, expected=1)
    assert expected_ag_count_fact_set(mop_plan, bob_person, 525599, 525599, expected=0)
