from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import get_default_sorted_list, get_idea_config_dict
from src.ch18_etl_config.etl_config import get_dimen_abbv7
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_insert_heard_vld_sqlstrs,
)
from src.ch19_etl_main.etl_main import etl_heard_agg_tables_to_heard_vld_tables
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_get_insert_heard_vld_sqlstrs_ReturnsObj_CheckMomentDimen(cursor0: Cursor):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    insert_heard_vld_sqlstrs = get_insert_heard_vld_sqlstrs()

    # THEN
    gen_heard_vld_tablenames = set(insert_heard_vld_sqlstrs.keys())
    moment_dimes = get_moment_dimens()
    moment_vld_tablenames = {prime_tbl(dimen, kw.h_vld) for dimen in moment_dimes}
    # print(f"{gen_heard_vld_tablenames=}")
    # print(f"     {get_moment_dimens()=}")
    assert moment_vld_tablenames.issubset(gen_heard_vld_tablenames)
    idea_config = get_idea_config_dict({kw.moment})
    create_sound_and_heard_tables(cursor0)

    for x_dimen in idea_config:
        # print(f"{x_dimen} checking...")
        agg_tablename = prime_tbl(x_dimen, kw.h_agg)
        vld_tablename = prime_tbl(x_dimen, kw.h_vld)
        agg_columns = get_table_columns(cursor0, agg_tablename)
        vld_columns = get_table_columns(cursor0, vld_tablename)
        agg_columns = {agg_col for agg_col in agg_columns if agg_col[-3:] != "otx"}
        agg_columns.remove(kw.face_name)
        agg_columns.remove(kw.spark_num)
        agg_columns = get_default_sorted_list(agg_columns)

        agg_columns_str = ", ".join(agg_columns)
        vld_columns_str = ", ".join(vld_columns)
        # print(f"{agg_columns_str=}")
        # print(f"{vld_columns_str=}")
        expected_table2table_vld_insert_sqlstr = f"""
INSERT INTO {vld_tablename} ({vld_columns_str})
SELECT {agg_columns_str}
FROM {agg_tablename}
GROUP BY {agg_columns_str}
"""
        dimen_abbv7 = get_dimen_abbv7(x_dimen)
        # print(f'"{x_dimen}": {dimen_abbv7.upper()}_HEARD_VLD_INSERT_SQLSTR,')
        print(
            f'{dimen_abbv7.upper()}_HEARD_VLD_INSERT_SQLSTR = """{expected_table2table_vld_insert_sqlstr}"""'
        )
        gen_sqlstr = insert_heard_vld_sqlstrs.get(vld_tablename)
        assert gen_sqlstr == expected_table2table_vld_insert_sqlstr


def remove_otx_and_excluded_cols(cols: set) -> set:
    excluded_cols = {
        "context_plan_close",
        "context_plan_denom",
        "context_plan_morph",
        "inx_epoch_diff",
    }
    return {col for col in cols if col[-3:] != "otx" and col not in excluded_cols}


