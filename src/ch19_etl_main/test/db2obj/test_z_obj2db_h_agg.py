from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
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
from src.ch18_etl_config.etl_sqlstr import create_sound_and_heard_tables
from src.ch19_etl_main.obj2db_person import (
    ObjKeysHolder,
    insert_h_agg_obj,
    insert_h_agg_prnawar,
    insert_h_agg_prncase,
    insert_h_agg_prnfact,
    insert_h_agg_prngrou,
    insert_h_agg_prnheal,
    insert_h_agg_prnlabo,
    insert_h_agg_prnmemb,
    insert_h_agg_prnplan,
    insert_h_agg_prnptnr,
    insert_h_agg_prnreas,
    insert_h_agg_prnunit,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_insert_h_agg_prnunit_CreatesTableRowsFor_personunit_h_agg(cursor0: Cursor):
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_person_name = "Sue"
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_mana_grain = 4.0
    x_respect_grain = 0.2
    x_knot = exx.dash
    sue_person = personunit_shop(x_person_name, exx.a23_dash, exx.dash)
    sue_person.fund_pool = x_fund_pool
    sue_person.fund_grain = x_fund_grain
    sue_person.mana_grain = x_mana_grain
    sue_person.respect_grain = x_respect_grain
    sue_person.max_tree_traverse = x_max_tree_traverse
    sue_person.credor_respect = x_credor_respect
    sue_person.debtor_respect = x_debtor_respect

    create_sound_and_heard_tables(cursor0)
    x_table_name = "personunit_put_h_agg"
    assert get_row_count(cursor0, x_table_name) == 0
    objkeysholder = ObjKeysHolder(x_spark_num, x_face_name)

    # WHEN
    insert_h_agg_prnunit(cursor0, objkeysholder, sue_person)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        x_spark_num,
        x_face_name,
        exx.a23_dash,
        x_person_name,
        x_credor_respect,
        x_debtor_respect,
        x_fund_pool,
        x_max_tree_traverse,
        x_fund_grain,
        x_mana_grain,
        x_respect_grain,
        x_knot,
    )
    expected_data = [expected_row0]
    assert rows == expected_data


def test_insert_h_agg_prnplan_CreatesTableRowsFor_prnplan_h_agg(cursor0: Cursor):
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_person_name = 2
    x_knot = exx.dash
    casa_rope = create_rope(exx.a23_dash, "casa", x_knot)
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
    x_plan = planunit_shop(exx.casa, knot=x_knot)
    x_plan.parent_rope = x_parent_rope
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

    create_sound_and_heard_tables(cursor0)
    x_table_name = "person_planunit_put_h_agg"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        spark_num=x_spark_num,
        face_name=x_face_name,
        moment_rope=exx.a23_dash,
        person_name=x_person_name,
        knot=x_knot,
    )

    # WHEN
    insert_h_agg_prnplan(cursor0, x_objkeysholder, x_plan)

    # THEN
    clean_rope = create_rope(casa_rope, "clean", x_knot)
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        x_spark_num,
        x_face_name,
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
        x_knot,
    )
    print(f"      {rows[0]=}")
    print(f"{expected_row0=}")
    assert rows[0] == expected_row0


def test_insert_h_agg_prnreas_CreatesTableRowsFor_prnreas_h_agg(cursor0: Cursor):
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_person_name = 2
    x_rope = 3
    x_knot = exx.dash
    x_reason_context = 4
    x_active_requisite = 5
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context, knot=x_knot)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.active_requisite = x_active_requisite

    create_sound_and_heard_tables(cursor0)
    x_table_name = "person_plan_reasonunit_put_h_agg"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        spark_num=x_spark_num,
        face_name=x_face_name,
        moment_rope=exx.a23_dash,
        person_name=x_person_name,
        rope=x_rope,
        knot=x_knot,
    )

    # WHEN
    insert_h_agg_prnreas(cursor0, x_objkeysholder, x_reasonheir)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        x_spark_num,
        x_face_name,
        str(x_person_name),
        str(x_rope),
        str(x_reason_context),
        x_active_requisite,
        x_knot,
    )
    print(f"      {rows[0]=}")
    print(f"{expected_row0=}")
    assert rows[0] == expected_row0


