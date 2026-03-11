from sqlite3 import Cursor
from src.ch00_py.db_toolbox import (
    create_type_reference_insert_sqlstr,
    get_row_count,
    get_table_columns,
)
from src.ch06_plan.test._util.ch06_examples import get_range_attrs
from src.ch07_person_logic.person_tool import (
    PersonUnit,
    person_plan_factunit_exists,
    person_plan_factunit_get_obj,
    person_plan_reason_caseunit_exists,
    person_plan_reason_caseunit_get_obj,
    person_plan_reasonunit_get_obj,
    person_planunit_get_obj,
)
from src.ch13_time.epoch_main import (
    DEFAULT_EPOCH_LENGTH,
    add_epoch_planunit,
    get_c400_constants,
)
from src.ch13_time.epoch_reason import set_epoch_cases_by_args_dict
from src.ch13_time.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_person,
    get_lizzy9_config,
)
from src.ch15_nabu.nabu_config import get_nabu_config_dict
from src.ch17_idea.idea_config import get_dimens_with_idea_element
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_nabu import (
    add_epoch_frame_to_db_personunit,
    add_frame_to_db_caseunit,
    add_frame_to_db_factunit,
    add_frame_to_db_personunit,
    add_frame_to_db_reasonunit,
)
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_update_heard_agg_timenum_sqlstr,
    get_update_heard_agg_timenum_sqlstrs,
    get_update_prncase_context_plan_sqlstr,
    get_update_prncase_inx_epoch_diff_sqlstr,
    get_update_prnfact_context_plan_sqlstr,
    get_update_prnfact_inx_epoch_diff_sqlstr,
    update_heard_agg_timenum_columns,
)
from src.ch18_world_etl.obj2db_person import insert_h_agg_obj
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ch18_world_etl.test._util.ch18_examples import (
    get_bob_five_with_mop_dayly,
    insert_mmtoffi_special_offi_time_otx as insert_offi_time_otx,
    insert_mmtunit_special_c400_number as insert_c400_number,
    insert_nabtime_h_agg_otx_inx_time as insert_otx_inx_time,
    insert_prncase_special_h_agg as insert_prncase,
    insert_prnfact_special_h_agg as insert_prnfact,
    select_mmtoffi_special_offi_time_inx as select_offi_time_inx,
    select_prncase_special_h_agg as pchap1_select_prncase,
    select_prnfact_special_h_agg as select_prnfact,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO TODO create function that updates all nabuable otx fields.
# restart a little bit
# 0. identify all fields that are nabuable
#   "reason_lower", "reason_upper"
#   "fact_lower", "fact_upper"
#   "bud_time"
#   "offi_time"
#   "tran_time"
# 1. on each of their h_agg tables make sure there is inx_epoch_diff
# 2. create update queries to set inx_epoch_diff for all of them
# 3. create update queries to set the nabuable fields using inx_epoch_diff column
# 4. create test for function that both updates inx_epoch_diff and nabuable fields
# 5. create a heard_agg test that confirms heard_vld pulls from nabuable_inx fields (probably not case now)


# identify the change
# update semantic_type: ReasonNum person_plan_reason_caseunit_h_agg_put reason_lower, reason_upper


# update semantic_type: ReasonNum person_plan_factunit_h_agg_put fact_lower, fact_upper
# def test_get_update_prnfact_inx_epoch_diff_sqlstr_SetsColumnValues(cursor0: Cursor):
#     # ESTABLISH
#     spark7 = 7
#     bob_person = get_bob_five_with_mop_dayly()
#     create_sound_and_heard_tables(cursor0)
#     otx_time = 199
#     inx_time = 13
#     m_label = bob_person.planroot.get_plan_rope()
#     insert_otx_inx_time(cursor0, spark7, exx.yao, m_label, otx_time, inx_time)
#     insert_h_agg_obj(cursor0, bob_person, spark7, exx.yao)
#     prnfact_old_objs = select_prnfact(
#         cursor0, spark7, exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
#     )
#     prnfact_old_obj0 = prnfact_old_objs[0]
#     assert prnfact_old_obj0.inx_epoch_diff is None

#     # WHEN
#     update_sql = get_update_prnfact_inx_epoch_diff_sqlstr()
#     cursor0.execute(update_sql)

#     # THEN
#     prnfact_new_objs = select_prnfact(
#         cursor0, spark7, exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
#     )
#     prnfact_new_obj0 = prnfact_new_objs[0]
#     assert prnfact_new_obj0.inx_epoch_diff == otx_time - inx_time
#     assert prnfact_new_obj0.inx_epoch_diff == 186


# def test_get_update_prnfact_inx_epoch_diff_sqlstr_SetsTable(): # ESTABLISH # WHEN # THEN
# def test_get_update_prncase_range_sqlstr_SetsTable(): # ESTABLISH # WHEN # THEN
# def test_get_update_prnfact_range_sqlstr_SetsTable(): # ESTABLISH # WHEN # THEN


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario0_NoWrap_dayly():
# #     # ESTABLISH
#     spark7 = 7
#     bob_person = get_bob_five_person()
#     print(f"{bob_person.planroot.get_plan_rope()=}")
#     x_dayly_lower_min = 600
#     x_dayly_duration_min = 90
#     mop_dayly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.day_rope,
#         kw.reason_state: wx.day_rope,
#         kw.epoch_label: wx.five_str,
#         kw.dayly_lower_min: x_dayly_lower_min,
#         kw.dayly_duration_min: x_dayly_duration_min,
#     }
#     day_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.day_rope})
#     set_epoch_cases_by_args_dict(bob_person, mop_dayly_args)
#         create_sound_and_heard_tables(cursor)
#         m_label = bob_person.planroot.get_plan_rope()
#         otx_time = 100
#         inx_time = 0
#         insert_otx_inx_time(cursor, spark7, exx.yao, m_label, otx_time, inx_time)
#         insert_h_agg_obj(cursor, bob_person, spark7, exx.yao)
#         prncase_objs = pchap1_select_prncase(
#             cursor, spark7, "YY", exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
#         )
#         print(f"{prncase_objs=}")
#         assert prncase_objs
#         prncase_obj0 = prncase_objs[0]
#         assert prncase_obj0.reason_lower_otx == 600
#         assert prncase_obj0.reason_lower_otx == x_dayly_lower_min
#         assert not prncase_obj0.reason_lower_inx
#         assert prncase_obj0.reason_upper_otx == 690
#         assert prncase_obj0.reason_upper_otx == x_dayly_lower_min + x_dayly_duration_min
#         assert not prncase_obj0.reason_upper_inx

#         # WHEN
#         add_frame_to_db_caseunit(cursor, day_plan.close, day_plan.denom, day_plan.morph)

#         # THEN
#         after_prncase_obj0 = pchap1_select_prncase(
#             cursor, spark7, "YY", exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
#         )[0]
#         expected_lower_inx = prncase_obj0.reason_lower_otx + otx_time - inx_time
#         expected_upper_inx = prncase_obj0.reason_upper_otx + otx_time - inx_time
#         assert after_prncase_obj0.reason_lower_otx == 600
#         assert after_prncase_obj0.reason_lower_inx == expected_lower_inx
#         assert after_prncase_obj0.reason_upper_otx == 690
#         assert after_prncase_obj0.reason_upper_inx == expected_upper_inx
#         assert after_prncase_obj0.reason_upper_inx == 690 + otx_time - inx_time


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario1_Wrap_dayly():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_dayly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.day_rope,
#         kw.reason_state: wx.day_rope,
#         kw.epoch_label: wx.five_str,
#         kw.dayly_lower_min: 600,
#         kw.dayly_duration_min: 90,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_dayly_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_dayly_args)
#     day_case = person_plan_reason_caseunit_get_obj(bob_person, mop_dayly_args)
#     day_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.day_rope})
#     x_epoch_frame_min = 1000
#     assert day_case.reason_lower == 600
#     assert day_case.reason_upper == 690

#     # WHEN
#     add_frame_to_db_caseunit(
#         day_case, x_epoch_frame_min, day_plan.close, day_plan.denom, day_plan.morph
#     )

#     # THEN
#     assert day_case.reason_lower != 600
#     assert day_case.reason_upper != 690
#     assert day_case.reason_lower == (600 + x_epoch_frame_min) % day_case.reason_divisor
#     assert day_case.reason_upper == (690 + x_epoch_frame_min) % day_case.reason_divisor


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario3_adds_epoch_frame_NoWarp_xdays():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_days_lower_day = 3
#     mop_days_upper_day = 4
#     mop_every_xdays = 13
#     mop_xdays_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.days_rope,
#         kw.reason_state: wx.days_rope,
#         kw.epoch_label: wx.five_str,
#         kw.days_lower_day: mop_days_lower_day,
#         kw.days_upper_day: mop_days_upper_day,
#         kw.every_xdays: mop_every_xdays,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_xdays_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)
#     days_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.days_rope})
#     days_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xdays_args)
#     x_epoch_frame_min = 5000
#     assert days_case.reason_lower == mop_days_lower_day
#     assert days_case.reason_upper == mop_days_upper_day

#     # WHEN
#     add_frame_to_db_caseunit(
#         days_case, x_epoch_frame_min, days_plan.close, days_plan.denom, days_plan.morph
#     )

#     # THEN
#     assert days_case.reason_lower != mop_days_lower_day
#     assert days_case.reason_upper != mop_days_upper_day
#     assert days_case.reason_lower == mop_days_lower_day + 3
#     assert days_case.reason_upper == mop_days_upper_day + 3


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario4_adds_epoch_frame_Wrap_xdays():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_days_lower_day = 3
#     mop_days_upper_day = 4
#     mop_every_xdays = 13
#     mop_xdays_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.days_rope,
#         kw.reason_state: wx.days_rope,
#         kw.epoch_label: wx.five_str,
#         kw.days_lower_day: mop_days_lower_day,
#         kw.days_upper_day: mop_days_upper_day,
#         kw.every_xdays: mop_every_xdays,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_xdays_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_xdays_args)
#     days_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xdays_args)
#     days_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.days_rope})
#     x_epoch_frame_min = 50000
#     assert days_case.reason_lower == mop_days_lower_day
#     assert days_case.reason_upper == mop_days_upper_day

#     # WHEN
#     add_frame_to_db_caseunit(
#         days_case, x_epoch_frame_min, days_plan.close, days_plan.denom, days_plan.morph
#     )

#     # THEN
#     assert days_case.reason_lower != mop_days_lower_day
#     assert days_case.reason_upper != mop_days_upper_day
#     print(f"{x_epoch_frame_min//1440=}")
#     print(f"{mop_days_lower_day + (x_epoch_frame_min//1440)=}")
#     ex_lower = (mop_days_lower_day + (x_epoch_frame_min // 1440)) % mop_every_xdays
#     ex_upper = (mop_days_upper_day + (x_epoch_frame_min // 1440)) % mop_every_xdays
#     assert days_case.reason_lower == ex_lower
#     assert days_case.reason_upper == ex_upper


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario5_adds_epoch_frame_NoWrap_weekly():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_weekly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.week_rope,
#         kw.reason_state: wx.week_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weekly_lower_min: 600,
#         kw.weekly_duration_min: 90,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_weekly_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
#     week_case = person_plan_reason_caseunit_get_obj(bob_person, mop_weekly_args)
#     week_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.week_rope})
#     x_epoch_frame_min = 100
#     assert week_case.reason_lower == 600
#     assert week_case.reason_upper == 690

#     # WHEN
#     add_frame_to_db_caseunit(
#         week_case, x_epoch_frame_min, week_plan.close, week_plan.denom, week_plan.morph
#     )

#     # THEN
#     assert week_case.reason_lower != 600
#     assert week_case.reason_upper != 690
#     assert week_case.reason_lower == 600 + 100
#     assert week_case.reason_upper == 690 + 100


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario6_adds_epoch_frame_Wrap_weekly():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_weekly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.week_rope,
#         kw.reason_state: wx.week_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weekly_lower_min: 600,
#         kw.weekly_duration_min: 90,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_weekly_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_weekly_args)
#     week_case = person_plan_reason_caseunit_get_obj(bob_person, mop_weekly_args)
#     week_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.week_rope})
#     x_epoch_frame_min = 10000
#     assert week_case.reason_lower == 600
#     assert week_case.reason_upper == 690

#     # WHEN
#     add_frame_to_db_caseunit(
#         week_case, x_epoch_frame_min, week_plan.close, week_plan.denom, week_plan.morph
#     )

#     # THEN
#     assert week_case.reason_lower != 600
#     assert week_case.reason_upper != 690
#     assert (
#         week_case.reason_lower == (600 + x_epoch_frame_min) % week_case.reason_divisor
#     )
#     assert (
#         week_case.reason_upper == (690 + x_epoch_frame_min) % week_case.reason_divisor
#     )


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario7_adds_epoch_frame_NoWrap_xweeks():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_weeks_lower_week = 3
#     mop_weeks_upper_week = 4
#     mop_every_xweeks = 13
#     mop_xweeks_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.weeks_rope,
#         kw.reason_state: wx.weeks_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weeks_lower_week: mop_weeks_lower_week,
#         kw.weeks_upper_week: mop_weeks_upper_week,
#         kw.every_xweeks: mop_every_xweeks,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_xweeks_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)
#     xweeks_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xweeks_args)
#     weeks_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.weeks_rope})
#     x_epoch_frame_min = 24000
#     assert xweeks_case.reason_lower == mop_weeks_lower_week
#     assert xweeks_case.reason_upper == mop_weeks_upper_week

#     # WHEN
#     add_frame_to_db_caseunit(
#         xweeks_case,
#         x_epoch_frame_min,
#         weeks_plan.close,
#         weeks_plan.denom,
#         weeks_plan.morph,
#     )

#     # THEN
#     assert xweeks_case.reason_lower != mop_weeks_lower_week
#     assert xweeks_case.reason_upper != mop_weeks_upper_week
#     assert xweeks_case.reason_lower == mop_weeks_lower_week + 3
#     assert xweeks_case.reason_upper == mop_weeks_upper_week + 3


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario8_adds_epoch_frame_Wraps_every_xweeks():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     mop_weeks_lower_week = 3
#     mop_weeks_upper_week = 4
#     mop_every_xweeks = 13
#     mop_xweeks_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.weeks_rope,
#         kw.reason_state: wx.weeks_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weeks_lower_week: mop_weeks_lower_week,
#         kw.weeks_upper_week: mop_weeks_upper_week,
#         kw.every_xweeks: mop_every_xweeks,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_xweeks_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_xweeks_args)
#     xweeks_case = person_plan_reason_caseunit_get_obj(bob_person, mop_xweeks_args)
#     weeks_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.weeks_rope})
#     x_epoch_frame_min = 50000
#     assert xweeks_case.reason_lower == mop_weeks_lower_week
#     assert xweeks_case.reason_upper == mop_weeks_upper_week

#     # WHEN
#     add_frame_to_db_caseunit(
#         xweeks_case,
#         x_epoch_frame_min,
#         weeks_plan.close,
#         weeks_plan.denom,
#         weeks_plan.morph,
#     )

#     # THEN
#     assert xweeks_case.reason_lower != mop_weeks_lower_week
#     assert xweeks_case.reason_upper != mop_weeks_upper_week
#     print(f"{x_epoch_frame_min//7200=}")
#     print(f"{mop_weeks_lower_week + (x_epoch_frame_min//7200)=}")
#     ex_lower = (mop_weeks_lower_week + (x_epoch_frame_min // 7200)) % mop_every_xweeks
#     ex_upper = (mop_weeks_upper_week + (x_epoch_frame_min // 7200)) % mop_every_xweeks
#     assert xweeks_case.reason_lower == ex_lower
#     assert xweeks_case.reason_upper == ex_upper


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario9_adds_epoch_frame_NoWrap_monthday():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthday_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: geo_rope,
#         kw.reason_state: geo_rope,
#         kw.month_label: wx.Geo,
#         kw.year_monthday_lower: 5,
#         kw.year_monthday_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_monthday_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)
#     year_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.five_year_rope})
#     monthday_case = person_plan_reason_caseunit_get_obj(bob_person, mop_monthday_args)

#     print(f"{monthday_case.reason_divisor=}")
#     x_epoch_frame_min = 500
#     geo_5_TimeNum = 43200
#     geo_8_TimeNum = 47520
#     assert monthday_case.reason_lower == geo_5_TimeNum
#     assert monthday_case.reason_upper == geo_8_TimeNum

#     # WHEN
#     add_frame_to_db_caseunit(
#         monthday_case,
#         x_epoch_frame_min,
#         year_plan.close,
#         year_plan.denom,
#         year_plan.morph,
#     )

#     # THEN
#     assert monthday_case.reason_lower != geo_5_TimeNum
#     assert monthday_case.reason_upper != geo_8_TimeNum
#     assert monthday_case.reason_lower == geo_5_TimeNum + x_epoch_frame_min
#     assert monthday_case.reason_upper == geo_8_TimeNum + x_epoch_frame_min


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario10_adds_epoch_frame_Wraps_monthday():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthday_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: geo_rope,
#         kw.reason_state: geo_rope,
#         kw.month_label: wx.Geo,
#         kw.year_monthday_lower: 5,
#         kw.year_monthday_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_monthday_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_monthday_args)
#     monthday_case = person_plan_reason_caseunit_get_obj(bob_person, mop_monthday_args)
#     year_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.five_year_rope})
#     x_epoch_frame_min = 5000000
#     geo_5_TimeNum = 43200
#     geo_8_TimeNum = 47520
#     assert monthday_case.reason_lower == geo_5_TimeNum
#     assert monthday_case.reason_upper == geo_8_TimeNum

#     # WHEN
#     add_frame_to_db_caseunit(
#         monthday_case,
#         x_epoch_frame_min,
#         year_plan.close,
#         year_plan.denom,
#         year_plan.morph,
#     )

#     # THEN
#     assert monthday_case.reason_lower != geo_5_TimeNum
#     assert monthday_case.reason_upper != geo_8_TimeNum
#     print(f"{(geo_5_TimeNum + x_epoch_frame_min) % 525600=}")
#     print(f"{(geo_8_TimeNum + x_epoch_frame_min) % 525600=}")
#     assert monthday_case.reason_lower == (geo_5_TimeNum + x_epoch_frame_min) % 525600
#     assert monthday_case.reason_upper == (geo_8_TimeNum + x_epoch_frame_min) % 525600


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario11_adds_epoch_frame_NoWrap_monthly():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.monthly_monthday_lower: 5,
#         kw.monthly_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_monthly_args)
#     geo_month_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_year_rope,
#         kw.reason_state: geo_rope,
#     }
#     assert person_plan_reason_caseunit_exists(bob_person, geo_month_args)
#     geo_case = person_plan_reason_caseunit_get_obj(bob_person, geo_month_args)
#     year_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.five_year_rope})

#     print(f"{geo_case.reason_divisor=}")
#     x_epoch_frame_min = 500
#     geo_5_TimeNum = 43200
#     geo_8_TimeNum = 47520
#     assert geo_case.reason_lower == geo_5_TimeNum
#     assert geo_case.reason_upper == geo_8_TimeNum

#     # WHEN
#     add_frame_to_db_caseunit(
#         geo_case, x_epoch_frame_min, year_plan.close, year_plan.denom, year_plan.morph
#     )

#     # THEN
#     assert geo_case.reason_lower != geo_5_TimeNum
#     assert geo_case.reason_upper != geo_8_TimeNum
#     assert geo_case.reason_lower == geo_5_TimeNum + x_epoch_frame_min
#     assert geo_case.reason_upper == geo_8_TimeNum + x_epoch_frame_min


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario12_adds_epoch_frame_Wraps_monthly():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     geo_rope = bob_person.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.monthly_monthday_lower: 5,
#         kw.monthly_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_monthly_args)
#     geo_month_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_year_rope,
#         kw.reason_state: geo_rope,
#     }
#     assert person_plan_reason_caseunit_exists(bob_person, geo_month_args)
#     geo_case = person_plan_reason_caseunit_get_obj(bob_person, geo_month_args)
#     year_plan = person_planunit_get_obj(bob_person, {kw.plan_rope: wx.five_year_rope})
#     x_epoch_frame_min = 5000000
#     geo_5_TimeNum = 43200
#     geo_8_TimeNum = 47520
#     assert geo_case.reason_lower == geo_5_TimeNum
#     assert geo_case.reason_upper == geo_8_TimeNum

#     # WHEN
#     add_frame_to_db_caseunit(
#         geo_case, x_epoch_frame_min, year_plan.close, year_plan.denom, year_plan.morph
#     )

#     # THEN
#     assert geo_case.reason_lower != geo_5_TimeNum
#     assert geo_case.reason_upper != geo_8_TimeNum
#     print(f"{(geo_5_TimeNum + x_epoch_frame_min) % 525600=}")
#     print(f"{(geo_8_TimeNum + x_epoch_frame_min) % 525600=}")
#     assert geo_case.reason_lower == (geo_5_TimeNum + x_epoch_frame_min) % 525600
#     assert geo_case.reason_upper == (geo_8_TimeNum + x_epoch_frame_min) % 525600


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario13_adds_epoch_frame_NoWrap_range():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_range_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_range_args)
#     epoch_args = {kw.plan_rope: wx.five_rope}
#     epoch_plan = person_planunit_get_obj(bob_person, epoch_args)
#     print(f"{get_range_attrs(epoch_plan)=}")
#     epoch_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)

