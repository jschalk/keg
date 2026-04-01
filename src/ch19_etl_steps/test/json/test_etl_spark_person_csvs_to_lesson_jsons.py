from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import open_file, open_json, save_file
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_main import get_lessonunit_from_dict, lessonunit_shop
from src.ch11_bud._ref.ch11_path import (
    create_person_spark_dir_path as person_spark_dir,
    create_spark_all_lesson_path as all_lesson_path,
)
from src.ch18_etl_config.etl_sqlstr import create_prime_tablename
from src.ch19_etl_steps.etl_main import etl_spark_person_csvs_to_lesson_json
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_spark_person_csvs_to_lesson_json_CreatesFiles_Scenario0_IgnoresCSV_personunit(
    temp3_fs,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    spark3 = 3
    put_agg_tablename = create_prime_tablename(kw.personunit, kw.h_vld, "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, spark3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, spark7)
    a23_bob_e3_dir = person_spark_dir(moment_mstr_dir, a23_lasso, bob_inx, spark3)
    e3_put_csv = f"""{kw.spark_num},{kw.face_name},moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain
{spark3},{sue_inx},{exx.a23},{bob_inx},,,,,,,,
"""
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    e3_all_lesson_path = all_lesson_path(moment_mstr_dir, a23_lasso, bob_inx, spark3)
    assert os_path_exists(e3_all_lesson_path) is False

    # WHEN
    etl_spark_person_csvs_to_lesson_json(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_lesson_path)
    expected_e3_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark3)
    e3_lessonunit = get_lessonunit_from_dict(open_json(e3_all_lesson_path))
    assert e3_lessonunit.spark_num == expected_e3_lesson.spark_num
    expected_persondelta = expected_e3_lesson.persondelta
    generated_e3_persondelta = e3_lessonunit.persondelta
    assert generated_e3_persondelta.personatoms == expected_persondelta.personatoms
    assert e3_lessonunit.persondelta == expected_e3_lesson.persondelta
    assert e3_lessonunit == expected_e3_lesson


def test_etl_spark_person_csvs_to_lesson_json_CreatesFiles_Scenario1(
    temp3_fs,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    spark3 = 3
    spark7 = 7
    credit77 = 77
    credit88 = 88
    debt_empty = ""
    prncont_str = kw.person_contactunit
    put_agg_tablename = create_prime_tablename(prncont_str, kw.h_vld, "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, spark3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, spark7)
    a23_bob_e3_dir = person_spark_dir(moment_mstr_dir, a23_lasso, bob_inx, spark3)
    a23_bob_e7_dir = person_spark_dir(moment_mstr_dir, a23_lasso, bob_inx, spark7)
    e3_put_csv = f"""{kw.spark_num},{kw.face_name},{kw.moment_rope},{kw.person_name},{kw.contact_name},{kw.contact_cred_lumen},{kw.contact_debt_lumen}
{spark3},{sue_inx},{exx.a23},{bob_inx},{bob_inx},{credit77},{debt_empty}
"""
    e7_put_csv = f"""{kw.spark_num},{kw.face_name},{kw.moment_rope},{kw.person_name},{kw.contact_name},{kw.contact_cred_lumen},{kw.contact_debt_lumen}
{spark7},{sue_inx},{exx.a23},{bob_inx},{bob_inx},{credit77},{debt_empty}
{spark7},{sue_inx},{exx.a23},{bob_inx},{sue_inx},{credit88},{debt_empty}
"""
    print(f"     {a23_bob_e3_dir=}  {put_agg_csv_filename}")
    print(f"     {a23_bob_e7_dir=}  {put_agg_csv_filename}")
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    save_file(a23_bob_e7_dir, put_agg_csv_filename, e7_put_csv)
    e3_all_lesson_path = all_lesson_path(moment_mstr_dir, a23_lasso, bob_inx, spark3)
    e7_all_lesson_path = all_lesson_path(moment_mstr_dir, a23_lasso, bob_inx, spark7)
    print(f"   {e3_all_lesson_path=}")
    print(f"   {e7_all_lesson_path=}")
    assert os_path_exists(e3_all_lesson_path) is False
    assert os_path_exists(e7_all_lesson_path) is False

    # WHEN
    etl_spark_person_csvs_to_lesson_json(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_lesson_path)
    assert os_path_exists(e7_all_lesson_path)
    # print(f"{open_file(e3_lesson_path)=}")
    # print(f"{open_file(e7_lesson_path)=}")
    # lessons_dir = create_path(fay_wdir.moment_mstr_dir, "lessons")
    # atoms_dir = create_path(fay_wdir.moment_mstr_dir, "atoms")
    # e3_lesson = lessonunit_shop(bob_inx, sue_inx, exx.a23, lessons_dir, atoms_dir, spark3)
    # e7_lesson = lessonunit_shop(bob_inx, sue_inx, exx.a23, lessons_dir, atoms_dir, spark7)
    expected_e3_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark3)
    expected_e7_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark7)
    prncont_dimen = kw.person_contactunit
    expected_e3_lesson.persondelta.add_personatom(
        prncont_dimen,
        kw.INSERT,
        jkeys={kw.contact_name: bob_inx},
        jvalues={kw.contact_cred_lumen: credit77, kw.contact_debt_lumen: None},
    )
    expected_e7_lesson.persondelta.add_personatom(
        prncont_dimen,
        kw.INSERT,
        jkeys={kw.contact_name: bob_inx},
        jvalues={kw.contact_cred_lumen: credit77, kw.contact_debt_lumen: None},
    )
    expected_e7_lesson.persondelta.add_personatom(
        prncont_dimen,
        kw.INSERT,
        jkeys={kw.contact_name: sue_inx},
        jvalues={kw.contact_cred_lumen: credit88, kw.contact_debt_lumen: None},
    )
    e3_lessonunit = get_lessonunit_from_dict(open_json(e3_all_lesson_path))
    e7_lessonunit = get_lessonunit_from_dict(open_json(e7_all_lesson_path))
    # print(f"{e7_lessonunit=}")
    assert e3_lessonunit.spark_num == expected_e3_lesson.spark_num
    expected_persondelta = expected_e3_lesson.persondelta
    generated_e3_persondelta = e3_lessonunit.persondelta
    assert generated_e3_persondelta.personatoms == expected_persondelta.personatoms
    assert e3_lessonunit.persondelta == expected_e3_lesson.persondelta
    assert e3_lessonunit == expected_e3_lesson
    e7_insert = e7_lessonunit.persondelta.personatoms.get("INSERT")
    expected_e7_insert = expected_e7_lesson.persondelta.personatoms.get("INSERT")
    # print(e7_insert.get("person_contactunit").keys())
    # print(expected_e7_insert.get("person_contactunit").keys())
    e7_prncont = e7_insert.get("person_contactunit")
    expected_e7_prncont = expected_e7_insert.get("person_contactunit")
    assert e7_prncont.keys() == expected_e7_prncont.keys()
    # print(f"{expected_e7_insert.keys()=}")
    assert e7_insert == expected_e7_insert
    assert e7_lessonunit.persondelta == expected_e7_lesson.persondelta
    assert e7_lessonunit == expected_e7_lesson
