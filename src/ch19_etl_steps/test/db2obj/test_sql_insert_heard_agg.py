from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import create_insert_query
from src.ch18_etl_config.etl_config import (
    etl_idea_category_config_dict as get_etl_config,
    get_prime_columns,
    remove_inx_columns,
    remove_staging_columns,
)
from src.ch18_etl_config.etl_sqlstr import create_sound_and_heard_tables
from src.ch19_etl_steps.obj2db_person import (
    create_prnawar_put_h_agg_insert_sqlstr,
    create_prncase_put_h_agg_insert_sqlstr,
    create_prncont_put_h_agg_insert_sqlstr,
    create_prnfact_put_h_agg_insert_sqlstr,
    create_prngrou_put_h_agg_insert_sqlstr,
    create_prnheal_put_h_agg_insert_sqlstr,
    create_prnlabo_put_h_agg_insert_sqlstr,
    create_prnmemb_put_h_agg_insert_sqlstr,
    create_prnplan_put_h_agg_insert_sqlstr,
    create_prnreas_put_h_agg_insert_sqlstr,
    create_prnunit_put_h_agg_insert_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_create_prnunit_put_h_agg_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_moment_rope = exx.a23_dash
    x_knot = exx.dash
    x_person_name = "Sue"
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_mana_grain = 4
    x_respect_grain = 0.2
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.moment_rope: x_moment_rope,
        kw.person_name: x_person_name,
        kw.credor_respect: x_credor_respect,
        kw.debtor_respect: x_debtor_respect,
        kw.fund_grain: x_fund_grain,
        kw.fund_pool: x_fund_pool,
        kw.max_tree_traverse: x_max_tree_traverse,
        kw.mana_grain: x_mana_grain,
        kw.respect_grain: x_respect_grain,
        kw.knot: x_knot,
    }
    etl_config = get_etl_config()
    prnunit = kw.personunit
    dst_columns = get_prime_columns(prnunit, [kw.h_agg, "put"], etl_config)
    # print(f"{dst_columns=}")
    # all args included in values dict
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnunit_put_h_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_sound_and_heard_tables(cursor0)
    table_name = "personunit_put_h_agg"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print(expected_sqlstr)
    print("")
    print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnplan_put_h_agg_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_person_name = "Sue"
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
    x_knot = exx.dash
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.person_name: x_person_name,
        kw.addin: x_addin,
        kw.begin: x_begin,
        kw.close: x_close,
        kw.denom: x_denom,
        kw.gogo_want: x_gogo_want,
        kw.star: x_star,
        kw.morph: x_morph,
        kw.numor: x_numor,
        kw.plan_rope: x_rope,
        kw.knot: x_knot,
        kw.pledge: x_pledge,
        kw.problem_bool: x_problem_bool,
        kw.stop_want: x_stop_want,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.person_planunit
    dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnplan_put_h_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_sound_and_heard_tables(cursor0)
    table_name = "person_planunit_put_h_agg"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print(expected_sqlstr)
    # print("")
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prnreas_put_h_agg_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_person_name = "Sue"
    x_rope = 1
    x_knot = exx.dash
    x_reason_context = 2
    x_active_requisite = 3
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.reason_context: x_reason_context,
        kw.active_requisite: x_active_requisite,
        kw.knot: x_knot,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.person_plan_reasonunit
    dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnreas_put_h_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_sound_and_heard_tables(cursor0)
    table_name = "person_plan_reasonunit_put_h_agg"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    # print(expected_sqlstr)
    print("")
    print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_prncase_put_h_agg_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_person_name = "Sue"
    x_rope = 1
    x_knot = exx.dash
    x_reason_context = 2
    x_reason_state = 3
    x_reason_lower = 4
    x_reason_upper = 5
    x_reason_divisor = 6
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.reason_context: x_reason_context,
        kw.reason_state: x_reason_state,
        f"{kw.reason_lower}_otx": x_reason_lower,
        f"{kw.reason_upper}_otx": x_reason_upper,
        kw.reason_divisor: x_reason_divisor,
        kw.knot: x_knot,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.person_plan_reason_caseunit
    dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
    dst_columns = remove_inx_columns(dst_columns)
    dst_columns = remove_staging_columns(dst_columns)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prncase_put_h_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_sound_and_heard_tables(cursor0)
    table_name = "person_plan_reason_caseunit_put_h_agg"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    # print(expected_sqlstr)
    print("")
    print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


