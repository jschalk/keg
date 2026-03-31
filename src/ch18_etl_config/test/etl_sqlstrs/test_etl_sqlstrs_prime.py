from sqlite3 import Cursor
from src.ch00_py.db_toolbox import (
    create_insert_into_clause_str as get_insert_sql,
    create_select_query as get_select_sql,
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
    db_table_exists,
    get_db_tables,
    get_table_columns,
)
from src.ch08_person_atom.atom_config import get_person_dimens
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch16_translate.translate_config import (
    get_translate_dimens,
    set_translateable_otx_inx_args,
)
from src.ch17_idea.idea_config import get_default_sorted_list, get_idea_config_dict
from src.ch18_etl_config.etl_config import (
    create_prime_table_sqlstr,
    get_dimen_abbv7,
    get_etl_category_stages_dict,
    get_etl_stage_types_config_dict,
)
from src.ch18_etl_config.etl_sqlstr import (
    create_insert_into_translate_core_raw_sqlstr,
    create_insert_missing_face_name_into_translate_core_vld_sqlstr,
    create_insert_translate_core_agg_into_vld_sqlstr,
    create_insert_translate_sound_vld_table_sqlstr,
    create_prime_db_table,
    create_prime_tablename as prime_tbl,
    create_sound_agg_insert_sqlstrs,
    create_sound_and_heard_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    get_insert_into_heard_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
    get_moment_person_sound_agg_tablenames,
    get_person_heard_vld_tablenames,
    get_prime_create_table_sqlstrs,
)
from src.ref.keywords import Ch18Keywords as kw


def test_get_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    prime_tablenames = set(create_table_sqlstrs.keys())
    etl_category_stages_dict = get_etl_category_stages_dict()
    expected_tablenames = set()
    expected_sqlstrs_dict = {}
    expected_var_refs = set()
    expected_sql_refs = set()
    for stage_name in sorted(etl_category_stages_dict.keys(), reverse=True):
        stage_dict = etl_category_stages_dict.get(stage_name)
        x_idea_category = stage_dict.get("idea_category")
        stage_type = stage_dict.get("stage_type")
        x_put_del = stage_dict.get("put_del")
        # if x_idea_category == kw.moment:
        # print(f"{x_idea_category=}")
        for x_dimen in sorted(get_idea_config_dict(x_idea_category)):
            add_dimen_to_agg_variables(
                x_dimen,
                stage_type,
                x_put_del,
                expected_tablenames,
                expected_var_refs,
                expected_sql_refs,
                expected_sqlstrs_dict,
            )
    for trlcore_stage_type in {kw.s_raw, "s_agg", kw.s_vld}:
        add_dimen_to_agg_variables(
            x_dimen="translate_core",
            stage_type=trlcore_stage_type,
            x_put_del=None,
            expected_tablenames=expected_tablenames,
            expected_var_refs=expected_var_refs,
            expected_sql_refs=expected_sql_refs,
            expected_sqlstrs_dict=expected_sqlstrs_dict,
        )
    # print("################################################################")
    # for expected_sql_ref in sorted(expected_sql_refs):
    #     print(expected_sql_ref)
    # print("")

    assert prime_tablenames == expected_tablenames
    for expected_sql_ref, expected_sqlstr in expected_sqlstrs_dict.items():
        gen_sqlstr = create_table_sqlstrs.get(expected_sql_ref)
        if gen_sqlstr != expected_sqlstr:
            print(f"{expected_sql_ref=}")
            print(expected_sqlstr)
        # print(f"{expected_sql_ref=}")
        assert gen_sqlstr == expected_sqlstr
    assert create_table_sqlstrs == expected_sqlstrs_dict

    # translate_dimens_config = get_idea_config_dict({kw.translate})
    # for x_dimen in translate_dimens_config:
    #     s_vld_tablename = prime_tbl(abbv7(x_dimen), kw.s_vld)
    #     expected_s_vld_sqlstr = create_prime_table_sqlstr(x_dimen, kw.s_vld)

    #     abbv7 = abbv7(x_dimen)
    #     print(f'CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR= """{expected_s_vld_sqlstr}"""')

    #     # print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
    #     assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)


