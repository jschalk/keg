from ch00_py.db_toolbox import get_nonconvertible_columns


def test_get_nonconvertible_columns_Scenario0_AllValid():
    # ESTABLISH
    row = {"id": "123", "score": "98.6", "name": "Alice"}
    col_types = {"id": "INTEGER", "score": "REAL", "name": "TEXT"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {}


def test_get_nonconvertible_columns_Scenario1_InvalidInteger():
    # ESTABLISH
    row = {"id": "abc", "score": "98.6", "name": "Alice"}
    col_types = {"id": "INTEGER", "score": "REAL", "name": "TEXT"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {"id": "abc"}


def test_get_nonconvertible_columns_Scenario2_InvalidReal():
    # ESTABLISH
    row = {"id": "123", "score": "not_a_number", "name": "Bob"}
    col_types = {"id": "INTEGER", "score": "REAL", "name": "TEXT"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {"score": "not_a_number"}


def test_get_nonconvertible_columns_Scenario3_MultipleInvalid():
    # ESTABLISH
    row = {"id": "xyz", "score": "none", "name": "Charlie"}
    col_types = {"id": "INTEGER", "score": "REAL", "name": "TEXT"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {"id": "xyz", "score": "none"}


def test_get_nonconvertible_columns_Scenario4_UnsupportedType():
    # ESTABLISH
    row = {"id": "123", "score": "90", "current": "yes"}
    col_types = {
        "id": "INTEGER",
        "score": "REAL",
        "current": "Boolean",
    }

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {"current": "yes"}


def test_get_nonconvertible_columns_Scenario5_MissingColumnsAreIgnored():
    # ESTABLISH
    row = {"score": "100.0"}
    col_types = {"id": "INTEGER", "score": "REAL"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {}


def test_get_nonconvertible_columns_Scenario6_NonDeclaredTypesIgnored():
    # ESTABLISH
    row = {"id": "123", "score": "90", "current": "yes"}
    col_types = {"id": "INTEGER", "score": "REAL"}

    # WHEN / THEN
    assert get_nonconvertible_columns(row, col_types) == {}
