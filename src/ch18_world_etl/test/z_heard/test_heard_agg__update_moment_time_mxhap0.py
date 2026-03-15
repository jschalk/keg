from sqlite3 import Cursor
from src.ch00_py.db_toolbox import create_type_reference_insert_sqlstr, get_row_count
from src.ch13_time.epoch_main import DEFAULT_EPOCH_LENGTH, get_c400_constants
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch15_nabu.nabu_config import get_nabu_config_dict
from src.ch17_idea.idea_config import get_dimens_with_idea_element
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    get_update_heard_agg_moment_timenum_sqlstrs,
    get_update_heard_agg_timenum_sqlstr,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def mxhap0_insert_mmtunit(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.moment_rope, kw.c400_number]"""

    x_cols = [kw.spark_num, kw.moment_rope, kw.c400_number]
    tablename = create_prime_db_table(cursor0, kw.mmtunit, "h", "agg")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def mxhap0_insert_nabtime(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]"""

    x_cols = [kw.spark_num, kw.moment_rope, kw.otx_time, kw.inx_time]
    tablename = create_prime_db_table(cursor0, kw.nabtime, "h", "agg")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def mxhap0_insert_mmtoffi(cursor0: Cursor, x_values: list[list]) -> str:
    """x_cols = [kw.spark_num, kw.moment_rope, "offi_time_otx"]"""

    x_cols = [kw.spark_num, kw.moment_rope, f"{kw.offi_time}_otx"]
    tablename = create_prime_db_table(cursor0, kw.mmtoffi, "h", "agg")
    insert_sql = create_type_reference_insert_sqlstr(tablename, x_cols, x_values)
    cursor0.execute(insert_sql)
    return insert_sql


def mxhap0_select_mmtoffi(cursor0: Cursor, print_rows: bool = False) -> list[tuple]:
    """SELECT spark_num, moment_rope, offi_time_otx, offi_time_inx"""

    prnfact_h_agg_table = create_prime_tablename(kw.mmtoffi, "h", "agg")
    sel_prnfact_str = f"""
SELECT {kw.spark_num}, {kw.moment_rope}, offi_time_otx, offi_time_inx
FROM {prnfact_h_agg_table}
ORDER BY {kw.spark_num}, {kw.moment_rope}, offi_time_otx, offi_time_inx
;"""
    x_rows = cursor0.execute(sel_prnfact_str).fetchall()
    if print_rows:
        print(x_rows)
    return x_rows


def test_get_update_heard_agg_timenum_sqlstr_SQLTEST_Scenario0_PopulatesTableWithSingleRecord(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    a23_c400_number = 8
    mmtunit_vals = [[spark7, exx.a23, a23_c400_number]]
    mxhap0_insert_mmtunit(cursor0, mmtunit_vals)
    s7_otx_time = 44
    s7_inx_time = 55
    s7_offi_time_otx = 200
    nabtime_vals = [[spark7, exx.a23, s7_otx_time, s7_inx_time]]
    mxhap0_insert_nabtime(cursor0, nabtime_vals)
    mmtoffi_vals = [[spark7, exx.a23, s7_offi_time_otx]]
    mxhap0_insert_mmtoffi(cursor0, mmtoffi_vals)

    # BEFORE
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (spark7, exx.a23, s7_offi_time_otx, None)
    ]

    # WHEN
    mxhap0_table = create_prime_tablename(kw.mmtoffi, "h", "agg")
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(mxhap0_table, kw.offi_time)
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s7_offi_time_inx = s7_offi_time_otx + (s7_otx_time - s7_inx_time)
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (spark7, exx.a23, s7_offi_time_otx, s7_offi_time_inx)
    ]
    assert mxhap0_select_mmtoffi(cursor0) == [(7, exx.a23, 200, 189)]


