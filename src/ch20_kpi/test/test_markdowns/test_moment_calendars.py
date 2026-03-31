from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import (
    count_files,
    create_path,
    get_level1_dirs,
    save_json,
)
from src.ch09_person_lesson._ref.ch09_path import (
    create_moment_json_path,
    create_moments_dir_path,
)
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch13_time.epoch_main import epochunit_shop
from src.ch13_time.test._util.ch13_examples import (
    get_creg_config,
    get_expected_creg_year0_markdown,
)
from src.ch14_moment.moment_main import momentunit_shop
from src.ch20_kpi.kpi_mstr import create_calendar_markdown_files
from src.ref.keywords import ExampleStrs as exx


def test_create_calendar_markdown_files_Senario0_NoFileIfWorldIsEmpty(temp3_fs):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    moment_mstr_dir = create_path(temp_dir, "moment_mstr")
    output_dir = create_path(temp_dir, "output")
    assert not os_path_exists(output_dir)

    # WHEN
    create_calendar_markdown_files(moment_mstr_dir, output_dir)

    # THEN
    assert os_path_exists(output_dir)
    assert count_files(output_dir) == 0


def test_create_calendar_markdown_files_Senario1_CreatesFileFromMomentUnitJSON(
    temp3_fs,
):
    # ESTABLISH
    temp_dir = str(temp3_fs)
    moment_mstr_dir = create_path(temp_dir, "moment_mstr")
    output_dir = create_path(temp_dir, "output")
    a23_lasso = lassounit_shop(exx.a23)
    a23_moment_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    a23_momentunit = momentunit_shop(exx.a23, moment_mstr_dir)
    assert a23_momentunit.epoch == epochunit_shop(get_creg_config())
    save_json(a23_moment_path, None, a23_momentunit.to_dict())
    a23_calendar_md_path = create_path(output_dir, "Amy23_calendar.md")
    print(f"{a23_calendar_md_path=}")
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    print(f"{get_level1_dirs(moments_dir)=}")
    assert not os_path_exists(a23_calendar_md_path)

    # WHEN
    create_calendar_markdown_files(moment_mstr_dir, output_dir)

    # THEN
    assert os_path_exists(a23_calendar_md_path)
    expected_csv_str = get_expected_creg_year0_markdown()
    assert open(a23_calendar_md_path).read() == expected_csv_str
