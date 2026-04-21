from ch07_person_logic.person_main import personunit_shop
from ch07_person_logic.person_tool import (
    get_contact_agenda_net_ledger,
    get_contact_mandate_ledger,
    get_credit_ledger,
    get_person_contact_agenda_award_array,
    get_person_contact_agenda_award_csv,
)
from ref.keywords import ExampleStrs as exx


def test_get_person_contact_agenda_award_array_ReturnsObj_ScenarioZeroContactUnits():
    # ESTABLISH
    sue_person = personunit_shop("Sue")

    # WHEN / THEN
    assert get_person_contact_agenda_award_array(sue_person) == []


def test_get_person_contact_agenda_award_array_ReturnsObj_ScenarioSingleContactUnit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)

    # WHEN / THEN
    assert len(get_person_contact_agenda_award_array(sue_person)) == 1


def test_get_person_contact_agenda_award_array_ReturnsObj_ScenarioMultipleContactUnit():
    # ESTABLISH
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    sue_person.add_contactunit(exx.zia)
    sue_person.get_contact(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_person.get_contact(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_person.get_contact(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_person.get_contact(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    person_contact_agenda_award_array = get_person_contact_agenda_award_array(
        sue_person
    )

    # THEN
    assert len(person_contact_agenda_award_array) == 3
    assert person_contact_agenda_award_array[0][0] == exx.bob
    assert person_contact_agenda_award_array[1][0] == exx.yao
    assert person_contact_agenda_award_array[2][0] == exx.zia
    assert len(person_contact_agenda_award_array[0]) == 3
    assert len(person_contact_agenda_award_array[1]) == 3
    assert len(person_contact_agenda_award_array[2]) == 3
    assert person_contact_agenda_award_array[0][1] == bob_fund_agenda_take
    assert person_contact_agenda_award_array[0][2] == bob_fund_agenda_give
    assert person_contact_agenda_award_array[1][1] == yao_fund_agenda_take
    assert person_contact_agenda_award_array[1][2] == yao_fund_agenda_give


def test_get_person_contact_agenda_award_csv_ReturnsObj_ScenarioMultipleContactUnit():
    # ESTABLISH
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    sue_person.add_contactunit(exx.zia)
    sue_person.get_contact(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_person.get_contact(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_person.get_contact(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_person.get_contact(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    person_contact_agenda_award_csv_str = get_person_contact_agenda_award_csv(
        sue_person
    )

    # THEN
    print(f"{person_contact_agenda_award_csv_str=}")
    print("")
    example_csv_str = f"""contact_name,fund_agenda_take,fund_agenda_give
{exx.bob},{bob_fund_agenda_take},{bob_fund_agenda_give}
{exx.yao},{yao_fund_agenda_take},{yao_fund_agenda_give}
{exx.zia},0,0
"""
    print(f"{example_csv_str=}")
    assert person_contact_agenda_award_csv_str == example_csv_str


def test_get_person_contact_agenda_award_csv_ReturnsObj_thinkout_True():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    sue_person.add_contactunit(exx.xio)
    sue_person.add_contactunit(exx.zia)
    empty_contact_agenda_award = f"""contact_name,fund_agenda_take,fund_agenda_give
{exx.bob},0,0
{exx.xio},0,0
{exx.yao},0,0
{exx.zia},0,0
"""
    assert empty_contact_agenda_award == get_person_contact_agenda_award_csv(sue_person)

    # WHEN
    person_contact_agenda_award_csv_str = get_person_contact_agenda_award_csv(
        sue_person, thinkout=True
    )

    # THEN
    print(f"{person_contact_agenda_award_csv_str=}")
    print("")
    q_fund_agenda_give = int(sue_person.fund_pool * 0.25)
    q_fund_agenda_take = int(sue_person.fund_pool * 0.25)
    example_csv_str = f"""contact_name,fund_agenda_take,fund_agenda_give
{exx.bob},{q_fund_agenda_take},{q_fund_agenda_give}
{exx.xio},{q_fund_agenda_take},{q_fund_agenda_give}
{exx.yao},{q_fund_agenda_take},{q_fund_agenda_give}
{exx.zia},{q_fund_agenda_take},{q_fund_agenda_give}
"""
    print(f"{example_csv_str=}")
    assert person_contact_agenda_award_csv_str == example_csv_str


def test_get_contact_mandate_ledger_ReturnsObj_Scenario0_MultipleContactUnit():
    # ESTABLISH
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_person = personunit_shop("Sue", fund_pool=200)
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    sue_person.add_contactunit(exx.zia)
    sue_person.get_contact(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_person.get_contact(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_person.get_contact(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_person.get_contact(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    person_bud_net_dict = get_contact_mandate_ledger(sue_person)

    # THEN
    print(f"{person_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.bob: 58,
        exx.yao: 142,
        exx.zia: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == person_bud_net_dict


def test_get_contact_mandate_ledger_ReturnsObj_Scenario1_thinkout_True():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao, 13, 5)
    sue_person.add_contactunit(exx.bob, 5, 7)
    sue_person.add_contactunit(exx.xio, 2, 3)
    sue_person.add_contactunit(exx.zia, 0, 0)
    pool4th = sue_person.fund_pool / 4
    pre_settle_contact_mandate_ledger = {
        exx.bob: pool4th,
        exx.xio: pool4th,
        exx.yao: pool4th,
        exx.zia: pool4th,
    }
    assert get_contact_mandate_ledger(sue_person) == pre_settle_contact_mandate_ledger

    # WHEN
    sue_person_settle_net_dict = get_contact_mandate_ledger(sue_person, thinkout=True)

    # THEN
    assert sue_person_settle_net_dict != pre_settle_contact_mandate_ledger
    print(f"{sue_person_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.yao: 650000000,
        exx.bob: 250000000,
        exx.xio: 100000000,
        exx.zia: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_person_settle_net_dict.get(exx.yao) != None
    assert sue_person_settle_net_dict.get(exx.bob) != None
    assert sue_person_settle_net_dict.get(exx.xio) != None
    assert sue_person_settle_net_dict.get(exx.zia) != None
    assert sue_person_settle_net_dict == example_bud_net_dict


def test_get_contact_mandate_ledger_ReturnsObj_Scenario2_No_contactunits():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    empty_contact_mandate_ledger = {exx.sue: sue_person.fund_pool}

    # WHEN / THEN
    assert get_contact_mandate_ledger(sue_person) == empty_contact_mandate_ledger


def test_get_contact_mandate_ledger_ReturnsObj_Scenario3_No_personunit():
    # ESTABLISH / WHEN / THEN
    assert get_contact_mandate_ledger(None) == {}


def test_get_contact_mandate_ledger_ReturnsObj_Scenario4_MandateSumEqual_fund_pool():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao, 13, 5)
    sue_person.add_contactunit(exx.bob, 5, 7)
    sue_person.add_contactunit(exx.xio, 2, 3)
    sue_person.add_contactunit(exx.zia, 0, 0)
    pool4th = sue_person.fund_pool / 4
    pre_settle_contact_mandate_ledger = {
        exx.bob: pool4th,
        exx.xio: pool4th,
        exx.yao: pool4th,
        exx.zia: pool4th,
    }
    assert get_contact_mandate_ledger(sue_person) == pre_settle_contact_mandate_ledger

    # WHEN
    sue_person_settle_net_dict = get_contact_mandate_ledger(sue_person, thinkout=True)

    # THEN
    assert sue_person_settle_net_dict != pre_settle_contact_mandate_ledger
    print(f"{sue_person_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.yao: 650000000,
        exx.bob: 250000000,
        exx.xio: 100000000,
        exx.zia: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_person_settle_net_dict.get(exx.yao) != None
    assert sue_person_settle_net_dict.get(exx.bob) != None
    assert sue_person_settle_net_dict.get(exx.xio) != None
    assert sue_person_settle_net_dict.get(exx.zia) != None
    assert sue_person_settle_net_dict == example_bud_net_dict


def test_get_contact_mandate_ledger_ReturnsObj_Scenario5_Zero_fund_agenda_give():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_fund_pool = 800
    sue_person.set_fund_pool(sue_fund_pool)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = sue_person.make_l1_rope(exx.casa)
    floor_rope = sue_person.make_rope(casa_rope, floor_str)
    clean_rope = sue_person.make_rope(floor_rope, exx.clean)
    dirty_rope = sue_person.make_rope(floor_rope, dirty_str)
    mop_rope = sue_person.make_rope(casa_rope, exx.mop)
    sue_person.add_plan(floor_rope)
    sue_person.add_plan(clean_rope)
    sue_person.add_plan(dirty_rope)
    sue_person.add_plan(mop_rope, pledge=True)
    sue_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    sue_person.add_contactunit(exx.yao, 13, 5)

    # WHEN
    sue_person_settle_net_dict = get_contact_mandate_ledger(sue_person, thinkout=True)

    # THEN
    assert sue_person_settle_net_dict == {exx.yao: sue_fund_pool}


def test_get_contact_agenda_net_ledger_ReturnsObj_ScenarioMultipleContactUnit():
    # ESTABLISH
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao)
    sue_person.add_contactunit(exx.bob)
    sue_person.add_contactunit(exx.zia)
    sue_person.get_contact(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_person.get_contact(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_person.get_contact(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_person.get_contact(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    person_bud_net_dict = get_contact_agenda_net_ledger(sue_person)

    # THEN
    print(f"{person_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.bob: bob_fund_agenda_give - bob_fund_agenda_take,
        exx.yao: yao_fund_agenda_give - yao_fund_agenda_take,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == person_bud_net_dict


def test_get_contact_agenda_net_ledger_ReturnsObj_thinkout_True():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_contactunit(exx.yao, 13, 5)
    sue_person.add_contactunit(exx.bob, 5, 7)
    sue_person.add_contactunit(exx.xio, 2, 3)
    sue_person.add_contactunit(exx.zia, 0, 0)
    assert get_contact_agenda_net_ledger(sue_person) == {}

    # WHEN
    sue_person_settle_net_dict = get_contact_agenda_net_ledger(
        sue_person, thinkout=True
    )

    # THEN
    print(f"{sue_person_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.bob: -216666667,
        exx.yao: 316666667,
        exx.xio: -100000000,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_person_settle_net_dict.get(exx.yao) != None
    assert sue_person_settle_net_dict.get(exx.bob) != None
    assert sue_person_settle_net_dict.get(exx.xio) != None
    assert sue_person_settle_net_dict.get(exx.zia) is None
    assert sue_person_settle_net_dict == example_bud_net_dict


def test_get_credit_ledger_ReturnsObj_Scenario0_No_contactunits():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    # WHEN / THEN
    assert get_credit_ledger(sue_person) == {}


def test_get_credit_ledger_ReturnsObj_Scenario1_contactunits_Exist():
    # ESTABLISH
    sue_person = personunit_shop(exx.sue)
    bob_contact_cred_lumen = 11
    yao_contact_cred_lumen = 13
    xio_contact_cred_lumen = 17
    sue_person.add_contactunit(exx.yao, yao_contact_cred_lumen)
    sue_person.add_contactunit(exx.bob, bob_contact_cred_lumen)
    sue_person.add_contactunit(exx.xio, xio_contact_cred_lumen)

    # WHEN
    sue_credit_ledger = get_credit_ledger(sue_person)

    # THEN
    print(f"{sue_credit_ledger=}")
    print("")
    expected_sue_credit_ledger = {
        exx.bob: bob_contact_cred_lumen,
        exx.yao: yao_contact_cred_lumen,
        exx.xio: xio_contact_cred_lumen,
    }
    print(f"{expected_sue_credit_ledger=}")
    assert sue_credit_ledger.get(exx.yao) != None
    assert sue_credit_ledger.get(exx.bob) != None
    assert sue_credit_ledger.get(exx.xio) != None
    assert sue_credit_ledger.get(exx.zia) is None
    assert sue_credit_ledger == expected_sue_credit_ledger
