from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch04_rope.rope import create_rope
from src.ch18_etl_config.etl_sqlstr import (
    CREATE_JOB_PRNPLAN_SQLSTR,
    create_prime_tablename,
)
from src.ch20_kpi.kpi_mstr import create_populate_kpi002_table
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_create_populate_kpi002_table_PopulatesTable_Scenario0_NoPledges(
    cursor0: Cursor,
):
    # ESTABLISH
    casa_rope = create_rope(exx.a23, "casa")
    casa_pledge = 0
    casa_active = 0
    casa_plan_task = 0

    cursor0.execute(CREATE_JOB_PRNPLAN_SQLSTR)
    job_prnplan_tablename = create_prime_tablename("PRNPLAN", "job", None)
    insert_sqlstr = f"""INSERT INTO {job_prnplan_tablename} (
  {kw.moment_rope}
, {kw.person_name}
, {kw.plan_rope}
, {kw.pledge}
, {kw.plan_active}
, {kw.plan_task}
)
VALUES 
  ('{exx.a23}', '{exx.bob}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_plan_task})
, ('{exx.a23}', '{exx.yao}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_plan_task})
"""
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, job_prnplan_tablename) == 2
    moment_kpi002_person_pledges_tablename = kw.moment_kpi002_person_pledges
    assert not db_table_exists(cursor0, moment_kpi002_person_pledges_tablename)

    # WHEN
    create_populate_kpi002_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, moment_kpi002_person_pledges_tablename)
    assert get_table_columns(cursor0, moment_kpi002_person_pledges_tablename) == [
        kw.moment_rope,
        kw.person_name,
        kw.plan_rope,
        kw.pledge,
        kw.plan_active,
        kw.plan_task,
    ]
    assert get_row_count(cursor0, moment_kpi002_person_pledges_tablename) == 0


def test_create_populate_kpi002_table_PopulatesTable_Scenario1_TwoPledges(
    cursor0: Cursor,
):
    # ESTABLISH
    casa_rope = create_rope(exx.a23, "casa")
    casa_pledge = 0
    casa_active = 0
    casa_plan_task = 0
    clean_rope = create_rope(casa_rope, "clean")
    clean_pledge = 1
    clean_active = 1
    clean_plan_task = 1

    cursor0.execute(CREATE_JOB_PRNPLAN_SQLSTR)
    job_prnplan_tablename = create_prime_tablename("PRNPLAN", "job", None)
    insert_sqlstr = f"""INSERT INTO {job_prnplan_tablename} (
  {kw.moment_rope}
, {kw.person_name}
, {kw.plan_rope}
, {kw.pledge}
, {kw.plan_active}
, {kw.plan_task}
)
VALUES 
  ('{exx.a23}', '{exx.bob}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_plan_task})
, ('{exx.a23}', '{exx.yao}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_plan_task})
, ('{exx.a23}', '{exx.bob}', '{clean_rope}', {clean_pledge}, {clean_active}, {clean_plan_task})
, ('{exx.a23}', '{exx.yao}', '{clean_rope}', {clean_pledge}, {clean_active}, {clean_plan_task})
"""
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, job_prnplan_tablename) == 4
    moment_kpi002_person_pledges_tablename = kw.moment_kpi002_person_pledges
    assert not db_table_exists(cursor0, moment_kpi002_person_pledges_tablename)

    # WHEN
    create_populate_kpi002_table(cursor0)

    # THEN
    assert db_table_exists(cursor0, moment_kpi002_person_pledges_tablename)
    assert get_table_columns(cursor0, moment_kpi002_person_pledges_tablename) == [
        kw.moment_rope,
        kw.person_name,
        kw.plan_rope,
        kw.pledge,
        kw.plan_active,
        kw.plan_task,
    ]
    assert get_row_count(cursor0, moment_kpi002_person_pledges_tablename) == 2
