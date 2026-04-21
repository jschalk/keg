from ch00_py.file_toolbox import create_path
from ch02_contact.group import awardunit_shop
from ch04_rope.rope import to_rope
from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.delta import persondelta_shop
from ch09_person_lesson.lesson_main import lessonunit_shop
from ch17_idea.idea_belief_csv import (
    add_momentunit_to_belief_csv_strs,
    add_momentunits_to_belief_csv_strs,
    add_person_to_ii00120_csv,
    add_person_to_ii00121_csv,
    add_person_to_ii00122_csv,
    add_person_to_ii00123_csv,
    add_person_to_ii00124_csv,
    add_person_to_ii00125_csv,
    add_person_to_ii00126_csv,
    add_person_to_ii00127_csv,
    add_person_to_ii00128_csv,
    add_person_to_ii00129_csv,
    add_personunit_to_belief_csv_strs,
    create_init_belief_idea_csv_strs,
)
from ch17_idea.idea_db_tool import get_ordered_csv
from ch17_idea.idea_main import moment_build_from_df
from ch17_idea.test._util.ch17_examples import (  # get_ex2_ii00106_df,
    J45_ROPE,
    get_ex2_ii00100_df,
    get_ex2_ii00101_df,
    get_ex2_ii00102_df,
    get_ex2_ii00103_df,
    get_ex2_ii00104_df,
    get_ex2_ii00105_df,
)
from copy import deepcopy as copy_deepcopy
from ref.keywords import ExampleStrs as exx