# def test_create_prnawar_put_h_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_rope = exx.a23_dash
#     x_person_name = "Sue"
#     x_rope = 1
#     x_awardee_title = 2
#     x_give_force = 3
#     x_take_force = 4
#     x_fund_give = 5
#     x_fund_take = 6
#     values_dict = {
#     kw.spark_num: 77,
#     kw.face_name: exx.yao,
#     kw.moment_rope: x_moment_rope,
#     kw.person_name: x_person_name,
#     kw.plan_rope: x_rope,
#     kw.awardee_title: x_awardee_title,
#     kw.give_force: x_give_force,
#     kw.take_force: x_take_force,
#     kw.fund_give: x_fund_give,
#     kw.fund_take: x_fund_take,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.personunit
#     dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_prnawar_put_h_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     table_name = "person_plan_awardunit_put_h_agg"
#     expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
#     print("")
#     print(expected_sqlstr)
#     # print(insert_sqlstr)
#     assert insert_sqlstr == expected_sqlstr


def test_create_prnfact_put_h_agg_insert_sqlstr_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_person_name = "Sue"
    x_rope = 1
    x_knot = exx.dash
    x_fact_context = 2
    x_fact_state = 3
    x_fact_lower_otx = 4
    x_fact_upper_otx = 5
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.person_name: x_person_name,
        kw.plan_rope: x_rope,
        kw.knot: x_knot,
        kw.fact_context: x_fact_context,
        kw.fact_state: x_fact_state,
        f"{kw.fact_lower}_otx": x_fact_lower_otx,
        f"{kw.fact_upper}_otx": x_fact_upper_otx,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.person_plan_factunit
    dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
    dst_columns = remove_inx_columns(dst_columns)
    dst_columns = remove_staging_columns(dst_columns)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_prnfact_put_h_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    create_sound_and_heard_tables(cursor0)
    table_name = "person_plan_factunit_put_h_agg"
    expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
    print("")
    print(expected_sqlstr)
    # print(insert_sqlstr)
    assert insert_sqlstr == expected_sqlstr


# def test_create_prnheal_put_h_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_rope = exx.a23_dash
#     x_person_name = "Sue"
#     x_rope = 1
#     x_healer_name = 2
#     values_dict = {
#     kw.spark_num: 77,
#     kw.face_name: exx.yao,
#     kw.moment_rope: x_moment_rope,
#     kw.person_name: x_person_name,
#     kw.plan_rope: x_rope,
#     kw.healer_name: x_healer_name,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.personunit
#     dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_prnheal_put_h_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     table_name = "person_plan_healerunit_put_h_agg"
#     expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
#     print("")
#     print(expected_sqlstr)
#     # print(insert_sqlstr)
#     assert insert_sqlstr == expected_sqlstr


# def test_create_prnlabo_put_h_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_rope = exx.a23_dash
#     x_person_name = "Sue"
#     x_rope = 1
#     x_labor_title = 2
#     x_solo = 4
#     x_person_name_is_workforce = 3
#     values_dict = {
#     kw.spark_num: 77,
#     kw.face_name: exx.yao,
#     kw.moment_rope: x_moment_rope,
#     kw.person_name: x_person_name,
#     kw.plan_rope: x_rope,
#     kw.labor_title: x_labor_title,
#     kw.solo: x_solo,
#     kw.person_name_is_workforce: x_person_name_is_workforce,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.personunit
#     dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_prnlabo_put_h_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     table_name = "person_plan_laborunit_put_h_agg"
#     expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
#     print("")
#     print(expected_sqlstr)
#     print("")
#     print(insert_sqlstr)
#     assert insert_sqlstr == expected_sqlstr


