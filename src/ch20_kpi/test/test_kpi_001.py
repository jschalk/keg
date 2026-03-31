from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch04_rope.rope import create_rope
from src.ch18_etl_config.etl_sqlstr import (
    CREATE_JOB_PRNPLAN_SQLSTR,
    create_prime_tablename,
)
from src.ch19_etl_main.etl_main import CREATE_MOMENT_PARTNER_NETS_SQLSTR
from src.ch20_kpi.kpi_mstr import create_populate_kpi001_table
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_create_populate_kpi001_table_PopulatesTable_Scenario0_NoPledges(
    cursor0: Cursor,
):
    # ESTABLISH
    yao_partner_net = -55
    bob_partner_net = 600

    cursor0.execute(CREATE_JOB_PRNPLAN_SQLSTR)
    cursor0.execute(CREATE_MOMENT_PARTNER_NETS_SQLSTR)
    moment_partner_nets_tablename = kw.moment_partner_nets
    insert_sqlstr = f"""INSERT INTO {moment_partner_nets_tablename} ({kw.moment_rope}, {kw.person_name}, {kw.person_net_amount}) 
VALUES 
  ('{exx.a23}', '{exx.bob}', {bob_partner_net})
, ('{exx.a23}', '{exx.yao}', {yao_partner_net})
"""
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, moment_partner_nets_tablename) == 2
    moment_kpi001_partner_nets_tablename = kw.moment_kpi001_partner_nets
    assert not db_table_exists(cursor0, moment_kpi001_partner_nets_tablename)

    # WHEN
    create_populate_kpi001_table(cursor0)

    # THEN
    assert get_table_columns(cursor0, moment_kpi001_partner_nets_tablename) == [
        kw.moment_rope,
        kw.person_name,
        kw.net_funds,
        kw.fund_rank,
        kw.pledges_count,
    ]
    assert get_row_count(cursor0, moment_kpi001_partner_nets_tablename)
    select_sqlstr = f"""
SELECT 
  {kw.moment_rope}
, {kw.person_name}
, {kw.net_funds}
, {kw.fund_rank}
, {kw.pledges_count}
FROM {moment_kpi001_partner_nets_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [(exx.a23, exx.bob, 600.0, 1, 0), (exx.a23, exx.yao, -55.0, 2, 0)]


def test_create_populate_kpi001_table_PopulatesTable_Scenario1_1pledge(cursor0: Cursor):
    # ESTABLISH
    yao_partner_net = -55
    bob_partner_net = 600
    casa_rope = create_rope(exx.a23, "casa")

    cursor0.execute(CREATE_MOMENT_PARTNER_NETS_SQLSTR)
    moment_partner_nets_tablename = kw.moment_partner_nets
    insert_sqlstr = f"""INSERT INTO {moment_partner_nets_tablename} ({kw.moment_rope}, {kw.person_name}, {kw.person_net_amount})
VALUES
  ('{exx.a23}', '{exx.bob}', {bob_partner_net})
, ('{exx.a23}', '{exx.yao}', {yao_partner_net})
"""
    cursor0.execute(insert_sqlstr)
    assert get_row_count(cursor0, moment_partner_nets_tablename) == 2

    cursor0.execute(CREATE_JOB_PRNPLAN_SQLSTR)
    job_prnplan_tablename = create_prime_tablename("prnplan", "job", None)
    insert_sqlstr = f"""
INSERT INTO {job_prnplan_tablename} ({kw.moment_rope}, {kw.person_name}, {kw.plan_rope}, {kw.pledge})
VALUES ('{exx.a23}', '{exx.bob}', '{casa_rope}', 1)
"""
    cursor0.execute(insert_sqlstr)
    moment_kpi001_partner_nets_tablename = kw.moment_kpi001_partner_nets
    assert not db_table_exists(cursor0, moment_kpi001_partner_nets_tablename)

    # WHEN
    create_populate_kpi001_table(cursor0)

    # THEN
    assert get_row_count(cursor0, moment_kpi001_partner_nets_tablename)
    select_sqlstr = f"""SELECT {kw.moment_rope}, {kw.person_name}, {kw.net_funds}, {kw.fund_rank}, {kw.pledges_count} FROM {moment_kpi001_partner_nets_tablename}"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (exx.a23, exx.bob, bob_partner_net, 1, 1),
        (exx.a23, exx.yao, yao_partner_net, 2, 0),
    ]
