from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_db_table,
    update_factunit_heard_agg_timenum_columns,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ref.keywords import Ch18Keywords as kw


def pfhapx_insert_nabtime(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]"""

    x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]
    tablename = create_prime_db_table(cursor0, kw.nabu_timenum, "h", "agg")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pfhapx_insert_prnplan(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.close]"""

    x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.close]
    tablename = create_prime_db_table(cursor0, kw.prnplan, "h", "agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pfhapx_insert_prnfact(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.fact_context, "fact_lower_otx", "fact_upper_otx"]"""
    x_cols = [
        kw.spark_num,
        kw.person_name,
        kw.plan_rope,
        kw.fact_context,
        "fact_lower_otx",
        "fact_upper_otx",
    ]

    tablename = create_prime_db_table(cursor0, kw.prnfact, "h", "agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pfhapx_select_prnfact(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx"""

    prnfact_h_agg_table = create_prime_tablename(kw.prnfact, "h", "agg", "put")
    sel_prnfact_str = f"""
SELECT fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx
FROM {prnfact_h_agg_table}
ORDER BY fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx
;"""
    x_rows = cursor0.execute(sel_prnfact_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_update_factunit_heard_agg_timenum_columns_SQLTEST_Scenario0_NoWarp_range(
    cursor0,
):
    # ESTABLISH modeled after # def test_add_frame_to_factunit_SetsAttr_epoch_Scenario0_NoWrap

    spark7 = 7
    time_otx, time_inx = (300, 200)
    fact_lower_otx, fact_upper_otx = (7777, 8000)
    plan_close = 5259492000
    nabtime_val = [spark7, wx.root_rope, time_otx, time_inx]
    prnplan_val = [spark7, wx.Bob, wx.mop_rope, plan_close]
    prnfact_val = [
        spark7,
        wx.Bob,
        wx.clean_rope,
        wx.mop_rope,
        fact_lower_otx,
        fact_upper_otx,
    ]

    insert_nabtime_sql = pfhapx_insert_nabtime(cursor0, [nabtime_val])
    insert_prnplan_sql = pfhapx_insert_prnplan(cursor0, [prnplan_val])
    insert_prnfact_sql = pfhapx_insert_prnfact(cursor0, [prnfact_val])

    # BEFORE
    assert pfhapx_select_prnfact(cursor0) == [
        (fact_lower_otx, None, fact_upper_otx, None)
    ]

    # WHEN
    update_factunit_heard_agg_timenum_columns(cursor0)

    # THEN
    inx_epoch_diff = time_otx - time_inx
    fact_lower_inx = fact_lower_otx + inx_epoch_diff
    fact_upper_inx = fact_upper_otx + inx_epoch_diff
    assert pfhapx_select_prnfact(cursor0, True) == [
        (fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx)
    ]
    assert pfhapx_select_prnfact(cursor0) == [(7777, 7877, 8000, 8100)]
