from pytest import mark as pytest_mark
from ch19_db_tool.sql_format import (
    format_sql,
    _rewrite_select_leading_commas,
    _rewrite_group_by_leading_commas,
    _rewrite_single_item_clauses,
)


def test_rewrite_single_item_clauses_ReturnsObj_Scenario1_MovesSingleSelectColumnOntoSelectLine() -> (
    None
):
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people"""

    expected = """SELECT alpha
FROM people"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == expected


def test_rewrite_single_item_clauses_ReturnsObj_Scenario2_MovesSingleWhereConditionOntoWhereLine() -> (
    None
):
    # ESTABLISH
    sql = """SELECT alpha
FROM people
WHERE
  age > 18"""

    expected = """SELECT alpha
FROM people
WHERE age > 18"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == expected


def test_rewrite_single_item_clauses_ReturnsObj_Scenario3_MovesSingleGroupByColumnOntoGroupByLine() -> (
    None
):
    # ESTABLISH
    sql = """SELECT alpha
FROM people
GROUP BY
  category"""

    expected = """SELECT alpha
FROM people
GROUP BY category"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == expected


def test_rewrite_single_item_clauses_ReturnsObj_Scenario4_MovesSingleOrderByColumnOntoOrderByLine() -> (
    None
):
    # ESTABLISH
    sql = """SELECT alpha
FROM people
ORDER BY
  created_at"""

    expected = """SELECT alpha
FROM people
ORDER BY created_at"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == expected


def test_rewrite_single_item_clauses_ReturnsObj_Scenario5_MovesSingleHavingConditionOntoHavingLine() -> (
    None
):
    # ESTABLISH
    sql = """SELECT
  category,
  COUNT(*)
FROM people
GROUP BY
  category
HAVING
  COUNT(*) > 10"""

    expected = """SELECT
  category,
  COUNT(*)
FROM people
GROUP BY category
HAVING COUNT(*) > 10"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == expected


def test_rewrite_single_item_clauses_ReturnsObj_Scenario6_DoesNotChangeMultiColumnSelect() -> (
    None
):
    # ESTABLISH
    sql = """SELECT
  alpha,
  beta
FROM people"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == sql


def test_rewrite_single_item_clauses_ReturnsObj_Scenario7_DoesNotChangeMultiColumnGroupBy() -> (
    None
):
    # ESTABLISH
    sql = """SELECT alpha
FROM people
GROUP BY
  category,
  location"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == sql


def test_rewrite_single_item_clauses_ReturnsObj_Scenario8_DoesNotChangeIndentedNestedExpression() -> (
    None
):
    # ESTABLISH
    sql = """SELECT
  CASE
    WHEN active THEN 1
  END
FROM people"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    expected_sql = """SELECT CASE
    WHEN active THEN 1
  END
FROM people"""
    assert result == expected_sql


def test_rewrite_single_item_clauses_ReturnsObj_Scenario9_HandlesMultipleSingleItemClauses() -> (
    None
):
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people
WHERE
  active = true
GROUP BY
  category
ORDER BY
  created_at"""

    expected = """SELECT alpha
FROM people
WHERE active = true
GROUP BY category
ORDER BY created_at"""

    # WHEN
    result = _rewrite_single_item_clauses(sql)

    # THEN
    assert result == expected


def test_rewrite_single_item_clauses_ReturnsObj_Scenario10_IsIdempotent() -> None:
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people
WHERE
  active = true"""

    # WHEN
    formatted = _rewrite_single_item_clauses(sql)
    reformatted = _rewrite_single_item_clauses(formatted)

    # THEN
    assert reformatted == formatted


def test_rewrite_select_leading_commas_ReturnsObj_Scenario1_ConvertsSelectListToLeadingCommas():
    # ESTABLISH
    sql = """SELECT
  alpha_extralong,
  beta_extralong,
  COUNT(*)
FROM people"""

    expected = """SELECT
  alpha_extralong
, beta_extralong
, COUNT(*)
FROM people"""

    # WHEN
    result = _rewrite_select_leading_commas(sql)

    # THEN
    assert result == expected


def test_rewrite_select_leading_commas_ReturnsObj_Scenario2_DoesNotChangeSingleSelectColumn():
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people"""

    # WHEN
    result = _rewrite_select_leading_commas(sql)

    # THEN
    assert result == sql


