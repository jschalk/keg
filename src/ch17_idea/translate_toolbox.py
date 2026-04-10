from os.path import exists as os_path_exists
from pandas import DataFrame
from src.ch00_py.file_toolbox import create_path, get_dir_file_strs, save_file
from src.ch16_translate.translate_main import (
    LabelMap,
    NameMap,
    RopeMap,
    TitleMap,
    TranslateUnit,
    translateunit_shop,
)
from src.ch17_idea.brick_db_tool import get_ordered_csv, open_csv


def get_translate_name_dt_columns() -> list[str]:
    return [
        "spark_num",
        "spark_face",
        "otx_knot",
        "inx_knot",
        "unknown_str",
        "otx_name",
        "inx_name",
    ]


def get_translate_title_dt_columns() -> list[str]:
    return [
        "spark_num",
        "spark_face",
        "otx_knot",
        "inx_knot",
        "unknown_str",
        "otx_title",
        "inx_title",
    ]


def get_translate_label_dt_columns() -> list[str]:
    return [
        "spark_num",
        "spark_face",
        "otx_knot",
        "inx_knot",
        "unknown_str",
        "otx_label",
        "inx_label",
    ]


def get_translate_rope_dt_columns() -> list[str]:
    return [
        "spark_num",
        "spark_face",
        "otx_knot",
        "inx_knot",
        "unknown_str",
        "otx_rope",
        "inx_rope",
    ]


