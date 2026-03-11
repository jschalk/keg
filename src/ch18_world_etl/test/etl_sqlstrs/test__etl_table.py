from os import getcwd as os_getcwd
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.idea_config import get_idea_config_dict
from src.ch18_world_etl.etl_config import (
    ALL_DIMEN_ABBV2,
    ALL_DIMEN_ABBV7,
    create_prime_table_sqlstr,
    create_prime_tablename,
    etl_idea_category_config_dict,
    etl_idea_category_config_path,
    get_all_dimen_columns_set,
    get_del_dimen_columns_set,
    get_dimen_abbv2,
    get_dimen_abbv7,
    get_etl_category_stages_dict,
    get_prime_columns,
    remove_inx_columns,
    remove_otx_columns,
    remove_staging_columns,
)
from src.ref.keywords import Ch18Keywords as kw


def test_remove_otx_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert remove_otx_columns({"fizz", "buzz"}) == {"fizz", "buzz"}
    assert remove_otx_columns({"fizz", "buzz_otx"}) == {"fizz"}
    assert remove_otx_columns({"fizz_otx", "otx_buzz"}) == {"otx_buzz"}


def test_remove_inx_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert remove_inx_columns({"fizz", "buzz"}) == {"fizz", "buzz"}
    assert remove_inx_columns({"fizz", "buzz_inx"}) == {"fizz"}
    assert remove_inx_columns({"fizz_inx", "inx_buzz"}) == {"inx_buzz"}


def test_remove_staging_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert remove_staging_columns({"fizz", "buzz"}) == {"fizz", "buzz"}
    assert remove_staging_columns({"fizz", "inx_epoch_diff"}) == {"fizz"}
    assert remove_staging_columns({"context_plan_close", "inx_buzz"}) == {"inx_buzz"}


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH
    idea_config_keys = set(get_idea_config_dict().keys())
    idea_config_keys.add("translate_core")

    # WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(idea_config_keys)


def test_get_dimen_abbv7_HasAll_dimens():
    # ESTABLISH / WHEN / THEN
    for idea_dimen in get_idea_config_dict().keys():
        assert get_dimen_abbv7(idea_dimen) in ALL_DIMEN_ABBV7


def test_get_dimen_abbv2_HasAll_dimens():
    # ESTABLISH / WHEN
    gen_abbv2_set = ALL_DIMEN_ABBV2

    # THEN
    expected_abbv2_set = set()
    idea_config_keys = set(get_idea_config_dict().keys())
    idea_config_keys.add("translate_core")
    for idea_dimen in idea_config_keys:
        abbv2 = get_dimen_abbv2(idea_dimen)
        print(f"{abbv2=}")
        assert abbv2
        expected_abbv2_set.add(abbv2)
        assert abbv2 in gen_abbv2_set

    assert gen_abbv2_set == expected_abbv2_set
    assert len(gen_abbv2_set) == len(ALL_DIMEN_ABBV7)