def test_create_init_belief_idea_csv_strs_ReturnsObj_Scenario0_EmptyMomentUnit(
    temp3_fs,
):
    # ESTABLISH
    csv_delimiter = ","

    # WHEN
    x_ideas = create_init_belief_idea_csv_strs()

    # THEN
    expected_belief_csv_strs = {
        "ii00100": "moment_rope,epoch_label,c400_number,yr1_jan1_offset,monthday_index,fund_grain,mana_grain,respect_grain,knot,job_listen_rotations\n",
        "ii00101": "moment_rope,person_name,bud_time,knot,quota,celldepth\n",
        "ii00102": "moment_rope,person_name,contact_name,tran_time,amount,knot\n",
        "ii00103": "moment_rope,cumulative_minute,hour_label,knot\n",
        "ii00104": "moment_rope,cumulative_day,month_label,knot\n",
        "ii00105": "moment_rope,weekday_order,weekday_label,knot\n",
        # "ii00106": "moment_rope,offi_time,_offi_time_max\n",
        "ii00120": "moment_rope,person_name,contact_name,group_title,group_cred_lumen,group_debt_lumen,knot\n",
        "ii00121": "moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot\n",
        "ii00122": "person_name,plan_rope,awardee_title,give_force,take_force,knot\n",
        "ii00123": "person_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper,knot\n",
        "ii00124": "person_name,plan_rope,labor_title,solo,knot\n",
        "ii00125": "person_name,plan_rope,healer_name,knot\n",
        "ii00126": "person_name,plan_rope,reason_context,reason_state,reason_lower,reason_upper,reason_divisor,knot\n",
        "ii00127": "person_name,plan_rope,reason_context,active_requisite,knot\n",
        "ii00128": "person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool,knot\n",
        "ii00129": "moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain,knot\n",
        "ii00142": "otx_title,inx_title,otx_knot,inx_knot,unknown_str\n",
        "ii00143": "otx_name,inx_name,otx_knot,inx_knot,unknown_str\n",
        "ii00144": "otx_label,inx_label,otx_knot,inx_knot,unknown_str\n",
        "ii00145": "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n",
    }
    expected_ii00100_csv = expected_belief_csv_strs.get("ii00100")
    expected_ii00101_csv = expected_belief_csv_strs.get("ii00101")
    expected_ii00102_csv = expected_belief_csv_strs.get("ii00102")
    expected_ii00103_csv = expected_belief_csv_strs.get("ii00103")
    expected_ii00104_csv = expected_belief_csv_strs.get("ii00104")
    expected_ii00105_csv = expected_belief_csv_strs.get("ii00105")
    # expected_ii00106_csv = expected_belief_csv_strs.get("ii00106")
    expected_ii00120_csv = expected_belief_csv_strs.get("ii00120")
    expected_ii00121_csv = expected_belief_csv_strs.get("ii00121")
    expected_ii00122_csv = expected_belief_csv_strs.get("ii00122")
    expected_ii00123_csv = expected_belief_csv_strs.get("ii00123")
    expected_ii00124_csv = expected_belief_csv_strs.get("ii00124")
    expected_ii00125_csv = expected_belief_csv_strs.get("ii00125")
    expected_ii00126_csv = expected_belief_csv_strs.get("ii00126")
    expected_ii00127_csv = expected_belief_csv_strs.get("ii00127")
    expected_ii00128_csv = expected_belief_csv_strs.get("ii00128")
    expected_ii00129_csv = expected_belief_csv_strs.get("ii00129")
    expected_ii00142_csv = expected_belief_csv_strs.get("ii00142")
    expected_ii00143_csv = expected_belief_csv_strs.get("ii00143")
    expected_ii00144_csv = expected_belief_csv_strs.get("ii00144")
    expected_ii00145_csv = expected_belief_csv_strs.get("ii00145")
    print(f"{expected_ii00101_csv=}")

    face_spark_str = "spark_num,spark_face,"
    assert x_ideas.get("ii00100") == f"{face_spark_str}{expected_ii00100_csv}"
    assert x_ideas.get("ii00101") == f"{face_spark_str}{expected_ii00101_csv}"
    assert x_ideas.get("ii00102") == f"{face_spark_str}{expected_ii00102_csv}"
    assert x_ideas.get("ii00103") == f"{face_spark_str}{expected_ii00103_csv}"
    assert x_ideas.get("ii00104") == f"{face_spark_str}{expected_ii00104_csv}"
    assert x_ideas.get("ii00105") == f"{face_spark_str}{expected_ii00105_csv}"
    # assert x_ideas.get("ii00106") == f"{face_spark_str}{expected_ii00106_csv}"
    print(f"{expected_ii00120_csv=}")
    print(x_ideas.get("ii00120"))
    assert x_ideas.get("ii00120") == f"{face_spark_str}{expected_ii00120_csv}"
    assert x_ideas.get("ii00121") == f"{face_spark_str}{expected_ii00121_csv}"
    assert x_ideas.get("ii00122") == f"{face_spark_str}{expected_ii00122_csv}"
    assert x_ideas.get("ii00123") == f"{face_spark_str}{expected_ii00123_csv}"
    assert x_ideas.get("ii00124") == f"{face_spark_str}{expected_ii00124_csv}"
    assert x_ideas.get("ii00125") == f"{face_spark_str}{expected_ii00125_csv}"
    assert x_ideas.get("ii00126") == f"{face_spark_str}{expected_ii00126_csv}"
    assert x_ideas.get("ii00127") == f"{face_spark_str}{expected_ii00127_csv}"
    assert x_ideas.get("ii00128") == f"{face_spark_str}{expected_ii00128_csv}"
    assert x_ideas.get("ii00129") == f"{face_spark_str}{expected_ii00129_csv}"
    assert x_ideas.get("ii00142") == f"{face_spark_str}{expected_ii00142_csv}"
    assert x_ideas.get("ii00143") == f"{face_spark_str}{expected_ii00143_csv}"
    assert x_ideas.get("ii00144") == f"{face_spark_str}{expected_ii00144_csv}"
    assert x_ideas.get("ii00145") == f"{face_spark_str}{expected_ii00145_csv}"
    assert len(x_ideas) == 20


