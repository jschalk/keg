from ch33_pitch.pitch import PitchUnit, pitchunit_shop
from ref.keywords import Ch33Keywords as kw, ExampleStrs as exx


def test_PitchUnit_Exists():
    # ESTABLISH / WHEN
    x_pitchunit = PitchUnit()

    # THEN
    assert not x_pitchunit.pitcher_name
    assert not x_pitchunit.peer_name
    assert not x_pitchunit.gift_ideabook
    assert not x_pitchunit.request_ideabook
    assert not x_pitchunit.offer_ideabook
    assert not x_pitchunit.pitch_id
    assert not x_pitchunit.pitch_active
    assert set(x_pitchunit.__dict__.keys()) == {
        kw.pitcher_name,
        "pitch_active",
        kw.pitch_id,
        "peer_name",
        "gift_ideabook",
        "gift_spark_num",
        "request_ideabook",
        "request_spark_num",
        "offer_ideabook",
        "offer_spark_num",
    }


def test_pitchunit_shop_ReturnsObj():
    # ESTABLISH / WHEN
    sue_pitchunit = pitchunit_shop(exx.sue)

    # THEN
    assert sue_pitchunit.pitcher_name == exx.sue
    assert not sue_pitchunit.peer_name
    assert not sue_pitchunit.gift_ideabook
    assert not sue_pitchunit.request_ideabook
    assert not sue_pitchunit.offer_ideabook
    assert not sue_pitchunit.pitch_id


def test_PitchUnit_validate_spark_nums_ReturnsObj_Scenario0_Basic():
    # ESTABLISH
    sue_pitchunit = pitchunit_shop(exx.sue)
    sue_pitchunit.gift_spark_num = 11
    sue_pitchunit.request_spark_num = 22
    sue_pitchunit.offer_spark_num = 33
    # WHEN
    validate_spark_nums_bool = sue_pitchunit.validate_spark_nums()
    # THEN
    assert validate_spark_nums_bool is True


def test_PitchUnit_validate_spark_nums_ReturnsObj_Scenario1_False():
    # ESTABLISH
    sue_pitchunit = pitchunit_shop(exx.sue)
    sue_pitchunit.gift_spark_num = 30
    sue_pitchunit.request_spark_num = 22
    sue_pitchunit.offer_spark_num = 33
    # WHEN
    validate_spark_nums_bool = sue_pitchunit.validate_spark_nums()
    # THEN
    assert validate_spark_nums_bool is False


def test_PitchUnit_validate_spark_nums_ReturnsObj_Scenario2_False():
    # ESTABLISH
    sue_pitchunit = pitchunit_shop(exx.sue)
    sue_pitchunit.gift_spark_num = 11
    sue_pitchunit.request_spark_num = 35
    sue_pitchunit.offer_spark_num = 33
    # WHEN
    validate_spark_nums_bool = sue_pitchunit.validate_spark_nums()
    # THEN
    assert validate_spark_nums_bool is False


# The pitch process model is as follows from Pitcher to Peer
# 1. offer gift. Gifts are Ideas at the pitcher is vowing to make into a brick. Are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.
