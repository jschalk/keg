from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_etl_config.etl_config import create_prime_tablename
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    get_update_prncase_context_plan_sqlstr,
)
from src.ch19_etl_main.test._util.ch19_env import cursor0
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_get_update_prncase_context_plan_sqlstr_ReturnsObj():
    # ESTABLISH
    prncase_tablename = prime_tbl(kw.person_plan_reason_caseunit, "h_agg", "put")
    prnplan_tablename = prime_tbl(kw.person_planunit, "h_agg", "put")

    # WHEN
    update_sqlstr = get_update_prncase_context_plan_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
UPDATE {prncase_tablename} as prncase
SET 
  context_plan_denom = prnplan.{kw.denom}
, context_plan_morph = prnplan.{kw.morph}
FROM {prnplan_tablename} prnplan
WHERE prncase.{kw.spark_num} = prnplan.{kw.spark_num}
    AND prncase.{kw.person_name} = prnplan.{kw.person_name}
    AND prncase.{kw.reason_context} = prnplan.{kw.plan_rope}
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def pchap1_insert_prncase(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.reason_context]"""
    x_cols = [kw.spark_num, kw.person_name, kw.reason_context]
    tablename = create_prime_db_table(cursor0, kw.prncase, "h_agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchap1_insert_prnplan(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.denom, kw.morph]"""
    x_cols = [kw.spark_num, kw.person_name, kw.plan_rope, kw.denom, kw.morph]
    tablename = create_prime_db_table(cursor0, kw.prnplan, "h_agg", "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchap1_select_prncase(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT spark_num, person_name, reason_context, context_plan_denom, context_plan_morph"""
    prncase_h_agg_table = create_prime_tablename(kw.prncase, "h_agg", "put")
    sel_prncase_str = f"""
SELECT spark_num, person_name, reason_context, context_plan_denom, context_plan_morph 
FROM {prncase_h_agg_table}
ORDER BY spark_num, person_name, reason_context, context_plan_denom, context_plan_morph
;"""
    x_rows = cursor0.execute(sel_prncase_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario0_1row(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    prncase_vals = [[spark7, exx.sue, wx.clean_rope]]
    x0_denom, x0_morph = (55, 66)
    prncase_insert_sql = pchap1_insert_prncase(cursor0, prncase_vals)
    prnplan_in_vals = [[spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph]]
    prnplan_insert_sql = pchap1_insert_prnplan(cursor0, prnplan_in_vals)

    # BEFORE
    assert pchap1_select_prncase(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, None, None)
    ]

    # WHEN
    cursor0.execute(get_update_prncase_context_plan_sqlstr())

    # THEN
    assert pchap1_select_prncase(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph)
    ]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario1_2rows(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7, spark9 = (7, 9)
    x0_denom, x0_morph = (55, 66)
    x1_denom, x1_morph = (88, 99)
    prnplan_in_vals = [
        [spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph],
        [spark9, exx.sue, wx.clean_rope, x1_denom, x1_morph],
    ]
    prnplan_insert_sql = pchap1_insert_prnplan(cursor0, prnplan_in_vals)
    prncase_vals = [[spark7, exx.sue, wx.clean_rope], [spark9, exx.sue, wx.clean_rope]]
    prncase_insert_sql = pchap1_insert_prncase(cursor0, prncase_vals)

    # BEFORE
    assert pchap1_select_prncase(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, None, None),
        (spark9, exx.sue, wx.clean_rope, None, None),
    ]

    # WHEN
    update_sql = get_update_prncase_context_plan_sqlstr()
    cursor0.execute(update_sql)

    # THEN
    assert pchap1_select_prncase(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph),
        (spark9, exx.sue, wx.clean_rope, x1_denom, x1_morph),
    ]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario3_DifferentPersons(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    x0_denom, x0_morph = (55, 66)
    x1_denom, x1_morph = (88, 99)
    prnplan_in_vals = [
        [spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph],
        [spark7, exx.zia, wx.clean_rope, x1_denom, x1_morph],
    ]
    prnplan_insert_sql = pchap1_insert_prnplan(cursor0, prnplan_in_vals)
    prncase_vals = [[spark7, exx.sue, wx.clean_rope], [spark7, exx.zia, wx.clean_rope]]
    prncase_insert_sql = pchap1_insert_prncase(cursor0, prncase_vals)

    # BEFORE
    assert pchap1_select_prncase(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, None, None),
        (spark7, exx.zia, wx.clean_rope, None, None),
    ]

    # WHEN
    update_sql = get_update_prncase_context_plan_sqlstr()
    cursor0.execute(update_sql)

    # THEN
    assert pchap1_select_prncase(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph),
        (spark7, exx.zia, wx.clean_rope, x1_denom, x1_morph),
    ]


def test_get_update_prncase_context_plan_sqlstr_SQLTEST_Scenario4_Different_plan_rope(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    x0_denom, x0_morph = (55, 66)
    x1_denom, x1_morph = (88, 99)
    prnplan_in_vals = [
        [spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph],
        [spark7, exx.sue, wx.mop_rope, x1_denom, x1_morph],
    ]
    prnplan_insert_sql = pchap1_insert_prnplan(cursor0, prnplan_in_vals)
    prncase_vals = [[spark7, exx.sue, wx.clean_rope], [spark7, exx.sue, wx.mop_rope]]
    prncase_insert_sql = pchap1_insert_prncase(cursor0, prncase_vals)

    # BEFORE
    assert pchap1_select_prncase(cursor0) == [
        (spark7, exx.sue, wx.clean_rope, None, None),
        (spark7, exx.sue, wx.mop_rope, None, None),
    ]

    # WHEN
    update_sql = get_update_prncase_context_plan_sqlstr()
    cursor0.execute(update_sql)

    # THEN
    assert pchap1_select_prncase(cursor0, True) == [
        (spark7, exx.sue, wx.clean_rope, x0_denom, x0_morph),
        (spark7, exx.sue, wx.mop_rope, x1_denom, x1_morph),
    ]
