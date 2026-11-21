from ch00_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    set_modular_dict_values,
)
from ch16_tash._ref.ch16_semantic_types import FaceName, SparkInt, TimeNum
from dataclasses import dataclass


@dataclass
class TashTime:
    spark_face: FaceName = None
    spark_num: SparkInt = None
    # otx2inx dict key 'otx_epoch_length', key can be None is only inx_epoch_diff is given
    # otx2inx dict value 'inx_epoch_diff'
    otx2inx: dict[TimeNum, TimeNum] = None

    def set_all_otx2inx(self, otx2inx: dict[TimeNum, TimeNum]):
        self.otx2inx = set_modular_dict_values(get_empty_dict_if_None(otx2inx))

    def set_otx2inx(self, epoch_length: TimeNum, inx_epoch_diff: TimeNum):
        self.otx2inx[epoch_length] = inx_epoch_diff
        self.otx2inx = set_modular_dict_values(get_empty_dict_if_None(self.otx2inx))

    def get_inx_value(self, otx_epoch_length: TimeNum) -> TimeNum:
        return self.otx2inx.get(otx_epoch_length)

    def otx2inx_exists(self, epoch_length: TimeNum, inx_epoch_diff: TimeNum) -> bool:
        return self.otx2inx.get(epoch_length) == inx_epoch_diff

    def otx_exists(self, epoch_length: TimeNum) -> bool:
        return self.otx2inx.get(epoch_length) != None

    def del_otx2inx(self, epoch_length: TimeNum):
        self.otx2inx.pop(epoch_length)

    def reveal_inx(self, otx_epoch_length: TimeNum, otx_value: TimeNum) -> TimeNum:
        if inx_epoch_diff := self.get_inx_value(otx_epoch_length):
            otx_value += inx_epoch_diff
        otx_value = otx_value % otx_epoch_length
        return otx_value

    def to_dict(self) -> dict:
        """Returns seralizable dictionary"""
        return {
            "spark_face": self.spark_face,
            "spark_num": self.spark_num,
            "otx2inx": self.otx2inx,
        }


def timetash_shop(
    spark_face: FaceName,
    spark_num: SparkInt = None,
    otx2inx: dict[TimeNum, TimeNum] = None,
):
    x_timetash = TashTime(spark_face=spark_face, spark_num=get_0_if_None(spark_num))
    x_timetash.set_all_otx2inx(otx2inx)
    return x_timetash


def get_timetash_from_dict(x_dict: dict) -> TashTime:
    return timetash_shop(
        spark_face=x_dict.get("spark_face"),
        spark_num=x_dict.get("spark_num"),
        otx2inx=x_dict.get("otx2inx"),
    )


class InheritTimeTashError(Exception):
    pass


def inherit_timetash(new: TashTime, old: TashTime):
    if new.spark_face != old.spark_face:
        exception_str = "Core attrs in conflict"
        raise InheritTimeTashError(exception_str)
    if new.spark_num <= old.spark_num:
        exception_str = "older TashTime is not older"
        raise InheritTimeTashError(exception_str)
    for otx_epoch_length, inx_epoch_diff in old.otx2inx.items():
        if not new.otx_exists(otx_epoch_length):
            new.set_otx2inx(otx_epoch_length, inx_epoch_diff)
