from src.ch04_rope.rope import LabelTerm, RopeTerm, create_rope
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop, planunit_shop
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    LessonFileHandler,
    gut_file_exists,
    lessonfilehandler_shop,
    save_gut_file,
)
from src.ch10_person_listen.keep_tool import (
    get_vision_person,
    job_file_exists,
    open_job_file,
    save_duty_person,
    vision_file_exists,
)
from src.ch10_person_listen.listen_main import (
    create_vision_file_from_duty_file,
    listen_to_person_visions,
)
from src.ch10_person_listen.test._util.ch10_examples import (
    ch10_example_moment_rope,
    eat_str,
    full_str,
    get_texas_lessonfilehandler,
    get_texas_rope,
    hungry_str,
    run_str,
)
from src.ref.keywords import Ch10Keywords as kw, ExampleStrs as exx


def sanitation_str() -> str:
    return "sanitation"


def dirty_str() -> str:
    return "dirty"


def casa_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), exx.casa)


def cuisine_rope() -> RopeTerm:
    return create_rope(casa_rope(), exx.cuisine)


def eat_rope() -> RopeTerm:
    return create_rope(casa_rope(), eat_str())


def hungry_rope() -> RopeTerm:
    return create_rope(eat_rope(), hungry_str())


def full_rope() -> RopeTerm:
    return create_rope(eat_rope(), full_str())


def sanitation_rope() -> RopeTerm:
    return create_rope(casa_rope(), sanitation_str())


def clean_rope() -> RopeTerm:
    return create_rope(sanitation_rope(), exx.clean)


def dirty_rope() -> RopeTerm:
    return create_rope(sanitation_rope(), dirty_str())


def sweep_rope() -> RopeTerm:
    return create_rope(casa_rope(), exx.sweep)


def run_rope() -> RopeTerm:
    return create_rope(casa_rope(), run_str())


def get_example_yao_person() -> PersonUnit:
    yao_speaker = personunit_shop(exx.yao, ch10_example_moment_rope())
    yao_speaker.set_plan_obj(planunit_shop(run_str()), casa_rope())
    yao_speaker.add_partnerunit(exx.yao, partner_debt_lumen=10)
    yao_speaker.add_partnerunit(exx.zia, partner_debt_lumen=30)
    yao_speaker.add_partnerunit(exx.bob, partner_debt_lumen=40)
    yao_speaker.set_partner_respect(80)
    return yao_speaker


def get_example_yao_vision1_speaker() -> PersonUnit:
    yao_speaker = get_example_yao_person()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_partner_respect(40)
    yao_speaker.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), casa_rope())
    yao_speaker.set_plan_obj(planunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_plan_obj(planunit_shop(full_str()), eat_rope())
    cuisine_planunit = yao_speaker.get_plan_obj(cuisine_rope())
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    yao_speaker.edit_reason(cuisine_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())
    return yao_speaker


def get_example_yao_vision2_speaker() -> PersonUnit:
    yao_speaker = get_example_yao_person()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_partner_respect(30)
    yao_speaker.set_plan_obj(planunit_shop(exx.cuisine, pledge=True), casa_rope())
    yao_speaker.set_plan_obj(planunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_plan_obj(planunit_shop(full_str()), eat_rope())
    cuisine_planunit = yao_speaker.get_plan_obj(cuisine_rope())
    cuisine_planunit.workforceunit.add_labor(exx.yao)
    yao_speaker.edit_reason(cuisine_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())

    yao_speaker.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope())
    yao_speaker.set_plan_obj(planunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_plan_obj(planunit_shop(exx.clean), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_example_yao_vision3_speaker() -> PersonUnit:
    yao_speaker = get_example_yao_person()
    yao_speaker.del_plan_obj(run_rope())
    yao_speaker.set_partner_respect(10)
    yao_speaker.set_plan_obj(planunit_shop(exx.sweep, pledge=True), casa_rope())
    yao_speaker.set_plan_obj(planunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_plan_obj(planunit_shop(exx.clean), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_usa_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), "USA")


def get_iowa_str() -> LabelTerm:
    return "Iowa"


def get_ohio_str() -> LabelTerm:
    return "Ohio"


def get_utah_str() -> LabelTerm:
    return "Utah"


def get_swim_str() -> LabelTerm:
    return "swim"


def get_location_str() -> LabelTerm:
    return "location"


def get_in_mer_str() -> LabelTerm:
    return "in_mer"


def get_on_land_str() -> LabelTerm:
    return "on_land"


def get_iowa_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_iowa_str())


def get_ohio_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_ohio_str())


def get_utah_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_utah_str())


def get_swim_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), get_swim_str())


def get_location_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), get_location_str())


def get_in_mer_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_in_mer_str())


def get_on_land_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_on_land_str())


