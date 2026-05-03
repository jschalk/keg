from ch00_py.file_toolbox import create_path
from ch02_contact.group import awardunit_shop
from ch04_rope.rope import to_rope
from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.delta import persondelta_shop
from ch09_person_lesson.lesson_main import lessonunit_shop
from ch17_brick.brick_dataframe import moment_build_from_df
from ch17_brick.brick_db_tool import get_ordered_csv
from ch17_brick.brick_idea_csv import (
    add_momentunit_to_idea_csv_strs,
    add_momentunits_to_idea_csv_strs,
    add_person_to_bk00120_csv,
    add_person_to_bk00121_csv,
    add_person_to_bk00122_csv,
    add_person_to_bk00123_csv,
    add_person_to_bk00124_csv,
    add_person_to_bk00125_csv,
    add_person_to_bk00126_csv,
    add_person_to_bk00127_csv,
    add_person_to_bk00128_csv,
    add_person_to_bk00129_csv,
    add_personunit_to_idea_csv_strs,
    create_init_idea_brick_csv_strs,
)
from ch17_brick.test._util.ch17_examples import (  # get_ex2_bk00106_df,
    J45_ROPE,
    get_ex2_bk00100_df,
    get_ex2_bk00101_df,
    get_ex2_bk00102_df,
    get_ex2_bk00103_df,
    get_ex2_bk00104_df,
    get_ex2_bk00105_df,
)
from copy import deepcopy as copy_deepcopy
from ref.keywords import ExampleStrs as exx


