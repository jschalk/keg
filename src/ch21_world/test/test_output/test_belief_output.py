from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal
from shutil import copy2 as shutil_copy2
from src.ch00_py.file_toolbox import create_path, set_dir
from src.ch17_idea.idea_db_tool import get_sheet_names, save_sheet
from src.ch18_etl_config._ref.ch18_path import (
    create_belief0001_path,
    create_beliefs_dir_path,
)
from src.ch21_world.world import create_beliefs, idea_sheets_to_lynx_mstr, worlddir_shop
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


def test_create_beliefs_CreatesFile_Senario0_EmptyWorld(temp3_fs):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(str(temp3_fs), "output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), output_dir)
    idea_sheets_to_lynx_mstr(
        world_db_path=fay_wdir.get_world_db_path(),
        i_src_dir=fay_wdir.i_src_dir,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
    )
    fay_belief0001_path = create_belief0001_path(fay_wdir.output_dir)
    assert os_path_exists(fay_belief0001_path) is False

    # WHEN
    create_beliefs(
        fay_wdir.world_dir,
        fay_wdir.output_dir,
        fay_wdir.world_name,
        fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(fay_belief0001_path)


def test_create_beliefs_CreatesFile_Senario1_SingleSmallSpark(temp3_fs):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(str(temp3_fs), "output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00011_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    save_sheet(i_src_dir_file_path, "br00011_ex3", br00011_df)
    idea_sheets_to_lynx_mstr(
        world_db_path=fay_wdir.get_world_db_path(),
        i_src_dir=fay_wdir.i_src_dir,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
    )
    fay_belief0001_path = create_belief0001_path(fay_wdir.output_dir)
    assert os_path_exists(fay_belief0001_path) is False

    # WHEN
    create_beliefs(
        fay_wdir.world_dir,
        fay_wdir.output_dir,
        fay_wdir.world_name,
        fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(fay_belief0001_path)
    print(get_sheet_names(fay_belief0001_path))
    br00021_sheet_df = pandas_read_excel(fay_belief0001_path, "br00021")
    print(f"{br00021_sheet_df=}")
    assert br00021_sheet_df.iloc[0][kw.spark_face] == "Fay"


def test_create_beliefs_CreatesFile_Senario2_CreatedBeliefCanBeIdeasForOtherWorldDir(
    temp3_fs,
):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    fay_str = "Fay"
    fay_output_dir = create_path(str(temp3_fs), "Fay_output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), fay_output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00011_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    save_sheet(i_src_dir_file_path, "br00011_ex3", br00011_df)
    idea_sheets_to_lynx_mstr(
        world_db_path=fay_wdir.get_world_db_path(),
        i_src_dir=fay_wdir.i_src_dir,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
    )
    fay_belief0001_path = create_belief0001_path(fay_wdir.output_dir)
    create_beliefs(
        world_dir=fay_wdir.world_dir,
        output_dir=fay_wdir.output_dir,
        world_name=fay_wdir.world_name,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )
    bob_output_dir = create_path(str(temp3_fs), "Bob_output")
    bob_wdir = worlddir_shop("Bob", str(temp3_fs), bob_output_dir)
    bob_i_src_dir_st0001_path = create_path(
        bob_wdir.moment_mstr_dir, "Bob_i_src_dir.xlsx"
    )
    set_dir(create_beliefs_dir_path(bob_wdir.moment_mstr_dir))
    shutil_copy2(fay_belief0001_path, dst=bob_i_src_dir_st0001_path)
    # print(f" {pandas_read_excel(fay_belief0001_path)=}")
    # print(f"{pandas_read_excel(bob_i_src_dir_st0001_path)=}")
    print(f"{bob_i_src_dir_st0001_path=}")
    print(f"{get_sheet_names(bob_i_src_dir_st0001_path)=}")
    idea_sheets_to_lynx_mstr(
        world_db_path=fay_wdir.get_world_db_path(),
        i_src_dir=fay_wdir.i_src_dir,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
    )
    bob_belief0001_path = create_belief0001_path(bob_wdir.output_dir)
    assert os_path_exists(bob_belief0001_path) is False

    # WHEN
    create_beliefs(
        bob_wdir.world_dir,
        bob_wdir.output_dir,
        bob_wdir.world_name,
        bob_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(bob_belief0001_path)
    print(f"{get_sheet_names(bob_belief0001_path)=}")
    for sheetname in get_sheet_names(bob_belief0001_path):
        print(f"comparing {sheetname=}...")
        fay_sheet_df = pandas_read_excel(fay_belief0001_path, sheetname)
        bob_sheet_df = pandas_read_excel(fay_belief0001_path, sheetname)
        # if sheetname == "br00021":
        #     print(f"{fay_sheet_df=}")
        #     print(f"{bob_sheet_df=}")
        assert_frame_equal(fay_sheet_df, bob_sheet_df)


def test_create_beliefs_CreatesFile_Senario3_Create_calendar_markdown(
    temp3_fs,
):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(str(temp3_fs), "output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
    br00011_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    save_sheet(i_src_dir_file_path, "br00011_ex3", br00011_df)
    idea_sheets_to_lynx_mstr(
        world_db_path=fay_wdir.get_world_db_path(),
        i_src_dir=fay_wdir.i_src_dir,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
    )

    a23_calendar_md_path = create_path(output_dir, "Amy23_calendar.md")
    print(f"      {a23_calendar_md_path=}")
    assert not os_path_exists(a23_calendar_md_path)

    # WHEN
    create_beliefs(
        fay_wdir.world_dir,
        fay_wdir.output_dir,
        fay_wdir.world_name,
        fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(a23_calendar_md_path)


# def test_WorldDir_sheets_i_src_dir_to_lynx_CreatesFiles(temp3_fs):
#     # ESTABLISH
#     fay_str = "Fay"
#     fay_wdir = worlddir_shop(fay_str, str(temp3_fs))
#     # delete_dir(fay_wdir.worlds_dir)
#     spark1 = 1
#     spark2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "Faybob.xlsx"
#     i_src_dir_file_path = create_path(fay_wdir.i_src_dir, ex_filename)
#     br00003_columns = [
#         kw.spark_face,
#         kw.spark_num,
#         kw.cumulative_minute,
#         kw.moment_rope,
#         kw.hour_label,
#     ]
#     br00001_columns = [
#         kw.spark_face,
#         kw.spark_num,
#         kw.moment_rope,
#         kw.person_name,
#         bud_time(),
#         kw.quota,
#         kw.celldepth,
#     ]
#     exx.a23 = exx.a23
#     tp37 = 37
#     sue_quota = 235
#     sue_celldepth = 3
#     br1row0 = [spark2, exx.sue, exx.a23, exx.sue, tp37, sue_quota, sue_celldepth]
#     br00001_1df = DataFrame([br1row0], columns=br00001_columns)
#     br00001_ex0_str = "example0_br00001"
#     save_sheet(i_src_dir_file_path, br00001_ex0_str, br00001_1df)

#     br3row0 = [spark1, exx.sue,  minute_360, exx.a23, hour6am]
#     br3row1 = [spark1, exx.sue,  minute_420, exx.a23, hour7am]
#     br3row2 = [spark2, exx.sue, minute_420, exx.a23, hour7am]
#     br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
#     br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex3_str = "example3_br00003"
#     save_sheet(i_src_dir_file_path, br00003_ex1_str, br00003_1df)
#     save_sheet(i_src_dir_file_path, br00003_ex3_str, br00003_3df)
#     br00011_columns = [
#         kw.spark_face,
#         kw.spark_num,
#         kw.moment_rope,
#         kw.person_name,
#         kw.contact_name,
#     ]
#     br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     save_sheet(i_src_dir_file_path, "br00011_ex3", br00011_df)
#     mstr_dir = fay_wdir.moment_mstr_dir
#     wrong_a23_moment_dir = create_path(mstr_dir, exx.a23)
#     assert os_path_exists(wrong_a23_moment_dir) is False
#     a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
#     a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, exx.sue)
#     a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, exx.sue)
#     sue37_mandate_path = bud_mandate(mstr_dir, a23_lasso, exx.sue, tp37)
#     assert os_path_exists(i_src_dir_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_gut_path) is False
#     assert os_path_exists(a23_sue_job_path) is False
#     assert os_path_exists(sue37_mandate_path) is False
#     assert count_dirs_files(fay_wdir.worlds_dir) == 7

#     # WHEN
# idea_sheets_to_lynx_mstr(
#     world_db_path=fay_wdir.get_world_db_path(),
#     i_src_dir=fay_wdir.i_src_dir,
#     moment_mstr_dir=fay_wdir.moment_mstr_dir,
# )

#     # THEN
#     assert os_path_exists(wrong_a23_moment_dir) is False
#     brick_file_path = create_path(fay_wdir.brick_dir, "br00003.xlsx")
#     assert os_path_exists(i_src_dir_file_path)
#     assert os_path_exists(brick_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_gut_path)
#     assert os_path_exists(a23_sue_job_path)
#     assert os_path_exists(sue37_mandate_path)
#     assert count_dirs_files(fay_wdir.worlds_dir) == 91
