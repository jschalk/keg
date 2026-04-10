from src.ch00_py.file_toolbox import create_path, get_dir_file_strs
from src.ch17_idea.brick_main import (
    _generate_brick_dataframe,
    _get_headers_list,
    get_brickref_obj,
)
from src.ch17_idea.idea_config import (
    br00013_planunit_v0_0_0,
    br00019_planunit_v0_0_0,
    br00020_person_contact_membership_v0_0_0,
    br00021_person_contactunit_v0_0_0,
    get_brick_format_filenames,
    get_brick_format_headers,
    get_brick_formats_dir,
    get_brickref_from_file,
    get_default_sorted_list,
    get_dimen_minimum_del_brick_names,
    get_dimen_minimum_put_brick_names,
    get_idea_config_dict,
    get_idea_elements_sort_order,
)
from src.ch17_idea.test.test_brick.test__idea_config import change_erase_attrs
from src.ref.keywords import Ch17Keywords as kw


def test_config_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    x00021_idea = "br00021_person_contactunit_v0_0_0"
    assert br00021_person_contactunit_v0_0_0() == x00021_idea
    x00020_idea = "br00020_person_contact_membership_v0_0_0"
    assert br00020_person_contact_membership_v0_0_0() == x00020_idea
    x0003_idea = "br00013_planunit_v0_0_0"
    assert br00013_planunit_v0_0_0() == x0003_idea


def test_get_brick_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    idea_dir = get_brick_formats_dir()
    # THEN
    print(f"{idea_dir=}")
    src_chapter_dir = create_path("src", "ch17_idea")
    print(f"{src_chapter_dir=}")
    assert idea_dir == create_path(src_chapter_dir, "brick_formats")


def test_get_brickref_obj_ReturnsObj():
    # ESTABLISH
    brick_name_00021 = br00021_person_contactunit_v0_0_0()

    # WHEN
    x_brickref = get_brickref_obj(brick_name_00021)

    # THEN
    assert x_brickref.brick_name == brick_name_00021
    assert set(x_brickref.dimens) == {
        kw.person_contactunit,
        kw.personunit,
        kw.momentunit,
    }
    assert x_brickref.attributes != {}
    assert len(x_brickref.attributes) == 8


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(br00021_person_contactunit_v0_0_0())

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        kw.spark_num,
        kw.spark_face,
        kw.moment_rope,
        kw.person_name,
        kw.contact_name,
        kw.contact_cred_lumen,
        kw.contact_debt_lumen,
        kw.knot,
    ]


def get_sorted_headers_str(idea_filename):
    x_brickref = get_brickref_from_file(idea_filename)
    idea_attributes = set(x_brickref.get(kw.attributes).keys())
    idea_attributes.remove(kw.spark_face)
    idea_attributes.remove(kw.spark_num)
    # print(f"{idea_attributes=}")
    attr_sort = get_idea_elements_sort_order()
    idea_attributes = get_default_sorted_list(idea_attributes, attr_sort)
    # print(f"{idea_attributes=}")
    header_str = "".join(f",{x_header}" for x_header in idea_attributes)
    return header_str[1:]
    # return create_sorted_planatenated_str(list(idea_attributes))


def test_get_sorted_headers_str_ReturnsObj_Scenario0_SingleExample():
    # ESTABLISH
    filebasename = br00021_person_contactunit_v0_0_0()

    # WHEN
    br00021_headers = get_sorted_headers_str(filebasename)

    # THEN
    expected_br00021_headers_str = f"{kw.moment_rope},{kw.person_name},{kw.contact_name},{kw.contact_cred_lumen},{kw.contact_debt_lumen},{kw.knot}"
    assert br00021_headers == expected_br00021_headers_str


def test_get_sorted_headers_str_ReturnsObj_Scenario1_SingleExample():
    # ESTABLISH / WHEN
    br00019_headers = get_sorted_headers_str(br00019_planunit_v0_0_0())

    # THEN
    print(f"{br00019_headers=}")
    expected_plan_headers_str = f"{kw.moment_rope},{kw.person_name},{kw.plan_rope},{kw.begin},{kw.close},{kw.addin},{kw.numor},{kw.denom},{kw.morph},{kw.gogo_want},{kw.stop_want}"
    assert br00019_headers == expected_plan_headers_str


