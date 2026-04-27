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
    set_all_heard_raw_inx_columns(cursor)
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
