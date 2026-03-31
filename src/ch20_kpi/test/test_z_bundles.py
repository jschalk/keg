from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_db_tables, get_row_count
from src.ch18_etl_config.etl_sqlstr import (
    CREATE_JOB_PRNPLAN_SQLSTR,
    create_prime_tablename,
)
from src.ch19_etl_main.etl_main import CREATE_MOMENT_PARTNER_NETS_SQLSTR
from src.ch20_kpi.kpi_mstr import populate_kpi_bundle
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_populate_kpi_bundle_PopulatesTable_Scenario0_WithDefaultBundleID(
    cursor0: Cursor,
):
    # ESTABLISH
    yao_partner_net = -55
    bob_partner_net = 600

    cursor0.execute(CREATE_JOB_PRNPLAN_SQLSTR)
    cursor0.execute(CREATE_MOMENT_PARTNER_NETS_SQLSTR)
    moment_partner_nets_tablename = kw.moment_partner_nets
    prnplan_job_tablename = create_prime_tablename("PRNPLAN", "job", None)
    insert_sqlstr = f"""INSERT INTO {moment_partner_nets_tablename} ({kw.moment_rope}, {kw.person_name}, {kw.person_net_amount})
VALUES
  ('{exx.a23}', '{exx.bob}', {bob_partner_net})
, ('{exx.a23}', '{exx.yao}', {yao_partner_net})
"""
    cursor0.execute(insert_sqlstr)
    assert db_table_exists(cursor0, prnplan_job_tablename)
    assert get_row_count(cursor0, moment_partner_nets_tablename) == 2
    moment_kpi001_tablename = kw.moment_kpi001_partner_nets
    moment_kpi002_tablename = kw.moment_kpi002_person_pledges
    assert not db_table_exists(cursor0, moment_kpi001_tablename)
    assert not db_table_exists(cursor0, moment_kpi002_tablename)

    # WHEN
    populate_kpi_bundle(cursor0, kw.default_kpi_bundle)

    # THEN
    assert db_table_exists(cursor0, moment_kpi001_tablename)
    assert db_table_exists(cursor0, moment_kpi002_tablename)
    assert get_row_count(cursor0, moment_kpi001_tablename) == 2
    assert get_row_count(cursor0, moment_kpi002_tablename) == 0
    assert set(get_db_tables(cursor0).keys()) == {
        kw.moment_kpi001_partner_nets,
        kw.moment_kpi002_person_pledges,
        moment_partner_nets_tablename,
        prnplan_job_tablename,
    }


def test_populate_kpi_bundle_PopulatesTable_Scenario1_WithNoBundleID(cursor0: Cursor):
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
    populate_kpi_bundle(cursor0)

    # THEN
    assert get_row_count(cursor0, moment_kpi001_partner_nets_tablename) == 2
    prnplan_job_tablename = create_prime_tablename("PRNPLAN", "job", None)
    assert set(get_db_tables(cursor0).keys()) == {
        kw.moment_kpi001_partner_nets,
        kw.moment_kpi002_person_pledges,
        moment_partner_nets_tablename,
        prnplan_job_tablename,
    }
