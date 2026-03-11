from csv import reader as csv_reader
from dataclasses import dataclass
from sqlite3 import Connection as sqlite3_Connection, Error as sqlite3_Error


def sqlite_obj_str(x_obj: any, sqlite_datatype: str):
    if x_obj is None:
        return "NULL"
    elif sqlite_datatype == "TEXT":
        if isinstance(x_obj, bool):
            if x_obj == True:
                return """'TRUE'"""
            elif x_obj == False:
                return """'FALSE'"""
        else:
            return f"""'{x_obj}'"""
    elif sqlite_datatype == "INTEGER":
        if x_obj == True:
            return "1"
        elif x_obj == False:
            return "0"
        else:
            return f"{int(x_obj)}"
    elif sqlite_datatype == "REAL":
        if x_obj == True:
            return "1"
        elif x_obj == False:
            return "0"
        else:
            return f"{x_obj}"


def sqlite_to_python(query_value) -> str:
    """SQLite string to Python None or True"""
    return None if query_value == "NULL" else query_value


def check_connection(conn: sqlite3_Connection) -> bool:
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


def get_sorted_cols_only_list(
    existing_columns: set[str], sorting_columns: list[str]
) -> list[str]:
    sort_columns_in_existing = set(sorting_columns) & existing_columns
    return [x_col for x_col in sorting_columns if x_col in sort_columns_in_existing]


def get_nonconvertible_columns(
    row_dict: dict[str, str], col_types: dict[str, str]
) -> dict[str, str]:
    """
    Returns a list of columns from row_dict that cannot be converted
    to the expected numeric type defined in col_types.

    Parameters:
    - row_dict: dict with column names as keys and cell values.
    - col_types: dict mapping column names to "Integer", "Real", or "Text".

    Returns:
    - Dictionary of column names and the values where numeric conversion fails.
    """
    nonconvertible = {}
    for col, value in row_dict.items():
        expected_type = col_types.get(col)
        if expected_type == "INTEGER":
            try:
                int_val = int(value)
                if isinstance(value, float) and not value.is_integer():
                    raise ValueError("float with decimal")
            except (ValueError, TypeError):
                nonconvertible[col] = value

        elif expected_type == "REAL":
            try:
                float(value)
            except (ValueError, TypeError):
                nonconvertible[col] = value
        elif expected_type and expected_type != "TEXT":
            nonconvertible[col] = value
        # ignore if expected_type == "Text" or expected_type is None:
    return nonconvertible


def create_type_reference_insert_sqlstr(
    x_table: str, x_columns: list[str], x_values: list[list]
) -> str:
    x_str = f"""
INSERT INTO {x_table} ("""

    # Build column list
    columns_str = ""
    for x_column in x_columns:
        if columns_str == "":
            columns_str = f"""{columns_str}
  {x_column}"""
        else:
            columns_str = f"""{columns_str}
, {x_column}"""

    # Build values for multiple rows
    rows_str = ""
    for row in x_values:
        values_str = ""
        for x_value in row:
            if x_value is None:
                x_value = "NULL"
            else:
                try:
                    float(x_value)
                except (ValueError, TypeError):
                    x_value = f"'{x_value}'"

            if values_str == "":
                values_str = f"""{values_str}{x_value}"""
            else:
                values_str = f"""{values_str}, {x_value}"""
        if rows_str == "":
            rows_str = f"""{rows_str}
  ({values_str})"""
        else:
            rows_str = f"""{rows_str}
, ({values_str})"""

    return f"""{x_str}{columns_str}
)
VALUES{rows_str}
;
"""


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


@dataclass
class RowData:
    tablename: str = None
    row_dict: str = None


class row_dict_Exception(Exception):
    pass


def rowdata_shop(
    tablename: str,
    row_dict: str,
):
    if str(type(row_dict)) != "<class 'dict'>":
        raise row_dict_Exception("row_dict is not dictionary")
    x_dict = {
        x_key: x_value for x_key, x_value in row_dict.items() if x_value is not None
    }
    return RowData(tablename, x_dict)


def get_rowdata(
    tablename: str, x_conn: sqlite3_Connection, select_sqlstr: str
) -> RowData:
    x_conn.row_factory = dict_factory
    results = x_conn.execute(select_sqlstr)
    row1 = results.fetchone()
    return rowdata_shop(tablename, row1)


