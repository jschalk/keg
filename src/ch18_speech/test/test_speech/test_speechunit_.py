from ch05_rope.rope import default_knot_if_None
from ch09_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_atom_args_obj_types,
)
from ch15_moment.moment_config import get_moment_args_obj_types
from ch17_jargon.jargon_config import (
    get_jargon_args_obj_types,
    jargonable_obj_types,
    get_jargonable_args,
)
from ch18_speech.yap_term import (
    labelyap_shop,
    nameyap_shop,
    ropeyap_shop,
    titleyap_shop,
)
from ch18_speech.speech_config import (
    get_speech_args_obj_types,
    # get_speech_labelterm_args,
    # get_speech_nameterm_args,
    # get_speech_ropeterm_args,
    # get_speech_titleterm_args,
    get_speechable_args,
    # set_speechable_otx_inx_args,
    speechable_obj_types,
)

# from ch18_speech.speech_main import SpeechUnit, speechunit_shop
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx


def test_get_speech_args_obj_types_ReturnsObj():
    # ESTABLISH / WHEN
    speech_args_obj_types = get_speech_args_obj_types()

    # THEN
    assert speech_args_obj_types == get_jargon_args_obj_types()


def test_speechable_obj_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_speechable_obj_types = speechable_obj_types()

    # THEN
    assert x_speechable_obj_types == jargonable_obj_types()


def test_get_speechable_args_ReturnsObj():
    # ESTABLISH / WHEN
    speechable_args = get_speechable_args()

    # THEN
    print(f"{speechable_obj_types()=}")
    assert speechable_args == get_jargonable_args()
    assert speechable_args == {
        kw.awardee_title,
        kw.person_name,
        kw.epoch_label,
        kw.spark_face,
        kw.fact_context,
        kw.fact_state,
        kw.group_title,
        kw.healer_name,
        kw.hour_label,
        kw.moment_rope,
        kw.month_label,
        kw.plan_rope,
        kw.labor_title,
        kw.reason_context,
        kw.reason_state,
        kw.contact_name,
        kw.weekday_label,
    }


# def test_set_speechable_otx_inx_args_ReturnsObj_Scenario0_All_speechable_args():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     speechable_args = get_speechable_args()

#     # WHEN
#     otx_inx_args = set_speechable_otx_inx_args(speechable_args)

#     # THEN
#     expected_otx_inx_args = set()
#     for speechable_arg in speechable_args:
#         expected_otx_inx_args.add(f"{speechable_arg}_otx")
#         expected_otx_inx_args.add(f"{speechable_arg}_inx")
#     print(f"{otx_inx_args=}")
#     assert otx_inx_args == expected_otx_inx_args


# def test_set_speechable_otx_inx_args_ReturnsObj_Scenario1_person_dimen_delete_keys():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     person_dimen_delete_keys = get_all_person_dimen_delete_keys()

#     # WHEN
#     otx_inx_args = set_speechable_otx_inx_args(person_dimen_delete_keys)

#     # THEN
#     expected_otx_inx_args = set()
#     for speechable_arg in person_dimen_delete_keys:
#         expected_otx_inx_args.add(f"{speechable_arg}_otx")
#         expected_otx_inx_args.add(f"{speechable_arg}_inx")
#     print(f"{otx_inx_args=}")
#     assert otx_inx_args == expected_otx_inx_args


# def test_set_speechable_otx_inx_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     run_str = "run"
#     given_person_dimen_delete_keys = get_all_person_dimen_delete_keys()
#     given_person_dimen_delete_keys.add(run_str)

#     # WHEN
#     otx_inx_args = set_speechable_otx_inx_args(given_person_dimen_delete_keys)

#     # THEN
#     expected_otx_inx_args = set()
#     for speechable_arg in get_all_person_dimen_delete_keys():
#         expected_otx_inx_args.add(f"{speechable_arg}_otx")
#         expected_otx_inx_args.add(f"{speechable_arg}_inx")
#     expected_otx_inx_args.add(run_str)
#     print(f"{otx_inx_args=}")
#     assert otx_inx_args == expected_otx_inx_args


# def test_set_speechable_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
#     # ESTABLISH
#     healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
#     run_str = "run"
#     given_person_dimen_delete_keys = {run_str, healer_name_ERASE_str}

#     # WHEN
#     otx_inx_args = set_speechable_otx_inx_args(given_person_dimen_delete_keys)

#     # THEN
#     healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
#     expected_otx_inx_args = {
#         f"{healer_name_ERASE_str}_otx",
#         f"{healer_name_ERASE_str}_inx",
#         run_str,
#     }
#     print(f"{otx_inx_args=}")
#     assert otx_inx_args == expected_otx_inx_args


