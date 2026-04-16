from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch10_person_listen.keep_tool import save_duty_person, save_vision_person
from src.ch10_person_listen.listen_main import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
    listen_to_facts_duty_vision,
)
from src.ch10_person_listen.test._util.ch10_examples import (
    a23_casa_rope,
    a23_clean_rope,
    a23_eat_rope,
    a23_full_rope,
    a23_hungry_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    get_texas_lessonfilehandler,
    get_texas_rope,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_facts_duty_vision_SetsSingleFactUnit_v1(temp3_fs):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    zia_contact_cred_lumen = 47
    zia_contact_debt_lumen = 41
    zia_pool = 87
    yao_duty.add_contactunit(exx.zia, zia_contact_cred_lumen, zia_contact_debt_lumen)
    yao_duty.set_contact_respect(zia_pool)
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None
    listen_to_agendas_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )
    assert (
        new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope())
        is not None
    )

    # WHEN
    listen_to_facts_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    assert new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None


def test_listen_to_facts_duty_vision_SetsSingleFactUnitWithDifferentcase_task(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    yao_contact_cred_lumen = 47
    yao_contact_debt_lumen = 41
    yao_pool = 87
    yao_duty.add_contactunit(exx.zia, yao_contact_cred_lumen, yao_contact_debt_lumen)
    yao_duty.set_contact_respect(yao_pool)
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    zia_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    clean_planunit = zia_vision.get_plan_obj(a23_clean_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None
    listen_to_agendas_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )
    assert (
        new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope())
        is not None
    )
    assert new_yao_vision.get_fact(a23_eat_rope()) is None

    # WHEN
    listen_to_facts_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    assert new_yao_vision.get_fact(a23_eat_rope()) is not None


def test_listen_to_facts_duty_vision_GetsFactsFromSrcPersonSelfNotSpeakerSelf(
    temp3_fs,
):
    # ESTABLISH
    # yao_duty has fact a23_eat_rope = full
    # yao_vision has fact a23_eat_rope = hungry
    # new_yao_vision fact_states yao_duty fact a23_eat_rope = full
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(a23_eat_rope(), a23_full_rope())
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    assert yao_duty.get_fact(a23_eat_rope()).fact_state == a23_full_rope()

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        old_yao_vision,
    )

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(a23_eat_rope()) is None
    assert new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None
    listen_to_agendas_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )
    assert (
        new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope())
        is not None
    )

    # WHEN
    listen_to_facts_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    assert new_yao_vision.get_fact(a23_eat_rope()) is not None
    assert new_yao_vision.get_fact(a23_eat_rope()).fact_state == a23_full_rope()


def test_listen_to_facts_duty_vision_ConfirmNoFactfact_stateedFromPersonsSpeakerDirPerson_v1(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(a23_eat_rope())
    assert yao_duty.get_fact(a23_eat_rope()) is None
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(a23_eat_rope(), a23_eat_rope())
    assert zia_vision.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    old_yao_vision = get_example_yao_speaker()
    assert old_yao_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        old_yao_vision,
    )

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(a23_eat_rope()) is None
    assert new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None
    listen_to_agendas_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )
    print(f"{new_yao_vision.get_missing_fact_reason_contexts().keys()=}")
    print(f"{new_yao_vision.planroot.factunits.keys()=}")
    assert (
        new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope())
        is not None
    )

    # WHEN
    listen_to_facts_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    assert yao_duty.get_fact(a23_eat_rope()) is None
    assert zia_vision.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()
    assert old_yao_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    assert new_yao_vision.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()


