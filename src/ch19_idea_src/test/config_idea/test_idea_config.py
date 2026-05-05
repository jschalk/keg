from ch00_py.dict_toolbox import normalize_obj
from ch00_py.file_toolbox import create_path, save_json
from ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_args_sqlite_datatype_dict,
)
from ch08_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_person_dimens,
)
from ch14_moment.moment_config import (
    get_moment_args_dimen_mapping,
    get_moment_config_dict,
    get_moment_dimens,
)
from ch15_nabu.nabu_config import (
    get_nabu_args,
    get_nabu_config_dict,
    get_nabu_dimens,
    get_nabuable_args,
)
from ch16_translate.translate_config import (
    get_translate_args_dimen_mapping,
    get_translate_config_dict,
    get_translate_dimens,
    get_translateable_args,
)
from ch17_brick.brick_config import (
    BrickFormatsEnum,
    brick_config_path,
    get_allowed_curds,
    get_brick_config_dict,
    get_brick_dimen_ref,
    get_brick_format_filename,
    get_brick_format_filenames,
    get_brick_sqlite_types,
    get_brick_types,
    get_brickref_from_file,
    get_default_sorted_list,
    get_dimens_with_brick_element,
    get_quick_bricks_column_ref,
)
from ch19_idea_src.idea_config import get_idea_config_dict, idea_config_path
from copy import copy as copy_copy
from os import getcwd as os_getcwd
from ref.keywords import Ch19Keywords as kw
from ref.sorter import get_keg_elements_sort_order


def test_idea_config_path_ReturnsObj_Brick() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch19_idea_src")
    assert idea_config_path() == create_path(chapter_dir, "idea_config.json")


def test_get_idea_config_dict_ReturnsObj_Scenario0_AllBrickTypesRepresented():
    # ESTABLISH / WHEN
    x_idea_config = get_idea_config_dict()
    config_idea_types = set(x_idea_config.keys())
    # THEN
    assert x_idea_config
    # Confirm every brick_type is mirrored
    for brick_type in get_brick_types():
        idea_type = brick_type.replace(kw.bk, kw.ii)
        # print(f""""{idea_type}": {{"brick_type": "{brick_type}"}}""")
        assert idea_type in config_idea_types
        config_dict = x_idea_config.get(idea_type)
        assert config_dict == {kw.brick_type: brick_type}


def test_get_idea_config_dict_ReturnsObj_Scenario1_NonMirrored_idea_type_Format():
    # ESTABLISH / WHEN
    x_idea_config = get_idea_config_dict()
    config_idea_types = set(x_idea_config.keys())
    mirrored_brick_types = {bt.replace(kw.bk, kw.ii) for bt in get_brick_types()}
    # THEN
    non_mirror_idea_types = config_idea_types.difference(mirrored_brick_types)
    assert non_mirror_idea_types
    # Confirm every brick_type is mirrored
    for idea_type in non_mirror_idea_types:
        print(f""""{idea_type}": """)
        assert idea_type in config_idea_types
        config_dict = x_idea_config.get(idea_type)
        config_keys = set(config_dict.keys())
        assert config_keys == {kw.brick_type, "columns", "description"}


