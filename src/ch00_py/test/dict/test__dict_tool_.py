from copy import deepcopy as copy_deepcopy
from numpy import int64 as numpy_int64
from pytest import raises as pytest_raises
from src.ch00_py.dict_toolbox import (
    add_headers_to_csv,
    add_nested_dict_if_missing,
    change_nested_key,
    create_2d_array_from_dict,
    create_l2nested_csv_dict,
    del_in_nested_dict,
    exists_in_nested_dict,
    extract_csv_headers,
    get_0_if_None,
    get_1_if_None,
    get_all_nondictionary_objs,
    get_csv_column1_column2_metrics,
    get_empty_str_if_None,
    get_from_nested_dict,
    get_max_key,
    get_nested_dict_key_by_level,
    get_nested_dict_keys_by_level,
    get_nested_keys_by_level,
    get_nested_non_dict_keys_by_level,
    get_nested_non_dict_keys_list,
    get_positional_dict,
    get_positive_int,
    get_sorted_list_of_dict_keys,
    get_str_in_all_sub_dict,
    get_str_in_sub_dict,
    is_2d_with_unique_keys,
    is_camel_case,
    modular_addition,
    set_in_nested_dict,
    set_modular_dict_values,
    str_in_all_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    uppercase_in_str,
    uppercase_is_first,
)
from src.ch00_py.test._util.ch00_examples import DictToolExampleStrs as ex0


def test_uppercase_in_str_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert uppercase_in_str("hello") == False
    assert uppercase_in_str("Hello")
    assert uppercase_in_str("HELLO")
    assert uppercase_in_str("123abc") == False
    assert uppercase_in_str("123ABC")
    assert uppercase_in_str("") == False
    assert uppercase_in_str(" ") == False
    assert uppercase_in_str("mixed123Case")
    assert uppercase_in_str("mixed123case") == False


def test_uppercase_is_first_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert uppercase_is_first("hello") == False
    assert uppercase_is_first("Hello")
    assert uppercase_is_first("HELLO")
    assert uppercase_is_first("123abc") == False
    assert uppercase_is_first("123ABC") == False
    assert uppercase_is_first("") == False
    assert uppercase_is_first(" ") == False
    assert uppercase_is_first("mixed123Case") == False


def test_is_camel_case_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert is_camel_case("hello") == False
    assert is_camel_case("123abc") == False
    assert is_camel_case("123ABC") == False
    assert is_camel_case("") == False
    assert is_camel_case(" ") == False
    assert is_camel_case("MyClass")
    assert is_camel_case("MyCLASS")
    assert is_camel_case("My_Class") is False
    assert is_camel_case("myClass") is False


def test_get_1_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_1_if_None(None) == 1
    assert get_1_if_None(2) == 2
    assert get_1_if_None(-3) == -3
    x_nan = float("nan")
    assert get_1_if_None(x_nan) == 1


def test_get_empty_str_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_empty_str_if_None(None) == ""
    assert get_empty_str_if_None(2) == "2"
    assert get_empty_str_if_None(-3) == "-3"
    assert get_empty_str_if_None("Fay") == "Fay"
    x_nan = float("nan")
    assert get_empty_str_if_None(x_nan) == ""


def test_get_0_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_0_if_None(None) == 0
    assert get_0_if_None(2) == 2
    assert get_0_if_None(-3) == -3
    e7 = numpy_int64(7)
    assert str(type(get_0_if_None(e7))) != "<class 'numpy.int64'>"
    assert str(type(get_0_if_None(e7))) == "<class 'int'>"
    x_nan = float("nan")
    assert get_0_if_None(x_nan) == 0


def test_add_nested_dict_if_missing_AddsToDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    add_nested_dict_if_missing(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3])

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: {}}}}


def test_set_in_nested_dict_AddsToDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    fly_str = "flying"
    set_in_nested_dict(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3], x_obj=fly_str)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: fly_str}}}


def test_exists_in_nested_dict_AddsToDict():
    # ESTABLISH
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    y_keylist = [y_key1, y_key2, y_key3]
    fly_str = "flying"
    assert exists_in_nested_dict(x_dict=y_dict, x_keylist=y_keylist) is False

    # WHEN
    set_in_nested_dict(y_dict, y_keylist, x_obj=fly_str)

    # THEN
    assert exists_in_nested_dict(y_dict, y_keylist)