def test_add_momentunit_to_belief_csv_strs_ReturnsObj_Scenario0_OneMomentUnit(
    temp3_fs,
):
    # ESTABLISH
    ii00100_df = get_ex2_ii00100_df()
    # print(f"{ii00100_df=}")
    ii00101_df = get_ex2_ii00101_df()
    ii00102_df = get_ex2_ii00102_df()
    ii00103_df = get_ex2_ii00103_df()
    ii00104_df = get_ex2_ii00104_df()
    ii00105_df = get_ex2_ii00105_df()
    # ii00106_df = get_ex2_ii00106_df()
    x_fund_grain = 1
    x_respect_grain = 1
    x_mana_grain = 1
    x_moments_dir = create_path(str(temp3_fs), "Fay")
    x_momentunits = moment_build_from_df(
        ii00100_df,
        ii00101_df,
        ii00102_df,
        ii00103_df,
        ii00104_df,
        ii00105_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )
    csv_delimiter = ","
    x_csvs = create_init_belief_idea_csv_strs()
    ii00_csv_header = x_csvs.get("ii00100")
    ii01_csv_header = x_csvs.get("ii00101")
    ii02_csv_header = x_csvs.get("ii00102")
    ii03_csv_header = x_csvs.get("ii00103")
    ii04_csv_header = x_csvs.get("ii00104")
    ii05_csv_header = x_csvs.get("ii00105")
    # ii06_csv_header = x_csvs.get("ii00106")
    a23_momentunit = x_momentunits.get(exx.a23_slash)

    # WHEN
    add_momentunit_to_belief_csv_strs(a23_momentunit, x_csvs, csv_delimiter)

    # THEN
    gen_ii00100_csv = x_csvs.get("ii00100")
    gen_ii00101_csv = x_csvs.get("ii00101")
    gen_ii00102_csv = x_csvs.get("ii00102")
    gen_ii00103_csv = x_csvs.get("ii00103")
    gen_ii00104_csv = x_csvs.get("ii00104")
    gen_ii00105_csv = x_csvs.get("ii00105")
    # gen_ii00106_csv = x_csvs.get("ii00106")
    expected_ii00100_csv = ",,/Amy23/,creg,7,440640,1,1,1,1,/,4\n"
    expected_ii00101_csv = ",,/Amy23/,Bob,999,/,332,3\n,,/Amy23/,Sue,777,/,445,3\n,,/Amy23/,Yao,222,/,700,3\n"
    expected_ii00102_csv = ",,/Amy23/,Bob,Zia,777,888,/\n,,/Amy23/,Sue,Zia,999,234,/\n,,/Amy23/,Yao,Zia,999,234,/\n,,/Amy23/,Zia,Bob,777,888,/\n"
    expected_ii00103_csv = ",,/Amy23/,60,12am,/\n,,/Amy23/,120,1am,/\n,,/Amy23/,180,2am,/\n,,/Amy23/,240,3am,/\n,,/Amy23/,300,4am,/\n,,/Amy23/,360,5am,/\n,,/Amy23/,420,6am,/\n,,/Amy23/,480,7am,/\n,,/Amy23/,540,8am,/\n,,/Amy23/,600,9am,/\n,,/Amy23/,660,10am,/\n,,/Amy23/,720,11am,/\n,,/Amy23/,780,12pm,/\n,,/Amy23/,840,1pm,/\n,,/Amy23/,900,2pm,/\n,,/Amy23/,960,3pm,/\n,,/Amy23/,1020,4pm,/\n,,/Amy23/,1080,5pm,/\n,,/Amy23/,1140,6pm,/\n,,/Amy23/,1200,7pm,/\n,,/Amy23/,1260,8pm,/\n,,/Amy23/,1320,9pm,/\n,,/Amy23/,1380,10pm,/\n,,/Amy23/,1440,11pm,/\n"
    expected_ii00104_csv = ",,/Amy23/,31,March,/\n,,/Amy23/,61,April,/\n,,/Amy23/,92,May,/\n,,/Amy23/,122,June,/\n,,/Amy23/,153,July,/\n,,/Amy23/,184,August,/\n,,/Amy23/,214,September,/\n,,/Amy23/,245,October,/\n,,/Amy23/,275,November,/\n,,/Amy23/,306,December,/\n,,/Amy23/,337,January,/\n,,/Amy23/,365,February,/\n"
    expected_ii00105_csv = ",,/Amy23/,0,Wednesday,/\n,,/Amy23/,1,Thursday,/\n,,/Amy23/,2,Friday,/\n,,/Amy23/,3,Saturday,/\n,,/Amy23/,4,Sunday,/\n,,/Amy23/,5,Monday,/\n,,/Amy23/,6,Tuesday,/\n"
    # expected_ii00106_csv = ",,/Amy23/,0,Wednesday\n,,/Amy23/,1,Thursday\n,,/Amy23/,2,Friday\n,,/Amy23/,3,Saturday\n,,/Amy23/,4,Sunday\n,,/Amy23/,5,Monday\n,,/Amy23/,6,Tuesday\n"

    # print(f"      {ii02_csv_header=}")
    print(f"      {gen_ii00105_csv=}")
    # print(f" {expected_ii00104_csv=}")
    # print(f"      {gen_ii00104_csv=}")
    # print(f"      {gen_ii00105_csv=}")
    assert gen_ii00100_csv == f"{ii00_csv_header}{expected_ii00100_csv}"
    assert gen_ii00101_csv == f"{ii01_csv_header}{expected_ii00101_csv}"
    assert gen_ii00102_csv == f"{ii02_csv_header}{expected_ii00102_csv}"
    assert gen_ii00103_csv == f"{ii03_csv_header}{expected_ii00103_csv}"
    assert gen_ii00104_csv == f"{ii04_csv_header}{expected_ii00104_csv}"
    assert gen_ii00105_csv == f"{ii05_csv_header}{expected_ii00105_csv}"
    # assert gen_ii00106_csv == f"{ii06_csv_header}{expected_ii00106_csv}"


def test_add_momentunits_to_belief_csv_strs_ReturnsObj_Scenario1_TwoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    ii00100_df = get_ex2_ii00100_df()
    ii00101_df = get_ex2_ii00101_df()
    ii00102_df = get_ex2_ii00102_df()
    ii00103_df = get_ex2_ii00103_df()
    ii00104_df = get_ex2_ii00104_df()
    ii00105_df = get_ex2_ii00105_df()
    x_fund_grain = 1
    x_respect_grain = 1
    x_mana_grain = 1
    x_moments_dir = create_path(str(temp3_fs), "Fay")
    x_momentunits = moment_build_from_df(
        ii00100_df,
        ii00101_df,
        ii00102_df,
        ii00103_df,
        ii00104_df,
        ii00105_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()

    # WHEN
    add_momentunits_to_belief_csv_strs(x_momentunits, x_ideas, csv_delimiter)

    # THEN
    expected_ii00100_csv = get_ordered_csv(get_ex2_ii00100_df())
    expected_ii00101_csv = get_ordered_csv(get_ex2_ii00101_df())
    expected_ii00102_csv = get_ordered_csv(get_ex2_ii00102_df())
    expected_ii00103_csv = get_ordered_csv(get_ex2_ii00103_df())
    expected_ii00104_csv = get_ordered_csv(get_ex2_ii00104_df())
    expected_ii00105_csv = get_ordered_csv(get_ex2_ii00105_df())
    expected_ii00100_csv = f"spark_num,spark_face,{expected_ii00100_csv}"
    expected_ii00101_csv = f"spark_num,spark_face,{expected_ii00101_csv}"
    expected_ii00102_csv = f"spark_num,spark_face,{expected_ii00102_csv}"
    expected_ii00103_csv = f"spark_num,spark_face,{expected_ii00103_csv}"
    expected_ii00104_csv = f"spark_num,spark_face,{expected_ii00104_csv}"
    expected_ii00105_csv = f"spark_num,spark_face,{expected_ii00105_csv}"
    x_rope = exx.a23_slash
    expected_ii00100_csv = expected_ii00100_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00101_csv = expected_ii00101_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00102_csv = expected_ii00102_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00103_csv = expected_ii00103_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00104_csv = expected_ii00104_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00105_csv = expected_ii00105_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00100_csv = expected_ii00100_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00101_csv = expected_ii00101_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00102_csv = expected_ii00102_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00103_csv = expected_ii00103_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00104_csv = expected_ii00104_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00105_csv = expected_ii00105_csv.replace(J45_ROPE, f",,{J45_ROPE}")

    assert len(x_ideas) == 20
    generated_ii00100_csv = x_ideas.get("ii00100")
    generated_ii00101_csv = x_ideas.get("ii00101")
    generated_ii00102_csv = x_ideas.get("ii00102")
    generated_ii00103_csv = x_ideas.get("ii00103")
    generated_ii00104_csv = x_ideas.get("ii00104")
    generated_ii00105_csv = x_ideas.get("ii00105")
    print(f"{generated_ii00101_csv=}")
    print(f" {expected_ii00101_csv=}")
    assert generated_ii00100_csv == expected_ii00100_csv
    assert generated_ii00101_csv == expected_ii00101_csv
    assert generated_ii00102_csv == expected_ii00102_csv
    assert len(generated_ii00103_csv) == len(expected_ii00103_csv)
    assert generated_ii00104_csv == expected_ii00104_csv
    assert generated_ii00105_csv == expected_ii00105_csv


def test_add_person_to_ii00120_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao)
    run_credit = 33
    run_debt = 55
    bob_person.get_contact(exx.yao).add_membership(exx.run, run_credit, run_debt)
    csv_header = x_ideas.get("ii00120")

    # WHEN
    x_csv = add_person_to_ii00120_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_yao_row = f",,{exx.a23},{exx.bob},{exx.yao},{exx.yao},1,1,;\n"
    yao_run_row = (
        f",,{exx.a23},{exx.bob},{exx.yao},{exx.run},{run_credit},{run_debt},;\n"
    )
    print(f"{x_csv=}")
    print(f"{yao_run_row=}")
    assert x_csv == f"{csv_header}{yao_yao_row}{yao_run_row}"


