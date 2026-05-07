from ch00_py.dict_toolbox import get_0_if_None
from ch09_person_lesson.lesson_main import LessonUnit
from ch19_idea_src.idea2brick import IdeaBook
from ch32_world.world import WorldName
from ch33_pitch._ref.ch33_semantic_types import PersonName, SparkInt
from dataclasses import dataclass


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
        if self.gift_spark_num is None and (
            self.request_spark_num is not None or self.offer_spark_num is not None
        ):
            return False
        elif self.request_spark_num == 0 or self.offer_spark_num == 0:
            return False

        gift_spark_num = get_0_if_None(self.gift_spark_num)
        request_spark_num = get_0_if_None(self.request_spark_num)
        offer_spark_num = get_0_if_None(self.offer_spark_num)
        return (
            gift_spark_num < request_spark_num
            and gift_spark_num < offer_spark_num
            and request_spark_num < offer_spark_num
        )


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
# Deal deal needs to be added here so the word isn't used anywhere else.
