# ch27_lego — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 27 — `ch27_lego`**
**"Lego — the final ETL stage: assembling PersonAtoms from heard CSVs into LessonUnits, applying them cumulatively to produce gut files, running the listening pipeline, and loading job PersonUnits into the database"**

---

## 2. Prompt Used to Build This

From `ch27_ref.json`:
> "Defines the lego stage of data. Source of Job Persons, complete Moment data."

Ontology note:
> "The most static and clear of all etl stages. Everything has been calculated except for audience idea."

---

## 3. Summary of Previous Relevant Chapters

Ch27 is the final integration point of the entire ETL pipeline. It imports from more chapters than any other single file:

- **ch00_py**: File I/O, path, directory walking.
- **ch05_rope**: `create_rope` for moment rope construction.
- **ch08_person_logic**: `PersonUnit`, `personunit_shop` — the object being reconstructed.
- **ch09_person_atom**: `get_person_dimens`, `personatom_shop` — atoms are reconstructed from CSV rows.
- **ch10_person_lesson**: `get_minimal_persondelta`, `LassoUnit`, `lassounit_shop`, `LessonUnit`, `get_lessonunit_from_dict`, `lessonunit_shop`, path helpers — lessons are the vehicle for applying deltas.
- **ch11_person_listen**: `open_job_file` — job files are loaded for DB insertion.
- **ch12_bud**: Path helpers, `TranBook`, `collect_person_spark_dir_sets`, `get_persons_downhill_spark_nums`, `open_person_file`.
- **ch15_moment**: `create_moment_persons_cell_trees`, `set_cell_tree_cell_mandates`, `set_cell_trees_decrees`, `set_cell_trees_found_facts`, `create_bud_mandate_ledgers`, `open_moment_file`.
- **ch19_db_tool**: `delete_all_duplicate_rows`, `get_db_tables`.
- **ch20_brick**: `get_brick_sqlite_types` for type-aware CSV parsing.
- **ch22_etl_config**: Path helpers, `create_job_tables`, `create_prime_tablename`, `save_to_split_csvs`.
- **ch27_lego.lego_job2db**: `insert_job_obj` — inserts a fully evaluated job `PersonUnit` into all job-tracking SQLite tables.

---

## 4. Summary of What This Chapter Does

`ch27_lego` is where all ETL threads converge into running `PersonUnit` and `MomentUnit` objects.

**`etl_moment_ote1_agg_csvs_to_jsons`** — converts the `moment_ote1_agg` CSVs (from ch26) into JSON dicts mapping `person_name → bud_time → spark_num`, creating the lookup table that tells the system which spark to apply at each budget time.

**`etl_lego_spark_person_csvs_to_lesson_json`** — walks the `moments/{moment}/persons/{person}/sparks/{spark_num}/` directory tree (written by ch26) and for each spark directory, reads all `h_vld_put` and `h_vld_del` CSVs, reconstructs `PersonAtom`s row by row (skipping provenance columns `spark_face`, `spark_num`, `moment_rope`, `person_name`), assembles them into a `LessonUnit`'s `PersonDelta`, and saves the result as `spark_all_lesson.json`.

**`etl_lego_spark_lesson_json_to_spark_inherited_personunits`** — the cumulative application loop. For each person across all moments, it walks sparks in order. For each spark:
1. Loads the previous spark's `PersonUnit` from disk (or creates an empty one for spark 0).
2. Loads the current spark's `LessonUnit` from `spark_all_lesson.json`.
3. Calls `get_minimal_persondelta` to strip no-op atoms.
4. Applies the delta to the previous `PersonUnit` to produce the current one.
5. Saves the current `PersonUnit` as `personspark.json`.
6. Saves a minimal `expressed_lesson.json` (only the atoms that actually changed something).

This is the moment when the full atom-based version history from ch09/ch10 is replayed against real data.

**`etl_spark_inherited_personunits_to_mind_gut`** — identifies the max spark number for each person (the most recent state) and copies that `PersonUnit` JSON to the person's `gut` file — their current belief system.

**`add_lego_epoch_to_mind_guts`** — injects the shared epoch into all gut files via `MomentUnit.add_epoch_to_guts()`.

**`etl_mind_guts_to_mind_jobs`** — calls `MomentUnit.generate_all_jobs()` for each moment, running the full listening pipeline (ch11) across all persons to produce job files.

**`etl_mind_job_jsons_to_job_tables`** — loads each person's job `PersonUnit` and inserts it into the SQLite job tables via `lego_job2db.insert_job_obj`, making the final computed state queryable from SQL.

**`calc_moment_bud_contact_mandate_net_ledgers`** — orchestrates the full cell-tree pipeline from ch15: builds root cells from `ote1` data, creates cell trees, propagates found facts, computes decrees, sets mandates, and generates bud mandate ledgers — the fund-distribution calculation for each budget time point.

**`create_last_run_metrics_json`** — records the max `spark_num` seen across all `b_agg` tables, providing a aguamark for the next ETL run.

`lego_job2db.py` provides `insert_job_obj` which calls `thinkout()` on the job `PersonUnit` and inserts the resulting contacts, memberships, plans, reasons, facts, and fund metrics into dedicated `_job` SQLite tables — making the fully evaluated, post-listening state of every person queryable.
