from ch05_rope.rope import default_knot_if_None
from ch09_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_atom_args_obj_types,
)
from ch15_moment.moment_config import get_moment_args_obj_types
from ch17_jargon.map_term import (
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from ch17_jargon.jargon_config import (
    default_unknown_str_if_None,
    get_jargon_args_obj_types,
    get_jargon_labelterm_args,
    get_jargon_nameterm_args,
    get_jargon_ropeterm_args,
    get_jargon_titleterm_args,
    get_jargonable_args,
    set_jargonable_otx_inx_args,
    jargonable_obj_types,
)
from ch17_jargon.jargon_main import JargonUnit, jargonunit_shop
from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx


def test_get_jargon_args_obj_types_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_args_obj_types = get_jargon_args_obj_types()

    # THEN
    assert jargon_args_obj_types.get(kw.contact_name) == kw.NameTerm
    assert jargon_args_obj_types.get(kw.addin) == "float"
    assert jargon_args_obj_types.get(kw.amount) == "float"
    assert jargon_args_obj_types.get(kw.awardee_title) == kw.TitleTerm
    assert jargon_args_obj_types.get(kw.reason_context) == kw.RopeTerm
    assert jargon_args_obj_types.get(kw.active_requisite) == "bool"
    assert jargon_args_obj_types.get(kw.begin) == "float"
    assert jargon_args_obj_types.get(kw.c400_number) == "int"
    assert jargon_args_obj_types.get(kw.close) == "float"
    assert jargon_args_obj_types.get(kw.contact_cred_mass) == "float"
    assert jargon_args_obj_types.get(kw.group_cred_mass) == "float"
    assert jargon_args_obj_types.get(kw.credor_respect) == "float"
    assert jargon_args_obj_types.get(kw.cumulative_day) == "int"
    assert jargon_args_obj_types.get(kw.cumulative_minute) == "int"
    assert jargon_args_obj_types.get(kw.contact_debt_mass) == "float"
    assert jargon_args_obj_types.get(kw.group_debt_mass) == "float"
    assert jargon_args_obj_types.get(kw.debtor_respect) == "float"
    assert jargon_args_obj_types.get(kw.denom) == "int"
    assert jargon_args_obj_types.get(kw.reason_divisor) == "int"
    assert jargon_args_obj_types.get(kw.spark_face) == kw.NameTerm
    assert jargon_args_obj_types.get(kw.fact_context) == kw.RopeTerm
    assert jargon_args_obj_types.get(kw.moment_rope) == kw.RopeTerm
    assert jargon_args_obj_types.get(kw.fact_upper) == kw.FactNum
    assert jargon_args_obj_types.get(kw.fact_lower) == kw.FactNum
    assert jargon_args_obj_types.get(kw.fund_grain) == "float"
    assert jargon_args_obj_types.get(kw.fund_pool) == "float"
    assert jargon_args_obj_types.get(kw.give_force) == "float"
    assert jargon_args_obj_types.get(kw.gogo_want) == "float"
    assert jargon_args_obj_types.get(kw.group_title) == kw.TitleTerm
    assert jargon_args_obj_types.get(kw.healer_name) == kw.NameTerm
    assert jargon_args_obj_types.get(kw.hour_label) == kw.LabelTerm
    assert jargon_args_obj_types.get(kw.poynt) == "int"
    assert jargon_args_obj_types.get(kw.max_tree_traverse) == "int"
    assert jargon_args_obj_types.get(kw.month_label) == kw.LabelTerm
    assert jargon_args_obj_types.get(kw.monthday_index) == "int"
    assert jargon_args_obj_types.get(kw.morph) == "bool"
    assert jargon_args_obj_types.get(kw.reason_state) == kw.RopeTerm
    assert jargon_args_obj_types.get(kw.reason_upper) == kw.ReasonNum
    assert jargon_args_obj_types.get(kw.numor) == "int"
    assert jargon_args_obj_types.get(kw.offi_time) == kw.TimeNum
    assert jargon_args_obj_types.get(kw.person_name) == kw.NameTerm
    assert jargon_args_obj_types.get(kw.reason_lower) == kw.ReasonNum
    assert jargon_args_obj_types.get(kw.mana_grain) == "float"
    assert jargon_args_obj_types.get(kw.fact_state) == kw.RopeTerm
    assert jargon_args_obj_types.get(kw.pledge) == "bool"
    assert jargon_args_obj_types.get(kw.problem_bool) == "bool"
    assert jargon_args_obj_types.get(kw.quota) == "int"
    assert jargon_args_obj_types.get(kw.respect_grain) == "float"
    assert jargon_args_obj_types.get(kw.plan_rope) == kw.RopeTerm
    assert jargon_args_obj_types.get(kw.celldepth) == "int"
    assert jargon_args_obj_types.get(kw.stop_want) == "float"
    assert jargon_args_obj_types.get(kw.take_force) == "float"
    assert jargon_args_obj_types.get(kw.labor_title) == kw.TitleTerm
    assert jargon_args_obj_types.get(kw.bud_time) == kw.TimeNum
    assert jargon_args_obj_types.get(kw.tran_time) == kw.TimeNum
    assert jargon_args_obj_types.get(kw.epoch_label) == kw.LabelTerm
    assert jargon_args_obj_types.get(kw.weekday_label) == kw.LabelTerm
    assert jargon_args_obj_types.get(kw.weekday_order) == "int"
    assert jargon_args_obj_types.get(kw.knot) == "str"
    assert jargon_args_obj_types.get(kw.yr1_jan1_offset) == "int"
    assert jargon_args_obj_types.get(kw.solo) == "int"

    # make sure it jargon_arg_obj_types has all moment and all atom args
    jargon_args = set(jargon_args_obj_types.keys())
    atom_args = set(get_atom_args_obj_types().keys())
    moment_args = set(get_moment_args_obj_types().keys())
    assert atom_args.issubset(jargon_args)
    assert moment_args.issubset(jargon_args)
    assert atom_args & (moment_args) == {
        kw.contact_name,
        kw.fund_grain,
        kw.mana_grain,
        kw.respect_grain,
    }
    assert atom_args.union(moment_args) != jargon_args
    assert atom_args.union(moment_args).union({kw.spark_face}) == jargon_args
    assert check_obj_types_are_correct(jargon_args_obj_types)
    # assert jargon_args_obj_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_obj_types_are_correct(x_obj_types)

    for jargon_arg in jargon_args_obj_types.keys():
        assert not jargon_arg.endswith("_otx"), f"Error with '{jargon_arg}'"
        assert not jargon_arg.endswith("_inx"), f"Error with '{jargon_arg}'"


def check_obj_types_are_correct(jargon_args_obj_types: dict[str, str]) -> bool:
    atom_args_obj_types = get_atom_args_obj_types()
    moment_args_obj_types = get_moment_args_obj_types()
    for jargon_arg, jargon_type in jargon_args_obj_types.items():
        # print(f"check {jargon_arg=} {jargon_type=}")
        if atom_args_obj_types.get(jargon_arg) not in [None, jargon_type]:
            print(
                f"{jargon_arg=} {jargon_type=} {atom_args_obj_types.get(jargon_arg)=}"
            )
            return False
        if moment_args_obj_types.get(jargon_arg) not in [None, jargon_type]:
            print(
                f"{jargon_arg=} {jargon_type=} {moment_args_obj_types.get(jargon_arg)=}"
            )
            return False
    return True


def test_jargonable_obj_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_jargonable_obj_types = jargonable_obj_types()

    # THEN
    assert len(x_jargonable_obj_types) == 4
    assert x_jargonable_obj_types == {
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
    }
    print(f"{set(get_atom_args_obj_types().values())=}")
    all_atom_obj_types = set(get_atom_args_obj_types().values())
    all_atom_obj_types.add(kw.LabelTerm)
    all_atom_obj_types.add(kw.TimeNum)
    x_cL_tyep = set(all_atom_obj_types) & (x_jargonable_obj_types)
    assert x_cL_tyep == x_jargonable_obj_types


def test_get_jargonable_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{jargonable_obj_types()=}")
    all_jargon_args = set(get_jargon_args_obj_types().keys())
    print(f"{get_jargonable_args().difference(all_jargon_args)}")
    assert get_jargonable_args().issubset(all_jargon_args)
    static_get_jargonable_args = {
        x_arg
        for x_arg, obj_type in get_jargon_args_obj_types().items()
        if obj_type in jargonable_obj_types()
    }
    assert get_jargonable_args() == static_get_jargonable_args

    assert len(get_jargonable_args()) == 17
    assert get_jargonable_args() == {
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


def test_set_jargonable_otx_inx_args_ReturnsObj_Scenario0_All_jargonable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    jargonable_args = get_jargonable_args()

    # WHEN
    otx_inx_args = set_jargonable_otx_inx_args(jargonable_args)

    # THEN
    expected_otx_inx_args = set()
    for jargonable_arg in jargonable_args:
        expected_otx_inx_args.add(f"{jargonable_arg}_otx")
        expected_otx_inx_args.add(f"{jargonable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_jargonable_otx_inx_args_ReturnsObj_Scenario1_person_dimen_delete_keys():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    person_dimen_delete_keys = get_all_person_dimen_delete_keys()

    # WHEN
    otx_inx_args = set_jargonable_otx_inx_args(person_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for jargonable_arg in person_dimen_delete_keys:
        expected_otx_inx_args.add(f"{jargonable_arg}_otx")
        expected_otx_inx_args.add(f"{jargonable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_jargonable_otx_inx_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    given_person_dimen_delete_keys = get_all_person_dimen_delete_keys()
    given_person_dimen_delete_keys.add(run_str)

    # WHEN
    otx_inx_args = set_jargonable_otx_inx_args(given_person_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for jargonable_arg in get_all_person_dimen_delete_keys():
        expected_otx_inx_args.add(f"{jargonable_arg}_otx")
        expected_otx_inx_args.add(f"{jargonable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_set_jargonable_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    run_str = "run"
    given_person_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    otx_inx_args = set_jargonable_otx_inx_args(given_person_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    expected_otx_inx_args = {
        f"{healer_name_ERASE_str}_otx",
        f"{healer_name_ERASE_str}_inx",
        run_str,
    }
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_jargon_nameterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_NameTerm_args = get_jargon_nameterm_args()

    # THEN
    assert jargon_NameTerm_args == {
        kw.contact_name,
        kw.spark_face,
        kw.healer_name,
        kw.person_name,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_jargon_args_obj_types().items()
        if obj_type == kw.NameTerm
    }
    assert jargon_NameTerm_args == expected_args


def test_get_jargon_titleterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_TitleTerm_args = get_jargon_titleterm_args()

    # THEN
    assert jargon_TitleTerm_args == {
        kw.awardee_title,
        kw.group_title,
        kw.labor_title,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_jargon_args_obj_types().items()
        if obj_type == kw.TitleTerm
    }
    assert jargon_TitleTerm_args == expected_args


def test_get_jargon_labelterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_LabelTerm_args = get_jargon_labelterm_args()

    # THEN
    assert jargon_LabelTerm_args == {
        kw.hour_label,
        kw.month_label,
        kw.epoch_label,
        kw.weekday_label,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_jargon_args_obj_types().items()
        if obj_type == kw.LabelTerm
    }
    assert jargon_LabelTerm_args == expected_args


def test_get_jargon_ropeterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    jargon_RopeTerm_args = get_jargon_ropeterm_args()

    # THEN
    assert jargon_RopeTerm_args == {
        kw.moment_rope,
        kw.fact_state,
        kw.fact_context,
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    }
    expected_args = {
        x_arg
        for x_arg, obj_type in get_jargon_args_obj_types().items()
        if obj_type == kw.RopeTerm
    }
    assert jargon_RopeTerm_args == expected_args


def test_JargonUnit_Exists():
    # ESTABLISH
    x_jargonunit = JargonUnit()

    # WHEN / THEN
    assert not x_jargonunit.spark_face
    assert not x_jargonunit.spark_num
    assert not x_jargonunit.titlemap
    assert not x_jargonunit.namemap
    assert not x_jargonunit.labelmap
    assert not x_jargonunit.ropemap
    assert not x_jargonunit.unknown_str
    assert not x_jargonunit.otx_knot
    assert not x_jargonunit.inx_knot
    assert set(x_jargonunit.__dict__.keys()) == {
        kw.spark_face,
        kw.spark_num,
        kw.titlemap,
        kw.namemap,
        kw.labelmap,
        kw.ropemap,
        kw.unknown_str,
        kw.otx_knot,
        kw.inx_knot,
    }


def test_jargonunit_shop_ReturnsObj_Scenario0():
    # ESTABLISH

    # WHEN
    sue_jargonunit = jargonunit_shop(exx.sue)

    # THEN
    assert sue_jargonunit.spark_face == exx.sue
    assert sue_jargonunit.spark_num == 0
    assert sue_jargonunit.unknown_str == default_unknown_str_if_None()
    assert sue_jargonunit.otx_knot == default_knot_if_None()
    assert sue_jargonunit.inx_knot == default_knot_if_None()
    assert sue_jargonunit.titlemap == titlemap_shop(spark_face=exx.sue)
    assert sue_jargonunit.namemap == namemap_shop(spark_face=exx.sue)
    assert sue_jargonunit.labelmap == labelmap_shop(spark_face=exx.sue)
    assert sue_jargonunit.ropemap == ropemap_shop(spark_face=exx.sue)
    assert sue_jargonunit.namemap.spark_num == 0
    assert sue_jargonunit.namemap.unknown_str == default_unknown_str_if_None()
    assert sue_jargonunit.namemap.otx_knot == default_knot_if_None()
    assert sue_jargonunit.namemap.inx_knot == default_knot_if_None()
    assert sue_jargonunit.titlemap.spark_num == 0
    assert sue_jargonunit.titlemap.unknown_str == default_unknown_str_if_None()
    assert sue_jargonunit.titlemap.otx_knot == default_knot_if_None()
    assert sue_jargonunit.titlemap.inx_knot == default_knot_if_None()
    assert sue_jargonunit.labelmap.spark_num == 0
    assert sue_jargonunit.labelmap.unknown_str == default_unknown_str_if_None()
    assert sue_jargonunit.labelmap.otx_knot == default_knot_if_None()
    assert sue_jargonunit.labelmap.inx_knot == default_knot_if_None()
    assert sue_jargonunit.ropemap.spark_num == 0
    assert sue_jargonunit.ropemap.unknown_str == default_unknown_str_if_None()
    assert sue_jargonunit.ropemap.otx_knot == default_knot_if_None()
    assert sue_jargonunit.ropemap.inx_knot == default_knot_if_None()


def test_jargonunit_shop_ReturnsObj_Scenario1():
    # ESTABLISH
    five_spark_num = 5
    y_uk = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"

    # WHEN
    sue_jargonunit = jargonunit_shop(
        spark_face=exx.sue,
        spark_num=five_spark_num,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=y_uk,
    )

    # THEN
    assert sue_jargonunit.spark_num == five_spark_num
    assert sue_jargonunit.unknown_str == y_uk
    assert sue_jargonunit.otx_knot == slash_otx_knot
    assert sue_jargonunit.inx_knot == colon_inx_knot

    # x_titlemap = titlemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
    # )
    # x_ropemap = ropemap_shop(
    #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, exx.sue, five_spark_num
    # )
    # assert sue_jargonunit.titlemap == x_titlemap
    # assert sue_jargonunit.namemap == x_namemap
    # assert sue_jargonunit.ropemap == x_ropemap

    assert sue_jargonunit.namemap.spark_face == exx.sue
    assert sue_jargonunit.namemap.spark_num == five_spark_num
    assert sue_jargonunit.namemap.unknown_str == y_uk
    assert sue_jargonunit.namemap.otx_knot == slash_otx_knot
    assert sue_jargonunit.namemap.inx_knot == colon_inx_knot
    assert sue_jargonunit.titlemap.spark_face == exx.sue
    assert sue_jargonunit.titlemap.spark_num == five_spark_num
    assert sue_jargonunit.titlemap.unknown_str == y_uk
    assert sue_jargonunit.titlemap.otx_knot == slash_otx_knot
    assert sue_jargonunit.titlemap.inx_knot == colon_inx_knot
    assert sue_jargonunit.labelmap.spark_face == exx.sue
    assert sue_jargonunit.labelmap.spark_num == five_spark_num
    assert sue_jargonunit.labelmap.unknown_str == y_uk
    assert sue_jargonunit.labelmap.otx_knot == slash_otx_knot
    assert sue_jargonunit.labelmap.inx_knot == colon_inx_knot
    assert sue_jargonunit.ropemap.spark_face == exx.sue
    assert sue_jargonunit.ropemap.spark_num == five_spark_num
    assert sue_jargonunit.ropemap.unknown_str == y_uk
    assert sue_jargonunit.ropemap.otx_knot == slash_otx_knot
    assert sue_jargonunit.ropemap.inx_knot == colon_inx_knot


def test_jargonunit_shop_ReturnsObj_Scenario2_JargonCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    x_nan = float("nan")

    # WHEN
    x_jargonunit = jargonunit_shop(
        spark_face=exx.bob,
        spark_num=spark7,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_jargonunit.spark_face == exx.bob
    assert x_jargonunit.spark_num == spark7
    assert x_jargonunit.unknown_str == default_unknown_str_if_None()
    assert x_jargonunit.otx_knot == default_knot_if_None()
    assert x_jargonunit.inx_knot == default_knot_if_None()
