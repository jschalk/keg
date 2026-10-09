from ch05_rope.rope import default_knot_if_None
from ch17_jargon.jargon_config import (
    get_jargon_labelterm_args,
    get_jargon_nameterm_args,
    get_jargon_ropeterm_args,
    get_jargon_titleterm_args,
    get_jargon_column_ref,
)
from ch17_jargon.jargon_main import default_unknown_str_if_None
from ch19_db_tool.db_toolbox import (
    create_update_inconsistency_error_query,
    delete_all_duplicate_rows,
    get_table_columns,
)
from ch20_brick.brick_config import get_brick_dimen_ref
from ch22_etl_config.etl_sqlstr import (
    create_insert_into_jargon_core_raw_sqlstr,
    create_insert_missing_spark_face_into_jargon_core_vld_sqlstr,
    create_insert_jargon_core_agg_into_vld_sqlstr,
    create_insert_jargon_sound_vld_table_sqlstr,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
    create_sound_agg_insert_sqlstrs,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    create_update_jargon_sound_agg_inconsist_sqlstr,
    create_update_trllabe_sound_agg_knot_error_sqlstr,
    create_update_trlname_sound_agg_knot_error_sqlstr,
    create_update_trlrope_sound_agg_knot_error_sqlstr,
    create_update_trltitl_sound_agg_knot_error_sqlstr,
    get_insert_into_heard_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
    get_moment_person_sound_agg_tablenames,
    get_prime_create_table_sqlstrs,
)
from copy import copy as copy_copy
from sqlite3 import Cursor as sqlite3_Cursor


def set_sound_raw_tables_error_message(cursor: sqlite3_Cursor):
    for dimen in get_brick_dimen_ref().keys():
        sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(cursor, dimen)
        cursor.execute(sqlstr)


def insert_sound_raw_selects_into_sound_agg_tables(cursor: sqlite3_Cursor):
    for dimen in get_brick_dimen_ref().keys():
        sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)
        for sqlstr in sqlstrs:
            cursor.execute(sqlstr)
    _delete_all_duplicate_rows_in_s_agg_tables(cursor)


def _delete_all_duplicate_rows_in_s_agg_tables(cursor: sqlite3_Cursor):
    for prime_tablename in get_prime_create_table_sqlstrs().keys():
        if prime_tablename.endswith("s_agg"):
            delete_all_duplicate_rows(cursor, prime_tablename)


def etl_sound_raw_tables_to_sound_agg_tables(cursor: sqlite3_Cursor):
    set_sound_raw_tables_error_message(cursor)
    insert_sound_raw_selects_into_sound_agg_tables(cursor)


def insert_jargon_sound_agg_into_jargon_core_raw_table(cursor: sqlite3_Cursor):
    for dimen in get_jargon_column_ref():
        cursor.execute(create_insert_into_jargon_core_raw_sqlstr(dimen))
    delete_all_duplicate_rows(cursor, create_prime_tablename("trlcore", "s_raw"))


def insert_jargon_core_agg_to_jargon_core_vld_table(cursor: sqlite3_Cursor):
    knot = default_knot_if_None()
    unknown = default_unknown_str_if_None()
    insert_sqlstr = create_insert_jargon_core_agg_into_vld_sqlstr(knot, unknown)
    cursor.execute(insert_sqlstr)
    delete_all_duplicate_rows(cursor, create_prime_tablename("trlcore", "s_vld"))


def update_inconsistency_jargon_core_raw_table(cursor: sqlite3_Cursor):
    jargon_core_s_raw_tablename = create_prime_tablename("trlcore", "s_raw")
    sqlstr = create_update_inconsistency_error_query(
        cursor,
        x_tablename=jargon_core_s_raw_tablename,
        focus_columns={"spark_face"},
        exclude_columns={"source_dimen"},
        error_holder_column="error_message",
        error_str="Inconsistent data",
    )

    cursor.execute(sqlstr)


def insert_jargon_core_raw_to_jargon_core_agg_table(cursor: sqlite3_Cursor):
    jargon_core_s_raw_tablename = create_prime_tablename("trlcore", "s_raw")
    jargon_core_s_agg_tablename = create_prime_tablename("trlcore", "s_agg")
    sqlstr = f"""
INSERT INTO {jargon_core_s_agg_tablename} (spark_face, otx_knot, inx_knot, unknown_str)
SELECT spark_face, MAX(otx_knot), MAX(inx_knot), MAX(unknown_str)
FROM {jargon_core_s_raw_tablename}
WHERE error_message IS NULL
GROUP BY spark_face
"""
    cursor.execute(sqlstr)
    delete_all_duplicate_rows(cursor, jargon_core_s_agg_tablename)