def test_del_in_nested_dict_SetsDict():
    # ESTABLISH
    y_dict = {}
    y_key1 = "sports"
    y_key2 = "running"
    y_key3_0 = "fun running"
    y_key3_1 = "rain running"
    y3_0_keylist = [y_key1, y_key2, y_key3_0]
    y3_1_keylist = [y_key1, y_key2, y_key3_1]
    fly_str = "flying"
    set_in_nested_dict(y_dict, y3_1_keylist, x_obj=fly_str)
    assert y_dict == {y_key1: {y_key2: {y_key3_1: fly_str}}}
    assert exists_in_nested_dict(y_dict, y3_0_keylist) is False
    assert exists_in_nested_dict(y_dict, y3_1_keylist)

    # WHEN
    del_in_nested_dict(y_dict, y3_0_keylist)

    # THEN
    assert exists_in_nested_dict(y_dict, y3_0_keylist) is False

    # ESTABLISH
    set_in_nested_dict(y_dict, y3_0_keylist, x_obj=fly_str)
    assert y_dict == {y_key1: {y_key2: {y_key3_0: fly_str, y_key3_1: fly_str}}}
    assert exists_in_nested_dict(y_dict, y3_0_keylist)
    assert exists_in_nested_dict(y_dict, y3_1_keylist)

    # WHEN
    del_in_nested_dict(y_dict, y3_0_keylist)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3_1: fly_str}}}
    assert exists_in_nested_dict(y_dict, y3_0_keylist) is False
    assert exists_in_nested_dict(y_dict, y3_1_keylist)

    # WHEN
    del_in_nested_dict(y_dict, y3_1_keylist)

    # THEN
    assert not y_dict
    assert not get_from_nested_dict(y_dict, y3_0_keylist, True)


def test_get_all_nondictionary_objs_ReturnsDict():
    # ESTABLISH
    y_dict = {}
    sports_str = "sports"
    run_str = "running"
    run_list = [sports_str, run_str]
    fun_str = "fun running"
    fun_list = [sports_str, run_str, fun_str]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_str = "mountains"
    mount_list = [sports_str, run_str, mount_str]
    mount_obj = "hard"

    frank_str = "franklin mountain"
    _2pm_str = "_2pm"
    _1am_str = "_1am"
    _2pm_list = [sports_str, run_str, frank_str, _2pm_str]
    _2pm_obj = "is hot"
    _1am_list = [sports_str, run_str, frank_str, _1am_str]
    _1am_obj = "is cool"
    rain_str = "raining"
    coat_str = "coat"
    fluf_str = "fluffy"
    button_str = "buttons"
    silver_obj = "silver"
    rain_list = [
        sports_str,
        run_str,
        frank_str,
        rain_str,
        coat_str,
        fluf_str,
        button_str,
    ]

    set_in_nested_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_2pm_list, x_obj=_2pm_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_1am_list, x_obj=_1am_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=rain_list, x_obj=silver_obj)
    print(y_dict)

    assert y_dict == {
        sports_str: {
            run_str: {
                fun_str: fun_obj,
                mount_str: mount_obj,
                frank_str: {
                    _2pm_str: _2pm_obj,
                    _1am_str: _1am_obj,
                    rain_str: {coat_str: {fluf_str: {button_str: silver_obj}}},
                },
            }
        }
    }

    # WHEN
    childless_objs = get_all_nondictionary_objs(y_dict)

    # THEN
    assert childless_objs == {
        sports_str: [fun_obj, mount_obj, _2pm_obj, _1am_obj, silver_obj]
    }
    assert get_from_nested_dict(y_dict, _2pm_list) == _2pm_obj
    assert get_from_nested_dict(y_dict, mount_list) == mount_obj


def test_get_from_nested_dict_RaisesNestedError():
    # ESTABLISH
    y_dict = {}
    sports_str = "sports"
    run_str = "running"
    run_list = [sports_str, run_str]
    fun_str = "fun running"
    fun_list = [sports_str, run_str, fun_str]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_str = "mountains"
    mount_list = [sports_str, run_str, mount_str]
    mount_obj = "hard"

    frank_str = "franklin mountain"
    _2pm_str = "_2pm"
    _1am_str = "_1am"
    _2pm_list = [sports_str, run_str, frank_str, _2pm_str]
    _2pm_obj = "is hot"
    _1am_list = [sports_str, run_str, frank_str, _1am_str]
    _1am_obj = "is cool"

    set_in_nested_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_2pm_list, x_obj=_2pm_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_1am_list, x_obj=_1am_obj)
    assert get_from_nested_dict(y_dict, _2pm_list) == _2pm_obj

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_from_nested_dict(y_dict, [ex0.bowl])
    assert str(excinfo.value) == f"'{ex0.bowl}' failed at level 0."

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_from_nested_dict(y_dict, [sports_str, ex0.bowl])
    assert str(excinfo.value) == f"'{ex0.bowl}' failed at level 1."

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_from_nested_dict(y_dict, [sports_str, ex0.bowl, _2pm_str])
    assert str(excinfo.value) == f"'{ex0.bowl}' failed at level 1."


