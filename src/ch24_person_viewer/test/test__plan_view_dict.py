from src.ch06_plan.plan import planunit_shop
from src.ch13_time.epoch_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.ch24_person_viewer.person_viewer_example import (
    best_bowl_str,
    best_run_str,
    best_soccer_str,
    best_sport_str,
    get_personunit_irrational_example,
    get_sue_person_with_facts_and_reasons,
    get_sue_personunit,
    play_bowl_str,
    play_run_str,
    play_soccer_str,
    play_str,
)
from src.ch24_person_viewer.person_viewer_tool import add_small_dot, get_plan_view_dict
from src.ref.keywords import Ch24Keywords as kw, ExampleStrs as exx


def test_get_plan_view_dict_ReturnsObj_Scenario0_EmptyPlan():
    # ESTABLISH
    casa_plan = planunit_shop("casa")
    casa_plan.fund_ratio = 1
    assert casa_plan.kids == {}
    print(f"{type(casa_plan)=}")

    # WHEN
    # casa_dict = dataclasses_asdict(casa_plan)
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    assert set(casa_dict.keys()) == {
        kw.plan_label,
        kw.parent_rope,
        kw.kids,
        kw.star,
        kw.plan_uid,
        kw.awardunits,
        kw.reasonunits,
        kw.workforceunit,
        kw.factunits,
        kw.healerunit,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
        kw.gogo_want,
        kw.stop_want,
        kw.pledge,
        kw.problem_bool,
        kw.knot,
        kw.is_expanded,
        kw.plan_active,
        kw.plan_active_hx,
        kw.all_contact_cred,
        kw.all_contact_debt,
        kw.awardheirs,
        kw.awardlines,
        kw.descendant_pledge_count,
        kw.factheirs,
        kw.fund_ratio,
        kw.fund_grain,
        kw.fund_onset,
        kw.fund_cease,
        kw.healerunit_ratio,
        kw.tree_level,
        kw.range_evaluated,
        kw.reasonheirs,
        kw.plan_task,
        kw.workforceheir,
        kw.gogo_calc,
        kw.stop_calc,
        kw.plan_fund_total,
    }
    assert casa_dict.get(kw.healerunit) == {"healer_names": []}


def test_get_plan_view_dict_ReturnsObj_Scenario1_workforceunit():
    # ESTABLISH
    sue_person = get_sue_person_with_facts_and_reasons()
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, "clean")
    mop_rope = sue_person.make_rope(clean_rope, "mop")
    mop_plan = sue_person.get_plan_obj(mop_rope)

    # WHEN
    mop_dict = get_plan_view_dict(mop_plan)

    # THEN
    # workforceunit
    mop_workforce_dict = mop_dict.get(kw.workforceunit)
    mop_labors_dict = mop_workforce_dict.get(kw.labors)
    mop_sue_dict = mop_labors_dict.get(exx.sue)
    mop_bob_dict = mop_labors_dict.get(exx.bob)
    mop_sue_unit_readable = mop_sue_dict.get(kw.readable)
    mop_bob_unit_readable = mop_bob_dict.get(kw.readable)
    expected_mop_sue_unit_readable = add_small_dot(f"WorkforceUnit: {exx.sue}")
    expected_mop_bob_unit_readable = add_small_dot(
        f"WorkforceUnit: {exx.bob} Solo: True"
    )
    assert mop_sue_unit_readable == expected_mop_sue_unit_readable
    assert mop_bob_unit_readable == expected_mop_bob_unit_readable
    print(f"{mop_workforce_dict=}")
    print(f"{mop_sue_dict=}")
    print(f"{mop_bob_dict=}")

    # workforceheir
    mop_workforce_dict = mop_dict.get(kw.workforceheir)
    mop_labors_dict = mop_workforce_dict.get(kw.labors)
    mop_sue_dict = mop_labors_dict.get(exx.sue)
    mop_bob_dict = mop_labors_dict.get(exx.bob)
    mop_sue_heir_readable = mop_sue_dict.get(kw.readable)
    mop_bob_heir_readable = mop_bob_dict.get(kw.readable)
    expected_mop_sue_heir_readable = add_small_dot(f"WorkforceHeir: {exx.sue}")
    expected_mop_bob_heir_readable = add_small_dot(
        f"WorkforceHeir: {exx.bob} Solo: True"
    )
    assert mop_sue_heir_readable == expected_mop_sue_heir_readable
    assert mop_bob_heir_readable == expected_mop_bob_heir_readable
    print(f"{mop_workforce_dict=}")
    print(f"{mop_sue_dict=}")
    print(f"{mop_bob_dict=}")