def test_insert_h_agg_prncase_CreatesTableRowsFor_prncase_h_agg(cursor0: Cursor):
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_person_name = 2
    x_rope = 3
    x_knot = exx.dash
    x_reason_context = 4
    x_reason_state = 5
    x_reason_lower_otx = 7.0
    x_reason_upper_otx = 6.0
    x_reason_lower_inx = None
    x_reason_upper_inx = None
    x_reason_divisor = 8
    x_caseunit = caseunit_shop(reason_state=x_reason_state, knot=x_knot)
    x_caseunit.reason_state = x_reason_state
    x_caseunit.reason_lower = x_reason_lower_otx
    x_caseunit.reason_upper = x_reason_upper_otx
    x_caseunit.reason_divisor = x_reason_divisor

    create_sound_and_heard_tables(cursor0)
    x_table_name = "person_plan_reason_caseunit_put_h_agg"
    print(
        f"{get_table_columns(cursor0, x_table_name)=} {len(get_table_columns(cursor0, x_table_name))=}"
    )
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        spark_num=x_spark_num,
        face_name=x_face_name,
        person_name=x_person_name,
        rope=x_rope,
        reason_context=x_reason_context,
        knot=x_knot,
    )

    # WHEN
    insert_h_agg_prncase(cursor0, x_objkeysholder, x_caseunit)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        x_spark_num,
        x_face_name,
        str(x_person_name),
        str(x_rope),
        str(x_reason_context),
        str(x_reason_state),
        x_reason_lower_otx,
        x_reason_lower_inx,
        x_reason_upper_otx,
        x_reason_upper_inx,
        x_reason_divisor,
        x_knot,
        None,
        None,
        None,
        None,
    )
    print(f"      {rows[0]=}")
    print(f"{expected_row0=}")
    assert len(rows[0]) == len(expected_row0)
    assert rows[0] == expected_row0


# def test_insert_h_agg_prnmemb_CreatesTableRowsFor_prnmemb_h_agg():
# #     # ESTABLISH
#     # x_args = get_person_calc_dimen_args("person_partner_membership")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_membership.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""        x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_person_name = 2
#     x_partner_name = 3
#     x_group_title = 4
#     x_group_cred_lumen = 5.0
#     x_group_debt_lumen = 6.0
#     x_credor_pool = 7.0
#     x_debtor_pool = 8.0
#     x_fund_give = 9.0
#     x_fund_take = 10.0
#     x_fund_agenda_give = 11.0
#     x_fund_agenda_take = 12.0
#     x_fund_agenda_ratio_give = 13.0
#     x_fund_agenda_ratio_take = 14.0
#     x_membership = membership_shop(x_group_title)
#     x_membership.partner_name = x_partner_name
#     x_membership.group_cred_lumen = x_group_cred_lumen
#     x_membership.group_debt_lumen = x_group_debt_lumen
#     x_membership.credor_pool = x_credor_pool
#     x_membership.debtor_pool = x_debtor_pool
#     x_membership.fund_give = x_fund_give
#     x_membership.fund_take = x_fund_take
#     x_membership.fund_agenda_give = x_fund_agenda_give
#     x_membership.fund_agenda_take = x_fund_agenda_take
#     x_membership.fund_agenda_ratio_give = x_fund_agenda_ratio_give
#     x_membership.fund_agenda_ratio_take = x_fund_agenda_ratio_take


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     x_table_name = "person_partner_membership_put_h_agg"
#     assert get_row_count(cursor0, x_table_name) == 0
#     x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_rope=exx.a23_dash, person_name=x_person_name)

