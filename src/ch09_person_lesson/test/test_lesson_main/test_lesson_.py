from pytest import raises as pytest_raises
from src.ch00_py.dict_toolbox import get_json_from_dict
from src.ch02_contact.contact import contactunit_shop
from src.ch07_person_logic.person_main import get_default_rope, personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson._ref.ch09_semantic_types import (
    FaceName,
    default_knot_if_None,
)
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.lesson_main import (
    LessonUnit,
    get_init_lesson_id_if_None,
    get_lessonunit_from_dict,
    init_lesson_id,
    lessonunit_shop,
)
from src.ch09_person_lesson.test._util.ch09_examples import (
    get_atom_example_planunit_sports,
    get_persondelta_sue_example,
)
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cuisine") == "cuisine"


def test_init_lesson_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_lesson_id() == 0


def test_get_init_lesson_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_lesson_id_if_None() == init_lesson_id()
    assert get_init_lesson_id_if_None(None) == init_lesson_id()
    assert get_init_lesson_id_if_None(1) == 1


def test_LessonUnit_Exists():
    # ESTABLISH / WHEN
    x_lessonunit = LessonUnit()

    # THEN
    assert not x_lessonunit.spark_face
    assert not x_lessonunit.moment_rope
    assert not x_lessonunit.person_name
    assert not x_lessonunit.lesson_id
    assert not x_lessonunit.persondelta
    assert not x_lessonunit.delta_start
    assert not x_lessonunit.lessons_dir
    assert not x_lessonunit.atoms_dir
    assert not x_lessonunit.spark_num
    assert x_lessonunit.__dict__.keys() == {
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        "lesson_id",
        "persondelta",
        "delta_start",
        "lessons_dir",
        "atoms_dir",
        kw.spark_num,
    }


def test_lessonunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH

    # WHEN
    bob_lessonunit = lessonunit_shop(person_name=exx.bob)

    # THEN
    assert not bob_lessonunit.spark_face
    assert bob_lessonunit.moment_rope == get_default_rope()
    assert bob_lessonunit.person_name == exx.bob
    assert bob_lessonunit.lesson_id == 0
    assert bob_lessonunit.persondelta == persondelta_shop()
    assert bob_lessonunit.delta_start == 0
    assert not bob_lessonunit.lessons_dir
    assert not bob_lessonunit.atoms_dir
    assert not bob_lessonunit.spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_lesson_id = 13
    bob_persondelta = get_persondelta_sue_example()
    bob_delta_start = 6
    bob_lessons_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    amy45_str = "amy45"
    amy45_e5_spark_num = 5

    # WHEN
    bob_lessonunit = lessonunit_shop(
        spark_face=exx.sue,
        person_name=exx.bob,
        moment_rope=amy45_str,
        lesson_id=bob_lesson_id,
        persondelta=bob_persondelta,
        delta_start=bob_delta_start,
        lessons_dir=bob_lessons_dir,
        atoms_dir=bob_atoms_dir,
        spark_num=amy45_e5_spark_num,
    )

    # THEN
    assert bob_lessonunit.spark_face == exx.sue
    assert bob_lessonunit.person_name == exx.bob
    assert bob_lessonunit.moment_rope == amy45_str
    assert bob_lessonunit.lesson_id == bob_lesson_id
    assert bob_lessonunit.persondelta == bob_persondelta
    assert bob_lessonunit.delta_start == bob_delta_start
    assert bob_lessonunit.lessons_dir == bob_lessons_dir
    assert bob_lessonunit.atoms_dir == bob_atoms_dir
    assert bob_lessonunit.spark_num == amy45_e5_spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH

    # WHEN
    bob_lessonunit = lessonunit_shop(person_name=exx.bob, spark_face=exx.yao)

    # THEN
    assert bob_lessonunit.person_name == exx.bob
    assert bob_lessonunit.spark_face == exx.yao


def test_LessonUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(person_name=exx.bob)
    assert bob_lessonunit.spark_face is None
    assert bob_lessonunit.spark_face != exx.sue

    # WHEN
    bob_lessonunit.set_face(exx.sue)

    # THEN
    assert bob_lessonunit.spark_face == exx.sue


def test_LessonUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(person_name=exx.bob)
    bob_lessonunit.set_face(exx.yao)
    assert bob_lessonunit.spark_face == exx.yao

    # WHEN
    bob_lessonunit.del_face()

    # THEN
    assert bob_lessonunit.spark_face != exx.yao
    assert bob_lessonunit.spark_face is None