def test_create_init_idea_brick_csv_strs_ReturnsObj_Scenario0_EmptyMomentUnit(
    temp3_fs,
):
    # ESTABLISH
    csv_delimiter = ","

    # WHEN
    x_bricks = create_init_idea_brick_csv_strs()

    # THEN
    expected_idea_csv_strs = {
        "bk00100": "moment_rope,epoch_label,c400_number,yr1_jan1_offset,monthday_index,fund_grain,mana_grain,respect_grain,knot,job_listen_rotations\n",
        "bk00101": "moment_rope,person_name,bud_time,knot,quota,celldepth\n",
        "bk00102": "moment_rope,person_name,contact_name,tran_time,amount,knot\n",
        "bk00103": "moment_rope,cumulative_minute,hour_label,knot\n",
        "bk00104": "moment_rope,cumulative_day,month_label,knot\n",
        "bk00105": "moment_rope,weekday_order,weekday_label,knot\n",
        # "bk00106": "moment_rope,offi_time,_offi_time_max\n",
        "bk00120": "moment_rope,person_name,contact_name,group_title,group_cred_lumen,group_debt_lumen,knot\n",
        "bk00121": "moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot\n",
        "bk00122": "person_name,plan_rope,awardee_title,give_force,take_force,knot\n",
        "bk00123": "person_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper,knot\n",
        "bk00124": "person_name,plan_rope,labor_title,solo,knot\n",
        "bk00125": "person_name,plan_rope,healer_name,knot\n",
        "bk00126": "person_name,plan_rope,reason_context,reason_state,reason_lower,reason_upper,reason_divisor,knot\n",
        "bk00127": "person_name,plan_rope,reason_context,active_requisite,knot\n",
        "bk00128": "person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool,knot\n",
        "bk00129": "moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain,knot\n",
        "bk00142": "otx_title,inx_title,otx_knot,inx_knot,unknown_str\n",
        "bk00143": "otx_name,inx_name,otx_knot,inx_knot,unknown_str\n",
        "bk00144": "otx_label,inx_label,otx_knot,inx_knot,unknown_str\n",
        "bk00145": "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n",
    }
    expected_bk00100_csv = expected_idea_csv_strs.get("bk00100")
    expected_bk00101_csv = expected_idea_csv_strs.get("bk00101")
    expected_bk00102_csv = expected_idea_csv_strs.get("bk00102")
    expected_bk00103_csv = expected_idea_csv_strs.get("bk00103")
    expected_bk00104_csv = expected_idea_csv_strs.get("bk00104")
    expected_bk00105_csv = expected_idea_csv_strs.get("bk00105")
    # expected_bk00106_csv = expected_idea_csv_strs.get("bk00106")
    expected_bk00120_csv = expected_idea_csv_strs.get("bk00120")
    expected_bk00121_csv = expected_idea_csv_strs.get("bk00121")
    expected_bk00122_csv = expected_idea_csv_strs.get("bk00122")
    expected_bk00123_csv = expected_idea_csv_strs.get("bk00123")
    expected_bk00124_csv = expected_idea_csv_strs.get("bk00124")
    expected_bk00125_csv = expected_idea_csv_strs.get("bk00125")
    expected_bk00126_csv = expected_idea_csv_strs.get("bk00126")
    expected_bk00127_csv = expected_idea_csv_strs.get("bk00127")
    expected_bk00128_csv = expected_idea_csv_strs.get("bk00128")
    expected_bk00129_csv = expected_idea_csv_strs.get("bk00129")
    expected_bk00142_csv = expected_idea_csv_strs.get("bk00142")
    expected_bk00143_csv = expected_idea_csv_strs.get("bk00143")
    expected_bk00144_csv = expected_idea_csv_strs.get("bk00144")
    expected_bk00145_csv = expected_idea_csv_strs.get("bk00145")
    print(f"{expected_bk00101_csv=}")

    face_spark_str = "spark_num,spark_face,"
    assert x_bricks.get("bk00100") == f"{face_spark_str}{expected_bk00100_csv}"
    assert x_bricks.get("bk00101") == f"{face_spark_str}{expected_bk00101_csv}"
    assert x_bricks.get("bk00102") == f"{face_spark_str}{expected_bk00102_csv}"
    assert x_bricks.get("bk00103") == f"{face_spark_str}{expected_bk00103_csv}"
    assert x_bricks.get("bk00104") == f"{face_spark_str}{expected_bk00104_csv}"
    assert x_bricks.get("bk00105") == f"{face_spark_str}{expected_bk00105_csv}"
    # assert x_bricks.get("bk00106") == f"{face_spark_str}{expected_bk00106_csv}"
    print(f"{expected_bk00120_csv=}")
    print(x_bricks.get("bk00120"))
    assert x_bricks.get("bk00120") == f"{face_spark_str}{expected_bk00120_csv}"
    assert x_bricks.get("bk00121") == f"{face_spark_str}{expected_bk00121_csv}"
    assert x_bricks.get("bk00122") == f"{face_spark_str}{expected_bk00122_csv}"
    assert x_bricks.get("bk00123") == f"{face_spark_str}{expected_bk00123_csv}"
    assert x_bricks.get("bk00124") == f"{face_spark_str}{expected_bk00124_csv}"
    assert x_bricks.get("bk00125") == f"{face_spark_str}{expected_bk00125_csv}"
    assert x_bricks.get("bk00126") == f"{face_spark_str}{expected_bk00126_csv}"
    assert x_bricks.get("bk00127") == f"{face_spark_str}{expected_bk00127_csv}"
    assert x_bricks.get("bk00128") == f"{face_spark_str}{expected_bk00128_csv}"
    assert x_bricks.get("bk00129") == f"{face_spark_str}{expected_bk00129_csv}"
    assert x_bricks.get("bk00142") == f"{face_spark_str}{expected_bk00142_csv}"
    assert x_bricks.get("bk00143") == f"{face_spark_str}{expected_bk00143_csv}"
    assert x_bricks.get("bk00144") == f"{face_spark_str}{expected_bk00144_csv}"
    assert x_bricks.get("bk00145") == f"{face_spark_str}{expected_bk00145_csv}"
    assert len(x_bricks) == 20