#     # WHEN
#     insert_h_agg_prnmemb(cursor0, x_objkeysholder, x_membership)

#     # THEN
#     assert get_row_count(cursor0, x_table_name) == 1
#     select_sqlstr = f"SELECT * FROM {x_table_name};"
#     cursor0.execute(select_sqlstr)
#     rows = cursor0.fetchall()
#     expected_row0 = (
#         x_spark_num,
#         x_face_name,
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_partner_name),
#         str(x_group_title),
#         x_group_cred_lumen,
#         x_group_debt_lumen,
#         x_credor_pool,
#         x_debtor_pool,
#         x_fund_give,
#         x_fund_take,
#         x_fund_agenda_give,
#         x_fund_agenda_take,
#         x_fund_agenda_ratio_give,
#         x_fund_agenda_ratio_take,
#     )
#     expected_data = [expected_row0]
#     assert rows == expected_data


# def test_insert_h_agg_prnptnr_CreatesTableRowsFor_prnptnr_h_agg():
# #     # ESTABLISH
#     # x_args = get_person_calc_dimen_args("person_partnerunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_partner.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""        x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_person_name = 2
#     x_partner_name = 3
#     x_partner_cred_lumen = 4
#     x_partner_debt_lumen = 5
#     x_credor_pool = 6
#     x_debtor_pool = 7
#     x_fund_give = 8
#     x_fund_take = 9
#     x_fund_agenda_give = 10
#     x_fund_agenda_take = 11
#     x_fund_agenda_ratio_give = 12
#     x_fund_agenda_ratio_take = 13
#     x_inallocable_partner_debt_lumen = 14
#     x_irrational_partner_debt_lumen = 15
#     x_groupmark = 16
#     x_partner = partnerunit_shop(x_partner_name)
#     x_partner.partner_name = x_partner_name
#     x_partner.partner_cred_lumen = x_partner_cred_lumen
#     x_partner.partner_debt_lumen = x_partner_debt_lumen
#     x_partner.credor_pool = x_credor_pool
#     x_partner.debtor_pool = x_debtor_pool
#     x_partner.fund_give = x_fund_give
#     x_partner.fund_take = x_fund_take
#     x_partner.fund_agenda_give = x_fund_agenda_give
#     x_partner.fund_agenda_take = x_fund_agenda_take
#     x_partner.fund_agenda_ratio_give = x_fund_agenda_ratio_give
#     x_partner.fund_agenda_ratio_take = x_fund_agenda_ratio_take
#     x_partner.inallocable_partner_debt_lumen = x_inallocable_partner_debt_lumen
#     x_partner.irrational_partner_debt_lumen = x_irrational_partner_debt_lumen
#     x_partner.groupmark = x_groupmark


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     x_table_name = "person_partnerunit_put_h_agg"
#     assert get_row_count(cursor0, x_table_name) == 0
#     x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_rope=exx.a23_dash, person_name=x_person_name)

#     # WHEN
#     insert_h_agg_prnptnr(cursor0, x_objkeysholder, x_partner)

#     # THEN
#     assert get_row_count(cursor0, x_table_name) == 1
#     select_sqlstr = f"SELECT * FROM {x_table_name};"
#     cursor0.execute(select_sqlstr)
#     rows = cursor0.fetchall()
#     expected_row0 = (
#         x_spark_num,
#         x_face_name,
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_partner_name),
#         x_partner_cred_lumen,
#         x_partner_debt_lumen,
#         str(x_groupmark),
#         x_credor_pool,
#         x_debtor_pool,
#         x_fund_give,
#         x_fund_take,
#         x_fund_agenda_give,
#         x_fund_agenda_take,
#         x_fund_agenda_ratio_give,
#         x_fund_agenda_ratio_take,
#         x_inallocable_partner_debt_lumen,
#         x_irrational_partner_debt_lumen,
#     )
#     expected_data = [expected_row0]
#     assert rows == expected_data


