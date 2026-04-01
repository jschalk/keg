from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import open_json, save_json
from src.ch07_person_logic.person_main import get_personunit_from_dict, personunit_shop
from src.ch09_person_lesson._ref.ch09_path import (
    create_gut_path,
    create_moment_json_path,
)
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch10_person_listen._ref.ch10_path import create_job_path
from src.ch14_moment.moment_main import momentunit_shop
from src.ch19_etl_steps.etl_main import etl_moment_guts_to_moment_jobs
from src.ref.keywords import ExampleStrs as exx


def test_etl_moment_guts_to_moment_jobs_SetsFiles_Scenario0(temp3_fs):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    credit44 = 44
    credit77 = 77
    credit88 = 88
    moment_mstr_dir = str(temp3_fs)
    bob_gut = personunit_shop(bob_inx, exx.a23)
    bob_gut.add_contactunit(bob_inx, credit77)
    bob_gut.add_contactunit(yao_inx, credit44)
    bob_gut.add_contactunit(bob_inx, credit77)
    bob_gut.add_contactunit(sue_inx, credit88)
    bob_gut.add_contactunit(yao_inx, credit44)
    a23_lasso = lassounit_shop(exx.a23)
    a23_bob_gut_path = create_gut_path(moment_mstr_dir, a23_lasso, bob_inx)
    save_json(a23_bob_gut_path, None, bob_gut.to_dict())
    a23_bob_job_path = create_job_path(moment_mstr_dir, a23_lasso, bob_inx)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    save_json(
        moment_json_path, None, momentunit_shop(exx.a23, moment_mstr_dir).to_dict()
    )
    assert os_path_exists(moment_json_path)
    assert os_path_exists(a23_bob_gut_path)
    print(f"{a23_bob_gut_path=}")
    assert os_path_exists(a23_bob_job_path) is False

    # WHEN
    etl_moment_guts_to_moment_jobs(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_job_path)
    generated_job = get_personunit_from_dict(open_json(a23_bob_job_path))
    expected_job = personunit_shop(bob_inx, exx.a23)
    expected_job.add_contactunit(bob_inx, credit77)
    expected_job.add_contactunit(yao_inx, credit44)
    expected_job.add_contactunit(bob_inx, credit77)
    expected_job.add_contactunit(sue_inx, credit88)
    expected_job.add_contactunit(yao_inx, credit44)
    # assert generated_job.get_contact(sue_inx) == expected_job.get_contact(sue_inx)
    # assert generated_job.get_contact(bob_inx) == expected_job.get_contact(bob_inx)
    # assert generated_job.get_contact(yao_inx) == expected_job.get_contact(yao_inx)
    assert generated_job.contacts.keys() == expected_job.contacts.keys()
    # assert generated_job.contacts == expected_job.contacts
    # assert generated_job.get_plan_dict() == expected_job.to_dict()
    # assert generated_job.to_dict() == expected_job.to_dict()
    # assert generated_job == expected_job