def get_yao_ohio_lessonfilehandler(moment_mstr_dir) -> LessonFileHandler:
    yao_person = get_example_yao_person()
    return lessonfilehandler_shop(
        moment_mstr_dir=moment_mstr_dir,
        moment_lasso=lassounit_shop(yao_person.planroot.get_plan_rope()),
        person_name=yao_person.person_name,
    )


def get_yao_iowa_lessonfilehandler(moment_mstr_dir) -> LessonFileHandler:
    yao_person = get_example_yao_person()
    return lessonfilehandler_shop(
        moment_mstr_dir=moment_mstr_dir,
        moment_lasso=lassounit_shop(yao_person.planroot.get_plan_rope()),
        person_name=yao_person.person_name,
    )


def get_zia_utah_lessonfilehandler(moment_mstr_dir) -> LessonFileHandler:
    yao_person = get_example_yao_person()
    return lessonfilehandler_shop(
        moment_mstr_dir=moment_mstr_dir,
        moment_lasso=lassounit_shop(yao_person.planroot.get_plan_rope()),
        person_name="Zia",
    )


def get_example_yao_gut_with_3_healers(moment_mstr_dir) -> PersonUnit:
    d = moment_mstr_dir
    yao_gut = get_example_yao_person()
    iowa_plan = planunit_shop(get_iowa_str(), problem_bool=True)
    ohio_plan = planunit_shop(get_ohio_str(), problem_bool=True)
    utah_plan = planunit_shop(get_utah_str(), problem_bool=True)
    iowa_plan.healerunit.set_healer_name(get_yao_iowa_lessonfilehandler(d).person_name)
    ohio_plan.healerunit.set_healer_name(get_yao_ohio_lessonfilehandler(d).person_name)
    utah_plan.healerunit.set_healer_name(get_zia_utah_lessonfilehandler(d).person_name)
    yao_gut.set_plan_obj(iowa_plan, get_usa_rope())
    yao_gut.set_plan_obj(ohio_plan, get_usa_rope())
    yao_gut.set_plan_obj(utah_plan, get_usa_rope())

    return yao_gut


