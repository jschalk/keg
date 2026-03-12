from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_db_table,
    get_update_prncase_range_sqlstr,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO reactivate
# def test_get_update_prncase_range_sqlstr_ReturnsObj():
#     # ESTABLISH
#     prncase_tablename = prime_tbl(kw.person_plan_reason_caseunit, "h", "agg", "put")

#     # WHEN
#     update_sqlstr = get_update_prncase_range_sqlstr()

#     # THEN
#     assert update_sqlstr
#     expected_update_sqlstr = f"""
# WITH spark_prncase AS (
#     SELECT
#       spark_num
#     , IFNULL(reason_divisor, IFNULL(context_plan_close, context_plan_denom)) modulus
#     , CASE WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_plan_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
#     FROM {prncase_tablename}
#     GROUP BY spark_num, reason_divisor, context_plan_close, context_plan_denom, context_plan_morph
# )
# UPDATE {prncase_tablename}
# SET
#   reason_lower_inx = (reason_lower_otx + spark_prncase.calc_epoch_diff) % spark_prncase.modulus
# , reason_upper_inx = (reason_upper_otx + spark_prncase.calc_epoch_diff) % spark_prncase.modulus
# FROM spark_prncase
# WHERE {prncase_tablename}.spark_num IN (SELECT spark_num FROM spark_prncase)
# ;
# """
#     print(expected_update_sqlstr)
#     assert update_sqlstr == expected_update_sqlstr
#     assert 1 == 2


def pchap2_insert_prncase(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = kw.spark_num, "reason_lower_otx", "reason_upper_otx", kw.reason_divisor, "context_plan_close", "context_plan_denom", "context_plan_morph", kw.inx_epoch_diff"""

    x_cols = [
        kw.spark_num,
        "reason_lower_otx",
        "reason_upper_otx",
        kw.reason_divisor,
        "context_plan_close",
        "context_plan_denom",
        "context_plan_morph",
        kw.inx_epoch_diff,
    ]
    tablename = create_prime_db_table(cursor0, kw.prncase, "h", "agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchap2_select_prncase(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT spark_num, reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx"""

    prncase_h_agg_table = create_prime_tablename(kw.prncase, "h", "agg", "put")
    sel_prncase_str = f"""
SELECT spark_num, reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx
FROM {prncase_h_agg_table}
ORDER BY spark_num, reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx
;"""
    x_rows = cursor0.execute(sel_prncase_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario0_NoWrap_dayly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario0_NoWrap_dayly
    spark7 = 7
    reason_lower_otx, reason_upper_otx, reason_divisor = (600, 690, 1440)
    context_plan_close, context_plan_denom, context_plan_morph = (None, 1440, True)
    inx_epoch_diff = 100
    prncase_val = [
        spark7,
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_close,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (spark7, reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = reason_lower_otx + inx_epoch_diff
    reason_upper_inx = reason_upper_otx + inx_epoch_diff
    assert pchap2_select_prncase(cursor0) == [
        (spark7, reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(spark7, 600, 700, 690, 790)]


def test_test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario0_Wrap_dayly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario0_NoWrap_dayly
    spark7 = 7
    reason_lower_otx, reason_upper_otx, reason_divisor = (600, 690, 1440)
    context_plan_close, context_plan_denom, context_plan_morph = (None, 1440, True)
    inx_epoch_diff = 1000
    prncase_val = [
        spark7,
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_close,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (spark7, reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = (reason_lower_otx + inx_epoch_diff) % reason_divisor
    reason_upper_inx = (reason_upper_otx + inx_epoch_diff) % reason_divisor
    assert pchap2_select_prncase(cursor0) == [
        (spark7, reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(spark7, 600, 160, 690, 250)]


# TODO
# test_add_frame_to_caseunit_SetsAttr_Scenario3_adds_epoch_frame_NoWarp_xdays
# test_add_frame_to_caseunit_SetsAttr_Scenario4_adds_epoch_frame_Wrap_xdays
# test_add_frame_to_caseunit_SetsAttr_Scenario5_adds_epoch_frame_NoWrap_weekly
# test_add_frame_to_caseunit_SetsAttr_Scenario6_adds_epoch_frame_Wrap_weekly
