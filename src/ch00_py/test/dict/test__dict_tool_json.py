from ch00_py.dict_toolbox import get_serializable_dict
from ref.keywords import ExampleStrs as exx


def test_get_serializable_dict_ReturnsObj_Scenario0_FlatDict():
    # ESTABLISH
    data = {"color": exx.red, "shape": exx.square, "name": "box"}
    # WHEN
    result = get_serializable_dict(data)
    # THEN
    assert result == {"color": exx.red, "shape": "square", "name": "box"}


def test_get_serializable_dict_ReturnsObj_Scenario1_NestedDict():
    # ESTABLISH
    data = {"outer": {"inner": {"color": exx.blue, "count": 5}}}
    # WHEN
    result = get_serializable_dict(data)
    # THEN
    assert result == {"outer": {"inner": {"color": "blue", "count": 5}}}


def test_get_serializable_dict_ReturnsObj_Scenario2_List():
    # ESTABLISH
    data = [exx.red, exx.blue, "plain"]
    # WHEN
    result = get_serializable_dict(data)
    # THEN
    assert result == [exx.red, "blue", "plain"]


def test_get_serializable_dict_ReturnsObj_Scenario3_Set():
    # ESTABLISH
    data = {exx.red, exx.blue, "plain"}
    # WHEN
    result = get_serializable_dict(data)
    # THEN
    assert result == ["blue", "plain", exx.red]


def test_get_serializable_dict_ReturnsObj_Scenario4_Mixed():
    # ESTABLISH
    data = {
        "colors": [exx.red, exx.blue],
        "shapes": {"main": exx.square, "alt": "triangle"},
        "count": 3,
    }
    # WHEN
    result = get_serializable_dict(data)
    # THEN
    assert result == {
        "colors": [exx.red, "blue"],
        "shapes": {"main": exx.square, "alt": "triangle"},
        "count": 3,
    }


def test_get_serializable_dict_ReturnsObj_Scenario5_NonEnumValuesUnchanged():
    # ESTABLISH
    data = {"num": 10, "text": "hello", "flag": True}
    # WHEN
    result = get_serializable_dict(data)
    # THEN
    assert result == data


def test_get_serializable_dict_ReturnsObj_Scenario6_SimpleDict():
    # ESTABLISH
    obj = {"a": 1, "b": 2}
    expected = {"a": 1, "b": 2}
    # WHEN / THEN
    assert get_serializable_dict(obj) == expected


def test_get_serializable_dict_ReturnsObj_Scenario7_NestedDict():
    # ESTABLISH
    obj = {"a": {"b": {"c": 3}}}
    expected = {"a": {"b": {"c": 3}}}
    # WHEN / THEN
    assert get_serializable_dict(obj) == expected


def test_get_serializable_dict_ReturnsObj_Scenario8_ListInsideDict():
    # ESTABLISH
    obj = {"a": [1, 2, {"b": 3}]}
    expected = {"a": [1, 2, {"b": 3}]}
    # WHEN / THEN
    assert get_serializable_dict(obj) == expected


def test_get_serializable_dict_ReturnsObj_Scenario9_SetConversion():
    # ESTABLISH
    obj = {"a": {1, 2, 3}}
    # WHEN
    result = get_serializable_dict(obj)
    # THEN
    assert isinstance(result["a"], list)
    assert sorted(result["a"]) == [1, 2, 3]


def test_get_serializable_dict_ReturnsObj_Scenario10_ListOfSets():
    # ESTABLISH
    obj = [{"x": {1, 2}}, {"y": {3, 4}}]
    # WHEN
    result = get_serializable_dict(obj)
    # THEN
    assert isinstance(result[0]["x"], list)
    assert sorted(result[0]["x"]) == [1, 2]
    assert sorted(result[1]["y"]) == [3, 4]


def test_get_serializable_dict_ReturnsObj_Scenario11_ScalarValues():
    # ESTABLISH / WHEN / THEN
    assert get_serializable_dict(42) == 42
    assert get_serializable_dict("hello") == "hello"
    assert get_serializable_dict(3.14) == 3.14
    assert get_serializable_dict(True) is True
    assert get_serializable_dict(None) is None


def test_get_serializable_dict_ReturnsObj_Scenario12_EmptyContainers():
    # ESTABLISH / WHEN / THEN
    assert get_serializable_dict({}) == {}
    assert get_serializable_dict([]) == []
    assert get_serializable_dict(set()) == []


def test_get_serializable_dict_ReturnsObj_Scenario13_DictWithSetKeys():
    # ESTABLISH
    obj = {frozenset([1, 2]): "value"}
    # WHEN
    result = get_serializable_dict(obj)
    # THEN
    assert list(result.keys())[0] == frozenset([1, 2])
    assert result[frozenset([1, 2])] == "value"
