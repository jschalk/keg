from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_pool_num
from src.ch11_bud.bud_main import (
    DEFAULT_CELLDEPTH,
    BudUnit,
    budunit_shop,
    get_budunit_from_dict,
)
from src.ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_DEFAULT_CELLDEPTH():
    # ESTABLISH / WHEN / THEN
    assert DEFAULT_CELLDEPTH == 2


def test_BudUnit_Exists():
    # ESTABLISH / WHEN
    x_budunit = BudUnit()

    # THEN
    assert x_budunit
    assert not x_budunit.bud_time
    assert not x_budunit.quota
    assert not x_budunit.celldepth
    assert not x_budunit.bud_contact_nets
    assert not x_budunit.magnitude


def test_budunit_shop_ReturnsObj():
    # ESTABLISH
    t4_bud_time = 4

    # WHEN
    t4_budunit = budunit_shop(t4_bud_time)

    # THEN
    assert t4_budunit
    assert t4_budunit.bud_time == t4_bud_time
    assert t4_budunit.quota == default_pool_num()
    assert t4_budunit.magnitude == 0
    assert t4_budunit.celldepth == 2
    assert not t4_budunit.bud_contact_nets


def test_budunit_shop_ReturnsObjWith_bud_contact_net():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_bud_contact_nets = {"Sue": -4}
    t4_magnitude = 677
    t4_celldepth = 88

    # WHEN
    x_budunit = budunit_shop(
        bud_time=t4_bud_time,
        quota=t4_quota,
        bud_contact_nets=t4_bud_contact_nets,
        magnitude=t4_magnitude,
        celldepth=t4_celldepth,
    )

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit.celldepth == t4_celldepth
    assert x_budunit.magnitude == 677
    assert x_budunit.bud_contact_nets == t4_bud_contact_nets


def test_BudUnit_set_bud_contact_net_SetsAttr():
    # ESTABLISH
    yao_budunit = budunit_shop(exx.yao, 33)
    assert yao_budunit.bud_contact_nets == {}

    # WHEN
    sue_bud_contact_net = -44
    yao_budunit.set_bud_contact_net(exx.sue, sue_bud_contact_net)

    # THEN
    assert yao_budunit.bud_contact_nets != {}
    assert yao_budunit.bud_contact_nets.get(exx.sue) == sue_bud_contact_net


def test_BudUnit_bud_contact_net_exists_ReturnsObj():
    # ESTABLISH
    yao_budunit = budunit_shop(exx.yao, 33)
    sue_bud_contact_net = -44
    assert yao_budunit.bud_contact_net_exists(exx.sue) is False

    # WHEN
    yao_budunit.set_bud_contact_net(exx.sue, sue_bud_contact_net)

    # THEN
    assert yao_budunit.bud_contact_net_exists(exx.sue)


def test_BudUnit_get_bud_contact_net_ReturnsObj():
    # ESTABLISH
    yao_budunit = budunit_shop(exx.yao, 33)
    sue_bud_contact_net = -44
    yao_budunit.set_bud_contact_net(exx.sue, sue_bud_contact_net)

    # WHEN / THEN
    assert yao_budunit.get_bud_contact_net(exx.sue)
    assert yao_budunit.get_bud_contact_net(exx.sue) == sue_bud_contact_net


def test_BudUnit_del_bud_contact_net_SetsAttr():
    # ESTABLISH
    yao_budunit = budunit_shop(exx.yao, 33)
    sue_bud_contact_net = -44
    yao_budunit.set_bud_contact_net(exx.sue, sue_bud_contact_net)
    assert yao_budunit.bud_contact_net_exists(exx.sue)

    # WHEN
    yao_budunit.del_bud_contact_net(exx.sue)

    # THEN
    assert yao_budunit.bud_contact_net_exists(exx.sue) is False


def test_BudUnit_to_dict_ReturnsObj():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_budunit = budunit_shop(t4_bud_time, t4_quota)

    # WHEN
    t4_dict = t4_budunit.to_dict()

    # THEN
    assert t4_dict == {kw.bud_time: t4_bud_time, kw.quota: t4_quota}


def test_BudUnit_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_bud_time = 4
    t4_budunit = budunit_shop(t4_bud_time)
    assert t4_budunit.magnitude == 0

    # WHEN
    t4_budunit.calc_magnitude()

    # THEN
    assert t4_budunit.magnitude == 0


def test_BudUnit_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_bud_time = 4
    t4_bud_contact_nets = {"Sue": -4, exx.yao: 2, "Zia": 2}

    t4_budunit = budunit_shop(t4_bud_time, bud_contact_nets=t4_bud_contact_nets)
    assert t4_budunit.magnitude == 0

    # WHEN
    t4_budunit.calc_magnitude()

    # THEN
    assert t4_budunit.magnitude == 4


def test_BudUnit_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_bud_time = 4
    t4_bud_contact_nets = {"Bob": -13, "Sue": -7, exx.yao: 18, "Zia": 2}

    t4_budunit = budunit_shop(t4_bud_time, bud_contact_nets=t4_bud_contact_nets)
    assert t4_budunit.magnitude == 0

    # WHEN
    t4_budunit.calc_magnitude()

    # THEN
    assert t4_budunit.magnitude == 20


def test_BudUnit_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_bud_time = 4
    bob_bud_contact_net = -13
    sue_bud_contact_net = -3
    yao_bud_contact_net = 100
    t4_bud_contact_nets = {
        "Bob": bob_bud_contact_net,
        "Sue": sue_bud_contact_net,
        exx.yao: yao_bud_contact_net,
    }
    t4_budunit = budunit_shop(t4_bud_time, bud_contact_nets=t4_bud_contact_nets)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_budunit.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_bud_contact_net={bob_bud_contact_net+sue_bud_contact_net}, cred_bud_contact_net={yao_bud_contact_net}"
    assert str(excinfo.value) == exception_str


def test_BudUnit_to_dict_ReturnsObjWith_bud_contact_net():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_bud_contact_nets = {"Sue": -4}
    t4_magnitude = 67
    t4_celldepth = 5
    t4_budunit = budunit_shop(
        t4_bud_time, t4_quota, t4_bud_contact_nets, t4_magnitude, t4_celldepth
    )

    # WHEN
    t4_dict = t4_budunit.to_dict()

    # THEN
    assert t4_dict == {
        kw.bud_time: t4_bud_time,
        kw.quota: t4_quota,
        kw.magnitude: t4_magnitude,
        kw.bud_contact_nets: t4_bud_contact_nets,
        kw.celldepth: t4_celldepth,
    }


def test_get_budunit_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_budunit = budunit_shop(t4_bud_time, t4_quota)
    t4_dict = t4_budunit.to_dict()
    assert t4_dict == {kw.bud_time: t4_bud_time, kw.quota: t4_quota}

    # WHEN
    x_budunit = get_budunit_from_dict(t4_dict)

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit.magnitude == 0
    assert x_budunit == t4_budunit


def test_get_budunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_celldepth = 33
    t4_bud_contact_nets = {"Sue": -77}
    t4_budunit = budunit_shop(
        t4_bud_time,
        t4_quota,
        t4_bud_contact_nets,
        t4_magnitude,
        celldepth=t4_celldepth,
    )
    t4_dict = t4_budunit.to_dict()

    # WHEN
    x_budunit = get_budunit_from_dict(t4_dict)

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit.magnitude == t4_magnitude
    assert x_budunit.bud_contact_nets == t4_bud_contact_nets
    assert x_budunit.celldepth == t4_celldepth
    assert x_budunit == t4_budunit
