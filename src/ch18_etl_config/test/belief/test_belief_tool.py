from ch00_py.file_toolbox import create_path, set_dir
from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.lasso import lassounit_shop
from ch09_person_lesson.lesson_filehandler import save_gut_file
from ch14_moment.moment_main import momentunit_shop, save_moment_file
from ch17_idea.idea_belief_csv import (
    add_momentunit_to_belief_csv_strs,
    add_personunit_to_belief_csv_strs,
    create_init_belief_idea_csv_strs,
)
from ch17_idea.idea_db_tool import get_sheet_names
from ch18_etl_config._ref.ch18_path import (
    create_belief0001_path,
    create_moment_mstr_path,
    create_world_db_path,
)
from ch18_etl_config.belief_tool import collect_belief_csv_strs, create_belief0001_file
from ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)
from os.path import exists as os_path_exists
from pandas import read_excel as pandas_read_excel
from ref.keywords import Ch18Keywords as kw, ExampleStrs as exx
from sqlite3 import connect as sqlite3_connect


def test_collect_belief_csv_strs_ReturnsObj_Scenario0_NoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)

    # WHEN
    gen_belief_csv_strs = collect_belief_csv_strs(world_dir)

    # THEN
    expected_belief_csv_strs = create_init_belief_idea_csv_strs()
    assert gen_belief_csv_strs == expected_belief_csv_strs