def test_get_insert_heard_vld_sqlstrs_ReturnsObj_PersonDimensRequired(cursor0: Cursor):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    person_dimens_config = get_idea_config_dict({kw.person})

    # WHEN
    insert_heard_vld_sqlstrs = get_insert_heard_vld_sqlstrs()

    # THEN
    create_sound_and_heard_tables(cursor0)

    for person_dimen in person_dimens_config:
        # print(f"{person_dimen=}")
        h_agg_put_tablename = prime_tbl(person_dimen, kw.h_agg, "put")
        h_agg_del_tablename = prime_tbl(person_dimen, kw.h_agg, "del")
        h_vld_put_tablename = prime_tbl(person_dimen, kw.h_vld, "put")
        h_vld_del_tablename = prime_tbl(person_dimen, kw.h_vld, "del")
        h_agg_put_cols = get_table_columns(cursor0, h_agg_put_tablename)
        h_agg_del_cols = get_table_columns(cursor0, h_agg_del_tablename)
        h_vld_put_cols = get_table_columns(cursor0, h_vld_put_tablename)
        h_vld_del_cols = get_table_columns(cursor0, h_vld_del_tablename)
        h_agg_put_cols = remove_otx_and_excluded_cols(h_agg_put_cols)
        h_agg_del_cols = remove_otx_and_excluded_cols(h_agg_del_cols)
        h_agg_put_cols = get_default_sorted_list(h_agg_put_cols)
        h_agg_del_cols = get_default_sorted_list(h_agg_del_cols)
        h_agg_put_columns_str = ", ".join(h_agg_put_cols)
        h_agg_put_columns_str = ", ".join(h_agg_put_cols)
        h_agg_del_columns_str = ", ".join(h_agg_del_cols)
        h_vld_put_columns_str = ", ".join(h_vld_put_cols)
        h_vld_del_columns_str = ", ".join(h_vld_del_cols)
        expected_vld_put_insert_sqlstr = f"""
INSERT INTO {h_vld_put_tablename} ({h_vld_put_columns_str})
SELECT {h_agg_put_columns_str}
FROM {h_agg_put_tablename}
GROUP BY {h_agg_put_columns_str}
"""
        expected_vld_del_insert_sqlstr = f"""
INSERT INTO {h_vld_del_tablename} ({h_vld_del_columns_str})
SELECT {h_agg_del_columns_str}
FROM {h_agg_del_tablename}
GROUP BY {h_agg_del_columns_str}
"""
        abbv7 = get_dimen_abbv7(person_dimen)
        put_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_VLD_PUT_SQLSTR"
        del_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_VLD_DEL_SQLSTR"
        print(f'{put_sqlstr_ref}= """{expected_vld_put_insert_sqlstr}"""')
        print(f'{del_sqlstr_ref}= """{expected_vld_del_insert_sqlstr}"""')
        # print(f"'{h_vld_put_tablename}': {put_sqlstr_ref},")
        # print(f"'{h_vld_del_tablename}': {del_sqlstr_ref},")
        insert_h_vld_put_sqlstr = insert_heard_vld_sqlstrs.get(h_vld_put_tablename)
        insert_h_vld_del_sqlstr = insert_heard_vld_sqlstrs.get(h_vld_del_tablename)
        assert insert_h_vld_put_sqlstr == expected_vld_put_insert_sqlstr
        assert insert_h_vld_del_sqlstr == expected_vld_del_insert_sqlstr


def test_get_insert_heard_vld_sqlstrs_ReturnsObj_PopulatesTable_Scenario0(
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
    prnptnr_h_agg_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_agg, "put")
    print(f"{get_table_columns(cursor0, prnptnr_h_agg_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prnptnr_h_agg_put_tablename} (
{kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
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
    assert get_row_count(cursor0, prnptnr_h_agg_put_tablename) == 5
    prnptnr_h_vld_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_vld, "put")
    assert get_row_count(cursor0, prnptnr_h_vld_put_tablename) == 0

    # WHEN
    sqlstr = get_insert_heard_vld_sqlstrs().get(prnptnr_h_vld_put_tablename)
    print(sqlstr)
    cursor0.execute(sqlstr)

    # THEN
    assert get_row_count(cursor0, prnptnr_h_vld_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
FROM {prnptnr_h_vld_put_tablename}
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


def test_etl_heard_agg_tables_to_heard_vld_tables_PopulatesTable_Scenario0(
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
    prnptnr_h_agg_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_agg, "put")
    print(f"{get_table_columns(cursor0, prnptnr_h_agg_put_tablename)=}")
    insert_into_clause = f"""INSERT INTO {prnptnr_h_agg_put_tablename} (
{kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
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
    assert get_row_count(cursor0, prnptnr_h_agg_put_tablename) == 5
    prnptnr_h_vld_put_tablename = prime_tbl(kw.person_partnerunit, kw.h_vld, "put")
    assert get_row_count(cursor0, prnptnr_h_vld_put_tablename) == 0

    # WHEN
    etl_heard_agg_tables_to_heard_vld_tables(cursor0)

    # THEN
    assert get_row_count(cursor0, prnptnr_h_vld_put_tablename) == 4
    select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.person_name}
, {kw.partner_name}
, {kw.partner_cred_lumen}
, {kw.partner_debt_lumen}
FROM {prnptnr_h_vld_put_tablename}
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
