from src.ch01_allot.allot import default_grain_num_if_None
from src.ch07_person_logic.person_main import personunit_shop
from src.ch12_keep.rivercycle import (
    RiverBook,
    create_riverbook,
    get_patientledger,
    riverbook_shop,
)
from src.ref.keywords import Ch12Keywords as kw, ExampleStrs as exx


def test_RiverBook_Exists():
    # ESTABLISH / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert not x_riverbook.person_name
    assert not x_riverbook.rivercares
    assert not x_riverbook.mana_grain
    assert set(x_riverbook.__dict__.keys()) == {
        kw.person_name,
        kw.rivercares,
        kw.mana_grain,
    }


def test_riverbook_shop_ReturnsObj_Scenario0_mana_grain_IsNone():
    # ESTABLISH

    # WHEN
    bob_riverbook = riverbook_shop(exx.bob)

    # THEN
    assert bob_riverbook.person_name == exx.bob
    assert bob_riverbook.rivercares == {}
    assert bob_riverbook.mana_grain == default_grain_num_if_None()


def test_riverbook_shop_ReturnsObj_Scenario1_mana_grain_Exists():
    # ESTABLISH
    bob_mana_grain = 3
    assert bob_mana_grain != default_grain_num_if_None()

    # WHEN
    bob_riverbook = riverbook_shop(exx.bob, bob_mana_grain)

    # THEN
    assert bob_riverbook.person_name == exx.bob
    assert bob_riverbook.rivercares == {}
    assert bob_riverbook.mana_grain == bob_mana_grain


def test_create_riverbook_ReturnsObj_Scenario0_mana_grain_IsNone():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao)
    yao_person.add_contactunit(exx.sue)
    yao_book_point_amount = 500
    yao_patientledger = get_patientledger(yao_person)

    # WHEN
    yao_riverbook = create_riverbook(exx.yao, yao_patientledger, yao_book_point_amount)

    # THEN
    assert yao_riverbook.person_name == exx.yao
    assert yao_riverbook.rivercares == {exx.yao: 250, exx.sue: 250}
    assert sum(yao_riverbook.rivercares.values()) == yao_book_point_amount
    assert yao_riverbook.mana_grain == default_grain_num_if_None()


def test_create_riverbook_ReturnsObj_Scenario1_mana_grain_ArgPassed():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao)
    yao_person.add_contactunit(exx.sue)
    yao_book_point_amount = 500
    yao_patientledger = get_patientledger(yao_person)
    yao_mana_grain = 4

    # WHEN
    yao_riverbook = create_riverbook(
        exx.yao, yao_patientledger, yao_book_point_amount, yao_mana_grain
    )

    # THEN
    assert yao_riverbook.person_name == exx.yao
    assert yao_riverbook.rivercares == {exx.yao: 248, exx.sue: 252}
    assert sum(yao_riverbook.rivercares.values()) == yao_book_point_amount
    assert yao_riverbook.mana_grain == yao_mana_grain