def test_add_momentunit_to_idea_csv_strs_ReturnsObj_Scenario0_OneMomentUnit(
    temp3_fs,
):
    # ESTABLISH
    bk00100_df = get_ex2_bk00100_df()
    # print(f"{bk00100_df=}")
    bk00101_df = get_ex2_bk00101_df()
    bk00102_df = get_ex2_bk00102_df()
    bk00103_df = get_ex2_bk00103_df()
    bk00104_df = get_ex2_bk00104_df()
    bk00105_df = get_ex2_bk00105_df()
    # bk00106_df = get_ex2_bk00106_df()
    x_fund_grain = 1
    x_respect_grain = 1
    x_mana_grain = 1
    x_moments_dir = create_path(str(temp3_fs), "Fay")
    x_momentunits = moment_build_from_df(
        bk00100_df,
        bk00101_df,
        bk00102_df,
        bk00103_df,
        bk00104_df,
        bk00105_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )
    csv_delimiter = ","
    x_csvs = create_init_idea_brick_csv_strs()
    bk00_csv_header = x_csvs.get("bk00100")
    bk01_csv_header = x_csvs.get("bk00101")
    bk02_csv_header = x_csvs.get("bk00102")
    bk03_csv_header = x_csvs.get("bk00103")
    bk04_csv_header = x_csvs.get("bk00104")
    bk05_csv_header = x_csvs.get("bk00105")
    # bk06_csv_header = x_csvs.get("bk00106")
    a23_momentunit = x_momentunits.get(exx.a23_slash)

    # WHEN
    add_momentunit_to_idea_csv_strs(a23_momentunit, x_csvs, csv_delimiter)

    # THEN
    gen_bk00100_csv = x_csvs.get("bk00100")
    gen_bk00101_csv = x_csvs.get("bk00101")
    gen_bk00102_csv = x_csvs.get("bk00102")
    gen_bk00103_csv = x_csvs.get("bk00103")
    gen_bk00104_csv = x_csvs.get("bk00104")
    gen_bk00105_csv = x_csvs.get("bk00105")
    # gen_bk00106_csv = x_csvs.get("bk00106")
    expected_bk00100_csv = ",,/Amy23/,creg,7,440640,1,1,1,1,/,4\n"
    expected_bk00101_csv = ",,/Amy23/,Bob,999,/,332,3\n,,/Amy23/,Sue,777,/,445,3\n,,/Amy23/,Yao,222,/,700,3\n"
    expected_bk00102_csv = ",,/Amy23/,Bob,Zia,777,888,/\n,,/Amy23/,Sue,Zia,999,234,/\n,,/Amy23/,Yao,Zia,999,234,/\n,,/Amy23/,Zia,Bob,777,888,/\n"
    expected_bk00103_csv = ",,/Amy23/,60,12am,/\n,,/Amy23/,120,1am,/\n,,/Amy23/,180,2am,/\n,,/Amy23/,240,3am,/\n,,/Amy23/,300,4am,/\n,,/Amy23/,360,5am,/\n,,/Amy23/,420,6am,/\n,,/Amy23/,480,7am,/\n,,/Amy23/,540,8am,/\n,,/Amy23/,600,9am,/\n,,/Amy23/,660,10am,/\n,,/Amy23/,720,11am,/\n,,/Amy23/,780,12pm,/\n,,/Amy23/,840,1pm,/\n,,/Amy23/,900,2pm,/\n,,/Amy23/,960,3pm,/\n,,/Amy23/,1020,4pm,/\n,,/Amy23/,1080,5pm,/\n,,/Amy23/,1140,6pm,/\n,,/Amy23/,1200,7pm,/\n,,/Amy23/,1260,8pm,/\n,,/Amy23/,1320,9pm,/\n,,/Amy23/,1380,10pm,/\n,,/Amy23/,1440,11pm,/\n"
    expected_bk00104_csv = ",,/Amy23/,31,March,/\n,,/Amy23/,61,April,/\n,,/Amy23/,92,May,/\n,,/Amy23/,122,June,/\n,,/Amy23/,153,July,/\n,,/Amy23/,184,August,/\n,,/Amy23/,214,September,/\n,,/Amy23/,245,October,/\n,,/Amy23/,275,November,/\n,,/Amy23/,306,December,/\n,,/Amy23/,337,January,/\n,,/Amy23/,365,February,/\n"
    expected_bk00105_csv = ",,/Amy23/,0,Wednesday,/\n,,/Amy23/,1,Thursday,/\n,,/Amy23/,2,Friday,/\n,,/Amy23/,3,Saturday,/\n,,/Amy23/,4,Sunday,/\n,,/Amy23/,5,Monday,/\n,,/Amy23/,6,Tuesday,/\n"
    # expected_bk00106_csv = ",,/Amy23/,0,Wednesday\n,,/Amy23/,1,Thursday\n,,/Amy23/,2,Friday\n,,/Amy23/,3,Saturday\n,,/Amy23/,4,Sunday\n,,/Amy23/,5,Monday\n,,/Amy23/,6,Tuesday\n"

    # print(f"      {bk02_csv_header=}")
    print(f"      {gen_bk00105_csv=}")
    # print(f" {expected_bk00104_csv=}")
    # print(f"      {gen_bk00104_csv=}")
    # print(f"      {gen_bk00105_csv=}")
    assert gen_bk00100_csv == f"{bk00_csv_header}{expected_bk00100_csv}"
    assert gen_bk00101_csv == f"{bk01_csv_header}{expected_bk00101_csv}"
    assert gen_bk00102_csv == f"{bk02_csv_header}{expected_bk00102_csv}"
    assert gen_bk00103_csv == f"{bk03_csv_header}{expected_bk00103_csv}"
    assert gen_bk00104_csv == f"{bk04_csv_header}{expected_bk00104_csv}"
    assert gen_bk00105_csv == f"{bk05_csv_header}{expected_bk00105_csv}"
    # assert gen_bk00106_csv == f"{bk06_csv_header}{expected_bk00106_csv}"


