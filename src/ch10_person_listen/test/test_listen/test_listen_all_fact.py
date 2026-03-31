from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch10_person_listen.listen_main import (
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_fact,
    migrate_all_facts,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_debtors_roll_ReturnsObj():
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.conpute()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_partnerunit = yao_duty.get_partner(exx.zia)
    assert yao_roll == [zia_partnerunit]


def test_get_debtors_roll_ReturnsObjIgnoresZero_partner_debt_lumen():
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    wei_str = "Wei"
    wei_partner_cred_lumen = 67
    wei_partner_debt_lumen = 0
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.add_partnerunit(wei_str, wei_partner_cred_lumen, wei_partner_debt_lumen)
    yao_duty.conpute()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_partnerunit = yao_duty.get_partner(exx.zia)
    assert yao_roll == [zia_partnerunit]


def test_get_ordered_debtors_roll_ReturnsObj_InOrder():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    sue_partner_cred_lumen = 57
    sue_partner_debt_lumen = 51
    yao_person.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_person.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_person.set_partner_respect(yao_pool)

    # WHEN
    ordered_partners1 = get_ordered_debtors_roll(yao_person)

    # THEN
    zia_partner = yao_person.get_partner(exx.zia)
    sue_partner = yao_person.get_partner(exx.sue)
    assert ordered_partners1[0].to_dict() == sue_partner.to_dict()
    assert ordered_partners1 == [sue_partner, zia_partner]

    # ESTABLISH
    bob_partner_debt_lumen = 75
    yao_person.add_partnerunit(exx.bob, 0, bob_partner_debt_lumen)
    bob_partner = yao_person.get_partner(exx.bob)

    # WHEN
    ordered_partners2 = get_ordered_debtors_roll(yao_person)

    # THEN
    assert ordered_partners2[0].to_dict() == bob_partner.to_dict()
    assert ordered_partners2 == [bob_partner, sue_partner, zia_partner]


def test_get_ordered_debtors_roll_DoesNotReturnZero_partner_debt_lumen():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    zia_partner_debt_lumen = 41
    sue_partner_debt_lumen = 51
    yao_pool = 92
    yao_person.set_partner_respect(yao_pool)
    bob_partner_debt_lumen = 75
    yao_person.add_partnerunit(exx.zia, 0, zia_partner_debt_lumen)
    yao_person.add_partnerunit(exx.sue, 0, sue_partner_debt_lumen)
    yao_person.add_partnerunit(exx.bob, 0, bob_partner_debt_lumen)
    yao_person.add_partnerunit(exx.yao, 0, 0)
    yao_person.add_partnerunit(exx.xio, 0, 0)

    # WHEN
    ordered_partners2 = get_ordered_debtors_roll(yao_person)

    # THEN
    assert len(ordered_partners2) == 3
    zia_partner = yao_person.get_partner(exx.zia)
    sue_partner = yao_person.get_partner(exx.sue)
    bob_partner = yao_person.get_partner(exx.bob)
    assert ordered_partners2[0].to_dict() == bob_partner.to_dict()
    assert ordered_partners2 == [bob_partner, sue_partner, zia_partner]


def test_set_listen_to_speaker_fact_SetsFact():
    # ESTABLISH
    yao_listener = personunit_shop(exx.yao)
    casa_rope = yao_listener.make_l1_rope(exx.casa)
    situation_str = "situation"
    situation_rope = yao_listener.make_rope(casa_rope, situation_str)
    clean_rope = yao_listener.make_rope(situation_rope, exx.clean)
    dirty_str = "dirty"
    dirty_rope = yao_listener.make_rope(situation_rope, dirty_str)

    sweep_rope = yao_listener.make_rope(casa_rope, exx.sweep)

    yao_listener.add_partnerunit(exx.yao)
    yao_listener.set_partner_respect(20)
    yao_listener.set_plan_obj(planunit_shop(exx.clean), situation_rope)
    yao_listener.set_plan_obj(planunit_shop(dirty_str), situation_rope)
    yao_listener.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope)
    yao_listener.edit_plan_attr(
        sweep_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    missing_fact_fact_contexts = list(
        yao_listener.get_missing_fact_reason_contexts().keys()
    )

    yao_speaker = personunit_shop(exx.yao)
    yao_speaker.add_fact(situation_rope, clean_rope, create_missing_plans=True)
    assert yao_listener.get_missing_fact_reason_contexts().keys() == {situation_rope}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fact_contexts)

    # THEN
    assert len(yao_listener.get_missing_fact_reason_contexts().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # ESTABLISH
    yao_listener = personunit_shop(exx.yao)
    yao_listener.add_partnerunit(exx.yao)
    yao_listener.set_partner_respect(20)
    casa_rope = yao_listener.make_l1_rope(exx.casa)
    situation_str = "situation"
    situation_rope = yao_listener.make_rope(casa_rope, situation_str)
    clean_rope = yao_listener.make_rope(situation_rope, exx.clean)
    dirty_str = "dirty"
    dirty_rope = yao_listener.make_rope(situation_rope, dirty_str)

    sweep_rope = yao_listener.make_rope(casa_rope, exx.sweep)
    fridge_str = "fridge"
    fridge_rope = yao_listener.make_rope(casa_rope, fridge_str)
    running_str = "running"
    running_rope = yao_listener.make_rope(fridge_rope, running_str)

    yao_listener.set_plan_obj(planunit_shop(running_str), fridge_rope)
    yao_listener.set_plan_obj(planunit_shop(exx.clean), situation_rope)
    yao_listener.set_plan_obj(planunit_shop(dirty_str), situation_rope)
    yao_listener.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope)
    yao_listener.edit_plan_attr(
        sweep_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    yao_listener.edit_plan_attr(
        sweep_rope, reason_context=fridge_rope, reason_case=running_rope
    )
    assert len(yao_listener.get_missing_fact_reason_contexts()) == 2
    yao_listener.add_fact(situation_rope, dirty_rope)
    assert len(yao_listener.get_missing_fact_reason_contexts()) == 1
    assert yao_listener.get_fact(situation_rope).fact_state == dirty_rope

    # WHEN
    yao_speaker = personunit_shop(exx.yao)
    yao_speaker.add_fact(situation_rope, clean_rope, create_missing_plans=True)
    yao_speaker.add_fact(fridge_rope, running_rope, create_missing_plans=True)
    missing_fact_fact_contexts = list(
        yao_listener.get_missing_fact_reason_contexts().keys()
    )
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fact_contexts)

    # THEN
    assert len(yao_listener.get_missing_fact_reason_contexts()) == 0
    # did not grab speaker's factunit
    assert yao_listener.get_fact(situation_rope).fact_state == dirty_rope
    # grabed speaker's factunit
    assert yao_listener.get_fact(fridge_rope).fact_state == running_rope


