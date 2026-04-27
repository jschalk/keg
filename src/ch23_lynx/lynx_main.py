from ch00_py.db_toolbox import get_db_tables
from ch00_py.file_toolbox import create_path, get_level1_dirs, open_json, save_json
from ch04_rope.rope import create_rope
from ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from ch09_person_lesson.lasso import lassounit_shop
from ch10_person_listen.keep_tool import open_job_file
from ch11_bud.bud_main import TranBook
from ch14_moment.moment_cell import (
    create_bud_mandate_ledgers,
    create_moment_persons_cell_trees,
    set_cell_tree_cell_mandates,
    set_cell_trees_decrees,
    set_cell_trees_found_facts,
)
from ch14_moment.moment_main import open_moment_file
from ch18_etl_config._ref.ch18_path import create_last_run_metrics_path
from ch18_etl_config.etl_sqlstr import create_job_tables
from ch19_etl_steps.obj2db_person import insert_job_obj
from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor


def get_max_ideax_agg_spark_num(cursor: sqlite3_Cursor) -> int:
    agg_tables = get_db_tables(cursor, "ideax_agg")
    ideax_aggs_max_spark_num = 0
    for agg_table in agg_tables:
        if agg_table.startswith("ii") and agg_table.endswith("ideax_agg"):
            sqlstr = f"SELECT MAX(spark_num) FROM {agg_table}"
            table_max_spark_num = cursor.execute(sqlstr).fetchone()[0] or 1
            if table_max_spark_num > ideax_aggs_max_spark_num:
                ideax_aggs_max_spark_num = table_max_spark_num
    return ideax_aggs_max_spark_num


def add_lynx_epoch_to_lynx_guts(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        x_momentunit.add_epoch_to_guts()


def etl_lynx_guts_to_lynx_jobs(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        x_momentunit.generate_all_jobs()


def etl_lynx_job_jsons_to_job_tables(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    create_job_tables(cursor)
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_rope = create_rope(moment_label)
        moment_lasso = lassounit_shop(moment_rope)
        moment_path = create_path(moments_dir, moment_label)
        persons_dir = create_path(moment_path, "persons")
        for person_name in get_level1_dirs(persons_dir):
            job_obj = open_job_file(moment_mstr_dir, moment_lasso, person_name)
            insert_job_obj(cursor, job_obj)


CREATE_MOMENT_CONTACT_NETS_SQLSTR = "CREATE TABLE IF NOT EXISTS moment_contact_nets (moment_rope TEXT, person_name TEXT, person_net_amount REAL)"


def insert_tranunit_contacts_net(cursor: sqlite3_Cursor, tranbook: TranBook):
    """
    Insert the net amounts for each contact in the tranbook into the specified table.

    :param cursor: SQLite cursor object
    :param tranbook: TranBook object containing transaction units
    :param dst_tablename: Name of the destination table
    """
    contacts_net_array = tranbook._get_contacts_net_array()
    cursor.executemany(
        f"INSERT INTO moment_contact_nets (moment_rope, person_name, person_net_amount) VALUES ('{tranbook.moment_rope}', ?, ?)",
        contacts_net_array,
    )


def etl_moment_json_contact_nets_to_moment_contact_nets_table(
    cursor: sqlite3_Cursor, moment_mstr_dir: str
):
    cursor.execute(CREATE_MOMENT_CONTACT_NETS_SQLSTR)
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        x_momentunit.set_all_tranbook()
        insert_tranunit_contacts_net(cursor, x_momentunit.all_tranbook)


def create_last_run_metrics_json(cursor: sqlite3_Cursor, moment_mstr_dir: str):
    max_ideax_agg_spark_num = get_max_ideax_agg_spark_num(cursor)
    last_run_metrics_path = create_last_run_metrics_path(moment_mstr_dir)
    last_run_metrics_dict = {"max_ideax_agg_spark_num": max_ideax_agg_spark_num}
    save_json(last_run_metrics_path, None, last_run_metrics_dict)


def etl_create_buds_root_cells(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_dir = create_path(moments_dir, moment_label)
        moment_lasso = lassounit_shop(create_rope(moment_label))
        ote1_json_path = create_path(moment_dir, "moment_ote1_agg.json")
        if os_path_exists(ote1_json_path):
            ote1_dict = open_json(ote1_json_path)
            x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
            x_momentunit.create_buds_root_cells(ote1_dict)


def etl_create_moment_cell_trees(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        create_moment_persons_cell_trees(moment_mstr_dir, moment_lasso)


def etl_set_cell_trees_found_facts(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        set_cell_trees_found_facts(moment_mstr_dir, moment_lasso)


def etl_set_cell_trees_decrees(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        set_cell_trees_decrees(moment_mstr_dir, moment_lasso)


def etl_set_cell_tree_cell_mandates(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        set_cell_tree_cell_mandates(moment_mstr_dir, moment_lasso)


def etl_create_bud_mandate_ledgers(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        create_bud_mandate_ledgers(moment_mstr_dir, moment_lasso)


def calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir: str):
    etl_create_buds_root_cells(moment_mstr_dir)
    etl_create_moment_cell_trees(moment_mstr_dir)
    etl_set_cell_trees_found_facts(moment_mstr_dir)
    etl_set_cell_trees_decrees(moment_mstr_dir)
    etl_set_cell_tree_cell_mandates(moment_mstr_dir)
    etl_create_bud_mandate_ledgers(moment_mstr_dir)