def test_listen_to_facts_duty_vision_SetsPrioritizesSelfFactsOverSpeakers(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = get_example_yao_speaker()
    yao_duty.add_fact(a23_eat_rope(), a23_full_rope())
    assert yao_duty.get_fact(a23_eat_rope()).fact_state == a23_full_rope()
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(a23_eat_rope(), a23_hungry_rope())
    assert zia_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    new_yao_vision = create_listen_basis(yao_duty)
    assert new_yao_vision.get_fact(a23_eat_rope()) is None
    assert new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None
    listen_to_agendas_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )
    assert (
        new_yao_vision.get_missing_fact_reason_contexts().get(a23_eat_rope())
        is not None
    )

    # WHEN
    listen_to_facts_duty_vision(
        new_yao_vision, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    assert new_yao_vision.get_fact(a23_eat_rope()) is not None
    assert new_yao_vision.get_fact(a23_eat_rope()).fact_state == a23_full_rope()


def test_listen_to_facts_duty_vision_ConfirmNoFactfact_stateedFromPersonsSpeakerDirPerson_v2(
    temp3_fs,
):
    # ESTABLISH
    zia_vision = get_example_zia_speaker()
    zia_vision.add_fact(a23_eat_rope(), a23_eat_rope())
    assert zia_vision.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    bob_vision = get_example_bob_speaker()
    bob_str = bob_vision.person_name
    assert bob_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    save_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        bob_vision,
    )

    yao_duty = get_example_yao_speaker()
    yao_duty.del_fact(a23_eat_rope())
    assert yao_duty.get_fact(a23_eat_rope()) is None
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    new_yao_vision1 = create_listen_basis(yao_duty)
    assert new_yao_vision1.get_fact(a23_eat_rope()) is None
    assert (
        new_yao_vision1.get_missing_fact_reason_contexts().get(a23_eat_rope()) is None
    )
    listen_to_agendas_duty_vision(
        new_yao_vision1, sue_texas_lessonfilehandler, get_texas_rope()
    )
    print(f"{new_yao_vision1.get_missing_fact_reason_contexts().keys()=}")
    print(f"{new_yao_vision1.planroot.factunits.keys()=}")
    assert (
        new_yao_vision1.get_missing_fact_reason_contexts().get(a23_eat_rope())
        is not None
    )

    # WHEN
    listen_to_facts_duty_vision(
        new_yao_vision1, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    assert yao_duty.get_fact(a23_eat_rope()) is None
    zia_contactunit = new_yao_vision1.get_contact(exx.zia)
    bob_contactunit = new_yao_vision1.get_contact(bob_str)
    assert zia_contactunit.contact_debt_lumen < bob_contactunit.contact_debt_lumen
    assert bob_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    assert zia_vision.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()
    assert new_yao_vision1.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()

    # WHEN
    yao_zia_contact_debt_lumen = 15
    yao_bob_contact_debt_lumen = 5
    yao_duty.add_contactunit(exx.zia, None, yao_zia_contact_debt_lumen)
    yao_duty.add_contactunit(bob_str, None, yao_bob_contact_debt_lumen)
    yao_duty.set_contact_respect(100)
    new_yao_vision2 = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision2, sue_texas_lessonfilehandler, get_texas_rope()
    )
    listen_to_facts_duty_vision(
        new_yao_vision2, sue_texas_lessonfilehandler, get_texas_rope()
    )

    # THEN
    zia_contactunit = new_yao_vision2.get_contact(exx.zia)
    bob_contactunit = new_yao_vision2.get_contact(bob_str)
    assert zia_contactunit.contact_debt_lumen > bob_contactunit.contact_debt_lumen
    assert bob_vision.get_fact(a23_eat_rope()).fact_state == a23_hungry_rope()
    assert zia_vision.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()
    assert new_yao_vision2.get_fact(a23_eat_rope()).fact_state == a23_eat_rope()


# def test_listen_to_facts_duty_vision_SetsFact(temp3_fs):
#     # ESTABLISH
#     exx.yao = exx.yao
#     sue_speaker = personunit_shop(exx.yao)
#     casa_rope = sue_speaker.make_l1_rope(casa_str)
#     situation_str = "situation"
#     situation_rope = sue_speaker.make_rope(casa_rope, situation_str)
#     a23_clean_rope = sue_speaker.make_rope(situation_rope, exx.clean)
#     dirty_str = "dirty"
#     dirty_rope = sue_speaker.make_rope(situation_rope, dirty_str)
#
#     sweep_rope = sue_speaker.make_rope(casa_rope, exx.sweep)