def test_get_plan_view_dict_ReturnsObj_Scenario2_PlanRootUnit_attrs():
    # ESTABLISH
    sue_personunit = get_sue_personunit()

    # WHEN
    root_plan_view_dict = get_plan_view_dict(sue_personunit.planroot)

    # THEN
    # for dict_key, value in casa_dict.items():
    #     print(f"{dict_key=} \t\t {value=}")
    # expected_workforceunit_dict = {
    #     kw.labors: {exx.sue: {kw.labor_title: exx.sue, "solo": False}}
    # }
    expected_parent_rope = add_small_dot("Root Plan parent_rope is empty str")
    assert root_plan_view_dict.get(kw.parent_rope) == expected_parent_rope


def test_get_plan_view_dict_ReturnsObj_Scenario3_PlanUnit_base_attrs():
    # ESTABLISH
    sue_personunit = get_sue_personunit()
    casa_rope = sue_personunit.make_l1_rope("casa")
    casa_plan = sue_personunit.get_plan_obj(casa_rope)

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    assert casa_dict.get(kw.plan_fund_total) > 0
    expected_parent_rope = add_small_dot(casa_plan.parent_rope)
    assert casa_dict.get(kw.parent_rope) == expected_parent_rope
    expected_all_contact_cred = f"all_contact_cred = {casa_plan.all_contact_cred}"
    expected_all_contact_debt = f"all_contact_debt = {casa_plan.all_contact_debt}"
    expected_all_contact_cred = add_small_dot(expected_all_contact_cred)
    expected_all_contact_debt = add_small_dot(expected_all_contact_debt)
    assert casa_dict.get(kw.all_contact_cred) == expected_all_contact_cred
    assert casa_dict.get(kw.all_contact_debt) == expected_all_contact_debt
    assert casa_dict.get(kw.fund_ratio) == "38%"


def test_get_plan_view_dict_ReturnsObj_Scenario4_PlanUnit_AwardUnits():
    # ESTABLISH
    sue_personunit = get_sue_personunit()
    casa_rope = sue_personunit.make_l1_rope("casa")
    casa_plan = sue_personunit.get_plan_obj(casa_rope)

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    # awardunits
    awardunits_dict = casa_dict.get(kw.awardunits)
    assert len(awardunits_dict) == 2
    # print(f"{len(awardunits_dict)=}")
    sue_awardunit_dict = awardunits_dict.get(exx.sue)
    bob_awardunit_dict = awardunits_dict.get(exx.bob)
    expected_sue_readable = add_small_dot(f"{exx.sue}: Take 0.8, Give 1")
    expected_bob_readable = add_small_dot(f"{exx.bob}: Take 0.9, Give 0.7")
    # print(f"{sue_awardunit_dict.get(kw.readable)=}")
    # print(f"{bob_awardunit_dict.get(kw.readable)=}")
    assert sue_awardunit_dict.get(kw.readable) == expected_sue_readable
    assert bob_awardunit_dict.get(kw.readable) == expected_bob_readable

    # awardheirs
    awardheirs_dict = casa_dict.get(kw.awardheirs)
    assert len(awardheirs_dict) == 4
    # print(f"{len(awardheirs_dict)=}")
    sue_awardheir_dict = awardheirs_dict.get(exx.sue)
    bob_awardheir_dict = awardheirs_dict.get(exx.bob)
    expected_sue_readable = f"{exx.sue}: Take 0.8 (150000000), Give 1 (150000000)"
    expected_bob_readable = f"{exx.bob}: Take 0.9 (168750000), Give 0.7 (105000000)"
    # print(f"{sue_awardheir_dict.get(kw.readable)=}")
    # print(f"{bob_awardheir_dict.get(kw.readable)=}")
    assert sue_awardheir_dict.get(kw.readable) == add_small_dot(expected_sue_readable)
    assert bob_awardheir_dict.get(kw.readable) == add_small_dot(expected_bob_readable)

    # awardlines
    awardlines_dict = casa_dict.get(kw.awardlines)
    assert len(awardlines_dict) == 4
    print(f"{len(awardlines_dict)=}")
    sue_awardline_dict = awardlines_dict.get(exx.sue)
    bob_awardline_dict = awardlines_dict.get(exx.bob)
    expected_sue_readable = f"{exx.sue}: take_fund (150000000), give_fund (150000000)"
    expected_bob_readable = f"{exx.bob}: take_fund (168750000), give_fund (105000000)"
    print(f"{sue_awardline_dict.get(kw.readable)=}")
    print(f"{bob_awardline_dict.get(kw.readable)=}")
    assert sue_awardline_dict.get(kw.readable) == add_small_dot(expected_sue_readable)
    assert bob_awardline_dict.get(kw.readable) == add_small_dot(expected_bob_readable)


