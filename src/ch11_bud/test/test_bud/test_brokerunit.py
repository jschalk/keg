from ch11_bud._ref.ch11_semantic_types import SparkInt
from ch11_bud.bud_main import (
    PersonBudHistory,
    budunit_shop,
    get_personbudhistory_from_dict,
    personbudhistory_shop,
)
from ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_SparkInt_Exists():
    # ESTABLISH / WHEN / THEN
    assert SparkInt(13) == 13
    assert SparkInt(13.5) == 13


def test_PersonBudHistory_Exists():
    # ESTABLISH / WHEN
    x_personbudhistory = PersonBudHistory()

    # THEN
    assert x_personbudhistory
    assert not x_personbudhistory.person_name
    assert not x_personbudhistory.buds
    assert not x_personbudhistory.sum_budunit_quota
    assert not x_personbudhistory.sum_contact_bud_nets
    assert not x_personbudhistory.bud_time_min
    assert not x_personbudhistory.bud_time_max


def test_personbudhistory_shop_ReturnsObj():
    # ESTABLISH

    # WHEN
    x_personbudhistory = personbudhistory_shop(exx.sue)

    # THEN
    assert x_personbudhistory
    assert x_personbudhistory.person_name == exx.sue
    assert x_personbudhistory.buds == {}
    assert not x_personbudhistory.sum_budunit_quota
    assert x_personbudhistory.sum_contact_bud_nets == {}
    assert not x_personbudhistory.bud_time_min
    assert not x_personbudhistory.bud_time_max


def test_PersonBudHistory_set_bud_SetsAttr():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop("sue")
    assert sue_personbudhistory.buds == {}

    # WHEN
    t1_int = 145
    t1_budunit = budunit_shop(t1_int, 0)
    sue_personbudhistory.set_bud(t1_budunit)

    # THEN
    assert sue_personbudhistory.buds != {}
    assert sue_personbudhistory.buds.get(t1_int) == t1_budunit


def test_PersonBudHistory_bud_time_exists_ReturnsObj():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop("Sue")
    t1_int = 145
    assert sue_personbudhistory.bud_time_exists(t1_int) is False

    # WHEN
    t1_budunit = budunit_shop(t1_int, 0)
    sue_personbudhistory.set_bud(t1_budunit)

    # THEN
    assert sue_personbudhistory.bud_time_exists(t1_int)


def test_PersonBudHistory_get_bud_ReturnsObj():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop("sue")
    t1_int = 145
    t1_stat_budunit = budunit_shop(t1_int, 0)
    sue_personbudhistory.set_bud(t1_stat_budunit)

    # WHEN
    t1_gen_budunit = sue_personbudhistory.get_bud(t1_int)

    # THEN
    assert t1_gen_budunit
    assert t1_gen_budunit == t1_stat_budunit


def test_PersonBudHistory_del_bud_SetsAttr():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop("Sue")
    t1_int = 145
    t1_stat_budunit = budunit_shop(t1_int, 0)
    sue_personbudhistory.set_bud(t1_stat_budunit)
    assert sue_personbudhistory.bud_time_exists(t1_int)

    # WHEN
    sue_personbudhistory.del_bud(t1_int)

    # THEN
    assert sue_personbudhistory.bud_time_exists(t1_int) is False


def test_PersonBudHistory_add_bud_SetsAttr():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop("sue")
    assert sue_personbudhistory.buds == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_personbudhistory.add_bud(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_personbudhistory.buds != {}
    t1_budunit = budunit_shop(t1_int, t1_quota)
    assert sue_personbudhistory.buds.get(t1_int) == t1_budunit


def test_PersonBudHistory_add_bud_SetsAttr_celldepth():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop("sue")
    assert sue_personbudhistory.buds == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    t1_celldepth = 3
    sue_personbudhistory.add_bud(t1_int, t1_quota, t1_celldepth)

    # THEN
    assert sue_personbudhistory.buds != {}
    t1_budunit = budunit_shop(t1_int, t1_quota, celldepth=t1_celldepth)
    assert sue_personbudhistory.buds.get(t1_int) == t1_budunit


def test_PersonBudHistory_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)

    # WHEN
    sue_buds_2d_array = sue_personbudhistory.get_2d_array()

    # THEN
    assert sue_buds_2d_array == []


def test_PersonBudHistory_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota)

    # WHEN
    sue_buds_2d_array = sue_personbudhistory.get_2d_array()

    # THEN
    assert sue_buds_2d_array == [
        [exx.sue, x4_bud_time, x4_quota],
        [exx.sue, x7_bud_time, x7_quota],
    ]


def test_PersonBudHistory_get_bud_times_ReturnsObj():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    assert sue_personbudhistory.get_bud_times() == set()

    # WHEN
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota)

    # THEN
    assert sue_personbudhistory.get_bud_times() == {x4_bud_time, x7_bud_time}


def test_PersonBudHistory_get_headers_ReturnsObj():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota)

    # WHEN
    sue_headers_list = sue_personbudhistory.get_headers()

    # THEN
    assert sue_headers_list == [kw.person_name, kw.bud_time, kw.quota]


