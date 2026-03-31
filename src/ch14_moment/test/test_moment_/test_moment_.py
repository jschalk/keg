from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.ch00_py.file_toolbox import create_path, get_json_filename, set_dir
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch04_rope.rope import default_knot_if_None
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_person_dir_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    gut_file_exists,
    open_gut_file,
    save_gut_file,
)
from src.ch10_person_listen._ref.ch10_path import create_keep_dutys_path, create_path
from src.ch10_person_listen.keep_tool import (
    job_file_exists,
    open_job_file,
    save_job_file,
)
from src.ch11_bud.bud_main import tranbook_shop
from src.ch13_time.epoch_main import epochunit_shop
from src.ch14_moment.moment_main import (
    MomentUnit,
    get_default_job_listen_count,
    momentunit_shop,
)
from src.ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_get_default_job_listen_count_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_job_listen_count() == 3


def test_MomentUnit_Exists():
    # ESTABLISH / WHEN
    amy_moment = MomentUnit()
    # THEN
    assert not amy_moment.moment_rope
    assert not amy_moment.epoch
    assert not amy_moment.personbudhistorys
    assert not amy_moment.paybook
    assert not amy_moment.offi_times
    assert not amy_moment.knot
    assert not amy_moment.fund_grain
    assert not amy_moment.respect_grain
    assert not amy_moment.mana_grain
    assert not amy_moment.job_listen_rotations
    assert not amy_moment.moment_mstr_dir
    # Calculated fields
    assert not amy_moment.offi_time_max
    assert not amy_moment.persons_dir
    assert not amy_moment.lessons_dir
    assert not amy_moment.all_tranbook
    assert set(amy_moment.__dict__) == {
        kw.moment_rope,
        kw.epoch,
        kw.personbudhistorys,
        kw.paybook,
        kw.knot,
        kw.fund_grain,
        kw.respect_grain,
        kw.mana_grain,
        kw.job_listen_rotations,
        "moment_dir",
        "moment_mstr_dir",
        kw.offi_times,
        kw.all_tranbook,
        kw.offi_time_max,
        "persons_dir",
        "lessons_dir",
    }


def test_momentunit_shop_ReturnsMomentUnit(temp3_dir):
    # ESTABLISH

    # WHEN
    a23_moment = momentunit_shop(exx.a23, temp3_dir)

    # THEN
    assert a23_moment.moment_rope == exx.a23
    assert a23_moment.epoch == epochunit_shop()
    assert a23_moment.personbudhistorys == {}
    assert a23_moment.paybook == tranbook_shop(exx.a23)
    assert a23_moment.offi_times == set()
    assert a23_moment.knot == default_knot_if_None()
    assert a23_moment.fund_grain == default_grain_num_if_None()
    assert a23_moment.respect_grain == default_grain_num_if_None()
    assert a23_moment.mana_grain == default_grain_num_if_None()
    assert a23_moment.moment_mstr_dir == temp3_dir
    assert a23_moment.job_listen_rotations == get_default_job_listen_count()
    # Calculated fields
    assert a23_moment.persons_dir != None
    assert a23_moment.lessons_dir != None
    assert a23_moment.all_tranbook == tranbook_shop(exx.a23)


def test_momentunit_shop_ReturnsMomentUnitWith_moments_dir(temp3_dir):
    # ESTABLISH

    # WHEN
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir=temp3_dir)

    # THEN
    assert a23_moment.moment_rope == exx.a23
    assert a23_moment.moment_mstr_dir == temp3_dir
    assert a23_moment.persons_dir is not None
    assert a23_moment.lessons_dir is not None


def test_momentunit_shop_ReturnsMomentUnitWith_knot(temp3_dir):
    # ESTABLISH
    x_fund_grain = 7.0
    x_respect_grain = 9
    x_mana_grain = 3
    a45_offi_times = {12, 15}
    x_job_listen_rotations = 888

    # WHEN
    a23_moment = momentunit_shop(
        moment_rope=exx.a23_slash,
        moment_mstr_dir=temp3_dir,
        offi_times=a45_offi_times,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
        job_listen_rotations=x_job_listen_rotations,
    )

    # THEN
    assert a23_moment.knot == exx.slash
    assert a23_moment.fund_grain == x_fund_grain
    assert a23_moment.respect_grain == x_respect_grain
    assert a23_moment.mana_grain == x_mana_grain
    assert a23_moment.offi_times == a45_offi_times
    assert a23_moment.job_listen_rotations == x_job_listen_rotations