def test_get_from_nested_dict_ReturnsNoneWhen_if_missing_return_None_True():
    # ESTABLISH
    y_dict = {}
    sports_str = "sports"
    run_str = "running"
    run_list = [sports_str, run_str]
    fun_str = "fun running"
    fun_list = [sports_str, run_str, fun_str]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_str = "mountains"
    mount_list = [sports_str, run_str, mount_str]
    mount_obj = "hard"

    frank_str = "franklin mountain"
    _2pm_str = "_2pm"
    _1am_str = "_1am"
    _2pm_list = [sports_str, run_str, frank_str, _2pm_str]
    _2pm_obj = "is hot"
    _1am_list = [sports_str, run_str, frank_str, _1am_str]
    _1am_obj = "is cool"

    set_in_nested_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_2pm_list, x_obj=_2pm_obj)
    set_in_nested_dict(x_dict=y_dict, x_keylist=_1am_list, x_obj=_1am_obj)
    assert (
        get_from_nested_dict(y_dict, _2pm_list, if_missing_return_None=True) == _2pm_obj
    )

    # WHEN / THEN
    assert get_from_nested_dict(y_dict, [ex0.bowl], if_missing_return_None=True) is None

    # WHEN / THEN
    x_value = get_from_nested_dict(
        y_dict, [sports_str, ex0.bowl], if_missing_return_None=True
    )
    assert x_value is None

    # WHEN / THEN
    x_value = get_from_nested_dict(
        y_dict, [sports_str, ex0.bowl, _2pm_str], if_missing_return_None=True
    )
    assert x_value is None


def test_get_positive_int_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_positive_int(None) == 0
    assert get_positive_int("sports") == 0
    assert get_positive_int() == 0
    assert get_positive_int(10) == 10
    assert get_positive_int(10.0) == 10
    assert get_positive_int(10.8) == 10
    assert get_positive_int(-10.8) == 0


def test_extract_csv_headers_ReturnsObj_empty_list():
    # ESTABLISH
    x_csv = ""

    # WHEN
    x_headers = extract_csv_headers(x_csv)

    # THEN
    assert x_headers == []


def test_extract_csv_headers_ReturnsObj():
    # ESTABLISH
    x_csv = """x_id,y_id,w_id,u_id,z_id
amy,Sue,Bob,13,29
amy,Sue,Sue,11,23
amy,Sue,Yao,41,37
"""

    # WHEN
    x_headers, x_csv = extract_csv_headers(x_csv)

    # THEN
    x_id_str = "x_id"
    y_id_str = "y_id"
    w_id_str = "w_id"
    u_id_str = "u_id"
    z_id_str = "z_id"
    assert x_headers == [
        x_id_str,
        y_id_str,
        w_id_str,
        u_id_str,
        z_id_str,
    ]


def test_extract_csv_headers_RemovesHeaders_csv():
    # ESTABLISH
    x_csv = """x_id,y_id,w_id,u_id,z_id
amy,Sue,Bob,13,29
amy,Sue,Sue,11,23
amy,Sue,Yao,41,37
"""

    # WHEN
    x_headers, new_csv = extract_csv_headers(x_csv)

    # THEN
    print(f"{new_csv=}")
    headerless_csv = """amy,Sue,Bob,13,29
amy,Sue,Sue,11,23
amy,Sue,Yao,41,37
"""
    assert new_csv == headerless_csv


def test_get_csv_column1_column2_metrics_ReturnsObj_empty_dict():
    # ESTABLISH
    headerless_csv = ""

    # WHEN
    x_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {}


def test_get_csv_column1_column2_metrics_ReturnsObj_Scenario1():
    # ESTABLISH
    x_id = "amy56"
    y_id = ex0.yao
    headerless_csv = f"""{x_id},{y_id},Bob,13,29
"""

    # WHEN
    x_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {x_id: {y_id: 1}}


def test_get_csv_column1_column2_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    x_id = "amy56"
    headerless_csv = f"""{x_id},{ex0.sue},Bob,13,29
{x_id},{ex0.sue},Sue,11,23
{x_id},{ex0.sue},Yao,41,37
{x_id},{ex0.sue},Zia,41,37
{x_id},{ex0.bob},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_column1_column2_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {x_id: {ex0.sue: 1}}
    assert u_dict == {x_id: {ex0.sue: 4, ex0.bob: 1}}


def test_create_l2nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    x_id = "amy56"

    headerless_csv = f""",,{x_id},{ex0.sue},Bob,13,29
,,{x_id},{ex0.sue},Sue,11,23
,,{x_id},{ex0.sue},Yao,41,37
,,{x_id},{ex0.sue},Zia,41,37
,,{x_id},{ex0.bob},Yao,41,37
"""

    # WHEN
    u_dict = create_l2nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f""",,{x_id},{ex0.sue},Bob,13,29
,,{x_id},{ex0.sue},Sue,11,23
,,{x_id},{ex0.sue},Yao,41,37
,,{x_id},{ex0.sue},Zia,41,37
"""
    static_bob_csv = f""",,{x_id},{ex0.bob},Yao,41,37
"""
    generated_sue_bob_dict = u_dict.get(x_id)
    assert generated_sue_bob_dict
    assert list(generated_sue_bob_dict.keys()) == [ex0.sue, ex0.bob]
    generated_bob_csv = generated_sue_bob_dict.get(ex0.bob)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_sue_bob_dict.get(ex0.sue)
    assert generated_sue_csv == static_sue_csv
    sue_bob_csv_dict = {ex0.sue: static_sue_csv, ex0.bob: static_bob_csv}
    assert u_dict == {x_id: sue_bob_csv_dict}


def test_create_l2nested_csv_dict_ReturnsObj_Scenario1_Multiple1stLevels():
    # ESTABLISH
    amy3_id = "amy3"
    amy4_id = "amy4"

    headerless_csv = f""",,{amy3_id},{ex0.sue},Bob,13,29
