def get_create_kpi001_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 contact nets table.
    """
    return """
CREATE TABLE moment_kpi001_contact_nets AS
SELECT
  moment_contact_nets.moment_rope
, moment_contact_nets.person_name
, person_net_amount AS net_funds
, RANK() OVER (ORDER BY person_net_amount DESC) AS fund_rank
, IFNULL(SUM(person_planunit_job.pledge), 0) AS pledges_count
FROM moment_contact_nets
LEFT JOIN person_planunit_job ON
  person_planunit_job.moment_rope = moment_contact_nets.moment_rope
  AND person_planunit_job.person_name = moment_contact_nets.person_name
GROUP BY moment_contact_nets.moment_rope, moment_contact_nets.person_name
;
"""


def get_create_kpi002_sqlstr() -> str:
    return """
CREATE TABLE moment_kpi002_person_pledges AS
SELECT
  moment_rope
, person_name
, plan_rope
, pledge
, plan_active
, plan_task
FROM person_planunit_job
WHERE pledge == 1 AND plan_active == 1
;
"""
