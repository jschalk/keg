from ch11_bud.bud_main import (
    TranBook,
    TranUnit,
    get_tranbook_from_dict,
    tranbook_shop,
    tranunit_shop,
)
from pytest import raises as pytest_raises
from ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_TranUnit_Exists():
    # ESTABLISH / WHEN
    x_tranunit = TranUnit()

    # THEN
    assert x_tranunit
    assert not x_tranunit.src
    assert not x_tranunit.dst
    assert not x_tranunit.tran_time
    assert not x_tranunit.amount


def test_tranunit_shop_WithParametersReturnsObj():
    # ESTABLISH
    t55_tran_time = 5505
    t55_fundnum = -45

    # WHEN
    x_tranunit = tranunit_shop(exx.sue, exx.yao, t55_tran_time, t55_fundnum)

    # THEN
    assert x_tranunit
    assert x_tranunit.src == exx.sue
    assert x_tranunit.dst == exx.yao
    assert x_tranunit.tran_time == t55_tran_time
    assert x_tranunit.amount == t55_fundnum


def test_TranBook_Exists():
    # ESTABLISH / WHEN
    x_tranbook = TranBook()

    # THEN
    assert x_tranbook
    assert not x_tranbook.moment_rope
    assert not x_tranbook.tranunits
    assert not x_tranbook._contacts_net


def test_tranbook_shop_WithParametersReturnsObj():
    # ESTABLISH
    x_timenum = 5505
    x_fundnum = -45
    x_tranunits = {exx.sue: {exx.yao: {x_timenum: x_fundnum}}}

    # WHEN
    x_tranbook = tranbook_shop(exx.a23, x_tranunits)

    # THEN
    assert x_tranbook
    assert x_tranbook.moment_rope == exx.a23
    assert x_tranbook.tranunits == x_tranunits
    assert x_tranbook._contacts_net == {}


def test_tranbook_shop_WithoutParametersReturnsObj():
    # ESTABLISH

    # WHEN
    x_tranbook = tranbook_shop(exx.a23)

    # THEN
    assert x_tranbook
    assert x_tranbook.moment_rope == exx.a23
    assert x_tranbook.tranunits == {}
    assert x_tranbook._contacts_net == {}


def test_TranBook_set_tranunit_SetsAttr():
    # ESTABLISH
    x_tranbook = tranbook_shop(exx.a23)
    assert x_tranbook.tranunits == {}

    # WHEN
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount)
    x_tranbook.set_tranunit(sue_yao_t55_tranunit)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {exx.sue: {exx.yao: {t55_t: t55_yao_amount}}}

    # WHEN
    t55_bob_amount = 600
    sue_bob_t55_tranunit = tranunit_shop(exx.sue, exx.bob, t55_t, t55_bob_amount)
    x_tranbook.set_tranunit(sue_bob_t55_tranunit)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_t: t55_yao_amount},
            exx.bob: {t55_t: t55_bob_amount},
        }
    }

    # WHEN
    t66_t = 6606
    t66_yao_amount = -66
    sue_yao_t66_tranunit = tranunit_shop(exx.sue, exx.yao, t66_t, t66_yao_amount)
    x_tranbook.set_tranunit(sue_yao_t66_tranunit)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_t: t55_yao_amount, t66_t: t66_yao_amount},
            exx.bob: {t55_t: t55_bob_amount},
        }
    }

    # WHEN
    t77_t = 7707
    t77_yao_amount = -77
    yao_yao_77_tranunit = tranunit_shop(exx.yao, exx.yao, t77_t, t77_yao_amount)
    x_tranbook.set_tranunit(yao_yao_77_tranunit)

    # THEN
    print(f"{x_tranbook.tranunits=}")
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_t: t55_yao_amount, t66_t: t66_yao_amount},
            exx.bob: {t55_t: t55_bob_amount},
        },
        exx.yao: {exx.yao: {t77_t: t77_yao_amount}},
    }


def test_TranBook_set_tranunit_SetsAttrWithBlocktran_time():
    # ESTABLISH
    x_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN
    x_blocked_tran_times = {44}
    x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_tran_times)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {exx.sue: {exx.yao: {t55_t: t55_yao_amount}}}


def test_TranBook_set_tranunit_SetsAttrWithBlocktran_time_RaisesError():
    # ESTABLISH
    x_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    x_blocked_tran_times = {t55_t}
    sue_yao_t55_tranunit = tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_tran_times)
    exception_str = f"Cannot set tranunit for tran_time={t55_t}, TimeNum is blocked"
    assert str(excinfo.value) == exception_str


