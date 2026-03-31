from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_row_count
from src.ch02_partner.group import (
    awardheir_shop,
    awardunit_shop,
    groupunit_shop,
    membership_shop,
)
from src.ch02_partner.partner import partnerunit_shop
from src.ch03_labor.labor import laborheir_shop, laborunit_shop, partyheir_shop
from src.ch04_rope.rope import create_rope
from src.ch05_reason.reason_main import caseunit_shop, factheir_shop, reasonheir_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch18_etl_config.etl_sqlstr import create_job_tables
from src.ch19_etl_main.obj2db_person import (
    ObjKeysHolder,
    insert_job_obj,
    insert_job_prnawar,
    insert_job_prncase,
    insert_job_prnfact,
    insert_job_prngrou,
    insert_job_prnheal,
    insert_job_prnlabo,
    insert_job_prnmemb,
    insert_job_prnplan,
    insert_job_prnptnr,
    insert_job_prnreas,
    insert_job_prnunit,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_ObjKeysHolder_Exists():
    # ESTABLISH / WHEN
    x_objkeyholder = ObjKeysHolder()

    # THEN
    assert not x_objkeyholder.moment_rope
    assert not x_objkeyholder.person_name
    assert not x_objkeyholder.rope
    assert not x_objkeyholder.reason_context
    assert not x_objkeyholder.partner_name
    assert not x_objkeyholder.membership
    assert not x_objkeyholder.group_title
    assert not x_objkeyholder.fact_rope


def test_insert_job_prnunit_CreatesTableRowsFor_personunit_job(cursor0: Cursor):
    # ESTABLISH
    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_keeps_buildable = 99
    x_keeps_justified = 77
    x_offtrack_fund = 55.5
    x_rational = 92
    x_sum_healerunit_plans_fund_total = 66.6
    x_tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_mana_grain = 4.0
    x_respect_grain = 0.2
    sue_person = personunit_shop(x_person_name, x_moment_rope)
    sue_person.fund_pool = x_fund_pool
    sue_person.fund_grain = x_fund_grain
    sue_person.mana_grain = x_mana_grain
    sue_person.respect_grain = x_respect_grain
    sue_person.max_tree_traverse = x_max_tree_traverse
    sue_person.keeps_buildable = x_keeps_buildable
    sue_person.keeps_justified = x_keeps_justified
    sue_person.offtrack_fund = x_offtrack_fund
    sue_person.rational = x_rational
    sue_person.sum_healerunit_plans_fund_total = x_sum_healerunit_plans_fund_total
    sue_person.tree_traverse_count = x_tree_traverse_count
    sue_person.credor_respect = x_credor_respect
    sue_person.debtor_respect = x_debtor_respect
    sue_person.knot = x_knot

    create_job_tables(cursor0)
    x_table_name = "personunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    objkeysholder = ObjKeysHolder()

    # WHEN
    insert_job_prnunit(cursor0, objkeysholder, sue_person)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    print(f"{select_sqlstr=}")
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        x_moment_rope,
        x_person_name,
        x_credor_respect,
        x_debtor_respect,
        x_fund_pool,
        x_max_tree_traverse,
        x_fund_grain,
        x_mana_grain,
        x_respect_grain,
        x_knot,
        x_rational,
        x_keeps_justified,
        x_offtrack_fund,
        x_sum_healerunit_plans_fund_total,
        x_keeps_buildable,
        x_tree_traverse_count,
    )
    expected_data = [expected_row0]
    assert rows == expected_data


