from ch06_plan.plan import planunit_shop
from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.delta import get_dimens_cruds_persondelta, persondelta_shop
from ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PersonDelta_get_dimens_cruds_persondelta_ReturnsObjWithCorrectDimensAndCRUDsBy_contactunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_contactunit(exx.yao)
    after_sue_person = personunit_shop(exx.sue)
    bob_contact_cred_lumen = 33
    bob_contact_debt_lumen = 44
    after_sue_person.add_contactunit(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    after_sue_person.set_l1_plan(planunit_shop("casa"))
    old_persondelta = persondelta_shop()
    old_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    dimen_set = [kw.person_contactunit]
    curd_set = {kw.INSERT}

    # WHEN
    new_persondelta = get_dimens_cruds_persondelta(old_persondelta, dimen_set, curd_set)

    # THEN
    new_persondelta.get_dimen_sorted_personatoms_list()
    assert len(new_persondelta.get_dimen_sorted_personatoms_list()) == 1
    sue_insert_dict = new_persondelta.personatoms.get(kw.INSERT)
    sue_contactunit_dict = sue_insert_dict.get(kw.person_contactunit)
    bob_personatom = sue_contactunit_dict.get(exx.bob)
    assert bob_personatom.get_value(kw.contact_name) == exx.bob
    assert bob_personatom.get_value("contact_cred_lumen") == bob_contact_cred_lumen
    assert bob_personatom.get_value("contact_debt_lumen") == bob_contact_debt_lumen