def test_TranBook_set_tranunit_SetsAttrWithCurrenttran_time():
    # ESTABLISH
    x_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN
    x_offi_time_max = 8808
    x_tranbook.set_tranunit(sue_yao_t55_tranunit, offi_time_max=x_offi_time_max)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {exx.sue: {exx.yao: {t55_t: t55_yao_amount}}}


def test_TranBook_set_tranunit_SetsAttrWithCurrenttran_time_RaisesError():
    # ESTABLISH
    x_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, offi_time_max=t55_t)
    exception_str = f"Cannot set tranunit for tran_time={t55_t}, TimeNum is greater than current time={t55_t}"
    assert str(excinfo.value) == exception_str

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, offi_time_max=33)
    exception_str = f"Cannot set tranunit for tran_time={t55_t}, TimeNum is greater than current time=33"
    assert str(excinfo.value) == exception_str


def test_TranBook_add_tranunit_SetsAttr():
    # ESTABLISH
    x_tranbook = tranbook_shop(exx.a23)
    assert x_tranbook.tranunits == {}

    # WHEN
    t55_tran_time = 5505
    t55_yao_amount = -55
    x_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {exx.sue: {exx.yao: {t55_tran_time: t55_yao_amount}}}

    # WHEN
    t55_bob_amount = 600
    x_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        }
    }

    # WHEN
    t66_tran_time = 6606
    t66_yao_amount = -66
    x_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        }
    }

    # WHEN
    t77_tran_time = 7707
    t77_yao_amount = -77
    x_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)

    # THEN
    print(f"{x_tranbook.tranunits=}")
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        },
        exx.yao: {exx.yao: {t77_tran_time: t77_yao_amount}},
    }


def test_TranBook_tranunit_exists_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert amy23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t) is False

    # WHEN
    amy23_tranbook.set_tranunit(sue_yao_t55_tranunit)

    # THEN
    assert amy23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t)


def test_TranBook_get_tranunit_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert amy23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t)

    # WHEN
    sue_yao_t55_tranunit = amy23_tranbook.get_tranunit(exx.sue, exx.yao, t55_t)

    # THEN
    assert sue_yao_t55_tranunit
    assert sue_yao_t55_tranunit.src == exx.sue
    assert sue_yao_t55_tranunit.dst == exx.yao
    assert sue_yao_t55_tranunit.tran_time == t55_t
    assert sue_yao_t55_tranunit.amount == t55_yao_amount

    # WHEN / THEN
    assert not amy23_tranbook.get_tranunit(exx.sue, "Bob", t55_t)
    assert not amy23_tranbook.get_tranunit("Bob", exx.yao, t55_t)
    assert not amy23_tranbook.get_tranunit(exx.sue, exx.yao, 44)


def test_TranBook_get_amount_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert amy23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t)

    # WHEN / THEN
    assert amy23_tranbook.get_amount(exx.sue, exx.yao, t55_t) == t55_yao_amount
    assert not amy23_tranbook.get_amount(exx.sue, "Bob", t55_t)
    assert not amy23_tranbook.get_amount("Bob", exx.yao, t55_t)
    assert not amy23_tranbook.get_amount(exx.sue, exx.yao, 44)


def test_TranBook_del_tranunit_SetsAttr():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_t, t55_yao_amount)
    assert amy23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t)

    # WHEN
    amy23_tranbook.del_tranunit(exx.sue, exx.yao, t55_t)

    # THEN
    assert amy23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t) is False


def test_TranBook_get_tran_times_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_bob_amount = -77
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t77_tran_time, t77_bob_amount)

    # WHEN
    amy23_tran_times = amy23_tranbook.get_tran_times()

    # THEN
    assert amy23_tran_times
    assert len(amy23_tran_times)
    assert amy23_tran_times == {t55_tran_time, t66_tran_time, t77_tran_time}


def test_TranBook_get_persons_contacts_net_ReturnsObj_Scenario0():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_bob_amount = 600
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {exx.bob: {t55_tran_time: t55_bob_amount}}
    }

    # WHEN
    amy23_contacts_net_dict = amy23_tranbook.get_persons_contacts_net()

    # THEN
    assert amy23_contacts_net_dict
    assert amy23_contacts_net_dict == {exx.sue: {exx.bob: t55_bob_amount}}


def test_TranBook_get_persons_contacts_net_ReturnsObj_Scenario1():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        }
    }

    # WHEN
    amy23_contacts_net_dict = amy23_tranbook.get_persons_contacts_net()

    # THEN
    assert amy23_contacts_net_dict
    assert amy23_contacts_net_dict == {
        exx.sue: {exx.yao: t55_yao_amount + t66_yao_amount, exx.bob: t55_bob_amount}
    }


