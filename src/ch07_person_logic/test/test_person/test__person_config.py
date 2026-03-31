# from src.ch00_py.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path
from src.ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_args_sqlite_datatype_dict,
    get_person_calc_args_type_dict,
    get_person_calc_dimen_args,
    get_person_calc_dimens,
    get_person_config_dict,
    max_tree_traverse_default,
    person_config_path,
)
from src.ch07_person_logic.person_main import PartnerUnit, PersonUnit
from src.ref.keywords import Ch07Keywords as kw


def test_max_tree_traverse_default_ReturnsObj() -> str:
    # ESTABLISH / WHEN / THEN
    assert max_tree_traverse_default() == 20


def test_get_person_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "ch07_person_logic")

    # WHEN
    config_path = person_config_path()
    # THEN
    expected_path = create_path(expected_dir, "person_config.json")
    assert config_path == expected_path
    assert os_path_exists(person_config_path())


def test_get_person_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    person_config = get_person_config_dict()
    person_config_keys = set(person_config.keys())

    # THEN
    assert kw.personunit in person_config_keys
    assert kw.person_partnerunit in person_config_keys
    assert kw.person_partner_membership in person_config_keys
    assert kw.person_planunit in person_config_keys
    assert kw.person_plan_awardunit in person_config_keys
    assert kw.person_plan_reasonunit in person_config_keys
    assert kw.person_plan_reason_caseunit in person_config_keys
    assert kw.person_plan_laborunit in person_config_keys
    assert kw.person_plan_healerunit in person_config_keys
    assert kw.person_plan_factunit in person_config_keys
    assert kw.person_groupunit in person_config_keys
    assert len(get_person_config_dict()) == 11


def test_get_person_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    person_config = get_person_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for person_dimen, attribute_dict in person_config.items():
        attribute_keys = set(attribute_dict.keys())
        # print(f"{person_dimen=} {attribute_keys=}")
        assert "abbreviation" in attribute_keys
        assert "description" in attribute_keys
        assert kw.jkeys in attribute_keys
        assert kw.jvalues in attribute_keys
        assert len(attribute_keys) == 4
        dimen_description = attribute_dict.get("description")
        print(f"{dimen_description=}")
        assert "A person dimen representing" in dimen_description
        for jkey in attribute_dict.get(kw.jkeys):
            assert jkey in dimen_description


def test_get_person_config_dict_ReturnsObj_Check_calc_by_conpute():
    # ESTABLISH / WHEN
    person_config = get_person_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    abbr_str = "abbreviation"
    description_str = "description"
    for level1_key, attribute_dict in person_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key not in {abbr_str, description_str}:
                for fm_attr_key, fm_attr_value in fm_attribute_dict.items():
                    calc_by_conpute_value = fm_attr_value.get("calc_by_conpute")
                    assertion_fail_str = (
                        f"{fm_attr_key} Value must be Boolean {calc_by_conpute_value=}"
                    )
                    assert calc_by_conpute_value in [
                        True,
                        False,
                    ], assertion_fail_str


def test_get_person_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    person_config = get_person_config_dict()

    # THEN
    prnunit_attribute = person_config.get(kw.personunit)
    prnptnr_attribute = person_config.get(kw.person_partnerunit)
    prnmemb_attribute = person_config.get(kw.person_partner_membership)
    prnplan_attribute = person_config.get(kw.person_planunit)
    prnawar_attribute = person_config.get(kw.person_plan_awardunit)
    prnreas_attribute = person_config.get(kw.person_plan_reasonunit)
    prncase_attribute = person_config.get(kw.person_plan_reason_caseunit)
    prnlabo_attribute = person_config.get(kw.person_plan_laborunit)
    prnheal_attribute = person_config.get(kw.person_plan_healerunit)
    prnfact_attribute = person_config.get(kw.person_plan_factunit)
    prngrou_attribute = person_config.get(kw.person_groupunit)
    abbr_str = "abbreviation"
    assert prnunit_attribute.get(abbr_str) == kw.prnunit
    assert prnptnr_attribute.get(abbr_str) == kw.prnptnr
    assert prnmemb_attribute.get(abbr_str) == kw.prnmemb
    assert prnplan_attribute.get(abbr_str) == kw.prnplan
    assert prnawar_attribute.get(abbr_str) == kw.prnawar
    assert prnreas_attribute.get(abbr_str) == kw.prnreas
    assert prncase_attribute.get(abbr_str) == kw.prncase
    assert prnlabo_attribute.get(abbr_str) == kw.prnlabo
    assert prnheal_attribute.get(abbr_str) == kw.prnheal
    assert prnfact_attribute.get(abbr_str) == kw.prnfact
    assert prngrou_attribute.get(abbr_str) == kw.prngrou