#     x_epoch_frame_min = 500
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_db_caseunit(
#         epoch_case,
#         x_epoch_frame_min,
#         epoch_plan.close,
#         epoch_plan.denom,
#         epoch_plan.morph,
#     )

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min + x_epoch_frame_min
#     assert epoch_case.reason_upper == x_range_upper_min + x_epoch_frame_min


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario14_adds_epoch_frame_Wraps_range():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_range_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_range_args)
#     epoch_args = {kw.plan_rope: wx.five_rope}
#     epoch_plan = person_planunit_get_obj(bob_person, epoch_args)
#     print(f"{get_range_attrs(epoch_plan)=}")
#     epoch_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)

#     x_epoch_frame_min = epoch_plan.close + 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_db_caseunit(
#         epoch_case,
#         x_epoch_frame_min,
#         epoch_plan.close,
#         epoch_plan.denom,
#         epoch_plan.morph,
#     )

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_duration
#     print(
#         f"{x_range_lower_min + x_epoch_frame_min=} vs {epoch_plan.close} (epoch_length)"
#     )
#     expected_lower = (x_range_lower_min + x_epoch_frame_min) % epoch_plan.close
#     expected_upper = (x_range_upper_min + x_epoch_frame_min) % epoch_plan.close
#     assert epoch_case.reason_lower == expected_lower
#     assert epoch_case.reason_upper == expected_upper


