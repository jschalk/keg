from os.path import exists as os_path_exists
from sqlite3 import Cursor
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import create_person_spark_dir_path
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename,
    create_sound_and_heard_tables,
)
from src.ch19_etl_main.etl_main import etl_heard_vld_to_spark_person_csvs
from src.ch19_etl_main.test._util.ch19_env import cursor0, get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_heard_vld_to_spark_person_csvs_PopulatesPersonPulabelTables(
    temp_dir_setup, cursor0: Cursor
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    spark3 = 3
    spark7 = 7
    yao_partner_cred_lumen5 = 5
    sue_partner_cred_lumen7 = 7
    put_agg_tablename = create_prime_tablename(kw.person_partnerunit, "h_vld", "put")
    put_agg_csv = f"{put_agg_tablename}.csv"
    x_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23_dash, exx.dash)
    a23_bob_e3_dir = create_person_spark_dir_path(x_dir, a23_lasso, bob_inx, spark3)
    a23_bob_e7_dir = create_person_spark_dir_path(x_dir, a23_lasso, bob_inx, spark7)
    a23_e3_prnptnr_put_path = create_path(a23_bob_e3_dir, put_agg_csv)
    a23_e7_prnptnr_put_path = create_path(a23_bob_e7_dir, put_agg_csv)

    create_sound_and_heard_tables(cursor0)
    insert_raw_sqlstr = f"""
INSERT INTO {put_agg_tablename} ({kw.spark_num},{kw.face_name},{kw.moment_rope},{kw.person_name},{kw.partner_name},{kw.partner_cred_lumen},{kw.knot})
VALUES
  ({spark3},'{sue_inx}','{exx.a23_dash}','{bob_inx}','{yao_inx}',{yao_partner_cred_lumen5},'{exx.dash}')
, ({spark7},'{sue_inx}','{exx.a23_dash}','{bob_inx}','{yao_inx}',{yao_partner_cred_lumen5},'{exx.dash}')
, ({spark7},'{sue_inx}','{exx.a23_dash}','{bob_inx}','{sue_inx}',{sue_partner_cred_lumen7},'{exx.dash}')
;
"""
    print(insert_raw_sqlstr)
    cursor0.execute(insert_raw_sqlstr)
    print(f"{a23_e3_prnptnr_put_path=}")
    print(f"{a23_e7_prnptnr_put_path=}")
    assert os_path_exists(a23_e3_prnptnr_put_path) is False
    assert os_path_exists(a23_e7_prnptnr_put_path) is False

    # WHEN
    etl_heard_vld_to_spark_person_csvs(cursor0, x_dir)

    # THEN
    assert os_path_exists(a23_e3_prnptnr_put_path)
    assert os_path_exists(a23_e7_prnptnr_put_path)
    e3_put_csv = open_file(a23_e3_prnptnr_put_path)
    e7_put_csv = open_file(a23_e7_prnptnr_put_path)
    print(f"{e3_put_csv=}")
    print(f"{e7_put_csv=}")
    expected_e3_put_csv = f"""spark_num,face_name,moment_rope,person_name,partner_name,partner_cred_lumen,partner_debt_lumen,knot
3,Suzy,{exx.a23_dash},Bobby,Bobby,5.0,,{exx.dash}
"""
    expected_e7_put_csv = f"""spark_num,face_name,moment_rope,person_name,partner_name,partner_cred_lumen,partner_debt_lumen,knot
7,Suzy,{exx.a23_dash},Bobby,Bobby,5.0,,{exx.dash}
7,Suzy,{exx.a23_dash},Bobby,Suzy,7.0,,{exx.dash}
"""
    assert e3_put_csv == expected_e3_put_csv
    assert e7_put_csv == expected_e7_put_csv
