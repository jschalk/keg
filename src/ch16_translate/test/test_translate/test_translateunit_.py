from src.ch04_rope.rope import default_knot_if_None
from src.ch08_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_atom_args_class_types,
)
from src.ch14_moment.moment_config import get_moment_args_class_types
from src.ch16_translate.map_term import (
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.ch16_translate.translate_config import (
    default_unknown_str_if_None,
    get_translate_args_class_types,
    get_translate_labelterm_args,
    get_translate_nameterm_args,
    get_translate_ropeterm_args,
    get_translate_titleterm_args,
    get_translateable_args,
    set_translateable_otx_inx_args,
    translateable_class_types,
)
from src.ch16_translate.translate_main import TranslateUnit, translateunit_shop
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_get_translate_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    translate_args_class_types = get_translate_args_class_types()

    # THEN
    assert translate_args_class_types.get(kw.partner_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.addin) == "float"
    assert translate_args_class_types.get(kw.amount) == "float"
    assert translate_args_class_types.get(kw.awardee_title) == kw.TitleTerm
    assert translate_args_class_types.get(kw.reason_context) == kw.RopeTerm
    assert translate_args_class_types.get(kw.active_requisite) == "bool"
    assert translate_args_class_types.get(kw.begin) == "float"
    assert translate_args_class_types.get(kw.c400_number) == "int"
    assert translate_args_class_types.get(kw.close) == "float"
    assert translate_args_class_types.get(kw.partner_cred_lumen) == "float"
    assert translate_args_class_types.get(kw.group_cred_lumen) == "float"
    assert translate_args_class_types.get(kw.credor_respect) == "float"
    assert translate_args_class_types.get(kw.cumulative_day) == "int"
    assert translate_args_class_types.get(kw.cumulative_minute) == "int"
    assert translate_args_class_types.get(kw.partner_debt_lumen) == "float"
    assert translate_args_class_types.get(kw.group_debt_lumen) == "float"
    assert translate_args_class_types.get(kw.debtor_respect) == "float"
    assert translate_args_class_types.get(kw.denom) == "int"
    assert translate_args_class_types.get(kw.reason_divisor) == "int"
    assert translate_args_class_types.get(kw.face_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.fact_context) == kw.RopeTerm
    assert translate_args_class_types.get(kw.moment_rope) == kw.RopeTerm
    assert translate_args_class_types.get(kw.fact_upper) == kw.FactNum
    assert translate_args_class_types.get(kw.fact_lower) == kw.FactNum
    assert translate_args_class_types.get(kw.fund_grain) == "float"
    assert translate_args_class_types.get(kw.fund_pool) == "float"
    assert translate_args_class_types.get(kw.give_force) == "float"
    assert translate_args_class_types.get(kw.gogo_want) == "float"
    assert translate_args_class_types.get(kw.group_title) == kw.TitleTerm
    assert translate_args_class_types.get(kw.healer_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.hour_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.star) == "int"
    assert translate_args_class_types.get(kw.max_tree_traverse) == "int"
    assert translate_args_class_types.get(kw.month_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.monthday_index) == "int"
    assert translate_args_class_types.get(kw.morph) == "bool"
    assert translate_args_class_types.get(kw.reason_state) == kw.RopeTerm
    assert translate_args_class_types.get(kw.reason_upper) == kw.ReasonNum
    assert translate_args_class_types.get(kw.numor) == "int"
    assert translate_args_class_types.get(kw.offi_time) == kw.TimeNum
    assert translate_args_class_types.get(kw.person_name) == kw.NameTerm
    assert translate_args_class_types.get(kw.reason_lower) == kw.ReasonNum
    assert translate_args_class_types.get(kw.mana_grain) == "float"
    assert translate_args_class_types.get(kw.fact_state) == kw.RopeTerm
    assert translate_args_class_types.get(kw.pledge) == "bool"
    assert translate_args_class_types.get(kw.problem_bool) == "bool"
    assert translate_args_class_types.get(kw.quota) == "int"
    assert translate_args_class_types.get(kw.respect_grain) == "float"
    assert translate_args_class_types.get(kw.plan_rope) == kw.RopeTerm
    assert translate_args_class_types.get(kw.celldepth) == "int"
    assert translate_args_class_types.get(kw.stop_want) == "float"
    assert translate_args_class_types.get(kw.take_force) == "float"
    assert translate_args_class_types.get(kw.labor_title) == kw.TitleTerm
    assert translate_args_class_types.get(kw.bud_time) == kw.TimeNum
    assert translate_args_class_types.get(kw.tran_time) == kw.TimeNum
    assert translate_args_class_types.get(kw.epoch_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.weekday_label) == kw.LabelTerm
    assert translate_args_class_types.get(kw.weekday_order) == "int"
    assert translate_args_class_types.get(kw.knot) == "str"
    assert translate_args_class_types.get(kw.yr1_jan1_offset) == "int"
    assert translate_args_class_types.get(kw.solo) == "int"

    # make sure it translate_arg_class_types has all moment and all atom args
    translate_args = set(translate_args_class_types.keys())
    atom_args = set(get_atom_args_class_types().keys())
    moment_args = set(get_moment_args_class_types().keys())
    assert atom_args.issubset(translate_args)
    assert moment_args.issubset(translate_args)
    assert atom_args & (moment_args) == {
        kw.partner_name,
        kw.fund_grain,
        kw.mana_grain,
        kw.respect_grain,
    }
    assert atom_args.union(moment_args) != translate_args
    assert atom_args.union(moment_args).union({kw.face_name}) == translate_args
    assert check_class_types_are_correct()
    # assert translate_args_class_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_class_types_are_correct(x_class_types)


def check_class_types_are_correct() -> bool:
    translate_args_class_types = get_translate_args_class_types()
    atom_args_class_types = get_atom_args_class_types()
    moment_args_class_types = get_moment_args_class_types()
    for translate_arg, translate_type in translate_args_class_types.items():
        print(f"check {translate_arg=} {translate_type=}")
        if atom_args_class_types.get(translate_arg) not in [None, translate_type]:
            print(
                f"{translate_arg=} {translate_type=} {atom_args_class_types.get(translate_arg)=}"
            )
            return False
        if moment_args_class_types.get(translate_arg) not in [None, translate_type]:
            print(
                f"{translate_arg=} {translate_type=} {moment_args_class_types.get(translate_arg)=}"
            )
            return False
    return True


def test_translateable_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_translateable_class_types = translateable_class_types()

    # THEN
    assert len(x_translateable_class_types) == 4
    assert x_translateable_class_types == {
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
    }
    print(f"{set(get_atom_args_class_types().values())=}")
    all_atom_class_types = set(get_atom_args_class_types().values())
    all_atom_class_types.add(kw.LabelTerm)
    all_atom_class_types.add(kw.TimeNum)
    x_cL_tyep = set(all_atom_class_types) & (x_translateable_class_types)
    assert x_cL_tyep == x_translateable_class_types


def test_get_translateable_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{translateable_class_types()=}")
    all_translate_args = set(get_translate_args_class_types().keys())
    print(f"{get_translateable_args().difference(all_translate_args)}")
    assert get_translateable_args().issubset(all_translate_args)
    static_get_translateable_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type in translateable_class_types()
    }
    assert get_translateable_args() == static_get_translateable_args

    assert len(get_translateable_args()) == 17
    assert get_translateable_args() == {
        kw.awardee_title,
        kw.person_name,
        kw.epoch_label,
        kw.face_name,
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
        kw.partner_name,
        kw.weekday_label,
    }


