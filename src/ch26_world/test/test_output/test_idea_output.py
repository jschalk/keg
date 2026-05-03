from ch00_py.file_toolbox import create_path, set_dir
from ch17_brick.brick_db_tool import get_sheet_names, save_sheet
from ch18_etl_config._ref.ch18_path import create_ideas_dir_path
from ch24_idea_dst._ref.ch24_path import create_idea0001_path
from ch26_world.world import brick_sheets_to_mind_mstr, create_ideas, worlddir_shop
from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal
from ref.keywords import Ch26Keywords as kw, ExampleStrs as exx
from shutil import copy2 as shutil_copy2


def test_create_ideas_CreatesFile_Senario0_EmptyWorld(temp3_fs):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(str(temp3_fs), "output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), output_dir)
    brick_sheets_to_mind_mstr(fay_wdir)
    fay_idea0001_path = create_idea0001_path(fay_wdir.output_dir)
    assert os_path_exists(fay_idea0001_path) is False

    # WHEN
    create_ideas(
        fay_wdir.world_dir,
        fay_wdir.output_dir,
        fay_wdir.world_name,
        fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(fay_idea0001_path)


def test_create_ideas_CreatesFile_Senario1_SingleSmallSpark(temp3_fs):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(str(temp3_fs), "output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00001_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    bk00001_df = DataFrame(bk00001_rows, columns=bk00001_columns)
    save_sheet(b_src_dir_file_path, "bk00001_ex3", bk00001_df)
    brick_sheets_to_mind_mstr(fay_wdir)
    fay_idea0001_path = create_idea0001_path(fay_wdir.output_dir)
    assert os_path_exists(fay_idea0001_path) is False

    # WHEN
    create_ideas(
        fay_wdir.world_dir,
        fay_wdir.output_dir,
        fay_wdir.world_name,
        fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(fay_idea0001_path)
    print(get_sheet_names(fay_idea0001_path))
    bk00121_sheet_df = pandas_read_excel(fay_idea0001_path, "bk00121")
    print(f"{bk00121_sheet_df=}")
    assert bk00121_sheet_df.iloc[0][kw.spark_face] == "Fay"


def test_create_ideas_CreatesFile_Senario2_CreatedIdeaCanBeBricksForOtherWorldDir(
    temp3_fs,
):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    fay_str = "Fay"
    fay_output_dir = create_path(str(temp3_fs), "Fay_output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), fay_output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00001_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    bk00001_df = DataFrame(bk00001_rows, columns=bk00001_columns)
    save_sheet(b_src_dir_file_path, "bk00001_ex3", bk00001_df)
    brick_sheets_to_mind_mstr(fay_wdir)
    fay_idea0001_path = create_idea0001_path(fay_wdir.output_dir)
    create_ideas(
        world_dir=fay_wdir.world_dir,
        output_dir=fay_wdir.output_dir,
        world_name=fay_wdir.world_name,
        moment_mstr_dir=fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )
    bob_output_dir = create_path(str(temp3_fs), "Bob_output")
    bob_wdir = worlddir_shop("Bob", str(temp3_fs), bob_output_dir)
    bob_b_src_dir_st0001_path = create_path(
        bob_wdir.moment_mstr_dir, "Bob_b_src_dir.xlsx"
    )
    set_dir(create_ideas_dir_path(bob_wdir.moment_mstr_dir))
    shutil_copy2(fay_idea0001_path, dst=bob_b_src_dir_st0001_path)
    # print(f" {pandas_read_excel(fay_idea0001_path)=}")
    # print(f"{pandas_read_excel(bob_b_src_dir_st0001_path)=}")
    print(f"{bob_b_src_dir_st0001_path=}")
    print(f"{get_sheet_names(bob_b_src_dir_st0001_path)=}")
    brick_sheets_to_mind_mstr(fay_wdir)
    bob_idea0001_path = create_idea0001_path(bob_wdir.output_dir)
    assert os_path_exists(bob_idea0001_path) is False

    # WHEN
    create_ideas(
        bob_wdir.world_dir,
        bob_wdir.output_dir,
        bob_wdir.world_name,
        bob_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(bob_idea0001_path)
    print(f"{get_sheet_names(bob_idea0001_path)=}")
    for sheetname in get_sheet_names(bob_idea0001_path):
        print(f"comparing {sheetname=}...")
        fay_sheet_df = pandas_read_excel(fay_idea0001_path, sheetname)
        bob_sheet_df = pandas_read_excel(fay_idea0001_path, sheetname)
        # if sheetname == "bk00121":
        #     print(f"{fay_sheet_df=}")
        #     print(f"{bob_sheet_df=}")
        assert_frame_equal(fay_sheet_df, bob_sheet_df)


def test_create_ideas_CreatesFile_Senario3_Create_calendar_markdown(
    temp3_fs,
):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(str(temp3_fs), "output")
    fay_wdir = worlddir_shop(fay_str, str(temp3_fs), output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
    bk00001_columns = [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
    ]
    bk00001_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    bk00001_df = DataFrame(bk00001_rows, columns=bk00001_columns)
    save_sheet(b_src_dir_file_path, "bk00001_ex3", bk00001_df)
    brick_sheets_to_mind_mstr(fay_wdir)
    a23_calendar_md_path = create_path(output_dir, "Amy23_calendar.md")
    print(f"      {a23_calendar_md_path=}")
    assert not os_path_exists(a23_calendar_md_path)

    # WHEN
    create_ideas(
        fay_wdir.world_dir,
        fay_wdir.output_dir,
        fay_wdir.world_name,
        fay_wdir.moment_mstr_dir,
        prettify_excel_bool=False,
    )

    # THEN
    assert os_path_exists(a23_calendar_md_path)


# def test_WorldDir_sheets_b_src_dir_to_mind_CreatesFiles(temp3_fs):
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
#     b_src_dir_file_path = create_path(fay_wdir.bricks_src_dir, ex_filename)
#     bk00103_columns = [
#         kw.spark_face,
#         kw.spark_num,
#         kw.cumulative_minute,
#         kw.moment_rope,
#         kw.hour_label,
#     ]
#     bk00101_columns = [
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
#     bk1row0 = [spark2, exx.sue, exx.a23, exx.sue, tp37, sue_quota, sue_celldepth]
#     bk00101_1df = DataFrame([bk1row0], columns=bk00101_columns)
#     bk00101_ex0_str = "example0_bk00101"
#     save_sheet(b_src_dir_file_path, bk00101_ex0_str, bk00101_1df)

#     bk3row0 = [spark1, exx.sue,  minute_360, exx.a23, hour6am]
#     bk3row1 = [spark1, exx.sue,  minute_420, exx.a23, hour7am]
#     bk3row2 = [spark2, exx.sue, minute_420, exx.a23, hour7am]
#     bk00103_1df = DataFrame([bk3row0, bk3row1], columns=bk00103_columns)
#     bk00103_3df = DataFrame([bk3row1, bk3row0, bk3row2], columns=bk00103_columns)
#     bk00103_ex1_str = "example1_bk00103"
#     bk00103_ex3_str = "example3_bk00103"
#     save_sheet(b_src_dir_file_path, bk00103_ex1_str, bk00103_1df)
#     save_sheet(b_src_dir_file_path, bk00103_ex3_str, bk00103_3df)
#     bk00001_columns = [
#         kw.spark_face,
#         kw.spark_num,
#         kw.moment_rope,
#         kw.person_name,
#         kw.contact_name,
#     ]
#     bk00001_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
#     bk00001_df = DataFrame(bk00001_rows, columns=bk00001_columns)
#     save_sheet(b_src_dir_file_path, "bk00001_ex3", bk00001_df)
#     mstr_dir = fay_wdir.moment_mstr_dir
#     wrong_a23_moment_dir = create_path(mstr_dir, exx.a23)
#     assert os_path_exists(wrong_a23_moment_dir) is False
#     a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
#     a23_sue_gut_path = create_gut_path(mstr_dir, a23_lasso, exx.sue)
#     a23_sue_job_path = create_job_path(mstr_dir, a23_lasso, exx.sue)
#     sue37_mandate_path = bud_mandate(mstr_dir, a23_lasso, exx.sue, tp37)
#     assert os_path_exists(b_src_dir_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_gut_path) is False
#     assert os_path_exists(a23_sue_job_path) is False
#     assert os_path_exists(sue37_mandate_path) is False
#     assert count_dirs_files(fay_wdir.worlds_dir) == 7

#     # WHEN
# brick_sheets_to_mind_mstr(
#     world_db_path=fay_wdir.get_world_db_path(),
#     b_src_dir=fay_wdir.bricks_src_dir,
#     moment_mstr_dir=fay_wdir.moment_mstr_dir,
# )

#     # THEN
#     assert os_path_exists(wrong_a23_moment_dir) is False
#     b_src_file_path = create_path(fay_wdir.bricks_src_dir, "bk00103.xlsx")
#     assert os_path_exists(b_src_dir_file_path)
#     assert os_path_exists(brick_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_gut_path)
#     assert os_path_exists(a23_sue_job_path)
#     assert os_path_exists(sue37_mandate_path)
#     assert count_dirs_files(fay_wdir.worlds_dir) == 91
