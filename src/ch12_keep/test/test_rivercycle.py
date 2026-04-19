from ch01_allot.allot import default_grain_num_if_None
from ch07_person_logic.person_main import personunit_shop
from ch12_keep.rivercycle import (
    RiverCycle,
    create_init_rivercycle,
    create_next_rivercycle,
    create_riverbook,
    get_patientledger,
    rivercycle_shop,
)
from ch12_keep.test._util.ch12_examples import (
    example_bob_patientledger,
    example_yao_patientledger,
    example_zia_patientledger,
)
from ref.keywords import Ch12Keywords as wk, ExampleStrs as exx


def test_RiverCylce_Exists():
    # ESTABLISH / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert not x_rivercycle.healer_name
    assert not x_rivercycle.number
    assert not x_rivercycle.keep_patientledgers
    assert not x_rivercycle.riverbooks
    assert set(x_rivercycle.__dict__.keys()) == {
        wk.healer_name,
        "number",
        wk.keep_patientledgers,
        wk.riverbooks,
        wk.mana_grain,
    }


def test_rivercycle_shop_ReturnsObj_Scenario0_SomeParametersNotPassed():
    # ESTABLISH
    one_int = 1

    # WHEN
    one_rivercycle = rivercycle_shop(exx.yao, one_int)

    # THEN
    assert one_rivercycle.healer_name == exx.yao
    assert one_rivercycle.number == 1
    assert one_rivercycle.keep_patientledgers == {}
    assert one_rivercycle.riverbooks == {}
    assert one_rivercycle.mana_grain == default_grain_num_if_None()


def test_rivercycle_shop_ReturnsObj_Scenario1_ParametersPassed():
    # ESTABLISH
    one_int = 1
    yao_mana_grain = 4

    # WHEN
    one_rivercycle = rivercycle_shop(exx.yao, one_int, mana_grain=yao_mana_grain)

    # THEN
    assert one_rivercycle.healer_name == exx.yao
    assert one_rivercycle.number == 1
    assert one_rivercycle.keep_patientledgers == {}
    assert one_rivercycle.riverbooks == {}
    assert one_rivercycle.mana_grain == yao_mana_grain


