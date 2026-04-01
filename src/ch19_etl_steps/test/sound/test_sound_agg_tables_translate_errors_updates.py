from sqlite3 import Cursor
from src.ch18_etl_config.etl_sqlstr import (
    CREATE_MMTMONT_SOUND_AGG_SQLSTR,
    CREATE_PRNCONT_PUT_SOUND_AGG_SQLSTR,
    CREATE_TRLCORE_SOUND_VLD_SQLSTR,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
)
from src.ch19_etl_steps.etl_main import set_moment_person_sound_agg_knot_errors
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_create_knot_exists_in_name_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    colon = ":"
    bob_str = f"{colon}Bob"
    comma = ","
    ukx = "Unknown"
    spark1 = 1

    cursor0.execute(CREATE_PRNCONT_PUT_SOUND_AGG_SQLSTR)
    prncont_dimen = kw.person_contactunit
    prncont_s_agg_put = create_prime_tablename(prncont_dimen, "s_agg", "put")
    insert_prncont_sqlstr = f"""INSERT INTO {prncont_s_agg_put} (
  {kw.spark_num}, {kw.face_name}, {kw.moment_rope}, {kw.person_name}, {kw.contact_name})
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{exx.yao}')
, ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{bob_str}')
;
"""
    cursor0.execute(insert_prncont_sqlstr)
    cursor0.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", kw.s_vld)
    insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
  {kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{exx.sue}', '{colon}', '{colon}', '{ukx}')
, ('{exx.yao}', '{comma}', '{comma}', '{ukx}')
;
"""
    cursor0.execute(insert_trlcore_sqlstr)
    error_count_sqlstr = (
        f"SELECT COUNT(*) FROM {prncont_s_agg_put} WHERE {kw.error_message} IS NOT NULL"
    )
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 0

    # WHEN
    sqlstr = create_knot_exists_in_name_error_update_sqlstr(
        prncont_s_agg_put, kw.contact_name
    )
    print(f"{sqlstr=}")
    cursor0.execute(sqlstr)

    # THEN
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 1
    select_core_raw_sqlstr = f"SELECT * FROM {prncont_s_agg_put}"
    cursor0.execute(select_core_raw_sqlstr)
    name_knot_str = f"Knot cannot exist in NameTerm column {kw.contact_name}"
    assert cursor0.fetchall() == [
        (spark1, exx.sue, exx.a23, exx.yao, exx.yao, None, None, None, None),
        (spark1, exx.sue, exx.a23, exx.yao, bob_str, None, None, None, name_knot_str),
    ]


def test_create_knot_exists_in_label_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    colon = ":"
    bad_june_str = f"{colon}{exx.June}"
    comma = ","
    ukx = "Unknown"
    spark1 = 1

    cursor0.execute(CREATE_MMTMONT_SOUND_AGG_SQLSTR)
    mmtmont_s_agg_put = create_prime_tablename(kw.mmtmont, "s_agg")
    insert_mmtmont_sqlstr = f"""INSERT INTO {mmtmont_s_agg_put} (
  {kw.spark_num}, {kw.face_name}, {kw.moment_rope}, {kw.month_label}, {kw.cumulative_day})
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.June}', 101)
, ({spark1}, '{exx.sue}', '{exx.a23}', '{bad_june_str}', 101)
;
"""
    cursor0.execute(insert_mmtmont_sqlstr)
    cursor0.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
    trlcore_s_vld_tablename = create_prime_tablename(kw.trlcore, kw.s_vld)
    insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
  {kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{exx.sue}', '{colon}', '{colon}', '{ukx}')
, ('{exx.yao}', '{comma}', '{comma}', '{ukx}')
;
"""
    cursor0.execute(insert_trlcore_sqlstr)
    error_count_sqlstr = (
        f"SELECT COUNT(*) FROM {mmtmont_s_agg_put} WHERE {kw.error_message} IS NOT NULL"
    )
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 0

    # WHEN
    sqlstr = create_knot_exists_in_label_error_update_sqlstr(
        mmtmont_s_agg_put, kw.month_label
    )
    print(sqlstr)
    cursor0.execute(sqlstr)

    # THEN
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 1
    select_core_raw_sqlstr = f"SELECT * FROM {mmtmont_s_agg_put}"
    cursor0.execute(select_core_raw_sqlstr)
    label_knot_str = f"Knot cannot exist in LabelTerm column {kw.month_label}"
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (spark1, exx.sue, exx.a23, 101, exx.June, None, None),
        (spark1, exx.sue, exx.a23, 101, bad_june_str, None, label_knot_str),
    ]


def test_set_moment_person_sound_agg_knot_errors_PopulatesTable_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    colon = ":"
    bob_str = f"{colon}Bob"
    a45_str = f"{colon}amy45"
    comma = ","
    ukx = "Unknown"
    spark1 = 1

    cursor0.execute(CREATE_PRNCONT_PUT_SOUND_AGG_SQLSTR)
    prncont_dimen = kw.person_contactunit
    prncont_s_agg_put = create_prime_tablename(prncont_dimen, "s_agg", "put")
    insert_prncont_sqlstr = f"""INSERT INTO {prncont_s_agg_put} (
  {kw.spark_num}, {kw.face_name}, {kw.moment_rope}, {kw.person_name}, {kw.contact_name})
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{exx.yao}')
, ({spark1}, '{exx.sue}', '{exx.a23}', '{exx.yao}', '{bob_str}')
, ({spark1}, '{exx.sue}', '{a45_str}', '{exx.yao}', '{exx.yao}')
;
"""
    cursor0.execute(insert_prncont_sqlstr)
    cursor0.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", kw.s_vld)
    insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
  {kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{exx.sue}', '{colon}', '{colon}', '{ukx}')
, ('{exx.yao}', '{comma}', '{comma}', '{ukx}')
;
"""
    cursor0.execute(insert_trlcore_sqlstr)
    error_count_sqlstr = (
        f"SELECT COUNT(*) FROM {prncont_s_agg_put} WHERE {kw.error_message} IS NOT NULL"
    )
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 0

    # WHEN
    set_moment_person_sound_agg_knot_errors(cursor0)

    # THEN
    assert cursor0.execute(error_count_sqlstr).fetchone()[0] == 1
    select_core_raw_sqlstr = f"SELECT * FROM {prncont_s_agg_put} ORDER BY {kw.moment_rope}, {kw.person_name}, {kw.contact_name}"
    cursor0.execute(select_core_raw_sqlstr)
    name_knot_str = f"Knot cannot exist in NameTerm column {kw.contact_name}"
    rope_knot_str = f"Trailing knot must exist in RopeTerm column {kw.moment_rope}"
    rows = cursor0.fetchall()
    print(f"{rows=}")
    assert rows == [
        (spark1, exx.sue, a45_str, exx.yao, exx.yao, None, None, None, None),
        (spark1, exx.sue, exx.a23, exx.yao, bob_str, None, None, None, name_knot_str),
        (spark1, exx.sue, exx.a23, exx.yao, exx.yao, None, None, None, None),
    ]
