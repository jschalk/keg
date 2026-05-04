from ch09_person_lesson.lesson_main import LessonUnit
from ch19_idea_src.idea2brick import IdeaBook
from ch26_world.world import WorldName
from ch27_pitch._ref.ch27_semantic_types import PersonName
from dataclasses import dataclass


# TODO add "Deal" to keywords
@dataclass
class PitchUnit:
    pitcher_name: PersonName = None
    peer: PersonName = None
    gift: IdeaBook = None
    request: IdeaBook = None
    offer: IdeaBook = None
    pitch_id: str = None


def pitchunit_shop(
    pitcher_name: PersonName,
    peer: PersonName = None,
    gift: IdeaBook = None,
    request: IdeaBook = None,
    offer: IdeaBook = None,
    pitch_id: str = None,
) -> PitchUnit:
    return PitchUnit(pitcher_name=pitcher_name)


# The pitch process model is as follows from Pitcher to Peer
# 1. offer gift. Gifts are Ideas at the pitcher is vowing to make into a brick. Are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.
