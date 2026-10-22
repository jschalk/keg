# ch32_world — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 32 — `ch32_world`**
**"WorldDir — the top-level orchestrator: a single entry point that runs the complete ETL pipeline from idea sheets to lego output and KPIs"**

---

## 2. Prompt Used to Build This

From `ch32_ref.json`:
> "WorldDirs create and admin MomentUnits."

Ontology note:
> "WorldUnits can hold multiple disjoint MomentUnits, because every moment is independent."

---

## 3. Summary of Previous Relevant Chapters

Ch32 imports from every ETL chapter (ch23–ch31) simultaneously — it is the conductor:

- **ch20_brick**: `export_db_to_excel` — full database export to Excel.
- **ch22_etl_config**: `reorder_etl_db_sheets`, path helpers.
- **ch23_idea_src**: `ideas_sheets_to_brick_sheets` — idea → brick conversion.
- **ch24_etl_brick**: All six brick ETL stage functions.
- **ch25_sound**: All four sound ETL stage functions.
- **ch26_heard**: All seven heard ETL stage functions.
- **ch27_lego**: All eleven lego ETL stage functions.
- **ch30_idea_dst**: `create_lego0001_file` — world-level idea export.
- **ch31_kpi**: `create_calendar_markdown_files`, `populate_kpi_bundle`, `lego_to_person_gcal_day_punchs`, `copy_person_day_punches_to_dst_dir`, `get_day_punchs_persons`.

New semantic type: `WorldName` (a `str`) — identifies a world, the top-level container for one or more disjoint `MomentUnit`s.

---

## 4. Summary of What This Chapter Does

`ch32_world` defines `WorldDir` and its generation function `worlddir_shop` — the user-facing entry point for the entire keg system.

**`WorldDir`** is a dataclass holding the directory layout for one world:
- `world_name` / `worlds_dir` — the name and parent directory of this world.
- `world_dir` — computed as `worlds_dir/world_name`.
- `db_path` — the SQLite database at `world_dir/world.db`.
- `moment_mstr_dir` — the moment master directory at `world_dir/moment_mstr`.
- `bricks_src_dir` — where brick Excel files are staged.
- `ideas_src_dir` — where human-authored idea Excel files are placed.
- `output_dir` — where output Excel files and CSVs are written.

**`brick_sheets_to_lego_with_cursor(cursor, bricks_src_dir, moment_mstr_dir)`** — the complete ordered ETL pipeline as a single function. Called with an open SQLite cursor, it executes all ~20 ETL stage functions in sequence:
1. `etl_brick_dfs_to_brick_raw_tables` through `etl_brick_vld_tables_to_sound_raw_tables` (ch24 — brick validation).
2. `etl_sound_raw_tables_to_sound_agg_tables` through `etl_sound_vld_tables_to_heard_raw_tables` (ch25 — sound/translation).
3. `etl_heard_raw_tables_to_heard_agg_tables` through `etl_heard_vld_to_lego_spark_person_csvs` (ch26 — heard/reconstruction).
4. `etl_lego_spark_person_csvs_to_lesson_json` through `calc_moment_bud_contact_mandate_net_ledgers` (ch27 — lego/listening).
5. `etl_mind_job_jsons_to_job_tables` + `etl_moment_json_contact_nets_to_moment_tranbook_nets_table` (ch27 — DB population).
6. `populate_kpi_bundle` + `create_last_run_metrics_json` (ch31/ch27 — analytics).

**`brick_sheets_to_lego_mstr(worlddir)`** — wraps the above in a `sqlite3_connect` context manager, commits, and optionally exports the full database to a formatted Excel file via `save_and_reformat_db_export`.

**`idea_sheets_to_lego_mstr(worlddir)`** — the end-to-end user-facing pipeline:
1. Reads the current `max_b_agg_spark_num` from the existing database (to avoid re-processing already-ingested sparks).
2. Calls `ideas_sheets_to_brick_sheets` (ch23) to convert idea sheets to brick sheets.
3. Calls `brick_sheets_to_lego_mstr`.

**`idea_sheets_to_gcal_day_punchs(worlddir, person_names, day)`** — runs `idea_sheets_to_lego_mstr` then generates Google Calendar day-punch files for each named person for the given day.

**`create_today_punchs`** — convenience wrapper that calls `idea_sheets_to_gcal_day_punchs` with `datetime.now()`.

`WorldDir` is what a user or operator instantiates to run keg. All other chapters are internal machinery; this is the interface.