def get_db_tables(
    x_conn: sqlite3_Connection, tablename_contains: str = None, prefix: str = None
) -> dict[str, int]:
    sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
    results = x_conn.execute(sqlstr)
    tablenames_dict = {row[0]: 1 for row in results}
    if tablename_contains:
        new_dict = {}
        for table, dict_value in tablenames_dict.items():
            if not prefix and table.find(tablename_contains) != -1:
                new_dict[table] = dict_value
            elif (
                prefix
                and table.find(prefix) == 0
                and table.find(tablename_contains) != -1
            ):
                new_dict[table] = dict_value
        tablenames_dict = new_dict
    return tablenames_dict


def get_db_columns(x_conn: sqlite3_Connection) -> dict[str : dict[str, int]]:
    return {
        table_name: get_table_columns(x_conn, table_name)
        for table_name in get_db_tables(x_conn).keys()
    }


def get_column_data_type(cursor: sqlite3_Connection, table_name: str, column_name: str):
    """
    Given a cursor object, table name, and column name, return the column's data type for SQLite.

    :param cursor: Database cursor object
    :param table_name: Name of the table
    :param column_name: Name of the column
    :return: Data type of the column as a string
    """
    try:
        # Query to fetch column info for SQLite
        query = f"PRAGMA table_info({table_name})"
        cursor.execute(query)
        columns = cursor.fetchall()
        return next((col[2] for col in columns if col[1] == column_name), None)
    except Exception as e:
        return None


def get_single_result(db_conn: sqlite3_Connection, sqlstr: str) -> any:
    results = db_conn.execute(sqlstr)
    return results.fetchone()[0]


def get_row_count_sqlstr(table_name: str) -> str:
    return f"SELECT COUNT(*) FROM {table_name}"


def get_row_count(db_conn: sqlite3_Connection, table_name: str) -> str:
    return get_single_result(db_conn, get_row_count_sqlstr(table_name))


def _get_grouping_select_clause(
    groupby_columns: list[str], value_columns: list[str]
) -> str:
    select_str = "SELECT"
    for groupby_column in groupby_columns:
        select_str += f" {groupby_column},"
    for value_column in value_columns:
        select_str += f" MAX({value_column}) AS {value_column},"
    return _remove_comma_at_end(select_str)


def _remove_comma_at_end(x_str: str) -> str:
    return x_str.removesuffix(",")


def _get_grouping_groupby_clause(groupby_columns: list[str]) -> str:
    groupby_str = "GROUP BY"
    for groupby_column in groupby_columns:
        groupby_str += f" {groupby_column},"
    return _remove_comma_at_end(groupby_str)


def _get_having_equal_value_clause(value_columns: list[str]) -> str:
    if not value_columns:
        return ""
    having_clause = "HAVING"
    for value_column in value_columns:
        if having_clause != "HAVING":
            having_clause += " AND"
        having_clause += f" MIN({value_column}) = MAX({value_column})"
    return _remove_comma_at_end(having_clause)


def get_groupby_sql_query(
    x_table: str,
    groupby_columns: list[str],
    value_columns: list[str],
    where_clause: str = None,
) -> str:
    where_clause = f"{where_clause} " if where_clause else ""
    return f"{_get_grouping_select_clause(groupby_columns, value_columns)} FROM {x_table} {where_clause}{_get_grouping_groupby_clause(groupby_columns)}"


def get_grouping_with_all_values_equal_sql_query(
    x_table: str,
    groupby_columns: list[str],
    value_columns: list[str],
    where_clause: str = None,
) -> str:
    where_clause = f"{where_clause} " if where_clause else ""
    return f"{_get_grouping_select_clause(groupby_columns, value_columns)} FROM {x_table} {where_clause}{_get_grouping_groupby_clause(groupby_columns)} {_get_having_equal_value_clause(value_columns)}"


class insert_csv_Exception(Exception):
    pass


def insert_csv(csv_file_path: str, conn_or_cursor: sqlite3_Connection, table_name: str):
    """
    Inserts data from a CSV file into a specified SQLite database table.

    Args:
        csv_file_path (str): Path to the CSV file.
        conn_or_cursor (sqlite3.Connection): SQLite database connection object.
        table_name (str): Name of the table to insert data into.

    Returns:
        None
    """
    try:
        # Open the CSV file
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv_reader(csv_file)

            # Extract the header row from the CSV file
            headers = next(reader)

            # Create a parameterized SQL query for inserting data
            placeholders = ", ".join(["?"] * len(headers))
            insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
            # Insert each row into the database
            for row in reader:
                conn_or_cursor.execute(insert_query, row)

    except sqlite3_Error as e:
        raise insert_csv_Exception(f"SQLite error: {e}") from e

    except Exception as e:
        raise insert_csv_Exception(f"Error: {e}") from e


