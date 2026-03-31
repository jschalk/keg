from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch07_person_logic.person_main import get_personunit_from_dict, personunit_shop
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_main import get_lessonunit_from_dict, lessonunit_shop
from src.ch11_bud._ref.ch11_path import (
    create_person_spark_dir_path,
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path,
)
from src.ch19_etl_main.etl_main import (
    etl_spark_lesson_json_to_spark_inherited_personunits,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_etl_spark_lesson_json_to_spark_inherited_personunits_SetsFiles_person_json(
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
    a23_lasso = lassounit_shop(exx.a23)
    x_dir = str(temp3_fs)
    a23_bob_e3_dir = create_person_spark_dir_path(x_dir, a23_lasso, bob_inx, spark3)
    a23_bob_e7_dir = create_person_spark_dir_path(x_dir, a23_lasso, bob_inx, spark7)
    a23_bob_e3_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark3)
    a23_bob_e7_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark7)
    prnptnr_dimen = kw.person_partnerunit
    bob_jkeys = {kw.partner_name: bob_inx}
    bob_jvalues = {kw.partner_cred_lumen: credit77, kw.partner_debt_lumen: None}
    yao_jkeys = {kw.partner_name: yao_inx}
    yao_jvalues = {kw.partner_cred_lumen: credit44, kw.partner_debt_lumen: None}
    a23_bob_e3_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {kw.partner_name: sue_inx}
    sue_jvalues = {kw.partner_cred_lumen: credit88, kw.partner_debt_lumen: None}
    a23_bob_e7_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, sue_jkeys, sue_jvalues)
    e3_all_lesson_path = create_spark_all_lesson_path(x_dir, a23_lasso, bob_inx, spark3)
    e7_all_lesson_path = create_spark_all_lesson_path(x_dir, a23_lasso, bob_inx, spark7)
    save_json(e3_all_lesson_path, None, a23_bob_e3_lesson.get_serializable_step_dict())
    save_json(e7_all_lesson_path, None, a23_bob_e7_lesson.get_serializable_step_dict())
    assert os_path_exists(e3_all_lesson_path)
    assert os_path_exists(e7_all_lesson_path)
    person_filename = "person.json"
    e3_person_path = create_path(a23_bob_e3_dir, person_filename)
    e7_person_path = create_path(a23_bob_e7_dir, person_filename)
    assert os_path_exists(e3_person_path) is False
    assert os_path_exists(e7_person_path) is False

    # WHEN
    etl_spark_lesson_json_to_spark_inherited_personunits(x_dir)

    # THEN
    assert os_path_exists(e3_person_path)
    assert os_path_exists(e7_person_path)
    expected_e3_bob_person = personunit_shop(bob_inx, exx.a23)
    expected_e7_bob_person = personunit_shop(bob_inx, exx.a23)
    expected_e3_bob_person.add_partnerunit(bob_inx, credit77)
    expected_e3_bob_person.add_partnerunit(yao_inx, credit44)
    expected_e7_bob_person.add_partnerunit(bob_inx, credit77)
    expected_e7_bob_person.add_partnerunit(sue_inx, credit88)
    expected_e7_bob_person.add_partnerunit(yao_inx, credit44)
    generated_e3_person = get_personunit_from_dict(open_json(e3_person_path))
    generated_e7_person = get_personunit_from_dict(open_json(e7_person_path))
    assert generated_e3_person.partners == expected_e3_bob_person.partners
    assert generated_e3_person == expected_e3_bob_person
    assert generated_e3_person.to_dict() == expected_e3_bob_person.to_dict()
    assert generated_e7_person.partners == expected_e7_bob_person.partners
    assert generated_e7_person.to_dict() == expected_e7_bob_person.to_dict()


