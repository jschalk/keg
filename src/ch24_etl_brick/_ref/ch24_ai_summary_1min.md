# ch24_etl_brick — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 24 — `ch24_etl_brick`**
**"ETL Brick — the multi-stage SQLite pipeline that validates brick data from raw through aggregated, validated, and sound-ready tables"**

---

## 2. Prompt Used to Build This

From `ch24_ref.json`:
> "Defines the 'Etl Bricks' process. Where valid 'Brick' data is translated into clean 'Sound' data."

Ontology note:
> "Bricks have data type validations and then are turned into Sound data."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `create_path` for file path construction.
- **ch19_db_tool**: `create_insert_into_clause_str`, `create_select_query`, `create_table_from_columns`, `create_type_reference_insert_sqlstr`, `db_table_exists`, `delete_all_duplicate_rows`, `get_create_table_sqlstr`, `get_db_tables`, `get_grouping_with_all_values_equal_sql_query`, `get_nonconvertible_columns`, `get_table_columns` — ch24 is the primary consumer of ch19's full SQL utility library.
- **ch20_brick**: `get_brick_format_filename`, `get_brick_sqlite_types`, `get_brick_types`, `get_brickref_from_file`, `get_brickref_obj`, `create_brick_df_from_file`, `create_brick_sorted_table`, `get_default_sorted_list` — all brick schema operations.
- **ch22_etl_config**: `BrickFileRef`, `get_all_brickfilerefs`, `create_prime_tablename`, `create_sound_and_heard_tables`, `etl_sqlstr` — stage naming and table creation helper tools.

`ch24_semantic_types.py` adds `SheetName` from ch20 to the full accumulated type chain.

---

## 4. Summary of What This Chapter Does

`ch24_etl_brick` executes the **four-stage brick validation pipeline** entirely within SQLite, transforming raw Excel brick data into clean, validated "sound" tables ready for person/moment reconstruction.

**Stage 1 — `etl_brick_dfs_to_brick_raw_tables(cursor, bricks_src_dir)`**
Discovers all brick Excel files in the source directory via `get_all_brickfilerefs`, reads each sheet into a DataFrame, sorts columns to the canonical order, prepends `file_dir`/`filename`/`sheet_name` provenance columns, creates a `{brick_type}_b_raw` SQLite table, and inserts each row. On insertion, `get_nonconvertible_columns` checks every cell against the expected SQLite type — any row with type errors has the offending columns nulled and an `error_message` written. Duplicate rows are deleted at the end.

**Stage 2 — `etl_brick_raw_tables_to_brick_agg_tables(conn)`**
For each `_b_raw` table, produces a `{brick_type}_b_agg` table. Uses `get_grouping_with_all_values_equal_sql_query` (from ch19) to GROUP BY the brick's key columns and filter to only rows where all value columns are consistent across duplicates — i.e. rows where the same key has conflicting values are excluded. Only rows with no `error_message` from stage 1 are considered. This is the **deduplication and consistency check** stage.

**Stage 3 — Spark validation (`etl_brick_agg_tables_to_sparks_b_agg_table` + `etl_sparks_b_agg_table_to_sparks_b_vld_table`)**
Aggregates all `spark_num`/`spark_face` pairs from every `_b_agg` table into a `sparks_b_agg` table. Flags any `spark_num` that maps to more than one `spark_face` as invalid (a spark number must belong to exactly one face). Valid sparks are written to `sparks_b_vld`. This enforces the provenance rule: a single spark event cannot be attributed to two different faces.

**Stage 4 — `etl_brick_agg_tables_to_brick_vld_tables(conn)`**
Produces `{brick_type}_b_vld` by JOINing the `_b_agg` table against `sparks_b_vld` — only rows with validated `spark_num` pass through. This is the final validated brick layer.

**Stage 5 — `etl_brick_vld_tables_to_sound_raw_tables(cursor)`**
Maps validated brick rows into "sound" dimension tables (`{ABBV7}_s_raw_put` / `{ABBV7}_s_raw_del`) by intersecting the brick's columns with the focus sound table's columns and inserting the common fields. The `brick_type` column is prepended to each inserted row for traceability. This produces the `s_raw` tables that downstream chapters will aggregate into `s_agg`, validate into `s_vld`, and ultimately use to reconstruct `PersonUnit` and `MomentUnit` objects.

The table naming convention throughout: `{brick_type}_b_{stage}` for brick-level tables, `{ABBV7}_s_{stage}_{crud}` for sound-level tables.
