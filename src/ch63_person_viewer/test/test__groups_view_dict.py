from ch08_person_logic.person_main import personunit_shop
from ch63_person_viewer.person_viewer_tool import add_small_dot, get_groups_view_dict
from ch63_person_viewer.test.test__contacts_view_dict import add_readable
from ch99_glossary.ch_keyword import Ch63Keywords as kw, ExampleStrs as exx


def test_get_groups_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_believer = personunit_shop(exx.sue)
    sue_believer.thinkout()

    # WHEN
    groups_view_dict = get_groups_view_dict(sue_believer)

    # THEN
    assert groups_view_dict == {}


# def test_get_groups_view_dict_ReturnsObj_Scenario1_groups():
#     # ESTABLISH
#     sue_believer = personunit_shop(exx.sue)
#     exx.yao = exx.yao
#     bob_str = "Bob"
#     yao_cred_mass = 110
#     yao_debt_mass = 130
#     bob_cred_mass = 230
#     bob_debt_mass = 290
#     sue_believer.add_contactunit(exx.yao, yao_cred_mass, yao_debt_mass)
#     sue_believer.add_contactunit(bob_str, bob_cred_mass, bob_debt_mass)
#     bowlers_str = ";bowlers"
#     bob_bowl_cred_mass = 66
#     bob_bowl_debt_mass = 77
#     yao_bowl_cred_mass = 88
#     yao_bowl_debt_mass = 99
#     yao_contact = sue_believer.get_contact(exx.yao)
#     bob_contact = sue_believer.get_contact(bob_str)
#     yao_contact.add_membership(bowlers_str, yao_bowl_cred_mass, yao_bowl_debt_mass)
#     bob_contact.add_membership(bowlers_str, bob_bowl_cred_mass, bob_bowl_debt_mass)
#     sue_believer.thinkout()

#     # WHEN
#     groups_view_dict = get_groups_view_dict(sue_believer)

#     # THEN
#     assert set(groups_view_dict.keys()) == {exx.yao, bob_str, bowlers_str}

#     bowl_group_dict = groups_view_dict.get(bowlers_str)
#     group_title_readable_key = add_readable(kw.group_title)
#     memberships_readable_key = add_readable(kw.memberships)
#     fund_give_readable_key = add_readable(kw.fund_give)
#     fund_take_readable_key = add_readable(kw.fund_take)
#     fund_agenda_give_readable_key = add_readable(kw.fund_agenda_give)
#     fund_agenda_take_readable_key = add_readable(kw.fund_agenda_take)
#     credor_pool_readable_key = add_readable(kw.credor_pool)
#     debtor_pool_readable_key = add_readable(kw.debtor_pool)
#     assert set(bowl_group_dict.keys()) == {
#         kw.group_title,
#         kw.memberships,
#         kw.fund_give,
#         kw.fund_take,
#         kw.fund_agenda_give,
#         kw.fund_agenda_take,
#         kw.credor_pool,
#         kw.debtor_pool,
#         group_title_readable_key,
#         memberships_readable_key,
#         fund_give_readable_key,
#         fund_take_readable_key,
#         fund_agenda_give_readable_key,
#         fund_agenda_take_readable_key,
#         credor_pool_readable_key,
#         debtor_pool_readable_key,
#     }

#     bowl_groupunit = sue_believer.get_groupunit(bowlers_str)
#     bowl_group_title_readable = f"group_title_readable: {bowl_groupunit.group_title}"
#     bowl_memberships_readable = f"memberships_readable: {bowl_groupunit.memberships}"
#     bowl_fund_give_readable = f"fund_give_readable: {bowl_groupunit.fund_give}"
#     bowl_fund_take_readable = f"fund_take_readable: {bowl_groupunit.fund_take}"
#     bowl_fund_agenda_give_readable = (
#         f"fund_agenda_give_readable: {bowl_groupunit.fund_agenda_give}"
#     )
#     bowl_fund_agenda_take_readable = (
#         f"fund_agenda_take_readable: {bowl_groupunit.fund_agenda_take}"
#     )
#     bowl_credor_pool_readable = f"credor_pool_readable: {bowl_groupunit.credor_pool}"
#     bowl_debtor_pool_readable = f"debtor_pool_readable: {bowl_groupunit.debtor_pool}"