def test_etl_spark_lesson_json_to_spark_inherited_personunits_SetsFiles_expressed_lesson(
    temp3_fs,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    xia_inx = "Xia"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_lasso = lassounit_shop(exx.a23)
    mstr_dir = str(temp3_fs)
    a23_bob_e3_lesson = lessonunit_shop(bob_inx, xia_inx, exx.a23, spark_num=spark3)
    a23_bob_e7_lesson = lessonunit_shop(bob_inx, xia_inx, exx.a23, spark_num=spark7)
    prnptnr_dimen = kw.person_partnerunit
    bob_jkeys = {kw.partner_name: bob_inx}
    bob_jvalues = {kw.partner_cred_lumen: credit77}
    yao_jkeys = {kw.partner_name: yao_inx}
    yao_jvalues = {kw.partner_cred_lumen: credit44}
    a23_bob_e3_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {kw.partner_name: sue_inx}
    sue_jvalues = {kw.partner_cred_lumen: credit88}
    a23_bob_e7_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_lesson.add_p_personatom(prnptnr_dimen, kw.INSERT, sue_jkeys, sue_jvalues)
    a23_bob_e3_all_lesson_path = create_spark_all_lesson_path(
        mstr_dir, a23_lasso, bob_inx, spark3
    )
    a23_bob_e7_all_lesson_path = create_spark_all_lesson_path(
        mstr_dir, a23_lasso, bob_inx, spark7
    )
    save_json(
        a23_bob_e3_all_lesson_path, None, a23_bob_e3_lesson.get_serializable_step_dict()
    )
    save_json(
        a23_bob_e7_all_lesson_path, None, a23_bob_e7_lesson.get_serializable_step_dict()
    )
    e3_expressed_lesson_path = create_spark_expressed_lesson_path(
        mstr_dir, a23_lasso, bob_inx, spark3
    )
    e7_expressed_lesson_path = create_spark_expressed_lesson_path(
        mstr_dir, a23_lasso, bob_inx, spark7
    )
    assert os_path_exists(a23_bob_e3_all_lesson_path)
    assert os_path_exists(a23_bob_e7_all_lesson_path)
    assert os_path_exists(e3_expressed_lesson_path) is False
    assert os_path_exists(e7_expressed_lesson_path) is False

    # WHEN
    etl_spark_lesson_json_to_spark_inherited_personunits(mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_lesson_path)
    assert os_path_exists(e7_expressed_lesson_path)
    gen_e3_express_lesson = get_lessonunit_from_dict(
        open_json(e3_expressed_lesson_path)
    )
    gen_e7_express_lesson = get_lessonunit_from_dict(
        open_json(e7_expressed_lesson_path)
    )
    expected_e3_bob_lesson = lessonunit_shop(
        bob_inx, xia_inx, exx.a23, spark_num=spark3
    )
    expected_e7_bob_lesson = lessonunit_shop(
        bob_inx, xia_inx, exx.a23, spark_num=spark7
    )
    expected_e3_bob_lesson.add_p_personatom(
        prnptnr_dimen, kw.INSERT, bob_jkeys, bob_jvalues
    )
    expected_e3_bob_lesson.add_p_personatom(
        prnptnr_dimen, kw.INSERT, yao_jkeys, yao_jvalues
    )
    expected_e7_bob_lesson.add_p_personatom(
        prnptnr_dimen, kw.INSERT, sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_lesson == a23_bob_e3_lesson
    assert expected_e7_bob_lesson.persondelta != a23_bob_e7_lesson.persondelta
    assert expected_e7_bob_lesson != a23_bob_e7_lesson
    # expected_e3_bob_lesson.add_p_personatom()
    # expected_e3_bob_lesson.add_p_personatom()
    # expected_e7_bob_lesson.add_p_personatom()
    # expected_e7_bob_lesson.add_p_personatom()
    # expected_e7_bob_lesson.add_p_personatom()
    assert gen_e3_express_lesson == expected_e3_bob_lesson
    gen_e7_express_delta = gen_e7_express_lesson.persondelta
    expected_e7_delta = expected_e7_bob_lesson.persondelta
    assert gen_e7_express_delta.personatoms == expected_e7_delta.personatoms
    assert gen_e7_express_lesson.persondelta == expected_e7_bob_lesson.persondelta
    assert gen_e7_express_lesson == expected_e7_bob_lesson
