from ch00_py.file_toolbox import open_json
from ch17_idea.idea_db_tool import create_idea_sorted_table
from ch18_etl_config._ref.ch18_path import create_last_run_metrics_path
from ch18_etl_config.etl_sqlstr import create_sound_and_heard_tables
from ch19_etl_steps.etl_main import create_last_run_metrics_json
from os.path import exists as os_path_exists
from ref.keywords import Ch19Keywords as kw
from sqlite3 import Cursor


def test_create_last_run_metrics_json_CreatesFile(cursor0: Cursor, temp3_fs):
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    moment_mstr_dir = str(temp3_fs)
    last_run_metrics_path = create_last_run_metrics_path(moment_mstr_dir)
    create_sound_and_heard_tables(cursor0)
    agg_ii00103_tablename = f"ii00103_{kw.ideax_agg}"
    agg_ii00103_columns = [kw.spark_num]
    create_idea_sorted_table(cursor0, agg_ii00103_tablename, agg_ii00103_columns)
    agg_ii00103_insert_sqlstr = f"""
INSERT INTO {agg_ii00103_tablename} ({kw.spark_num})
VALUES ('{spark1}'), ('{spark1}'), ('{spark9}');"""
    cursor0.execute(agg_ii00103_insert_sqlstr)

    agg_ii00144_tablename = f"ii00144_{kw.ideax_agg}"
    agg_ii00144_columns = [kw.spark_num]
    create_idea_sorted_table(cursor0, agg_ii00144_tablename, agg_ii00144_columns)
    agg_ii00144_insert_sqlstr = f"""
INSERT INTO {agg_ii00144_tablename} ({kw.spark_num})
VALUES ('{spark3}');"""
    cursor0.execute(agg_ii00144_insert_sqlstr)
    assert not os_path_exists(last_run_metrics_path)

    # WHEN
    create_last_run_metrics_json(cursor0, moment_mstr_dir)

    # THEN
    assert os_path_exists(last_run_metrics_path)
    last_run_metrics_dict = open_json(last_run_metrics_path)
    max_ideax_agg_spark_num_str = "max_ideax_agg_spark_num"
    assert max_ideax_agg_spark_num_str in set(last_run_metrics_dict.keys())
    max_ideax_agg_spark_num = last_run_metrics_dict.get(max_ideax_agg_spark_num_str)
    assert max_ideax_agg_spark_num == spark9
