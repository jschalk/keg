from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch10_person_listen._ref.ch10_semantic_types import PersonName


def create_empty_person_from_person(
    ref_person: PersonUnit, x_person_name: PersonName = None
) -> PersonUnit:
    x_person_name = ref_person.person_name if x_person_name is None else x_person_name
    x_knot = ref_person.knot
    x_fund_pool = ref_person.fund_pool
    x_fund_grain = ref_person.fund_grain
    x_respect_grain = ref_person.respect_grain
    x_mana_grain = ref_person.mana_grain
    return personunit_shop(
        person_name=x_person_name,
        planroot_rope=ref_person.planroot.get_plan_rope(),
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )


def create_listen_basis(x_person: PersonUnit) -> PersonUnit:
    x_listen = create_empty_person_from_person(x_person, x_person.person_name)
    x_listen.contacts = x_person.contacts
    x_listen.set_max_tree_traverse(x_person.max_tree_traverse)
    if x_person.credor_respect is not None:
        x_listen.set_credor_respect(x_person.credor_respect)
    if x_person.debtor_respect is not None:
        x_listen.set_debtor_respect(x_person.debtor_respect)
    for x_contactunit in x_listen.contacts.values():
        x_contactunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: PersonUnit) -> PersonUnit:
    default_job = create_listen_basis(gut)
    default_job.last_lesson_id = gut.last_lesson_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
