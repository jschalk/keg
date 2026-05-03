from ch09_person_lesson.lesson_main import LessonUnit
from ch26_world.world import WorldName
from dataclasses import dataclass


# TODO replace "lobby" with "pitch"
# TODO add "Deal" to keywords
@dataclass
class LobbyUnit:
    lobby_id: str = None
    option_lessons: list[LessonUnit] = None
    selected_lesson: LessonUnit = None
    worlds: list[WorldName] = None


def lobbyunit_shop(
    lobby_id: str,
    option_lessons: list[LessonUnit] = None,
    selected_lesson: LessonUnit = None,
    worlds: list[WorldName] = None,
) -> LobbyUnit:
    return LobbyUnit(lobby_id=lobby_id)


# The lobby process model is as follows
# 1. offer gift. Gifts are Ideas that are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.
