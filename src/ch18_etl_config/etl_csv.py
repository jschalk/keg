from csv import writer as csv_writer
from os.path import join as os_path_join
from sqlite3 import Connection as sqlite3_Connection
from src.ch00_py.db_toolbox import get_table_columns
from src.ch00_py.file_toolbox import create_path, set_dir
from src.ch04_rope.rope import get_all_rope_labels


def save_to_split_csvs(
    conn_or_cursor: sqlite3_Connection,
    tablename,
    key_columns,
    dst_dir,
    col1_prefix=None,
    col2_prefix=None,
):
    """
    Select a single table from a SQLite DB, filter rows into CSVs by key columns, and creates the csvs.

    :param db_path: Path to the SQLite database file.
    :param tablename: Name of the table to query.
    :param key_columns: List of columns to use as keys for filtering rows.
    :param dst_dir: Directory to save the resulting CSVs.
    """
    # Fetch all rows from the table
    column_names = get_table_columns(conn_or_cursor, tablename)
    query = f"SELECT * FROM {tablename}"
    rows = conn_or_cursor.execute(query).fetchall()

    # Find the indices of key columns
    key_indices = [column_names.index(key) for key in key_columns]

    # Organize rows by key values
    collectioned_rows = {}
    for row in rows:
        # Create a tuple of key values
        key_values = tuple(row[index] for index in key_indices)

        if key_values not in collectioned_rows:
            collectioned_rows[key_values] = []
        collectioned_rows[key_values].append(row)

    # Write collectioned rows to separate CSV files
    for key_values, collection in collectioned_rows.items():
        if col1_prefix:
            new_key_values = [key_values[0], col1_prefix]
            new_key_values.extend(key_values[1:])
            key_values = new_key_values
        if col2_prefix:
            new_key_values = key_values[:3]
            new_key_values.append(col2_prefix)
            new_key_values.extend(key_values[3:])
            key_values = new_key_values

        knot_index = column_names.index("knot")
        knot_str = collection[0][knot_index]
        x_rope = key_values[0]

        path_dirs = get_all_rope_labels(x_rope, knot_str)
        path_dirs = [path_dirs[0]]
        path_dirs.extend(key_values[1:])
        key_path = get_key_dir_part(path_dirs)
        csv_path = create_path(dst_dir, key_path)
        set_dir(csv_path)
        dst_file = os_path_join(csv_path, f"{tablename}.csv")
        # Write to CSV
        with open(dst_file, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv_writer(csv_file)
            writer.writerow(column_names)
            writer.writerows(collection)


def get_key_dir_part(key_values: list[str]) -> str:
    return "/".join(str(value) for value in key_values)