def add_dimen_to_agg_variables(
    x_dimen,
    stage_type: str,
    x_put_del,
    expected_tablenames,
    expected_var_refs,
    expected_sql_refs,
    expected_sqlstrs_dict,
):
    abbv7 = get_dimen_abbv7(x_dimen)
    tablename = prime_tbl(abbv7, stage_type, x_put_del)
    table_sql = create_prime_table_sqlstr(x_dimen, stage_type, x_put_del)
    stage_types_config = get_etl_stage_types_config_dict()

    if x_put_del:
        abbv5_stages = set(stage_types_config.keys())
        for abbv5_stage in abbv5_stages:
            if stage_type.startswith(abbv5_stage):
                abbv5_dict = stage_types_config.get(abbv5_stage)
                abbv9_stage = abbv5_dict.get("abbv9")
                stage_type = stage_type.replace(abbv5_stage, abbv9_stage)

    if x_put_del == "put":
        global_variable_ref = f"CREATE_{abbv7.upper()}_PUT_{stage_type.upper()}_SQLSTR"
    elif x_put_del == "del":
        global_variable_ref = f"CREATE_{abbv7.upper()}_DEL_{stage_type.upper()}_SQLSTR"
    else:
        global_variable_ref = f"CREATE_{abbv7.upper()}_{stage_type.upper()}_SQLSTR"
    # # print(f""""{tablename}": {global_variable_ref},""")
    # print("")
    # print()
    # print(f'{global_variable_ref}= """{table_sql}"""')
    expected_tablenames.add(tablename)
    expected_var_refs.add(f""""{tablename}": {global_variable_ref},""")
    expected_sql_refs.add(f'{global_variable_ref} = """{table_sql}"""')
    expected_sqlstrs_dict[tablename] = table_sql
    # assert tablename in prime_tablenames, f"{tablename} missing"
    # assert create_table_sqlstrs.get(tablename) == table_sql


def test_get_prime_create_table_sqlstrs_ReturnsObj_HasAllKeys():
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    assert create_table_sqlstrs
    translate_dimens_count = len(get_translate_dimens()) * 3
    nabu_dimens_count = len(get_nabu_dimens()) * 5
    moment_dimens_count = len(get_moment_dimens()) * 6
    person_dimens_count = len(get_person_dimens()) * 12
    print(f"{translate_dimens_count=}")
    print(f"{nabu_dimens_count=}")
    print(f"{moment_dimens_count=}")
    print(f"{person_dimens_count=}")
    all_dimens_count = (
        translate_dimens_count
        + nabu_dimens_count
        + moment_dimens_count
        + person_dimens_count
    )
    translate_core_count = 3
    all_dimens_count += translate_core_count
    assert len(create_table_sqlstrs) == all_dimens_count


def test_get_moment_person_sound_agg_tablenames_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    moment_person_sound_agg_tablenames = get_moment_person_sound_agg_tablenames()

    # THEN
    assert moment_person_sound_agg_tablenames
    expected_sound_agg_tablenames = set()
    for person_dimen in get_person_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(person_dimen, "s_agg", "put"))
        expected_sound_agg_tablenames.add(prime_tbl(person_dimen, "s_agg", "del"))
    for nabu_dimen in get_nabu_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(nabu_dimen, "s_agg"))
    for moment_dimen in get_moment_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(moment_dimen, "s_agg"))
    print(sorted(list(expected_sound_agg_tablenames)))
    assert moment_person_sound_agg_tablenames == expected_sound_agg_tablenames
    prime_create_tablenames = set(get_prime_create_table_sqlstrs().keys())
    assert moment_person_sound_agg_tablenames.issubset(prime_create_tablenames)


