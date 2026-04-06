from inspect import getdoc as inspect_getdoc
from re import fullmatch as re_fullmatch
from src.ch00_py.keyword_class_builder import get_keywords_src_config
from src.ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_config_dict,
)
from src.ch13_time.epoch_main import get_c400_constants, get_default_epoch_config_dict
from src.ch14_moment.moment_config import get_moment_config_args
from src.ch15_nabu.nabu_config import get_nabu_args, get_nabuable_args
from src.ch16_translate.translate_config import (
    get_translate_config_args,
    get_translate_config_dict,
)
from src.ch18_etl_config.etl_config import get_etl_stage_types_config_dict
from src.ch19_etl_steps.etl_main import etl_heard_raw_tables_to_moment_ote1_agg
from src.ch98_docs_builder._ref.ch98_semantic_types import (
    BreakTerm,
    ContactName,
    CRUD_command,
    EpochLabel,
    FaceName,
    FactNum,
    FirstLabel,
    FundGrain,
    FundNum,
    GrainNum,
    GroupMark,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    LobbyID,
    ManaGrain,
    ManaNum,
    MomentRope,
    NameTerm,
    PersonName,
    PoolNum,
    ReasonNum,
    RespectGrain,
    RespectNum,
    RopeTerm,
    SparkInt,
    TimeNum,
    TitleTerm,
    WeightNum,
    WorldName,
)
from src.ch98_docs_builder.keg_definitions_builder import (
    get_chxx_prefix_path_dict,
    get_chxx_ref_blurb,
    get_keg_definitions,
    get_person_dimen_config,
)
from src.ref.keywords import Ch98Keywords as kw


def python_keywords() -> set:
    return {"self", "class", "assert", "import", "global", "yield", "break", "match"}


def test_get_keg_definitions_ReturnsObj_Check_python_keywords():
    # ESTABLISH
    python_keyword_args = python_keywords()
    # print(f"{person_config_args.keys()=}")

    # WHEN
    keg_definitions = get_keg_definitions()

    # THEN
    py_used_often_str = (
        "Used so often in Python that it cannot be given any kegolgy meaning."
    )
    for python_keyword in python_keyword_args:
        py_key_description = keg_definitions.get(python_keyword)
        assert py_used_often_str in py_key_description, python_keyword


def test_get_keg_definitions_ReturnsObj_Check_moment_ote1_agg():
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()

    # THEN
    moment_ote1_agg_desc = inspect_getdoc(etl_heard_raw_tables_to_moment_ote1_agg)
    assert moment_ote1_agg_desc in keg_definitions.get(kw.moment_ote1_agg)


def test_get_keg_definitions_ReturnsObj_CheckNoChapter_keywords():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    for keyword, kw_config in get_keywords_src_config().items():
        x_init_chapter = kw_config.get("init_chapter")
        if not bool(re_fullmatch(r"ch\d{2}", x_init_chapter)):
            config_description = keg_definitions.get(keyword)
            assert "Not used in codebase." in config_description, keyword


def test_get_keg_definitions_ReturnsObj_Check_person_dimen():
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    for person_dimen, attribute_dict in get_person_config_dict().items():
        dimen_description = attribute_dict.get("description")
        print(dimen_description)
        assert keg_definitions.get(person_dimen) == dimen_description


def test_get_keg_definitions_ReturnsObj_Check_stages_types():
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    stage_types_config = get_etl_stage_types_config_dict()
    for stage_type_abbv5, type_dict in stage_types_config.items():
        abbv5_keyword_description = keg_definitions.get(stage_type_abbv5)
        abbv9_str = type_dict.get("abbv9")
        type_description_str = type_dict.get("description")
        stage_type_order = type_dict.get("stage_type_order")
        expected_abbv5_description = f"5 character abbreviation of {abbv9_str}. {stage_type_order=} {type_description_str}"
        abbv5_fail_str = expected_abbv5_description
        print(f"{stage_type_abbv5=}")
        assert expected_abbv5_description == abbv5_keyword_description, abbv5_fail_str

        print(f"{abbv9_str=}")
        expected_abbv9_description = f"{stage_type_order=} {type_description_str}"
        gen_abbv9_description = keg_definitions.get(abbv9_str)
        abbv9_fail_str = f"assert failed: {expected_abbv9_description}"
        assert expected_abbv9_description == gen_abbv9_description, abbv9_fail_str


