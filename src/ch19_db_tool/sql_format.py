from sqlglot import parse_one
from sqlglot.errors import ParseError
from re import compile as re_compile

_SINGLE_LINE_CLAUSES = {
    "SELECT",
    "WHERE",
    "GROUP BY",
    "ORDER BY",
    "HAVING",
}


def _rewrite_single_item_clauses(sql: str) -> str:
    lines = sql.splitlines()
    result = []

    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip().upper()

        if stripped in _SINGLE_LINE_CLAUSES and i + 1 < len(lines):
            next_line = lines[i + 1]

            if (
                next_line.startswith("  ")
                and not next_line.startswith("    ")
                and "," not in next_line
            ):
                result.append(f"{line.strip()} {next_line.strip()}")
                i += 2
                continue

        result.append(line)
        i += 1

    return "\n".join(result)


_SQL_CLAUSES = {
    "FROM",
    "WHERE",
    "GROUP BY",
    "ORDER BY",
    "HAVING",
    "LIMIT",
    "QUALIFY",
    "UNION",
    "INTERSECT",
    "EXCEPT",
}


_CLAUSE_ITEM_RE = re_compile(r"^(?P<indent>\s{2})(?P<expr>.+?)(?P<comma>,?)$")


def _rewrite_clause_leading_commas(
    sql: str,
    start_clause: str,
) -> str:
    lines = sql.splitlines()
    out = []

    in_clause = False

    for line in lines:
        stripped = line.strip()

        upper = stripped.upper()

        if upper == start_clause.upper():
            in_clause = True
            out.append(line)
            continue

        if in_clause and any(
            upper.startswith(clause)
            for clause in _SQL_CLAUSES
            if clause != start_clause.upper()
        ):
            in_clause = False
            out.append(line)
            continue

        if in_clause:
            match = _CLAUSE_ITEM_RE.match(line)

            if match:
                expr = match.group("expr")

                if out[-1].strip().upper() == start_clause.upper():
                    out.append(f"  {expr}")
                else:
                    out.append(f", {expr}")

                continue

        out.append(line)

    return "\n".join(out)


def _rewrite_select_leading_commas(sql: str) -> str:
    return _rewrite_clause_leading_commas(sql, "SELECT")


def _rewrite_group_by_leading_commas(sql: str) -> str:
    return _rewrite_clause_leading_commas(sql, "GROUP BY")


def _rewrite_order_by_leading_commas(sql: str) -> str:
    return _rewrite_clause_leading_commas(sql, "ORDER BY")


def format_sql(
    sql: str,
    dialect: str = "sqlite",
    max_line_length: int = 120,
    always_one_line: bool = False,
) -> str:
    try:
        pretty = parse_one(sql, dialect=dialect).sql(pretty=True)
        one_line = " ".join(pretty.split())

        if always_one_line or len(one_line) <= max_line_length:
            return one_line
        else:
            pretty = _rewrite_single_item_clauses(pretty)
            pretty = _rewrite_select_leading_commas(pretty)
            pretty = _rewrite_group_by_leading_commas(pretty)
            pretty = _rewrite_order_by_leading_commas(pretty)

        return pretty

    except ParseError:
        return sql
