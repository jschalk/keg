# ch22_etl_config — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 22 — `ch22_etl_config`**
**"ETL Configuration — dimension abbreviations, stage-type ordering, SQL generation, and Excel brick collection for the full data pipeline"**

---

## 2. Prompt Used to Build This

From `ch22_ref.json`:
> "All the tools used by WorldDirs to create MomentUnits."

Ontology note:
> "Defines the tools that move data through pipelines."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `create_path`, `open_json` — config files are loaded via file toolbox.
- **ch09_person_atom**: `get_delete_key_name` — used when constructing DELETE-type SQL stage queries to identify the correct key column.
- **ch16_nabu**: `get_context_nabuable_args`, `set_nabuable_otx_inx_args` — ETL config expands nabuable columns into `_otx`/`_inx` pairs in SQL table definitions.
- **ch17_translate**: `set_translateable_otx_inx_args` — same expansion for translateable string columns.
- **ch19_db_tool**: `get_create_table_sqlstr` — used to generate CREATE TABLE statements for each pipeline stage.
- **ch20_brick**: `get_brick_config_dict`, `get_brick_sqlite_types`, `get_default_sorted_list`, `get_brick_types`, `get_quick_bricks_column_ref` — all brick schema information flows through ch22.

---

## 4. Summary of What This Chapter Does

`ch22_etl_config` is the configuration and orchestration backbone of the ETL pipeline — it defines the stage ordering, dimension abbreviations, SQL generation utilities, and Excel file collection tools that the actual ETL execution chapters consume.

**`etl_config.py`** — the core configuration module:

- `ALL_DIMEN_ABBV7` and `ALL_DIMEN_ABBV2` — two abbreviation sets for all 23 dimension types (e.g. `"moment_ceckbook"` → `"MMTCECK"` / `"MP"`). These abbreviated names are used as table name prefixes throughout the SQLite ETL database.
- `get_dimen_abbv7(dimen)` and `get_dimen_abbv2(dimen)` — dispatch functions mapping full dimension names to abbreviations.
- `get_etl_stage_types_config_dict()` — loads `etl_stage_types_config.json`, which defines the ordered sequence of ETL stages (e.g. `b_raw` → `b_agg` → `b_vld` → `s_raw` → `s_agg` → `s_vld` → `h_raw` → ...). Each stage has a `stage_type_order` integer determining its position in the pipeline.
- `get_stage_create_table_sqlstr(dimen, stage_type)` — generates the `CREATE TABLE` SQL for a specific dimension at a specific pipeline stage, incorporating `_otx`/`_inx` column expansions for translated and nabu fields.

**`brick_collector.py`** — Excel discovery and sheet reordering:

- `BrickFileRef` — a dataclass identifying a specific brick sheet within an Excel file: `file_dir`, `filename`, `sheet_name`, `brick_type`.
- `get_all_brickfilerefs(dir)` — scans a directory for `.xlsx` files, finds all sheets with names that contain a known `brick_type`, validates that the sheet has the required columns, and returns a list of `BrickFileRef` objects ready for ETL loading.
- `reorder_etl_db_sheets(filepath)` — reorders sheets in an Excel output file to match the canonical stage-type ordering defined in `etl_stage_types_config.json`.

**`etl_sqlstr.py`** — SQL string generation for sound and heard tables:

- `create_prime_tablename(dimen, stage, crud)` — constructs table names like `"PRNPLAN_s_raw_put"` or `"MMTBUDD_s_raw"` following the `ABBV7_stage_crud` naming convention.
- `create_sound_and_heard_tables(cursor)` — iterates all dimensions and all stage types, generating and executing `CREATE TABLE IF NOT EXISTS` statements for every table in the full pipeline.

**`etl_csv.py`** provides CSV export utilities for pipeline stage tables.

The chapter has no new semantic types of its own — `ch22_semantic_types.py` re-exports through ch20. Ch22's role is purely infrastructural: it defines the names, shapes, and ordering of every table in the ETL database before any data flows through it.
