# ch26_heard — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 26 — `ch26_heard`**
**"Heard — applying otx→inx string translation and TimeNum conversion to produce fully resolved heard tables, then reconstructing MomentUnit JSON from them"**

---

## 2. Prompt Used to Build This

From `ch26_ref.json`:
> "Defines the 'Heard' process. Where valid 'Sound' data is aggregated into clean 'lego' data."

Ontology note:
> "Sounds are turned into trusted concepts, Nabu interpreted (time conversion included) and produces Moment and Person objects."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `set_in_nested_dict`, `get_level1_dirs`, `save_file`, `save_json` — moment JSON files are assembled from query results using nested dict helpers and persisted to disk.
- **ch05_rope**: `create_rope` — used when constructing `LassoUnit` objects to navigate moment directory paths.
- **ch10_person_lesson**: `create_moment_json_path`, `create_moments_dir_path`, `LassoUnit`, `lassounit_shop` — the moment file system layout is defined in ch10 path helpers.
- **ch12_bud**: `MomentRope` — scopes all heard table queries.
- **ch17_translate**: `get_translate_args_obj_types`, `translateable_obj_types` — drives which `h_raw` columns need `_inx` values populated via translation lookups.
- **ch19_db_tool**: `delete_all_duplicate_rows`, `get_row_count`, `get_table_columns` — SQL utilities.
- **ch22_etl_config**: `etl_sqlstr` functions — `create_update_heard_raw_empty_inx_col_sqlstr`, `create_update_heard_raw_existing_inx_col_sqlstr`, `get_insert_heard_agg_sqlstrs`, `get_insert_heard_vld_sqlstrs`, `update_heard_agg_timenum_columns`, `get_moment_heard_select1_sqlstrs`, `get_person_heard_vld_tablenames`, `save_to_split_csvs` — all SQL generation delegated to ch22.

---

## 4. Summary of What This Chapter Does

`ch26_heard` is the final ETL stage before data becomes usable `PersonUnit` and `MomentUnit` objects. It advances data through `h_raw → h_agg → h_vld` and then reconstructs structured files from the validated heard tables.

**`etl_heard_raw_tables_to_heard_agg_tables(cursor)`** — three steps:
1. `set_all_heard_raw_inx_columns` — for every `_otx`-suffixed column in every `h_raw` table, determines the translation type (`NameTerm`, `TitleTerm`, `LabelTerm`, or `RopeTerm`) from the ch17 translate-args registry. If the column's base type is translateable, runs an UPDATE query that JOINs against the validated `trl{type}_s_vld` table to fill in the `_inx` value. For rows where no translation mapping exists, goes back to copying the `_otx` value into `_inx` directly (pass-through for untranslated terms).
2. INSERT into `h_agg` tables from `h_raw`, deduplicating while excluding `_inx` columns from duplicate comparison.
3. `update_heard_agg_timenum_columns` — applies NabuTime conversion to all time-numeric columns (`bud_time`, `fact_lower`, `fact_upper`, `reason_lower`, `reason_upper`, `tran_time`, `offi_time`) in `h_agg` tables: reads the `_otx` value, applies the epoch-length modular offset from the validated nabu table, and writes the result to the `_inx` column. This is where ch16's numeric translation is finally executed against real data.

**`etl_heard_agg_tables_to_heard_vld_tables(cursor)`** — promotes `h_agg` rows to `h_vld` via pre-generated INSERT/SELECT queries, deduplicating.

**`get_moment_dict_from_heard_tables(cursor, moment_rope)`** — the reconstruction function. Runs a series of SELECT queries against the fully validated `h_vld` tables for a given `moment_rope` and assembles a nested Python dict representing the complete `MomentUnit` state: `momentunit` row for top-level attributes, `moment_ceckbook` rows for `TranUnit`s (nested `person_name → contact_name → tran_time → amount`), `moment_budunit` rows for `BudUnit`s, and epoch configuration rows (hours, months, weekdays, offi_times).

**`etl_heard_vld_tables_to_mind_moment_jsons(cursor, moment_mstr_dir)`** — iterates all `moment_rope`s from `momentunit_h_vld`, calls `get_moment_dict_from_heard_tables` for each, and writes the result as a `moment.json` file to the appropriate directory. The inline comment notes a known architectural tension: using rope-based file paths is idiomatic but problematic when `moment_rope` contains characters that don't translate to valid OS paths — a hash-based directory scheme is suggested as an alternative.

**`etl_heard_raw_tables_to_lego_moment_ote1_agg`** — builds the `moment_ote1_agg` table: a mapping of `(moment_rope, person_name, spark_num) → bud_time`, which tells later chapters which spark to apply at which budget time.

**`etl_heard_vld_to_lego_spark_person_csvs`** — splits validated `h_vld` person dimension tables into per-moment/per-person/per-spark CSV files on disk, organized as `moments/{moment}/persons/{person}/sparks/{spark_num}/{dimen_h_vld_put.csv}`. These CSVs are the raw material later chapters convert into `LessonUnit`s.
