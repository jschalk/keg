from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch01_allot.allot import allot_scale
from src.ch04_rope.rope import get_ancestor_ropes, get_first_label_from_rope
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PartnerUnit, PersonUnit
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import LessonFileHandler, open_gut_file
from src.ch10_person_listen._ref.ch10_semantic_types import PersonName, RopeTerm
from src.ch10_person_listen.basis_person import (
    create_empty_person_from_person,
    create_listen_basis,
)
from src.ch10_person_listen.keep_tool import (
    get_duty_person,
    get_perspective_person,
    get_vision_person,
    open_job_file,
    rj_speaker_person,
    save_job_file,
    save_vision_person,
    vision_file_exists,
)


class MissingDebtorRespectError(Exception):
    pass


def generate_perspective_agenda(perspective_person: PersonUnit) -> list[PlanUnit]:
    for x_factunit in perspective_person.planroot.factunits.values():
        x_factunit.set_fact_state_to_fact_context()
    return list(perspective_person.get_agenda_dict().values())


def _ingest_perspective_agenda(
    listener: PersonUnit, agenda: list[PlanUnit]
) -> PersonUnit:
    debtor_respect = listener.debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_respect, listener.respect_grain)
    for ingest_planunit in ingest_list:
        _ingest_single_planunit(listener, ingest_planunit)
    return listener


def _allocate_irrational_partner_debt_lumen(
    listener: PersonUnit, speaker_person_name: PersonName
) -> PersonUnit:
    speaker_partnerunit = listener.get_partner(speaker_person_name)
    speaker_partner_debt_lumen = speaker_partnerunit.partner_debt_lumen
    speaker_partnerunit.add_irrational_partner_debt_lumen(speaker_partner_debt_lumen)
    return listener


def _allocate_inallocable_partner_debt_lumen(
    listener: PersonUnit, speaker_person_name: PersonName
) -> PersonUnit:
    speaker_partnerunit = listener.get_partner(speaker_person_name)
    speaker_partnerunit.add_inallocable_partner_debt_lumen(
        speaker_partnerunit.partner_debt_lumen
    )
    return listener


def generate_ingest_list(
    plan_list: list[PlanUnit], debtor_respect: float, respect_grain: float
) -> list[PlanUnit]:
    plan_ledger = {x_plan.get_plan_rope(): x_plan.star for x_plan in plan_list}
    star_allot = allot_scale(plan_ledger, debtor_respect, respect_grain)
    for x_planunit in plan_list:
        x_planunit.star = star_allot.get(x_planunit.get_plan_rope())
    return plan_list


def _ingest_single_planunit(listener: PersonUnit, ingest_planunit: PlanUnit):
    star_data = _create_star_data(listener, ingest_planunit.get_plan_rope())

    if listener.plan_exists(ingest_planunit.get_plan_rope()) is False:
        x_parent_rope = ingest_planunit.parent_rope
        listener.set_plan_obj(ingest_planunit, x_parent_rope, create_missing_plans=True)

    _add_and_replace_planunit_stars(
        listener=listener,
        replace_star_list=star_data.replace_star_list,
        add_to_star_list=star_data.add_to_star_list,
        x_star=ingest_planunit.star,
    )


@dataclass
class starReplaceOrAddData:
    add_to_star_list: list = None
    replace_star_list: list = None


def _create_star_data(listener: PersonUnit, x_rope: RopeTerm) -> list:
    star_data = starReplaceOrAddData()
    star_data.add_to_star_list = []
    star_data.replace_star_list = []
    ancestor_ropes = get_ancestor_ropes(x_rope, listener.knot)
    root_rope = get_first_label_from_rope(x_rope, listener.knot)
    for ancestor_rope in ancestor_ropes:
        if ancestor_rope != root_rope:
            if listener.plan_exists(ancestor_rope):
                star_data.add_to_star_list.append(ancestor_rope)
            else:
                star_data.replace_star_list.append(ancestor_rope)
    return star_data


def _add_and_replace_planunit_stars(
    listener: PersonUnit,
    replace_star_list: list[RopeTerm],
    add_to_star_list: list[RopeTerm],
    x_star: float,
) -> None:
    for plan_rope in replace_star_list:
        listener.edit_plan_attr(plan_rope, star=x_star)
    for plan_rope in add_to_star_list:
        x_planunit = listener.get_plan_obj(plan_rope)
        x_planunit.star += x_star