def check_sorted_headers_exist(brick_format_filename: str, x_headers: dict):
    print(f"{brick_format_filename=}")
    sorted_headers = get_sorted_headers_str(brick_format_filename)
    assert_str = f"{brick_format_filename=} {sorted_headers=}"
    assert x_headers.get(sorted_headers) == brick_format_filename, assert_str


def test_get_brick_format_headers_ReturnsObj():
    # ESTABLISH / WHEN
    x_headers = get_brick_format_headers()

    # THEN
    # print(f"{set(get_brick_format_headers().values())=}")
    # sourcery skip: no-loop-in-tests
    for x_idea_filename in sorted(list(get_brick_format_filenames())):
        check_sorted_headers_exist(x_idea_filename, x_headers)

    # print(f"{x_headers=}")
    assert len(x_headers) == len(get_brick_format_filenames())
    assert set(x_headers.values()) == get_brick_format_filenames()


def test__generate_brick_dataframe_ReturnsObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = _generate_brick_dataframe(empty_d2, br00021_person_contactunit_v0_0_0())
    # THEN
    headers_list = _get_headers_list(br00021_person_contactunit_v0_0_0())
    assert list(x_df.columns) == headers_list


def for_all_ideas__generate_brick_dataframe():
    # Catching brope exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
    empty_d2 = []
    for x_filename in get_brick_format_filenames():
        try:
            _generate_brick_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"_generate_brick_dataframe failed for {x_filename=}")
            return False
    return True


def test__generate_brick_dataframe_ReturnsObjForEvery_idea():
    # ESTABLISH / WHEN / THEN
    assert for_all_ideas__generate_brick_dataframe()


def test_idea_FilesExist():
    # ESTABLISH
    idea_dir = get_brick_formats_dir()

    # WHEN
    idea_files = get_dir_file_strs(idea_dir, True)

    # THEN
    idea_filenames = set(idea_files.keys())
    print(f"{idea_filenames=}")
    assert idea_filenames == get_brick_format_filenames()
    assert len(idea_filenames) == len(get_brick_format_filenames())


def test_get_brickref_obj_HasAttrs_br00021_person_contactunit_v0_0_0():
    # ESTABLISH
    brick_name = br00021_person_contactunit_v0_0_0()

    # WHEN
    format_00001_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00001_brickref.attributes) == 8
    assert format_00001_brickref.attributes == {
        kw.contact_name: {kw.otx_key: True},
        kw.contact_cred_lumen: {kw.otx_key: False},
        kw.contact_debt_lumen: {kw.otx_key: False},
        kw.spark_num: {kw.otx_key: True},
        kw.spark_face: {kw.otx_key: True},
        kw.moment_rope: {kw.otx_key: True},
        kw.person_name: {kw.otx_key: True},
        kw.knot: {kw.otx_key: False},
    }
    headers_list = format_00001_brickref.get_headers_list()
    assert headers_list[0] == kw.spark_num
    assert headers_list[1] == kw.spark_face
    assert headers_list[2] == kw.moment_rope
    assert headers_list[3] == kw.person_name
    assert headers_list[4] == kw.contact_name
    assert headers_list[5] == kw.contact_cred_lumen
    assert headers_list[6] == kw.contact_debt_lumen


def test_get_brickref_obj_HasAttrs_br00020_person_contact_membership_v0_0_0():
    # ESTABLISH
    brick_name = br00020_person_contact_membership_v0_0_0()

    # WHEN
    format_00020_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00020_brickref.attributes) == 9
    headers_list = format_00020_brickref.get_headers_list()
    assert headers_list[0] == kw.spark_num
    assert headers_list[1] == kw.spark_face
    assert headers_list[2] == kw.moment_rope
    assert headers_list[3] == kw.person_name
    assert headers_list[4] == kw.contact_name
    assert headers_list[5] == kw.group_title
    assert headers_list[6] == kw.group_cred_lumen
    assert headers_list[7] == kw.group_debt_lumen
    assert headers_list[8] == kw.knot


