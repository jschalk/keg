from ch09_person_lesson.lesson_main import LessonUnit
from ch26_world.world import WorldName
from dataclasses import dataclass


# TODO replace "pitch" with "pitch"
# TODO add "Deal" to keywords
@dataclass
class PitchUnit:
    pitch_id: str = None
    option_lessons: list[LessonUnit] = None
    selected_lesson: LessonUnit = None
    worlds: list[WorldName] = None


def pitchunit_shop(
    pitch_id: str,
    option_lessons: list[LessonUnit] = None,
    selected_lesson: LessonUnit = None,
    worlds: list[WorldName] = None,
) -> PitchUnit:
    return PitchUnit(pitch_id=pitch_id)


# The pitch process model is as follows
# 1. offer gift. Gifts are Ideas at the pitcher is vowing to make into a brick. Are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.
