from src.ch04_rope.rope import create_rope
from src.ch07_person_logic.person_main import personunit_shop
from src.ch17_idea.idea_config import idea_format_00021_person_partnerunit_v0_0_0
from src.ch17_idea.idea_db_tool import open_csv
from src.ch17_idea.idea_main import get_idearef_obj, save_idea_csv
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_open_csv_ReturnsObjWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_partner_cred_lumen = 11
    bob_partner_cred_lumen = 13
    yao_partner_cred_lumen = 41
    sue_partner_debt_lumen = 23
    bob_partner_debt_lumen = 29
    yao_partner_debt_lumen = 37
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    sue_personunit.add_partnerunit(
        exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen
    )
    sue_personunit.add_partnerunit(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    sue_personunit.add_partnerunit(
        exx.yao, yao_partner_cred_lumen, yao_partner_debt_lumen
    )
    j1_ideaname = idea_format_00021_person_partnerunit_v0_0_0()
    name_filename = f"{exx.sue}_partner_example_01.csv"
    save_idea_csv(j1_ideaname, sue_personunit, str(temp3_fs), name_filename)

    # WHEN
    partner_dataframe = open_csv(str(temp3_fs), name_filename)

    # THEN
    array_headers = list(partner_dataframe.columns)
    partner_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == partner_idearef.get_headers_list()
    assert partner_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert partner_dataframe.loc[0, kw.person_name] == sue_personunit.person_name
    assert partner_dataframe.loc[0, kw.partner_name] == exx.bob
    assert partner_dataframe.loc[0, kw.partner_cred_lumen] == bob_partner_cred_lumen
    assert partner_dataframe.loc[0, kw.partner_debt_lumen] == bob_partner_debt_lumen

    assert partner_dataframe.loc[1, kw.moment_rope] == amy_moment_rope
    assert partner_dataframe.loc[1, kw.person_name] == sue_personunit.person_name
    assert partner_dataframe.loc[1, kw.partner_name] == exx.sue
    assert partner_dataframe.loc[1, kw.partner_cred_lumen] == sue_partner_cred_lumen
    assert partner_dataframe.loc[1, kw.partner_debt_lumen] == sue_partner_debt_lumen

    assert partner_dataframe.loc[2, kw.moment_rope] == amy_moment_rope
    assert partner_dataframe.loc[2, kw.person_name] == sue_personunit.person_name
    assert partner_dataframe.loc[2, kw.partner_name] == exx.yao
    assert partner_dataframe.loc[2, kw.partner_cred_lumen] == yao_partner_cred_lumen
    assert partner_dataframe.loc[2, kw.partner_debt_lumen] == yao_partner_debt_lumen

    assert len(partner_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(temp3_fs):
    # ESTABLISH
    name_filename = f"{exx.sue}_partner_example_77.csv"

    # WHEN
    partner_dataframe = open_csv(str(temp3_fs), name_filename)

    # THEN
    assert partner_dataframe is None