def test_add_momentunits_to_idea_csv_strs_ReturnsObj_Scenario1_TwoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    bk00100_df = get_ex2_bk00100_df()
    bk00101_df = get_ex2_bk00101_df()
    bk00102_df = get_ex2_bk00102_df()
    bk00103_df = get_ex2_bk00103_df()
    bk00104_df = get_ex2_bk00104_df()
    bk00105_df = get_ex2_bk00105_df()
    x_fund_grain = 1
    x_respect_grain = 1
    x_mana_grain = 1
    x_moments_dir = create_path(str(temp3_fs), "Fay")
    x_momentunits = moment_build_from_df(
        bk00100_df,
        bk00101_df,
        bk00102_df,
        bk00103_df,
        bk00104_df,
        bk00105_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()

    # WHEN
    add_momentunits_to_idea_csv_strs(x_momentunits, x_bricks, csv_delimiter)

    # THEN
    expected_bk00100_csv = get_ordered_csv(get_ex2_bk00100_df())
    expected_bk00101_csv = get_ordered_csv(get_ex2_bk00101_df())
    expected_bk00102_csv = get_ordered_csv(get_ex2_bk00102_df())
    expected_bk00103_csv = get_ordered_csv(get_ex2_bk00103_df())
    expected_bk00104_csv = get_ordered_csv(get_ex2_bk00104_df())
    expected_bk00105_csv = get_ordered_csv(get_ex2_bk00105_df())
    expected_bk00100_csv = f"spark_num,spark_face,{expected_bk00100_csv}"
    expected_bk00101_csv = f"spark_num,spark_face,{expected_bk00101_csv}"
    expected_bk00102_csv = f"spark_num,spark_face,{expected_bk00102_csv}"
    expected_bk00103_csv = f"spark_num,spark_face,{expected_bk00103_csv}"
    expected_bk00104_csv = f"spark_num,spark_face,{expected_bk00104_csv}"
    expected_bk00105_csv = f"spark_num,spark_face,{expected_bk00105_csv}"
    x_rope = exx.a23_slash
    expected_bk00100_csv = expected_bk00100_csv.replace(x_rope, f",,{x_rope}")
    expected_bk00101_csv = expected_bk00101_csv.replace(x_rope, f",,{x_rope}")
    expected_bk00102_csv = expected_bk00102_csv.replace(x_rope, f",,{x_rope}")
    expected_bk00103_csv = expected_bk00103_csv.replace(x_rope, f",,{x_rope}")
    expected_bk00104_csv = expected_bk00104_csv.replace(x_rope, f",,{x_rope}")
    expected_bk00105_csv = expected_bk00105_csv.replace(x_rope, f",,{x_rope}")
    expected_bk00100_csv = expected_bk00100_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_bk00101_csv = expected_bk00101_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_bk00102_csv = expected_bk00102_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_bk00103_csv = expected_bk00103_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_bk00104_csv = expected_bk00104_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_bk00105_csv = expected_bk00105_csv.replace(J45_ROPE, f",,{J45_ROPE}")

    assert len(x_bricks) == 20
    generated_bk00100_csv = x_bricks.get("bk00100")
    generated_bk00101_csv = x_bricks.get("bk00101")
    generated_bk00102_csv = x_bricks.get("bk00102")
    generated_bk00103_csv = x_bricks.get("bk00103")
    generated_bk00104_csv = x_bricks.get("bk00104")
    generated_bk00105_csv = x_bricks.get("bk00105")
    print(f"{generated_bk00101_csv=}")
    print(f" {expected_bk00101_csv=}")
    assert generated_bk00100_csv == expected_bk00100_csv
    assert generated_bk00101_csv == expected_bk00101_csv
    assert generated_bk00102_csv == expected_bk00102_csv
    assert len(generated_bk00103_csv) == len(expected_bk00103_csv)
    assert generated_bk00104_csv == expected_bk00104_csv
    assert generated_bk00105_csv == expected_bk00105_csv


def test_add_person_to_bk00120_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao)
    run_credit = 33
    run_debt = 55
    bob_person.get_contact(exx.yao).add_membership(exx.run, run_credit, run_debt)
    csv_header = x_bricks.get("bk00120")

    # WHEN
    x_csv = add_person_to_bk00120_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_yao_row = f",,{exx.a23},{exx.bob},{exx.yao},{exx.yao},1,1,;\n"
    yao_run_row = (
        f",,{exx.a23},{exx.bob},{exx.yao},{exx.run},{run_credit},{run_debt},;\n"
    )
    print(f"{x_csv=}")
    print(f"{yao_run_row=}")
    assert x_csv == f"{csv_header}{yao_yao_row}{yao_run_row}"