def test_MomentUnit_set_moment_dirs_SetsDirsAndFiles(temp3_dir):
    # ESTABLISH
    amy_moment = MomentUnit(exx.a23, temp3_dir)
    x_moments_dir = create_path(temp3_dir, "moments")
    x_moment_dir = create_path(x_moments_dir, "Amy23")
    x_persons_dir = create_path(x_moment_dir, "persons")
    x_lessons_dir = create_path(x_moment_dir, "lessons")

    assert not amy_moment.moment_dir
    assert not amy_moment.persons_dir
    assert not amy_moment.lessons_dir
    assert os_path_exists(x_moment_dir) is False
    assert os_path_isdir(x_moment_dir) is False
    assert os_path_exists(x_persons_dir) is False
    assert os_path_exists(x_lessons_dir) is False

    # WHEN
    amy_moment._set_moment_dirs()

    # THEN
    print(f"{amy_moment.moment_dir=}")
    print(f"         {x_moment_dir=}")
    assert amy_moment.moment_dir == x_moment_dir
    assert amy_moment.persons_dir == x_persons_dir
    assert amy_moment.lessons_dir == x_lessons_dir
    assert os_path_exists(x_moment_dir)
    assert os_path_isdir(x_moment_dir)
    assert os_path_exists(x_persons_dir)
    assert os_path_exists(x_lessons_dir)


def test_momentunit_shop_SetsmomentsDirs(temp3_dir):
    # ESTABLISH

    # WHEN
    a23_moment = momentunit_shop(exx.a23, temp3_dir)

    # THEN
    assert a23_moment.moment_rope == exx.a23
    x_moments_dir = create_path(temp3_dir, "moments")
    assert a23_moment.moment_dir == create_path(x_moments_dir, "Amy23")
    assert a23_moment.persons_dir == create_path(a23_moment.moment_dir, "persons")


def test_MomentUnit_create_empty_person_from_moment_ReturnsObj_Scenario0(
    temp3_dir,
):
    # ESTABLISH
    moment_mstr_dir = temp3_dir
    x_fund_grain = 4
    x_respect_grain = 5
    x_mana_grain = 6
    a23_moment = momentunit_shop(
        exx.a23_slash,
        moment_mstr_dir,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )

    # WHEN
    generated_person = a23_moment.create_empty_person_from_moment(exx.sue)

    # THEN
    assert generated_person.knot == exx.slash
    assert generated_person.fund_grain == x_fund_grain
    assert generated_person.respect_grain == x_respect_grain
    assert generated_person.mana_grain == x_mana_grain


def test_MomentUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario1_person_dir_ExistsNoFile(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_lasso = lassounit_shop(exx.a23)
    sue_person_dir = create_person_dir_path(moment_mstr_dir, a23_lasso, exx.sue)
    assert not os_path_exists(sue_person_dir)
    assert not gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)

    # WHEN
    a23_moment.create_gut_file_if_none(exx.sue)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    expected_sue_gut = personunit_shop(exx.sue, exx.a23)
    assert open_gut_file(moment_mstr_dir, a23_lasso, exx.sue) == expected_sue_gut


def test_MomentUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario2_person_dir_ExistsNoFile_Create_gut_AndConfirmMomentAttributesPassed(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    x_fund_grain = 4
    x_respect_grain = 5
    x_mana_grain = 6
    a23_moment = momentunit_shop(
        exx.a23_slash,
        moment_mstr_dir,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )
    a23_lasso = lassounit_shop(exx.a23_slash, exx.slash)
    sue_person_dir = create_person_dir_path(moment_mstr_dir, a23_lasso, exx.sue)
    set_dir(sue_person_dir)
    assert os_path_exists(sue_person_dir)
    assert not gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)

    # WHEN
    a23_moment.create_gut_file_if_none(exx.sue)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    generated_gut = open_gut_file(moment_mstr_dir, a23_lasso, exx.sue)
    assert generated_gut.knot == exx.slash
    assert generated_gut.fund_grain == x_fund_grain
    assert generated_gut.respect_grain == x_respect_grain
    assert generated_gut.mana_grain == x_mana_grain


def test_MomentUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario3_FileExistsIsNotReplaced(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    sue_gut = personunit_shop(exx.sue, exx.a23)
    sue_gut.add_partnerunit(exx.bob)
    save_gut_file(moment_mstr_dir, sue_gut)
    a23_lasso = lassounit_shop(exx.a23)
    sue_person_dir = create_person_dir_path(moment_mstr_dir, a23_lasso, exx.sue)
    assert os_path_exists(sue_person_dir)
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)

    # WHEN
    a23_moment.create_gut_file_if_none(exx.sue)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert gut_file_exists(moment_mstr_dir, a23_lasso, exx.sue)
    assert open_gut_file(moment_mstr_dir, a23_lasso, exx.sue) == sue_gut