def test_create_prime_tablename_ReturnsObj_Scenario0_ExpectedReturns():
    # ESTABLISH
    raw_str = "raw"
    agg_str = "agg"
    vld_str = "vld"
    put_str = "put"
    del_str = "del"

    # WHEN
    prnunit_s_agg_table = create_prime_tablename(kw.prnunit, "s", agg_str, put_str)
    prnptnr_s_agg_table = create_prime_tablename(kw.prnptnr, "s", agg_str, put_str)
    prnmemb_s_agg_table = create_prime_tablename(kw.prnmemb, "s", agg_str, put_str)
    prnplan_s_agg_table = create_prime_tablename(kw.prnplan, "s", agg_str, put_str)
    prnawar_s_agg_table = create_prime_tablename(kw.prnawar, "s", agg_str, put_str)
    prnreas_s_agg_table = create_prime_tablename(kw.prnreas, "s", agg_str, put_str)
    prncase_s_agg_table = create_prime_tablename(kw.prncase, "s", agg_str, put_str)
    prnlabo_s_agg_table = create_prime_tablename(kw.prnlabo, "s", agg_str, put_str)
    prnheal_s_agg_table = create_prime_tablename(kw.prnheal, "s", agg_str, put_str)
    prnfact_s_agg_table = create_prime_tablename(kw.prnfact, "s", agg_str, put_str)
    prnfact_s_del_table = create_prime_tablename(kw.prnfact, "s", agg_str, del_str)
    mmtunit_s_agg_table = create_prime_tablename(kw.mmtunit, "s", agg_str)
    mmtpayy_s_agg_table = create_prime_tablename(kw.mmtpayy, "s", agg_str)
    mmtbudd_s_agg_table = create_prime_tablename(kw.mmtbudd, "s", agg_str)
    mmthour_s_agg_table = create_prime_tablename(kw.mmthour, "s", agg_str)
    mmtmont_s_agg_table = create_prime_tablename(kw.mmtmont, "s", agg_str)
    mmtweek_s_agg_table = create_prime_tablename(kw.mmtweek, "s", agg_str)
    mmtoffi_s_agg_table = create_prime_tablename(kw.mmtoffi, "s", agg_str)
    nabtime_s_agg_table = create_prime_tablename(kw.nabtime, "s", agg_str)
    trlname_s_agg_table = create_prime_tablename(kw.trlname, "s", agg_str)
    trllabe_s_agg_table = create_prime_tablename(kw.trllabe, "s", agg_str)
    trlrope_s_agg_table = create_prime_tablename(kw.trlrope, "s", agg_str)
    trltitl_s_agg_table = create_prime_tablename(kw.trltitl, "s", agg_str)
    trltitl_h_vld_table = create_prime_tablename(kw.trltitl, "h", vld_str)
    trltitl_s_raw_table = create_prime_tablename(kw.trltitl, "s", raw_str)
    trltitl_s_val_table = create_prime_tablename(kw.trltitl, "s", vld_str)
    trlcore_s_raw_table = create_prime_tablename(kw.trlcore, "s", raw_str)
    trlcore_s_agg_table = create_prime_tablename(kw.trlcore, "s", agg_str)
    prnptnr_job_table = create_prime_tablename(kw.prnptnr, kw.job, None)
    x_prnptnr_raw = create_prime_tablename(kw.prnptnr, "k", raw_str)
    prngrou_job_table = create_prime_tablename(kw.prngrou, kw.job, None)

    # THEN
    assert prnunit_s_agg_table == f"{kw.personunit}_s_put_agg"
    assert prnptnr_s_agg_table == f"{kw.person_partnerunit}_s_put_agg"
    assert prnmemb_s_agg_table == f"{kw.person_partner_membership}_s_put_agg"
    assert prnplan_s_agg_table == f"{kw.person_planunit}_s_put_agg"
    assert prnawar_s_agg_table == f"{kw.person_plan_awardunit}_s_put_agg"
    assert prnreas_s_agg_table == f"{kw.person_plan_reasonunit}_s_put_agg"
    assert prncase_s_agg_table == f"{kw.person_plan_reason_caseunit}_s_put_agg"
    assert prnlabo_s_agg_table == f"{kw.person_plan_partyunit}_s_put_agg"
    assert prnheal_s_agg_table == f"{kw.person_plan_healerunit}_s_put_agg"
    assert prnfact_s_agg_table == f"{kw.person_plan_factunit}_s_put_agg"
    assert prnfact_s_del_table == f"{kw.person_plan_factunit}_s_del_agg"
    assert mmtunit_s_agg_table == f"{kw.momentunit}_s_agg"
    assert mmtpayy_s_agg_table == f"{kw.moment_paybook}_s_agg"
    assert mmtbudd_s_agg_table == f"{kw.moment_budunit}_s_agg"
    assert mmthour_s_agg_table == f"{kw.moment_epoch_hour}_s_agg"
    assert mmtmont_s_agg_table == f"{kw.moment_epoch_month}_s_agg"
    assert mmtweek_s_agg_table == f"{kw.moment_epoch_weekday}_s_agg"
    assert mmtoffi_s_agg_table == f"{kw.moment_timeoffi}_s_agg"
    assert nabtime_s_agg_table == f"{kw.nabu_timenum}_s_agg"
    assert trlname_s_agg_table == f"{kw.translate_name}_s_agg"
    assert trllabe_s_agg_table == f"{kw.translate_label}_s_agg"
    assert trlrope_s_agg_table == f"{kw.translate_rope}_s_agg"
    assert trltitl_s_agg_table == f"{kw.translate_title}_s_agg"
    assert trltitl_h_vld_table == f"{kw.translate_title}_h_vld"
    assert trltitl_s_raw_table == f"{kw.translate_title}_s_raw"
    assert trltitl_s_val_table == f"{kw.translate_title}_s_vld"
    assert trlcore_s_raw_table == f"{kw.translate_core}_s_raw"
    assert trlcore_s_agg_table == f"{kw.translate_core}_s_agg"
    assert prnptnr_job_table == f"{kw.person_partnerunit}_job"
    assert prngrou_job_table == f"{kw.person_groupunit}_job"
    assert x_prnptnr_raw == f"{kw.person_partnerunit}_raw"


def test_get_all_dimen_columns_set_ReturnsObj_Scenario0_idea_config_Dimens():
    # ESTABLISH
    for x_dimen in get_idea_config_dict().keys():
        # WHEN
        dimen_columns = get_all_dimen_columns_set(x_dimen)

        # THEN
        dimen_idea_config = get_idea_config_dict().get(x_dimen)
        expected_columns = set(dimen_idea_config.get(kw.jkeys).keys())
        expected_columns.update(set(dimen_idea_config.get(kw.jvalues).keys()))
        assert dimen_columns == expected_columns


def test_get_all_dimen_columns_set_ReturnsObj_Scenario1_translate_core_Dimens():
    # ESTABLISH / WHEN
    translate_core_columns = get_all_dimen_columns_set(kw.translate_core)

    # THEN
    expected_columns = {kw.face_name, kw.otx_knot, kw.inx_knot, kw.unknown_str}
    assert translate_core_columns == expected_columns


def test_etl_idea_category_config_path_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch18_world_etl")
    assert etl_idea_category_config_path() == create_path(
        chapter_dir, "etl_idea_category_config.json"
    )


def test_get_etl_idea_category_config_dict_ReturnsObj_Scenario0_IsFullyPopulated():
    # ESTABLISH / WHEN
    etl_idea_category_config = etl_idea_category_config_dict()

    # THEN
    assert etl_idea_category_config
    etl_idea_category_config_dimens = set(etl_idea_category_config.keys())
    assert kw.moment in etl_idea_category_config_dimens
    assert kw.translate_core in etl_idea_category_config_dimens
    assert kw.translate in etl_idea_category_config_dimens
    assert kw.person in etl_idea_category_config_dimens
    assert kw.nabu in etl_idea_category_config_dimens
    assert len(etl_idea_category_config_dimens) == 5


def test_get_etl_category_stages_dict_ReturnsObj():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    etl_category_stages_dict = get_etl_category_stages_dict()

    # THEN
    expected_dict = {}
    expected_count = 0
    etl_idea_category_config = etl_idea_category_config_dict()
    for idea_category, dimen_dict in etl_idea_category_config.items():
        for stage0_key, stage0_dict in dimen_dict.get("stages").items():
            for stage1_key, stage1_dict in stage0_dict.items():
                expected_count += 1
                if set(stage1_dict.keys()) == {"del", "put"}:
                    stage_key_put = f"{idea_category}_{stage0_key}_{stage1_key}_put"
                    stage_key_del = f"{idea_category}_{stage0_key}_{stage1_key}_del"
                    # print(f"{expected_count} {stage_key_put=}")
                    expected_count += 1
                    expected_dict[stage_key_put] = {
                        kw.idea_category: idea_category,
                        "stage0": stage0_key,
                        "stage1": stage1_key,
                        "put_del": "put",
                    }
                    expected_dict[stage_key_del] = {
                        kw.idea_category: idea_category,
                        "stage0": stage0_key,
                        "stage1": stage1_key,
                        "put_del": "del",
                    }
                    # print(f"{expected_count} {stage_key_del=}")
                else:
                    stage_key = f"{idea_category}_{stage0_key}_{stage1_key}"
                    expected_dict[stage_key] = {
                        kw.idea_category: idea_category,
                        "stage0": stage0_key,
                        "stage1": stage1_key,
                    }
                    # print(f"{expected_count} {stage_key=} ")
    # print(expected_dict)
    assert etl_category_stages_dict == expected_dict


def test_get_prime_columns_ReturnsObj_Scenario0_EmptyKeylist():
    # ESTABLISH
    x_dimen = kw.momentunit

    # WHEN / THEN
    assert get_prime_columns(x_dimen, [], None) == set()


def test_get_prime_columns_ReturnsObj_Scenario1_EmptyConfig():
    # ESTABLISH
    x_dimen = kw.momentunit
    table_keylist = ["h", "agg"]

    # WHEN / THEN
    assert get_prime_columns(x_dimen, table_keylist, {}) == set()


