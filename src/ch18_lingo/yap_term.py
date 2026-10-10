from ch00_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_str_in_sub_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
)
from ch05_rope.rope import (
    create_rope,
    create_rope_from_labels,
    get_all_rope_labels,
    get_parent_rope,
    get_tail_label,
)
from ch18_lingo._ref.ch18_semantic_types import (
    FaceName,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    SparkInt,
    default_knot_if_None,
)
from copy import copy as copy_copy
from dataclasses import dataclass


class SetAlliux2auxError(Exception):
    pass


class SetLabelError(Exception):
    pass


@dataclass
class YapCore:
    pass
    # spark_face: FaceName = None
    # spark_num: SparkInt = None
    # iux2aux: dict[str, str] = None
    # unknown_str: str = None
    # iux_knot: KnotTerm = None
    # aux_knot: KnotTerm = None

    # def unknown_str_in_iux2aux(self) -> bool:
    #     return str_in_dict(self.unknown_str, self.iux2aux)

    # def set_all_iux2aux(
    #     self, x_iux2aux: dict, raise_exception_if_invalid: bool = False
    # ):
    #     if raise_exception_if_invalid and str_in_dict(self.unknown_str, x_iux2aux):
    #         error_dict = get_str_in_sub_dict(self.unknown_str, x_iux2aux)
    #         exception_str = f"iux2aux cannot have unknown_str '{self.unknown_str}' in any str. Affected keys include {list(error_dict.keys())}."
    #         raise SetAlliux2auxError(exception_str)
    #     self.iux2aux = x_iux2aux

    # def to_dict(self) -> dict:
    #     """Returns dict that is serializable to JSON."""

    #     return {
    #         "spark_face": self.spark_face,
    #         "spark_num": self.spark_num,
    #         "iux_knot": self.iux_knot,
    #         "aux_knot": self.aux_knot,
    #         "unknown_str": self.unknown_str,
    #         "iux2aux": self.iux2aux,
    #     }


class NameYap(YapCore):
    pass
    # def set_iux2aux(self, iux_name: str, aux_name: str):
    #     self.iux2aux[iux_name] = aux_name

    # def get_aux_value(self, iux_name: str) -> str:
    #     return self.iux2aux.get(iux_name)

    # def iux2aux_exists(self, iux_name: str, aux_name: str) -> bool:
    #     return self.get_aux_value(iux_name) == aux_name

    # def iux_exists(self, iux_name: str) -> bool:
    #     return self.get_aux_value(iux_name) != None

    # def del_iux2aux(self, iux_name: str):
    #     self.iux2aux.pop(iux_name)

    # def reveal_aux(self, iux_name: str, missing_add: bool = True) -> str:
    #     if missing_add and self.iux_exists(iux_name) is False:
    #         aux_name = copy_copy(iux_name)
    #         if self.aux_knot in iux_name:
    #             return None
    #         iux_r_knot = self.iux_knot
    #         aux_r_knot = self.aux_knot
    #         aux_name = aux_name.replace(iux_r_knot, aux_r_knot)
    #         self.set_iux2aux(iux_name, aux_name)

    #     return self.get_aux_value(iux_name)

    # def _is_aux_knot_inclusion_correct(self) -> bool:
    #     return not str_in_dict_values(self.aux_knot, self.iux2aux)

    # def _is_iux_knot_inclusion_correct(self) -> bool:
    #     return not str_in_dict_keys(self.iux_knot, self.iux2aux)

    # def is_valid(self) -> bool:
    #     return (
    #         self._is_aux_knot_inclusion_correct()
    #         and self._is_iux_knot_inclusion_correct()
    #     )


# def nameyap_shop(
#     spark_face: FaceName = None,
#     spark_num: SparkInt = None,
#     iux_knot: KnotTerm = None,
#     aux_knot: KnotTerm = None,
#     iux2aux: dict = None,
#     unknown_str: str = None,
# ) -> NameYap:
#     unknown_str = default_unknown_str_if_None(unknown_str)
#     iux_knot = default_knot_if_None(iux_knot)
#     aux_knot = default_knot_if_None(aux_knot)

#     return NameYap(
#         spark_face=spark_face,
#         spark_num=get_0_if_None(spark_num),
#         iux_knot=iux_knot,
#         aux_knot=aux_knot,
#         unknown_str=unknown_str,
#         iux2aux=get_empty_dict_if_None(iux2aux),
#     )


# def get_nameyap_from_dict(x_dict: dict) -> NameYap:
#     return nameyap_shop(
#         spark_face=x_dict.get("spark_face"),
#         spark_num=x_dict.get("spark_num"),
#         iux_knot=x_dict.get("iux_knot"),
#         aux_knot=x_dict.get("aux_knot"),
#         iux2aux=x_dict.get("iux2aux"),
#         unknown_str=x_dict.get("unknown_str"),
#     )


