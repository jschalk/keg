from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch07_person_logic.person_main import get_personunit_from_dict, personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_gut_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import create_person_spark_dir_path
from src.ch19_etl_steps.etl_main import etl_spark_inherited_personunits_to_moment_gut
from src.ref.keywords import ExampleStrs as exx

# create test where spark create_person_spark_dir_path()
# test that budunit with depth 0 is able to create
# test that budunit with depth 1 is able to create nested personunits directories and populate with spark relevant


def test_etl_spark_inherited_personunits_to_moment_gut_SetsFiles_Scenario0(
    temp3_fs,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    a23_bob_e3_dir = create_person_spark_dir_path(mstr_dir, a23_lasso, bob_inx, spark3)
    a23_bob_e7_dir = create_person_spark_dir_path(mstr_dir, a23_lasso, bob_inx, spark7)
    person_filename = "person.json"
    e3_bob_person = personunit_shop(bob_inx, exx.a23)
    e7_bob_person = personunit_shop(bob_inx, exx.a23)
    e3_bob_person.add_contactunit(bob_inx, credit77)
    e3_bob_person.add_contactunit(yao_inx, credit44)
    e7_bob_person.add_contactunit(bob_inx, credit77)
    e7_bob_person.add_contactunit(sue_inx, credit88)
    e7_bob_person.add_contactunit(yao_inx, credit44)
    save_json(a23_bob_e3_dir, person_filename, e3_bob_person.to_dict())
    save_json(a23_bob_e7_dir, person_filename, e7_bob_person.to_dict())
    e3_person_path = create_path(a23_bob_e3_dir, person_filename)
    e7_person_path = create_path(a23_bob_e7_dir, person_filename)
    assert os_path_exists(e3_person_path)
    assert os_path_exists(e7_person_path)
    print(e3_person_path)
    print(e7_person_path)
    a23_bob_gut_path = create_gut_path(mstr_dir, a23_lasso, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_spark_inherited_personunits_to_moment_gut(mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_person = get_personunit_from_dict(open_json(a23_bob_gut_path))
    assert generated_gut_person.contacts == e7_bob_person.contacts
    assert generated_gut_person == e7_bob_person
    assert generated_gut_person.to_dict() == e7_bob_person.to_dict()
