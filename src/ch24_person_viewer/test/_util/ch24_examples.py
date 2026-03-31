from datetime import datetime
from enum import Enum
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx

SUE_PERSON = personunit_shop(exx.sue, exx.a23)
CASA_ROPE = SUE_PERSON.make_l1_rope(exx.casa)
CLEAN_ROPE = SUE_PERSON.make_rope(CASA_ROPE, exx.clean)
MOP_ROPE = SUE_PERSON.make_rope(CLEAN_ROPE, exx.mop)
SWEEP_ROPE = SUE_PERSON.make_rope(CLEAN_ROPE, exx.sweep)
SCRUB_ROPE = SUE_PERSON.make_rope(CLEAN_ROPE, exx.scrub)


class ExampleValuesRef(str, Enum):
    sue = exx.sue
    a23 = exx.a23
    casa_str = exx.casa
    casa_rope = CASA_ROPE
    clean_str = exx.clean
    clean_rope = CLEAN_ROPE
    mop_str = exx.mop
    mop_rope = MOP_ROPE
    sweep_str = exx.sweep
    sweep_rope = SWEEP_ROPE
    scrub_str = exx.sweep
    scrub_rope = SCRUB_ROPE

    def __str__(self):
        return self.value