def test_get_brickref_obj_HasAttrs_br00013_planunit_v0_0_0():
    # ESTABLISH
    brick_name = br00013_planunit_v0_0_0()

    # WHEN
    format_00003_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00003_brickref.attributes) == 7
    headers_list = format_00003_brickref.get_headers_list()
    assert headers_list[0] == kw.spark_num
    assert headers_list[1] == kw.spark_face
    assert headers_list[2] == kw.moment_rope
    assert headers_list[3] == kw.person_name
    assert headers_list[4] == kw.plan_rope
    assert headers_list[5] == kw.star
    assert headers_list[6] == kw.pledge


def test_get_brickref_obj_HasAttrs_br00019_planunit_v0_0_0():
    # ESTABLISH
    brick_name = br00019_planunit_v0_0_0()

    # WHEN
    format_00019_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00019_brickref.attributes) == 13
    headers_list = format_00019_brickref.get_headers_list()
    assert headers_list[0] == kw.spark_num
    assert headers_list[1] == kw.spark_face
    assert headers_list[2] == kw.moment_rope
    assert headers_list[3] == kw.person_name
    assert headers_list[4] == kw.plan_rope
    assert headers_list[5] == kw.begin
    assert headers_list[6] == kw.close
    assert headers_list[7] == kw.addin
    assert headers_list[8] == kw.numor
    assert headers_list[9] == kw.denom
    assert headers_list[10] == kw.morph
    assert headers_list[11] == kw.gogo_want
    assert headers_list[12] == kw.stop_want


def test_get_dimen_minimum_put_brick_names_ReturnsObj():
    # ESTABLISH / WHEN
    dimen_minimum_put_brick_names = get_dimen_minimum_put_brick_names()

    # THEN
    assert dimen_minimum_put_brick_names
    dimen_minimum_keys = set(dimen_minimum_put_brick_names.keys())
    idea_config_dict = get_idea_config_dict()
    idea_config_dimens = set(idea_config_dict.keys())
    # print(f"{idea_config_dimens=}")
    assert dimen_minimum_keys == idea_config_dimens
    for idea_dimen, dimen_config in idea_config_dict.items():
        brick_name = dimen_minimum_put_brick_names.get(idea_dimen)
        format_brickref = get_brickref_obj(brick_name)

        print(f"{idea_dimen=} {format_brickref.brick_name=}")
        dimen_args = set(dimen_config.get(kw.jkeys).keys())
        dimen_args.update(set(dimen_config.get(kw.jvalues).keys()))

        brickref_args = set(format_brickref.attributes.keys())
        # print(f"  {dimen_args=}")
        # print(f"{brickref_args=}")
        assert dimen_args == brickref_args


def test_get_dimen_minimum_del_brick_names_ReturnsObj():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    dimen_minimum_del_brick_names = get_dimen_minimum_del_brick_names()

    # THEN
    assert dimen_minimum_del_brick_names
    dimen_minimum_keys = set(dimen_minimum_del_brick_names.keys())
    idea_config_dict = get_idea_config_dict()
    idea_config_dimens = {
        idea_dimen
        for idea_dimen, dimen_config in idea_config_dict.items()
        if dimen_config.get(kw.idea_category) == kw.person
    }
    print(f"{idea_config_dimens=}")
    assert dimen_minimum_keys == idea_config_dimens
    for idea_dimen in idea_config_dimens:
        dimen_config = idea_config_dict.get(idea_dimen)
        brick_name = dimen_minimum_del_brick_names.get(idea_dimen)
        format_brickref = get_brickref_obj(brick_name)

        print(f"{idea_dimen=} {format_brickref.brick_name=}")
        dimen_args = set(dimen_config.get(kw.jkeys).keys())
        brickref_args = set(format_brickref.attributes.keys())
        change_erase_attrs(brickref_args)
        print(f"  {dimen_args=}")
        print(f"{brickref_args=}")
        assert dimen_args == brickref_args
