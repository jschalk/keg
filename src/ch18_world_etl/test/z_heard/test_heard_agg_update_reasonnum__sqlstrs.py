from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_update_heard_agg_timenum_sqlstr,
    get_update_heard_agg_timenum_sqlstrs,
    get_update_prncase_context_plan_sqlstr,
    get_update_prncase_inx_epoch_diff_sqlstr,
    get_update_prncase_range_sqlstr,
    get_update_prnfact_context_plan_sqlstr,
    get_update_prnfact_inx_epoch_diff_sqlstr,
    get_update_prnfact_range_sqlstr,
    update_heard_agg_timenum_columns,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_update_prncase_inx_epoch_diff_sqlstr_ReturnsObj():
    # ESTABLISH
    prncase_tablename = prime_tbl(kw.prncase, "h", "agg", "put")
    nabtime_tablename = prime_tbl(kw.nabtime, "h", "agg")

    # WHEN
    update_sqlstr = get_update_prncase_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabtime_tablename}
    GROUP BY spark_num, otx_time, inx_time
)
UPDATE {prncase_tablename}
SET inx_epoch_diff = spark_inx_epoch_diff.inx_epoch_diff
FROM spark_inx_epoch_diff
WHERE {prncase_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_prnfact_inx_epoch_diff_sqlstr_ReturnsObj():
    # ESTABLISH
    prnfact_tablename = prime_tbl(kw.prnfact, "h", "agg", "put")
    nabtime_tablename = prime_tbl(kw.nabtime, "h", "agg")

    # WHEN
    update_sqlstr = get_update_prnfact_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabtime_tablename}
    GROUP BY spark_num, otx_time, inx_time
)
UPDATE {prnfact_tablename}
SET inx_epoch_diff = spark_inx_epoch_diff.inx_epoch_diff
FROM spark_inx_epoch_diff
WHERE {prnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


# def test_get_update_prncase_context_plan_sqlstr_ReturnsObj():
# TODO reactivate
#     # ESTABLISH
#     prncase_tablename = prime_tbl(kw.person_plan_reason_caseunit, "h", "agg", "put")
#     prnplan_tablename = prime_tbl(kw.person_planunit, "h", "agg", "put")

#     # WHEN
#     update_sqlstr = get_update_prncase_context_plan_sqlstr()

#     # THEN
#     assert update_sqlstr
#     expected_update_sqlstr = f"""
# WITH spark_prnplan AS (
#     SELECT {kw.spark_num}, {kw.close}, {kw.denom}, {kw.morph}
#     FROM {prnplan_tablename}
#     GROUP BY {kw.spark_num}, {kw.close}, {kw.denom}, {kw.morph}
# )
# UPDATE {prncase_tablename}
# SET
#   context_plan_close = spark_prnplan.{kw.close}
# , context_plan_denom = spark_prnplan.{kw.denom}
# , context_plan_morph = spark_prnplan.{kw.morph}
# FROM spark_prnplan
# WHERE {prncase_tablename}.spark_num IN (SELECT spark_num FROM spark_prnplan)
# ;
# """
#     print(expected_update_sqlstr)
#     assert update_sqlstr == expected_update_sqlstr

# TODO reactivate test
# def test_get_update_prnfact_context_plan_sqlstr_ReturnsObj():
#     # ESTABLISH
#     prnfact_tablename = prime_tbl(kw.prnfact, "h", "agg", "put")
#     prnplan_tablename = prime_tbl(kw.person_planunit, "h", "agg", "put")

#     # WHEN
#     update_sqlstr = get_update_prnfact_context_plan_sqlstr()

#     # THEN
#     assert update_sqlstr
#     expected_update_sqlstr = f"""
# WITH spark_prnplan AS (
#     SELECT spark_num, close, denom, morph
#     FROM {prnplan_tablename}
#     GROUP BY spark_num, close, denom, morph
# )
# UPDATE {prnfact_tablename}
# SET
#   context_plan_close = spark_prnplan.close
# , context_plan_denom = spark_prnplan.denom
# , context_plan_morph = spark_prnplan.morph
# FROM spark_prnplan
# WHERE {prnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_prnplan)
# ;
# """
#     print(expected_update_sqlstr)
#     assert update_sqlstr == expected_update_sqlstr


def test_get_update_prncase_range_sqlstr_ReturnsObj():
    # ESTABLISH
    prncase_tablename = prime_tbl(kw.person_plan_reason_caseunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_prncase_range_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_prncase AS (
    SELECT 
      spark_num
    , IFNULL(reason_divisor, IFNULL(context_plan_close, context_plan_denom)) modulus
    , CASE WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_plan_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
    FROM {prncase_tablename}
    GROUP BY spark_num, reason_divisor, context_plan_close, context_plan_denom, context_plan_morph
)
UPDATE {prncase_tablename}
SET 
  reason_lower_inx = (reason_lower_otx + spark_prncase.calc_epoch_diff) % spark_prncase.modulus
, reason_upper_inx = (reason_upper_otx + spark_prncase.calc_epoch_diff) % spark_prncase.modulus
FROM spark_prncase
WHERE {prncase_tablename}.spark_num IN (SELECT spark_num FROM spark_prncase)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_prnfact_range_sqlstr_ReturnsObj():
    # ESTABLISH
    prnfact_tablename = prime_tbl(kw.prnfact, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_prnfact_range_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_prnfact AS (
    SELECT 
      spark_num
    , IFNULL(reason_divisor, IFNULL(context_plan_close, context_plan_denom)) modulus
    , FACT WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_plan_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
    FROM {prnfact_tablename}
    GROUP BY spark_num, reason_divisor, context_plan_close, context_plan_denom, context_plan_morph
)
UPDATE {prnfact_tablename}
SET 
  reason_lower_inx = (reason_lower_otx + spark_prnfact.calc_epoch_diff) % spark_prnfact.modulus
, reason_upper_inx = (reason_upper_otx + spark_prnfact.calc_epoch_diff) % spark_prnfact.modulus
FROM spark_prnfact
WHERE {prnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_prnfact)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


# TODO create function that updates all nabuable otx fields.
# identify the change
# update semantic_type: ReasonNum person_plan_reason_caseunit_h_agg_put reason_lower, reason_upper
# update semantic_type: ReasonNum person_plan_factunit_h_agg_put fact_lower, fact_upper
