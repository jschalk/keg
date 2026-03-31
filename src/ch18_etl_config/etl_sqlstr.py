from sqlite3 import Connection as sqlite3_Connection
from src.ch00_py.db_toolbox import (
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
)
from src.ch13_time.epoch_main import DEFAULT_EPOCH_LENGTH, get_c400_constants
from src.ch17_idea.idea_config import get_idea_config_dict, get_quick_ideas_column_ref
from src.ch17_idea.idea_db_tool import create_idea_sorted_table, get_default_sorted_list
from src.ch18_etl_config._ref.ch18_semantic_types import KnotTerm
from src.ch18_etl_config.etl_config import create_prime_tablename

CREATE_MMTBUDD_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, bud_time_otx INTEGER, bud_time_inx INTEGER, knot TEXT, quota REAL, celldepth INTEGER)"""
CREATE_MMTBUDD_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, bud_time INTEGER, knot TEXT, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_MMTBUDD_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_vld (moment_rope TEXT, person_name TEXT, bud_time INTEGER, knot TEXT, quota REAL, celldepth INTEGER)"""
CREATE_MMTBUDD_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, bud_time INTEGER, knot TEXT, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_MMTBUDD_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, bud_time INTEGER, knot TEXT, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_MMTBUDD_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, bud_time INTEGER, knot TEXT, quota REAL, celldepth INTEGER)"""
CREATE_MMTHOUR_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, knot TEXT)"""
CREATE_MMTHOUR_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, cumulative_minute INTEGER, hour_label_otx TEXT, hour_label_inx TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTHOUR_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_vld (moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, knot TEXT)"""
CREATE_MMTHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTHOUR_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_minute INTEGER, hour_label TEXT, knot TEXT)"""
CREATE_MMTMONT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, knot TEXT)"""
CREATE_MMTMONT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, cumulative_day INTEGER, month_label_otx TEXT, month_label_inx TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTMONT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_vld (moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, knot TEXT)"""
CREATE_MMTMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTMONT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, cumulative_day INTEGER, month_label TEXT, knot TEXT)"""
CREATE_MMTOFFI_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time_otx INTEGER, offi_time_inx INTEGER, knot TEXT)"""
CREATE_MMTOFFI_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, offi_time INTEGER, knot TEXT, error_message TEXT)"""
CREATE_MMTOFFI_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_vld (moment_rope TEXT, offi_time INTEGER, knot TEXT)"""
CREATE_MMTOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time INTEGER, knot TEXT, error_message TEXT)"""
CREATE_MMTOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time INTEGER, knot TEXT, error_message TEXT)"""
CREATE_MMTOFFI_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, offi_time INTEGER, knot TEXT)"""
CREATE_MMTPAYY_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, tran_time_otx INTEGER, tran_time_inx INTEGER, amount REAL, knot TEXT)"""
CREATE_MMTPAYY_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, contact_name_otx TEXT, contact_name_inx TEXT, tran_time INTEGER, amount REAL, knot TEXT, error_message TEXT)"""
CREATE_MMTPAYY_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_vld (moment_rope TEXT, person_name TEXT, contact_name TEXT, tran_time INTEGER, amount REAL, knot TEXT)"""
CREATE_MMTPAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, tran_time INTEGER, amount REAL, knot TEXT, error_message TEXT)"""
CREATE_MMTPAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, tran_time INTEGER, amount REAL, knot TEXT, error_message TEXT)"""
CREATE_MMTPAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, tran_time INTEGER, amount REAL, knot TEXT)"""
CREATE_MMTUNIT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_MMTUNIT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, epoch_label_otx TEXT, epoch_label_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_MMTUNIT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_vld (moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_MMTUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_MMTUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_MMTUNIT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_MMTWEEK_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, knot TEXT)"""
CREATE_MMTWEEK_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, weekday_order INTEGER, weekday_label_otx TEXT, weekday_label_inx TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTWEEK_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_vld (moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, knot TEXT)"""
CREATE_MMTWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, knot TEXT, error_message TEXT)"""
CREATE_MMTWEEK_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, weekday_order INTEGER, weekday_label TEXT, knot TEXT)"""
CREATE_NABTIME_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER)"""
CREATE_NABTIME_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, otx_time INTEGER, inx_time INTEGER, error_message TEXT)"""
CREATE_NABTIME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER, error_message TEXT)"""
CREATE_NABTIME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER, error_message TEXT)"""
CREATE_NABTIME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS nabu_timenum_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, otx_time INTEGER, inx_time INTEGER)"""
CREATE_PRNAWAR_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PRNAWAR_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, awardee_title_ERASE_otx TEXT, awardee_title_ERASE_inx TEXT)"""
CREATE_PRNAWAR_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PRNAWAR_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, knot TEXT)"""
CREATE_PRNAWAR_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, awardee_title_otx TEXT, awardee_title_inx TEXT, give_force REAL, take_force REAL, knot TEXT)"""
CREATE_PRNAWAR_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, knot TEXT)"""
CREATE_PRNAWAR_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT, error_message TEXT)"""
CREATE_PRNAWAR_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PRNAWAR_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"""
CREATE_PRNAWAR_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNAWAR_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNAWAR_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, knot TEXT)"""
CREATE_PRNCASE_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PRNCASE_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_ERASE_otx TEXT, reason_state_ERASE_inx TEXT)"""
CREATE_PRNCASE_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PRNCASE_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower_otx REAL, reason_lower_inx REAL, reason_upper_otx REAL, reason_upper_inx REAL, reason_divisor INTEGER, knot TEXT, context_plan_close REAL, context_plan_denom REAL, context_plan_morph REAL, inx_epoch_diff INTEGER)"""
CREATE_PRNCASE_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_otx TEXT, reason_state_inx TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT)"""
CREATE_PRNCASE_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT)"""
CREATE_PRNCASE_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT, error_message TEXT)"""
CREATE_PRNCASE_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PRNCASE_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"""
CREATE_PRNCASE_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNCASE_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNCASE_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT)"""
CREATE_PRNFACT_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PRNFACT_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, fact_context_ERASE_otx TEXT, fact_context_ERASE_inx TEXT)"""
CREATE_PRNFACT_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PRNFACT_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower_otx REAL, fact_lower_inx REAL, fact_upper_otx REAL, fact_upper_inx REAL, knot TEXT, context_plan_close REAL, context_plan_denom REAL, context_plan_morph REAL, inx_epoch_diff INTEGER)"""
CREATE_PRNFACT_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, fact_context_otx TEXT, fact_context_inx TEXT, fact_state_otx TEXT, fact_state_inx TEXT, fact_lower REAL, fact_upper REAL, knot TEXT)"""
CREATE_PRNFACT_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, knot TEXT)"""
CREATE_PRNFACT_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT, error_message TEXT)"""
CREATE_PRNFACT_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PRNFACT_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"""
CREATE_PRNFACT_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNFACT_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNFACT_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, knot TEXT)"""
CREATE_PRNHEAL_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PRNHEAL_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"""
CREATE_PRNHEAL_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PRNHEAL_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name TEXT, knot TEXT)"""
CREATE_PRNHEAL_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT, knot TEXT)"""
CREATE_PRNHEAL_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name TEXT, knot TEXT)"""
CREATE_PRNHEAL_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT, error_message TEXT)"""
CREATE_PRNHEAL_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PRNHEAL_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"""
CREATE_PRNHEAL_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name TEXT, knot TEXT, error_message TEXT)"""
CREATE_PRNHEAL_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name TEXT, knot TEXT, error_message TEXT)"""
CREATE_PRNHEAL_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, healer_name TEXT, knot TEXT)"""
CREATE_PRNLABO_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"""
CREATE_PRNLABO_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, labor_title_ERASE_otx TEXT, labor_title_ERASE_inx TEXT)"""
CREATE_PRNLABO_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"""
CREATE_PRNLABO_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title TEXT, solo INTEGER, knot TEXT)"""
CREATE_PRNLABO_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, labor_title_otx TEXT, labor_title_inx TEXT, solo INTEGER, knot TEXT)"""
CREATE_PRNLABO_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title TEXT, solo INTEGER, knot TEXT)"""
CREATE_PRNLABO_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT, error_message TEXT)"""
CREATE_PRNLABO_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"""
CREATE_PRNLABO_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"""
CREATE_PRNLABO_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title TEXT, solo INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNLABO_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title TEXT, solo INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNLABO_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, labor_title TEXT, solo INTEGER, knot TEXT)"""
CREATE_PRNMEMB_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_del_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title_ERASE TEXT)"""
CREATE_PRNMEMB_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, contact_name_otx TEXT, contact_name_inx TEXT, group_title_ERASE_otx TEXT, group_title_ERASE_inx TEXT)"""
CREATE_PRNMEMB_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_del_h_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title_ERASE TEXT)"""
CREATE_PRNMEMB_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_put_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, knot TEXT)"""
CREATE_PRNMEMB_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, contact_name_otx TEXT, contact_name_inx TEXT, group_title_otx TEXT, group_title_inx TEXT, group_cred_lumen REAL, group_debt_lumen REAL, knot TEXT)"""
CREATE_PRNMEMB_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_put_h_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, knot TEXT)"""
CREATE_PRNMEMB_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_del_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title_ERASE TEXT, error_message TEXT)"""
CREATE_PRNMEMB_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title_ERASE TEXT)"""
CREATE_PRNMEMB_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_del_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title_ERASE TEXT)"""
CREATE_PRNMEMB_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_put_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNMEMB_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNMEMB_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_put_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, knot TEXT)"""
CREATE_PRNPLAN_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope_ERASE TEXT)"""
CREATE_PRNPLAN_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_ERASE_otx TEXT, plan_rope_ERASE_inx TEXT)"""
CREATE_PRNPLAN_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope_ERASE TEXT)"""
CREATE_PRNPLAN_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, knot TEXT)"""
CREATE_PRNPLAN_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, knot TEXT)"""
CREATE_PRNPLAN_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, knot TEXT)"""
CREATE_PRNPLAN_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope_ERASE TEXT, error_message TEXT)"""
CREATE_PRNPLAN_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope_ERASE TEXT)"""
CREATE_PRNPLAN_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope_ERASE TEXT)"""
CREATE_PRNPLAN_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNPLAN_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNPLAN_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, knot TEXT)"""
CREATE_PRNCONT_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_del_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name_ERASE TEXT)"""
CREATE_PRNCONT_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, contact_name_ERASE_otx TEXT, contact_name_ERASE_inx TEXT)"""
CREATE_PRNCONT_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_del_h_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name_ERASE TEXT)"""
CREATE_PRNCONT_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_put_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, knot TEXT)"""
CREATE_PRNCONT_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, contact_name_otx TEXT, contact_name_inx TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, knot TEXT)"""
CREATE_PRNCONT_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_put_h_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, knot TEXT)"""
CREATE_PRNCONT_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_del_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name_ERASE TEXT, error_message TEXT)"""
CREATE_PRNCONT_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name_ERASE TEXT)"""
CREATE_PRNCONT_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_del_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name_ERASE TEXT)"""
CREATE_PRNCONT_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_put_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNCONT_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNCONT_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_put_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, contact_name TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, knot TEXT)"""
CREATE_PRNREAS_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_del_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PRNREAS_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_ERASE_otx TEXT, reason_context_ERASE_inx TEXT)"""
CREATE_PRNREAS_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_del_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PRNREAS_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_put_h_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, knot TEXT)"""
CREATE_PRNREAS_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, active_requisite INTEGER, knot TEXT)"""
CREATE_PRNREAS_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_put_h_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, knot TEXT)"""
CREATE_PRNREAS_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_del_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT, error_message TEXT)"""
CREATE_PRNREAS_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PRNREAS_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_del_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"""
CREATE_PRNREAS_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_put_s_agg (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNREAS_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, knot TEXT, error_message TEXT)"""
CREATE_PRNREAS_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_put_s_vld (spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, knot TEXT)"""
CREATE_PRNUNIT_DEL_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_del_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name_ERASE TEXT)"""
CREATE_PRNUNIT_DEL_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_del_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_ERASE_otx TEXT, person_name_ERASE_inx TEXT)"""
CREATE_PRNUNIT_DEL_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_del_h_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name_ERASE TEXT)"""
CREATE_PRNUNIT_PUT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_put_h_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT)"""
CREATE_PRNUNIT_PUT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_put_h_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_rope_otx TEXT, moment_rope_inx TEXT, person_name_otx TEXT, person_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT)"""
CREATE_PRNUNIT_PUT_HEARD_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_put_h_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT)"""
CREATE_PRNUNIT_DEL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_del_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name_ERASE TEXT, error_message TEXT)"""
CREATE_PRNUNIT_DEL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_del_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name_ERASE TEXT)"""
CREATE_PRNUNIT_DEL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_del_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name_ERASE TEXT)"""
CREATE_PRNUNIT_PUT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_put_s_agg (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNUNIT_PUT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_put_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, error_message TEXT)"""
CREATE_PRNUNIT_PUT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_put_s_vld (spark_num INTEGER, face_name TEXT, moment_rope TEXT, person_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT)"""
CREATE_TRLCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_agg (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""
CREATE_TRLCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_raw (source_dimen TEXT, face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_vld (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""
CREATE_TRLLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_agg (spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_vld (spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""
CREATE_TRLNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_agg (spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_vld (spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_TRLROPE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_agg (spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLROPE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLROPE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_vld (spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT)"""
CREATE_TRLTITL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_agg (spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLTITL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLTITL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_vld (spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT)"""


def get_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "person_plan_awardunit_del_h_agg": CREATE_PRNAWAR_DEL_HEARD_AGG_SQLSTR,
        "person_plan_awardunit_del_h_raw": CREATE_PRNAWAR_DEL_HEARD_RAW_SQLSTR,
        "person_plan_awardunit_del_h_vld": CREATE_PRNAWAR_DEL_HEARD_VLD_SQLSTR,
        "person_plan_awardunit_put_h_agg": CREATE_PRNAWAR_PUT_HEARD_AGG_SQLSTR,
        "person_plan_awardunit_put_h_raw": CREATE_PRNAWAR_PUT_HEARD_RAW_SQLSTR,
        "person_plan_awardunit_put_h_vld": CREATE_PRNAWAR_PUT_HEARD_VLD_SQLSTR,
        "person_plan_awardunit_del_s_agg": CREATE_PRNAWAR_DEL_SOUND_AGG_SQLSTR,
        "person_plan_awardunit_del_s_raw": CREATE_PRNAWAR_DEL_SOUND_RAW_SQLSTR,
        "person_plan_awardunit_del_s_vld": CREATE_PRNAWAR_DEL_SOUND_VLD_SQLSTR,
        "person_plan_awardunit_put_s_agg": CREATE_PRNAWAR_PUT_SOUND_AGG_SQLSTR,
        "person_plan_awardunit_put_s_raw": CREATE_PRNAWAR_PUT_SOUND_RAW_SQLSTR,
        "person_plan_awardunit_put_s_vld": CREATE_PRNAWAR_PUT_SOUND_VLD_SQLSTR,
        "person_plan_factunit_del_h_agg": CREATE_PRNFACT_DEL_HEARD_AGG_SQLSTR,
        "person_plan_factunit_del_h_raw": CREATE_PRNFACT_DEL_HEARD_RAW_SQLSTR,
        "person_plan_factunit_del_h_vld": CREATE_PRNFACT_DEL_HEARD_VLD_SQLSTR,
        "person_plan_factunit_put_h_agg": CREATE_PRNFACT_PUT_HEARD_AGG_SQLSTR,
        "person_plan_factunit_put_h_raw": CREATE_PRNFACT_PUT_HEARD_RAW_SQLSTR,
        "person_plan_factunit_put_h_vld": CREATE_PRNFACT_PUT_HEARD_VLD_SQLSTR,
        "person_plan_factunit_del_s_agg": CREATE_PRNFACT_DEL_SOUND_AGG_SQLSTR,
        "person_plan_factunit_del_s_raw": CREATE_PRNFACT_DEL_SOUND_RAW_SQLSTR,
        "person_plan_factunit_del_s_vld": CREATE_PRNFACT_DEL_SOUND_VLD_SQLSTR,
        "person_plan_factunit_put_s_agg": CREATE_PRNFACT_PUT_SOUND_AGG_SQLSTR,
        "person_plan_factunit_put_s_raw": CREATE_PRNFACT_PUT_SOUND_RAW_SQLSTR,
        "person_plan_factunit_put_s_vld": CREATE_PRNFACT_PUT_SOUND_VLD_SQLSTR,
        "person_plan_healerunit_del_h_agg": CREATE_PRNHEAL_DEL_HEARD_AGG_SQLSTR,
        "person_plan_healerunit_del_h_raw": CREATE_PRNHEAL_DEL_HEARD_RAW_SQLSTR,
        "person_plan_healerunit_del_h_vld": CREATE_PRNHEAL_DEL_HEARD_VLD_SQLSTR,
        "person_plan_healerunit_put_h_agg": CREATE_PRNHEAL_PUT_HEARD_AGG_SQLSTR,
        "person_plan_healerunit_put_h_raw": CREATE_PRNHEAL_PUT_HEARD_RAW_SQLSTR,
        "person_plan_healerunit_put_h_vld": CREATE_PRNHEAL_PUT_HEARD_VLD_SQLSTR,
        "person_plan_healerunit_del_s_agg": CREATE_PRNHEAL_DEL_SOUND_AGG_SQLSTR,
        "person_plan_healerunit_del_s_raw": CREATE_PRNHEAL_DEL_SOUND_RAW_SQLSTR,
        "person_plan_healerunit_del_s_vld": CREATE_PRNHEAL_DEL_SOUND_VLD_SQLSTR,
        "person_plan_healerunit_put_s_agg": CREATE_PRNHEAL_PUT_SOUND_AGG_SQLSTR,
        "person_plan_healerunit_put_s_raw": CREATE_PRNHEAL_PUT_SOUND_RAW_SQLSTR,
        "person_plan_healerunit_put_s_vld": CREATE_PRNHEAL_PUT_SOUND_VLD_SQLSTR,
        "person_plan_laborunit_del_h_agg": CREATE_PRNLABO_DEL_HEARD_AGG_SQLSTR,
        "person_plan_laborunit_del_h_raw": CREATE_PRNLABO_DEL_HEARD_RAW_SQLSTR,
        "person_plan_laborunit_del_h_vld": CREATE_PRNLABO_DEL_HEARD_VLD_SQLSTR,
        "person_plan_laborunit_put_h_agg": CREATE_PRNLABO_PUT_HEARD_AGG_SQLSTR,
        "person_plan_laborunit_put_h_raw": CREATE_PRNLABO_PUT_HEARD_RAW_SQLSTR,
        "person_plan_laborunit_put_h_vld": CREATE_PRNLABO_PUT_HEARD_VLD_SQLSTR,
        "person_plan_laborunit_del_s_agg": CREATE_PRNLABO_DEL_SOUND_AGG_SQLSTR,
        "person_plan_laborunit_del_s_raw": CREATE_PRNLABO_DEL_SOUND_RAW_SQLSTR,
        "person_plan_laborunit_del_s_vld": CREATE_PRNLABO_DEL_SOUND_VLD_SQLSTR,
        "person_plan_laborunit_put_s_agg": CREATE_PRNLABO_PUT_SOUND_AGG_SQLSTR,
        "person_plan_laborunit_put_s_raw": CREATE_PRNLABO_PUT_SOUND_RAW_SQLSTR,
        "person_plan_laborunit_put_s_vld": CREATE_PRNLABO_PUT_SOUND_VLD_SQLSTR,
        "person_plan_reason_caseunit_del_h_agg": CREATE_PRNCASE_DEL_HEARD_AGG_SQLSTR,
        "person_plan_reason_caseunit_del_h_raw": CREATE_PRNCASE_DEL_HEARD_RAW_SQLSTR,
        "person_plan_reason_caseunit_del_h_vld": CREATE_PRNCASE_DEL_HEARD_VLD_SQLSTR,
        "person_plan_reason_caseunit_put_h_agg": CREATE_PRNCASE_PUT_HEARD_AGG_SQLSTR,
        "person_plan_reason_caseunit_put_h_raw": CREATE_PRNCASE_PUT_HEARD_RAW_SQLSTR,
        "person_plan_reason_caseunit_put_h_vld": CREATE_PRNCASE_PUT_HEARD_VLD_SQLSTR,
        "person_plan_reason_caseunit_del_s_agg": CREATE_PRNCASE_DEL_SOUND_AGG_SQLSTR,
        "person_plan_reason_caseunit_del_s_raw": CREATE_PRNCASE_DEL_SOUND_RAW_SQLSTR,
        "person_plan_reason_caseunit_del_s_vld": CREATE_PRNCASE_DEL_SOUND_VLD_SQLSTR,
        "person_plan_reason_caseunit_put_s_agg": CREATE_PRNCASE_PUT_SOUND_AGG_SQLSTR,
        "person_plan_reason_caseunit_put_s_raw": CREATE_PRNCASE_PUT_SOUND_RAW_SQLSTR,
        "person_plan_reason_caseunit_put_s_vld": CREATE_PRNCASE_PUT_SOUND_VLD_SQLSTR,
        "person_plan_reasonunit_del_h_agg": CREATE_PRNREAS_DEL_HEARD_AGG_SQLSTR,
        "person_plan_reasonunit_del_h_raw": CREATE_PRNREAS_DEL_HEARD_RAW_SQLSTR,
        "person_plan_reasonunit_del_h_vld": CREATE_PRNREAS_DEL_HEARD_VLD_SQLSTR,
        "person_plan_reasonunit_put_h_agg": CREATE_PRNREAS_PUT_HEARD_AGG_SQLSTR,
        "person_plan_reasonunit_put_h_raw": CREATE_PRNREAS_PUT_HEARD_RAW_SQLSTR,
        "person_plan_reasonunit_put_h_vld": CREATE_PRNREAS_PUT_HEARD_VLD_SQLSTR,
        "person_plan_reasonunit_del_s_agg": CREATE_PRNREAS_DEL_SOUND_AGG_SQLSTR,
        "person_plan_reasonunit_del_s_raw": CREATE_PRNREAS_DEL_SOUND_RAW_SQLSTR,
        "person_plan_reasonunit_del_s_vld": CREATE_PRNREAS_DEL_SOUND_VLD_SQLSTR,
        "person_plan_reasonunit_put_s_agg": CREATE_PRNREAS_PUT_SOUND_AGG_SQLSTR,
        "person_plan_reasonunit_put_s_raw": CREATE_PRNREAS_PUT_SOUND_RAW_SQLSTR,
        "person_plan_reasonunit_put_s_vld": CREATE_PRNREAS_PUT_SOUND_VLD_SQLSTR,
        "person_planunit_del_h_agg": CREATE_PRNPLAN_DEL_HEARD_AGG_SQLSTR,
        "person_planunit_del_h_raw": CREATE_PRNPLAN_DEL_HEARD_RAW_SQLSTR,
        "person_planunit_del_h_vld": CREATE_PRNPLAN_DEL_HEARD_VLD_SQLSTR,
        "person_planunit_put_h_agg": CREATE_PRNPLAN_PUT_HEARD_AGG_SQLSTR,
        "person_planunit_put_h_raw": CREATE_PRNPLAN_PUT_HEARD_RAW_SQLSTR,
        "person_planunit_put_h_vld": CREATE_PRNPLAN_PUT_HEARD_VLD_SQLSTR,
        "person_planunit_del_s_agg": CREATE_PRNPLAN_DEL_SOUND_AGG_SQLSTR,
        "person_planunit_del_s_raw": CREATE_PRNPLAN_DEL_SOUND_RAW_SQLSTR,
        "person_planunit_del_s_vld": CREATE_PRNPLAN_DEL_SOUND_VLD_SQLSTR,
        "person_planunit_put_s_agg": CREATE_PRNPLAN_PUT_SOUND_AGG_SQLSTR,
        "person_planunit_put_s_raw": CREATE_PRNPLAN_PUT_SOUND_RAW_SQLSTR,
        "person_planunit_put_s_vld": CREATE_PRNPLAN_PUT_SOUND_VLD_SQLSTR,
        "person_contact_membership_del_h_agg": CREATE_PRNMEMB_DEL_HEARD_AGG_SQLSTR,
        "person_contact_membership_del_h_raw": CREATE_PRNMEMB_DEL_HEARD_RAW_SQLSTR,
        "person_contact_membership_del_h_vld": CREATE_PRNMEMB_DEL_HEARD_VLD_SQLSTR,
        "person_contact_membership_put_h_agg": CREATE_PRNMEMB_PUT_HEARD_AGG_SQLSTR,
        "person_contact_membership_put_h_raw": CREATE_PRNMEMB_PUT_HEARD_RAW_SQLSTR,
        "person_contact_membership_put_h_vld": CREATE_PRNMEMB_PUT_HEARD_VLD_SQLSTR,
        "person_contact_membership_del_s_agg": CREATE_PRNMEMB_DEL_SOUND_AGG_SQLSTR,
        "person_contact_membership_del_s_raw": CREATE_PRNMEMB_DEL_SOUND_RAW_SQLSTR,
        "person_contact_membership_del_s_vld": CREATE_PRNMEMB_DEL_SOUND_VLD_SQLSTR,
        "person_contact_membership_put_s_agg": CREATE_PRNMEMB_PUT_SOUND_AGG_SQLSTR,
        "person_contact_membership_put_s_raw": CREATE_PRNMEMB_PUT_SOUND_RAW_SQLSTR,
        "person_contact_membership_put_s_vld": CREATE_PRNMEMB_PUT_SOUND_VLD_SQLSTR,
        "person_contactunit_del_h_agg": CREATE_PRNCONT_DEL_HEARD_AGG_SQLSTR,
        "person_contactunit_del_h_raw": CREATE_PRNCONT_DEL_HEARD_RAW_SQLSTR,
        "person_contactunit_del_h_vld": CREATE_PRNCONT_DEL_HEARD_VLD_SQLSTR,
        "person_contactunit_put_h_agg": CREATE_PRNCONT_PUT_HEARD_AGG_SQLSTR,
        "person_contactunit_put_h_raw": CREATE_PRNCONT_PUT_HEARD_RAW_SQLSTR,
        "person_contactunit_put_h_vld": CREATE_PRNCONT_PUT_HEARD_VLD_SQLSTR,
        "person_contactunit_del_s_agg": CREATE_PRNCONT_DEL_SOUND_AGG_SQLSTR,
        "person_contactunit_del_s_raw": CREATE_PRNCONT_DEL_SOUND_RAW_SQLSTR,
        "person_contactunit_del_s_vld": CREATE_PRNCONT_DEL_SOUND_VLD_SQLSTR,
        "person_contactunit_put_s_agg": CREATE_PRNCONT_PUT_SOUND_AGG_SQLSTR,
        "person_contactunit_put_s_raw": CREATE_PRNCONT_PUT_SOUND_RAW_SQLSTR,
        "person_contactunit_put_s_vld": CREATE_PRNCONT_PUT_SOUND_VLD_SQLSTR,
        "personunit_del_h_agg": CREATE_PRNUNIT_DEL_HEARD_AGG_SQLSTR,
        "personunit_del_h_raw": CREATE_PRNUNIT_DEL_HEARD_RAW_SQLSTR,
        "personunit_del_h_vld": CREATE_PRNUNIT_DEL_HEARD_VLD_SQLSTR,
        "personunit_put_h_agg": CREATE_PRNUNIT_PUT_HEARD_AGG_SQLSTR,
        "personunit_put_h_raw": CREATE_PRNUNIT_PUT_HEARD_RAW_SQLSTR,
        "personunit_put_h_vld": CREATE_PRNUNIT_PUT_HEARD_VLD_SQLSTR,
        "personunit_del_s_agg": CREATE_PRNUNIT_DEL_SOUND_AGG_SQLSTR,
        "personunit_del_s_raw": CREATE_PRNUNIT_DEL_SOUND_RAW_SQLSTR,
        "personunit_del_s_vld": CREATE_PRNUNIT_DEL_SOUND_VLD_SQLSTR,
        "personunit_put_s_agg": CREATE_PRNUNIT_PUT_SOUND_AGG_SQLSTR,
        "personunit_put_s_raw": CREATE_PRNUNIT_PUT_SOUND_RAW_SQLSTR,
        "personunit_put_s_vld": CREATE_PRNUNIT_PUT_SOUND_VLD_SQLSTR,
        "moment_budunit_h_agg": CREATE_MMTBUDD_HEARD_AGG_SQLSTR,
        "moment_budunit_h_raw": CREATE_MMTBUDD_HEARD_RAW_SQLSTR,
        "moment_budunit_h_vld": CREATE_MMTBUDD_HEARD_VLD_SQLSTR,
        "moment_budunit_s_agg": CREATE_MMTBUDD_SOUND_AGG_SQLSTR,
        "moment_budunit_s_raw": CREATE_MMTBUDD_SOUND_RAW_SQLSTR,
        "moment_budunit_s_vld": CREATE_MMTBUDD_SOUND_VLD_SQLSTR,
        "moment_epoch_hour_h_agg": CREATE_MMTHOUR_HEARD_AGG_SQLSTR,
        "moment_epoch_hour_h_raw": CREATE_MMTHOUR_HEARD_RAW_SQLSTR,
        "moment_epoch_hour_h_vld": CREATE_MMTHOUR_HEARD_VLD_SQLSTR,
        "moment_epoch_hour_s_agg": CREATE_MMTHOUR_SOUND_AGG_SQLSTR,
        "moment_epoch_hour_s_raw": CREATE_MMTHOUR_SOUND_RAW_SQLSTR,
        "moment_epoch_hour_s_vld": CREATE_MMTHOUR_SOUND_VLD_SQLSTR,
        "moment_epoch_month_h_agg": CREATE_MMTMONT_HEARD_AGG_SQLSTR,
        "moment_epoch_month_h_raw": CREATE_MMTMONT_HEARD_RAW_SQLSTR,
        "moment_epoch_month_h_vld": CREATE_MMTMONT_HEARD_VLD_SQLSTR,
        "moment_epoch_month_s_agg": CREATE_MMTMONT_SOUND_AGG_SQLSTR,
        "moment_epoch_month_s_raw": CREATE_MMTMONT_SOUND_RAW_SQLSTR,
        "moment_epoch_month_s_vld": CREATE_MMTMONT_SOUND_VLD_SQLSTR,
        "moment_epoch_weekday_h_agg": CREATE_MMTWEEK_HEARD_AGG_SQLSTR,
        "moment_epoch_weekday_h_raw": CREATE_MMTWEEK_HEARD_RAW_SQLSTR,
        "moment_epoch_weekday_h_vld": CREATE_MMTWEEK_HEARD_VLD_SQLSTR,
        "moment_epoch_weekday_s_agg": CREATE_MMTWEEK_SOUND_AGG_SQLSTR,
        "moment_epoch_weekday_s_raw": CREATE_MMTWEEK_SOUND_RAW_SQLSTR,
        "moment_epoch_weekday_s_vld": CREATE_MMTWEEK_SOUND_VLD_SQLSTR,
        "moment_paybook_h_agg": CREATE_MMTPAYY_HEARD_AGG_SQLSTR,
        "moment_paybook_h_raw": CREATE_MMTPAYY_HEARD_RAW_SQLSTR,
        "moment_paybook_h_vld": CREATE_MMTPAYY_HEARD_VLD_SQLSTR,
        "moment_paybook_s_agg": CREATE_MMTPAYY_SOUND_AGG_SQLSTR,
        "moment_paybook_s_raw": CREATE_MMTPAYY_SOUND_RAW_SQLSTR,
        "moment_paybook_s_vld": CREATE_MMTPAYY_SOUND_VLD_SQLSTR,
        "moment_timeoffi_h_agg": CREATE_MMTOFFI_HEARD_AGG_SQLSTR,
        "moment_timeoffi_h_raw": CREATE_MMTOFFI_HEARD_RAW_SQLSTR,
        "moment_timeoffi_h_vld": CREATE_MMTOFFI_HEARD_VLD_SQLSTR,
        "moment_timeoffi_s_agg": CREATE_MMTOFFI_SOUND_AGG_SQLSTR,
        "moment_timeoffi_s_raw": CREATE_MMTOFFI_SOUND_RAW_SQLSTR,
        "moment_timeoffi_s_vld": CREATE_MMTOFFI_SOUND_VLD_SQLSTR,
        "momentunit_h_agg": CREATE_MMTUNIT_HEARD_AGG_SQLSTR,
        "momentunit_h_raw": CREATE_MMTUNIT_HEARD_RAW_SQLSTR,
        "momentunit_h_vld": CREATE_MMTUNIT_HEARD_VLD_SQLSTR,
        "momentunit_s_agg": CREATE_MMTUNIT_SOUND_AGG_SQLSTR,
        "momentunit_s_raw": CREATE_MMTUNIT_SOUND_RAW_SQLSTR,
        "momentunit_s_vld": CREATE_MMTUNIT_SOUND_VLD_SQLSTR,
        "nabu_timenum_h_agg": CREATE_NABTIME_HEARD_AGG_SQLSTR,
        "nabu_timenum_h_raw": CREATE_NABTIME_HEARD_RAW_SQLSTR,
        "nabu_timenum_s_agg": CREATE_NABTIME_SOUND_AGG_SQLSTR,
        "nabu_timenum_s_raw": CREATE_NABTIME_SOUND_RAW_SQLSTR,
        "nabu_timenum_s_vld": CREATE_NABTIME_SOUND_VLD_SQLSTR,
        "translate_core_s_agg": CREATE_TRLCORE_SOUND_AGG_SQLSTR,
        "translate_core_s_raw": CREATE_TRLCORE_SOUND_RAW_SQLSTR,
        "translate_core_s_vld": CREATE_TRLCORE_SOUND_VLD_SQLSTR,
        "translate_label_s_agg": CREATE_TRLLABE_SOUND_AGG_SQLSTR,
        "translate_label_s_raw": CREATE_TRLLABE_SOUND_RAW_SQLSTR,
        "translate_label_s_vld": CREATE_TRLLABE_SOUND_VLD_SQLSTR,
        "translate_name_s_agg": CREATE_TRLNAME_SOUND_AGG_SQLSTR,
        "translate_name_s_raw": CREATE_TRLNAME_SOUND_RAW_SQLSTR,
        "translate_name_s_vld": CREATE_TRLNAME_SOUND_VLD_SQLSTR,
        "translate_rope_s_agg": CREATE_TRLROPE_SOUND_AGG_SQLSTR,
        "translate_rope_s_raw": CREATE_TRLROPE_SOUND_RAW_SQLSTR,
        "translate_rope_s_vld": CREATE_TRLROPE_SOUND_VLD_SQLSTR,
        "translate_title_s_agg": CREATE_TRLTITL_SOUND_AGG_SQLSTR,
        "translate_title_s_raw": CREATE_TRLTITL_SOUND_RAW_SQLSTR,
        "translate_title_s_vld": CREATE_TRLTITL_SOUND_VLD_SQLSTR,
    }


def get_moment_person_sound_agg_tablenames():
    return {
        "person_contact_membership_del_s_agg",
        "person_contact_membership_put_s_agg",
        "person_contactunit_del_s_agg",
        "person_contactunit_put_s_agg",
        "person_plan_awardunit_del_s_agg",
        "person_plan_awardunit_put_s_agg",
        "person_plan_factunit_del_s_agg",
        "person_plan_factunit_put_s_agg",
        "person_plan_healerunit_del_s_agg",
        "person_plan_healerunit_put_s_agg",
        "person_plan_laborunit_del_s_agg",
        "person_plan_laborunit_put_s_agg",
        "person_plan_reason_caseunit_del_s_agg",
        "person_plan_reason_caseunit_put_s_agg",
        "person_plan_reasonunit_del_s_agg",
        "person_plan_reasonunit_put_s_agg",
        "person_planunit_del_s_agg",
        "person_planunit_put_s_agg",
        "personunit_del_s_agg",
        "personunit_put_s_agg",
        "moment_paybook_s_agg",
        "moment_budunit_s_agg",
        "moment_epoch_hour_s_agg",
        "moment_epoch_month_s_agg",
        "moment_epoch_weekday_s_agg",
        "moment_timeoffi_s_agg",
        "momentunit_s_agg",
        "nabu_timenum_s_agg",
    }


def get_person_heard_vld_tablenames() -> set[str]:
    return {
        "personunit_put_h_vld",
        "person_plan_healerunit_put_h_vld",
        "person_contactunit_put_h_vld",
        "person_plan_reason_caseunit_put_h_vld",
        "person_plan_laborunit_put_h_vld",
        "person_plan_reasonunit_put_h_vld",
        "person_plan_factunit_put_h_vld",
        "person_contact_membership_put_h_vld",
        "person_planunit_put_h_vld",
        "person_plan_awardunit_put_h_vld",
    }


def create_sound_and_heard_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_prime_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_prime_db_table(
    cursor: sqlite3_Connection,
    idea_dimen_or_abbv7: str,
    stage_type: str,
    put_del: str = None,
) -> str:
    """Creates table in database and returns tablename"""
    tablename = create_prime_tablename(idea_dimen_or_abbv7, stage_type, put_del)
    prime_create_table_sqlstrs = get_prime_create_table_sqlstrs()
    x_create_table_sqlstr = prime_create_table_sqlstrs.get(tablename)
    cursor.execute(x_create_table_sqlstr)
    return tablename


def create_all_idea_tables(conn_or_cursor: sqlite3_Connection):
    idea_refs = get_quick_ideas_column_ref()
    for idea_number, idea_columns in idea_refs.items():
        x_tablename = f"{idea_number}_raw"
        create_idea_sorted_table(conn_or_cursor, x_tablename, idea_columns)


def create_sound_raw_update_inconsist_error_message_sqlstr(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    if dimen.lower().startswith("moment") or dimen.lower().startswith("nabu"):
        exclude_cols = {"idea_number", "spark_num", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("person"):
        x_tablename = create_prime_tablename(dimen, "s_raw", "put")
    else:
        x_tablename = create_prime_tablename(dimen, "s_raw")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())
    return create_update_inconsistency_error_query(
        conn_or_cursor=conn_or_cursor,
        x_tablename=x_tablename,
        focus_columns=dimen_focus_columns,
        exclude_columns=exclude_cols,
        error_holder_column="error_message",
        error_str="Inconsistent data",
    )


def create_sound_agg_insert_sqlstrs(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())

    if dimen.lower().startswith("moment"):
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("person"):
        agg_tablename = create_prime_tablename(dimen, "s_agg", "put")
        raw_tablename = create_prime_tablename(dimen, "s_raw", "put")
    else:
        raw_tablename = create_prime_tablename(dimen, "s_raw")
        agg_tablename = create_prime_tablename(dimen, "s_agg")

    translate_moment_person_put_sqlstr = create_table2table_agg_insert_query(
        conn_or_cursor,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    sqlstrs = [translate_moment_person_put_sqlstr]
    if dimen.lower().startswith("person"):
        del_raw_tablename = create_prime_tablename(dimen, "s_raw", "del")
        del_agg_tablename = create_prime_tablename(dimen, "s_agg", "del")
        dimen_focus_columns = get_default_sorted_list(set(dimen_focus_columns))
        last_element = dimen_focus_columns.pop(-1)
        dimen_focus_columns.append(f"{last_element}_ERASE")
        person_del_sqlstr = create_table2table_agg_insert_query(
            conn_or_cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="",
        )
        sqlstrs.append(person_del_sqlstr)

    return sqlstrs


def create_insert_into_translate_core_raw_sqlstr(dimen: str) -> str:
    translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s_raw")
    translate_s_agg_tablename = create_prime_tablename(dimen, "s_agg")
    return f"""INSERT INTO {translate_core_s_raw_tablename} (source_dimen, face_name, otx_knot, inx_knot, unknown_str)
SELECT '{translate_s_agg_tablename}', face_name, otx_knot, inx_knot, unknown_str
FROM {translate_s_agg_tablename}
GROUP BY face_name, otx_knot, inx_knot, unknown_str
;
"""


def create_insert_translate_core_agg_into_vld_sqlstr(
    default_knot: KnotTerm, default_unknown: str
):
    return f"""INSERT INTO translate_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  face_name
, IFNULL(otx_knot, '{default_knot}')
, IFNULL(inx_knot, '{default_knot}')
, IFNULL(unknown_str, '{default_unknown}')
FROM translate_core_s_agg
;
"""


def create_insert_missing_face_name_into_translate_core_vld_sqlstr(
    default_knot: KnotTerm, default_unknown: str, moment_person_sound_agg_tablename: str
):
    return f"""INSERT INTO translate_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  {moment_person_sound_agg_tablename}.face_name
, '{default_knot}'
, '{default_knot}'
, '{default_unknown}'
FROM {moment_person_sound_agg_tablename} 
LEFT JOIN translate_core_s_vld ON translate_core_s_vld.face_name = {moment_person_sound_agg_tablename}.face_name
WHERE translate_core_s_vld.face_name IS NULL
GROUP BY {moment_person_sound_agg_tablename}.face_name
;
"""


def create_update_translate_sound_agg_inconsist_sqlstr(dimen: str) -> str:
    translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    translate_s_agg_tablename = create_prime_tablename(dimen, "s_agg")
    return f"""UPDATE {translate_s_agg_tablename}
SET error_message = 'Inconsistent translate core data'
WHERE face_name IN (
    SELECT {translate_s_agg_tablename}.face_name
    FROM {translate_s_agg_tablename} 
    LEFT JOIN {translate_core_s_vld_tablename} ON {translate_core_s_vld_tablename}.face_name = {translate_s_agg_tablename}.face_name
    WHERE {translate_core_s_vld_tablename}.face_name IS NULL
)
;
"""


def create_update_trllabe_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    trllabe_s_agg_tablename = create_prime_tablename("trllabe", "s_agg")
    return f"""UPDATE {trllabe_s_agg_tablename}
SET error_message = 'Knot cannot exist in LabelTerm'
WHERE rowid IN (
    SELECT label_agg.rowid
    FROM {trllabe_s_agg_tablename} label_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = label_agg.face_name
    WHERE label_agg.otx_label LIKE '%' || core_vld.otx_knot || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_trlrope_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    trlrope_s_agg_tablename = create_prime_tablename("trlrope", "s_agg")
    return f"""UPDATE {trlrope_s_agg_tablename}
SET error_message = 'Knot must exist in RopeTerm'
WHERE rowid IN (
    SELECT rope_agg.rowid
    FROM {trlrope_s_agg_tablename} rope_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = rope_agg.face_name
    WHERE NOT rope_agg.otx_rope LIKE core_vld.otx_knot || '%'
        OR NOT rope_agg.inx_rope LIKE core_vld.inx_knot || '%'
)
;
"""


def create_update_trlname_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    trlname_s_agg_tablename = create_prime_tablename("trlname", "s_agg")
    return f"""UPDATE {trlname_s_agg_tablename}
SET error_message = 'Knot cannot exist in NameTerm'
WHERE rowid IN (
    SELECT name_agg.rowid
    FROM {trlname_s_agg_tablename} name_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = name_agg.face_name
    WHERE name_agg.otx_name LIKE '%' || core_vld.otx_knot || '%'
      OR name_agg.inx_name LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_trltitl_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    trltitl_s_agg_tablename = create_prime_tablename("trltitl", "s_agg")
    return f"""UPDATE {trltitl_s_agg_tablename}
SET error_message = 'Otx and inx titles must match knot.'
WHERE rowid IN (
  SELECT title_agg.rowid
  FROM {trltitl_s_agg_tablename} title_agg
  JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = title_agg.face_name
  WHERE NOT ((
            title_agg.otx_title LIKE core_vld.otx_knot || '%' 
        AND title_agg.inx_title LIKE core_vld.inx_knot || '%') 
      OR (
            NOT title_agg.otx_title LIKE core_vld.otx_knot || '%'
        AND NOT title_agg.inx_title LIKE core_vld.inx_knot || '%'
        ))
)
;
"""


def create_insert_translate_sound_vld_table_sqlstr(dimen: str) -> str:
    translate_s_agg_tablename = create_prime_tablename(dimen, "s_agg")
    translate_s_vld_tablename = create_prime_tablename(dimen, "s_vld")
    dimen_otx_inx_obj_names = {
        "translate_name": "name",
        "translate_title": "title",
        "translate_label": "label",
        "translate_rope": "rope",
    }
    otx_str = f"otx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    inx_str = f"inx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    return f"""
INSERT INTO {translate_s_vld_tablename} (spark_num, face_name, {otx_str}, {inx_str})
SELECT spark_num, face_name, MAX({otx_str}), MAX({inx_str})
FROM {translate_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY spark_num, face_name
;
"""


def create_knot_exists_in_name_error_update_sqlstr(table: str, column: str) -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in NameTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


def create_knot_exists_in_label_error_update_sqlstr(table: str, column: str) -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s_vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in LabelTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


INSERT_PRNMEMB_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_contact_membership_put_s_vld (spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot) SELECT spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot FROM person_contact_membership_put_s_agg WHERE error_message IS NULL"
INSERT_PRNMEMB_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_contact_membership_del_s_vld (spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE) SELECT spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE FROM person_contact_membership_del_s_agg WHERE error_message IS NULL"
INSERT_PRNCONT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_contactunit_put_s_vld (spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot) SELECT spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot FROM person_contactunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNCONT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_contactunit_del_s_vld (spark_num, face_name, moment_rope, person_name, contact_name_ERASE) SELECT spark_num, face_name, moment_rope, person_name, contact_name_ERASE FROM person_contactunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNAWAR_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_plan_awardunit_put_s_vld (spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot) SELECT spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot FROM person_plan_awardunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNAWAR_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_plan_awardunit_del_s_vld (spark_num, face_name, person_name, plan_rope, awardee_title_ERASE) SELECT spark_num, face_name, person_name, plan_rope, awardee_title_ERASE FROM person_plan_awardunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNFACT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_plan_factunit_put_s_vld (spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper, knot) SELECT spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper, knot FROM person_plan_factunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNFACT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_plan_factunit_del_s_vld (spark_num, face_name, person_name, plan_rope, fact_context_ERASE) SELECT spark_num, face_name, person_name, plan_rope, fact_context_ERASE FROM person_plan_factunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNHEAL_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_plan_healerunit_put_s_vld (spark_num, face_name, person_name, plan_rope, healer_name, knot) SELECT spark_num, face_name, person_name, plan_rope, healer_name, knot FROM person_plan_healerunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNHEAL_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_plan_healerunit_del_s_vld (spark_num, face_name, person_name, plan_rope, healer_name_ERASE) SELECT spark_num, face_name, person_name, plan_rope, healer_name_ERASE FROM person_plan_healerunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNLABO_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_plan_laborunit_put_s_vld (spark_num, face_name, person_name, plan_rope, labor_title, solo, knot) SELECT spark_num, face_name, person_name, plan_rope, labor_title, solo, knot FROM person_plan_laborunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNLABO_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_plan_laborunit_del_s_vld (spark_num, face_name, person_name, plan_rope, labor_title_ERASE) SELECT spark_num, face_name, person_name, plan_rope, labor_title_ERASE FROM person_plan_laborunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNCASE_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_plan_reason_caseunit_put_s_vld (spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor, knot) SELECT spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor, knot FROM person_plan_reason_caseunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNCASE_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_plan_reason_caseunit_del_s_vld (spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE) SELECT spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE FROM person_plan_reason_caseunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNREAS_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_plan_reasonunit_put_s_vld (spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot) SELECT spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot FROM person_plan_reasonunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNREAS_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_plan_reasonunit_del_s_vld (spark_num, face_name, person_name, plan_rope, reason_context_ERASE) SELECT spark_num, face_name, person_name, plan_rope, reason_context_ERASE FROM person_plan_reasonunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNPLAN_SOUND_VLD_PUT_SQLSTR = "INSERT INTO person_planunit_put_s_vld (spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot) SELECT spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot FROM person_planunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNPLAN_SOUND_VLD_DEL_SQLSTR = "INSERT INTO person_planunit_del_s_vld (spark_num, face_name, person_name, plan_rope_ERASE) SELECT spark_num, face_name, person_name, plan_rope_ERASE FROM person_planunit_del_s_agg WHERE error_message IS NULL"
INSERT_PRNUNIT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO personunit_put_s_vld (spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot) SELECT spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot FROM personunit_put_s_agg WHERE error_message IS NULL"
INSERT_PRNUNIT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO personunit_del_s_vld (spark_num, face_name, moment_rope, person_name_ERASE) SELECT spark_num, face_name, moment_rope, person_name_ERASE FROM personunit_del_s_agg WHERE error_message IS NULL"

INSERT_MMTBUDD_SOUND_VLD_SQLSTR = "INSERT INTO moment_budunit_s_vld (spark_num, face_name, moment_rope, person_name, bud_time, knot, quota, celldepth) SELECT spark_num, face_name, moment_rope, person_name, bud_time, knot, quota, celldepth FROM moment_budunit_s_agg WHERE error_message IS NULL"
INSERT_MMTHOUR_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_hour_s_vld (spark_num, face_name, moment_rope, cumulative_minute, hour_label, knot) SELECT spark_num, face_name, moment_rope, cumulative_minute, hour_label, knot FROM moment_epoch_hour_s_agg WHERE error_message IS NULL"
INSERT_MMTMONT_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_month_s_vld (spark_num, face_name, moment_rope, cumulative_day, month_label, knot) SELECT spark_num, face_name, moment_rope, cumulative_day, month_label, knot FROM moment_epoch_month_s_agg WHERE error_message IS NULL"
INSERT_MMTWEEK_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_weekday_s_vld (spark_num, face_name, moment_rope, weekday_order, weekday_label, knot) SELECT spark_num, face_name, moment_rope, weekday_order, weekday_label, knot FROM moment_epoch_weekday_s_agg WHERE error_message IS NULL"
INSERT_MMTPAYY_SOUND_VLD_SQLSTR = "INSERT INTO moment_paybook_s_vld (spark_num, face_name, moment_rope, person_name, contact_name, tran_time, amount, knot) SELECT spark_num, face_name, moment_rope, person_name, contact_name, tran_time, amount, knot FROM moment_paybook_s_agg WHERE error_message IS NULL"
INSERT_MMTOFFI_SOUND_VLD_SQLSTR = "INSERT INTO moment_timeoffi_s_vld (spark_num, face_name, moment_rope, offi_time, knot) SELECT spark_num, face_name, moment_rope, offi_time, knot FROM moment_timeoffi_s_agg WHERE error_message IS NULL"
INSERT_MMTUNIT_SOUND_VLD_SQLSTR = "INSERT INTO momentunit_s_vld (spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations) SELECT spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations FROM momentunit_s_agg WHERE error_message IS NULL"

INSERT_NABTIME_SOUND_VLD_SQLSTR = "INSERT INTO nabu_timenum_s_vld (spark_num, face_name, moment_rope, otx_time, inx_time) SELECT spark_num, face_name, moment_rope, otx_time, inx_time FROM nabu_timenum_s_agg WHERE error_message IS NULL"


def get_insert_into_sound_vld_sqlstrs() -> dict[str, str]:
    return {
        "person_contact_membership_put_s_vld": INSERT_PRNMEMB_SOUND_VLD_PUT_SQLSTR,
        "person_contact_membership_del_s_vld": INSERT_PRNMEMB_SOUND_VLD_DEL_SQLSTR,
        "person_contactunit_put_s_vld": INSERT_PRNCONT_SOUND_VLD_PUT_SQLSTR,
        "person_contactunit_del_s_vld": INSERT_PRNCONT_SOUND_VLD_DEL_SQLSTR,
        "person_plan_awardunit_put_s_vld": INSERT_PRNAWAR_SOUND_VLD_PUT_SQLSTR,
        "person_plan_awardunit_del_s_vld": INSERT_PRNAWAR_SOUND_VLD_DEL_SQLSTR,
        "person_plan_factunit_put_s_vld": INSERT_PRNFACT_SOUND_VLD_PUT_SQLSTR,
        "person_plan_factunit_del_s_vld": INSERT_PRNFACT_SOUND_VLD_DEL_SQLSTR,
        "person_plan_healerunit_put_s_vld": INSERT_PRNHEAL_SOUND_VLD_PUT_SQLSTR,
        "person_plan_healerunit_del_s_vld": INSERT_PRNHEAL_SOUND_VLD_DEL_SQLSTR,
        "person_plan_reason_caseunit_put_s_vld": INSERT_PRNCASE_SOUND_VLD_PUT_SQLSTR,
        "person_plan_reason_caseunit_del_s_vld": INSERT_PRNCASE_SOUND_VLD_DEL_SQLSTR,
        "person_plan_reasonunit_put_s_vld": INSERT_PRNREAS_SOUND_VLD_PUT_SQLSTR,
        "person_plan_reasonunit_del_s_vld": INSERT_PRNREAS_SOUND_VLD_DEL_SQLSTR,
        "person_plan_laborunit_put_s_vld": INSERT_PRNLABO_SOUND_VLD_PUT_SQLSTR,
        "person_plan_laborunit_del_s_vld": INSERT_PRNLABO_SOUND_VLD_DEL_SQLSTR,
        "person_planunit_put_s_vld": INSERT_PRNPLAN_SOUND_VLD_PUT_SQLSTR,
        "person_planunit_del_s_vld": INSERT_PRNPLAN_SOUND_VLD_DEL_SQLSTR,
        "personunit_put_s_vld": INSERT_PRNUNIT_SOUND_VLD_PUT_SQLSTR,
        "personunit_del_s_vld": INSERT_PRNUNIT_SOUND_VLD_DEL_SQLSTR,
        "moment_paybook_s_vld": INSERT_MMTPAYY_SOUND_VLD_SQLSTR,
        "moment_budunit_s_vld": INSERT_MMTBUDD_SOUND_VLD_SQLSTR,
        "moment_epoch_hour_s_vld": INSERT_MMTHOUR_SOUND_VLD_SQLSTR,
        "moment_epoch_month_s_vld": INSERT_MMTMONT_SOUND_VLD_SQLSTR,
        "moment_epoch_weekday_s_vld": INSERT_MMTWEEK_SOUND_VLD_SQLSTR,
        "moment_timeoffi_s_vld": INSERT_MMTOFFI_SOUND_VLD_SQLSTR,
        "momentunit_s_vld": INSERT_MMTUNIT_SOUND_VLD_SQLSTR,
        "nabu_timenum_s_vld": INSERT_NABTIME_SOUND_VLD_SQLSTR,
    }


INSERT_MMTBUDD_HEARD_RAW_SQLSTR = "INSERT INTO moment_budunit_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, bud_time, knot, quota, celldepth) SELECT spark_num, face_name, moment_rope, person_name, bud_time, knot, quota, celldepth FROM moment_budunit_s_vld "
INSERT_MMTHOUR_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_hour_h_raw (spark_num, face_name_otx, moment_rope_otx, cumulative_minute, hour_label_otx, knot) SELECT spark_num, face_name, moment_rope, cumulative_minute, hour_label, knot FROM moment_epoch_hour_s_vld "
INSERT_MMTMONT_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_month_h_raw (spark_num, face_name_otx, moment_rope_otx, cumulative_day, month_label_otx, knot) SELECT spark_num, face_name, moment_rope, cumulative_day, month_label, knot FROM moment_epoch_month_s_vld "
INSERT_MMTWEEK_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_weekday_h_raw (spark_num, face_name_otx, moment_rope_otx, weekday_order, weekday_label_otx, knot) SELECT spark_num, face_name, moment_rope, weekday_order, weekday_label, knot FROM moment_epoch_weekday_s_vld "
INSERT_MMTPAYY_HEARD_RAW_SQLSTR = "INSERT INTO moment_paybook_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, contact_name_otx, tran_time, amount, knot) SELECT spark_num, face_name, moment_rope, person_name, contact_name, tran_time, amount, knot FROM moment_paybook_s_vld "
INSERT_MMTOFFI_HEARD_RAW_SQLSTR = "INSERT INTO moment_timeoffi_h_raw (spark_num, face_name_otx, moment_rope_otx, offi_time, knot) SELECT spark_num, face_name, moment_rope, offi_time, knot FROM moment_timeoffi_s_vld "
INSERT_MMTUNIT_HEARD_RAW_SQLSTR = "INSERT INTO momentunit_h_raw (spark_num, face_name_otx, moment_rope_otx, epoch_label_otx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations) SELECT spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations FROM momentunit_s_vld "
INSERT_NABTIME_HEARD_RAW_SQLSTR = "INSERT INTO nabu_timenum_h_raw (spark_num, face_name_otx, moment_rope_otx, otx_time, inx_time) SELECT spark_num, face_name, moment_rope, otx_time, inx_time FROM nabu_timenum_s_vld "

INSERT_PRNMEMB_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_contact_membership_put_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, contact_name_otx, group_title_otx, group_cred_lumen, group_debt_lumen, knot) SELECT spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot FROM person_contact_membership_put_s_vld "
INSERT_PRNMEMB_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_contact_membership_del_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, contact_name_otx, group_title_ERASE_otx) SELECT spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE FROM person_contact_membership_del_s_vld "
INSERT_PRNCONT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_contactunit_put_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, contact_name_otx, contact_cred_lumen, contact_debt_lumen, knot) SELECT spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot FROM person_contactunit_put_s_vld "
INSERT_PRNCONT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_contactunit_del_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, contact_name_ERASE_otx) SELECT spark_num, face_name, moment_rope, person_name, contact_name_ERASE FROM person_contactunit_del_s_vld "
INSERT_PRNAWAR_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_plan_awardunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, awardee_title_otx, give_force, take_force, knot) SELECT spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot FROM person_plan_awardunit_put_s_vld "
INSERT_PRNAWAR_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_plan_awardunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, awardee_title_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope, awardee_title_ERASE FROM person_plan_awardunit_del_s_vld "
INSERT_PRNFACT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_plan_factunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, fact_context_otx, fact_state_otx, fact_lower, fact_upper, knot) SELECT spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper, knot FROM person_plan_factunit_put_s_vld "
INSERT_PRNFACT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_plan_factunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, fact_context_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope, fact_context_ERASE FROM person_plan_factunit_del_s_vld "
INSERT_PRNHEAL_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_plan_healerunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, healer_name_otx, knot) SELECT spark_num, face_name, person_name, plan_rope, healer_name, knot FROM person_plan_healerunit_put_s_vld "
INSERT_PRNHEAL_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_plan_healerunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, healer_name_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope, healer_name_ERASE FROM person_plan_healerunit_del_s_vld "
INSERT_PRNLABO_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_plan_laborunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, labor_title_otx, solo, knot) SELECT spark_num, face_name, person_name, plan_rope, labor_title, solo, knot FROM person_plan_laborunit_put_s_vld "
INSERT_PRNLABO_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_plan_laborunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, labor_title_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope, labor_title_ERASE FROM person_plan_laborunit_del_s_vld "
INSERT_PRNCASE_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_plan_reason_caseunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, reason_context_otx, reason_state_otx, reason_lower, reason_upper, reason_divisor, knot) SELECT spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor, knot FROM person_plan_reason_caseunit_put_s_vld "
INSERT_PRNCASE_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_plan_reason_caseunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, reason_context_otx, reason_state_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE FROM person_plan_reason_caseunit_del_s_vld "
INSERT_PRNREAS_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_plan_reasonunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, reason_context_otx, active_requisite, knot) SELECT spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot FROM person_plan_reasonunit_put_s_vld "
INSERT_PRNREAS_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_plan_reasonunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, reason_context_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope, reason_context_ERASE FROM person_plan_reasonunit_del_s_vld "
INSERT_PRNPLAN_HEARD_RAW_PUT_SQLSTR = "INSERT INTO person_planunit_put_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot) SELECT spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot FROM person_planunit_put_s_vld "
INSERT_PRNPLAN_HEARD_RAW_DEL_SQLSTR = "INSERT INTO person_planunit_del_h_raw (spark_num, face_name_otx, person_name_otx, plan_rope_ERASE_otx) SELECT spark_num, face_name, person_name, plan_rope_ERASE FROM person_planunit_del_s_vld "
INSERT_PRNUNIT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO personunit_put_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot) SELECT spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot FROM personunit_put_s_vld "
INSERT_PRNUNIT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO personunit_del_h_raw (spark_num, face_name_otx, moment_rope_otx, person_name_ERASE_otx) SELECT spark_num, face_name, moment_rope, person_name_ERASE FROM personunit_del_s_vld "

INSERT_NABTIME_HEARD_RAW_SQLSTR = "INSERT INTO nabu_timenum_h_raw (spark_num, face_name_otx, moment_rope_otx, otx_time, inx_time) SELECT spark_num, face_name, moment_rope, otx_time, inx_time FROM nabu_timenum_s_vld "


def get_insert_into_heard_raw_sqlstrs() -> dict[str, str]:
    return {
        "nabu_timenum_h_raw": INSERT_NABTIME_HEARD_RAW_SQLSTR,
        "moment_paybook_h_raw": INSERT_MMTPAYY_HEARD_RAW_SQLSTR,
        "moment_budunit_h_raw": INSERT_MMTBUDD_HEARD_RAW_SQLSTR,
        "moment_epoch_hour_h_raw": INSERT_MMTHOUR_HEARD_RAW_SQLSTR,
        "moment_epoch_month_h_raw": INSERT_MMTMONT_HEARD_RAW_SQLSTR,
        "moment_epoch_weekday_h_raw": INSERT_MMTWEEK_HEARD_RAW_SQLSTR,
        "moment_timeoffi_h_raw": INSERT_MMTOFFI_HEARD_RAW_SQLSTR,
        "momentunit_h_raw": INSERT_MMTUNIT_HEARD_RAW_SQLSTR,
        "person_contact_membership_put_h_raw": INSERT_PRNMEMB_HEARD_RAW_PUT_SQLSTR,
        "person_contact_membership_del_h_raw": INSERT_PRNMEMB_HEARD_RAW_DEL_SQLSTR,
        "person_contactunit_put_h_raw": INSERT_PRNCONT_HEARD_RAW_PUT_SQLSTR,
        "person_contactunit_del_h_raw": INSERT_PRNCONT_HEARD_RAW_DEL_SQLSTR,
        "person_plan_awardunit_put_h_raw": INSERT_PRNAWAR_HEARD_RAW_PUT_SQLSTR,
        "person_plan_awardunit_del_h_raw": INSERT_PRNAWAR_HEARD_RAW_DEL_SQLSTR,
        "person_plan_factunit_put_h_raw": INSERT_PRNFACT_HEARD_RAW_PUT_SQLSTR,
        "person_plan_factunit_del_h_raw": INSERT_PRNFACT_HEARD_RAW_DEL_SQLSTR,
        "person_plan_healerunit_put_h_raw": INSERT_PRNHEAL_HEARD_RAW_PUT_SQLSTR,
        "person_plan_healerunit_del_h_raw": INSERT_PRNHEAL_HEARD_RAW_DEL_SQLSTR,
        "person_plan_reason_caseunit_put_h_raw": INSERT_PRNCASE_HEARD_RAW_PUT_SQLSTR,
        "person_plan_reason_caseunit_del_h_raw": INSERT_PRNCASE_HEARD_RAW_DEL_SQLSTR,
        "person_plan_reasonunit_put_h_raw": INSERT_PRNREAS_HEARD_RAW_PUT_SQLSTR,
        "person_plan_reasonunit_del_h_raw": INSERT_PRNREAS_HEARD_RAW_DEL_SQLSTR,
        "person_plan_laborunit_put_h_raw": INSERT_PRNLABO_HEARD_RAW_PUT_SQLSTR,
        "person_plan_laborunit_del_h_raw": INSERT_PRNLABO_HEARD_RAW_DEL_SQLSTR,
        "person_planunit_put_h_raw": INSERT_PRNPLAN_HEARD_RAW_PUT_SQLSTR,
        "person_planunit_del_h_raw": INSERT_PRNPLAN_HEARD_RAW_DEL_SQLSTR,
        "personunit_put_h_raw": INSERT_PRNUNIT_HEARD_RAW_PUT_SQLSTR,
        "personunit_del_h_raw": INSERT_PRNUNIT_HEARD_RAW_DEL_SQLSTR,
    }


def create_update_heard_raw_existing_inx_col_sqlstr(
    translate_type_abbv: str, table: str, column_prefix: str
) -> str:
    return f"""
WITH trl_face_otx_spark AS (
    SELECT 
      raw_dim.rowid raw_rowid
    , raw_dim.spark_num
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
    , MAX(trl.spark_num) translate_spark_num
    FROM {table} raw_dim
    LEFT JOIN translate_{translate_type_abbv}_s_vld trl ON trl.face_name = raw_dim.face_name_otx
        AND trl.otx_{translate_type_abbv} = raw_dim.{column_prefix}_otx
        AND raw_dim.spark_num >= trl.spark_num
    GROUP BY 
      raw_dim.rowid
    , raw_dim.spark_num
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
),
trl_inx_strs AS (
    SELECT trl_foe.raw_rowid, trl_vld.inx_{translate_type_abbv}
    FROM trl_face_otx_spark trl_foe
    LEFT JOIN translate_{translate_type_abbv}_s_vld trl_vld
        ON trl_vld.face_name = trl_foe.face_name_otx
        AND trl_vld.otx_{translate_type_abbv} = trl_foe.{column_prefix}_otx
        AND trl_vld.spark_num = trl_foe.translate_spark_num
)
UPDATE {table} as dim_h_raw
SET {column_prefix}_inx = (
    SELECT trl_inx_strs.inx_{translate_type_abbv}
    FROM trl_inx_strs
    WHERE dim_h_raw.rowid = trl_inx_strs.raw_rowid
)
;
"""


def create_update_heard_raw_empty_inx_col_sqlstr(table: str, column_prefix: str) -> str:
    """UPDATE statement that will always set the "inx" column to the "otx" value if "inx" is NULL"""
    return f"""
UPDATE {table} as dim_h_raw
SET {column_prefix}_inx = {column_prefix}_otx
WHERE {column_prefix}_inx IS NULL
;
"""


PRNMEMB_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_contact_membership_del_h_agg (spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, group_title_ERASE_inx
FROM person_contact_membership_del_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, group_title_ERASE_inx
"""
PRNCONT_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_contactunit_del_h_agg (spark_num, face_name, moment_rope, person_name, contact_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_ERASE_inx
FROM person_contactunit_del_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_ERASE_inx
"""
PRNAWAR_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_plan_awardunit_del_h_agg (spark_num, face_name, person_name, plan_rope, awardee_title_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, awardee_title_ERASE_inx
FROM person_plan_awardunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, awardee_title_ERASE_inx
"""
PRNFACT_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_plan_factunit_del_h_agg (spark_num, face_name, person_name, plan_rope, fact_context_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, fact_context_ERASE_inx
FROM person_plan_factunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, fact_context_ERASE_inx
"""
PRNHEAL_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_plan_healerunit_del_h_agg (spark_num, face_name, person_name, plan_rope, healer_name_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, healer_name_ERASE_inx
FROM person_plan_healerunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, healer_name_ERASE_inx
"""
PRNLABO_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_plan_laborunit_del_h_agg (spark_num, face_name, person_name, plan_rope, labor_title_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, labor_title_ERASE_inx
FROM person_plan_laborunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, labor_title_ERASE_inx
"""
PRNCASE_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_plan_reason_caseunit_del_h_agg (spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_inx, reason_state_ERASE_inx
FROM person_plan_reason_caseunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_inx, reason_state_ERASE_inx
"""
PRNREAS_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_plan_reasonunit_del_h_agg (spark_num, face_name, person_name, plan_rope, reason_context_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_ERASE_inx
FROM person_plan_reasonunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_ERASE_inx
"""
PRNPLAN_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO person_planunit_del_h_agg (spark_num, face_name, person_name, plan_rope_ERASE)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_ERASE_inx
FROM person_planunit_del_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_ERASE_inx
"""
PRNUNIT_HEARD_AGG_DEL_INSERT_SQLSTR = """
INSERT INTO personunit_del_h_agg (spark_num, face_name, moment_rope, person_name_ERASE)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_ERASE_inx
FROM personunit_del_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_ERASE_inx
"""
PRNMEMB_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_contact_membership_put_h_agg (spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen, knot
FROM person_contact_membership_put_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen, knot
"""
PRNCONT_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_contactunit_put_h_agg (spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, contact_cred_lumen, contact_debt_lumen, knot
FROM person_contactunit_put_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, contact_cred_lumen, contact_debt_lumen, knot
"""
PRNAWAR_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_plan_awardunit_put_h_agg (spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, awardee_title_inx, give_force, take_force, knot
FROM person_plan_awardunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, awardee_title_inx, give_force, take_force, knot
"""
PRNFACT_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_plan_factunit_put_h_agg (spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower_otx, fact_upper_otx, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper, knot
FROM person_plan_factunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper, knot
"""
PRNHEAL_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_plan_healerunit_put_h_agg (spark_num, face_name, person_name, plan_rope, healer_name, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, healer_name_inx, knot
FROM person_plan_healerunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, healer_name_inx, knot
"""
PRNLABO_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_plan_laborunit_put_h_agg (spark_num, face_name, person_name, plan_rope, labor_title, solo, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, labor_title_inx, solo, knot
FROM person_plan_laborunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, labor_title_inx, solo, knot
"""
PRNCASE_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_plan_reason_caseunit_put_h_agg (spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower_otx, reason_upper_otx, reason_divisor, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_inx, reason_state_inx, reason_lower, reason_upper, reason_divisor, knot
FROM person_plan_reason_caseunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_inx, reason_state_inx, reason_lower, reason_upper, reason_divisor, knot
"""
PRNREAS_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_plan_reasonunit_put_h_agg (spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_inx, active_requisite, knot
FROM person_plan_reasonunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, reason_context_inx, active_requisite, knot
"""
PRNPLAN_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO person_planunit_put_h_agg (spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot)
SELECT spark_num, face_name_inx, person_name_inx, plan_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot
FROM person_planunit_put_h_raw
GROUP BY spark_num, face_name_inx, person_name_inx, plan_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot
"""
PRNUNIT_HEARD_AGG_PUT_INSERT_SQLSTR = """
INSERT INTO personunit_put_h_agg (spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot
FROM personunit_put_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot
"""
MMTBUDD_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_budunit_h_agg (spark_num, face_name, moment_rope, person_name, bud_time_otx, knot, quota, celldepth)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, bud_time, knot, quota, celldepth
FROM moment_budunit_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, bud_time, knot, quota, celldepth
"""
MMTHOUR_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_hour_h_agg (spark_num, face_name, moment_rope, cumulative_minute, hour_label, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, cumulative_minute, hour_label_inx, knot
FROM moment_epoch_hour_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, cumulative_minute, hour_label_inx, knot
"""
MMTMONT_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_month_h_agg (spark_num, face_name, moment_rope, cumulative_day, month_label, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, cumulative_day, month_label_inx, knot
FROM moment_epoch_month_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, cumulative_day, month_label_inx, knot
"""
MMTWEEK_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_weekday_h_agg (spark_num, face_name, moment_rope, weekday_order, weekday_label, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, weekday_order, weekday_label_inx, knot
FROM moment_epoch_weekday_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, weekday_order, weekday_label_inx, knot
"""
MMTPAYY_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_paybook_h_agg (spark_num, face_name, moment_rope, person_name, contact_name, tran_time_otx, amount, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, tran_time, amount, knot
FROM moment_paybook_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, person_name_inx, contact_name_inx, tran_time, amount, knot
"""
MMTOFFI_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_timeoffi_h_agg (spark_num, face_name, moment_rope, offi_time_otx, knot)
SELECT spark_num, face_name_inx, moment_rope_inx, offi_time, knot
FROM moment_timeoffi_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, offi_time, knot
"""
MMTUNIT_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO momentunit_h_agg (spark_num, face_name, moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations)
SELECT spark_num, face_name_inx, moment_rope_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
FROM momentunit_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
"""
NABTIME_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO nabu_timenum_h_agg (spark_num, face_name, moment_rope, otx_time, inx_time)
SELECT spark_num, face_name_inx, moment_rope_inx, otx_time, inx_time
FROM nabu_timenum_h_raw
GROUP BY spark_num, face_name_inx, moment_rope_inx, otx_time, inx_time
"""


def get_insert_heard_agg_sqlstrs() -> dict[str, str]:
    return {
        "person_plan_awardunit_del_h_agg": PRNAWAR_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_plan_factunit_del_h_agg": PRNFACT_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_plan_healerunit_del_h_agg": PRNHEAL_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_plan_laborunit_del_h_agg": PRNLABO_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_plan_reason_caseunit_del_h_agg": PRNCASE_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_plan_reasonunit_del_h_agg": PRNREAS_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_planunit_del_h_agg": PRNPLAN_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_contact_membership_del_h_agg": PRNMEMB_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_contactunit_del_h_agg": PRNCONT_HEARD_AGG_DEL_INSERT_SQLSTR,
        "personunit_del_h_agg": PRNUNIT_HEARD_AGG_DEL_INSERT_SQLSTR,
        "person_plan_awardunit_put_h_agg": PRNAWAR_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_plan_factunit_put_h_agg": PRNFACT_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_plan_healerunit_put_h_agg": PRNHEAL_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_plan_laborunit_put_h_agg": PRNLABO_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_plan_reason_caseunit_put_h_agg": PRNCASE_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_plan_reasonunit_put_h_agg": PRNREAS_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_planunit_put_h_agg": PRNPLAN_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_contact_membership_put_h_agg": PRNMEMB_HEARD_AGG_PUT_INSERT_SQLSTR,
        "person_contactunit_put_h_agg": PRNCONT_HEARD_AGG_PUT_INSERT_SQLSTR,
        "personunit_put_h_agg": PRNUNIT_HEARD_AGG_PUT_INSERT_SQLSTR,
        "moment_budunit_h_agg": MMTBUDD_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_hour_h_agg": MMTHOUR_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_month_h_agg": MMTMONT_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_weekday_h_agg": MMTWEEK_HEARD_AGG_INSERT_SQLSTR,
        "moment_paybook_h_agg": MMTPAYY_HEARD_AGG_INSERT_SQLSTR,
        "moment_timeoffi_h_agg": MMTOFFI_HEARD_AGG_INSERT_SQLSTR,
        "momentunit_h_agg": MMTUNIT_HEARD_AGG_INSERT_SQLSTR,
        "nabu_timenum_h_agg": NABTIME_HEARD_AGG_INSERT_SQLSTR,
    }


def get_update_heard_agg_timenum_sqlstr(dst_tablename: str, focus_column: str) -> str:
    """Given: destionation table and focus column (Must be "offitime" or "tran_time" or "bud_time")
    Return Update statement that will set the timenum inx column
    reference key: mxhap0"""

    return f"""
WITH mmtunit AS (
    SELECT moment_rope, c400_number
    FROM momentunit_h_agg
    GROUP BY moment_rope, c400_number
),
enriched AS (
    SELECT
        dst2_table.spark_num,
        dst2_table.moment_rope,
        nabtime.otx_time - nabtime.inx_time AS inx_epoch_diff,
        mmtunit.c400_number
    FROM {dst_tablename} as dst2_table
    LEFT JOIN nabu_timenum_h_agg as nabtime
        ON nabtime.spark_num = (
            SELECT MAX(n2.spark_num)
            FROM nabu_timenum_h_agg as n2
            WHERE n2.spark_num <= dst2_table.spark_num
                AND dst2_table.moment_rope LIKE n2.moment_rope || '%'
        )
    LEFT JOIN mmtunit
        ON mmtunit.moment_rope = nabtime.moment_rope
)
UPDATE {dst_tablename} as dst_table
SET {focus_column}_inx = mod(
    dst_table.{focus_column}_otx + IFNULL(enriched.inx_epoch_diff, 0)
    , IFNULL(enriched.c400_number * 210379680, 1472657760)
    )
FROM enriched
WHERE enriched.spark_num = dst_table.spark_num
    AND enriched.moment_rope = dst_table.moment_rope
;
"""


def get_update_heard_agg_moment_timenum_sqlstrs() -> dict[str]:
    mmtoffi_tbl = create_prime_tablename("moment_timeoffi", "h_agg")
    mmtoffi_key = ("moment_timeoffi", "offi_time")
    mmtpayy_tbl = create_prime_tablename("moment_paybook", "h_agg")
    mmtpayy_key = ("moment_paybook", "tran_time")
    mmtbudd_tbl = create_prime_tablename("moment_budunit", "h_agg")
    mmtbudd_key = ("moment_budunit", "bud_time")
    return {
        mmtpayy_key: get_update_heard_agg_timenum_sqlstr(mmtpayy_tbl, "tran_time"),
        mmtoffi_key: get_update_heard_agg_timenum_sqlstr(mmtoffi_tbl, "offi_time"),
        mmtbudd_key: get_update_heard_agg_timenum_sqlstr(mmtbudd_tbl, "bud_time"),
    }


def get_update_prncase_inx_epoch_diff_sqlstr() -> str:
    """Returns update statement that sets put_h_agg.inx_epoch_diff column from nabtime values
    reference key: pchap0
    """

    return """
UPDATE person_plan_reason_caseunit_put_h_agg as prncase
SET inx_epoch_diff = otx_time - inx_time
FROM nabu_timenum_h_agg as nabtime
WHERE 
    nabtime.spark_num = (
        SELECT MAX(n2.spark_num)
        FROM nabu_timenum_h_agg as n2
        WHERE n2.spark_num <= prncase.spark_num
            AND prncase.plan_rope LIKE n2.moment_rope || '%'
        )
    AND prncase.plan_rope LIKE nabtime.moment_rope || '%'
;
"""


def get_update_prnfact_inx_epoch_diff_sqlstr() -> str:
    """Returns update statement that sets put_h_agg.inx_epoch_diff column from nabtime values
    reference key: pfhap0
    """

    return """
UPDATE person_plan_factunit_put_h_agg as prnfact
SET inx_epoch_diff = otx_time - inx_time
FROM nabu_timenum_h_agg as nabtime
WHERE
    nabtime.spark_num = (
        SELECT MAX(n2.spark_num)
        FROM nabu_timenum_h_agg as n2
        WHERE n2.spark_num <= prnfact.spark_num
            AND prnfact.plan_rope LIKE n2.moment_rope || '%'
        )
    AND prnfact.plan_rope LIKE nabtime.moment_rope || '%'
;
"""


def get_update_prncase_context_plan_sqlstr() -> str:
    """Returns update statement that sets prncase_put_h_agg columns from prnplan columns
    context_plan_denom = spark_prnplan.denom
    context_plan_morph = spark_prnplan.morph
    reference key: pchap1
    """
    return """
UPDATE person_plan_reason_caseunit_put_h_agg as prncase
SET 
  context_plan_denom = prnplan.denom
, context_plan_morph = prnplan.morph
FROM person_planunit_put_h_agg prnplan
WHERE prncase.spark_num = prnplan.spark_num
    AND prncase.person_name = prnplan.person_name
    AND prncase.reason_context = prnplan.plan_rope
;
"""


def get_update_prnfact_context_plan_sqlstr() -> str:
    """Returns update statement that sets prnfact_put_h_agg columns from prnplan columns
    context_plan_close = spark_prnplan.close
    context_plan_denom = spark_prnplan.denom
    context_plan_morph = spark_prnplan.morph
    """
    return """
UPDATE person_plan_factunit_put_h_agg as prnfact
SET context_plan_close = prnplan.close
FROM person_planunit_put_h_agg prnplan
WHERE prnfact.spark_num = prnplan.spark_num
    AND prnfact.person_name = prnplan.person_name
    AND prnfact.fact_context = prnplan.plan_rope
;
"""


def get_update_prncase_range_sqlstr() -> str:
    """Given any case append number to caseunit reason_lower and reason_upper

        Step 0: calculate modulus:
            If it exists set to the caseunit's reason_divisor
            Elfe if it exists set to the context plan's denom
        Step 1: morph x_frame
            If context plan's morph is True then divide frame by context_plan_denom
        Step 2: define CaseUnit attrs
            Change CaseUnit's reason_lower and reason_upper range attrs by adding frame
            to each and use modulus to make result is not negative or more then modulus.
    reference key: pchap2
    """

    return """
UPDATE person_plan_reason_caseunit_put_h_agg as prncase
SET
 reason_lower_inx =
  CASE
   WHEN reason_divisor IS NOT NULL THEN
    CASE
     WHEN inx_epoch_diff IS NULL
     THEN reason_lower_otx
     WHEN context_plan_morph = 1
     THEN (reason_lower_otx + inx_epoch_diff) % reason_divisor
     WHEN context_plan_morph IS NULL
     THEN (reason_lower_otx + CAST(inx_epoch_diff / IFNULL(context_plan_denom, 1) AS INTEGER)) % reason_divisor
    END
   WHEN context_plan_denom IS NOT NULL THEN
    CASE
     WHEN inx_epoch_diff IS NULL
     THEN reason_lower_otx
     WHEN context_plan_morph = 1
     THEN (reason_lower_otx + inx_epoch_diff) % context_plan_denom
     WHEN context_plan_morph IS NULL
     THEN (reason_lower_otx + CAST(inx_epoch_diff / IFNULL(context_plan_denom, 1) AS INTEGER)) % context_plan_denom
    END
  END,
 reason_upper_inx =
  CASE
   WHEN reason_divisor IS NOT NULL THEN
    CASE
     WHEN inx_epoch_diff IS NULL
     THEN reason_upper_otx
     WHEN context_plan_morph = 1
     THEN (reason_upper_otx + inx_epoch_diff) % reason_divisor
     WHEN context_plan_morph IS NULL
     THEN (reason_upper_otx + CAST(inx_epoch_diff / IFNULL(context_plan_denom, 1) AS INTEGER)) % reason_divisor
    END
   WHEN context_plan_denom IS NOT NULL THEN
    CASE
     WHEN inx_epoch_diff IS NULL
     THEN reason_upper_otx
     WHEN context_plan_morph = 1
     THEN (reason_upper_otx + inx_epoch_diff) % context_plan_denom
     WHEN context_plan_morph IS NULL
     THEN (reason_upper_otx + CAST(inx_epoch_diff / IFNULL(context_plan_denom, 1) AS INTEGER)) % context_plan_denom
    END
  END
;
"""


def get_update_prnfact_range_sqlstr() -> str:
    """
    reference key: pchap2
    """

    return """
UPDATE person_plan_factunit_put_h_agg
SET
 fact_lower_inx =
  CASE
   WHEN inx_epoch_diff IS NULL
   THEN fact_lower_otx
   WHEN context_plan_close IS NOT NULL
   THEN (fact_lower_otx + inx_epoch_diff) % context_plan_close
  END,
 fact_upper_inx =
  CASE
   WHEN inx_epoch_diff IS NULL
   THEN fact_upper_otx
   WHEN context_plan_close IS NOT NULL
   THEN (fact_upper_otx + inx_epoch_diff) % context_plan_close
  END
;
"""


def update_caseunit_heard_agg_timenum_columns(cursor: sqlite3_Connection):
    cursor.execute(get_update_prncase_inx_epoch_diff_sqlstr())
    cursor.execute(get_update_prncase_context_plan_sqlstr())
    cursor.execute(get_update_prncase_range_sqlstr())


def update_factunit_heard_agg_timenum_columns(cursor: sqlite3_Connection):
    cursor.execute(get_update_prnfact_inx_epoch_diff_sqlstr())
    cursor.execute(get_update_prnfact_context_plan_sqlstr())
    cursor.execute(get_update_prnfact_range_sqlstr())


def update_heard_agg_timenum_columns(cursor: sqlite3_Connection):
    # for bud_time, tran_time, offi_time
    for update_sqlstr in get_update_heard_agg_moment_timenum_sqlstrs().values():
        cursor.execute(update_sqlstr)
    # for reason_lower, reason_upper
    update_caseunit_heard_agg_timenum_columns(cursor)
    # for fact_lower, fact_upper
    update_factunit_heard_agg_timenum_columns(cursor)


MMTBUDD_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_budunit_h_vld (moment_rope, person_name, bud_time, knot, quota, celldepth)
SELECT moment_rope, person_name, bud_time_inx, knot, quota, celldepth
FROM moment_budunit_h_agg
GROUP BY moment_rope, person_name, bud_time_inx, knot, quota, celldepth
"""
MMTHOUR_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_epoch_hour_h_vld (moment_rope, cumulative_minute, hour_label, knot)
SELECT moment_rope, cumulative_minute, hour_label, knot
FROM moment_epoch_hour_h_agg
GROUP BY moment_rope, cumulative_minute, hour_label, knot
"""
MMTMONT_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_epoch_month_h_vld (moment_rope, cumulative_day, month_label, knot)
SELECT moment_rope, cumulative_day, month_label, knot
FROM moment_epoch_month_h_agg
GROUP BY moment_rope, cumulative_day, month_label, knot
"""
MMTWEEK_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_epoch_weekday_h_vld (moment_rope, weekday_order, weekday_label, knot)
SELECT moment_rope, weekday_order, weekday_label, knot
FROM moment_epoch_weekday_h_agg
GROUP BY moment_rope, weekday_order, weekday_label, knot
"""
MMTPAYY_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_paybook_h_vld (moment_rope, person_name, contact_name, tran_time, amount, knot)
SELECT moment_rope, person_name, contact_name, tran_time_inx, amount, knot
FROM moment_paybook_h_agg
GROUP BY moment_rope, person_name, contact_name, tran_time_inx, amount, knot
"""
MMTOFFI_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO moment_timeoffi_h_vld (moment_rope, offi_time, knot)
SELECT moment_rope, offi_time_inx, knot
FROM moment_timeoffi_h_agg
GROUP BY moment_rope, offi_time_inx, knot
"""
MMTUNIT_HEARD_VLD_INSERT_SQLSTR = """
INSERT INTO momentunit_h_vld (moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations)
SELECT moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
FROM momentunit_h_agg
GROUP BY moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations
"""
INSERT_PRNMEMB_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_contact_membership_put_h_vld (spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot)
SELECT spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot
FROM person_contact_membership_put_h_agg
GROUP BY spark_num, face_name, moment_rope, person_name, contact_name, group_title, group_cred_lumen, group_debt_lumen, knot
"""
INSERT_PRNMEMB_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_contact_membership_del_h_vld (spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE)
SELECT spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE
FROM person_contact_membership_del_h_agg
GROUP BY spark_num, face_name, moment_rope, person_name, contact_name, group_title_ERASE
"""
INSERT_PRNCONT_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_contactunit_put_h_vld (spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot)
SELECT spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot
FROM person_contactunit_put_h_agg
GROUP BY spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen, knot
"""
INSERT_PRNCONT_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_contactunit_del_h_vld (spark_num, face_name, moment_rope, person_name, contact_name_ERASE)
SELECT spark_num, face_name, moment_rope, person_name, contact_name_ERASE
FROM person_contactunit_del_h_agg
GROUP BY spark_num, face_name, moment_rope, person_name, contact_name_ERASE
"""
INSERT_PRNAWAR_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_plan_awardunit_put_h_vld (spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot)
SELECT spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot
FROM person_plan_awardunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot
"""
INSERT_PRNAWAR_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_plan_awardunit_del_h_vld (spark_num, face_name, person_name, plan_rope, awardee_title_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, awardee_title_ERASE
FROM person_plan_awardunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, awardee_title_ERASE
"""
INSERT_PRNFACT_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_plan_factunit_put_h_vld (spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper, knot)
SELECT spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower_inx, fact_upper_inx, knot
FROM person_plan_factunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, fact_context, fact_state, fact_lower_inx, fact_upper_inx, knot
"""
INSERT_PRNFACT_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_plan_factunit_del_h_vld (spark_num, face_name, person_name, plan_rope, fact_context_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, fact_context_ERASE
FROM person_plan_factunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, fact_context_ERASE
"""
INSERT_PRNHEAL_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_plan_healerunit_put_h_vld (spark_num, face_name, person_name, plan_rope, healer_name, knot)
SELECT spark_num, face_name, person_name, plan_rope, healer_name, knot
FROM person_plan_healerunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, healer_name, knot
"""
INSERT_PRNHEAL_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_plan_healerunit_del_h_vld (spark_num, face_name, person_name, plan_rope, healer_name_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, healer_name_ERASE
FROM person_plan_healerunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, healer_name_ERASE
"""
INSERT_PRNLABO_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_plan_laborunit_put_h_vld (spark_num, face_name, person_name, plan_rope, labor_title, solo, knot)
SELECT spark_num, face_name, person_name, plan_rope, labor_title, solo, knot
FROM person_plan_laborunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, labor_title, solo, knot
"""
INSERT_PRNLABO_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_plan_laborunit_del_h_vld (spark_num, face_name, person_name, plan_rope, labor_title_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, labor_title_ERASE
FROM person_plan_laborunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, labor_title_ERASE
"""
INSERT_PRNCASE_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_plan_reason_caseunit_put_h_vld (spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower, reason_upper, reason_divisor, knot)
SELECT spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower_inx, reason_upper_inx, reason_divisor, knot
FROM person_plan_reason_caseunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, reason_context, reason_state, reason_lower_inx, reason_upper_inx, reason_divisor, knot
"""
INSERT_PRNCASE_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_plan_reason_caseunit_del_h_vld (spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE
FROM person_plan_reason_caseunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, reason_context, reason_state_ERASE
"""
INSERT_PRNREAS_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_plan_reasonunit_put_h_vld (spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot)
SELECT spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot
FROM person_plan_reasonunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, reason_context, active_requisite, knot
"""
INSERT_PRNREAS_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_plan_reasonunit_del_h_vld (spark_num, face_name, person_name, plan_rope, reason_context_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, reason_context_ERASE
FROM person_plan_reasonunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, reason_context_ERASE
"""
INSERT_PRNPLAN_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO person_planunit_put_h_vld (spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot)
SELECT spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot
FROM person_planunit_put_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool, knot
"""
INSERT_PRNPLAN_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO person_planunit_del_h_vld (spark_num, face_name, person_name, plan_rope_ERASE)
SELECT spark_num, face_name, person_name, plan_rope_ERASE
FROM person_planunit_del_h_agg
GROUP BY spark_num, face_name, person_name, plan_rope_ERASE
"""
INSERT_PRNUNIT_HEARD_VLD_PUT_SQLSTR = """
INSERT INTO personunit_put_h_vld (spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot)
SELECT spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot
FROM personunit_put_h_agg
GROUP BY spark_num, face_name, moment_rope, person_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, fund_grain, mana_grain, respect_grain, knot
"""
INSERT_PRNUNIT_HEARD_VLD_DEL_SQLSTR = """
INSERT INTO personunit_del_h_vld (spark_num, face_name, moment_rope, person_name_ERASE)
SELECT spark_num, face_name, moment_rope, person_name_ERASE
FROM personunit_del_h_agg
GROUP BY spark_num, face_name, moment_rope, person_name_ERASE
"""


def get_insert_heard_vld_sqlstrs() -> dict[str, str]:
    return {
        "moment_paybook_h_vld": MMTPAYY_HEARD_VLD_INSERT_SQLSTR,
        "moment_budunit_h_vld": MMTBUDD_HEARD_VLD_INSERT_SQLSTR,
        "moment_epoch_hour_h_vld": MMTHOUR_HEARD_VLD_INSERT_SQLSTR,
        "moment_epoch_month_h_vld": MMTMONT_HEARD_VLD_INSERT_SQLSTR,
        "moment_epoch_weekday_h_vld": MMTWEEK_HEARD_VLD_INSERT_SQLSTR,
        "moment_timeoffi_h_vld": MMTOFFI_HEARD_VLD_INSERT_SQLSTR,
        "momentunit_h_vld": MMTUNIT_HEARD_VLD_INSERT_SQLSTR,
        "person_contact_membership_put_h_vld": INSERT_PRNMEMB_HEARD_VLD_PUT_SQLSTR,
        "person_contact_membership_del_h_vld": INSERT_PRNMEMB_HEARD_VLD_DEL_SQLSTR,
        "person_contactunit_put_h_vld": INSERT_PRNCONT_HEARD_VLD_PUT_SQLSTR,
        "person_contactunit_del_h_vld": INSERT_PRNCONT_HEARD_VLD_DEL_SQLSTR,
        "person_plan_awardunit_put_h_vld": INSERT_PRNAWAR_HEARD_VLD_PUT_SQLSTR,
        "person_plan_awardunit_del_h_vld": INSERT_PRNAWAR_HEARD_VLD_DEL_SQLSTR,
        "person_plan_factunit_put_h_vld": INSERT_PRNFACT_HEARD_VLD_PUT_SQLSTR,
        "person_plan_factunit_del_h_vld": INSERT_PRNFACT_HEARD_VLD_DEL_SQLSTR,
        "person_plan_healerunit_put_h_vld": INSERT_PRNHEAL_HEARD_VLD_PUT_SQLSTR,
        "person_plan_healerunit_del_h_vld": INSERT_PRNHEAL_HEARD_VLD_DEL_SQLSTR,
        "person_plan_reason_caseunit_put_h_vld": INSERT_PRNCASE_HEARD_VLD_PUT_SQLSTR,
        "person_plan_reason_caseunit_del_h_vld": INSERT_PRNCASE_HEARD_VLD_DEL_SQLSTR,
        "person_plan_reasonunit_put_h_vld": INSERT_PRNREAS_HEARD_VLD_PUT_SQLSTR,
        "person_plan_reasonunit_del_h_vld": INSERT_PRNREAS_HEARD_VLD_DEL_SQLSTR,
        "person_plan_laborunit_put_h_vld": INSERT_PRNLABO_HEARD_VLD_PUT_SQLSTR,
        "person_plan_laborunit_del_h_vld": INSERT_PRNLABO_HEARD_VLD_DEL_SQLSTR,
        "person_planunit_put_h_vld": INSERT_PRNPLAN_HEARD_VLD_PUT_SQLSTR,
        "person_planunit_del_h_vld": INSERT_PRNPLAN_HEARD_VLD_DEL_SQLSTR,
        "personunit_put_h_vld": INSERT_PRNUNIT_HEARD_VLD_PUT_SQLSTR,
        "personunit_del_h_vld": INSERT_PRNUNIT_HEARD_VLD_DEL_SQLSTR,
    }


MMTPAYY_FU2_SELECT_SQLSTR = "SELECT moment_rope, person_name, contact_name, tran_time, amount, knot FROM moment_paybook_h_vld WHERE moment_rope = "
MMTBUDD_FU2_SELECT_SQLSTR = "SELECT moment_rope, person_name, bud_time, knot, quota, celldepth FROM moment_budunit_h_vld WHERE moment_rope = "
MMTHOUR_FU2_SELECT_SQLSTR = "SELECT moment_rope, cumulative_minute, hour_label, knot FROM moment_epoch_hour_h_vld WHERE moment_rope = "
MMTMONT_FU2_SELECT_SQLSTR = "SELECT moment_rope, cumulative_day, month_label, knot FROM moment_epoch_month_h_vld WHERE moment_rope = "
MMTWEEK_FU2_SELECT_SQLSTR = "SELECT moment_rope, weekday_order, weekday_label, knot FROM moment_epoch_weekday_h_vld WHERE moment_rope = "
MMTOFFI_FU2_SELECT_SQLSTR = "SELECT moment_rope, offi_time, knot FROM moment_timeoffi_h_vld WHERE moment_rope = "
MMTUNIT_FU2_SELECT_SQLSTR = "SELECT moment_rope, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, mana_grain, respect_grain, knot, job_listen_rotations FROM momentunit_h_vld WHERE moment_rope = "


def get_moment_heard_select1_sqlstrs(moment_rope: str) -> dict[str, str]:
    return {
        "momentunit": f"{MMTUNIT_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_budunit": f"{MMTBUDD_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_paybook": f"{MMTPAYY_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_epoch_hour": f"{MMTHOUR_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_epoch_month": f"{MMTMONT_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_epoch_weekday": f"{MMTWEEK_FU2_SELECT_SQLSTR}'{moment_rope}'",
        "moment_timeoffi": f"{MMTOFFI_FU2_SELECT_SQLSTR}'{moment_rope}'",
    }


def get_idea_stageble_put_dimens() -> dict[str, list[str]]:
    return {
        "br00000": ["momentunit"],
        "br00001": ["personunit", "moment_budunit", "momentunit"],
        "br00002": ["person_contactunit", "personunit", "moment_paybook", "momentunit"],
        "br00003": ["moment_epoch_hour", "momentunit"],
        "br00004": ["moment_epoch_month", "momentunit"],
        "br00005": ["moment_epoch_weekday", "momentunit"],
        "br00006": ["moment_timeoffi", "momentunit"],
        "br00011": ["person_contactunit", "personunit", "momentunit"],
        "br00012": [
            "person_contact_membership",
            "person_contactunit",
            "personunit",
            "momentunit",
        ],
        "br00013": ["person_planunit", "personunit", "momentunit"],
        "br00019": ["person_planunit", "personunit", "momentunit"],
        "br00020": [
            "person_contact_membership",
            "person_contactunit",
            "personunit",
            "momentunit",
        ],
        "br00021": ["person_contactunit", "personunit", "momentunit"],
        "br00022": [
            "person_plan_awardunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00023": [
            "person_plan_factunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00024": [
            "person_plan_laborunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00025": [
            "person_plan_healerunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00026": [
            "person_plan_reason_caseunit",
            "person_plan_reasonunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00027": [
            "person_plan_reasonunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00028": ["person_planunit", "personunit", "momentunit"],
        "br00029": ["personunit", "momentunit"],
        "br00036": [
            "person_plan_healerunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["person_contactunit", "personunit", "momentunit"],
        "br00051": ["personunit", "momentunit"],
        "br00052": ["person_planunit", "personunit", "momentunit"],
        "br00053": ["person_planunit", "personunit", "momentunit"],
        "br00054": ["person_planunit", "personunit", "momentunit"],
        "br00055": ["person_planunit", "personunit", "momentunit"],
        "br00056": [
            "person_plan_reasonunit",
            "person_planunit",
            "personunit",
            "momentunit",
        ],
        "br00057": ["person_planunit", "personunit", "momentunit"],
        "br00058": ["personunit", "momentunit"],
        "br00059": ["momentunit"],
        "br00070": ["momentunit", "nabu_timenum"],
        "br00113": ["person_contactunit", "personunit", "momentunit"],
        "br00115": ["person_contactunit", "personunit", "momentunit"],
        "br00116": ["person_contactunit", "personunit", "momentunit"],
        "br00117": ["person_contactunit", "personunit", "momentunit"],
    }


IDEA_STAGEBLE_DEL_DIMENS = {
    "br00050": ["person_contact_membership"],
    "br00051": ["person_contactunit"],
    "br00052": ["person_plan_awardunit"],
    "br00053": ["person_plan_factunit"],
    "br00054": ["person_plan_laborunit"],
    "br00055": ["person_plan_healerunit"],
    "br00056": ["person_plan_reason_caseunit"],
    "br00057": ["person_plan_reasonunit"],
    "br00058": ["person_planunit"],
    "br00059": ["personunit"],
}


CREATE_MOMENT_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS moment_ote1_agg (
  moment_rope TEXT
, person_name TEXT
, spark_num INTEGER
, bud_time INTEGER
, knot TEXT
, error_message TEXT
)
;
"""
INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR = """
INSERT INTO moment_ote1_agg (moment_rope, person_name, spark_num, bud_time, knot)
SELECT moment_rope, person_name, spark_num, bud_time, knot
FROM (
    SELECT 
      moment_rope_inx moment_rope
    , person_name_inx person_name
    , spark_num
    , bud_time
    , knot
    FROM moment_budunit_h_raw
    GROUP BY moment_rope_inx, person_name_inx, spark_num, bud_time, knot
)
ORDER BY moment_rope, person_name, spark_num, bud_time, knot
;
"""


CREATE_JOB_PRNGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS person_groupunit_job (moment_rope TEXT, person_name TEXT, group_title TEXT, fund_grain REAL, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL)"""
CREATE_JOB_PRNMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contact_membership_job (moment_rope TEXT, person_name TEXT, contact_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL, fund_agenda_ratio_give REAL, fund_agenda_ratio_take REAL)"""
CREATE_JOB_PRNCONT_SQLSTR = """CREATE TABLE IF NOT EXISTS person_contactunit_job (moment_rope TEXT, person_name TEXT, contact_name TEXT, contact_cred_lumen REAL, contact_debt_lumen REAL, groupmark TEXT, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL, fund_agenda_ratio_give REAL, fund_agenda_ratio_take REAL, inallocable_contact_debt_lumen REAL, irrational_contact_debt_lumen REAL)"""
CREATE_JOB_PRNAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_awardunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, knot TEXT, fund_give REAL, fund_take REAL)"""
CREATE_JOB_PRNFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_factunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, knot TEXT)"""
CREATE_JOB_PRNHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_healerunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, healer_name TEXT, knot TEXT)"""
CREATE_JOB_PRNLABO_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_laborunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, labor_title TEXT, solo INTEGER, knot TEXT, person_name_is_workforce INTEGER)"""
CREATE_JOB_PRNCASE_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT, case_task INTEGER, case_active INTEGER)"""
CREATE_JOB_PRNREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS person_plan_reasonunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, knot TEXT, reason_active INTEGER, reason_task INTEGER, parent_heir_active INTEGER)"""
CREATE_JOB_PRNPLAN_SQLSTR = """CREATE TABLE IF NOT EXISTS person_planunit_job (moment_rope TEXT, person_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, fund_grain REAL, knot TEXT, plan_active INTEGER, plan_task INTEGER, fund_onset REAL, fund_cease REAL, fund_ratio REAL, gogo_calc REAL, stop_calc REAL, tree_level INTEGER, range_evaluated INTEGER, descendant_pledge_count INTEGER, healerunit_ratio REAL, all_contact_cred INTEGER, all_contact_debt INTEGER)"""
CREATE_JOB_PRNUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS personunit_job (moment_rope TEXT, person_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, fund_grain REAL, mana_grain REAL, respect_grain REAL, knot TEXT, rational INTEGER, keeps_justified INTEGER, offtrack_fund REAL, sum_healerunit_plans_fund_total REAL, keeps_buildable INTEGER, tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "person_contact_membership_job": CREATE_JOB_PRNMEMB_SQLSTR,
        "person_contactunit_job": CREATE_JOB_PRNCONT_SQLSTR,
        "person_groupunit_job": CREATE_JOB_PRNGROU_SQLSTR,
        "person_plan_awardunit_job": CREATE_JOB_PRNAWAR_SQLSTR,
        "person_plan_factunit_job": CREATE_JOB_PRNFACT_SQLSTR,
        "person_plan_healerunit_job": CREATE_JOB_PRNHEAL_SQLSTR,
        "person_plan_reason_caseunit_job": CREATE_JOB_PRNCASE_SQLSTR,
        "person_plan_reasonunit_job": CREATE_JOB_PRNREAS_SQLSTR,
        "person_plan_laborunit_job": CREATE_JOB_PRNLABO_SQLSTR,
        "person_planunit_job": CREATE_JOB_PRNPLAN_SQLSTR,
        "personunit_job": CREATE_JOB_PRNUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)