def test_set_translateable_otx_inx_args_ReturnsObj_Scenario0_All_translateable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    translateable_args = get_translateable_args()

    # WHEN
    otx_inx_args = set_translateable_otx_inx_args(translateable_args)

    # THEN
    expected_otx_inx_args = set()
    for translateable_arg in translateable_args:
        expected_otx_inx_args.add(f"{translateable_arg}_otx")
        expected_otx_inx_args.add(f"{translateable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_translateable_otx_inx_args_ReturnsObj_Scenario1_person_dimen_delete_keys():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    person_dimen_delete_keys = get_all_person_dimen_delete_keys()

    # WHEN
    otx_inx_args = set_translateable_otx_inx_args(person_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for translateable_arg in person_dimen_delete_keys:
        expected_otx_inx_args.add(f"{translateable_arg}_otx")
        expected_otx_inx_args.add(f"{translateable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_translateable_otx_inx_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    given_person_dimen_delete_keys = get_all_person_dimen_delete_keys()
    given_person_dimen_delete_keys.add(run_str)

    # WHEN
    otx_inx_args = set_translateable_otx_inx_args(given_person_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for translateable_arg in get_all_person_dimen_delete_keys():
        expected_otx_inx_args.add(f"{translateable_arg}_otx")
        expected_otx_inx_args.add(f"{translateable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_translateable_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    run_str = "run"
    given_person_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    otx_inx_args = set_translateable_otx_inx_args(given_person_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    expected_otx_inx_args = {
        f"{healer_name_ERASE_str}_otx",
        f"{healer_name_ERASE_str}_inx",
        run_str,
    }
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_translate_nameterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_NameTerm_args = get_translate_nameterm_args()

    # THEN
    assert translate_NameTerm_args == {
        kw.partner_name,
        kw.face_name,
        kw.healer_name,
        kw.person_name,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.NameTerm
    }
    assert translate_NameTerm_args == expected_args


def test_get_translate_titleterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_TitleTerm_args = get_translate_titleterm_args()

    # THEN
    assert translate_TitleTerm_args == {
        kw.awardee_title,
        kw.group_title,
        kw.labor_title,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.TitleTerm
    }
    assert translate_TitleTerm_args == expected_args


def test_get_translate_labelterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_LabelTerm_args = get_translate_labelterm_args()

    # THEN
    assert translate_LabelTerm_args == {
        kw.hour_label,
        kw.month_label,
        kw.epoch_label,
        kw.weekday_label,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.LabelTerm
    }
    assert translate_LabelTerm_args == expected_args


def test_get_translate_ropeterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    translate_RopeTerm_args = get_translate_ropeterm_args()

    # THEN
    assert translate_RopeTerm_args == {
        kw.moment_rope,
        kw.fact_state,
        kw.fact_context,
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_translate_args_class_types().items()
        if class_type == kw.RopeTerm
    }
    assert translate_RopeTerm_args == expected_args


def test_TranslateUnit_Exists():
    # ESTABLISH
    x_translateunit = TranslateUnit()

    # WHEN / THEN
    assert not x_translateunit.face_name
    assert not x_translateunit.spark_num
    assert not x_translateunit.titlemap
    assert not x_translateunit.namemap
    assert not x_translateunit.labelmap
    assert not x_translateunit.ropemap
    assert not x_translateunit.unknown_str
    assert not x_translateunit.otx_knot
    assert not x_translateunit.inx_knot
    assert set(x_translateunit.__dict__.keys()) == {
        kw.face_name,
        kw.spark_num,
        kw.titlemap,
        kw.namemap,
        kw.labelmap,
        kw.ropemap,
        kw.unknown_str,
        kw.otx_knot,
        kw.inx_knot,
    }


def test_translateunit_shop_ReturnsObj_Scenario0():
    # ESTABLISH

    # WHEN
    sue_translateunit = translateunit_shop(exx.sue)

    # THEN
    assert sue_translateunit.face_name == exx.sue
    assert sue_translateunit.spark_num == 0
    assert sue_translateunit.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.otx_knot == default_knot_if_None()
    assert sue_translateunit.inx_knot == default_knot_if_None()
    assert sue_translateunit.titlemap == titlemap_shop(face_name=exx.sue)
    assert sue_translateunit.namemap == namemap_shop(face_name=exx.sue)
    assert sue_translateunit.labelmap == labelmap_shop(face_name=exx.sue)
    assert sue_translateunit.ropemap == ropemap_shop(face_name=exx.sue)
    assert sue_translateunit.namemap.spark_num == 0
    assert sue_translateunit.namemap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.namemap.otx_knot == default_knot_if_None()
    assert sue_translateunit.namemap.inx_knot == default_knot_if_None()
    assert sue_translateunit.titlemap.spark_num == 0
    assert sue_translateunit.titlemap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.titlemap.otx_knot == default_knot_if_None()
    assert sue_translateunit.titlemap.inx_knot == default_knot_if_None()
    assert sue_translateunit.labelmap.spark_num == 0
    assert sue_translateunit.labelmap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.labelmap.otx_knot == default_knot_if_None()
    assert sue_translateunit.labelmap.inx_knot == default_knot_if_None()
    assert sue_translateunit.ropemap.spark_num == 0
    assert sue_translateunit.ropemap.unknown_str == default_unknown_str_if_None()
    assert sue_translateunit.ropemap.otx_knot == default_knot_if_None()
    assert sue_translateunit.ropemap.inx_knot == default_knot_if_None()


def test_translateunit_shop_ReturnsObj_Scenario1():
    # ESTABLISH
    five_spark_num = 5
    y_uk = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    sue_translateunit = translateunit_shop(
        face_name=exx.sue,
        spark_num=five_spark_num,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=y_uk,
    )

    # THEN
    assert sue_translateunit.spark_num == five_spark_num
    assert sue_translateunit.unknown_str == y_uk
    assert sue_translateunit.otx_knot == slash_otx_knot
    assert sue_translateunit.inx_knot == colon_inx_knot

    # x_titlemap = titlemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
    # )
    # x_ropemap = ropemap_shop(
    #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, exx.sue, five_spark_num
    # )
    # assert sue_translateunit.titlemap == x_titlemap
    # assert sue_translateunit.namemap == x_namemap
    # assert sue_translateunit.ropemap == x_ropemap

    assert sue_translateunit.namemap.face_name == exx.sue
    assert sue_translateunit.namemap.spark_num == five_spark_num
    assert sue_translateunit.namemap.unknown_str == y_uk
    assert sue_translateunit.namemap.otx_knot == slash_otx_knot
    assert sue_translateunit.namemap.inx_knot == colon_inx_knot
    assert sue_translateunit.titlemap.face_name == exx.sue
    assert sue_translateunit.titlemap.spark_num == five_spark_num
    assert sue_translateunit.titlemap.unknown_str == y_uk
    assert sue_translateunit.titlemap.otx_knot == slash_otx_knot
    assert sue_translateunit.titlemap.inx_knot == colon_inx_knot
    assert sue_translateunit.labelmap.face_name == exx.sue
    assert sue_translateunit.labelmap.spark_num == five_spark_num
    assert sue_translateunit.labelmap.unknown_str == y_uk
    assert sue_translateunit.labelmap.otx_knot == slash_otx_knot
    assert sue_translateunit.labelmap.inx_knot == colon_inx_knot
    assert sue_translateunit.ropemap.face_name == exx.sue
    assert sue_translateunit.ropemap.spark_num == five_spark_num
    assert sue_translateunit.ropemap.unknown_str == y_uk
    assert sue_translateunit.ropemap.otx_knot == slash_otx_knot
    assert sue_translateunit.ropemap.inx_knot == colon_inx_knot


def test_translateunit_shop_ReturnsObj_Scenario2_TranslateCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    x_nan = float("nan")

    # WHEN
    x_translateunit = translateunit_shop(
        face_name=exx.bob,
        spark_num=spark7,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_translateunit.face_name == exx.bob
    assert x_translateunit.spark_num == spark7
    assert x_translateunit.unknown_str == default_unknown_str_if_None()
    assert x_translateunit.otx_knot == default_knot_if_None()
    assert x_translateunit.inx_knot == default_knot_if_None()