def test_get_keg_definitions_ReturnsObj_Check_semantic_types():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()

    # THEN
    all_semantic_types = get_all_semantic_types_with_doc_strs()
    for semantic_class, class_doc_str in all_semantic_types.items():
        semantic_description = keg_definitions.get(semantic_class)
        # print(f"{semantic_class=} {class_doc_str=}")
        assert class_doc_str in semantic_description


def test_get_keg_definitions_ReturnsObj_Check_src_config_keywords():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()

    # THEN
    all_semantic_types = get_all_semantic_types_with_doc_strs()
    doc_str_semantic_types = set(all_semantic_types.keys())
    for keyword, kw_config in get_keywords_src_config().items():
        if semantic_type := kw_config.get("semantic_type"):
            # print(f"{keyword} {kw_config=}")
            x_init_chapter = kw_config.get("init_chapter")
            kw_desc = f"{semantic_type} first used in {x_init_chapter}"
            config_description = keg_definitions.get(keyword)
            assert kw_desc in config_description, keyword
            assert keyword in doc_str_semantic_types


def test_get_keg_definitions_ReturnsObj_Check_epoch_config():
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    for config_key, config_obj in get_default_epoch_config_dict().items():
        config_description = keg_definitions.get(config_key)
        # print(f"{config_key=} {config_description=}")
        assert f"Epoch config" in config_description


def test_get_keg_definitions_ReturnsObj_Check_c400_constants():
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    for constant_name, constant_int in get_c400_constants().__dict__.items():
        formated_constant = f"{constant_int:,}"
        constant_description = keg_definitions.get(constant_name)
        # print(f"{constant_name} {formated_constant} {constant_description=}")
        assert formated_constant in constant_description
        assert "C400Constant for building Epochs" in constant_description


def test_get_keg_definitions_ReturnsObj_CheckChapter():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    ch_dict = get_chxx_prefix_path_dict()
    for chxx_prefix, ch_ref_path in ch_dict.items():
        ch_blurb = get_chxx_ref_blurb(ch_dict, chxx_prefix)
        ch_desc = keg_definitions.get(chxx_prefix)
        print(f"{chxx_prefix=} {ch_blurb=}")
        assert ch_blurb == ch_desc, ch_blurb


