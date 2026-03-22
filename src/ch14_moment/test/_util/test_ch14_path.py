from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import create_rope
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch14_moment._ref.ch14_path import (
    BUD_MANDATE_FILENAME,
    create_bud_partner_mandate_ledger_path,
)
from src.ch14_moment.test._util.ch14_env import get_temp_dir
from src.ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_create_bud_partner_mandate_ledger_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    timenum7 = 7
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_bud_path = create_bud_partner_mandate_ledger_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, timenum7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    timenum_dir = create_path(buds_dir, timenum7)
    expected_bud_path_dir = create_path(timenum_dir, BUD_MANDATE_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


LINUX_OS = platform_system() == "Linux"


def test_create_bud_partner_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_partner_mandate_ledger_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=lassounit_shop(create_rope(kw.moment_rope)),
        person_name=kw.person_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_partner_mandate_ledger_path) == doc_str