def test_get_person_heard_vld_tablenames_ReturnsObj_PersonDimens():
    # ESTABLISH / WHEN
    person_heard_vld_tablenames = get_person_heard_vld_tablenames()

    # THEN
    assert person_heard_vld_tablenames
    expected_person_heard_vld_tablenames = {
        prime_tbl(person_dimen, kw.h_vld, "put") for person_dimen in get_person_dimens()
    }
    print(f"{expected_person_heard_vld_tablenames=}")
    assert expected_person_heard_vld_tablenames == person_heard_vld_tablenames
    assert len(person_heard_vld_tablenames) == len(get_person_dimens())
    agg_tablenames = person_heard_vld_tablenames
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_create_sound_and_heard_tables_CreatesMomentRawTables(cursor0: Cursor):
    # ESTABLISH
    assert len(get_db_tables(cursor0)) == 0
    put_str = "put"
    del_str = "del"
    prnunit_put_s_agg_table = prime_tbl(kw.personunit, "s_agg", put_str)
    prnptnr_put_s_agg_table = prime_tbl(kw.prnptnr, "s_agg", put_str)
    prnmemb_put_s_agg_table = prime_tbl(kw.prnmemb, "s_agg", put_str)
    prnfact_del_s_agg_table = prime_tbl(kw.prnfact, "s_agg", del_str)
    prnfact_del_s_vld_table = prime_tbl(kw.prnfact, kw.s_vld, del_str)
    momentunit_s_agg_table = prime_tbl(kw.momentunit, "s_agg")
    momentunit_s_vld_table = prime_tbl(kw.momentunit, kw.s_vld)
    trltitl_s_agg_table = prime_tbl(kw.trltitl, "s_agg")
    mmthour_h_vld_table = prime_tbl(kw.mmthour, kw.h_vld)
    nabtime_s_raw_table = prime_tbl(kw.nabtime, kw.s_raw)
    trltitl_s_raw_table = prime_tbl(kw.trltitl, kw.s_raw)
    trlcore_s_raw_table = prime_tbl(kw.trlcore, kw.s_raw)
    trlcore_s_agg_table = prime_tbl(kw.trlcore, "s_agg")
    trlcore_s_vld_table = prime_tbl(kw.trlcore, kw.s_vld)

    assert not db_table_exists(cursor0, prnunit_put_s_agg_table)
    assert not db_table_exists(cursor0, prnptnr_put_s_agg_table)
    assert not db_table_exists(cursor0, prnmemb_put_s_agg_table)
    assert not db_table_exists(cursor0, prnfact_del_s_agg_table)
    assert not db_table_exists(cursor0, prnfact_del_s_vld_table)
    assert not db_table_exists(cursor0, momentunit_s_agg_table)
    assert not db_table_exists(cursor0, momentunit_s_vld_table)
    assert not db_table_exists(cursor0, trltitl_s_agg_table)
    assert not db_table_exists(cursor0, mmthour_h_vld_table)
    assert not db_table_exists(cursor0, nabtime_s_raw_table)
    assert not db_table_exists(cursor0, trltitl_s_raw_table)
    assert not db_table_exists(cursor0, trlcore_s_raw_table)
    assert not db_table_exists(cursor0, trlcore_s_agg_table)
    assert not db_table_exists(cursor0, trlcore_s_vld_table)

    # WHEN
    create_sound_and_heard_tables(cursor0)

    # THEN
    cursor0.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
    # print(f"{cursor.fetchall()=}")
    # x_count = 0
    # for x_row in cursor.fetchall():
    #     print(f"{x_count} {x_row[1]=}")
    #     x_count += 1
    assert db_table_exists(cursor0, prnunit_put_s_agg_table)
    assert db_table_exists(cursor0, prnptnr_put_s_agg_table)
    assert db_table_exists(cursor0, prnmemb_put_s_agg_table)
    assert db_table_exists(cursor0, prnfact_del_s_agg_table)
    assert db_table_exists(cursor0, prnfact_del_s_vld_table)
    assert db_table_exists(cursor0, momentunit_s_agg_table)
    assert db_table_exists(cursor0, momentunit_s_vld_table)
    assert db_table_exists(cursor0, trltitl_s_agg_table)
    assert db_table_exists(cursor0, mmthour_h_vld_table)
    assert db_table_exists(cursor0, nabtime_s_raw_table)
    assert db_table_exists(cursor0, trltitl_s_raw_table)
    assert db_table_exists(cursor0, trlcore_s_raw_table)
    assert db_table_exists(cursor0, trlcore_s_agg_table)
    assert db_table_exists(cursor0, trlcore_s_vld_table)
    assert len(get_db_tables(cursor0)) == 182


def test_create_prime_db_table_CreatesSingleTable(cursor0: Cursor):
    # ESTABLISH
    assert len(get_db_tables(cursor0)) == 0
    put_str = "put"
    prnunit_put_s_agg_table = prime_tbl(kw.personunit, "s_agg", put_str)

    assert not db_table_exists(cursor0, prnunit_put_s_agg_table)
    assert len(get_db_tables(cursor0)) == 0

    # WHEN
    gen_tablename = create_prime_db_table(cursor0, kw.personunit, "s_agg", put_str)

    # THEN
    assert db_table_exists(cursor0, prnunit_put_s_agg_table)
    assert len(get_db_tables(cursor0)) == 1
    assert gen_tablename == prnunit_put_s_agg_table


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario0_TranslateDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.translate_title
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
        cursor0, dimen
    )

    # THEN
    x_tablename = prime_tbl(dimen, kw.s_raw)
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    exclude_cols = {kw.idea_number, kw.error_message}
    expected_update_sqlstr = create_update_inconsistency_error_query(
        cursor0,
        x_tablename,
        dimen_focus_columns,
        exclude_cols,
        error_holder_column=kw.error_message,
        error_str="Inconsistent data",
    )
    assert update_sqlstr == expected_update_sqlstr

    static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT spark_num, face_name, otx_title
FROM translate_title_s_raw
GROUP BY spark_num, face_name, otx_title
HAVING MIN(inx_title) != MAX(inx_title)
    OR MIN(otx_knot) != MAX(otx_knot)
    OR MIN(inx_knot) != MAX(inx_knot)
    OR MIN(unknown_str) != MAX(unknown_str)
)
UPDATE translate_title_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.spark_num = translate_title_s_raw.spark_num
    AND inconsistency_rows.face_name = translate_title_s_raw.face_name
    AND inconsistency_rows.otx_title = translate_title_s_raw.otx_title
