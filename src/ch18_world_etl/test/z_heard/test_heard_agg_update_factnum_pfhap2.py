from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    get_update_prnfact_range_sqlstr,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def pfhap2_insert_prnfact(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = "fact_lower_otx", "fact_upper_otx", "context_plan_close", kw.inx_epoch_diff"""

    x_cols = [
        "fact_lower_otx",
        "fact_upper_otx",
        "context_plan_close",
        kw.inx_epoch_diff,
    ]
    tablename = create_prime_db_table(cursor0, kw.prnfact, "h", "agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pfhap2_select_prnfact(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
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


def test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario0_NoWrap_dayly(
    cursor0,
):
    # ESTABLISH modeled after # def test_add_frame_to_factunit_SetsAttr_epoch_Scenario0_NoWrap

    fact_lower_otx, fact_upper_otx = (7777, 8000)
    context_plan_close = 5259492000
    inx_epoch_diff = 100
    prnfact_val = [fact_lower_otx, fact_upper_otx, context_plan_close, inx_epoch_diff]
    prnfact_insert_sql = pfhap2_insert_prnfact(cursor0, [prnfact_val])

    # BEFORE
    assert pfhap2_select_prnfact(cursor0) == [
        (fact_lower_otx, None, fact_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prnfact_range_sqlstr())

    # THEN
    fact_lower_inx = fact_lower_otx + inx_epoch_diff
    fact_upper_inx = fact_upper_otx + inx_epoch_diff
    assert pfhap2_select_prnfact(cursor0) == [
        (fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx)
    ]
    assert pfhap2_select_prnfact(cursor0) == [(7777, 7877, 8000, 8100)]


def test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario1_Wrap_dayly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_factunit_SetsAttr_Scenario1_Wrap_dayly
    fact_lower_otx, fact_upper_otx = (7777, 8000)
    context_plan_close = 5259492000
    inx_epoch_diff = 200 + context_plan_close
    prnfact_val = [fact_lower_otx, fact_upper_otx, context_plan_close, inx_epoch_diff]
    prnfact_insert_sql = pfhap2_insert_prnfact(cursor0, [prnfact_val])

    # BEFORE
    assert pfhap2_select_prnfact(cursor0) == [
        (fact_lower_otx, None, fact_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prnfact_range_sqlstr())

    # THEN
    fact_lower_inx = (fact_lower_otx + inx_epoch_diff) % context_plan_close
    fact_upper_inx = (fact_upper_otx + inx_epoch_diff) % context_plan_close
    assert pfhap2_select_prnfact(cursor0) == [
        (fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx)
    ]
    assert pfhap2_select_prnfact(cursor0) == [(7777, 7977, 8000, 8200)]


def test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario2_inx_epoch_diff_IsNULL(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_factunit_SetsAttr_Scenario1_Wrap_dayly
    fact_lower_otx, fact_upper_otx = (7777, 8000)
    context_plan_close = 5259492000
    inx_epoch_diff = None
    prnfact_val = [fact_lower_otx, fact_upper_otx, context_plan_close, inx_epoch_diff]
    prnfact_insert_sql = pfhap2_insert_prnfact(cursor0, [prnfact_val])

    # BEFORE
    assert pfhap2_select_prnfact(cursor0) == [
        (fact_lower_otx, None, fact_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prnfact_range_sqlstr())

    # THEN
    fact_lower_inx = fact_lower_otx
    fact_upper_inx = fact_upper_otx
    assert pfhap2_select_prnfact(cursor0) == [
        (fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx)
    ]
    assert pfhap2_select_prnfact(cursor0) == [(7777, 7777, 8000, 8000)]


def test_get_update_prnfact_range_sqlstr_ReturnsObj():
    # ESTABLISH
    prnfact_tablename = prime_tbl(kw.person_plan_factunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_prnfact_range_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
UPDATE {prnfact_tablename}
SET
 {kw.fact_lower}_inx =
  CASE
   WHEN {kw.inx_epoch_diff} IS NULL
   THEN {kw.fact_lower}_otx
   WHEN context_plan_{kw.close} IS NOT NULL
   THEN ({kw.fact_lower}_otx + {kw.inx_epoch_diff}) % context_plan_{kw.close}
  END,
 {kw.fact_upper}_inx =
  CASE
   WHEN {kw.inx_epoch_diff} IS NULL
   THEN {kw.fact_upper}_otx
   WHEN context_plan_{kw.close} IS NOT NULL
   THEN ({kw.fact_upper}_otx + {kw.inx_epoch_diff}) % context_plan_{kw.close}
  END
;
"""
    print(update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr
