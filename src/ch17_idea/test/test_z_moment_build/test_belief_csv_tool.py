from copy import deepcopy as copy_deepcopy
from src.ch00_py.file_toolbox import create_path
from src.ch02_contact.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.lesson_main import lessonunit_shop
from src.ch17_idea.idea_belief_csv import (
    add_momentunit_to_belief_csv_strs,
    add_momentunits_to_belief_csv_strs,
    add_person_to_ii00020_csv,
    add_person_to_ii00021_csv,
    add_person_to_ii00022_csv,
    add_person_to_ii00023_csv,
    add_person_to_ii00024_csv,
    add_person_to_ii00025_csv,
    add_person_to_ii00026_csv,
    add_person_to_ii00027_csv,
    add_person_to_ii00028_csv,
    add_person_to_ii00029_csv,
    add_personunit_to_belief_csv_strs,
    create_init_belief_idea_csv_strs,
)
from src.ch17_idea.idea_db_tool import get_ordered_csv
from src.ch17_idea.idea_main import moment_build_from_df
from src.ch17_idea.test._util.ch17_examples import (  # get_ex2_ii00006_df,
    J45_ROPE,
    get_ex2_ii00000_df,
    get_ex2_ii00001_df,
    get_ex2_ii00002_df,
    get_ex2_ii00003_df,
    get_ex2_ii00004_df,
    get_ex2_ii00005_df,
)
from src.ref.keywords import ExampleStrs as exx


def test_create_init_belief_idea_csv_strs_ReturnsObj_Scenario0_EmptyMomentUnit(
    temp3_fs,
):
    # ESTABLISH
    csv_delimiter = ","

    # WHEN
    x_ideas = create_init_belief_idea_csv_strs()

    # THEN
    expected_belief_csv_strs = {
        "ii00000": "moment_rope,epoch_label,c400_number,yr1_jan1_offset,monthday_index,fund_grain,mana_grain,respect_grain,knot,job_listen_rotations\n",
        "ii00001": "moment_rope,person_name,bud_time,knot,quota,celldepth\n",
        "ii00002": "moment_rope,person_name,contact_name,tran_time,amount,knot\n",
        "ii00003": "moment_rope,cumulative_minute,hour_label,knot\n",
        "ii00004": "moment_rope,cumulative_day,month_label,knot\n",
        "ii00005": "moment_rope,weekday_order,weekday_label,knot\n",
        # "ii00006": "moment_rope,offi_time,_offi_time_max\n",
        "ii00020": "moment_rope,person_name,contact_name,group_title,group_cred_lumen,group_debt_lumen,knot\n",
        "ii00021": "moment_rope,person_name,contact_name,contact_cred_lumen,contact_debt_lumen,knot\n",
        "ii00022": "person_name,plan_rope,awardee_title,give_force,take_force,knot\n",
        "ii00023": "person_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper,knot\n",
        "ii00024": "person_name,plan_rope,labor_title,solo,knot\n",
        "ii00025": "person_name,plan_rope,healer_name,knot\n",
        "ii00026": "person_name,plan_rope,reason_context,reason_state,reason_lower,reason_upper,reason_divisor,knot\n",
        "ii00027": "person_name,plan_rope,reason_context,active_requisite,knot\n",
        "ii00028": "person_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool,knot\n",
        "ii00029": "moment_rope,person_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,fund_grain,mana_grain,respect_grain,knot\n",
        "ii00042": "otx_title,inx_title,otx_knot,inx_knot,unknown_str\n",
        "ii00043": "otx_name,inx_name,otx_knot,inx_knot,unknown_str\n",
        "ii00044": "otx_label,inx_label,otx_knot,inx_knot,unknown_str\n",
        "ii00045": "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n",
    }
    expected_ii00000_csv = expected_belief_csv_strs.get("ii00000")
    expected_ii00001_csv = expected_belief_csv_strs.get("ii00001")
    expected_ii00002_csv = expected_belief_csv_strs.get("ii00002")
    expected_ii00003_csv = expected_belief_csv_strs.get("ii00003")
    expected_ii00004_csv = expected_belief_csv_strs.get("ii00004")
    expected_ii00005_csv = expected_belief_csv_strs.get("ii00005")
    # expected_ii00006_csv = expected_belief_csv_strs.get("ii00006")
    expected_ii00020_csv = expected_belief_csv_strs.get("ii00020")
    expected_ii00021_csv = expected_belief_csv_strs.get("ii00021")
    expected_ii00022_csv = expected_belief_csv_strs.get("ii00022")
    expected_ii00023_csv = expected_belief_csv_strs.get("ii00023")
    expected_ii00024_csv = expected_belief_csv_strs.get("ii00024")
    expected_ii00025_csv = expected_belief_csv_strs.get("ii00025")
    expected_ii00026_csv = expected_belief_csv_strs.get("ii00026")
    expected_ii00027_csv = expected_belief_csv_strs.get("ii00027")
    expected_ii00028_csv = expected_belief_csv_strs.get("ii00028")
    expected_ii00029_csv = expected_belief_csv_strs.get("ii00029")
    expected_ii00042_csv = expected_belief_csv_strs.get("ii00042")
    expected_ii00043_csv = expected_belief_csv_strs.get("ii00043")
    expected_ii00044_csv = expected_belief_csv_strs.get("ii00044")
    expected_ii00045_csv = expected_belief_csv_strs.get("ii00045")
    print(f"{expected_ii00001_csv=}")

    face_spark_str = "spark_num,spark_face,"
    assert x_ideas.get("ii00000") == f"{face_spark_str}{expected_ii00000_csv}"
    assert x_ideas.get("ii00001") == f"{face_spark_str}{expected_ii00001_csv}"
    assert x_ideas.get("ii00002") == f"{face_spark_str}{expected_ii00002_csv}"
    assert x_ideas.get("ii00003") == f"{face_spark_str}{expected_ii00003_csv}"
    assert x_ideas.get("ii00004") == f"{face_spark_str}{expected_ii00004_csv}"
    assert x_ideas.get("ii00005") == f"{face_spark_str}{expected_ii00005_csv}"
    # assert x_ideas.get("ii00006") == f"{face_spark_str}{expected_ii00006_csv}"
    print(f"{expected_ii00020_csv=}")
    print(x_ideas.get("ii00020"))
    assert x_ideas.get("ii00020") == f"{face_spark_str}{expected_ii00020_csv}"
    assert x_ideas.get("ii00021") == f"{face_spark_str}{expected_ii00021_csv}"
    assert x_ideas.get("ii00022") == f"{face_spark_str}{expected_ii00022_csv}"
    assert x_ideas.get("ii00023") == f"{face_spark_str}{expected_ii00023_csv}"
    assert x_ideas.get("ii00024") == f"{face_spark_str}{expected_ii00024_csv}"
    assert x_ideas.get("ii00025") == f"{face_spark_str}{expected_ii00025_csv}"
    assert x_ideas.get("ii00026") == f"{face_spark_str}{expected_ii00026_csv}"
    assert x_ideas.get("ii00027") == f"{face_spark_str}{expected_ii00027_csv}"
    assert x_ideas.get("ii00028") == f"{face_spark_str}{expected_ii00028_csv}"
    assert x_ideas.get("ii00029") == f"{face_spark_str}{expected_ii00029_csv}"
    assert x_ideas.get("ii00042") == f"{face_spark_str}{expected_ii00042_csv}"
    assert x_ideas.get("ii00043") == f"{face_spark_str}{expected_ii00043_csv}"
    assert x_ideas.get("ii00044") == f"{face_spark_str}{expected_ii00044_csv}"
    assert x_ideas.get("ii00045") == f"{face_spark_str}{expected_ii00045_csv}"
    assert len(x_ideas) == 20


def test_add_momentunit_to_belief_csv_strs_ReturnsObj_Scenario0_OneMomentUnit(
    temp3_fs,
):
    # ESTABLISH
    ii00000_df = get_ex2_ii00000_df()
    # print(f"{ii00000_df=}")
    ii00001_df = get_ex2_ii00001_df()
    ii00002_df = get_ex2_ii00002_df()
    ii00003_df = get_ex2_ii00003_df()
    ii00004_df = get_ex2_ii00004_df()
    ii00005_df = get_ex2_ii00005_df()
    # ii00006_df = get_ex2_ii00006_df()
    x_fund_grain = 1
    x_respect_grain = 1
    x_mana_grain = 1
    x_moments_dir = create_path(str(temp3_fs), "Fay")
    x_momentunits = moment_build_from_df(
        ii00000_df,
        ii00001_df,
        ii00002_df,
        ii00003_df,
        ii00004_df,
        ii00005_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )
    csv_delimiter = ","
    x_csvs = create_init_belief_idea_csv_strs()
    ii00_csv_header = x_csvs.get("ii00000")
    ii01_csv_header = x_csvs.get("ii00001")
    ii02_csv_header = x_csvs.get("ii00002")
    ii03_csv_header = x_csvs.get("ii00003")
    ii04_csv_header = x_csvs.get("ii00004")
    ii05_csv_header = x_csvs.get("ii00005")
    # ii06_csv_header = x_csvs.get("ii00006")
    a23_momentunit = x_momentunits.get(exx.a23_slash)

    # WHEN
    add_momentunit_to_belief_csv_strs(a23_momentunit, x_csvs, csv_delimiter)

    # THEN
    gen_ii00000_csv = x_csvs.get("ii00000")
    gen_ii00001_csv = x_csvs.get("ii00001")
    gen_ii00002_csv = x_csvs.get("ii00002")
    gen_ii00003_csv = x_csvs.get("ii00003")
    gen_ii00004_csv = x_csvs.get("ii00004")
    gen_ii00005_csv = x_csvs.get("ii00005")
    # gen_ii00006_csv = x_csvs.get("ii00006")
    expected_ii00000_csv = ",,/Amy23/,creg,7,440640,1,1,1,1,/,4\n"
    expected_ii00001_csv = ",,/Amy23/,Bob,999,/,332,3\n,,/Amy23/,Sue,777,/,445,3\n,,/Amy23/,Yao,222,/,700,3\n"
    expected_ii00002_csv = ",,/Amy23/,Bob,Zia,777,888,/\n,,/Amy23/,Sue,Zia,999,234,/\n,,/Amy23/,Yao,Zia,999,234,/\n,,/Amy23/,Zia,Bob,777,888,/\n"
    expected_ii00003_csv = ",,/Amy23/,60,12am,/\n,,/Amy23/,120,1am,/\n,,/Amy23/,180,2am,/\n,,/Amy23/,240,3am,/\n,,/Amy23/,300,4am,/\n,,/Amy23/,360,5am,/\n,,/Amy23/,420,6am,/\n,,/Amy23/,480,7am,/\n,,/Amy23/,540,8am,/\n,,/Amy23/,600,9am,/\n,,/Amy23/,660,10am,/\n,,/Amy23/,720,11am,/\n,,/Amy23/,780,12pm,/\n,,/Amy23/,840,1pm,/\n,,/Amy23/,900,2pm,/\n,,/Amy23/,960,3pm,/\n,,/Amy23/,1020,4pm,/\n,,/Amy23/,1080,5pm,/\n,,/Amy23/,1140,6pm,/\n,,/Amy23/,1200,7pm,/\n,,/Amy23/,1260,8pm,/\n,,/Amy23/,1320,9pm,/\n,,/Amy23/,1380,10pm,/\n,,/Amy23/,1440,11pm,/\n"
    expected_ii00004_csv = ",,/Amy23/,31,March,/\n,,/Amy23/,61,April,/\n,,/Amy23/,92,May,/\n,,/Amy23/,122,June,/\n,,/Amy23/,153,July,/\n,,/Amy23/,184,August,/\n,,/Amy23/,214,September,/\n,,/Amy23/,245,October,/\n,,/Amy23/,275,November,/\n,,/Amy23/,306,December,/\n,,/Amy23/,337,January,/\n,,/Amy23/,365,February,/\n"
    expected_ii00005_csv = ",,/Amy23/,0,Wednesday,/\n,,/Amy23/,1,Thursday,/\n,,/Amy23/,2,Friday,/\n,,/Amy23/,3,Saturday,/\n,,/Amy23/,4,Sunday,/\n,,/Amy23/,5,Monday,/\n,,/Amy23/,6,Tuesday,/\n"
    # expected_ii00006_csv = ",,/Amy23/,0,Wednesday\n,,/Amy23/,1,Thursday\n,,/Amy23/,2,Friday\n,,/Amy23/,3,Saturday\n,,/Amy23/,4,Sunday\n,,/Amy23/,5,Monday\n,,/Amy23/,6,Tuesday\n"

    # print(f"      {ii02_csv_header=}")
    print(f"      {gen_ii00005_csv=}")
    # print(f" {expected_ii00004_csv=}")
    # print(f"      {gen_ii00004_csv=}")
    # print(f"      {gen_ii00005_csv=}")
    assert gen_ii00000_csv == f"{ii00_csv_header}{expected_ii00000_csv}"
    assert gen_ii00001_csv == f"{ii01_csv_header}{expected_ii00001_csv}"
    assert gen_ii00002_csv == f"{ii02_csv_header}{expected_ii00002_csv}"
    assert gen_ii00003_csv == f"{ii03_csv_header}{expected_ii00003_csv}"
    assert gen_ii00004_csv == f"{ii04_csv_header}{expected_ii00004_csv}"
    assert gen_ii00005_csv == f"{ii05_csv_header}{expected_ii00005_csv}"
    # assert gen_ii00006_csv == f"{ii06_csv_header}{expected_ii00006_csv}"


def test_add_momentunits_to_belief_csv_strs_ReturnsObj_Scenario1_TwoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    ii00000_df = get_ex2_ii00000_df()
    ii00001_df = get_ex2_ii00001_df()
    ii00002_df = get_ex2_ii00002_df()
    ii00003_df = get_ex2_ii00003_df()
    ii00004_df = get_ex2_ii00004_df()
    ii00005_df = get_ex2_ii00005_df()
    x_fund_grain = 1
    x_respect_grain = 1
    x_mana_grain = 1
    x_moments_dir = create_path(str(temp3_fs), "Fay")
    x_momentunits = moment_build_from_df(
        ii00000_df,
        ii00001_df,
        ii00002_df,
        ii00003_df,
        ii00004_df,
        ii00005_df,
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
    expected_ii00000_csv = get_ordered_csv(get_ex2_ii00000_df())
    expected_ii00001_csv = get_ordered_csv(get_ex2_ii00001_df())
    expected_ii00002_csv = get_ordered_csv(get_ex2_ii00002_df())
    expected_ii00003_csv = get_ordered_csv(get_ex2_ii00003_df())
    expected_ii00004_csv = get_ordered_csv(get_ex2_ii00004_df())
    expected_ii00005_csv = get_ordered_csv(get_ex2_ii00005_df())
    expected_ii00000_csv = f"spark_num,spark_face,{expected_ii00000_csv}"
    expected_ii00001_csv = f"spark_num,spark_face,{expected_ii00001_csv}"
    expected_ii00002_csv = f"spark_num,spark_face,{expected_ii00002_csv}"
    expected_ii00003_csv = f"spark_num,spark_face,{expected_ii00003_csv}"
    expected_ii00004_csv = f"spark_num,spark_face,{expected_ii00004_csv}"
    expected_ii00005_csv = f"spark_num,spark_face,{expected_ii00005_csv}"
    x_rope = exx.a23_slash
    expected_ii00000_csv = expected_ii00000_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00001_csv = expected_ii00001_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00002_csv = expected_ii00002_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00003_csv = expected_ii00003_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00004_csv = expected_ii00004_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00005_csv = expected_ii00005_csv.replace(x_rope, f",,{x_rope}")
    expected_ii00000_csv = expected_ii00000_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00001_csv = expected_ii00001_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00002_csv = expected_ii00002_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00003_csv = expected_ii00003_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00004_csv = expected_ii00004_csv.replace(J45_ROPE, f",,{J45_ROPE}")
    expected_ii00005_csv = expected_ii00005_csv.replace(J45_ROPE, f",,{J45_ROPE}")

    assert len(x_ideas) == 20
    generated_ii00000_csv = x_ideas.get("ii00000")
    generated_ii00001_csv = x_ideas.get("ii00001")
    generated_ii00002_csv = x_ideas.get("ii00002")
    generated_ii00003_csv = x_ideas.get("ii00003")
    generated_ii00004_csv = x_ideas.get("ii00004")
    generated_ii00005_csv = x_ideas.get("ii00005")
    print(f"{generated_ii00001_csv=}")
    print(f" {expected_ii00001_csv=}")
    assert generated_ii00000_csv == expected_ii00000_csv
    assert generated_ii00001_csv == expected_ii00001_csv
    assert generated_ii00002_csv == expected_ii00002_csv
    assert len(generated_ii00003_csv) == len(expected_ii00003_csv)
    assert generated_ii00004_csv == expected_ii00004_csv
    assert generated_ii00005_csv == expected_ii00005_csv


def test_add_person_to_ii00020_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao)
    run_credit = 33
    run_debt = 55
    bob_person.get_contact(exx.yao).add_membership(exx.run, run_credit, run_debt)
    csv_header = x_ideas.get("ii00020")

    # WHEN
    x_csv = add_person_to_ii00020_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_yao_row = f",,{exx.a23},{exx.bob},{exx.yao},{exx.yao},1,1,;\n"
    yao_run_row = (
        f",,{exx.a23},{exx.bob},{exx.yao},{exx.run},{run_credit},{run_debt},;\n"
    )
    print(f"{x_csv=}")
    print(f"{yao_run_row=}")
    assert x_csv == f"{csv_header}{yao_yao_row}{yao_run_row}"


