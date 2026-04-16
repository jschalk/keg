from sqlite3 import Cursor
from src.ch14_moment.moment_main import get_momentunit_from_dict
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename,
    create_sound_and_heard_tables,
)
from src.ch19_etl_steps.obj2db_moment import get_moment_dict_from_heard_tables
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario0_With_momentunit_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    a23_epoch_label = "epoch88"
    a23_c400_number = 3
    a23_yr1_jan1_offset = 7
    a23_monthday_index = 9
    a23_fund_grain = 13
    a23_mana_grain = 17
    a23_respect_grain = 23
    a23_knot = "."

    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentunit_insert_sqlstr = f"""INSERT INTO {mmtunit_h_vld_tablename} (
  moment_rope
, epoch_label
, c400_number
, yr1_jan1_offset
, monthday_index
, fund_grain
, mana_grain
, respect_grain
, knot
)
VALUES (
  '{exx.a23}'
, '{a23_epoch_label}'
, {a23_c400_number}
, {a23_yr1_jan1_offset}
, {a23_monthday_index}
, {a23_fund_grain}
, {a23_mana_grain}
, {a23_respect_grain}
, '{a23_knot}'
)
;"""
    cursor0.execute(momentunit_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    assert a23_dict
    assert a23_dict.get(kw.moment_rope) == exx.a23
    print(f"{a23_dict=}")
    a23_epoch_dict = a23_dict.get(kw.epoch)
    assert a23_epoch_dict.get(kw.epoch_label) == a23_epoch_label
    assert a23_epoch_dict.get(kw.c400_number) == a23_c400_number
    assert a23_epoch_dict.get(kw.yr1_jan1_offset) == a23_yr1_jan1_offset
    assert a23_epoch_dict.get(kw.monthday_index) == a23_monthday_index
    assert a23_dict.get(kw.fund_grain) == a23_fund_grain
    assert a23_dict.get(kw.mana_grain) == a23_mana_grain
    assert a23_dict.get(kw.respect_grain) == a23_respect_grain
    assert a23_dict.get(kw.knot) == a23_knot


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario1_With_momentunit_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    assert a23_dict
    assert a23_dict.get(kw.moment_rope) == exx.a23
    assert "epoch" in set(a23_dict.keys())
    assert a23_dict.get(kw.fund_grain) is None
    assert a23_dict.get(kw.mana_grain) is None
    assert a23_dict.get(kw.respect_grain) is None
    assert a23_dict.get(kw.knot) is None
    assert set(a23_dict.keys()) == {
        kw.moment_rope,
        "offi_times",
        kw.epoch,
        kw.paybook,
        kw.personbudhistorys,
    }


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario2_With_mmtpayy_Attrs(
    cursor0: Cursor,
):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    tp55 = 55
    bob_sue_tp55_amount = 444
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentpay_h_vld_tablename = create_prime_tablename("mmtpayy", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {momentpay_h_vld_tablename} (moment_rope, person_name, contact_name, tran_time, amount)
VALUES ('{exx.a23}', '{exx.bob}', '{exx.sue}', {tp55}, {bob_sue_tp55_amount})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_paybook_dict = a23_dict.get("paybook")
    assert a23_paybook_dict
    assert a23_paybook_dict.get(kw.moment_rope) == exx.a23
    a23_tranunits_dict = a23_paybook_dict.get("tranunits")
    assert a23_tranunits_dict
    a23_trans_bob_dict = a23_tranunits_dict.get(exx.bob)
    assert a23_trans_bob_dict
    a23_trans_bob_sue_dict = a23_trans_bob_dict.get(exx.sue)
    assert a23_trans_bob_sue_dict
    assert a23_trans_bob_sue_dict.get(tp55) == bob_sue_tp55_amount


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario3_With_mmtpayy_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    a45_str = "amy45"
    tp55 = 55
    a23_bob_sue_tp55_amount = 444
    a45_bob_sue_tp55_amount = 800
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentpay_h_vld_tablename = create_prime_tablename("mmtpayy", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {momentpay_h_vld_tablename} (moment_rope, person_name, contact_name, tran_time, amount)
VALUES
  ('{exx.a23}', '{exx.bob}', '{exx.sue}', {tp55}, {a23_bob_sue_tp55_amount})
, ('{a45_str}', '{exx.bob}', '{exx.sue}', {tp55}, {a45_bob_sue_tp55_amount})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_paybook_dict = a23_dict.get("paybook")
    assert a23_paybook_dict
    assert a23_paybook_dict.get(kw.moment_rope) == exx.a23
    a23_tranunits_dict = a23_paybook_dict.get("tranunits")
    assert a23_tranunits_dict
    a23_trans_bob_dict = a23_tranunits_dict.get(exx.bob)
    assert a23_trans_bob_dict
    a23_trans_bob_sue_dict = a23_trans_bob_dict.get(exx.sue)
    assert a23_trans_bob_sue_dict
    assert a23_trans_bob_sue_dict == {tp55: a23_bob_sue_tp55_amount}


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario4_With_momentbud_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    tp55 = 55
    bob_tp55_quota = 444
    bob_tp55_celldepth = 3
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentbud_h_vld_tablename = create_prime_tablename("mmtbudd", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {momentbud_h_vld_tablename} (moment_rope, person_name, bud_time, knot, quota, celldepth)
VALUES ('{exx.a23}', '{exx.bob}', {tp55}, '{exx.dash}', {bob_tp55_quota}, {bob_tp55_celldepth})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_personbudhistory_dict = a23_dict.get("personbudhistorys")
    print(f"{a23_personbudhistory_dict=}")
    assert a23_personbudhistory_dict
    a23_personbudhistory_bob_dict = a23_personbudhistory_dict.get(exx.bob)
    assert a23_personbudhistory_bob_dict
    a23_bob_buds_dict = a23_personbudhistory_bob_dict.get("buds")
    assert a23_bob_buds_dict
    a23_personbudhistory_bob_tp55_dict = a23_bob_buds_dict.get(tp55)
    assert a23_personbudhistory_bob_tp55_dict
    expected_bob_tp55_dict = {
        kw.bud_time: 55,
        kw.quota: bob_tp55_quota,
        kw.celldepth: bob_tp55_celldepth,
    }
    assert a23_personbudhistory_bob_tp55_dict == expected_bob_tp55_dict


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario5_With_mmthour_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    hour3_min = 300
    hour4_min = 400
    hour3_label = "3xm"
    hour4_label = "4xm"
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmthour_h_vld_tablename = create_prime_tablename("mmthour", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmthour_h_vld_tablename} (moment_rope, cumulative_minute, hour_label)
VALUES
  ('{exx.a23}', {hour3_min}, '{hour3_label}')
, ('{exx.a23}', {hour4_min}, '{hour4_label}')
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_epoch_dict = a23_dict.get("epoch")
    print(f"{a23_epoch_dict=}")
    assert a23_epoch_dict
    a23_hours_config_dict = a23_epoch_dict.get("hours_config")
    print(f"{a23_hours_config_dict=}")
    assert a23_hours_config_dict == [[hour3_label, hour3_min], [hour4_label, hour4_min]]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario6_With_mmtmont_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    day111_min = 111
    day222_min = 222
    month111_label = "jan111"
    month222_label = "feb222"
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmtmont_h_vld_tablename = create_prime_tablename("mmtmont", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmtmont_h_vld_tablename} (moment_rope, cumulative_day, month_label)
VALUES
  ('{exx.a23}', {day111_min}, '{month111_label}')
, ('{exx.a23}', {day222_min}, '{month222_label}')
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_epoch_dict = a23_dict.get("epoch")
    assert a23_epoch_dict
    a23_months_config_dict = a23_epoch_dict.get("months_config")
    assert a23_months_config_dict == [
        [month111_label, day111_min],
        [month222_label, day222_min],
    ]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario7_With_mmtweek_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    ana_order = 1
    bee_order = 2
    ana_label = "ana_weekday"
    bee_label = "bee_weekday"
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmtweek_h_vld_tablename = create_prime_tablename("mmtweek", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmtweek_h_vld_tablename} (moment_rope, weekday_order, weekday_label)
VALUES
  ('{exx.a23}', {ana_order}, '{ana_label}')
, ('{exx.a23}', {bee_order}, '{bee_label}')
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_epoch_dict = a23_dict.get("epoch")
    assert a23_epoch_dict
    a23_weekdays_config_dict = a23_epoch_dict.get(kw.weekdays_config)
    assert a23_weekdays_config_dict == [ana_label, bee_label]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario8_With_mmtoffi_Attrs(
    cursor0: Cursor,
):
    # ESTABLISH
    offi_time5 = 5
    offi_time7 = 7
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmtoffi_h_vld_tablename = create_prime_tablename("mmtoffi", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmtoffi_h_vld_tablename} (moment_rope, offi_time)
VALUES
  ('{exx.a23}', {offi_time5})
, ('{exx.a23}', {offi_time7})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)

    # WHEN
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # THEN
    a23_offi_times_config_dict = a23_dict.get("offi_times")
    print(f"{a23_offi_times_config_dict=}")
    assert a23_offi_times_config_dict == [offi_time5, offi_time7]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario9_IsFormatted_momentunit(
    cursor0: Cursor,
):
    # ESTABLISH
    a23_epoch_label = "epoch88"
    a23_c400_number = 3
    a23_yr1_jan1_offset = 7
    a23_monthday_index = 9
    a23_fund_grain = 13
    a23_mana_grain = 17
    a23_respect_grain = 23
    a23_knot = "."

    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentunit_insert_sqlstr = f"""INSERT INTO {mmtunit_h_vld_tablename} (
  moment_rope
, epoch_label
, c400_number
, yr1_jan1_offset
, monthday_index
, fund_grain
, mana_grain
, respect_grain
, knot
)
VALUES (
  '{exx.a23}'
, '{a23_epoch_label}'
, {a23_c400_number}
, {a23_yr1_jan1_offset}
, {a23_monthday_index}
, {a23_fund_grain}
, {a23_mana_grain}
, {a23_respect_grain}
, '{a23_knot}'
)
;"""
    cursor0.execute(momentunit_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    assert a23_momentunit.moment_rope == exx.a23
    assert a23_momentunit.epoch.epoch_label == a23_epoch_label
    assert a23_momentunit.epoch.c400_number == a23_c400_number
    assert a23_momentunit.epoch.yr1_jan1_offset == a23_yr1_jan1_offset
    assert a23_momentunit.epoch.monthday_index == a23_monthday_index
    assert a23_momentunit.fund_grain == a23_fund_grain
    assert a23_momentunit.mana_grain == a23_mana_grain
    assert a23_momentunit.respect_grain == a23_respect_grain
    assert a23_momentunit.knot == a23_knot


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario10_IsFormatted_mmtpayy(
    cursor0: Cursor,
):
    # ESTABLISH
    tp55 = 55
    bob_sue_tp55_amount = 444
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentpay_h_vld_tablename = create_prime_tablename("mmtpayy", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {momentpay_h_vld_tablename} (moment_rope, person_name, contact_name, tran_time, amount)
VALUES ('{exx.a23}', '{exx.bob}', '{exx.sue}', {tp55}, {bob_sue_tp55_amount})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    assert a23_momentunit.moment_rope == exx.a23
    assert a23_momentunit.paybook.tranunits.get(exx.bob)
    bob_tranunit = a23_momentunit.paybook.tranunits.get(exx.bob)
    assert bob_tranunit == {exx.sue: {tp55: bob_sue_tp55_amount}}


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario11_IsFormatted_momentbud(
    cursor0: Cursor,
):
    # ESTABLISH
    tp55 = 55
    bob_tp55_quota = 444
    bob_tp55_celldepth = 3
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    momentbud_h_vld_tablename = create_prime_tablename("mmtbudd", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {momentbud_h_vld_tablename} (moment_rope, person_name, bud_time, quota, celldepth)
VALUES ('{exx.a23}', '{exx.bob}', {tp55}, {bob_tp55_quota}, {bob_tp55_celldepth})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    a23_bob_personbudhistory = a23_momentunit.get_personbudhistory(exx.bob)
    print(f"{a23_bob_personbudhistory=}")
    assert a23_bob_personbudhistory
    a23_bob_55_bud = a23_bob_personbudhistory.get_bud(tp55)
    assert a23_bob_55_bud.bud_time == tp55
    assert a23_bob_55_bud.quota == bob_tp55_quota
    assert a23_bob_55_bud.celldepth == bob_tp55_celldepth


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario12_mmthour(
    cursor0: Cursor,
):
    # ESTABLISH
    hour3_min = 300
    hour4_min = 400
    hour3_label = "3xm"
    hour4_label = "4xm"
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmthour_h_vld_tablename = create_prime_tablename("mmthour", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmthour_h_vld_tablename} (moment_rope, cumulative_minute, hour_label)
VALUES
  ('{exx.a23}', {hour3_min}, '{hour3_label}')
, ('{exx.a23}', {hour4_min}, '{hour4_label}')
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    a23_momentunit.epoch.hours_config == [
        [hour3_label, hour3_min],
        [hour4_label, hour4_min],
    ]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario13_mmtmont(
    cursor0: Cursor,
):
    # ESTABLISH
    day111_min = 111
    day222_min = 222
    month111_label = "jan111"
    month222_label = "feb222"
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmtmont_h_vld_tablename = create_prime_tablename("mmtmont", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmtmont_h_vld_tablename} (moment_rope, cumulative_day, month_label)
VALUES
  ('{exx.a23}', {day111_min}, '{month111_label}')
, ('{exx.a23}', {day222_min}, '{month222_label}')
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    assert a23_momentunit.epoch.months_config == [
        [month111_label, day111_min],
        [month222_label, day222_min],
    ]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario14_mmtweek(
    cursor0: Cursor,
):
    # ESTABLISH
    ana_order = 1
    bee_order = 2
    ana_label = "ana_weekday"
    bee_label = "bee_weekday"
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmtweek_h_vld_tablename = create_prime_tablename("mmtweek", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmtweek_h_vld_tablename} (moment_rope, weekday_order, weekday_label)
VALUES
  ('{exx.a23}', {ana_order}, '{ana_label}')
, ('{exx.a23}', {bee_order}, '{bee_label}')
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    assert a23_momentunit.epoch.weekdays_config == [ana_label, bee_label]


def test_get_moment_dict_from_heard_tables_ReturnsObj_Scenario15_mmtoffi(
    cursor0: Cursor,
):
    # ESTABLISH
    offi_time5 = 5
    offi_time7 = 7
    create_sound_and_heard_tables(cursor0)
    mmtunit_h_vld_tablename = create_prime_tablename("mmtunit", kw.h_vld)
    mmtoffi_h_vld_tablename = create_prime_tablename("mmtoffi", kw.h_vld)
    momentunit_insert_sqlstr = (
        f"INSERT INTO {mmtunit_h_vld_tablename} (moment_rope) VALUES ('{exx.a23}');"
    )
    cursor0.execute(momentunit_insert_sqlstr)
    mmtpayy_insert_sqlstr = f"""INSERT INTO {mmtoffi_h_vld_tablename} (moment_rope, offi_time)
VALUES
  ('{exx.a23}', {offi_time5})
, ('{exx.a23}', {offi_time7})
;
"""
    cursor0.execute(mmtpayy_insert_sqlstr)
    a23_dict = get_moment_dict_from_heard_tables(cursor0, exx.a23)

    # WHEN
    a23_momentunit = get_momentunit_from_dict(a23_dict)

    # THEN
    assert a23_momentunit.offi_times == {offi_time5, offi_time7}