def test_rewrite_select_leading_commas_ReturnsObj_Scenario3_DoesNotModifyFromClause():
    # ESTABLISH
    sql = """SELECT
  alpha,
  beta
FROM
  people,
  locations"""

    expected = """SELECT
  alpha
, beta
FROM
  people,
  locations"""

    # WHEN
    result = _rewrite_select_leading_commas(sql)

    # THEN
    assert result == expected


def test_rewrite_select_leading_commas_ReturnsObj_Scenario4_StopsRewritingAfterWhereClause():
    # ESTABLISH
    sql = """SELECT
  alpha,
  beta
FROM people
WHERE
  alpha,
  beta"""

    expected = """SELECT
  alpha
, beta
FROM people
WHERE
  alpha,
  beta"""

    # WHEN
    result = _rewrite_select_leading_commas(sql)

    # THEN
    assert result == expected


@pytest_mark.parametrize(
    "clause",
    [
        "FROM people",
        "WHERE alpha = 1",
        "GROUP BY alpha",
        "ORDER BY alpha",
        "HAVING COUNT(*) > 1",
        "LIMIT 10",
        "QUALIFY alpha > 1",
    ],
)
def test_rewrite_select_leading_commas_ReturnsObj_Scenario5_StopsAtFollowingSqlClauses(
    clause: str,
):
    # ESTABLISH
    sql = f"""SELECT
  alpha,
  beta
{clause}"""

    # WHEN
    result = _rewrite_select_leading_commas(sql)

    # THEN
    assert f"{clause}" in result


def test_rewrite_group_by_leading_commas_ReturnsObj_Scenario1_ConvertsGroupByListToLeadingCommas():
    # ESTABLISH
    sql = """SELECT
  alpha,
  beta
FROM people
GROUP BY
  alpha,
  beta"""

    expected = """SELECT
  alpha,
  beta
FROM people
GROUP BY
  alpha
, beta"""

    # WHEN
    result = _rewrite_group_by_leading_commas(sql)

    # THEN
    assert result == expected


def test_rewrite_group_by_leading_commas_ReturnsObj_Scenario2_DoesNotChangeSingleGroupByColumn():
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people
GROUP BY
  alpha"""

    # WHEN
    result = _rewrite_group_by_leading_commas(sql)

    # THEN
    assert result == sql


def test_rewrite_group_by_leading_commas_ReturnsObj_Scenario3_DoesNotModifySelectClause():
    # ESTABLISH
    sql = """SELECT
  alpha,
  beta
FROM people
GROUP BY
  alpha,
  beta"""

    expected = """SELECT
  alpha,
  beta
FROM people
GROUP BY
  alpha
, beta"""

    # WHEN
    result = _rewrite_group_by_leading_commas(sql)

    # THEN
    assert result == expected


def test_rewrite_group_by_leading_commas_ReturnsObj_Scenario4_StopsRewritingAfterOrderByClause():
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people
GROUP BY
  alpha,
  beta
ORDER BY
  alpha,
  beta"""

    expected = """SELECT
  alpha
FROM people
GROUP BY
  alpha
, beta
ORDER BY
  alpha,
  beta"""

    # WHEN
    result = _rewrite_group_by_leading_commas(sql)

    # THEN
    assert result == expected


def test_rewrite_group_by_leading_commas_ReturnsObj_Scenario5_IsIdempotent():
    # ESTABLISH
    sql = """SELECT
  alpha
FROM people
GROUP BY
  alpha,
  beta"""

    # WHEN
    formatted = _rewrite_group_by_leading_commas(sql)
    reformatted = _rewrite_group_by_leading_commas(formatted)

    # THEN
    assert reformatted == formatted


def test_format_sql_ReturnsObj_Scenario0_FormatsSimpleSelect():
    # ESTABLISH
    sql = "select a,b from people"
    expected = """SELECT a, b FROM people"""
    # WHEN / THEN
    assert format_sql(sql) == expected


def test_format_sql_ReturnsObj_Scenario1_FormatsWhereClause():
    sql = "select * from people where age > 18"

    expected = """SELECT * FROM people WHERE age > 18"""
    # WHEN / THEN
    assert format_sql(sql) == expected


