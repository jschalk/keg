from sqlite3 import Cursor
from src.ch17_idea.idea_config import get_idea_config_dict
from src.ch17_idea.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ref.keywords import Ch17Keywords as kw


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_person_plan_laborunit(
    cursor0: Cursor,
):
    # ESTABLISH
    idea_number = "br000XX"
    idea_cols = [
        kw.spark_num,
        kw.face_name,
        kw.plan_rope,
        kw.labor_title,
        kw.person_name,
        kw.contact_name,
        kw.amount,
    ]
    prnlabo_cat = "person_plan_laborunit"
    src_table = f"{idea_number}_raw"
    dst_table = f"{prnlabo_cat}_raw"
    idea_config = get_idea_config_dict()
    prnlabo_config = idea_config.get(prnlabo_cat)
    print(f"{prnlabo_cat=}")
    print(f"{prnlabo_config=}")
    prnlabo_jkeys = prnlabo_config.get(kw.jkeys)
    prnlabo_jvals = prnlabo_config.get(kw.jvalues)
    prnlabo_args = set(prnlabo_jkeys.keys()).union(set(prnlabo_jvals.keys()))
    prnlabo_args = get_default_sorted_list(prnlabo_args)
    print(f"{prnlabo_jkeys=}")
    print(f"{prnlabo_jvals=}")
    create_idea_sorted_table(cursor0, src_table, idea_cols)
    create_idea_sorted_table(cursor0, dst_table, prnlabo_args)

    # WHEN
    gen_sqlstr = get_idea_into_dimen_raw_query(
        cursor0, idea_number, prnlabo_cat, prnlabo_jkeys
    )

    # THEN
    columns_str = f"{kw.spark_num}, {kw.face_name}, {kw.person_name}, {kw.plan_rope}, {kw.labor_title}"
    expected_sqlstr = f"""INSERT INTO {prnlabo_cat}_raw ({kw.idea_number}, {columns_str})
SELECT '{idea_number}' as {kw.idea_number}, {columns_str}
FROM {idea_number}_raw
WHERE {kw.spark_num} IS NOT NULL AND {kw.face_name} IS NOT NULL AND {kw.person_name} IS NOT NULL AND {kw.plan_rope} IS NOT NULL AND {kw.labor_title} IS NOT NULL
GROUP BY {columns_str}
;
"""
    print("")
    print(gen_sqlstr)
    print(expected_sqlstr)
    assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_person_contactunit(
    cursor0: Cursor,
):
    # ESTABLISH
    idea_number = "br000XX"
    idea_cols = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.labor_title,
        kw.person_name,
        kw.contact_name,
        kw.contact_cred_lumen,
        kw.contact_debt_lumen,
        kw.amount,
    ]
    src_table = f"{idea_number}_raw"
    prncont_table = f"{kw.person_contactunit}_raw"
    idea_config = get_idea_config_dict()
    prncont_config = idea_config.get(kw.person_contactunit)
    prncont_jkeys = prncont_config.get(kw.jkeys)
    prncont_jvals = prncont_config.get(kw.jvalues)
    prncont_args = set(prncont_jkeys.keys()).union(set(prncont_jvals.keys()))
    print(f"{prncont_jkeys=}")
    print(f"{prncont_jvals=}")
    create_idea_sorted_table(cursor0, src_table, idea_cols)
    create_idea_sorted_table(cursor0, prncont_table, list(prncont_args))

    # WHEN
    gen_sqlstr = get_idea_into_dimen_raw_query(
        cursor0, idea_number, kw.person_contactunit, prncont_jkeys
    )

    # THEN
    columns_str = "spark_num, face_name, moment_rope, person_name, contact_name, contact_cred_lumen, contact_debt_lumen"
    expected_sqlstr = f"""INSERT INTO {kw.person_contactunit}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE spark_num IS NOT NULL AND face_name IS NOT NULL AND moment_rope IS NOT NULL AND person_name IS NOT NULL AND contact_name IS NOT NULL
GROUP BY {columns_str}
;
"""
    print("")
    print(gen_sqlstr)
    print(expected_sqlstr)

    assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_person_contactunit(
    cursor0: Cursor,
):
    # ESTABLISH
    idea_number = "br000XX"
    idea_cols = [
        kw.spark_num,
        kw.face_name,
        kw.plan_rope,
        kw.labor_title,
        kw.person_name,
        kw.contact_name,
        kw.contact_cred_lumen,
        kw.amount,
    ]
    src_table = f"{idea_number}_raw"
    prncont_table = f"{kw.person_contactunit}_raw"
    idea_config = get_idea_config_dict()
    prncont_config = idea_config.get(kw.person_contactunit)
    prncont_jkeys = prncont_config.get(kw.jkeys)
    prncont_jvals = prncont_config.get(kw.jvalues)
    prncont_args = set(prncont_jkeys.keys()).union(set(prncont_jvals.keys()))
    print(f"{prncont_jkeys=}")
    print(f"{prncont_jvals=}")
    create_idea_sorted_table(cursor0, src_table, idea_cols)
    create_idea_sorted_table(cursor0, prncont_table, list(prncont_args))

    # WHEN
    gen_sqlstr = get_idea_into_dimen_raw_query(
        cursor0, idea_number, kw.person_contactunit, prncont_jkeys
    )

    # THEN
    columns_str = "spark_num, face_name, person_name, contact_name, contact_cred_lumen"
    expected_sqlstr = f"""INSERT INTO {kw.person_contactunit}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE spark_num IS NOT NULL AND face_name IS NOT NULL AND moment_rope IS NOT NULL AND person_name IS NOT NULL AND contact_name IS NOT NULL
GROUP BY {columns_str}
;
"""
    print("generated:")
    print(gen_sqlstr)
    print(expected_sqlstr)

    assert gen_sqlstr == expected_sqlstr