def test_get_update_heard_agg_timenum_sqlstr_SQLTEST_Scenario1_PopulatesTableWhen_nabtime_RowDoesNotExist(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    a23_c400_number = 8
    mmtunit_vals = [[spark7, exx.a23, a23_c400_number]]
    mxhap0_insert_mmtunit(cursor0, mmtunit_vals)
    s7_offi_time_otx = 200
    mmtoffi_vals = [[spark7, exx.a23, s7_offi_time_otx]]
    create_prime_db_table(cursor0, kw.nabtime, "h", "agg")
    mxhap0_insert_mmtoffi(cursor0, mmtoffi_vals)

    # BEFORE
    assert mxhap0_select_mmtoffi(cursor0) == [(spark7, exx.a23, s7_offi_time_otx, None)]

    # WHEN
    mxhap0_table = create_prime_tablename(kw.mmtoffi, "h", "agg")
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(mxhap0_table, kw.offi_time)
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s7_offi_time_inx = s7_offi_time_otx
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (spark7, exx.a23, s7_offi_time_otx, s7_offi_time_inx)
    ]
    assert mxhap0_select_mmtoffi(cursor0) == [(7, exx.a23, 200, 200)]


def test_get_update_heard_agg_timenum_sqlstr_SQLTEST_Scenario3_PopulatesTableWithTwoRecords(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1, spark3 = (1, 3)
    s1_otx_time, s1_inx_time = (44, 55)
    s3_otx_time, s3_inx_time = (400, 550)
    s1_offi_time_otx = 200
    s3_offi_time_otx = 2000

    nabtime_vals = [
        [spark1, exx.a23, s1_otx_time, s1_inx_time],
        [spark3, exx.a23, s3_otx_time, s3_inx_time],
    ]
    mxhap0_insert_nabtime(cursor0, nabtime_vals)
    mmtoffi_vals = [
        [spark1, exx.a23, s1_offi_time_otx],
        [spark3, exx.a23, s3_offi_time_otx],
    ]
    mxhap0_insert_mmtoffi(cursor0, mmtoffi_vals)
    create_prime_db_table(cursor0, kw.mmtunit, "h", "agg")

    # BEFORE
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (spark1, exx.a23, s1_offi_time_otx, None),
        (spark3, exx.a23, s3_offi_time_otx, None),
    ]

    # WHEN
    mmtoffi_tbl = prime_tbl(kw.mmtoffi, "h", "agg")
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(mmtoffi_tbl, kw.offi_time)
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s1_inx_epoch_diff = s1_otx_time - s1_inx_time
    s3_inx_epoch_diff = s3_otx_time - s3_inx_time
    s1_offi_time_inx = s1_offi_time_otx + s1_inx_epoch_diff
    s3_offi_time_inx = s3_offi_time_otx + s3_inx_epoch_diff
    assert mxhap0_select_mmtoffi(cursor0) == [
        (spark1, exx.a23, s1_offi_time_otx, s1_offi_time_inx),
        (spark3, exx.a23, s3_offi_time_otx, s3_offi_time_inx),
    ]
    assert mxhap0_select_mmtoffi(cursor0) == [
        (1, exx.a23, 200, 189),
        (3, exx.a23, 2000, 1850),
    ]


def test_get_update_heard_agg_timenum_sqlstr_SQLTEST_Scenario4_PopulatesTableWithTwoRecordsAndDoesModularMath(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1, spark3 = (1, 3)
    s1_otx_time, s1_inx_time = (44, 55)
    s3_otx_time, s3_inx_time = (400, 550)
    s1_offi_time_otx, s3_offi_time_otx = (200, 2000)
    a23_c400_number = 5
    a23_epoch_length = get_c400_constants().c400_leap_length * a23_c400_number
    print(f"{a23_epoch_length=}")
    print(f"{DEFAULT_EPOCH_LENGTH=}")
    s3_otx_time, s3_inx_time = (400 + a23_epoch_length, 550)

    mmtunit_vals = [[spark1, exx.a23, a23_c400_number]]
    mxhap0_insert_mmtunit(cursor0, mmtunit_vals)
    nabtime_vals = [
        [spark1, exx.a23, s1_otx_time, s1_inx_time],
        [spark3, exx.a23, s3_otx_time, s3_inx_time],
    ]
    mxhap0_insert_nabtime(cursor0, nabtime_vals)
    mmtoffi_vals = [
        [spark1, exx.a23, s1_offi_time_otx],
        [spark3, exx.a23, s3_offi_time_otx],
    ]
    mxhap0_insert_mmtoffi(cursor0, mmtoffi_vals)

    # BEFORE
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (1, exx.a23, 200, None),
        (3, exx.a23, 2000, None),
    ]

    # WHEN
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(
        mmtoffi_h_agg_tablename, kw.offi_time
    )
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s1_inx_epoch_diff = s1_otx_time - s1_inx_time
    s3_inx_epoch_diff = s3_otx_time - s3_inx_time
    s1_offi_time_inx = s1_offi_time_otx + s1_inx_epoch_diff
    s3_offi_time_inx = (s3_offi_time_otx + s3_inx_epoch_diff) % a23_epoch_length
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (1, exx.a23, 200, s1_offi_time_inx),
        (3, exx.a23, 2000, s3_offi_time_inx),
    ]
    assert mxhap0_select_mmtoffi(cursor0) == [
        (1, exx.a23, 200, 189),
        (3, exx.a23, 2000, 1850),
    ]


