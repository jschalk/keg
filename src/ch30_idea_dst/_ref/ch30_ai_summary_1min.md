# ch30_idea_dst — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 30 — `ch30_idea_dst`**
**"Idea Destination — exporting the fully processed world state back to human-understandable Excel idea files for external audiences"**

---

## 2. Prompt Used to Build This

From `ch30_ref.json`:
> "Defines how ideas for outside audiences are created."

Ontology note:
> "Tools for creating ideax_dst files with for-audience translation."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `delete_column_from_csv_string`, `replace_csv_column_from_string` — used to strip or replace `spark_num`/`spark_face` columns before writing output files.
- **ch05_rope**: `create_rope`, `default_knot_if_None` — moment ropes are constructed when walking the moment directory tree.
- **ch10_person_lesson**: `create_moments_dir_path`, `lassounit_shop` — path navigation for the moment file system.
- **ch12_bud**: `open_person_file` — gut and job `PersonUnit` JSON files are loaded for export.
- **ch15_moment**: `open_moment_file` — `MomentUnit` objects are loaded for export.
- **ch20_brick**: `csv_dict_to_excel`, `prettify_excel_file`, `remove_empty_sheets` — the final output is an Excel file with one sheet per brick/idea type.
- **ch22_etl_config**: `create_moment_mstr_path`, `create_world_db_path`, `create_prime_tablename`, `create_sound_and_heard_tables` — path helpers and SQL table names for loading translation data.
- **ch23_idea_src**: `add_momentunit_to_idea_csv_strs`, `add_personunit_to_idea_csv_strs`, `create_init_idea_csv_strs` — the idea CSV structure from the source chapter is reused for the destination output.

New semantic type: none. `ch30_semantic_types.py` re-exports through ch22.

---

## 4. Summary of What This Chapter Does

Ch30 is the **output inverse of ch23** — where ch23 reads human-authored idea sheets and converts them into bricks for ingestion, ch30 takes the fully processed world state and writes it back out as idea-format Excel files for human consumption.

**`collect_full_world_idea_csv_strs(world_dir)`** — the main data-collection function:
1. Walks all moment directories, loads each `MomentUnit` via `open_moment_file`, and calls `add_momentunit_to_idea_csv_strs` to serialize moment-level fields (budget units, epoch config, ceckbook, offi_times) into the idea CSV string dict.
2. For each person within each moment, loads the **gut** `PersonUnit` (the person's own belief system, not the job) and calls `add_personunit_to_idea_csv_strs` to serialize their full plan tree, contacts, reasons, facts, etc.
3. Opens the world SQLite database, creates sound/heard tables if absent, then calls `add_jargon_rows_to_idea_csv_strs` to append validated translation mappings (from `trltitl_s_vld`, `trlname_s_vld`, `trllabe_s_vld`, `trlrope_s_vld` joined with `trlcore_s_vld`) into the four translation idea sheets (`ii00142`–`ii00145`).

**`create_lego0001_file(world_dir, output_dir, world_name)`** — produces the **world-level** output Excel:
- Calls `collect_full_world_idea_csv_strs`.
- Replaces the `spark_face` column value with `world_name` on every sheet (re-attributing all data to the world as author for the audience).
- Deletes the `spark_num` column (internal provenance not relevant to the audience).
- Writes the result as `lego0001.xlsx` and optionally prettifies it.

**`create_lego0002_file(world_dir, output_dir, person_name)`** — produces a **person-level** output Excel:
- Collects only the moments and **job** `PersonUnit`s (the post-listening state) for the specified person.
- Strips both `spark_face` and `spark_num` columns entirely.
- Writes as `{person_name}_ideas.xlsx`, removes empty sheets, and prettifies.

The distinction between `lego0001` (gut-based, world-attributed) and `lego0002` (job-based, person-scoped) reflects the gut/job duality established in ch11: the world sees raw belief systems; a person sees their listening-synthesized agenda.