class sqlite3_Error_Exception(Exception):
    pass


def get_create_table_sqlstr(
    tablename: str,
    columns_list: list[str],
    column_types: dict[str, str],
) -> str:
    # Dynamically create a table schema based on the provided column types
    columns = []
    for column in columns_list:
        data_type = column_types.get(column, "TEXT")  # Default to TEXT
        columns.append(f"{column} {data_type}")
    columns_definition = ", ".join(columns)
    return f"CREATE TABLE IF NOT EXISTS {tablename} ({columns_definition})"


def create_table_from_columns(
    conn_or_cursor: sqlite3_Connection,
    tablename: str,
    columns_list: list[str],
    column_types: dict[str, str],
):
    x_sqlstr = get_create_table_sqlstr(tablename, columns_list, column_types)
    conn_or_cursor.execute(x_sqlstr)


def create_table_from_csv(
    csv_file_path: str,
    conn_or_cursor: sqlite3_Connection,
    table_name: str,
    column_types: dict[str, str],
):
    """
    Creates a SQLite table based on the header of a CSV file and a dictionary of column names and their data types.

    Args:
        csv_file_path (str): Path to the CSV file.
        conn_or_cursor (sqlite3.Connection): SQLite database connection object.
        table_name (str): Name of the table to create.
        column_types (dict): Dictionary mapping column names to their SQLite data types.

    Returns:
        None
    """
    try:
        # Open the CSV file to read the header
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            headers = csv_file.readline().strip().split(",")
        create_table_from_columns(conn_or_cursor, table_name, headers, column_types)

    except sqlite3_Error as e:
        raise sqlite3_Error_Exception(f"SQLite error: {e}") from e

    # except Exception as e:
    #     raise Exception(f"Error: {e}")


def db_table_exists(conn_or_cursor: sqlite3_Connection, tablename: str) -> bool:
    table_master_sqlstr = (
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}';"
    )
    result = conn_or_cursor.execute(table_master_sqlstr).fetchone()
    return bool(result)


def get_table_columns(conn_or_cursor: sqlite3_Connection, tablename: str) -> list[str]:
    db_columns = conn_or_cursor.execute(f"PRAGMA table_info({tablename})").fetchall()
    if db_columns and isinstance(db_columns[0], dict):
        return [db_column.get("name") for db_column in db_columns]
    return [db_column[1] for db_column in db_columns]


def create_select_inconsistency_query(
    conn_or_cursor: sqlite3_Connection,
    x_tablename: str,
    focus_columns: set[str],
    exclude_columns: set[str],
) -> str:
    table_columns = get_table_columns(conn_or_cursor, x_tablename)
    having_str = None
    for x_column in table_columns:
        if x_column not in exclude_columns and x_column not in focus_columns:
            if having_str:
                having_str += f"\n    OR MIN({x_column}) != MAX({x_column})"
            else:
                having_str = f"HAVING MIN({x_column}) != MAX({x_column})"
    if not having_str:
        having_str = "HAVING 1=2"
    focus_columns_list = []
    focus_columns_list.extend(
        t_column
        for t_column in table_columns
        if t_column not in exclude_columns and t_column in focus_columns
    )
    focus_columns_str = ", ".join(focus_columns_list)
    return f"""SELECT {focus_columns_str}
FROM {x_tablename}
GROUP BY {focus_columns_str}
{having_str}
"""


def create_update_inconsistency_error_query(
    conn_or_cursor: sqlite3_Connection,
    x_tablename: str,
    focus_columns: set[str],
    exclude_columns: set[str],
    error_holder_column: str,
    error_str: str,
):
    select_inconsistency_query = create_select_inconsistency_query(
        conn_or_cursor, x_tablename, focus_columns, exclude_columns
    )
    table_columns = get_table_columns(conn_or_cursor, x_tablename)
    where_str = None
    for x_column in table_columns:
        if x_column not in exclude_columns and x_column in focus_columns:
            if where_str:
                where_str += f"\n    AND inconsistency_rows.{x_column} = {x_tablename}.{x_column}"
            else:
                where_str = (
                    f"WHERE inconsistency_rows.{x_column} = {x_tablename}.{x_column}"
                )

    return f"""WITH inconsistency_rows AS (
{select_inconsistency_query})
UPDATE {x_tablename}
SET {error_holder_column} = '{error_str}'
FROM inconsistency_rows
{where_str}
;
"""


