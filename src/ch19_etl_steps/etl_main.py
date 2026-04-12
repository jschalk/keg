from copy import copy as copy_copy, deepcopy as copy_deepcopy
from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor
from src.ch00_py.csv_toolbox import open_csv_with_types
from src.ch00_py.db_toolbox import (
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
from src.ch00_py.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_file,
    open_json,
    save_file,
    save_json,
)
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch08_person_atom.atom_config import get_person_dimens
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson._ref.ch09_path import (
    create_gut_path,
    create_moment_json_path,
    create_moments_dir_path,
)
from src.ch09_person_lesson.delta import get_minimal_persondelta
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_person_lesson.lesson_main import (
    LessonUnit,
    get_lessonunit_from_dict,
    lessonunit_shop,
)
from src.ch10_person_listen.keep_tool import open_job_file
from src.ch11_bud._ref.ch11_path import (
    create_person_spark_dir_path,
    create_personspark_path,
    create_spark_all_lesson_path,
)
from src.ch11_bud.bud_filehandler import (
    collect_person_spark_dir_sets,
    get_persons_downhill_spark_nums,
    open_person_file,
)
from src.ch11_bud.bud_main import TranBook
from src.ch14_moment.moment_cell import (
    create_bud_mandate_ledgers,
    create_moment_persons_cell_trees,
    set_cell_tree_cell_mandates,
    set_cell_trees_decrees,
    set_cell_trees_found_facts,
)
from src.ch14_moment.moment_main import open_moment_file
from src.ch16_translate.translate_config import (
    get_translate_args_class_types,
    get_translate_labelterm_args,
    get_translate_nameterm_args,
    get_translate_ropeterm_args,
    get_translate_titleterm_args,
    get_translates_column_ref,
    translateable_class_types,
)
from src.ch16_translate.translate_main import default_unknown_str_if_None
from src.ch17_idea.idea_config import (
    get_idea_dimen_ref,
    get_idea_format_filename,
    get_idea_sqlite_types,
    get_idea_types,
    get_idearef_from_file,
)
from src.ch17_idea.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    split_excel_into_dirs,
)
from src.ch17_idea.idea_main import get_idearef_obj
from src.ch18_etl_config._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from src.ch18_etl_config.etl_csv import save_to_split_csvs
from src.ch18_etl_config.etl_sqlstr import (
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    create_insert_into_translate_core_raw_sqlstr,
    create_insert_missing_spark_face_into_translate_core_vld_sqlstr,
    create_insert_translate_core_agg_into_vld_sqlstr,
    create_insert_translate_sound_vld_table_sqlstr,
    create_job_tables,
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
from src.ch18_etl_config.idea_collector import IdeaFileRef, get_all_idea_dataframes
from src.ch19_etl_steps._ref.ch19_semantic_types import FaceName, SparkInt
from src.ch19_etl_steps.obj2db_moment import get_moment_dict_from_heard_tables
from src.ch19_etl_steps.obj2db_person import insert_job_obj


def etl_idea_dfs_to_ideax_raw_tables(cursor: sqlite3_Cursor, ideas_src_dir: str):
    idea_sqlite_types = get_idea_sqlite_types()

    for ref in get_all_idea_dataframes(ideas_src_dir):
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
            row_dict = row.to_dict()
            nonconvertible_columns = get_nonconvertible_columns(
                row_dict, idea_sqlite_types
            )
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


def get_max_ideax_agg_spark_num(cursor: sqlite3_Cursor) -> int:
    agg_tables = get_db_tables(cursor, "ideax_agg")
    ideax_aggs_max_spark_num = 0
    for agg_table in agg_tables:
        if agg_table.startswith("ii") and agg_table.endswith("ideax_agg"):
            sqlstr = f"SELECT MAX(spark_num) FROM {agg_table}"
            table_max_spark_num = cursor.execute(sqlstr).fetchone()[0] or 1
            if table_max_spark_num > ideax_aggs_max_spark_num:
                ideax_aggs_max_spark_num = table_max_spark_num
    return ideax_aggs_max_spark_num


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


def ideax_vld_tables_to_translate_prime_raw_tables(cursor: sqlite3_Cursor):
    ideax_vld_tables = get_ideax_vld_tables(cursor)
    idea_dimen_ref = {
        translate_dimen: idea_types
        for translate_dimen, idea_types in get_idea_dimen_ref().items()
        if translate_dimen[:6] == "translate"
    }
    translate_raw_tables = {}
    for translate_dimen in idea_dimen_ref:
        idea_types = idea_dimen_ref.get(translate_dimen)
        raw_tablename = f"{translate_dimen}_raw"
        translate_raw_tables[raw_tablename] = idea_types

    for ideax_vld_table, idea_type in ideax_vld_tables.items():
        for raw_tablename, idea_types in translate_raw_tables.items():
            if idea_type in idea_types:
                etl_ideax_vld_table_into_old_prime_table(
                    cursor, ideax_vld_table, raw_tablename, idea_type
                )


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
    set_all_heard_raw_inx_columns(cursor)


def set_all_heard_raw_inx_columns(cursor: sqlite3_Cursor):
    translate_args = get_translate_args_class_types()
    for heard_raw_tablename, otx_columnname in get_all_heard_raw_otx_columns(cursor):
        columnname_without_otx = otx_columnname[:-4]
        x_arg = copy_copy(columnname_without_otx)
        if x_arg[-5:] == "ERASE":
            x_arg = x_arg[:-6]
        arg_class_type = translate_args.get(x_arg)
        set_heard_raw_inx_column(
            cursor, heard_raw_tablename, columnname_without_otx, arg_class_type
        )


def get_all_heard_raw_otx_columns(cursor: sqlite3_Cursor) -> set[tuple[str, str]]:
    """Returns tuple of all columns ending in 'otx'. Tuple: (TableName, ColumnName)"""

    otx_tble_columns = set()
    for heard_raw_tablename in get_insert_into_heard_raw_sqlstrs().keys():
        for columnname in get_table_columns(cursor, heard_raw_tablename):
            if columnname[-3:] in {"otx"}:
                otx_tble_columns.add((heard_raw_tablename, columnname))
    return otx_tble_columns


def set_heard_raw_inx_column(
    cursor: sqlite3_Cursor,
    heard_raw_tablename: str,
    column_without_otx: str,
    arg_class_type: str,
):
    if arg_class_type in translateable_class_types():
        translate_type_abbv = None
        if arg_class_type == "NameTerm":
            translate_type_abbv = "name"
        elif arg_class_type == "TitleTerm":
            translate_type_abbv = "title"
        elif arg_class_type == "LabelTerm":
            translate_type_abbv = "label"
        elif arg_class_type == "RopeTerm":
            translate_type_abbv = "rope"
        update_calc_inx_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            translate_type_abbv, heard_raw_tablename, column_without_otx
        )
        cursor.execute(update_calc_inx_sqlstr)
    update_empty_inx_sqlstr = create_update_heard_raw_empty_inx_col_sqlstr(
        heard_raw_tablename, column_without_otx
    )
    cursor.execute(update_empty_inx_sqlstr)


