from ch07_person_logic.person_main import personunit_shop
from ch07_person_logic.person_tool import get_person_unique_short_ropes
from ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_get_person_unique_short_ropes_ReturnsObj_Scenario0_RootOnly():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)

    # WHEN
    unique_short_ropes = get_person_unique_short_ropes(sue_person)

    # THEN
    assert unique_short_ropes == {sue_person.planroot.get_plan_rope(): "Amy23"}


def test_get_person_unique_short_ropess_ReturnsObj_Scenario1_PlansWithUniqueLabels():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    mop_rope = sue_person.make_rope(casa_rope, exx.mop)
    sue_person.add_plan(mop_rope)

    # WHEN
    unique_short_ropes = get_person_unique_short_ropes(sue_person)

    # THEN
    root_rope = sue_person.planroot.get_plan_rope()
    assert unique_short_ropes == {
        root_rope: "Amy23",
        casa_rope: exx.casa,
        mop_rope: exx.mop,
    }


def test_get_person_unique_short_ropess_ReturnsObj_Scenario2_PlansWithCommonLabels():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    casa_mop_rope = sue_person.make_rope(casa_rope, exx.mop)
    sports_str = "sports"
    sports_rope = sue_person.make_l1_rope(sports_str)
    sports_mop_rope = sue_person.make_rope(sports_rope, exx.mop)
    sue_person.add_plan(casa_mop_rope)
    sue_person.add_plan(sports_mop_rope)

    # WHEN
    unique_short_ropes = get_person_unique_short_ropes(sue_person)

    # THEN
    root_rope = sue_person.planroot.get_plan_rope()
    knot = sue_person.knot
    expected_short_casa_mop = f"{exx.casa}{knot}{exx.mop}"
    assert unique_short_ropes.get(casa_mop_rope) == expected_short_casa_mop
    assert unique_short_ropes == {
        root_rope: "Amy23",
        casa_rope: exx.casa,
        casa_mop_rope: expected_short_casa_mop,
        sports_rope: sports_str,
        sports_mop_rope: f"{sports_str}{knot}{exx.mop}",
    }