def test_get_plan_view_dict_ReturnsObj_Scenario5_PlanUnit_FactUnit():
    # ESTABLISH
    sue_person = get_sue_person_with_facts_and_reasons()

    # WHEN
    root_dict = get_plan_view_dict(sue_person.planroot)

    # THEN
    # sports ropes
    sports_rope = sue_person.make_l1_rope("sports")
    best_sport_str = "best sport"
    best_rope = sue_person.make_rope(sports_rope, best_sport_str)

    # casa ropes
    casa_rope = sue_person.make_l1_rope("casa")
    tidi_rope = sue_person.make_rope(casa_rope, "tidiness")

    # factunits
    root_factunits_dict = root_dict.get(kw.factunits)
    assert len(root_factunits_dict) == 2
    # print(f"{len(factunits_dict)=}")
    tidi_factunit_dict = root_factunits_dict.get(tidi_rope)
    best_factunit_dict = root_factunits_dict.get(best_rope)
    # print(f"{tidi_factunit_dict=}")
    # print(f"{best_factunit_dict=}")
    tidi_factunit = sue_person.get_fact(tidi_rope)
    best_factunit = sue_person.get_fact(best_rope)
    tidi_factunit_readable = get_fact_state_readable_str(
        tidi_factunit, None, sue_person
    )
    best_factunit_readable = get_fact_state_readable_str(
        best_factunit, None, sue_person
    )
    expected_tidi_factunit_str = add_small_dot(tidi_factunit_readable)
    expected_best_factunit_str = add_small_dot(best_factunit_readable)
    # print(f"{expected_tidi_factunit_str=}")
    # print(f"{expected_best_factunit_str=}")
    assert tidi_factunit_dict.get(kw.readable) == expected_tidi_factunit_str
    assert best_factunit_dict.get(kw.readable) == expected_best_factunit_str

    # factheirs
    casa_factheirs_dict = root_dict.get("factheirs")
    assert len(casa_factheirs_dict) == 2
    print(f"{len(casa_factheirs_dict)=}")
    casa_tidi_factheir_dict = casa_factheirs_dict.get(tidi_rope)
    casa_best_factheir_dict = casa_factheirs_dict.get(best_rope)
    print(f"{casa_tidi_factheir_dict=}")
    print(f"{casa_best_factheir_dict=}")
    casa_plan = sue_person.get_plan_obj(casa_rope)
    tidi_factheir = casa_plan.factheirs.get(tidi_rope)
    best_factheir = casa_plan.factheirs.get(best_rope)
    casa_tidi_factheir_readable = get_fact_state_readable_str(
        tidi_factheir, None, sue_person
    )
    casa_best_factheir_readable = get_fact_state_readable_str(
        best_factheir, None, sue_person
    )
    expected_casa_tidi_factheir_str = add_small_dot(casa_tidi_factheir_readable)
    expected_casa_best_factheir_str = add_small_dot(casa_best_factheir_readable)
    assert casa_tidi_factheir_dict.get(kw.readable) == expected_casa_tidi_factheir_str
    assert casa_best_factheir_dict.get(kw.readable) == expected_casa_best_factheir_str