def test_LessonUnit_set_persondelta_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(person_name=exx.bob)
    assert bob_lessonunit.persondelta == persondelta_shop()

    # WHEN
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(get_atom_example_planunit_sports())
    bob_lessonunit.set_persondelta(x_persondelta)

    # THEN
    assert bob_lessonunit.persondelta == x_persondelta


def test_LessonUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(exx.bob)
    assert bob_lessonunit.delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_lessonunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_lessonunit.delta_start == x_delta_start


def test_LessonUnit_personatom_exists_ReturnsObj():
    # ESTABLISH
    x_persondelta = persondelta_shop()
    bob_lessonunit = lessonunit_shop(person_name=exx.bob)
    bob_lessonunit.set_persondelta(x_persondelta)

    # WHEN
    sports_personatom = get_atom_example_planunit_sports()

    # THEN
    assert bob_lessonunit.personatom_exists(sports_personatom) is False

    # WHEN
    x_persondelta.set_personatom(sports_personatom)
    bob_lessonunit.set_persondelta(x_persondelta)

    # THEN
    assert bob_lessonunit.personatom_exists(sports_personatom)


def test_LessonUnit_del_persondelta_SetsAttribute():
    # ESTABLISH
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(get_atom_example_planunit_sports())
    bob_lessonunit = lessonunit_shop(person_name=exx.bob, persondelta=x_persondelta)
    assert bob_lessonunit.persondelta != persondelta_shop()
    assert bob_lessonunit.persondelta == x_persondelta

    # WHEN
    bob_lessonunit.del_persondelta()

    # THEN
    assert bob_lessonunit.persondelta == persondelta_shop()


def test_LessonUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_lessonunit = lessonunit_shop(
        moment_rope=amy45_str, person_name=exx.bob, spark_num=amy45_e5_int
    )
    bob_lessonunit.set_face(exx.sue)

    # WHEN
    x_dict = bob_lessonunit.get_step_dict()

    # THEN
    assert x_dict.get(kw.moment_rope) is not None
    assert x_dict.get(kw.moment_rope) == amy45_str
    assert x_dict.get(kw.person_name) is not None
    assert x_dict.get(kw.person_name) == exx.bob
    assert x_dict.get(kw.spark_face) is not None
    assert x_dict.get(kw.spark_face) == exx.sue
    assert x_dict.get(kw.spark_num) is not None
    assert x_dict.get(kw.spark_num) == amy45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == persondelta_shop().get_ordered_personatoms()
    assert x_dict.get(delta_str) == {}


def test_LessonUnit_get_step_dict_ReturnsObj_WithPersonDeltaPopulated():
    # ESTABLISH
    sue_persondelta = get_persondelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, persondelta=sue_persondelta)

    # WHEN
    x_dict = bob_lessonunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_persondelta.get_ordered_personatoms()
    sue_personatoms_dict = x_dict.get(delta_str)
    print(f"{len(sue_persondelta.get_sorted_personatoms())=}")
    print(f"{sue_personatoms_dict.keys()=}")
    # print(f"{sue_personatoms_dict.get(0)=}")
    assert sue_personatoms_dict.get(2) is None
    assert sue_personatoms_dict.get(0) is not None
    assert sue_personatoms_dict.get(1) is not None


def test_LessonUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    sue_persondelta = get_persondelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(
        exx.bob, persondelta=sue_persondelta, delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_lessonunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_persondelta.get_ordered_personatoms(
        x_delta_start
    )
    sue_personatoms_dict = step_dict.get(delta_str)
    print(f"{len(sue_persondelta.get_sorted_personatoms())=}")
    print(f"{sue_personatoms_dict.keys()=}")
    # print(f"{sue_personatoms_dict.get(0)=}")
    assert sue_personatoms_dict.get(x_delta_start + 2) is None
    assert sue_personatoms_dict.get(x_delta_start + 0) is not None
    assert sue_personatoms_dict.get(x_delta_start + 1) is not None


def test_LessonUnit_get_serializable_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_lessonunit = lessonunit_shop(
        moment_rope=amy45_str, person_name=exx.bob, spark_num=amy45_e5_int
    )
    bob_lessonunit.set_face(exx.sue)

    # WHEN
    total_dict = bob_lessonunit.get_serializable_step_dict()

    # THEN
    assert total_dict.get(kw.moment_rope) is not None
    assert total_dict.get(kw.moment_rope) == amy45_str
    assert total_dict.get(kw.person_name) is not None
    assert total_dict.get(kw.person_name) == exx.bob
    assert total_dict.get(kw.spark_face) is not None
    assert total_dict.get(kw.spark_face) == exx.sue
    assert total_dict.get(kw.spark_num) is not None
    assert total_dict.get(kw.spark_num) == amy45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_LessonUnit_get_serializable_step_dict_ReturnsObj_Scenario0_WithPersonDeltaPopulated():
    # ESTABLISH
    sue_persondelta = get_persondelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, persondelta=sue_persondelta)

    # WHEN
    total_dict = bob_lessonunit.get_serializable_step_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_persondelta.get_ordered_dict()