# def test_add_frame_to_db_reasonunit_SetsAttr_Scenario0_AllCaseUnitsAre_epoch():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_range_args)
#     assert person_plan_reason_caseunit_exists(bob_person, mop_range_args)
#     epoch_args = {kw.plan_rope: wx.five_rope}
#     five_reason = person_plan_reasonunit_get_obj(bob_person, mop_range_args)
#     epoch_plan = person_planunit_get_obj(bob_person, epoch_args)
#     print(f"{get_range_attrs(epoch_plan)=}")
#     epoch_length = epoch_plan.close
#     epoch_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)

#     x_epoch_frame_min = epoch_length + 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_db_reasonunit(
#         five_reason,
#         x_epoch_frame_min,
#         epoch_plan.close,
#         epoch_plan.denom,
#         epoch_plan.morph,
#     )

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_duration
#     expected_lower = (x_range_lower_min + x_epoch_frame_min) % epoch_length
#     expected_upper = (x_range_upper_min + x_epoch_frame_min) % epoch_length
#     assert epoch_case.reason_lower == expected_lower
#     assert epoch_case.reason_upper == expected_upper


# def test_add_frame_to_db_factunit_SetsAttr_epoch_Scenario0_NoWrap():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_person.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     epoch_args = {kw.plan_rope: wx.mop_rope, kw.plan_rope: wx.five_rope}
#     epoch_plan = person_planunit_get_obj(bob_person, epoch_args)
#     assert person_plan_factunit_exists(bob_person, root_five_args)
#     root_five_fact = person_plan_factunit_get_obj(bob_person, root_five_args)
#     x_epoch_frame_min = 10005
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_db_factunit(root_five_fact, x_epoch_frame_min, epoch_plan.close)

