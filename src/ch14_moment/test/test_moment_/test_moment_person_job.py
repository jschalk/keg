from src.ch00_py.file_toolbox import set_dir
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_person_dir_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import gut_file_exists, save_gut_file
from src.ch10_person_listen.keep_tool import (
    job_file_exists,
    open_job_file,
    save_job_file,
)
from src.ch14_moment.moment_main import momentunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_MomentUnit_rotate_job_ReturnsObj_Scenario1(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    a23_moment.create_init_job_from_guts(exx.sue)
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)

    # WHEN
    sue_job = a23_moment.rotate_job(exx.sue)

    # THEN
    example_person = personunit_shop(exx.sue, exx.a23)
    assert sue_job.planroot.get_plan_rope() == example_person.planroot.get_plan_rope()
    assert sue_job.person_name == example_person.person_name


def test_MomentUnit_rotate_job_ReturnsObj_Scenario2_EmptyContactsCause_inallocable_contact_debt_lumen(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    init_sue_job = personunit_shop(exx.sue, exx.a23)
    init_sue_job.add_contactunit(exx.yao)
    init_sue_job.add_contactunit(exx.bob)
    init_sue_job.add_contactunit(exx.zia)
    save_job_file(moment_mstr_dir, init_sue_job)
    a23_lasso = lassounit_shop(exx.a23)
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.yao) is False
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.bob) is False
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.zia) is False

    # WHEN
    rotated_sue_job = a23_moment.rotate_job(exx.sue)

    # THEN method should wipe over job person
    assert rotated_sue_job.contact_exists(exx.bob)
    assert rotated_sue_job.to_dict() != init_sue_job.to_dict()
    assert init_sue_job.get_contact(exx.bob).inallocable_contact_debt_lumen == 0
    assert rotated_sue_job.get_contact(exx.bob).inallocable_contact_debt_lumen == 1


def a23_job(person_name: str, moment_mstr_dir: str) -> PersonUnit:
    a23_lasso = lassounit_shop(exx.a23)
    return open_job_file(moment_mstr_dir, a23_lasso, person_name)


def test_MomentUnit_rotate_job_ReturnsObj_Scenario3_job_ChangesFromRotation(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    init_sue_job = personunit_shop(exx.sue, exx.a23)
    init_sue_job.add_contactunit(exx.yao)
    init_yao_job = personunit_shop(exx.yao, exx.a23)
    init_yao_job.add_contactunit(exx.bob)
    init_bob_job = personunit_shop(exx.bob, exx.a23)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_plan(clean_rope, pledge=True)
    save_job_file(moment_mstr_dir, init_sue_job)
    save_job_file(moment_mstr_dir, init_yao_job)
    save_job_file(moment_mstr_dir, init_bob_job)
    assert len(a23_job(exx.sue, moment_mstr_dir).get_agenda_dict()) == 0
    assert len(a23_job(exx.yao, moment_mstr_dir).get_agenda_dict()) == 0
    assert len(a23_job(exx.bob, moment_mstr_dir).get_agenda_dict()) == 1

    # WHEN / THEN
    assert len(a23_moment.rotate_job(exx.sue).get_agenda_dict()) == 0
    assert len(a23_moment.rotate_job(exx.yao).get_agenda_dict()) == 1
    assert len(a23_moment.rotate_job(exx.bob).get_agenda_dict()) == 0


def test_MomentUnit_rotate_job_ReturnsObj_Scenario4_job_SelfReferenceWorks(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    init_bob_job = personunit_shop(exx.bob, exx.a23)
    init_bob_job.add_contactunit(exx.bob)
    init_sue_job = personunit_shop(exx.sue, exx.a23)
    init_sue_job.add_contactunit(exx.yao)
    init_yao_job = personunit_shop(exx.yao, exx.a23)
    init_yao_job.add_contactunit(exx.bob)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_plan(clean_rope, pledge=True)
    save_job_file(moment_mstr_dir, init_sue_job)
    save_job_file(moment_mstr_dir, init_yao_job)
    save_job_file(moment_mstr_dir, init_bob_job)
    assert len(a23_job(exx.bob, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.sue, moment_mstr_dir).get_agenda_dict()) == 0
    assert len(a23_job(exx.yao, moment_mstr_dir).get_agenda_dict()) == 0

    # WHEN / THEN
    assert len(a23_moment.rotate_job(exx.bob).get_agenda_dict()) == 1
    assert len(a23_moment.rotate_job(exx.sue).get_agenda_dict()) == 0
    assert len(a23_moment.rotate_job(exx.yao).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario0_init_job_IsCreated(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    bob_gut = personunit_shop(exx.bob, exx.a23)
    save_gut_file(moment_mstr_dir, bob_gut)
    a23_lasso = lassounit_shop(exx.a23)
    sue_dir = create_person_dir_path(moment_mstr_dir, a23_lasso, exx.sue)
    set_dir(sue_dir)
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.bob)
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue) is False
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.bob) is False
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.sue) is False

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.bob)
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.bob)
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)


