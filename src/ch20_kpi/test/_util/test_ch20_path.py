from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import create_rope
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch20_kpi._ref.ch20_path import (
    create_day_report_txt_path,
    create_moments_dir_path,
)
from src.ch20_kpi.test._util.ch20_env import get_temp_dir
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_create_day_report_txt_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_bob_day_report_txt_path = create_day_report_txt_path(
        x_moment_mstr_dir, a23_lasso, exx.bob
    )

    # THEN
    moments_dir = create_moments_dir_path(x_moment_mstr_dir)
    moment_path = create_path(moments_dir, a23_lasso.make_path())
    day_reports_dir = create_path(moment_path, "day_reports")
    expected_bob_day_report_txt_path = create_path(day_reports_dir, f"{exx.bob}.txt")
    assert gen_bob_day_report_txt_path == expected_bob_day_report_txt_path


LINUX_OS = platform_system() == "Linux"


def test_create_day_report_txt_path_HasDocString():
    # ESTABLISH
    x_moment_mstr_dir = "moment_mstr_dir"
    moment_rope_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_day_report_txt_path(
        x_moment_mstr_dir, moment_rope_lasso, kw.person_name
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_day_report_txt_path) == doc_str