# class TitleYap(YapCore):
#     def set_iux2aux(self, iux_title: str, aux_title: str):
#         self.iux2aux[iux_title] = aux_title

#     def get_aux_value(self, iux_title: str) -> str:
#         return self.iux2aux.get(iux_title)

#     def iux2aux_exists(self, iux_title: str, aux_title: str) -> bool:
#         return self.get_aux_value(iux_title) == aux_title

#     def iux_exists(self, iux_title: str) -> bool:
#         return self.get_aux_value(iux_title) != None

#     def del_iux2aux(self, iux_title: str):
#         self.iux2aux.pop(iux_title)

#     def reveal_aux(self, iux_title: str, missing_add: bool = True) -> str:
#         if missing_add and self.iux_exists(iux_title) is False:
#             aux_title = copy_copy(iux_title)
#             if self.aux_knot in iux_title:
#                 return None
#             iux_r_knot = self.iux_knot
#             aux_r_knot = self.aux_knot
#             aux_title = aux_title.replace(iux_r_knot, aux_r_knot)
#             self.set_iux2aux(iux_title, aux_title)

#         return self.get_aux_value(iux_title)

#     def _is_aux_knot_inclusion_correct(self):
#         return str_in_all_dict_values(self.aux_knot, self.iux2aux)

#     def _is_iux_knot_inclusion_correct(self):
#         return str_in_all_dict_keys(self.iux_knot, self.iux2aux)

#     def is_valid(self):
#         return (
#             self._is_iux_knot_inclusion_correct()
#             and self._is_aux_knot_inclusion_correct()
#         )


# def titleyap_shop(
#     spark_face: FaceName = None,
#     spark_num: SparkInt = None,
#     iux_knot: KnotTerm = None,
#     aux_knot: KnotTerm = None,
#     iux2aux: dict = None,
#     unknown_str: str = None,
# ) -> TitleYap:
#     unknown_str = default_unknown_str_if_None(unknown_str)
#     iux_knot = default_knot_if_None(iux_knot)
#     aux_knot = default_knot_if_None(aux_knot)

#     return TitleYap(
#         spark_face=spark_face,
#         spark_num=get_0_if_None(spark_num),
#         iux_knot=iux_knot,
#         aux_knot=aux_knot,
#         unknown_str=unknown_str,
#         iux2aux=get_empty_dict_if_None(iux2aux),
#     )


# def get_titleyap_from_dict(x_dict: dict) -> TitleYap:
#     return titleyap_shop(
#         spark_face=x_dict.get("spark_face"),
#         spark_num=x_dict.get("spark_num"),
#         iux_knot=x_dict.get("iux_knot"),
#         aux_knot=x_dict.get("aux_knot"),
#         iux2aux=x_dict.get("iux2aux"),
#         unknown_str=x_dict.get("unknown_str"),
#     )


# class LabelYap(YapCore):
#     def set_iux2aux(self, iux_label: str, aux_label: str):
#         self.iux2aux[iux_label] = aux_label

#     def get_aux_value(self, iux_label: str) -> str:
#         return self.iux2aux.get(iux_label)

#     def iux2aux_exists(self, iux_label: str, aux_label: str) -> bool:
#         return self.get_aux_value(iux_label) == aux_label

#     def iux_exists(self, iux_label: str) -> bool:
#         return self.get_aux_value(iux_label) != None

#     def del_iux2aux(self, iux_label: str):
#         self.iux2aux.pop(iux_label)

#     def reveal_aux(self, iux_label: str, missing_add: bool = True) -> str:
#         if missing_add and self.iux_exists(iux_label) is False:
#             aux_label = copy_copy(iux_label)
#             if self.aux_knot in iux_label:
#                 return None
#             iux_r_knot = self.iux_knot
#             aux_r_knot = self.aux_knot
#             aux_label = aux_label.replace(iux_r_knot, aux_r_knot)
#             self.set_iux2aux(iux_label, aux_label)

#         return self.get_aux_value(iux_label)

#     def _is_aux_knot_inclusion_correct(self) -> bool:
#         return not str_in_dict_values(self.aux_knot, self.iux2aux)

#     def _is_iux_knot_inclusion_correct(self) -> bool:
#         return not str_in_dict_keys(self.iux_knot, self.iux2aux)

#     def is_valid(self) -> bool:
#         return (
#             self._is_aux_knot_inclusion_correct()
#             and self._is_iux_knot_inclusion_correct()
#         )