def test_RiverCylce_set_complete_riverbook_SetsAttr():
    # ESTABLISH
    one_int = 1
    one_rivercycle = rivercycle_shop(exx.yao, one_int)
    bob_book_point_amount = 555
    bob_riverbook = create_riverbook(exx.bob, {}, bob_book_point_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle._set_complete_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {exx.bob: bob_riverbook}


def test_RiverCylce_set_riverbook_SetsAttr():
    # ESTABLISH
    one_int = 1
    keep_patientledger = {exx.bob: {exx.yao: 75, exx.bob: 25}}
    one_rivercycle = rivercycle_shop(exx.yao, one_int, keep_patientledger)
    bob_book_point_amount = 500
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(exx.bob, bob_book_point_amount)

    # THEN
    bob_patientledger = keep_patientledger.get(exx.bob)
    bob_riverbook = create_riverbook(exx.bob, bob_patientledger, bob_book_point_amount)
    assert one_rivercycle.riverbooks == {exx.bob: bob_riverbook}


def test_RiverCylce_create_cylceledger_ReturnsObjOneRiverBook():
    # ESTABLISH
    one_int = 1
    yao_patientledger = {exx.yao: {exx.yao: 334.0}}
    one_rivercycle = rivercycle_shop(exx.yao, one_int, yao_patientledger)
    book_point_amount = 450
    one_rivercycle.set_riverbook(exx.yao, book_point_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    assert one_cylceledger == {exx.yao: book_point_amount}


def test_RiverCylce_create_cylceledger_ReturnsObjTwoRiverBooks():
    # ESTABLISH
    one_int = 1
    keep_patientledgers = {
        exx.yao: {exx.yao: 75, exx.bob: 25},
        exx.bob: {exx.yao: 49, exx.bob: 51},
    }
    one_rivercycle = rivercycle_shop(exx.yao, one_int, keep_patientledgers)
    yao_book_point_amount = 500
    bob_book_point_amount = 100000
    one_rivercycle.set_riverbook(exx.yao, yao_book_point_amount)
    one_rivercycle.set_riverbook(exx.bob, bob_book_point_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    yao_mana = (yao_book_point_amount * 0.75) + (bob_book_point_amount * 0.49)
    bob_mana = (yao_book_point_amount * 0.25) + (bob_book_point_amount * 0.51)
    assert one_cylceledger == {exx.yao: yao_mana, exx.bob: bob_mana}


def test_create_init_rivercycle_ReturnsObj_Scenario1_contactunit():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao)
    yao_patientledger = get_patientledger(yao_person)
    keep_patientledgers = {exx.yao: yao_patientledger}
    keep_magnitude = 1200

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(
        exx.yao, keep_patientledgers, keep_magnitude
    )

    # THEN
    assert yao_init_rivercycle.healer_name == exx.yao
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(exx.yao) is not None


def test_create_init_rivercycle_ReturnsObj_Scenario2_magnitude_Default():
    # ESTABLISH
    yao_contact_cred_lumen = 7
    bob_contact_cred_lumen = 3
    zia_contact_cred_lumen = 10
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao, yao_contact_cred_lumen)
    yao_person.add_contactunit(exx.bob, bob_contact_cred_lumen)
    yao_person.add_contactunit(exx.zia, zia_contact_cred_lumen)
    yao_patientledger = get_patientledger(yao_person)
    keep_patientledgers = {exx.yao: yao_patientledger}
    print(f"{keep_patientledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(exx.yao, keep_patientledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(exx.yao)
    assert yao_riverbook is not None
    assert len(yao_riverbook.rivercares) == 3
    assert yao_riverbook.rivercares.get(exx.yao) == 350000000
    assert yao_riverbook.rivercares.get(exx.bob) == 150000000
    assert yao_riverbook.rivercares.get(exx.zia) == 500000000


def test_create_init_rivercycle_ReturnsObj_Scenario3_contactunit():
    # ESTABLISH
    yao_contact_cred_lumen = 7
    bob_contact_cred_lumen = 3
    zia_contact_cred_lumen = 10
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao, yao_contact_cred_lumen)
    yao_person.add_contactunit(exx.bob, bob_contact_cred_lumen)
    yao_person.add_contactunit(exx.zia, zia_contact_cred_lumen)
    yao_patientledger = get_patientledger(yao_person)
    keep_patientledgers = {exx.yao: yao_patientledger}
    print(f"{keep_patientledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(
        exx.yao, keep_patientledgers, keep_point_magnitude=1001
    )

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(exx.yao)
    assert yao_riverbook is not None
    assert len(yao_riverbook.rivercares) == 3
    assert yao_riverbook.rivercares.get(exx.yao) == 350
    assert yao_riverbook.rivercares.get(exx.bob) == 150
    assert yao_riverbook.rivercares.get(exx.zia) == 501


def test_create_next_rivercycle_ReturnsObj_ScenarioThree_contactunit():
    # ESTABLISH
    yao_patientledger = example_yao_patientledger()
    bob_patientledger = example_bob_patientledger()
    zia_patientledger = example_zia_patientledger()
    keep_patientledgers = {
        exx.yao: yao_patientledger,
        exx.bob: bob_patientledger,
        exx.zia: zia_patientledger,
    }
    print(f"{keep_patientledgers=}")
    init_rivercycle = create_init_rivercycle(exx.yao, keep_patientledgers)
    init_cycleledger = init_rivercycle.create_cylceledger()
    print(f"{init_cycleledger=}")

    # WHEN
    next_rivercycle = create_next_rivercycle(init_rivercycle, init_cycleledger)

    # THEN
    assert next_rivercycle.number == init_rivercycle.number + 1
    assert len(next_rivercycle.riverbooks) == 3
    yao_riverbook = next_rivercycle.riverbooks.get(exx.yao)
    bob_riverbook = next_rivercycle.riverbooks.get(exx.bob)
    zia_riverbook = next_rivercycle.riverbooks.get(exx.zia)
    assert yao_riverbook is not None
    assert bob_riverbook is not None
    assert zia_riverbook is not None
    assert len(yao_riverbook.rivercares) == 3
    assert yao_riverbook.rivercares.get(exx.yao) == 122500000
    assert yao_riverbook.rivercares.get(exx.bob) == 52500000
    assert yao_riverbook.rivercares.get(exx.zia) == 175000000
    assert bob_riverbook.rivercares.get(exx.yao) == 3000000
    assert bob_riverbook.rivercares.get(exx.bob) == 21000000
    assert bob_riverbook.rivercares.get(exx.zia) == 126000000
    assert zia_riverbook.rivercares.get(exx.yao) == 148333333
    assert zia_riverbook.rivercares.get(exx.bob) == 250000000
    assert zia_riverbook.rivercares.get(exx.zia) == 101666667

    assert sum(zia_riverbook.rivercares.values()) == init_cycleledger.get(exx.zia)
    assert sum(bob_riverbook.rivercares.values()) == init_cycleledger.get(exx.bob)
    assert sum(yao_riverbook.rivercares.values()) == init_cycleledger.get(exx.yao)


def test_create_next_rivercycle_ReturnsObjDoesNotReference_cycleledger_From_prev_rivercycle():
    # ESTABLISH
    yao_patientledger = example_yao_patientledger()
    bob_patientledger = example_bob_patientledger()
    zia_patientledger = example_zia_patientledger()
    keep_patientledgers = {
        exx.yao: yao_patientledger,
        exx.bob: bob_patientledger,
        exx.zia: zia_patientledger,
    }
    print(f"{keep_patientledgers=}")
    init_rivercycle = create_init_rivercycle(exx.yao, keep_patientledgers)
    init_cycleledger = init_rivercycle.create_cylceledger()
    print(f"{init_cycleledger=}")
    init_cycleledger[exx.bob] = init_cycleledger.get(exx.bob) - 500000

    # WHEN
    next_rivercycle = create_next_rivercycle(init_rivercycle, init_cycleledger)

    # THEN
    assert next_rivercycle.number == init_rivercycle.number + 1
    assert len(next_rivercycle.riverbooks) == 3
    yao_riverbook = next_rivercycle.riverbooks.get(exx.yao)
    bob_riverbook = next_rivercycle.riverbooks.get(exx.bob)
    zia_riverbook = next_rivercycle.riverbooks.get(exx.zia)
    assert yao_riverbook is not None
    assert bob_riverbook is not None
    assert zia_riverbook is not None
    assert len(yao_riverbook.rivercares) == 3
    assert yao_riverbook.rivercares.get(exx.yao) == 122500000
    assert yao_riverbook.rivercares.get(exx.bob) == 52500000
    assert yao_riverbook.rivercares.get(exx.zia) == 175000000

    assert bob_riverbook.rivercares.get(exx.yao) != 3000000
    assert bob_riverbook.rivercares.get(exx.yao) == 2990000
    assert bob_riverbook.rivercares.get(exx.bob) != 21000000
    assert bob_riverbook.rivercares.get(exx.bob) == 20930000
    assert bob_riverbook.rivercares.get(exx.zia) != 126000000
    assert bob_riverbook.rivercares.get(exx.zia) == 125580000

    assert zia_riverbook.rivercares.get(exx.yao) == 148333333
    assert zia_riverbook.rivercares.get(exx.bob) == 250000000
    assert zia_riverbook.rivercares.get(exx.zia) == 101666667

    assert sum(zia_riverbook.rivercares.values()) == init_cycleledger.get(exx.zia)
    assert sum(bob_riverbook.rivercares.values()) == init_cycleledger.get(exx.bob)
    assert sum(yao_riverbook.rivercares.values()) == init_cycleledger.get(exx.yao)