def test_listen_to_person_visions_Pipeline_Scenario1_yao_gut_CanOnlyReferenceItself(
    temp3_fs,
):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    # yao0_gut with 3 debotors of different partner_cred_lumens
    # yao_vision1 with 1 case_task, fact that doesn't make that case_task active
    # yao_vision2 with 2 case_tasks, one is equal fact that makes case_task active
    # yao_vision3 with 1 new case_task, fact stays with it
    moment_mstr_dir = str(temp3_fs)
    moment_rope = ch10_example_moment_rope()
    yao_gut0 = get_example_yao_gut_with_3_healers(moment_mstr_dir)
    yao_gut0.set_l1_plan(planunit_shop(get_location_str()))
    yao_gut0.set_plan_obj(planunit_shop(get_in_mer_str()), get_location_rope())
    yao_gut0.set_plan_obj(planunit_shop(get_on_land_str()), get_location_rope())
    yao_gut0.set_l1_plan(planunit_shop(get_swim_str(), pledge=True))
    yao_gut0.edit_reason(get_swim_rope(), get_location_rope(), get_in_mer_rope())
    yao_gut0.add_fact(get_location_rope(), get_in_mer_rope())
    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    yao_gut0.del_plan_obj(run_rope())
    assert yao_gut0._keep_dict.get(get_iowa_rope())
    assert yao_gut0._keep_dict.get(get_ohio_rope())
    assert yao_gut0._keep_dict.get(get_utah_rope())
    yao_gut0.conpute()
    assert len(yao_gut0._keep_dict) == 3
    # print(f"{yao_gut0._plan_dict.keys()=}")

    yao_vision1 = get_example_yao_vision1_speaker()
    yao_vision2 = get_example_yao_vision2_speaker()
    yao_vision3 = get_example_yao_vision3_speaker()
    yao_iowa_lessonfilehandler = get_yao_iowa_lessonfilehandler(str(temp3_fs))
    yao_ohio_lessonfilehandler = get_yao_ohio_lessonfilehandler(str(temp3_fs))
    zia_utah_lessonfilehandler = get_zia_utah_lessonfilehandler(str(temp3_fs))
    # delete_dir(yao_iowa_lessonfilehandler.persons_dir())
    moment_lasso = lassounit_shop(moment_rope)
    assert gut_file_exists(moment_mstr_dir, moment_lasso, exx.yao) is False
    assert job_file_exists(moment_mstr_dir, moment_lasso, exx.yao) is False
    assert (
        vision_file_exists(
            yao_iowa_lessonfilehandler.moment_mstr_dir,
            yao_iowa_lessonfilehandler.person_name,
            yao_iowa_lessonfilehandler.moment_lasso.moment_rope,
            get_iowa_rope(),
            yao_iowa_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            yao_ohio_lessonfilehandler.moment_mstr_dir,
            yao_ohio_lessonfilehandler.person_name,
            yao_ohio_lessonfilehandler.moment_lasso.moment_rope,
            get_ohio_rope(),
            yao_ohio_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            zia_utah_lessonfilehandler.moment_mstr_dir,
            zia_utah_lessonfilehandler.person_name,
            zia_utah_lessonfilehandler.moment_lasso.moment_rope,
            get_utah_rope(),
            zia_utah_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
        is False
    )

    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    save_gut_file(str(temp3_fs), yao_gut0)
    assert gut_file_exists(moment_mstr_dir, moment_lasso, exx.yao)
    assert (
        vision_file_exists(
            yao_iowa_lessonfilehandler.moment_mstr_dir,
            yao_iowa_lessonfilehandler.person_name,
            yao_iowa_lessonfilehandler.moment_lasso.moment_rope,
            get_iowa_rope(),
            yao_iowa_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            yao_ohio_lessonfilehandler.moment_mstr_dir,
            yao_ohio_lessonfilehandler.person_name,
            yao_ohio_lessonfilehandler.moment_lasso.moment_rope,
            get_ohio_rope(),
            yao_ohio_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            zia_utah_lessonfilehandler.moment_mstr_dir,
            zia_utah_lessonfilehandler.person_name,
            zia_utah_lessonfilehandler.moment_lasso.moment_rope,
            get_utah_rope(),
            zia_utah_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
        is False
    )
    # WHEN / THEN
    assert job_file_exists(moment_mstr_dir, moment_lasso, exx.yao) is False
    listen_to_person_visions(yao_iowa_lessonfilehandler, get_iowa_rope())
    assert job_file_exists(moment_mstr_dir, moment_lasso, exx.yao)

    yao_job = open_job_file(moment_mstr_dir, moment_lasso, exx.yao)
    yao_job.conpute()
    assert yao_job.partners.keys() == yao_gut0.partners.keys()
    assert yao_job.get_partner(exx.yao).irrational_partner_debt_lumen == 0
    yao_job_partners = yao_job.to_dict().get(kw.partners)
    yao_gut0_partners = yao_gut0.to_dict().get(kw.partners)
    yao_job_bob = yao_job_partners.get("Bob")
    yao_gut0_bob = yao_gut0_partners.get("Bob")
    print(f"{yao_job_bob=}")
    print(f"{yao_gut0_bob=}")
    assert yao_job_bob == yao_gut0_bob
    assert yao_job_partners.keys() == yao_gut0_partners.keys()
    assert yao_job_partners == yao_gut0_partners
    assert len(yao_job.to_dict().get(kw.partners)) == 3
    assert len(yao_job._plan_dict) == 4
    print(f"{yao_job._plan_dict.keys()=}")
    print(f"{yao_job.get_planroot_factunits_dict().keys()=}")
    assert yao_job.plan_exists(cuisine_rope()) is False
    assert yao_job.plan_exists(clean_rope()) is False
    assert yao_job.plan_exists(run_rope()) is False
    assert yao_job.plan_exists(get_swim_rope())
    assert yao_job.plan_exists(get_in_mer_rope())
    assert yao_job.plan_exists(get_on_land_rope()) is False
    assert yao_job.get_fact(get_location_rope()) is not None
    assert yao_job.get_fact(get_location_rope()).fact_state == get_in_mer_rope()
    assert len(yao_job.get_agenda_dict()) == 1
    assert len(yao_job.planroot.factunits) == 1
    assert yao_job != yao_gut0


def test_create_vision_file_from_duty_file_CreatesEmptyvision(temp3_fs):
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao)
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler(str(temp3_fs))
    save_duty_person(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        person_name=sue_texas_lessonfilehandler.person_name,
        moment_rope=sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_person=yao_duty,
    )

    assert not (
        vision_file_exists(
            sue_texas_lessonfilehandler.moment_mstr_dir,
            sue_texas_lessonfilehandler.person_name,
            sue_texas_lessonfilehandler.moment_lasso.moment_rope,
            get_texas_rope(),
            sue_texas_lessonfilehandler.moment_lasso.knot,
            exx.yao,
        )
    )

    # WHEN
    print(f"{sue_texas_lessonfilehandler.moment_lasso.moment_rope=}")
    create_vision_file_from_duty_file(
        sue_texas_lessonfilehandler, exx.yao, get_texas_rope()
    )

    # THEN
    assert vision_file_exists(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        exx.yao,
    )
    yao_vision = get_vision_person(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.person_name,
        sue_texas_lessonfilehandler.moment_lasso.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.moment_lasso.knot,
        exx.yao,
    )
    assert yao_vision.person_name is not None
    assert yao_vision.person_name == exx.yao
    assert yao_vision.to_dict() == yao_duty.to_dict()