def test_get_keg_definitions_ReturnsObj_CheckConfigArgs():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    person_args = get_person_dimen_config(kw.personunit)
    plan_args = get_person_dimen_config(kw.person_planunit)
    reason_args = get_person_dimen_config(kw.person_plan_reasonunit)
    case_args = get_person_dimen_config(kw.person_plan_reason_caseunit)
    fact_args = get_person_dimen_config(kw.person_plan_factunit)
    award_args = get_person_dimen_config(kw.person_plan_awardunit)
    labor_args = get_person_dimen_config(kw.person_plan_laborunit)
    healer_args = get_person_dimen_config(kw.person_plan_healerunit)
    contact_args = get_person_dimen_config(kw.person_contactunit)
    member_args = get_person_dimen_config(kw.person_contact_membership)

    trllabe_args = get_translate_config_args(kw.translate_label)
    trlname_args = get_translate_config_args(kw.translate_name)
    trlrope_args = get_translate_config_args(kw.translate_rope)
    trltitl_args = get_translate_config_args(kw.translate_title)

    mmtbudd_args = get_moment_config_args(kw.moment_budunit)
    mmthour_args = get_moment_config_args(kw.moment_epoch_hour)
    mmtmont_args = get_moment_config_args(kw.moment_epoch_month)
    mmtweek_args = get_moment_config_args(kw.moment_epoch_weekday)
    mmtpayy_args = get_moment_config_args(kw.moment_paybook)
    mmtoffi_args = get_moment_config_args(kw.moment_timeoffi)
    mmtunit_args = get_moment_config_args(kw.momentunit)
    nabu_args = get_nabu_args()
    nabuable_args = get_nabuable_args()
    for keyword, desc in keg_definitions.items():
        check_person_desc_str(person_args, keyword, desc, "Person")
        check_person_desc_str(plan_args, keyword, desc, "Plan")
        check_person_desc_str(reason_args, keyword, desc, "Reason")
        check_person_desc_str(case_args, keyword, desc, "Case")
        check_person_desc_str(fact_args, keyword, desc, "Fact")
        check_person_desc_str(award_args, keyword, desc, "Award")
        check_person_desc_str(labor_args, keyword, desc, "Workforce")
        check_person_desc_str(healer_args, keyword, desc, "Healer")
        check_person_desc_str(contact_args, keyword, desc, "Contact")
        check_person_desc_str(member_args, keyword, desc, "Member")
        check_translate_desc_str(trllabe_args, keyword, desc, kw.translate_label)
        check_translate_desc_str(trlname_args, keyword, desc, kw.translate_name)
        check_translate_desc_str(trlrope_args, keyword, desc, kw.translate_rope)
        check_translate_desc_str(trltitl_args, keyword, desc, kw.translate_title)
        check_mmtunit_desc_str(mmtbudd_args, keyword, desc, "bud")
        check_mmtunit_desc_str(mmthour_args, keyword, desc, kw.mmthour)
        check_mmtunit_desc_str(mmtmont_args, keyword, desc, kw.mmtmont)
        check_mmtunit_desc_str(mmtweek_args, keyword, desc, kw.mmtweek)
        check_mmtunit_desc_str(mmtpayy_args, keyword, desc, kw.paybook)
        check_mmtunit_desc_str(mmtoffi_args, keyword, desc, kw.offi_time)
        check_mmtunit_desc_str(mmtunit_args, keyword, desc, "Moment")
        check_mmtunit_desc_str(nabu_args, keyword, desc, kw.nabu)
        check_mmtunit_desc_str(nabuable_args, keyword, desc, "Nabuable")


def test_get_keg_definitions_ReturnsObj_CheckTranslate_dimen():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()
    # THEN
    for translate_dimen, translate_dict in get_translate_config_dict().items():
        translate_description = translate_dict.get("description")
        print(translate_description)
        assert keg_definitions.get(translate_dimen) == translate_description


