from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import delete_dir
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_gut_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    lessonfilehandler_shop,
    save_gut_file,
)
from src.ch10_person_listen.keep_tool import save_job_file
from src.ch10_person_listen.listen_main import (
    create_listen_basis,
    listen_to_agendas_jobs_into_job,
)
from src.ch10_person_listen.test._util.ch10_examples import (
    a23_casa_rope,
    a23_clean_rope,
    a23_cuisine_rope,
    a23_eat_rope,
    a23_hungry_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_agendas_jobs_into_job_Addscase_tasksToPersonWhenNo_laborunitIsSet(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    yao_gut = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    zia_pool = 87
    yao_gut.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_gut.set_partner_respect(zia_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_job = personunit_shop(exx.zia, exx.a23)
    zia_job.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_partnerunit(exx.yao, partner_debt_lumen=12)
    save_job_file(moment_mstr_dir, zia_job)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_Addscase_tasksToPerson(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    yao_gut = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    zia_pool = 87
    yao_gut.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_gut.set_partner_respect(zia_pool)
    save_job_file(moment_mstr_dir, yao_gut)

    zia_job = personunit_shop(exx.zia, exx.a23)
    zia_job.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_job.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_job.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_Addscase_tasksToPersonWithDetailsDecidedBy_partner_debt_lumen(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    zia_job = get_example_zia_speaker()
    bob_job = get_example_bob_speaker()
    bob_job.edit_plan_attr(
        a23_cuisine_rope(),
        reason_del_case_reason_context=a23_eat_rope(),
        reason_del_case_reason_state=a23_hungry_rope(),
    )
    bob_cuisine_planunit = bob_job.get_plan_obj(a23_cuisine_rope())
    zia_cuisine_planunit = zia_job.get_plan_obj(a23_cuisine_rope())
    assert bob_cuisine_planunit != zia_cuisine_planunit
    assert len(zia_cuisine_planunit.reasonunits) == 1
    assert len(bob_cuisine_planunit.reasonunits) == 0
    save_job_file(moment_mstr_dir, zia_job)
    save_job_file(moment_mstr_dir, bob_job)

    yao_gut = get_example_yao_speaker()
    save_gut_file(moment_mstr_dir, yao_gut)

    new_yao_job1 = create_listen_basis(yao_gut)
    a23_lasso = lassounit_shop(exx.a23)
    assert new_yao_job1.plan_exists(a23_cuisine_rope()) is False

    # WHEN
    yao_lessonfilehandler = lessonfilehandler_shop(moment_mstr_dir, a23_lasso, exx.yao)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job1)

    # THEN
    assert new_yao_job1.plan_exists(a23_cuisine_rope())
    new_cuisine_plan = new_yao_job1.get_plan_obj(a23_cuisine_rope())
    zia_partnerunit = new_yao_job1.get_partner(exx.zia)
    bob_partnerunit = new_yao_job1.get_partner(exx.bob)
    assert zia_partnerunit.partner_debt_lumen < bob_partnerunit.partner_debt_lumen
    assert new_cuisine_plan.get_reasonunit(a23_eat_rope()) is None

    yao_zia_partner_debt_lumen = 15
    yao_bob_partner_debt_lumen = 5
    yao_gut.add_partnerunit(exx.zia, None, yao_zia_partner_debt_lumen)
    yao_gut.add_partnerunit(exx.bob, None, yao_bob_partner_debt_lumen)
    yao_gut.set_partner_respect(100)
    new_yao_job2 = create_listen_basis(yao_gut)
    assert new_yao_job2.plan_exists(a23_cuisine_rope()) is False

    # WHEN
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job2)

    # THEN
    assert new_yao_job2.plan_exists(a23_cuisine_rope())
    new_cuisine_plan = new_yao_job2.get_plan_obj(a23_cuisine_rope())
    zia_partnerunit = new_yao_job2.get_partner(exx.zia)
    bob_partnerunit = new_yao_job2.get_partner(exx.bob)
    assert zia_partnerunit.partner_debt_lumen > bob_partnerunit.partner_debt_lumen
    zia_eat_reasonunit = zia_cuisine_planunit.get_reasonunit(a23_eat_rope())
    assert new_cuisine_plan.get_reasonunit(a23_eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_jobs_into_job_ProcessesIrrationalPerson(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    yao_gut = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    sue_partner_cred_lumen = 57
    sue_partner_debt_lumen = 51
    yao_gut.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_gut.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_gut.set_partner_respect(yao_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_job = personunit_shop(exx.zia, exx.a23)
    zia_job.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_job.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_job.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)

    sue_job = personunit_shop(exx.sue, exx.a23)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_partnerunit(exx.yao, partner_debt_lumen=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_job.make_l1_rope(vacuum_str)
    sue_job.set_l1_plan(planunit_shop(vacuum_str, pledge=True))
    vacuum_planunit = sue_job.get_plan_obj(vacuum_rope)
    vacuum_planunit.workforceunit.add_labor(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_job.make_l1_rope(egg_str)
    sue_job.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_job.make_l1_rope(chicken_str)
    sue_job.set_l1_plan(planunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_job.edit_plan_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_job.edit_plan_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    save_job_file(moment_mstr_dir, sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN irrational person is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_partnerunit = new_yao_job.get_partner(exx.zia)
    sue_partnerunit = new_yao_job.get_partner(exx.sue)
    print(f"{sue_partnerunit.partner_debt_lumen=}")
    print(f"{sue_partnerunit.irrational_partner_debt_lumen=}")
    assert zia_partnerunit.irrational_partner_debt_lumen == 0
    assert sue_partnerunit.irrational_partner_debt_lumen == 51


def test_listen_to_agendas_jobs_into_job_ProcessesMissingDebtorPerson(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    yao_gut_path = create_gut_path(moment_mstr_dir, a23_lasso, exx.yao)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = personunit_shop(exx.yao, exx.a23)
    zia_partner_cred_lumen = 47
    sue_partner_cred_lumen = 57
    zia_partner_debt_lumen = 41
    sue_partner_debt_lumen = 51
    yao_gut.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_gut.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_gut.set_partner_respect(yao_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_job = personunit_shop(exx.zia, exx.a23)
    zia_job.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_job.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_job.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN irrational person is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_partnerunit = new_yao_job.get_partner(exx.zia)
    sue_partnerunit = new_yao_job.get_partner(exx.sue)
    print(f"{sue_partnerunit.partner_debt_lumen=}")
    print(f"{sue_partnerunit.inallocable_partner_debt_lumen=}")
    assert zia_partnerunit.inallocable_partner_debt_lumen == 0
    assert sue_partnerunit.inallocable_partner_debt_lumen == 51


def test_listen_to_agendas_jobs_into_job_ListensToPerson_gut_AndNotPerson_job(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    yao_gut = personunit_shop(exx.yao, exx.a23)
    yao_partner_cred_lumen = 57
    yao_partner_debt_lumen = 51
    yao_gut.add_partnerunit(exx.yao, yao_partner_cred_lumen, yao_partner_debt_lumen)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    yao_gut.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_pool = 87
    yao_gut.set_partner_respect(yao_pool)
    # save yao without case_task to dutys
    save_gut_file(moment_mstr_dir, yao_gut)

    # Save Zia to job
    zia_job = personunit_shop(exx.zia, exx.a23)
    zia_job.set_plan_obj(planunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_partnerunit(exx.yao, partner_debt_lumen=12)
    clean_planunit = zia_job.get_plan_obj(a23_clean_rope())
    cuisine_planunit = zia_job.get_plan_obj(a23_cuisine_rope())
    clean_planunit.workforceunit.add_labor(exx.yao)
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)

    # save yao with case_task to dutys
    yao_old_job = personunit_shop(exx.yao, exx.a23)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_job.make_l1_rope(vacuum_str)
    yao_old_job.set_l1_plan(planunit_shop(vacuum_str, pledge=True))
    vacuum_planunit = yao_old_job.get_plan_obj(vacuum_rope)
    vacuum_planunit.workforceunit.add_labor(exx.yao)
    save_job_file(moment_mstr_dir, yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN irrational person is ignored
    assert len(new_yao_job.get_agenda_dict()) != 2
    assert len(new_yao_job.get_agenda_dict()) == 3