def test_format_sql_ReturnsObj_Scenario2_FormatsGroupByAndOrderBy():
    sql = (
        "select alpha_extralong,beta_extralong,count(*) from people "
        "group by alpha_extralong,beta_extralong "
        "order by count(*) desc, alpha_extralong, beta_extralong desc"
    )
    expected = """SELECT
  alpha_extralong
, beta_extralong
, COUNT(*)
FROM people
GROUP BY
  alpha_extralong
, beta_extralong
ORDER BY
  COUNT(*) DESC
, alpha_extralong
, beta_extralong DESC"""

    # WHEN / THEN
    assert format_sql(sql) == expected


def test_format_sql_ReturnsObj_Scenario3_ReturnsOriginalSql_WhenParseFails():
    # ESTABLISH
    sql = "SELECT FROM"

    # WHEN / THEN
    assert format_sql(sql) == sql


@pytest_mark.parametrize(
    "dialect",
    ["sqlite", "postgres", "duckdb"],
)
def test_format_sql_ReturnsObj_Scenario4_SupportsMultipleDialects(dialect: str):
    # ESTABLISH
    sql = "select a,b from people"
    # WHEN
    formatted = format_sql(sql, dialect=dialect)
    # THEN
    assert formatted.startswith("SELECT")
    assert "FROM people" in formatted


def test_format_sql_ReturnsObj_Scenario5_IsIdempotent():
    # ESTABLISH
    sql = "select a,b from people where age>18"
    # WHEN
    formatted = format_sql(sql)
    # THEN
    assert format_sql(formatted) == formatted


def test_format_sql_ReturnsObj_Scenario7_IsIdempotent_WhenAlwaysOneLineIsTrue():
    # ESTABLISH
    sql = """
select alpha_extralong,beta_extralong,count(*) 
from people 
group by alpha_extralong,beta_extralong 
order by count(*) desc"""

    # WHEN
    formatted = format_sql(sql, always_one_line=True)
    reformatted = format_sql(formatted, always_one_line=True)

    # THEN
    assert reformatted == formatted


def test_format_sql_ReturnsObj_Scenario8_FormatsCteSelectStatement():
    # ESTABLISH
    sql = """
WITH my_cte AS (
SELECT alpha_longcolumn,beta_longcolumn FROM people_longtablename WHERE age>18
)
SELECT *
FROM my_cte
"""

    expected = """WITH my_cte AS (
  SELECT
    alpha_longcolumn
,   beta_longcolumn
  FROM people_longtablename
  WHERE
    age > 18
)
SELECT *
FROM my_cte"""

    # WHEN
    result = format_sql(sql)

    # THEN
    assert result == expected


def test_format_sql_ReturnsObj_Scenario9_IndentsMultipleCtes():
    # ESTABLISH
    sql = """
WITH first_cte AS (SELECT alpha FROM people),
second_cte AS (SELECT beta FROM locations)
SELECT *
FROM first_cte
"""

    expected = """WITH first_cte AS ( SELECT alpha FROM people ), second_cte AS ( SELECT beta FROM locations ) SELECT * FROM first_cte"""

    # WHEN
    result = format_sql(sql)

    # THEN
    assert result == expected


def test_format_sql_ReturnsObj_Scenario10_FormatsNestedCteWhereClause():
    # ESTABLISH
    sql = """
WITH adults AS (
SELECT name_longcolumnname,age_longcolumnname FROM people WHERE age_longcolumnname>=18
)
SELECT name_longcolumnname FROM adults
"""

    expected = """WITH adults AS (
  SELECT
    name_longcolumnname
,   age_longcolumnname
  FROM people
  WHERE
    age_longcolumnname >= 18
)
SELECT name_longcolumnname
FROM adults"""

    # WHEN
    result = format_sql(sql, max_line_length=40)

    # THEN
    print(result)
    assert result == expected


def test_format_sql_ReturnsObj_Scenario11_PreservesCteIndentation_WhenAlreadyFormatted() -> (
    None
):
    # ESTABLISH
    sql = """WITH adults AS ( SELECT name, age FROM people ) SELECT name FROM adults"""

    # WHEN
    result = format_sql(sql)

    # THEN
    print(result)
    assert result == sql


def test_format_sql_ReturnsObj_Scenario12_IsIdempotent_WithCte():
    # ESTABLISH
    sql = """
WITH adults AS (
SELECT name,age FROM people WHERE age>=18
)
SELECT name FROM adults
"""

    # WHEN
    formatted = format_sql(sql)
    reformatted = format_sql(formatted)

    # THEN
    assert reformatted == formatted