#     # THEN
#     assert x_brick_config
#     brick_config_dimens = set(x_brick_config.keys())
#     assert kw.momentunit in brick_config_dimens
#     assert kw.moment_budunit in brick_config_dimens
#     assert kw.moment_paybook in brick_config_dimens
#     assert kw.moment_epoch_hour in brick_config_dimens
#     assert kw.moment_epoch_month in brick_config_dimens
#     assert kw.moment_epoch_weekday in brick_config_dimens
#     assert kw.moment_timeoffi in brick_config_dimens
#     assert kw.person_contact_membership in brick_config_dimens
#     assert kw.person_contactunit in brick_config_dimens
#     assert kw.person_plan_awardunit in brick_config_dimens
#     assert kw.person_plan_factunit in brick_config_dimens
#     assert kw.person_plan_laborunit in brick_config_dimens
#     assert kw.person_plan_healerunit in brick_config_dimens
#     assert kw.person_plan_reason_caseunit in brick_config_dimens
#     assert kw.person_plan_reasonunit in brick_config_dimens
#     assert kw.person_planunit in brick_config_dimens
#     assert kw.personunit in brick_config_dimens
#     assert kw.nabu_timenum in brick_config_dimens
#     assert kw.translate_name in brick_config_dimens
#     assert kw.translate_title in brick_config_dimens
#     assert kw.translate_label in brick_config_dimens
#     assert kw.translate_rope in brick_config_dimens
#     assert get_person_dimens().issubset(brick_config_dimens)
#     assert get_moment_dimens().issubset(brick_config_dimens)
#     assert get_nabu_dimens().issubset(brick_config_dimens)
#     assert get_translate_dimens().issubset(brick_config_dimens)
#     gen_all_dimens = get_person_dimens()
#     gen_all_dimens.update(get_moment_dimens())
#     gen_all_dimens.update(get_nabu_dimens())
#     gen_all_dimens.update(get_translate_dimens())
#     assert gen_all_dimens == brick_config_dimens
#     assert len(x_brick_config) == 22
#     _validate_brick_config(x_brick_config)


# def get_brick_categorys():
#     return {kw.person, kw.moment, kw.translate, kw.nabu}


# def _validate_brick_config(x_brick_config: dict):
#     # sourcery skip: low-code-quality
#     atom_config_dict = get_atom_config_dict()
#     moment_config_dict = get_moment_config_dict()
#     nabu_config_dict = get_nabu_config_dict()
#     translate_config_dict = get_translate_config_dict()
#     # for every brick_format file there exists a unique brick_type with leading zeros to make 5 digits
#     for brick_dimen, brick_dict in x_brick_config.items():
#         print(f"{brick_dimen=}")
#         assert brick_dict.get(kw.brick_category) in get_brick_categorys()
#         assert brick_dict.get(kw.jkeys) is not None
#         assert brick_dict.get(kw.jvalues) is not None
#         assert brick_dict.get(kw.allowed_crud) is not None
#         assert brick_dict.get(kw.UPDATE) is None
#         assert brick_dict.get(kw.INSERT) is None
#         assert brick_dict.get(kw.DELETE) is None
#         assert brick_dict.get(kw.normal_specs) is None
#         if brick_dict.get(kw.brick_category) == kw.person:
#             sub_dimen = atom_config_dict.get(brick_dimen)
#         elif brick_dict.get(kw.brick_category) == kw.moment:
#             sub_dimen = moment_config_dict.get(brick_dimen)
#         elif brick_dict.get(kw.brick_category) == kw.nabu:
#             sub_dimen = nabu_config_dict.get(brick_dimen)
#         elif brick_dict.get(kw.brick_category) == kw.translate:
#             sub_dimen = translate_config_dict.get(brick_dimen)

#         assert brick_dict.get(kw.allowed_crud) in get_allowed_curds()

