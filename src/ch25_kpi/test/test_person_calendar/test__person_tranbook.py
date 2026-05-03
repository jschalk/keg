from src.ch25_kpi.gcalendar import PersonTranBookMetric, persontranbookmetric_shop
from src.ref.keywords import Ch25Keywords as kw, ExampleStrs as exx


def test_PersonTranBookMetric_Exists():
    # ESTABLISH / WHEN
    persontranbookmetric = PersonTranBookMetric()
    # THEN
    assert persontranbookmetric
    assert not persontranbookmetric.moment_rope
    assert not persontranbookmetric.person_name
    assert not persontranbookmetric.offi_time
    assert not persontranbookmetric.last_tran_time
    assert not persontranbookmetric.net
    assert not persontranbookmetric.circulation_total
    assert set(persontranbookmetric.__dict__.keys()) == {
        kw.moment_rope,
        kw.person_name,
        kw.offi_time,
        "last_tran_time",
        "net",
        "circulation_total",
    }


def test_persontranbookmetric_shop_ReturnsObj_Scenario0():
    # ESTABLISH
    x_offi_time = 222
    x_last_tran_time = 333
    x_net = 7000
    x_circulation_total = 500000
    # WHEN
    transkpi = persontranbookmetric_shop(
        exx.a23, exx.sue, x_offi_time, x_last_tran_time, x_net, x_circulation_total
    )
    # THEN
    assert transkpi.moment_rope == exx.a23
    assert transkpi.person_name == exx.sue
    assert transkpi.offi_time == x_offi_time
    assert transkpi.last_tran_time == x_last_tran_time
    assert transkpi.net == x_net
    assert transkpi.circulation_total == x_circulation_total


def test_PersonTranBookMetric_get_circulation_str_ReturnsObj_Scenario0():
    # ESTABLISH
    x_offi_time = 222
    x_last_tran_time = 333
    x_net = 7000
    x_circulation_total = 500000
    transkpi = persontranbookmetric_shop(
        exx.a23, exx.sue, x_offi_time, x_last_tran_time, x_net, x_circulation_total
    )
    # WHEN
    circulation_str = transkpi.get_circulation_str()
    # THEN
    assert circulation_str
    expected_circulation_str = (
        f"{x_net} funds out of {x_circulation_total} at {x_offi_time}"
    )
    assert circulation_str == expected_circulation_str


def test_PersonTranBookMetric_get_circulation_str_ReturnsObj_Scenario1_Only_net():
    # ESTABLISH
    x_net = 7000
    transkpi = persontranbookmetric_shop(exx.a23, exx.sue, None, None, x_net, None)
    # WHEN
    circulation_str = transkpi.get_circulation_str()
    # THEN
    assert circulation_str
    expected_circulation_str = f"{x_net} funds"
    assert circulation_str == expected_circulation_str


def test_PersonTranBookMetric_get_circulation_str_ReturnsObj_Scenario2_Only_net_circulation_total():
    # ESTABLISH
    x_net = 7000
    x_circulation_total = 500000
    transkpi = persontranbookmetric_shop(
        exx.a23, exx.sue, None, None, x_net, x_circulation_total
    )
    # WHEN
    circulation_str = transkpi.get_circulation_str()
    # THEN
    assert circulation_str
    expected_circulation_str = f"{x_net} funds out of {x_circulation_total}"
    assert circulation_str == expected_circulation_str


def test_PersonTranBookMetric_get_circulation_str_ReturnsObj_Scenario3_ZeroAppears():
    # ESTABLISH
    x_net = 0
    x_circulation_total = 500000
    transkpi = persontranbookmetric_shop(
        exx.a23, exx.sue, None, None, x_net, x_circulation_total
    )
    # WHEN
    circulation_str = transkpi.get_circulation_str()
    # THEN
    assert circulation_str
    expected_circulation_str = f"0 funds out of {x_circulation_total}"
    assert circulation_str == expected_circulation_str
