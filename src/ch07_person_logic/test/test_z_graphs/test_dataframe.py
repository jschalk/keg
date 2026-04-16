from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.person_report import (
    get_person_agenda_dataframe,
    get_person_contactunits_dataframe,
)
from src.ch07_person_logic.test._util.ch07_examples import (
    personunit_v001_with_large_agenda,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_get_person_contactunits_dataframe_ReturnsDataFrame():
    # ESTABLISH
    luca_person = personunit_shop()
    luca_person.set_credor_respect(500)
    luca_person.set_debtor_respect(400)
    yao_contact_cred_lumen = 66
    yao_contact_debt_lumen = 77
    luca_person.add_contactunit(exx.yao, yao_contact_cred_lumen, yao_contact_debt_lumen)
    sue_contact_cred_lumen = 434
    sue_contact_debt_lumen = 323
    luca_person.add_contactunit(exx.sue, sue_contact_cred_lumen, sue_contact_debt_lumen)

    # WHEN
    x_df = get_person_contactunits_dataframe(luca_person)

    # THEN
    contactunit_colums = {
        kw.contact_name,
        "contact_cred_lumen",
        "contact_debt_lumen",
        "memberships",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == contactunit_colums
    assert x_df.shape[0] == 2


def test_get_person_contactunits_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    luca_person = personunit_shop()

    # WHEN
    x_df = get_person_contactunits_dataframe(luca_person)

    # THEN
    contactunit_colums = {
        kw.contact_name,
        "contact_cred_lumen",
        "contact_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == contactunit_colums
    assert x_df.shape[0] == 0


def test_get_person_agenda_dataframe_ReturnsDataFrame():
    # ESTABLISH
    yao_person = personunit_v001_with_large_agenda()
    assert len(yao_person.get_agenda_dict()) == 69

    # WHEN
    x_df = get_person_agenda_dataframe(yao_person)
    print(x_df)

    # THEN
    contactunit_colums = {
        kw.person_name,
        "fund_ratio",
        kw.plan_label,
        kw.parent_rope,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == contactunit_colums
    assert x_df.shape[0] == 69


def test_get_person_agenda_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    yao_person = personunit_shop(exx.yao)
    assert len(yao_person.get_agenda_dict()) == 0

    # WHEN
    x_df = get_person_agenda_dataframe(yao_person)
    print(x_df)

    # THEN
    contactunit_colums = {
        kw.person_name,
        "fund_ratio",
        kw.plan_label,
        kw.parent_rope,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == contactunit_colums