def test_LessonUnit_get_serializable_step_dict_ReturnsObj_Scenario1_WithPersonDeltaPopulated():
    # ESTABLISH
    sue_persondelta = get_persondelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, persondelta=sue_persondelta)

    # WHEN
    generated_dict = bob_lessonunit.get_serializable_step_dict()

    # THEN
    assert generated_dict
    print("generated_json")
    print(generated_dict)
    expected_json = """{
  "delta": {
    "0": {
      "crud": "DELETE", 
      "dimen": "person_contactunit", 
      "jkeys": {"contact_name": "Sue"}, 
      "jvalues": {}
    }, 
    "1": {
      "crud": "UPDATE", 
      "dimen": "personunit", 
      "jkeys": {}, 
      "jvalues": {"credor_respect": 77}
    }
  }, 
  "moment_rope": ";YY;", 
  "person_name": "Bob", 
  "spark_face": null, 
  "spark_num": null
}"""
    assert get_json_from_dict(generated_dict) == expected_json


def test_get_lessonunit_from_dict_ReturnsObj_WithPersonDeltaPopulated():
    # ESTABLISH
    sue_persondelta = get_persondelta_sue_example()
    bob_lessonunit = lessonunit_shop(
        exx.bob, persondelta=sue_persondelta, spark_num=778
    )

    # WHEN
    generated_bob_lessonunit = get_lessonunit_from_dict(
        bob_lessonunit.get_serializable_step_dict()
    )

    # THEN
    assert generated_bob_lessonunit
    assert generated_bob_lessonunit.spark_face == bob_lessonunit.spark_face
    assert generated_bob_lessonunit.spark_num == bob_lessonunit.spark_num
    assert generated_bob_lessonunit.moment_rope == bob_lessonunit.moment_rope
    assert generated_bob_lessonunit.persondelta == bob_lessonunit.persondelta
    assert generated_bob_lessonunit == bob_lessonunit


def test_LessonUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    sue_persondelta = get_persondelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_lessonunit.set_persondelta(sue_persondelta)
    bob_lessonunit.set_delta_start(x_delta_start)
    bob_lessonunit.set_face(exx.yao)
    x_dict = bob_lessonunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_lessonunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_LessonUnit_get_deltametric_dict_ReturnsObj():
    # ESTABLISH
    spark5_int = 5550
    sue_persondelta = get_persondelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_lessonunit.set_persondelta(sue_persondelta)
    bob_lessonunit.set_delta_start(x_delta_start)
    bob_lessonunit.set_face(exx.yao)
    bob_lessonunit.spark_num = spark5_int

    # WHEN
    x_dict = bob_lessonunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(kw.person_name) is not None
    assert x_dict.get(kw.person_name) == exx.bob
    assert x_dict.get(kw.spark_face) is not None
    assert x_dict.get(kw.spark_face) == exx.yao
    assert x_dict.get(kw.spark_num) is not None
    assert x_dict.get(kw.spark_num) == spark5_int

    delta_atom_numbers_str = "delta_atom_numbers"
    assert x_dict.get(delta_atom_numbers_str) is not None
    assert x_dict.get(delta_atom_numbers_str) == [7, 8]

    delta_min_str = "delta_min"
    assert x_dict.get(delta_min_str) is None
    delta_max_str = "delta_max"
    assert x_dict.get(delta_max_str) is None


