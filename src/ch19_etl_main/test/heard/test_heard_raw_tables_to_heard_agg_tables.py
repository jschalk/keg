from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
from src.ch00_py.dict_toolbox import get_empty_set_if_None
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch17_idea.idea_config import get_default_sorted_list, get_idea_config_dict
from src.ch18_etl_config.etl_config import (
    etl_idea_category_config_dict,
    get_dimen_abbv7,
    get_etl_category_stages_dict,
    get_prime_columns,
    remove_inx_columns,
    remove_otx_columns,
    remove_staging_columns,
)
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_insert_heard_agg_sqlstrs,
)
from src.ch19_etl_main.etl_main import etl_heard_raw_tables_to_heard_agg_tables
from src.ch19_etl_main.test.heard.test_heard_agg__update_factnum_pfhapx import (
    pfhapx_insert_nabtime,
    pfhapx_insert_prnfact,
    pfhapx_insert_prnplan,
    pfhapx_select_prnfact,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def check_insert_sqlstr_exists(
    dimen: str,
    insert_heard_agg_sqlstrs: dict,
    stage_dict: dict,
    put_del: str = None,
):
    raw_tablename = prime_tbl(dimen, kw.h_raw, put_del)
    agg_tablename = prime_tbl(dimen, kw.h_agg, put_del)

    print(f"{raw_tablename=} {agg_tablename=}")
    # print(f"{stage_dict=}")
    config_dict = etl_idea_category_config_dict()
    raw_keylist = [kw.h_raw, put_del] if put_del else [kw.h_raw]
    agg_keylist = [kw.h_agg, put_del] if put_del else [kw.h_agg]
    p_agg_columns = get_prime_columns(dimen, agg_keylist, config_dict)
    p_raw_columns = get_prime_columns(dimen, raw_keylist, config_dict)
    if stage_dict.get("exclude_otx_from_insert"):
        p_raw_columns = remove_otx_columns(p_raw_columns)
        p_agg_columns = remove_inx_columns(p_agg_columns)
        p_agg_columns = remove_staging_columns(p_agg_columns)
    exclude_from_insert = stage_dict.get("exclude_from_insert")
    exclude_from_insert = set(get_empty_set_if_None(exclude_from_insert))
    p_raw_columns -= exclude_from_insert
    p_raw_columns = get_default_sorted_list(p_raw_columns)
    p_agg_columns = get_default_sorted_list(p_agg_columns)

    raw_columns_str = ", ".join(p_raw_columns)
    agg_columns_str = ", ".join(p_agg_columns)
    expected_table2table_agg_insert_sqlstr = f"""
INSERT INTO {agg_tablename} ({agg_columns_str})
SELECT {raw_columns_str}
FROM {raw_tablename}
GROUP BY {raw_columns_str}
"""
    dimen_abbv7 = get_dimen_abbv7(dimen)
    if put_del:
        variable_name = (
            f"{dimen_abbv7.upper()}_HEARD_AGG_{put_del.upper()}_INSERT_SQLSTR"
        )
    else:
        variable_name = f"{dimen_abbv7.upper()}_HEARD_AGG_INSERT_SQLSTR"

    # print(f'"{agg_tablename}": {variable_name},')
    # print(f'{variable_name} = """{expected_table2table_agg_insert_sqlstr}"""')
    gen_sqlstr = insert_heard_agg_sqlstrs.get(agg_tablename)
    # print(f"{expected_table2table_agg_insert_sqlstr=}")
    # print(f"                            {gen_sqlstr=}")
    assert gen_sqlstr == expected_table2table_agg_insert_sqlstr


def test_get_insert_heard_agg_sqlstrs_ReturnsObj(cursor0: Cursor):
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    insert_heard_agg_sqlstrs = get_insert_heard_agg_sqlstrs()

    # THEN
    agg_sqlstrs = insert_heard_agg_sqlstrs
    etl_idea_category_config = etl_idea_category_config_dict()
    create_sound_and_heard_tables(cursor0)
    for idea_category, category_dict in etl_idea_category_config.items():
        category_config = get_idea_config_dict(idea_category)
        if agg_dict := category_dict.get("stages").get(kw.h_agg):
            # print(f"{idea_category=}")
            if agg_dict.get("del") is None:
                for dimen in sorted(category_config.keys()):
                    check_insert_sqlstr_exists(dimen, agg_sqlstrs, agg_dict)
            if agg_dict.get("del") is not None:
                del_dict = agg_dict.get("del")
                for dimen in sorted(category_config.keys()):
                    check_insert_sqlstr_exists(dimen, agg_sqlstrs, del_dict, "del")
            if agg_dict.get("put") is not None:
                put_dict = agg_dict.get("put")
                for dimen in sorted(category_config.keys()):
                    check_insert_sqlstr_exists(dimen, agg_sqlstrs, put_dict, "put")
    # gen_heard_agg_tablenames = set(insert_heard_agg_sqlstrs.keys())
    # assert gen_heard_agg_tablenames.issubset()


def test_get_insert_heard_agg_sqlstrs_ReturnsObj_PopulatesTable_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    yao_inx = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    create_sound_and_heard_tables(cursor0)
    prnptnr_h_raw_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_raw, "put")
    print(f"{get_table_columns(cursor0, prnptnr_h_raw_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prnptnr_h_raw_put_tablename} (
  {kw.spark_num}
, {kw.face_name}_inx
, {kw.moment_rope}_inx
, {kw.person_name}_inx
, {kw.partner_name}_inx
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
)
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
    cursor0.execute(insert_into_clause)
    assert get_row_count(cursor0, prnptnr_h_raw_put_tablename) == 5
    prnptnr_h_agg_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_agg, "put")
    assert get_row_count(cursor0, prnptnr_h_agg_put_tablename) == 0

    # WHEN
    sqlstr = get_insert_heard_agg_sqlstrs().get(prnptnr_h_agg_put_tablename)
    print(sqlstr)
    cursor0.execute(sqlstr)

    # THEN
    assert get_row_count(cursor0, prnptnr_h_agg_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
FROM {prnptnr_h_agg_put_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (spark1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
        (spark2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (spark5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (spark7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
    ]


def test_etl_heard_raw_tables_to_heard_agg_tables_PopulatesTable_Scenario0(
    cursor0: Cursor,
):
    # ESTABLISH
    yao_inx = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    create_sound_and_heard_tables(cursor0)
    prnptnr_h_raw_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_raw, "put")
    print(f"{get_table_columns(cursor0, prnptnr_h_raw_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prnptnr_h_raw_put_tablename} (
  {kw.spark_num}
, {kw.face_name}_inx
, {kw.moment_rope}_inx
, {kw.person_name}_inx
, {kw.partner_name}_inx
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
)
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
    cursor0.execute(insert_into_clause)
    assert get_row_count(cursor0, prnptnr_h_raw_put_tablename) == 5
    prnptnr_h_agg_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_agg, "put")
    assert get_row_count(cursor0, prnptnr_h_agg_put_tablename) == 0

    # WHEN
    etl_heard_raw_tables_to_heard_agg_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, prnptnr_h_agg_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
FROM {prnptnr_h_agg_put_tablename}
"""
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [
        (spark1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
        (spark2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (spark5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
        (spark7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
    ]


def test_etl_heard_raw_tables_to_heard_agg_tables_SQLTEST_Scenario1_FactUnit_TimeNums(
    cursor0,
):
    # ESTABLISH modeled after # def test_update_heard_agg_timenum_columns_SQLTEST_Scenario2_FactUnit_TimeNums

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
    etl_heard_raw_tables_to_heard_agg_tables(cursor0)

    # THEN
    inx_epoch_diff = time_otx - time_inx
    fact_lower_inx = fact_lower_otx + inx_epoch_diff
    fact_upper_inx = fact_upper_otx + inx_epoch_diff
    assert pfhapx_select_prnfact(cursor0, True) == [
        (fact_lower_otx, fact_lower_inx, fact_upper_otx, fact_upper_inx)
    ]
    assert pfhapx_select_prnfact(cursor0) == [(7777, 7877, 8000, 8100)]
