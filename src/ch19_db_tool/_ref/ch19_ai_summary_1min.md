# ch19_db_tool — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 18 — `ch19_db_tool`**
**"Database Toolbox — SQLite helper utilities for creating tables, inserting CSVs, and querying keg data from relational storage"**

---

## 2. Prompt Used to Build This

From `ch19_ref.json`:
> "Create some standard tools for creating sqlite sql statements. Some are complicated."

Ontology note:
> "Beginning of a mapping from objects to relational databases."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `ch19_db_tool` is structurally parallel to ch00 — it is a pure utility chapter with no domain logic, just as ch00 provided Python/file toolboxes. The main difference is ch19 uses SQLite rather than the file system.
- All prior semantic types are re-exported through `ch19_semantic_types.py` (the full chain through ch14) — but ch19's own code imports only from Python's `sqlite3`, `csv`, `pandas`, `re`, and `dataclasses` standard/third-party libraries. It does not import from any prior keg chapter in `db_toolbox.py` itself.

This is a deliberate design: ch19 is a low-level database infrastructure chapter — like ch00, it intentionally avoids domain dependencies so it can be used freely by all higher chapters.

---

## 4. Summary of What This Chapter Does

`ch19_db_tool` provides two files of SQLite utility functions that later chapters use to persist and query keg data in relational databases.

**`db_toolbox.py`** — the main utility library:

- **Type conversion**: `sqlite_obj_str(x_obj, sqlite_datatype)` converts Python objects (including booleans, None) to properly quoted SQLite literal strings. `sqlite_to_python(query_value)` converts SQLite results back to Python values. These handle the type-mapping quirks between Python's type system and SQLite's loose typing.

- **Table introspection**: `get_db_tables(conn)` lists all tables in a database; `get_db_columns(conn)` returns column names and types; `get_table_columns(conn, tablename)` retrieves column names for a specific table. `db_table_exists(conn, tablename)` checks for table existence before operations.

- **Table creation**: `create_table_from_columns(conn, tablename, columns_list, column_types)` generates and executes a `CREATE TABLE` statement. `create_table_from_csv(csv_file_path, conn, table_name, column_types)` reads a CSV header and creates a matching table automatically.

- **Data insertion**: `insert_csv(csv_file_path, conn, table_name)` bulk-inserts CSV rows into a table, handling type coercion and NULL conversion. `create_table2table_agg_insert_query(...)` builds a complex aggregation INSERT query that copies and aggregates data from one table into another — used for producing summary/rollup tables.

- **Data quality**: `get_nonconvertible_columns(row_dict, col_types)` identifies cells that cannot be coerced to their expected type. `delete_all_duplicate_rows(conn, tablename, key_columns)` removes duplicate rows while keeping one copy. `create_select_inconsistency_query(conn, tablename, focus_columns, exclude_columns)` generates a GROUP BY/HAVING query that finds rows where non-key columns disagree across identical key groups — useful for detecting data inconsistencies in ledger tables.

- **Column utilities**: `get_sorted_cols_only_list(existing_columns, sorting_columns)` returns an intersection of columns in a specified order — used to produce consistently-ordered SELECT lists.

**`notebook_toolbox.py`** provides Jupyter-notebook-oriented utilities — helpers for displaying query results and database state in an interactive analysis context.

Ch19 is the "ch00 of persistence" — a deliberately dependency-free utility layer. It carries the full semantic type chain in its `_ref` file as preparation for the ETL chapters that will use both these database tools and the domain objects to build the full data pipeline.
