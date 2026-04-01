from sqlite3 import Cursor
from src.ch13_time.epoch_main import DEFAULT_EPOCH_LENGTH, get_c400_constants
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_etl_config.etl_sqlstr import (
    create_sound_and_heard_tables,
    update_heard_agg_timenum_columns,
)
from src.ch19_etl_steps.test.heard.test_heard_agg__update_casenum_pchapx import (
    pchapx_insert_nabtime,
    pchapx_insert_prncase,
    pchapx_insert_prnplan,
    pchapx_select_prncase,
)
from src.ch19_etl_steps.test.heard.test_heard_agg__update_factnum_pfhapx import (
    pfhapx_insert_nabtime,
    pfhapx_insert_prnfact,
    pfhapx_insert_prnplan,
    pfhapx_select_prnfact,
)
from src.ch19_etl_steps.test.heard.test_heard_agg__update_moment_time_mxhap0 import (
    mxhap0_insert_mmtoffi,
    mxhap0_insert_mmtunit,
    mxhap0_insert_nabtime,
    mxhap0_select_mmtoffi,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_update_heard_agg_timenum_columns_SQLTEST_Scenario0_TwoRecordsAndDoesModularMath(
    cursor0: Cursor,
):
    # ESTABLISH
    create_sound_and_heard_tables(cursor0)
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
    update_heard_agg_timenum_columns(cursor0)

    # THEN
    s1_inx_epoch_diff = s1_otx_time - s1_inx_time
    s3_inx_epoch_diff = s3_otx_time - s3_inx_time
    s1_offi_time_inx = s1_offi_time_otx + s1_inx_epoch_diff
    s3_offi_time_inx = (s3_offi_time_otx + s3_inx_epoch_diff) % a23_epoch_length
    assert mxhap0_select_mmtoffi(cursor0, True) == [
        (1, exx.a23, s1_offi_time_otx, s1_offi_time_inx),
        (3, exx.a23, s3_offi_time_otx, s3_offi_time_inx),
    ]
    assert mxhap0_select_mmtoffi(cursor0) == [
        (1, exx.a23, 200, 189),
        (3, exx.a23, 2000, 1850),
    ]


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
