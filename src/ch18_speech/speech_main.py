from ch00_py.dict_toolbox import get_0_if_None
from ch18_speech._ref.ch18_semantic_types import (
    KnotTerm,
    PersonName,
    FlareInt,
    default_knot_if_None,
)

from ch18_speech.yap_term import (
    LabelYap,
    YapCore,
    NameYap,
    RopeYap,
    TitleYap,
    get_labelyap_from_dict,
    get_nameyap_from_dict,
    get_ropeyap_from_dict,
    get_titleyap_from_dict,
    inherit_labelyap,
    inherit_nameyap,
    inherit_ropeyap,
    inherit_titleyap,
    labelyap_shop,
    nameyap_shop,
    ropeyap_shop,
    titleyap_shop,
)
from dataclasses import dataclass


class CheckSpeechAttrError(Exception):
    pass


@dataclass
class SpeechUnit:
    """Per face object that translates any translatable str.
    iux is the reference for the outside, what the face says
    aux is the reference for the inside, what the same inteprets from the face
    Contains a yapunit for each translatable type: RopeTerm, NameTerm, TitleTerm...
    """

    flare_num: FlareInt = None
    flare_audie: PersonName = None
    titleyap: TitleYap = None
    nameyap: NameYap = None
    labelyap: LabelYap = None
    ropeyap: RopeYap = None
    iux_knot: KnotTerm = None  # speechunit
    aux_knot: KnotTerm = None  # speechunit

    def _check_speech_attr_match(self, attr: str, yapcore):
        self_attr = getattr(self, attr)
        unit_attr = getattr(yapcore, attr)
        if self_attr != unit_attr:
            exception_str = f"set_yapcore Error: SpeechUnit {attr} is '{self_attr}', YapCore is '{unit_attr}'."
            raise CheckSpeechAttrError(exception_str)

    def _check_speech_core_attrs_match(self, x_yapcore: YapCore):
        self._check_speech_attr_match("flare_audie", x_yapcore)
        self._check_speech_attr_match("iux_knot", x_yapcore)
        self._check_speech_attr_match("aux_knot", x_yapcore)

    def set_nameyap(self, x_nameyap: NameYap):
        self._check_speech_core_attrs_match(x_nameyap)
        self.nameyap = x_nameyap

    def get_nameyap(self) -> NameYap:
        return self.nameyap

    def set_speech_nameterm(self, iux_name: str, aux_name: str):
        self.nameyap.set_iux2aux(iux_name, aux_name)

    def nameterm_speech_exists(self, iux_name: str, aux_name: str):
        return self.nameyap.iux2aux_exists(iux_name, aux_name)

    def _get_aux_name(self, iux_name: str):
        return self.nameyap.get_aux_value(iux_name)

    def del_speech_nameterm(self, iux_name: str):
        return self.nameyap.del_iux2aux(iux_name)

    def set_titleyap(self, x_titleyap: TitleYap):
        self._check_speech_core_attrs_match(x_titleyap)
        self.titleyap = x_titleyap

    def get_titleyap(self) -> TitleYap:
        return self.titleyap

    def set_speech_titleterm(self, iux_title: str, aux_title: str):
        self.titleyap.set_iux2aux(iux_title, aux_title)

    def titleterm_speech_exists(self, iux_title: str, aux_title: str):
        return self.titleyap.iux2aux_exists(iux_title, aux_title)

    def _get_aux_title(self, iux_title: str):
        return self.titleyap.get_aux_value(iux_title)

    def del_speech_titleterm(self, iux_title: str):
        return self.titleyap.del_iux2aux(iux_title)

    def set_labelyap(self, x_labelyap: LabelYap):
        self._check_speech_core_attrs_match(x_labelyap)
        self.labelyap = x_labelyap

    def get_labelyap(self) -> LabelYap:
        return self.labelyap

    def set_ropeyap(self, x_ropeyap: RopeYap):
        self._check_speech_core_attrs_match(x_ropeyap)
        self.ropeyap = x_ropeyap

    def set_roadyap_label(self, x_iux: str, x_aux: str):
        self.ropeyap.set_label(x_iux, x_aux)

    def roadyap_label_exists(self, x_iux: str, x_aux: str) -> bool:
        return self.ropeyap.label_exists(x_iux, x_aux)

    def del_roadyap_label(self, x_iux: str):
        self.ropeyap.del_label(x_iux)

    def get_ropeyap(self) -> RopeYap:
        return self.ropeyap

    def set_speech_rope(self, iux_rope: str, aux_rope: str):
        self.ropeyap.set_iux2aux(iux_rope, aux_rope)

    def rope_speech_exists(self, iux_rope: str, aux_rope: str):
        return self.ropeyap.iux2aux_exists(iux_rope, aux_rope)

    def _get_aux_rope(self, iux_rope: str):
        return self.ropeyap.get_aux_value(iux_rope)

    def del_speech_rope(self, iux_rope: str):
        return self.ropeyap.del_iux2aux(iux_rope)

    def get_yapunit(self, x_obj_type: str):
        if x_obj_type == "NameTerm":
            return self.nameyap
        elif x_obj_type == "TitleTerm":
            return self.titleyap
        elif x_obj_type == "LabelTerm":
            return self.labelyap
        elif x_obj_type == "RopeTerm":
            return self.ropeyap
        else:
            return None

    def is_valid(self) -> bool:
        return (
            self.nameyap.is_valid()
            and self.titleyap.is_valid()
            and self.labelyap.is_valid()
            and self.ropeyap.is_valid()
        )

    def set_iux2aux(self, x_obj_type: str, x_iux: str, x_aux: str):
        """obj_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_obj_type == "NameTerm":
            self.nameyap.set_iux2aux(x_iux, x_aux)
        elif x_obj_type == "TitleTerm":
            self.titleyap.set_iux2aux(x_iux, x_aux)
        elif x_obj_type == "LabelTerm":
            self.labelyap.set_iux2aux(x_iux, x_aux)
        elif x_obj_type == "RopeTerm":
            self.ropeyap.set_iux2aux(x_iux, x_aux)

    def iux2aux_exists(self, x_obj_type: str, x_iux: str, x_aux: str) -> bool:
        """obj_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_obj_type == "NameTerm":
            return self.nameyap.iux2aux_exists(x_iux, x_aux)
        elif x_obj_type == "TitleTerm":
            return self.titleyap.iux2aux_exists(x_iux, x_aux)
        elif x_obj_type == "LabelTerm":
            return self.labelyap.iux2aux_exists(x_iux, x_aux)
        elif x_obj_type == "RopeTerm":
            return self.ropeyap.iux2aux_exists(x_iux, x_aux)

    def get_aux_value(self, x_obj_type: str, x_iux: str) -> str:
        """obj_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_obj_type == "NameTerm":
            return self.nameyap.get_aux_value(x_iux)
        elif x_obj_type == "TitleTerm":
            return self.titleyap.get_aux_value(x_iux)
        elif x_obj_type == "LabelTerm":
            return self.labelyap.get_aux_value(x_iux)
        elif x_obj_type == "RopeTerm":
            return self.ropeyap.get_aux_value(x_iux)

    def del_iux2aux(self, x_obj_type: str, x_iux: str):
        """obj_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_obj_type == "NameTerm":
            self.nameyap.del_iux2aux(x_iux)
        elif x_obj_type == "TitleTerm":
            self.titleyap.del_iux2aux(x_iux)
        elif x_obj_type == "LabelTerm":
            self.labelyap.del_iux2aux(x_iux)
        elif x_obj_type == "RopeTerm":
            self.ropeyap.del_iux2aux(x_iux)

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        x_nameyap = _get_rid_of_speech_core_keys(self.nameyap.to_dict())
        x_titleyap = _get_rid_of_speech_core_keys(self.titleyap.to_dict())
        x_labelyap = _get_rid_of_speech_core_keys(self.labelyap.to_dict())
        x_ropeyap = _get_rid_of_speech_core_keys(self.ropeyap.to_dict())

        return {
            "flare_audie": self.flare_audie,
            "flare_num": self.flare_num,
            "iux_knot": self.iux_knot,
            "aux_knot": self.aux_knot,
            "nameyap": x_nameyap,
            "labelyap": x_labelyap,
            "titleyap": x_titleyap,
            "ropeyap": x_ropeyap,
        }