def test_get_prime_columns_ReturnsObj_Scenario2_moment_epoch_month():
    # ESTABLISH
    x_dimen = kw.moment_epoch_month
    table_keylist = ["h", "agg"]
    config_dict = get_idea_config_dict()

    # WHEN
    mmtunit_h_agg_columns = get_prime_columns(x_dimen, table_keylist, config_dict)

    # THEN
    print(f"{mmtunit_h_agg_columns}")
    assert mmtunit_h_agg_columns == {
        kw.spark_num,
        kw.moment_rope,
        kw.month_label,
        kw.face_name,
        kw.cumulative_day,
        kw.knot,
    }


def test_get_prime_columns_ReturnsObj_Scenario3_h_raw_set_translateable_otx_inx_args():
    # ESTABLISH
    x_dimen = kw.moment_epoch_month
    table_keylist = ["h", "raw"]
    config_dict = etl_idea_category_config_dict()

    # WHEN
    mmtepoc_h_raw_columns = get_prime_columns(x_dimen, table_keylist, config_dict)

    # THEN
    print(f"{mmtepoc_h_raw_columns}")
    assert mmtepoc_h_raw_columns == {
        kw.spark_num,
        f"{kw.moment_rope}_otx",
        f"{kw.moment_rope}_inx",
        f"{kw.month_label}_otx",
        f"{kw.month_label}_inx",
        f"{kw.face_name}_otx",
        f"{kw.face_name}_inx",
        kw.cumulative_day,
        kw.error_message,
        kw.knot,
    }


def test_get_prime_columns_ReturnsObj_Scenario4_h_agg_set_nabuable_otx_inx_args():
    # ESTABLISH
    x_dimen = kw.moment_timeoffi
    table_keylist = ["h", "agg"]
    config_dict = etl_idea_category_config_dict()

    # WHEN
    mmtoffi_h_agg_columns = get_prime_columns(x_dimen, table_keylist, config_dict)

    # THEN
    print(f"{mmtoffi_h_agg_columns=}")
    assert mmtoffi_h_agg_columns == {
        kw.face_name,
        kw.moment_rope,
        f"{kw.offi_time}_otx",
        f"{kw.offi_time}_inx",
        kw.spark_num,
        kw.knot,
    }


def test_get_prime_columns_ReturnsObj_Scenario5_h_agg_set_nabuable_otx_inx_args_ContextNabuableArgs():
    # ESTABLISH
    x_dimen = kw.person_plan_reason_caseunit
    table_keylist = ["h", "agg", "put"]
    config_dict = etl_idea_category_config_dict()

    # WHEN
    prncase_h_agg_columns = get_prime_columns(x_dimen, table_keylist, config_dict)

    # THEN
    print(f"{prncase_h_agg_columns=}")
    assert prncase_h_agg_columns
    expected_added_columns = {
        f"context_plan_{kw.close}",
        f"context_plan_{kw.denom}",
        f"context_plan_{kw.morph}",
        kw.inx_epoch_diff,
    }
    assert expected_added_columns.issubset(prncase_h_agg_columns)
    assert prncase_h_agg_columns == {
        kw.person_name,
        f"context_plan_{kw.close}",
        f"context_plan_{kw.denom}",
        f"context_plan_{kw.morph}",
        kw.face_name,
        kw.inx_epoch_diff,
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
        kw.reason_divisor,
        f"{kw.reason_lower}_otx",
        f"{kw.reason_lower}_inx",
        f"{kw.reason_upper}_otx",
        f"{kw.reason_upper}_inx",
        kw.spark_num,
        kw.knot,
    }


def test_get_del_dimen_columns_set_ReturnsObj_Scenario0() -> list[str]:
    # ESTABLISH / WHEN
    del_dimen_columns_set = get_del_dimen_columns_set(kw.person_plan_partyunit)

    # THEN
    assert del_dimen_columns_set
    assert del_dimen_columns_set == {
        kw.plan_rope,
        kw.spark_num,
        kw.person_name,
        kw.face_name,
        f"{kw.party_title}_ERASE",
    }


def test_create_prime_table_sqlstr_ReturnsObj_Scenario0_CaseUnit():
    # ESTABLISH / WHEN
    table_sqlstr = create_prime_table_sqlstr(
        kw.person_plan_reason_caseunit, "s", "raw", "put"
    )

    # THEN
    assert table_sqlstr
    print(table_sqlstr)
    expected_sqlstr = "CREATE TABLE IF NOT EXISTS person_plan_reason_caseunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, person_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_lower REAL, reason_upper REAL, reason_divisor INTEGER, knot TEXT, error_message TEXT)"
    assert table_sqlstr == expected_sqlstr
