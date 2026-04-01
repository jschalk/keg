from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor
from src.ch00_py.db_toolbox import sqlite_obj_str
from src.ch02_contact.contact import ContactUnit
from src.ch02_contact.group import AwardHeir, GroupUnit, MemberShip
from src.ch03_workforce.workforce import WorkforceHeir
from src.ch05_reason.reason_main import CaseUnit, FactHeir, ReasonHeir
from src.ch06_plan.plan import HealerUnit, PlanUnit
from src.ch07_person_logic.person_main import PersonUnit
from src.ch11_bud.bud_main import MomentRope
from src.ch19_etl_steps._ref.ch19_semantic_types import (
    ContactName,
    FaceName,
    GroupTitle,
    KnotTerm,
    PersonName,
    RopeTerm,
    SparkInt,
)


def create_prnmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    person_name = values_dict.get("person_name")
    contact_name = values_dict.get("contact_name")
    group_title = values_dict.get("group_title")
    group_cred_lumen = values_dict.get("group_cred_lumen")
    group_debt_lumen = values_dict.get("group_debt_lumen")
    credor_pool = values_dict.get("credor_pool")
    debtor_pool = values_dict.get("debtor_pool")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    fund_agenda_give = values_dict.get("fund_agenda_give")
    fund_agenda_take = values_dict.get("fund_agenda_take")
    fund_agenda_ratio_give = values_dict.get("fund_agenda_ratio_give")
    fund_agenda_ratio_take = values_dict.get("fund_agenda_ratio_take")
    real_str = "REAL"
    return f"""INSERT INTO person_contact_membership_job (moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take, fund_agenda_ratio_give, fund_agenda_ratio_take)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(contact_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
, {sqlite_obj_str(group_cred_lumen, real_str)}
, {sqlite_obj_str(group_debt_lumen, real_str)}
, {sqlite_obj_str(credor_pool, real_str)}
, {sqlite_obj_str(debtor_pool, real_str)}
, {sqlite_obj_str(fund_give, real_str)}
, {sqlite_obj_str(fund_take, real_str)}
, {sqlite_obj_str(fund_agenda_give, real_str)}
, {sqlite_obj_str(fund_agenda_take, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_take, real_str)}
)
;
"""


def create_prncont_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    person_name = values_dict.get("person_name")
    contact_name = values_dict.get("contact_name")
    contact_cred_lumen = values_dict.get("contact_cred_lumen")
    contact_debt_lumen = values_dict.get("contact_debt_lumen")
    groupmark = values_dict.get("groupmark")
    credor_pool = values_dict.get("credor_pool")
    debtor_pool = values_dict.get("debtor_pool")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    fund_agenda_give = values_dict.get("fund_agenda_give")
    fund_agenda_take = values_dict.get("fund_agenda_take")
    fund_agenda_ratio_give = values_dict.get("fund_agenda_ratio_give")
    fund_agenda_ratio_take = values_dict.get("fund_agenda_ratio_take")
    inallocable_contact_debt_lumen = values_dict.get("inallocable_contact_debt_lumen")
    irrational_contact_debt_lumen = values_dict.get("irrational_contact_debt_lumen")
    real_str = "REAL"
    return f"""INSERT INTO person_contactunit_job (moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, groupmark, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take, fund_agenda_ratio_give, fund_agenda_ratio_take, inallocable_contact_debt_lumen, irrational_contact_debt_lumen)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(contact_name, "TEXT")}
, {sqlite_obj_str(contact_cred_lumen, real_str)}
, {sqlite_obj_str(contact_debt_lumen, real_str)}
, {sqlite_obj_str(groupmark, "TEXT")}
, {sqlite_obj_str(credor_pool, real_str)}
, {sqlite_obj_str(debtor_pool, real_str)}
, {sqlite_obj_str(fund_give, real_str)}
, {sqlite_obj_str(fund_take, real_str)}
, {sqlite_obj_str(fund_agenda_give, real_str)}
, {sqlite_obj_str(fund_agenda_take, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_give, real_str)}
, {sqlite_obj_str(fund_agenda_ratio_take, real_str)}
, {sqlite_obj_str(inallocable_contact_debt_lumen, real_str)}
, {sqlite_obj_str(irrational_contact_debt_lumen, real_str)}
)
;
"""


def create_prngrou_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    person_name = values_dict.get("person_name")
    group_title = values_dict.get("group_title")
    credor_pool = values_dict.get("credor_pool")
    debtor_pool = values_dict.get("debtor_pool")
    fund_grain = values_dict.get("fund_grain")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    fund_agenda_give = values_dict.get("fund_agenda_give")
    fund_agenda_take = values_dict.get("fund_agenda_take")
    real_str = "REAL"
    return f"""INSERT INTO person_groupunit_job (moment_rope, person_name, group_title, fund_grain, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(group_title, "TEXT")}
, {sqlite_obj_str(fund_grain, real_str)}
, {sqlite_obj_str(credor_pool, real_str)}
, {sqlite_obj_str(debtor_pool, real_str)}
, {sqlite_obj_str(fund_give, real_str)}
, {sqlite_obj_str(fund_take, real_str)}
, {sqlite_obj_str(fund_agenda_give, real_str)}
, {sqlite_obj_str(fund_agenda_take, real_str)}
)
;
"""


