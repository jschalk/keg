from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_db_tables,
)
from src.ch07_person_logic.person_config import get_person_config_dict
from src.ch17_idea.idea_config import get_idea_sqlite_types
from src.ch17_idea.idea_db_tool import get_default_sorted_list
from src.ch18_etl_config.etl_sqlstr import (
    create_job_tables,
    create_prime_tablename as prime_table,
    get_job_create_table_sqlstrs,
)
from src.ref.keywords import Ch18Keywords as kw


def test_get_job_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_job_create_table_sqlstrs()

    # THEN
    s_types = get_idea_sqlite_types()
    person_config = get_person_config_dict()
    for x_dimen in person_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = person_config.get(x_dimen)

        job_table = prime_table(x_dimen, kw.job, None)
        job_cols = {kw.moment_rope, kw.person_name}
        job_cols.update(set(x_config.get(kw.jkeys).keys()))
        job_cols.update(set(x_config.get(kw.jvalues).keys()))
        job_cols = get_default_sorted_list(job_cols)
        expected_create_sqlstr = get_create_table_sqlstr(job_table, job_cols, s_types)
        job_dimen_abbr = x_config.get("abbreviation").upper()
        print(
            f'CREATE_JOB_{job_dimen_abbr.upper()}_SQLSTR= """{expected_create_sqlstr}"""'
        )
        # print(f'"{job_table}": CREATE_JOB_{job_dimen_abbr}_SQLSTR,')
        assert create_table_sqlstrs.get(job_table) == expected_create_sqlstr


def test_create_job_tables_CreatesTables(cursor0: Cursor):
    # ESTABLISH
    assert len(get_db_tables(cursor0)) == 0

    prnmemb_job_table = prime_table(kw.person_contact_membership, kw.job, None)
    prncont_job_table = prime_table(kw.person_contactunit, kw.job, None)
    prngrou_job_table = prime_table(kw.person_groupunit, kw.job, None)
    prnawar_job_table = prime_table(kw.person_plan_awardunit, kw.job, None)
    prnfact_job_table = prime_table(kw.person_plan_factunit, kw.job, None)
    prnheal_job_table = prime_table(kw.person_plan_healerunit, kw.job, None)
    prncase_job_table = prime_table(kw.person_plan_reason_caseunit, kw.job, None)
    personares_job_table = prime_table(kw.person_plan_reasonunit, kw.job, None)
    prnlabo_job_table = prime_table(kw.person_plan_laborunit, kw.job, None)
    prnplan_job_table = prime_table(kw.person_planunit, kw.job, None)
    prnunit_job_table = prime_table(kw.personunit, kw.job, None)
    # prnmemb_job_table = f"{kw.person_contact_membership}_job"
    # prncont_job_table = f"{kw.person_contactunit}_job"
    # prngrou_job_table = f"{kw.person_groupunit}_job"
    # prnawar_job_table = f"{kw.person_plan_awardunit}_job"
    # prnfact_job_table = f"{kw.person_plan_factunit}_job"
    # prnheal_job_table = f"{kw.person_plan_healerunit}_job"
    # prncase_job_table = f"{kw.person_plan_reason_caseunit}_job"
    # personares_job_table = f"{kw.person_plan_reasonunit}_job"
    # prnlabo_job_table = f"{kw.person_plan_laborunit}_job"
    # prnplan_job_table = f"{kw.person_planunit}_job"
    # prnunit_job_table = f"{kw.personunit}_job"

    assert db_table_exists(cursor0, prnmemb_job_table) is False
    assert db_table_exists(cursor0, prncont_job_table) is False
    assert db_table_exists(cursor0, prngrou_job_table) is False
    assert db_table_exists(cursor0, prnawar_job_table) is False
    assert db_table_exists(cursor0, prnfact_job_table) is False
    assert db_table_exists(cursor0, prnheal_job_table) is False
    assert db_table_exists(cursor0, prncase_job_table) is False
    assert db_table_exists(cursor0, personares_job_table) is False
    assert db_table_exists(cursor0, prnlabo_job_table) is False
    assert db_table_exists(cursor0, prnplan_job_table) is False
    assert db_table_exists(cursor0, prnunit_job_table) is False

    # WHEN
    create_job_tables(cursor0)

    # THEN
    cursor0.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
    # print(f"{cursor0.fetchall()=}")
    # x_count = 0
    # for x_row in cursor0.fetchall():
    #     print(f"{x_count} {x_row[1]=}")
    #     x_count += 1
    assert db_table_exists(cursor0, prnmemb_job_table)
    assert db_table_exists(cursor0, prncont_job_table)
    assert db_table_exists(cursor0, prngrou_job_table)
    assert db_table_exists(cursor0, prnawar_job_table)
    assert db_table_exists(cursor0, prnfact_job_table)
    assert db_table_exists(cursor0, prnheal_job_table)
    assert db_table_exists(cursor0, prncase_job_table)
    assert db_table_exists(cursor0, personares_job_table)
    assert db_table_exists(cursor0, prnlabo_job_table)
    assert db_table_exists(cursor0, prnplan_job_table)
    assert db_table_exists(cursor0, prnunit_job_table)
    assert len(get_db_tables(cursor0)) == 11
