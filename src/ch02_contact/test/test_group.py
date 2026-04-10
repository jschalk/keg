from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch02_contact.group import GroupUnit, groupunit_shop, membership_shop
from src.ref.keywords import Ch02Keywords as kw, ExampleStrs as exx


def test_GroupUnit_Exists():
    # ESTABLISH / WHEN
    x_groupunit = GroupUnit()
    # THEN
    assert x_groupunit is not None
    assert not x_groupunit.group_title
    assert not x_groupunit.memberships
    assert not x_groupunit.fund_give
    assert not x_groupunit.fund_take
    assert not x_groupunit.fund_agenda_give
    assert not x_groupunit.fund_agenda_take
    assert not x_groupunit.credor_pool
    assert not x_groupunit.debtor_pool
    assert not x_groupunit.fund_grain
    print(f"{x_groupunit.__dict__=}")
    assert set(x_groupunit.__dict__.keys()) == {
        kw.group_title,
        kw.memberships,
        kw.fund_give,
        kw.fund_take,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_grain,
    }


def test_groupunit_shop_ReturnsObj():
    # ESTABLISH
    bowlers_str = ";bowlers"

    # WHEN
    bowl_groupunit = groupunit_shop(group_title=bowlers_str)

    # THEN
    print(f"{bowlers_str}")
    assert bowl_groupunit is not None
    assert bowl_groupunit.group_title is not None
    assert bowl_groupunit.group_title == bowlers_str
    assert bowl_groupunit.memberships == {}
    assert bowl_groupunit.fund_give == 0
    assert bowl_groupunit.fund_take == 0
    assert bowl_groupunit.fund_agenda_give == 0
    assert bowl_groupunit.fund_agenda_take == 0
    assert bowl_groupunit.credor_pool == 0
    assert bowl_groupunit.debtor_pool == 0
    assert bowl_groupunit.fund_grain == default_grain_num_if_None()


def test_groupunit_shop_ReturnsObj_Scenario1_DefaultsPopulated():
    # ESTABLISH
    bowlers_str = "/bowlers"
    x_fund_grain = 7

    # WHEN
    bowl_groupunit = groupunit_shop(group_title=bowlers_str, fund_grain=x_fund_grain)

    # THEN
    assert bowl_groupunit.fund_grain == x_fund_grain


def test_GroupUnit_set_membership_SetsAttr():
    # ESTABLISH
    bowlers_str = ";bowlers"
    yao_bowl_membership = membership_shop(bowlers_str)
    sue_bowl_membership = membership_shop(bowlers_str)
    yao_bowl_membership.contact_name = exx.yao
    sue_bowl_membership.contact_name = exx.sue
    bowlers_groupunit = groupunit_shop(bowlers_str)

    # WHEN
    bowlers_groupunit.set_g_membership(yao_bowl_membership)
    bowlers_groupunit.set_g_membership(sue_bowl_membership)

    # THEN
    bowlers_memberships = {
        yao_bowl_membership.contact_name: yao_bowl_membership,
        sue_bowl_membership.contact_name: sue_bowl_membership,
    }
    assert bowlers_groupunit.memberships == bowlers_memberships


def test_GroupUnit_set_membership_SetsAttr_credor_pool_debtor_pool():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    ohio_str = ";Ohio"
    yao_ohio_membership = membership_shop(ohio_str)
    sue_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership.contact_name = exx.yao
    yao_ohio_membership.contact_name = exx.yao
    sue_ohio_membership.contact_name = exx.sue
    yao_ohio_membership.credor_pool = 66
    sue_ohio_membership.credor_pool = 22
    yao_ohio_membership.debtor_pool = 6600
    sue_ohio_membership.debtor_pool = 2200
    ohio_groupunit = groupunit_shop(ohio_str)
    assert ohio_groupunit.credor_pool == 0
    assert ohio_groupunit.debtor_pool == 0

    # WHEN
    ohio_groupunit.set_g_membership(yao_ohio_membership)
    # THEN
    assert ohio_groupunit.credor_pool == 66
    assert ohio_groupunit.debtor_pool == 6600

    # WHEN
    ohio_groupunit.set_g_membership(sue_ohio_membership)
    # THEN
    assert ohio_groupunit.credor_pool == 88
    assert ohio_groupunit.debtor_pool == 8800


def test_GroupUnit_set_membership_RaisesErrorIf_membership_group_title_IsWrong():
    # ESTABLISH
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    yao_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership.contact_name = exx.yao
    yao_ohio_membership.contact_name = exx.yao
    yao_ohio_membership.credor_pool = 66
    yao_ohio_membership.debtor_pool = 6600
    iowa_groupunit = groupunit_shop(iowa_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        iowa_groupunit.set_g_membership(yao_ohio_membership)
    exception_str = (
        f"GroupUnit.group_title={iowa_str} cannot set membership.group_title={ohio_str}"
    )
    assert str(excinfo.value) == exception_str


def test_GroupUnit_set_membership_RaisesErrorIf_contact_name_IsNone():
    # ESTABLISH
    ohio_str = ";Ohio"
    ohio_groupunit = groupunit_shop(ohio_str)
    yao_ohio_membership = membership_shop(ohio_str)
    assert yao_ohio_membership.contact_name is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ohio_groupunit.set_g_membership(yao_ohio_membership)

    # THEN
    exception_str = (
        f"membership group_title={ohio_str} cannot be set when _contact_name is None."
    )
    assert str(excinfo.value) == exception_str