# def test_insert_h_agg_prngrou_CreatesTableRowsFor_prngrou_h_agg():
# #     # ESTABLISH
#     # x_args = get_person_calc_dimen_args("person_groupunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_group.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""        x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_person_name = 2
#     x_group_title = 3
#     x_fund_grain = 4
#     x_credor_pool = 6
#     x_debtor_pool = 7
#     x_fund_give = 8
#     x_fund_take = 9
#     x_fund_agenda_give = 10
#     x_fund_agenda_take = 11
#     x_group = groupunit_shop(x_group_title)
#     x_group.group_title = x_group_title
#     x_group.fund_grain = x_fund_grain
#     x_group.credor_pool = x_credor_pool
#     x_group.debtor_pool = x_debtor_pool
#     x_group.fund_give = x_fund_give
#     x_group.fund_take = x_fund_take
#     x_group.fund_agenda_give = x_fund_agenda_give
#     x_group.fund_agenda_take = x_fund_agenda_take


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     x_table_name = "person_groupunit_put_h_agg"
#     assert get_row_count(cursor0, x_table_name) == 0
#     x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_rope=exx.a23_dash, person_name=x_person_name)

#     # WHEN
#     insert_h_agg_prngrou(cursor0, x_objkeysholder, x_group)

#     # THEN
#     assert get_row_count(cursor0, x_table_name) == 1
#     select_sqlstr = f"SELECT * FROM {x_table_name};"
#     cursor0.execute(select_sqlstr)
#     rows = cursor0.fetchall()
#     expected_row0 = (
#         x_spark_num,
#         x_face_name,
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_group_title),
#         x_fund_grain,
#         x_credor_pool,
#         x_debtor_pool,
#         x_fund_give,
#         x_fund_take,
#         x_fund_agenda_give,
#         x_fund_agenda_take,
#     )
#     expected_data = [expected_row0]
#     assert rows == expected_data


# def test_insert_h_agg_prnawar_CreatesTableRowsFor_prnawar_h_agg():
# #     # ESTABLISH
#     # x_args = get_person_calc_dimen_args("person_plan_awardunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_awardheir.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""        x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_person_name = 2
#     x_rope = 3
#     x_awardee_title = 4
#     x_give_force = 5
#     x_take_force = 6
#     x_fund_give = 7
#     x_fund_take = 8
#     x_awardheir = awardheir_shop(x_awardee_title)
#     x_awardheir.awardee_title = x_awardee_title
#     x_awardheir.give_force = x_give_force
#     x_awardheir.take_force = x_take_force
#     x_awardheir.fund_give = x_fund_give
#     x_awardheir.fund_take = x_fund_take


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     x_table_name = "person_plan_awardunit_put_h_agg"
#     assert get_row_count(cursor0, x_table_name) == 0
#     x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_rope=exx.a23_dash, person_name=x_person_name, rope=x_rope)

#     # WHEN
#     insert_h_agg_prnawar(cursor0, x_objkeysholder, x_awardheir)

#     # THEN
#     assert get_row_count(cursor0, x_table_name) == 1
#     select_sqlstr = f"SELECT * FROM {x_table_name};"
#     cursor0.execute(select_sqlstr)
#     rows = cursor0.fetchall()
#     expected_row0 = (
#         x_spark_num,
#         x_face_name,
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_rope),
#         str(x_awardee_title),
#         x_give_force,
#         x_take_force,
#         x_fund_give,
#         x_fund_take,
#     )
#     expected_data = [expected_row0]
#     assert rows == expected_data