def create_table2table_agg_insert_query(
    conn_or_cursor: sqlite3_Connection,
    src_table: str,
    dst_table: str,
    focus_cols: list[str],
    exclude_cols: set[str],
    where_block: str,
) -> str:
    if not focus_cols:
        focus_cols = set(get_table_columns(conn_or_cursor, dst_table))
    focus_cols_set = set(focus_cols)
    dst_columns = get_table_columns(conn_or_cursor, dst_table)
    focus_col_list = get_sorted_cols_only_list(focus_cols_set, dst_columns)
    dst_columns = [dst_col for dst_col in dst_columns if dst_col not in exclude_cols]
    dst_columns_str = ", ".join(list(dst_columns))
    select_columns_str = None
    for dst_column in dst_columns:
        if select_columns_str is None and dst_column in focus_cols_set:
            select_columns_str = f"{dst_column}"
        elif dst_column in focus_cols_set:
            select_columns_str += f", {dst_column}"
        else:
            select_columns_str += f", MAX({dst_column})"
    groupby_columns_str = ", ".join(focus_col_list)
    where_block = f"\n{where_block}" if where_block else ""
    return f"""INSERT INTO {dst_table} ({dst_columns_str})
SELECT {select_columns_str}
FROM {src_table}{where_block}
GROUP BY {groupby_columns_str}
;
"""


def create_select_query(
    cursor: sqlite3_Connection,
    x_tablename: str,
    select_columns: list[str],
    where_dict: dict[str,] = None,
    flat_bool: bool = False,
):
    if where_dict is None:
        where_dict = {}
    table_columns = get_table_columns(cursor, x_tablename)
    if not select_columns:
        select_columns = table_columns
    else:
        select_columns = get_sorted_cols_only_list(set(select_columns), table_columns)
    select_columns_str = ", ".join(list(select_columns))
    where_str = ""
    for where_column, where_value in where_dict.items():
        column_type = get_column_data_type(cursor, x_tablename, where_column)
        value_str = f"'{where_value}'" if column_type == "TEXT" else where_value
        if where_str == "":
            where_str = f"WHERE {where_column} = {value_str}"
        else:
            where_str += f"""\n  AND {where_column} = {value_str}"""
    sqlstr = f"""SELECT {select_columns_str}\nFROM {x_tablename}\n{where_str}\n"""
    if flat_bool:
        sqlstr = sqlstr[:-1].replace("\n", " ").replace("  ", " ").replace("  ", " ")
    return sqlstr


def create_insert_into_clause_str(
    cursor: sqlite3_Connection,
    x_tablename: str,
    columns_set: set[str],
) -> str:
    table_columns = get_table_columns(cursor, x_tablename)
    columns_list = get_sorted_cols_only_list(columns_set, table_columns)
    into_columns_str = ", ".join(columns_list)
    return f"INSERT INTO {x_tablename} ({into_columns_str})"


def create_insert_query(
    cursor: sqlite3_Connection,
    x_tablename: str,
    values_dict: dict[str,],
    flat_bool: bool = False,
) -> str:
    columns_set = set(values_dict.keys())
    table_columns = get_table_columns(cursor, x_tablename)
    columns_list = get_sorted_cols_only_list(columns_set, table_columns)
    values_str = ""
    for x_column in columns_list:
        column_type = get_column_data_type(cursor, x_tablename, x_column)
        x_value = values_dict.get(x_column)
        value_str = sqlite_obj_str(x_value, column_type)
        if values_str == "":
            values_str += f"""\n  {value_str}"""
        else:
            values_str += f"""\n, {value_str}"""
    values_str += "\n)\n;\n"
    into_columns_str = ", ".join(columns_list)
    if flat_bool:
        values_str = values_str.replace("\n", "").replace("  ", "")
    return f"""INSERT INTO {x_tablename} ({into_columns_str})
VALUES ({values_str}"""


def required_columns_exist(
    conn_or_cursor: sqlite3_Connection,
    src_table: str,
    required_columns: set[str],
):
    src_columns = set(get_table_columns(conn_or_cursor, src_table))
    return required_columns.issubset(src_columns)