def test_insert_job_prnplan_CreatesTableRowsFor_prnplan_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_planunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_plan.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")
    # print("")
    x_moment_rope = exx.a23_slash
    x_knot = exx.slash
    x_person_name = 2
    casa_rope = create_rope(x_moment_rope, "casa", x_knot)
    x_parent_rope = casa_rope
    x_plan_label = "clean"
    x_begin = 5.0
    x_close = 6.0
    x_addin = 7.0
    x_numor = 8
    x_denom = 9
    x_morph = 10
    x_gogo_want = 11.0
    x_stop_want = 12.0
    x_star = 13
    x_pledge = 14
    x_problem_bool = 15
    x_active = 16
    x_plan_task = 17
    x_fund_grain = 18.0
    x_fund_onset = 19.0
    x_fund_cease = 20.0
    x_fund_ratio = 21.0
    x_gogo_calc = 22.0
    x_stop_calc = 23.0
    x_level = 24
    x_range_evaluated = 25
    x_descendant_pledge_count = 26
    x_healerunit_ratio = 27.0
    x_all_partner_cred = 28
    x_all_partner_debt = 29
    x_plan = planunit_shop(exx.casa)
    x_plan.parent_rope = x_parent_rope
    x_plan.knot = x_knot
    x_plan.plan_label = x_plan_label
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.star = x_star
    x_plan.pledge = x_pledge
    x_plan.problem_bool = x_problem_bool
    x_plan.plan_active = x_active
    x_plan.plan_task = x_plan_task
    x_plan.fund_grain = x_fund_grain
    x_plan.fund_onset = x_fund_onset
    x_plan.fund_cease = x_fund_cease
    x_plan.fund_ratio = x_fund_ratio
    x_plan.gogo_calc = x_gogo_calc
    x_plan.stop_calc = x_stop_calc
    x_plan.tree_level = x_level
    x_plan.range_evaluated = x_range_evaluated
    x_plan.descendant_pledge_count = x_descendant_pledge_count
    x_plan.healerunit_ratio = x_healerunit_ratio
    x_plan.all_partner_cred = x_all_partner_cred
    x_plan.all_partner_debt = x_all_partner_debt
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.star = x_star
    x_plan.pledge = x_pledge
    x_plan.problem_bool = x_problem_bool
    x_plan.plan_active = x_active
    x_plan.plan_task = x_plan_task
    x_plan.fund_grain = x_fund_grain
    x_plan.fund_onset = x_fund_onset
    x_plan.fund_cease = x_fund_cease
    x_plan.fund_ratio = x_fund_ratio
    x_plan.gogo_calc = x_gogo_calc
    x_plan.stop_calc = x_stop_calc
    x_plan.tree_level = x_level
    x_plan.range_evaluated = x_range_evaluated
    x_plan.descendant_pledge_count = x_descendant_pledge_count
    x_plan.healerunit_ratio = x_healerunit_ratio
    x_plan.all_partner_cred = x_all_partner_cred
    x_plan.all_partner_debt = x_all_partner_debt

    create_job_tables(cursor0)
    x_table_name = "person_planunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name
    )

    # WHEN
    insert_job_prnplan(cursor0, x_objkeysholder, x_plan)

    # THEN
    clean_rope = create_rope(casa_rope, "clean", x_knot)
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        None,
        str(x_person_name),
        clean_rope,
        x_begin,
        x_close,
        x_addin,
        x_numor,
        x_denom,
        x_morph,
        x_gogo_want,
        x_stop_want,
        x_star,
        x_pledge,
        x_problem_bool,
        x_fund_grain,
        x_knot,
        x_active,
        x_plan_task,
        x_fund_onset,
        x_fund_cease,
        x_fund_ratio,
        x_gogo_calc,
        x_stop_calc,
        x_level,
        x_range_evaluated,
        x_descendant_pledge_count,
        x_healerunit_ratio,
        x_all_partner_cred,
        x_all_partner_debt,
    )
    assert rows[0] == expected_row0


def test_insert_job_prnreas_CreatesTableRowsFor_prnreas_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_plan_reasonunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_reasonunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")
    # print("")

    x_moment_rope = 1
    x_knot = exx.slash
    x_person_name = 2
    x_rope = 3
    x_reason_context = 4
    x_active_requisite = 5
    x_reason_active = 6
    x_reason_task = 7
    x_heir_active = 8
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.active_requisite = x_active_requisite
    x_reasonheir.reason_task = x_reason_task
    x_reasonheir.reason_active = x_reason_active
    x_reasonheir.parent_heir_active = x_heir_active
    x_reasonheir.knot = x_knot

    create_job_tables(cursor0)
    x_table_name = "person_plan_reasonunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name, rope=x_rope
    )

    # WHEN
    insert_job_prnreas(cursor0, x_objkeysholder, x_reasonheir)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        str(x_reason_context),
        x_active_requisite,
        x_knot,
        x_reason_active,
        x_reason_task,
        x_heir_active,
    )
    expected_data = [expected_row0]
    assert rows == expected_data


def test_insert_job_prncase_CreatesTableRowsFor_prncase_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_plan_reason_caseunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_caseunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_knot = exx.slash
    x_person_name = 2
    x_rope = 3
    x_reason_context = 4
    x_reason_state = 5
    x_reason_lower = 7.0
    x_reason_upper = 6.0
    x_reason_divisor = 8
    x_case_task = 9
    x_case_active = 10
    x_caseunit = caseunit_shop(reason_state=x_reason_state)
    x_caseunit.reason_state = x_reason_state
    x_caseunit.reason_lower = x_reason_lower
    x_caseunit.reason_upper = x_reason_upper
    x_caseunit.reason_divisor = x_reason_divisor
    x_caseunit.case_task = x_case_task
    x_caseunit.case_active = x_case_active
    x_caseunit.knot = x_knot

    create_job_tables(cursor0)
    x_table_name = "person_plan_reason_caseunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope,
        person_name=x_person_name,
        rope=x_rope,
        reason_context=x_reason_context,
    )

    # WHEN
    insert_job_prncase(cursor0, x_objkeysholder, x_caseunit)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        str(x_reason_context),
        str(x_reason_state),
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_knot,
        x_case_task,
        x_case_active,
    )
    assert rows[0] == expected_row0


