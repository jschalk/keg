from os.path import exists as os_path_exists
from pandas import DataFrame
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch17_idea.brick_db_tool import (
    get_ordered_csv,
    get_relevant_columns_dataframe,
    save_dataframe_to_csv,
)
from src.ch17_idea.test._util.ch17_examples import (
    get_empty_dataframe,
    get_ex01_dataframe,
    get_ex01_ordered_by_count_bob_csv,
    get_ex01_ordered_by_count_csv,
    get_ex01_ordered_by_count_x_boolean_csv,
    get_ex01_ordered_by_fay_csv,
    get_ex01_unordered_csv,
    get_ex02_atom_csv,
    get_ex02_atom_dataframe,
    get_small_example01_csv,
    get_small_example01_dataframe,
)
from src.ref.keywords import Ch17Keywords as kw


def test_get_ordered_csv_ReturnsObj():
    # ESTABLISH
    empty_dt = get_empty_dataframe()
    empty_csv = get_ordered_csv(empty_dt).replace("\r", "")
    x1_dt = get_ex01_dataframe()
    unordered_csv = get_ex01_unordered_csv()
    fay_csv = get_ex01_ordered_by_fay_csv()
    count_csv = get_ex01_ordered_by_count_csv()
    count_bob_csv = get_ex01_ordered_by_count_bob_csv()
    count_bool_csv = get_ex01_ordered_by_count_x_boolean_csv()

    # WHEN / THEN
    # print(f"    {empty_csv=}")
    # print(f"{unordered_csv=}")
    assert get_ordered_csv(empty_dt) == """\n"""
    fay0_order = ["fay", "bob", "x_boolean", "count"]
    count0_order = ["count", "fay", "bob", "x_boolean"]
    count0_bob1_order = ["count", "bob", "fay", "x_boolean"]
    count0_xboolean1_order = ["count", "x_boolean", "fay", "bob"]
    print(f"                                {count_bool_csv=}")
    print(f"{get_ordered_csv(x1_dt, count0_xboolean1_order)=}")
    assert get_ordered_csv(x1_dt, fay0_order) != unordered_csv
    assert get_ordered_csv(x1_dt, fay0_order) == fay_csv
    assert get_ordered_csv(x1_dt, count0_order) == count_csv
    assert get_ordered_csv(x1_dt, count0_bob1_order) == count_bob_csv
    assert get_ordered_csv(x1_dt, count0_xboolean1_order) == count_bool_csv
    # have sorting work even if sorting column does not exist
    count0_vic1_bob2_order = ["count", "vic", "bob", "fay", "x_boolean"]
    assert get_ordered_csv(x1_dt, count0_vic1_bob2_order) == count_bob_csv


def test_save_dataframe_to_csv_SavesFile_Scenario0_SmallDataFrame(
    temp3_fs,
):
    # ESTABLISH
    env_dir = str(temp3_fs)
    small_dt = get_small_example01_dataframe()
    ex_filename = "Faybob.csv"
    ex_file_path = create_path(env_dir, ex_filename)
    assert os_path_exists(ex_file_path) is False

    # WHEN
    save_dataframe_to_csv(small_dt, env_dir, ex_filename)

    # THEN
    assert os_path_exists(ex_file_path)
    small_example01_csv = get_small_example01_csv()
    assert open_file(env_dir, ex_filename) != small_example01_csv
    assert open_file(env_dir, ex_filename) != "\n\n\n\n"


def test_save_dataframe_to_csv_SavesFile_Scenario1_OrdersColumns(
    temp3_fs,
):
    # ESTABLISH
    env_dir = str(temp3_fs)
    atom_example_dt = get_ex02_atom_dataframe()
    ex_filename = "atom_example.csv"

    # WHEN
    save_dataframe_to_csv(atom_example_dt, env_dir, ex_filename)

    # THEN
    function_ex02_atom_csv = get_ex02_atom_csv()
    file_ex02_atom_csv = open_file(env_dir, ex_filename)
    print(f"{function_ex02_atom_csv=}")
    print(f"    {file_ex02_atom_csv=}")
    assert file_ex02_atom_csv == function_ex02_atom_csv


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario0():
    # ESTABLISH
    spam_str = "spam"
    df1 = DataFrame([["AAA", "BBB"]], columns=[spam_str, "egg"])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1)

    # THEN
    assert relevant_dataframe is not None
    assert not list(relevant_dataframe.columns)


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario1():
    # ESTABLISH
    spam_str = "spam"
    df1 = DataFrame([["AAA", "BBB"]], columns=[spam_str, "egg"])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1, [spam_str])

    # THEN
    assert relevant_dataframe is not None
    print(f"{type(relevant_dataframe.columns)=}")
    print(f"{relevant_dataframe.columns.to_list()=}")
    assert relevant_dataframe.columns.to_list() == [spam_str]


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario2_UnimportantOnesAreignored():
    # ESTABLISH
    spam_str = "spam"
    df1 = DataFrame([["AAA", "BBB"]], columns=[spam_str, "egg"])

    # WHEN
    relevant_columns = [spam_str, "not_relevant_else"]
    relevant_dataframe = get_relevant_columns_dataframe(df1, relevant_columns)

    # THEN
    assert relevant_dataframe is not None
    assert relevant_dataframe.columns.to_list() == [spam_str]


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario3_ColumnOrderCorrect():
    # ESTABLISH
    spam_str = "spam"
    egg_str = "egg"
    ham_str = "ham"
    df1 = DataFrame([["AAA", "BBB", "CCC"]], columns=[ham_str, spam_str, egg_str])

    # WHEN
    relevant_columns = [egg_str, spam_str, ham_str]
    relevant_dataframe = get_relevant_columns_dataframe(df1, relevant_columns)

    # THEN
    assert relevant_dataframe is not None
    print(f"{relevant_dataframe.columns=}")
    assert relevant_dataframe.columns.to_list() == relevant_columns
    assert relevant_dataframe.columns.to_list()[0] == egg_str


def test_get_relevant_columns_dataframe_ReturnsObj_Scenario4_ColumnOrderCorrect():
    # ESTABLISH
    df1 = DataFrame([["AAA", "BBB"]], columns=[kw.group_title, kw.contact_name])

    # WHEN
    relevant_dataframe = get_relevant_columns_dataframe(df1)

    # THEN
    assert relevant_dataframe is not None
    print(f"{relevant_dataframe.columns=}")
    assert relevant_dataframe.columns.to_list()[0] == kw.contact_name
    assert relevant_dataframe.columns.to_list() == [
        kw.contact_name,
        kw.group_title,
    ]
