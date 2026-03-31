from os.path import exists as os_path_exists
from pandas import DataFrame
from pandas.testing import assert_frame_equal
from sqlite3 import connect as sqlite3_connect
from src.ch00_py.file_toolbox import count_files, create_path, set_dir
from src.ch17_idea.idea_db_tool import open_csv
from src.ch20_kpi.kpi_mstr import create_kpi_csvs
from src.ref.keywords import Ch20Keywords as kw


def test_create_kpi_csvs_Scenario0_NotCreateFileWhenNoKPITables(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    db_path = create_path(temp_dir, "example3.db")
    set_dir(temp_dir)
    with sqlite3_connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        create_populate_table = (
            "CREATE TABLE test_table AS SELECT 'fay' as moment_rope;"
        )
        cursor.execute(create_populate_table)
    assert count_files(temp_dir) == 1

    # WHEN
    create_kpi_csvs(db_path, dst_dir=temp_dir)

    # THEN
    assert count_files(temp_dir) == 1
    db_conn.close()


def test_create_kpi_csvs_Scenario1_CreateFile(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    set_dir(temp_dir)
    db_path = create_path(temp_dir, "example2.db")
    kpi_tablename = "test_kpi_table"
    with sqlite3_connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        cursor.execute("CREATE TABLE test_table AS SELECT 'Fay' as moment_rope;")
        cursor.execute(f"CREATE TABLE {kpi_tablename} AS SELECT 'Fay' as moment_rope;")
    kpi_csv_path = create_path(temp_dir, f"{kpi_tablename}.csv")
    assert not os_path_exists(kpi_csv_path)

    # WHEN
    create_kpi_csvs(db_path, dst_dir=temp_dir)

    # THEN
    assert os_path_exists(kpi_csv_path)
    expected_df = DataFrame(["Fay"], columns=[kw.moment_rope])
    assert_frame_equal(open_csv(kpi_csv_path), expected_df)
    db_conn.close()
