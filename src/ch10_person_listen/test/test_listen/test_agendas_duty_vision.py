from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import lessonfilehandler_shop
from src.ch10_person_listen.keep_tool import save_duty_person, save_vision_person
from src.ch10_person_listen.listen_main import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
)
from src.ch10_person_listen.test._util.ch10_examples import (
    a23_casa_rope,
    a23_clean_rope,
    a23_cuisine_rope,
    a23_eat_rope,
    a23_hungry_rope,
    a23_run_rope,
    get_dakota_lessonfilehandler,
    get_dakota_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    run_str,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_agenda_duty_vision_agenda_Addscase_tasksTovision_PersonWhenNo_laborunitIsSet(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    zia_pool = 87
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.set_partner_respect(zia_pool)

    zia_vision = personunit_shop(exx.zia, exx.a23)
    zia_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_partnerunit(exx.yao, partner_debt_lumen=12)
    a23_lasso = lassounit_shop(exx.a23)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(
        str(temp3_fs), a23_lasso, exx.yao
    )
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_plan_dict())=}")
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_Addscase_tasksTovision_Person(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    zia_pool = 87
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.set_partner_respect(zia_pool)

    zia_vision = personunit_shop(exx.zia, exx.a23)
    zia_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_vision.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_vision.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    a23_lasso = lassounit_shop(exx.a23)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(
        str(temp3_fs), a23_lasso, exx.yao
    )
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    # zia_file_path = create_path(visions_path, exx.zia}.json")
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_plan_dict())=}")
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_Addscase_tasksTovisionPersonWithDetailsDecidedBy_partner_debt_lumen(
    temp3_fs,
):
    # ESTABLISH
    zia_vision = get_example_zia_speaker()
    bob_vision = get_example_bob_speaker()
    bob_vision.edit_plan_attr(
        a23_cuisine_rope(),
        reason_del_case_reason_context=a23_eat_rope(),
        reason_del_case_reason_state=a23_hungry_rope(),
    )
    bob_cuisine_planunit = bob_vision.get_plan_obj(a23_cuisine_rope())
    zia_cuisine_planunit = zia_vision.get_plan_obj(a23_cuisine_rope())
    assert bob_cuisine_planunit != zia_cuisine_planunit
    assert len(zia_cuisine_planunit.reasonunits) == 1
    assert len(bob_cuisine_planunit.reasonunits) == 0
    sue_dakota_lessonfilehandler = get_dakota_lessonfilehandler(str(temp3_fs))
    save_vision_person(
        sue_dakota_lessonfilehandler.moment_mstr_dir,
        sue_dakota_lessonfilehandler.person_name,
        sue_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        sue_dakota_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )
    save_vision_person(
        sue_dakota_lessonfilehandler.moment_mstr_dir,
        sue_dakota_lessonfilehandler.person_name,
        sue_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        sue_dakota_lessonfilehandler.moment_lasso.knot,
        bob_vision,
    )

    yao_duty = get_example_yao_speaker()
    save_duty_person(
        moment_mstr_dir=sue_dakota_lessonfilehandler.moment_mstr_dir,
        person_name=sue_dakota_lessonfilehandler.person_name,
        moment_rope=sue_dakota_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_person=yao_duty,
    )
    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.plan_exists(a23_cuisine_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(
        new_yao_job1, sue_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert new_yao_job1.plan_exists(a23_cuisine_rope())
    new_cuisine_plan = new_yao_job1.get_plan_obj(a23_cuisine_rope())
    zia_partnerunit = new_yao_job1.get_partner(exx.zia)
    bob_partnerunit = new_yao_job1.get_partner(exx.bob)
    assert zia_partnerunit.partner_debt_lumen < bob_partnerunit.partner_debt_lumen
    assert new_cuisine_plan.get_reasonunit(a23_eat_rope()) is None

    yao_zia_partner_debt_lumen = 15
    yao_bob_partner_debt_lumen = 5
    yao_duty.add_partnerunit(exx.zia, None, yao_zia_partner_debt_lumen)
    yao_duty.add_partnerunit(exx.bob, None, yao_bob_partner_debt_lumen)
    yao_duty.set_partner_respect(100)
    new_yao_job2 = create_listen_basis(yao_duty)
    assert new_yao_job2.plan_exists(a23_cuisine_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(
        new_yao_job2, sue_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert new_yao_job2.plan_exists(a23_cuisine_rope())
    new_cuisine_plan = new_yao_job2.get_plan_obj(a23_cuisine_rope())
    zia_partnerunit = new_yao_job2.get_partner(exx.zia)
    bob_partnerunit = new_yao_job2.get_partner(exx.bob)
    assert zia_partnerunit.partner_debt_lumen > bob_partnerunit.partner_debt_lumen
    zia_eat_reasonunit = zia_cuisine_planunit.get_reasonunit(a23_eat_rope())
    assert new_cuisine_plan.get_reasonunit(a23_eat_rope()) == zia_eat_reasonunit


def test_listen_to_agenda_duty_vision_agenda_ProcessesIrrationalPerson(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    sue_partner_cred_lumen = 57
    sue_partner_debt_lumen = 51
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_duty.set_partner_respect(yao_pool)
    a23_lasso = lassounit_shop(exx.a23)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(
        str(temp3_fs), a23_lasso, exx.yao
    )
    save_duty_person(
        moment_mstr_dir=yao_dakota_lessonfilehandler.moment_mstr_dir,
        person_name=yao_dakota_lessonfilehandler.person_name,
        moment_rope=yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    zia_vision = personunit_shop(exx.zia, exx.a23)
    zia_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_vision.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_vision.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    sue_vision = personunit_shop(exx.sue)
    sue_vision.set_max_tree_traverse(5)
    zia_vision.add_partnerunit(exx.yao, partner_debt_lumen=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_vision.make_l1_rope(vacuum_str)
    sue_vision.set_l1_plan(planunit_shop(vacuum_str, pledge=True))
    vacuum_planunit = sue_vision.get_plan_obj(vacuum_rope)
    vacuum_planunit.workforceunit.add_labor(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_vision.make_l1_rope(egg_str)
    sue_vision.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_vision.make_l1_rope(chicken_str)
    sue_vision.set_l1_plan(planunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_vision.edit_plan_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_vision.edit_plan_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        sue_vision,
    )

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN irrational person is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_partnerunit = new_yao_vision.get_partner(exx.zia)
    sue_partnerunit = new_yao_vision.get_partner(exx.sue)
    print(f"{sue_partnerunit.partner_debt_lumen=}")
    print(f"{sue_partnerunit.irrational_partner_debt_lumen=}")
    assert zia_partnerunit.irrational_partner_debt_lumen == 0
    assert sue_partnerunit.irrational_partner_debt_lumen == 51


def test_listen_to_agenda_duty_vision_agenda_ProcessesMissingDebtorvisionPerson(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    sue_partner_cred_lumen = 57
    zia_partner_debt_lumen = 41
    sue_partner_debt_lumen = 51
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_duty.set_partner_respect(yao_pool)
    a23_lasso = lassounit_shop(exx.a23)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(
        str(temp3_fs), a23_lasso, exx.yao
    )
    save_duty_person(
        moment_mstr_dir=yao_dakota_lessonfilehandler.moment_mstr_dir,
        person_name=yao_dakota_lessonfilehandler.person_name,
        moment_rope=yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    zia_vision = personunit_shop(exx.zia, exx.a23)
    zia_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_vision.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_vision.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(
        str(temp3_fs), a23_lasso, exx.yao
    )
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN irrational person is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_partnerunit = new_yao_vision.get_partner(exx.zia)
    sue_partnerunit = new_yao_vision.get_partner(exx.sue)
    print(f"{sue_partnerunit.partner_debt_lumen=}")
    print(f"{sue_partnerunit.inallocable_partner_debt_lumen=}")
    assert zia_partnerunit.inallocable_partner_debt_lumen == 0
    assert sue_partnerunit.inallocable_partner_debt_lumen == 51


def test_listen_to_agenda_duty_vision_agenda_ListensToPerson_duty_AndNotPerson_vision(
    temp3_fs,
):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao, exx.a23)
    yao_partner_cred_lumen = 57
    yao_partner_debt_lumen = 51
    yao_duty.add_partnerunit(exx.yao, yao_partner_cred_lumen, yao_partner_debt_lumen)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_pool = 87
    yao_duty.set_partner_respect(yao_pool)
    # save yao without case_task to dutys
    a23_lasso = lassounit_shop(exx.a23)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(
        str(temp3_fs), a23_lasso, exx.yao
    )
    save_duty_person(
        moment_mstr_dir=yao_dakota_lessonfilehandler.moment_mstr_dir,
        person_name=yao_dakota_lessonfilehandler.person_name,
        moment_rope=yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    # Save Zia to visions
    zia_vision = personunit_shop(exx.zia, exx.a23)
    zia_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_vision.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_vision.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        zia_vision,
    )

    # save yao with case_task to visions
    yao_old_vision = personunit_shop(exx.yao, exx.a23)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_vision.make_l1_rope(vacuum_str)
    yao_old_vision.set_l1_plan(planunit_shop(vacuum_str, pledge=True))
    vacuum_planunit = yao_old_vision.get_plan_obj(vacuum_rope)
    vacuum_planunit.workforceunit.add_labor(exx.yao)
    save_vision_person(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.person_name,
        yao_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.moment_lasso.knot,
        yao_old_vision,
    )

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN irrational person is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_GetsAgendaFromSrcPersonNotSpeakerSelf(
    temp3_fs,
):
    # ESTABLISH
    # yao_duty has case_task run_rope
    # yao_vision has case_task a23_clean_rope
    # yao_new_vision fact_states yao_duty case_task run_rope and not a23_clean_rope
    yao_duty = get_example_yao_speaker()
    assert yao_duty.plan_exists(a23_run_rope()) is False
    assert yao_duty.plan_exists(a23_clean_rope()) is False
    yao_duty.set_plan_obj(planunit_shop(run_str(), pledge=True), a23_casa_rope())
    sue_dakota_lessonfilehandler = get_dakota_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_dakota_lessonfilehandler.moment_mstr_dir,
        person_name=sue_dakota_lessonfilehandler.person_name,
        moment_rope=sue_dakota_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_person=yao_duty,
    )
    yao_old_vision = get_example_yao_speaker()
    assert yao_old_vision.plan_exists(a23_run_rope()) is False
    assert yao_old_vision.plan_exists(a23_clean_rope()) is False
    yao_old_vision.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    save_vision_person(
        sue_dakota_lessonfilehandler.moment_mstr_dir,
        sue_dakota_lessonfilehandler.person_name,
        sue_dakota_lessonfilehandler.moment_lasso.moment_rope,
        get_dakota_rope(),
        sue_dakota_lessonfilehandler.moment_lasso.knot,
        yao_old_vision,
    )

    yao_new_vision = create_listen_basis(yao_duty)
    assert yao_new_vision.plan_exists(a23_run_rope()) is False
    assert yao_new_vision.plan_exists(a23_clean_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(
        yao_new_vision, sue_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert yao_new_vision.plan_exists(a23_clean_rope()) is False
    assert yao_new_vision.plan_exists(a23_run_rope())