#     # THEN
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     expected_lower = (x_lower_min + x_epoch_frame_min) % epoch_plan.close
#     expected_upper = (x_upper_min + x_epoch_frame_min) % epoch_plan.close
#     assert root_five_fact.fact_lower == expected_lower
#     assert root_five_fact.fact_upper == expected_upper


# def test_add_frame_to_db_factunit_SetsAttr_epoch_Scenario1_Wrap():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_person.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     epoch_args = {kw.plan_rope: wx.mop_rope, kw.plan_rope: wx.five_rope}
#     epoch_plan = person_planunit_get_obj(bob_person, epoch_args)
#     assert person_plan_factunit_exists(bob_person, root_five_args)
#     root_five_fact = person_plan_factunit_get_obj(bob_person, root_five_args)
#     x_epoch_frame_min = epoch_plan.close + 10010
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_db_factunit(root_five_fact, x_epoch_frame_min, epoch_plan.close)

#     # THEN
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     expected_lower = (x_lower_min + x_epoch_frame_min) % epoch_plan.close
#     expected_upper = (x_upper_min + x_epoch_frame_min) % epoch_plan.close
#     assert root_five_fact.fact_lower == expected_lower
#     assert root_five_fact.fact_upper == expected_upper


# def test_add_frame_to_db_personunit_SetsAttrs_Scenario0_OnlyEpochFactsAndReasons():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_person.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     epoch_args = {kw.plan_rope: wx.mop_rope, kw.plan_rope: wx.five_rope}
#     epoch_plan = person_planunit_get_obj(bob_person, epoch_args)
#     assert person_plan_factunit_exists(bob_person, root_five_args)
#     root_five_fact = person_plan_factunit_get_obj(bob_person, root_five_args)