def test_LessonUnit_add_p_personatom_Sets_PersonUnit_contactunits():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    bob_contactunit = contactunit_shop(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen
    print(f"{bob_contactunit.to_dict()=}")
    bob_required_dict = {
        kw.contact_name: bob_contactunit.to_dict().get(kw.contact_name)
    }
    bob_optional_dict = {cw_str: bob_contactunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_contactunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_lessonunit.persondelta.personatoms == {}

    # WHEN
    bob_lessonunit.add_p_personatom(
        dimen=kw.person_contactunit,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_lessonunit.persondelta.personatoms) == 1
    assert (
        bob_lessonunit.persondelta.personatoms.get(kw.INSERT)
        .get(kw.person_contactunit)
        .get(exx.bob)
        is not None
    )


def test_LessonUnit_get_edited_person_ReturnsObj_PersonUnit_insert_contact():
    # ESTABLISH
    sue_lessonunit = lessonunit_shop(exx.sue)

    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_contactunit(exx.yao)
    assert before_sue_personunit.contact_exists(exx.yao)
    assert before_sue_personunit.contact_exists(exx.zia) is False
    dimen = kw.person_contactunit
    x_personatom = personatom_shop(dimen, kw.INSERT)
    x_personatom.set_jkey(kw.contact_name, exx.zia)
    x_contact_cred_lumen = 55
    x_contact_debt_lumen = 66
    x_personatom.set_jvalue("contact_cred_lumen", x_contact_cred_lumen)
    x_personatom.set_jvalue("contact_debt_lumen", x_contact_debt_lumen)
    sue_lessonunit.persondelta.set_personatom(x_personatom)
    print(f"{sue_lessonunit.persondelta.personatoms.keys()=}")

    # WHEN
    after_sue_personunit = sue_lessonunit.get_lesson_edited_person(
        before_sue_personunit
    )

    # THEN
    yao_contactunit = after_sue_personunit.get_contact(exx.yao)
    zia_contactunit = after_sue_personunit.get_contact(exx.zia)
    assert yao_contactunit is not None
    assert zia_contactunit is not None
    assert zia_contactunit.contact_cred_lumen == x_contact_cred_lumen
    assert zia_contactunit.contact_debt_lumen == x_contact_debt_lumen


def test_LessonUnit_get_edited_person_RaisesErrorWhenlessonAttrsAndPersonAttrsAreNotTheSame():
    # ESTABLISH
    xia_str = "Xia"
    bob_lessonunit = lessonunit_shop(exx.yao, xia_str, moment_rope=exx.a23)
    before_sue_personunit = personunit_shop(exx.sue, planroot_rope=exx.a23)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_lessonunit.get_lesson_edited_person(before_sue_personunit)
    assertion_failure_str = (
        f"lesson person conflict {exx.a23} != {exx.a23} or Yao != Sue"
    )
    assert str(excinfo.value) == assertion_failure_str


def test_LessonUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_contact_cred_lumen = 55
    bob_contact_debt_lumen = 66
    bob_contactunit = contactunit_shop(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    cw_str = kw.contact_cred_lumen
    dw_str = kw.contact_debt_lumen
    print(f"{bob_contactunit.to_dict()=}")
    bob_required_dict = {
        kw.contact_name: bob_contactunit.to_dict().get(kw.contact_name)
    }
    bob_optional_dict = {cw_str: bob_contactunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_contactunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_lessonunit.persondelta.personatoms == {}
    assert bob_lessonunit.is_empty()

    # WHEN
    bob_lessonunit.add_p_personatom(
        dimen=kw.person_contactunit,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_lessonunit.persondelta.personatoms) == 1
    assert bob_lessonunit.is_empty() is False

    # WHEN
    bob_lessonunit.persondelta.personatoms = {}

    # THEN
    assert bob_lessonunit.is_empty()

    # Test for UPDATE_str operation
    bob_lessonunit_update = lessonunit_shop(exx.bob)
    bob_lessonunit_update.add_p_personatom(
        dimen=kw.person_contactunit,
        crud_str=kw.UPDATE,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_lessonunit_update.persondelta.personatoms) == 1
    assert bob_lessonunit_update.is_empty() is False

    # Test for DELETE_str operation
    bob_lessonunit_delete = lessonunit_shop(exx.bob)
    bob_lessonunit_delete.add_p_personatom(
        dimen=kw.person_contactunit,
        crud_str=kw.DELETE,
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_lessonunit_delete.persondelta.personatoms) == 1
    assert bob_lessonunit_delete.is_empty() is False
