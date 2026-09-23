# ch23_idea_src — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 23 — `ch23_idea_src`**
**"Idea Source — the first ETL stage: reading raw Excel idea sheets, running fission transforms, and writing validated brick DataFrames"**

---

## 2. Prompt Used to Build This

From `ch23_ref.json`:
> "Defines the 'Idea Src' process. Where valid 'Idea' data is sparked and moved to Bricks."

Ontology note:
> "Source Ideas are validated some and then converted to Bricks."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `delete_dir`, `set_dir` — idea output directories are wiped and recreated on each run.
- **ch05_rope**: `default_knot_if_None` — used in `fission_add_ancestor_rope_rows` to parse rope paths and infer missing ancestor plan rows.
- **ch20_brick**: `create_brick_df_from_file`, `save_sheet`, `_sort_dataframe` — bricks are read from and written to Excel via ch20 tooling.
- **ch22_etl_config**: `get_etl_stage_types_config_dict` — used to determine valid stage type names during idea processing.
- **ch99_glossary**: `get_keg_elements_sort_order` — column sort order is enforced via the master glossary.

`ch23_semantic_types.py` re-exports through ch20 with no additions.

---

## 4. Summary of What This Chapter Does

`ch23_idea_src` is the **entry point of the ETL pipeline** — where raw human-authored Excel data ("ideas") is first read, lightly transformed, and written out as structured brick DataFrames ready for validation in later chapters.

**`fission_step.py`** — data transformation functions applied to raw idea DataFrames before they become bricks. Each function is a pure DataFrame → DataFrame transform:

- `fission_add_ancestor_rope_rows(df)` — inspects all `plan_rope` values in the DataFrame; for any rope that references an ancestor path not already present as a row, it inserts synthetic ancestor rows (with `pledge=0`, `poynt=None`). This ensures the plan tree is complete before it reaches the person object.
- `fission_set_pledge_to_one(df)` — sets all `pledge` values to 1 (marking all rows as active pledges).
- `fission_set_plan_rope_from_health_label(df)` — constructs `plan_rope` values by combining `moment_rope` and `health_label` columns, with strict null validation raising `ValueError` on missing values.
- `fission_set_moment_rope_from_moment_label(df)` — constructs `moment_rope` from a `moment_label` column.
- `run_fission_steps(df, fission_config)` — dispatches the configured sequence of fission steps for a given brick type, as specified in `idea_config.json`.

**`idea2brick.py`** — the main orchestration layer:

- `get_spark_faces_from_df(df)` / `get_spark_faces_from_files(directory)` — extract the set of distinct `spark_face` values present in idea files, used to validate provenance before loading.
- `get_max_spark_num_from_files(directory)` — finds the highest `spark_num` across all idea files, used to sequence the next ingestion spark.
- The main pipeline function (not fully read) reads each Excel idea file, applies fission steps per sheet, validates column presence against the brick schema, and writes valid rows to brick-format CSV/Excel outputs.

**`idea_config.json`** defines per-brick-type fission step sequences — which transforms to apply and in which order when converting a given idea sheet type to its corresponding brick format.

The "idea → brick" boundary is keg's human-computer interface: ideas are loosely structured, human-friendly spreadsheets; bricks are precisely schema-validated tabular records. Ch23 bridges the two.
