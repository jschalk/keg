from ch45_wheel.wheel_logic import (
    FamilyUnit,
    familyunit_shop,
    PillarUnit,
    pillarunit_shop,
    FAMU_STATUSES,
    WheelUnit,
    wheelunit_shop,
    LandUnit,
    landunit_shop,
)
from ch99_glossary.ch_keyword import Ch45Keywords as kw, ExampleStrs as exx
from pytest import raises as pytest_raises

# linchpin


def test_FamilyUnit_Exists():
    # ESTABLISH / WHEN
    x_familyunit = FamilyUnit()

    # THEN
    assert x_familyunit
    assert not x_familyunit.famu_name
    assert not x_familyunit.prestige
    assert not x_familyunit.famu_status
    assert set(x_familyunit.__dict__.keys()) == {
        "famu_name",
        kw.prestige,
        "famu_status",
    }


def test_FAMU_STATUSES_Exists():
    # ESTABLISH / WHEN / THEN
    assert FAMU_STATUSES == {kw.winning, kw.losing, kw.stable, None}


def test_FamilyUnit_set_famu_status_SetsAttr_Scenario0_FAMU_STATUSES():
    # ESTABLISH
    x_familyunit = FamilyUnit()
    assert x_familyunit.famu_status is None
    for x_famu_status in FAMU_STATUSES:
        # WHEN
        x_familyunit.set_famu_status(x_famu_status)
        # THEN
        assert x_familyunit.famu_status == x_famu_status


def test_FamilyUnit_set_famu_status_RaisesException_Scenario1_SetNonFamuStatus():
    # ESTABLISH
    sue_familyunit = FamilyUnit(famu_name=exx.sue)
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_familyunit.set_famu_status(exx.sweep)
    excepted_exception_str = (
        f"FamilyUnit '{exx.sue}': '{exx.sweep}' is not acceptable famu_status."
    )
    assert str(excinfo.value) == excepted_exception_str


def test_FamilyUnit_set_famu_status_SetsAttr_Scenario1_Losing():
    # ESTABLISH
    x_familyunit = FamilyUnit()
    assert x_familyunit.famu_status is None
    # WHEN
    x_familyunit.set_famu_status(kw.losing)
    # THEN
    assert x_familyunit.famu_status == kw.losing


def test_familyunit_shop_ReturnsObj_Scenario0_MinimumParameters():
    # ESTABLISH
    kennedy_str = "Kennedy"

    # WHEN
    familyunit = familyunit_shop(kennedy_str)

    # THEN
    assert familyunit
    assert familyunit.famu_name == kennedy_str
    assert familyunit.prestige is False
    assert familyunit.famu_status is None


def test_familyunit_shop_ReturnsObj_Scenario1_MaxParameters():
    # ESTABLISH
    kennedy_str = "Kennedy"

    # WHEN
    familyunit = familyunit_shop(famu_name=kennedy_str, famu_status=kw.winning)

    # THEN
    assert familyunit
    assert familyunit.famu_name == kennedy_str
    assert familyunit.prestige is False
    assert familyunit.famu_status == kw.winning


def test_PillarUnit_Exists():
    # ESTABLISH / WHEN
    pillarunit = PillarUnit()

    # THEN
    assert pillarunit
    assert not pillarunit.pillar_name
    assert not pillarunit.bearers
    assert set(pillarunit.__dict__.keys()) == {"pillar_name", "bearers"}


def test_pillarunit_shop_ReturnsObj():
    # ESTABLISH
    sigma_phi_str = "sigma phi"
    # WHEN
    pillarunit = pillarunit_shop(sigma_phi_str)

    # THEN
    assert pillarunit
    assert pillarunit.pillar_name == sigma_phi_str
    assert pillarunit.bearers == {}


def test_WheelUnit_Exists():
    # ESTABLISH / WHEN
    x_wheelunit = WheelUnit()
    # THEN
    assert not x_wheelunit.wheel_name
    assert not x_wheelunit.familyunits
    assert not x_wheelunit.stable_size
    assert not x_wheelunit.moving_size
    assert set(x_wheelunit.__dict__.keys()) == {
        "wheel_name",
        "familyunits",
        "stable_size",
        "moving_size",
    }


def test_wheelunit_shop_ReturnsObj():
    # ESTABLISH
    paris_str = "Paris"
    # WHEN
    paris_wheelunit = wheelunit_shop(paris_str)
    # THEN
    assert paris_wheelunit.wheel_name == paris_str
    assert paris_wheelunit.familyunits == {}


def test_WheelUnit_familyunit_exists_ReturnsObj():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    kennedy_str = "Kennedy"
    assert not paris_wheelunit.familyunit_exists(kennedy_str)
    # WHEN
    paris_wheelunit.familyunits[kennedy_str] = familyunit_shop(kennedy_str)
    # THEN
    assert paris_wheelunit.familyunit_exists(kennedy_str)