def test_MomentUnit_create_init_job_from_guts_Scenario0_CreatesFile(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        exx.a23_slash,
        moment_mstr_dir,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    a23_lasso = lassounit_shop(exx.a23_slash, exx.slash)
    assert not job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)

    # WHEN
    a23_moment.create_init_job_from_guts(exx.sue)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert job_file_exists(moment_mstr_dir, a23_lasso, exx.sue)


def test_MomentUnit_create_init_job_from_guts_Scenario1_ReplacesFile(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        exx.a23_slash,
        moment_mstr_dir,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    x0_sue_job = personunit_shop(exx.sue, exx.a23_slash, exx.slash)
    x0_sue_job.add_partnerunit(exx.bob)
    save_job_file(moment_mstr_dir, x0_sue_job)
    a23_lasso = lassounit_shop(exx.a23_slash, exx.slash)
    assert open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_partner(exx.bob)

    # WHEN
    a23_moment.create_init_job_from_guts(exx.sue)

    # THEN
    assert not open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_partner(exx.bob)


def test_MomentUnit_create_init_job_from_guts_Scenario2_job_Has_gut_Partners(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        exx.a23_slash,
        moment_mstr_dir,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    a23_moment.create_init_job_from_guts(exx.sue)
    sue_gut = personunit_shop(exx.sue, exx.a23_slash, exx.slash)
    sue_gut.add_partnerunit(exx.bob)
    save_gut_file(moment_mstr_dir, sue_gut)
    a23_lasso = lassounit_shop(exx.a23_slash, exx.slash)
    assert not open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_partner(exx.bob)

    # WHEN
    a23_moment.create_init_job_from_guts(exx.sue)

    # THEN
    assert open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_partner(exx.bob)


def test_MomentUnit_create_init_job_from_guts_Scenario3_gut_FilesAreListenedTo(
    temp3_fs,
):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        exx.a23_slash,
        moment_mstr_dir,
        knot=exx.slash,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    a23_moment.create_init_job_from_guts(exx.sue)

    # create Sue gut
    sue_gut = personunit_shop(exx.sue, exx.a23_slash, knot=exx.slash)
    sue_gut.add_partnerunit(exx.bob)
    save_gut_file(moment_mstr_dir, sue_gut)
    # create Bob gut with agenda plan for Sue
    bob_gut = personunit_shop(exx.bob, exx.a23_slash, knot=exx.slash)
    bob_gut.add_partnerunit(exx.sue)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_plan(clean_rope, pledge=True)
    bob_gut.get_plan_obj(clean_rope).workforceunit.add_labor(exx.sue)
    save_gut_file(moment_mstr_dir, bob_gut)
    a23_lasso = lassounit_shop(exx.a23_slash, exx.slash)
    assert not open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_agenda_dict()

    # WHEN
    a23_moment.create_init_job_from_guts(exx.sue)

    # THEN
    assert open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_agenda_dict()
    sue_agenda = open_job_file(moment_mstr_dir, a23_lasso, exx.sue).get_agenda_dict()
    assert len(sue_agenda) == 1
    assert sue_agenda.get(clean_rope).get_plan_rope() == clean_rope


def test_MomentUnit__set_all_healer_dutys_Setsdutys(
    temp3_fs,
):
    # ESTABLISH
    x_moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, x_moment_mstr_dir)
    a23_moment.create_init_job_from_guts(exx.sue)
    a23_moment.create_init_job_from_guts(exx.yao)
    a23_lasso = lassounit_shop(exx.a23)
    sue_gut_person = open_gut_file(x_moment_mstr_dir, a23_lasso, exx.sue)
    yao_gut_person = open_gut_file(x_moment_mstr_dir, a23_lasso, exx.yao)

    sue_gut_person.add_partnerunit(exx.sue)
    sue_gut_person.add_partnerunit(exx.yao)
    yao_gut_person.add_partnerunit(exx.sue)
    yao_gut_person.add_partnerunit(exx.yao)
    texas_str = "Texas"
    texas_rope = sue_gut_person.make_l1_rope(texas_str)
    sue_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    yao_gut_person.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_person.make_rope(texas_rope, dallas_str)
    dallas_healerunit = healerunit_shop({exx.sue, exx.yao})
    dallas_plan = planunit_shop(dallas_str, healerunit=dallas_healerunit)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_person.make_rope(texas_rope, elpaso_str)
    elpaso_healerunit = healerunit_shop({exx.sue})
    elpaso_plan = planunit_shop(elpaso_str, healerunit=elpaso_healerunit)

    sue_gut_person.set_plan_obj(dallas_plan, texas_rope)
    sue_gut_person.set_plan_obj(elpaso_plan, texas_rope)
    yao_gut_person.set_plan_obj(dallas_plan, texas_rope)
    yao_gut_person.set_plan_obj(elpaso_plan, texas_rope)

    save_gut_file(x_moment_mstr_dir, sue_gut_person)
    save_gut_file(x_moment_mstr_dir, yao_gut_person)
    sue_filename = get_json_filename(exx.sue)
    yao_filename = get_json_filename(exx.yao)

    mstr_dir = x_moment_mstr_dir
    sue_dutys_path = create_keep_dutys_path(
        mstr_dir, exx.sue, exx.a23, dallas_rope, None
    )
    yao_dutys_path = create_keep_dutys_path(
        mstr_dir, exx.yao, exx.a23, dallas_rope, None
    )
    sue_dallas_sue_duty_file_path = create_path(sue_dutys_path, sue_filename)
    sue_dallas_yao_duty_file_path = create_path(sue_dutys_path, yao_filename)
    yao_dallas_sue_duty_file_path = create_path(yao_dutys_path, sue_filename)
    yao_dallas_yao_duty_file_path = create_path(yao_dutys_path, yao_filename)
    assert os_path_exists(sue_dallas_sue_duty_file_path) is False
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path) is False
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_moment._set_all_healer_dutys(exx.sue)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_moment._set_all_healer_dutys(exx.yao)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


