from ch00_py.db_toolbox import (
    create_update_inconsistency_error_query,
    get_table_columns,
)
from ch04_rope.rope import default_knot_if_None
from ch16_translate.translate_config import (
    get_translate_labelterm_args,
    get_translate_nameterm_args,
    get_translate_ropeterm_args,
    get_translate_titleterm_args,
    get_translates_column_ref,
)
from ch16_translate.translate_main import default_unknown_str_if_None
from ch17_idea.idea_config import get_idea_dimen_ref
from ch18_etl_config.etl_sqlstr import (
    create_insert_into_translate_core_raw_sqlstr,
    create_insert_missing_spark_face_into_translate_core_vld_sqlstr,
    create_insert_translate_core_agg_into_vld_sqlstr,
    create_insert_translate_sound_vld_table_sqlstr,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
    create_sound_agg_insert_sqlstrs,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    create_update_translate_sound_agg_inconsist_sqlstr,
    create_update_trllabe_sound_agg_knot_error_sqlstr,
    create_update_trlname_sound_agg_knot_error_sqlstr,
    create_update_trlrope_sound_agg_knot_error_sqlstr,
    create_update_trltitl_sound_agg_knot_error_sqlstr,
    get_insert_into_heard_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
    get_moment_person_sound_agg_tablenames,
)
from copy import copy as copy_copy
from sqlite3 import Cursor as sqlite3_Cursor


def set_sound_raw_tables_error_message(cursor: sqlite3_Cursor):
    for dimen in get_idea_dimen_ref().keys():
        sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(cursor, dimen)
        cursor.execute(sqlstr)


def insert_sound_raw_selects_into_sound_agg_tables(cursor: sqlite3_Cursor):
    for dimen in get_idea_dimen_ref().keys():
        sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)
        for sqlstr in sqlstrs:
            cursor.execute(sqlstr)


def etl_sound_raw_tables_to_sound_agg_tables(cursor: sqlite3_Cursor):
    set_sound_raw_tables_error_message(cursor)
    insert_sound_raw_selects_into_sound_agg_tables(cursor)


def insert_translate_sound_agg_into_translate_core_raw_table(cursor: sqlite3_Cursor):
    for dimen in get_translates_column_ref():
        if dimen != "translate_epoch":
            cursor.execute(create_insert_into_translate_core_raw_sqlstr(dimen))


def insert_translate_core_agg_to_translate_core_vld_table(cursor: sqlite3_Cursor):
    knot = default_knot_if_None()
    unknown = default_unknown_str_if_None()
    insert_sqlstr = create_insert_translate_core_agg_into_vld_sqlstr(knot, unknown)
    cursor.execute(insert_sqlstr)


def update_inconsistency_translate_core_raw_table(cursor: sqlite3_Cursor):
    translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s_raw")
    sqlstr = create_update_inconsistency_error_query(
        cursor,
        x_tablename=translate_core_s_raw_tablename,
        focus_columns={"spark_face"},
        exclude_columns={"source_dimen"},
        error_holder_column="error_message",
        error_str="Inconsistent data",
    )

    cursor.execute(sqlstr)


def insert_translate_core_raw_to_translate_core_agg_table(cursor: sqlite3_Cursor):
    translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s_raw")
    translate_core_s_agg_tablename = create_prime_tablename("trlcore", "s_agg")
    sqlstr = f"""
INSERT INTO {translate_core_s_agg_tablename} (spark_face, otx_knot, inx_knot, unknown_str)
SELECT spark_face, MAX(otx_knot), MAX(inx_knot), MAX(unknown_str)
FROM {translate_core_s_raw_tablename}
WHERE error_message IS NULL
GROUP BY spark_face
"""
    cursor.execute(sqlstr)


def update_translate_sound_agg_inconsist_errors(cursor: sqlite3_Cursor):
    for dimen in get_translates_column_ref():
        cursor.execute(create_update_translate_sound_agg_inconsist_sqlstr(dimen))


def update_translate_sound_agg_knot_errors(cursor: sqlite3_Cursor):
    cursor.execute(create_update_trllabe_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_trlrope_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_trlname_sound_agg_knot_error_sqlstr())
    cursor.execute(create_update_trltitl_sound_agg_knot_error_sqlstr())


def insert_translate_sound_agg_tables_to_translate_sound_vld_table(
    cursor: sqlite3_Cursor,
):
    for dimen in get_translates_column_ref():
        if dimen != "translate_epoch":
            cursor.execute(create_insert_translate_sound_vld_table_sqlstr(dimen))


def set_moment_person_sound_agg_knot_errors(cursor: sqlite3_Cursor):
    translate_label_args = get_translate_labelterm_args()
    translate_name_args = get_translate_nameterm_args()
    translate_title_args = get_translate_titleterm_args()
    translate_rope_args = get_translate_ropeterm_args()
    translate_args = copy_copy(translate_label_args)
    translate_args.update(translate_name_args)
    translate_args.update(translate_title_args)
    translate_args.update(translate_rope_args)
    translateable_tuples = get_moment_person_sound_agg_translateable_columns(
        cursor, translate_args
    )
    for heard_raw_tablename, translateable_columnname in translateable_tuples:
        error_update_sqlstr = None
        if translateable_columnname in translate_label_args:
            error_update_sqlstr = create_knot_exists_in_label_error_update_sqlstr(
                heard_raw_tablename, translateable_columnname
            )
        if translateable_columnname in translate_name_args:
            error_update_sqlstr = create_knot_exists_in_name_error_update_sqlstr(
                heard_raw_tablename, translateable_columnname
            )
        if error_update_sqlstr:
            cursor.execute(error_update_sqlstr)


def get_moment_person_sound_agg_translateable_columns(
    cursor: sqlite3_Cursor, translate_args: set[str]
) -> set[tuple[str, str]]:
    translate_columns = set()
    for x_tablename in get_insert_into_heard_raw_sqlstrs().keys():
        x_tablename = x_tablename.replace("_h_", "_s_")
        x_tablename = x_tablename.replace("_raw", "_agg")
        for columnname in get_table_columns(cursor, x_tablename):
            if columnname in translate_args:
                translate_columns.add((x_tablename, columnname))
    return translate_columns


def populate_translate_core_vld_with_missing_spark_faces(cursor: sqlite3_Cursor):
    for agg_tablename in get_moment_person_sound_agg_tablenames():
        insert_sqlstr = create_insert_missing_spark_face_into_translate_core_vld_sqlstr(
            default_knot=default_knot_if_None(),
            default_unknown=default_unknown_str_if_None(),
            moment_person_sound_agg_tablename=agg_tablename,
        )
        cursor.execute(insert_sqlstr)


def etl_translate_sound_agg_tables_to_translate_sound_vld_tables(
    cursor: sqlite3_Cursor,
):
    insert_translate_sound_agg_into_translate_core_raw_table(cursor)
    update_inconsistency_translate_core_raw_table(cursor)
    insert_translate_core_raw_to_translate_core_agg_table(cursor)
    insert_translate_core_agg_to_translate_core_vld_table(cursor)
    populate_translate_core_vld_with_missing_spark_faces(cursor)
    update_translate_sound_agg_inconsist_errors(cursor)
    update_translate_sound_agg_knot_errors(cursor)
    insert_translate_sound_agg_tables_to_translate_sound_vld_table(cursor)


def etl_sound_agg_tables_to_sound_vld_tables(cursor: sqlite3_Cursor):
    for sqlstr in get_insert_into_sound_vld_sqlstrs().values():
        cursor.execute(sqlstr)


def etl_sound_vld_tables_to_heard_raw_tables(cursor: sqlite3_Cursor):
    for sqlstr in get_insert_into_heard_raw_sqlstrs().values():
        cursor.execute(sqlstr)
