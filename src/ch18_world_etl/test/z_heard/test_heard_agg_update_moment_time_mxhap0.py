from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch13_time.epoch_main import DEFAULT_EPOCH_LENGTH, get_c400_constants
from src.ch15_nabu.nabu_config import get_nabu_config_dict
from src.ch17_idea.idea_config import get_dimens_with_idea_element
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_update_heard_agg_timenum_sqlstr,
    get_update_heard_agg_timenum_sqlstrs,
    update_heard_agg_timenum_columns,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ch18_world_etl.test._util.ch18_examples import (
    insert_mmtoffi_special_offi_time_otx as insert_offi_time_otx,
    insert_mmtunit_special_c400_number as insert_c400_number,
    insert_nabtime_h_agg_otx_inx_time as insert_otx_inx_time,
    select_mmtoffi_special_offi_time_inx as select_offi_time_inx,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario0_MMTOFFI():
    # ESTABLISH
    mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
    nabtime_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    c400_leap_length = get_c400_constants().c400_leap_length
    cte_tablename = f"spark_{kw.inx_epoch_diff}"

    # WHEN
    generated_update_heard_agg_timenum_sqlstr = get_update_heard_agg_timenum_sqlstr(
        mmtoffi_h_agg_tablename, kw.offi_time
    )

    # THEN
    expected_sqlstr = f"""WITH {cte_tablename} AS (
SELECT 
  {kw.spark_num}
, {kw.otx_time} - {kw.inx_time} AS {kw.inx_epoch_diff}
, IFNULL({kw.c400_number} * {c400_leap_length}, {DEFAULT_EPOCH_LENGTH}) as {kw.epoch_length}
FROM {nabtime_h_agg_tablename}
LEFT JOIN (
    SELECT {kw.moment_rope}, {kw.c400_number} 
    FROM {mmtunit_h_agg_tablename} 
    GROUP BY {kw.moment_rope}, {kw.c400_number}
    ) x_moment ON x_moment.{kw.moment_rope} = {nabtime_h_agg_tablename}.{kw.moment_rope}
)
UPDATE {mmtoffi_h_agg_tablename}
SET {kw.offi_time}_inx = mod({kw.offi_time}_otx + (
    SELECT {kw.inx_epoch_diff}
    FROM {cte_tablename}
    WHERE {cte_tablename}.{kw.spark_num} = {mmtoffi_h_agg_tablename}.{kw.spark_num}
), (SELECT {kw.epoch_length}
    FROM {cte_tablename}
    WHERE {cte_tablename}.{kw.spark_num} = {mmtoffi_h_agg_tablename}.{kw.spark_num}
))
FROM {cte_tablename}
WHERE {mmtoffi_h_agg_tablename}.{kw.spark_num} IN (SELECT {kw.spark_num} FROM {cte_tablename})
;
"""
    assert generated_update_heard_agg_timenum_sqlstr == expected_sqlstr


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario1_MMTPAYY():
    # ESTABLISH
    mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
    nabtime_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
    mmtpayy_h_agg_tablename = prime_tbl(kw.moment_paybook, "h", "agg")
    c400_leap_length = get_c400_constants().c400_leap_length
    cte_tablename = f"spark_{kw.inx_epoch_diff}"

    # WHEN
    generated_update_heard_agg_timenum_sqlstr = get_update_heard_agg_timenum_sqlstr(
        mmtpayy_h_agg_tablename, kw.tran_time
    )

    # THEN
    expected_sqlstr = f"""WITH {cte_tablename} AS (
SELECT 
  {kw.spark_num}
, {kw.otx_time} - {kw.inx_time} AS {kw.inx_epoch_diff}
, IFNULL({kw.c400_number} * {c400_leap_length}, {DEFAULT_EPOCH_LENGTH}) as {kw.epoch_length}
FROM {nabtime_h_agg_tablename}
LEFT JOIN (
    SELECT {kw.moment_rope}, {kw.c400_number} 
    FROM {mmtunit_h_agg_tablename} 
    GROUP BY {kw.moment_rope}, {kw.c400_number}
    ) x_moment ON x_moment.{kw.moment_rope} = {nabtime_h_agg_tablename}.{kw.moment_rope}
)
UPDATE {mmtpayy_h_agg_tablename}
SET {kw.tran_time}_inx = mod({kw.tran_time}_otx + (
    SELECT {kw.inx_epoch_diff}
    FROM {cte_tablename}
    WHERE {cte_tablename}.{kw.spark_num} = {mmtpayy_h_agg_tablename}.{kw.spark_num}
), (SELECT {kw.epoch_length}
    FROM {cte_tablename}
    WHERE {cte_tablename}.{kw.spark_num} = {mmtpayy_h_agg_tablename}.{kw.spark_num}
))
FROM {cte_tablename}
WHERE {mmtpayy_h_agg_tablename}.{kw.spark_num} IN (SELECT {kw.spark_num} FROM {cte_tablename})
;
"""
    assert generated_update_heard_agg_timenum_sqlstr == expected_sqlstr


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario2_PopulatesTableWithSingleRecord(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    s1_otx_time = 44
    s1_inx_time = 55
    x200_offi_time = 200

    create_sound_and_heard_tables(cursor0)
    insert_otx_inx_time(cursor0, spark1, exx.sue, exx.a23, s1_otx_time, s1_inx_time)
    insert_offi_time_otx(cursor0, spark1, exx.sue, exx.a23, x200_offi_time)
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    assert not select_offi_time_inx(cursor0, spark1, exx.a23)[0][3]

    # WHEN
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(
        mmtoffi_h_agg_tablename, kw.offi_time
    )
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    x211_offi_time = x200_offi_time + s1_otx_time - s1_inx_time
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == x211_offi_time


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario3_PopulatesTableWithTwoRecords(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    s1_otx_time = 44
    s1_inx_time = 55
    s1_offi_time_otx = 200
    s3_otx_time = 400
    s3_inx_time = 550
    s3_offi_time_otx = 2000

    create_sound_and_heard_tables(cursor0)
    insert_otx_inx_time(cursor0, spark1, exx.sue, exx.a23, s1_otx_time, s1_inx_time)
    insert_otx_inx_time(cursor0, spark3, exx.sue, exx.a23, s3_otx_time, s3_inx_time)
    insert_offi_time_otx(cursor0, spark1, exx.sue, exx.a23, s1_offi_time_otx)
    insert_offi_time_otx(cursor0, spark3, exx.sue, exx.a23, s3_offi_time_otx)
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] is None
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] is None

    # WHEN
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(
        mmtoffi_h_agg_tablename, kw.offi_time
    )
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s1_inx_epoch_diff = s1_otx_time - s1_inx_time
    s3_inx_epoch_diff = s3_otx_time - s3_inx_time
    s1_offi_time_inx = s1_offi_time_otx + s1_inx_epoch_diff
    s3_offi_time_inx = s3_offi_time_otx + s3_inx_epoch_diff
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == s1_offi_time_inx
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] == s3_offi_time_inx
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == 189
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] == 1850