def test_insert_job_prnmemb_CreatesTableRowsFor_prnmemb_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_partner_membership")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_membership.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_person_name = 2
    x_partner_name = 3
    x_group_title = 4
    x_group_cred_lumen = 5.0
    x_group_debt_lumen = 6.0
    x_credor_pool = 7.0
    x_debtor_pool = 8.0
    x_fund_give = 9.0
    x_fund_take = 10.0
    x_fund_agenda_give = 11.0
    x_fund_agenda_take = 12.0
    x_fund_agenda_ratio_give = 13.0
    x_fund_agenda_ratio_take = 14.0
    x_membership = membership_shop(x_group_title)
    x_membership.partner_name = x_partner_name
    x_membership.group_cred_lumen = x_group_cred_lumen
    x_membership.group_debt_lumen = x_group_debt_lumen
    x_membership.credor_pool = x_credor_pool
    x_membership.debtor_pool = x_debtor_pool
    x_membership.fund_give = x_fund_give
    x_membership.fund_take = x_fund_take
    x_membership.fund_agenda_give = x_fund_agenda_give
    x_membership.fund_agenda_take = x_fund_agenda_take
    x_membership.fund_agenda_ratio_give = x_fund_agenda_ratio_give
    x_membership.fund_agenda_ratio_take = x_fund_agenda_ratio_take

    create_job_tables(cursor0)
    x_table_name = "person_partner_membership_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name
    )

    # WHEN
    insert_job_prnmemb(cursor0, x_objkeysholder, x_membership)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_partner_name),
        str(x_group_title),
        x_group_cred_lumen,
        x_group_debt_lumen,
        x_credor_pool,
        x_debtor_pool,
        x_fund_give,
        x_fund_take,
        x_fund_agenda_give,
        x_fund_agenda_take,
        x_fund_agenda_ratio_give,
        x_fund_agenda_ratio_take,
    )
    expected_data = [expected_row0]
    assert rows == expected_data


def test_insert_job_prnptnr_CreatesTableRowsFor_prnptnr_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_partnerunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_partner.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_person_name = 2
    x_partner_name = 3
    x_partner_cred_lumen = 4
    x_partner_debt_lumen = 5
    x_credor_pool = 6
    x_debtor_pool = 7
    x_fund_give = 8
    x_fund_take = 9
    x_fund_agenda_give = 10
    x_fund_agenda_take = 11
    x_fund_agenda_ratio_give = 12
    x_fund_agenda_ratio_take = 13
    x_inallocable_partner_debt_lumen = 14
    x_irrational_partner_debt_lumen = 15
    x_groupmark = 16
    x_partner = partnerunit_shop(x_partner_name)
    x_partner.partner_name = x_partner_name
    x_partner.partner_cred_lumen = x_partner_cred_lumen
    x_partner.partner_debt_lumen = x_partner_debt_lumen
    x_partner.credor_pool = x_credor_pool
    x_partner.debtor_pool = x_debtor_pool
    x_partner.fund_give = x_fund_give
    x_partner.fund_take = x_fund_take
    x_partner.fund_agenda_give = x_fund_agenda_give
    x_partner.fund_agenda_take = x_fund_agenda_take
    x_partner.fund_agenda_ratio_give = x_fund_agenda_ratio_give
    x_partner.fund_agenda_ratio_take = x_fund_agenda_ratio_take
    x_partner.inallocable_partner_debt_lumen = x_inallocable_partner_debt_lumen
    x_partner.irrational_partner_debt_lumen = x_irrational_partner_debt_lumen
    x_partner.groupmark = x_groupmark

    create_job_tables(cursor0)
    x_table_name = "person_partnerunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name
    )

    # WHEN
    insert_job_prnptnr(cursor0, x_objkeysholder, x_partner)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_partner_name),
        x_partner_cred_lumen,
        x_partner_debt_lumen,
        str(x_groupmark),
        x_credor_pool,
        x_debtor_pool,
        x_fund_give,
        x_fund_take,
        x_fund_agenda_give,
        x_fund_agenda_take,
        x_fund_agenda_ratio_give,
        x_fund_agenda_ratio_take,
        x_inallocable_partner_debt_lumen,
        x_irrational_partner_debt_lumen,
    )
    expected_data = [expected_row0]
    assert rows == expected_data


