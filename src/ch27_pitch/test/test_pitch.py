from ch27_pitch.pitch import PitchUnit, pitchunit_shop


def test_PitchUnit_Exists():
    # ESTABLISH / WHEN
    x_pitchunit = PitchUnit()

    # THEN
    assert not x_pitchunit.pitch_id
    assert not x_pitchunit.option_lessons
    assert not x_pitchunit.selected_lesson
    assert not x_pitchunit.worlds


def test_pitchunit_shop_ReturnsObj():
    # ESTABLISH
    d456_str = "d456"

    # WHEN
    d456_pitchunit = pitchunit_shop(d456_str)

    # THEN
    assert d456_pitchunit.pitch_id
    assert not d456_pitchunit.option_lessons
    assert not d456_pitchunit.selected_lesson
    assert not d456_pitchunit.worlds


# def test_PitchUnit_CreateOptionLessons():
# The pitch process model is as follows
# 1. offer gift. Gifts are Ideas at the pitcher is vowing to make into a brick. Are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.