def etl_heard_raw_tables_to_heard_agg_tables(cursor: sqlite3_Cursor):
    for insert_heard_agg_sqlstr in get_insert_heard_agg_sqlstrs().values():
        cursor.execute(insert_heard_agg_sqlstr)
    update_heard_agg_timenum_columns(cursor)


def etl_heard_agg_tables_to_heard_vld_tables(cursor: sqlite3_Cursor):
    for insert_heard_vld_sqlstr in get_insert_heard_vld_sqlstrs().values():
        cursor.execute(insert_heard_vld_sqlstr)


def etl_heard_vld_tables_to_moment_jsons(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    select_moment_rope_sqlstr = """SELECT moment_rope FROM momentunit_h_vld;"""
    cursor.execute(select_moment_rope_sqlstr)
    for moment_label_set in cursor.fetchall():
        moment_label = moment_label_set[0]
        moment_dict = get_moment_dict_from_heard_tables(cursor, moment_label)
        moment_lasso = lassounit_shop(create_rope(moment_label))
        moment_json_path = create_moment_json_path(moment_mstr_dir, moment_lasso)
        save_json(moment_json_path, None, moment_dict)


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


def etl_ideax_vld_table_into_old_prime_table(
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
    group_by_clause_str = _get_grouping_groupby_clause(common_cols)
    # tension
    common_cols.append("idea_type")
    common_cols = get_default_sorted_list(common_cols)
    x_dict = {common_col: None for common_col in common_cols}
    insert_clause_str = create_insert_into_clause_str(cursor, raw_tablename, x_dict)
    insert_select_sqlstr = f"{insert_clause_str}\n{select_str}{group_by_clause_str}"
    cursor.execute(insert_select_sqlstr)


def split_excel_into_sparks_dirs(translate_file: str, face_dir: str, sheet_name: str):
    split_excel_into_dirs(
        translate_file, face_dir, "spark_num", "translate", sheet_name
    )


def get_most_recent_spark_num(
    spark_set: set[SparkInt], max_spark_num: SparkInt
) -> SparkInt:
    recent_spark_nums = [e_id for e_id in spark_set if e_id <= max_spark_num]
    return max(recent_spark_nums, default=None)


def etl_heard_raw_tables_to_moment_ote1_agg(conn_or_cursor: sqlite3_Connection):
    """Create Database Table that holds all spark_num to bud_time pairs. Include moment_rope and person_name"""
    conn_or_cursor.execute(CREATE_MOMENT_OTE1_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR)


def etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs(
    conn_or_cursor: sqlite3_Connection, moment_mstr_dir: str
):
    empty_ote1_csv_str = """moment_rope,person_name,spark_num,bud_time,error_message
"""
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        ote1_csv_path = create_moment_ote1_csv_path(moment_mstr_dir, moment_lasso)
        save_file(ote1_csv_path, None, empty_ote1_csv_str)

    save_to_split_csvs(conn_or_cursor, "moment_ote1_agg", ["moment_rope"], moments_dir)


def etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir: str):
    idea_types = get_idea_sqlite_types()
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        csv_path = create_moment_ote1_csv_path(moment_mstr_dir, moment_lasso)
        csv_arrays = open_csv_with_types(csv_path, idea_types)
        x_dict = {}
        header_row = csv_arrays.pop(0)
        for row in csv_arrays:
            person_name = row[1]
            spark_num = row[2]
            bud_time = row[3]
            if x_dict.get(person_name) is None:
                x_dict[person_name] = {}
            person_dict = x_dict.get(person_name)
            person_dict[int(bud_time)] = spark_num
        json_path = create_moment_ote1_json_path(moment_mstr_dir, moment_lasso)
        save_json(json_path, None, x_dict)


def etl_create_buds_root_cells(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_dir = create_path(moments_dir, moment_label)
        moment_lasso = lassounit_shop(create_rope(moment_label))
        ote1_json_path = create_path(moment_dir, "moment_ote1_agg.json")
        if os_path_exists(ote1_json_path):
            ote1_dict = open_json(ote1_json_path)
            x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
            x_momentunit.create_buds_root_cells(ote1_dict)


def etl_create_moment_cell_trees(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        create_moment_persons_cell_trees(moment_mstr_dir, moment_lasso)


def etl_set_cell_trees_found_facts(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        set_cell_trees_found_facts(moment_mstr_dir, moment_lasso)


def etl_set_cell_trees_decrees(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        set_cell_trees_decrees(moment_mstr_dir, moment_lasso)


def etl_set_cell_tree_cell_mandates(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        set_cell_tree_cell_mandates(moment_mstr_dir, moment_lasso)


def etl_create_bud_mandate_ledgers(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        create_bud_mandate_ledgers(moment_mstr_dir, moment_lasso)


def etl_heard_vld_to_spark_person_csvs(
    conn_or_cursor: sqlite3_Connection, moment_mstr_dir: str
):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for person_table in get_person_heard_vld_tablenames():
        if get_row_count(conn_or_cursor, person_table) > 0:
            table_columns = set(get_table_columns(conn_or_cursor, person_table))
            key_columns = ["moment_rope", "person_name", "spark_num"]
            if "moment_rope" not in table_columns:
                key_columns = ["plan_rope", "person_name", "spark_num"]
            save_to_split_csvs(
                conn_or_cursor=conn_or_cursor,
                tablename=person_table,
                key_columns=key_columns,
                dst_dir=moments_dir,
                col1_prefix="persons",
                col2_prefix="sparks",
            )


def etl_spark_person_csvs_to_lesson_json(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        moment_path = create_path(moments_dir, moment_lasso.make_path())
        persons_path = create_path(moment_path, "persons")
        for person_name in get_level1_dirs(persons_path):
            person_path = create_path(persons_path, person_name)
            sparks_path = create_path(person_path, "sparks")
            for spark_num in get_level1_dirs(sparks_path):
                save_spark_lesson_json(
                    moment_mstr_dir, moment_lasso, person_name, spark_num, sparks_path
                )


def save_spark_lesson_json(
    moment_mstr_dir, moment_lasso, person_name, spark_num, sparks_path
):
    spark_lesson = lessonunit_shop(
        person_name=person_name,
        spark_face=None,
        moment_rope=moment_lasso.moment_rope,
        spark_num=spark_num,
    )
    spark_dir = create_path(sparks_path, spark_num)
    add_personatoms_from_csv(spark_lesson, spark_dir)
    spark_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    spark_lesson_json = spark_lesson.get_serializable_step_dict()
    save_json(spark_all_lesson_path, None, spark_lesson_json)


def add_personatoms_from_csv(spark_lesson: LessonUnit, spark_dir: str):
    idea_sqlite_types = get_idea_sqlite_types()
    person_dimens = get_person_dimens()
    person_dimens.remove("personunit")
    for person_dimen in person_dimens:
        person_dimen_put_tablename = create_prime_tablename(
            person_dimen, "h_vld", "put"
        )
        person_dimen_del_tablename = create_prime_tablename(
            person_dimen, "h_vld", "del"
        )
        person_dimen_put_csv = f"{person_dimen_put_tablename}.csv"
        person_dimen_del_csv = f"{person_dimen_del_tablename}.csv"
        put_path = create_path(spark_dir, person_dimen_put_csv)
        del_path = create_path(spark_dir, person_dimen_del_csv)
        if os_path_exists(put_path):
            put_rows = open_csv_with_types(put_path, idea_sqlite_types)
            headers = put_rows.pop(0)
            for put_row in put_rows:
                x_atom = personatom_shop(person_dimen, "INSERT")
                for col_name, row_value in zip(headers, put_row):
                    if col_name not in {
                        "spark_face",
                        "spark_num",
                        "moment_rope",
                        "person_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                spark_lesson.persondelta.set_personatom(x_atom)

        if os_path_exists(del_path):
            del_rows = open_csv_with_types(del_path, idea_sqlite_types)
            headers = del_rows.pop(0)
            for del_row in del_rows:
                x_atom = personatom_shop(person_dimen, "DELETE")
                for col_name, row_value in zip(headers, del_row):
                    if col_name not in {
                        "spark_face",
                        "spark_num",
                        "moment_rope",
                        "person_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                spark_lesson.persondelta.set_personatom(x_atom)


def etl_spark_lesson_json_to_spark_inherited_personunits(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_path = create_path(moments_dir, moment_label)
        moment_rope = create_rope(moment_label)
        moment_lasso = lassounit_shop(moment_rope)
        persons_dir = create_path(moment_path, "persons")
        for person_name in get_level1_dirs(persons_dir):
            person_dir = create_path(persons_dir, person_name)
            sparks_dir = create_path(person_dir, "sparks")
            prev_spark_num = None
            for spark_num in get_level1_dirs(sparks_dir):
                prev_spark_num = create_lesson_json_and_get_spark_num(
                    moment_mstr_dir,
                    moment_lasso,
                    person_name,
                    prev_spark_num,
                    spark_num,
                )


def create_lesson_json_and_get_spark_num(
    moment_mstr_dir, moment_lasso, person_name, prev_spark_num, spark_num
):
    m_dir = moment_mstr_dir
    m_lasso = moment_lasso
    p_name = person_name
    prev_spark = prev_spark_num

    prev_person = _get_prev_spark_num_personunit(m_dir, m_lasso, p_name, prev_spark)
    personspark_path = create_personspark_path(m_dir, m_lasso, p_name, spark_num)
    spark_dir = create_person_spark_dir_path(m_dir, m_lasso, p_name, spark_num)
    all_lesson_path = create_spark_all_lesson_path(m_dir, m_lasso, p_name, spark_num)
    spark_lesson = get_lessonunit_from_dict(open_json(all_lesson_path))
    sift_delta = get_minimal_persondelta(spark_lesson.persondelta, prev_person)
    curr_person = spark_lesson.get_lesson_edited_person(prev_person)
    save_json(personspark_path, None, curr_person.to_dict())
    expressed_lesson = copy_deepcopy(spark_lesson)
    expressed_lesson.set_persondelta(sift_delta)
    expressed_lesson_json = expressed_lesson.get_serializable_step_dict()
    save_json(spark_dir, "expressed_lesson.json", expressed_lesson_json)
    return spark_num


def _get_prev_spark_num_personunit(
    moment_mstr_dir, moment_lasso: LassoUnit, person_name, prev_spark_num
) -> PersonUnit:
    if prev_spark_num is None:
        return personunit_shop(person_name, moment_lasso.moment_rope)
    prev_personspark_path = create_personspark_path(
        moment_mstr_dir, moment_lasso, person_name, prev_spark_num
    )
    return open_person_file(prev_personspark_path)


def etl_spark_inherited_personunits_to_moment_gut(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        person_sparks = collect_person_spark_dir_sets(moment_mstr_dir, moment_lasso)
        persons_max_spark_num_dict = get_persons_downhill_spark_nums(person_sparks)
        for person_name, max_spark_num in persons_max_spark_num_dict.items():
            max_personspark_path = create_personspark_path(
                moment_mstr_dir, moment_lasso, person_name, max_spark_num
            )
            max_spark_person_json = open_file(max_personspark_path)
            gut_path = create_gut_path(moment_mstr_dir, moment_lasso, person_name)
            save_file(gut_path, None, max_spark_person_json)


def add_moment_epoch_to_guts(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        x_momentunit.add_epoch_to_guts()


def etl_moment_guts_to_moment_jobs(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        x_momentunit.generate_all_jobs()


def etl_moment_job_jsons_to_job_tables(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    create_job_tables(cursor)
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_rope = create_rope(moment_label)
        moment_lasso = lassounit_shop(moment_rope)
        moment_path = create_path(moments_dir, moment_label)
        persons_dir = create_path(moment_path, "persons")
        for person_name in get_level1_dirs(persons_dir):
            job_obj = open_job_file(moment_mstr_dir, moment_lasso, person_name)
            insert_job_obj(cursor, job_obj)


CREATE_MOMENT_CONTACT_NETS_SQLSTR = "CREATE TABLE IF NOT EXISTS moment_contact_nets (moment_rope TEXT, person_name TEXT, person_net_amount REAL)"


def insert_tranunit_contacts_net(cursor: sqlite3_Cursor, tranbook: TranBook):
    """
    Insert the net amounts for each contact in the tranbook into the specified table.

    :param cursor: SQLite cursor object
    :param tranbook: TranBook object containing transaction units
    :param dst_tablename: Name of the destination table
    """
    contacts_net_array = tranbook._get_contacts_net_array()
    cursor.executemany(
        f"INSERT INTO moment_contact_nets (moment_rope, person_name, person_net_amount) VALUES ('{tranbook.moment_rope}', ?, ?)",
        contacts_net_array,
    )


def etl_moment_json_contact_nets_to_moment_contact_nets_table(
    cursor: sqlite3_Cursor, moment_mstr_dir: str
):
    cursor.execute(CREATE_MOMENT_CONTACT_NETS_SQLSTR)
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        x_momentunit.set_all_tranbook()
        insert_tranunit_contacts_net(cursor, x_momentunit.all_tranbook)


def create_last_run_metrics_json(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    max_ideax_agg_spark_num = get_max_ideax_agg_spark_num(cursor)
    last_run_metrics_path = create_last_run_metrics_path(moment_mstr_dir)
    last_run_metrics_dict = {"max_ideax_agg_spark_num": max_ideax_agg_spark_num}
    save_json(last_run_metrics_path, None, last_run_metrics_dict)


def calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir: str):
    etl_create_buds_root_cells(moment_mstr_dir)
    etl_create_moment_cell_trees(moment_mstr_dir)
    etl_set_cell_trees_found_facts(moment_mstr_dir)
    etl_set_cell_trees_decrees(moment_mstr_dir)
    etl_set_cell_tree_cell_mandates(moment_mstr_dir)
    etl_create_bud_mandate_ledgers(moment_mstr_dir)