# def test_get_speech_nameterm_args_ReturnsObj():
#     # ESTABLISH / WHEN
#     speech_NameTerm_args = get_speech_nameterm_args()

#     # THEN
#     assert speech_NameTerm_args == {
#         kw.contact_name,
#         kw.spark_face,
#         kw.healer_name,
#         kw.person_name,
#     }
#     expected_args = {
#         x_arg
#         for x_arg, obj_type in get_speech_args_obj_types().items()
#         if obj_type == kw.NameTerm
#     }
#     assert speech_NameTerm_args == expected_args


# def test_get_speech_titleterm_args_ReturnsObj():
#     # ESTABLISH / WHEN
#     speech_TitleTerm_args = get_speech_titleterm_args()

#     # THEN
#     assert speech_TitleTerm_args == {
#         kw.awardee_title,
#         kw.group_title,
#         kw.labor_title,
#     }
#     expected_args = {
#         x_arg
#         for x_arg, obj_type in get_speech_args_obj_types().items()
#         if obj_type == kw.TitleTerm
#     }
#     assert speech_TitleTerm_args == expected_args


# def test_get_speech_labelterm_args_ReturnsObj():
#     # ESTABLISH / WHEN
#     speech_LabelTerm_args = get_speech_labelterm_args()

#     # THEN
#     assert speech_LabelTerm_args == {
#         kw.hour_label,
#         kw.month_label,
#         kw.epoch_label,
#         kw.weekday_label,
#     }
#     expected_args = {
#         x_arg
#         for x_arg, obj_type in get_speech_args_obj_types().items()
#         if obj_type == kw.LabelTerm
#     }
#     assert speech_LabelTerm_args == expected_args


# def test_get_speech_ropeterm_args_ReturnsObj():
#     # ESTABLISH / WHEN
#     speech_RopeTerm_args = get_speech_ropeterm_args()

#     # THEN
#     assert speech_RopeTerm_args == {
#         kw.moment_rope,
#         kw.fact_state,
#         kw.fact_context,
#         kw.plan_rope,
#         kw.reason_context,
#         kw.reason_state,
#     }
#     expected_args = {
#         x_arg
#         for x_arg, obj_type in get_speech_args_obj_types().items()
#         if obj_type == kw.RopeTerm
#     }
#     assert speech_RopeTerm_args == expected_args


# def test_SpeechUnit_Exists():
#     # ESTABLISH
#     x_speechunit = SpeechUnit()

#     # WHEN / THEN
#     assert not x_speechunit.spark_face
#     assert not x_speechunit.spark_num
#     assert not x_speechunit.titleyap
#     assert not x_speechunit.nameyap
#     assert not x_speechunit.labelyap
#     assert not x_speechunit.ropeyap
#     assert not x_speechunit.unknown_str
#     assert not x_speechunit.otx_knot
#     assert not x_speechunit.inx_knot
#     assert set(x_speechunit.__dict__.keys()) == {
#         kw.spark_face,
#         kw.spark_num,
#         kw.titleyap,
#         kw.nameyap,
#         kw.labelyap,
#         kw.ropeyap,
#         kw.unknown_str,
#         kw.otx_knot,
#         kw.inx_knot,
#     }


# def test_speechunit_shop_ReturnsObj_Scenario0():
#     # ESTABLISH

#     # WHEN
#     sue_speechunit = speechunit_shop(exx.sue)

#     # THEN
#     assert sue_speechunit.spark_face == exx.sue
#     assert sue_speechunit.spark_num == 0
#     assert sue_speechunit.unknown_str == default_unknown_str_if_None()
#     assert sue_speechunit.otx_knot == default_knot_if_None()
#     assert sue_speechunit.inx_knot == default_knot_if_None()
#     assert sue_speechunit.titleyap == titleyap_shop(spark_face=exx.sue)
#     assert sue_speechunit.nameyap == nameyap_shop(spark_face=exx.sue)
#     assert sue_speechunit.labelyap == labelyap_shop(spark_face=exx.sue)
#     assert sue_speechunit.ropeyap == ropeyap_shop(spark_face=exx.sue)
#     assert sue_speechunit.nameyap.spark_num == 0
#     assert sue_speechunit.nameyap.unknown_str == default_unknown_str_if_None()
#     assert sue_speechunit.nameyap.otx_knot == default_knot_if_None()
#     assert sue_speechunit.nameyap.inx_knot == default_knot_if_None()
#     assert sue_speechunit.titleyap.spark_num == 0
#     assert sue_speechunit.titleyap.unknown_str == default_unknown_str_if_None()
#     assert sue_speechunit.titleyap.otx_knot == default_knot_if_None()
#     assert sue_speechunit.titleyap.inx_knot == default_knot_if_None()
#     assert sue_speechunit.labelyap.spark_num == 0
#     assert sue_speechunit.labelyap.unknown_str == default_unknown_str_if_None()
#     assert sue_speechunit.labelyap.otx_knot == default_knot_if_None()
#     assert sue_speechunit.labelyap.inx_knot == default_knot_if_None()
#     assert sue_speechunit.ropeyap.spark_num == 0
#     assert sue_speechunit.ropeyap.unknown_str == default_unknown_str_if_None()
#     assert sue_speechunit.ropeyap.otx_knot == default_knot_if_None()
#     assert sue_speechunit.ropeyap.inx_knot == default_knot_if_None()