def test_TranBook_get_contacts_net_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_bob_amount = 600
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {exx.bob: {t55_tran_time: t55_bob_amount}}
    }

    # WHEN
    amy23_contacts_net_dict = amy23_tranbook.get_contacts_net_dict()

    # THEN
    assert amy23_contacts_net_dict
    assert amy23_contacts_net_dict == {exx.bob: t55_bob_amount}


def test_TranBook_get_contacts_net_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)

    amy23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        },
        exx.yao: {exx.yao: {t77_tran_time: t77_yao_amount}},
    }

    # WHEN
    amy23_contacts_net_dict = amy23_tranbook.get_contacts_net_dict()

    # THEN
    assert amy23_contacts_net_dict
    assert amy23_contacts_net_dict == {
        exx.yao: t55_yao_amount + t66_yao_amount + t77_yao_amount,
        exx.bob: t55_bob_amount,
    }


def test_TranBook_get_contacts_net_array_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)

    amy23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        },
        exx.yao: {exx.yao: {t77_tran_time: t77_yao_amount}},
    }

    # WHEN
    amy23_contacts_net_array = amy23_tranbook._get_contacts_net_array()

    # THEN
    assert amy23_contacts_net_array
    assert amy23_contacts_net_array == [
        [exx.bob, t55_bob_amount],
        [exx.yao, t55_yao_amount + t66_yao_amount + t77_yao_amount],
    ]


def test_TranBook_get_contacts_headers_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)

    # WHEN / THEN
    assert amy23_tranbook._get_contacts_headers() == [kw.contact_name, "net_amount"]


def test_TranBook_get_contacts_csv_ReturnsObj():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)

    amy23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        },
        exx.yao: {exx.yao: {t77_tran_time: t77_yao_amount}},
    }

    # WHEN
    amy23_contacts_net_csv = amy23_tranbook.get_contacts_net_csv()

    # THEN
    assert amy23_contacts_net_csv
    example_csv = f"""contact_name,net_amount
{exx.bob},{t55_bob_amount}
{exx.yao},{t55_yao_amount + t66_yao_amount + t77_yao_amount}
"""
    assert amy23_contacts_net_csv == example_csv


def test_TranBook_to_dict_ReturnsObj():
    # ESTABLISH
    x_timenum = 5505
    x_fundnum = -45
    all_tranunits = {exx.sue: {exx.yao: {x_timenum: x_fundnum}}}
    x_tranbook = tranbook_shop(exx.a23, all_tranunits)

    # WHEN
    x_dict = x_tranbook.to_dict()

    # THEN
    tranunits_str = "tranunits"
    assert x_dict
    assert kw.moment_rope in x_dict.keys()
    assert x_dict.get(kw.moment_rope) == exx.a23
    assert tranunits_str in x_dict.keys()
    tranunits_dict = x_dict.get(tranunits_str)
    assert tranunits_dict.get(exx.sue)
    sue_trans_dict = tranunits_dict.get(exx.sue)
    assert sue_trans_dict.get(exx.yao)
    assert sue_trans_dict.get(exx.yao) == {x_timenum: x_fundnum}
    assert tranunits_dict == all_tranunits


def test_get_tranbook_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    amy23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    assert amy23_tranbook.tranunits == {
        exx.sue: {
            exx.yao: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            exx.bob: {t55_tran_time: t55_bob_amount},
        },
        exx.yao: {exx.yao: {t77_tran_time: t77_yao_amount}},
    }
    amy23_dict = amy23_tranbook.to_dict()

    # WHEN
    generated_tranbook = get_tranbook_from_dict(amy23_dict)

    # THEN
    assert generated_tranbook
    assert generated_tranbook.moment_rope == exx.a23
    assert generated_tranbook.tranunits == amy23_tranbook.tranunits
    assert generated_tranbook == amy23_tranbook


def test_get_tranbook_from_dict_ReturnsObj_Sccenario1():
    # ESTABLISH
    amy23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    amy23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    amy23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)

    str_tran_time_amy23_dict = {
        kw.moment_rope: exx.a23,
        "tranunits": {
            exx.sue: {
                exx.yao: {
                    str(t55_tran_time): t55_yao_amount,
                    str(t66_tran_time): t66_yao_amount,
                },
                exx.bob: {str(t55_tran_time): t55_bob_amount},
            },
            exx.yao: {exx.yao: {str(t77_tran_time): t77_yao_amount}},
        },
    }

    # WHEN
    generated_tranbook = get_tranbook_from_dict(str_tran_time_amy23_dict)

    # THEN
    assert generated_tranbook
    assert generated_tranbook.moment_rope == exx.a23
    assert generated_tranbook.tranunits == amy23_tranbook.tranunits
    assert generated_tranbook == amy23_tranbook