def test_collect_belief_csv_strs_ReturnsObj_Scenario1_SingleMomentUnit_NoPersonUnits(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    save_moment_file(a23_moment, a23_lasso)

    # WHEN
    gen_belief_csv_strs = collect_belief_csv_strs(world_dir)

    # THEN
    expected_belief_csv_strs = create_init_belief_idea_csv_strs()
    add_momentunit_to_belief_csv_strs(a23_moment, expected_belief_csv_strs, ",")
    assert gen_belief_csv_strs == expected_belief_csv_strs


def test_collect_belief_csv_strs_ReturnsObj_Scenario2_gut_PersonUnits(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    save_moment_file(a23_moment, a23_lasso)
    # create two gut file
    bob_gut = personunit_shop(exx.bob, exx.a23)
    yao_gut = personunit_shop(exx.yao, exx.a23)
    bob_gut.add_contactunit(exx.yao, 44, 55)
    bob_gut.add_contactunit(exx.yao, 44, 55)
    save_gut_file(moment_mstr_dir, bob_gut)

    # WHEN
    gen_belief_csv_strs = collect_belief_csv_strs(world_dir)

    # THEN
    expected_belief_csv_strs = create_init_belief_idea_csv_strs()
    add_momentunit_to_belief_csv_strs(a23_moment, expected_belief_csv_strs, ",")
    add_personunit_to_belief_csv_strs(bob_gut, expected_belief_csv_strs, ",")
    expected_ii00120_csv_str = expected_belief_csv_strs.get("ii00120")
    gen_ii00120_csv_str = gen_belief_csv_strs.get("ii00120")
    print(f"{expected_ii00120_csv_str=}")
    print(f"     {gen_ii00120_csv_str=}")
    assert gen_ii00120_csv_str == expected_ii00120_csv_str
    assert gen_belief_csv_strs == expected_belief_csv_strs


def test_collect_belief_csv_strs_ReturnsObj_Scenario3_TranslateRowsInDB(
    temp3_fs,
):
    # ESTABLISH database with translate data
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    spark1 = 1
    spark7 = 7
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = str(temp3_fs)
    output_dir = create_path(str(temp3_fs), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, kw.s_vld)
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.spark_face}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({kw.spark_face}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
        VALUES
          ('{sue_otx}', '{exx.slash}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{exx.slash}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)
    db_conn.close()

    # WHEN
    gen_belief_csv_strs = collect_belief_csv_strs(world_dir)

    # THEN
    assert gen_belief_csv_strs
    generated_belief_csv_keys = set(gen_belief_csv_strs.keys())
    print(f"{generated_belief_csv_keys=}")
    belief_csv_strs = create_init_belief_idea_csv_strs()
    assert generated_belief_csv_keys == set(belief_csv_strs.keys())
    ii00142_str = "ii00142"
    ii00143_str = "ii00143"
    ii00144_str = "ii00144"
    ii00145_str = "ii00145"
    ii00142_csv = gen_belief_csv_strs.get(ii00142_str)
    ii00143_csv = gen_belief_csv_strs.get(ii00143_str)
    ii00144_csv = gen_belief_csv_strs.get(ii00144_str)
    ii00145_csv = gen_belief_csv_strs.get(ii00145_str)

    expected_ii00142_csv = (
        "spark_num,spark_face,otx_title,inx_title,otx_knot,inx_knot,unknown_str\n"
    )
    expected_ii00143_csv = f"""spark_num,spark_face,otx_name,inx_name,otx_knot,inx_knot,unknown_str
,{bob_otx},{bob_otx},{bob_inx},{exx.slash},{colon_str},{bob_unknown_str}
,{sue_otx},{sue_otx},{sue_inx},{exx.slash},{colon_str},{sue_unknown_str}
"""
    expected_ii00144_csv = (
        "spark_num,spark_face,otx_label,inx_label,otx_knot,inx_knot,unknown_str\n"
    )
    expected_ii00145_csv = (
        "spark_num,spark_face,otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n"
    )
    assert ii00142_csv == expected_ii00142_csv
    assert ii00143_csv == expected_ii00143_csv
    assert ii00144_csv == expected_ii00144_csv
    assert ii00145_csv == expected_ii00145_csv


# TODO change collect_belief_csv_strs so that if it's passed a person_name it only collects that person's beliefs
def test_collect_belief_csv_strs_ReturnsObj_Scenario4_TranslateRowsInDB(
    temp3_fs,
):
    # ESTABLISH database with translate data
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    spark1 = 1
    spark7 = 7
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = str(temp3_fs)
    output_dir = create_path(str(temp3_fs), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, kw.s_vld)
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.spark_face}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({kw.spark_face}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
        VALUES
          ('{sue_otx}', '{exx.slash}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{exx.slash}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)
    db_conn.close()

    # WHEN
    gen_belief_csv_strs = collect_belief_csv_strs(world_dir)

    # THEN
    assert gen_belief_csv_strs
    generated_belief_csv_keys = set(gen_belief_csv_strs.keys())
    print(f"{generated_belief_csv_keys=}")
    belief_csv_strs = create_init_belief_idea_csv_strs()
    assert generated_belief_csv_keys == set(belief_csv_strs.keys())
    ii00142_str = "ii00142"
    ii00143_str = "ii00143"
    ii00144_str = "ii00144"
    ii00145_str = "ii00145"
    ii00142_csv = gen_belief_csv_strs.get(ii00142_str)
    ii00143_csv = gen_belief_csv_strs.get(ii00143_str)
    ii00144_csv = gen_belief_csv_strs.get(ii00144_str)
    ii00145_csv = gen_belief_csv_strs.get(ii00145_str)

    expected_ii00142_csv = (
        "spark_num,spark_face,otx_title,inx_title,otx_knot,inx_knot,unknown_str\n"
    )
    expected_ii00143_csv = f"""spark_num,spark_face,otx_name,inx_name,otx_knot,inx_knot,unknown_str
,{bob_otx},{bob_otx},{bob_inx},{exx.slash},{colon_str},{bob_unknown_str}
,{sue_otx},{sue_otx},{sue_inx},{exx.slash},{colon_str},{sue_unknown_str}
"""
    expected_ii00144_csv = (
        "spark_num,spark_face,otx_label,inx_label,otx_knot,inx_knot,unknown_str\n"
    )
    expected_ii00145_csv = (
        "spark_num,spark_face,otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n"
    )
    assert ii00142_csv == expected_ii00142_csv
    assert ii00143_csv == expected_ii00143_csv
    assert ii00144_csv == expected_ii00144_csv
    assert ii00145_csv == expected_ii00145_csv


def test_create_belief0001_file_CreatesFile_Scenario0_NoMomentUnits(
    temp3_fs,
):
    # ESTABLISH
    world_dir = str(temp3_fs)
    output_dir = create_path(world_dir, "output")
    belief0001_path = create_belief0001_path(output_dir)
    assert os_path_exists(belief0001_path) is False

    # WHEN
    create_belief0001_file(world_dir, output_dir, exx.sue)

    # THEN
    assert os_path_exists(belief0001_path)
    bob_belief0001_sheetnames = get_sheet_names(belief0001_path)
    belief_csv_strs = create_init_belief_idea_csv_strs()
    assert set(bob_belief0001_sheetnames) == set(belief_csv_strs.keys())


def test_create_belief0001_file_CreatesFile_Scenario1_TranslateRowsInDB(
    temp3_fs,
):
    # ESTABLISH database with translate data
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    spark1 = 1
    spark7 = 7
    colon_str = ":"
    sue_unknown_str = "SueUnknown"
    bob_unknown_str = "BobUnknown"
    world_dir = str(temp3_fs)
    output_dir = create_path(str(temp3_fs), "output")
    world_db_path = create_world_db_path(world_dir)
    print(f"{world_db_path=}")
    set_dir(world_dir)

    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, kw.s_vld)
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.spark_face}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({kw.spark_face}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
        VALUES
          ('{sue_otx}', '{exx.slash}', '{colon_str}', '{sue_unknown_str}')
        , ('{bob_otx}', '{exx.slash}', '{colon_str}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)
    db_conn.close()

    belief0001_path = create_belief0001_path(output_dir)
    assert os_path_exists(belief0001_path) is False

    # WHEN
    create_belief0001_file(world_dir, output_dir, exx.yao, False)

    # THEN
    assert os_path_exists(belief0001_path)
    bob_belief0001_sheetnames = get_sheet_names(belief0001_path)
    print(f"{bob_belief0001_sheetnames=}")
    belief_csv_strs = create_init_belief_idea_csv_strs()
    assert set(bob_belief0001_sheetnames) == set(belief_csv_strs.keys())
    ii00142_str = "ii00142"
    ii00143_str = "ii00143"
    ii00144_str = "ii00144"
    ii00145_str = "ii00145"
    ii00142_df = pandas_read_excel(belief0001_path, ii00142_str)
    ii00143_df = pandas_read_excel(belief0001_path, ii00143_str)
    ii00144_df = pandas_read_excel(belief0001_path, ii00144_str)
    ii00145_df = pandas_read_excel(belief0001_path, ii00145_str)
    assert len(ii00142_df) == 0
    assert len(ii00143_df) == 2
    assert len(ii00144_df) == 0
    assert len(ii00145_df) == 0
