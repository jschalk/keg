from src.ch02_partner.group import groupunit_shop, membership_shop
from src.ch03_workforce._ref.ch03_semantic_types import GroupTitle
from src.ch03_workforce.workforce import (
    LaborHeir,
    LaborUnit,
    WorkforceHeir,
    WorkforceUnit,
    laborheir_shop,
    laborunit_shop,
    workforceheir_shop,
    workforceunit_shop,
)
from src.ref.keywords import Ch03Keywords as kw, ExampleStrs as exx


def test_LaborUnit_Exists():
    # ESTABLISH / WHEN
    x_laborunit = LaborUnit()

    # THEN
    assert not x_laborunit.labor_title
    assert not x_laborunit.solo
    obj_attrs = set(x_laborunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {kw.labor_title, kw.solo}


def test_laborunit_shop_ReturnsObj_Scenario0_WithParameters():
    # ESTABLISH
    bob_solo_bool = True

    # WHEN
    x_laborunit = laborunit_shop(exx.bob, solo=bob_solo_bool)

    # THEN
    assert x_laborunit.labor_title == exx.bob
    assert x_laborunit.solo == bob_solo_bool


def test_laborunit_shop_ReturnsObj_Scenario1_WithParametersNot():
    # ESTABLISH

    # WHEN
    x_laborunit = laborunit_shop(exx.bob)

    # THEN
    assert x_laborunit.labor_title == exx.bob
    assert x_laborunit.solo is False


def test_LaborHeir_Exists():
    # ESTABLISH / WHEN
    x_laborheir = LaborHeir()

    # THEN
    assert not x_laborheir.labor_title
    assert not x_laborheir.solo
    assert not x_laborheir.parent_solo
    obj_attrs = set(x_laborheir.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {kw.labor_title, kw.solo, kw.parent_solo}


def test_laborheir_shop_ReturnsObj():
    # ESTABLISH
    bob_solo_bool = True

    # WHEN
    x_laborheir = laborheir_shop(exx.bob, bob_solo_bool)

    # THEN
    assert x_laborheir.labor_title == exx.bob
    assert x_laborheir.solo == bob_solo_bool


def test_WorkforceUnit_Exists():
    # ESTABLISH / WHEN
    x_workforceunit = WorkforceUnit()

    # THEN
    assert x_workforceunit
    assert not x_workforceunit.labors
    obj_attrs = set(x_workforceunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {kw.labors}


def test_workforceunit_shop_ReturnsWithCorrectAttributes_v1():
    # ESTABLISH
    x_labors = {1}

    # WHEN
    x_workforceunit = workforceunit_shop(labors=x_labors)

    # THEN
    assert x_workforceunit
    assert x_workforceunit.labors == x_labors


def test_workforceunit_shop_ifEmptyReturnsWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_workforceunit = workforceunit_shop()

    # THEN
    assert x_workforceunit
    assert x_workforceunit.labors == {}


def test_WorkforceUnit_add_labor_SetsAttr_Secnario0():
    # ESTABLISH
    x_workforceunit = workforceunit_shop()
    assert len(x_workforceunit.labors) == 0

    # WHEN
    x_workforceunit.add_labor(labor_title=exx.yao)

    # THEN
    assert len(x_workforceunit.labors) == 1
    expected_labors = {exx.yao: laborunit_shop(exx.yao)}
    assert x_workforceunit.labors == expected_labors


def test_WorkforceUnit_add_labor_SetsAttr_Secnario1():
    # ESTABLISH
    x_workforceunit = workforceunit_shop()
    yao_solo_bool = True
    assert len(x_workforceunit.labors) == 0

    # WHEN
    x_workforceunit.add_labor(labor_title=exx.yao, solo=yao_solo_bool)

    # THEN
    assert len(x_workforceunit.labors) == 1
    expected_labors = {exx.yao: laborunit_shop(exx.yao, solo=yao_solo_bool)}
    assert x_workforceunit.labors == expected_labors


def test_WorkforceUnit_laborunit_exists_ReturnsObj():
    # ESTABLISH
    x_workforceunit = workforceunit_shop()
    assert x_workforceunit.laborunit_exists(exx.yao) is False

    # WHEN
    x_workforceunit.add_labor(labor_title=exx.yao)

    # THEN
    assert x_workforceunit.laborunit_exists(exx.yao)


def test_WorkforceUnit_del_laborunit_Deletes_labors_v1():
    # ESTABLISH
    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(labor_title=exx.yao)
    x_workforceunit.add_labor(labor_title=exx.sue)
    assert len(x_workforceunit.labors) == 2

    # WHEN
    x_workforceunit.del_laborunit(labor_title=exx.sue)

    # THEN
    assert len(x_workforceunit.labors) == 1


def test_WorkforceHeir_Exists():
    # ESTABLISH / WHEN
    x_workforceheir = WorkforceHeir()

    # THEN
    assert x_workforceheir
    assert not x_workforceheir.labors
    assert not x_workforceheir.person_name_is_workforce
    obj_attrs = set(x_workforceheir.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {kw.labors, kw.person_name_is_workforce}


def test_workforceheir_shop_ReturnsObj_Scenario1_WithAttributes():
    # ESTABLISH
    swim_labor_title = GroupTitle("swimmers")
    _person_name_x_workforceunit = "example"
    x_labors = {swim_labor_title: laborunit_shop(swim_labor_title)}

    # WHEN
    x_workforceheir = workforceheir_shop(
        labors=x_labors, person_name_is_workforce=_person_name_x_workforceunit
    )

    # THEN
    assert x_workforceheir
    assert x_workforceheir.labors == x_labors
    assert x_workforceheir.person_name_is_workforce == _person_name_x_workforceunit


def test_WorkforceHeir_set_person_name_is_workforce_SetsAttribute_Emptyx_labors():
    # ESTABLISH
    x_labors = {}
    x_workforceheir = workforceheir_shop(labors=x_labors)
    assert x_workforceheir.person_name_is_workforce is False

    # WHEN
    groupunits = {}
    x_workforceheir.set_person_name_is_workforce(groupunits, person_name="")

    # THEN
    assert x_workforceheir.person_name_is_workforce


def test_WorkforceHeir_set_person_name_is_workforce_SetsAttribute_NonEmptyx_labors_v1():
    # ESTABLISH
    yao_groupunit = groupunit_shop(exx.yao)
    sue_groupunit = groupunit_shop(exx.sue)
    yao_groupunit.set_g_membership(membership_shop(exx.yao, partner_name=exx.yao))
    sue_groupunit.set_g_membership(membership_shop(exx.sue, partner_name=exx.sue))
    x_groupunits = {exx.yao: yao_groupunit, exx.sue: sue_groupunit}
    person_name = exx.yao

    x_labors = {exx.yao}
    x_workforceheir = workforceheir_shop(labors=x_labors)
    assert x_workforceheir.person_name_is_workforce is False

    # WHEN
    x_workforceheir.set_person_name_is_workforce(x_groupunits, person_name)

    # THEN
    assert x_workforceheir.person_name_is_workforce


def test_WorkforceHeir_set_person_name_is_workforce_SetsAttribute_NonEmptyx_labors_v2():
    # ESTABLISH
    yao_groupunit = groupunit_shop(exx.yao)
    sue_groupunit = groupunit_shop(exx.sue)
    yao_groupunit.set_g_membership(membership_shop(exx.yao, partner_name=exx.yao))
    sue_groupunit.set_g_membership(membership_shop(exx.sue, partner_name=exx.sue))
    x_groupunits = {exx.yao: yao_groupunit, exx.sue: sue_groupunit}
    x_labors = {exx.sue}
    x_workforceheir = workforceheir_shop(labors=x_labors)
    assert yao_groupunit.get_partner_membership(exx.yao) is not None
    assert x_workforceheir.person_name_is_workforce is False

    # WHEN
    x_workforceheir.set_person_name_is_workforce(x_groupunits, exx.yao)

    # THEN
    assert x_workforceheir.person_name_is_workforce is False


def test_WorkforceHeir_set_person_name_is_workforce_SetsAttribute_NonEmptyx_labors_v3():
    # ESTABLISH
    yao_groupunit = groupunit_shop(exx.yao)
    sue_groupunit = groupunit_shop(exx.sue)
    bob_groupunit = groupunit_shop(exx.bob)
    yao_groupunit.set_g_membership(membership_shop(exx.yao, partner_name=exx.yao))
    sue_groupunit.set_g_membership(membership_shop(exx.sue, partner_name=exx.sue))

    swim_str = ",swim"
    swim_groupunit = groupunit_shop(group_title=swim_str)
    swim_groupunit.set_g_membership(membership_shop(swim_str, partner_name=exx.yao))
    swim_groupunit.set_g_membership(membership_shop(swim_str, partner_name=exx.sue))
    x_groupunits = {
        exx.yao: yao_groupunit,
        exx.sue: sue_groupunit,
        exx.bob: bob_groupunit,
        swim_str: swim_groupunit,
    }

    x_labors = {swim_str}
    x_workforceheir = workforceheir_shop(labors=x_labors)
    assert x_workforceheir.person_name_is_workforce is False
    x_workforceheir.set_person_name_is_workforce(x_groupunits, person_name=exx.yao)
    assert x_workforceheir.person_name_is_workforce

    # WHEN
    swim_groupunit.del_membership(exx.yao)
    x_workforceheir.set_person_name_is_workforce(x_groupunits, exx.yao)

    # THEN
    assert x_workforceheir.person_name_is_workforce is False


def test_WorkforceHeir_set_labors_Scenario0_WorkforceUnitIsEmptyAndParentWorkforceHeirIsEmpty():
    # ESTABLISH
    x_workforceheir = workforceheir_shop(labors={})
    parent_workforceheir_empty = workforceheir_shop()
    x_workforceunit = workforceunit_shop()

    # WHEN
    x_workforceheir.set_labors(
        parent_workforceheir=parent_workforceheir_empty,
        workforceunit=x_workforceunit,
        groupunits=None,
    )

    # THEN
    x_workforceheir.labors = {}


def test_WorkforceHeir_set_labors_Scenario1_WorkforceUnitNotEmpty_ParentWorkforceHeirIsNone():
    # ESTABLISH
    xio_solo_bool = True
    swim_str = ",swim"
    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(exx.xio, xio_solo_bool)
    x_workforceunit.add_labor(swim_str)
    x_workforceheir = workforceheir_shop()
    assert x_workforceheir.labors == {}

    # WHEN
    x_workforceheir.set_labors(None, workforceunit=x_workforceunit, groupunits=None)

    # THEN
    assert x_workforceheir.labors.keys() == x_workforceunit.labors.keys()
    expected_labors = {
        exx.xio: laborheir_shop(exx.xio, xio_solo_bool),
        swim_str: laborheir_shop(swim_str, False),
    }
    print(f"{x_workforceheir.labors=}")
    print(f"    {expected_labors=}")
    assert x_workforceheir.labors == expected_labors


def test_WorkforceHeir_set_labors_Scenario2_WorkforceUnitNotEmpty_ParentWorkforceHeirEmpty():
    # ESTABLISH
    xio_solo_bool = True
    swim_str = ",swim"
    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(exx.xio, xio_solo_bool)
    x_workforceunit.add_labor(swim_str)
    x_workforceheir = workforceheir_shop()
    parent_workforceheir_empty = workforceheir_shop()
    assert x_workforceheir.labors == {}

    # WHEN
    x_workforceheir.set_labors(
        parent_workforceheir_empty, x_workforceunit, groupunits=None
    )

    # THEN
    assert x_workforceheir.labors.keys() == x_workforceunit.labors.keys()
    expected_labors = {
        exx.xio: laborheir_shop(exx.xio, xio_solo_bool),
        swim_str: laborheir_shop(swim_str, False),
    }
    print(f"{x_workforceheir.labors=}")
    print(f"    {expected_labors=}")
    assert x_workforceheir.labors == expected_labors


def test_WorkforceHeir_set_labors_Scenario3_WorkforceUnit_Empty_ParentWorkforceHeirNotEmpty():
    # ESTABLISH
    xio_solo_bool = True
    swim_str = ",swim"
    workforceunit_swim = workforceunit_shop()
    workforceunit_swim.add_labor(exx.xio, xio_solo_bool)
    workforceunit_swim.add_labor(swim_str, False)
    empty_workforceheir = workforceheir_shop()
    parent_workforceheir = workforceheir_shop()
    parent_workforceheir.set_labors(
        empty_workforceheir, workforceunit_swim, groupunits=None
    )

    workforceunit_empty = workforceunit_shop()
    x_workforceheir = workforceheir_shop()
    assert x_workforceheir.labors == {}
    assert workforceunit_empty.labors == {}

    # WHEN
    x_workforceheir.set_labors(
        parent_workforceheir, workforceunit_empty, groupunits=None
    )

    # THEN
    assert x_workforceheir.labors.keys() == parent_workforceheir.labors.keys()
    expected_labors = {
        exx.xio: laborheir_shop(exx.xio, xio_solo_bool),
        swim_str: laborheir_shop(swim_str, False),
    }
    print(f"{x_workforceheir.labors=}")
    print(f"    {expected_labors=}")
    assert x_workforceheir.labors == expected_labors


def test_WorkforceHeir_set_labors_Scenario4_WorkforceUnitEqualParentWorkforceHeir_NonEmpty():
    # ESTABLISH
    xio_solo_bool = True
    xio_workforceunit = workforceunit_shop()
    xio_workforceunit.add_labor(exx.xio, xio_solo_bool)
    empty_workforceheir = workforceheir_shop()
    parent_workforceheir = workforceheir_shop()
    parent_workforceheir.set_labors(
        empty_workforceheir, xio_workforceunit, groupunits=None
    )

    swim_str = ",swim"
    swim_workforceunit = workforceunit_shop()
    swim_workforceunit.add_labor(swim_str)

    x_workforceheir = workforceheir_shop()
    assert x_workforceheir.labors == {}

    # WHEN
    x_workforceheir.set_labors(
        parent_workforceheir, swim_workforceunit, groupunits=None
    )

    # THEN
    assert x_workforceheir.labors.keys() != parent_workforceheir.labors.keys()
    assert x_workforceheir.labors.keys() != swim_workforceunit.labors.keys()
    expected_labors = {
        exx.xio: laborheir_shop(exx.xio, xio_solo_bool),
        swim_str: laborheir_shop(swim_str, False),
    }
    print(f"{x_workforceheir.labors=}")
    print(f"    {expected_labors=}")
    assert x_workforceheir.labors == expected_labors


# def test_WorkforceHeir_set_labors_Scenario5_WorkforceUnit_NotEqual_ParentWorkforceHeir_NonEmpty():
#     # ESTABLISH
#     yao_groupunit = groupunit_shop(exx.yao)
#     sue_groupunit = groupunit_shop(exx.sue)
#     bob_groupunit = groupunit_shop(exx.bob)
#     bob_groupunit = groupunit_shop(exx.zia)
#     yao_groupunit.set_g_membership(membership_shop(exx.yao, partner_name=exx.yao))
#     sue_groupunit.set_g_membership(membership_shop(exx.sue, partner_name=exx.sue))

#     swim2_str = ",swim2"
#     swim2_groupunit = groupunit_shop(group_title=swim2_str)
#     swim2_groupunit.set_g_membership(membership_shop(swim2_str, partner_name=exx.yao))
#     swim2_groupunit.set_g_membership(membership_shop(swim2_str, partner_name=exx.sue))

#     swim3_str = ",swim3"
#     swim3_groupunit = groupunit_shop(group_title=swim3_str)
#     swim3_groupunit.set_g_membership(membership_shop(swim3_str, partner_name=exx.yao))
#     swim3_groupunit.set_g_membership(membership_shop(swim3_str, partner_name=exx.sue))
#     swim3_groupunit.set_g_membership(membership_shop(swim3_str, partner_name=exx.zia))

#     x_groupunits = {
#         exx.yao: yao_groupunit,
#         exx.sue: sue_groupunit,
#         exx.bob: bob_groupunit,
#         swim2_str: swim2_groupunit,
#         swim3_str: swim3_groupunit,
#     }

#     parent_workforceunit = workforceunit_shop()
#     parent_workforceunit.add_labor(labor_title=swim3_str)
#     parent_workforceheir = workforceheir_shop()
#     parent_workforceheir.set_labors(
#         parent_workforceheir=None, workforceunit=parent_workforceunit, groupunits=None
#     )

#     workforceunit_swim2 = workforceunit_shop()
#     workforceunit_swim2.add_labor(labor_title=swim2_str)
#     x_workforceheir = workforceheir_shop()
#     assert x_workforceheir.labors == {}

#     # WHEN
#     x_workforceheir.set_labors(parent_workforceheir, workforceunit_swim2, x_groupunits)

#     # THEN
#     assert x_workforceheir.labors.keys() == workforceunit_swim2.labors.keys()
#     assert len(x_workforceheir.labors) == 1
#     assert list(x_workforceheir.labors) == [swim2_str]


def test_WorkforceUnit_get_laborunit_ReturnsObj():
    # ESTABLISH
    climb_str = ",climbers"
    hike_str = ",hikers"
    swim_str = ";swimmers"

    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(climb_str)
    x_workforceunit.add_labor(hike_str)
    x_workforceunit.add_labor(swim_str)

    # WHEN / THEN
    assert x_workforceunit.get_laborunit(hike_str) is not None
    assert x_workforceunit.get_laborunit(swim_str) is not None
    assert x_workforceunit.get_laborunit(exx.run) is None


def test_WorkforceHeir_labor_title_in_ReturnsBoolWhen_laborsNotEmpty():
    # ESTABLISH
    swim_str = ",swim"
    hike_str = ",hike"
    swim_dict = {swim_str}
    hike_dict = {hike_str}
    x_workforceunit = workforceunit_shop()
    x_workforceunit.add_labor(labor_title=swim_str)
    x_workforceunit.add_labor(labor_title=hike_str)
    x_workforceheir = workforceheir_shop()
    x_workforceheir.set_labors(
        parent_workforceheir=None, workforceunit=x_workforceunit, groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert swim_str in x_workforceheir.labors
    assert hike_str in x_workforceheir.labors
    print(f"{hunt_str in x_workforceheir.labors=}")
    assert hunt_str not in x_workforceheir.labors
    assert play_str not in x_workforceheir.labors
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_workforceheir.has_labor(swim_dict)
    assert x_workforceheir.has_labor(hike_dict)
    assert x_workforceheir.has_labor(hunt_dict) is False
    assert x_workforceheir.has_labor(hunt_hike_dict)
    assert x_workforceheir.has_labor(hunt_play_dict) is False


def test_WorkforceHeir_has_labor_ReturnsObj():
    # ESTABLISH
    hike_str = ",hike"
    hike_dict = {hike_str}
    hike_laborunit = laborunit_shop(hike_str)
    hike_workforceunit = workforceunit_shop({hike_str: hike_laborunit})
    hike_workforceheir = workforceheir_shop()
    hike_workforceheir.set_labors(
        parent_workforceheir=None, workforceunit=hike_workforceunit, groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert len(hike_workforceheir.labors) == 1
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert hike_workforceheir.has_labor(hike_dict)
    assert not hike_workforceheir.has_labor(hunt_dict)
    assert not hike_workforceheir.has_labor(play_dict)
    assert hike_workforceheir.has_labor(hunt_hike_dict)
    assert not hike_workforceheir.has_labor(hunt_play_dict)