def update_jargon_sound_agg_inconsist_errors(cursor: sqlite3_Cursor):
    for dimen in get_jargon_column_ref():
        cursor.execute(create_update_jargon_sound_agg_inconsist_sqlstr(dimen))


def update_jargon_sound_agg_knot_errors(cursor: sqlite3_Cursor):
    cursor.execute(create_update_trllabe_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_trlrope_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_trlname_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_trltitl_sound_agg_knot_error_sqlstr())


def insert_jargon_sound_agg_tables_to_jargon_sound_vld_table(
    cursor: sqlite3_Cursor,
):
    for dimen in get_jargon_column_ref():
        cursor.execute(create_insert_jargon_sound_vld_table_sqlstr(dimen))
        delete_all_duplicate_rows(cursor, create_prime_tablename(dimen, "s_vld"))


def set_moment_person_sound_agg_knot_errors(cursor: sqlite3_Cursor):
    jargon_label_args = get_jargon_labelterm_args()
    jargon_name_args = get_jargon_nameterm_args()
    jargon_title_args = get_jargon_titleterm_args()
    jargon_rope_args = get_jargon_ropeterm_args()
    jargon_args = copy_copy(jargon_label_args)
    jargon_args.update(jargon_name_args)
    jargon_args.update(jargon_title_args)
    jargon_args.update(jargon_rope_args)
    jargonable_tuples = get_moment_person_sound_agg_jargonable_columns(
        cursor, jargon_args
    )
    for heard_raw_tablename, jargonable_columnname in jargonable_tuples:
        error_update_sqlstr = None
        if jargonable_columnname in jargon_label_args:
            error_update_sqlstr = create_knot_exists_in_label_error_update_sqlstr(
                heard_raw_tablename, jargonable_columnname
            )
        if jargonable_columnname in jargon_name_args:
            error_update_sqlstr = create_knot_exists_in_name_error_update_sqlstr(
                heard_raw_tablename, jargonable_columnname
            )
        if error_update_sqlstr:
            cursor.execute(error_update_sqlstr)


def get_moment_person_sound_agg_jargonable_columns(
    cursor: sqlite3_Cursor, jargon_args: set[str]
) -> set[tuple[str, str]]:
    jargon_columns = set()
    for x_tablename in get_insert_into_heard_raw_sqlstrs().keys():
        x_tablename = x_tablename.replace("_h_", "_s_")
        x_tablename = x_tablename.replace("_raw", "_agg")
        for columnname in get_table_columns(cursor, x_tablename):
            if columnname in jargon_args:
                jargon_columns.add((x_tablename, columnname))
    return jargon_columns


def populate_jargon_core_vld_with_missing_spark_faces(cursor: sqlite3_Cursor):
    for agg_tablename in get_moment_person_sound_agg_tablenames():
        insert_sqlstr = create_insert_missing_spark_face_into_jargon_core_vld_sqlstr(
            default_knot=default_knot_if_None(),
            default_unknown=default_unknown_str_if_None(),
            moment_person_sound_agg_tablename=agg_tablename,
        )
        cursor.execute(insert_sqlstr)


def etl_jargon_sound_agg_tables_to_jargon_sound_vld_tables(
    cursor: sqlite3_Cursor,
):
    insert_jargon_sound_agg_into_jargon_core_raw_table(cursor)
    update_inconsistency_jargon_core_raw_table(cursor)
    insert_jargon_core_raw_to_jargon_core_agg_table(cursor)
    insert_jargon_core_agg_to_jargon_core_vld_table(cursor)
    populate_jargon_core_vld_with_missing_spark_faces(cursor)
    update_jargon_sound_agg_inconsist_errors(cursor)
    update_jargon_sound_agg_knot_errors(cursor)
    insert_jargon_sound_agg_tables_to_jargon_sound_vld_table(cursor)


def etl_sound_agg_tables_to_sound_vld_tables(cursor: sqlite3_Cursor):
    for sound_vld_tablename, sqlstr in get_insert_into_sound_vld_sqlstrs().items():
        cursor.execute(sqlstr)
        delete_all_duplicate_rows(cursor, sound_vld_tablename)


def etl_sound_vld_tables_to_heard_raw_tables(cursor: sqlite3_Cursor):
    for h_raw_tablename, sqlstr in get_insert_into_heard_raw_sqlstrs().items():
        cursor.execute(sqlstr)
        delete_all_duplicate_rows(cursor, h_raw_tablename, exclude_postfix="_inx")