def create_prnawar_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    awardee_title = values_dict.get("awardee_title")
    give_force = values_dict.get("give_force")
    take_force = values_dict.get("take_force")
    fund_give = values_dict.get("fund_give")
    fund_take = values_dict.get("fund_take")
    return f"""INSERT INTO person_plan_awardunit_job (moment_rope, person_name, plan_rope, awardee_title, give_force, take_force, knot, fund_give, fund_take)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(awardee_title, "TEXT")}
, {sqlite_obj_str(give_force, "REAL")}
, {sqlite_obj_str(take_force, "REAL")}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(fund_give, "REAL")}
, {sqlite_obj_str(fund_take, "REAL")}
)
;
"""


def create_prnfact_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    fact_context = values_dict.get("fact_context")
    fact_state = values_dict.get("fact_state")
    fact_lower = values_dict.get("fact_lower")
    fact_upper = values_dict.get("fact_upper")
    return f"""INSERT INTO person_plan_factunit_job (moment_rope, person_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper, knot)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(fact_context, "TEXT")}
, {sqlite_obj_str(fact_state, "TEXT")}
, {sqlite_obj_str(fact_lower, "REAL")}
, {sqlite_obj_str(fact_upper, "REAL")}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prnheal_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    healer_name = values_dict.get("healer_name")
    return f"""INSERT INTO person_plan_healerunit_job (moment_rope, person_name, plan_rope, healer_name, knot)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(healer_name, "TEXT")}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prncase_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    reason_context = values_dict.get("reason_context")
    reason_state = values_dict.get("reason_state")
    reason_lower = values_dict.get("reason_lower")
    reason_upper = values_dict.get("reason_upper")
    reason_divisor = values_dict.get("reason_divisor")
    case_task = values_dict.get("case_task")
    case_active = values_dict.get("case_active")
    return f"""INSERT INTO person_plan_reason_caseunit_job (moment_rope, person_name, plan_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor, knot, case_task, case_active)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(reason_state, "TEXT")}
, {sqlite_obj_str(reason_lower, "REAL")}
, {sqlite_obj_str(reason_upper, "REAL")}
, {sqlite_obj_str(reason_divisor, "REAL")}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(case_task, "INTEGER")}
, {sqlite_obj_str(case_active, "INTEGER")}
)
;
"""


def create_prnreas_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    reason_context = values_dict.get("reason_context")
    active_requisite = values_dict.get("active_requisite")
    reason_task = values_dict.get("reason_task")
    reason_active = values_dict.get("reason_active")
    parent_heir_active = values_dict.get("parent_heir_active")
    return f"""INSERT INTO person_plan_reasonunit_job (moment_rope, person_name, plan_rope, reason_context, active_requisite, knot, reason_active, reason_task, parent_heir_active)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(active_requisite, "INTEGER")}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(reason_active, "INTEGER")}
, {sqlite_obj_str(reason_task, "INTEGER")}
, {sqlite_obj_str(parent_heir_active, "INTEGER")}
)
;
"""


def create_prnlabo_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    labor_title = values_dict.get("labor_title")
    solo = values_dict.get("solo")
    person_name_is_workforce = values_dict.get("person_name_is_workforce")
    return f"""INSERT INTO person_plan_laborunit_job (moment_rope, person_name, plan_rope, labor_title, solo, knot, person_name_is_workforce)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(labor_title, "TEXT")}
, {sqlite_obj_str(solo, "INTEGER")}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(person_name_is_workforce, "INTEGER")}
)
;
"""


def create_prnplan_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    begin = values_dict.get("begin")
    close = values_dict.get("close")
    addin = values_dict.get("addin")
    numor = values_dict.get("numor")
    denom = values_dict.get("denom")
    morph = values_dict.get("morph")
    gogo_want = values_dict.get("gogo_want")
    stop_want = values_dict.get("stop_want")
    star = values_dict.get("star")
    pledge = values_dict.get("pledge")
    problem_bool = values_dict.get("problem_bool")
    active = values_dict.get("plan_active")
    plan_task = values_dict.get("plan_task")
    fund_grain = values_dict.get("fund_grain")
    fund_onset = values_dict.get("fund_onset")
    fund_cease = values_dict.get("fund_cease")
    fund_ratio = values_dict.get("fund_ratio")
    gogo_calc = values_dict.get("gogo_calc")
    stop_calc = values_dict.get("stop_calc")
    tree_level = values_dict.get("tree_level")
    range_evaluated = values_dict.get("range_evaluated")
    descendant_pledge_count = values_dict.get("descendant_pledge_count")
    healerunit_ratio = values_dict.get("healerunit_ratio")
    all_contact_cred = values_dict.get("all_contact_cred")
    all_contact_debt = values_dict.get("all_contact_debt")
    integer_str = "INTEGER"
    real_str = "REAL"

    return f"""INSERT INTO person_planunit_job (moment_rope, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, fund_grain, knot, plan_active, plan_task, fund_onset, fund_cease, fund_ratio, gogo_calc, stop_calc, tree_level, range_evaluated, descendant_pledge_count, healerunit_ratio, all_contact_cred, all_contact_debt)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(begin, real_str)}
, {sqlite_obj_str(close, real_str)}
, {sqlite_obj_str(addin, real_str)}
, {sqlite_obj_str(numor, "INTEGER")}
, {sqlite_obj_str(denom, "INTEGER")}
, {sqlite_obj_str(morph, real_str)}
, {sqlite_obj_str(gogo_want, real_str)}
, {sqlite_obj_str(stop_want, real_str)}
, {sqlite_obj_str(star, real_str)}
, {sqlite_obj_str(pledge, real_str)}
, {sqlite_obj_str(problem_bool, "INTEGER")}
, {sqlite_obj_str(fund_grain, real_str)}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(active, "INTEGER")}
, {sqlite_obj_str(plan_task, "INTEGER")}
, {sqlite_obj_str(fund_onset, real_str)}
, {sqlite_obj_str(fund_cease, real_str)}
, {sqlite_obj_str(fund_ratio, real_str)}
, {sqlite_obj_str(gogo_calc, real_str)}
, {sqlite_obj_str(stop_calc, real_str)}
, {sqlite_obj_str(tree_level, "INTEGER")}
, {sqlite_obj_str(range_evaluated, "INTEGER")}
, {sqlite_obj_str(descendant_pledge_count, "INTEGER")}
, {sqlite_obj_str(healerunit_ratio, real_str)}
, {sqlite_obj_str(all_contact_cred, real_str)}
, {sqlite_obj_str(all_contact_debt, real_str)}
)
;
"""


