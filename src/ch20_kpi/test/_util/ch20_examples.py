from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch13_time.epoch_main import add_epoch_planunit
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def get_a23_sue_clean_example() -> PersonUnit:
    sue_person = personunit_shop(exx.sue, exx.a23)
    add_epoch_planunit(sue_person)
    sue_person.add_partnerunit(exx.bob, 2)
    sue_person.add_partnerunit(exx.sue, 1)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sue_person.add_plan(clean_rope, 1, pledge=True)
    sue_person.get_partner(exx.sue).add_membership(exx.run)
    sue_person.conpute()
    return sue_person


def get_ep8_sue_clean_example() -> PersonUnit:
    sue_person = personunit_shop(exx.sue, exx.ep8)
    add_epoch_planunit(sue_person)
    sue_person.add_partnerunit(exx.zia, 2)
    sue_person.add_partnerunit(exx.yao, 1)
    sue_person.add_partnerunit(exx.sue, 1)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    mop_rope = sue_person.make_rope(casa_rope, exx.mop)
    sue_person.add_plan(mop_rope, 1, pledge=True)
    sue_person.get_partner(exx.sue).add_membership(exx.run)
    sue_person.conpute()
    return sue_person


def get_ep8_yao_clean_example() -> PersonUnit:
    yao_person = personunit_shop(exx.yao, exx.ep8)
    add_epoch_planunit(yao_person)
    yao_person.add_partnerunit(exx.zia, 2)
    yao_person.add_partnerunit(exx.yao, 1)
    yao_person.add_partnerunit(exx.sue, 1)
    casa_rope = yao_person.make_l1_rope(exx.casa)
    swim_rope = yao_person.make_rope(casa_rope, exx.swim)
    yao_person.add_plan(swim_rope, 1, pledge=True)
    yao_person.get_partner(exx.yao).add_membership(exx.run)
    yao_person.conpute()
    return yao_person
