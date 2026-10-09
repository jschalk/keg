from ch00_py.file_toolbox import create_path, get_dir_file_strs
from ch17_jargon.test._util.ch17_examples import (  # get_casa_maison_jargonunit_set_by_epoch,
    get_casa_maison_label_dt,
    get_casa_maison_rope_otx2inx_dt,
    get_casa_maison_jargonunit_set_by_label,
    get_casa_maison_jargonunit_set_by_otx2inx,
    get_slash_namemap,
    get_sue_jargonunit,
)
from ch17_jargon.jargon_main import jargonunit_shop
from ch20_brick.brick_db_tool import get_ordered_csv
from ch20_brick.jargon_toolbox import (
    _load_labelmap_from_csv,
    _load_namemap_from_csv,
    _load_ropemap_from_csv,
    _load_titlemap_from_csv,
    _save_jargon_label_csv,
    create_dir_valid_empty_jargonunit,
    create_jargon_label_dt,
    create_jargon_name_dt,
    create_jargon_rope_dt,
    create_jargon_title_dt,
    get_jargon_label_dt_columns,
    get_jargon_name_dt_columns,
    get_jargon_rope_dt_columns,
    get_jargon_title_dt_columns,
    init_jargonunit_from_dir,
    save_all_csvs_from_jargonunit,
)
from ch99_glossary.ch_keyword import Ch20Keywords as kw, ExampleStrs as exx
from ch99_glossary.sorter import get_keg_elements_sort_order as sorting_columns
from os.path import exists as os_path_exists


def test_get_jargon_name_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_jargon_name_dt_columns()
    assert len(get_jargon_name_dt_columns()) == 7
    static_list = [
        kw.spark_num,
        kw.spark_face,
        kw.otx_knot,
        kw.inx_knot,
        kw.unknown_str,
        "otx_name",
        "inx_name",
    ]
    assert get_jargon_name_dt_columns() == static_list
    assert set(get_jargon_name_dt_columns()).issubset(set(sorting_columns()))


def test_get_jargon_title_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_jargon_title_dt_columns()
    assert len(get_jargon_title_dt_columns()) == 7
    static_list = [
        kw.spark_num,
        kw.spark_face,
        kw.otx_knot,
        kw.inx_knot,
        kw.unknown_str,
        kw.otx_title,
        kw.inx_title,
    ]
    assert get_jargon_title_dt_columns() == static_list
    assert set(get_jargon_title_dt_columns()).issubset(set(sorting_columns()))


def test_get_jargon_label_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_jargon_label_dt_columns()
    assert len(get_jargon_label_dt_columns()) == 7
    static_list = [
        kw.spark_num,
        kw.spark_face,
        kw.otx_knot,
        kw.inx_knot,
        kw.unknown_str,
        kw.otx_label,
        kw.inx_label,
    ]
    assert get_jargon_label_dt_columns() == static_list
    assert set(get_jargon_label_dt_columns()).issubset(set(sorting_columns()))


def test_get_jargon_rope_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_jargon_rope_dt_columns()
    assert len(get_jargon_rope_dt_columns()) == 7
    static_list = [
        kw.spark_num,
        kw.spark_face,
        kw.otx_knot,
        kw.inx_knot,
        kw.unknown_str,
        kw.otx_rope,
        kw.inx_rope,
    ]
    assert get_jargon_rope_dt_columns() == static_list
    assert set(get_jargon_rope_dt_columns()).issubset(set(sorting_columns()))


def test_create_jargon_rope_dt_ReturnsObj():
    # ESTABLISH
    casa_jargonunit = get_casa_maison_jargonunit_set_by_otx2inx()
    casa_mapunit = casa_jargonunit.get_ropemap()

    # WHEN
    casa_dataframe = create_jargon_rope_dt(casa_mapunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_jargon_rope_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{get_jargon_rope_dt_columns()=}")
    print(f"{casa_dataframe.columns=}")
    print(casa_csv)
    print(get_ordered_csv(get_casa_maison_rope_otx2inx_dt()))
    assert casa_csv == get_ordered_csv(get_casa_maison_rope_otx2inx_dt())


def test_create_jargon_label_dt_ReturnsObj():
    # ESTABLISH
    casa_jargonunit = get_casa_maison_jargonunit_set_by_label()
    casa_mapunit = casa_jargonunit.get_labelmap()

    # WHEN
    casa_dataframe = create_jargon_label_dt(casa_mapunit)

    # THEN
    # print(f"{get_jargon_label_dt_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_jargon_label_dt_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_label_csv = get_ordered_csv(get_casa_maison_label_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_label_csv=}")
    assert casa_csv == ex_label_csv


def test_save_all_csvs_from_jargonunit_SavesFiles(temp3_fs):
    # ESTABLISH
    sue_jargonunit = get_sue_jargonunit()
    map_dir = str(temp3_fs)
    name_filename = "name.csv"
    title_filename = "title.csv"
    label_filename = "label.csv"
    rope_filename = "rope.csv"
    name_csv_path = create_path(map_dir, name_filename)
    group_csv_path = create_path(map_dir, title_filename)
    label_csv_path = create_path(map_dir, label_filename)
    rope_csv_path = create_path(map_dir, rope_filename)
    assert os_path_exists(name_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(label_csv_path) is False
    assert os_path_exists(rope_csv_path) is False
    assert len(get_dir_file_strs(map_dir)) == 0

    # WHEN
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)

    # THEN
    assert os_path_exists(name_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(label_csv_path)
    assert os_path_exists(rope_csv_path)
    assert len(get_dir_file_strs(map_dir)) == 4


def test_load_namemap_from_csv_SetsAttrWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_jargonunit = get_sue_jargonunit()
    map_dir = str(temp3_fs)
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)
    assert os_path_exists(name_csv_path)
    empty_jargonunit = jargonunit_shop("Sue")
    sue_namemap = empty_jargonunit.get_mapunit(kw.NameTerm)
    sue_namemap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 3
    ex_namemap = sue_jargonunit.get_mapunit(kw.NameTerm)
    assert ex_namemap == sue_namemap


def test_load_namemap_from_csv_DoesNotChangeWhenFileDoesNotExist(temp3_fs):
    # ESTABLISH
    map_dir = str(temp3_fs)
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    assert os_path_exists(name_csv_path) is False
    empty_jargonunit = jargonunit_shop("Sue")
    sue_namemap = empty_jargonunit.get_mapunit(kw.NameTerm)
    sue_namemap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 0


def test_load_titlemap_from_csv_SetsAttrWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_jargonunit = get_sue_jargonunit()
    map_dir = str(temp3_fs)
    title_filename = "title.csv"
    group_csv_path = create_path(map_dir, title_filename)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)
    assert os_path_exists(group_csv_path)
    empty_jargonunit = jargonunit_shop("Sue")
    sue_titlemap = empty_jargonunit.get_mapunit(kw.TitleTerm)
    sue_titlemap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 2
    ex_titlemap = sue_jargonunit.get_mapunit(kw.TitleTerm)
    assert ex_titlemap == sue_titlemap


def test_load_titlemap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    temp3_fs,
):
    # ESTABLISH
    map_dir = str(temp3_fs)
    title_filename = "title.csv"
    group_csv_path = create_path(map_dir, title_filename)
    assert os_path_exists(group_csv_path) is False
    empty_jargonunit = jargonunit_shop("Sue")
    sue_titlemap = empty_jargonunit.get_mapunit(kw.TitleTerm)
    sue_titlemap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 0


def test_load_labelmap_from_csv_SetsAttrWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_jargonunit = get_sue_jargonunit()
    map_dir = str(temp3_fs)
    label_filename = "label.csv"
    label_csv_path = create_path(map_dir, label_filename)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)
    assert os_path_exists(label_csv_path)
    empty_jargonunit = jargonunit_shop("Sue")
    sue_labelmap = empty_jargonunit.get_mapunit(kw.LabelTerm)
    sue_labelmap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 2
    ex_labelmap = sue_jargonunit.get_mapunit(kw.LabelTerm)
    assert ex_labelmap == sue_labelmap


def test_load_labelmap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    temp3_fs,
):
    # ESTABLISH
    map_dir = str(temp3_fs)
    label_filename = "label.csv"
    label_csv_path = create_path(map_dir, label_filename)
    assert os_path_exists(label_csv_path) is False
    empty_jargonunit = jargonunit_shop("Sue")
    sue_labelmap = empty_jargonunit.get_mapunit(kw.LabelTerm)
    sue_labelmap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 0


def test_load_ropemap_from_csv_SetsAttrWhenFileExists(temp3_fs):
    # ESTABLISH
    sue_jargonunit = get_sue_jargonunit()
    map_dir = str(temp3_fs)
    rope_filename = "rope.csv"
    rope_csv_path = create_path(map_dir, rope_filename)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)
    assert os_path_exists(rope_csv_path)
    empty_jargonunit = jargonunit_shop("Sue")
    sue_ropemap = empty_jargonunit.get_mapunit(kw.RopeTerm)
    sue_ropemap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_ropemap=}")
    assert len(sue_ropemap.otx2inx) == 0

    # WHEN
    sue_ropemap = _load_ropemap_from_csv(map_dir, sue_ropemap)

    # THEN
    assert len(sue_ropemap.otx2inx) == 2
    ex_ropemap = sue_jargonunit.get_mapunit(kw.RopeTerm)
    assert ex_ropemap.spark_num == sue_ropemap.spark_num
    assert ex_ropemap.spark_face == sue_ropemap.spark_face
    assert ex_ropemap.otx2inx == sue_ropemap.otx2inx
    assert ex_ropemap.labelmap != sue_ropemap.labelmap


def test_load_ropemap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    temp3_fs,
):
    # ESTABLISH
    map_dir = str(temp3_fs)
    rope_filename = "rope.csv"
    rope_csv_path = create_path(map_dir, rope_filename)
    assert os_path_exists(rope_csv_path) is False
    empty_jargonunit = jargonunit_shop("Sue")
    sue_ropemap = empty_jargonunit.get_mapunit(kw.RopeTerm)
    sue_ropemap.spark_face = "Sue"
    print(f"{empty_jargonunit=} {sue_ropemap=}")
    assert len(sue_ropemap.otx2inx) == 0

    # WHEN
    sue_ropemap = _load_ropemap_from_csv(map_dir, sue_ropemap)

    # THEN
    assert len(sue_ropemap.otx2inx) == 0


def test_create_dir_valid_empty_jargonunit_Sets_otx_knot_inx_knot(
    temp3_fs,
):  # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_jargonunit = jargonunit_shop(
        spark_face=exx.sue,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_jargonunit.set_namemap(get_slash_namemap())
    map_dir = str(temp3_fs)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)

    # WHEN
    gen_jargonunit = create_dir_valid_empty_jargonunit(map_dir)

    # # THEN
    assert gen_jargonunit.unknown_str == x_unknown_str
    assert gen_jargonunit.otx_knot == slash_otx_knot
    assert gen_jargonunit.inx_knot == colon_inx_knot
    gen_mapunit = gen_jargonunit.get_mapunit(kw.NameTerm)
    assert gen_mapunit.unknown_str == x_unknown_str
    assert gen_mapunit.otx_knot == slash_otx_knot
    assert gen_mapunit.inx_knot == colon_inx_knot


def test_create_dir_valid_empty_jargonunit_Returns_spark_num(
    temp3_fs,
):
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    spark7 = 7
    sue_jargonunit = jargonunit_shop(
        spark_face=exx.sue,
        spark_num=spark7,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_jargonunit.set_namemap(get_slash_namemap())
    map_dir = str(temp3_fs)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)

    # WHEN
    gen_jargonunit = create_dir_valid_empty_jargonunit(map_dir)

    # THEN
    assert gen_jargonunit.spark_face == exx.sue
    assert gen_jargonunit.spark_num == spark7
    assert gen_jargonunit.unknown_str == x_unknown_str
    assert gen_jargonunit.otx_knot == slash_otx_knot
    assert gen_jargonunit.inx_knot == colon_inx_knot
    gen_mapunit = gen_jargonunit.get_mapunit(kw.NameTerm)
    assert gen_mapunit.unknown_str == x_unknown_str
    assert gen_mapunit.otx_knot == slash_otx_knot
    assert gen_mapunit.inx_knot == colon_inx_knot


def test_init_jargonunit_from_dir_ReturnsObj(temp3_fs):
    # ESTABLISH
    sue_jargonunit = get_sue_jargonunit()
    map_dir = str(temp3_fs)
    save_all_csvs_from_jargonunit(map_dir, sue_jargonunit)

    # WHEN
    gen_jargonunit = init_jargonunit_from_dir(map_dir)

    # THEN
    assert gen_jargonunit
    assert len(gen_jargonunit.namemap.otx2inx) == 3

    assert len(sue_jargonunit.namemap.otx2inx) == 3
    assert gen_jargonunit.namemap == sue_jargonunit.namemap
    assert gen_jargonunit.titlemap == sue_jargonunit.titlemap
    assert gen_jargonunit.labelmap == sue_jargonunit.labelmap
    assert gen_jargonunit.ropemap.labelmap == sue_jargonunit.ropemap.labelmap
    assert gen_jargonunit.ropemap == sue_jargonunit.ropemap
    assert gen_jargonunit == sue_jargonunit