# def test_speechunit_shop_ReturnsObj_Scenario1():
#     # ESTABLISH
#     five_spark_num = 5
#     y_uk = "UnknownTerm"
#     slash_otx_knot = "/"
#     colon_inx_knot = ":"

#     # WHEN
#     sue_speechunit = speechunit_shop(
#         spark_face=exx.sue,
#         spark_num=five_spark_num,
#         otx_knot=slash_otx_knot,
#         inx_knot=colon_inx_knot,
#         unknown_str=y_uk,
#     )

#     # THEN
#     assert sue_speechunit.spark_num == five_spark_num
#     assert sue_speechunit.unknown_str == y_uk
#     assert sue_speechunit.otx_knot == slash_otx_knot
#     assert sue_speechunit.inx_knot == colon_inx_knot

#     # x_titleyap = titleyap_shop(
#     #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
#     # )
#     # x_nameyap = nameyap_shop(
#     #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
#     # )
#     # x_ropeyap = ropeyap_shop(
#     #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, exx.sue, five_spark_num
#     # )
#     # assert sue_speechunit.titleyap == x_titleyap
#     # assert sue_speechunit.nameyap == x_nameyap
#     # assert sue_speechunit.ropeyap == x_ropeyap

#     assert sue_speechunit.nameyap.spark_face == exx.sue
#     assert sue_speechunit.nameyap.spark_num == five_spark_num
#     assert sue_speechunit.nameyap.unknown_str == y_uk
#     assert sue_speechunit.nameyap.otx_knot == slash_otx_knot
#     assert sue_speechunit.nameyap.inx_knot == colon_inx_knot
#     assert sue_speechunit.titleyap.spark_face == exx.sue
#     assert sue_speechunit.titleyap.spark_num == five_spark_num
#     assert sue_speechunit.titleyap.unknown_str == y_uk
#     assert sue_speechunit.titleyap.otx_knot == slash_otx_knot
#     assert sue_speechunit.titleyap.inx_knot == colon_inx_knot
#     assert sue_speechunit.labelyap.spark_face == exx.sue
#     assert sue_speechunit.labelyap.spark_num == five_spark_num
#     assert sue_speechunit.labelyap.unknown_str == y_uk
#     assert sue_speechunit.labelyap.otx_knot == slash_otx_knot
#     assert sue_speechunit.labelyap.inx_knot == colon_inx_knot
#     assert sue_speechunit.ropeyap.spark_face == exx.sue
#     assert sue_speechunit.ropeyap.spark_num == five_spark_num
#     assert sue_speechunit.ropeyap.unknown_str == y_uk
#     assert sue_speechunit.ropeyap.otx_knot == slash_otx_knot
#     assert sue_speechunit.ropeyap.inx_knot == colon_inx_knot


# def test_speechunit_shop_ReturnsObj_Scenario2_SpeechCoreAttrAreDefaultWhenGiven_float_nan():
#     # ESTABLISH
#     spark7 = 7
#     x_nan = float("nan")

#     # WHEN
#     x_speechunit = speechunit_shop(
#         spark_face=exx.bob,
#         spark_num=spark7,
#         unknown_str=x_nan,
#         otx_knot=x_nan,
#         inx_knot=x_nan,
#     )

#     # THEN
#     assert x_speechunit.spark_face == exx.bob
#     assert x_speechunit.spark_num == spark7
#     assert x_speechunit.unknown_str == default_unknown_str_if_None()
#     assert x_speechunit.otx_knot == default_knot_if_None()
#     assert x_speechunit.inx_knot == default_knot_if_None()
