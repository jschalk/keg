from ch04_rope.rope import RopeTerm, create_rope_from_labels
from ch07_person_logic.person_main import personunit_shop
from ch12_keep._ref.ch12_semantic_types import ContactName, PersonName
from ch12_keep.rivercycle import get_patientledger
from ref.keywords import ExampleStrs as exx


def get_nation_texas_rope() -> RopeTerm:
    naton_str = "nation"
    usa_str = "usa"
    texas_str = "texas"
    return create_rope_from_labels([naton_str, usa_str, texas_str])


def example_yao_patientledger() -> dict[str, float]:
    yao_contact_cred_lumen = 7
    bob_contact_cred_lumen = 3
    zia_contact_cred_lumen = 10
    yao_person = personunit_shop(exx.yao)
    yao_person.add_contactunit(exx.yao, yao_contact_cred_lumen)
    yao_person.add_contactunit(exx.bob, bob_contact_cred_lumen)
    yao_person.add_contactunit(exx.zia, zia_contact_cred_lumen)
    return get_patientledger(yao_person)


def example_bob_patientledger() -> dict[str, float]:
    yao_contact_cred_lumen = 1
    bob_contact_cred_lumen = 7
    zia_contact_cred_lumen = 42
    bob_person = personunit_shop(exx.bob)
    bob_person.add_contactunit(exx.yao, yao_contact_cred_lumen)
    bob_person.add_contactunit(exx.bob, bob_contact_cred_lumen)
    bob_person.add_contactunit(exx.zia, zia_contact_cred_lumen)
    return get_patientledger(bob_person)


def example_zia_patientledger() -> dict[str, float]:
    yao_contact_cred_lumen = 89
    bob_contact_cred_lumen = 150
    zia_contact_cred_lumen = 61
    zia_person = personunit_shop(exx.zia)
    zia_person.add_contactunit(exx.yao, yao_contact_cred_lumen)
    zia_person.add_contactunit(exx.bob, bob_contact_cred_lumen)
    zia_person.add_contactunit(exx.zia, zia_contact_cred_lumen)
    return get_patientledger(zia_person)


def example_yao_bob_zia_patientledgers() -> dict[PersonName : dict[ContactName, float]]:
    return {
        exx.yao: example_yao_patientledger,
        exx.bob: example_bob_patientledger,
        exx.zia: example_zia_patientledger,
    }


def example_yao_bob_zia_need_dues() -> dict[ContactName, float]:
    yao_sum = sum(example_yao_patientledger().values())
    bob_sum = sum(example_bob_patientledger().values())
    zia_sum = sum(example_zia_patientledger().values())

    return {
        exx.yao: yao_sum - 60000,
        exx.bob: bob_sum - 500000,
        exx.zia: zia_sum - 4000,
    }