def test_insert_job_prngrou_CreatesTableRowsFor_prngrou_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_groupunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_group.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_person_name = 2
    x_group_title = 3
    x_fund_grain = 4
    x_credor_pool = 6
    x_debtor_pool = 7
    x_fund_give = 8
    x_fund_take = 9
    x_fund_agenda_give = 10
    x_fund_agenda_take = 11
    x_group = groupunit_shop(x_group_title)
    x_group.group_title = x_group_title
    x_group.fund_grain = x_fund_grain
    x_group.credor_pool = x_credor_pool
    x_group.debtor_pool = x_debtor_pool
    x_group.fund_give = x_fund_give
    x_group.fund_take = x_fund_take
    x_group.fund_agenda_give = x_fund_agenda_give
    x_group.fund_agenda_take = x_fund_agenda_take

    create_job_tables(cursor0)
    x_table_name = "person_groupunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name
    )

    # WHEN
    insert_job_prngrou(cursor0, x_objkeysholder, x_group)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_group_title),
        x_fund_grain,
        x_credor_pool,
        x_debtor_pool,
        x_fund_give,
        x_fund_take,
        x_fund_agenda_give,
        x_fund_agenda_take,
    )
    expected_data = [expected_row0]
    assert rows == expected_data


def test_insert_job_prnawar_CreatesTableRowsFor_prnawar_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_plan_awardunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_awardheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_knot = exx.slash
    x_person_name = 2
    x_rope = 3
    x_awardee_title = 4
    x_give_force = 5
    x_take_force = 6
    x_fund_give = 7
    x_fund_take = 8
    x_awardheir = awardheir_shop(x_awardee_title)
    x_awardheir.awardee_title = x_awardee_title
    x_awardheir.give_force = x_give_force
    x_awardheir.take_force = x_take_force
    x_awardheir.fund_give = x_fund_give
    x_awardheir.fund_take = x_fund_take

    create_job_tables(cursor0)
    x_table_name = "person_plan_awardunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name, rope=x_rope, knot=x_knot
    )

    # WHEN
    insert_job_prnawar(cursor0, x_objkeysholder, x_awardheir)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        str(x_awardee_title),
        x_give_force,
        x_take_force,
        x_knot,
        x_fund_give,
        x_fund_take,
    )
    assert rows[0] == expected_row0


def test_insert_job_prnfact_CreatesTableRowsFor_prnfact_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_plan_factunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_factheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_knot = exx.slash
    x_person_name = 2
    x_rope = 3
    x_reason_context = 4
    x_fact_state = 5
    x_fact_lower = 6
    x_fact_upper = 7
    x_factheir = factheir_shop()
    x_factheir.fact_context = x_reason_context
    x_factheir.fact_state = x_fact_state
    x_factheir.fact_lower = x_fact_lower
    x_factheir.fact_upper = x_fact_upper

    create_job_tables(cursor0)
    x_table_name = "person_plan_factunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name, rope=x_rope, knot=x_knot
    )

    # WHEN
    insert_job_prnfact(cursor0, x_objkeysholder, x_factheir)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        str(x_reason_context),
        str(x_fact_state),
        x_fact_lower,
        x_fact_upper,
        x_knot,
    )
    assert rows[0] == expected_row0


def test_insert_job_prnheal_CreatesTableRowsFor_prnheal_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_plan_healerunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_healerunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_knot = exx.slash
    x_person_name = 2
    x_rope = 3
    x_healerunit = healerunit_shop()
    x_healerunit.set_healer_name(exx.bob)
    x_healerunit.set_healer_name(exx.sue)

    create_job_tables(cursor0)
    x_table_name = "person_plan_healerunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name, rope=x_rope, knot=x_knot
    )

    # WHEN
    insert_job_prnheal(cursor0, x_objkeysholder, x_healerunit)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 2
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        exx.bob,
        x_knot,
    )
    expected_row1 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        exx.sue,
        x_knot,
    )
    expected_data = [expected_row0, expected_row1]
    assert rows == expected_data