#         UPDATE_dimen = sub_dimen.get(kw.UPDATE)
#         INSERT_dimen = sub_dimen.get(kw.INSERT)
#         DELETE_dimen = sub_dimen.get(kw.DELETE)
#         brick_allowed_crud = brick_dict.get(kw.allowed_crud)
#         # print(
#         #     f"{brick_dimen=} {UPDATE_dimen} {INSERT_dimen} {DELETE_dimen=} {brick_allowed_crud=}"
#         # )
#         if brick_dimen in {
#             kw.moment_epoch_hour,
#             kw.moment_epoch_month,
#             kw.moment_epoch_weekday,
#             kw.momentunit,
#             "map_otx2inx",
#             kw.nabu_timenum,
#             kw.translate_title,
#             kw.translate_name,
#             kw.translate_label,
#             kw.translate_rope,
#         }:
#             assert brick_allowed_crud == kw.insert_one_time
#         elif brick_dimen in {kw.moment_budunit, kw.moment_paybook, kw.moment_timeoffi}:
#             assert brick_allowed_crud == kw.insert_multiple
#         elif UPDATE_dimen != None and INSERT_dimen != None and DELETE_dimen != None:
#             assert brick_allowed_crud == kw.delete_insert_update
#         elif UPDATE_dimen != None and INSERT_dimen != None and DELETE_dimen is None:
#             assert brick_allowed_crud == kw.insert_update
#         elif UPDATE_dimen is None and INSERT_dimen != None and DELETE_dimen != None:
#             assert brick_allowed_crud == kw.delete_insert
#         elif UPDATE_dimen != None and INSERT_dimen is None and DELETE_dimen != None:
#             assert brick_allowed_crud == kw.delete_update
#         elif UPDATE_dimen != None and INSERT_dimen is None and DELETE_dimen is None:
#             assert brick_allowed_crud == kw.UPDATE
#         elif UPDATE_dimen is None and INSERT_dimen != None and DELETE_dimen is None:
#             assert brick_allowed_crud == kw.INSERT
#         elif UPDATE_dimen is None and INSERT_dimen is None and DELETE_dimen != None:
#             assert brick_allowed_crud == kw.DELETE
#         else:
#             assert brick_allowed_crud == f"{kw.allowed_crud} not checked by test"

#         sub_jkeys_keys = set(sub_dimen.get(kw.jkeys).keys())
#         brick_jkeys_keys = set(brick_dict.get(kw.jkeys).keys())
#         # print(f"   {sub_jkeys_keys=}")
#         # print(f"  {brick_jkeys_keys=}")
#         assert kw.spark_face in brick_jkeys_keys
#         assert kw.spark_num in brick_jkeys_keys
#         if brick_dict.get(kw.brick_category) in {kw.person} and kw.plan in brick_dimen:
#             assert kw.moment_rope not in brick_jkeys_keys, brick_dimen
#         elif brick_dict.get(kw.brick_category) in {kw.moment, kw.person}:
#             assert kw.moment_rope in brick_jkeys_keys
#             # print(f"2{brick_dimen=}")
#             if brick_dict.get(kw.brick_category) in {kw.person}:
#                 brick_jkeys_keys.remove(kw.moment_rope)
#         if brick_dict.get(kw.brick_category) in {kw.person}:
#             brick_jkeys_keys.remove(kw.person_name)
#         brick_jkeys_keys.remove(kw.spark_face)
#         brick_jkeys_keys.remove(kw.spark_num)
#         assertion_failure_str = f"{brick_dimen=} {sub_jkeys_keys=} {brick_jkeys_keys=}"
#         assert sub_jkeys_keys == brick_jkeys_keys, assertion_failure_str

#         expected_jvalues_keys = set(sub_dimen.get(kw.jvalues).keys())
#         # all moment and plan dimen must have knot jvalue because they all have rope keys
#         if brick_dict.get(kw.brick_category) in {kw.moment, kw.person}:
#             expected_jvalues_keys.add(kw.knot)
#         # print(f"{brick_dimen=}")
#         # if kw.moment_rope in expected_jvalues_keys:
#         #     expected_jvalues_keys.remove(kw.moment_rope)

#         brick_jvalues_dict = brick_dict.get(kw.jvalues)
#         brick_jvalues_keys = set(brick_jvalues_dict.keys())
#         # print(f" {expected_jvalues_keys=}")
#         # print(f"{brick_jvalues_keys=}")
#         assert expected_jvalues_keys == brick_jvalues_keys


# def test_get_brick_format_filenames_ReturnsObj_CheckSome_brick_format_filesnames_Exist():
#     # ESTABLISH
#     brick_filenames_set = get_brick_format_filenames()