def speechunit_shop(
    flare_audie: PersonName,
    flare_num: FlareInt = None,
    iux_knot: KnotTerm = None,
    aux_knot: KnotTerm = None,
) -> SpeechUnit:
    iux_knot = default_knot_if_None(iux_knot)
    aux_knot = default_knot_if_None(aux_knot)

    x_nameyap = nameyap_shop(
        flare_audie=flare_audie,
        flare_num=flare_num,
        iux_knot=iux_knot,
        aux_knot=aux_knot,
    )
    x_titleyap = titleyap_shop(
        flare_audie=flare_audie,
        flare_num=flare_num,
        iux_knot=iux_knot,
        aux_knot=aux_knot,
    )
    x_labelyap = labelyap_shop(
        flare_audie=flare_audie,
        flare_num=flare_num,
        iux_knot=iux_knot,
        aux_knot=aux_knot,
    )
    x_ropeyap = ropeyap_shop(
        flare_audie=flare_audie,
        flare_num=flare_num,
        iux_knot=iux_knot,
        aux_knot=aux_knot,
        x_labelyap=x_labelyap,
    )

    return SpeechUnit(
        flare_audie=flare_audie,
        flare_num=get_0_if_None(flare_num),
        iux_knot=iux_knot,
        aux_knot=aux_knot,
        nameyap=x_nameyap,
        titleyap=x_titleyap,
        labelyap=x_labelyap,
        ropeyap=x_ropeyap,
    )