def test_insert_h_agg_prnfact_CreatesTableRowsFor_prnfact_h_agg(cursor0: Cursor):
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_person_name = 2
    x_rope = 3
    x_knot = exx.dash
    x_reason_context = 4
    x_fact_state = 5
    x_fact_lower_otx = 6
    x_fact_upper_otx = 7
    x_fact_lower_inx = None
    x_fact_upper_inx = None
    x_factheir = factheir_shop()
    x_factheir.fact_context = x_reason_context
    x_factheir.fact_state = x_fact_state
    x_factheir.fact_lower = x_fact_lower_otx
    x_factheir.fact_upper = x_fact_upper_otx

    create_sound_and_heard_tables(cursor0)
    x_table_name = "person_plan_factunit_put_h_agg"
    assert get_row_count(cursor0, x_table_name) == 0
    x_objkeysholder = ObjKeysHolder(
        spark_num=x_spark_num,
        face_name=x_face_name,
        person_name=x_person_name,
        rope=x_rope,
        knot=x_knot,
    )

    # WHEN
    insert_h_agg_prnfact(cursor0, x_objkeysholder, x_factheir)

    # THEN
    assert get_row_count(cursor0, x_table_name) == 1
    select_sqlstr = f"SELECT * FROM {x_table_name};"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    expected_row0 = (
        x_spark_num,
        x_face_name,
        str(x_person_name),
        str(x_rope),
        str(x_reason_context),
        str(x_fact_state),
        x_fact_lower_otx,
        x_fact_lower_inx,
        x_fact_upper_otx,
        x_fact_upper_inx,
        x_knot,
        None,
        None,
        None,
        None,
    )
    assert len(rows[0]) == len(expected_row0)
    print(rows[0])
    print(expected_row0)
    assert rows[0] == expected_row0


# def test_insert_h_agg_prnheal_CreatesTableRowsFor_prnheal_h_agg():
# #     # ESTABLISH
#     # x_args = get_person_calc_dimen_args("person_plan_healerunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_healerunit.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""        x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_person_name = 2
#     x_rope = 3
#     x_healerunit = healerunit_shop()
#     x_healerunit.set_healer_name(exx.bob)
#     x_healerunit.set_healer_name(exx.sue)


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     x_table_name = "person_plan_healerunit_put_h_agg"
#     assert get_row_count(cursor0, x_table_name) == 0
#     x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_rope=exx.a23_dash, person_name=x_person_name, rope=x_rope)

#     # WHEN
#     insert_h_agg_prnheal(cursor0, x_objkeysholder, x_healerunit)

#     # THEN
#     assert get_row_count(cursor0, x_table_name) == 2
#     select_sqlstr = f"SELECT * FROM {x_table_name};"
#     cursor0.execute(select_sqlstr)
#     rows = cursor0.fetchall()
#     expected_row0 = (
#         x_spark_num,
#         x_face_name,
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_rope),
#         exx.bob,
#     )
#     expected_row1 = (
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_rope),
#         exx.sue,
#     )
#     expected_data = [expected_row0, expected_row1]
#     assert rows == expected_data


# def test_insert_h_agg_prnlabo_CreatesTableRowsFor_prnlabo_h_agg():
# #     # ESTABLISH
#     # x_args = get_person_calc_dimen_args("person_plan_partyunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_laborheir.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""        x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_person_name = 2
#     x_rope = 3
#     x_person_name_is_labor = 5
#     x_laborheir = laborheir_shop()
#     x_laborheir.person_name_is_labor = x_person_name_is_labor
#     bob_solo_bool = 6
#     sue_solo_bool = 7
#     bob_partyheir = partyheir_shop(exx.bob, bob_solo_bool)
#     sue_partyheir = partyheir_shop(exx.sue, sue_solo_bool)
#     x_laborheir.partys = {exx.bob: bob_partyheir, exx.sue: sue_partyheir}


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     x_table_name = "person_plan_partyunit_put_h_agg"
#     assert get_row_count(cursor0, x_table_name) == 0
#     x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_rope=exx.a23_dash, person_name=x_person_name, rope=x_rope)

