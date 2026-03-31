from src.ch03_workforce._ref.ch03_semantic_types import GroupTitle
from src.ch03_workforce.workforce import (
    get_workforceunit_from_dict,
    laborunit_get_from_dict,
    laborunit_shop,
    workforceunit_shop,
)
from src.ref.keywords import Ch03Keywords as kw, ExampleStrs as exx


def test_LaborUnit_to_dict_ReturnsObj_Scenario0_solo_IsTrue():
    # ESTABLISH
    bob_solo_bool = True
    x_laborunit = laborunit_shop(exx.bob, solo=bob_solo_bool)

    # WHEN
    labor_dict = x_laborunit.to_dict()

    # THEN
    assert labor_dict
    assert labor_dict.get(kw.labor_title) == exx.bob
    assert labor_dict.get(kw.solo) == bob_solo_bool
    assert set(labor_dict.keys()) == {kw.labor_title, kw.solo}


def test_LaborUnit_to_dict_ReturnsObj_Scenario1_solo_IsFalse():
    # ESTABLISH
    x_laborunit = laborunit_shop(exx.bob, solo=False)

    # WHEN
    labor_dict = x_laborunit.to_dict()

    # THEN
    assert labor_dict
    assert labor_dict.get(kw.labor_title) == exx.bob
    assert set(labor_dict.keys()) == {kw.labor_title}


def test_laborunit_get_from_dict_ReturnsObj_Scenario0_solo_KeyExists():
    # ESTABLISH
    bob_solo_bool = True
    expected_bob_laborunit = laborunit_shop(exx.bob, solo=bob_solo_bool)
    bob_labor_dict = expected_bob_laborunit.to_dict()

    # WHEN
    gen_bob_labor = laborunit_get_from_dict(bob_labor_dict)

    # THEN
    assert gen_bob_labor == expected_bob_laborunit


def test_laborunit_get_from_dict_ReturnsObj_Scenario1_solo_KeyDoesNotExist():
    # ESTABLISH
    bob_solo_bool = False
    expected_bob_laborunit = laborunit_shop(exx.bob, solo=bob_solo_bool)
    bob_labor_dict = expected_bob_laborunit.to_dict()
    assert set(bob_labor_dict.keys()) == {kw.labor_title}

    # WHEN
    gen_bob_labor = laborunit_get_from_dict(bob_labor_dict)

    # THEN
    assert gen_bob_labor.solo == False
    assert gen_bob_labor == expected_bob_laborunit


def test_WorkforceUnit_to_dict_ReturnsDictWithSingle_laborunit():
    # ESTABLISH
    bob_labor_title = GroupTitle("Bob")
    bob_laborunit = laborunit_shop(bob_labor_title)
    x_labors = {bob_labor_title: bob_laborunit}
    x_workforceunit = workforceunit_shop(labors=x_labors)

    # WHEN
    obj_dict = x_workforceunit.to_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {kw.labors: {bob_labor_title: bob_laborunit.to_dict()}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_get_workforceunit_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    expected_workforceunit = workforceunit_shop()
    expected_workforceunit.add_labor(exx.run, True)
    expected_workforceunit.add_labor(exx.xio, False)
    run_laborunit = expected_workforceunit.get_laborunit(exx.run)
    xio_laborunit = expected_workforceunit.get_laborunit(exx.xio)
    src_workforceunit_dict = {
        kw.labors: {
            exx.run: run_laborunit.to_dict(),
            exx.xio: xio_laborunit.to_dict(),
        }
    }

    # WHEN
    gen_workforceunit = get_workforceunit_from_dict(src_workforceunit_dict)

    # THEN
    assert gen_workforceunit == expected_workforceunit