# def test_create_prncont_put_h_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_rope = exx.a23_dash
#     x_person_name = "Sue"
#     x_contact_name = 1
#     x_contact_cred_lumen = 2
#     x_contact_debt_lumen = 3
#     x_credor_pool = 4
#     x_debtor_pool = 5
#     x_fund_give = 6
#     x_fund_take = 7
#     x_fund_agenda_give = 8
#     x_fund_agenda_take = 9
#     x_fund_agenda_ratio_give = 10
#     x_fund_agenda_ratio_take = 11
#     x_inallocable_contact_debt_lumen = 12
#     x_irrational_contact_debt_lumen = 13
#     x_groupmark = 13
#     values_dict = {
#     kw.spark_num: 77,
#     kw.face_name: exx.yao,
#     kw.moment_rope: x_moment_rope,
#     kw.person_name: x_person_name,
#     kw.contact_name: x_contact_name,
#     kw.contact_cred_lumen: x_contact_cred_lumen,
#     kw.contact_debt_lumen: x_contact_debt_lumen,
#     kw.credor_pool: x_credor_pool,
#     kw.debtor_pool: x_debtor_pool,
#     kw.fund_give: x_fund_give,
#     kw.fund_take: x_fund_take,
#     kw.fund_agenda_give: x_fund_agenda_give,
#     kw.fund_agenda_take: x_fund_agenda_take,
#     kw.fund_agenda_ratio_give: x_fund_agenda_ratio_give,
#     kw.fund_agenda_ratio_take: x_fund_agenda_ratio_take,
#     kw.inallocable_contact_debt_lumen: x_inallocable_contact_debt_lumen,
#     kw.irrational_contact_debt_lumen: x_irrational_contact_debt_lumen,
#     kw.groupmark: x_groupmark,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.personunit
#     dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_prncont_put_h_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     table_name = "person_contactunit_put_h_agg"
#     expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
#     print("")
#     print(expected_sqlstr)
#     # print(insert_sqlstr)
#     assert insert_sqlstr == expected_sqlstr


# def test_create_prnmemb_put_h_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_rope = exx.a23_dash
#     x_person_name = "Sue"
#     x_contact_name = 1
#     x_group_title = 2
#     x_group_cred_lumen = 3
#     x_group_debt_lumen = 4
#     x_credor_pool = 5
#     x_debtor_pool = 6
#     x_fund_give = 7
#     x_fund_take = 8
#     x_fund_agenda_give = 9
#     x_fund_agenda_take = 10
#     x_fund_agenda_ratio_give = 11
#     x_fund_agenda_ratio_take = 12
#     values_dict = {
#     kw.spark_num: 77,
#     kw.face_name: exx.yao,
#     kw.moment_rope: x_moment_rope,
#     kw.person_name: x_person_name,
#     kw.contact_name: x_contact_name,
#     kw.group_title: x_group_title,
#     kw.group_cred_lumen: x_group_cred_lumen,
#     kw.group_debt_lumen: x_group_debt_lumen,
#     kw.credor_pool: x_credor_pool,
#     kw.debtor_pool: x_debtor_pool,
#     kw.fund_give: x_fund_give,
#     kw.fund_take: x_fund_take,
#     kw.fund_agenda_give: x_fund_agenda_give,
#     kw.fund_agenda_take: x_fund_agenda_take,
#     kw.fund_agenda_ratio_give: x_fund_agenda_ratio_give,
#     kw.fund_agenda_ratio_take: x_fund_agenda_ratio_take,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.personunit
#     dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_prnmemb_put_h_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     table_name = "person_contact_membership_put_h_agg"
#     expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
#     print("")
#     print(expected_sqlstr)
#     # print(insert_sqlstr)
#     assert insert_sqlstr == expected_sqlstr


# def test_create_prngrou_put_h_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_rope = exx.a23_dash
#     x_person_name = "Sue"
#     x_group_title = 1
#     x_credor_pool = 2
#     x_debtor_pool = 3
#     x_fund_grain = 4
#     x_fund_give = 5
#     x_fund_take = 6
#     x_fund_agenda_give = 7
#     x_fund_agenda_take = 8
#     values_dict = {
#     kw.spark_num: 77,
#     kw.face_name: exx.yao,
#     kw.moment_rope: x_moment_rope,
#     kw.person_name: x_person_name,
#     kw.group_title: x_group_title,
#     kw.credor_pool: x_credor_pool,
#     kw.debtor_pool: x_debtor_pool,
#     kw.fund_grain: x_fund_grain,
#     kw.fund_give: x_fund_give,
#     kw.fund_take: x_fund_take,
#     kw.fund_agenda_give: x_fund_agenda_give,
#     kw.fund_agenda_take: x_fund_agenda_take,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.personunit
#     dst_columns = get_prime_columns(dimen, [kw.h_agg, "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_prngrou_put_h_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     table_name = "person_groupunit_put_h_agg"
#     expected_sqlstr = create_insert_query(cursor0, table_name, values_dict)
#     print("")
#     print(expected_sqlstr)
#     # print(insert_sqlstr)
#     assert insert_sqlstr == expected_sqlstr