#     sue_speaker.add_contactunit(exx.yao)
#     sue_speaker.set_contact_respect(20)
#     sue_speaker.set_plan_obj(planunit_shop(exx.clean), situation_rope)
#     sue_speaker.set_plan_obj(planunit_shop(dirty_str), situation_rope)
#     sue_speaker.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope)
#     sue_speaker.edit_plan_attr(
#         sweep_rope, reason_context=situation_rope, reason_case=dirty_rope
#     )
#     sweep_plan = sue_speaker.get_plan_obj(sweep_rope)
#     sweep_plan.workforceunit.add_labor(exx.yao)

#     sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
#     save_vision_person(sue_texas_lessonfilehandler, exx.sue, sue_speaker.get_json(), True)
#     yao_duty = personunit_shop(exx.yao)
#     yao_duty.add_contactunit(exx.yao)
#     yao_duty.add_contactunit(exx.sue)
#     new_yao_vision = create_listen_basis(yao_duty)
#     print(f"{new_yao_vision.get_plan_dict().keys()=}")
#     # assert new_yao_vision.get_missing_fact_reason_contexts().get(situation_rope) is None
#     listen_to_agendas_duty_vision(new_yao_vision, texas_lessonfilehandler)
#     print(f"{new_yao_vision.get_plan_dict().keys()=}")
#     assert new_yao_vision.get_missing_fact_reason_contexts().get(situation_rope) is not None

#     # assert new_yao_vision.get_missing_fact_reason_contexts().keys() == {situation_rope}
#     # sue_speaker.add_fact(situation_rope, a23_clean_rope, create_missing_plans=True)

#     # # WHEN
#     # listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fact_contexts)

#     # # THEN
#     # assert len(yao_duty.get_missing_fact_reason_contexts().keys()) == 0
#     assert 1 == 3


# def test_listen_to_facts_duty_vision_DoesNotOverrideFact():
#     # ESTABLISH
#     exx.yao = exx.yao
#     yao_duty = personunit_shop(exx.yao)
#     yao_duty.add_contactunit(exx.yao)
#     yao_duty.set_contact_respect(20)
#     casa_rope = yao_duty.make_l1_rope(casa_str)
#     situation_str = "situation"
#     situation_rope = yao_duty.make_rope(casa_rope, situation_str)
#     a23_clean_rope = yao_duty.make_rope(situation_rope, exx.clean)
#     dirty_str = "dirty"
#     dirty_rope = yao_duty.make_rope(situation_rope, dirty_str)
#
#     sweep_rope = yao_duty.make_rope(casa_rope, exx.sweep)
#     fridge_str = "fridge"
#     fridge_rope = yao_duty.make_rope(casa_rope, fridge_str)
#     running_str = "running"
#     running_rope = yao_duty.make_rope(fridge_rope, running_str)

#     yao_duty.set_plan_obj(planunit_shop(running_str), fridge_rope)
#     yao_duty.set_plan_obj(planunit_shop(exx.clean), situation_rope)
#     yao_duty.set_plan_obj(planunit_shop(dirty_str), situation_rope)
#     yao_duty.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope)
#     yao_duty.edit_plan_attr(
#         sweep_rope, reason_context=situation_rope, reason_case=dirty_rope
#     )
#     yao_duty.edit_plan_attr(
#         sweep_rope, reason_context=fridge_rope, reason_case=running_rope
#     )
#     assert len(yao_duty.get_missing_fact_reason_contexts()) == 2
#     yao_duty.add_fact(situation_rope, dirty_rope)
#     assert len(yao_duty.get_missing_fact_reason_contexts()) == 1
#     assert yao_duty.get_fact(situation_rope).fact_state == dirty_rope

#     # WHEN
#     yao_vision = personunit_shop(exx.yao)
#     yao_vision.add_fact(situation_rope, a23_clean_rope, create_missing_plans=True)
#     yao_vision.add_fact(fridge_rope, running_rope, create_missing_plans=True)
#     missing_fact_fact_contexts = list(yao_duty.get_missing_fact_reason_contexts().keys())
#     listen_to_facts_duty_vision(yao_duty, yao_vision, missing_fact_fact_contexts)

#     # THEN
#     assert len(yao_duty.get_missing_fact_reason_contexts()) == 0
#     # did not grab speaker's factunit
#     assert yao_duty.get_fact(situation_rope).fact_state == dirty_rope
#     # grabed speaker's factunit
#     assert yao_duty.get_fact(fridge_rope).fact_state == running_rope
