from src.ch07_person_logic.person_main import get_personunit_from_dict, personunit_shop
from src.ch13_time.epoch_main import add_epoch_planunit
from src.ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_get_personunit_from_dict_ReturnsObj_TracksEpochUnitAttributes():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue, exx.a23)
    add_epoch_planunit(sue_person)
    sue_person.add_contactunit(exx.bob, 2)
    sue_person.add_contactunit(exx.sue, 1)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sue_person.add_plan(clean_rope, 1, pledge=True)
    sue_person.get_contact(exx.sue).add_membership(exx.run)
    sue_person.conpute()
    yr1_jan1_offset_rope = ";Amy23;time;creg;yr1_jan1_offset;"
    before_yr1_jan1_offset_plan = sue_person.get_plan_obj(yr1_jan1_offset_rope)
    # print(x_person.get_plan_obj(";Amy23;time;creg;yr1_jan1_offset;"))
    print(f"{before_yr1_jan1_offset_plan.addin=}")
    expected_addin = 440640
    assert before_yr1_jan1_offset_plan.addin == expected_addin
    assert before_yr1_jan1_offset_plan.addin == 440640

    # WHEN
    x2_person = get_personunit_from_dict(sue_person.to_dict())

    # THEN
    after_yr1_jan1_offset_plan = x2_person.get_plan_obj(yr1_jan1_offset_rope)
    assert after_yr1_jan1_offset_plan.addin == expected_addin
    assert after_yr1_jan1_offset_plan.addin == 440640