def get_debtors_roll(x_duty: PersonUnit) -> list[PartnerUnit]:
    return [
        x_partnerunit
        for x_partnerunit in x_duty.partners.values()
        if x_partnerunit.partner_debt_lumen != 0
    ]


def get_ordered_debtors_roll(x_person: PersonUnit) -> list[PartnerUnit]:
    partners_ordered_list = get_debtors_roll(x_person)
    partners_ordered_list.sort(
        key=lambda x: (x.partner_debt_lumen, x.partner_name), reverse=True
    )
    return partners_ordered_list


def migrate_all_facts(src_listener: PersonUnit, dst_listener: PersonUnit):
    for x_factunit in src_listener.planroot.factunits.values():
        fact_context_rope = x_factunit.fact_context
        fact_state_rope = x_factunit.fact_state
        if dst_listener.plan_exists(fact_context_rope) is False:
            reason_context_plan = src_listener.get_plan_obj(fact_context_rope)
            dst_listener.set_plan_obj(
                reason_context_plan, reason_context_plan.parent_rope
            )
        if dst_listener.plan_exists(fact_state_rope) is False:
            fact_state_plan = src_listener.get_plan_obj(fact_state_rope)
            dst_listener.set_plan_obj(fact_state_plan, fact_state_plan.parent_rope)
        dst_listener.add_fact(fact_context_rope, fact_state_rope)


def listen_to_speaker_fact(
    listener: PersonUnit,
    speaker: PersonUnit,
    missing_fact_reason_contexts: list[RopeTerm] = None,
) -> PersonUnit:
    if missing_fact_reason_contexts is None:
        missing_fact_reason_contexts = list(listener.get_missing_fact_reason_contexts())
    for missing_fact_reason_context in missing_fact_reason_contexts:
        x_factunit = speaker.get_fact(missing_fact_reason_context)
        if x_factunit is not None:
            listener.add_fact(
                fact_context=x_factunit.fact_context,
                fact_state=x_factunit.fact_state,
                fact_lower=x_factunit.fact_lower,
                fact_upper=x_factunit.fact_upper,
                create_missing_plans=True,
            )


def listen_to_speaker_agenda(listener: PersonUnit, speaker: PersonUnit) -> PersonUnit:
    if listener.partner_exists(speaker.person_name) is False:
        raise MissingDebtorRespectError(
            f"listener '{listener.person_name}' person is assumed to have {speaker.person_name} partnerunit."
        )
    perspective_person = get_perspective_person(speaker, listener.person_name)
    if perspective_person.rational is False:
        return _allocate_irrational_partner_debt_lumen(listener, speaker.person_name)
    if listener.debtor_respect is None:
        return _allocate_inallocable_partner_debt_lumen(listener, speaker.person_name)
    if listener.person_name != speaker.person_name:
        agenda = generate_perspective_agenda(perspective_person)
    else:
        agenda = list(perspective_person.get_all_pledges().values())
    if len(agenda) == 0:
        return _allocate_inallocable_partner_debt_lumen(listener, speaker.person_name)
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_create_init_job_from_guts(
    moment_mstr_dir: str, listener_job: PersonUnit
):
    for x_partnerunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_partnerunit.partner_name
        moment_lasso = lassounit_shop(
            listener_job.planroot.get_plan_rope(), listener_job.knot
        )
        speaker_gut = open_gut_file(moment_mstr_dir, moment_lasso, speaker_id)
        if speaker_gut is None:
            speaker_gut = create_empty_person_from_person(listener_job, speaker_id)
        if speaker_gut:
            listen_to_speaker_agenda(listener_job, speaker_gut)


def listen_to_agendas_jobs_into_job(moment_mstr_dir: str, listener_job: PersonUnit):
    moment_lasso = lassounit_shop(
        listener_job.planroot.get_plan_rope(), listener_job.knot
    )
    for x_partnerunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_partnerunit.partner_name
        speaker_job = open_job_file(moment_mstr_dir, moment_lasso, speaker_id)
        if speaker_job is None:
            speaker_job = create_empty_person_from_person(listener_job, speaker_id)
        listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_agendas_duty_vision(
    listener_vision: PersonUnit,
    healer_lessonfilehandler: LessonFileHandler,
    healer_keep_rope: RopeTerm,
):
    listener_id = listener_vision.person_name
    for x_partnerunit in get_ordered_debtors_roll(listener_vision):
        if x_partnerunit.partner_name == listener_id:
            listener_duty = get_duty_person(
                moment_mstr_dir=healer_lessonfilehandler.moment_mstr_dir,
                person_name=healer_lessonfilehandler.person_name,
                moment_rope=healer_lessonfilehandler.moment_lasso.moment_rope,
                keep_rope=healer_keep_rope,
                knot=healer_lessonfilehandler.moment_lasso.knot,
                duty_person_name=listener_id,
            )
            listen_to_speaker_agenda(listener_vision, listener_duty)
        else:
            speaker_id = x_partnerunit.partner_name
            healer_name = healer_lessonfilehandler.person_name
            speaker_vision = rj_speaker_person(
                healer_lessonfilehandler.moment_mstr_dir,
                healer_lessonfilehandler.moment_lasso.moment_rope,
                healer_keep_rope,
                healer_lessonfilehandler.moment_lasso.knot,
                healer_name,
                speaker_id,
            )
            if speaker_vision is None:
                speaker_vision = create_empty_person_from_person(
                    listener_vision, speaker_id
                )
            listen_to_speaker_agenda(listener_vision, speaker_vision)


def listen_to_facts_duty_vision(
    new_vision: PersonUnit,
    healer_lessonfilehandler: LessonFileHandler,
    healer_keep_rope: RopeTerm,
):
    duty = get_duty_person(
        moment_mstr_dir=healer_lessonfilehandler.moment_mstr_dir,
        person_name=healer_lessonfilehandler.person_name,
        moment_rope=healer_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=healer_keep_rope,
        knot=healer_lessonfilehandler.moment_lasso.knot,
        duty_person_name=new_vision.person_name,
    )
    migrate_all_facts(duty, new_vision)
    for x_partnerunit in get_ordered_debtors_roll(new_vision):
        if x_partnerunit.partner_name != new_vision.person_name:
            speaker_vision = get_vision_person(
                healer_lessonfilehandler.moment_mstr_dir,
                healer_lessonfilehandler.person_name,
                healer_lessonfilehandler.moment_lasso.moment_rope,
                healer_keep_rope,
                healer_lessonfilehandler.moment_lasso.knot,
                x_partnerunit.partner_name,
            )
            if speaker_vision is not None:
                listen_to_speaker_fact(new_vision, speaker_vision)


def listen_to_facts_gut_job(moment_mstr_dir: str, new_job: PersonUnit):
    moment_lasso = lassounit_shop(new_job.planroot.get_plan_rope(), new_job.knot)
    old_job = open_job_file(moment_mstr_dir, moment_lasso, new_job.person_name)
    for x_partnerunit in get_ordered_debtors_roll(old_job):
        speaker_id = x_partnerunit.partner_name
        speaker_job = open_job_file(moment_mstr_dir, moment_lasso, speaker_id)
        if speaker_job is not None:
            listen_to_speaker_fact(new_job, speaker_job)


def listen_to_debtors_roll_jobs_into_job(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> PersonUnit:
    old_job = open_job_file(moment_mstr_dir, moment_lasso, person_name)
    new_job = create_listen_basis(old_job)
    if old_job.debtor_respect is None:
        return new_job
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_job)
    listen_to_facts_gut_job(moment_mstr_dir, new_job)
    return new_job


def listen_to_debtors_roll_duty_vision(
    healer_lessonfilehandler: LessonFileHandler,
    listener_id: PersonName,
    healer_keep_rope: RopeTerm,
) -> PersonUnit:
    duty = get_duty_person(
        moment_mstr_dir=healer_lessonfilehandler.moment_mstr_dir,
        person_name=healer_lessonfilehandler.person_name,
        moment_rope=healer_lessonfilehandler.moment_lasso.moment_rope,
        keep_rope=healer_keep_rope,
        knot=healer_lessonfilehandler.moment_lasso.knot,
        duty_person_name=listener_id,
    )
    new_duty = create_listen_basis(duty)
    if duty.debtor_respect is None:
        return new_duty
    listen_to_agendas_duty_vision(new_duty, healer_lessonfilehandler, healer_keep_rope)
    listen_to_facts_duty_vision(new_duty, healer_lessonfilehandler, healer_keep_rope)
    return new_duty


