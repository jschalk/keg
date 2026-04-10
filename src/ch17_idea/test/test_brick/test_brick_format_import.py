from src.ch04_rope.rope import create_rope
from src.ch07_person_logic.person_main import personunit_shop
from src.ch17_idea.brick_main import get_brickref_obj, save_idea_csv
from src.ch17_idea.idea_config import br00021_person_contactunit_v0_0_0
from src.ch17_idea.idea_db_tool import open_csv
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_open_csv_ReturnsObjWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_contact_cred_lumen = 11
    bob_contact_cred_lumen = 13
    yao_contact_cred_lumen = 41
    sue_contact_debt_lumen = 23
    bob_contact_debt_lumen = 29
    yao_contact_debt_lumen = 37
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    sue_personunit.add_contactunit(
        exx.sue, sue_contact_cred_lumen, sue_contact_debt_lumen
    )
    sue_personunit.add_contactunit(
        exx.bob, bob_contact_cred_lumen, bob_contact_debt_lumen
    )
    sue_personunit.add_contactunit(
        exx.yao, yao_contact_cred_lumen, yao_contact_debt_lumen
    )
    j1_ideaname = br00021_person_contactunit_v0_0_0()
    name_filename = f"{exx.sue}_contact_example_01.csv"
    save_idea_csv(j1_ideaname, sue_personunit, str(temp3_fs), name_filename)

    # WHEN
    contact_dataframe = open_csv(str(temp3_fs), name_filename)

    # THEN
    array_headers = list(contact_dataframe.columns)
    contact_brickref = get_brickref_obj(j1_ideaname)
    assert array_headers == contact_brickref.get_headers_list()
    assert contact_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[0, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[0, kw.contact_name] == exx.bob
    assert contact_dataframe.loc[0, kw.contact_cred_lumen] == bob_contact_cred_lumen
    assert contact_dataframe.loc[0, kw.contact_debt_lumen] == bob_contact_debt_lumen

    assert contact_dataframe.loc[1, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[1, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[1, kw.contact_name] == exx.sue
    assert contact_dataframe.loc[1, kw.contact_cred_lumen] == sue_contact_cred_lumen
    assert contact_dataframe.loc[1, kw.contact_debt_lumen] == sue_contact_debt_lumen

    assert contact_dataframe.loc[2, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[2, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[2, kw.contact_name] == exx.yao
    assert contact_dataframe.loc[2, kw.contact_cred_lumen] == yao_contact_cred_lumen
    assert contact_dataframe.loc[2, kw.contact_debt_lumen] == yao_contact_debt_lumen

    assert len(contact_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(temp3_fs):
    # ESTABLISH
    name_filename = f"{exx.sue}_contact_example_77.csv"

    # WHEN
    contact_dataframe = open_csv(str(temp3_fs), name_filename)

    # THEN
    assert contact_dataframe is None