def test_insert_job_prnlabo_CreatesTableRowsFor_prnlabo_job(cursor0: Cursor):
    # ESTABLISH
    # x_args = get_person_calc_dimen_args("person_plan_partyunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_laborheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""        x_{x_arg},""")

    x_moment_rope = 1
    x_knot = exx.slash
    x_person_name = 2
    x_rope = 3
    x_person_name_is_labor = 5
    x_laborheir = laborheir_shop()
    x_laborheir.person_name_is_labor = x_person_name_is_labor
    bob_solo_bool = 6
    sue_solo_bool = 7
    bob_partyheir = partyheir_shop(exx.bob, bob_solo_bool)
    sue_partyheir = partyheir_shop(exx.sue, sue_solo_bool)
    x_laborheir.partys = {exx.bob: bob_partyheir, exx.sue: sue_partyheir}

    create_job_tables(cursor0)
    x_table_name = "person_plan_partyunit_job"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        moment_rope=x_moment_rope, person_name=x_person_name, rope=x_rope, knot=x_knot
    )

    # WHEN
    insert_job_prnlabo(cursor0, x_objkeysholder, x_laborheir)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 2
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        exx.bob,
        bob_solo_bool,
        x_knot,
        x_person_name_is_labor,
    )
    expected_row1 = (
        str(x_moment_rope),
        str(x_person_name),
        str(x_rope),
        exx.sue,
        sue_solo_bool,
        x_knot,
        x_person_name_is_labor,
    )
    expected_data = [expected_row0, expected_row1]
    assert rows == expected_data


def test_insert_job_obj_CreatesTableRows_Scenario0(cursor0: Cursor):
    # ESTABLISH
    sue_person = personunit_shop(exx.sue, exx.a23)
    sue_person.add_partnerunit(exx.sue)
    sue_person.add_partnerunit(exx.bob)
    sue_person.get_partner(exx.bob).add_membership(exx.run)
    casa_rope = sue_person.make_l1_rope("casa")
    situation_rope = sue_person.make_l1_rope(kw.reason_active)
    clean_rope = sue_person.make_rope(situation_rope, "clean")
    dirty_rope = sue_person.make_rope(situation_rope, "dirty")
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    sue_person.add_plan(dirty_rope)
    sue_person.edit_plan_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_person.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run))
    sue_person.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    casa_laborunit = laborunit_shop()
    casa_laborunit.add_party(exx.sue, True)
    sue_person.edit_plan_attr(casa_rope, laborunit=casa_laborunit)
    sue_person.add_fact(situation_rope, clean_rope)

    create_job_tables(cursor0)
    prnmemb_job_table = f"{kw.person_partner_membership}_job"
    prnptnr_job_table = f"{kw.person_partnerunit}_job"
    prngrou_job_table = f"{kw.person_groupunit}_job"
    prnawar_job_table = f"{kw.person_plan_awardunit}_job"
    prnfact_job_table = f"{kw.person_plan_factunit}_job"
    prnheal_job_table = f"{kw.person_plan_healerunit}_job"
    prncase_job_table = f"{kw.person_plan_reason_caseunit}_job"
    prnreas_job_table = f"{kw.person_plan_reasonunit}_job"
    prnlabo_job_table = f"{kw.person_plan_partyunit}_job"
    prnplan_job_table = f"{kw.person_planunit}_job"
    prnunit_job_table = f"{kw.personunit}_job"
    assert get_row_count(cursor0, prnunit_job_table) == 0
    assert get_row_count(cursor0, prnplan_job_table) == 0
    assert get_row_count(cursor0, prnptnr_job_table) == 0
    assert get_row_count(cursor0, prnmemb_job_table) == 0
    assert get_row_count(cursor0, prngrou_job_table) == 0
    assert get_row_count(cursor0, prnawar_job_table) == 0
    assert get_row_count(cursor0, prnfact_job_table) == 0
    assert get_row_count(cursor0, prnheal_job_table) == 0
    assert get_row_count(cursor0, prnreas_job_table) == 0
    assert get_row_count(cursor0, prncase_job_table) == 0
    assert get_row_count(cursor0, prnlabo_job_table) == 0

    # WHEN
    insert_job_obj(cursor0, sue_person)

    # THEN
    assert get_row_count(cursor0, prnunit_job_table) == 1
    assert get_row_count(cursor0, prnplan_job_table) == 5
    assert get_row_count(cursor0, prnptnr_job_table) == 2
    assert get_row_count(cursor0, prnmemb_job_table) == 3
    assert get_row_count(cursor0, prngrou_job_table) == 3
    assert get_row_count(cursor0, prnawar_job_table) == 1
    assert get_row_count(cursor0, prnfact_job_table) == 1
    assert get_row_count(cursor0, prnheal_job_table) == 1
    assert get_row_count(cursor0, prnreas_job_table) == 1
    assert get_row_count(cursor0, prncase_job_table) == 1
    assert get_row_count(cursor0, prnlabo_job_table) == 1
