from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import create_insert_query
from src.ch07_person_logic.person_config import get_person_calc_dimen_args
from src.ch18_etl_config.etl_sqlstr import create_job_tables
from src.ch19_etl_main.obj2db_person import (
    create_personunit_metrics_insert_sqlstr,
    create_prnawar_metrics_insert_sqlstr,
    create_prncase_metrics_insert_sqlstr,
    create_prnfact_metrics_insert_sqlstr,
    create_prngrou_metrics_insert_sqlstr,
    create_prnheal_metrics_insert_sqlstr,
    create_prnlabo_metrics_insert_sqlstr,
    create_prnmemb_metrics_insert_sqlstr,
    create_prnplan_metrics_insert_sqlstr,
    create_prnptnr_metrics_insert_sqlstr,
    create_prnreas_metrics_insert_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_create_personunit_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("personunit")
    x_args.add("moment_rope")
    # for x_arg in sorted(x_args):
    #     print(f"{x_arg=}")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_keeps_buildable = True
    x_keeps_justified = False
    x_offtrack_fund = 55.5
    x_rational = True
    x_sum_healerunit_plans_fund_total = 66.6
    x_tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_mana_grain = 4
    x_respect_grain = 0.2
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.knot: x_knot,
        kw.person_name: x_person_name,
        kw.keeps_buildable: x_keeps_buildable,
        kw.keeps_justified: x_keeps_justified,
        kw.offtrack_fund: x_offtrack_fund,
        kw.rational: x_rational,
        kw.sum_healerunit_plans_fund_total: x_sum_healerunit_plans_fund_total,
        kw.tree_traverse_count: x_tree_traverse_count,
        kw.credor_respect: x_credor_respect,
        kw.debtor_respect: x_debtor_respect,
        kw.fund_grain: x_fund_grain,
        kw.fund_pool: x_fund_pool,
        kw.max_tree_traverse: x_max_tree_traverse,
        kw.mana_grain: x_mana_grain,
        kw.respect_grain: x_respect_grain,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_personunit_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "personunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print(expected_sqlstr)
    print("")
    print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnplan_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_planunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     # print(f"    x_{x_arg} = {x_count}")
    #     # print(f"""    "{x_arg}": x_{x_arg},""")
    #     print(f""" {x_arg} = values_dict.get("{x_arg}")""")
    #     # b0_str = "{"
    #     # b1_str = "}"
    #     # print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_active = 1
    x_all_partner_cred = 2
    x_all_partner_debt = 3
    x_descendant_pledge_count = 4
    x_fund_cease = 5
    x_fund_grain = 6
    x_fund_onset = 7
    x_fund_ratio = 8
    x_gogo_calc = 9
    x_healerunit_ratio = 10
    x_tree_level = 11
    x_range_evaluated = 12
    x_stop_calc = 13
    x_plan_task = 14
    x_addin = 15
    x_begin = 16
    x_close = 17
    x_denom = 18
    x_gogo_want = 19
    x_star = 21
    x_morph = 22
    x_numor = 23
    x_rope = 24
    x_pledge = 25
    x_problem_bool = 26
    x_stop_want = 27
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.knot: x_knot,
        kw.person_name: x_person_name,
        kw.plan_active: x_active,
        kw.all_partner_cred: x_all_partner_cred,
        kw.all_partner_debt: x_all_partner_debt,
        kw.descendant_pledge_count: x_descendant_pledge_count,
        kw.fund_cease: x_fund_cease,
        kw.fund_grain: x_fund_grain,
        kw.fund_onset: x_fund_onset,
        kw.fund_ratio: x_fund_ratio,
        kw.gogo_calc: x_gogo_calc,
        kw.healerunit_ratio: x_healerunit_ratio,
        kw.tree_level: x_tree_level,
        kw.range_evaluated: x_range_evaluated,
        kw.stop_calc: x_stop_calc,
        kw.plan_task: x_plan_task,
        kw.addin: x_addin,
        kw.begin: x_begin,
        kw.close: x_close,
        kw.denom: x_denom,
        kw.gogo_want: x_gogo_want,
        kw.star: x_star,
        kw.morph: x_morph,
        kw.numor: x_numor,
        kw.plan_rope: x_rope,
        kw.pledge: x_pledge,
        kw.problem_bool: x_problem_bool,
        kw.stop_want: x_stop_want,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnplan_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_planunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print(expected_sqlstr)
    print("")
    print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnreas_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_plan_reasonunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_active_requisite = 3
    x_reason_active = 4
    x_reason_task = 5
    x_heir_active = 6
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.knot: x_knot,
        kw.reason_context: x_reason_context,
        kw.active_requisite: x_active_requisite,
        kw.reason_active: x_reason_active,
        kw.reason_task: x_reason_task,
        kw.parent_heir_active: x_heir_active,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnreas_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_plan_reasonunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print(expected_sqlstr)
    print("")
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prncase_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_plan_reason_caseunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_reason_state = 3
    x_reason_lower = 5
    x_reason_upper = 4
    x_reason_divisor = 6
    x_case_task = 7
    x_case_active = 8
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.knot: x_knot,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.reason_context: x_reason_context,
        kw.reason_state: x_reason_state,
        kw.reason_lower: x_reason_lower,
        kw.reason_upper: x_reason_upper,
        kw.reason_divisor: x_reason_divisor,
        kw.case_task: x_case_task,
        kw.case_active: x_case_active,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prncase_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_plan_reason_caseunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print(expected_sqlstr)
    # print("")
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnawar_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_plan_awardunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_rope = 1
    x_awardee_title = 2
    x_give_force = 3
    x_take_force = 4
    x_fund_give = 5
    x_fund_take = 6
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.person_name: x_person_name,
        kw.knot: x_knot,
        kw.plan_rope: x_rope,
        kw.awardee_title: x_awardee_title,
        kw.give_force: x_give_force,
        kw.take_force: x_take_force,
        kw.fund_give: x_fund_give,
        kw.fund_take: x_fund_take,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnawar_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_plan_awardunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnfact_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_plan_factunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_slash = exx.slash
    x_person_name = "Sue"
    x_rope = 1
    x_fact_context = 2
    x_fact_state = 3
    x_fact_lower = 4
    x_fact_upper = 5
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.knot: x_slash,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.fact_context: x_fact_context,
        kw.fact_state: x_fact_state,
        kw.fact_lower: x_fact_lower,
        kw.fact_upper: x_fact_upper,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnfact_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_plan_factunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnheal_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_plan_healerunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_rope = 1
    x_healer_name = 2
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.knot: x_knot,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.healer_name: x_healer_name,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnheal_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_plan_healerunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnlabo_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_plan_laborunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_knot = exx.slash
    x_person_name = "Sue"
    x_rope = 1
    x_labor_title = 2
    x_solo = 4
    x_person_name_is_workforce = 3
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.knot: x_knot,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.labor_title: x_labor_title,
        kw.solo: x_solo,
        kw.person_name_is_workforce: x_person_name_is_workforce,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnlabo_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_plan_laborunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    print("")
    print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnptnr_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_partnerunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_person_name = "Sue"
    x_partner_name = 1
    x_partner_cred_lumen = 2
    x_partner_debt_lumen = 3
    x_credor_pool = 4
    x_debtor_pool = 5
    x_fund_give = 6
    x_fund_take = 7
    x_fund_agenda_give = 8
    x_fund_agenda_take = 9
    x_fund_agenda_ratio_give = 10
    x_fund_agenda_ratio_take = 11
    x_inallocable_partner_debt_lumen = 12
    x_irrational_partner_debt_lumen = 13
    x_groupmark = 13
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.person_name: x_person_name,
        kw.partner_name: x_partner_name,
        kw.partner_cred_lumen: x_partner_cred_lumen,
        kw.partner_debt_lumen: x_partner_debt_lumen,
        kw.credor_pool: x_credor_pool,
        kw.debtor_pool: x_debtor_pool,
        kw.fund_give: x_fund_give,
        kw.fund_take: x_fund_take,
        kw.fund_agenda_give: x_fund_agenda_give,
        kw.fund_agenda_take: x_fund_agenda_take,
        kw.fund_agenda_ratio_give: x_fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take: x_fund_agenda_ratio_take,
        kw.inallocable_partner_debt_lumen: x_inallocable_partner_debt_lumen,
        kw.irrational_partner_debt_lumen: x_irrational_partner_debt_lumen,
        kw.groupmark: x_groupmark,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnptnr_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_partnerunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnmemb_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_partner_membership")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_person_name = "Sue"
    x_partner_name = 1
    x_group_title = 2
    x_group_cred_lumen = 3
    x_group_debt_lumen = 4
    x_credor_pool = 5
    x_debtor_pool = 6
    x_fund_give = 7
    x_fund_take = 8
    x_fund_agenda_give = 9
    x_fund_agenda_take = 10
    x_fund_agenda_ratio_give = 11
    x_fund_agenda_ratio_take = 12
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.person_name: x_person_name,
        kw.partner_name: x_partner_name,
        kw.group_title: x_group_title,
        kw.group_cred_lumen: x_group_cred_lumen,
        kw.group_debt_lumen: x_group_debt_lumen,
        kw.credor_pool: x_credor_pool,
        kw.debtor_pool: x_debtor_pool,
        kw.fund_give: x_fund_give,
        kw.fund_take: x_fund_take,
        kw.fund_agenda_give: x_fund_agenda_give,
        kw.fund_agenda_take: x_fund_agenda_take,
        kw.fund_agenda_ratio_give: x_fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take: x_fund_agenda_ratio_take,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnmemb_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_partner_membership_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prngrou_metrics_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_args = get_person_calc_dimen_args("person_groupunit")
    x_args.add("moment_rope")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_moment_rope = exx.a23
    x_person_name = "Sue"
    x_group_title = 1
    x_credor_pool = 2
    x_debtor_pool = 3
    x_fund_grain = 4
    x_fund_give = 5
    x_fund_take = 6
    x_fund_agenda_give = 7
    x_fund_agenda_take = 8
    values_dict = {
        kw.moment_rope: x_moment_rope,
        kw.person_name: x_person_name,
        kw.group_title: x_group_title,
        kw.credor_pool: x_credor_pool,
        kw.debtor_pool: x_debtor_pool,
        kw.fund_grain: x_fund_grain,
        kw.fund_give: x_fund_give,
        kw.fund_take: x_fund_take,
        kw.fund_agenda_give: x_fund_agenda_give,
        kw.fund_agenda_take: x_fund_agenda_take,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prngrou_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_job_tables(cursor0)
    table_name = "person_groupunit_job"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr
