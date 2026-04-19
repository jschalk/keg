from ch04_rope.rope import create_rope
from ch05_reason.reason_main import FactUnit, factunit_shop
from ch11_bud.bud_main import BudUnit, budunit_shop
from ref.keywords import ExampleStrs as exx


def get_ch11_example_moment_rope() -> str:
    return "fizz"


def example_casa_clean_factunit() -> FactUnit:
    casa_rope = create_rope(exx.a23, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    return factunit_shop(casa_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    casa_rope = create_rope(exx.a23, "casa")
    dirty_rope = create_rope(casa_rope, "dirty")
    return factunit_shop(casa_rope, dirty_rope)


def example_casa_grimy_factunit() -> FactUnit:
    casa_rope = create_rope(exx.a23, "casa")
    grimy_rope = create_rope(casa_rope, "grimy")
    return factunit_shop(casa_rope, grimy_rope)


def example_sky_blue_factunit() -> FactUnit:
    sky_rope = create_rope(exx.a23, "sky color")
    blue_rope = create_rope(sky_rope, "blue")
    return factunit_shop(sky_rope, blue_rope)


def get_budunit_55_example() -> BudUnit:
    x_bud_time = 55
    return budunit_shop(x_bud_time)


def get_budunit_66_example() -> BudUnit:
    t66_bud_time = 66
    t66_budunit = budunit_shop(t66_bud_time)
    t66_budunit.set_bud_contact_net("Sue", -5)
    t66_budunit.set_bud_contact_net("Bob", 5)
    return t66_budunit


def get_budunit_88_example() -> BudUnit:
    t88_bud_time = 88
    t88_budunit = budunit_shop(t88_bud_time)
    t88_budunit.quota = 800
    return t88_budunit


def get_budunit_invalid_example() -> BudUnit:
    t55_bud_time = 55
    t55_budunit = budunit_shop(t55_bud_time)
    t55_budunit.set_bud_contact_net("Sue", -5)
    t55_budunit.set_bud_contact_net("Bob", 3)
    return t55_budunit
