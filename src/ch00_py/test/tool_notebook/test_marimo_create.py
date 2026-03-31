from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_file, save_file
from src.ch00_py.notebook_toolbox import (
    create_marimo_notebook_from_test_str,
    save_marimo_notebook_from_test_file,
)
from src.ref.keywords import Ch00Keywords as kw, ExampleStrs as exx


def test_create_marimo_notebook_from_test_str_ReturnsObj_Scenario0_simple_example(
    temp3_fs, temp3_dir
):
    # ESTABLISH
    test_file_path = create_path(temp3_dir, "test_sql_inserts.py")
    example_import_str = "from math import remainder"
    save_file(test_file_path, None, example_import_str)
    # source test name: test_custom_insert_ModifiesTable_Scenario0
    test_func_str = """
def test_remainder_ReturnsObj(cursor0: Cursor):
    # ESTABLISH
    x_count = 3

    # WHEN 
    x_remainder = remainder(50, 20)
    
    # THEN
    assert x_remainder == 10
"""

    # WHEN
    marimo_file_str = create_marimo_notebook_from_test_str(
        test_file_path, test_func_str
    )

    # THEN
    print(marimo_file_str[300:600])
    expected_marimo_front_str = """import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup(hide_code=True):"""
    expected_marimo_back_str = """
    cursor0 = conn.cursor()
    print("cursor0 created for SQLite db in memory.")


@app.cell
def _():
    # ESTABLISH
    x_count = 3

    return


@app.cell
def _():
    # WHEN 
    x_remainder = remainder(50, 20)
    
    return


@app.cell
def _():
    # THEN
    assert x_remainder == 10
    return


if __name__ == "__main__":
    app.run()
"""
    assert marimo_file_str.find(expected_marimo_front_str) > -1
    assert marimo_file_str.endswith(expected_marimo_back_str)


def test_create_marimo_notebook_from_test_str_ReturnsObj_Scenario1(temp3_fs, temp3_dir):
    # ESTABLISH
    test_file_path = create_path(temp3_dir, "test_sql_inserts.py")
    example_import_str = "from sqlite3 import Cursor\nfrom src.ch00_py.test._util.ch00_envv import cursor0"
    save_file(test_file_path, None, example_import_str)
    # source test name: test_custom_insert_ModifiesTable_Scenario0
    test_func_str = '''
def test_custom_insert_ModifiesTable_Scenario0(cursor0: Cursor):
    # ESTABLISH
    create_orders_table_sql = """CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT, stuff INTEGER);"""
    cursor0.execute(create_orders_table_sql)
    create_cust_totals_table_sql = """CREATE TABLE  IF NOT EXISTS customer_totals (customer TEXT, total_stuff INTEGER);"""
    cursor0.execute(create_cust_totals_table_sql)
    conn.commit()

    # Populate source table
    rows = [("Alice", 50), ("Alice", 25), ("Bob", 40), ("Bob", 60), ("Charlie", 30)]
    cursor0.executemany("INSERT INTO orders (customer, stuff) VALUES (?, ?)", rows)
    conn.commit()
    assert cursor0.execute("SELECT COUNT(*) FROM customer_totals").fetchone()[0] == 0

    # WHEN Execute Aggregate INSERT using GROUP BY
    cursor0.execute(
        """
    INSERT INTO customer_totals (customer, total_stuff)
    SELECT customer, SUM(stuff)
    FROM orders
    GROUP BY customer;
    """
    )
    conn.commit()
    print("Aggregate insert completed.")

    # THEN
    assert cursor0.execute("SELECT COUNT(*) FROM customer_totals").fetchone()[0] == 3
    cursor0.execute(
        "SELECT customer, total_stuff FROM customer_totals ORDER BY customer"
    )
    results = cursor0.fetchall()
    print("Rows by customer, total_stuff")
    count = 0
    for row in results:
        print(f"Row #{count} {row}")
        count += 1
'''

    # WHEN
    marimo_file_str = create_marimo_notebook_from_test_str(
        test_file_path, test_func_str
    )

    # THEN
    expected_marimo_front_str = """import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup(hide_code=True):"""
    expected_marimo_back_str = '''
    # source test name: test_custom_insert_ModifiesTable_Scenario0
    from sqlite3 import Cursor
    from src.ch00_py.test._util.ch00_envv import cursor0
    from sqlite3 import connect as sqlite3_connect

    conn = sqlite3_connect(":memory:")
    cursor0 = conn.cursor()
    print("cursor0 created for SQLite db in memory.")


@app.cell
def _():
    # ESTABLISH
    create_orders_table_sql = """CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT, stuff INTEGER);"""
    cursor0.execute(create_orders_table_sql)
    create_cust_totals_table_sql = """CREATE TABLE  IF NOT EXISTS customer_totals (customer TEXT, total_stuff INTEGER);"""
    cursor0.execute(create_cust_totals_table_sql)
    conn.commit()

    return


@app.cell
def _():
    # Populate source table
    rows = [("Alice", 50), ("Alice", 25), ("Bob", 40), ("Bob", 60), ("Charlie", 30)]
    cursor0.executemany("INSERT INTO orders (customer, stuff) VALUES (?, ?)", rows)
    conn.commit()
    assert cursor0.execute("SELECT COUNT(*) FROM customer_totals").fetchone()[0] == 0

    return


@app.cell
def _():
    # WHEN Execute Aggregate INSERT using GROUP BY
    cursor0.execute(
        """
    INSERT INTO customer_totals (customer, total_stuff)
    SELECT customer, SUM(stuff)
    FROM orders
    GROUP BY customer;
    """
    )
    conn.commit()
    print("Aggregate insert completed.")

    return


@app.cell
def _():
    # THEN
    assert cursor0.execute("SELECT COUNT(*) FROM customer_totals").fetchone()[0] == 3
    cursor0.execute(
        "SELECT customer, total_stuff FROM customer_totals ORDER BY customer"
    )
    results = cursor0.fetchall()
    print("Rows by customer, total_stuff")
    count = 0
    for row in results:
        print(f"Row #{count} {row}")
        count += 1
    return


if __name__ == "__main__":
    app.run()
'''
    assert marimo_file_str.find(expected_marimo_front_str) > -1
    assert marimo_file_str.find(expected_marimo_back_str) > -1


