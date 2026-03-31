from src.ch07_person_logic.person_main import personunit_shop
from src.ch24_person_viewer.person_viewer_tool import (
    get_person_view_dict,
    get_plan_view_dict,
)
from src.ref.keywords import Ch24Keywords as kw, ExampleStrs as exx


def test_get_person_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_believer = personunit_shop(exx.sue)
    sue_believer.conpute()

    # WHEN
    sue_person_view_dict = get_person_view_dict(sue_believer)

    # THEN
    assert set(sue_person_view_dict.keys()) == {
        # kw.groupunits,
        kw.contacts,
        kw.planroot,
    }
    sue_plan_view_dict = sue_person_view_dict.get(kw.planroot)
    expected_sue_plan_view_dict = get_plan_view_dict(sue_believer.planroot)
    assert sue_plan_view_dict == expected_sue_plan_view_dict