def test_add_person_to_ii00121_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    yao_credit = 33
    yao_debt = 55
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao, yao_credit, yao_debt)
    csv_header = x_ideas.get("ii00121")

    # WHEN
    x_csv = add_person_to_ii00121_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_row = f",,{exx.a23},{exx.bob},{exx.yao},{yao_credit},{yao_debt},;\n"
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_person_to_ii00122_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    yao_give_force = 55
    yao_take_force = 77
    casa_awardunit = awardunit_shop(exx.yao, yao_give_force, yao_take_force)
    bob_person.add_plan(casa_rope)
    bob_person.edit_plan_attr(casa_rope, awardunit=casa_awardunit)
    csv_header = x_ideas.get("ii00122")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_ii00122_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_award_row = (
        f",,{exx.bob},{casa_rope},{exx.yao},{yao_give_force},{yao_take_force},;\n"
    )
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_person_to_ii00123_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    a23_rope = to_rope(exx.a23)
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    clean_rope = bob_person.make_rope(casa_rope, "clean")
    clean_fact_lower = 55
    clean_fact_upper = 77
    bob_person.add_plan(casa_rope)
    bob_person.add_plan(clean_rope)
    bob_person.add_fact(casa_rope, clean_rope, clean_fact_lower, clean_fact_upper)
    csv_header = x_ideas.get("ii00123")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_person_to_ii00123_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    clean_row = f",,{exx.bob},{a23_rope},{casa_rope},{clean_rope},{clean_fact_lower},{clean_fact_upper},;\n"
    assert x_csv == f"{csv_header}{clean_row}"