# def labelyap_shop(
#     spark_face: FaceName = None,
#     spark_num: SparkInt = None,
#     iux_knot: KnotTerm = None,
#     aux_knot: KnotTerm = None,
#     iux2aux: dict = None,
#     unknown_str: str = None,
# ) -> LabelYap:
#     unknown_str = default_unknown_str_if_None(unknown_str)
#     iux_knot = default_knot_if_None(iux_knot)
#     aux_knot = default_knot_if_None(aux_knot)

#     return LabelYap(
#         spark_face=spark_face,
#         spark_num=get_0_if_None(spark_num),
#         iux_knot=iux_knot,
#         aux_knot=aux_knot,
#         unknown_str=unknown_str,
#         iux2aux=get_empty_dict_if_None(iux2aux),
#     )


# def get_labelyap_from_dict(x_dict: dict) -> LabelYap:
#     return labelyap_shop(
#         spark_face=x_dict.get("spark_face"),
#         spark_num=x_dict.get("spark_num"),
#         iux_knot=x_dict.get("iux_knot"),
#         aux_knot=x_dict.get("aux_knot"),
#         iux2aux=x_dict.get("iux2aux"),
#         unknown_str=x_dict.get("unknown_str"),
#     )


# @dataclass
# class RopeYap:
#     spark_face: FaceName = None
#     spark_num: SparkInt = None
#     iux2aux: dict = None
#     unknown_str: str = None
#     iux_knot: KnotTerm = None
#     aux_knot: KnotTerm = None
#     labelyap: LabelYap = None

#     def set_all_iux2aux(
#         self, x_iux2aux: dict, raise_exception_if_invalid: bool = False
#     ):
#         if raise_exception_if_invalid and str_in_dict(self.unknown_str, x_iux2aux):
#             error_dict = get_str_in_sub_dict(self.unknown_str, x_iux2aux)
#             exception_str = f"iux2aux cannot have unknown_str '{self.unknown_str}' in any str. Affected keys include {list(error_dict.keys())}."
#             raise SetAlliux2auxError(exception_str)
#         self.iux2aux = x_iux2aux

#     def set_iux2aux(self, iux_rope: str, aux_rope: str):
#         self.iux2aux[iux_rope] = aux_rope

#     def get_aux_value(self, iux_rope: str) -> str:
#         return self.iux2aux.get(iux_rope)

#     def reveal_aux(self, iux_rope: str, missing_add: bool = True) -> str:
#         if missing_add and self.iux_exists(iux_rope) is False:
#             aux_rope = copy_copy(iux_rope)
#             aux_rope = self._reveal_rope_aux(iux_rope)
#             self.set_iux2aux(iux_rope, aux_rope)

#         return self.get_aux_value(iux_rope)

#     def _reveal_rope_aux(self, iux_rope) -> RopeTerm:
#         iux_parent_rope = get_parent_rope(iux_rope, self.iux_knot)
#         if self.iux_exists(iux_parent_rope) is False and iux_parent_rope != "":
#             return None
#         iux_tail = get_tail_label(iux_rope, self.iux_knot)
#         iux_tail = self._get_labelyap_labelterm(iux_tail)
#         if iux_parent_rope == "":
#             aux_parent_rope = ""
#         else:
#             aux_parent_rope = self.get_aux_value(iux_parent_rope)
#         return create_rope(aux_parent_rope, iux_tail, self.aux_knot)

#     def _get_labelyap_labelterm(self, x_labelTerm: LabelTerm) -> LabelTerm:
#         if self.iux_label_exists(x_labelTerm):
#             return self.labelyap.reveal_aux(x_labelTerm)
#         return x_labelTerm

#     def iux2aux_exists(self, iux_rope: str, aux_rope: str) -> bool:
#         return self.get_aux_value(iux_rope) == aux_rope

#     def iux_exists(self, iux_rope: str) -> bool:
#         return self.get_aux_value(iux_rope) != None

#     def del_iux2aux(self, iux_rope: str):
#         self.iux2aux.pop(iux_rope)

#     def set_label(self, iux_label: LabelTerm, aux_label: LabelTerm):
#         if self.iux_knot in iux_label:
#             exception_str = f"label cannot have iux_label '{iux_label}'. It must be not have knot {self.iux_knot}."
#             raise SetLabelError(exception_str)
#         if self.aux_knot in aux_label:
#             exception_str = f"label cannot have aux_label '{aux_label}'. It must be not have knot {self.aux_knot}."
#             raise SetLabelError(exception_str)

#         self.labelyap.set_iux2aux(iux_label, aux_label)
#         self._set_new_label_to_iux_aux(iux_label, aux_label)

