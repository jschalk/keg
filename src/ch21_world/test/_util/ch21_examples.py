from src.ch07_person_logic.person_main import PersonUnit
from src.ch14_moment.test._util.ch14_examples import _example_empty_bob_personunit
from src.ref.keywords import ExampleStrs as exx


def get_mop_with_no_reason_personunit_example() -> PersonUnit:
    bob_person = _example_empty_bob_personunit()
    casa_rope = bob_person.make_l1_rope(exx.casa)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(mop_rope, pledge=True)
    return bob_person


def get_bob_mop_reason_personunit_example() -> PersonUnit:
    bob_person = _example_empty_bob_personunit()
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_person.make_l1_rope(exx.casa)
    floor_rope = bob_person.make_rope(casa_rope, floor_str)
    clean_rope = bob_person.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_person.make_rope(floor_rope, dirty_str)
    mop_rope = bob_person.make_rope(casa_rope, exx.mop)
    bob_person.add_plan(floor_rope)
    bob_person.add_plan(clean_rope)
    bob_person.add_plan(dirty_rope)
    bob_person.add_plan(mop_rope, pledge=True)
    bob_person.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    return bob_person