def test_get_all_person_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_person_calc_args = get_all_person_calc_args()

    # THEN
    assert all_person_calc_args
    assert kw.stop_want in all_person_calc_args
    assert kw.plan_rope in all_person_calc_args
    assert kw.fund_give in all_person_calc_args
    assert kw.case_task in all_person_calc_args
    assert kw.reason_task in all_person_calc_args
    assert kw.plan_task in all_person_calc_args
    assert all_person_calc_args.get(kw.fund_give) == {
        kw.person_plan_awardunit,
        kw.person_partner_membership,
        kw.person_groupunit,
        kw.person_partnerunit,
    }

    assert len(all_person_calc_args) == 79


def test_get_person_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    person_config = get_person_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, attribute_dict in person_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key in {kw.jkeys, kw.jvalues}:
                for level3_key, attr_dict in fm_attribute_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {
                        kw.class_type,
                        kw.sqlite_datatype,
                        kw.calc_by_conpute,
                    }


def test_get_person_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    person_calc_dimens = get_person_calc_dimens()

    # THEN
    expected_person_calc_dimens = {
        kw.personunit,
        kw.person_partnerunit,
        kw.person_partner_membership,
        kw.person_planunit,
        kw.person_plan_awardunit,
        kw.person_plan_reasonunit,
        kw.person_plan_reason_caseunit,
        kw.person_plan_laborunit,
        kw.person_plan_healerunit,
        kw.person_plan_factunit,
        kw.person_groupunit,
    }
    assert person_calc_dimens == expected_person_calc_dimens
    assert person_calc_dimens == set(get_person_config_dict().keys())


def test_get_person_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    person_partnerunit_args = get_person_calc_dimen_args(kw.person_partnerunit)
    person_planunit_args = get_person_calc_dimen_args(kw.person_planunit)
    person_groupunit_args = get_person_calc_dimen_args(kw.person_groupunit)

    #  THEN
    print(f"          {person_partnerunit_args=}")
    print("")
    print(f"{set(PartnerUnit().__dict__.keys())=}")
    # print(person_partnerunit_args.difference(set(PartnerUnit().__dict__.keys())))
    # assert person_partnerunit_args == set(PartnerUnit().__dict__.keys())
    assert person_partnerunit_args == {
        kw.person_name,
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_give,
        kw.fund_take,
        kw.partner_cred_lumen,
        kw.partner_debt_lumen,
        kw.partner_name,
        kw.inallocable_partner_debt_lumen,
        kw.irrational_partner_debt_lumen,
        kw.groupmark,
    }
    assert person_planunit_args == {
        kw.person_name,
        kw.morph,
        kw.denom,
        kw.pledge,
        kw.close,
        kw.addin,
        kw.numor,
        kw.star,
        kw.stop_want,
        kw.gogo_calc,
        kw.stop_calc,
        kw.plan_active,
        kw.fund_onset,
        kw.fund_cease,
        kw.descendant_pledge_count,
        kw.all_partner_cred,
        kw.all_partner_debt,
        kw.healerunit_ratio,
        kw.tree_level,
        kw.plan_task,
        kw.fund_grain,
        kw.fund_ratio,
        kw.range_evaluated,
        kw.problem_bool,
        kw.gogo_want,
        kw.plan_rope,
        kw.knot,
        kw.begin,
    }
    print(f"{person_groupunit_args=}")
    assert person_groupunit_args == {
        kw.person_name,
        kw.debtor_pool,
        kw.credor_pool,
        kw.fund_give,
        kw.group_title,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_take,
        kw.fund_grain,
    }


def g_class_type(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.class_type)


def g_sqlitetype(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.sqlite_datatype)


def g_popconpute(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.calc_by_conpute)


