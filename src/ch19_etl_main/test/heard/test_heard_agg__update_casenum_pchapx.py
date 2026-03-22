from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_etl_config.etl_config import create_prime_tablename
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_db_table,
    update_caseunit_heard_agg_timenum_columns,
)
from src.ch19_etl_main.test._util.ch19_env import cursor0
from src.ref.keywords import Ch19Keywords as kw


def pchapx_insert_nabtime(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]"""

    x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]
    tablename = create_prime_db_table(cursor0, kw.nabu_timenum, "h_agg")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchapx_insert_prnplan(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.denom, kw.morph]"""

    x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.denom, kw.morph]
    tablename = create_prime_db_table(cursor0, kw.prnplan, "h_agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchapx_insert_prncase(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.reason_context, "reason_lower_otx", "reason_upper_otx"]"""
    x_cols = [
        kw.spark_num,
        kw.person_name,
        kw.plan_rope,
        kw.reason_context,
        "reason_lower_otx",
        "reason_upper_otx",
    ]

    tablename = create_prime_db_table(cursor0, kw.prncase, "h_agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchapx_select_prncase(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx"""

    prncase_h_agg_table = create_prime_tablename(kw.prncase, "h_agg", "put")
    sel_prncase_str = f"""
SELECT reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx
FROM {prncase_h_agg_table}
ORDER BY reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx
;"""
    x_rows = cursor0.execute(sel_prncase_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_update_caseunit_heard_agg_timenum_columns_SQLTEST_Scenario0_NoWarp_range(
    cursor0,
):
    # ESTABLISH modeled after # def test_add_frame_to_caseunit_SetsAttr_epoch_Scenario0_NoWrap

    spark7 = 7
    time_otx, time_inx = (300, 200)
    reason_lower_otx, reason_upper_otx = (600, 690)
    plan_denom, plan_morph = (1440, True)
    nabtime_val = [spark7, wx.root_rope, time_otx, time_inx]
    prnplan_val = [spark7, wx.Bob, wx.mop_rope, plan_denom, plan_morph]
    prncase_val = [
        spark7,
        wx.Bob,
        wx.clean_rope,
        wx.mop_rope,
        reason_lower_otx,
        reason_upper_otx,
    ]

    insert_nabtime_sql = pchapx_insert_nabtime(cursor0, [nabtime_val])
    insert_prnplan_sql = pchapx_insert_prnplan(cursor0, [prnplan_val])
    insert_prncase_sql = pchapx_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchapx_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    update_caseunit_heard_agg_timenum_columns(cursor0)

    # THEN
    inx_epoch_diff = time_otx - time_inx
    reason_lower_inx = reason_lower_otx + inx_epoch_diff
    reason_upper_inx = reason_upper_otx + inx_epoch_diff
    assert pchapx_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchapx_select_prncase(cursor0) == [(600, 700, 690, 790)]
