from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_0_if_None
from src.ch16_translate._ref.ch16_semantic_types import (
    KnotTerm,
    PersonName,
    SparkInt,
    default_knot_if_None,
)
from src.ch16_translate.map_term import (
    LabelMap,
    MapCore,
    NameMap,
    RopeMap,
    TitleMap,
    get_labelmap_from_dict,
    get_namemap_from_dict,
    get_ropemap_from_dict,
    get_titlemap_from_dict,
    inherit_labelmap,
    inherit_namemap,
    inherit_ropemap,
    inherit_titlemap,
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.ch16_translate.translate_config import default_unknown_str_if_None


class CheckAttrError(Exception):
    pass


@dataclass
class TranslateUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a mapunit for each translatable type: RopeTerm, NameTerm, TitleTerm...
    """

    spark_num: SparkInt = None
    spark_face: PersonName = None
    titlemap: TitleMap = None
    namemap: NameMap = None
    labelmap: LabelMap = None
    ropemap: RopeMap = None
    unknown_str: str = None  # translateunit
    otx_knot: KnotTerm = None  # translateunit
    inx_knot: KnotTerm = None  # translateunit

    def set_titlemap(self, x_titlemap: TitleMap):
        self._check_all_core_attrs_match(x_titlemap)
        self.titlemap = x_titlemap

    def get_titlemap(self) -> TitleMap:
        return self.titlemap

    def set_titleterm(self, otx_title: str, inx_title: str):
        self.titlemap.set_otx2inx(otx_title, inx_title)

    def titleterm_exists(self, otx_title: str, inx_title: str):
        return self.titlemap.otx2inx_exists(otx_title, inx_title)

    def _get_inx_title(self, otx_title: str):
        return self.titlemap.get_inx_value(otx_title)

    def del_titleterm(self, otx_title: str):
        return self.titlemap.del_otx2inx(otx_title)

    def get_mapunit(self, x_class_type: str):
        if x_class_type == "NameTerm":
            return self.namemap
        elif x_class_type == "TitleTerm":
            return self.titlemap
        elif x_class_type == "LabelTerm":
            return self.labelmap
        elif x_class_type == "RopeTerm":
            return self.ropemap
        else:
            return None

    def set_namemap(self, x_namemap: NameMap):
        self._check_all_core_attrs_match(x_namemap)
        self.namemap = x_namemap

    def get_namemap(self) -> NameMap:
        return self.namemap

    def set_nameterm(self, otx_name: str, inx_name: str):
        self.namemap.set_otx2inx(otx_name, inx_name)

    def nameterm_exists(self, otx_name: str, inx_name: str):
        return self.namemap.otx2inx_exists(otx_name, inx_name)

    def _get_inx_name(self, otx_name: str):
        return self.namemap.get_inx_value(otx_name)

    def del_nameterm(self, otx_name: str):
        return self.namemap.del_otx2inx(otx_name)

    def set_labelmap(self, x_labelmap: LabelMap):
        self._check_all_core_attrs_match(x_labelmap)
        self.labelmap = x_labelmap

    def get_labelmap(self) -> LabelMap:
        return self.labelmap

    def set_ropemap(self, x_ropemap: RopeMap):
        self._check_all_core_attrs_match(x_ropemap)
        self.ropemap = x_ropemap

    def get_ropemap(self) -> RopeMap:
        return self.ropemap

    def set_rope(self, otx_rope: str, inx_rope: str):
        self.ropemap.set_otx2inx(otx_rope, inx_rope)

    def rope_exists(self, otx_rope: str, inx_rope: str):
        return self.ropemap.otx2inx_exists(otx_rope, inx_rope)

    def _get_inx_rope(self, otx_rope: str):
        return self.ropemap.get_inx_value(otx_rope)

    def del_rope(self, otx_rope: str):
        return self.ropemap.del_otx2inx(otx_rope)

    def _check_all_core_attrs_match(self, x_mapcore: MapCore):
        self._check_attr_match("spark_face", x_mapcore)
        self._check_attr_match("otx_knot", x_mapcore)
        self._check_attr_match("inx_knot", x_mapcore)
        self._check_attr_match("unknown_str", x_mapcore)

    def _check_attr_match(self, attr: str, mapcore):
        self_attr = getattr(self, attr)
        unit_attr = getattr(mapcore, attr)
        if self_attr != unit_attr:
            exception_str = f"set_mapcore Error: TranslateUnit {attr} is '{self_attr}', MapCore is '{unit_attr}'."
            raise CheckAttrError(exception_str)

    def is_valid(self) -> bool:
        return (
            self.namemap.is_valid()
            and self.titlemap.is_valid()
            and self.labelmap.is_valid()
            and self.ropemap.is_valid()
        )

    def set_otx2inx(self, x_class_type: str, x_otx: str, x_inx: str):
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            self.namemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "TitleTerm":
            self.titlemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "LabelTerm":
            self.labelmap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "RopeTerm":
            self.ropemap.set_otx2inx(x_otx, x_inx)

    def get_inx_value(self, x_class_type: str, x_otx: str) -> str:
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            return self.namemap.get_inx_value(x_otx)
        elif x_class_type == "TitleTerm":
            return self.titlemap.get_inx_value(x_otx)
        elif x_class_type == "LabelTerm":
            return self.labelmap.get_inx_value(x_otx)
        elif x_class_type == "RopeTerm":
            return self.ropemap.get_inx_value(x_otx)

    def otx2inx_exists(self, x_class_type: str, x_otx: str, x_inx: str) -> bool:
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            return self.namemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "TitleTerm":
            return self.titlemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "LabelTerm":
            return self.labelmap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "RopeTerm":
            return self.ropemap.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_class_type: str, x_otx: str):
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            self.namemap.del_otx2inx(x_otx)
        elif x_class_type == "TitleTerm":
            self.titlemap.del_otx2inx(x_otx)
        elif x_class_type == "LabelTerm":
            self.labelmap.del_otx2inx(x_otx)
        elif x_class_type == "RopeTerm":
            self.ropemap.del_otx2inx(x_otx)

    def set_roadmap_label(self, x_otx: str, x_inx: str):
        self.ropemap.set_label(x_otx, x_inx)

    def roadmap_label_exists(self, x_otx: str, x_inx: str) -> bool:
        return self.ropemap.label_exists(x_otx, x_inx)

    def del_roadmap_label(self, x_otx: str):
        self.ropemap.del_label(x_otx)

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        x_namemap = _get_rid_of_translate_core_keys(self.namemap.to_dict())
        x_titlemap = _get_rid_of_translate_core_keys(self.titlemap.to_dict())
        x_labelmap = _get_rid_of_translate_core_keys(self.labelmap.to_dict())
        x_ropemap = _get_rid_of_translate_core_keys(self.ropemap.to_dict())

        return {
            "spark_face": self.spark_face,
            "spark_num": self.spark_num,
            "otx_knot": self.otx_knot,
            "inx_knot": self.inx_knot,
            "unknown_str": self.unknown_str,
            "namemap": x_namemap,
            "labelmap": x_labelmap,
            "titlemap": x_titlemap,
            "ropemap": x_ropemap,
        }


def translateunit_shop(
    spark_face: PersonName,
    spark_num: SparkInt = None,
    otx_knot: KnotTerm = None,
    inx_knot: KnotTerm = None,
    unknown_str: str = None,
) -> TranslateUnit:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_knot = default_knot_if_None(otx_knot)
    inx_knot = default_knot_if_None(inx_knot)

    x_namemap = namemap_shop(
        spark_face=spark_face,
        spark_num=spark_num,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )
    x_titlemap = titlemap_shop(
        spark_face=spark_face,
        spark_num=spark_num,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )
    x_labelmap = labelmap_shop(
        spark_face=spark_face,
        spark_num=spark_num,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )
    x_ropemap = ropemap_shop(
        spark_face=spark_face,
        spark_num=spark_num,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
        x_labelmap=x_labelmap,
    )

    return TranslateUnit(
        spark_face=spark_face,
        spark_num=get_0_if_None(spark_num),
        unknown_str=unknown_str,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        namemap=x_namemap,
        titlemap=x_titlemap,
        labelmap=x_labelmap,
        ropemap=x_ropemap,
    )


def get_translateunit_from_dict(x_dict: dict) -> TranslateUnit:
    x_spark_num = x_dict.get("spark_num")
    x_spark_face = x_dict.get("spark_face")
    x_otx_knot = x_dict.get("otx_knot")
    x_inx_knot = x_dict.get("inx_knot")
    x_unknown_str = x_dict.get("unknown_str")
    namemap_dict = x_dict.get("namemap")
    titlemap_dict = x_dict.get("titlemap")
    labelmap_dict = x_dict.get("labelmap")
    ropemap_dict = x_dict.get("ropemap")
    namemap_dict = _add_translate_core_keys(
        namemap_dict,
        x_spark_num,
        x_spark_face,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    titlemap_dict = _add_translate_core_keys(
        titlemap_dict,
        x_spark_num,
        x_spark_face,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    labelmap_dict = _add_translate_core_keys(
        labelmap_dict,
        x_spark_num,
        x_spark_face,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    ropemap_dict = _add_translate_core_keys(
        ropemap_dict,
        x_spark_num,
        x_spark_face,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    x_namemap = get_namemap_from_dict(namemap_dict)
    x_titlemap = get_titlemap_from_dict(titlemap_dict)
    x_labelmap = get_labelmap_from_dict(labelmap_dict)
    x_ropemap = get_ropemap_from_dict(ropemap_dict)
    x_ropemap.labelmap = x_labelmap
    return TranslateUnit(
        spark_face=x_spark_face,
        spark_num=x_spark_num,
        otx_knot=x_otx_knot,
        inx_knot=x_inx_knot,
        unknown_str=x_unknown_str,
        namemap=x_namemap,
        titlemap=x_titlemap,
        labelmap=x_labelmap,
        ropemap=x_ropemap,
    )


def _get_rid_of_translate_core_keys(map_dict: dict) -> dict:
    map_dict.pop("spark_num")
    map_dict.pop("spark_face")
    map_dict.pop("otx_knot")
    map_dict.pop("inx_knot")
    map_dict.pop("unknown_str")
    return map_dict


def _add_translate_core_keys(
    map_dict: dict,
    spark_num: int,
    spark_face: str,
    otx_knot: KnotTerm,
    inx_knot: KnotTerm,
    unknown_str: str,
) -> dict:
    map_dict["spark_num"] = spark_num
    map_dict["spark_face"] = spark_face
    map_dict["otx_knot"] = otx_knot
    map_dict["inx_knot"] = inx_knot
    map_dict["unknown_str"] = unknown_str
    return map_dict


class TranslateCoreAttrConflictError(Exception):
    pass


def inherit_translateunit(older: TranslateUnit, newer: TranslateUnit) -> TranslateUnit:
    if (
        older.spark_face != newer.spark_face
        or older.otx_knot != newer.otx_knot
        or older.inx_knot != newer.inx_knot
        or older.unknown_str != newer.unknown_str
    ):
        raise TranslateCoreAttrConflictError("Core attrs in conflict")
    if older.spark_num >= newer.spark_num:
        raise TranslateCoreAttrConflictError("older translateunit is not older")
    newer.set_namemap(inherit_namemap(newer.namemap, older.namemap))
    newer.set_titlemap(inherit_titlemap(newer.titlemap, older.titlemap))
    newer.set_labelmap(inherit_labelmap(newer.labelmap, older.labelmap))
    newer.set_ropemap(inherit_ropemap(newer.ropemap, older.ropemap))

    return newer
