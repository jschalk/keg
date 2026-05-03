from ch00_py.db_toolbox import (
    create_insert_into_clause_str,
    create_select_query,
    create_table_from_columns,
    create_type_reference_insert_sqlstr,
    db_table_exists,
    delete_all_duplicate_rows,
    get_create_table_sqlstr,
    get_db_tables,
    get_grouping_with_all_values_equal_sql_query,
    get_nonconvertible_columns,
    get_table_columns,
)
from ch00_py.file_toolbox import create_path
from ch17_brick.brick_config import (
    get_brick_format_filename,
    get_brick_sqlite_types,
    get_brick_types,
    get_brickref_from_file,
)
from ch17_brick.brick_dataframe import get_brickref_obj
from ch17_brick.brick_db_tool import create_brick_sorted_table, get_default_sorted_list
from ch18_etl_config.brick_collector import BrickFileRef, get_all_brickfilerefs
from ch18_etl_config.etl_sqlstr import (
    create_prime_tablename,
    create_sound_and_heard_tables,
)
from ch20_etl_brick._ref.ch20_semantic_types import FaceName, SparkInt
from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor


def etl_brick_dfs_to_brixk_raw_tables(cursor: sqlite3_Cursor, bricks_src_dir: str):
    brick_sqlite_types = get_brick_sqlite_types()
    brickfilerefs = get_all_brickfilerefs(bricks_src_dir)
    for ref in brickfilerefs:
        x_file_path = create_path(ref.file_dir, ref.filename)
        df = pandas_read_excel(x_file_path, ref.sheet_name)
        brick_sorting_columns = get_default_sorted_list(set(df.columns))
        df = df.reindex(columns=brick_sorting_columns)
        df.sort_values(brick_sorting_columns, inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns=["index"], inplace=True)
        df.insert(0, "file_dir", ref.file_dir)
        df.insert(1, "filename", ref.filename)
        df.insert(2, "sheet_name", ref.sheet_name)
        x_tablename = f"{ref.brick_type}_brixk_raw"
        column_names = list(df.columns)
        column_names.append("error_message")
        create_table_sqlstr = get_create_table_sqlstr(
            x_tablename, column_names, brick_sqlite_types
        )
        cursor.execute(create_table_sqlstr)

        for idx, row in df.iterrows():
            _insert_row_into_brixk_raw_table(
                cursor, x_tablename, column_names, row, brick_sqlite_types
            )

    for ref in brickfilerefs:
        x_tablename = f"{ref.brick_type}_brixk_raw"
        delete_all_duplicate_rows(cursor, x_tablename)


def _insert_row_into_brixk_raw_table(
    cursor: sqlite3_Cursor,
    x_tablename: str,
    column_names: list[str],
    row,
    brick_sqlite_types: dict,
):
    row_dict = row.to_dict()
    nonconvertible_columns = get_nonconvertible_columns(row_dict, brick_sqlite_types)
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


def get_existing_excel_brick_file_refs(x_dir: str) -> list[BrickFileRef]:
    existing_excel_brick_filepaths = []
    for brick_type in sorted(get_brick_types()):
        brick_filename = f"{brick_type}.xlsx"
        x_brick_path = create_path(x_dir, brick_filename)
        if os_path_exists(x_brick_path):
            x_fileref = BrickFileRef(x_dir, brick_filename, brick_type=brick_type)
            existing_excel_brick_filepaths.append(x_fileref)
    return existing_excel_brick_filepaths