def test_add_person_to_ii00021_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    yao_credit = 33
    yao_debt = 55
    bob_person = personunit_shop(exx.bob, exx.a23)
    bob_person.add_contactunit(exx.yao, yao_credit, yao_debt)
    csv_header = x_ideas.get("ii00021")

    # WHEN
    x_csv = add_person_to_ii00021_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_row = f",,{exx.a23},{exx.bob},{exx.yao},{yao_credit},{yao_debt},;\n"
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_person_to_ii00022_csv_ReturnsObj():
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
    csv_header = x_ideas.get("ii00022")
    print(f"{csv_header=}")

    # WHEN
    bob_person.conpute()
    x_csv = add_person_to_ii00022_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    yao_award_row = (
        f",,{exx.bob},{casa_rope},{exx.yao},{yao_give_force},{yao_take_force},;\n"
    )
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_person_to_ii00023_csv_ReturnsObj():
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
    csv_header = x_ideas.get("ii00023")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_person_to_ii00023_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    clean_row = f",,{exx.bob},{a23_rope},{casa_rope},{clean_rope},{clean_fact_lower},{clean_fact_upper},;\n"
    assert x_csv == f"{csv_header}{clean_row}"


def test_add_person_to_ii00024_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(casa_rope)
    casa_plan = bob_person.get_plan_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_plan.workforceunit.add_labor(cleaners_str)
    csv_header = x_ideas.get("ii00024")
    print(f"{csv_header=}")

    # WHEN
    bob_person.conpute()
    x_csv = add_person_to_ii00024_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    cleaners_row = f",,{exx.bob},{casa_rope},{cleaners_str},;\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_person_to_ii00025_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_belief_idea_csv_strs()
    bob_person = personunit_shop(exx.bob, exx.a23)
    casa_rope = bob_person.make_l1_rope("casa")
    bob_person.add_plan(casa_rope)
    casa_plan = bob_person.get_plan_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_plan.healerunit.set_healer_name(cleaners_str)
    csv_header = x_ideas.get("ii00025")
    print(f"{csv_header=}")

    # WHEN
    bob_person.conpute()
    x_csv = add_person_to_ii00025_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    cleaners_row = f",,{exx.bob},{casa_rope},{cleaners_str},;\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_person_to_ii00026_csv_ReturnsObj():
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
    csv_header = x_ideas.get("ii00026")
    print(f"{csv_header=}")

    # WHEN
    bob_person.conpute()
    x_csv = add_person_to_ii00026_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    mop_row = f",,{exx.bob},{mop_rope},{casa_rope},{clean_rope},{clean_reason_lower},{clean_reason_upper},{clean_reason_divisor},;\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_person_to_ii00027_csv_ReturnsObj():
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
    csv_header = x_ideas.get("ii00027")
    print(f"{csv_header=}")

    # WHEN
    bob_person.conpute()
    x_csv = add_person_to_ii00027_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    casa_row = f",,{exx.bob},{mop_rope},{casa_rope},True,;\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_person_to_ii00028_csv_ReturnsObj():
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
    csv_header = x_ideas.get("ii00028")
    print(f"{csv_header=}")

    # WHEN
    bob_person.conpute()
    x_csv = add_person_to_ii00028_csv(csv_header, bob_person, csv_delimiter)

    # THEN
    root_row = f",,{exx.bob},,{a23_rope},,,,,,,,,1,False,False,;\n"
    mop_row = f",,{exx.bob},{mop_rope},{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_star},{casa_pledge},{casa_problem_bool},;\n"
    casa_row = f",,{exx.bob},{casa_rope},,,,,,,,,0,False,False,;\n"
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{mop_row}{casa_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_person_to_ii00029_csv_ReturnsObj():
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
    csv_header = x_ideas.get("ii00029")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_person_to_ii00029_csv(csv_header, bob_person, csv_delimiter)

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

    ii00020_header = x_ideas.get("ii00020")
    ii00021_header = x_ideas.get("ii00021")
    ii00022_header = x_ideas.get("ii00022")
    ii00023_header = x_ideas.get("ii00023")
    ii00024_header = x_ideas.get("ii00024")
    ii00025_header = x_ideas.get("ii00025")
    ii00026_header = x_ideas.get("ii00026")
    ii00027_header = x_ideas.get("ii00027")
    ii00028_header = x_ideas.get("ii00028")
    ii00029_header = x_ideas.get("ii00029")

    # WHEN
    bob_person.conpute()
    add_personunit_to_belief_csv_strs(bob_person, x_ideas, csv_delimiter)

    # THEN
    assert x_ideas.get("ii00020") != ii00020_header
    assert x_ideas.get("ii00021") != ii00021_header
    assert x_ideas.get("ii00022") != ii00022_header
    assert x_ideas.get("ii00023") != ii00023_header
    # assert x_ideas.get("ii00024") != ii00024_header
    # assert x_ideas.get("ii00025") != ii00025_header
    assert x_ideas.get("ii00026") != ii00026_header
    assert x_ideas.get("ii00027") != ii00027_header
    assert x_ideas.get("ii00028") != ii00028_header
    assert x_ideas.get("ii00029") != ii00029_header