def test_PersonBudHistory_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    x7_celldepth = 22
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota, celldepth=x7_celldepth)

    # WHEN
    sue_buds_dict = sue_personbudhistory.to_dict()

    # THEN
    assert sue_buds_dict == {
        kw.person_name: exx.sue,
        "buds": {
            x4_bud_time: {kw.quota: x4_quota, kw.bud_time: x4_bud_time},
            x7_bud_time: {
                kw.quota: x7_quota,
                kw.bud_time: x7_bud_time,
                kw.celldepth: x7_celldepth,
            },
        },
    }


def test_get_personbudhistory_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    sue_buds_dict = sue_personbudhistory.to_dict()
    assert sue_buds_dict == {kw.person_name: exx.sue, "buds": {}}

    # WHEN
    x_personbudhistory = get_personbudhistory_from_dict(sue_buds_dict)

    # THEN
    assert x_personbudhistory
    assert x_personbudhistory.person_name == exx.sue
    assert x_personbudhistory.buds == {}
    assert x_personbudhistory.buds == sue_personbudhistory.buds
    assert x_personbudhistory == sue_personbudhistory


def test_get_personbudhistory_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota)
    sue_buds_dict = sue_personbudhistory.to_dict()
    assert sue_buds_dict == {
        kw.person_name: exx.sue,
        "buds": {
            x4_bud_time: {kw.bud_time: x4_bud_time, kw.quota: x4_quota},
            x7_bud_time: {kw.bud_time: x7_bud_time, kw.quota: x7_quota},
        },
    }

    # WHEN
    x_personbudhistory = get_personbudhistory_from_dict(sue_buds_dict)

    # THEN
    assert x_personbudhistory
    assert x_personbudhistory.person_name == exx.sue
    assert x_personbudhistory.get_bud(x4_bud_time) != None
    assert x_personbudhistory.get_bud(x7_bud_time) != None
    assert x_personbudhistory.buds == sue_personbudhistory.buds
    assert x_personbudhistory == sue_personbudhistory


def test_get_personbudhistory_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota)
    zia_bud_contact_net = 887
    sue_bud_contact_net = 445
    sue_personbudhistory.get_bud(x7_bud_time).set_bud_contact_net(
        exx.sue, sue_bud_contact_net
    )
    sue_personbudhistory.get_bud(x7_bud_time).set_bud_contact_net(
        exx.zia, zia_bud_contact_net
    )
    sue_buds_dict = sue_personbudhistory.to_dict()
    assert sue_buds_dict == {
        kw.person_name: exx.sue,
        "buds": {
            x4_bud_time: {kw.bud_time: x4_bud_time, kw.quota: x4_quota},
            x7_bud_time: {
                kw.bud_time: x7_bud_time,
                kw.quota: x7_quota,
                kw.bud_contact_nets: {
                    exx.sue: sue_bud_contact_net,
                    exx.zia: zia_bud_contact_net,
                },
            },
        },
    }

    # WHEN
    x_personbudhistory = get_personbudhistory_from_dict(sue_buds_dict)

    # THEN
    assert x_personbudhistory
    assert x_personbudhistory.person_name == exx.sue
    assert x_personbudhistory.get_bud(x4_bud_time) != None
    assert x_personbudhistory.get_bud(x7_bud_time) != None
    assert x_personbudhistory.get_bud(x7_bud_time).bud_contact_nets != {}
    assert len(x_personbudhistory.get_bud(x7_bud_time).bud_contact_nets) == 2
    assert x_personbudhistory.buds == sue_personbudhistory.buds
    assert x_personbudhistory == sue_personbudhistory


def test_PersonBudHistory_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_personbudhistory = personbudhistory_shop(exx.sue)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_personbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_personbudhistory.add_bud(x7_bud_time, x7_quota)
    zia_bud_contact_net = 887
    bob_bud_contact_net = 445
    sue_personbudhistory.get_bud(x4_bud_time).set_bud_contact_net(
        exx.bob, bob_bud_contact_net
    )
    sue_personbudhistory.get_bud(x7_bud_time).set_bud_contact_net(
        exx.zia, zia_bud_contact_net
    )
    sue_buds_dict = sue_personbudhistory.to_dict()
    assert sue_buds_dict == {
        kw.person_name: exx.sue,
        "buds": {
            x4_bud_time: {
                kw.bud_time: x4_bud_time,
                kw.quota: x4_quota,
                kw.bud_contact_nets: {exx.bob: bob_bud_contact_net},
            },
            x7_bud_time: {
                kw.bud_time: x7_bud_time,
                kw.quota: x7_quota,
                kw.bud_contact_nets: {exx.zia: zia_bud_contact_net},
            },
        },
    }

    # WHEN
    x_moment_rope = "moment_rope_x"
    sue_tranbook = sue_personbudhistory.get_tranbook(x_moment_rope)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.moment_rope == x_moment_rope
    assert sue_tranbook.tranunit_exists(exx.sue, exx.zia, x7_bud_time)
    assert sue_tranbook.tranunit_exists(exx.sue, exx.bob, x4_bud_time)
    assert sue_tranbook.get_amount(exx.sue, exx.zia, x7_bud_time) == zia_bud_contact_net
    assert sue_tranbook.get_amount(exx.sue, exx.bob, x4_bud_time) == bob_bud_contact_net