#     # WHEN / THEN
#     ifx = BrickFormatsEnum
#     assert ifx.bk00121_person_contactunit_v0_0_0 in brick_filenames_set
#     assert ifx.bk00120_person_contact_membership_v0_0_0 in brick_filenames_set
#     assert ifx.bk00002_planunit_v0_0_0 in brick_filenames_set


# def change_erase_attrs(brick_attrs: set):
#     brick_attrs_list = get_default_sorted_list(brick_attrs)
#     if brick_attrs_list[-1].find("_ERASE") > 0:
#         delete_attr_with_erase = brick_attrs_list[-1]
#         delete_attr_without_erase = delete_attr_with_erase.replace("_ERASE", "")
#         brick_attrs.remove(delete_attr_with_erase)
#         brick_attrs.add(delete_attr_without_erase)


# def test_get_brick_format_filenames_ReturnsObj_Validate_brick_format_files():
#     # sourcery skip:  no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     brick_filenames_sorted = list(get_brick_format_filenames())

#     # THEN
#     brick_filenames_sorted.sort(key=lambda x: x)
#     print(f"{len(brick_filenames_sorted)=}")

#     all_dimen_keys_dict = {
#         dimen: set(dict.get(kw.jkeys).keys())
#         for dimen, dict in get_brick_config_dict().items()
#     }

#     valid_brick_dimens = set()
#     valid_brick_dimens.update(get_person_dimens())
#     valid_brick_dimens.update(get_moment_dimens())
#     valid_brick_dimens.update(get_nabu_dimens())
#     valid_brick_dimens.update(get_translate_dimens())
#     print("get_brick_config_dict")
#     config_dict = get_brick_config_dict()

#     # for every brick_format file there exists a unique brick_type with leading zeros to make 5 digits
#     brick_types_set = set()
#     for brick_filename in brick_filenames_sorted:
#         ref_dict = get_brickref_from_file(brick_filename)
#         # print(f"{brick_filename=} {ref_dict.get(kw.brick_type)=}")
#         brick_type_value = ref_dict.get(kw.brick_type)
#         assert brick_type_value
#         assert brick_type_value[2:8] == brick_filename[2:7]
#         brick_types_set.add(brick_type_value)

#         format_dimens = ref_dict.get(kw.dimens)
#         assert format_dimens is not None
#         assert len(format_dimens) > 0
#         for brick_format_dimen in format_dimens:
#             assert brick_format_dimen in valid_brick_dimens

#         assert ref_dict.get(kw.attributes)
#         brick_format_attributes = ref_dict.get(kw.attributes)
#         for brick_attribute, attr_dict in brick_format_attributes.items():
#             # print(f"{brick_attribute=}")
#             assert kw.otx_key in set(attr_dict.keys())
#             otx_key_value = attr_dict.get(kw.otx_key)
#             for brick_format_dimen in format_dimens:
#                 format_config = config_dict.get(brick_format_dimen)
#                 dimen_required_attrs = set(format_config.get(kw.jkeys).keys())
#                 dimen_optional_attrs = set(format_config.get(kw.jvalues).keys())
#                 attr_in_required = brick_attribute in dimen_required_attrs
#                 attr_in_optional = brick_attribute in dimen_optional_attrs
#                 attr_in_keys = attr_in_required or attr_in_optional
#                 assert_fail_str = (
#                     f"{brick_format_dimen=} {brick_attribute=} {otx_key_value=}"
#                 )
#                 if attr_in_keys and otx_key_value:
#                     assert attr_in_required, assert_fail_str
#                 elif attr_in_keys:
#                     assert attr_in_optional, assert_fail_str
#         # check all implied dimens are there
#         brick_attrs = set(ref_dict.get(kw.attributes).keys())
#         change_erase_attrs(brick_attrs)

#         for x_dimen, dimen_keys in all_dimen_keys_dict.items():
#             # if x_dimen == kw.person_plan_factunit and x_dimen in format_dimens:
#             #     print(f"{brick_type_value}  {x_dimen=} {brick_attrs_list=}")
#             if dimen_keys.issubset(brick_attrs):
#                 if x_dimen not in format_dimens:
#                     print(f"MISSING {x_dimen=} {brick_type_value} {brick_attrs=}")
#                 assert x_dimen in format_dimens
#             else:
#                 # dimen_keys_list = get_default_sorted_list(dimen_keys)
#                 #     brick_attrs_list[-1] = brick_attrs_list[-1].removesuffix("_ERASE")
#                 #     brick_attrs = set(brick_attrs_list)
#                 if x_dimen in format_dimens:
#                     print(
#                         f"SHOULDNT BE {x_dimen=} {brick_type_value} : {get_default_sorted_list(brick_attrs)}"
#                     )
#                     # print(
#                     #     f"SHOULDNT BE {x_dimen=} {brick_type_value} : {get_default_sorted_list(dimen_keys)}"
#                     # )
#                 assert x_dimen not in format_dimens

#     # assert kw.spark_face in brick_format_attributes
#     # assert kw.spark_num in brick_format_attributes

#     # confirm every bricknumber is unique
#     assert len(brick_types_set) == len(brick_filenames_sorted)
#     assert brick_types_set == get_brick_types()


# def test_get_brick_format_filename_ReturnsObj():
#     # ESTABLISH
#     bk00121_str = "bk00121"
#     bk00120_str = "bk00120"
#     bk00002_str = "bk00002"

#     # WHEN
#     bk00121_filename = get_brick_format_filename(bk00121_str)
#     bk00120_filename = get_brick_format_filename(bk00120_str)
#     bk00002_filename = get_brick_format_filename(bk00002_str)

#     # THEN
#     ifx = BrickFormatsEnum
#     assert bk00121_filename == ifx.bk00121_person_contactunit_v0_0_0
#     assert bk00120_filename == ifx.bk00120_person_contact_membership_v0_0_0
#     assert bk00002_filename == ifx.bk00002_planunit_v0_0_0

#     all_set = {
#         get_brick_format_filename(brick_type) for brick_type in get_brick_types()
#     }
#     assert all_set == get_brick_format_filenames()


# def set_brick_config_json(dimen: str, build_order: int):
#     x_brick_config = get_brick_config_dict()
#     dimen_dict = x_brick_config.get(dimen)
#     dimen_dict[kw.build_order] = build_order
#     x_brick_config[dimen] = dimen_dict
#     save_json(brick_config_path(), None, x_brick_config)


# def test_get_brick_config_dict_ReturnsObj_Scenario1_Check_build_order():
#     # ESTABLISH / WHEN
#     bo = kw.build_order
#     # set_brick_config_json(kw.translate_name, 0)
#     # set_brick_config_json(kw.translate_title, 1)
#     # set_brick_config_json(kw.translate_label, 2)
#     # set_brick_config_json(kw.translate_rope, 3)
#     # set_brick_config_json(kw.momentunit, 5)
#     # set_brick_config_json(kw.moment_epoch_hour, 6)
#     # set_brick_config_json(kw.moment_epoch_month, 7)
#     # set_brick_config_json(kw.moment_epoch_weekday, 8)
#     # set_brick_config_json(kw.person_contact_membership, 9)
#     # set_brick_config_json(kw.person_contactunit, 10)
#     # set_brick_config_json(kw.person_plan_awardunit, 11)
#     # set_brick_config_json(kw.person_plan_factunit, 12)
#     # set_brick_config_json(kw.person_plan_laborunit, 14)
#     # set_brick_config_json(kw.person_plan_healerunit, 15)
#     # set_brick_config_json(kw.person_plan_reason_caseunit, 16)
#     # set_brick_config_json(kw.person_plan_reasonunit, 17)
#     # set_brick_config_json(kw.person_planunit, 18)
#     # set_brick_config_json(kw.personunit, 19)
#     # set_brick_config_json(kw.moment_budunit, 20)
#     # set_brick_config_json(kw.moment_paybook, 21)

