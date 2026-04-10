from pandas import DataFrame
from src.ch17_idea.brick_db_tool import dataframe_to_dict


def test_dataframe_to_dict_ReturnsObj_Empty():
    # ESTABLISH
    data = {"id": [], "name": [], "age": [], "city": []}
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, ["name"])

    # THEN
    expected_dict = {}
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str


def test_dataframe_to_dict_ReturnsObj_WithValues():
    # ESTABLISH
    data = {
        "id": [1, 2, 3],
        "name": ["Sue", "Bob", "Yao"],
        "age": [25, 30, 35],
        "city": ["NYC", "Dallas", "Paris"],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, ["name"])

    # THEN
    expected_dict = {
        "Sue": {"name": "Sue", "age": 25, "city": "NYC"},
        "Bob": {"name": "Bob", "age": 30, "city": "Dallas"},
        "Yao": {"name": "Yao", "age": 35, "city": "Paris"},
    }
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str


def test_dataframe_to_dict_ReturnsObj_WithOutIndex():
    # ESTABLISH
    data = {
        "name": ["Sue", "Bob", "Yao"],
        "age": [25, 30, 35],
        "city": ["NYC", "Dallas", "Paris"],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, ["name"])

    # THEN
    expected_dict = {
        "Sue": {"name": "Sue", "age": 25, "city": "NYC"},
        "Bob": {"name": "Bob", "age": 30, "city": "Dallas"},
        "Yao": {"name": "Yao", "age": 35, "city": "Paris"},
    }
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str


def test_dataframe_to_dict_ReturnsObj_TwoKeyColumns():
    # ESTABLISH
    data = {
        "id": [1, 2, 3, 4],
        "name": ["Sue", "Sue", "Bob", "Yao"],
        "age": [25, 46, 30, 35],
        "city": ["NYC", "Boston", "Dallas", "Paris"],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, ["name", "age"])

    # THEN
    expected_dict = {
        "Sue": {
            25: {"name": "Sue", "age": 25, "city": "NYC"},
            46: {"name": "Sue", "age": 46, "city": "Boston"},
        },
        "Bob": {30: {"name": "Bob", "age": 30, "city": "Dallas"}},
        "Yao": {35: {"name": "Yao", "age": 35, "city": "Paris"}},
    }
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str


def test_dataframe_to_dict_ReturnsObj_ThreeKeyColumns():
    # ESTABLISH
    data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Sue", "Sue", "Sue", "Bob", "Yao"],
        "age": [25, 46, 46, 30, 35],
        "city": ["NYC", "Boston", "ElPaso", "Dallas", "Paris"],
        "sport": ["run", "bowl", "tennis", "run", "bowl"],
    }
    df = DataFrame(data)

    # WHEN
    result_dict = dataframe_to_dict(df, ["name", "age", "city"])

    # THEN
    expected_dict = {
        "Sue": {
            25: {
                "NYC": {
                    "name": "Sue",
                    "age": 25,
                    "city": "NYC",
                    "sport": "run",
                }
            },
            46: {
                "Boston": {
                    "name": "Sue",
                    "age": 46,
                    "city": "Boston",
                    "sport": "bowl",
                },
                "ElPaso": {
                    "name": "Sue",
                    "age": 46,
                    "city": "ElPaso",
                    "sport": "tennis",
                },
            },
        },
        "Bob": {
            30: {
                "Dallas": {
                    "name": "Bob",
                    "age": 30,
                    "city": "Dallas",
                    "sport": "run",
                }
            }
        },
        "Yao": {
            35: {
                "Paris": {
                    "name": "Yao",
                    "age": 35,
                    "city": "Paris",
                    "sport": "bowl",
                }
            }
        },
    }
    assert_exception_str = f"Expected {expected_dict}, but got {result_dict}"
    assert result_dict == expected_dict, assert_exception_str