,,{amy4_id},{ex0.sue},Sue,11,23
,,{amy4_id},{ex0.sue},Yao,41,37
,,{amy4_id},{ex0.sue},Zia,41,37
,,{amy4_id},{ex0.bob},Yao,41,37
"""

    # WHEN
    tiered_dict = create_l2nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    amy3_sue_csv = f""",,{amy3_id},{ex0.sue},Bob,13,29
"""
    amy4_sue_csv = f""",,{amy4_id},{ex0.sue},Sue,11,23
,,{amy4_id},{ex0.sue},Yao,41,37
,,{amy4_id},{ex0.sue},Zia,41,37
"""
    static_bob_csv = f""",,{amy4_id},{ex0.bob},Yao,41,37
"""
    amy3_dict = tiered_dict.get(amy3_id)
    amy4_dict = tiered_dict.get(amy4_id)
    assert amy3_dict
    assert amy4_dict
    assert list(amy3_dict.keys()) == [ex0.sue]
    assert list(amy4_dict.keys()) == [ex0.sue, ex0.bob]
    generated_bob_csv = amy4_dict.get(ex0.bob)
    assert generated_bob_csv == static_bob_csv
    generated3_sue_csv = amy3_dict.get(ex0.sue)
    generated4_sue_csv = amy4_dict.get(ex0.sue)
    print(f"{generated3_sue_csv=}")
    print(f"{generated4_sue_csv=}")
    assert generated3_sue_csv == amy3_sue_csv
    assert generated4_sue_csv == amy4_sue_csv
    people3_csv_dict = {ex0.sue: amy3_sue_csv}
    people4_csv_dict = {ex0.sue: amy4_sue_csv, ex0.bob: static_bob_csv}
    assert tiered_dict == {
        amy3_id: people3_csv_dict,
        amy4_id: people4_csv_dict,
    }


def test_get_positional_dict_ReturnsObj():
    # ESTABLISH

    x_list = [ex0.bob, ex0.sue, ex0.yao]

    # WHEN / THEN
    assert get_positional_dict([]) == {}
    assert get_positional_dict([ex0.bob]) == {ex0.bob: 0}
    assert get_positional_dict(x_list) == {ex0.bob: 0, ex0.sue: 1, ex0.yao: 2}


def test_add_headers_to_csv_ReturnsObj():
    # ESTABLISH
    six_str = "six"
    seven_str = "seven"
    headers = [ex0.bowl, six_str, seven_str]
    headerless_csv = """Bob,13,29
