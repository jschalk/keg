from src.ch18_etl_config.etl_sqlstr import create_prime_tablename
from src.ch20_kpi.kpi_sqlstr import get_create_kpi001_sqlstr, get_create_kpi002_sqlstr
from src.ref.keywords import Ch20Keywords as kw


def test_get_create_kpi001_sqlstr_ReturnsObj():
    # ESTABLISH
    prnplan_str = kw.person_planunit
    prnplan_job = create_prime_tablename(prnplan_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_create_kpi001_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {kw.moment_kpi001_contact_nets} AS
SELECT
  {kw.moment_contact_nets}.{kw.moment_rope}
, {kw.moment_contact_nets}.{kw.person_name}
, {kw.person_net_amount} AS {kw.net_funds}
, RANK() OVER (ORDER BY {kw.person_net_amount} DESC) AS {kw.fund_rank}
, IFNULL(SUM({prnplan_job}.{kw.pledge}), 0) AS {kw.pledges_count}
FROM {kw.moment_contact_nets}
LEFT JOIN {prnplan_job} ON
  {prnplan_job}.{kw.moment_rope} = {kw.moment_contact_nets}.{kw.moment_rope}
  AND {prnplan_job}.{kw.person_name} = {kw.moment_contact_nets}.{kw.person_name}
GROUP BY {kw.moment_contact_nets}.{kw.moment_rope}, {kw.moment_contact_nets}.{kw.person_name}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_create_kpi002_sqlstr_ReturnsObj():
    # ESTABLISH
    prnplan_str = kw.person_planunit
    prnplan_job = create_prime_tablename(prnplan_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_create_kpi002_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {kw.moment_kpi002_person_pledges} AS
SELECT
  {kw.moment_rope}
, {kw.person_name}
, {kw.plan_rope}
, {kw.pledge}
, {kw.plan_active}
, {kw.plan_task}
FROM {prnplan_job}
WHERE {kw.pledge} == 1 AND {kw.plan_active} == 1
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