def test_migrate_all_facts_AddsPlanUnitsAndSetsFactUnits():
    # ESTABLISH
    yao_src = personunit_shop(exx.yao)
    casa_rope = yao_src.make_l1_rope(exx.casa)
    situation_str = "situation"
    situation_rope = yao_src.make_rope(casa_rope, situation_str)
    clean_rope = yao_src.make_rope(situation_rope, exx.clean)
    dirty_str = "dirty"
    dirty_rope = yao_src.make_rope(situation_rope, dirty_str)

    sweep_rope = yao_src.make_rope(casa_rope, exx.sweep)
    weather_str = "weather"
    weather_rope = yao_src.make_l1_rope(weather_str)
    rain_str = "raining"
    rain_rope = yao_src.make_rope(weather_rope, rain_str)
    snow_str = "snow"
    snow_rope = yao_src.make_rope(weather_rope, snow_str)

    yao_src.add_partnerunit(exx.yao)
    yao_src.set_partner_respect(20)
    yao_src.set_plan_obj(planunit_shop(exx.clean), situation_rope)
    yao_src.set_plan_obj(planunit_shop(dirty_str), situation_rope)
    yao_src.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope)
    yao_src.edit_reason(sweep_rope, situation_rope, dirty_rope)
    # missing_fact_fact_contexts = list(yao_src.get_missing_fact_reason_contexts().keys())
    yao_src.set_plan_obj(planunit_shop(rain_str), weather_rope)
    yao_src.set_plan_obj(planunit_shop(snow_str), weather_rope)
    yao_src.add_fact(weather_rope, rain_rope)
    yao_src.add_fact(situation_rope, clean_rope)
    yao_src.conpute()

    yao_dst = personunit_shop(exx.yao)
    assert yao_dst.plan_exists(clean_rope) is False
    assert yao_dst.plan_exists(dirty_rope) is False
    assert yao_dst.plan_exists(rain_rope) is False
    assert yao_dst.plan_exists(snow_rope) is False
    assert yao_dst.get_fact(weather_rope) is None
    assert yao_dst.get_fact(situation_rope) is None

    # WHEN
    migrate_all_facts(yao_src, yao_dst)

    # THEN
    assert yao_dst.plan_exists(clean_rope)
    assert yao_dst.plan_exists(dirty_rope)
    assert yao_dst.plan_exists(rain_rope)
    assert yao_dst.plan_exists(snow_rope)
    assert yao_dst.get_fact(weather_rope) is not None
    assert yao_dst.get_fact(situation_rope) is not None
    assert yao_dst.get_fact(weather_rope).fact_state == rain_rope
    assert yao_dst.get_fact(situation_rope).fact_state == clean_rope