def test_create_marimo_notebook_from_test_str_ReturnsObj_Scenario2(temp3_fs, temp3_dir):
    # ESTABLISH
    test_function_str = """
def test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1(
    cursor0: Cursor,
):
    # ESTABLISH
    casa_color_tblname = "casa_color"
    insert_into_clause = f"INSERT INTO {casa_color_tblname} (casa_id, color)"
    values_clause = f"VALUES (1, 'Red'), (2, 'Blue'), (3, 'Blue');"
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, casa_color_tblname) == 3
    # Confirm destination table is empty
    casa_agg_tblname = "casa_agg"
    assert get_row_count(cursor0, casa_agg_tblname) == 0

    # WHEN
    insert_color_casa_into_casa_agg(cursor0)

    # THEN
    assert get_row_count(cursor0, casa_agg_tblname) == 2

    select_agg_sqlstr = f"SELECT * FROM {casa_agg_tblname};"
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [("Blue", 2), ("Red", 1)]
"""
    # create test file so that imports and be collected
    example_color_import_str = "from src.color import insert_color_casa_into_casa_agg"
    example_cursor0_import_str = "from src.ch00_py.test._util.ch00_envv import cursor0"
    example_import_str = f"{example_color_import_str}\n{example_cursor0_import_str}"
    test_file_str = f"{example_import_str}\n\n\n{test_function_str}"
    test_file_path = create_path(temp3_dir, "test_color_sql.py")
    save_file(test_file_path, None, test_file_str)

    # WHEN
    marimo_file_str = create_marimo_notebook_from_test_str(
        test_file_path, test_function_str
    )

    # THEN
    assert marimo_file_str
    print(marimo_file_str)
    print(example_import_str)
    assert f"    {example_color_import_str}" in marimo_file_str
    assert f"    {example_cursor0_import_str}" in marimo_file_str
    expected1_str = """import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup(hide_code=True):"""
    expected2_str = """
    # source test name: test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1
    from src.color import insert_color_casa_into_casa_agg
    from src.ch00_py.test._util.ch00_envv import cursor0
    from sqlite3 import connect as sqlite3_connect"""
    assert marimo_file_str.find(expected1_str) == 0
    assert marimo_file_str.find(expected2_str) > 0


def test_save_marimo_notebook_from_test_file_ReturnsObj_Scenario2(temp3_fs, temp3_dir):
    # ESTABLISH
    test_function_str = """
def test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1(
    cursor0: Cursor,
):
    # ESTABLISH
    casa_color_tblname = "casa_color"
    insert_into_clause = f"INSERT INTO {casa_color_tblname} (casa_id, color)"
    values_clause = f"VALUES (1, 'Red'), (2, 'Blue'), (3, 'Blue');"
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, casa_color_tblname) == 3
    # Confirm destination table is empty
    casa_agg_tblname = "casa_agg"
    assert get_row_count(cursor0, casa_agg_tblname) == 0

    # WHEN
    insert_color_casa_into_casa_agg(cursor0)

    # THEN
    assert get_row_count(cursor0, casa_agg_tblname) == 2

    select_agg_sqlstr = f"SELECT * FROM {casa_agg_tblname};"
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [("Blue", 2), ("Red", 1)]
"""
    # create test file so that imports and be collected
    example_color_import_str = "from src.color import insert_color_casa_into_casa_agg"
    example_cursor0_import_str = "from src.ch00_py.test._util.ch00_envv import cursor0"
    example_import_str = f"{example_color_import_str}\n{example_cursor0_import_str}"
    test_file_str = f"{example_import_str}\n\n\n{test_function_str}"
    test_file_path = create_path(temp3_dir, "test_color_sql.py")
    save_file(test_file_path, None, test_file_str)
    dest_file_path = create_path(temp3_dir, "test_marimo01.py")
    assert not os_path_exists(dest_file_path)

    # WHEN
    casa_testname = "test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1"
    return_value = save_marimo_notebook_from_test_file(
        test_file_path, casa_testname, dest_file_path
    )

    # THEN
    assert os_path_exists(dest_file_path)
    assert not return_value
    marimo_file_str = open_file(dest_file_path)
    assert marimo_file_str
    # print(marimo_file_str)
    # print(example_import_str)
    assert f"    {example_color_import_str}" in marimo_file_str
    assert f"    {example_cursor0_import_str}" in marimo_file_str
    expected1_str = """import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup(hide_code=True):"""
    expected2_str = """
    # source test name: test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1
    from src.color import insert_color_casa_into_casa_agg
    from src.ch00_py.test._util.ch00_envv import cursor0
    from sqlite3 import connect as sqlite3_connect"""
    assert marimo_file_str.find(expected1_str) == 0
    assert marimo_file_str.find(expected2_str) > 0
