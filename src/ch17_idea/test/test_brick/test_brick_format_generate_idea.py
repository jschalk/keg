from src.ch04_rope.rope import create_rope
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import personunit_v001
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch17_idea.brick_main import create_brick_df, get_brickref_obj, make_persondelta
from src.ch17_idea.idea_config import (
    br00013_planunit_v0_0_0,
    br00021_person_contactunit_v0_0_0,
)
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_make_persondelta_Arg_br00021_person_contactunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_contact_cred_lumen = 11
    bob_contact_cred_lumen = 13
    yao_contact_cred_lumen = 41
    sue_contact_debt_lumen = 23
    bob_contact_debt_lumen = 29
    yao_contact_debt_lumen = 37
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    sue_personunit.add_contactunit(
        exx.sue, sue_contact_cred_lumen, sue_contact_debt_lumen
    )
    sue_personunit.add_contactunit(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    sue_personunit.add_contactunit(
        exx.yao, yao_contact_cred_lumen, yao_contact_debt_lumen
    )
    x_brick_name = br00021_person_contactunit_v0_0_0()
    contact_dataframe = create_brick_df(sue_personunit, x_brick_name)
    print(f"{contact_dataframe.columns=}")
    contact_csv = contact_dataframe.to_csv(index=False)

    # WHEN
    sue_contact_persondelta = make_persondelta(contact_csv)

    # THEN
    assert sue_contact_persondelta
    sue_personatom = personatom_shop(kw.person_contactunit, kw.INSERT)
    sue_personatom.set_arg(kw.contact_name, exx.sue)
    sue_personatom.set_arg(kw.contact_cred_lumen, sue_contact_cred_lumen)
    sue_personatom.set_arg(kw.contact_debt_lumen, sue_contact_debt_lumen)
    sue_personatom.set_atom_order()
    bob_personatom = personatom_shop(kw.person_contactunit, kw.INSERT)
    bob_personatom.set_arg(kw.contact_name, exx.bob)
    bob_personatom.set_arg(kw.contact_cred_lumen, bob_contact_cred_lumen)
    bob_personatom.set_arg(kw.contact_debt_lumen, bob_contact_debt_lumen)
    bob_personatom.set_atom_order()
    # print(f"{sue_contact_persondelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_contact_persondelta.personatoms.get(kw.INSERT).get(kw.person_contactunit).get(exx.sue)=}"
    # )
    print(f"{sue_personatom=}")
    assert sue_contact_persondelta.c_personatom_exists(sue_personatom)
    assert sue_contact_persondelta.c_personatom_exists(bob_personatom)
    assert len(sue_contact_persondelta.get_ordered_personatoms()) == 3


# def test_make_persondelta_Arg_br00020_person_contact_membership_v0_0_0():
#     # ESTABLISH
#     exx.bob = "Bob"
#     exx.yao = "Yao"
#     amy_moment_rope = create_rope("amy56")
#     sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
#     sue_personunit.add_contactunit(exx.sue)
#     sue_personunit.add_contactunit(exx.bob)
#     sue_personunit.add_contactunit(exx.yao)
#     iowa_str = ";Iowa"
#     sue_iowa_group_cred_lumen = 37
#     bob_iowa_group_cred_lumen = 43
#     yao_iowa_group_cred_lumen = 51
#     sue_iowa_group_debt_lumen = 57
#     bob_iowa_group_debt_lumen = 61
#     yao_iowa_group_debt_lumen = 67
#     ohio_str = ";Ohio"
#     yao_ohio_group_cred_lumen = 73
#     yao_ohio_group_debt_lumen = 67
#     sue_contactunit = sue_personunit.get_contact(exx.sue)
#     bob_contactunit = sue_personunit.get_contact(exx.bob)
#     yao_contactunit = sue_personunit.get_contact(exx.yao)
#     sue_contactunit.add_membership(iowa_str, sue_iowa_group_cred_lumen, sue_iowa_group_debt_lumen)
#     bob_contactunit.add_membership(iowa_str, bob_iowa_group_cred_lumen, bob_iowa_group_debt_lumen)
#     yao_contactunit.add_membership(iowa_str, yao_iowa_group_cred_lumen, yao_iowa_group_debt_lumen)
#     yao_contactunit.add_membership(ohio_str, yao_ohio_group_cred_lumen, yao_ohio_group_debt_lumen)
#     x_brick_name = br00020_person_contact_membership_v0_0_0()
#     membership_dataframe = create_brick_df(sue_personunit, x_brick_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_persondelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_personatom = personatom_shop(kw.person_contact_membership, kw.INSERT)
#     bob_iowa_personatom = personatom_shop(kw.person_contact_membership, kw.INSERT)
#     yao_iowa_personatom = personatom_shop(kw.person_contact_membership, kw.INSERT)
#     yao_ohio_personatom = personatom_shop(kw.person_contact_membership, kw.INSERT)
#     sue_iowa_personatom.set_arg(kw.group_title, iowa_str)
#     bob_iowa_personatom.set_arg(kw.group_title, iowa_str)
#     yao_iowa_personatom.set_arg(kw.group_title, iowa_str)
#     yao_ohio_personatom.set_arg(kw.group_title, ohio_str)
#     sue_iowa_personatom.set_arg(kw.contact_name, exx.sue)
#     bob_iowa_personatom.set_arg(kw.contact_name, exx.bob)
#     yao_iowa_personatom.set_arg(kw.contact_name, exx.yao)
#     yao_ohio_personatom.set_arg(kw.contact_name, exx.yao)
#     sue_iowa_personatom.set_arg(kw.group_cred_lumen, sue_iowa_group_cred_lumen)
#     bob_iowa_personatom.set_arg(kw.group_cred_lumen, bob_iowa_group_cred_lumen)
#     yao_iowa_personatom.set_arg(kw.group_cred_lumen, yao_iowa_group_cred_lumen)
#     yao_ohio_personatom.set_arg(kw.group_cred_lumen, yao_ohio_group_cred_lumen)
#     sue_iowa_personatom.set_arg(kw.group_debt_lumen, sue_iowa_group_debt_lumen)
#     bob_iowa_personatom.set_arg(kw.group_debt_lumen, bob_iowa_group_debt_lumen)
#     yao_iowa_personatom.set_arg(kw.group_debt_lumen, yao_iowa_group_debt_lumen)
#     yao_ohio_personatom.set_arg(kw.group_debt_lumen, yao_ohio_group_debt_lumen)
#     bob_iowa_personatom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_personatoms()[2]=}")
#     # print(f"{sue_iowa_personatom=}")
#     assert len(membership_changunit.get_ordered_personatoms()) == 10
#     assert membership_changunit.get_ordered_personatoms()[0] == bob_iowa_personatom
#     assert membership_changunit.personatom_exists(sue_iowa_personatom)
#     assert membership_changunit.personatom_exists(bob_iowa_personatom)
#     assert membership_changunit.personatom_exists(yao_iowa_personatom)
#     assert membership_changunit.personatom_exists(yao_ohio_personatom)
#     assert len(membership_changunit.get_ordered_personatoms()) == 10


def test_make_persondelta_Arg_br00013_planunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_personunit.set_l1_plan(planunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    x_brick_name = br00013_planunit_v0_0_0()
    planunit_dataframe = create_brick_df(sue_personunit, x_brick_name)
    planunit_csv = planunit_dataframe.to_csv(index=False)

    # WHEN
    planunit_changunit = make_persondelta(planunit_csv)

    # THEN
    casa_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    casa_personatom.set_arg(kw.plan_rope, casa_rope)
    casa_personatom.set_arg(kw.pledge, False)
    casa_personatom.set_arg(kw.star, casa_star)
    print(f"{casa_personatom=}")
    assert casa_personatom.get_value(kw.star) == casa_star
    clean_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    clean_personatom.set_arg(kw.plan_rope, clean_rope)
    clean_personatom.set_arg(kw.pledge, True)
    clean_personatom.set_arg(kw.star, 1)
    assert planunit_changunit.c_personatom_exists(casa_personatom)
    assert planunit_changunit.c_personatom_exists(clean_personatom)
    assert len(planunit_changunit.get_ordered_personatoms()) == 2


def test_create_brick_df_Arg_br00013_planunit_v0_0_0_Scenario_personunit_v001(
    run_big_tests,
):
    # sourcery skip: no-conditionals-in-tests
    if run_big_tests:
        # ESTABLISH / WHEN
        x_brick_name = br00013_planunit_v0_0_0()

        # WHEN
        planunit_format = create_brick_df(personunit_v001(), x_brick_name)

        # THEN
        array_headers = list(planunit_format.columns)
        assert array_headers == get_brickref_obj(x_brick_name).get_headers_list()
        assert len(planunit_format) == 251
