from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    get_update_prnfact_context_plan_sqlstr,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_update_prnfact_context_plan_sqlstr_ReturnsObj():
    # ESTABLISH
    prnfact_tablename = prime_tbl(kw.prnfact, "h", "agg", "put")
    prnplan_tablename = prime_tbl(kw.person_planunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_prnfact_context_plan_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
UPDATE {prnfact_tablename} as prnfact
SET 
  context_plan_close = prnplan.{kw.close}
, context_plan_denom = prnplan.{kw.denom}
, context_plan_morph = prnplan.{kw.morph}
FROM {prnplan_tablename} prnplan
WHERE prnfact.{kw.spark_num} = prnplan.{kw.spark_num}
    AND prnfact.{kw.person_name} = prnplan.{kw.person_name}
    AND prnfact.{kw.fact_context} = prnplan.{kw.plan_rope}
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def pfhap1_insert_prnfact(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.fact_context]"""
    x_cols = [kw.spark_num, kw.person_name, kw.fact_context]
    tablename = create_prime_db_table(cursor0, kw.prnfact, "h", "agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pfhap1_insert_prnplan(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.close, kw.denom, kw.morph]"""
    x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.close, kw.denom, kw.morph]
    tablename = create_prime_db_table(cursor0, kw.prnplan, "h", "agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pfhap1_select_prnfact(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT spark_num, person_name, fact_context, context_plan_close, context_plan_denom, context_plan_morph"""
    prnfact_h_agg_table = create_prime_tablename(kw.prnfact, "h", "agg", "put")
    sel_prnfact_str = f"""
SELECT spark_num, person_name, fact_context, context_plan_close, context_plan_denom, context_plan_morph 
FROM {prnfact_h_agg_table}
ORDER BY spark_num, person_name, fact_context, context_plan_close, context_plan_denom, context_plan_morph
;"""
    x_rows = cursor0.execute(sel_prnfact_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario0_1row(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    prnfact_vals = [[spark7, exx.sue, wx.clean_rope]]
    x0_close, x0_denom, x0_morph = (44, 55, 66)
    prnfact_insert_sql = pfhap1_insert_prnfact(cursor0, prnfact_vals)
    prnplan_in_vals = [[spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph]]
    prnplan_insert_sql = pfhap1_insert_prnplan(cursor0, prnplan_in_vals)
    assert pfhap1_select_prnfact(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, None, None, None)
    ]

    # WHEN
    cursor0.execute(get_update_prnfact_context_plan_sqlstr())

    # THEN
    assert pfhap1_select_prnfact(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph)
    ]


def test_test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario1_2rows(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7, spark9 = (7, 9)
    x0_close, x0_denom, x0_morph = (44, 55, 66)
    x1_close, x1_denom, x1_morph = (77, 88, 99)
    prnplan_in_vals = [
        [spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph],
        [spark9, exx.sue, wx.clean_rope, x1_close, x1_denom, x1_morph],
    ]
    prnplan_insert_sql = pfhap1_insert_prnplan(cursor0, prnplan_in_vals)
    print(prnplan_insert_sql)
    prnfact_vals = [[spark7, exx.sue, wx.clean_rope], [spark9, exx.sue, wx.clean_rope]]
    prnfact_insert_sql = pfhap1_insert_prnfact(cursor0, prnfact_vals)

    # BEFORE
    assert pfhap1_select_prnfact(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, None, None, None),
        (spark9, exx.sue, wx.clean_rope, None, None, None),
    ]

    # WHEN
    update_sql = get_update_prnfact_context_plan_sqlstr()
    cursor0.execute(update_sql)

    # THEN
    assert pfhap1_select_prnfact(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph),
        (spark9, exx.sue, wx.clean_rope, x1_close, x1_denom, x1_morph),
    ]


def test_test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario3_DifferentPersons(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    x0_close, x0_denom, x0_morph = (44, 55, 66)
    x1_close, x1_denom, x1_morph = (77, 88, 99)
    prnplan_in_vals = [
        [spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph],
        [spark7, exx.zia, wx.clean_rope, x1_close, x1_denom, x1_morph],
    ]
    prnplan_insert_sql = pfhap1_insert_prnplan(cursor0, prnplan_in_vals)
    prnfact_vals = [[spark7, exx.sue, wx.clean_rope], [spark7, exx.zia, wx.clean_rope]]
    prnfact_insert_sql = pfhap1_insert_prnfact(cursor0, prnfact_vals)

    # BEFORE
    assert pfhap1_select_prnfact(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, None, None, None),
        (spark7, exx.zia, wx.clean_rope, None, None, None),
    ]

    # WHEN
    update_sql = get_update_prnfact_context_plan_sqlstr()
    cursor0.execute(update_sql)

    # THEN
    assert pfhap1_select_prnfact(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph),
        (spark7, exx.zia, wx.clean_rope, x1_close, x1_denom, x1_morph),
    ]


def test_test_get_update_prnfact_context_plan_sqlstr_SQLTEST_Scenario4_Different_plan_rope(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    x0_close, x0_denom, x0_morph = (44, 55, 66)
    x1_close, x1_denom, x1_morph = (77, 88, 99)
    prnplan_in_vals = [
        [spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph],
        [spark7, exx.sue, wx.mop_rope, x1_close, x1_denom, x1_morph],
    ]
    prnplan_insert_sql = pfhap1_insert_prnplan(cursor0, prnplan_in_vals)
    prnfact_vals = [[spark7, exx.sue, wx.clean_rope], [spark7, exx.sue, wx.mop_rope]]
    prnfact_insert_sql = pfhap1_insert_prnfact(cursor0, prnfact_vals)

    # BEFORE
    assert pfhap1_select_prnfact(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, None, None, None),
        (spark7, exx.sue, wx.mop_rope, None, None, None),
    ]

    # WHEN
    update_sql = get_update_prnfact_context_plan_sqlstr()
    cursor0.execute(update_sql)

    # THEN
    assert pfhap1_select_prnfact(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, x0_close, x0_denom, x0_morph),
        (spark7, exx.sue, wx.mop_rope, x1_close, x1_denom, x1_morph),
    ]