def etl_brixk_raw_tables_to_brixk_agg_tables(conn_or_cursor: sqlite3_Connection):
    brixk_raw_dict = {f"{brick}_brixk_raw": brick for brick in get_brick_types()}
    brixk_raw_tables = set(brixk_raw_dict.keys())
    for x_tablename in get_db_tables(conn_or_cursor):
        if x_tablename in brixk_raw_tables:
            brick_type = brixk_raw_dict.get(x_tablename)
            brick_filename = get_brick_format_filename(brick_type)
            brickref = get_brickref_obj(brick_filename)
            key_columns_set = set(brickref.get_otx_keys_list())
            brick_columns_set = set(brickref.attributes.keys())
            value_columns_set = brick_columns_set.difference(key_columns_set)
            brick_columns = get_default_sorted_list(brick_columns_set)
            key_columns_list = get_default_sorted_list(key_columns_set, brick_columns)
            value_columns_list = get_default_sorted_list(
                value_columns_set, brick_columns
            )
            agg_tablename = f"{brick_type}_brixk_agg"
            if not db_table_exists(conn_or_cursor, agg_tablename):
                create_brick_sorted_table(conn_or_cursor, agg_tablename, brick_columns)
            select_sqlstr = get_grouping_with_all_values_equal_sql_query(
                x_table=x_tablename,
                groupby_columns=key_columns_list,
                value_columns=value_columns_list,
                where_clause="WHERE error_message IS NULL",
            )
            insert_clause_sqlstr = create_insert_into_clause_str(
                conn_or_cursor,
                agg_tablename,
                columns_set=set(brickref.attributes.keys()),
            )
            insert_from_select_sqlstr = f"""
{insert_clause_sqlstr}
{select_sqlstr};"""
            conn_or_cursor.execute(insert_from_select_sqlstr)
            delete_all_duplicate_rows(conn_or_cursor, agg_tablename)