;
"""
    print(update_sqlstr)
    assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario1_MomentDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.moment_epoch_hour
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
        cursor0, dimen
    )

    # THEN
    x_tablename = prime_tbl(dimen, kw.s_raw)
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    exclude_cols = {
        kw.idea_number,
        kw.spark_num,
        kw.face_name,
        kw.error_message,
    }
    expected_update_sqlstr = create_update_inconsistency_error_query(
        cursor0,
        x_tablename,
        dimen_focus_columns,
        exclude_cols,
        error_holder_column=kw.error_message,
        error_str="Inconsistent data",
    )
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr

    static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT moment_rope, cumulative_minute
FROM moment_epoch_hour_s_raw
GROUP BY moment_rope, cumulative_minute
HAVING MIN(hour_label) != MAX(hour_label)
    OR MIN(knot) != MAX(knot)
)
UPDATE moment_epoch_hour_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.moment_rope = moment_epoch_hour_s_raw.moment_rope
    AND inconsistency_rows.cumulative_minute = moment_epoch_hour_s_raw.cumulative_minute
;
"""
    # print(update_sqlstr)
    assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario2_NabuDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.nabu_timenum
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
        cursor0, dimen
    )

    # THEN
    x_tablename = prime_tbl(dimen, kw.s_raw)
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    exclude_cols = {
        kw.idea_number,
        kw.spark_num,
        kw.face_name,
        kw.error_message,
    }
    expected_update_sqlstr = create_update_inconsistency_error_query(
        cursor0,
        x_tablename,
        dimen_focus_columns,
        exclude_cols,
        error_holder_column=kw.error_message,
        error_str="Inconsistent data",
    )
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr

    static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT moment_rope, otx_time
FROM nabu_timenum_s_raw
GROUP BY moment_rope, otx_time
HAVING MIN(inx_time) != MAX(inx_time)
)
UPDATE nabu_timenum_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.moment_rope = nabu_timenum_s_raw.moment_rope
    AND inconsistency_rows.otx_time = nabu_timenum_s_raw.otx_time