def test_get_plan_view_dict_ReturnsObj_Scenario6_PlanUnit_ReasonUnit():
    # ESTABLISH
    sue_person = get_sue_person_with_facts_and_reasons()
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, "clean")
    mop_rope = sue_person.make_rope(clean_rope, "mop")
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    tidi_rope = sue_person.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_person.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_person.make_rope(tidi_rope, "tidy")
    sports_rope = sue_person.make_l1_rope("sports")
    best_rope = sue_person.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_person.make_rope(best_rope, best_soccer_str())
    best_bowl_rope = sue_person.make_rope(best_rope, best_bowl_str())
    best_run_rope = sue_person.make_rope(best_rope, best_run_str())
    play_rope = sue_person.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_person.make_rope(play_rope, play_soccer_str())
    play_bowl_rope = sue_person.make_rope(play_rope, play_bowl_str())
    play_run_rope = sue_person.make_rope(play_rope, play_run_str())
    play_soccer_plan = sue_person.get_plan_obj(play_soccer_rope)

    # WHEN
    play_soccer_dict = get_plan_view_dict(play_soccer_plan)

    # THEN
    # reasonunits
    play_soccer_reasonunits_dict = play_soccer_dict.get(kw.reasonunits)
    print(f"{play_soccer_reasonunits_dict.keys()=}")
    assert len(play_soccer_reasonunits_dict) == 2
    # print(f"{len(play_soccer_reasonunits_dict)=}")
    best_reasonunit_dict = play_soccer_reasonunits_dict.get(best_rope)
    tidi_reasonunit_dict = play_soccer_reasonunits_dict.get(tidi_rope)
    print(f"{best_reasonunit_dict.keys()=}")
    expected_reason_str = add_small_dot(f"ReasonUnit: context is {best_rope}")
    assert best_reasonunit_dict.get(kw.readable) == expected_reason_str

    best_cases_dict = best_reasonunit_dict.get(kw.cases)
    tidi_cases_dict = tidi_reasonunit_dict.get(kw.cases)
    best_soccer_case_dict = best_cases_dict.get(best_soccer_rope)
    best_run_case_dict = best_cases_dict.get(best_run_rope)
    tidy_case_dict = tidi_cases_dict.get(tidy_rope)
    # print(f"{best_soccer_case_dict.get(kw.reason_state)=}")
    # print(f"{best_run_case_dict.get(kw.reason_state)=}")
    # print(f"{tidy_case_dict.get(kw.reason_state)=}")
    assert best_soccer_case_dict.get(kw.reason_state) == best_soccer_rope
    assert best_run_case_dict.get(kw.reason_state) == best_run_rope
    assert tidy_case_dict.get(kw.reason_state) == tidy_rope

    play_best_reasonunit = play_soccer_plan.get_reasonunit(best_rope)
    play_tidi_reasonunit = play_soccer_plan.get_reasonunit(tidi_rope)
    # print(f"{play_best_reasonunit.cases.keys()=}")
    # print(f"{play_tidi_reasonunit.cases.keys()=}")
    best_soccer_caseunit = play_best_reasonunit.get_case(best_soccer_rope)
    best_run_caseunit = play_best_reasonunit.get_case(best_run_rope)
    tidy_caseunit = play_tidi_reasonunit.get_case(tidy_rope)
    expected_soccer_case_readable = get_reason_case_readable_str(
        best_rope, best_soccer_caseunit, None, sue_person
    )
    expected_run_case_readable = get_reason_case_readable_str(
        best_rope, best_run_caseunit, None, sue_person
    )
    expected_tidy_case_readable = get_reason_case_readable_str(
        tidi_rope, tidy_caseunit, None, sue_person
    )
    expected_soccer_case_readable = f"  {add_small_dot(expected_soccer_case_readable)}"
    expected_run_case_readable = f"  {add_small_dot(expected_run_case_readable)}"
    expected_tidy_case_readable = f"  {add_small_dot(expected_tidy_case_readable)}"
    print(f"{best_run_caseunit=}")
    # print(f"{expected_best_reasonunit_str=}")
    print(f"{best_soccer_case_dict.get(kw.readable)=}")
    print(f"{best_soccer_case_dict.get(kw.readable)=}")
    assert best_soccer_case_dict.get(kw.readable) == expected_soccer_case_readable
    assert best_run_case_dict.get(kw.readable) == expected_run_case_readable
    assert tidy_case_dict.get(kw.readable) == expected_tidy_case_readable
    print(f"{expected_soccer_case_readable=}")
    print(f"{expected_run_case_readable=}")
    print(f"{expected_tidy_case_readable=}")