#     x_brick_config = get_brick_config_dict()

#     # THEN
#     assert x_brick_config.get(kw.translate_name).get(bo) == 0
#     assert x_brick_config.get(kw.translate_title).get(bo) == 1
#     assert x_brick_config.get(kw.translate_label).get(bo) == 2
#     assert x_brick_config.get(kw.translate_rope).get(bo) == 3
#     assert x_brick_config.get(kw.nabu_timenum).get(bo) == 4
#     assert x_brick_config.get(kw.momentunit).get(bo) == 5
#     assert x_brick_config.get(kw.moment_epoch_hour).get(bo) == 6
#     assert x_brick_config.get(kw.moment_epoch_month).get(bo) == 7
#     assert x_brick_config.get(kw.moment_epoch_weekday).get(bo) == 8
#     assert x_brick_config.get(kw.person_contact_membership).get(bo) == 9
#     assert x_brick_config.get(kw.person_contactunit).get(bo) == 10
#     assert x_brick_config.get(kw.person_plan_awardunit).get(bo) == 11
#     assert x_brick_config.get(kw.person_plan_factunit).get(bo) == 12
#     assert x_brick_config.get(kw.person_plan_laborunit).get(bo) == 14
#     assert x_brick_config.get(kw.person_plan_healerunit).get(bo) == 15
#     assert x_brick_config.get(kw.person_plan_reason_caseunit).get(bo) == 16
#     assert x_brick_config.get(kw.person_plan_reasonunit).get(bo) == 17
#     assert x_brick_config.get(kw.person_planunit).get(bo) == 18
#     assert x_brick_config.get(kw.personunit).get(bo) == 19
#     assert x_brick_config.get(kw.moment_budunit).get(bo) == 20
#     assert x_brick_config.get(kw.moment_paybook).get(bo) == 21
#     assert x_brick_config.get(kw.moment_timeoffi).get(bo) == 22
#     builder_order_dict = {}
#     for dimen_key, dimen_dict in x_brick_config.items():
#         dimen_builder_order = dimen_dict.get(bo)
#         assert dimen_builder_order is not None
#         print(
#             f"{dimen_key:30} build order: {dimen_builder_order:2} {sorted(builder_order_dict.keys())=}"
#         )
#         assert not builder_order_dict.get(dimen_builder_order)
#         builder_order_dict[dimen_builder_order] = dimen_key
#     print(f"{sorted(builder_order_dict.keys())=}")


# def test_get_brick_config_dict_ReturnsObj_Scenario2_Person():
#     # ESTABLISH / WHEN
#     person_brick_config = get_brick_config_dict(kw.person)

#     # THEN
#     assert not person_brick_config.get(kw.translate_name)
#     assert not person_brick_config.get(kw.translate_title)
#     assert not person_brick_config.get(kw.translate_label)
#     assert not person_brick_config.get(kw.translate_rope)
#     assert not person_brick_config.get(kw.nabu_timenum)
#     assert not person_brick_config.get(kw.momentunit)
#     assert not person_brick_config.get(kw.moment_epoch_hour)
#     assert not person_brick_config.get(kw.moment_epoch_month)
#     assert not person_brick_config.get(kw.moment_epoch_weekday)
#     assert person_brick_config.get(kw.person_contact_membership)
#     assert person_brick_config.get(kw.person_contactunit)
#     assert person_brick_config.get(kw.person_plan_awardunit)
#     assert person_brick_config.get(kw.person_plan_factunit)
#     assert person_brick_config.get(kw.person_plan_laborunit)
#     assert person_brick_config.get(kw.person_plan_healerunit)
#     assert person_brick_config.get(kw.person_plan_reason_caseunit)
#     assert person_brick_config.get(kw.person_plan_reasonunit)
#     assert person_brick_config.get(kw.person_planunit)
#     assert person_brick_config.get(kw.personunit)
#     assert not person_brick_config.get(kw.moment_budunit)
#     assert not person_brick_config.get(kw.moment_paybook)
#     assert not person_brick_config.get(kw.moment_timeoffi)