def test_WheelUnit_set_familyunit_SetsAttr_Scenario0():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    kennedy_str = "Kennedy"
    kennedy_familyunit = familyunit_shop(kennedy_str)
    kennedy_familyunit.set_famu_status(kw.losing)
    assert not paris_wheelunit.familyunit_exists(kennedy_str)
    # WHEN
    paris_wheelunit.set_familyunit(kennedy_familyunit)
    # THEN
    assert paris_wheelunit.familyunit_exists(kennedy_str)


def test_WheelUnit_set_familyunit_RaisesException_Scenario1():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    kennedy_str = "Kennedy"
    kennedy_familyunit = familyunit_shop(kennedy_str)
    kennedy_familyunit.famu_status = "kinda cool"
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        paris_wheelunit.set_familyunit(kennedy_familyunit)
    excepted_exception_str = (
        f"FamilyUnit '{kennedy_str}': 'kinda cool' is not acceptable famu_status."
    )
    assert str(excinfo.value) == excepted_exception_str


def test_WheelUnit_del_familyunit_SetsAttr():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    kennedy_str = "Kennedy"
    kennedy_familyunit = familyunit_shop(kennedy_str)
    kennedy_familyunit.set_famu_status(kw.stable)
    paris_wheelunit.set_familyunit(kennedy_familyunit)
    assert paris_wheelunit.familyunit_exists(kennedy_str)
    # WHEN
    paris_wheelunit.del_familyunit(kennedy_str)
    # THEN
    assert not paris_wheelunit.familyunit_exists(kennedy_str)


def test_WheelUnit_get_familyunit_ReturnsObj():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    kennedy_str = "Kennedy"
    before_kennedy_familyunit = familyunit_shop(kennedy_str)
    before_kennedy_familyunit.set_famu_status(kw.stable)
    paris_wheelunit.set_familyunit(before_kennedy_familyunit)
    assert paris_wheelunit.familyunit_exists(kennedy_str)
    # WHEN
    after_kennedy_familyunit = paris_wheelunit.get_familyunit(kennedy_str)
    # THEN
    assert after_kennedy_familyunit == before_kennedy_familyunit


def test_WheelUnit_get_stable_familyunits_ReturnsObj_Scenario0():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    duran_str = "Duran"
    echoa_str = "Echoa"
    duran_familyunit = familyunit_shop(duran_str)
    echoa_familyunit = familyunit_shop(echoa_str)
    duran_familyunit.set_famu_status(kw.winning)
    echoa_familyunit.set_famu_status(kw.stable)
    paris_wheelunit.set_familyunit(duran_familyunit)
    paris_wheelunit.set_familyunit(echoa_familyunit)
    # WHEN
    stable_familyunits = paris_wheelunit.get_stable_familyunits()
    # THEN
    assert stable_familyunits
    assert stable_familyunits == [echoa_familyunit]


def test_WheelUnit_get_losing_familyunits_ReturnsObj_Scenario0():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    duran_str = "Duran"
    echoa_str = "Echoa"
    falco_str = "Falco"
    duran_familyunit = familyunit_shop(duran_str)
    echoa_familyunit = familyunit_shop(echoa_str)
    falco_familyunit = familyunit_shop(falco_str)
    duran_familyunit.set_famu_status(kw.winning)
    echoa_familyunit.set_famu_status(kw.stable)
    falco_familyunit.set_famu_status(kw.losing)
    paris_wheelunit.set_familyunit(duran_familyunit)
    paris_wheelunit.set_familyunit(echoa_familyunit)
    paris_wheelunit.set_familyunit(falco_familyunit)
    # WHEN
    losing_familyunits = paris_wheelunit.get_losing_familyunits()
    # THEN
    assert losing_familyunits
    assert losing_familyunits == [falco_familyunit]


def test_WheelUnit_get_no_prestige_familyunits_ReturnsObj_Scenario0():
    # ESTABLISH
    paris_wheelunit = wheelunit_shop("Paris")
    duran_str = "Duran"
    echoa_str = "Echoa"
    duran_familyunit = familyunit_shop(duran_str)
    echoa_familyunit = familyunit_shop(echoa_str)
    duran_familyunit.set_famu_status(kw.winning)
    paris_wheelunit.set_familyunit(duran_familyunit)
    paris_wheelunit.set_familyunit(echoa_familyunit)
    assert paris_wheelunit.get_familyunit(echoa_str).famu_status is None
    # WHEN
    no_prestige_familyunits = paris_wheelunit.get_no_prestige_familyunits()
    # THEN
    assert no_prestige_familyunits
    assert no_prestige_familyunits == [echoa_familyunit]


def test_LandUnit_Exists():
    # ESTABLISH / WHEN
    x_landunit = LandUnit()
    # THEN
    assert not x_landunit.land_name
    assert not x_landunit.pillars


def test_landunit_shop_ReturnsObj():
    # ESTABLISH
    france_str = "France"
    # WHEN
    france_landunit = landunit_shop(france_str)
    # THEN
    assert france_landunit.land_name == france_str
    assert france_landunit.pillars == set()