def listen_to_person_visions(
    listener_lessonfilehandler: LessonFileHandler, healer_keep_rope: RopeTerm
) -> None:
    moment_lasso = lassounit_shop(listener_lessonfilehandler.moment_lasso.moment_rope)
    gut = open_gut_file(
        listener_lessonfilehandler.moment_mstr_dir,
        moment_lasso,
        listener_lessonfilehandler.person_name,
    )
    new_job = create_listen_basis(gut)
    pre_job_dict = new_job.to_dict()
    gut.conpute()
    new_job.conpute()

    for x_healer_name, keep_dict in gut._healers_dict.items():
        listener_id = listener_lessonfilehandler.person_name
        healer_lessonfilehandler = copy_deepcopy(listener_lessonfilehandler)
        healer_lessonfilehandler.person_name = x_healer_name
        fact_state_keep_visions_and_listen(
            listener_id,
            keep_dict,
            healer_lessonfilehandler,
            new_job,
            healer_keep_rope=healer_keep_rope,
        )

    if new_job.to_dict() == pre_job_dict:
        agenda = list(gut.get_agenda_dict().values())
        _ingest_perspective_agenda(new_job, agenda)
        listen_to_speaker_fact(new_job, gut)

    save_job_file(listener_lessonfilehandler.moment_mstr_dir, new_job)


def fact_state_keep_visions_and_listen(
    listener_id: PersonName,
    keep_dict: dict[RopeTerm],
    healer_lessonfilehandler: LessonFileHandler,
    new_job: PersonUnit,
    healer_keep_rope: RopeTerm,
):
    for keep_path in keep_dict:
        healer_keep_rope = keep_path
        fact_state_keep_vision_and_listen(
            listener_id, healer_lessonfilehandler, new_job, healer_keep_rope
        )


def fact_state_keep_vision_and_listen(
    listener_person_name: PersonName,
    healer_lessonfilehandler: LessonFileHandler,
    new_job: PersonUnit,
    healer_keep_rope: RopeTerm,
):
    listener_id = listener_person_name
    if vision_file_exists(
        healer_lessonfilehandler.moment_mstr_dir,
        healer_lessonfilehandler.person_name,
        healer_lessonfilehandler.moment_lasso.moment_rope,
        healer_keep_rope,
        healer_lessonfilehandler.moment_lasso.knot,
        listener_id,
    ):
        keep_vision = get_vision_person(
            healer_lessonfilehandler.moment_mstr_dir,
            healer_lessonfilehandler.person_name,
            healer_lessonfilehandler.moment_lasso.moment_rope,
            healer_keep_rope,
            healer_lessonfilehandler.moment_lasso.knot,
            listener_id,
        )
    else:
        keep_vision = create_empty_person_from_person(new_job, new_job.person_name)
    listen_to_vision_agenda(new_job, keep_vision)


def listen_to_vision_agenda(listener: PersonUnit, vision: PersonUnit):
    for x_plan in vision._plan_dict.values():
        if listener.plan_exists(x_plan.get_plan_rope()) is False:
            listener.set_plan_obj(x_plan, x_plan.parent_rope)
        if listener.get_fact(x_plan.get_plan_rope()) is False:
            listener.set_plan_obj(x_plan, x_plan.parent_rope)
    for x_fact_rope, x_fact_unit in vision.planroot.factunits.items():
        listener.planroot.set_factunit(x_fact_unit)
    listener.conpute()


def create_vision_file_from_duty_file(
    healer_lessonfilehandler: LessonFileHandler,
    person_name: PersonName,
    healer_keep_rope: RopeTerm,
):
    x_vision = listen_to_debtors_roll_duty_vision(
        healer_lessonfilehandler,
        listener_id=person_name,
        healer_keep_rope=healer_keep_rope,
    )
    save_vision_person(
        healer_lessonfilehandler.moment_mstr_dir,
        healer_lessonfilehandler.person_name,
        healer_lessonfilehandler.moment_lasso.moment_rope,
        healer_keep_rope,
        healer_lessonfilehandler.moment_lasso.knot,
        x_vision,
    )