def _get_rid_of_speech_core_keys(yap_dict: dict) -> dict:
    yap_dict.pop("flare_num")
    yap_dict.pop("flare_audie")
    yap_dict.pop("iux_knot")
    yap_dict.pop("aux_knot")
    return yap_dict


def _add_speech_core_keys(
    yap_dict: dict,
    flare_num: int,
    flare_audie: str,
    iux_knot: KnotTerm,
    aux_knot: KnotTerm,
) -> dict:
    yap_dict["flare_num"] = flare_num
    yap_dict["flare_audie"] = flare_audie
    yap_dict["iux_knot"] = iux_knot
    yap_dict["aux_knot"] = aux_knot
    return yap_dict


def get_speechunit_from_dict(x_dict: dict) -> SpeechUnit:
    x_flare_num = x_dict.get("flare_num")
    x_flare_audie = x_dict.get("flare_audie")
    x_iux_knot = x_dict.get("iux_knot")
    x_aux_knot = x_dict.get("aux_knot")
    nameyap_dict = x_dict.get("nameyap")
    titleyap_dict = x_dict.get("titleyap")
    labelyap_dict = x_dict.get("labelyap")
    ropeyap_dict = x_dict.get("ropeyap")
    nameyap_dict = _add_speech_core_keys(
        nameyap_dict,
        x_flare_num,
        x_flare_audie,
        x_iux_knot,
        x_aux_knot,
    )
    titleyap_dict = _add_speech_core_keys(
        titleyap_dict,
        x_flare_num,
        x_flare_audie,
        x_iux_knot,
        x_aux_knot,
    )
    labelyap_dict = _add_speech_core_keys(
        labelyap_dict,
        x_flare_num,
        x_flare_audie,
        x_iux_knot,
        x_aux_knot,
    )
    ropeyap_dict = _add_speech_core_keys(
        ropeyap_dict,
        x_flare_num,
        x_flare_audie,
        x_iux_knot,
        x_aux_knot,
    )
    x_nameyap = get_nameyap_from_dict(nameyap_dict)
    x_titleyap = get_titleyap_from_dict(titleyap_dict)
    x_labelyap = get_labelyap_from_dict(labelyap_dict)
    x_ropeyap = get_ropeyap_from_dict(ropeyap_dict)
    x_ropeyap.labelyap = x_labelyap
    return SpeechUnit(
        flare_audie=x_flare_audie,
        flare_num=x_flare_num,
        iux_knot=x_iux_knot,
        aux_knot=x_aux_knot,
        nameyap=x_nameyap,
        titleyap=x_titleyap,
        labelyap=x_labelyap,
        ropeyap=x_ropeyap,
    )


class SpeechCoreAttrConflictError(Exception):
    pass


# find out why no tests trip without "Core attrs in conflict"
def inherit_speechunit(older: SpeechUnit, newer: SpeechUnit) -> SpeechUnit:
    # if (
    #     older.flare_audie != newer.flare_audie
    #     or older.iux_knot != newer.iux_knot
    #     or older.aux_knot != newer.aux_knot
    # ):
    #     raise SpeechCoreAttrConflictError("Core attrs in conflict")
    if older.flare_num >= newer.flare_num:
        raise SpeechCoreAttrConflictError("older speechunit is not older")
    newer.set_nameyap(inherit_nameyap(newer.nameyap, older.nameyap))
    newer.set_titleyap(inherit_titleyap(newer.titleyap, older.titleyap))
    newer.set_labelyap(inherit_labelyap(newer.labelyap, older.labelyap))
    newer.set_ropeyap(inherit_ropeyap(newer.ropeyap, older.ropeyap))

    return newer
