from ch00_py.csv_toolbox import open_csv_with_types
from ch00_py.db_toolbox import get_db_tables
from ch00_py.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_file,
    open_json,
    save_file,
    save_json,
)
from ch04_rope.rope import create_rope
from ch07_person_logic.person_main import PersonUnit, personunit_shop
from ch08_person_atom.atom_config import get_person_dimens
from ch08_person_atom.atom_main import personatom_shop
from ch09_person_lesson._ref.ch09_path import create_gut_path, create_moments_dir_path
from ch09_person_lesson.delta import get_minimal_persondelta
from ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from ch09_person_lesson.lesson_main import (
    LessonUnit,
    get_lessonunit_from_dict,
    lessonunit_shop,
)
from ch10_person_listen.keep_tool import open_job_file
from ch11_bud._ref.ch11_path import (
    create_person_spark_dir_path,
    create_personspark_path,
    create_spark_all_lesson_path,
)
from ch11_bud.bud_filehandler import (
    collect_person_spark_dir_sets,
    get_persons_downhill_spark_nums,
    open_person_file,
)
from ch11_bud.bud_main import TranBook
from ch14_moment.moment_cell import (
    create_bud_mandate_ledgers,
    create_moment_persons_cell_trees,
    set_cell_tree_cell_mandates,
    set_cell_trees_decrees,
    set_cell_trees_found_facts,
)
from ch14_moment.moment_main import open_moment_file
from ch17_idea.idea_config import get_idea_sqlite_types
from ch18_etl_config._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from ch18_etl_config.etl_sqlstr import create_job_tables, create_prime_tablename
from ch19_etl_steps.obj2db_person import insert_job_obj
from copy import deepcopy as copy_deepcopy
from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor


def etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir: str):
    idea_types = get_idea_sqlite_types()
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        csv_path = create_moment_ote1_csv_path(moment_mstr_dir, moment_lasso)
        csv_arrays = open_csv_with_types(csv_path, idea_types)
        x_dict = {}
        header_row = csv_arrays.pop(0)
        for row in csv_arrays:
            person_name = row[1]
            spark_num = row[2]
            bud_time = row[3]
            if x_dict.get(person_name) is None:
                x_dict[person_name] = {}
            person_dict = x_dict.get(person_name)
            person_dict[int(bud_time)] = spark_num
        json_path = create_moment_ote1_json_path(moment_mstr_dir, moment_lasso)
        save_json(json_path, None, x_dict)