def test_add_person_to_bk00121_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    yao_credit = 33
    yao_debt = 55
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao, yao_credit, yao_debt)
    csv_header = x_bricks.get("bk00121")

    # WHEN
    x_csv = add_person_to_bk00121_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_row = f",,{exx.a23},{exx.bob},{exx.yao},{yao_credit},{yao_debt},;\n"
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_person_to_bk00122_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    yao_give_force = 55
    yao_take_force = 77
    casa_awardunit = awardunit_shop(exx.yao, yao_give_force, yao_take_force)
    bob_person.add_plan(casa_rope)
    bob_person.edit_plan_attr(casa_rope, awardunit=casa_awardunit)
    csv_header = x_bricks.get("bk00122")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_bk00122_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_award_row = (
        f",,{exx.bob},{casa_rope},{exx.yao},{yao_give_force},{yao_take_force},;\n"
    )
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_person_to_bk00123_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    a23_rope = to_rope(exx.a23)
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    clean_rope = bob_person.make_rope(casa_rope, "clean")
    clean_fact_lower = 55
    clean_fact_upper = 77
    bob_person.add_plan(casa_rope)
    bob_person.add_plan(clean_rope)
    bob_person.add_fact(casa_rope, clean_rope, clean_fact_lower, clean_fact_upper)
    csv_header = x_bricks.get("bk00123")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_person_to_bk00123_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    clean_row = f",,{exx.bob},{a23_rope},{casa_rope},{clean_rope},{clean_fact_lower},{clean_fact_upper},;\n"
    assert x_csv == f"{csv_header}{clean_row}"