def create_translate_name_dt(x_map: NameMap) -> DataFrame:
    x_rows_list = [
        {
            "spark_num": x_map.spark_num,
            "spark_face": x_map.spark_face,
            "otx_knot": x_map.otx_knot,
            "inx_knot": x_map.inx_knot,
            "unknown_str": x_map.unknown_str,
            "otx_name": otx_value,
            "inx_name": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_translate_name_dt_columns())


def create_translate_title_dt(x_map: TitleMap) -> DataFrame:
    x_rows_list = [
        {
            "spark_num": x_map.spark_num,
            "spark_face": x_map.spark_face,
            "otx_knot": x_map.otx_knot,
            "inx_knot": x_map.inx_knot,
            "unknown_str": x_map.unknown_str,
            "otx_title": otx_value,
            "inx_title": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_translate_title_dt_columns())


def create_translate_label_dt(x_map: LabelMap) -> DataFrame:
    x_rows_list = [
        {
            "spark_num": x_map.spark_num,
            "spark_face": x_map.spark_face,
            "otx_knot": x_map.otx_knot,
            "inx_knot": x_map.inx_knot,
            "unknown_str": x_map.unknown_str,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_translate_label_dt_columns())


def create_translate_rope_dt(x_map: RopeMap) -> DataFrame:
    x_rows_list = [
        {
            "spark_num": x_map.spark_num,
            "spark_face": x_map.spark_face,
            "otx_knot": x_map.otx_knot,
            "inx_knot": x_map.inx_knot,
            "unknown_str": x_map.unknown_str,
            "otx_rope": otx_value,
            "inx_rope": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_translate_rope_dt_columns())


def save_all_csvs_from_translateunit(x_dir: str, x_translateunit: TranslateUnit):
    _save_translate_name_csv(x_dir, x_translateunit.namemap)
    _save_translate_title_csv(x_dir, x_translateunit.titlemap)
    _save_translate_label_csv(x_dir, x_translateunit.labelmap)
    _save_translate_rope_csv(x_dir, x_translateunit.ropemap)


def _save_translate_name_csv(x_dir: str, namemap: NameMap):
    x_dt = create_translate_name_dt(namemap)
    save_file(x_dir, "name.csv", get_ordered_csv(x_dt))


def _save_translate_title_csv(x_dir: str, titlemap: TitleMap):
    x_dt = create_translate_title_dt(titlemap)
    save_file(x_dir, "title.csv", get_ordered_csv(x_dt))


def _save_translate_label_csv(x_dir: str, labelmap: LabelMap):
    x_dt = create_translate_label_dt(labelmap)
    save_file(x_dir, "label.csv", get_ordered_csv(x_dt))


def _save_translate_rope_csv(x_dir: str, ropemap: RopeMap):
    x_dt = create_translate_rope_dt(ropemap)
    save_file(x_dir, "rope.csv", get_ordered_csv(x_dt))


def _load_namemap_from_csv(x_dir, x_namemap: NameMap) -> NameMap:
    name_filename = "name.csv"
    if os_path_exists(create_path(x_dir, name_filename)):
        otx2inx_dt = open_csv(x_dir, name_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_name")
            inx_value = table_row.get("inx_name")
            if x_namemap.otx2inx_exists(otx_value, inx_value) is False:
                x_namemap.set_otx2inx(otx_value, inx_value)
    return x_namemap


def _load_titlemap_from_csv(x_dir, x_titlemap: TitleMap) -> TitleMap:
    title_filename = "title.csv"
    if os_path_exists(create_path(x_dir, title_filename)):
        otx2inx_dt = open_csv(x_dir, title_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_title")
            inx_value = table_row.get("inx_title")
            if x_titlemap.otx2inx_exists(otx_value, inx_value) is False:
                x_titlemap.set_otx2inx(otx_value, inx_value)
    return x_titlemap


def _load_labelmap_from_csv(x_dir, x_labelmap: LabelMap) -> LabelMap:
    label_filename = "label.csv"
    if os_path_exists(create_path(x_dir, label_filename)):
        otx2inx_dt = open_csv(x_dir, "label.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_label")
            inx_value = table_row.get("inx_label")
            if x_labelmap.otx2inx_exists(otx_value, inx_value) is False:
                x_labelmap.set_otx2inx(otx_value, inx_value)
    return x_labelmap


def _load_ropemap_from_csv(x_dir, x_ropemap: RopeMap) -> RopeMap:
    rope_filename = "rope.csv"
    if os_path_exists(create_path(x_dir, rope_filename)):
        otx2inx_dt = open_csv(x_dir, "rope.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_rope")
            inx_value = table_row.get("inx_rope")
            if x_ropemap.otx2inx_exists(otx_value, inx_value) is False:
                x_ropemap.set_otx2inx(otx_value, inx_value)
    return x_ropemap


def create_dir_valid_empty_translateunit(x_dir: str) -> TranslateUnit:
    spark_face_set = set()
    spark_num_set = set()
    unknown_str_set = set()
    otx_knot_set = set()
    inx_knot_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        spark_face_set.update(x_dt.spark_face.unique())
        spark_num_set.update(x_dt.spark_num.unique())
        unknown_str_set.update(x_dt.unknown_str.unique())
        otx_knot_set.update(x_dt.otx_knot.unique())
        inx_knot_set.update(x_dt.inx_knot.unique())

    if len(spark_face_set) == 1:
        spark_face = spark_face_set.pop()
    if len(spark_num_set) == 1:
        spark_num = spark_num_set.pop()
    if len(unknown_str_set) == 1:
        unknown_str = unknown_str_set.pop()
    if len(otx_knot_set) == 1:
        otx_knot = otx_knot_set.pop()
    if len(inx_knot_set) == 1:
        inx_knot = inx_knot_set.pop()

    return translateunit_shop(
        spark_face=spark_face,
        spark_num=spark_num,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )


def init_translateunit_from_dir(x_dir: str) -> TranslateUnit:
    x_translateunit = create_dir_valid_empty_translateunit(x_dir)
    _load_namemap_from_csv(x_dir, x_translateunit.namemap)
    _load_titlemap_from_csv(x_dir, x_translateunit.titlemap)
    _load_labelmap_from_csv(x_dir, x_translateunit.labelmap)
    _load_ropemap_from_csv(x_dir, x_translateunit.ropemap)
    x_translateunit.ropemap.labelmap = x_translateunit.labelmap
    return x_translateunit
