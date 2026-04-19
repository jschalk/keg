from ch00_py.dict_toolbox import sort_keys_case_insensitive


def test_sort_keys_case_insensitive_ReturnsObj_Scenario0_FlatDictCaseInsensitiveSort():
    # ESTABLISH
    data = {"apple": 1, "Banana": 2, "Apricot": 3, "banana": 4, "Apple": 5}

    # WHEN
    result = sort_keys_case_insensitive(data)

    # THEN
    assert list(result.keys()) == ["Apple", "apple", "Apricot", "Banana", "banana"]


def test_sort_keys_case_insensitive_ReturnsObj_Scenario1_NestedDictsSorted():
    # ESTABLISH
    data = {"b": {"Zoo": 1, "ant": 2, "Ant": 3}, "A": {"dog": 1, "Cat": 2, "cat": 3}}

    # WHEN
    result = sort_keys_case_insensitive(data)

    # THEN
    assert list(result.keys()) == ["A", "b"]
    assert list(result["A"].keys()) == ["Cat", "cat", "dog"]
    assert list(result["b"].keys()) == ["Ant", "ant", "Zoo"]


def test_sort_keys_case_insensitive_ReturnsObj_Scenario2_ListOfDictsSorted():
    # ESTABLISH
    data = [{"b": 2, "A": 1}, {"Dog": 1, "cat": 2}]

    # WHEN
    result = sort_keys_case_insensitive(data)

    # THEN
    assert list(result[0].keys()) == ["A", "b"]
    assert list(result[1].keys()) == ["cat", "Dog"]


def test_sort_keys_case_insensitive_ReturnsObj_Scenario3_MixedDictListNesting():
    # ESTABLISH
    data = {
        "b": [
            {"Zoo": 1, "ant": 2},
            {"Cat": 1, "dog": 2},
        ],
        "A": "value",
    }

    # WHEN
    result = sort_keys_case_insensitive(data)

    # THEN
    assert list(result.keys()) == ["A", "b"]
    assert list(result["b"][0].keys()) == ["ant", "Zoo"]
    assert list(result["b"][1].keys()) == ["Cat", "dog"]


def test_sort_keys_case_insensitive_ReturnsObj_Scenario5_EmptyDictAndList():
    # ESTABLISH / WHEN / THEN
    assert sort_keys_case_insensitive({}) == {}
    assert sort_keys_case_insensitive([]) == []


def test_sort_keys_case_insensitive_ReturnsObj_Scenario6_OriginalNotMutated():
    # ESTABLISH
    data = {"b": 2, "A": 1}
    copy = dict(data)

    # WHEN
    result = sort_keys_case_insensitive(data)

    # THEN
    assert data == copy
    assert result is not data
