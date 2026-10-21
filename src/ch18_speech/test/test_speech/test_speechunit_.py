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
    get_jargon_labelterm_args,
    get_jargon_nameterm_args,
    get_jargon_ropeterm_args,
    get_jargon_titleterm_args,
)
from ch18_speech.yap_term import (
    labelyap_shop,
    nameyap_shop,
    ropeyap_shop,
    titleyap_shop,
)
from ch18_speech.speech_config import (
    get_speech_args_obj_types,
    get_speech_labelterm_args,
    get_speech_nameterm_args,
    get_speech_ropeterm_args,
    get_speech_titleterm_args,
    get_speechable_args,
    set_speechable_iux_aux_args,
    speechable_obj_types,
)
from ch18_speech.speech_main import SpeechUnit, speechunit_shop
from ch99_glossary.ch_keyword import Ch18Keywords as kw, ExampleStrs as exx


def test_get_speech_args_obj_types_ReturnsObj():
    # ESTABLISH / WHEN
    speech_args_obj_types = get_speech_args_obj_types()

    # THEN
    expected_speech_args_obj_types = get_jargon_args_obj_types()
    expected_speech_args_obj_types.pop(kw.spark_face)
    expected_speech_args_obj_types[kw.flare_audie] = kw.TitleTerm
    assert speech_args_obj_types == expected_speech_args_obj_types


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
    # assert speechable_args == get_jargonable_args()
    assert speechable_args == {
        kw.awardee_title,
        kw.person_name,
        kw.epoch_label,
        kw.flare_audie,
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


def test_set_speechable_iux_aux_args_ReturnsObj_Scenario0_All_speechable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    speechable_args = get_speechable_args()

    # WHEN
    iux_aux_args = set_speechable_iux_aux_args(speechable_args)

    # THEN
    expected_iux_aux_args = set()
    for speechable_arg in speechable_args:
        expected_iux_aux_args.add(f"{speechable_arg}_iux")
        expected_iux_aux_args.add(f"{speechable_arg}_aux")
    print(f"{iux_aux_args=}")
    assert iux_aux_args == expected_iux_aux_args


def test_set_speechable_iux_aux_args_ReturnsObj_Scenario1_person_dimen_delete_keys():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    person_dimen_delete_keys = get_all_person_dimen_delete_keys()

    # WHEN
    iux_aux_args = set_speechable_iux_aux_args(person_dimen_delete_keys)

    # THEN
    expected_iux_aux_args = set()
    for speechable_arg in person_dimen_delete_keys:
        expected_iux_aux_args.add(f"{speechable_arg}_iux")
        expected_iux_aux_args.add(f"{speechable_arg}_aux")
    print(f"{iux_aux_args=}")
    assert iux_aux_args == expected_iux_aux_args


def test_set_speechable_iux_aux_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    given_person_dimen_delete_keys = get_all_person_dimen_delete_keys()
    given_person_dimen_delete_keys.add(run_str)

    # WHEN
    iux_aux_args = set_speechable_iux_aux_args(given_person_dimen_delete_keys)

    # THEN
    expected_iux_aux_args = set()
    for speechable_arg in get_all_person_dimen_delete_keys():
        expected_iux_aux_args.add(f"{speechable_arg}_iux")
        expected_iux_aux_args.add(f"{speechable_arg}_aux")
    expected_iux_aux_args.add(run_str)
    print(f"{iux_aux_args=}")
    assert iux_aux_args == expected_iux_aux_args


def test_set_speechable_iux_aux_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    run_str = "run"
    given_person_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    iux_aux_args = set_speechable_iux_aux_args(given_person_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    expected_iux_aux_args = {
        f"{healer_name_ERASE_str}_iux",
        f"{healer_name_ERASE_str}_aux",
        run_str,
    }
    print(f"{iux_aux_args=}")
    assert iux_aux_args == expected_iux_aux_args


def test_get_speech_nameterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    speech_NameTerm_args = get_speech_nameterm_args()

    # THEN
    assert speech_NameTerm_args == {
        kw.contact_name,
        kw.healer_name,
        kw.person_name,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_speech_args_obj_types().items()
        if obj_type == kw.NameTerm
    }
    assert speech_NameTerm_args == expected_args


def test_get_speech_titleterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    speech_TitleTerm_args = get_speech_titleterm_args()

    # THEN
    assert speech_TitleTerm_args == {
        kw.flare_audie,
        kw.awardee_title,
        kw.group_title,
        kw.labor_title,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_speech_args_obj_types().items()
        if obj_type == kw.TitleTerm
    }
    assert speech_TitleTerm_args == expected_args


def test_get_speech_labelterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    speech_LabelTerm_args = get_speech_labelterm_args()

    # THEN
    assert speech_LabelTerm_args == {
        kw.hour_label,
        kw.month_label,
        kw.epoch_label,
        kw.weekday_label,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_speech_args_obj_types().items()
        if obj_type == kw.LabelTerm
    }
    assert speech_LabelTerm_args == expected_args


def test_get_speech_ropeterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    speech_RopeTerm_args = get_speech_ropeterm_args()

    # THEN
    assert speech_RopeTerm_args == {
        kw.moment_rope,
        kw.fact_state,
        kw.fact_context,
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_speech_args_obj_types().items()
        if obj_type == kw.RopeTerm
    }
    assert speech_RopeTerm_args == expected_args


def test_SpeechUnit_Exists():
    # ESTABLISH
    x_speechunit = SpeechUnit()

    # WHEN / THEN
    assert not x_speechunit.flare_audie
    assert not x_speechunit.flare_num
    assert not x_speechunit.titleyap
    assert not x_speechunit.nameyap
    assert not x_speechunit.labelyap
    assert not x_speechunit.ropeyap
    assert not x_speechunit.iux_knot
    assert not x_speechunit.aux_knot
    print(f"{set(x_speechunit.__dict__.keys())=}")
    assert set(x_speechunit.__dict__.keys()) == {
        kw.flare_audie,
        kw.flare_num,
        kw.titleyap,
        kw.nameyap,
        kw.labelyap,
        kw.ropeyap,
        kw.iux_knot,
        kw.aux_knot,
    }


def test_speechunit_shop_ReturnsObj_Scenario0():
    # ESTABLISH

    # WHEN
    sue_speechunit = speechunit_shop(exx.sue)

    # THEN
    assert sue_speechunit.flare_audie == exx.sue
    assert sue_speechunit.flare_num == 0
    assert sue_speechunit.iux_knot == default_knot_if_None()
    assert sue_speechunit.aux_knot == default_knot_if_None()
    assert sue_speechunit.titleyap == titleyap_shop(flare_audie=exx.sue)
    assert sue_speechunit.nameyap == nameyap_shop(flare_audie=exx.sue)
    assert sue_speechunit.labelyap == labelyap_shop(flare_audie=exx.sue)
    assert sue_speechunit.ropeyap == ropeyap_shop(flare_audie=exx.sue)
    assert sue_speechunit.nameyap.flare_num == 0
    assert sue_speechunit.nameyap.iux_knot == default_knot_if_None()
    assert sue_speechunit.nameyap.aux_knot == default_knot_if_None()
    assert sue_speechunit.titleyap.flare_num == 0
    assert sue_speechunit.titleyap.iux_knot == default_knot_if_None()
    assert sue_speechunit.titleyap.aux_knot == default_knot_if_None()
    assert sue_speechunit.labelyap.flare_num == 0
    assert sue_speechunit.labelyap.iux_knot == default_knot_if_None()
    assert sue_speechunit.labelyap.aux_knot == default_knot_if_None()
    assert sue_speechunit.ropeyap.flare_num == 0
    assert sue_speechunit.ropeyap.iux_knot == default_knot_if_None()
    assert sue_speechunit.ropeyap.aux_knot == default_knot_if_None()


def test_speechunit_shop_ReturnsObj_Scenario1():
    # ESTABLISH
    five_flare_num = 5
    slash_iux_knot = "/"
    colon_aux_knot = ":"

    # WHEN
    sue_speechunit = speechunit_shop(
        flare_audie=exx.sue,
        flare_num=five_flare_num,
        iux_knot=slash_iux_knot,
        aux_knot=colon_aux_knot,
    )

    # THEN
    assert sue_speechunit.flare_num == five_flare_num
    assert sue_speechunit.iux_knot == slash_iux_knot
    assert sue_speechunit.aux_knot == colon_aux_knot

    # x_titleyap = titleyap_shop(
    #     slash_iux_knot, colon_aux_knot, {}, y_uk, exx.sue, five_flare_num
    # )
    # x_nameyap = nameyap_shop(
    #     slash_iux_knot, colon_aux_knot, {}, y_uk, exx.sue, five_flare_num
    # )
    # x_ropeyap = ropeyap_shop(
    #     slash_iux_knot, colon_aux_knot, None, {}, y_uk, exx.sue, five_flare_num
    # )
    # assert sue_speechunit.titleyap == x_titleyap
    # assert sue_speechunit.nameyap == x_nameyap
    # assert sue_speechunit.ropeyap == x_ropeyap

    assert sue_speechunit.nameyap.flare_audie == exx.sue
    assert sue_speechunit.nameyap.flare_num == five_flare_num
    assert sue_speechunit.nameyap.iux_knot == slash_iux_knot
    assert sue_speechunit.nameyap.aux_knot == colon_aux_knot
    assert sue_speechunit.titleyap.flare_audie == exx.sue
    assert sue_speechunit.titleyap.flare_num == five_flare_num
    assert sue_speechunit.titleyap.iux_knot == slash_iux_knot
    assert sue_speechunit.titleyap.aux_knot == colon_aux_knot
    assert sue_speechunit.labelyap.flare_audie == exx.sue
    assert sue_speechunit.labelyap.flare_num == five_flare_num
    assert sue_speechunit.labelyap.iux_knot == slash_iux_knot
    assert sue_speechunit.labelyap.aux_knot == colon_aux_knot
    assert sue_speechunit.ropeyap.flare_audie == exx.sue
    assert sue_speechunit.ropeyap.flare_num == five_flare_num
    assert sue_speechunit.ropeyap.iux_knot == slash_iux_knot
    assert sue_speechunit.ropeyap.aux_knot == colon_aux_knot


def test_speechunit_shop_ReturnsObj_Scenario2_SpeechCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    flare7 = 7
    x_nan = float("nan")

    # WHEN
    x_speechunit = speechunit_shop(
        flare_audie=exx.bob,
        flare_num=flare7,
        iux_knot=x_nan,
        aux_knot=x_nan,
    )

    # THEN
    assert x_speechunit.flare_audie == exx.bob
    assert x_speechunit.flare_num == flare7
    assert x_speechunit.iux_knot == default_knot_if_None()
    assert x_speechunit.aux_knot == default_knot_if_None()