# TODO reactivate and pass this test
def test_get_update_heard_agg_timenum_sqlstr_SQLTEST_Scenario5_CanDstTableCanJoinOnPreviousSparkNum(
    cursor0: Cursor,
):
    # ESTABLISH
    spark3 = 3
    s7_otx_time, s7_inx_time = (44, 55)
    nabtime_vals = [[spark3, exx.a23, s7_otx_time, s7_inx_time]]
    mxhap0_insert_nabtime(cursor0, nabtime_vals)
    spark7 = 7
    s7_offi_time_otx = 200
    mmtoffi_vals = [[spark7, exx.a23, s7_offi_time_otx]]
    mxhap0_insert_mmtoffi(cursor0, mmtoffi_vals)
    a23_c400_number = 8
    mmtunit_vals = [[spark7, exx.a23, a23_c400_number]]
    mxhap0_insert_mmtunit(cursor0, mmtunit_vals)

    # BEFORE
    assert mxhap0_select_mmtoffi(cursor0) == [(spark7, exx.a23, s7_offi_time_otx, None)]

    # WHEN
    mxhap0_table = create_prime_tablename(kw.mmtoffi, "h", "agg")
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(mxhap0_table, kw.offi_time)
    print(update_mmtoffi_sql)
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s7_offi_time_inx = s7_offi_time_otx + (s7_otx_time - s7_inx_time)
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (spark7, exx.a23, s7_offi_time_otx, s7_offi_time_inx)
    ]
    assert mxhap0_select_mmtoffi(cursor0) == [(7, exx.a23, 200, 189)]


