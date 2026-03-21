from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import (
    count_files,
    create_path,
    get_level1_dirs,
    save_json,
)
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch13_time.epoch_main import epochunit_shop
from src.ch13_time.test._util.ch13_examples import (
    get_creg_config,
    get_expected_creg_year0_markdown,
)
from src.ch14_moment.moment_main import momentunit_shop
from src.ch20_kpi.kpi_mstr import create_calendar_markdown_files
from src.ch20_kpi.test._util.ch20_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import ExampleStrs as exx


def test_create_calendar_markdown_files_Senario0_NoFileIfWorldIsEmpty(
    temp_dir_setup,
):
    # ESTABLISH
    temp_dir = get_temp_dir()
    moment_mstr_dir = create_path(temp_dir, "moment_mstr")
    output_dir = create_path(temp_dir, "output")
    assert not os_path_exists(output_dir)

    # WHEN
    create_calendar_markdown_files(moment_mstr_dir, output_dir)

    # THEN
    assert os_path_exists(output_dir)
    assert count_files(output_dir) == 0


def test_create_calendar_markdown_files_Senario1_CreatesFileFromMomentUnitJSON(
    temp_dir_setup,
):
    # ESTABLISH
    temp_dir = get_temp_dir()
    moment_mstr_dir = create_path(temp_dir, "moment_mstr")
    output_dir = create_path(temp_dir, "output")
    a23_lasso = lassounit_shop(exx.a23)
    a23_moment_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    a23_momentunit = momentunit_shop(exx.a23, moment_mstr_dir)
    assert a23_momentunit.epoch == epochunit_shop(get_creg_config())
    save_json(a23_moment_path, None, a23_momentunit.to_dict())
    a23_calendar_md_path = create_path(output_dir, "Amy23_calendar.md")
    print(f"{a23_calendar_md_path=}")
    moments_dir = create_path(moment_mstr_dir, "moments")
    print(f"{get_level1_dirs(moments_dir)=}")
    assert not os_path_exists(a23_calendar_md_path)

    # WHEN
    create_calendar_markdown_files(moment_mstr_dir, output_dir)

    # THEN
    assert os_path_exists(a23_calendar_md_path)
    expected_csv_str = get_expected_creg_year0_markdown()
    assert open(a23_calendar_md_path).read() == expected_csv_str


# def test_create_calendar_markdown_files_Senario1_Add_CreatesFile(
#     temp_dir_setup,
# ):
#     # ESTABLISH
#     fay_str = "Fay"
#     output_dir = create_path(worlds_dir(), "output")
#     fay_wdir = shop(fay_str, worlds_dir(), output_dir)
#     spark2 = 2
#     ex_filename = "Faybob.xlsx"
#     input_file_path = create_path(fay_wdir._input_dir, ex_filename)
#     exx.a23 = exx.a23
#     br00011_columns = [
#         kw.spark_num,
#         kw.face_name,
#         kw.moment_rope,
#         kw.person_name,
#         kw.partner_name
#     ]
#     br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
#     fay_wdir.sheets_input_to_clarity_mstr()

#     a23_calendar_md_path = create_path(output_dir, f"{exx.a23}_calendar.md")
#     print(f"      {a23_calendar_md_path=}")
#     assert not os_path_exists(a23_calendar_md_path)

#     # WHEN
#     fay_wdir.create_calendar_markdown_files()

#     # THEN
#     assert os_path_exists(a23_calendar_md_path)
#     expected_csv_str = "moment_rope,person_name,funds,fund_rank,pledges_count\n"
#     assert open(a23_calendar_md_path).read() == expected_csv_str
