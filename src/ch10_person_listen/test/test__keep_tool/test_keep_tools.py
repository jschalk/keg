from inspect import getdoc as inspect_getdoc
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import delete_dir, open_file, save_file
from src.ch04_rope.rope import create_rope
from src.ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from src.ch09_person_lesson._ref.ch09_path import create_job_path
from src.ch10_person_listen._ref.ch10_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_treasury_db_path,
)
from src.ch10_person_listen.keep_tool import (
    create_keep_path_dir_if_missing,
    create_treasury_db_file,
    get_duty_person,
    open_job_file,
    save_duty_person,
    treasury_db_file_exists,
)
from src.ch10_person_listen.test._util.ch10_env import get_temp_dir, temp_dir_setup
from src.ch10_person_listen.test._util.ch10_examples import ch10_example_moment_rope
from src.ref.keywords import ExampleStrs as exx


def test_create_keep_path_dir_if_missing_CreatesDirectory(
    temp_dir_setup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    moment_mstr_dir = get_temp_dir()
    keep_path = create_keep_rope_path(
        moment_mstr_dir, exx.sue, exx.a23, texas_rope, None
    )
    assert os_path_exists(keep_path) is False

    # WHEN
    create_keep_path_dir_if_missing(moment_mstr_dir, exx.sue, exx.a23, texas_rope, None)

    # THEN
    assert os_path_exists(keep_path)


def test_treasury_db_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    texas_rope = create_rope(ch10_example_moment_rope(), "Texas")
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )
    assert (
        treasury_db_file_exists(
            moment_mstr_dir,
            person_name=exx.sue,
            moment_rope=exx.a23,
            keep_rope=texas_rope,
            knot=None,
        )
        is False
    )

    # WHEN
    save_file(treasury_db_path, None, "fizzbuzz")

    # THEN
    assert treasury_db_file_exists(
        moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )


def test_create_treasury_db_file_CreatesDatabase(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    texas_rope = create_rope(exx.a23, "Texas")
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )
    assert os_path_exists(treasury_db_path) is False

    # WHEN
    create_treasury_db_file(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )

    # THEN
    assert os_path_exists(treasury_db_path)


def test_create_treasury_db_DoesNotOverWriteDBIfExists(
    temp_dir_setup,
):
    # ESTABLISH create keep
    moment_mstr_dir = get_temp_dir()
    texas_rope = create_rope(exx.a23, "Texas")
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )
    delete_dir(treasury_db_path)  # clear out any treasury.db file
    create_treasury_db_file(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )
    assert os_path_exists(treasury_db_path)

    # ESTABLISH
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir, exx.sue, exx.a23, texas_rope, None
    )
    x_file_str = "Texas Dallas ElPaso"
    save_file(treasury_db_path, None, file_str=x_file_str, replace=True)
    assert os_path_exists(treasury_db_path)
    assert open_file(treasury_db_path) == x_file_str

    # WHEN
    create_treasury_db_file(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
    )

    # THEN
    assert open_file(treasury_db_path) == x_file_str


def test_save_duty_person_SavesFile(temp_dir_setup):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    moment_mstr_dir = get_temp_dir()
    bob_person = get_personunit_with_4_levels()
    bob_person.set_person_name(exx.bob)
    keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
        duty_person=exx.bob,
    )
    assert os_path_exists(keep_duty_path) is False

    # WHEN
    save_duty_person(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
        duty_person=bob_person,
    )

    # THEN
    assert os_path_exists(keep_duty_path)


def test_get_duty_person_reason_lowersFile(temp_dir_setup):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    moment_mstr_dir = get_temp_dir()
    bob_person = get_personunit_with_4_levels()
    bob_person.set_person_name(exx.bob)
    save_duty_person(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
        duty_person=bob_person,
    )

    # WHEN
    gen_bob_duty = get_duty_person(
        moment_mstr_dir=moment_mstr_dir,
        person_name=exx.sue,
        moment_rope=exx.a23,
        keep_rope=texas_rope,
        knot=None,
        duty_person_name=exx.bob,
    )

    # THEN
    assert gen_bob_duty.to_dict() == bob_person.to_dict()


def test_open_job_file_HasDocString():
    # ESTABLISH
    create_job_path_doc_str = inspect_getdoc(create_job_path)
    # WHEN / THEN
    assert inspect_getdoc(open_job_file) in create_job_path_doc_str