;
"""
    # print(update_sqlstr)
    assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario3_PersonDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.person_plan_awardunit
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
        cursor0, dimen
    )

    # THEN
    x_tablename = prime_tbl(dimen, kw.s_raw, "put")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    exclude_cols = {kw.idea_number, kw.error_message}
    expected_update_sqlstr = create_update_inconsistency_error_query(
        cursor0,
        x_tablename,
        dimen_focus_columns,
        exclude_cols,
        error_holder_column=kw.error_message,
        error_str="Inconsistent data",
    )
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr

    static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT spark_num, face_name, person_name, plan_rope, awardee_title
FROM person_plan_awardunit_put_s_raw
GROUP BY spark_num, face_name, person_name, plan_rope, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
    OR MIN(knot) != MAX(knot)
)
UPDATE person_plan_awardunit_put_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.spark_num = person_plan_awardunit_put_s_raw.spark_num
    AND inconsistency_rows.face_name = person_plan_awardunit_put_s_raw.face_name
    AND inconsistency_rows.person_name = person_plan_awardunit_put_s_raw.person_name
    AND inconsistency_rows.plan_rope = person_plan_awardunit_put_s_raw.plan_rope
    AND inconsistency_rows.awardee_title = person_plan_awardunit_put_s_raw.awardee_title
;
"""
    print(update_sqlstr)
    assert update_sqlstr == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario0_TranslateDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.translate_title
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor0, dimen)

    # THEN
    raw_tablename = prime_tbl(dimen, kw.s_raw)
    agg_tablename = prime_tbl(dimen, "s_agg")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    exclude_cols = {kw.idea_number, kw.error_message}
    expected_insert_sqlstr = create_table2table_agg_insert_query(
        cursor0,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    # print(expected_insert_sqlstr)
    assert update_sqlstrs[0] == expected_insert_sqlstr

    static_example_sqlstr = """INSERT INTO translate_title_s_agg (spark_num, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str)
SELECT spark_num, face_name, otx_title, MAX(inx_title), MAX(otx_knot), MAX(inx_knot), MAX(unknown_str)
FROM translate_title_s_raw
WHERE error_message IS NULL
GROUP BY spark_num, face_name, otx_title
;
"""
    print(update_sqlstrs[0])
    assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario1_MomentDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.moment_epoch_hour
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor0, dimen)

    # THEN
    raw_tablename = prime_tbl(dimen, kw.s_raw)
    agg_tablename = prime_tbl(dimen, "s_agg")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {kw.idea_number, kw.error_message}
    print("yeah")
    expected_insert_sqlstr = create_table2table_agg_insert_query(
        cursor0,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    print(expected_insert_sqlstr)
    assert update_sqlstrs[0] == expected_insert_sqlstr

    static_example_sqlstr = """INSERT INTO moment_epoch_hour_s_agg (spark_num, face_name, moment_rope, cumulative_minute, hour_label, knot)
SELECT spark_num, face_name, moment_rope, cumulative_minute, MAX(hour_label), MAX(knot)
FROM moment_epoch_hour_s_raw
WHERE error_message IS NULL
GROUP BY spark_num, face_name, moment_rope, cumulative_minute
;
"""
    print(update_sqlstrs[0])
    assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario2_NabuDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.nabu_timenum
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor0, dimen)

    # THEN
    raw_tablename = prime_tbl(dimen, kw.s_raw)
    agg_tablename = prime_tbl(dimen, "s_agg")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get(kw.jkeys).keys())
    dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {kw.idea_number, kw.error_message}
    print("yeah")
    expected_insert_sqlstr = create_table2table_agg_insert_query(
        cursor0,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    print(expected_insert_sqlstr)
    assert update_sqlstrs[0] == expected_insert_sqlstr

    static_example_sqlstr = """INSERT INTO nabu_timenum_s_agg (spark_num, face_name, moment_rope, otx_time, inx_time)
SELECT spark_num, face_name, moment_rope, otx_time, MAX(inx_time)
FROM nabu_timenum_s_raw
WHERE error_message IS NULL
GROUP BY spark_num, face_name, moment_rope, otx_time
;
"""
    print(update_sqlstrs[0])
    assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario3_PersonDimen(
    cursor0: Cursor,
):
    # ESTABLISH
    dimen = kw.person_plan_awardunit
    create_sound_and_heard_tables(cursor0)

    # WHEN
    update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor0, dimen)

    # THEN
    put_raw_tablename = prime_tbl(dimen, kw.s_raw, "put")
    put_agg_tablename = prime_tbl(dimen, "s_agg", "put")
    put_dimen_config = get_idea_config_dict().get(dimen)
    put_dimen_focus_columns = set(put_dimen_config.get(kw.jkeys).keys())
    put_exclude_cols = {kw.idea_number, kw.error_message}
    put_expected_insert_sqlstr = create_table2table_agg_insert_query(
        cursor0,
        src_table=put_raw_tablename,
        dst_table=put_agg_tablename,
        focus_cols=put_dimen_focus_columns,
        exclude_cols=put_exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    print(put_expected_insert_sqlstr)
    assert update_sqlstrs[0] == put_expected_insert_sqlstr

    static_example_put_sqlstr = """INSERT INTO person_plan_awardunit_put_s_agg (spark_num, face_name, person_name, plan_rope, awardee_title, give_force, take_force, knot)
SELECT spark_num, face_name, person_name, plan_rope, awardee_title, MAX(give_force), MAX(take_force), MAX(knot)
FROM person_plan_awardunit_put_s_raw
WHERE error_message IS NULL
GROUP BY spark_num, face_name, person_name, plan_rope, awardee_title
;
"""
    # print(update_sqlstrs[0])
    assert update_sqlstrs[0] == static_example_put_sqlstr

    # del
    del_raw_tablename = prime_tbl(dimen, kw.s_raw, "del")
    del_agg_tablename = prime_tbl(dimen, "s_agg", "del")
    del_dimen_focus_columns = set(put_dimen_config.get(kw.jkeys).keys())
    del_dimen_focus_columns = get_default_sorted_list(del_dimen_focus_columns)
    last_element = del_dimen_focus_columns.pop(-1)
    del_dimen_focus_columns.append(f"{last_element}_ERASE")
    print(f"{del_dimen_focus_columns=} {last_element}")
    del_exclude_cols = {kw.idea_number, kw.error_message}
    del_expected_insert_sqlstr = create_table2table_agg_insert_query(
        cursor0,
        src_table=del_raw_tablename,
        dst_table=del_agg_tablename,
        focus_cols=del_dimen_focus_columns,
        exclude_cols=del_exclude_cols,
        where_block="",
    )
    print(del_expected_insert_sqlstr)
    print(update_sqlstrs[1])
    assert update_sqlstrs[1] == del_expected_insert_sqlstr

    static_example_del_sqlstr = """INSERT INTO person_plan_awardunit_del_s_agg (spark_num, face_name, person_name, plan_rope, awardee_title_ERASE)
SELECT spark_num, face_name, person_name, plan_rope, awardee_title_ERASE
FROM person_plan_awardunit_del_s_raw
GROUP BY spark_num, face_name, person_name, plan_rope, awardee_title_ERASE
;
"""
    assert update_sqlstrs[1] == static_example_del_sqlstr


def test_create_insert_into_translate_core_raw_sqlstr_ReturnsObj():
    # ESTABLISH
    dimen = kw.translate_rope
    # WHEN
    rope_sqlstr = create_insert_into_translate_core_raw_sqlstr(dimen)

    # THEN
    translate_s_agg_tablename = prime_tbl(dimen, "s_agg")
    translate_core_s_raw_tablename = prime_tbl("TRLCORE", kw.s_raw)
    expected_sqlstr = f"""INSERT INTO {translate_core_s_raw_tablename} (source_dimen, face_name, otx_knot, inx_knot, unknown_str)
SELECT '{translate_s_agg_tablename}', face_name, otx_knot, inx_knot, unknown_str
FROM {translate_s_agg_tablename}
GROUP BY face_name, otx_knot, inx_knot, unknown_str
;
"""
    assert rope_sqlstr == expected_sqlstr


def test_create_insert_translate_core_agg_into_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_knot = "|"
    default_unknown_str = "unknown2"

    # WHEN
    insert_sqlstr = create_insert_translate_core_agg_into_vld_sqlstr(
        default_knot, default_unknown_str
    )

    # THEN
    trlcore_dimen = "TRLCORE"
    translate_core_s_agg_tablename = prime_tbl(trlcore_dimen, "s_agg")
    translate_core_s_vld_tablename = prime_tbl(trlcore_dimen, kw.s_vld)
    expected_sqlstr = f"""INSERT INTO {translate_core_s_vld_tablename} (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  face_name
, IFNULL(otx_knot, '{default_knot}')
, IFNULL(inx_knot, '{default_knot}')
, IFNULL(unknown_str, '{default_unknown_str}')
FROM {translate_core_s_agg_tablename}
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_missing_face_name_into_translate_core_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_knot = "|"
    default_unknown_str = "unknown2"
    prnptnr_s_agg_tablename = prime_tbl(kw.person_partnerunit, "s_agg")

    # WHEN
    insert_sqlstr = create_insert_missing_face_name_into_translate_core_vld_sqlstr(
        default_knot, default_unknown_str, prnptnr_s_agg_tablename
    )

    # THEN
    trlcore_dimen = "TRLCORE"
    translate_core_s_vld_tablename = prime_tbl(trlcore_dimen, kw.s_vld)
    expected_sqlstr = f"""INSERT INTO {translate_core_s_vld_tablename} (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  {prnptnr_s_agg_tablename}.face_name
, '{default_knot}'
, '{default_knot}'
, '{default_unknown_str}'
FROM {prnptnr_s_agg_tablename} 
LEFT JOIN translate_core_s_vld ON translate_core_s_vld.face_name = {prnptnr_s_agg_tablename}.face_name
WHERE translate_core_s_vld.face_name IS NULL
GROUP BY {prnptnr_s_agg_tablename}.face_name
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_translate_sound_vld_table_sqlstr_ReturnsObj_translate_rope():
    # ESTABLISH
    dimen = kw.translate_rope
    # WHEN
    rope_sqlstr = create_insert_translate_sound_vld_table_sqlstr(dimen)

    # THEN
    translate_dimen_s_agg_tablename = prime_tbl(dimen, "s_agg")
    translate_dimen_s_vld_tablename = prime_tbl(dimen, kw.s_vld)
    expected_rope_sqlstr = f"""
INSERT INTO {translate_dimen_s_vld_tablename} (spark_num, face_name, otx_rope, inx_rope)
SELECT spark_num, face_name, MAX(otx_rope), MAX(inx_rope)
FROM {translate_dimen_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY spark_num, face_name
;
"""
    print(expected_rope_sqlstr)
    assert rope_sqlstr == expected_rope_sqlstr


def test_create_insert_translate_sound_vld_table_sqlstr_ReturnsObj_translate_label():
    # ESTABLISH
    dimen = kw.translate_label
    # WHEN
    label_sqlstr = create_insert_translate_sound_vld_table_sqlstr(dimen)

    # THEN
    translate_label_s_agg_tablename = prime_tbl(dimen, "s_agg")
    translate_label_s_vld_tablename = prime_tbl(dimen, kw.s_vld)
    expected_label_sqlstr = f"""
INSERT INTO {translate_label_s_vld_tablename} (spark_num, face_name, otx_label, inx_label)
SELECT spark_num, face_name, MAX(otx_label), MAX(inx_label)
FROM {translate_label_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY spark_num, face_name
;
"""
    assert label_sqlstr == expected_label_sqlstr


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_PersonDimens(cursor0: Cursor):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    person_dimens_config = get_idea_config_dict({kw.person})

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    create_sound_and_heard_tables(cursor0)

    for person_dimen in person_dimens_config:
        # print(f"{person_dimen=}")
        put_s_agg_tablename = prime_tbl(person_dimen, "s_agg", "put")
        del_s_agg_tablename = prime_tbl(person_dimen, "s_agg", "del")
        put_s_vld_tablename = prime_tbl(person_dimen, kw.s_vld, "put")
        del_s_vld_tablename = prime_tbl(person_dimen, kw.s_vld, "del")
        put_s_agg_cols = get_table_columns(cursor0, put_s_agg_tablename)
        del_s_agg_cols = get_table_columns(cursor0, del_s_agg_tablename)
        put_s_agg_cols.remove(kw.error_message)
        del_s_agg_cols.remove(kw.error_message)
        put_s_agg_cols = set(put_s_agg_cols)
        del_s_agg_cols = set(del_s_agg_cols)
        put_s_vld_cols = set(get_table_columns(cursor0, put_s_vld_tablename))
        del_s_vld_cols = set(get_table_columns(cursor0, del_s_vld_tablename))
        put_s_vld_tbl = put_s_vld_tablename
        del_s_vld_tbl = del_s_vld_tablename
        put_s_agg_tbl = put_s_agg_tablename
        del_s_agg_tbl = del_s_agg_tablename
        put_s_vld_insert_sql = get_insert_sql(cursor0, put_s_vld_tbl, put_s_vld_cols)
        del_s_vld_insert_sql = get_insert_sql(cursor0, del_s_vld_tbl, del_s_vld_cols)
        put_s_agg_select_sql = get_select_sql(
            cursor0, put_s_agg_tbl, put_s_agg_cols, flat_bool=True
        )
        del_s_agg_select_sql = get_select_sql(
            cursor0, del_s_agg_tbl, del_s_agg_cols, flat_bool=True
        )
        where_clause = "WHERE error_message IS NULL"
        put_s_agg_select_sql = f"{put_s_agg_select_sql}{where_clause}"
        del_s_agg_select_sql = f"{del_s_agg_select_sql}{where_clause}"
        put_s_vld_insert_select = f"{put_s_vld_insert_sql} {put_s_agg_select_sql}"
        del_s_vld_insert_select = f"{del_s_vld_insert_sql} {del_s_agg_select_sql}"
        # print(f"{put_s_vld_insert_sql=}")
        # create_select_query(cursor=)
        abbv7 = get_dimen_abbv7(person_dimen)
        put_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_PUT_SQLSTR"
        del_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_DEL_SQLSTR"
        # print(f'{put_sqlstr_ref}= "{put_s_vld_insert_select}"')
        # print(f'{del_sqlstr_ref}= "{del_s_vld_insert_select}"')
        # print(f"""'{put_s_vld_tablename}': {put_sqlstr_ref},""")
        # print(f"""'{del_s_vld_tablename}': {del_sqlstr_ref},""")
        assert insert_s_vld_sqlstrs.get(put_s_vld_tbl) == put_s_vld_insert_select
        assert insert_s_vld_sqlstrs.get(del_s_vld_tbl) == del_s_vld_insert_select


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_Moment_Nabu_Dimens(
    cursor0: Cursor,
):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    moment_dimens_config = get_idea_config_dict({kw.moment, kw.nabu})
    print(f"{moment_dimens_config.keys()=}")

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    create_sound_and_heard_tables(cursor0)

    for moment_dimen in moment_dimens_config:
        # print(f"{moment_dimen=}")
        s_agg_tablename = prime_tbl(moment_dimen, "s_agg")
        s_vld_tablename = prime_tbl(moment_dimen, kw.s_vld)
        s_agg_cols = get_table_columns(cursor0, s_agg_tablename)
        s_agg_cols.remove(kw.error_message)
        s_agg_cols = set(s_agg_cols)
        s_vld_cols = set(get_table_columns(cursor0, s_vld_tablename))
        s_vld_tbl = s_vld_tablename
        s_agg_tbl = s_agg_tablename
        s_vld_insert_sql = get_insert_sql(cursor0, s_vld_tbl, s_vld_cols)
        s_agg_select_sql = get_select_sql(
            cursor0, s_agg_tbl, s_agg_cols, flat_bool=True
        )
        where_clause = "WHERE error_message IS NULL"
        s_agg_select_sql = f"{s_agg_select_sql}{where_clause}"
        s_vld_insert_select = f"{s_vld_insert_sql} {s_agg_select_sql}"
        # create_select_query(cursor=)
        abbv7 = get_dimen_abbv7(moment_dimen)
        sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_SQLSTR"
        print(f'{sqlstr_ref}= "{s_vld_insert_select}"')
        # print(f""""{s_vld_tablename}": {sqlstr_ref},""")
        assert insert_s_vld_sqlstrs.get(s_vld_tbl) == s_vld_insert_select


def test_get_insert_into_heard_raw_sqlstrs_ReturnsObj_PersonDimens(cursor0: Cursor):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    person_dimens_config = get_idea_config_dict({kw.person})

    # WHEN
    insert_h_raw_sqlstrs = get_insert_into_heard_raw_sqlstrs()

    # THEN
    create_sound_and_heard_tables(cursor0)

    for person_dimen in person_dimens_config:
        # print(f"{person_dimen=}")
        put_s_vld_tablename = prime_tbl(person_dimen, kw.s_vld, "put")
        del_s_vld_tablename = prime_tbl(person_dimen, kw.s_vld, "del")
        put_h_raw_tablename = prime_tbl(person_dimen, kw.h_raw, "put")
        del_h_raw_tablename = prime_tbl(person_dimen, kw.h_raw, "del")
        put_s_cols = set(get_table_columns(cursor0, put_s_vld_tablename))
        s_del_cols = set(get_table_columns(cursor0, del_s_vld_tablename))
        # put_s_cols = set(put_s_cols).remove(kw.error_message)
        # s_del_cols = set(s_del_cols).remove(kw.error_message)
        put_h_raw_cols = set(get_table_columns(cursor0, put_h_raw_tablename))
        del_h_raw_cols = set(get_table_columns(cursor0, del_h_raw_tablename))
        put_h_cols = set_translateable_otx_inx_args(put_h_raw_cols)
        h_del_cols = set_translateable_otx_inx_args(del_h_raw_cols)
        put_h_cols.remove(kw.translate_spark_num)
        h_del_cols.remove(kw.translate_spark_num)
        put_h_cols = {col for col in put_h_cols if col[-3:] != "inx"}
        h_del_cols = {col for col in h_del_cols if col[-3:] != "inx"}
        put_h_raw_tbl = put_h_raw_tablename
        del_h_raw_tbl = del_h_raw_tablename
        put_s_vld_tbl = put_s_vld_tablename
        del_s_vld_tbl = del_s_vld_tablename
        put_h_raw_insert_sql = get_insert_sql(cursor0, put_h_raw_tbl, put_h_cols)
        del_h_raw_insert_sql = get_insert_sql(cursor0, del_h_raw_tbl, h_del_cols)
        put_s_vld_select_sql = get_select_sql(
            cursor0, put_s_vld_tbl, put_s_cols, flat_bool=True
        )
        del_s_vld_select_sql = get_select_sql(
            cursor0, del_s_vld_tbl, s_del_cols, flat_bool=True
        )
        put_h_raw_insert_select = f"{put_h_raw_insert_sql} {put_s_vld_select_sql}"
        del_h_raw_insert_select = f"{del_h_raw_insert_sql} {del_s_vld_select_sql}"
        # create_select_query(cursor=)
        abbv7 = get_dimen_abbv7(person_dimen)
        put_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_RAW_PUT_SQLSTR"
        del_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_RAW_DEL_SQLSTR"
        # print(f'{put_sqlstr_ref}= "{put_h_raw_insert_select}"')
        # print(f'{del_sqlstr_ref}= "{del_h_raw_insert_select}"')
        # print(f"""'{put_h_raw_tablename}': {put_sqlstr_ref},""")
        # print(f"""'{del_h_raw_tablename}': {del_sqlstr_ref},""")
        assert insert_h_raw_sqlstrs.get(put_h_raw_tbl) == put_h_raw_insert_select
        assert insert_h_raw_sqlstrs.get(del_h_raw_tbl) == del_h_raw_insert_select


def test_get_insert_into_heard_raw_sqlstrs_ReturnsObj_Moment_Nabu_Dimens(
    cursor0: Cursor,
):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    moment_dimens_config = get_idea_config_dict({kw.moment, kw.nabu})

    # WHEN
    insert_h_raw_sqlstrs = get_insert_into_heard_raw_sqlstrs()

    # THEN
    create_sound_and_heard_tables(cursor0)

    for moment_dimen in moment_dimens_config:
        # print(f"{moment_dimen=}")
        s_vld_tablename = prime_tbl(moment_dimen, kw.s_vld)
        h_raw_tablename = prime_tbl(moment_dimen, kw.h_raw)
        s_cols = set(get_table_columns(cursor0, s_vld_tablename))
        h_raw_cols = get_table_columns(cursor0, h_raw_tablename)
        h_raw_cols.remove(kw.error_message)
        v_cols = set_translateable_otx_inx_args(h_raw_cols)
        v_cols = {col for col in v_cols if col[-3:] != "inx"}
        h_raw_tbl = h_raw_tablename
        s_vld_tbl = s_vld_tablename
        h_raw_insert_sql = get_insert_sql(cursor0, h_raw_tbl, v_cols)
        s_vld_select_sql = get_select_sql(cursor0, s_vld_tbl, s_cols, flat_bool=True)
        h_raw_insert_select = f"{h_raw_insert_sql} {s_vld_select_sql}"
        # create_select_query(cursor=)
        abbv7 = get_dimen_abbv7(moment_dimen)
        sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_RAW_SQLSTR"
        print(f'{sqlstr_ref}= "{h_raw_insert_select}"')
        # print(f""""{h_raw_tablename}": {sqlstr_ref},""")
        assert insert_h_raw_sqlstrs.get(h_raw_tbl) == h_raw_insert_select