#     sgu = bowl_groupunit
#     sg_dict = bowl_group_dict
#     assert sgu.group_title == sg_dict.get(kw.group_title)
#     assert sgu.memberships == sg_dict.get(kw.memberships)
#     assert sgu.fund_give == sg_dict.get(kw.fund_give)
#     assert sgu.fund_take == sg_dict.get(kw.fund_take)
#     assert sgu.fund_agenda_give == sg_dict.get(kw.fund_agenda_give)
#     assert sgu.fund_agenda_take == sg_dict.get(kw.fund_agenda_take)
#     assert sgu.credor_pool == sg_dict.get(kw.credor_pool)
#     assert sgu.debtor_pool == sg_dict.get(kw.debtor_pool)
#     assert bowl_group_title_readable == sg_dict.get(group_title_readable_key)
#     assert bowl_memberships_readable == sg_dict.get(memberships_readable_key)
#     assert bowl_fund_give_readable == sg_dict.get(fund_give_readable_key)
#     assert bowl_fund_take_readable == sg_dict.get(fund_take_readable_key)
#     assert bowl_fund_agenda_give_readable == sg_dict.get(fund_agenda_give_readable_key)
#     assert bowl_fund_agenda_take_readable == sg_dict.get(fund_agenda_take_readable_key)
#     assert bowl_credor_pool_readable == sg_dict.get(credor_pool_readable_key)
#     assert bowl_debtor_pool_readable == sg_dict.get(debtor_pool_readable_key)


# def test_get_groups_view_dict_ReturnsObj_Scenario2_memberships():
#     # ESTABLISH
#     sue_believer = personunit_shop(exx.sue)
#     exx.yao = exx.yao
#     sue_believer.add_contactunit(exx.yao)
#     bowlers_str = ";bowlers"
#     yao_bowl_cred_mass = 311
#     yao_bowl_debt_mass = 313
#     yao_contactunit = sue_believer.get_contact(exx.yao)
#     yao_contactunit.add_membership(bowlers_str, yao_bowl_cred_mass, yao_bowl_debt_mass)
#     sue_believer.thinkout()

#     # WHEN
#     groups_view_dict = get_groups_view_dict(sue_believer)

#     # THEN
#     assert set(groups_view_dict.keys()) == {exx.yao}
#     yao_contact_dict = groups_view_dict.get(exx.yao)
#     assert kw.memberships in set(yao_contact_dict.keys())
#     yao_memberships_dict = yao_contact_dict.get(kw.memberships)
#     assert {bowlers_str, exx.yao} == set(yao_memberships_dict.keys())
#     yao_bowl_dict = yao_memberships_dict.get(bowlers_str)

#     group_title_readable_key = add_readable(kw.group_title)
#     group_cred_mass_readable_key = add_readable(kw.group_cred_mass)
#     group_debt_mass_readable_key = add_readable(kw.group_debt_mass)
#     credor_pool_readable_key = add_readable(kw.credor_pool)
#     debtor_pool_readable_key = add_readable(kw.debtor_pool)
#     fund_agenda_give_readable_key = add_readable(kw.fund_agenda_give)
#     fund_agenda_ratio_give_readable_key = add_readable(kw.fund_agenda_ratio_give)
#     fund_agenda_ratio_take_readable_key = add_readable(kw.fund_agenda_ratio_take)
#     fund_agenda_take_readable_key = add_readable(kw.fund_agenda_take)
#     fund_give_readable_key = add_readable(kw.fund_give)
#     fund_take_readable_key = add_readable(kw.fund_take)
#     assert set(yao_bowl_dict.keys()) == {
#         kw.contact_name,
#        kw.group_title,
#        kw.group_cred_mass,
#        kw.group_debt_mass,
#         kw.credor_pool,
#         kw.debtor_pool,
#         kw.fund_agenda_give,
#         kw.fund_agenda_ratio_give,
#         kw.fund_agenda_ratio_take,
#         kw.fund_agenda_take,
#         kw.fund_give,
#         kw.fund_take,
#         group_title_readable_key,
#         group_cred_mass_readable_key,
#         group_debt_mass_readable_key,
#         credor_pool_readable_key,
#         debtor_pool_readable_key,
#         fund_agenda_give_readable_key,
#         fund_agenda_ratio_give_readable_key,
#         fund_agenda_ratio_take_readable_key,
#         fund_agenda_take_readable_key,
#         fund_give_readable_key,
#         fund_take_readable_key,
#     }
#     yao_bowl_mu = yao_contactunit.get_membership(bowlers_str)
#     expected_group_title_readable = f"{kw.group_title}: {yao_bowl_mu.group_title}"
#     expected_group_cred_mass_readable = (
#         f"{kw.group_cred_mass}: {yao_bowl_mu.group_cred_mass}"
#     )
#     expected_group_debt_mass_readable = (
#         f"{kw.group_debt_mass}: {yao_bowl_mu.group_debt_mass}"
#     )
#     expected_credor_pool_readable = f"{kw.credor_pool}: {yao_bowl_mu.credor_pool}"
#     expected_debtor_pool_readable = f"{kw.debtor_pool}: {yao_bowl_mu.debtor_pool}"
#     expected_fund_agenda_give_readable = (
#         f"{kw.fund_agenda_give}: {yao_bowl_mu.fund_agenda_give}"
#     )
#     expected_fund_agenda_ratio_give_readable = (
#         f"{kw.fund_agenda_ratio_give}: {yao_bowl_mu.fund_agenda_ratio_give}"
#     )
#     expected_fund_agenda_ratio_take_readable = (
#         f"{kw.fund_agenda_ratio_take}: {yao_bowl_mu.fund_agenda_ratio_take}"
#     )
#     expected_fund_agenda_take_readable = (
#         f"{kw.fund_agenda_take}: {yao_bowl_mu.fund_agenda_take}"
#     )
#     expected_fund_give_readable = f"{kw.fund_give}: {yao_bowl_mu.fund_give}"
#     expected_fund_take_readable = f"{kw.fund_take}: {yao_bowl_mu.fund_take}"