def test_get_update_heard_agg_moment_timenum_sqlstrs_ReturnsObj():
    # ESTABLISH / WHEN
    gen_update_sqlstrs = get_update_heard_agg_moment_timenum_sqlstrs()

    # THEN
    assert gen_update_sqlstrs
    expected_update_sqlstrs = {}
    nabu_timenum_dict = get_nabu_config_dict().get(kw.nabu_timenum)
    TimeNum_dict = nabu_timenum_dict.get("affected_semantic_types").get("TimeNum")
    nabuable_dict = TimeNum_dict.get("nabuable_values")
    for timenum_arg in nabuable_dict:
        arg_dimens = get_dimens_with_idea_element(timenum_arg)
        print(f"{timenum_arg=} {arg_dimens=}")
        for arg_dimen in arg_dimens:
            prime_tablename = prime_tbl(arg_dimen, "h", "agg")
            update_sqlstr = get_update_heard_agg_timenum_sqlstr(
                prime_tablename, timenum_arg
            )
            expected_update_sqlstrs[(arg_dimen, timenum_arg)] = update_sqlstr
    assert set(gen_update_sqlstrs.keys()) == {
        (kw.moment_timeoffi, kw.offi_time),
        (kw.moment_paybook, kw.tran_time),
        (kw.moment_budunit, kw.bud_time),
    }
    assert gen_update_sqlstrs == expected_update_sqlstrs


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario1_MMTPAYY():
    # ESTABLISH
    mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
    nabtime_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
    mmtpayy_h_agg_tablename = prime_tbl(kw.moment_paybook, "h", "agg")
    c400_leap_length = get_c400_constants().c400_leap_length

    # WHEN
    generated_update_heard_agg_timenum_sqlstr = get_update_heard_agg_timenum_sqlstr(
        mmtpayy_h_agg_tablename, kw.tran_time
    )

    # THEN
    expected_sqlstr = f"""
WITH {kw.mmtunit} AS (
    SELECT {kw.moment_rope}, {kw.c400_number}
    FROM {mmtunit_h_agg_tablename}
    GROUP BY {kw.moment_rope}, {kw.c400_number}
),
enriched AS (
    SELECT
        dst2_table.{kw.spark_num},
        dst2_table.{kw.moment_rope},
        {kw.nabtime}.{kw.otx_time} - {kw.nabtime}.{kw.inx_time} AS {kw.inx_epoch_diff},
        {kw.mmtunit}.{kw.c400_number}
    FROM {mmtpayy_h_agg_tablename} as dst2_table
    LEFT JOIN {nabtime_h_agg_tablename} as {kw.nabtime}
        ON {kw.nabtime}.{kw.spark_num} = (
            SELECT MAX(n2.{kw.spark_num})
            FROM {nabtime_h_agg_tablename} as n2
            WHERE n2.{kw.spark_num} <= dst2_table.{kw.spark_num}
                AND dst2_table.{kw.moment_rope} LIKE n2.{kw.moment_rope} || '%'
        )
    LEFT JOIN {kw.mmtunit}
        ON {kw.mmtunit}.{kw.moment_rope} = {kw.nabtime}.{kw.moment_rope}
)
UPDATE {mmtpayy_h_agg_tablename} as dst_table
SET {kw.tran_time}_inx = mod(
    dst_table.{kw.tran_time}_otx + IFNULL(enriched.{kw.inx_epoch_diff}, 0)
    , IFNULL(enriched.{kw.c400_number} * {c400_leap_length}, {DEFAULT_EPOCH_LENGTH})
    )
FROM enriched
WHERE enriched.{kw.spark_num} = dst_table.{kw.spark_num}
    AND enriched.{kw.moment_rope} = dst_table.{kw.moment_rope}
;
"""
    assert generated_update_heard_agg_timenum_sqlstr == expected_sqlstr


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario0_MMTOFFI():
    # ESTABLISH
    mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
    nabtime_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    c400_leap_length = get_c400_constants().c400_leap_length

    # WHEN
    generated_update_heard_agg_timenum_sqlstr = get_update_heard_agg_timenum_sqlstr(
        mmtoffi_h_agg_tablename, kw.offi_time
    )

    # THEN
    expected_sqlstr = f"""
WITH {kw.mmtunit} AS (
    SELECT {kw.moment_rope}, {kw.c400_number}
    FROM {mmtunit_h_agg_tablename}
    GROUP BY {kw.moment_rope}, {kw.c400_number}
),
enriched AS (
    SELECT
        dst2_table.{kw.spark_num},
        dst2_table.{kw.moment_rope},
        {kw.nabtime}.{kw.otx_time} - {kw.nabtime}.{kw.inx_time} AS {kw.inx_epoch_diff},
        {kw.mmtunit}.{kw.c400_number}
    FROM {mmtoffi_h_agg_tablename} as dst2_table
    LEFT JOIN {nabtime_h_agg_tablename} as {kw.nabtime}
        ON {kw.nabtime}.{kw.spark_num} = (
            SELECT MAX(n2.{kw.spark_num})
            FROM {nabtime_h_agg_tablename} as n2
            WHERE n2.{kw.spark_num} <= dst2_table.{kw.spark_num}
                AND dst2_table.{kw.moment_rope} LIKE n2.{kw.moment_rope} || '%'
        )
    LEFT JOIN {kw.mmtunit}
        ON {kw.mmtunit}.{kw.moment_rope} = {kw.nabtime}.{kw.moment_rope}
)
UPDATE {mmtoffi_h_agg_tablename} as dst_table
SET {kw.offi_time}_inx = mod(
    dst_table.{kw.offi_time}_otx + IFNULL(enriched.{kw.inx_epoch_diff}, 0)
    , IFNULL(enriched.{kw.c400_number} * {c400_leap_length}, {DEFAULT_EPOCH_LENGTH})
    )
FROM enriched
WHERE enriched.{kw.spark_num} = dst_table.{kw.spark_num}
    AND enriched.{kw.moment_rope} = dst_table.{kw.moment_rope}
;
"""
    assert generated_update_heard_agg_timenum_sqlstr == expected_sqlstr