def create_personunit_metrics_insert_sqlstr(values_dict: dict[str,]):
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    integer_str = "INTEGER"
    real_str = "REAL"
    keeps_buildable = values_dict.get("keeps_buildable")
    keeps_justified = values_dict.get("keeps_justified")
    offtrack_fund = values_dict.get("offtrack_fund")
    rational = values_dict.get("rational")
    sum_healerunit_plans_fund_total = values_dict.get("sum_healerunit_plans_fund_total")
    tree_traverse_count = values_dict.get("tree_traverse_count")
    credor_respect = values_dict.get("credor_respect")
    debtor_respect = values_dict.get("debtor_respect")
    fund_grain = values_dict.get("fund_grain")
    fund_pool = values_dict.get("fund_pool")
    max_tree_traverse = values_dict.get("max_tree_traverse")
    mana_grain = values_dict.get("mana_grain")
    respect_grain = values_dict.get("respect_grain")

    return f"""INSERT INTO personunit_job (moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot, rational, keeps_justified, offtrack_fund, sum_healerunit_plans_fund_total, keeps_buildable, tree_traverse_count)
VALUES (
  {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(credor_respect, real_str)}
, {sqlite_obj_str(debtor_respect, real_str)}
, {sqlite_obj_str(fund_pool, real_str)}
, {sqlite_obj_str(max_tree_traverse, integer_str)}
, {sqlite_obj_str(fund_grain, real_str)}
, {sqlite_obj_str(mana_grain, real_str)}
, {sqlite_obj_str(respect_grain, real_str)}
, {sqlite_obj_str(knot, "TEXT")}
, {sqlite_obj_str(rational, integer_str)}
, {sqlite_obj_str(keeps_justified, integer_str)}
, {sqlite_obj_str(offtrack_fund, real_str)}
, {sqlite_obj_str(sum_healerunit_plans_fund_total, real_str)}
, {sqlite_obj_str(keeps_buildable, integer_str)}
, {sqlite_obj_str(tree_traverse_count, integer_str)}
)
;
"""


@dataclass
class ObjKeysHolder:
    spark_num: SparkInt = None
    face_name: FaceName = None
    moment_rope: MomentRope = None
    person_name: PersonName = None
    rope: RopeTerm = None
    reason_context: RopeTerm = None
    contact_name: ContactName = None
    membership: GroupTitle = None
    group_title: GroupTitle = None
    fact_rope: RopeTerm = None
    knot: KnotTerm = None


