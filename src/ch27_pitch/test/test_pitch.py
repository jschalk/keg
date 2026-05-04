from ch27_pitch.pitch import PitchUnit, pitchunit_shop
from ref.keywords import Ch27Keywords as kw, ExampleStrs as exx


def test_PitchUnit_Exists():
    # ESTABLISH / WHEN
    x_pitchunit = PitchUnit()

    # THEN
    assert not x_pitchunit.pitcher_name
    assert not x_pitchunit.peer
    assert not x_pitchunit.gift
    assert not x_pitchunit.request
    assert not x_pitchunit.offer
    assert not x_pitchunit.pitch_id
    assert set(x_pitchunit.__dict__.keys()) == {
        kw.pitch_id,
        kw.pitcher_name,
        kw.peer,
        kw.gift,
        kw.request,
        kw.offer,
    }


def test_pitchunit_shop_ReturnsObj():
    # ESTABLISH / WHEN
    sue_pitchunit = pitchunit_shop(exx.sue)

    # THEN
    assert sue_pitchunit.pitcher_name == exx.sue
    assert not sue_pitchunit.peer
    assert not sue_pitchunit.gift
    assert not sue_pitchunit.request
    assert not sue_pitchunit.offer
    assert not sue_pitchunit.pitch_id


# The pitch process model is as follows from Pitcher to Peer
# 1. offer gift. Gifts are Ideas at the pitcher is vowing to make into a brick. Are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.