Sue,11,23
Yao,41,37
Zia,41,37
Yao,41,37
"""

    # WHEN
    gen_csv = add_headers_to_csv(headers, headerless_csv)

    # THEN
    assert gen_csv
    assert (
        gen_csv
        == f"""{ex0.bowl},{six_str},{seven_str}
{headerless_csv}"""
    )


def test_is_2d_with_unique_keys_ReturnsObj():
    # ESTABLISH

    # WHEN / THEN
    assert is_2d_with_unique_keys({})
    assert is_2d_with_unique_keys({ex0.sue: {}})
    assert is_2d_with_unique_keys({ex0.sue: {}, ex0.bob: {}}) is False
    assert is_2d_with_unique_keys({"bowl": 155, ex0.sue: {}, ex0.bob: {}}) is False
    assert is_2d_with_unique_keys({"bowl": 155, ex0.sue: {}})
    assert is_2d_with_unique_keys({ex0.casa: {"clean": ex0.bob}})
    assert is_2d_with_unique_keys({ex0.casa: {"clean": {ex0.bob: 13}}})
    x0_dict = {ex0.casa: {"clean": {ex0.bob: 13}, "bowl": {}}}
    assert not (is_2d_with_unique_keys(x0_dict))
    assert is_2d_with_unique_keys({ex0.casa: {"clean": {ex0.bob: 13}}, "school": 14})
    x1_dict = {ex0.casa: {"clean": {ex0.bob: 3}}, "school": {"clean": 1}}
    assert not (is_2d_with_unique_keys(x1_dict))
    assert is_2d_with_unique_keys({ex0.casa: {"school": {ex0.sue: {1: {}}}}})
    x2_dict = {ex0.casa: {"clean": {ex0.bob: 13}, "school": {"bowl": 14}}}
    assert not (is_2d_with_unique_keys(x2_dict))

    # No duplicate keys paired to dictionarys
    assert is_2d_with_unique_keys({ex0.casa: {"school": {ex0.casa: {1: {}}}}}) is False

    # No duplicate keys off levels
    assert is_2d_with_unique_keys({ex0.casa: {"school": {ex0.casa: {1: {}}}}}) is False
    assert is_2d_with_unique_keys({ex0.casa: {"school": {ex0.casa: 1}}}) is False


def test_get_nested_dict_keys_by_level_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_nested_dict_keys_by_level({}) == {}
    assert get_nested_dict_keys_by_level({ex0.sue: {}}) == {0: {ex0.sue}}
    x2_dict = {ex0.sue: {}, ex0.bob: {}}
    assert get_nested_dict_keys_by_level(x2_dict) == {0: {ex0.sue, ex0.bob}}
    x3_dict = {"bowl": 155, ex0.sue: {}, ex0.bob: {}}
    assert get_nested_dict_keys_by_level(x3_dict) == {0: {ex0.sue, ex0.bob}}
    x4_dict = {"bowl": 155, ex0.sue: {ex0.zia: {}}, ex0.bob: {ex0.yao: {}}}
    expected_x4_dict = {0: {ex0.sue, ex0.bob}, 1: {ex0.zia, ex0.yao}}
    assert get_nested_dict_keys_by_level(x4_dict) == expected_x4_dict


def test_get_nested_keys_by_level_ReturnsObj():
    # ESTABLISH

    #  WHEN / THEN
    assert get_nested_keys_by_level({}) == {}
    assert get_nested_keys_by_level({ex0.sue: 1}) == {0: {ex0.sue}}
    assert get_nested_keys_by_level({ex0.sue: {}}) == {0: {ex0.sue}}
    x2_dict = {ex0.sue: {}, ex0.bob: {}}
    assert get_nested_keys_by_level(x2_dict) == {0: {ex0.sue, ex0.bob}}
    x3_dict = {ex0.bowl: 155, ex0.sue: {}, ex0.bob: {}}
    assert get_nested_keys_by_level(x3_dict) == {0: {ex0.bowl, ex0.sue, ex0.bob}}
    x4_dict = {ex0.bowl: 155, ex0.sue: {ex0.zia: {}}, ex0.bob: {ex0.yao: {ex0.bowl: 1}}}
    expected_x4_dict = {
        0: {ex0.sue, ex0.bob, ex0.bowl},
        1: {ex0.zia, ex0.yao},
        2: {ex0.bowl},
    }
    assert get_nested_keys_by_level(x4_dict) == expected_x4_dict


def test_get_nested_non_dict_keys_by_level_ReturnsObj():
    # ESTABLISH

    #  WHEN / THEN
    assert get_nested_non_dict_keys_by_level({}) == {}
    assert get_nested_non_dict_keys_by_level({ex0.sue: 1}) == {0: {ex0.sue}}
    assert get_nested_non_dict_keys_by_level({ex0.sue: {}}) == {0: set()}
    x2_dict = {ex0.sue: {}, ex0.bob: {}}
    assert get_nested_non_dict_keys_by_level(x2_dict) == {0: set()}
    x3_dict = {ex0.bowl: 155, ex0.sue: {}, ex0.bob: {}}
    assert get_nested_non_dict_keys_by_level(x3_dict) == {0: {ex0.bowl}}
    x4_dict = {ex0.bowl: 155, ex0.sue: {ex0.zia: {}}, ex0.bob: {ex0.yao: {ex0.bowl: 1}}}
    expected_x4_dict = {0: {ex0.bowl}, 1: set(), 2: {ex0.bowl}}
    assert get_nested_non_dict_keys_by_level(x4_dict) == expected_x4_dict


def test_get_nested_non_dict_keys_list_ReturnsObj():
    # ESTABLISH
    run_str = "run"

    #  WHEN / THEN
    assert get_nested_non_dict_keys_list({}) == []
    assert get_nested_non_dict_keys_list({ex0.sue: 1}) == [ex0.sue]
    assert get_nested_non_dict_keys_list({ex0.sue: {}}) == []
    x2_dict = {ex0.sue: {}, ex0.bob: {}}
    assert get_nested_non_dict_keys_list(x2_dict) == []
    x3_dict = {ex0.bowl: 155, ex0.sue: {}, ex0.bob: {}}
    assert get_nested_non_dict_keys_list(x3_dict) == [ex0.bowl]
    x4_dict = {ex0.bowl: 155, ex0.sue: {ex0.zia: {}}, ex0.bob: {ex0.yao: {run_str: 1}}}
    assert get_nested_non_dict_keys_list(x4_dict) == [ex0.bowl, run_str]
    x5_dict = {"casa": {"clean": {ex0.bob: 13}}, "school": 14}
    assert get_nested_non_dict_keys_list(x5_dict) == ["school", ex0.bob]


def test_get_nested_dict_key_by_level_RaisesError_is_2d_with_unique_keys_IsFalse():
    # ESTABLISH / WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        get_nested_dict_key_by_level({ex0.sue: {}, ex0.bob: {}})
    exception_str = "dictionary is not 2d_with_unique_keys."
    assert str(excinfo.value) == exception_str


def test_get_nested_dict_key_by_level_ReturnsObj():
    # ESTABLISH /  WHEN / THEN
    assert get_nested_dict_key_by_level({}) == []
    assert get_nested_dict_key_by_level({ex0.sue: {}}) == [ex0.sue]
    x4_dict = {"bowl": 155, ex0.sue: {ex0.bob: {ex0.yao: {}}}}
    assert get_nested_dict_key_by_level(x4_dict) == [ex0.sue, ex0.bob, ex0.yao]


def test_create_2d_array_from_dict_RaisesError_is_2d_with_unique_keys_IsFalse():
    # ESTABLISH / WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_2d_array_from_dict({ex0.sue: {}, ex0.bob: {}})
    exception_str = "dictionary is not 2d_with_unique_keys."
    assert str(excinfo.value) == exception_str


def test_create_2d_array_from_dict_ReturnsObj_Scenario0_Simple():
    # ESTABLISH
    x1_int = 1

    # WHEN / THEN
    assert create_2d_array_from_dict({}) == [[], []]
    assert create_2d_array_from_dict({ex0.sue: x1_int}) == [[ex0.sue], [x1_int]]
    assert create_2d_array_from_dict({ex0.sue: {}}) == [[], []]
    x0_2d_array = [["bowl"], [155]]
    assert create_2d_array_from_dict({"bowl": 155, ex0.sue: {}}) == x0_2d_array
    x1_2d_array = [["clean"], [ex0.bob]]
    assert create_2d_array_from_dict({"casa": {"clean": ex0.bob}}) == x1_2d_array
    x2_2d_array = [[ex0.bob], [13]]
    assert create_2d_array_from_dict({"casa": {"clean": {ex0.bob: 13}}}) == x2_2d_array
    x2_2d_dict = {"casa": {"clean": {ex0.bob: 13}}, "school": 14}
    x2_2d_array = [["school", ex0.bob], [14, 13]]
    assert create_2d_array_from_dict(x2_2d_dict) == x2_2d_array


def test_str_in_dict_keys_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_dict_keys("", {}) is False
    assert str_in_dict_keys("", {"": ex0.sue})
    assert str_in_dict_keys("", {ex0.sue: ex0.sue})
    assert str_in_dict_keys(ex0.sue, {ex0.sue: ex0.bob})
    assert str_in_dict_keys(ex0.sue, {ex0.zia: ex0.bob}) is False
    assert str_in_dict_keys(ex0.sue, {ex0.SueAndZia: ex0.bob})
    assert str_in_dict_keys(ex0.sue, {ex0.zia: ex0.bob}) is False
    assert str_in_dict_keys(ex0.sue, {ex0.bob: ex0.SueAndZia}) is False
    assert str_in_dict_keys(ex0.sue, {ex0.bob: ex0.zia}) is False


def test_str_in_dict_values_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_dict_values("", {}) is False
    assert str_in_dict_values("", {"": ex0.sue})
    assert str_in_dict_values("", {ex0.sue: ex0.sue})
    assert str_in_dict_values(ex0.sue, {ex0.sue: ex0.bob}) is False
    assert str_in_dict_values(ex0.sue, {ex0.zia: ex0.bob}) is False
    assert str_in_dict_values(ex0.sue, {ex0.SueAndZia: ex0.bob}) is False
    assert str_in_dict_values(ex0.sue, {ex0.zia: ex0.bob}) is False
    assert str_in_dict_values(ex0.sue, {ex0.bob: ex0.SueAndZia})
    assert str_in_dict_values(ex0.sue, {ex0.bob: ex0.zia}) is False


def test_str_in_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_dict("", {}) is False
    assert str_in_dict("", {"": ex0.sue})
    assert str_in_dict("", {ex0.sue: ex0.sue})
    assert str_in_dict(ex0.sue, {ex0.sue: ex0.bob})
    assert str_in_dict(ex0.sue, {ex0.zia: ex0.bob}) is False
    assert str_in_dict(ex0.sue, {ex0.SueAndZia: ex0.bob})
    assert str_in_dict(ex0.sue, {ex0.zia: ex0.bob}) is False
    assert str_in_dict(ex0.sue, {ex0.bob: ex0.SueAndZia})
    assert str_in_dict(ex0.sue, {ex0.bob: ex0.zia}) is False


def test_get_str_in_sub_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_str_in_sub_dict("", {}) == {}
    assert get_str_in_sub_dict("", {"": ex0.sue}) == {"": ex0.sue}
    assert get_str_in_sub_dict("", {ex0.sue: ex0.sue}) == {ex0.sue: ex0.sue}
    assert get_str_in_sub_dict(ex0.sue, {ex0.sue: ex0.bob}) == {ex0.sue: ex0.bob}
    assert get_str_in_sub_dict(ex0.sue, {ex0.zia: ex0.bob}) == {}
    x0_dict = {ex0.SueAndZia: ex0.bob}
    assert get_str_in_sub_dict(ex0.sue, {ex0.SueAndZia: ex0.bob}) == x0_dict
    assert get_str_in_sub_dict(ex0.sue, {ex0.zia: ex0.bob}) == {}
    x1_dict = {ex0.bob: ex0.SueAndZia}
    assert get_str_in_sub_dict(ex0.sue, {ex0.bob: ex0.SueAndZia}) == x1_dict
    assert get_str_in_sub_dict(ex0.sue, {ex0.bob: ex0.zia}) == {}

    xio_sue_dict = {ex0.xio: ex0.xio, ex0.sue: ex0.bob}
    assert get_str_in_sub_dict(ex0.sue, xio_sue_dict) == {ex0.sue: ex0.bob}
    xio_sueandzia_dict = {ex0.xio: ex0.xio, ex0.SueAndZia: ex0.bob}
    assert get_str_in_sub_dict(ex0.sue, xio_sueandzia_dict) == {ex0.SueAndZia: ex0.bob}
    xio_bob_dict = {ex0.xio: ex0.xio, ex0.bob: ex0.SueAndZia}
    assert get_str_in_sub_dict(ex0.sue, xio_bob_dict) == {ex0.bob: ex0.SueAndZia}


def test_str_in_all_dict_keys_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_all_dict_keys("", {})
    assert str_in_all_dict_keys("", {"": ex0.sue})
    assert str_in_all_dict_keys("", {ex0.sue: ex0.sue})
    assert not str_in_all_dict_keys(ex0.sue, {ex0.bob: ex0.sue})
    assert not str_in_all_dict_keys(ex0.sue, {ex0.sue: ex0.zia, ex0.bob: ex0.bob})
    assert not (
        str_in_all_dict_keys(ex0.sue, {ex0.zia: ex0.bob, ex0.SueAndZia: ex0.bob})
    )
    assert str_in_all_dict_keys(ex0.sue, {ex0.sue: ex0.bob, ex0.SueAndZia: ""})
    assert not str_in_all_dict_keys(ex0.sue, {ex0.bob: ex0.zia})


def test_str_in_all_dict_values_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_all_dict_values("", {})
    assert str_in_all_dict_values("", {"": ex0.sue})
    assert str_in_all_dict_values("", {ex0.sue: ex0.sue})
    assert str_in_all_dict_values(ex0.sue, {ex0.bob: ex0.sue})
    assert not (str_in_all_dict_values(ex0.sue, {ex0.zia: ex0.sue, ex0.sue: ex0.bob}))
    assert not (
        str_in_all_dict_values(ex0.sue, {ex0.zia: ex0.sue, ex0.SueAndZia: ex0.bob})
    )
    assert str_in_all_dict_values(ex0.sue, {ex0.zia: ex0.sue, ex0.bob: ex0.SueAndZia})
    assert str_in_all_dict_values(ex0.sue, {ex0.bob: ex0.zia}) is False


def test_str_in_all_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert str_in_all_dict("", {})
    assert str_in_all_dict("", {"": ex0.sue})
    assert str_in_all_dict("", {ex0.sue: ex0.sue})
    assert str_in_all_dict(ex0.sue, {ex0.sue: ex0.bob}) is False
    assert str_in_all_dict(ex0.sue, {ex0.zia: ex0.sue, ex0.sue: ex0.bob}) is False
    assert str_in_all_dict(ex0.sue, {ex0.sue: ex0.sue, "SueZia": "SueBob"})
    assert str_in_all_dict(ex0.sue, {ex0.zia: ex0.sue, "SueZia": "SueZia"}) is False
    assert str_in_all_dict(ex0.sue, {ex0.bob: ex0.zia}) is False


def test_get_str_not_in_sub_dict_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_str_in_all_sub_dict("", {}) == {}
    assert get_str_in_all_sub_dict("", {"": ex0.sue}) == {}
    assert get_str_in_all_sub_dict("", {ex0.sue: ex0.sue}) == {}
    assert get_str_in_all_sub_dict(ex0.sue, {ex0.sue: ex0.bob}) == {ex0.sue: ex0.bob}
    assert get_str_in_all_sub_dict(ex0.sue, {ex0.zia: ex0.bob}) == {ex0.zia: ex0.bob}
    assert get_str_in_all_sub_dict(ex0.sue, {ex0.sue: ex0.SueAndZia}) == {}
    assert get_str_in_all_sub_dict(ex0.sue, {ex0.SueAndZia: ex0.bob}) == {
        ex0.SueAndZia: ex0.bob
    }
    assert get_str_in_all_sub_dict(ex0.sue, {ex0.zia: ex0.bob}) == {ex0.zia: ex0.bob}
    x_dict = {ex0.bob: "SueZia", ex0.sue: ex0.sue}
    assert get_str_in_all_sub_dict(ex0.sue, x_dict) == {ex0.bob: "SueZia"}
    assert get_str_in_all_sub_dict(ex0.sue, {ex0.bob: ex0.zia}) == {ex0.bob: ex0.zia}

    suezia_sue_dict = {"SueZia": "SueZia", ex0.sue: ex0.bob}
    assert get_str_in_all_sub_dict(ex0.sue, suezia_sue_dict) == {ex0.sue: ex0.bob}
    suezia_sueandzia_dict = {"SueZia": "SueZia", ex0.SueAndZia: ex0.bob}
    expected_x0_dict = {ex0.SueAndZia: ex0.bob}
    assert get_str_in_all_sub_dict(ex0.sue, suezia_sueandzia_dict) == expected_x0_dict
    suezia_bob_dict = {"SueZia": "SueZia", ex0.bob: ex0.SueAndZia}
    assert get_str_in_all_sub_dict(ex0.sue, suezia_bob_dict) == {ex0.bob: ex0.SueAndZia}


def test_get_sorted_list_of_dict_keys_ReturnsObj_WhenEmptyDict():
    # ESTABLISH / WHEN / THEN
    assert get_sorted_list_of_dict_keys({}, "age") == []


def test_get_sorted_list_of_dict_keys_ReturnsObj_WhenValues():
    # ESTABLISH
    x_dict = {
        ex0.sue: {"name": ex0.sue, "age": 55, "city": "NYC"},
        ex0.bob: {"name": ex0.bob, "age": 30, "city": "Dallas"},
        ex0.yao: {"name": ex0.yao, "age": 35, "city": "Paris"},
    }

    # WHEN
    x_list = get_sorted_list_of_dict_keys(x_dict, "age")

    # THEN
    assert x_list == [ex0.bob, ex0.yao, ex0.sue]


def test_get_sorted_list_of_dict_keys_ReturnsObj_WithValues():
    # ESTABLISH
    x_dict = {
        ex0.sue: {"name": ex0.sue, "age": 55, "city": "NYC"},
        ex0.bob: {"name": ex0.bob, "age": 30, "city": "Dallas"},
        ex0.yao: {"name": ex0.yao, "age": 35, "city": "Paris"},
    }

    # WHEN
    x_list = get_sorted_list_of_dict_keys(x_dict, "age", include_sort_values=True)

    # THEN
    assert x_list == [[ex0.bob, 30], [ex0.yao, 35], [ex0.sue, 55]]


def test_get_max_key_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    x_dict = {}
    # WHEN / THEN
    assert not get_max_key(x_dict)


def test_get_max_key_ReturnsObj_Scenario1_Simple():
    # ESTABLISH
    x_dict = {
        (1, "b", 3, "z"): 2.5,
        (1, "a", 2, "x"): 3.4,
        (3, "c", 5, "w"): 1.8,
    }
    # WHEN / THEN
    assert get_max_key(x_dict) == (1, "a", 2, "x")


def test_get_max_key_ReturnsObj_Scenario2_TupleOrdering():
    # ESTABLISH
    x_dict = {
        (1, "b", 3, "z"): 2.5,
        (2, "a", 1, "y"): 3.4,
        (1, "a", 2, "x"): 3.4,
        (3, "c", 5, "w"): 1.8,
    }
    # WHEN / THEN
    assert get_max_key(x_dict) == (1, "a", 2, "x")


def test_change_nested_key_Scenario0():
    # ESTABLISH
    d = {"a": {"b": {"c": 123}}}
    expected = {"a": {"b": {"new_c": 123}}}

    # WHEN
    result = change_nested_key(copy_deepcopy(d), ["a", "b", "c"], "new_c")

    # THEN
    assert result == expected


def test_change_nested_key_Scenario1():
    # ESTABLISH
    d = {"old": "value"}
    expected = {"new": "value"}

    # WHEN
    result = change_nested_key(copy_deepcopy(d), ["old"], "new")

    # THEN
    assert result == expected


def test_change_nested_key_Scenario2():
    # ESTABLISH
    d = {"a": {"b": {"c": 123}}}
    original = copy_deepcopy(d)

    # WHEN
    result = change_nested_key(d, ["a", "b", "missing_key"], "new_key")

    # THEN Should be unchanged
    assert result == original


def test_change_nested_key_Scenario3():
    # ESTABLISH
    d = {"x": {"y": {"z": {"target": "val"}}}}
    expected = {"x": {"y": {"z": {"renamed": "val"}}}}

    # WHEN
    result = change_nested_key(copy_deepcopy(d), ["x", "y", "z", "target"], "renamed")

    # THEN
    assert result == expected


def test_change_nested_key_Scenario4():
    # ESTABLISH
    d = {"a": {"b": 123}}
    original = copy_deepcopy(d)

    # WHEN
    result = change_nested_key(d, ["a", "b", "c"], "d")

    # THEN Should not raise error, but should not modify
    assert result == original


def test_modular_addition_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert modular_addition(x_int=1000, y_int=500, modulus=1440) == 60
    assert modular_addition(1000, 500, 1440) == 60
    assert modular_addition(1000, 1200, 1200) == 1000
    assert modular_addition(1000, 200, 1200) == 0
    assert modular_addition(1000, -2000, 1200) == 200


def test_set_modular_dict_values_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert set_modular_dict_values({}) == {}
    assert set_modular_dict_values({5: 1, 7: 3}) == {5: 1, 7: 3}
    assert set_modular_dict_values({500: 1}) == {500: 1}
    assert set_modular_dict_values({500: 508}) == {500: 8}
    assert set_modular_dict_values({1: 1}) == {1: 0}
    assert set_modular_dict_values({None: 5}) == {None: 5}
