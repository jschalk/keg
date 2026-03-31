from csv import DictReader as csv_DictReader, reader as csv_reader
from io import StringIO as io_StringIO
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch00_py.csv_toolbox import (
    delete_column_from_csv_string,
    export_sqlite_tables_to_csv,
    open_csv_with_types,
    replace_csv_column_from_string,
)
from src.ch00_py.file_toolbox import create_path, save_file, set_dir


def test_open_csv_with_types_ReturnsObj(temp3_fs, temp3_dir):
    """Test open_csv_with_types with various data types."""
    # ESTABLISH
    set_dir(temp3_dir)
    column_types = {
        "id": "INTEGER",
        "name": "TEXT",
        "price": "REAL",
        "available": "BOOLEAN",
    }

    # Create test CSV file
    csv_str = """id,name,price,available,fay
1,Widget,19.99,True,fay
2,Gadget,5.49,False,bob
3,Doodad,12.00,true,fay
4,Doodad,12.00,truee,fay
,Doodad,,truee,fay
"""
    save_file(temp3_dir, "test.csv", csv_str)
    # with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    #     writer = csv_writer(csv_file)
    #     writer.writerow(["id", "name", "price", "available", "Fay"])
    #     writer.writerow(["1", "Widget", "19.99", "True", "Fay"])
    #     writer.writerow(["2", "Gadget", "5.49", "False", "Bob"])
    #     writer.writerow(["3", "Doodad", "12.00", "true", "Fay"])
    #     writer.writerow(["4", "Doodad", "12.00", "truee", "Fay"])
    csv_path = create_path(temp3_dir, "test.csv")

    # WHEN
    generated_rows = open_csv_with_types(csv_path, column_types)

    # THEN
    expected_rows = [
        ("id", "name", "price", "available", "fay"),
        (1, "Widget", 19.99, True, "fay"),
        (2, "Gadget", 5.49, False, "bob"),
        (3, "Doodad", 12.00, True, "fay"),
        (4, "Doodad", 12.00, None, "fay"),
        (None, "Doodad", None, None, "fay"),
    ]
    print(f"{generated_rows}")
    assert generated_rows == expected_rows


def test_export_sqlite_tables_to_csv_CreatesFiles(temp3_fs, temp3_dir):
    # ESTABLISH
    # 1. Create temporary SQLite DB
    set_dir(temp3_dir)
    db_path = create_path(temp3_dir, "test555.db")
    print(f"{db_path=}")
    conn = sqlite3_connect(db_path)
    cursor = conn.cursor()

    # 2. Create tables and insert data
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")

    cursor.execute("CREATE TABLE products (sku TEXT, price REAL)")
    cursor.execute("INSERT INTO products VALUES ('ABC', 9.99)")
    cursor.close()
    conn.commit()
    conn.close()

    # WHEN
    # 3. Run export function
    export_sqlite_tables_to_csv(str(db_path), str(temp3_dir))

    # THEN
    # 4. Check output files
    user_csv = create_path(temp3_dir, "users_2.csv")
    product_csv = create_path(temp3_dir, "products_1.csv")

    assert os_path_exists(user_csv)
    assert os_path_exists(product_csv)

    # 5. Check CSV contents (users table)
    with open(user_csv, newline="", encoding="utf-8") as f:
        reader = list(csv_reader(f))
        assert reader[0] == ["id", "name"]
        assert reader[1] == ["1", "Alice"]
        assert reader[2] == ["2", "Bob"]

    # 6. Check CSV contents (products table)
    with open(product_csv, newline="", encoding="utf-8") as f:
        reader = list(csv_reader(f))
        assert reader[0] == ["sku", "price"]
        assert reader[1] == ["ABC", "9.99"]


def test_replace_csv_column_from_string_ReturnsObj():
    # ESTABLISH
    csv_string = """id,name,classification
1,Alice,pending
2,Bob,in progress
"""

    # WHEN
    modified_csv = replace_csv_column_from_string(
        csv_string, "classification", "complete"
    )

    # THEN
    expected_csv = """id,name,classification
1,Alice,complete
2,Bob,complete
"""
    assert modified_csv == expected_csv
    reader = csv_DictReader(io_StringIO(modified_csv))
    rows = list(reader)

    # Assertions
    assert all(row["classification"] == "complete" for row in rows)
    assert rows[0]["name"] == "Alice"
    assert rows[1]["name"] == "Bob"


def test_delete_column_from_csv_string_ReturnsObj():
    # ESTABLISH
    csv_input = """id,name,classification
1,Alice,current
2,Bob,incurrent
"""

    # WHEN
    result = delete_column_from_csv_string(csv_input, "classification")

    # THEN
    # Parse the result using csv.DictReader
    reader = csv_DictReader(io_StringIO(result))
    rows = list(reader)
    # Expected CSV output after removing 'classification'
    expected_output = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
    assert reader.fieldnames == ["id", "name"]
    assert rows == expected_output