def etl_spark_person_csvs_to_lesson_json(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        moment_path = create_path(moments_dir, moment_lasso.make_path())
        persons_path = create_path(moment_path, "persons")
        for person_name in get_level1_dirs(persons_path):
            person_path = create_path(persons_path, person_name)
            sparks_path = create_path(person_path, "sparks")
            for spark_num in get_level1_dirs(sparks_path):
                save_spark_lesson_json(
                    moment_mstr_dir, moment_lasso, person_name, spark_num, sparks_path
                )


def save_spark_lesson_json(
    moment_mstr_dir, moment_lasso, person_name, spark_num, sparks_path
):
    spark_lesson = lessonunit_shop(
        person_name=person_name,
        spark_face=None,
        moment_rope=moment_lasso.moment_rope,
        spark_num=spark_num,
    )
    spark_dir = create_path(sparks_path, spark_num)
    add_personatoms_from_csv(spark_lesson, spark_dir)
    spark_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    spark_lesson_json = spark_lesson.get_serializable_step_dict()
    save_json(spark_all_lesson_path, None, spark_lesson_json)


def add_personatoms_from_csv(spark_lesson: LessonUnit, spark_dir: str):
    idea_sqlite_types = get_idea_sqlite_types()
    person_dimens = get_person_dimens()
    person_dimens.remove("personunit")
    for person_dimen in person_dimens:
        person_dimen_put_tablename = create_prime_tablename(
            person_dimen, "h_vld", "put"
        )
        person_dimen_del_tablename = create_prime_tablename(
            person_dimen, "h_vld", "del"
        )
        person_dimen_put_csv = f"{person_dimen_put_tablename}.csv"
        person_dimen_del_csv = f"{person_dimen_del_tablename}.csv"
        put_path = create_path(spark_dir, person_dimen_put_csv)
        del_path = create_path(spark_dir, person_dimen_del_csv)
        if os_path_exists(put_path):
            put_rows = open_csv_with_types(put_path, idea_sqlite_types)
            headers = put_rows.pop(0)
            for put_row in put_rows:
                x_atom = personatom_shop(person_dimen, "INSERT")
                for col_name, row_value in zip(headers, put_row):
                    if col_name not in {
                        "spark_face",
                        "spark_num",
                        "moment_rope",
                        "person_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                spark_lesson.persondelta.set_personatom(x_atom)

        if os_path_exists(del_path):
            del_rows = open_csv_with_types(del_path, idea_sqlite_types)
            headers = del_rows.pop(0)
            for del_row in del_rows:
                x_atom = personatom_shop(person_dimen, "DELETE")
                for col_name, row_value in zip(headers, del_row):
                    if col_name not in {
                        "spark_face",
                        "spark_num",
                        "moment_rope",
                        "person_name",
                    }:
                        x_atom.set_arg(col_name, row_value)
                spark_lesson.persondelta.set_personatom(x_atom)


def etl_spark_lesson_json_to_spark_inherited_personunits(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_path = create_path(moments_dir, moment_label)
        moment_rope = create_rope(moment_label)
        moment_lasso = lassounit_shop(moment_rope)
        persons_dir = create_path(moment_path, "persons")
        for person_name in get_level1_dirs(persons_dir):
            person_dir = create_path(persons_dir, person_name)
            sparks_dir = create_path(person_dir, "sparks")
            prev_spark_num = None
            for spark_num in get_level1_dirs(sparks_dir):
                prev_spark_num = create_lesson_json_and_get_spark_num(
                    moment_mstr_dir,
                    moment_lasso,
                    person_name,
                    prev_spark_num,
                    spark_num,
                )


def create_lesson_json_and_get_spark_num(
    moment_mstr_dir, moment_lasso, person_name, prev_spark_num, spark_num
):
    m_dir = moment_mstr_dir
    m_lasso = moment_lasso
    p_name = person_name
    prev_spark = prev_spark_num

    prev_person = _get_prev_spark_num_personunit(m_dir, m_lasso, p_name, prev_spark)
    personspark_path = create_personspark_path(m_dir, m_lasso, p_name, spark_num)
    spark_dir = create_person_spark_dir_path(m_dir, m_lasso, p_name, spark_num)
    all_lesson_path = create_spark_all_lesson_path(m_dir, m_lasso, p_name, spark_num)
    spark_lesson = get_lessonunit_from_dict(open_json(all_lesson_path))
    sift_delta = get_minimal_persondelta(spark_lesson.persondelta, prev_person)
    curr_person = spark_lesson.get_lesson_edited_person(prev_person)
    save_json(personspark_path, None, curr_person.to_dict())
    expressed_lesson = copy_deepcopy(spark_lesson)
    expressed_lesson.set_persondelta(sift_delta)
    expressed_lesson_json = expressed_lesson.get_serializable_step_dict()
    save_json(spark_dir, "expressed_lesson.json", expressed_lesson_json)
    return spark_num


def _get_prev_spark_num_personunit(
    moment_mstr_dir, moment_lasso: LassoUnit, person_name, prev_spark_num
) -> PersonUnit:
    if prev_spark_num is None:
        return personunit_shop(person_name, moment_lasso.moment_rope)
    prev_personspark_path = create_personspark_path(
        moment_mstr_dir, moment_lasso, person_name, prev_spark_num
    )
    return open_person_file(prev_personspark_path)


def etl_spark_inherited_personunits_to_lynx_gut(moment_mstr_dir: str):
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        person_sparks = collect_person_spark_dir_sets(moment_mstr_dir, moment_lasso)
        persons_max_spark_num_dict = get_persons_downhill_spark_nums(person_sparks)
        for person_name, max_spark_num in persons_max_spark_num_dict.items():
            max_personspark_path = create_personspark_path(
                moment_mstr_dir, moment_lasso, person_name, max_spark_num
            )
            max_spark_person_json = open_file(max_personspark_path)
            gut_path = create_gut_path(moment_mstr_dir, moment_lasso, person_name)
            save_file(gut_path, None, max_spark_person_json)


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