def test_MomentUnit_generate_all_jobs_Scenario1_jobs_rotated(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, job_listen_rotations=1)
    bob_gut = personunit_shop(exx.bob, exx.a23)
    bob_gut.add_contactunit(exx.bob)
    bob_gut.add_contactunit(exx.sue)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_plan(clean_rope, pledge=True)

    sue_gut = personunit_shop(exx.sue, exx.a23)
    sue_gut.add_contactunit(exx.sue)
    sue_gut.add_contactunit(exx.bob)
    yao_gut = personunit_shop(exx.yao, exx.a23)
    yao_gut.add_contactunit(exx.sue)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    a23_lasso = lassounit_shop(exx.a23)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.bob)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.yao)

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.sue, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao, moment_mstr_dir).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario2_jobs_rotated_InSortedOrder(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, job_listen_rotations=1)
    bob_gut = personunit_shop(exx.bob, exx.a23)
    bob_gut.add_contactunit(exx.bob)
    bob_gut.add_contactunit(exx.sue)

    sue_gut = personunit_shop(exx.sue, exx.a23)
    sue_gut.add_contactunit(exx.sue)
    sue_gut.add_contactunit(exx.bob)
    sue_gut.add_contactunit(exx.yao)

    yao_gut = personunit_shop(exx.yao, exx.a23)
    yao_gut.add_contactunit(exx.sue)
    yao_gut.add_contactunit(exx.yao)
    yao_gut.add_contactunit(exx.zia)

    zia_gut = personunit_shop(exx.zia, exx.a23)
    zia_gut.add_contactunit(exx.zia)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_plan(clean_rope, pledge=True)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    save_gut_file(moment_mstr_dir, zia_gut)
    a23_lasso = lassounit_shop(exx.a23)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.bob)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.yao)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.zia)

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob, moment_mstr_dir).get_agenda_dict()) == 0
    assert len(a23_job(exx.sue, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.zia, moment_mstr_dir).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario3_job_listen_rotation_AffectsJobs(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, job_listen_rotations=1)
    bob_gut = personunit_shop(exx.bob, exx.a23)
    bob_gut.add_contactunit(exx.bob)
    bob_gut.add_contactunit(exx.sue)

    sue_gut = personunit_shop(exx.sue, exx.a23)
    sue_gut.add_contactunit(exx.sue)
    sue_gut.add_contactunit(exx.bob)
    sue_gut.add_contactunit(exx.yao)

    yao_gut = personunit_shop(exx.yao, exx.a23)
    yao_gut.add_contactunit(exx.sue)
    yao_gut.add_contactunit(exx.yao)
    yao_gut.add_contactunit(exx.zia)

    zia_gut = personunit_shop(exx.zia, exx.a23)
    zia_gut.add_contactunit(exx.zia)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_plan(clean_rope, pledge=True)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    save_gut_file(moment_mstr_dir, zia_gut)
    a23_lasso = lassounit_shop(exx.a23)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.bob)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.yao)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.zia)
    assert a23_moment.job_listen_rotations == 1

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob, moment_mstr_dir).get_agenda_dict()) == 0
    assert len(a23_job(exx.sue, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.zia, moment_mstr_dir).get_agenda_dict()) == 1

    # WHEN
    a23_moment.job_listen_rotations = 2
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.sue, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao, moment_mstr_dir).get_agenda_dict()) == 1
    assert len(a23_job(exx.zia, moment_mstr_dir).get_agenda_dict()) == 1
