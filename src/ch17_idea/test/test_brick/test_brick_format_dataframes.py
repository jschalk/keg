from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch04_rope.rope import create_rope
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.test._util.ch13_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
)
from src.ch17_idea.brick_main import create_brick_df, get_brickref_obj, save_idea_csv
from src.ch17_idea.idea_config import (
    br00013_planunit_v0_0_0,
    br00019_planunit_v0_0_0,
    br00020_person_contact_membership_v0_0_0,
    br00021_person_contactunit_v0_0_0,
)
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_create_brick_df_Arg_br00021_person_contactunit_v0_0_0():
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

    # WHEN
    x_brick_name = br00021_person_contactunit_v0_0_0()
    contact_dataframe = create_brick_df(sue_personunit, x_brick_name)

    # THEN
    array_headers = list(contact_dataframe.columns)
    contact_brickref = get_brickref_obj(x_brick_name)
    assert array_headers == contact_brickref.get_headers_list()
    assert contact_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[0, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[0, kw.contact_name] == exx.bob
    assert contact_dataframe.loc[0, kw.contact_debt_lumen] == bob_contact_debt_lumen
    assert contact_dataframe.loc[0, kw.contact_cred_lumen] == bob_contact_cred_lumen

    assert contact_dataframe.loc[1, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[1, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[1, kw.contact_name] == exx.sue
    assert contact_dataframe.loc[1, kw.contact_debt_lumen] == sue_contact_debt_lumen
    assert contact_dataframe.loc[1, kw.contact_cred_lumen] == sue_contact_cred_lumen

    assert contact_dataframe.loc[2, kw.moment_rope] == amy_moment_rope
    assert contact_dataframe.loc[2, kw.person_name] == sue_personunit.person_name
    assert contact_dataframe.loc[2, kw.contact_name] == exx.yao
    assert contact_dataframe.loc[2, kw.contact_debt_lumen] == yao_contact_debt_lumen
    assert contact_dataframe.loc[2, kw.contact_cred_lumen] == yao_contact_cred_lumen

    assert len(contact_dataframe) == 3


def test_create_brick_df_Arg_br00020_person_contact_membership_v0_0_0():
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    sue_personunit.add_contactunit(exx.sue)
    sue_personunit.add_contactunit(exx.bob)
    sue_personunit.add_contactunit(exx.yao)
    iowa_str = ";Iowa"
    sue_iowa_credit_w = 37
    bob_iowa_credit_w = 43
    yao_iowa_credit_w = 51
    sue_iowa_debt_w = 57
    bob_iowa_debt_w = 61
    yao_iowa_debt_w = 67
    ohio_str = ";Ohio"
    yao_ohio_credit_w = 73
    yao_ohio_debt_w = 67
    sue_contactunit = sue_personunit.get_contact(exx.sue)
    bob_contactunit = sue_personunit.get_contact(exx.bob)
    yao_contactunit = sue_personunit.get_contact(exx.yao)
    sue_contactunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debt_w)
    bob_contactunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debt_w)
    yao_contactunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debt_w)
    yao_contactunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debt_w)

    # WHEN
    x_brick_name = br00020_person_contact_membership_v0_0_0()
    membership_dataframe = create_brick_df(sue_personunit, x_brick_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    contact_brickref = get_brickref_obj(x_brick_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == contact_brickref.get_headers_list()
    assert membership_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[0, kw.person_name] == sue_personunit.person_name
    assert membership_dataframe.loc[0, kw.contact_name] == exx.bob
    assert membership_dataframe.loc[0, kw.group_title] == iowa_str
    assert membership_dataframe.loc[0, kw.group_cred_lumen] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, kw.group_debt_lumen] == bob_iowa_debt_w

    assert membership_dataframe.loc[3, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[3, kw.person_name] == sue_personunit.person_name
    assert membership_dataframe.loc[3, kw.contact_name] == exx.sue
    assert membership_dataframe.loc[3, kw.group_title] == iowa_str
    assert membership_dataframe.loc[3, kw.group_cred_lumen] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, kw.group_debt_lumen] == sue_iowa_debt_w

    assert membership_dataframe.loc[4, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[4, kw.person_name] == sue_personunit.person_name
    assert membership_dataframe.loc[4, kw.contact_name] == exx.sue
    assert membership_dataframe.loc[4, kw.group_title] == exx.sue
    assert membership_dataframe.loc[4, kw.group_cred_lumen] == 1
    assert membership_dataframe.loc[4, kw.group_debt_lumen] == 1

    assert membership_dataframe.loc[7, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[7, kw.person_name] == sue_personunit.person_name
    assert membership_dataframe.loc[7, kw.contact_name] == exx.yao
    assert membership_dataframe.loc[7, kw.group_title] == ohio_str
    assert membership_dataframe.loc[7, kw.group_cred_lumen] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, kw.group_debt_lumen] == yao_ohio_debt_w
    assert len(membership_dataframe) == 10


def test_create_brick_df_Arg_br00013_planunit_v0_0_0():
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_personunit.set_l1_plan(planunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)

    # WHEN
    x_brick_name = br00013_planunit_v0_0_0()
    planunit_format = create_brick_df(sue_personunit, x_brick_name)

    # THEN
    array_headers = list(planunit_format.columns)
    assert array_headers == get_brickref_obj(x_brick_name).get_headers_list()

    assert planunit_format.loc[0, kw.person_name] == sue_personunit.person_name
    assert planunit_format.loc[0, kw.pledge] == ""
    assert planunit_format.loc[0, kw.moment_rope] == amy_moment_rope
    assert planunit_format.loc[0, kw.plan_rope] == casa_rope
    assert planunit_format.loc[0, kw.star] == casa_star

    assert planunit_format.loc[1, kw.person_name] == sue_personunit.person_name
    assert planunit_format.loc[1, kw.pledge] == "Yes"
    assert planunit_format.loc[1, kw.moment_rope] == amy_moment_rope
    assert planunit_format.loc[1, kw.plan_rope] == clean_rope
    assert planunit_format.loc[1, kw.star] == 1
    assert len(planunit_format) == 2


def test_save_idea_csv_Arg_br00019_planunit_v0_0_0():
    # ESTABLISH
    sue_personunit = personunit_shop("Sue", create_rope("amy56"))
    sue_personunit = add_time_creg_planunit(sue_personunit)
    sue_personunit = add_time_five_planunit(sue_personunit)
    x_brick_name = br00019_planunit_v0_0_0()

    # WHEN
    # name_filename = f"{exx.sue}_planunit_example_00019.csv"
    # csv_example_path = create_path(str(temp3_fs), name_filename)
    # save_idea_csv(x_brick_name, sue_personunit,, name_filename)
    idea_df = create_brick_df(sue_personunit, x_brick_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_brickref_obj(x_brick_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_br00021_person_contactunit_v0_0_0_SaveToCSV(
    temp3_fs,
):
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
    name_filename = f"{exx.sue}_contact_example_00.csv"
    csv_example_path = create_path(str(temp3_fs), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_personunit, str(temp3_fs), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """spark_num,spark_face,moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot
,,;amy56;,Sue,Bob,13,29,
,,;amy56;,Sue,Sue,11,23,
,,;amy56;,Sue,Yao,41,37,
"""
    idea_file_str = open_file(str(temp3_fs), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    sue_personunit.add_contactunit(exx.zia)
    save_idea_csv(j1_ideaname, sue_personunit, str(temp3_fs), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_contact_example_csv = """spark_num,spark_face,moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot
,,;amy56;,Sue,Bob,13,29,
,,;amy56;,Sue,Sue,11,23,
,,;amy56;,Sue,Yao,41,37,
,,;amy56;,Sue,Zia,1,1,
"""
    assert open_file(str(temp3_fs), name_filename) == sue2_contact_example_csv


def test_save_idea_csv_Arg_br00013_planunit_v0_0_0(
    temp3_fs,
):
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_personunit.set_l1_plan(planunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_plan_obj(planunit_shop(exx.clean, pledge=True), casa_rope)
    x_brick_name = br00013_planunit_v0_0_0()
    planunit_format = create_brick_df(sue_personunit, x_brick_name)
    name_filename = f"{exx.sue}_planunit_example_000.csv"
    csv_example_path = create_path(str(temp3_fs), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_brick_name, sue_personunit, str(temp3_fs), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