def insert_job_prnmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prnmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prncont(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_contact: ContactUnit,
):
    x_dict = copy_deepcopy(x_contact.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prncont_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prngrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prngrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prnawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["knot"] = x_objkeysholder.knot
    insert_sqlstr = create_prnawar_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prnfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["knot"] = x_objkeysholder.knot
    insert_sqlstr = create_prnfact_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prnheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerUnit,
):
    x_dict = {
        "moment_rope": x_objkeysholder.moment_rope,
        "person_name": x_objkeysholder.person_name,
        "plan_rope": x_objkeysholder.rope,
        "knot": x_objkeysholder.knot,
    }
    for healer_name in sorted(x_healer.healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_prnheal_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_prncase(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_caseunit: CaseUnit,
):
    x_dict = copy_deepcopy(x_caseunit.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["reason_context"] = x_objkeysholder.reason_context
    insert_sqlstr = create_prncase_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prnreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_prnreas_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prnlabo(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_workforceheir: WorkforceHeir,
):
    x_dict = copy_deepcopy(x_workforceheir.__dict__)
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["knot"] = x_objkeysholder.knot
    for labor_title in sorted(x_workforceheir.labors):
        laborheir = x_workforceheir.labors.get(labor_title)
        x_dict["labor_title"] = laborheir.labor_title
        x_dict["solo"] = laborheir.solo
        insert_sqlstr = create_prnlabo_metrics_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_job_prnplan(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_plan: PlanUnit
):
    x_dict = copy_deepcopy(x_plan.__dict__)
    x_dict["plan_rope"] = x_plan.get_plan_rope()
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prnplan_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_prnunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_person: PersonUnit
):
    x_dict = copy_deepcopy(x_person.__dict__)
    x_dict["moment_rope"] = x_person.planroot.get_plan_rope()
    insert_sqlstr = create_personunit_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_job_obj(cursor: sqlite3_Cursor, job_person: PersonUnit):
    job_person.conpute()
    x_objkeysholder = ObjKeysHolder(
        moment_rope=job_person.planroot.get_plan_rope(),
        person_name=job_person.person_name,
    )
    insert_job_prnunit(cursor, x_objkeysholder, job_person)
    for x_plan in job_person.get_plan_dict().values():
        x_objkeysholder.rope = x_plan.get_plan_rope()
        healerunit = x_plan.healerunit
        workforceheir = x_plan.workforceheir
        insert_job_prnplan(cursor, x_objkeysholder, x_plan)
        insert_job_prnheal(cursor, x_objkeysholder, healerunit)
        insert_job_prnlabo(cursor, x_objkeysholder, workforceheir)
        for x_awardheir in x_plan.awardheirs.values():
            insert_job_prnawar(cursor, x_objkeysholder, x_awardheir)
        for reason_context, reasonheir in x_plan.reasonheirs.items():
            insert_job_prnreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.reason_context = reason_context
            for prem in reasonheir.cases.values():
                insert_job_prncase(cursor, x_objkeysholder, prem)

    for x_contact in job_person.contacts.values():
        insert_job_prncont(cursor, x_objkeysholder, x_contact)
        for x_membership in x_contact.memberships.values():
            insert_job_prnmemb(cursor, x_objkeysholder, x_membership)

    for x_groupunit in job_person.groupunits.values():
        insert_job_prngrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_person.planroot.factheirs.values():
        x_objkeysholder.fact_rope = job_person.planroot.get_plan_rope()
        insert_job_prnfact(cursor, x_objkeysholder, x_factheir)


def create_prnawar_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    pass


def create_prncase_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    spark_num = values_dict.get("spark_num")
    face_name = values_dict.get("face_name")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    knot = values_dict.get("knot")
    reason_context = values_dict.get("reason_context")
    reason_state = values_dict.get("reason_state")
    reason_lower_otx = values_dict.get("reason_lower_otx")
    reason_upper_otx = values_dict.get("reason_upper_otx")
    reason_divisor = values_dict.get("reason_divisor")
    return f"""INSERT INTO person_plan_reason_caseunit_put_h_agg (spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower_otx, reason_upper_otx, reason_divisor, knot)
VALUES (
  {sqlite_obj_str(spark_num, "INTEGER")}
, {sqlite_obj_str(face_name, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(reason_state, "TEXT")}
, {sqlite_obj_str(reason_lower_otx, "REAL")}
, {sqlite_obj_str(reason_upper_otx, "REAL")}
, {sqlite_obj_str(reason_divisor, "REAL")}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prnfact_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    spark_num = values_dict.get("spark_num")
    face_name = values_dict.get("face_name")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    knot = values_dict.get("knot")
    fact_context = values_dict.get("fact_context")
    fact_state = values_dict.get("fact_state")
    fact_lower_otx = values_dict.get("fact_lower_otx")
    fact_upper_otx = values_dict.get("fact_upper_otx")
    return f"""INSERT INTO person_plan_factunit_put_h_agg (spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower_otx, fact_upper_otx, knot)
VALUES (
  {sqlite_obj_str(spark_num, "INTEGER")}
, {sqlite_obj_str(face_name, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(fact_context, "TEXT")}
, {sqlite_obj_str(fact_state, "TEXT")}
, {sqlite_obj_str(fact_lower_otx, "REAL")}
, {sqlite_obj_str(fact_upper_otx, "REAL")}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prngrou_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    pass


def create_prnheal_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    pass


def create_prnlabo_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    pass


def create_prnmemb_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    pass


def create_prnplan_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    spark_num = values_dict.get("spark_num")
    face_name = values_dict.get("face_name")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    knot = values_dict.get("knot")
    begin = values_dict.get("begin")
    close = values_dict.get("close")
    addin = values_dict.get("addin")
    numor = values_dict.get("numor")
    denom = values_dict.get("denom")
    morph = values_dict.get("morph")
    gogo_want = values_dict.get("gogo_want")
    stop_want = values_dict.get("stop_want")
    star = values_dict.get("star")
    pledge = values_dict.get("pledge")
    problem_bool = values_dict.get("problem_bool")
    integer_str = "INTEGER"
    real_str = "REAL"

    return f"""INSERT INTO person_planunit_put_h_agg (spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot)
VALUES (
  {sqlite_obj_str(spark_num, integer_str)}
, {sqlite_obj_str(face_name, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(begin, real_str)}
, {sqlite_obj_str(close, real_str)}
, {sqlite_obj_str(addin, real_str)}
, {sqlite_obj_str(numor, "INTEGER")}
, {sqlite_obj_str(denom, "INTEGER")}
, {sqlite_obj_str(morph, real_str)}
, {sqlite_obj_str(gogo_want, real_str)}
, {sqlite_obj_str(stop_want, real_str)}
, {sqlite_obj_str(star, real_str)}
, {sqlite_obj_str(pledge, real_str)}
, {sqlite_obj_str(problem_bool, "INTEGER")}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prnreas_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    spark_num = values_dict.get("spark_num")
    face_name = values_dict.get("face_name")
    person_name = values_dict.get("person_name")
    rope = values_dict.get("plan_rope")
    knot = values_dict.get("knot")
    reason_context = values_dict.get("reason_context")
    active_requisite = values_dict.get("active_requisite")
    return f"""INSERT INTO person_plan_reasonunit_put_h_agg (spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot)
VALUES (
  {sqlite_obj_str(spark_num, "INTEGER")}
, {sqlite_obj_str(face_name, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(rope, "TEXT")}
, {sqlite_obj_str(reason_context, "TEXT")}
, {sqlite_obj_str(active_requisite, "INTEGER")}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prnunit_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    spark_num = values_dict.get("spark_num")
    face_name = values_dict.get("face_name")
    moment_rope = values_dict.get("moment_rope")
    knot = values_dict.get("knot")
    person_name = values_dict.get("person_name")
    integer_str = "INTEGER"
    real_str = "REAL"
    credor_respect = values_dict.get("credor_respect")
    debtor_respect = values_dict.get("debtor_respect")
    fund_grain = values_dict.get("fund_grain")
    fund_pool = values_dict.get("fund_pool")
    max_tree_traverse = values_dict.get("max_tree_traverse")
    mana_grain = values_dict.get("mana_grain")
    respect_grain = values_dict.get("respect_grain")

    return f"""INSERT INTO personunit_put_h_agg (spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot)
VALUES (
  {sqlite_obj_str(spark_num, integer_str)}
, {sqlite_obj_str(face_name, "TEXT")}
, {sqlite_obj_str(moment_rope, "TEXT")}
, {sqlite_obj_str(person_name, "TEXT")}
, {sqlite_obj_str(credor_respect, real_str)}
, {sqlite_obj_str(debtor_respect, real_str)}
, {sqlite_obj_str(fund_pool, real_str)}
, {sqlite_obj_str(max_tree_traverse, integer_str)}
, {sqlite_obj_str(fund_grain, real_str)}
, {sqlite_obj_str(mana_grain, real_str)}
, {sqlite_obj_str(respect_grain, real_str)}
, {sqlite_obj_str(knot, "TEXT")}
)
;
"""


def create_prncont_put_h_agg_insert_sqlstr(values_dict: dict[str,]) -> str:
    pass


# def create_prnmemb_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     contact_name = values_dict.get("contact_name")
#     group_title = values_dict.get("group_title")
#     group_cred_lumen = values_dict.get("group_cred_lumen")
#     group_debt_lumen = values_dict.get("group_debt_lumen")
#     credor_pool = values_dict.get("credor_pool")
#     debtor_pool = values_dict.get("debtor_pool")
#     fund_give = values_dict.get("fund_give")
#     fund_take = values_dict.get("fund_take")
#     fund_agenda_give = values_dict.get("fund_agenda_give")
#     fund_agenda_take = values_dict.get("fund_agenda_take")
#     fund_agenda_ratio_give = values_dict.get("fund_agenda_ratio_give")
#     fund_agenda_ratio_take = values_dict.get("fund_agenda_ratio_take")
#     real_str = "REAL"
#     return f"""INSERT INTO person_contact_membership_put_h_agg (spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take, fund_agenda_ratio_give, fund_agenda_ratio_take)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(contact_name, "TEXT")}
# , {sqlite_obj_str(group_title, "TEXT")}
# , {sqlite_obj_str(group_cred_lumen, real_str)}
# , {sqlite_obj_str(group_debt_lumen, real_str)}
# , {sqlite_obj_str(credor_pool, real_str)}
# , {sqlite_obj_str(debtor_pool, real_str)}
# , {sqlite_obj_str(fund_give, real_str)}
# , {sqlite_obj_str(fund_take, real_str)}
# , {sqlite_obj_str(fund_agenda_give, real_str)}
# , {sqlite_obj_str(fund_agenda_take, real_str)}
# , {sqlite_obj_str(fund_agenda_ratio_give, real_str)}
# , {sqlite_obj_str(fund_agenda_ratio_take, real_str)}
# )
# ;
# """


# def create_prncont_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     contact_name = values_dict.get("contact_name")
#     contact_cred_lumen = values_dict.get("contact_cred_lumen")
#     contact_debt_lumen = values_dict.get("contact_debt_lumen")
#     groupmark = values_dict.get("groupmark")
#     credor_pool = values_dict.get("credor_pool")
#     debtor_pool = values_dict.get("debtor_pool")
#     fund_give = values_dict.get("fund_give")
#     fund_take = values_dict.get("fund_take")
#     fund_agenda_give = values_dict.get("fund_agenda_give")
#     fund_agenda_take = values_dict.get("fund_agenda_take")
#     fund_agenda_ratio_give = values_dict.get("fund_agenda_ratio_give")
#     fund_agenda_ratio_take = values_dict.get("fund_agenda_ratio_take")
#     inallocable_contact_debt_lumen = values_dict.get("inallocable_contact_debt_lumen")
#     irrational_contact_debt_lumen = values_dict.get("irrational_contact_debt_lumen")
#     real_str = "REAL"
#     return f"""INSERT INTO person_contactunit_put_h_agg (spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, groupmark, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take, fund_agenda_ratio_give, fund_agenda_ratio_take, inallocable_contact_debt_lumen, irrational_contact_debt_lumen)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(contact_name, "TEXT")}
# , {sqlite_obj_str(contact_cred_lumen, real_str)}
# , {sqlite_obj_str(contact_debt_lumen, real_str)}
# , {sqlite_obj_str(groupmark, "TEXT")}
# , {sqlite_obj_str(credor_pool, real_str)}
# , {sqlite_obj_str(debtor_pool, real_str)}
# , {sqlite_obj_str(fund_give, real_str)}
# , {sqlite_obj_str(fund_take, real_str)}
# , {sqlite_obj_str(fund_agenda_give, real_str)}
# , {sqlite_obj_str(fund_agenda_take, real_str)}
# , {sqlite_obj_str(fund_agenda_ratio_give, real_str)}
# , {sqlite_obj_str(fund_agenda_ratio_take, real_str)}
# , {sqlite_obj_str(inallocable_contact_debt_lumen, real_str)}
# , {sqlite_obj_str(irrational_contact_debt_lumen, real_str)}
# )
# ;
# """


# def create_prngrou_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     group_title = values_dict.get("group_title")
#     credor_pool = values_dict.get("credor_pool")
#     debtor_pool = values_dict.get("debtor_pool")
#     fund_grain = values_dict.get("fund_grain")
#     fund_give = values_dict.get("fund_give")
#     fund_take = values_dict.get("fund_take")
#     fund_agenda_give = values_dict.get("fund_agenda_give")
#     fund_agenda_take = values_dict.get("fund_agenda_take")
#     real_str = "REAL"
#     return f"""INSERT INTO person_groupunit_put_h_agg (spark_num, face_name, moment_rope, person_name, group_title, fund_grain, credor_pool, debtor_pool, fund_give, fund_take, fund_agenda_give, fund_agenda_take)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(group_title, "TEXT")}
# , {sqlite_obj_str(fund_grain, real_str)}
# , {sqlite_obj_str(credor_pool, real_str)}
# , {sqlite_obj_str(debtor_pool, real_str)}
# , {sqlite_obj_str(fund_give, real_str)}
# , {sqlite_obj_str(fund_take, real_str)}
# , {sqlite_obj_str(fund_agenda_give, real_str)}
# , {sqlite_obj_str(fund_agenda_take, real_str)}
# )
# ;
# """


# def create_prnawar_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     rope = values_dict.get("plan_rope")
#     awardee_title = values_dict.get("awardee_title")
#     give_force = values_dict.get("give_force")
#     take_force = values_dict.get("take_force")
#     fund_give = values_dict.get("fund_give")
#     fund_take = values_dict.get("fund_take")
#     return f"""INSERT INTO person_plan_awardunit_put_h_agg (spark_num, face_name, moment_rope, person_name, plan_rope, awardee_title, give_force, take_force, fund_give, fund_take)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(rope, "TEXT")}
# , {sqlite_obj_str(awardee_title, "TEXT")}
# , {sqlite_obj_str(give_force, "REAL")}
# , {sqlite_obj_str(take_force, "REAL")}
# , {sqlite_obj_str(fund_give, "REAL")}
# , {sqlite_obj_str(fund_take, "REAL")}
# )
# ;
# """


# def create_prnfact_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     rope = values_dict.get("plan_rope")
#     fact_context = values_dict.get("fact_context")
#     fact_state = values_dict.get("fact_state")
#     fact_lower = values_dict.get("fact_lower")
#     fact_upper = values_dict.get("fact_upper")
#     return f"""INSERT INTO person_plan_factunit_put_h_agg (spark_num, face_name, moment_rope, person_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(rope, "TEXT")}
# , {sqlite_obj_str(fact_context, "TEXT")}
# , {sqlite_obj_str(fact_state, "TEXT")}
# , {sqlite_obj_str(fact_lower, "REAL")}
# , {sqlite_obj_str(fact_upper, "REAL")}
# )
# ;
# """


# def create_prnheal_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     rope = values_dict.get("plan_rope")
#     healer_name = values_dict.get("healer_name")
#     return f"""INSERT INTO person_plan_healerunit_put_h_agg (spark_num, face_name, moment_rope, person_name, plan_rope, healer_name)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(rope, "TEXT")}
# , {sqlite_obj_str(healer_name, "TEXT")}
# )
# ;
# """


# def create_prnreas_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     rope = values_dict.get("plan_rope")
#     reason_context = values_dict.get("reason_context")
#     active_requisite = values_dict.get("active_requisite")
#     case_task = values_dict.get("case_task")
#     reason_active = values_dict.get("reason_active")
#     parent_heir_active = values_dict.get("parent_heir_active")
#     return f"""INSERT INTO person_plan_reasonunit_put_h_agg (spark_num, face_name, moment_rope, person_name, plan_rope, reason_context, active_requisite, reason_task, reason_active, parent_heir_active)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(rope, "TEXT")}
# , {sqlite_obj_str(reason_context, "TEXT")}
# , {sqlite_obj_str(active_requisite, "INTEGER")}
# , {sqlite_obj_str(case_task, "INTEGER")}
# , {sqlite_obj_str(reason_active, "INTEGER")}
# , {sqlite_obj_str(parent_heir_active, "INTEGER")}
# )
# ;
# """


# def create_prnlabo_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     rope = values_dict.get("plan_rope")
#     labor_title = values_dict.get("labor_title")
#     solo = values_dict.get("solo")
#     person_name_is_workforce = values_dict.get("person_name_is_workforce")
#     return f"""INSERT INTO person_plan_laborunit_put_h_agg (spark_num, face_name, moment_rope, person_name, plan_rope, labor_title, solo, person_name_is_workforce)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(rope, "TEXT")}
# , {sqlite_obj_str(labor_title, "TEXT")}
# , {sqlite_obj_str(solo, "INTEGER")}
# , {sqlite_obj_str(person_name_is_workforce, "INTEGER")}
# )
# ;
# """


# def create_prnplan_metrics_insert_sqlstr(values_dict: dict[str,]):
#     moment_rope = values_dict.get("moment_rope")
#     person_name = values_dict.get("person_name")
#     rope = values_dict.get("plan_rope")
#     begin = values_dict.get("begin")
#     close = values_dict.get("close")
#     addin = values_dict.get("addin")
#     numor = values_dict.get("numor")
#     denom = values_dict.get("denom")
#     morph = values_dict.get("morph")
#     gogo_want = values_dict.get("gogo_want")
#     stop_want = values_dict.get("stop_want")
#     star = values_dict.get("star")
#     pledge = values_dict.get("pledge")
#     problem_bool = values_dict.get("problem_bool")
#     active = values_dict.get("plan_active")
#     case_task = values_dict.get("case_task")
#     fund_grain = values_dict.get("fund_grain")
#     fund_onset = values_dict.get("fund_onset")
#     fund_cease = values_dict.get("fund_cease")
#     fund_ratio = values_dict.get("fund_ratio")
#     gogo_calc = values_dict.get("gogo_calc")
#     stop_calc = values_dict.get("stop_calc")
#     tree_level = values_dict.get("tree_level")
#     range_evaluated = values_dict.get("range_evaluated")
#     descendant_pledge_count = values_dict.get("descendant_pledge_count")
#     healerunit_ratio = values_dict.get("healerunit_ratio")
#     all_contact_cred = values_dict.get("all_contact_cred")
#     all_contact_debt = values_dict.get("all_contact_debt")
#     integer_str = "INTEGER"
#     real_str = "REAL"

#     return f"""INSERT INTO person_planunit_put_h_agg (spark_num, face_name, moment_rope, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, fund_grain, plan_active, case_task, fund_onset, fund_cease, fund_ratio, gogo_calc, stop_calc, tree_level, range_evaluated, descendant_pledge_count, healerunit_ratio, all_contact_cred, all_contact_debt)
# VALUES (
#   {sqlite_obj_str(spark_num, "INTEGER")}
# , {sqlite_obj_str(face_name, "TEXT")}
# , {sqlite_obj_str(moment_rope, "TEXT")}
# , {sqlite_obj_str(person_name, "TEXT")}
# , {sqlite_obj_str(rope, "TEXT")}
# , {sqlite_obj_str(begin, real_str)}
# , {sqlite_obj_str(close, real_str)}
# , {sqlite_obj_str(addin, real_str)}
# , {sqlite_obj_str(numor, "INTEGER")}
# , {sqlite_obj_str(denom, "INTEGER")}
# , {sqlite_obj_str(morph, real_str)}
# , {sqlite_obj_str(gogo_want, real_str)}
# , {sqlite_obj_str(stop_want, real_str)}
# , {sqlite_obj_str(star, real_str)}
# , {sqlite_obj_str(pledge, real_str)}
# , {sqlite_obj_str(problem_bool, "INTEGER")}
# , {sqlite_obj_str(fund_grain, real_str)}
# , {sqlite_obj_str(active, "INTEGER")}
# , {sqlite_obj_str(case_task, "INTEGER")}
# , {sqlite_obj_str(fund_onset, real_str)}
# , {sqlite_obj_str(fund_cease, real_str)}
# , {sqlite_obj_str(fund_ratio, real_str)}
# , {sqlite_obj_str(gogo_calc, real_str)}
# , {sqlite_obj_str(stop_calc, real_str)}
# , {sqlite_obj_str(tree_level, "INTEGER")}
# , {sqlite_obj_str(range_evaluated, "INTEGER")}
# , {sqlite_obj_str(descendant_pledge_count, "INTEGER")}
# , {sqlite_obj_str(healerunit_ratio, real_str)}
# , {sqlite_obj_str(all_contact_cred, real_str)}
# , {sqlite_obj_str(all_contact_debt, real_str)}
# )
# ;
# """


def insert_h_agg_prnmemb(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_membership: MemberShip,
):
    x_dict = copy_deepcopy(x_membership.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prnmemb_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prncont(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_contact: ContactUnit,
):
    x_dict = copy_deepcopy(x_contact.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prncont_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prngrou(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_groupunit: GroupUnit,
):
    x_dict = copy_deepcopy(x_groupunit.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prngrou_metrics_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prnawar(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_awardheir: AwardHeir,
):
    x_dict = copy_deepcopy(x_awardheir.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_prnawar_put_h_agg_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prnfact(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_factheir: FactHeir,
):
    x_dict = copy_deepcopy(x_factheir.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["knot"] = x_objkeysholder.knot
    x_dict["fact_upper_otx"] = x_dict["fact_upper"]
    x_dict["fact_lower_otx"] = x_dict["fact_lower"]
    insert_sqlstr = create_prnfact_put_h_agg_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prnheal(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_healer: HealerUnit,
):
    x_dict = {
        "moment_rope": x_objkeysholder.moment_rope,
        "person_name": x_objkeysholder.person_name,
        "plan_rope": x_objkeysholder.rope,
    }
    for healer_name in sorted(x_healer.healer_names):
        x_dict["healer_name"] = healer_name
        insert_sqlstr = create_prnheal_put_h_agg_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_h_agg_prncase(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_caseunit: CaseUnit,
):
    x_dict = copy_deepcopy(x_caseunit.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    x_dict["reason_context"] = x_objkeysholder.reason_context
    x_dict["reason_lower_otx"] = x_dict["reason_lower"]
    x_dict["reason_upper_otx"] = x_dict["reason_upper"]
    insert_sqlstr = create_prncase_put_h_agg_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prnreas(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_reasonheir: ReasonHeir,
):
    x_dict = copy_deepcopy(x_reasonheir.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    insert_sqlstr = create_prnreas_put_h_agg_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prnlabo(
    cursor: sqlite3_Cursor,
    x_objkeysholder: ObjKeysHolder,
    x_workforceheir: WorkforceHeir,
):
    x_dict = copy_deepcopy(x_workforceheir.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_objkeysholder.moment_rope
    x_dict["person_name"] = x_objkeysholder.person_name
    x_dict["plan_rope"] = x_objkeysholder.rope
    for labor_title in sorted(x_workforceheir.labors):
        laborheir = x_workforceheir.labors.get(labor_title)
        x_dict["labor_title"] = laborheir.labor_title
        x_dict["solo"] = laborheir.solo
        insert_sqlstr = create_prnlabo_put_h_agg_insert_sqlstr(x_dict)
        cursor.execute(insert_sqlstr)


def insert_h_agg_prnplan(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_plan: PlanUnit
):
    x_dict = copy_deepcopy(x_plan.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["plan_rope"] = x_plan.get_plan_rope()
    x_dict["person_name"] = x_objkeysholder.person_name
    insert_sqlstr = create_prnplan_put_h_agg_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_prnunit(
    cursor: sqlite3_Cursor, x_objkeysholder: ObjKeysHolder, x_person: PersonUnit
):
    x_dict = copy_deepcopy(x_person.__dict__)
    x_dict["spark_num"] = x_objkeysholder.spark_num
    x_dict["face_name"] = x_objkeysholder.face_name
    x_dict["moment_rope"] = x_person.planroot.get_plan_rope()
    insert_sqlstr = create_prnunit_put_h_agg_insert_sqlstr(x_dict)
    cursor.execute(insert_sqlstr)


def insert_h_agg_obj(
    cursor: sqlite3_Cursor,
    job_person: PersonUnit,
    spark_num: SparkInt,
    face_name: FaceName,
):
    """Given database cursor and PersonUnit obj insert obj attributes into h_agg tables"""
    job_person.conpute()
    x_objkeysholder = ObjKeysHolder(
        spark_num=spark_num,
        face_name=face_name,
        moment_rope=job_person.planroot.get_plan_rope(),
        person_name=job_person.person_name,
    )
    insert_h_agg_prnunit(cursor, x_objkeysholder, job_person)
    for x_plan in job_person.get_plan_dict().values():
        x_objkeysholder.rope = x_plan.get_plan_rope()
        insert_h_agg_prnplan(cursor, x_objkeysholder, x_plan)
        # healerunit = x_plan.healerunit
        # workforceheir = x_plan.workforceheir
        # insert_h_agg_prnheal(cursor, x_objkeysholder, healerunit)
        # insert_h_agg_prnlabo(cursor, x_objkeysholder, workforceheir)
        # for x_awardheir in x_plan.awardheirs.values():
        #     insert_h_agg_prnawar(cursor, x_objkeysholder, x_awardheir)
        for reason_context, reasonheir in x_plan.reasonheirs.items():
            insert_h_agg_prnreas(cursor, x_objkeysholder, reasonheir)
            x_objkeysholder.reason_context = reason_context
            for prem in reasonheir.cases.values():
                insert_h_agg_prncase(cursor, x_objkeysholder, prem)

    # for x_contact in job_person.contacts.values():
    #     insert_h_agg_prncont(cursor, x_objkeysholder, x_contact)
    #     for x_membership in x_contact.memberships.values():
    #         insert_h_agg_prnmemb(cursor, x_objkeysholder, x_membership)

    # for x_groupunit in job_person.groupunits.values():
    #     insert_h_agg_prngrou(cursor, x_objkeysholder, x_groupunit)

    for x_factheir in job_person.planroot.factheirs.values():
        x_objkeysholder.fact_rope = job_person.planroot.get_plan_rope()
        insert_h_agg_prnfact(cursor, x_objkeysholder, x_factheir)