def test_get_person_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH / WHEN
    cfig = get_person_config_dict()

    # THEN
    # for level1_key, attribute_dict in config.items():
    #     for level2_key, fm_attribute_dict in attribute_dict.items():
    #         if level2_key in {kw.jkeys, kw.jvalues}:
    #             for level3_key, attr_dict in fm_attribute_dict.items():
    #                 dimem = attribute_dict.get("abbreviation")
    #                 x_class_type = attr_dict.get(kw.class_type)
    #                 x_sqlite_datatype = attr_dict.get(kw.sqlite_datatype)
    #                 print(
    #                     f"""    assert g_class_type(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_class_type}" """
    #                 )
    #                 print(
    #                     f"""    assert g_sqlitetype(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_sqlite_datatype}" """
    #                 )

    jk = kw.jkeys
    jv = kw.jvalues
    prnunit = kw.personunit
    prnptnr = kw.person_partnerunit
    prnmemb = kw.person_partner_membership
    prnplan = kw.person_planunit
    prnawar = kw.person_plan_awardunit
    prnreas = kw.person_plan_reasonunit
    prncase = kw.person_plan_reason_caseunit
    prnlabo = kw.person_plan_laborunit
    prnheal = kw.person_plan_healerunit
    prnfact = kw.person_plan_factunit
    prngrou = kw.person_groupunit
    assert g_class_type(cfig, prnmemb, jk, kw.partner_name) == kw.NameTerm
    assert g_sqlitetype(cfig, prnmemb, jk, kw.partner_name) == "TEXT"
    assert g_popconpute(cfig, prnmemb, jk, kw.partner_name) == False

    assert g_class_type(cfig, prnmemb, jk, kw.group_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, prnmemb, jk, kw.group_title) == "TEXT"
    assert g_popconpute(cfig, prnmemb, jk, kw.group_title) == False

    assert g_class_type(cfig, prnmemb, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.credor_pool) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.credor_pool) == True

    assert g_class_type(cfig, prnmemb, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.debtor_pool) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, prnmemb, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.fund_agenda_give) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, prnmemb, jv, kw.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.fund_agenda_ratio_give) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, prnmemb, jv, kw.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.fund_agenda_ratio_take) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, prnmemb, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.fund_agenda_take) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, prnmemb, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.fund_give) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.fund_give) == True

    assert g_class_type(cfig, prnmemb, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.fund_take) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.fund_take) == True

    assert g_class_type(cfig, prnmemb, jv, kw.group_cred_lumen) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.group_cred_lumen) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.group_cred_lumen) == False

    assert g_class_type(cfig, prnmemb, jv, kw.group_debt_lumen) == "float"
    assert g_sqlitetype(cfig, prnmemb, jv, kw.group_debt_lumen) == "REAL"
    assert g_popconpute(cfig, prnmemb, jv, kw.group_debt_lumen) == False

    assert g_class_type(cfig, prnptnr, jk, kw.partner_name) == kw.NameTerm
    assert g_sqlitetype(cfig, prnptnr, jk, kw.partner_name) == "TEXT"
    assert g_popconpute(cfig, prnptnr, jk, kw.partner_name) == False

    assert g_class_type(cfig, prnptnr, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.credor_pool) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.credor_pool) == True

    assert g_class_type(cfig, prnptnr, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.debtor_pool) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, prnptnr, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.fund_agenda_give) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, prnptnr, jv, kw.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.fund_agenda_ratio_give) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, prnptnr, jv, kw.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.fund_agenda_ratio_take) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, prnptnr, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.fund_agenda_take) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, prnptnr, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.fund_give) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.fund_give) == True

    assert g_class_type(cfig, prnptnr, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.fund_take) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.fund_take) == True

    assert g_class_type(cfig, prnptnr, jv, kw.inallocable_partner_debt_lumen) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.inallocable_partner_debt_lumen) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.inallocable_partner_debt_lumen) == True

    assert g_class_type(cfig, prnptnr, jv, kw.irrational_partner_debt_lumen) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.irrational_partner_debt_lumen) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.irrational_partner_debt_lumen) == True

    assert g_class_type(cfig, prnptnr, jv, kw.partner_cred_lumen) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.partner_cred_lumen) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.partner_cred_lumen) == False

    assert g_class_type(cfig, prnptnr, jv, kw.partner_debt_lumen) == "float"
    assert g_sqlitetype(cfig, prnptnr, jv, kw.partner_debt_lumen) == "REAL"
    assert g_popconpute(cfig, prnptnr, jv, kw.partner_debt_lumen) == False

    assert g_class_type(cfig, prngrou, jk, kw.group_title) == "TitleTerm"
    assert g_sqlitetype(cfig, prngrou, jk, kw.group_title) == "TEXT"
    assert g_popconpute(cfig, prngrou, jk, kw.group_title) == True

    assert g_class_type(cfig, prngrou, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.debtor_pool) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, prngrou, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.credor_pool) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.credor_pool) == True

    assert g_class_type(cfig, prngrou, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.fund_give) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.fund_give) == True

    assert g_class_type(cfig, prngrou, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.fund_agenda_give) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, prngrou, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.fund_agenda_take) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, prngrou, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.fund_take) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.fund_take) == True

    assert g_class_type(cfig, prngrou, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, prngrou, jv, kw.fund_grain) == "REAL"
    assert g_popconpute(cfig, prngrou, jv, kw.fund_grain) == True

    assert g_class_type(cfig, prnawar, jk, kw.awardee_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, prnawar, jk, kw.awardee_title) == "TEXT"
    assert g_popconpute(cfig, prnawar, jk, kw.awardee_title) == False

    assert g_class_type(cfig, prnawar, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnawar, jk, kw.plan_rope) == "TEXT"
    assert g_popconpute(cfig, prnawar, jk, kw.plan_rope) == False

    assert g_class_type(cfig, prnawar, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, prnawar, jv, kw.fund_give) == "REAL"
    assert g_popconpute(cfig, prnawar, jv, kw.fund_give) == True

    assert g_class_type(cfig, prnawar, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, prnawar, jv, kw.fund_take) == "REAL"
    assert g_popconpute(cfig, prnawar, jv, kw.fund_take) == True

    assert g_class_type(cfig, prnawar, jv, kw.give_force) == "float"
    assert g_sqlitetype(cfig, prnawar, jv, kw.give_force) == "REAL"
    assert g_popconpute(cfig, prnawar, jv, kw.give_force) == False

    assert g_class_type(cfig, prnawar, jv, kw.take_force) == "float"
    assert g_sqlitetype(cfig, prnawar, jv, kw.take_force) == "REAL"
    assert g_popconpute(cfig, prnawar, jv, kw.take_force) == False

    assert g_class_type(cfig, prnfact, jk, kw.fact_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnfact, jk, kw.fact_context) == "TEXT"
    assert g_popconpute(cfig, prnfact, jk, kw.fact_context) == False

    assert g_class_type(cfig, prnfact, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnfact, jk, kw.plan_rope) == "TEXT"
    assert g_popconpute(cfig, prnfact, jk, kw.plan_rope) == False

    assert g_class_type(cfig, prnfact, jv, kw.fact_upper) == kw.FactNum
    assert g_sqlitetype(cfig, prnfact, jv, kw.fact_upper) == "REAL"
    assert g_popconpute(cfig, prnfact, jv, kw.fact_upper) == False

    assert g_class_type(cfig, prnfact, jv, kw.fact_lower) == kw.FactNum
    assert g_sqlitetype(cfig, prnfact, jv, kw.fact_lower) == "REAL"
    assert g_popconpute(cfig, prnfact, jv, kw.fact_lower) == False

    assert g_class_type(cfig, prnfact, jv, kw.fact_state) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnfact, jv, kw.fact_state) == "TEXT"
    assert g_popconpute(cfig, prnfact, jv, kw.fact_state) == False

    assert g_class_type(cfig, prnheal, jk, kw.healer_name) == kw.NameTerm
    assert g_sqlitetype(cfig, prnheal, jk, kw.healer_name) == "TEXT"
    assert g_popconpute(cfig, prnheal, jk, kw.healer_name) == False

    assert g_class_type(cfig, prnheal, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnheal, jk, kw.plan_rope) == "TEXT"
    assert g_popconpute(cfig, prnheal, jk, kw.plan_rope) == False

    assert g_class_type(cfig, prncase, jk, kw.reason_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, prncase, jk, kw.reason_context) == "TEXT"
    assert g_popconpute(cfig, prncase, jk, kw.reason_context) == False

    assert g_class_type(cfig, prncase, jk, kw.reason_state) == kw.RopeTerm
    assert g_sqlitetype(cfig, prncase, jk, kw.reason_state) == "TEXT"
    assert g_popconpute(cfig, prncase, jk, kw.reason_state) == False

    assert g_class_type(cfig, prncase, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, prncase, jk, kw.plan_rope) == "TEXT"
    assert g_popconpute(cfig, prncase, jk, kw.plan_rope) == False

    assert g_class_type(cfig, prncase, jv, kw.case_active) == "int"
    assert g_sqlitetype(cfig, prncase, jv, kw.case_active) == "INTEGER"
    assert g_popconpute(cfig, prncase, jv, kw.case_active) == True

    assert g_class_type(cfig, prncase, jv, kw.case_task) == "bool"
    assert g_sqlitetype(cfig, prncase, jv, kw.case_task) == "INTEGER"
    assert g_popconpute(cfig, prncase, jv, kw.case_task) == True

    assert g_class_type(cfig, prncase, jv, kw.reason_divisor) == "int"
    assert g_sqlitetype(cfig, prncase, jv, kw.reason_divisor) == "INTEGER"
    assert g_popconpute(cfig, prncase, jv, kw.reason_divisor) == False

    assert g_class_type(cfig, prncase, jv, kw.reason_upper) == kw.ReasonNum
    assert g_sqlitetype(cfig, prncase, jv, kw.reason_upper) == "REAL"
    assert g_popconpute(cfig, prncase, jv, kw.reason_upper) == False

    assert g_class_type(cfig, prncase, jv, kw.reason_lower) == kw.ReasonNum
    assert g_sqlitetype(cfig, prncase, jv, kw.reason_lower) == "REAL"
    assert g_popconpute(cfig, prncase, jv, kw.reason_lower) == False

    assert g_class_type(cfig, prnreas, jk, kw.reason_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnreas, jk, kw.reason_context) == "TEXT"
    assert g_popconpute(cfig, prnreas, jk, kw.reason_context) == False

    assert g_class_type(cfig, prnreas, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnreas, jk, kw.plan_rope) == "TEXT"
    assert g_popconpute(cfig, prnreas, jk, kw.plan_rope) == False

    assert g_class_type(cfig, prnreas, jv, kw.parent_heir_active) == "int"
    assert g_sqlitetype(cfig, prnreas, jv, kw.parent_heir_active) == "INTEGER"
    assert g_popconpute(cfig, prnreas, jv, kw.parent_heir_active) == True

    assert g_class_type(cfig, prnreas, jv, kw.reason_active) == "int"
    assert g_sqlitetype(cfig, prnreas, jv, kw.reason_active) == "INTEGER"
    assert g_popconpute(cfig, prnreas, jv, kw.reason_active) == True

    assert g_class_type(cfig, prnreas, jv, kw.reason_task) == "bool"
    assert g_sqlitetype(cfig, prnreas, jv, kw.reason_task) == "INTEGER"
    assert g_popconpute(cfig, prnreas, jv, kw.reason_task) == True

    assert g_class_type(cfig, prnreas, jv, kw.active_requisite) == "bool"
    assert g_sqlitetype(cfig, prnreas, jv, kw.active_requisite) == "INTEGER"
    assert g_popconpute(cfig, prnreas, jv, kw.active_requisite) == False

    assert g_class_type(cfig, prnlabo, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, prnlabo, jk, kw.plan_rope) == "TEXT"
    assert g_popconpute(cfig, prnlabo, jk, kw.plan_rope) == False

    assert g_class_type(cfig, prnlabo, jk, kw.labor_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, prnlabo, jk, kw.labor_title) == "TEXT"
    assert g_popconpute(cfig, prnlabo, jk, kw.labor_title) == False

    assert g_class_type(cfig, prnlabo, jv, kw.person_name_is_workforce) == "int"
    assert g_sqlitetype(cfig, prnlabo, jv, kw.person_name_is_workforce) == "INTEGER"
    assert g_popconpute(cfig, prnlabo, jv, kw.person_name_is_workforce) == True

    assert g_class_type(cfig, prnplan, jv, kw.plan_active) == "bool"
    assert g_sqlitetype(cfig, prnplan, jv, kw.plan_active) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.plan_active) == True

    assert g_class_type(cfig, prnplan, jv, kw.all_partner_cred) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.all_partner_cred) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.all_partner_cred) == True

    assert g_class_type(cfig, prnplan, jv, kw.all_partner_debt) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.all_partner_debt) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.all_partner_debt) == True

    assert g_class_type(cfig, prnplan, jv, kw.descendant_pledge_count) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.descendant_pledge_count) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.descendant_pledge_count) == True

    assert g_class_type(cfig, prnplan, jv, kw.fund_cease) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.fund_cease) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.fund_cease) == True

    assert g_class_type(cfig, prnplan, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.fund_grain) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.fund_grain) == True

    assert g_class_type(cfig, prnplan, jv, kw.fund_onset) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.fund_onset) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.fund_onset) == True

    assert g_class_type(cfig, prnplan, jv, kw.fund_ratio) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.fund_ratio) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.fund_ratio) == True

    assert g_class_type(cfig, prnplan, jv, kw.gogo_calc) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.gogo_calc) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.gogo_calc) == True

    assert g_class_type(cfig, prnplan, jv, kw.healerunit_ratio) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.healerunit_ratio) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.healerunit_ratio) == True

    assert g_class_type(cfig, prnplan, jv, kw.tree_level) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.tree_level) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.tree_level) == True

    assert g_class_type(cfig, prnplan, jv, kw.range_evaluated) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.range_evaluated) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.range_evaluated) == True

    assert g_class_type(cfig, prnplan, jv, kw.stop_calc) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.stop_calc) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.stop_calc) == True

    assert g_class_type(cfig, prnplan, jv, kw.plan_task) == "bool"
    assert g_sqlitetype(cfig, prnplan, jv, kw.plan_task) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.plan_task) == True

    assert g_class_type(cfig, prnplan, jv, kw.addin) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.addin) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.addin) == False

    assert g_class_type(cfig, prnplan, jv, kw.begin) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.begin) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.begin) == False

    assert g_class_type(cfig, prnplan, jv, kw.close) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.close) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.close) == False

    assert g_class_type(cfig, prnplan, jv, kw.denom) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.denom) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.denom) == False

    assert g_class_type(cfig, prnplan, jv, kw.gogo_want) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.gogo_want) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.gogo_want) == False

    assert g_class_type(cfig, prnplan, jv, kw.star) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.star) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.star) == False

    assert g_class_type(cfig, prnplan, jv, kw.morph) == "bool"
    assert g_sqlitetype(cfig, prnplan, jv, kw.morph) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.morph) == False

    assert g_class_type(cfig, prnplan, jv, kw.numor) == "int"
    assert g_sqlitetype(cfig, prnplan, jv, kw.numor) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.numor) == False

    assert g_class_type(cfig, prnplan, jv, kw.pledge) == "bool"
    assert g_sqlitetype(cfig, prnplan, jv, kw.pledge) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.pledge) == False

    assert g_class_type(cfig, prnplan, jv, kw.problem_bool) == "bool"
    assert g_sqlitetype(cfig, prnplan, jv, kw.problem_bool) == "INTEGER"
    assert g_popconpute(cfig, prnplan, jv, kw.problem_bool) == False

    assert g_class_type(cfig, prnplan, jv, kw.stop_want) == "float"
    assert g_sqlitetype(cfig, prnplan, jv, kw.stop_want) == "REAL"
    assert g_popconpute(cfig, prnplan, jv, kw.stop_want) == False

    assert g_class_type(cfig, prnunit, jv, "keeps_buildable") == "int"
    assert g_sqlitetype(cfig, prnunit, jv, "keeps_buildable") == "INTEGER"
    assert g_popconpute(cfig, prnunit, jv, "keeps_buildable") == True

    assert g_class_type(cfig, prnunit, jv, "keeps_justified") == "int"
    assert g_sqlitetype(cfig, prnunit, jv, "keeps_justified") == "INTEGER"
    assert g_popconpute(cfig, prnunit, jv, "keeps_justified") == True

    assert g_class_type(cfig, prnunit, jv, kw.offtrack_fund) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.offtrack_fund) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.offtrack_fund) == True

    assert g_class_type(cfig, prnunit, jv, kw.rational) == "bool"
    assert g_sqlitetype(cfig, prnunit, jv, kw.rational) == "INTEGER"
    assert g_popconpute(cfig, prnunit, jv, kw.rational) == True

    assert (
        g_class_type(cfig, prnunit, jv, kw.sum_healerunit_plans_fund_total) == "float"
    )
    assert g_sqlitetype(cfig, prnunit, jv, kw.sum_healerunit_plans_fund_total) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.sum_healerunit_plans_fund_total) == True

    assert g_class_type(cfig, prnunit, jv, kw.tree_traverse_count) == "int"
    assert g_sqlitetype(cfig, prnunit, jv, kw.tree_traverse_count) == "INTEGER"
    assert g_popconpute(cfig, prnunit, jv, kw.tree_traverse_count) == True

    assert g_class_type(cfig, prnunit, jv, kw.credor_respect) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.credor_respect) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.credor_respect) == False

    assert g_class_type(cfig, prnunit, jv, kw.debtor_respect) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.debtor_respect) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.debtor_respect) == False

    assert g_class_type(cfig, prnunit, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.fund_grain) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.fund_grain) == False

    assert g_class_type(cfig, prnunit, jv, kw.fund_pool) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.fund_pool) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.fund_pool) == False

    assert g_class_type(cfig, prnunit, jv, kw.max_tree_traverse) == "int"
    assert g_sqlitetype(cfig, prnunit, jv, kw.max_tree_traverse) == "INTEGER"
    assert g_popconpute(cfig, prnunit, jv, kw.max_tree_traverse) == False

    assert g_class_type(cfig, prnunit, jv, kw.mana_grain) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.mana_grain) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.mana_grain) == False

    assert g_class_type(cfig, prnunit, jv, kw.respect_grain) == "float"
    assert g_sqlitetype(cfig, prnunit, jv, kw.respect_grain) == "REAL"
    assert g_popconpute(cfig, prnunit, jv, kw.respect_grain) == False


