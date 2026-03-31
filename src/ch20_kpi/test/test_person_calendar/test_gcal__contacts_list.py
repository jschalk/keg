from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch20_kpi.gcalendar import (
    gcal_readable_percent,
    get_gcal_contacts_str,
    get_gcal_memberships_str,
)
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_get_gcal_contacts_str_ReturnsObj_Scenario1_TwoContacts():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_contactunit(exx.bob, 2)
    bob_person.add_contactunit(exx.sue, 1)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    clean_rope = bob_person.make_rope(casa_rope, exx.clean)
    bob_person.add_plan(clean_rope, 1, pledge=True)
    bob_person.conpute()

    # WHEN
    gcal_contacts_str = get_gcal_contacts_str(bob_person)

    # THEN
    assert gcal_contacts_str
    expected_gcal_contacts_str = f"""Person Contacts
16.67% {exx.bob}
-16.67% {exx.sue}"""
    assert gcal_contacts_str == expected_gcal_contacts_str


def test_get_gcal_contacts_str_ReturnsObj_Scenario2_TwoContactsCorrectOrder():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_contactunit(exx.bob, 1)
    bob_person.add_contactunit(exx.sue, 2)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    clean_rope = bob_person.make_rope(casa_rope, exx.clean)
    bob_person.add_plan(clean_rope, 1, pledge=True)
    bob_person.conpute()

    # WHEN
    gcal_contacts_str = get_gcal_contacts_str(bob_person)

    # THEN
    assert gcal_contacts_str
    expected_gcal_contacts_str = f"""Person Contacts
16.67% {exx.sue}
-16.67% {exx.bob}"""
    assert gcal_contacts_str == expected_gcal_contacts_str


def test_get_gcal_memberships_str_ReturnsObj_Scenario0_NoMembership():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_contactunit(exx.bob, 2)

    # WHEN
    run_memberships_str = get_gcal_memberships_str(bob_person, exx.run)

    # THEN
    assert run_memberships_str
    expected_run_memberships_str = f"""{exx.run} Group\nNo memberships"""
    print(run_memberships_str)
    print(expected_run_memberships_str)
    assert run_memberships_str == expected_run_memberships_str


def test_get_gcal_memberships_str_ReturnsObj_Scenario1_TwoContacts():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_contactunit(exx.bob, 2)
    bob_person.add_contactunit(exx.sue, 1)
    bob_person.get_contact(exx.sue).add_membership(exx.run)
    bob_person.conpute()

    # WHEN
    run_memberships_str = get_gcal_memberships_str(bob_person, exx.run)

    # THEN
    assert run_memberships_str
    expected_run_memberships_str = f"""{exx.run} Group
-16.67% {exx.sue}"""
    assert run_memberships_str == expected_run_memberships_str
