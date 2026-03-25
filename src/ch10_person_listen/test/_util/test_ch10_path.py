from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from pytest import mark as pytest_mark, raises as pytest_raises
from src.ch00_py.file_toolbox import create_path, get_json_filename
from src.ch04_rope.rope import create_rope, create_rope_from_labels
from src.ch10_person_listen._ref.ch10_path import (
    create_keep_duty_path,
    create_keep_dutys_path,
    create_keep_grade_path,
    create_keep_grades_path,
    create_keep_rope_path,
    create_keep_visions_path,
    create_keeps_dir_path,
    create_treasury_db_path,
    treasury_filename,
)
from src.ch10_person_listen.test._util.ch10_env import get_temp_dir
from src.ref.keywords import Ch10Keywords as kw, ExampleStrs as exx


def test_treasury_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert treasury_filename() == "treasury.db"


def test_create_keeps_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    keeps_dir = create_keeps_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    expected_keeps_dir = create_path(sue_dir, "keeps")
    assert keeps_dir == expected_keeps_dir


def test_create_keep_rope_path_ReturnsObj_Scenario0_SimpleRope():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )

    # THEN
    keeps_dir = create_keeps_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)
    keep_amy23_dir = create_path(keeps_dir, "Amy23")
    expected_keep_casa_dir = create_path(keep_amy23_dir, exx.casa)
    print(f"{expected_keep_casa_dir=}")
    print(f"        {keep_casa_path=}")
    assert keep_casa_path == expected_keep_casa_dir


def test_create_keep_rope_path_ReturnsObj_Scenario1_MoreTestsForRopePathCreation():
    # ESTABLISH
    peru_str = "peru"
    peru_rope = create_rope(peru_str)
    moment_mstr_dir = get_temp_dir()
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    texas_rope = create_rope_from_labels([peru_str, texas_str])
    dallas_rope = create_rope_from_labels([peru_str, texas_str, dallas_str])
    elpaso_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str])
    kern_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str, kern_str])

    # WHEN
    # texas_path = create_keep_rope_path(sue_lessonfilehandler, texas_rope)
    texas_path = create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=texas_rope,
        knot=None,
    )
    # dallas_path = createdallas_path_keep_rope_path(sue_lessonfilehandler, dallas_rope)
    dallas_path = create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=dallas_rope,
        knot=None,
    )
    # elpaso_path = create_keep_rope_path(sue_lessonfilehandler, elpaso_rope)
    elpaso_path = create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=elpaso_rope,
        knot=None,
    )
    # kern_path = create_keep_rope_path(sue_lessonfilehandler, kern_rope)
    kern_path = create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=kern_rope,
        knot=None,
    )

    # THEN
    keeps_dir = create_keeps_dir_path(moment_mstr_dir, peru_rope, exx.sue)
    planroot_dir = create_path(keeps_dir, peru_str)
    print(f"{kern_rope=}")
    print(f"{planroot_dir=}")
    assert texas_path == create_path(planroot_dir, texas_str)
    assert dallas_path == create_path(texas_path, dallas_str)
    assert elpaso_path == create_path(texas_path, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)

    # WHEN / THEN
    diff_root_texas_rope = create_rope_from_labels([peru_str, texas_str])
    diff_root_dallas_rope = create_rope_from_labels([peru_str, texas_str, dallas_str])
    diff_root_elpaso_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str])
    assert texas_path == create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=diff_root_texas_rope,
        knot=None,
    )
    assert dallas_path == create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=diff_root_dallas_rope,
        knot=None,
    )
    assert elpaso_path == create_keep_rope_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=peru_rope,
        keep_rope=diff_root_elpaso_rope,
        knot=None,
    )


def test_create_keep_rope_path_RaisesError_Scenarion2_keep_rope_DoesNotExist():
    # ESTABLISH

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_keep_rope_path("dir", exx.bob, exx.a23, None, None)
    assertion_fail_str = (
        f"'{exx.bob}' cannot save to keep_path because it does not have keep_rope."
    )
    assert str(excinfo.value) == assertion_fail_str