# def test_MomentUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     moment_mstr_dir = str(temp3_fs)
#     time56 = 56
#     a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, offi_time_max=time56)
#     assert a23_moment.offi_time == 0
#     assert a23_moment.offi_time_max == time56

#     # WHEN
#     time23 = 23
#     a23_moment.set_offi_time(time23)

#     # THEN
#     assert a23_moment.offi_time == time23
#     assert a23_moment.offi_time_max == time56


# def test_MomentUnit_set_offi_time_Scenario1_SetsAttr():
#     # ESTABLISH
#     a23_moment = momentunit_shop(exx.a23, str(temp3_fs))
#     assert a23_moment.offi_time == 0
#     assert a23_moment.offi_time_max == 0

#     # WHEN
#     time23 = 23
#     a23_moment.set_offi_time(time23)

#     # THEN
#     assert a23_moment.offi_time == time23
#     assert a23_moment.offi_time_max == time23


def test_MomentUnit_set_offi_time_max_Scenario0_SetsAttr(temp3_dir):
    # ESTABLISH
    moment_mstr_dir = temp3_dir
    time7 = 7
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_moment.offi_time_max = time7
    # assert a23_moment.offi_time == 0
    assert a23_moment.offi_time_max == time7

    # WHEN
    time23 = 23
    a23_moment.set_offi_time_max(time23)

    # THEN
    # assert a23_moment.offi_time == 0
    assert a23_moment.offi_time_max == time23


# def test_MomentUnit_set_offi_time_max_Scenario1_SetsAttr():
#     # ESTABLISH
#     moment_mstr_dir = str(temp3_fs)
#     time21 = 21
#     time77 = 77
#     a23_moment = momentunit_shop(
#         exx.a23, moment_mstr_dir, offi_time=time21, offi_time_max=time77
#     )
#     assert a23_moment.offi_time == time21
#     assert a23_moment.offi_time_max == time77

#     # WHEN / THEN
#     time11 = 11
#     with pytest_raises(Exception) as excinfo:
#         a23_moment.set_offi_time_max(time11)
#     exception_str = f"Cannot set offi_time_max={time11} because it is less than offi_time={time21}"
#     assert str(excinfo.value) == exception_str


# def test_MomentUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     a23_moment = momentunit_shop(exx.a23, str(temp3_fs))
#     assert a23_moment.offi_time == 0
#     assert a23_moment.offi_time_max == 0

#     # WHEN
#     time23 = 23
#     time55 = 55
#     a23_moment.set_offi_time(time23, time55)

#     # THEN
#     assert a23_moment.offi_time == time23
#     assert a23_moment.offi_time_max == time55