def get_all_semantic_types_with_doc_strs() -> dict[str, str]:
    x_dict = {
        BreakTerm.__name__: inspect_getdoc(BreakTerm("")),
        CRUD_command.__name__: inspect_getdoc(CRUD_command("")),
        EpochLabel.__name__: inspect_getdoc(EpochLabel("")),
        FaceName.__name__: inspect_getdoc(FaceName("")),
        FactNum.__name__: inspect_getdoc(FactNum(0)),
        FirstLabel.__name__: inspect_getdoc(FirstLabel("")),
        FundGrain.__name__: inspect_getdoc(FundGrain(0)),
        FundNum.__name__: inspect_getdoc(FundNum(0)),
        GrainNum.__name__: inspect_getdoc(GrainNum(0)),
        GroupMark.__name__: inspect_getdoc(GroupMark("")),
        GroupTitle.__name__: inspect_getdoc(GroupTitle("")),
        HealerName.__name__: inspect_getdoc(HealerName("")),
        KnotTerm.__name__: inspect_getdoc(KnotTerm("")),
        LabelTerm.__name__: inspect_getdoc(LabelTerm("")),
        LobbyID.__name__: inspect_getdoc(LobbyID("")),
        ManaGrain.__name__: inspect_getdoc(ManaGrain(0)),
        ManaNum.__name__: inspect_getdoc(ManaNum(0)),
        MomentRope.__name__: inspect_getdoc(MomentRope("")),
        NameTerm.__name__: inspect_getdoc(NameTerm("")),
        ContactName.__name__: inspect_getdoc(ContactName("")),
        PersonName.__name__: inspect_getdoc(PersonName("")),
        PoolNum.__name__: inspect_getdoc(PoolNum(0)),
        ReasonNum.__name__: inspect_getdoc(ReasonNum(0)),
        RespectGrain.__name__: inspect_getdoc(RespectGrain(0)),
        RespectNum.__name__: inspect_getdoc(RespectNum(0)),
        RopeTerm.__name__: inspect_getdoc(RopeTerm("")),
        SparkInt.__name__: inspect_getdoc(SparkInt(0)),
        TimeNum.__name__: inspect_getdoc(TimeNum(0)),
        TitleTerm.__name__: inspect_getdoc(TitleTerm("")),
        WeightNum.__name__: inspect_getdoc(WeightNum(0)),
        WorldName.__name__: inspect_getdoc(WorldName(0)),
    }
    for x_key in set(x_dict.keys()):
        x_dict[x_key] = str(x_dict.get(x_key)).replace("\n", " ")
    return x_dict


def check_person_desc_str(
    config_args: dict, keyword: str, description: str, src_label: str
):
    if keyword in config_args:
        keyword_config = config_args.get(keyword)
        calc_by_conpute_value = keyword_config.get(kw.calc_by_conpute)
        assert_fail_str = f"{keyword=} {description=} {calc_by_conpute_value=} "
        # print(f"{keyword} {assert_fail_str=}")
        conpute_str = f", {src_label} {kw.conpute}"
        seed_str = f", {src_label} seed"
        if keyword_config.get(kw.calc_by_conpute):
            assert conpute_str in description, assert_fail_str
            assert seed_str not in description, assert_fail_str
        else:
            assert seed_str in description, assert_fail_str
            assert conpute_str not in description, assert_fail_str


def check_mmtunit_desc_str(
    config_args: dict, keyword: str, description: str, src_label: str
):
    if keyword in config_args:
        # keyword_config = config_args.get(keyword)
        assert_fail_str = f"{keyword=} {description=} "
        # print(f"{keyword} {assert_fail_str=}")
        assert f", {src_label} arg" in description, assert_fail_str


def check_translate_desc_str(
    config_args: dict, keyword: str, description: str, src_label: str
):
    if keyword in config_args:
        assert_fail_str = f"{keyword=} {description=} "
        # print(f"{keyword} {assert_fail_str=}")
        assert f", {src_label.upper()} arg" in description, assert_fail_str


def test_get_keg_definitions_ReturnsObj_HasAllkeywords():
    # ESTABLISH / WHEN
    keg_definitions = get_keg_definitions()

    # THEN
    assert keg_definitions
    keywords_config = get_keywords_src_config()

    description_keywords = set(keg_definitions.keys())
    config_keywords = set(keywords_config.keys())
    config_keywords.update(python_keywords())
    print(f"{config_keywords.difference(description_keywords)=}")
    print(f"{description_keywords.difference(config_keywords)=}")
    assert set(keg_definitions.keys()) == config_keywords
    for keyword, description in keg_definitions.items():
        assert description, keyword


def test_get_keg_definitions_ReturnsObj_get_all_person_calc_args():
    # ESTABLISH
    all_person_calc_args = get_all_person_calc_args()
    # print(f"{person_config_args.keys()=}")

    # WHEN
    keg_definitions = get_keg_definitions()

    # THEN
    for person_calc_arg in all_person_calc_args:
        print(f"{person_calc_arg=}")
        py_key_description = keg_definitions.get(person_calc_arg)
        assert py_key_description, person_calc_arg