#     # WHEN
#     insert_h_agg_prnlabo(cursor0, x_objkeysholder, x_laborheir)

#     # THEN
#     assert get_row_count(cursor0, x_table_name) == 2
#     select_sqlstr = f"SELECT * FROM {x_table_name};"
#     cursor0.execute(select_sqlstr)
#     rows = cursor0.fetchall()
#     expected_row0 = (
#         x_spark_num,
#         x_face_name,
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_rope),
#         exx.bob,
#         bob_solo_bool,
#         x_person_name_is_labor,
#     )
#     expected_row1 = (
#         str(exx.a23_dash),
#         str(x_person_name),
#         str(x_rope),
#         exx.sue,
#         sue_solo_bool,
#         x_person_name_is_labor,
#     )
#     expected_data = [expected_row0, expected_row1]
#     assert rows == expected_data


def test_insert_h_agg_obj_CreatesTableRows_Scenario0_ReasonNumRelevantTables(
    cursor0: Cursor,
):
    # ESTABLISH
    sue_person = personunit_shop(exx.sue, exx.a23_dash, knot=exx.dash)
    sue_person.add_partnerunit(exx.sue)
    sue_person.add_partnerunit(exx.bob)
    sue_person.get_partner(exx.bob).add_membership(exx.run_dash)
    casa_rope = sue_person.make_l1_rope("casa")
    situation_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(situation_rope, "clean")
    dirty_rope = sue_person.make_rope(situation_rope, "dirty")
    sue_person.add_plan(casa_rope)
    sue_person.add_plan(clean_rope)
    sue_person.add_plan(dirty_rope)
    sue_person.edit_plan_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_person.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run_dash))
    sue_person.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    casa_laborunit = laborunit_shop()
    casa_laborunit.add_party(exx.sue, True)
    sue_person.edit_plan_attr(casa_rope, laborunit=casa_laborunit)
    sue_person.add_fact(situation_rope, clean_rope)

    create_sound_and_heard_tables(cursor0)
    prnfact_h_agg_table = f"{kw.person_plan_factunit}_put_h_agg"
    prncase_h_agg_table = f"{kw.person_plan_reason_caseunit}_put_h_agg"
    prnreas_h_agg_table = f"{kw.person_plan_reasonunit}_put_h_agg"
    prnplan_h_agg_table = f"{kw.person_planunit}_put_h_agg"
    prnunit_h_agg_table = f"{kw.personunit}_put_h_agg"
    assert get_row_count(cursor0, prnunit_h_agg_table) == 0
    assert get_row_count(cursor0, prnplan_h_agg_table) == 0
    assert get_row_count(cursor0, prnfact_h_agg_table) == 0
    assert get_row_count(cursor0, prnreas_h_agg_table) == 0
    assert get_row_count(cursor0, prncase_h_agg_table) == 0

    # WHEN
    spark7 = 7
    insert_h_agg_obj(cursor0, sue_person, spark7, face_name=exx.yao)

    # THEN
    assert get_row_count(cursor0, prnunit_h_agg_table) == 1
    assert get_row_count(cursor0, prnplan_h_agg_table) == 4
    assert get_row_count(cursor0, prnfact_h_agg_table) == 1
    assert get_row_count(cursor0, prnreas_h_agg_table) == 3
    assert get_row_count(cursor0, prncase_h_agg_table) == 3
    select_case_sqlstr = f"SELECT spark_num, face_name FROM {prncase_h_agg_table};"
    cursor0.execute(select_case_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [(spark7, exx.yao), (spark7, exx.yao), (spark7, exx.yao)]


# def test_insert_h_agg_obj_CreatesTableRows_Scenario1_AllTables():
# #     # ESTABLISH
#     sue_person = personunit_shop(exx.sue, exx.a23_dash)
#     sue_person.add_partnerunit(exx.sue)
#     sue_person.add_partnerunit(exx.bob)
#     sue_person.get_partner(exx.bob).add_membership(exx.run)
#     casa_rope = sue_person.make_l1_rope("casa")
#     situation_rope = sue_person.make_l1_rope(kw.reason_active)
#     clean_rope = sue_person.make_rope(situation_rope, "clean")
#     dirty_rope = sue_person.make_rope(situation_rope, "dirty")
#     sue_person.add_plan(casa_rope)
#     sue_person.add_plan(clean_rope)
#     sue_person.add_plan(dirty_rope)
#     sue_person.edit_plan_attr(
#     casa_rope, reason_context=situation_rope, reason_case=dirty_rope
#     )
#     sue_person.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run))
#     sue_person.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
#     casa_laborunit = laborunit_shop()
#     casa_laborunit.add_party(exx.sue, True)
#     sue_person.edit_plan_attr(casa_rope, laborunit=casa_laborunit)
#     sue_person.add_fact(situation_rope, clean_rope)


#     cursor = conn.cursor()
#     create_sound_and_heard_tables(cursor0)
#     prnmemb_h_agg_table = f"{kw.person_partner_membership}_put_h_agg"
#     prnptnr_h_agg_table = f"{kw.person_partnerunit}_put_h_agg"
#     prngrou_h_agg_table = f"{kw.person_groupunit}_put_h_agg"
#     prnawar_h_agg_table = f"{kw.person_plan_awardunit}_put_h_agg"
#     prnfact_h_agg_table = f"{kw.person_plan_factunit}_put_h_agg"
#     prnheal_h_agg_table = f"{kw.person_plan_healerunit}_put_h_agg"
#     prncase_h_agg_table = f"{kw.person_plan_reason_caseunit}_put_h_agg"
#     prnreas_h_agg_table = f"{kw.person_plan_reasonunit}_put_h_agg"
#     prnlabo_h_agg_table = f"{kw.person_plan_partyunit}_put_h_agg"
#     prnplan_h_agg_table = f"{kw.person_planunit}_put_h_agg"
#     prnunit_h_agg_table = f"{kw.personunit}_put_h_agg"
#     assert get_row_count(cursor0, prnunit_h_agg_table) == 0
#     assert get_row_count(cursor0, prnplan_h_agg_table) == 0
#     assert get_row_count(cursor0, prnptnr_h_agg_table) == 0
#     assert get_row_count(cursor0, prnmemb_h_agg_table) == 0
#     assert get_row_count(cursor0, prngrou_h_agg_table) == 0
#     assert get_row_count(cursor0, prnawar_h_agg_table) == 0
#     assert get_row_count(cursor0, prnfact_h_agg_table) == 0
#     assert get_row_count(cursor0, prnheal_h_agg_table) == 0
#     assert get_row_count(cursor0, prnreas_h_agg_table) == 0
#     assert get_row_count(cursor0, prncase_h_agg_table) == 0
#     assert get_row_count(cursor0, prnlabo_h_agg_table) == 0

#     # WHEN
#     insert_h_agg_obj(cursor0, sue_person)

#     # THEN
#     assert get_row_count(cursor0, prnunit_h_agg_table) == 1
#     assert get_row_count(cursor0, prnplan_h_agg_table) == 5
#     assert get_row_count(cursor0, prnptnr_h_agg_table) == 2
#     assert get_row_count(cursor0, prnmemb_h_agg_table) == 3
#     assert get_row_count(cursor0, prngrou_h_agg_table) == 3
#     assert get_row_count(cursor0, prnawar_h_agg_table) == 1
#     assert get_row_count(cursor0, prnfact_h_agg_table) == 1
#     assert get_row_count(cursor0, prnheal_h_agg_table) == 1
#     assert get_row_count(cursor0, prnreas_h_agg_table) == 1
#     assert get_row_count(cursor0, prncase_h_agg_table) == 1
#     assert get_row_count(cursor0, prnlabo_h_agg_table) == 1