#     five_reason = person_plan_reasonunit_get_obj(bob_person, mop_range_args)
#     epoch_length = epoch_plan.close
#     epoch_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)

#     x_epoch_frame_min = epoch_length + 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_db_personunit(bob_person, x_epoch_frame_min)

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_upper_min
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min


# def test_add_frame_to_db_personunit_SetsAttrs_Scenario1_FilterFactsAndReasonsEdited():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     add_epoch_planunit(bob_person, get_lizzy9_config())
#     lizzy9_str = get_lizzy9_config().get(kw.epoch_label)
#     time_rope = bob_person.make_l1_rope("time")
#     lizzy9_rope = bob_person.make_rope(time_rope, lizzy9_str)
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     mop_lizzy9_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: lizzy9_str,
#         kw.reason_context: lizzy9_rope,
#         kw.reason_state: lizzy9_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_five_args)
#     set_epoch_cases_by_args_dict(bob_person, mop_lizzy9_args)
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_person.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     bob_person.add_fact(lizzy9_rope, lizzy9_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     root_lizzy9_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: lizzy9_rope,
#     }
#     root_five_fact = person_plan_factunit_get_obj(bob_person, root_five_args)
#     root_lizzy9_fact = person_plan_factunit_get_obj(bob_person, root_lizzy9_args)
#     five_case = person_plan_reason_caseunit_get_obj(bob_person, mop_five_args)
#     lizzy9_case = person_plan_reason_caseunit_get_obj(bob_person, mop_lizzy9_args)

#     x_epoch_frame_min = 10005
#     assert five_case.reason_lower == x_range_lower_min
#     assert lizzy9_case.reason_lower == x_range_lower_min
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_lizzy9_fact.fact_lower == x_lower_min

#     # WHEN
#     add_frame_to_db_personunit(
#         bob_person, x_epoch_frame_min, required_context_subrope=wx.five_rope
#     )

#     # THEN
#     assert lizzy9_case.reason_lower == x_range_lower_min
#     assert root_lizzy9_fact.fact_lower == x_lower_min
#     assert five_case.reason_lower != x_range_lower_min
#     assert root_five_fact.fact_lower != x_lower_min


# def test_add_frame_to_db_personunit_SetsAttrs_Scenario2_IgnoreNonRangeReasonsFacts():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     bob_person.add_plan(wx.clean_rope)
#     bob_person.edit_plan_attr(
#         wx.mop_rope, reason_context=wx.clean_rope, reason_case=wx.clean_rope
#     )
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     mop_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.clean_rope,
#         kw.reason_state: wx.clean_rope,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_person.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     bob_person.add_fact(wx.clean_rope, wx.clean_rope)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     root_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.clean_rope,
#     }
#     assert person_plan_factunit_exists(bob_person, root_five_args)
#     assert person_plan_factunit_exists(bob_person, root_clean_args)
#     root_five_fact = person_plan_factunit_get_obj(bob_person, root_five_args)
#     root_clean_fact = person_plan_factunit_get_obj(bob_person, root_clean_args)
#     five_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
#     clean_case = person_plan_reason_caseunit_get_obj(bob_person, mop_clean_args)

#     x_epoch_frame_min = 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert five_case.reason_lower == x_range_lower_min
#     assert five_case.reason_upper == x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None

#     # WHEN
#     add_frame_to_db_personunit(bob_person, x_epoch_frame_min)

#     # THEN
#     assert five_case.reason_lower != x_range_lower_min
#     assert five_case.reason_upper != x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None


# def test_add_epoch_frame_to_db_personunit_SetsAttrs_Scenario0_IgnoreNonRangeReasonsFacts():
#     # ESTABLISH
#     bob_person = get_bob_five_person()
#     bob_person.add_plan(wx.clean_rope)
#     bob_person.edit_plan_attr(
#         wx.mop_rope, reason_context=wx.clean_rope, reason_case=wx.clean_rope
#     )
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     mop_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.clean_rope,
#         kw.reason_state: wx.clean_rope,
#     }
#     set_epoch_cases_by_args_dict(bob_person, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_person.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     bob_person.add_fact(wx.clean_rope, wx.clean_rope)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     root_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_person.planroot.get_plan_rope(),
#         kw.fact_context: wx.clean_rope,
#     }
#     assert person_plan_factunit_exists(bob_person, root_five_args)
#     assert person_plan_factunit_exists(bob_person, root_clean_args)
#     root_five_fact = person_plan_factunit_get_obj(bob_person, root_five_args)
#     root_clean_fact = person_plan_factunit_get_obj(bob_person, root_clean_args)
#     five_case = person_plan_reason_caseunit_get_obj(bob_person, mop_range_args)
#     clean_case = person_plan_reason_caseunit_get_obj(bob_person, mop_clean_args)

#     x_epoch_frame_min = 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert five_case.reason_lower == x_range_lower_min
#     assert five_case.reason_upper == x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None

#     # WHEN
#     add_epoch_frame_to_db_personunit(
#         x_person=bob_person, epoch_label=wx.five_str, epoch_frame_min=x_epoch_frame_min
#     )

#     # THEN
#     assert five_case.reason_lower != x_range_lower_min
#     assert five_case.reason_upper != x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None
