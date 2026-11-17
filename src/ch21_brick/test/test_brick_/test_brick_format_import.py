from ch05_rope.rope import create_rope
from ch08_person_logic.person_main import personunit_shop
from ch21_brick.brick_config import BrickFormatsEnum
from ch21_brick.brick_dataframe import get_brickref_obj, save_brick_csv
from ch21_brick.brick_db_tool import open_csv
from ch99_glossary.ch_keyword import Ch21Keywords as kw, ExampleStrs as exx


def test_open_csv_ReturnsObjWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_contact_cred_mass = 11
    bob_contact_cred_mass = 13
    yao_contact_cred_mass = 41
    sue_contact_debt_mass = 23
    bob_contact_debt_mass = 29
    yao_contact_debt_mass = 37
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    sue_personunit.add_contactunit(
        exx.sue, sue_contact_cred_mass, sue_contact_debt_mass
    )
    sue_personunit.add_contactunit(
        exx.bob, bob_contact_cred_mass, bob_contact_debt_mass
    )
    sue_personunit.add_contactunit(
        exx.yao, yao_contact_cred_mass, yao_contact_debt_mass
    )
    j1_brickname = BrickFormatsEnum.bk00121_person_contactunit_v0_0_0
    name_filename = f"{exx.sue}_contact_example_01.csv"
    save_brick_csv(j1_brickname, sue_personunit, str(temp3_fs), name_filename)

    # WHEN
    contact_dataframe = open_csv(str(temp3_fs), name_filename)

    # THEN
    array_headers = list(contact_dataframe.columns)
    contact_brickref = get_brickref_obj(j1_brickname)
    assert array_headers == contact_brickref.get_headers_list()
    assert contact_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[0, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[0, kw.contact_name] == exx.bob
    assert contact_dataframe.loc[0, kw.contact_cred_mass] == bob_contact_cred_mass
    assert contact_dataframe.loc[0, kw.contact_debt_mass] == bob_contact_debt_mass

    assert contact_dataframe.loc[1, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[1, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[1, kw.contact_name] == exx.sue
    assert contact_dataframe.loc[1, kw.contact_cred_mass] == sue_contact_cred_mass
    assert contact_dataframe.loc[1, kw.contact_debt_mass] == sue_contact_debt_mass

    assert contact_dataframe.loc[2, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[2, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[2, kw.contact_name] == exx.yao
    assert contact_dataframe.loc[2, kw.contact_cred_mass] == yao_contact_cred_mass
    assert contact_dataframe.loc[2, kw.contact_debt_mass] == yao_contact_debt_mass

    assert len(contact_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(temp3_fs):
    # ESTABLISH
    name_filename = f"{exx.sue}_contact_example_77.csv"

    # WHEN
    contact_dataframe = open_csv(str(temp3_fs), name_filename)

    # THEN
    assert contact_dataframe is None
