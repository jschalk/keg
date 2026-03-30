from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_person_logic.test._util.ch07_examples import get_personunit_with_4_levels
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import lessonfilehandler_shop
from src.ch10_person_listen.keep_tool import (
    get_dw_perspective_person,
    get_perspective_person,
    rj_perspective_person,
    save_job_file,
    save_vision_person,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_perspective_person_ReturnsPersonWith_person_nameSetToLessonFileHandler_person_name():
    # ESTABLISH
    bob_personunit = get_personunit_with_4_levels()
    bob_personunit.set_person_name(exx.bob)

    # WHEN
    perspective_personunit = get_perspective_person(bob_personunit, exx.sue)

    # THEN
    assert perspective_personunit.to_dict() != bob_personunit.to_dict()
    assert perspective_personunit.person_name == exx.sue
    perspective_personunit.set_person_name(exx.bob)
    assert perspective_personunit.to_dict() == bob_personunit.to_dict()


def test_get_dw_perspective_person_ReturnsPersonWith_person_nameSetToLessonFileHandler_person_name(
    temp3_fs,
):
    # ESTABLISH
    bob_personunit = get_personunit_with_4_levels()
    bob_personunit.set_person_name(exx.bob)
    a23_lasso = lassounit_shop(exx.a23)
    bob_lessonfilehandler = lessonfilehandler_shop(str(temp3_fs), a23_lasso, exx.bob)
    save_job_file(bob_lessonfilehandler.moment_mstr_dir, bob_personunit)

    # WHEN
    perspective_personunit = get_dw_perspective_person(
        str(temp3_fs), exx.a23, exx.bob, exx.sue
    )

    # THEN
    assert perspective_personunit.person_name == exx.sue
    assert perspective_personunit.to_dict() != bob_personunit.to_dict()
    perspective_personunit.set_person_name(exx.bob)
    assert perspective_personunit.to_dict() == bob_personunit.to_dict()


def test_rj_perspective_person_ReturnsPersonWith_person_nameSetToLessonFileHandler_person_name(
    temp3_fs,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(exx.a23, nation_str)
    iowa_rope = create_rope(nation_rope, "Iowa")

    yao_personunit = get_personunit_with_4_levels()
    yao_personunit.set_person_name(exx.yao)

    save_vision_person(
        moment_mstr_dir=str(temp3_fs),
        moment_rope=exx.a23,
        healer_name=exx.bob,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        x_person=yao_personunit,
    )

    # WHEN
    perspective_personunit = rj_perspective_person(
        moment_mstr_dir=str(temp3_fs),
        moment_rope=exx.a23,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        healer_name=exx.bob,
        speaker_id=exx.yao,
        perspective_id=exx.sue,
    )

    # THEN
    assert perspective_personunit.person_name == exx.sue
    assert perspective_personunit.to_dict() != yao_personunit.to_dict()
    perspective_personunit.set_person_name(exx.yao)
    assert perspective_personunit.to_dict() == yao_personunit.to_dict()