def test_add_person_to_bk00124_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(casa_rope)
    casa_plan = bob_person.get_plan_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_plan.workforceunit.add_labor(cleaners_str)
    csv_header = x_bricks.get("bk00124")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_bk00124_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    cleaners_row = f",,{exx.bob},{casa_rope},{cleaners_str},;\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_person_to_bk00125_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(casa_rope)
    casa_plan = bob_person.get_plan_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_plan.healerunit.set_healer_name(cleaners_str)
    csv_header = x_bricks.get("bk00125")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_bk00125_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    cleaners_row = f",,{exx.bob},{casa_rope},{cleaners_str},;\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_person_to_bk00126_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    mop_rope = bob_person.make_l1_rope("mop")
    casa_rope = bob_person.make_l1_rope("casa")
    clean_rope = bob_person.make_rope(casa_rope, "clean")
    clean_reason_lower = 22
    clean_reason_upper = 55
    clean_reason_divisor = 77
    bob_person.add_plan(mop_rope)
    bob_person.add_plan(casa_rope)
    bob_person.add_plan(clean_rope)
    bob_person.edit_plan_attr(
        mop_rope,
        reason_context=casa_rope,
        reason_case=clean_rope,
        reason_lower=clean_reason_lower,
        reason_upper=clean_reason_upper,
        reason_divisor=clean_reason_divisor,
    )
    csv_header = x_bricks.get("bk00126")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_bk00126_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    mop_row = f",,{exx.bob},{mop_rope},{casa_rope},{clean_rope},{clean_reason_lower},{clean_reason_upper},{clean_reason_divisor},;\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_person_to_bk00127_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    mop_rope = bob_person.make_l1_rope("mop")
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(mop_rope)
    bob_person.add_plan(casa_rope)
    bob_person.edit_plan_attr(
        mop_rope,
        reason_context=casa_rope,
        reason_requisite_active=True,
    )
    csv_header = x_bricks.get("bk00127")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_bk00127_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    casa_row = f",,{exx.bob},{mop_rope},{casa_rope},True,;\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_person_to_bk00128_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    a23_rope = to_rope(exx.a23)
    bob_person = personunit_shop(exx.bob, exx.a23)
    mop_rope = bob_person.make_l1_rope("mop")
    casa_rope = bob_person.make_l1_rope("casa")
    casa_begin = 3
    casa_close = 5
    casa_addin = 7
    casa_numor = 13
    casa_denom = 17
    casa_morph = 27
    casa_gogo_want = 31
    casa_stop_want = 41
    casa_star = 2
    casa_pledge = False
    casa_problem_bool = False
    bob_person.add_plan(casa_rope)
    bob_person.add_plan(mop_rope)
    bob_person.edit_plan_attr(
        mop_rope,
        begin=casa_begin,
        close=casa_close,
        addin=casa_addin,
        numor=casa_numor,
        denom=casa_denom,
        morph=casa_morph,
        gogo_want=casa_gogo_want,
        stop_want=casa_stop_want,
        star=casa_star,
        pledge=casa_pledge,
        problem_bool=casa_problem_bool,
    )
    csv_header = x_bricks.get("bk00128")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_bk00128_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    root_row = f",,{exx.bob},,{a23_rope},,,,,,,,,1,False,False,;\n"
    mop_row = f",,{exx.bob},{mop_rope},{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_star},{casa_pledge},{casa_problem_bool},;\n"
    casa_row = f",,{exx.bob},{casa_rope},,,,,,,,,0,False,False,;\n"
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{mop_row}{casa_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_person_to_bk00129_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.credor_respect = 444
    bob_person.debtor_respect = 555
    bob_person.fund_pool = 777
    bob_person.max_tree_traverse = 3
    bob_person.fund_grain = 12
    bob_person.mana_grain = 13
    bob_person.respect_grain = 15
    csv_header = x_bricks.get("bk00129")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_person_to_bk00129_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    person_row = f",,{exx.a23},{exx.bob},{bob_person.credor_respect},{bob_person.debtor_respect},{bob_person.fund_pool},{bob_person.max_tree_traverse},{bob_person.fund_grain},{bob_person.mana_grain},{bob_person.respect_grain},;\n"
    assert x_csv == f"{csv_header}{person_row}"


def test_add_personunit_to_idea_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_bricks = create_init_idea_brick_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao)
    mop_rope = bob_person.make_l1_rope("mop")
    casa_rope = bob_person.make_l1_rope("casa")
    clean_rope = bob_person.make_rope(casa_rope, "clean")
    bob_person.add_plan(mop_rope)
    bob_person.add_plan(casa_rope)
    bob_person.add_plan(clean_rope)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=casa_rope, reason_case=clean_rope
    )
    bob_person.add_plan(casa_rope)
    bob_person.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.yao))
    bob_person.add_fact(casa_rope, clean_rope)

    bk00120_header = x_bricks.get("bk00120")
    bk00121_header = x_bricks.get("bk00121")
    bk00122_header = x_bricks.get("bk00122")
    bk00123_header = x_bricks.get("bk00123")
    bk00124_header = x_bricks.get("bk00124")
    bk00125_header = x_bricks.get("bk00125")
    bk00126_header = x_bricks.get("bk00126")
    bk00127_header = x_bricks.get("bk00127")
    bk00128_header = x_bricks.get("bk00128")
    bk00129_header = x_bricks.get("bk00129")

    # WHEN
    bob_person.thinkout()
    add_personunit_to_idea_csv_strs(bob_person, x_bricks, csv_delimiter)

    # THEN
    assert x_bricks.get("bk00120") != bk00120_header
    assert x_bricks.get("bk00121") != bk00121_header
    assert x_bricks.get("bk00122") != bk00122_header
    assert x_bricks.get("bk00123") != bk00123_header
    # assert x_bricks.get("bk00124") != bk00124_header
    # assert x_bricks.get("bk00125") != bk00125_header
    assert x_bricks.get("bk00126") != bk00126_header
    assert x_bricks.get("bk00127") != bk00127_header
    assert x_bricks.get("bk00128") != bk00128_header
    assert x_bricks.get("bk00129") != bk00129_header