def test_get_plan_view_dict_ReturnsObj_Scenario7_PlanUnit_ReasonHeirs():
    # ESTABLISH
    sue_person = get_sue_person_with_facts_and_reasons()
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, "clean")
    mop_rope = sue_person.make_rope(clean_rope, "mop")
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    tidi_rope = sue_person.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_person.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_person.make_rope(tidi_rope, "tidy")
    sports_rope = sue_person.make_l1_rope("sports")
    best_rope = sue_person.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_person.make_rope(best_rope, best_soccer_str())
    best_bowl_rope = sue_person.make_rope(best_rope, best_bowl_str())
    best_run_rope = sue_person.make_rope(best_rope, best_run_str())
    play_rope = sue_person.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_person.make_rope(play_rope, play_soccer_str())
    play_bowl_rope = sue_person.make_rope(play_rope, play_bowl_str())
    play_run_rope = sue_person.make_rope(play_rope, play_run_str())
    play_soccer_plan = sue_person.get_plan_obj(play_soccer_rope)

    # WHEN
    play_soccer_dict = get_plan_view_dict(play_soccer_plan)

    # THEN
    # reasonheirs
    play_soccer_reasonheirs_dict = play_soccer_dict.get(kw.reasonheirs)
    assert len(play_soccer_reasonheirs_dict) == 2
    # print(f"{len(play_soccer_reasonheirs_dict)=}")
    best_reasonheir_dict = play_soccer_reasonheirs_dict.get(best_rope)
    tidi_reasonheir_dict = play_soccer_reasonheirs_dict.get(tidi_rope)
    print(f"{best_reasonheir_dict.keys()=}")
    expected_reason_str = add_small_dot(f"ReasonHeir: context is {best_rope}")
    assert best_reasonheir_dict.get(kw.readable) == expected_reason_str

    best_cases_dict = best_reasonheir_dict.get(kw.cases)
    tidi_cases_dict = tidi_reasonheir_dict.get(kw.cases)
    best_soccer_case_dict = best_cases_dict.get(best_soccer_rope)
    best_run_case_dict = best_cases_dict.get(best_run_rope)
    tidy_case_dict = tidi_cases_dict.get(tidy_rope)
    # print(f"{best_soccer_case_dict.get(kw.reason_state)=}")
    # print(f"{best_run_case_dict.get(kw.reason_state)=}")
    # print(f"{tidy_case_dict.get(kw.reason_state)=}")
    assert best_soccer_case_dict.get(kw.reason_state) == best_soccer_rope
    assert best_run_case_dict.get(kw.reason_state) == best_run_rope
    assert tidy_case_dict.get(kw.reason_state) == tidy_rope

    play_best_reasonheir = play_soccer_plan.get_reasonheir(best_rope)
    play_tidi_reasonheir = play_soccer_plan.get_reasonheir(tidi_rope)
    # print(f"{play_best_reasonheir.cases.keys()=}")
    # print(f"{play_tidi_reasonheir.cases.keys()=}")
    best_soccer_caseunit = play_best_reasonheir.get_case(best_soccer_rope)
    best_run_caseunit = play_best_reasonheir.get_case(best_run_rope)
    tidy_caseunit = play_tidi_reasonheir.get_case(tidy_rope)
    expected_soccer_case_readable = get_reason_case_readable_str(
        best_rope, best_soccer_caseunit, None, sue_person
    )
    expected_run_case_readable = get_reason_case_readable_str(
        best_rope, best_run_caseunit, None, sue_person
    )
    expected_tidy_case_readable = get_reason_case_readable_str(
        tidi_rope, tidy_caseunit, None, sue_person
    )
    expected_soccer_case_readable = f"  {add_small_dot(expected_soccer_case_readable)}"
    expected_run_case_readable = f"  {add_small_dot(expected_run_case_readable)}"
    expected_tidy_case_readable = f"  {add_small_dot(expected_tidy_case_readable)}"
    print(f"{best_run_caseunit=}")
    # print(f"{expected_best_reasonheir_str=}")
    print(f"{best_soccer_case_dict.get(kw.readable)=}")
    print(f"{best_soccer_case_dict.get(kw.readable)=}")
    assert best_soccer_case_dict.get(kw.readable) == expected_soccer_case_readable
    assert best_run_case_dict.get(kw.readable) == expected_run_case_readable
    assert tidy_case_dict.get(kw.readable) == expected_tidy_case_readable
    print(f"{expected_soccer_case_readable=}")
    print(f"{expected_run_case_readable=}")
    print(f"{expected_tidy_case_readable=}")