def test_get_update_heard_agg_timenum_sqlstr_ReturnsObj_Scenario4_PopulatesTableWithTwoRecordsAndDoesModularMath(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    a23_c400_number = 5
    a23_epoch_length = get_c400_constants().c400_leap_length * a23_c400_number
    print(f"{a23_epoch_length=}")
    print(f"{DEFAULT_EPOCH_LENGTH=}")
    s1_otx_time = 44
    s1_inx_time = 55
    s1_offi_time_otx = 200
    s3_otx_time = 400 + a23_epoch_length
    s3_inx_time = 550
    s3_offi_time_otx = 2000

    create_sound_and_heard_tables(cursor0)
    insert_c400_number(cursor0, spark1, exx.sue, exx.a23, a23_c400_number)
    insert_otx_inx_time(cursor0, spark1, exx.sue, exx.a23, s1_otx_time, s1_inx_time)
    insert_otx_inx_time(cursor0, spark3, exx.sue, exx.a23, s3_otx_time, s3_inx_time)
    insert_offi_time_otx(cursor0, spark1, exx.sue, exx.a23, s1_offi_time_otx)
    insert_offi_time_otx(cursor0, spark3, exx.sue, exx.a23, s3_offi_time_otx)
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] is None
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] is None

    # WHEN
    update_mmtoffi_sql = get_update_heard_agg_timenum_sqlstr(
        mmtoffi_h_agg_tablename, kw.offi_time
    )
    cursor0.execute(update_mmtoffi_sql)

    # THEN
    s1_inx_epoch_diff = s1_otx_time - s1_inx_time
    s3_inx_epoch_diff = s3_otx_time - s3_inx_time
    s1_offi_time_inx = s1_offi_time_otx + s1_inx_epoch_diff
    s3_offi_time_inx = (s3_offi_time_otx + s3_inx_epoch_diff) % a23_epoch_length
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == s1_offi_time_inx
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] == s3_offi_time_inx
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == 189
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] == 1850


def test_get_update_heard_agg_timenum_sqlstrs_ReturnsObj():
    # ESTABLISH / WHEN
    gen_update_sqlstrs = get_update_heard_agg_timenum_sqlstrs()

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


def test_update_heard_agg_timenum_columns_UpdatesDB_Scenario0_TwoRecordsAndDoesModularMath(
    cursor0: Cursor,
):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    a23_c400_number = 5
    a23_epoch_length = get_c400_constants().c400_leap_length * a23_c400_number
    print(f"{a23_epoch_length=}")
    print(f"{DEFAULT_EPOCH_LENGTH=}")
    s1_otx_time = 44
    s1_inx_time = 55
    s1_offi_time_otx = 200
    s3_otx_time = 400 + a23_epoch_length
    s3_inx_time = 550
    s3_offi_time_otx = 2000

    create_sound_and_heard_tables(cursor0)
    insert_c400_number(cursor0, spark1, exx.sue, exx.a23, a23_c400_number)
    insert_otx_inx_time(cursor0, spark1, exx.sue, exx.a23, s1_otx_time, s1_inx_time)
    insert_otx_inx_time(cursor0, spark3, exx.sue, exx.a23, s3_otx_time, s3_inx_time)
    insert_offi_time_otx(cursor0, spark1, exx.sue, exx.a23, s1_offi_time_otx)
    insert_offi_time_otx(cursor0, spark3, exx.sue, exx.a23, s3_offi_time_otx)
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] is None
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] is None

    # WHEN
    update_heard_agg_timenum_columns(cursor0)

    # THEN
    s1_inx_epoch_diff = s1_otx_time - s1_inx_time
    s3_inx_epoch_diff = s3_otx_time - s3_inx_time
    s1_offi_time_inx = s1_offi_time_otx + s1_inx_epoch_diff
    s3_offi_time_inx = (s3_offi_time_otx + s3_inx_epoch_diff) % a23_epoch_length
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == s1_offi_time_inx
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] == s3_offi_time_inx
    assert select_offi_time_inx(cursor0, spark1, exx.a23)[0][3] == 189
    assert select_offi_time_inx(cursor0, spark3, exx.a23)[0][3] == 1850
