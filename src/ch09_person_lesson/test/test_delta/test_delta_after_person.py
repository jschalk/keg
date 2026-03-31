from src.ch02_partner.group import awardunit_shop
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.test._util.ch09_examples import get_persondelta_example1
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PersonDelta_get_edited_person_ReturnsObj_SimplestScenario():
    # ESTABLISH
    ex1_persondelta = persondelta_shop()

    # WHEN
    sue_mana_grain = 55
    before_sue_personunit = personunit_shop(exx.sue, mana_grain=sue_mana_grain)
    after_sue_personunit = ex1_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    assert after_sue_personunit.mana_grain == sue_mana_grain
    assert after_sue_personunit == before_sue_personunit


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnitSimpleAttrs():
    # ESTABLISH
    sue_persondelta = persondelta_shop()

    sue_mana_grain = 44
    before_sue_personunit = personunit_shop(exx.sue, mana_grain=sue_mana_grain)

    dimen = kw.personunit
    x_personatom = personatom_shop(dimen, kw.UPDATE)
    new2_value = 66
    new2_arg = kw.max_tree_traverse
    x_personatom.set_jvalue(new2_arg, new2_value)
    new3_value = 77
    new3_arg = kw.credor_respect
    x_personatom.set_jvalue(new3_arg, new3_value)
    new4_value = 88
    new4_arg = kw.debtor_respect
    x_personatom.set_jvalue(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = kw.fund_pool
    x_personatom.set_jvalue(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = kw.fund_grain
    x_personatom.set_jvalue(new8_arg, new8_value)
    sue_persondelta.set_personatom(x_personatom)
    new6_value = 0.5
    new6_arg = kw.respect_grain
    x_personatom.set_jvalue(new6_arg, new6_value)
    sue_persondelta.set_personatom(x_personatom)
    new7_value = 0.025
    new7_arg = kw.mana_grain
    x_personatom.set_jvalue(new7_arg, new7_value)
    sue_persondelta.set_personatom(x_personatom)

    # WHEN
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    print(f"{sue_persondelta.personatoms.keys()=}")
    assert after_sue_personunit.max_tree_traverse == new2_value
    assert after_sue_personunit.credor_respect == new3_value
    assert after_sue_personunit.debtor_respect == new4_value
    assert after_sue_personunit.fund_pool == new9_value
    assert after_sue_personunit.fund_pool != before_sue_personunit.fund_pool
    assert after_sue_personunit.fund_grain == new8_value
    assert after_sue_personunit.fund_grain != before_sue_personunit.fund_grain
    assert after_sue_personunit.respect_grain == new6_value
    assert after_sue_personunit.respect_grain != before_sue_personunit.respect_grain
    assert after_sue_personunit.mana_grain == new7_value
    assert after_sue_personunit.mana_grain != before_sue_personunit.mana_grain


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_partner():
    # ESTABLISH
    sue_persondelta = persondelta_shop()

    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)

    dimen = kw.person_partnerunit
    x_personatom = personatom_shop(dimen, kw.DELETE)
    x_personatom.set_jkey(kw.partner_name, exx.zia)
    sue_persondelta.set_personatom(x_personatom)

    # WHEN
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    print(f"{sue_persondelta.personatoms=}")
    assert after_sue_personunit != before_sue_personunit
    assert after_sue_personunit.partner_exists(exx.yao)
    assert after_sue_personunit.partner_exists(exx.zia) is False


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_partner():
    # ESTABLISH
    sue_persondelta = persondelta_shop()

    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    assert before_sue_personunit.partner_exists(exx.yao)
    assert before_sue_personunit.partner_exists(exx.zia) is False

    # WHEN
    dimen = kw.person_partnerunit
    x_personatom = personatom_shop(dimen, kw.INSERT)
    x_personatom.set_jkey(kw.partner_name, exx.zia)
    x_partner_cred_lumen = 55
    x_partner_debt_lumen = 66
    x_personatom.set_jvalue("partner_cred_lumen", x_partner_cred_lumen)
    x_personatom.set_jvalue("partner_debt_lumen", x_partner_debt_lumen)
    sue_persondelta.set_personatom(x_personatom)
    print(f"{sue_persondelta.personatoms.keys()=}")
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    yao_partnerunit = after_sue_personunit.get_partner(exx.yao)
    zia_partnerunit = after_sue_personunit.get_partner(exx.zia)
    assert yao_partnerunit is not None
    assert zia_partnerunit is not None
    assert zia_partnerunit.partner_cred_lumen == x_partner_cred_lumen
    assert zia_partnerunit.partner_debt_lumen == x_partner_debt_lumen


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_partner():
    # ESTABLISH
    sue_persondelta = persondelta_shop()

    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    assert before_sue_personunit.get_partner(exx.yao).partner_cred_lumen == 1

    # WHEN
    dimen = kw.person_partnerunit
    x_personatom = personatom_shop(dimen, kw.UPDATE)
    x_personatom.set_jkey(kw.partner_name, exx.yao)
    yao_partner_cred_lumen = 55
    x_personatom.set_jvalue("partner_cred_lumen", yao_partner_cred_lumen)
    sue_persondelta.set_personatom(x_personatom)
    print(f"{sue_persondelta.personatoms.keys()=}")
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    yao_partner = after_sue_personunit.get_partner(exx.yao)
    assert yao_partner.partner_cred_lumen == yao_partner_cred_lumen


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)
    before_sue_personunit.add_partnerunit(exx.bob)
    yao_partnerunit = before_sue_personunit.get_partner(exx.yao)
    zia_partnerunit = before_sue_personunit.get_partner(exx.zia)
    bob_partnerunit = before_sue_personunit.get_partner(exx.bob)
    yao_partnerunit.add_membership(exx.run)
    zia_partnerunit.add_membership(exx.run)
    fly_str = ";flyers"
    yao_partnerunit.add_membership(fly_str)
    zia_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_personunit.get_partnerunit_group_titles_dict()
    assert len(before_group_titles_dict.get(exx.run)) == 2
    assert len(before_group_titles_dict.get(fly_str)) == 3

    # WHEN
    yao_personatom = personatom_shop(kw.person_partner_membership, kw.DELETE)
    yao_personatom.set_jkey(kw.group_title, exx.run)
    yao_personatom.set_jkey(kw.partner_name, exx.yao)
    # print(f"{yao_personatom=}")
    zia_personatom = personatom_shop(kw.person_partner_membership, kw.DELETE)
    zia_personatom.set_jkey(kw.group_title, fly_str)
    zia_personatom.set_jkey(kw.partner_name, exx.zia)
    # print(f"{zia_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(yao_personatom)
    sue_persondelta.set_personatom(zia_personatom)
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    after_group_titles_dict = after_sue_personunit.get_partnerunit_group_titles_dict()
    assert len(after_group_titles_dict.get(exx.run)) == 1
    assert len(after_group_titles_dict.get(fly_str)) == 2


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_membership():
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)
    before_sue_personunit.add_partnerunit(exx.bob)
    zia_partnerunit = before_sue_personunit.get_partner(exx.zia)
    zia_partnerunit.add_membership(exx.run)
    before_group_titles = before_sue_personunit.get_partnerunit_group_titles_dict()
    assert len(before_group_titles.get(exx.run)) == 1

    # WHEN
    yao_personatom = personatom_shop(kw.person_partner_membership, kw.INSERT)
    yao_personatom.set_jkey(kw.group_title, exx.run)
    yao_personatom.set_jkey(kw.partner_name, exx.yao)
    yao_run_group_cred_lumen = 17
    yao_personatom.set_jvalue(kw.group_cred_lumen, yao_run_group_cred_lumen)
    print(f"{yao_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(yao_personatom)
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    after_group_titles = after_sue_personunit.get_partnerunit_group_titles_dict()
    assert len(after_group_titles.get(exx.run)) == 2
    after_yao_partnerunit = after_sue_personunit.get_partner(exx.yao)
    after_yao_run_membership = after_yao_partnerunit.get_membership(exx.run)
    assert after_yao_run_membership is not None
    assert after_yao_run_membership.group_cred_lumen == yao_run_group_cred_lumen


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_yao_partnerunit = before_sue_personunit.get_partner(exx.yao)
    old_yao_run_group_cred_lumen = 3
    before_yao_partnerunit.add_membership(exx.run, old_yao_run_group_cred_lumen)
    yao_run_membership = before_yao_partnerunit.get_membership(exx.run)
    assert yao_run_membership.group_cred_lumen == old_yao_run_group_cred_lumen
    assert yao_run_membership.group_debt_lumen == 1

    # WHEN
    yao_personatom = personatom_shop(kw.person_partner_membership, kw.UPDATE)
    yao_personatom.set_jkey(kw.group_title, exx.run)
    yao_personatom.set_jkey(kw.partner_name, exx.yao)
    new_yao_run_group_cred_lumen = 7
    new_yao_run_group_debt_lumen = 11
    yao_personatom.set_jvalue(kw.group_cred_lumen, new_yao_run_group_cred_lumen)
    yao_personatom.set_jvalue(kw.group_debt_lumen, new_yao_run_group_debt_lumen)
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(yao_personatom)
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    after_yao_partnerunit = after_sue_personunit.get_partner(exx.yao)
    after_yao_run_membership = after_yao_partnerunit.get_membership(exx.run)
    assert after_yao_run_membership.group_cred_lumen == new_yao_run_group_cred_lumen
    assert after_yao_run_membership.group_debt_lumen == new_yao_run_group_debt_lumen


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_planunit():
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_personunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_personunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_personunit.make_rope(sports_rope, disc_str)
    before_sue_personunit.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_sue_personunit.set_plan_obj(planunit_shop(disc_str), sports_rope)
    delete_disc_personatom = personatom_shop(kw.person_planunit, kw.DELETE)
    delete_disc_personatom.set_jkey(kw.plan_rope, disc_rope)
    print(f"{disc_rope=}")
    delete_disc_personatom.set_jkey(kw.plan_rope, disc_rope)
    print(f"{delete_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(delete_disc_personatom)
    assert before_sue_personunit.plan_exists(ball_rope)
    assert before_sue_personunit.plan_exists(disc_rope)

    # WHEN
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    assert after_sue_personunit.plan_exists(ball_rope)
    assert after_sue_personunit.plan_exists(disc_rope) is False


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_planunit():
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_personunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_personunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_personunit.make_rope(sports_rope, disc_str)
    before_sue_personunit.set_plan_obj(planunit_shop(ball_str), sports_rope)
    assert before_sue_personunit.plan_exists(ball_rope)
    assert before_sue_personunit.plan_exists(disc_rope) is False

    # WHEN
    # x_addin = 140
    x_gogo_want = 1000
    x_stop_want = 1700
    # x_denom = 17
    # x_numor = 10
    x_pledge = True
    insert_disc_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    insert_disc_personatom.set_jkey(kw.plan_rope, disc_rope)
    # insert_disc_personatom.set_jvalue(kw.addin, x_addin)
    # insert_disc_personatom.set_jvalue(kw.begin, x_begin)
    # insert_disc_personatom.set_jvalue(kw.close, x_close)
    # insert_disc_personatom.set_jvalue(kw.denom, x_denom)
    # insert_disc_personatom.set_jvalue(kw.numor, x_numor)
    insert_disc_personatom.set_jvalue(kw.pledge, x_pledge)
    insert_disc_personatom.set_jvalue(kw.gogo_want, x_gogo_want)
    insert_disc_personatom.set_jvalue(kw.stop_want, x_stop_want)

    print(f"{insert_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(insert_disc_personatom)
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    assert after_sue_personunit.plan_exists(ball_rope)
    assert after_sue_personunit.plan_exists(disc_rope)
    disc_plan = after_sue_personunit.get_plan_obj(disc_rope)
    assert disc_plan.gogo_want == x_gogo_want
    assert disc_plan.stop_want == x_stop_want


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_planunit_SimpleAttributes():
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_personunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_personunit.make_rope(sports_rope, ball_str)
    before_sue_personunit.set_plan_obj(planunit_shop(ball_str), sports_rope)

    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_gogo_want = 1222
    x_stop_want = 1333
    x_pledge = True
    insert_disc_personatom = personatom_shop(kw.person_planunit, kw.UPDATE)
    insert_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    # insert_disc_personatom.set_jvalue(kw.addin, x_addin)
    insert_disc_personatom.set_jvalue(kw.begin, x_begin)
    insert_disc_personatom.set_jvalue(kw.close, x_close)
    # insert_disc_personatom.set_jvalue(kw.denom, x_denom)
    # insert_disc_personatom.set_jvalue(kw.numor, x_numor)
    insert_disc_personatom.set_jvalue(kw.pledge, x_pledge)
    insert_disc_personatom.set_jvalue(kw.gogo_want, x_gogo_want)
    insert_disc_personatom.set_jvalue(kw.stop_want, x_stop_want)

    print(f"{insert_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(insert_disc_personatom)
    assert before_sue_personunit.get_plan_obj(ball_rope).begin is None
    assert before_sue_personunit.get_plan_obj(ball_rope).close is None
    assert before_sue_personunit.get_plan_obj(ball_rope).pledge is False
    assert before_sue_personunit.get_plan_obj(ball_rope).gogo_want is None
    assert before_sue_personunit.get_plan_obj(ball_rope).stop_want is None

    # WHEN
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    assert after_sue_personunit.get_plan_obj(ball_rope).begin == x_begin
    assert after_sue_personunit.get_plan_obj(ball_rope).close == x_close
    assert after_sue_personunit.get_plan_obj(ball_rope).gogo_want == x_gogo_want
    assert after_sue_personunit.get_plan_obj(ball_rope).stop_want == x_stop_want
    assert after_sue_personunit.get_plan_obj(ball_rope).pledge


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_plan_awardunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)
    before_sue_personunit.add_partnerunit(exx.bob)
    yao_partnerunit = before_sue_personunit.get_partner(exx.yao)
    zia_partnerunit = before_sue_personunit.get_partner(exx.zia)
    bob_partnerunit = before_sue_personunit.get_partner(exx.bob)
    yao_partnerunit.add_membership(exx.run)
    zia_partnerunit.add_membership(exx.run)
    fly_str = ";flyers"
    yao_partnerunit.add_membership(fly_str)
    zia_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)

    sports_str = "sports"
    sports_rope = before_sue_personunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_personunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_personunit.make_rope(sports_rope, disc_str)
    before_sue_personunit.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_sue_personunit.set_plan_obj(planunit_shop(disc_str), sports_rope)
    before_sue_personunit.edit_plan_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    before_sue_personunit.edit_plan_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    before_sue_personunit.edit_plan_attr(disc_rope, awardunit=awardunit_shop(exx.run))
    before_sue_personunit.edit_plan_attr(disc_rope, awardunit=awardunit_shop(fly_str))
    assert len(before_sue_personunit.get_plan_obj(ball_rope).awardunits) == 2
    assert len(before_sue_personunit.get_plan_obj(disc_rope).awardunits) == 2

    # WHEN
    delete_disc_personatom = personatom_shop(kw.person_plan_awardunit, kw.DELETE)
    delete_disc_personatom.set_jkey(kw.plan_rope, disc_rope)
    delete_disc_personatom.set_jkey(kw.awardee_title, fly_str)
    print(f"{delete_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(delete_disc_personatom)
    after_sue_personunit = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    assert len(after_sue_personunit.get_plan_obj(ball_rope).awardunits) == 2
    assert len(after_sue_personunit.get_plan_obj(disc_rope).awardunits) == 1


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_plan_awardunit():
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)
    yao_partnerunit = before_sue_personunit.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)

    sports_str = "sports"
    sports_rope = before_sue_personunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_personunit.make_rope(sports_rope, ball_str)
    before_sue_personunit.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_sue_personunit.edit_plan_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    run_awardunit = before_sue_personunit.get_plan_obj(ball_rope).awardunits.get(
        exx.run
    )
    assert run_awardunit.give_force == 1
    assert run_awardunit.take_force == 1

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_personatom = personatom_shop(kw.person_plan_awardunit, kw.UPDATE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.awardee_title, exx.run)
    update_disc_personatom.set_jvalue(kw.give_force, x_give_force)
    update_disc_personatom.set_jvalue(kw.take_force, x_take_force)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    run_awardunit = after_sue_au.get_plan_obj(ball_rope).awardunits.get(exx.run)
    print(f"{run_awardunit.give_force=}")
    assert run_awardunit.give_force == x_give_force
    assert run_awardunit.take_force == x_take_force


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_plan_awardunit():
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)
    yao_partnerunit = before_sue_personunit.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)
    sports_str = "sports"
    sports_rope = before_sue_personunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_personunit.make_rope(sports_rope, ball_str)
    before_sue_personunit.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_plan = before_sue_personunit.get_plan_obj(ball_rope)
    assert before_ball_plan.awardunits.get(exx.run) is None

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_personatom = personatom_shop(kw.person_plan_awardunit, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.awardee_title, exx.run)
    update_disc_personatom.set_jvalue(kw.give_force, x_give_force)
    update_disc_personatom.set_jvalue(kw.take_force, x_take_force)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.awardunits.get(exx.run) is not None


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_plan_factunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits == {}

    # WHEN
    damaged_fact_lower = 55
    damaged_fact_upper = 66
    update_disc_personatom = personatom_shop(kw.person_plan_factunit, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_personatom.set_jvalue(kw.fact_state, damaged_rope)
    update_disc_personatom.set_jvalue(kw.fact_lower, damaged_fact_lower)
    update_disc_personatom.set_jvalue(kw.fact_upper, damaged_fact_upper)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits != {}
    assert after_ball_plan.factunits.get(knee_rope) is not None
    assert after_ball_plan.factunits.get(knee_rope).fact_context == knee_rope
    assert after_ball_plan.factunits.get(knee_rope).fact_state == damaged_rope
    assert after_ball_plan.factunits.get(knee_rope).fact_lower == damaged_fact_lower
    assert after_ball_plan.factunits.get(knee_rope).fact_upper == damaged_fact_upper


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_plan_factunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope,
        factunit=factunit_shop(fact_context=knee_rope, fact_state=damaged_rope),
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits != {}
    assert before_ball_plan.factunits.get(knee_rope) is not None

    # WHEN
    update_disc_personatom = personatom_shop(kw.person_plan_factunit, kw.DELETE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.fact_context, knee_rope)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits == {}


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_plan_factunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_sue_au.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_knee_factunit = factunit_shop(knee_rope, damaged_rope)
    before_sue_au.edit_plan_attr(ball_rope, factunit=before_knee_factunit)
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.factunits != {}
    assert before_ball_plan.factunits.get(knee_rope) is not None
    assert before_ball_plan.factunits.get(knee_rope).fact_state == damaged_rope
    assert before_ball_plan.factunits.get(knee_rope).fact_lower is None
    assert before_ball_plan.factunits.get(knee_rope).fact_upper is None

    # WHEN
    medical_fact_lower = 45
    medical_fact_upper = 77
    update_disc_personatom = personatom_shop(kw.person_plan_factunit, kw.UPDATE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_personatom.set_jvalue(kw.fact_state, medical_rope)
    update_disc_personatom.set_jvalue(kw.fact_lower, medical_fact_lower)
    update_disc_personatom.set_jvalue(kw.fact_upper, medical_fact_upper)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.factunits != {}
    assert after_ball_plan.factunits.get(knee_rope) is not None
    assert after_ball_plan.factunits.get(knee_rope).fact_state == medical_rope
    assert after_ball_plan.factunits.get(knee_rope).fact_lower == medical_fact_lower
    assert after_ball_plan.factunits.get(knee_rope).fact_upper == medical_fact_upper


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_plan_reason_caseunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.reasonunits != {}
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit is not None
    damaged_caseunit = before_knee_reasonunit.get_case(damaged_rope)
    assert damaged_caseunit.reason_state == damaged_rope
    assert damaged_caseunit.reason_lower is None
    assert damaged_caseunit.reason_upper is None
    assert damaged_caseunit.reason_divisor is None

    # WHEN
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    update_disc_personatom = personatom_shop(kw.person_plan_reason_caseunit, kw.UPDATE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.reason_context, knee_rope)
    update_disc_personatom.set_jkey(kw.reason_state, damaged_rope)
    update_disc_personatom.set_jvalue(kw.reason_lower, damaged_reason_lower)
    update_disc_personatom.set_jvalue(kw.reason_upper, damaged_reason_upper)
    update_disc_personatom.set_jvalue(kw.reason_divisor, damaged_reason_divisor)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    after_damaged_caseunit = after_knee_reasonunit.get_case(damaged_rope)
    assert after_damaged_caseunit.reason_state == damaged_rope
    assert after_damaged_caseunit.reason_lower == damaged_reason_lower
    assert after_damaged_caseunit.reason_upper == damaged_reason_upper
    assert after_damaged_caseunit.reason_divisor == damaged_reason_divisor


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_plan_reason_caseunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_sue_au.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_case(damaged_rope) is not None
    assert before_knee_reasonunit.get_case(medical_rope) is None

    # WHEN
    medical_reason_lower = 45
    medical_reason_upper = 77
    medical_reason_divisor = 3
    update_disc_personatom = personatom_shop(kw.person_plan_reason_caseunit, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.reason_context, knee_rope)
    update_disc_personatom.set_jkey(kw.reason_state, medical_rope)
    update_disc_personatom.set_jvalue(kw.reason_lower, medical_reason_lower)
    update_disc_personatom.set_jvalue(kw.reason_upper, medical_reason_upper)
    update_disc_personatom.set_jvalue(kw.reason_divisor, medical_reason_divisor)
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    after_medical_caseunit = after_knee_reasonunit.get_case(medical_rope)
    assert after_medical_caseunit is not None
    assert after_medical_caseunit.reason_state == medical_rope
    assert after_medical_caseunit.reason_lower == medical_reason_lower
    assert after_medical_caseunit.reason_upper == medical_reason_upper
    assert after_medical_caseunit.reason_divisor == medical_reason_divisor


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_plan_reason_caseunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(damaged_str), knee_rope)
    before_sue_au.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_sue_au.edit_plan_attr(
        ball_rope, reason_context=knee_rope, reason_case=medical_rope
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_knee_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_case(damaged_rope) is not None
    assert before_knee_reasonunit.get_case(medical_rope) is not None

    # WHEN
    update_disc_personatom = personatom_shop(kw.person_plan_reason_caseunit, kw.DELETE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.reason_context, knee_rope)
    update_disc_personatom.set_jkey(kw.reason_state, medical_rope)
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit.get_case(damaged_rope) is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_plan_reasonunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.get_reasonunit(knee_rope) is None

    # WHEN
    medical_active_requisite = True
    update_disc_personatom = personatom_shop(kw.person_plan_reasonunit, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey("reason_context", knee_rope)
    update_disc_personatom.set_jvalue(
        kw.active_requisite,
        medical_active_requisite,
    )
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None
    assert after_knee_reasonunit.active_requisite == medical_active_requisite


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_update_plan_reasonunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_medical_active_requisite = False
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.set_plan_obj(planunit_shop(medical_str), knee_rope)
    before_sue_au.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_requisite_active=before_medical_active_requisite,
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    before_ball_reasonunit = before_ball_plan.get_reasonunit(knee_rope)
    assert before_ball_reasonunit is not None
    assert before_ball_reasonunit.active_requisite == before_medical_active_requisite

    # WHEN
    after_medical_active_requisite = True
    update_disc_personatom = personatom_shop(kw.person_plan_reasonunit, kw.UPDATE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey("reason_context", knee_rope)
    update_disc_personatom.set_jvalue(
        kw.active_requisite,
        after_medical_active_requisite,
    )
    # print(f"{update_disc_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    after_knee_reasonunit = after_ball_plan.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None
    assert after_knee_reasonunit.active_requisite == after_medical_active_requisite


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_plan_reasonunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_active_requisite = False
    before_sue_au.set_l1_plan(planunit_shop(knee_str))
    before_sue_au.edit_plan_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_requisite_active=medical_active_requisite,
    )
    before_ball_plan = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_plan.get_reasonunit(knee_rope) is not None

    # WHEN
    update_disc_personatom = personatom_shop(kw.person_plan_reasonunit, kw.DELETE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey("reason_context", knee_rope)
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_plan = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_plan.get_reasonunit(knee_rope) is None


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_plan_laborunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_planunit.workforceunit.labors == {}

    # WHEN
    update_disc_personatom = personatom_shop(kw.person_plan_laborunit, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.labor_title, exx.yao)
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.workforceunit.labors != set()
    assert after_ball_planunit.workforceunit.get_laborunit(exx.yao) is not None


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_plan_laborunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    before_ball_planunit.workforceunit.add_labor(exx.yao)
    assert before_ball_planunit.workforceunit.labors != set()
    assert before_ball_planunit.workforceunit.get_laborunit(exx.yao) is not None

    # WHEN
    update_disc_personatom = personatom_shop(kw.person_plan_laborunit, kw.DELETE)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.labor_title, exx.yao)
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(update_disc_personatom)
    print(f"{before_sue_au.get_plan_obj(ball_rope).workforceunit=}")
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.workforceunit.labors == {}


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_insert_plan_healerunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    assert before_ball_planunit.healerunit.healer_names == set()
    assert not before_ball_planunit.healerunit.healer_name_exists(exx.yao)

    # WHEN
    x_personatom = personatom_shop(kw.person_plan_healerunit, kw.INSERT)
    x_personatom.set_jkey(kw.plan_rope, ball_rope)
    x_personatom.set_jkey(kw.healer_name, exx.yao)
    print(f"{x_personatom=}")
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(x_personatom)
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.healerunit.healer_names != set()
    assert after_ball_planunit.healerunit.healer_name_exists(exx.yao)


def test_PersonDelta_get_edited_person_ReturnsObj_PersonUnit_delete_plan_healerunit():
    # ESTABLISH
    before_sue_au = personunit_shop(exx.sue)
    before_sue_au.add_partnerunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_plan_obj(planunit_shop(ball_str), sports_rope)
    before_ball_planunit = before_sue_au.get_plan_obj(ball_rope)
    before_ball_planunit.healerunit.set_healer_name(exx.yao)
    assert before_ball_planunit.healerunit.healer_names != set()
    assert before_ball_planunit.healerunit.healer_name_exists(exx.yao)

    # WHEN
    x_personatom = personatom_shop(kw.person_plan_healerunit, kw.DELETE)
    x_personatom.set_jkey(kw.plan_rope, ball_rope)
    x_personatom.set_jkey(kw.healer_name, exx.yao)
    sue_persondelta = persondelta_shop()
    sue_persondelta.set_personatom(x_personatom)
    print(f"{before_sue_au.get_plan_obj(ball_rope).workforceunit=}")
    after_sue_au = sue_persondelta.get_atom_edited_person(before_sue_au)

    # THEN
    after_ball_planunit = after_sue_au.get_plan_obj(ball_rope)
    assert after_ball_planunit.healerunit.healer_names == set()
    assert not after_ball_planunit.healerunit.healer_name_exists(exx.yao)


def test_PersonDelta_get_persondelta_example1_ContainsPersonAtoms():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_personunit = personunit_shop(exx.sue)
    before_sue_personunit.add_partnerunit(exx.yao)
    before_sue_personunit.add_partnerunit(exx.zia)
    before_sue_personunit.add_partnerunit(exx.bob)
    yao_partnerunit = before_sue_personunit.get_partner(exx.yao)
    zia_partnerunit = before_sue_personunit.get_partner(exx.zia)
    bob_partnerunit = before_sue_personunit.get_partner(exx.bob)
    yao_partnerunit.add_membership(exx.run)
    zia_partnerunit.add_membership(exx.run)
    fly_str = ";flyers"
    yao_partnerunit.add_membership(fly_str)
    bob_partnerunit.add_membership(fly_str)
    assert before_sue_personunit.max_tree_traverse != 66
    assert before_sue_personunit.credor_respect != 77
    assert before_sue_personunit.debtor_respect != 88
    assert before_sue_personunit.partner_exists(exx.yao)
    assert before_sue_personunit.partner_exists(exx.zia)
    assert yao_partnerunit.get_membership(fly_str) is not None
    assert bob_partnerunit.get_membership(fly_str) is not None

    # WHEN
    ex1_persondelta = get_persondelta_example1()
    after_sue_personunit = ex1_persondelta.get_atom_edited_person(before_sue_personunit)

    # THEN
    assert after_sue_personunit.max_tree_traverse == 66
    assert after_sue_personunit.credor_respect == 77
    assert after_sue_personunit.debtor_respect == 88
    assert after_sue_personunit.partner_exists(exx.yao)
    assert after_sue_personunit.partner_exists(exx.zia) is False
