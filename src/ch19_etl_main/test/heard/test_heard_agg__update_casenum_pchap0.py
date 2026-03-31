from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr, get_row_count
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_etl_config.etl_config import create_prime_tablename
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    get_update_prncase_inx_epoch_diff_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def pchap0_insert_nabtime(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]"""

    x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]
    tablename = create_prime_db_table(cursor0, kw.nabu_timenum, kw.h_agg)
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchap0_insert_prncase(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.plan_rope]"""

    x_cols = [kw.spark_num, kw.plan_rope]
    tablename = create_prime_db_table(cursor0, kw.prncase, kw.h_agg, "put")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def pchap0_select_prncase(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT spark_num, plan_rope, {kw.inx_epoch_diff}"""

    prncase_h_agg_table = create_prime_tablename(kw.prncase, kw.h_agg, "put")
    sel_prncase_str = f"""
SELECT {kw.spark_num}, {kw.plan_rope}, {kw.inx_epoch_diff} 
FROM {prncase_h_agg_table}
ORDER BY {kw.spark_num}, {kw.plan_rope}, {kw.inx_epoch_diff}
;"""
    x_rows = cursor0.execute(sel_prncase_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_get_update_prncase_inx_epoch_diff_sqlstr_SQLTEST_One_row(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    otx_time = 199
    inx_time = 13
    nabtime_vals = [[spark7, wx.root_rope, otx_time, inx_time]]
    pchap0_insert_nabtime(cursor0, nabtime_vals)
    prncase_vals = [[spark7, wx.clean_rope]]
    prncase_insert_sql = pchap0_insert_prncase(cursor0, prncase_vals)
    print(prncase_insert_sql)

    # BEFORE
    assert pchap0_select_prncase(cursor0) == [(7, wx.clean_rope, None)]

    # WHEN
    cursor0.execute(get_update_prncase_inx_epoch_diff_sqlstr())

    # THEN
    expected_inx_epoch_diff = otx_time - 13
    assert pchap0_select_prncase(cursor0, True) == [
        (7, wx.clean_rope, expected_inx_epoch_diff)
    ]


def test_get_update_prncase_inx_epoch_diff_sqlstr_SQLTEST_Two_rows(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7, spark9 = (7, 9)
    otx_time7, inx_time7 = (199, 13)
    otx_time9, inx_time9 = (1000, 2)
    nabtime_vals = [
        [spark7, wx.root_rope, otx_time7, inx_time7],
        [spark9, wx.root_rope, otx_time9, inx_time9],
    ]
    pchap0_insert_nabtime(cursor0, nabtime_vals)
    prncase_vals = [[spark7, wx.clean_rope], [spark9, wx.clean_rope]]
    pchap0_insert_prncase(cursor0, prncase_vals)

    # BEFORE
    assert pchap0_select_prncase(cursor0) == [
        (7, wx.clean_rope, None),
        (9, wx.clean_rope, None),
    ]

    # WHEN
    update_sql = get_update_prncase_inx_epoch_diff_sqlstr()
    print(update_sql)
    cursor0.execute(update_sql)

    # THEN
    expected_inx_epoch_diff7 = otx_time7 - inx_time7
    expected_inx_epoch_diff9 = otx_time9 - inx_time9
    assert pchap0_select_prncase(cursor0, True) == [
        (7, wx.clean_rope, expected_inx_epoch_diff7),
        (9, wx.clean_rope, expected_inx_epoch_diff9),
    ]


def test_get_update_prncase_inx_epoch_diff_sqlstr_SQLTEST_Three_rows_Two_person_name(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7, spark9 = (7, 9)
    otx_time7, inx_time7 = (199, 13)
    yao_otx_time9, yao_inx_time9 = (1000, 2)
    zia_otx_time9, zia_inx_time9 = (37, 43)
    nabtime_vals = [
        [spark7, wx.root_rope, otx_time7, inx_time7],
        [spark9, wx.root_rope, yao_otx_time9, yao_inx_time9],
        [spark9, exx.a23_dash, zia_otx_time9, zia_inx_time9],
    ]
    assert wx.root_rope != exx.a23_dash
    pchap0_insert_nabtime(cursor0, nabtime_vals)
    prncase_vals = [
        [spark7, wx.clean_rope],
        [spark9, wx.clean_rope],
        [spark9, exx.a23_dash],
    ]
    pchap0_insert_prncase(cursor0, prncase_vals)

    # BEFORE
    assert pchap0_select_prncase(cursor0) == [
        (7, wx.clean_rope, None),
        (9, exx.a23_dash, None),
        (9, wx.clean_rope, None),
    ]

    # WHEN
    update_sql = get_update_prncase_inx_epoch_diff_sqlstr()
    print(update_sql)
    cursor0.execute(update_sql)

    # THEN
    expected_inx_epoch_diff7 = otx_time7 - inx_time7
    expected_yao9_inx_epoch_diff = yao_otx_time9 - yao_inx_time9
    expected_zia9_inx_epoch_diff = zia_otx_time9 - zia_inx_time9
    assert pchap0_select_prncase(cursor0, True) == [
        (7, wx.clean_rope, expected_inx_epoch_diff7),
        (9, exx.a23_dash, expected_zia9_inx_epoch_diff),
        (9, wx.clean_rope, expected_yao9_inx_epoch_diff),
    ]
    assert pchap0_select_prncase(cursor0) == [
        (7, wx.clean_rope, 186),
        (9, exx.a23_dash, -6),
        (9, wx.clean_rope, 998),
    ]


def test_get_update_prncase_inx_epoch_diff_sqlstr_SQLTEST_Populates_inx_epoch_diff_FromPreviousSparkNum(
    cursor0: Cursor,
):
    # ESTABLISH
    spark3 = 3
    otx_time, inx_time = (199, 13)
    nabtime_vals = [[spark3, wx.root_rope, otx_time, inx_time]]
    pchap0_insert_nabtime(cursor0, nabtime_vals)
    spark7 = 7
    prncase_vals = [[spark7, wx.clean_rope]]
    prncase_insert_sql = pchap0_insert_prncase(cursor0, prncase_vals)

    # BEFORE
    assert pchap0_select_prncase(cursor0) == [(spark7, wx.clean_rope, None)]

    # WHEN
    cursor0.execute(get_update_prncase_inx_epoch_diff_sqlstr())

    # THEN
    expected_inx_epoch_diff = otx_time - inx_time
    assert pchap0_select_prncase(cursor0, True) == [
        (spark7, wx.clean_rope, expected_inx_epoch_diff)
    ]
    assert pchap0_select_prncase(cursor0) == [(7, wx.clean_rope, 186)]


def test_get_update_prncase_inx_epoch_diff_sqlstr_ReturnsObj():
    # ESTABLISH
    prncase_tablename = prime_tbl(kw.prncase, kw.h_agg, "put")
    nabtime_tablename = prime_tbl(kw.nabtime, kw.h_agg)

    # WHEN
    update_sqlstr = get_update_prncase_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
UPDATE {prncase_tablename} as {kw.prncase}
SET {kw.inx_epoch_diff} = {kw.otx_time} - {kw.inx_time}
FROM {nabtime_tablename} as {kw.nabtime}
WHERE 
    {kw.nabtime}.{kw.spark_num} = (
        SELECT MAX(n2.{kw.spark_num})
        FROM {nabtime_tablename} as n2
        WHERE n2.{kw.spark_num} <= {kw.prncase}.{kw.spark_num}
            AND {kw.prncase}.{kw.plan_rope} LIKE n2.{kw.moment_rope} || '%'
        )
    AND {kw.prncase}.{kw.plan_rope} LIKE {kw.nabtime}.{kw.moment_rope} || '%'
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr
