from ch00_py.csv_toolbox import open_csv_with_types
from ch00_py.db_toolbox import (
    _get_grouping_groupby_clause,
    create_insert_into_clause_str,
    create_select_query,
    create_table_from_columns,
    create_type_reference_insert_sqlstr,
    create_update_inconsistency_error_query,
    db_table_exists,
    get_create_table_sqlstr,
    get_db_tables,
    get_grouping_with_all_values_equal_sql_query,
    get_nonconvertible_columns,
    get_row_count,
    get_table_columns,
)
from ch00_py.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_file,
    open_json,
    save_file,
    save_json,
)
from ch04_rope.rope import create_rope, default_knot_if_None
from ch07_person_logic.person_main import PersonUnit, personunit_shop
from ch08_person_atom.atom_config import get_person_dimens
from ch08_person_atom.atom_main import personatom_shop
from ch09_person_lesson._ref.ch09_path import (
    create_gut_path,
    create_moment_json_path,
    create_moments_dir_path,
)
from ch09_person_lesson.delta import get_minimal_persondelta
from ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from ch09_person_lesson.lesson_main import (
    LessonUnit,
    get_lessonunit_from_dict,
    lessonunit_shop,
)
from ch11_bud._ref.ch11_path import (
    create_person_spark_dir_path,
    create_personspark_path,
    create_spark_all_lesson_path,
)
from ch11_bud.bud_filehandler import (
    collect_person_spark_dir_sets,
    get_persons_downhill_spark_nums,
    open_person_file,
)
from ch16_translate.translate_config import (
    get_translate_args_class_types,
    get_translate_labelterm_args,
    get_translate_nameterm_args,
    get_translate_ropeterm_args,
    get_translate_titleterm_args,
    get_translates_column_ref,
    translateable_class_types,
)
from ch16_translate.translate_main import default_unknown_str_if_None
from ch17_idea.idea_config import (
    get_idea_dimen_ref,
    get_idea_format_filename,
    get_idea_sqlite_types,
    get_idea_types,
    get_idearef_from_file,
)
from ch17_idea.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    split_excel_into_dirs,
)
from ch17_idea.idea_main import get_idearef_obj
from ch18_etl_config._ref.ch18_path import (
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from ch18_etl_config.etl_csv import save_to_split_csvs
from ch18_etl_config.etl_sqlstr import (
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    create_insert_into_translate_core_raw_sqlstr,
    create_insert_missing_spark_face_into_translate_core_vld_sqlstr,
    create_insert_translate_core_agg_into_vld_sqlstr,
    create_insert_translate_sound_vld_table_sqlstr,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
    create_sound_agg_insert_sqlstrs,
    create_sound_and_heard_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    create_update_heard_raw_empty_inx_col_sqlstr,
    create_update_heard_raw_existing_inx_col_sqlstr,
    create_update_translate_sound_agg_inconsist_sqlstr,
    create_update_trllabe_sound_agg_knot_error_sqlstr,
    create_update_trlname_sound_agg_knot_error_sqlstr,
    create_update_trlrope_sound_agg_knot_error_sqlstr,
    create_update_trltitl_sound_agg_knot_error_sqlstr,
    get_insert_heard_agg_sqlstrs,
    get_insert_heard_vld_sqlstrs,
    get_insert_into_heard_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
    get_moment_person_sound_agg_tablenames,
    get_person_heard_vld_tablenames,
    update_heard_agg_timenum_columns,
)
from ch18_etl_config.idea_collector import IdeaFileRef, get_all_ideafilerefs
from ch19_etl_steps._ref.ch19_semantic_types import FaceName, SparkInt
from ch19_etl_steps.obj2db_moment import get_moment_dict_from_heard_tables
from copy import copy as copy_copy, deepcopy as copy_deepcopy
from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor


def etl_idea_dfs_to_ideax_raw_tables(cursor: sqlite3_Cursor, ideas_src_dir: str):
    idea_sqlite_types = get_idea_sqlite_types()

    for ref in get_all_ideafilerefs(ideas_src_dir):
        x_file_path = create_path(ref.file_dir, ref.filename)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        idea_sorting_columns = get_default_sorted_list(set(df.columns))
        df = df.reindex(columns=idea_sorting_columns)
        df.sort_values(idea_sorting_columns, inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=["index"], inplace=True)
        df.insert(0, "file_dir", ref.file_dir)
        df.insert(1, "filename", ref.filename)
        df.insert(2, "sheet_name", ref.sheet_name)
        x_tablename = f"{ref.idea_type}_ideax_raw"
        column_names = list(df.columns)
        column_names.append("error_message")
        create_table_sqlstr = get_create_table_sqlstr(
            x_tablename, column_names, idea_sqlite_types
        )
        cursor.execute(create_table_sqlstr)

        for idx, row in df.iterrows():
            _insert_row_into_ideax_raw_table(
                cursor, x_tablename, column_names, row, idea_sqlite_types
            )


def _insert_row_into_ideax_raw_table(
    cursor: sqlite3_Cursor,
    x_tablename: str,
    column_names: list[str],
    row,
    idea_sqlite_types: dict,
):
    row_dict = row.to_dict()
    nonconvertible_columns = get_nonconvertible_columns(row_dict, idea_sqlite_types)
    error_message = None
    if nonconvertible_columns:
        error_message = ""
        for issue_col, issue_value in nonconvertible_columns.items():
            if error_message:
                error_message += ", "
            error_message += f"{issue_col}: {issue_value}"
        error_message = f"Conversion errors: {error_message}"
    row_values = list(row)
    row_values.append(error_message)
    # Set value to None for non-convertible columns
    for x_index, col in enumerate(column_names):
        if nonconvertible_columns.get(col):
            row_values[x_index] = None
    insert_sqlstr = create_type_reference_insert_sqlstr(
        x_tablename, column_names, [row_values]
    )
    cursor.execute(insert_sqlstr)


def get_existing_excel_idea_file_refs(x_dir: str) -> list[IdeaFileRef]:
    existing_excel_idea_filepaths = []
    for idea_type in sorted(get_idea_types()):
        idea_filename = f"{idea_type}.xlsx"
        x_idea_path = create_path(x_dir, idea_filename)
        if os_path_exists(x_idea_path):
            x_fileref = IdeaFileRef(x_dir, idea_filename, idea_type=idea_type)
            existing_excel_idea_filepaths.append(x_fileref)
    return existing_excel_idea_filepaths


def etl_ideax_raw_tables_to_ideax_agg_tables(conn_or_cursor: sqlite3_Connection):
    ideax_raw_dict = {f"{idea}_ideax_raw": idea for idea in get_idea_types()}
    ideax_raw_tables = set(ideax_raw_dict.keys())
    for x_tablename in get_db_tables(conn_or_cursor):
        if x_tablename in ideax_raw_tables:
            idea_type = ideax_raw_dict.get(x_tablename)
            idea_filename = get_idea_format_filename(idea_type)
            idearef = get_idearef_obj(idea_filename)
            key_columns_set = set(idearef.get_otx_keys_list())
            idea_columns_set = set(idearef.attributes.keys())
            value_columns_set = idea_columns_set.difference(key_columns_set)
            idea_columns = get_default_sorted_list(idea_columns_set)
            key_columns_list = get_default_sorted_list(key_columns_set, idea_columns)
            value_columns_list = get_default_sorted_list(
                value_columns_set, idea_columns
            )
            agg_tablename = f"{idea_type}_ideax_agg"
            if not db_table_exists(conn_or_cursor, agg_tablename):
                create_idea_sorted_table(conn_or_cursor, agg_tablename, idea_columns)
            select_sqlstr = get_grouping_with_all_values_equal_sql_query(
                x_table=x_tablename,
                groupby_columns=key_columns_list,
                value_columns=value_columns_list,
                where_clause="WHERE error_message IS NULL",
            )
            insert_clause_sqlstr = create_insert_into_clause_str(
                conn_or_cursor,
                agg_tablename,
                columns_set=set(idearef.attributes.keys()),
            )
            insert_from_select_sqlstr = f"""
{insert_clause_sqlstr}
{select_sqlstr};"""
            conn_or_cursor.execute(insert_from_select_sqlstr)


def etl_ideax_agg_tables_to_ideax_vld_tables(conn_or_cursor: sqlite3_Connection):
    idea_sqlite_types = get_idea_sqlite_types()
    ideax_agg_dict = {f"{idea}_ideax_agg": idea for idea in get_idea_types()}
    ideax_agg_tables = set(ideax_agg_dict.keys())
    for x_tablename in get_db_tables(conn_or_cursor):
        if x_tablename in ideax_agg_tables:
            idea_type = ideax_agg_dict.get(x_tablename)
            valid_tablename = f"{idea_type}_ideax_vld"
            agg_columns = get_table_columns(conn_or_cursor, x_tablename)
            create_table_from_columns(
                conn_or_cursor,
                tablename=valid_tablename,
                columns_list=agg_columns,
                column_types=idea_sqlite_types,
            )
            agg_cols_set = set(agg_columns)
            insert_clause_str = create_insert_into_clause_str(
                conn_or_cursor, valid_tablename, agg_cols_set
            )
            select_sqlstr = create_select_query(
                conn_or_cursor, x_tablename, agg_columns
            )
            select_sqlstr = select_sqlstr.replace("spark_num", "agg.spark_num")
            select_sqlstr = select_sqlstr.replace("spark_face", "agg.spark_face")
            select_sqlstr = select_sqlstr.replace(x_tablename, f"{x_tablename} agg")
            join_clause_str = """JOIN sparks_ideax_vld valid_sparks ON valid_sparks.spark_num = agg.spark_num"""
            insert_select_into_sqlstr = f"""
{insert_clause_str}
{select_sqlstr}{join_clause_str}
"""
            conn_or_cursor.execute(insert_select_into_sqlstr)


def etl_ideax_agg_tables_to_sparks_ideax_agg_table(conn_or_cursor: sqlite3_Cursor):
    idea_sparks_tablename = "sparks_ideax_agg"
    if not db_table_exists(conn_or_cursor, idea_sparks_tablename):
        idea_sparks_columns = [
            "idea_type",
            "spark_face",
            "spark_num",
            "error_message",
        ]
        create_idea_sorted_table(
            conn_or_cursor, idea_sparks_tablename, idea_sparks_columns
        )

    ideax_agg_tables = {f"{idea}_ideax_agg": idea for idea in get_idea_types()}
    for agg_tablename in get_db_tables(conn_or_cursor):
        if agg_tablename in ideax_agg_tables:
            idea_type = ideax_agg_tables.get(agg_tablename)
            insert_from_select_sqlstr = f"""
INSERT INTO {idea_sparks_tablename} (idea_type, spark_num, spark_face)
SELECT '{idea_type}', spark_num, spark_face 
FROM {agg_tablename}
GROUP BY spark_num, spark_face
;
"""
            conn_or_cursor.execute(insert_from_select_sqlstr)

    update_error_message_sqlstr = f"""
UPDATE {idea_sparks_tablename}
SET error_message = 'invalid because of conflicting spark_num'
WHERE spark_num IN (
    SELECT spark_num 
    FROM {idea_sparks_tablename} 
    GROUP BY spark_num 
    HAVING MAX(spark_face) <> MIN(spark_face)
)
;
"""
    conn_or_cursor.execute(update_error_message_sqlstr)


def etl_sparks_ideax_agg_table_to_sparks_ideax_vld_table(
    conn_or_cursor: sqlite3_Cursor,
):
    valid_sparks_tablename = "sparks_ideax_vld"
    if not db_table_exists(conn_or_cursor, valid_sparks_tablename):
        idea_sparks_columns = ["spark_num", "spark_face"]
        create_idea_sorted_table(
            conn_or_cursor, valid_sparks_tablename, idea_sparks_columns
        )
    insert_select_sqlstr = f"""
INSERT INTO {valid_sparks_tablename} (spark_num, spark_face)
SELECT spark_num, spark_face 
FROM sparks_ideax_agg
WHERE error_message IS NULL
;
"""
    conn_or_cursor.execute(insert_select_sqlstr)


def etl_sparks_ideax_agg_db_to_spark_dict(
    conn_or_cursor: sqlite3_Cursor,
) -> dict[SparkInt, FaceName]:
    select_sqlstr = """
SELECT spark_num, spark_face 
FROM sparks_ideax_vld
;
"""
    conn_or_cursor.execute(select_sqlstr)
    return {int(row[0]): row[1] for row in conn_or_cursor.fetchall()}


def get_ideax_vld_tables(cursor: sqlite3_Cursor) -> dict[str, str]:
    possible_ideax_vld_tables = {f"ideax_vld_{idea}": idea for idea in get_idea_types()}
    active_tables = get_db_tables(cursor)
    return {
        active_table: possible_ideax_vld_tables.get(active_table)
        for active_table in active_tables
        if active_table in possible_ideax_vld_tables
    }


def get_sound_raw_tablenames(
    cursor: sqlite3_Cursor, dimens: list[str], ideax_vld_tablename: str
) -> set[str]:
    valid_columns = set(get_table_columns(cursor, ideax_vld_tablename))
    s_raw_tables = set()
    for dimen in dimens:
        if dimen.lower().startswith("person"):
            person_del_tablename = create_prime_tablename(dimen, "s_raw", "del")
            person_del_columns = get_table_columns(cursor, person_del_tablename)
            delete_key = person_del_columns[-1]
            if delete_key in valid_columns:
                s_raw_tables.add(person_del_tablename)
            else:
                s_raw_tables.add(create_prime_tablename(dimen, "s_raw", "put"))
        else:
            s_raw_tables.add(create_prime_tablename(dimen, "s_raw"))
    return s_raw_tables


def etl_ideax_vld_table_into_prime_table(
    cursor: sqlite3_Cursor,
    ideax_vld_table: str,
    raw_tablename: str,
    idea_type: str,
):
    lab_columns = set(get_table_columns(cursor, raw_tablename))
    valid_columns = set(get_table_columns(cursor, ideax_vld_table))
    common_cols = lab_columns & (valid_columns)
    common_cols = get_default_sorted_list(common_cols)
    select_str = create_select_query(cursor, ideax_vld_table, common_cols)
    select_str = select_str.replace("SELECT", f"SELECT '{idea_type}',")
    common_cols = set(common_cols)
    common_cols.add("idea_type")
    common_cols = get_default_sorted_list(common_cols)
    c_cols = set(common_cols)
    insert_clause_str = create_insert_into_clause_str(cursor, raw_tablename, c_cols)
    insert_select_sqlstr = f"{insert_clause_str}\n{select_str};"
    cursor.execute(insert_select_sqlstr)


def etl_ideax_vld_tables_to_sound_raw_tables(cursor: sqlite3_Cursor):
    create_sound_and_heard_tables(cursor)
    ideax_vld_tablenames = get_db_tables(cursor, "_ideax_vld", "ii")
    for ideax_vld_tablename in ideax_vld_tablenames:
        idea_type = ideax_vld_tablename[:7]
        idearef_filename = get_idea_format_filename(idea_type)
        idearef = get_idearef_from_file(idearef_filename)
        dimens = idearef.get("dimens")
        s_raw_tables = get_sound_raw_tablenames(cursor, dimens, ideax_vld_tablename)
        for sound_raw_table in s_raw_tables:
            etl_ideax_vld_table_into_prime_table(
                cursor, ideax_vld_tablename, sound_raw_table, idea_type
            )


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