def test_get_person_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    person_config_dict = get_person_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for person_calc_dimen, dimen_dict in person_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {kw.jkeys, kw.jvalues}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN / THEN
    for x_arg, arg_types in all_args.items():
        # print(f"{x_arg=} {arg_types=}")
        assertion_failure_str = f"{x_arg=} {arg_types=}"
        assert len(arg_types) == 1, assertion_failure_str


def test_get_person_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    person_config_dict = get_person_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for person_calc_dimen, dimen_dict in person_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {kw.jkeys, kw.jvalues}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.sqlite_datatype)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    for x_arg, arg_types in all_args.items():
        # print(f"{x_arg=} {arg_types=}")
        assertion_failure_str = f"{x_arg=} {arg_types=}"
        assert len(arg_types) == 1, assertion_failure_str

    # WHEN
    sqlite_datatype_dict = get_person_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert person_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        # print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert_failure_str = f""""{x_arg}": "{list(arg_types)[0]}","""
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg), assert_failure_str
    all_args_set = set(all_args.keys())
    sqlite_args_set = set(sqlite_datatype_dict.keys())
    all_args_set.add(kw.knot)
    print(sqlite_args_set.difference(all_args))
    assert all_args_set == sqlite_args_set


def test_get_person_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    person_config_dict = get_person_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for person_calc_dimen, dimen_dict in person_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {kw.jkeys, kw.jvalues}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    person_calc_args_type_dict = get_person_calc_args_type_dict()

    # THEN
    assert person_calc_args_type_dict.get(kw.partner_name) == kw.NameTerm
    assert person_calc_args_type_dict.get(kw.group_title) == kw.TitleTerm
    assert person_calc_args_type_dict.get(kw.case_active) == "int"
    assert person_calc_args_type_dict.get(kw.credor_pool) == "float"
    assert person_calc_args_type_dict.get(kw.debtor_pool) == "float"
    assert person_calc_args_type_dict.get(kw.fund_agenda_give) == "float"
    assert person_calc_args_type_dict.get(kw.fund_agenda_ratio_give) == "float"
    assert person_calc_args_type_dict.get(kw.fund_agenda_ratio_take) == "float"
    assert person_calc_args_type_dict.get(kw.fund_agenda_take) == "float"
    assert person_calc_args_type_dict.get(kw.fund_give) == "float"
    assert person_calc_args_type_dict.get(kw.fund_take) == "float"
    assert person_calc_args_type_dict.get(kw.group_cred_lumen) == "int"
    assert person_calc_args_type_dict.get(kw.group_debt_lumen) == "int"
    assert person_calc_args_type_dict.get(kw.inallocable_partner_debt_lumen) == "float"
    assert person_calc_args_type_dict.get(kw.irrational_partner_debt_lumen) == "float"
    assert person_calc_args_type_dict.get(kw.partner_cred_lumen) == "float"
    assert person_calc_args_type_dict.get(kw.partner_debt_lumen) == "float"
    assert person_calc_args_type_dict.get(kw.addin) == "float"
    assert person_calc_args_type_dict.get(kw.begin) == "float"
    assert person_calc_args_type_dict.get(kw.close) == "float"
    assert person_calc_args_type_dict.get(kw.denom) == "int"
    assert person_calc_args_type_dict.get(kw.gogo_want) == "float"
    assert person_calc_args_type_dict.get(kw.star) == "int"
    assert person_calc_args_type_dict.get(kw.morph) == "bool"
    assert person_calc_args_type_dict.get(kw.numor) == "int"
    assert person_calc_args_type_dict.get(kw.pledge) == "bool"
    assert person_calc_args_type_dict.get(kw.problem_bool) == "bool"
    assert person_calc_args_type_dict.get(kw.stop_want) == "float"
    assert person_calc_args_type_dict.get(kw.awardee_title) == kw.TitleTerm
    assert person_calc_args_type_dict.get(kw.plan_rope) == kw.RopeTerm
    assert person_calc_args_type_dict.get(kw.give_force) == "float"
    assert person_calc_args_type_dict.get(kw.take_force) == "float"
    assert person_calc_args_type_dict.get(kw.reason_context) == kw.RopeTerm
    assert person_calc_args_type_dict.get(kw.fact_upper) == kw.FactNum
    assert person_calc_args_type_dict.get(kw.fact_lower) == kw.FactNum
    assert person_calc_args_type_dict.get(kw.fact_state) == kw.RopeTerm
    assert person_calc_args_type_dict.get(kw.healer_name) == kw.NameTerm
    assert person_calc_args_type_dict.get(kw.reason_state) == kw.RopeTerm
    assert person_calc_args_type_dict.get(kw.reason_active) == "int"
    assert person_calc_args_type_dict.get(kw.case_task) == "bool"
    assert person_calc_args_type_dict.get(kw.reason_task) == "bool"
    assert person_calc_args_type_dict.get(kw.plan_task) == "bool"
    assert person_calc_args_type_dict.get(kw.reason_divisor) == "int"
    assert person_calc_args_type_dict.get(kw.reason_upper) == kw.ReasonNum
    assert person_calc_args_type_dict.get(kw.reason_lower) == kw.ReasonNum
    assert person_calc_args_type_dict.get(kw.parent_heir_active) == "int"
    assert person_calc_args_type_dict.get(kw.active_requisite) == "bool"
    assert person_calc_args_type_dict.get(kw.labor_title) == kw.TitleTerm
    assert person_calc_args_type_dict.get(kw.person_name_is_workforce) == "int"
    assert person_calc_args_type_dict.get(kw.plan_active) == "bool"
    assert person_calc_args_type_dict.get(kw.all_partner_cred) == "int"
    assert person_calc_args_type_dict.get(kw.all_partner_debt) == "int"
    assert person_calc_args_type_dict.get(kw.descendant_pledge_count) == "int"
    assert person_calc_args_type_dict.get(kw.fund_cease) == "float"
    assert person_calc_args_type_dict.get(kw.fund_onset) == "float"
    assert person_calc_args_type_dict.get(kw.fund_ratio) == "float"
    assert person_calc_args_type_dict.get(kw.gogo_calc) == "float"
    assert person_calc_args_type_dict.get(kw.healerunit_ratio) == "float"
    assert person_calc_args_type_dict.get(kw.tree_level) == "int"
    assert person_calc_args_type_dict.get(kw.range_evaluated) == "int"
    assert person_calc_args_type_dict.get(kw.stop_calc) == "float"
    assert person_calc_args_type_dict.get(kw.keeps_buildable) == "int"
    assert person_calc_args_type_dict.get(kw.keeps_justified) == "int"
    assert person_calc_args_type_dict.get(kw.offtrack_fund) == "int"
    assert person_calc_args_type_dict.get(kw.rational) == "bool"
    assert person_calc_args_type_dict.get(kw.sum_healerunit_plans_fund_total) == "float"
    assert person_calc_args_type_dict.get(kw.tree_traverse_count) == "int"
    assert person_calc_args_type_dict.get(kw.credor_respect) == "float"
    assert person_calc_args_type_dict.get(kw.debtor_respect) == "float"
    assert person_calc_args_type_dict.get(kw.fund_grain) == "float"
    assert person_calc_args_type_dict.get(kw.fund_pool) == "float"
    assert person_calc_args_type_dict.get(kw.max_tree_traverse) == "int"
    assert person_calc_args_type_dict.get(kw.mana_grain) == "float"
    assert person_calc_args_type_dict.get(kw.respect_grain) == "float"
    assert person_calc_args_type_dict.get(kw.knot) == "KnotTerm"
    assert len(person_calc_args_type_dict) == 75