def test_create_keep_dutys_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_keep_dutys_path(
        moment_mstr_dir=x_moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "dutys")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keep_duty_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=x_moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=casa_rope,
        knot=None,
        duty_person=exx.bob,
    )

    # THEN
    keep_dutys_path = create_keep_dutys_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    bob_filename = get_json_filename(exx.bob)
    expected_keep_duty_path = create_path(keep_dutys_path, bob_filename)
    assert gen_keep_duty_path == expected_keep_duty_path


def test_create_keep_grades_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_keep_grades_path(
        moment_mstr_dir=x_moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "grades")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keep_grade_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=casa_rope,
        knot=None,
        grade_person_name=exx.bob,
    )

    # THEN
    keep_grades_path = create_keep_grades_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_grade_path = create_path(keep_grades_path, get_json_filename(exx.bob))
    assert gen_keep_grade_path == expected_grade_path


def test_create_keep_visions_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_keep_visions_path(
        moment_mstr_dir=x_moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "visions")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_treasury_db_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_treasury_db_path(
        moment_mstr_dir=x_moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "treasury.db")
    assert gen_keep_dutys_path == expected_keep_dutys_path


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keeps_dir_path_HasDocString():
    # ESTABLISH
    x_moment_rope = create_rope(kw.moment_rope)
    doc_str = create_keeps_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert inspect_getdoc(create_keeps_dir_path) == doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keep_rope_path_HasDocString() -> None:
    # ESTABLISH
    level1_label_str = "level1_label"
    level1_rope = create_rope(kw.planroot, level1_label_str)
    x_moment_rope = create_rope(kw.moment_rope)
    doc_str = create_keep_rope_path(
        moment_mstr_dir="moment_mstr_dir",
        person_name=kw.person_name,
        moment_rope=x_moment_rope,
        keep_rope=level1_rope,
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert inspect_getdoc(create_keep_rope_path) == doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keep_dutys_path_HasDocString() -> None:
    # ESTABLISH
    x_moment_rope = create_rope(kw.moment_rope)
    expected_doc_str = create_keep_dutys_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    expected_doc_str = f"Returns path: {expected_doc_str}"
    print(f"{expected_doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keep_dutys_path) == expected_doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keep_duty_path_HasDocString() -> None:
    # ESTABLISH
    duty_person_str = "duty_person"
    x_moment_rope = create_rope(kw.moment_rope)
    expected_doc_str = create_keep_duty_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
        keep_rope="planroot;level1;leveln",
        knot=None,
        duty_person=duty_person_str,
    )
    expected_doc_str = f"Returns path: {expected_doc_str}"
    print(f"{expected_doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keep_duty_path) == expected_doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keep_grades_path_HasDocString() -> None:
    # ESTABLISH
    x_moment_rope = create_rope(kw.moment_rope)
    doc_str = create_keep_grades_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"                             {doc_str=}")
    print(f"{inspect_getdoc(create_keep_grades_path)=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keep_grades_path) == doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keep_grade_path_HasDocString() -> None:
    # ESTABLISH
    x_moment_rope = create_rope(kw.moment_rope)
    doc_str = create_keep_grade_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
        keep_rope="planroot;level1;leveln",
        knot=None,
        grade_person_name="grade_person_name",
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_keep_grade_path)=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keep_grade_path) == doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_keep_visions_path_HasDocString() -> None:
    # ESTABLISH
    x_moment_rope = create_rope(kw.moment_rope)
    doc_str = create_keep_visions_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_keep_visions_path) == doc_str


@pytest_mark.skipif(platform_system() == "Linux", reason="conflict in file path str")
def test_create_treasury_db_path_HasDocString() -> None:
    # ESTABLISH
    x_moment_rope = create_rope(kw.moment_rope)
    doc_str = create_treasury_db_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_rope=x_moment_rope,
        person_name=kw.person_name,
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert inspect_getdoc(create_treasury_db_path) == doc_str
