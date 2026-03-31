from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_etl_config.etl_config import create_prime_tablename
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    get_update_prncase_range_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def pchap2_insert_prncase(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = "reason_lower_otx", "reason_upper_otx", kw.reason_divisor, "context_plan_denom", "context_plan_morph", kw.inx_epoch_diff"""

    x_cols = [
        "reason_lower_otx",
        "reason_upper_otx",
        kw.reason_divisor,
        "context_plan_denom",
        "context_plan_morph",
        kw.inx_epoch_diff,
    ]
    tablename = create_prime_db_table(cursor0, kw.prncase, kw.h_agg, "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchap2_select_prncase(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx"""

    prncase_h_agg_table = create_prime_tablename(kw.prncase, kw.h_agg, "put")
    sel_prncase_str = f"""
SELECT reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx
FROM {prncase_h_agg_table}
ORDER BY reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx
;"""
    x_rows = cursor0.execute(sel_prncase_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario0_NoWrap_dayly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario0_NoWrap_dayly
    reason_lower_otx, reason_upper_otx, reason_divisor = (600, 690, 1440)
    context_plan_denom, context_plan_morph = (1440, True)
    inx_epoch_diff = 100
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = reason_lower_otx + inx_epoch_diff
    reason_upper_inx = reason_upper_otx + inx_epoch_diff
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(600, 700, 690, 790)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario1_Wrap_dayly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario1_Wrap_dayly
    reason_lower_otx, reason_upper_otx, reason_divisor = (600, 690, 1440)
    context_plan_denom, context_plan_morph = (1440, True)
    inx_epoch_diff = 1000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = (reason_lower_otx + inx_epoch_diff) % reason_divisor
    reason_upper_inx = (reason_upper_otx + inx_epoch_diff) % reason_divisor
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(600, 160, 690, 250)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario3_NoWarp_xdays(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario3_adds_epoch_frame_NoWarp_xdays
    reason_lower_otx, reason_upper_otx, reason_divisor = (3, 4, 13)
    context_plan_denom, context_plan_morph = (1440, None)
    inx_epoch_diff = 3000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    days_change = inx_epoch_diff // context_plan_denom
    reason_lower_inx = reason_lower_otx + days_change
    reason_upper_inx = reason_upper_otx + days_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(3, 5, 4, 6)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario4_Warp_xdays(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario4_adds_epoch_frame_Wrap_xdays
    reason_lower_otx, reason_upper_otx, reason_divisor = (3, 4, 13)
    context_plan_denom, context_plan_morph = (1440, None)
    inx_epoch_diff = 30000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    days_change = (inx_epoch_diff // context_plan_denom) % reason_divisor
    reason_lower_inx = reason_lower_otx + days_change
    reason_upper_inx = reason_upper_otx + days_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(3, 10, 4, 11)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario5_NoWarp_weekly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario5_adds_epoch_frame_NoWrap_weekly
    reason_lower_otx, reason_upper_otx, reason_divisor = (600, 690, 7200)
    context_plan_denom, context_plan_morph = (7200, True)
    inx_epoch_diff = 100
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    mins_change = inx_epoch_diff % context_plan_denom
    reason_lower_inx = reason_lower_otx + mins_change
    reason_upper_inx = reason_upper_otx + mins_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(600, 700, 690, 790)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario6_Wrap_weekly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario6_adds_epoch_frame_Wrap_weekly
    reason_lower_otx, reason_upper_otx, reason_divisor = (600, 690, 7200)
    context_plan_denom, context_plan_morph = (7200, True)
    inx_epoch_diff = 10000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    mins_change = inx_epoch_diff % context_plan_denom
    reason_lower_inx = reason_lower_otx + mins_change
    reason_upper_inx = reason_upper_otx + mins_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(600, 3400, 690, 3490)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario7_NoWrap_xweeks(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario7_adds_epoch_frame_NoWrap_xweeks
    reason_lower_otx, reason_upper_otx, reason_divisor = (3, 4, 13)
    context_plan_denom, context_plan_morph = (7200, None)
    inx_epoch_diff = 24000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    mins_change = inx_epoch_diff // context_plan_denom
    reason_lower_inx = reason_lower_otx + mins_change
    reason_upper_inx = reason_upper_otx + mins_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(3, 6, 4, 7)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario8_Wrap_xweeks(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario8_adds_epoch_frame_Wraps_every_xweeks
    reason_lower_otx, reason_upper_otx, reason_divisor = (3, 4, 13)
    context_plan_denom, context_plan_morph = (7200, None)
    inx_epoch_diff = 50000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    mins_change = inx_epoch_diff // context_plan_denom
    reason_lower_inx = reason_lower_otx + mins_change
    reason_upper_inx = reason_upper_otx + mins_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(3, 9, 4, 10)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario9_NoWrap_monthday(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario9_adds_epoch_frame_NoWrap_monthday
    reason_lower_otx, reason_upper_otx, reason_divisor = (43200, 47520, None)
    context_plan_denom, context_plan_morph = (525600, True)
    inx_epoch_diff = 500
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = reason_lower_otx + inx_epoch_diff
    reason_upper_inx = reason_upper_otx + inx_epoch_diff
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(43200, 43700, 47520, 48020)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario10_Wraps_monthday(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario10_adds_epoch_frame_Wraps_monthday
    reason_lower_otx, reason_upper_otx, reason_divisor = (43200, 47520, None)
    context_plan_denom, context_plan_morph = (525600, True)
    inx_epoch_diff = 5000000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = (reason_lower_otx + inx_epoch_diff) % context_plan_denom
    reason_upper_inx = (reason_upper_otx + inx_epoch_diff) % context_plan_denom
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(43200, 312800, 47520, 317120)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario11_NoWrap_monthly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario9_adds_epoch_frame_NoWrap_monthday
    reason_lower_otx, reason_upper_otx, reason_divisor = (43200, 47520, None)
    context_plan_denom, context_plan_morph = (525600, True)
    inx_epoch_diff = 500
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = reason_lower_otx + inx_epoch_diff
    reason_upper_inx = reason_upper_otx + inx_epoch_diff
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(43200, 43700, 47520, 48020)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario12_Wraps_monthly(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario12_adds_epoch_frame_Wraps_monthly
    reason_lower_otx, reason_upper_otx, reason_divisor = (43200, 47520, None)
    context_plan_denom, context_plan_morph = (525600, True)
    inx_epoch_diff = 5000000
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = (reason_lower_otx + inx_epoch_diff) % context_plan_denom
    reason_upper_inx = (reason_upper_otx + inx_epoch_diff) % context_plan_denom
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(43200, 312800, 47520, 317120)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario13_NoWarp_range(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario13_adds_epoch_frame_NoWrap_range
    epoch_len = 5259492000  # minutes in entire epoch range
    reason_lower_otx, reason_upper_otx, reason_divisor = (7777, 9777, epoch_len)
    context_plan_close, context_plan_denom, context_plan_morph = (epoch_len, None, None)
    inx_epoch_diff = 100
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    mins_change = inx_epoch_diff % context_plan_close
    reason_lower_inx = reason_lower_otx + mins_change
    reason_upper_inx = reason_upper_otx + mins_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0) == [(7777, 7877, 9777, 9877)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario14_Wraps_range(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario14_adds_epoch_frame_Wraps_range
    epoch_len = 5259492000  # minutes in entire epoch range
    reason_lower_otx, reason_upper_otx, reason_divisor = (7777, 9777, epoch_len)
    context_plan_close, context_plan_denom, context_plan_morph = (epoch_len, None, None)
    inx_epoch_diff = epoch_len + 101
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    mins_change = inx_epoch_diff % context_plan_close
    reason_lower_inx = reason_lower_otx + mins_change
    reason_upper_inx = reason_upper_otx + mins_change
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(7777, 7878, 9777, 9878)]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario15_inx_epoch_diff_IsNull(
    cursor0,
):
    # ESTABLISH modeled after test_add_frame_to_caseunit_SetsAttr_Scenario14_adds_epoch_frame_Wraps_range
    epoch_len = 5259492000  # minutes in entire epoch range
    reason_lower_otx, reason_upper_otx, reason_divisor = (7777, 9777, epoch_len)
    context_plan_close, context_plan_denom, context_plan_morph = (epoch_len, None, None)
    inx_epoch_diff = None
    prncase_val = [
        reason_lower_otx,
        reason_upper_otx,
        reason_divisor,
        context_plan_denom,
        context_plan_morph,
        inx_epoch_diff,
    ]
    prncase_insert_sql = pchap2_insert_prncase(cursor0, [prncase_val])

    # BEFORE
    assert pchap2_select_prncase(cursor0) == [
        (reason_lower_otx, None, reason_upper_otx, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_range_sqlstr())

    # THEN
    reason_lower_inx = reason_lower_otx
    reason_upper_inx = reason_upper_otx
    assert pchap2_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchap2_select_prncase(cursor0, True) == [(7777, 7777, 9777, 9777)]


def test_get_update_prncase_range_sqlstr_ReturnsObj():
    # ESTABLISH
    prncase_tablename = prime_tbl(kw.person_plan_reason_caseunit, kw.h_agg, "put")

    # WHEN
    update_sqlstr = get_update_prncase_range_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
UPDATE {prncase_tablename} as prncase
SET
 {kw.reason_lower}_inx =
  CASE
   WHEN {kw.reason_divisor} IS NOT NULL THEN
    CASE
     WHEN {kw.inx_epoch_diff} IS NULL
     THEN {kw.reason_lower}_otx
     WHEN context_plan_morph = 1
     THEN ({kw.reason_lower}_otx + {kw.inx_epoch_diff}) % {kw.reason_divisor}
     WHEN context_plan_morph IS NULL
     THEN ({kw.reason_lower}_otx + CAST({kw.inx_epoch_diff} / IFNULL(context_plan_denom, 1) AS INTEGER)) % {kw.reason_divisor}
    END
   WHEN context_plan_denom IS NOT NULL THEN
    CASE
     WHEN {kw.inx_epoch_diff} IS NULL
     THEN {kw.reason_lower}_otx
     WHEN context_plan_morph = 1
     THEN ({kw.reason_lower}_otx + {kw.inx_epoch_diff}) % context_plan_denom
     WHEN context_plan_morph IS NULL
     THEN ({kw.reason_lower}_otx + CAST({kw.inx_epoch_diff} / IFNULL(context_plan_denom, 1) AS INTEGER)) % context_plan_denom
    END
  END,
 {kw.reason_upper}_inx =
  CASE
   WHEN {kw.reason_divisor} IS NOT NULL THEN
    CASE
     WHEN {kw.inx_epoch_diff} IS NULL
     THEN {kw.reason_upper}_otx
     WHEN context_plan_morph = 1
     THEN ({kw.reason_upper}_otx + {kw.inx_epoch_diff}) % {kw.reason_divisor}
     WHEN context_plan_morph IS NULL
     THEN ({kw.reason_upper}_otx + CAST({kw.inx_epoch_diff} / IFNULL(context_plan_denom, 1) AS INTEGER)) % {kw.reason_divisor}
    END
   WHEN context_plan_denom IS NOT NULL THEN
    CASE
     WHEN {kw.inx_epoch_diff} IS NULL
     THEN {kw.reason_upper}_otx
     WHEN context_plan_morph = 1
     THEN ({kw.reason_upper}_otx + {kw.inx_epoch_diff}) % context_plan_denom
     WHEN context_plan_morph IS NULL
     THEN ({kw.reason_upper}_otx + CAST({kw.inx_epoch_diff} / IFNULL(context_plan_denom, 1) AS INTEGER)) % context_plan_denom
    END
  END
;
"""
    print(update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr
