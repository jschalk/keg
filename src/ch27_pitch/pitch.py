from ch09_person_lesson.lesson_main import LessonUnit
from ch19_idea_src.idea2brick import IdeaBook
from ch26_world.world import WorldName
from ch27_pitch._ref.ch27_semantic_types import PersonName, SparkInt
from dataclasses import dataclass


# TODO add "Deal" to keywords
@dataclass
class PitchUnit:
    pitcher_name: PersonName = None
    pitch_id: str = None
    pitch_active: bool = None
    peer_name: PersonName = None
    gift_ideabook: IdeaBook = None
    gift_spark_num: SparkInt = None
    request_ideabook: IdeaBook = None
    request_spark_num: SparkInt = None
    offer_ideabook: IdeaBook = None
    offer_spark_num: SparkInt = None

    def validate_spark_nums(self):
        if self.gift_spark_num and self.request_spark_num and self.offer_spark_num:
            if self.gift_spark_num >= self.request_spark_num:
                return False
            elif self.request_spark_num >= self.offer_spark_num:
                return False
        return True


def pitchunit_shop(
    pitcher_name: PersonName,
    peer_name: PersonName = None,
    gift_ideas: IdeaBook = None,
    request_ideas: IdeaBook = None,
    offer_ideas: IdeaBook = None,
    pitch_id: str = None,
    pitch_active: bool = None,
) -> PitchUnit:
    return PitchUnit(pitcher_name=pitcher_name)


# The pitch process model is as follows from Pitcher to Peer
# 1. offer gift. Gifts are Ideas at the pitcher is vowing to make into a brick. Are meant to appeal to the audience
# 2. Describe possible future Gifts. From you, from me.

# When a pitch is given the gift must automatically be bricked. The gift's spark_num
# could be added to the PitchUnit. Then if the pitch is accepted