#     def _set_new_label_to_iux_aux(self, iux_label, aux_label):
#         for iux_rope, aux_rope in self.iux2aux.items():
#             iux_labelterms = get_all_rope_labels(iux_rope, self.iux_knot)
#             aux_labelterms = get_all_rope_labels(aux_rope, self.aux_knot)
#             for x_count, iux_labelterm in enumerate(iux_labelterms):
#                 if iux_labelterm == iux_label:
#                     aux_labelterms[x_count] = aux_label
#             self.set_iux2aux(iux_rope, create_rope_from_labels(aux_labelterms))

#     def label_exists(self, iux_label: LabelTerm, aux_label: LabelTerm) -> bool:
#         return self.labelyap.iux2aux_exists(iux_label, aux_label)

#     def iux_label_exists(self, iux_label: LabelTerm) -> bool:
#         return self.labelyap.iux_exists(iux_label)

#     def del_label(self, iux_label: LabelTerm) -> bool:
#         self.labelyap.del_iux2aux(iux_label)

#     def unknown_str_in_iux2aux(self) -> bool:
#         return str_in_dict(self.unknown_str, self.iux2aux)

#     def all_iux_parent_ropes_exist(self) -> bool:
#         for x_rope in self.iux2aux.keys():
#             parent_rope = get_parent_rope(x_rope, self.iux_knot)
#             if parent_rope and self.iux_exists(parent_rope) is False:
#                 return False
#         return True

#     def is_valid(self) -> bool:
#         return self.all_iux_parent_ropes_exist()

#     def to_dict(self) -> dict:
#         """Returns dict that is serializable to JSON."""

#         return {
#             "spark_face": self.spark_face,
#             "spark_num": self.spark_num,
#             "iux_knot": self.iux_knot,
#             "aux_knot": self.aux_knot,
#             "unknown_str": self.unknown_str,
#             "iux2aux": self.iux2aux,
#         }


# def ropeyap_shop(
#     spark_face: FaceName = None,
#     spark_num: SparkInt = None,
#     iux_knot: KnotTerm = None,
#     aux_knot: KnotTerm = None,
#     x_labelyap: LabelYap = None,
#     iux2aux: dict = None,
#     unknown_str: str = None,
# ) -> RopeYap:
#     unknown_str = default_unknown_str_if_None(unknown_str)
#     iux_knot = default_knot_if_None(iux_knot)
#     aux_knot = default_knot_if_None(aux_knot)

#     if x_labelyap is None:
#         x_labelyap = labelyap_shop(
#             iux_knot=iux_knot,
#             aux_knot=aux_knot,
#             unknown_str=unknown_str,
#             spark_face=spark_face,
#             spark_num=spark_num,
#         )

#     return RopeYap(
#         iux2aux=get_empty_dict_if_None(iux2aux),
#         unknown_str=unknown_str,
#         iux_knot=iux_knot,
#         aux_knot=aux_knot,
#         labelyap=x_labelyap,
#         spark_face=spark_face,
#         spark_num=get_0_if_None(spark_num),
#     )


# def get_ropeyap_from_dict(x_dict: dict) -> RopeYap:
#     return ropeyap_shop(
#         spark_face=x_dict.get("spark_face"),
#         spark_num=x_dict.get("spark_num"),
#         iux_knot=x_dict.get("iux_knot"),
#         aux_knot=x_dict.get("aux_knot"),
#         iux2aux=x_dict.get("iux2aux"),
#         unknown_str=x_dict.get("unknown_str"),
#     )


# class YapCoreAttrConflictError(Exception):
#     pass


# def _check_core_attrs_match(new_obj: YapCore, old_obj: YapCore):
#     if (
#         old_obj.spark_face != new_obj.spark_face
#         or old_obj.iux_knot != new_obj.iux_knot
#         or old_obj.aux_knot != new_obj.aux_knot
#         or old_obj.unknown_str != new_obj.unknown_str
#     ):
#         raise YapCoreAttrConflictError("Core attrs in conflict")
#     if old_obj.spark_num >= new_obj.spark_num:
#         raise YapCoreAttrConflictError("older yapunit is not older")


# def _inherit_yapunit(new: YapCore, old: YapCore):
#     _check_core_attrs_match(new, old)
#     for iux2aux_key, old_aux in old.iux2aux.items():
#         if new.iux_exists(iux2aux_key) is False:
#             new.set_iux2aux(iux2aux_key, old_aux)
#     return new


# def inherit_nameyap(new: NameYap, old: NameYap) -> NameYap:
#     return _inherit_yapunit(new, old)


# def inherit_titleyap(new: TitleYap, old: TitleYap) -> TitleYap:
#     return _inherit_yapunit(new, old)


# def inherit_labelyap(new: LabelYap, old: LabelYap) -> LabelYap:
#     return _inherit_yapunit(new, old)


# def inherit_ropeyap(new: RopeYap, old: RopeYap) -> RopeYap:
#     return _inherit_yapunit(new, old)
