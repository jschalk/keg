from os.path import exists as os_path_exists
from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch00_py.file_toolbox import save_json
from src.ch02_contact.group import awardunit_shop
from src.ch03_workforce.workforce import workforceunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch10_person_listen._ref.ch10_path import create_job_path
from src.ch10_person_listen.keep_tool import save_job_file
from src.ch14_moment.moment_main import momentunit_shop
from src.ch18_etl_config.etl_sqlstr import create_prime_tablename as prime_table
from src.ch19_etl_steps.etl_main import etl_moment_job_jsons_to_job_tables
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario0(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    sue_person = personunit_shop(exx.sue, exx.a23)
    sue_person.add_contactunit(exx.sue)
    sue_person.add_contactunit(exx.bob)
    sue_person.get_contact(exx.bob).add_membership(exx.run)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    situation_rope = sue_person.make_l1_rope(kw.reason_active)
    clean_rope = sue_person.make_rope(situation_rope, exx.clean)
    dirty_rope = sue_person.make_rope(situation_rope, "dirty")
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    sue_person.add_plan(dirty_rope)
    sue_person.edit_plan_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_person.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run))
    sue_person.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    sue_workforceunit = workforceunit_shop()
    sue_workforceunit.add_labor(exx.sue)
    sue_person.edit_plan_attr(casa_rope, workforceunit=sue_workforceunit)
    sue_person.add_fact(situation_rope, clean_rope)
    # print(f"{sue_person.get_plan_obj(casa_rope).workforceunit=}")
    # print(f"{sue_person.get_plan_obj(casa_rope).to_dict()=}")
    save_job_file(moment_mstr_dir, sue_person)

    prnmemb_job_table = prime_table(kw.prnmemb, kw.job, None)
    prncont_job_table = prime_table(kw.prncont, kw.job, None)
    prngrou_job_table = prime_table(kw.prngrou, kw.job, None)
    prnawar_job_table = prime_table(kw.prnawar, kw.job, None)
    prnfact_job_table = prime_table(kw.prnfact, kw.job, None)
    prnheal_job_table = prime_table(kw.prnheal, kw.job, None)
    prncase_job_table = prime_table(kw.prncase, kw.job, None)
    prnreas_job_table = prime_table(kw.prnreas, kw.job, None)
    prnlabo_job_table = prime_table(kw.prnlabo, kw.job, None)
    prnplan_job_table = prime_table(kw.prnplan, kw.job, None)
    prnunit_job_table = prime_table(kw.prnunit, kw.job, None)
    assert not db_table_exists(cursor0, prnunit_job_table)
    assert not db_table_exists(cursor0, prnplan_job_table)
    assert not db_table_exists(cursor0, prncont_job_table)
    assert not db_table_exists(cursor0, prnmemb_job_table)
    assert not db_table_exists(cursor0, prngrou_job_table)
    assert not db_table_exists(cursor0, prnawar_job_table)
    assert not db_table_exists(cursor0, prnfact_job_table)
    assert not db_table_exists(cursor0, prnheal_job_table)
    assert not db_table_exists(cursor0, prnreas_job_table)
    assert not db_table_exists(cursor0, prncase_job_table)
    assert not db_table_exists(cursor0, prnlabo_job_table)

    # WHEN
    etl_moment_job_jsons_to_job_tables(cursor0, moment_mstr_dir)

    # THEN
    assert get_row_count(cursor0, prnunit_job_table) == 1
    assert get_row_count(cursor0, prnplan_job_table) == 5
    assert get_row_count(cursor0, prncont_job_table) == 2
    assert get_row_count(cursor0, prnmemb_job_table) == 3
    assert get_row_count(cursor0, prngrou_job_table) == 3
    assert get_row_count(cursor0, prnawar_job_table) == 1
    assert get_row_count(cursor0, prnfact_job_table) == 1
    assert get_row_count(cursor0, prnheal_job_table) == 1
    assert get_row_count(cursor0, prnreas_job_table) == 1
    assert get_row_count(cursor0, prncase_job_table) == 1
    assert get_row_count(cursor0, prnlabo_job_table) == 1


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario1(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    credit44 = 44
    credit77 = 77
    credit88 = 88
    moment_mstr_dir = str(temp3_fs)
    bob_job = personunit_shop(bob_inx, exx.a23)
    bob_job.add_contactunit(bob_inx, credit77)
    bob_job.add_contactunit(yao_inx, credit44)
    bob_job.add_contactunit(bob_inx, credit77)
    bob_job.add_contactunit(sue_inx, credit88)
    bob_job.add_contactunit(yao_inx, credit44)
    save_job_file(moment_mstr_dir, bob_job)
    a23_lasso = lassounit_shop(exx.a23)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    moment_dict = momentunit_shop(exx.a23, moment_mstr_dir).to_dict()
    save_json(moment_json_path, None, moment_dict)
    a23_bob_job_path = create_job_path(moment_mstr_dir, a23_lasso, bob_inx)
    assert os_path_exists(moment_json_path)
    assert os_path_exists(a23_bob_job_path)
    prncont_job_tablename = prime_table("prncont", kw.job, None)
    assert not db_table_exists(cursor0, prncont_job_tablename)

    # WHEN
    etl_moment_job_jsons_to_job_tables(cursor0, moment_mstr_dir)

    # THEN
    assert get_row_count(cursor0, prncont_job_tablename) == 3
    rows = cursor0.execute(f"SELECT * FROM {prncont_job_tablename}").fetchall()
    print(rows)
    assert rows == [
        (
            exx.a23,
            "Bobby",
            "Bobby",
            77.0,
            1.0,
            ";",
            368421053.0,
            333333334.0,
            368421053.0,
            333333334.0,
            368421053.0,
            333333334.0,
            0.368421053,
            0.333333334,
            0.0,
            0.0,
        ),
        (
            exx.a23,
            "Bobby",
            "Suzy",
            88.0,
            1.0,
            ";",
            421052631.0,
            333333333.0,
            421052631.0,
            333333333.0,
            421052631.0,
            333333333.0,
            0.421052631,
            0.333333333,
            0.0,
            0.0,
        ),
        (
            exx.a23,
            "Bobby",
            "Yaoe",
            44.0,
            1.0,
            ";",
            210526316.0,
            333333333.0,
            210526316.0,
            333333333.0,
            210526316.0,
            333333333.0,
            0.210526316,
            0.333333333,
            0.0,
            0.0,
        ),
    ]