#     assert yao_bowl_dict.get(kw.contact_name) == yao_bowl_mu.contact_name
#     assert yao_bowl_dict.get(kw.group_title) == yao_bowl_mu.group_title
#     assert yao_bowl_dict.get(kw.group_cred_mass) == yao_bowl_mu.group_cred_mass
#     assert yao_bowl_dict.get(kw.group_debt_mass) == yao_bowl_mu.group_debt_mass
#     assert yao_bowl_dict.get(kw.credor_pool) == yao_bowl_mu.credor_pool
#     assert yao_bowl_dict.get(kw.debtor_pool) == yao_bowl_mu.debtor_pool
#     assert yao_bowl_dict.get(kw.fund_agenda_give) == yao_bowl_mu.fund_agenda_give
#     assert (
#         yao_bowl_dict.get(kw.fund_agenda_ratio_give)
#         == yao_bowl_mu.fund_agenda_ratio_give
#     )
#     assert (
#         yao_bowl_dict.get(kw.fund_agenda_ratio_take)
#         == yao_bowl_mu.fund_agenda_ratio_take
#     )
#     assert yao_bowl_dict.get(kw.fund_agenda_take) == yao_bowl_mu.fund_agenda_take
#     assert yao_bowl_dict.get(kw.fund_give) == yao_bowl_mu.fund_give
#     assert yao_bowl_dict.get(kw.fund_take) == yao_bowl_mu.fund_take
#     assert yao_bowl_dict.get(group_title_readable_key) == expected_group_title_readable
#     assert (
#         yao_bowl_dict.get(group_cred_mass_readable_key)
#         == expected_group_cred_mass_readable
#     )
#     assert (
#         yao_bowl_dict.get(group_debt_mass_readable_key)
#         == expected_group_debt_mass_readable
#     )
#     assert (
#         yao_bowl_dict.get(credor_pool_readable_key) == expected_credor_pool_readable
#     )
#     assert (
#         yao_bowl_dict.get(debtor_pool_readable_key) == expected_debtor_pool_readable
#     )
#     assert (
#         yao_bowl_dict.get(fund_agenda_give_readable_key)
#         == expected_fund_agenda_give_readable
#     )
#     assert (
#         yao_bowl_dict.get(fund_agenda_ratio_give_readable_key)
#         == expected_fund_agenda_ratio_give_readable
#     )
#     assert (
#         yao_bowl_dict.get(fund_agenda_ratio_take_readable_key)
#         == expected_fund_agenda_ratio_take_readable
#     )
#     assert (
#         yao_bowl_dict.get(fund_agenda_take_readable_key)
#         == expected_fund_agenda_take_readable
#     )
#     assert yao_bowl_dict.get(fund_give_readable_key) == expected_fund_give_readable
#     assert yao_bowl_dict.get(fund_take_readable_key) == expected_fund_take_readable

#     # sue_believer = personunit_shop(exx.sue)
#     # exx.yao = exx.yao
#     # bob_str = "Bob"
#     # yao_cred_mass = 110
#     # yao_debt_mass = 130
#     # bob_cred_mass = 230
#     # bob_debt_mass = 290
#     # sue_believer.add_contactunit(exx.yao, yao_cred_mass, yao_debt_mass)
#     # sue_believer.add_contactunit(bob_str, bob_cred_mass, bob_debt_mass)
#     # bowlers_str = ";bowlers"
#     # yao_bowl_cred_mass = 311
#     # yao_bowl_debt_mass = 313
#     # bob_bowl_cred_mass = 411
#     # bob_bowl_debt_mass = 413
#     # clea_str = ";cleaners"
#     # cleaners_cred_mass = 511
#     # cleaners_debt_mass = 513
#     # yao_contactunit = sue_believer.get_contact(exx.yao)
#     # bob_contactunit = sue_believer.get_contact(bob_str)
#     # bob_contactunit.add_membership(bowlers_str, bob_bowl_cred_mass, bob_bowl_debt_mass)
#     # yao_contactunit.add_membership(bowlers_str, yao_bowl_cred_mass, yao_bowl_debt_mass)
#     # yao_contactunit.add_membership(clea_str, cleaners_cred_mass, cleaners_debt_mass)
#     # sue_believer.get_contact(exx.yao).add_membership()
