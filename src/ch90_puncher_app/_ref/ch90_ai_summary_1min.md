# ch90_puncher_app — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 50 — `ch90_puncher_app`**
**"Puncher App — a tkinter desktop GUI that wraps the full ETL pipeline, letting non-developers run keg from an Excel-file interface"**

---

## 2. Prompt Used to Build This

From `ch90_ref.json`:
> "Simple ETL app to create a world database from excel files."

Ontology note:
> "The entry point for most excel savvy users."

---

## 3. Summary of Previous Relevant Chapters

- **ch08_person_logic**: `personunit_shop` — used in `puncher_tool.py` to construct example `PersonUnit`s for the bundled starter idea files.
- **ch14_time**: `get_creg_config`, `get_five_config`, `epochunit_shop` — the "El Paso" and "TeamFive" example templates use real epoch configurations.
- **ch15_moment**: `momentunit_shop` — moment objects are built for example templates.
- **ch21_brick**: `csv_dict_to_excel`, `prettify_excel_file`, `remove_empty_sheets`, `prettify_excel_files` — all Excel output formatting is delegated to ch21.
- **ch23_idea_src**: `add_momentunits_to_idea_csv_strs`, `add_personunit_to_idea_csv_strs`, `create_init_idea_csv_strs` — example idea files are generated using the same CSV machinery as the ETL source layer.
- **ch30_idea_dst**: `create_lego0002_file` — person-level idea export is triggered from the GUI.
- **ch32_world**: `worlddir_shop`, `create_today_punchs` — the entire ETL pipeline is invoked via ch32's `WorldDir` entry point.

New semantic type: none. `ch90_semantic_types.py` re-exports through ch22.

---

## 4. Summary of What This Chapter Does

`ch90_puncher_app` is the **desktop application layer** of keg — the product that end users interact with directly.

**`puncher_tool.py`** contains three categories of logic:

*App settings and defaults:*
- `ETLAppSettings` — a dataclass holding all UI theming values (dark background `#1a1a1f`, accent yellow `#e8c547`, monospace fonts, etc.) with platform-specific font selection (Courier New on Windows, Menlo on macOS/Linux).
- `get_app_default_dir()` — returns `C:/keg/worlds` on Windows, `~/keg/worlds` on macOS/Linux.
- `get_app_default_dirs()` — builds the full `WorldDir` path layout for the default world (`hope1`).
- `get_app_default_me_personname()` / `get_app_default_you_personname()` — returns `"Emmanuel"` and `"Steve"` as starter person names, a deliberate reference to Levinas.

*Starter idea file generators:*
Eight named example generators build `PersonUnit`s and `MomentUnit`s programmatically and serialize them to idea-format Excel files, providing ready-made starting points:
- `create_simple_1m2p2pledges_idea_file` — 1 moment, 2 persons, 2 pledges.
- `create_simple_1m2p5pledges_idea_file` — 1 moment, 2 persons, 5 pledges (household tasks with baking soda — a recurring example throughout the codebase).
- `create_simple_2m2p5pledges_idea_file` — 2 moments (home + sport/dance), 2 persons.
- `create_emmanuel_lovemaking_idea_file` — 1 moment called "loving moment", 2 persons.
- `create_five_time_config_file` — a moment with the "Five" epoch (a custom 5-unit time system).
- `create_elpaso_time_config_file` — a moment with the standard Gregorian epoch, set in El Paso.
- Several `pass`-bodied stubs (`create_emmanuel_idea_file`, `create_example_moment_ledger_file`, `create_example_moment_budget_file`, `create_monopoly_idea_file`) reserved for future examples.

*Utility:*
- `fill_spark_face_in_directory(directory, face_name)` — fills empty `spark_face` cells in all Excel files in a directory with the provided face name. Used before running the pipeline when a user has authored idea sheets without attributing them to a face.
- `get_option_table_options()` — returns a dict mapping human-understandable option names to their generator functions, used to populate the GUI's dropdown/table of example actions.

**`puncher_app.py`** — the tkinter GUI:
- A dark-themed desktop window with labeled entry fields for `world_name`, `worlds_dir`, `me_name`, `you_name`, and `output_dir`.
- A scrollable option table listing the example generator functions from `get_option_table_options`.
- A "Run ETL" button that calls `create_today_punchs` (ch32) — the end-to-end pipeline from ideas to Google Calendar day punches — with a live log output pane showing stdout.
- A "Create Person Ideas" button that calls `create_lego0002_file` (ch30) to produce a person-scoped idea Excel for the named person.
- Settings are persisted to a local JSON config file between sessions.