def test_add_person_to_ii00124_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(casa_rope)
    casa_plan = bob_person.get_plan_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_plan.workforceunit.add_labor(cleaners_str)
    csv_header = x_ideas.get("ii00124")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_ii00124_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    cleaners_row = f",,{exx.bob},{casa_rope},{cleaners_str},;\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_person_to_ii00125_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(casa_rope)
    casa_plan = bob_person.get_plan_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_plan.healerunit.set_healer_name(cleaners_str)
    csv_header = x_ideas.get("ii00125")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_ii00125_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    cleaners_row = f",,{exx.bob},{casa_rope},{cleaners_str},;\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_person_to_ii00126_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
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
    csv_header = x_ideas.get("ii00126")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_ii00126_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    mop_row = f",,{exx.bob},{mop_rope},{casa_rope},{clean_rope},{clean_reason_lower},{clean_reason_upper},{clean_reason_divisor},;\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_person_to_ii00127_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
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
    csv_header = x_ideas.get("ii00127")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_ii00127_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    casa_row = f",,{exx.bob},{mop_rope},{casa_rope},True,;\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_person_to_ii00128_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
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
    csv_header = x_ideas.get("ii00128")
    print(f"{csv_header=}")

    # WHEN
    bob_person.thinkout()
    x_csv = add_person_to_ii00128_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    root_row = f",,{exx.bob},,{a23_rope},,,,,,,,,1,False,False,;\n"
    mop_row = f",,{exx.bob},{mop_rope},{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_star},{casa_pledge},{casa_problem_bool},;\n"
    casa_row = f",,{exx.bob},{casa_rope},,,,,,,,,0,False,False,;\n"
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{mop_row}{casa_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_person_to_ii00129_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.credor_respect = 444
    bob_person.debtor_respect = 555
    bob_person.fund_pool = 777
    bob_person.max_tree_traverse = 3
    bob_person.fund_grain = 12
    bob_person.mana_grain = 13
    bob_person.respect_grain = 15
    csv_header = x_ideas.get("ii00129")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_person_to_ii00129_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    person_row = f",,{exx.a23},{exx.bob},{bob_person.credor_respect},{bob_person.debtor_respect},{bob_person.fund_pool},{bob_person.max_tree_traverse},{bob_person.fund_grain},{bob_person.mana_grain},{bob_person.respect_grain},;\n"
    assert x_csv == f"{csv_header}{person_row}"


def test_add_personunit_to_belief_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
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

    ii00120_header = x_ideas.get("ii00120")
    ii00121_header = x_ideas.get("ii00121")
    ii00122_header = x_ideas.get("ii00122")
    ii00123_header = x_ideas.get("ii00123")
    ii00124_header = x_ideas.get("ii00124")
    ii00125_header = x_ideas.get("ii00125")
    ii00126_header = x_ideas.get("ii00126")
    ii00127_header = x_ideas.get("ii00127")
    ii00128_header = x_ideas.get("ii00128")
    ii00129_header = x_ideas.get("ii00129")

    # WHEN
    bob_person.thinkout()
    add_personunit_to_belief_csv_strs(bob_person, x_ideas, csv_delimiter)

    # THEN
    assert x_ideas.get("ii00120") != ii00120_header
    assert x_ideas.get("ii00121") != ii00121_header
    assert x_ideas.get("ii00122") != ii00122_header
    assert x_ideas.get("ii00123") != ii00123_header
    # assert x_ideas.get("ii00124") != ii00124_header
    # assert x_ideas.get("ii00125") != ii00125_header
    assert x_ideas.get("ii00126") != ii00126_header
    assert x_ideas.get("ii00127") != ii00127_header
    assert x_ideas.get("ii00128") != ii00128_header
    assert x_ideas.get("ii00129") != ii00129_header
