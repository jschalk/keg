from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch10_person_listen.listen_main import (
    _allocate_irrational_partner_debt_lumen,
    generate_ingest_list,
    generate_perspective_agenda,
)
from src.ref.keywords import ExampleStrs as exx


def test_allocate_irrational_partner_debt_lumen_SetsPersonAttr():
    # ESTABLISH
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    yao_person = personunit_shop(exx.yao)
    yao_person.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    zia_partnerunit = yao_person.get_partner(exx.zia)
    assert zia_partnerunit.irrational_partner_debt_lumen == 0

    # WHEN
    _allocate_irrational_partner_debt_lumen(yao_person, exx.zia)

    # THEN
    assert zia_partnerunit.irrational_partner_debt_lumen == zia_partner_debt_lumen


def test_generate_perspective_agenda_GrabsAgendacase_tasks():
    # ESTABLISH
    yao_speaker = personunit_shop(exx.yao)
    yao_speaker.add_partnerunit(exx.yao)
    yao_speaker.set_partner_respect(20)
    casa_rope = yao_speaker.make_l1_rope(exx.casa)
    situation_str = "situation"
    situation_rope = yao_speaker.make_rope(casa_rope, situation_str)
    clean_rope = yao_speaker.make_rope(situation_rope, exx.clean)
    dirty_str = "dirty"
    dirty_rope = yao_speaker.make_rope(situation_rope, dirty_str)

    sweep_rope = yao_speaker.make_rope(casa_rope, exx.sweep)
    yao_speaker.set_plan_obj(planunit_shop(exx.clean), situation_rope)
    yao_speaker.set_plan_obj(planunit_shop(dirty_str), situation_rope)
    yao_speaker.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope)
    yao_speaker.edit_plan_attr(
        sweep_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    yao_speaker.add_fact(situation_rope, clean_rope)
    assert len(yao_speaker.get_agenda_dict()) == 0

    # WHEN
    agenda_list = generate_perspective_agenda(yao_speaker)

    # THEN
    assert len(agenda_list) == 1


def test_generate_ingest_list_ReturnsList_v1():
    # ESTABLISH
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.set_l1_plan(planunit_shop(exx.clean, pledge=True))
    zia_debtor_pool = 78
    zia_resepect_bit = 2
    assert len(zia_personunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_personunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_personunit.make_l1_rope(exx.clean)
    clean_rope = zia_personunit.make_l1_rope(exx.clean)
    clean_planunit = zia_personunit.get_plan_obj(clean_rope)
    assert ingested_list[0] == clean_planunit
    assert ingested_list[0].star == zia_debtor_pool


def test_generate_ingest_list_ReturnsList_v2():
    # ESTABLISH
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.set_l1_plan(planunit_shop(exx.clean, pledge=True))
    zia_personunit.set_l1_plan(planunit_shop(exx.cuisine, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_personunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_personunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_personunit.make_l1_rope(exx.clean)
    assert len(ingested_list) == 2
    clean_rope = zia_personunit.make_l1_rope(exx.clean)
    cuisine_rope = zia_personunit.make_l1_rope(exx.cuisine)
    clean_planunit = zia_personunit.get_plan_obj(clean_rope)
    cuisine_planunit = zia_personunit.get_plan_obj(cuisine_rope)
    assert ingested_list[0] == cuisine_planunit
    assert ingested_list[0].star == 16.0
    assert ingested_list == [cuisine_planunit, clean_planunit]


def test_generate_ingest_list_ReturnsList_v3():
    # ESTABLISH
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.set_l1_plan(planunit_shop(exx.clean, pledge=True))
    zia_personunit.set_l1_plan(planunit_shop(exx.cuisine, star=3, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_personunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_personunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_personunit.make_l1_rope(exx.clean)
    cuisine_rope = zia_personunit.make_l1_rope(exx.cuisine)
    clean_planunit = zia_personunit.get_plan_obj(clean_rope)
    cuisine_planunit = zia_personunit.get_plan_obj(cuisine_rope)
    assert ingested_list == [cuisine_planunit, clean_planunit]
    assert ingested_list[0].star == 24.0
    assert ingested_list[1].star == 8.0


def test_generate_ingest_list_ReturnsList_v4():
    # ESTABLISH
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.set_l1_plan(planunit_shop(exx.clean, pledge=True))
    zia_personunit.set_l1_plan(planunit_shop(exx.cuisine, star=2, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_personunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_personunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_personunit.make_l1_rope(exx.clean)
    cuisine_rope = zia_personunit.make_l1_rope(exx.cuisine)
    clean_planunit = zia_personunit.get_plan_obj(clean_rope)
    cuisine_planunit = zia_personunit.get_plan_obj(cuisine_rope)
    assert ingested_list[0].star == 22
    assert ingested_list[1].star == 10
    assert ingested_list == [cuisine_planunit, clean_planunit]