def test_get_plan_view_dict_ReturnsObj_Scenario8_gogo_stop():
    # ESTABLISH
    casa_plan = planunit_shop(exx.casa)
    casa_gogo_want = 13
    casa_stop_want = 17
    casa_gogo_calc = 53
    casa_stop_calc = 57
    casa_plan.gogo_want = casa_gogo_want
    casa_plan.stop_want = casa_stop_want
    casa_plan.gogo_calc = casa_gogo_calc
    casa_plan.stop_calc = casa_stop_calc
    casa_plan.fund_ratio = 0

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    gogo_want_readable = casa_dict.get(kw.gogo_want)
    stop_want_readable = casa_dict.get(kw.stop_want)
    gogo_calc_readable = casa_dict.get(kw.gogo_calc)
    stop_calc_readable = casa_dict.get(kw.stop_calc)
    expected_gogo_want_readable = add_small_dot(f"gogo_want: {casa_plan.gogo_want}")
    expected_stop_want_readable = add_small_dot(f"stop_want: {casa_plan.stop_want}")
    expected_gogo_calc_readable = add_small_dot(f"gogo_calc: {casa_plan.gogo_calc}")
    expected_stop_calc_readable = add_small_dot(f"stop_calc: {casa_plan.stop_calc}")
    assert gogo_want_readable == expected_gogo_want_readable
    assert stop_want_readable == expected_stop_want_readable
    assert gogo_calc_readable == expected_gogo_calc_readable
    assert stop_calc_readable == expected_stop_calc_readable


def test_get_plan_view_dict_ReturnsObj_Scenario9_numeric_range_attrs():
    # ESTABLISH
    casa_plan = planunit_shop(exx.casa)
    casa_addin = 11
    casa_begin = 17
    casa_close = 23
    casa_denom = 29
    casa_morph = 37
    casa_numor = 43
    casa_plan.addin = casa_addin
    casa_plan.begin = casa_begin
    casa_plan.close = casa_close
    casa_plan.denom = casa_denom
    casa_plan.morph = casa_morph
    casa_plan.numor = casa_numor
    casa_plan.fund_ratio = 0

    # WHEN
    casa_dict = get_plan_view_dict(casa_plan)

    # THEN
    casa_addin_readable = casa_dict.get(kw.addin)
    casa_begin_readable = casa_dict.get(kw.begin)
    casa_close_readable = casa_dict.get(kw.close)
    casa_denom_readable = casa_dict.get(kw.denom)
    casa_morph_readable = casa_dict.get(kw.morph)
    casa_numor_readable = casa_dict.get(kw.numor)
    expected_casa_addin_readable = add_small_dot(f"addin: {casa_plan.addin}")
    expected_casa_begin_readable = add_small_dot(f"begin: {casa_plan.begin}")
    expected_casa_close_readable = add_small_dot(f"close: {casa_plan.close}")
    expected_casa_denom_readable = add_small_dot(f"denom: {casa_plan.denom}")
    expected_casa_morph_readable = add_small_dot(f"morph: {casa_plan.morph}")
    expected_casa_numor_readable = add_small_dot(f"numor: {casa_plan.numor}")
    assert casa_addin_readable == expected_casa_addin_readable
    assert casa_begin_readable == expected_casa_begin_readable
    assert casa_close_readable == expected_casa_close_readable
    assert casa_denom_readable == expected_casa_denom_readable
    assert casa_morph_readable == expected_casa_morph_readable
    assert casa_numor_readable == expected_casa_numor_readable


def test_get_plan_view_dict_ReturnsObj_Scenario10_active_hx():
    # ESTABLISH
    hatter_person = get_personunit_irrational_example()
    hatter_person.set_max_tree_traverse(8)
    hatter_person.conpute()
    egg_str = "egg first"
    egg_rope = hatter_person.make_l1_rope(egg_str)
    chicken_str = "chicken first"
    chicken_rope = hatter_person.make_l1_rope(chicken_str)
    chicken_plan = hatter_person.get_plan_obj(chicken_rope)

    # WHEN
    chicken_dict = get_plan_view_dict(chicken_plan)

    # THEN
    print(f"{chicken_plan.plan_active_hx=}")
    # sports ropes
    chicken_active_hx_str = chicken_dict.get(kw.plan_active_hx)
    expected_chicken_active_hx_str = f"plan_active_hx: {chicken_plan.plan_active_hx}"
    expected_chicken_active_hx_str = add_small_dot(expected_chicken_active_hx_str)
    assert expected_chicken_active_hx_str == chicken_active_hx_str