# def test_get_brick_config_dict_ReturnsObj_Scenario3_CountDimens():
#     # ESTABLISH / WHEN / THEN
#     assert len(get_brick_config_dict(brick_categorys={kw.person})) == 10
#     assert len(get_brick_config_dict(brick_categorys={kw.moment})) == 7
#     assert len(get_brick_config_dict(brick_categorys={kw.nabu})) == 1
#     assert len(get_brick_config_dict(brick_categorys={kw.translate})) == 4
#     assert len(get_brick_config_dict({kw.nabu, kw.translate})) == 5


# def test_get_quick_bricks_column_ref_ReturnsObj():
#     # ESTABLISH / WHEN
#     x_brick_quick_column_ref = get_quick_bricks_column_ref()

#     # THEN
#     assert len(x_brick_quick_column_ref) == len(get_brick_types())
#     assert x_brick_quick_column_ref.get("bk00100") == {
#         kw.spark_num,
#         kw.spark_face,
#         kw.c400_number,
#         kw.moment_rope,
#         kw.fund_grain,
#         kw.monthday_index,
#         kw.mana_grain,
#         kw.respect_grain,
#         kw.knot,
#         kw.epoch_label,
#         kw.yr1_jan1_offset,
#         kw.job_listen_rotations,
#     }


# def _create_expected_brick_dimen_ref() -> dict[str, list[str]]:
#     brick_types_sorted = list(get_brick_types())
#     brick_types_sorted.sort(key=lambda x: x)
#     expected_brick_dimen_ref = {}
#     for brick_type in brick_types_sorted:
#         brick_format_filename = get_brick_format_filename(brick_type)
#         x_brickref = get_brickref_from_file(brick_format_filename)
#         dimens_list = x_brickref.get(kw.dimens)
#         for x_dimen in dimens_list:
#             if expected_brick_dimen_ref.get(x_dimen) is None:
#                 expected_brick_dimen_ref[x_dimen] = {brick_type}
#             else:
#                 expected_brick_dimen_ref.get(x_dimen).add(brick_type)
#     return expected_brick_dimen_ref


# def print_sorted(obj, indent=0):
#     """Pretty-print dictionaries with sorted keys and sets printed in sorted order."""
#     space = " " * indent

#     if isinstance(obj, dict):
#         print(space + "{")
#         for key in sorted(obj):
#             print(f"{space}  {repr(key)}: ", end="")
#             print_sorted(obj[key], indent + 4)
#         print(space + "}")

#     elif isinstance(obj, set):
#         # print set elements in sorted order but keep set notation
#         items = sorted(obj)
#         print(space + "{" + ", ".join(repr(x) for x in items) + "}")

#     elif isinstance(obj, (list, tuple)):
#         open_c, close_c = ("[", "]") if isinstance(obj, list) else ("(", ")")
#         print(space + open_c)
#         for item in obj:
#             print_sorted(item, indent + 4)
#         print(space + close_c)

#     else:
#         print(space + repr(obj))


# def test_get_brick_dimen_ref_ReturnsObj():
#     # ESTABLISH
#     expected_brick_dimen_ref = _create_expected_brick_dimen_ref()
#     # print(f"{expected_brick_dimen_ref=}")
#     print_sorted(normalize_obj(expected_brick_dimen_ref))

#     # WHEN / THEN
#     assert get_brick_dimen_ref() == expected_brick_dimen_ref


# def test_get_dimens_with_brick_element_ReturnsObj_Scenario0_offi_time():
#     # ESTABLISH / WHEN / THEN
#     assert get_dimens_with_brick_element(kw.offi_time) == {kw.moment_timeoffi}
