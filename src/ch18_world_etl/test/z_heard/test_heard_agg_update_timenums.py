from sqlite3 import Cursor
from src.ch13_time.epoch_main import DEFAULT_EPOCH_LENGTH, get_c400_constants
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    update_heard_agg_timenum_columns,
)
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ch18_world_etl.test._util.ch18_examples import (
    insert_mmtoffi_special_offi_time_otx as insert_offi_time_otx,
    insert_mmtunit_special_c400_number as insert_c400_number,
    insert_nabtime_h_agg_otx_inx_time as insert_otx_inx_time,
    select_mmtoffi_special_offi_time_inx as select_offi_time_inx,
)
from src.ch18_world_etl.test.z_heard.test_heard_agg_update_casenum_pchapx import (
    pchapx_insert_nabtime,
    pchapx_insert_prncase,
    pchapx_insert_prnplan,
    pchapx_select_prncase,
)
from src.ch18_world_etl.test.z_heard.test_heard_agg_update_factnum_pfhapx import (
    pfhapx_insert_nabtime,
    pfhapx_insert_prnfact,
    pfhapx_insert_prnplan,
    pfhapx_select_prnfact,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


# TODO convert to bubba testing method once mxhap0 tests are complete
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


def test_update_heard_agg_timenum_columns_SQLTEST_Scenario1_CaseUnit_TimeNums(
    cursor0,
):
    # ESTABLISH modeled after # def test_update_caseunit_heard_agg_timenum_columns_SQLTEST_Scenario0_NoWarp_range

    create_sound_and_heard_tables(cursor0)
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
    update_heard_agg_timenum_columns(cursor0)

    # THEN
    inx_epoch_diff = time_otx - time_inx
    reason_lower_inx = reason_lower_otx + inx_epoch_diff
    reason_upper_inx = reason_upper_otx + inx_epoch_diff
    assert pchapx_select_prncase(cursor0, True) == [
        (reason_lower_otx, reason_lower_inx, reason_upper_otx, reason_upper_inx)
    ]
    assert pchapx_select_prncase(cursor0) == [(600, 700, 690, 790)]


def test_update_heard_agg_timenum_columns_SQLTEST_Scenario2_FactUnit_TimeNums(
    cursor0,
):
    # ESTABLISH modeled after # def test_update_heard_agg_timenum_columns_SQLTEST_Scenario0_NoWarp_range

    create_sound_and_heard_tables(cursor0)
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
    update_heard_agg_timenum_columns(cursor0)

    # THEN
    inx_epoch_diff = time_otx - time_inx
    fact_lower_inx = fact_lower_otx + inx_epoch_diff
    fact_upper_inx = fact_upper_otx + inx_epoch_diff
    assert pfhapx_select_prnfact(cursor0, True) == [
        (fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx)
    ]
    assert pfhapx_select_prnfact(cursor0) == [(7777, 7877, 8000, 8100)]
