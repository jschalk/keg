from src.ch02_contact.group import groupunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_get_contactunit_group_titles_dict_ReturnsObj():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob)
    bob_person.add_contactunit(exx.yao)
    bob_person.add_contactunit(exx.sue)
    bob_person.add_contactunit(exx.zia)
    sue_contactunit = bob_person.get_contact(exx.sue)
    zia_contactunit = bob_person.get_contact(exx.zia)
    bowl_group_str = ";bowl"
    sue_contactunit.add_membership(exx.run)
    zia_contactunit.add_membership(exx.run)
    zia_contactunit.add_membership(bowl_group_str)

    # WHEN
    group_titles_dict = bob_person.get_contactunit_group_titles_dict()

    # THEN
    print(f"{group_titles_dict=}")
    all_group_titles = {exx.yao, exx.sue, exx.zia, exx.run, bowl_group_str}
    assert set(group_titles_dict.keys()) == all_group_titles
    assert set(group_titles_dict.keys()) != {bowl_group_str, exx.run}
    assert group_titles_dict.get(bowl_group_str) == {exx.zia}
    assert group_titles_dict.get(exx.run) == {exx.zia, exx.sue}
    assert group_titles_dict.get(exx.yao) == {exx.yao}
    assert group_titles_dict.get(exx.sue) == {exx.sue}
    assert group_titles_dict.get(exx.zia) == {exx.zia}


def test_PersonUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob)
    assert not bob_person.groupunits.get(exx.run)

    # WHEN
    bob_person.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_person.groupunits.get(exx.run)


def test_PersonUnit_set_groupunit_Sets_rope_fund_grain():
    # ESTABLISH
    x_fund_grain = 5
    bob_person = personunit_shop(exx.bob, fund_grain=x_fund_grain)
    assert not bob_person.groupunits.get(exx.run)

    # WHEN
    bob_person.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_person.groupunits.get(exx.run).fund_grain == x_fund_grain


def test_PersonUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob)
    assert not bob_person.groupunit_exists(exx.run)

    # WHEN
    bob_person.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_person.groupunit_exists(exx.run)


def test_PersonUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_person = personunit_shop(exx.bob)
    x_run_groupunit = groupunit_shop(exx.run)
    bob_person.set_groupunit(x_run_groupunit)
    assert bob_person.groupunits.get(exx.run)

    # WHEN / THEN
    assert bob_person.get_groupunit(exx.run) == groupunit_shop(exx.run)


def test_PersonUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_group_cred_lumen = 3
    yao_group_debt_lumen = 2
    zia_group_cred_lumen = 4
    zia_group_debt_lumen = 5
    yao_person.add_contactunit(exx.yao, yao_group_cred_lumen, yao_group_debt_lumen)
    yao_person.add_contactunit(exx.zia, zia_group_cred_lumen, zia_group_debt_lumen)

    # WHEN
    xio_groupunit = yao_person.create_symmetry_groupunit(exx.xio)

    # THEN
    assert xio_groupunit.group_title == exx.xio
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert len(xio_groupunit.memberships) == 2
    yao_groupunit = xio_groupunit.get_contact_membership(exx.yao)
    zia_groupunit = xio_groupunit.get_contact_membership(exx.zia)
    assert yao_groupunit.group_cred_lumen == yao_group_cred_lumen
    assert zia_groupunit.group_cred_lumen == zia_group_cred_lumen
    assert yao_groupunit.group_debt_lumen == yao_group_debt_lumen
    assert zia_groupunit.group_debt_lumen == zia_group_debt_lumen