def etl_brixk_agg_tables_to_brixk_vld_tables(conn_or_cursor: sqlite3_Connection):
    brick_sqlite_types = get_brick_sqlite_types()
    brixk_agg_dict = {f"{brick}_brixk_agg": brick for brick in get_brick_types()}
    brixk_agg_tables = set(brixk_agg_dict.keys())
    for x_tablename in get_db_tables(conn_or_cursor):
        if x_tablename in brixk_agg_tables:
            brick_type = brixk_agg_dict.get(x_tablename)
            valid_tablename = f"{brick_type}_brixk_vld"
            agg_columns = get_table_columns(conn_or_cursor, x_tablename)
            create_table_from_columns(
                conn_or_cursor,
                tablename=valid_tablename,
                columns_list=agg_columns,
                column_types=brick_sqlite_types,
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
            join_clause_str = """JOIN sparks_brixk_vld valid_sparks ON valid_sparks.spark_num = agg.spark_num"""
            insert_select_into_sqlstr = f"""
{insert_clause_str}
{select_sqlstr}{join_clause_str}
"""
            conn_or_cursor.execute(insert_select_into_sqlstr)
            delete_all_duplicate_rows(conn_or_cursor, valid_tablename)


def get_create_sparks_brixk_agg_sqlstr() -> str:
    return "CREATE TABLE IF NOT EXISTS sparks_brixk_agg (brick_type TEXT, spark_num INTEGER, spark_face TEXT, error_message TEXT)"


def etl_brixk_agg_tables_to_sparks_brixk_agg_table(conn_or_cursor: sqlite3_Cursor):
    conn_or_cursor.execute(get_create_sparks_brixk_agg_sqlstr())
    brick_sparks_tablename = "sparks_brixk_agg"
    brixk_agg_tables = {f"{brick}_brixk_agg": brick for brick in get_brick_types()}
    for agg_tablename in get_db_tables(conn_or_cursor):
        if agg_tablename in brixk_agg_tables:
            brick_type = brixk_agg_tables.get(agg_tablename)
            insert_from_select_sqlstr = f"""
INSERT INTO {brick_sparks_tablename} (brick_type, spark_num, spark_face)
SELECT '{brick_type}', spark_num, spark_face 
FROM {agg_tablename}
GROUP BY spark_num, spark_face
;
"""
            conn_or_cursor.execute(insert_from_select_sqlstr)

    update_error_message_sqlstr = f"""
UPDATE {brick_sparks_tablename}
SET error_message = 'invalid because of conflicting spark_num'
WHERE spark_num IN (
    SELECT spark_num 
    FROM {brick_sparks_tablename} 
    GROUP BY spark_num 
    HAVING MAX(spark_face) <> MIN(spark_face)
)
;
"""
    conn_or_cursor.execute(update_error_message_sqlstr)
    delete_all_duplicate_rows(conn_or_cursor, brick_sparks_tablename)


def get_create_sparks_brixk_vld_sqlstr() -> str:
    return "CREATE TABLE IF NOT EXISTS sparks_brixk_vld (spark_num INTEGER, spark_face TEXT)"


def etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table(
    conn_or_cursor: sqlite3_Cursor,
):
    conn_or_cursor.execute(get_create_sparks_brixk_vld_sqlstr())
    valid_sparks_tablename = "sparks_brixk_vld"
    insert_select_sqlstr = f"""
INSERT INTO {valid_sparks_tablename} (spark_num, spark_face)
SELECT spark_num, spark_face 
FROM sparks_brixk_agg
WHERE error_message IS NULL
;
"""
    conn_or_cursor.execute(insert_select_sqlstr)
    delete_all_duplicate_rows(conn_or_cursor, valid_sparks_tablename)


def etl_sparks_brixk_agg_db_to_spark_dict(
    conn_or_cursor: sqlite3_Cursor,
) -> dict[SparkInt, FaceName]:
    select_sqlstr = """
SELECT spark_num, spark_face 
FROM sparks_brixk_vld
;
"""
    conn_or_cursor.execute(select_sqlstr)
    return {int(row[0]): row[1] for row in conn_or_cursor.fetchall()}


def get_sound_raw_tablenames(
    cursor: sqlite3_Cursor, dimens: list[str], brixk_vld_tablename: str
) -> set[str]:
    valid_columns = set(get_table_columns(cursor, brixk_vld_tablename))
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


def etl_brixk_vld_table_into_prime_table(
    cursor: sqlite3_Cursor,
    brixk_vld_table: str,
    raw_tablename: str,
    brick_type: str,
):
    lab_columns = set(get_table_columns(cursor, raw_tablename))
    valid_columns = set(get_table_columns(cursor, brixk_vld_table))
    common_cols = lab_columns & (valid_columns)
    common_cols = get_default_sorted_list(common_cols)
    select_str = create_select_query(cursor, brixk_vld_table, common_cols)
    select_str = select_str.replace("SELECT", f"SELECT '{brick_type}',")
    common_cols = set(common_cols)
    common_cols.add("brick_type")
    common_cols = get_default_sorted_list(common_cols)
    c_cols = set(common_cols)
    insert_clause_str = create_insert_into_clause_str(cursor, raw_tablename, c_cols)
    insert_select_sqlstr = f"{insert_clause_str}\n{select_str};"
    cursor.execute(insert_select_sqlstr)


def etl_brixk_vld_tables_to_sound_raw_tables(cursor: sqlite3_Cursor):
    all_touched_sound_raw_tables = set()
    create_sound_and_heard_tables(cursor)
    brixk_vld_tablenames = get_db_tables(cursor, "_brixk_vld", "bk")
    for brixk_vld_tablename in brixk_vld_tablenames:
        brick_type = brixk_vld_tablename[:7]
        brickref_filename = get_brick_format_filename(brick_type)
        brickref = get_brickref_from_file(brickref_filename)
        dimens = brickref.get("dimens")
        s_raw_tables = get_sound_raw_tablenames(cursor, dimens, brixk_vld_tablename)
        all_touched_sound_raw_tables.update(s_raw_tables)
        for sound_raw_table in s_raw_tables:
            etl_brixk_vld_table_into_prime_table(
                cursor, brixk_vld_tablename, sound_raw_table, brick_type
            )

    for x_sound_raw_table in all_touched_sound_raw_tables:
        delete_all_duplicate_rows(cursor, x_sound_raw_table)
